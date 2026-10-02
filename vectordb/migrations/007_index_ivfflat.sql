-- 007 — L'index de similarité des morceaux passe de HNSW à IVFFlat (D46).
--
-- Le HNSW de la migration 001 ne se construit pas sur la petite instance :
-- 145 356 vecteurs de 768 dimensions demandent plusieurs centaines de Mo pour
-- tenir le graphe en mémoire ; avec les 32 Mo par défaut, la construction du
-- 2026-10-01 est tombée à ~5 blocs par minute puis s'est arrêtée, en saturant
-- la base. IVFFlat se construit en une passe de k-moyennes, avec peu de mémoire.
--
-- Réglages (recommandations de pgvector, fixés avant tout essai) :
--   lists  = 150 ≈ lignes / 1000 (moins d'un million de lignes) ;
--   probes = 12  ≈ racine de lists, posé par la fonction de recherche à chaque
--                  appel (`set_config` local à la transaction) : Supabase refuse
--                  `set ivfflat.probes` dans la définition d'une fonction
--                  (« permission denied to set parameter », 2026-10-02).
-- L'index est approché : une recherche lit 12 des 150 listes. `vector_search`
-- garde sa signature ; seul le réglage de recherche s'ajoute.
--
-- Aucune donnée n'est touchée : un index se calcule à partir des vecteurs.

drop index if exists chunks_embedding_hnsw;

-- La construction demande plus que la mémoire de maintenance par défaut
-- (32 Mo) pour l'échantillon des k-moyennes ; un seul processus.
set maintenance_work_mem = '128MB';
set max_parallel_maintenance_workers = 0;

create index if not exists chunks_embedding_ivfflat on chunks
    using ivfflat (embedding vector_cosine_ops) with (lists = 150);

create or replace function vector_search(
    query_embedding vector(768),
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
language plpgsql volatile
as $$
begin
    perform set_config('ivfflat.probes', '12', true);
    return query
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
end;
$$;
