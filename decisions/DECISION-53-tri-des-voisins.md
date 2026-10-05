# D53 — Les voisins sont triés par un juge isolé avant la synthèse

**Date :** 2026-10-05
**Phase :** 09
**État :** prise. Demande de l'opérateur : « améliore la recherche pour avoir moins de hors sujet ». Complète `D47`, `D48` et `D52`.

## La question

Sur Lucca-Moench (`D52`), 7 voisins sur 10 étaient `hors_sujet`. Une meilleure
recherche peut-elle les écarter, et comment le mesurer ?

## Les options

Un banc de précision (`scripts/banc_precision_voisins.py`) a été fixé avant le
premier jugement :
- 6 graines variées ;
- les 10 premiers voisins de 5 variantes de recherche, mis en commun (135 candidats) ;
- un juge isolé (Sonnet) par graine, sans savoir quelle variante a proposé quoi,
  qui répond `meme` (même mécanisme) ou `autre`.

La mesure est la précision à 10, c'est-à-dire la part de `meme` parmi les dix
premiers voisins (`scripts/out/banc_precision/`).

| Variante | Précision à 10 |
|---|---|
| A. La fiche, toutes sections, moyenne des 3 meilleurs morceaux (`D48`) | 0,22 |
| B. La fiche, introductions et conclusions seulement | 0,17 |
| C. Le mécanisme seul (titre, affirmation, construction) | 0,23 |
| D. Le mécanisme seul, introductions et conclusions | 0,23 |
| E. A, puis un reclassement par cross-encodeur contre l'affirmation | 0,17 |

1. **Aucune variante de recherche ne fait mieux.** Les écarts tiennent à un ou
   deux papiers. Un modèle d'embeddings rapproche des thèmes ; il ne distingue
   pas « même mécanisme » de « même sujet ».
2. **La base a peu de voisins du même mécanisme.** Sur les 135 candidats, 23 sont
   `meme`, de 1 sur 21 (Gorton) à 6 sur 23 (Andersen). Une part des hors-sujet ne
   vient pas de la recherche : le bon voisin n'existe pas.
3. **Le juge, lui, trie nettement**, avec une raison par candidat.

## Le choix

Le tri devient une étape à part, entre la recherche et la synthèse :

1. `synthese_dossier.py --candidats <graine>` :
   - la recherche (`D48`) propose 30 candidats ;
   - les candidats sont versionnés dans `corpus/dossiers/tri-<graine>.json` ;
   - la consigne du trieur est écrite.
2. `fabrique-voisins` (Sonnet, Read et Write seulement, isolé) étiquette chaque
   candidat `meme` ou `autre`, avec sa raison, dans
   `corpus/dossiers/tri-<graine>.labels.json`.
3. `synthese_dossier.py --prepare <graine>` exige des étiquettes complètes et ne
   met au dossier que les candidats `meme`. **S'il n'y en a aucun, il n'y a pas
   de synthèse** : la base n'a pas de voisin du même mécanisme pour cette graine.
4. La synthèse et son validateur (`D52`) ne changent pas. Le rôle `hors_sujet`
   y reste possible, car le trieur peut se tromper.

Le dossier donne désormais l'année et les auteurs de chaque voisin, lus en base.
Sans eux, l'agent de synthèse avait dû déduire une année (essai ci-dessous).

## Pourquoi

C'est le seul levier mesuré qui sépare le mécanisme du thème. Le coût reste du
même ordre : environ 90 000 tokens de tri en Sonnet, mais une consigne de
synthèse deux à trois fois plus courte. Et la sortie dit honnêtement quand une
graine n'a pas de voisin utile.

**Ce qui est sacrifié.** Le tri est un jugement d'IA. Il est isolé, motivé et
versionné, mais pas mécanique. Il décide seulement de ce qu'on lit, jamais de
ce qu'on mesure : aucune valeur, aucun IC n'en dépend.

## Ce que ça verrouille

`scripts/synthese_dossier.py` (`--candidats`, `voisins_tries`), `.claude/agents/fabrique-voisins.md`,
`scripts/voisins.py` (année, auteurs), `scripts/banc_precision_voisins.py`.

## Ce qui reste ouvert

- Le juge du banc et le trieur sont du même modèle : la précision du trieur
  n'est pas mesurée contre un humain.
- Chercher au-delà de 30 candidats si une graine en garde trop peu.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-05 | banc de précision, 6 graines | voir le tableau ; 6 juges, environ 75 000 tokens chacun |
| 2026-10-05 | crypto momentum : tri, puis synthèse | 7 candidats `meme` sur 30 (88 737 tokens). Synthèse valide (66 187 tokens) : 4 `contredit`, 1 `confirme`, 1 `deja_teste` (H06), **1 seul `hors_sujet`** sur 7, contre 7 sur 10 sans tri. Apport `aucun`, donc **non codée**, comme l'exige `D52`. L'agent avait déduit `source.year` faute d'année des voisins : corrigé, le dossier porte désormais l'année et les auteurs |
