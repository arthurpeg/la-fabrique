---
type: research
updated: 2026-09-16
status: repere
ref: Bailey & López de Prado (2014)
amorce_entry: 22
fiche: null
implementable: oui
sources: [corpus/AMORCE.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Bailey & López de Prado (2014) — The deflated Sharpe ratio

*JPM* 40(5):94-107.
[SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)

## Ce que le papier affirme

Le Sharpe doit être **dégonflé** du **nombre d'essais**, de la non-normalité des
rendements et de la longueur de l'échantillon.

## Pourquoi ça nous concerne

C'est **la dernière opération du projet**. La phase 15 ouvre le `holdout` une
fois, et le Sharpe qui en sort est dégonflé du **nombre total de tests au
registre** (`D01` §9, `ETAT.md` phase 15).

C'est aussi la raison d'être du [[concepts/registre]], énoncée à l'envers : si le
compte des essais manque, le dégonflement n'est pas calculable et **le chiffre
final est faux**. C'est l'invariant III vu depuis la fin.

## Ce qu'il exige de nous

Trois intrants, dont deux ne s'obtiennent qu'en les ayant collectés au fur et à
mesure :

| Intrant | D'où il vient | État |
|---|---|---|
| Nombre d'essais | `registry/tests.jsonl` | **0 ligne** — le registre n'existe pas encore |
| Non-normalité (asymétrie, kurtosis) | les rendements de la stratégie | phase 10 |
| Longueur d'échantillon | la tranche `holdout`, 2,7 ans | acquis |

## Réserves

- 2,7 ans de `holdout` est **court** pour un dégonflement : la correction de
  longueur d'échantillon mordra. Ce n'est pas une surprise à découvrir en phase
  15 — c'est un ordre de grandeur à calculer en phase 03, pendant qu'il est encore
  temps d'en tenir compte.
- Le dégonflement suppose que le nombre d'essais est **connu**. Les règles de
  comptage de `D01` §4 sont donc une partie de cette référence, pas une
  convention séparée ([[concepts/comptage-des-tests]]).

## Statut chez nous

Non lu intégralement.

## Voir aussi

[[concepts/registre]] · [[concepts/comptage-des-tests]] · [[concepts/tranche]] ·
[[research/harvey-2016-cross-section]]
