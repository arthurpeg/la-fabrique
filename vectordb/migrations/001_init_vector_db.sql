-- ============================================================================
-- 001_init_vector_db.sql — la base vectorielle des papiers de recherche
--
-- DIMENSION DES VECTEURS : figée par le DDL. pgvector n'accepte pas de taille
-- dynamique, et il n'existe aucune façon honnête de contourner cela. Pour une
-- autre dimension, substituer AVANT de migrer :
--
--     sed -i 's/vector(1536)/vector(3072)/g' 001_init_vector_db.sql
--
-- Changer après chargement impose une migration de table complète.
--
-- Prose en français, identifiants en anglais — `CLAUDE.md` § Conventions.
-- ============================================================================

create extension if not exists vector;

-- ----------------------------------------------------------------------------
-- Listes CLOSES. Ajouter une valeur est un `alter type` explicite, jamais un
-- effet de bord. Une catégorie « other » qui gonfle est un signal à lire, pas
-- un fourre-tout à élargir en passant.
-- ----------------------------------------------------------------------------
create type section_type as enum (
    'intro', 'methodology', 'results', 'conclusion', 'other'
);

create type strategy_type as enum (
    'momentum', 'carry', 'mean_reversion', 'other'
);

-- ----------------------------------------------------------------------------
-- papers
-- ----------------------------------------------------------------------------
create table papers (
    id         uuid        primary key default gen_random_uuid(),
    title      text        not null check (length(trim(title)) > 0),
    authors    text[]      not null default '{}',
    year       int         check (year between 1800 and 2100),
    doi        text,
    pdf_url    text,
    abstract   text,
    added_at   timestamptz not null default now(),

    -- Titre normalisé, GÉNÉRÉ : c'est lui qui porte l'unicité quand le DOI
    -- manque. Le calculer côté client laisserait deux appelants diverger sur
    -- la même chaîne, et le doublon passerait.
    title_norm text generated always as (
                   trim(lower(regexp_replace(title, '[^a-zA-Z0-9]+', ' ', 'g')))
               ) stored,

    constraint papers_doi_key        unique (doi),
    constraint papers_title_norm_key unique (title_norm)
);

comment on constraint papers_doi_key on papers is
    'NULL autorisé et répétable : tous les papiers n''ont pas de DOI.';

-- ----------------------------------------------------------------------------
-- chunks
-- ----------------------------------------------------------------------------
create table chunks (
    id              uuid         primary key default gen_random_uuid(),
    paper_id        uuid         not null references papers(id) on delete cascade,
    content         text         not null check (length(content) > 0),
    section         section_type not null default 'other',
    page            int          check (page > 0),

    -- `position` est une fonction SQL (`position(x in y)`) : utilisable entre
    -- guillemets, mais chaque requête devrait l'écrire ainsi. `order` est
    -- réservé lui aussi. `ordinal` ne l'est pas.
    ordinal         int          not null check (ordinal >= 0),

    embedding       vector(1536),
    embedding_model text,

    tsv tsvector generated always as (to_tsvector('english', content)) stored,

    constraint chunks_paper_ordinal_key unique (paper_id, ordinal),

    -- Un vecteur sans son modèle est un nombre sans provenance : le jour où le
    -- modèle change, la colonne mélange des vecteurs incomparables SANS QUE
    -- RIEN NE LE DISE. Les deux vont ensemble ou ni l'un ni l'autre.
    constraint chunks_embedding_provenance check (
        (embedding is null) = (embedding_model is null)
    )
);

-- ----------------------------------------------------------------------------
-- strategies
-- ----------------------------------------------------------------------------
create table strategies (
    id              uuid          primary key default gen_random_uuid(),
    paper_id        uuid          not null references papers(id) on delete cascade,
    asset           text          not null check (length(trim(asset)) > 0),
    strategy_type   strategy_type not null default 'other',
    signals         text,
    period_start    date,
    period_end      date,
    sharpe_ratio    double precision,
    limitations     text,

    embedding       vector(1536),
    embedding_model text,

    constraint strategies_period_order check (
        period_start is null or period_end is null or period_start <= period_end
    ),
    constraint strategies_embedding_provenance check (
        (embedding is null) = (embedding_model is null)
    )
);

comment on column strategies.asset is
    'Texte libre, assumé : « oil », « Oil » et « CL » seront trois actifs
     distincts. Aucune jointure vers catalogue/catalogue.yaml.';

comment on column strategies.sharpe_ratio is
    'NULLABLE, et à laisser NULL quand le papier ne le donne pas. Une valeur
     plausible inventée devient indétectable en aval ; un NULL est bruyant.';

-- ----------------------------------------------------------------------------
-- Index
-- ----------------------------------------------------------------------------
create index chunks_embedding_hnsw on chunks
    using hnsw (embedding vector_cosine_ops) with (m = 16, ef_construction = 64);

create index strategies_embedding_hnsw on strategies
    using hnsw (embedding vector_cosine_ops) with (m = 16, ef_construction = 64);

create index chunks_tsv_gin on chunks using gin (tsv);

create index papers_year_idx           on papers     (year);
create index strategies_asset_idx      on strategies (asset);
create index strategies_type_idx       on strategies (strategy_type);
create index chunks_paper_id_idx       on chunks     (paper_id);
create index strategies_paper_id_idx   on strategies (paper_id);

