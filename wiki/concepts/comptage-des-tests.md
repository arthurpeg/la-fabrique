---
type: concept
updated: 2026-09-16
status: stable
sources: [decisions/DECISION-01-univers-et-donnees.md, registry/SCHEMA.md, CLAUDE.md]
---

# Comptage des tests

**Combien de lignes un travail donné écrit au registre. La règle est contraignante
et contre-intuitive dans les deux sens.**

## Ce que ça veut dire ici

| Ce qu'on fait | Ce que ça compte |
|---|---|
| Un signal évalué sur la grille des cellules retenues | **1 test** — la statistique poolée |
| La ventilation cellule par cellule de ce même signal | **0** — c'est un *diagnostic* |
| Les k plis d'un même schéma de walk-forward | **1 test**, pas k |
| Une cellule seule, retenue **après** avoir vu les résultats | **interdit** |
| Une cellule seule, **pré-enregistrée avant** de voir les résultats | **1 test de plus** — c'est une hypothèse distincte |

## Pourquoi c'est réglé si strictement

Dans les deux sens, une erreur de comptage détruit l'appareil statistique :

- **Compter trop** — 25 tests par famille parce qu'il y a 25 cellules — ferait
  exploser le seuil de FDR **pour une raison purement mécanique**, et tuerait des
  signaux valides sans rien apprendre.
- **Compter trop peu** — ne pas inscrire une exploration — rend le seuil trop
  permissif et transforme le meilleur de N tirages en résultat. Et le compte ne se
  reconstitue pas après coup : voir [[concepts/registre]].

## Ce que ça ne veut pas dire

- **Ce n'est pas un usage à respecter au mieux.** Aucun chemin de code ne produit
  un IC sans écrire au registre (invariant III). Le comptage n'est pas une
  discipline : c'est une propriété du code, à fabriquer en
  [[phases/phase-04-registre-et-holdout]].
- **Un diagnostic n'est pas un test — tant qu'on ne s'en sert pas pour choisir.**
  Dès qu'une ventilation par cellule sert à retenir une cellule, elle a cessé
  d'être un diagnostic. C'est exactement l'interdit ci-dessus.

## Ce à quoi le compte final sert

Au **Sharpe dégonflé** de la phase 15, du nombre total de tests au registre
([[research/bailey-2014-deflated-sharpe]]), et au seuil de FDR appliqué **dès le
premier test**, jamais un t-stat à 2 ([[research/harvey-2016-cross-section]]).

## Où c'est fixé

`D01` §4 et §9 · `registry/SCHEMA.md` · `CLAUDE.md` invariants III et IV

## Voir aussi

[[concepts/registre]] · [[concepts/ic]] · [[concepts/cellule]] ·
[[reference/metrique-et-comptage]]
