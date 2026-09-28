-- ============================================================================
-- 003_text_source_abstract.sql — un papier dont on n'a que le RÉSUMÉ — `D31`
--
-- Les dépôts SSRN ne sont pas lisibles par un robot (`D30`) : leur seul texte
-- accessible est le résumé que SSRN dépose chez Crossref. Il entre dans la
-- base, mais sous SA PROPRE étiquette. Le ranger sous `harvest` (« texte lu du
-- PDF ») le rendrait indiscernable d'un texte intégral — la confusion même que
-- `D22` a mise dans la donnée pour l'interdire.
-- ============================================================================

alter table papers drop constraint if exists papers_text_source_check;

alter table papers
    add constraint papers_text_source_check
        check (text_source in ('authoritative', 'harvest', 'abstract'));

comment on column papers.text_source is
    'authoritative = corpus/text/, versionné, empreinte au manifeste, `F2` peut
     s''en servir. harvest = lu du PDF à l''ingestion, NON reproductible depuis
     le dépôt (corpus/pdf/ est gitignoré), `F2` ne doit PAS s''en servir.
     abstract = le seul résumé déposé chez Crossref (D31) : un morceau, aucune
     fiche possible avant d''avoir le texte intégral puis D18.
     Ficher un papier `harvest` ou `abstract` exige de verser son texte sous
     D18 d''abord.';
