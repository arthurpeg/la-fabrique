# D44 — Les fiches vivent dans la base ; le dépôt n'en garde qu'un miroir

**Date :** 2026-10-01
**Phase :** 09
**État :** prise — choix de l'opérateur (« on utilisera que la base » ; option « les migrer dans la base »)

## La question

L'opérateur veut que la base Supabase soit la seule source : plus de fiches
« en local ». Mais une fiche n'est pas une copie du papier — c'est son résumé
structuré et cité (`D14`, `D16`), et toute la chaîne la lit : recettes, codeurs,
juge des signaux (`S5` vérifie chaque constante contre elle), hypothèses
(`D40` `A2`/`A6`), lot 09, Pupitre. Les supprimer aurait invalidé `H05`–`H14` et le
lot. Comment faire de la base la source sans rien casser ?

## Les options

1. **Supprimer les fiches locales.** Écartée par l'opérateur après exposé des
   conséquences.
2. **Les migrer dans la base, le dossier local devenant un miroir.** Retenue.
3. **Ne rien changer.** Écartée.

## Le choix

1. **La table `fiches`** (migration 006) porte chaque fiche : son texte exact
   (`raw`), sa forme interrogeable (`content`, jsonb), son empreinte, son origine
   (`amorce`, `harvest`, `synthese`) et le papier auquel elle se rattache
   (`paper_id`, par le titre normalisé). RLS activé sans politique : seule la
   clé secrète y accède.
2. **La base fait foi** ; les dossiers `corpus/fiches/`, `corpus/fiches_harvest/`
   et `corpus/fiches_synthese/` en sont le **miroir**, régénéré octet pour octet
   (`corpus/fiches_store.py --tirer`) et versionné dans git comme sauvegarde.
   Les empreintes des registres de production restent donc valides, et aucun
   outil de lecture n'a à changer.
3. **Le sens des écritures** : une fiche neuve est écrite par un sous-agent
   isolé (sans réseau) dans le miroir, inscrite et jugée, puis **versée**
   (`--pousser`). `avancer.py` tire puis pousse à chaque passage. Un conflit —
   une même fiche différente dans la base et le miroir — **n'est jamais écrasé** :
   il est signalé.
4. **Tout passe par l'API REST** et la clé secrète de `.env` : le port 5432 n'est
   pas nécessaire.

## Pourquoi

La base devient le lieu unique où papiers, morceaux, embeddings et fiches se
retrouvent ensemble, et où une recherche par le sens peut relier une fiche à
ses voisins. Le miroir garde ce qui rend une fiche fiable — son texte exact, son
empreinte, son historique git — et permet de travailler sans réseau.

**Ce qui est sacrifié.** Une dépendance au réseau pour verser et tirer ; et un
dossier local qui ne disparaît pas tout à fait, puisqu'il devient le miroir.

## Ce que ça verrouille

`vectordb/migrations/006_fiches.sql`, `corpus/fiches_store.py`,
`scripts/avancer.py` (étape 0), `scripts/verifier_tout.py` (contrôle réseau),
`.claude/commands/fabriquer-signaux.md`, `corpus/TRI-ET-FICHES.md`.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-01 | migration des 52 fiches | 52 dans la base, identiques au miroir à l'octet (empreintes égales) ; 49 reliées à leur papier — la synthèse n'a pas de papier unique, deux papiers (Mesfin 2026, une revue multifractale) ne sont pas dans la base. Un premier essai avait échoué sur ma contrainte d'identifiant (minuscules seules) : corrigée dans 006 |
