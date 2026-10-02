-- 008 — Le graphe du corpus se calcule dans la base, et se lit par l'API.
--
-- `vectordb/graph.py` calculait les centroïdes et toutes les paires par une
-- connexion directe (port 5432), bloquée sur certains réseaux ; et à travers
-- l'API, une requête est coupée à 8 s (rôle `authenticator`), quand 1 942
-- papiers font 1,9 million de paires. La fonction ci-dessous fait ce calcul
-- dans la base et range le résultat dans deux tables, que `graph.py` lit par
-- l'API. Même définition qu'avant : centroïde des vecteurs de chaque papier,
-- les `top` plus proches de chaque papier (par rang, pas par seuil), deux
-- extraits par section au plus.
--
-- On la lance par l'outil SQL ou l'éditeur (pas de délai de 8 s) :
--     select rafraichir_graphe(4);

create table if not exists graph_edges (
    pa   uuid not null references papers(id) on delete cascade,
    pb   uuid not null references papers(id) on delete cascade,
    sim  double precision not null,
    primary key (pa, pb)
);

create table if not exists graph_excerpts (
    paper_id uuid not null references papers(id) on delete cascade,
    page     int,
    section  section_type,
    excerpt  text not null
);
create index if not exists graph_excerpts_paper_idx on graph_excerpts (paper_id);

-- Comme les autres tables : RLS sans politique, seule la clé secrète y accède.
alter table graph_edges    enable row level security;
alter table graph_excerpts enable row level security;

create or replace function rafraichir_graphe(top int default 4)
returns json
language plpgsql
as $$
declare
    n_papiers int;
    n_aretes  int;
begin
    create temp table cent on commit drop as
        select paper_id, avg(embedding)::vector(768) as v
        from chunks
        where embedding is not null and paper_id in (
            select id from papers where text_source in ('authoritative', 'harvest'))
        group by paper_id;
    select count(*) into n_papiers from cent;

    truncate graph_edges;
    -- Les `top` plus proches de chaque papier, dans les deux sens, dédoublonnés :
    -- une arête gardée par l'un des deux suffit.
    insert into graph_edges (pa, pb, sim)
    select distinct least(a, b), greatest(a, b), s
    from (
        select a.paper_id as a, k.paper_id as b, k.s
        from cent a
        cross join lateral (
            select c.paper_id, 1 - (a.v <=> c.v) as s
            from cent c
            where c.paper_id <> a.paper_id
            order by a.v <=> c.v
            limit top
        ) k
    ) t;
    select count(*) into n_aretes from graph_edges;

    truncate graph_excerpts;
    -- Le deuxième morceau de chaque section : le début d'un PDF est une page de garde.
    insert into graph_excerpts (paper_id, page, section, excerpt)
    select paper_id, page, section, left(content, 320)
    from (
        select paper_id, page, section, content,
               row_number() over (partition by paper_id, section order by ordinal) as rang
        from chunks
        where paper_id in (select paper_id from cent)
    ) t
    where rang = 2;

    return json_build_object('papiers', n_papiers, 'aretes', n_aretes,
                             'extraits', (select count(*) from graph_excerpts));
end;
$$;

revoke all on function rafraichir_graphe(int) from public, anon, authenticated;
