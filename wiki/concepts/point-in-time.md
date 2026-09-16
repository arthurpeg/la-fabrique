---
type: concept
updated: 2026-09-16
status: stable
sources: [CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md, scripts/gate_01_pit.py]
---

# Point-in-time

**À la date `t`, le code ne voit que ce qui existait à `t`. Par construction, pas
par vigilance.**

## Ce que ça veut dire ici

C'est l'invariant II de `CLAUDE.md` : *le look-ahead est empêché par
construction, jamais par vigilance. Le code de signal n'a structurellement pas
accès au futur.*

Deux mécanismes distincts, et il faut les deux :

1. **L'horodatage** — aucune ligne n'est visible avant le sien. C'est la porte de
   la [[phases/phase-02-panel-pit]].
2. **L'ajustement à rebours borné** — la série ajustée construite à `t` n'utilise
   que les recollements ≤ `t`. Elle reste point-in-time parce qu'elle ne diffère
   de celle construite en `t+1` que par un **facteur d'échelle uniforme**, qui
   n'affecte ni les rendements ni les ratios (`D01` §6). Voir
   [[concepts/roulement]].

Un troisième mécanisme, de contrôle : l'**empreinte de préfixe**
(`scripts/gate_01_pit.py`, `scripts/out/pit_fingerprints.json`) détecte qu'un
historique aurait été réécrit sous nos pieds par le fournisseur. Son échec est
l'une des cinq conditions de révision de `D01`.

## Ce que ça ne veut pas dire

- **Ce n'est pas une revue de code.** « J'ai vérifié qu'il n'y a pas de
  look-ahead » n'est pas une réponse recevable : si la vérification était le
  mécanisme, l'invariant II n'existerait pas.
- **Ce n'est pas le rôle du signal.** Le traitement des roulements est au niveau
  du Panel. Un signal qui corrige lui-même une discontinuité contourne le
  mécanisme.
- Un ajustement à rebours **non borné** — le mode par défaut de la plupart des
  fournisseurs de séries continues — **n'est pas** point-in-time : il réécrit
  tout l'historique à chaque roulement.
- Le prix **brut** reste disponible séparément, pour les niveaux et l'exécution.
  Le brut et l'ajusté ne servent pas à la même chose.

## La phase qui le fabrique

[[phases/phase-02-panel-pit]], bloquée sur les dates de roulement autoritatives.
La phase 05 y ajoute un **test de causalité automatique** : un signal qui tente de
lire le futur doit échouer tout seul.

## Où c'est fixé

`CLAUDE.md` invariant II · `D01` §6 · `ETAT.md` phases 02 et 05

## Voir aussi

[[concepts/roulement]] · [[concepts/tranche]] · [[phases/phase-02-panel-pit]]
