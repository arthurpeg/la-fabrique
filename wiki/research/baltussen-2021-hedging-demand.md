---
type: research
updated: 2026-09-16
status: repere
ref: Baltussen, Da, Lammers & Martens (2021)
amorce_entry: 2
fiche: null
implementable: oui
sources: [corpus/AMORCE.md]
---

# Baltussen, Da, Lammers & Martens (2021) — Hedging demand and market intraday momentum

*JFE* 142(1). [SSRN 3760365](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365) ·
[PDF](https://www3.nd.edu/~zda/intramom.pdf)

## Ce que le papier affirme

Le rendement du **reste de la journée** prédit celui des **30 dernières minutes**.
Mécanisme proposé : la **couverture de gamma court** (options, ETF à levier).
Réversion les jours suivants. Testé sur **60+ futures** — actions, taux, matières
premières, devises — de 1974 à 2020.

## Ce qu'il exige comme données

Prix intraday de futures. **C'est exactement notre univers.**

## Pourquoi ça nous concerne

C'est la version *futures* de [[research/gao-2018-intraday-momentum]], sur un
univers qui contient le nôtre et un échantillon de 46 ans. C'est donc l'entrée la
plus directement transposable du corpus, et celle qui fournit un **mécanisme**
plutôt qu'un motif — ce qui compte pour l'invariant IV : une hypothèse avec
mécanisme se pré-enregistre mieux qu'une régularité.

La **réversion les jours suivants** est un test de contrôle gratuit : elle prédit
un signe, donc elle est falsifiable indépendamment du signal principal.

## Réserves — écrites avant de tester

- Le mécanisme de gamma court implique une dépendance à la structure du marché
  d'options, qui a beaucoup changé après 2020 — fin de l'échantillon. Les 0DTE
  n'y sont pas.
- « Le reste de la journée » se définit contre une séance de cotation. Chez nous,
  la grille découpe en trois fenêtres disjointes : la transposition n'est pas
  mécanique et devra être écrite avant d'être testée ([[concepts/cellule]]).

## Statut chez nous

Non lu intégralement. Fiche à produire en phase 07. Candidat sérieux au premier
signal codé, phase 08.

## Voir aussi

[[research/gao-2018-intraday-momentum]] ·
[[research/mesfin-2026-falsification]] · [[concepts/cellule]]
