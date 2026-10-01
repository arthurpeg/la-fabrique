-- 006 — Les fiches vivent dans la base (D44).
--
-- Une fiche est le résumé structuré et cité d'un papier (D14) : affirmation,
-- univers, horizon, construction, résultats avec leur citation mot pour mot. Elle
-- était un fichier du dépôt ; elle est désormais une ligne de cette table, à côté
-- de son papier et de ses morceaux. Le dossier local n'en est plus qu'un miroir,
-- régénéré depuis ici (`corpus/fiches_store.py --tirer`).
--
-- `raw` garde le texte EXACT de la fiche, octet pour octet : son empreinte
-- (`sha256`) est celle que les registres de production ont inscrite, et le miroir
-- la reproduit à l'identique. `content` en est la forme interrogeable.
--
-- SÉCURITÉ : RLS activé sans aucune politique — la clé publique ne lit ni n'écrit
-- rien ; seule la clé secrète (`service_role`) y accède.
--
-- À coller dans l'éditeur SQL du tableau de bord Supabase.

create table if not exists public.fiches (
    fiche_id    text        primary key check (fiche_id ~ '^[A-Za-z0-9][A-Za-z0-9-]*$'),
    origin      text        not null check (origin in ('amorce', 'harvest', 'synthese')),
    paper_id    uuid        references public.papers(id) on delete set null,
    raw         text        not null,
    content     jsonb       not null,
    sha256      text        not null check (sha256 ~ '^[0-9a-f]{64}$'),
    pushed_at   timestamptz not null default now()
);

create index if not exists fiches_paper_id_idx on public.fiches (paper_id);
create index if not exists fiches_origin_idx on public.fiches (origin);

alter table public.fiches enable row level security;
revoke all on public.fiches from anon, authenticated;
