---
type: hub
updated: 2026-09-16
status: vide
sources: [ETAT.md, wiki/SCHEMA.md, signals/]
---

# Signaux — un dossier vide, et il doit le rester pour l'instant

**Aucune page ici, et c'est la situation correcte.**

`registry/tests.jsonl` compte **0 ligne**. `signals/` est vide. `harness/` est
vide. Le premier signal se code en **phase 08**, et la porte 03 — le harnais d'IC
calibré — n'est pas franchie.

> **Ne jamais écrire de code de stratégie ou de backtest avant que le harnais
> d'IC existe et soit calibré.** — `CLAUDE.md` § Les interdits

> Si tu te retrouves à écrire un signal alors que `ETAT.md` annonce la phase 02,
> tu as confondu les deux ordres — **arrête-toi**.
> Voir [[concepts/les-deux-ordres]].

## Ce qui remplira ce dossier

Une page par signal, au gabarit `type: signal` de `wiki/SCHEMA.md` § 1.3, portant
son `signal_id`, sa `hypothesis_ref`, sa fiche d'origine et ses `test_ids`.

Rappels du gabarit, parce qu'ils sont faciles à enfreindre :

- **L'hypothèse est recopiée telle qu'écrite avant le test.** Jamais reformulée
  après coup (invariant IV).
- **Les chiffres ne sont pas retapés ici.** Renvoi au rapport d'IC par `test_id`.
  Une page de wiki n'est jamais une source d'IC (`wiki/SCHEMA.md` § 0).
- **Un signal abandonné exige une ligne** dans [[Failed Ideas/ledger]], avec la
  raison. Ce n'est pas une option.
- Les verdicts nuls ont une page comme les autres — **surtout** eux : le produit
  du projet est *un petit nombre de signaux survivants, accompagnés d'un compte
  honnête du nombre de tests qu'il a fallu pour les trouver*.

## Les candidats repérés

Aucun n'est un signal tant qu'il n'a pas de fiche et de code.

- [[research/baltussen-2021-hedging-demand]] — même univers, mécanisme explicite
- [[research/gao-2018-intraday-momentum]] — tête de la famille qui porte presque
  tout le corpus
- [[research/mesfin-2026-falsification]] — la réplication de la phase 06, pas un
  signal

## Voir aussi

[[phases/phase-03-harnais-ic]] · [[concepts/registre]] · [[index]]
