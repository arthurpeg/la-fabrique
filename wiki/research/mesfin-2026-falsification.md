---
type: research
updated: 2026-09-16
status: repere
ref: Mesfin (2026)
amorce_entry: 7
fiche: null
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
2. **Sa friction, surtout.** 2 points d'indice, rapportés au niveau du Nasdaq sur
   2021-2025 que **nos propres données mesurent** (13 000 à 25 000), valent **8 à
   15 bp** l'aller-retour — une **quinzaine de fois** l'écart d'un tick mesuré sur
   NQ (0,21 bp). Une hypothèse de coût quinze fois trop lourde tue n'importe quel
   signal intraday : **le résultat mesure peut-être davantage l'hypothèse que les
   signaux.**

Cette seconde réserve ne dit pas que le papier a tort. Elle dit que son verdict
n'est pas transportable tel quel, et qu'il faut refaire le calcul avec notre
modèle. Voir [[concepts/cout-aller-retour]].

## Statut chez nous

**Non lu intégralement** — comme toutes les entrées de `corpus/AMORCE.md`.
Programmé comme **réplication de la phase 06** : *le harnais réplique un résultat
publié connu, contrôles compris, sans intervention*. C'est la première cible de
cette porte (`ETAT.md`, phase 06).

## Voir aussi

[[concepts/cout-aller-retour]] · [[phases/phase-03-harnais-ic]] ·
[[research/gao-2018-intraday-momentum]] · [[Failed Ideas/ledger]]
