---
type: concept
updated: 2026-09-17
status: provisoire
sources: [decisions/DECISION-03-panel-et-catalogue.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Panel

**La couche de données. Un Panel s'ouvre à une date, et ne peut pas lire une
barre postérieure à cette date — pas « ne doit pas » : ne peut pas.**

`provisoire` tant que la série ajustée à rebours n'est pas écrite.

## Ce que ça veut dire ici

```python
from panel import Panel

p = Panel.open(asof="2021-06-15 20:00", slice="pool")
p.universe()               # les instruments cotés à cette date
p.bars("NQ", window="US")  # prix bruts, jamais une barre postérieure
p.truncate(end=t)          # un panel qui en sait moins ; jamais davantage
p.adjusted("NQ")           # RollDatesMissing, tant que les dates manquent
```

Le mécanisme tient en une phrase : **la coupe est poussée dans le lecteur
Parquet**. À `asof` donné, les barres postérieures ne sont pas filtrées après
lecture — elles ne sont jamais lues. Mesuré : 0,09 s contre 0,08 s pour une
lecture complète de NQ (1,88 M barres). L'alternative — tout lire, puis n'exposer
que le passé — est de la vigilance déguisée en architecture : il suffit d'un
cache lu par curiosité. Voir [[Failed Ideas/ledger]] F13.

## Les quatre refus

| Refus | Ce qui l'a déclenché |
|---|---|
| `LookaheadRefused` | demander à un panel un instant postérieur au sien |
| `SliceExceeded` | une date hors de la tranche travaillée |
| `HoldoutLocked` | la tranche scellée ([[concepts/tranche]]) |
| `RollDatesMissing` | la série ajustée, tant que les dates manquent |

Chacun a son nom parce qu'un `ValueError` générique ne dit pas ce qui vient
d'être tenté. `truncate` est l'accroche du test de causalité de la phase 05 : un
signal qui tente d'avancer l'`asof` lève.

## Ce que ça ne veut pas dire

- **Ce n'est pas le harnais.** Le Panel lit ; le harnais juge. Le harnais est
  figé à partir de la phase 03, le Panel ne l'est pas encore.
- **`bars()` ne rend pas une série ajustée.** Elle rend le prix **brut**, et
  c'est voulu (`D01` §6) : les niveaux et l'exécution en ont besoin. Le
  traitement du roulement se fera ici, au niveau du Panel, **jamais au niveau du
  signal** — un signal qui corrige lui-même un recollement est un bug
  d'architecture. Voir [[concepts/roulement]].
- **Le verrou du holdout n'est pas la phase 04.** Le Panel refuse la tranche
  scellée, mais la porte 04 exige davantage : qu'aucun chemin de code ne produise
  un IC sans écrire au registre. Elle n'est pas franchie pour autant.

## Où c'est fixé

`D03` · `panel/panel.py` · `scripts/gate_02_panel.py` · `catalogue/catalogue.yaml`

## Voir aussi

[[concepts/point-in-time]] · [[concepts/tranche]] · [[concepts/roulement]] ·
[[phases/phase-02-panel-pit]] · [[concepts/cellule]]