-- ----------------------------------------------------------------------------
-- RLS — REFUS PAR DÉFAUT.
--
-- Activer RLS sans définir aucune politique interdit tout accès aux rôles
-- `anon` et `authenticated`. `service_role` et une connexion `psycopg` directe
-- passent outre par conception. Ça ferme la fuite dans le cas où une clé
-- publique traînerait, sans rien coûter au cas serveur.
--
-- Pour ouvrir la lecture à un rôle, écrire une politique explicite ici — et la
-- considérer comme une décision, pas comme un réglage.
-- ----------------------------------------------------------------------------
alter table papers     enable row level security;
alter table chunks     enable row level security;
alter table strategies enable row level security;

-- ============================================================================
-- Fonctions de recherche
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Vectorielle pure. `<=>` est la distance cosinus ; la similarité vaut 1-d.
-- ----------------------------------------------------------------------------
create or replace function vector_search(
    query_embedding vector(1536),
    match_count     int          default 10,
    year_min        int          default null,
    year_max        int          default null,
    section_filter  section_type default null
)
returns table (
    chunk_id   uuid,
    paper_id   uuid,
    title      text,
    content    text,
    section    section_type,
    page       int,
    similarity double precision
)
language sql stable
as $$
    select c.id, c.paper_id, p.title, c.content, c.section, c.page,
           1 - (c.embedding <=> query_embedding)
    from chunks c
    join papers p on p.id = c.paper_id
    where c.embedding is not null
      and (year_min       is null or p.year    >= year_min)
      and (year_max       is null or p.year    <= year_max)
      and (section_filter is null or c.section  = section_filter)
    order by c.embedding <=> query_embedding
    limit match_count;
$$;

-- ----------------------------------------------------------------------------
-- 2. Hybride, par Reciprocal Rank Fusion.
--
--        score = somme, sur chaque liste, de  1 / (k + rang)
--
-- RRF combine des RANGS, jamais des scores. Une distance cosinus et un
-- `ts_rank_cd` ne vivent pas sur la même échelle : les additionner donnerait un
-- nombre dont personne ne saurait dire ce qu'il mesure. Le rang, lui, est
-- comparable par construction.
--
-- `k` amortit le poids des premières places ; 60 est la valeur de l'article
-- d'origine (Cormack et al., 2009) et se change en connaissance de cause.
-- ----------------------------------------------------------------------------
create or replace function hybrid_search(
    query_text      text,
    query_embedding vector(1536),
    match_count     int          default 10,
    year_min        int          default null,
    year_max        int          default null,
    section_filter  section_type default null,
    rrf_k           int          default 60
)
returns table (
    chunk_id uuid,
    paper_id uuid,
    title    text,
    content  text,
    section  section_type,
    page     int,
    score    double precision
)
language sql stable
as $$
    with filtered as (
        select c.id, c.paper_id, c.content, c.section, c.page, c.embedding, c.tsv
        from chunks c
        join papers p on p.id = c.paper_id
        where (year_min       is null or p.year    >= year_min)
          and (year_max       is null or p.year    <= year_max)
          and (section_filter is null or c.section  = section_filter)
    ),
    full_text as (
        select id,
               row_number() over (
                   order by ts_rank_cd(tsv, websearch_to_tsquery('english', query_text)) desc,
                            id
               ) as rank
        from filtered
        where query_text is not null
          and tsv @@ websearch_to_tsquery('english', query_text)
        limit match_count * 4
    ),
    semantic as (
        select id,
               row_number() over (order by embedding <=> query_embedding, id) as rank
        from filtered
        where embedding is not null
        limit match_count * 4
    ),
    fused as (
        select coalesce(f.id, s.id) as id,
               coalesce(1.0 / (rrf_k + f.rank), 0.0)
             + coalesce(1.0 / (rrf_k + s.rank), 0.0) as score
        from full_text f
        full outer join semantic s on s.id = f.id
    )
    select fl.id, fl.paper_id, p.title, fl.content, fl.section, fl.page, fu.score
    from fused fu
    join filtered fl on fl.id = fu.id
    join papers   p  on p.id  = fl.paper_id
    order by fu.score desc, fl.id
    limit match_count;
$$;

-- ----------------------------------------------------------------------------
-- 3. Stratégies.
-- ----------------------------------------------------------------------------
create or replace function strategy_search(
    query_embedding vector(1536),
    match_count     int              default 10,
    asset_filter    text             default null,
    type_filter     strategy_type    default null,
    sharpe_min      double precision default null
)
returns table (
    strategy_id   uuid,
    paper_id      uuid,
    title         text,
    asset         text,
    strategy_type strategy_type,
    signals       text,
    sharpe_ratio  double precision,
    limitations   text,
    similarity    double precision
)
language sql stable
as $$
    select s.id, s.paper_id, p.title, s.asset, s.strategy_type,
           s.signals, s.sharpe_ratio, s.limitations,
           1 - (s.embedding <=> query_embedding)
    from strategies s
    join papers p on p.id = s.paper_id
    where s.embedding is not null
      and (asset_filter is null or s.asset         = asset_filter)
      and (type_filter  is null or s.strategy_type = type_filter)
      -- Un `sharpe_min` non NULL EXCLUT les stratégies sans Sharpe. On ne peut
      -- pas filtrer sur un nombre absent, et les garder reviendrait à traiter
      -- « inconnu » comme « au-dessus du seuil ».
      and (sharpe_min   is null or s.sharpe_ratio >= sharpe_min)
    order by s.embedding <=> query_embedding
    limit match_count;
$$;
