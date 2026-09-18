---
type: research
updated: 2026-09-16
status: repere
ref: Mesfin (2026)
amorce_entry: 7
fiche: corpus/fiches/mesfin-2026-ohlcv-falsification.json
implementable: oui
sources: [corpus/AMORCE.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Mesfin (2026) — Structural Limits of OHLCV-Based Intraday Signals in MNQ Futures

*A Systematic Falsification Study*, arXiv:2605.04004.
**Résultat négatif**, et la référence la plus proche de notre situation.

## Ce que le papier affirme

14 familles de signaux prix/volume testées sur MNQ, barres 5 minutes, 947 séances
2021-2025. **Aucune ne survit** à un coût d'aller-retour réaliste : rendement brut
de 0,07 à 1,50 point par trade contre **2 points de friction supposés**.

## Ce qu'il exige comme données

OHLCV seul. Nous l'avons. Même univers d'esprit, même granularité, même pauvreté
de données.

## Pourquoi ça nous concerne

C'est **le calibrage d'attente le plus proche de notre situation**, et le plus
inconfortable. Si ce résultat tient avec notre modèle de coût, le corpus
implémentable perd sa famille principale — voir le verdict de `corpus/AMORCE.md`.

## Réserves — écrites avant de tester

Deux, qui ne l'annulent pas mais la bornent.

1. **Préprint d'un auteur seul, non arbitré.**
2. ~~**Sa friction, surtout.**~~ **RETIRÉE le 2026-09-18 — elle reposait sur une
   erreur d'un facteur 10.** Voir ci-dessous.

## La réserve sur la friction est tombée

Cette page a porté du 2026-09-16 au 2026-09-18 une réserve qui disait : « 2 points
d'indice valent **8 à 15 bp** l'aller-retour, une **quinzaine de fois** l'écart
d'un tick sur NQ ; une hypothèse de coût quinze fois trop lourde tue n'importe
quel signal intraday, donc le résultat mesure peut-être davantage l'hypothèse que
les signaux. »

**Le calcul est faux d'un facteur 10**, et il est refait par
`scripts/check_mesfin_premise.py`, sur nos données, tranche `pool`,
2021-01-01 → 2023-12-31 (le reste de sa fenêtre est dans le `holdout` scellé) :

| | |
|---|---|
| niveau NQ mesuré | c1 **11 512** · médiane **14 688** · c99 **17 556** |
| 2 points à la médiane | **1,36 bp** |
| 2 points sur la plage | **1,14 à 1,74 bp** |
| notre plancher `NQ × US` | 0,79 bp → sa friction vaut **1,7×** le nôtre |
| notre **pire** cellule | 1,55 bp → sa friction vaut **0,9×** le nôtre |

Et la comparaison lui est encore défavorable à tort : notre plancher est un
**écart seul**, `fee_bp` et `slippage_bp` étant `null`, tandis que ses 2 points
sont une friction **tout compris**. L'écart restant se refermera quand les frais
arriveront.

**Conséquence : son verdict est transportable.** Il ne peut pas être écarté au
motif d'une hypothèse de coût déraisonnable — elle est du même ordre que la
nôtre, et plus légère que notre pire cellule. La première réserve, elle, tient
toujours : préprint d'un auteur seul, non arbitré.

La plage de niveaux citée par la réserve d'origine — « 13 000 à 25 000 » — ne
correspond pas non plus à ce que la tranche `pool` contient : NQ n'y dépasse pas
17 556 au centile 99. Elle venait d'ailleurs que de nos données, tout en étant
présentée comme en venant. C'est précisément la maladie que `D09` traite au
catalogue, ici attrapée dans le wiki. Voir [[lessons|L14]].

## Statut chez nous

**LU le 2026-09-18** — PDF récupéré dans `corpus/pdf/`, fiche écrite à la main
dans `corpus/fiches/mesfin-2026-ohlcv-falsification.json`. C'est la première
entrée du corpus qui sorte du statut `repere`.

Deux obstacles à la réplication en sont ressortis, tous deux **structurels**, et
aucun n'a à voir avec les frais :

1. **La métrique.** Son critère est un `t ≥ 2,0` sur des **rendements nets par
   trade**, avec 30 trades minimum par pli et une permutation `p < 0,001`. Notre
   harnais produit un **IC de Spearman**. Onze de ses quatorze familles échouent
   parce que leur rendement brut (0,07 à 1,50 point) est **sous la friction** —
   ce qui n'est pas une absence de prédiction mais une insuffisance d'amplitude,
   et un IC ne la voit pas. Mesurer son critère demanderait un évaluateur au
   niveau du trade, c'est-à-dire le moteur de la phase 10.
2. **Les années.** Ses trois plis hors échantillon testent 2023, 2024 et 2025.
   Notre `holdout` couvre 2024-01-01 → 2026-08-28 et reste scellé (invariant V) :
   **seul le pli 1 est reproductible**, un tiers de son plan.

Programmé comme **réplication de la phase 06** : *le harnais réplique un résultat
publié connu, contrôles compris, sans intervention*. C'est la première cible de
cette porte (`ETAT.md`, phase 06) — et ce qu'elle peut signifier ici doit être
tranché par écrit.
Programmé comme **réplication de la phase 06** : *le harnais réplique un résultat
publié connu, contrôles compris, sans intervention*. C'est la première cible de
cette porte (`ETAT.md`, phase 06).

## Voir aussi

[[concepts/cout-aller-retour]] · [[phases/phase-03-harnais-ic]] ·
[[research/gao-2018-intraday-momentum]] · [[Failed Ideas/ledger]]
