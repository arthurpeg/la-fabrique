---
type: router
updated: 2026-09-16
status: actif
sources: [CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md, registry/SCHEMA.md]
---

# Où trouver : la métrique et le comptage des tests

> Page-routeur. **Aucun fait ici** — seulement l'adresse du fait.

| Question | Autorité |
|---|---|
| Quelle métrique d'évaluation, et pourquoi pas l'IC transversal | `decisions/DECISION-01-univers-et-donnees.md` §2 |
| Quelle cible d'IC viser | `D01` §2 — deux bornes, jamais une |
| Pourquoi la statistique doit être robuste à la corrélation transversale | `D01` §2 |
| Ce qui justifie le *pooling* entre instruments | `corpus/AMORCE.md` entrée 12 · [[research/bollerslev-2018-risk-everywhere]] |
| Quel seuil de significativité | `D01` §2 et §9 · `corpus/AMORCE.md` entrée 21 · [[research/harvey-2016-cross-section]] |
| Ce qui compte pour un test | `D01` §4 · [[concepts/comptage-des-tests]] |
| Le schéma d'une ligne de registre | `registry/SCHEMA.md` |
| Pourquoi aucun IC ne peut être calculé hors du harnais | `CLAUDE.md` invariant III et § Les interdits |
| Comment le Sharpe final est dégonflé | `D01` §9 · `corpus/AMORCE.md` entrée 22 · [[research/bailey-2014-deflated-sharpe]] |
| Qui produit les IC officiels | le **harnais**, `harness/` — **vide à ce jour**, construit en [[phases/phase-03-harnais-ic]] |
| Où sont les IC calculés | `registry/tests.jsonl` — **0 ligne à ce jour** |
