---
type: concept
updated: 2026-09-16
status: stable
sources: [decisions/DECISION-01-univers-et-donnees.md, LECONS.md, scripts/out/a3_breadth.json, scripts/out/a5_breadth_intraday.json]
---

# Largeur effective

**Le nombre de paris réellement indépendants que porte l'univers — pas le nombre
d'instruments.**

## Ce que ça veut dire ici

Neuf instruments corrélés ne font pas neuf paris. La mesure donne **4,03** en
journalier et **4,22** sur barres 15 minutes (`scripts/out/a3_breadth.json`).

Ce qui crée de la largeur ici est la **grille actif × séance**, et le gain ne
vient pas du nombre d'instruments mais de la **structure de blocs**, qui change
d'une séance à l'autre : le bloc devises, soudé en Europe et aux États-Unis,
**se dissout en séance asiatique** — 6E, 6J et 6A y deviennent trois paris
séparés.

| Fenêtre | Largeur | Instruments |
|---|---|---|
| `ASIA` | 4,43 | 7 |
| `EUROPE` | 4,10 | 9 |
| `US` | 3,87 | 9 |
| somme des trois | **12,40** | sous hypothèse d'indépendance entre fenêtres |

## Ce que ça ne veut pas dire

- **Ce n'est pas une constante.** La largeur *réalisée* séance par séance a une
  médiane de 3,74 mais un **centile 5 à 2,38** : 17 % des séances tombent sous
  3 paris, 1,7 % sous 2. Les pires — 2022-09-13, 2022-11-10, 2022-12-13,
  2023-02-14 — sont des jours de chiffre macro où un seul PC explique jusqu'à
  **84 %** de la variance transversale. Ces jours-là, neuf instruments font un
  pari. **Ça ne se voit jamais dans un IC moyen ; ça se voit dans la queue d'un
  PnL** (`LECONS.md` L03).
- **Le 12,40 n'est pas acquis.** Les trois fenêtres sont disjointes dans le temps ;
  elles ne sont pas indépendantes pour autant, une tendance traversant les trois.
  Si elles ne le sont pas pour une famille de signaux donnée, le compte retombe
  vers ~1 060 paris/an. Le rapport d'IC doit porter **les deux comptes**.
- **Ça ne se gagne pas en montant en fréquence** : 4,22 à 15 min, 4,19 à 30 min,
  4,17 à 60 min, 4,03 en journalier ([[Failed Ideas/ledger]] F06).
- La largeur *récoltable* sera encore plus basse : la taille de compte et le
  nombre de positions simultanées la plafonneront (`D01`, point ouvert, phase 10).

## Pourquoi c'est la contrainte centrale

Elle fixe la cible d'IC : ~3 100 paris/an donnent un IC requis de **0,018** pour
un IR de 1 ; ~1 060 paris/an le portent à **0,031**. Et elle interdit l'IC
transversal ([[Failed Ideas/ledger]] F03).

## Où c'est fixé

`decisions/DECISION-01-univers-et-donnees.md` §2 et §3 · `LECONS.md` L03

## Voir aussi

[[concepts/ic]] · [[concepts/cellule]] · [[concepts/comptage-des-tests]] ·
[[phases/phase-03-harnais-ic]]
