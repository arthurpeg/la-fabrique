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
| Les dates de roulement | `catalogue/roll_dates.json` — 527, reçues le 2026-09-17, avec la requête qui les a produites |
| Ce que valait notre détection empirique | `LECONS.md` L06 · `scripts/compare_rolls.py` |
| L'inventaire mesuré des fichiers | `scripts/out/a1_inventory.json` |
| Les diagnostics de recollement | `scripts/out/a2_roll_diagnostics.json` |
| La largeur effective mesurée | `scripts/out/a3_breadth.json`, `a5_breadth_intraday.json` |
| Les régimes par tranche | `scripts/out/a4_regimes.json` |
| La grille actif × séance et les cellules retenues | `scripts/out/a8_session_grid.json` · `D01` §3 |
| L'intégrité point-in-time | `scripts/gate_01_pit.py` · `scripts/out/pit_fingerprints.json` |
| Les métadonnées point-in-time par instrument | `catalogue/catalogue.yaml`, gardé par `catalogue/validate.py` |
| Comment les données se lisent | [[concepts/panel]] · `panel/` · `D03` |
| Le découpage en tranches | `D01` §5 · [[concepts/tranche]] |

> **Le projet tourne sur deux postes**, et `.env` n'est pas versionné : chacun
> déclare son propre `RSL_DATA_DIR`. Ne pas lire ce qui suit comme si une seule
> machine existait.
>
> | Poste | `RSL_DATA_DIR` | Vérifié le |
> |---|---|---|
> | Mathis | `C:\Users\Mathis\Desktop\Cotations`, hors OneDrive — une seconde copie sous `C:\Users\Mathis\Cotations`, empreintes identiques ; celle du Bureau fait foi | 2026-09-17 |
> | Arthur | `D:\quant-data\Cotations` | 2026-09-17 — portes 01, 02 et 03 rejouées, mêmes empreintes et mêmes comptes |
>
> Les copies **ne divergent pas** : mêmes empreintes à la ligne de base des deux
> côtés. Le chemin n'est jamais en dur dans le code — `panel/paths.py` le lit de
> l'environnement ou de `.env`.
