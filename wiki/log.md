---
type: hub
updated: 2026-09-16
status: actif
sources: [wiki/SCHEMA.md]
---

# LOG — le journal du wiki

> **Append-only.** On ajoute à la fin. On ne corrige pas une ligne, on en ajoute
> une qui la corrige — même règle que `registry/tests.jsonl` et `LECONS.md`.
>
> Format, fixe pour rester greppable (voir `wiki/SCHEMA.md` § 2.6) :
> `## [AAAA-MM-JJ] <type> | <ce qui s'est passé> | <résultat>`
>
> ```
> grep "^## \[" wiki/log.md | tail -5
> ```
>
> Ce fichier alimente [[hot]], qui est régénéré à partir de lui. Ne pas éditer
> `hot.md` : éditer ici.

---

## [2026-09-16] setup | Création du wiki : squelette wiki/, SCHEMA, ledger des idées abandonnées, générateur de hot.md, crochets .claude, groupes de graphe Obsidian ; DECISION-02 écrite d'abord, CLAUDE.md complété d'une section « Wiki » | wiki opérationnel, 12 idées abandonnées recensées rétrospectivement depuis D01 et LECONS.md

## [2026-09-17] phase | Phase 02 ouverte : D03 écrite, catalogue.yaml et son validateur, paquet panel/ (coupe poussée dans le lecteur Parquet, truncate vers le passé seul, holdout et tranche verrouillés), gate_02_panel.py ; porte 01 rejouée, empreintes identiques | 2 clauses sur 3 passent ; porte 02 NON franchie, bloquée sur les dates de roulement

## [2026-09-17] phase | Phase 02 complétée côté code : panel/rolls.py, l'ajustement multiplicatif à rebours (D01 §6), prouvé sur un cas synthétique — sauts retirés, rendements préservés, facteur d'échelle entre deux dates de construction, mouvement de la minute de raccord injecté et mesuré ; truncate() refuse aussi de sortir de la tranche par le bas | 30 vérifications sur 31 ; porte 02 toujours NON franchie — ce qui manque est de la donnée, pas du code
