---
type: concept
updated: 2026-09-16
status: provisoire
sources: [decisions/DECISION-01-univers-et-donnees.md, LECONS.md, scripts/out/a8_session_grid.json]
---

# Coût d'aller-retour

**Ce qu'un aller-retour coûte, par cellule, en points de base. Déclaré, sourcé et
pessimiste — parce qu'aucun barème réel n'est en main.**

> `status: provisoire` — deux des trois termes sont `null`.

## Ce que ça veut dire ici

```
round_trip_cost_bp(cell) = spread_floor_bp(cell)      mesuré
                         + fee_bp(instrument, size)    null -- todo
                         + slippage_bp(cell)           hypothèse déclarée, pessimiste
```

**Mesuré.** Le tick de chaque contrat est *observé* — plus petite variation de
prix non nulle sur onze ans — et non déclaré : NQ et ES 0,25 · YM 1,0 · GC 0,10 ·
CL 0,01 · 6E 0,00005 · 6B 0,0001 · 6J 0,0000005 · 6A 0,00005. Rapporté au prix
médian, l'écart plancher d'un tick vaut de **0,21 bp (NQ) à 1,55 bp (CL)**.
**Un marché ne peut pas être plus serré qu'un tick** : c'est le plancher du
modèle. Le tick est une *mesure*, pas une valeur déclarée — il ne tombe pas sous
l'interdit sur les valeurs inventées.

**`null` et ouvert en `todo`.** Frais d'échange et de compensation ; et les
**multiplicateurs** de contrat. Sources à dépouiller, jamais à deviner : barème
CME (*Non-Member Fee Finder* et le PDF daté) et liste de prix EUREX.

## Ce que ça ne veut pas dire

- **Zéro n'est pas gratuit.** L'estimateur de Corwin & Schultz (2012) rend une
  médiane **exactement nulle** sur 6A, 6B, 6J et toutes les cellules asiatiques :
  c'est une limite de l'estimateur sur barres 1 minute, pas un marché sans coût.
  Un critère bâti dessus déclarait 27 cellules sur 27 négociables, y compris là
  où 42 % des barres portent moins de dix contrats (`LECONS.md` L04,
  [[Failed Ideas/ledger]] F08). Il est **conservé comme borne haute** là où il
  dépasse le tick — CL en US : 1,08 bp contre 1,55 de tick ; NQ en US : 0,79 bp
  contre 0,21 de tick, c'est-à-dire que **NQ paie plus qu'un tick aux heures
  actives**.
- **Ce n'est pas un sujet de phase 10.** Coûts et capacité sont de première classe
  **dès la phase 03** (`D01` §9).
- **Un chiffre plausible n'est pas une mesure.** `null` est bruyant ; une valeur
  inventée devient indétectable en aval (`CLAUDE.md` § Les interdits).

## Plein contre micro — de l'arithmétique, pas une hypothèse

Un frais fixe de `F` dollars par contrat vaut `F / (P × M) × 10 000` bp. Si le
multiplicateur micro vaut un dixième du plein — **à vérifier** — la part fixe pèse
**exactement dix fois plus lourd en micro**, à prix égal. Le modèle devra afficher
**les deux tailles côte à côte** : c'est probablement là que se joue la viabilité
d'une stratégie à 1 ou 2 allers-retours par cellule et par jour.

## Le calibrage d'attente le plus proche

[[research/mesfin-2026-falsification]] conclut qu'aucune des 14 familles testées
sur MNQ ne survit à sa friction — mais cette friction, 2 points d'indice, vaut
**8 à 15 bp** l'aller-retour aux niveaux du Nasdaq que nos propres données
mesurent : une quinzaine de fois l'écart d'un tick sur NQ. À rejouer avec notre
modèle, phase 06.

## Où c'est fixé

`D01` §7 et §9 · `LECONS.md` L04

## Voir aussi

[[concepts/cellule]] · [[concepts/ic]] · [[phases/phase-03-harnais-ic]] ·
[[reference/ou-trouver-les-couts]]
