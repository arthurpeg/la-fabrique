-- ============================================================================
-- 002_text_source.sql — d'où vient le texte d'un papier — `D22`
--
-- Deux textes coexistent désormais dans la base, et ils n'ont pas la même
-- autorité. Sans cette colonne, un morceau de papier moissonné est
-- INDISCERNABLE d'un morceau passé par `D18` : quelqu'un en tirerait une
-- citation en croyant qu'elle a été vérifiée.
--
-- La distinction vit dans la DONNÉE et non dans la prose : une note de README
-- n'est lue ni par une requête SQL, ni par une session future.
-- ============================================================================

alter table papers
    add column text_source text
        check (text_source in ('authoritative', 'harvest'));

-- Les papiers déjà en base viennent tous de `corpus/text/`.
update papers set text_source = 'authoritative' where text_source is null;

-- PAS DE DÉFAUT, délibérément : insérer un papier oblige à dire d'où vient son
-- texte. Un défaut ferait passer l'oubli pour un choix.
alter table papers alter column text_source set not null;

comment on column papers.text_source is
    'authoritative = corpus/text/, versionné, empreinte au manifeste, `F2` peut
     s''en servir. harvest = lu du PDF à l''ingestion, NON reproductible depuis
     le dépôt (corpus/pdf/ est gitignoré), `F2` ne doit PAS s''en servir.
     Ficher un papier `harvest` exige de verser son texte sous D18 d''abord.';

create index papers_text_source_idx on papers (text_source);
