---
type: router
updated: 2026-09-24
status: actif
sources: [decisions/DECISION-01-univers-et-donnees.md, LECONS.md]
---

# Où trouver : les coûts, les frais, les multiplicateurs

> Page-routeur. **Aucun fait ici** — seulement l'adresse du fait.
> Plusieurs lignes pointent vers un `null` assumé : c'est le but.

| Question | Autorité |
|---|---|
| La structure du modèle de coût | `decisions/DECISION-01-univers-et-donnees.md` §7 · [[concepts/cout-aller-retour]] |
| Le tick de chaque contrat | `D01` §7 — **mesuré** sur onze ans, pas déclaré |
| L'écart plancher en bp par instrument | `D01` §7 |
| Pourquoi Corwin & Schultz ne suffit pas | `LECONS.md` L04 · [[Failed Ideas/ledger]] F08 |
| **Les frais d'échange et de compensation** | **`null`** — barème CME (*Non-Member Fee Finder* + PDF daté) et liste EUREX, `D01` §7. `ETAT.md` § Ce qui bloque |
| **Les multiplicateurs de contrat** | **déposés le 2026-09-24** pour les neuf CME, chacun sous sa citation « Contract Unit » : `catalogue/catalogue.yaml` § `provenance` (`D09`). FDAX reste `null` (unité en EUR) |
| Pourquoi plein et micro ne se valent pas | `D01` §7, arithmétique du frais fixe |
| À quelle phase les coûts entrent | `D01` §9 — **phase 03**, pas 10 |
| La règle sur les valeurs inventées | `CLAUDE.md` § Les interdits |
| Les coûts estimés par cellule | `scripts/out/a8_session_grid.json` |
