---
type: concept
updated: 2026-09-17
status: provisoire
sources: [decisions/DECISION-01-univers-et-donnees.md, LECONS.md, scripts/out/a2_roll_diagnostics.json]
---

# Roulement, recollement

**Le passage d'une échéance à la suivante dans une série continue. Une
discontinuité de niveau de prix, pas un détail de construction.**

> `status: provisoire` — les dates autoritatives ne sont pas reçues. Cette page
> sera révisée à leur arrivée.

## Ce que ça veut dire ici

Les séries sont **brutes (recollées)** : le raccord tombe à **00:00 UTC**, selon
un cycle **trimestriel** pour les indices et les devises, **mensuel** pour GC et
CL. Bonne nouvelle qui en découle : **l'historique ne se réécrira pas.**

Le traitement retenu : à chaque date d'évaluation `t`, construire une série
**ajustée à rebours en n'utilisant que les recollements ≤ `t`**. Elle reste
point-in-time car elle ne diffère de celle construite en `t+1` que par un facteur
d'échelle uniforme, qui n'affecte ni les rendements ni les ratios. Le prix brut
reste disponible séparément, pour les niveaux et l'exécution.

**Écrit depuis le 2026-09-17** : `panel/rolls.py`, ajustement multiplicatif —
le facteur d'échelle uniforme ci-dessus *est* la définition du multiplicatif
([[Failed Ideas/ledger]] F14) — prouvé sur un cas synthétique par la porte 02,
clause 3a. Il refuse tant que les dates manquent. Voir [[concepts/panel]].

## Ce que ça ne veut pas dire

- **Neutraliser la barre de roulement ne suffit pas — de loin.** Le niveau de prix
  est discontinu : toute grandeur calculée sur une fenêtre qui **enjambe** un
  recollement est fausse **sur toute sa largeur** — volatilité réalisée, moyennes
  mobiles, momentum.
- **Ce n'est pas au signal de s'en occuper.** Le traitement est au niveau du
  Panel, [[phases/phase-02-panel-pit]], jamais au niveau du signal.
- **Ce n'est pas un choix cosmétique de convention.** Calendaire (`.c.0`) contre
  volume (`.v.0`) décide de **la quantité d'historique qui existe** : l'or rendait
  136 702 barres au lieu de 3 717 717 (`LECONS.md` L01,
  [[Failed Ideas/ledger]] F01).
- **Notre détection empirique n'est pas la liste.** Elle rend 3,4–3,6
  roulements/an pour les indices là où il y en a 4, 8,5 pour CL là où il y en a
  12 ; 6A n'est pas tranché. Les trous sont **systématiques et corrélés au
  régime** — les années à taux proches de zéro. Une liste incomplète est plus
  dangereuse qu'aucune liste (`LECONS.md` L05, [[Failed Ideas/ledger]] F09).

## Ce qui manque

Les **dates de roulement autoritatives**, et la confirmation « brutes ou
ajustées », demandées à l'auteur des données. **Intrant bloquant de la phase 02.**

À leur réception : **comparer avant d'adopter**. L'écart mesure la méthode et fera
l'objet d'une entrée dans `LECONS.md`.

## Où c'est fixé

`D01` §6 · `LECONS.md` L01 et L05 · `scripts/out/a2_roll_diagnostics.json`

## Voir aussi

[[concepts/point-in-time]] · [[phases/phase-02-panel-pit]] ·
[[reference/ou-trouver-les-donnees]]
