---
type: concept
updated: 2026-09-16
status: stable
sources: [CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Tranche

**Le découpage temporel des données : `pool` et `holdout`. Deux, pas trois.**

## Ce que ça veut dire ici

| Tranche | Période | Durée | Statut |
|---|---|---|---|
| `pool` (recherche + validation) | 2016-01-03 → 2023-12-31 | 8,0 ans | walk-forward purgé, plusieurs plis, embargo aux frontières |
| `holdout` | 2024-01-01 → 2026-08-28 | 2,7 ans | **scellé jusqu'à la phase 15** |

`CLAUDE.md` § Le vocabulaire nomme encore trois tranches (`research`,
`validation`, `holdout`) ; `D01` §5, postérieure, a fondu les deux premières en
un `pool` en walk-forward. **La décision la plus récente fait foi.** Le champ
`data_slice` du registre garde les trois valeurs historiques.

## Ce que ça ne veut pas dire

- **Le `holdout` n'est pas « des données de test ».** Il s'ouvre **une fois**, à
  la phase 15. S'il est rouvert, il n'est plus un holdout (invariant V). Aucune
  exception, aucune « simple vérification » (`CLAUDE.md` § Les interdits).
- **Le `pool` n'est pas deux blocs contigus.** Trois blocs contigus ont été
  abandonnés : deux ans de validation composés d'un unique régime baissier
  (2022-2023, NQ à +2,0 % de dérive contre +20,9 % en recherche) ne valident
  qu'une chose ([[Failed Ideas/ledger]] F07).
- **Les plis d'un walk-forward ne sont pas k tests**, mais un seul. Voir
  [[concepts/comptage-des-tests]].

## Le holdout est typé, et son type est écrit d'avance

C'est la partie qu'on oublie. `D01` §5 décrit le holdout **avant de le lire** :
envolée de l'or (+48,4 % en 2025, volatilité de 14,2 % en moyenne de pool à
30,8 % en 2026), choc pétrolier en 2026 (volatilité 61,7 %, dérive +55,4 %),
actions calmes et haussières (NQ +20,2 %/an). Le pool, lui, contient le COVID
(2020 : NQ 34,9 % de volatilité, CL 95,9 %) et le marché baissier de 2022.

Un holdout décevant sur l'or ou le pétrole devra être lu à cette lumière —
**écrite avant, pas découverte après**. C'est l'invariant IV appliqué à la
lecture du résultat final.

## Où c'est fixé

`D01` §5 · `CLAUDE.md` invariant V · `registry/SCHEMA.md` champ `data_slice`

## Voir aussi

[[concepts/point-in-time]] · [[concepts/registre]] · [[concepts/porte]]
