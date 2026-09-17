---
type: router
updated: 2026-09-17
status: actif
sources: [CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md, ETAT.md]
---

# Où trouver : les données

> Page-routeur. **Aucun fait ici** — seulement l'adresse du fait.
> Ne pas confondre `wiki/reference/` (ces routeurs) avec `reference/` à la racine
> (documents tiers datés, en lecture seule).

| Question | Autorité |
|---|---|
| Où vivent physiquement les données | `CLAUDE.md` § Conventions, Données — variable `RSL_DATA_DIR`, `.env.example` |
| Quels instruments composent l'univers | `decisions/DECISION-01-univers-et-donnees.md` § Ce que ça verrouille, 1 |
| Pourquoi FDAX est exclu | `D01` §1 · `LECONS.md` L02 · [[Failed Ideas/ledger]] F02 |
| Quelle convention de roulement, et pourquoi | `D01` §6 · `LECONS.md` L01 · [[concepts/roulement]] |
| Les dates de roulement | **n'existent pas encore** — `ETAT.md` § Ce qui bloque |
| L'inventaire mesuré des fichiers | `scripts/out/a1_inventory.json` |
| Les diagnostics de recollement | `scripts/out/a2_roll_diagnostics.json` |
| La largeur effective mesurée | `scripts/out/a3_breadth.json`, `a5_breadth_intraday.json` |
| Les régimes par tranche | `scripts/out/a4_regimes.json` |
| La grille actif × séance et les cellules retenues | `scripts/out/a8_session_grid.json` · `D01` §3 |
| L'intégrité point-in-time | `scripts/gate_01_pit.py` · `scripts/out/pit_fingerprints.json` |
| Les métadonnées point-in-time par instrument | `catalogue/catalogue.yaml`, gardé par `catalogue/validate.py` |
| Comment les données se lisent | [[concepts/panel]] · `panel/` · `D03` |
| Le découpage en tranches | `D01` §5 · [[concepts/tranche]] |

> **Sur cette machine** (poste de travail, 2026-09-17) : `RSL_DATA_DIR` vaut
> `C:\Users\Mathis\Desktop\Cotations`, hors OneDrive. Une seconde copie
> existe sous `C:\Users\Mathis\Cotations` : porte 01 rejouée sur les deux,
> empreintes identiques à la ligne de base — **elles ne divergent pas**. C'est
> celle du Bureau qui fait foi. `.env` n'est pas versionné : une autre machine
> redéclare son propre chemin.
