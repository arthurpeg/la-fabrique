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

## [2026-09-17] setup | Emplacement des données fixé sur le poste de travail : RSL_DATA_DIR = C:\Users\Mathis\Desktop\Cotations (hors OneDrive) ; porte 01 rejouée sur les deux copies présentes | empreintes identiques à la ligne de base des deux côtés, catalogue valide, porte 02 inchangée (30/31)

## [2026-09-17] mesure | Deux vérifications : le raccord à 00:00 UTC tombe dans la fenêtre ASIA (19:00 NY en hiver, 20:00 en été) — pas dans la plage morte ; et les dates de roulement sont récupérables chez Databento par Historical.symbology.resolve (intervalles d0/d1/s, continuous -> raw_symbol), pas depuis nos fichiers | contrainte inscrite pour la phase 03 ; la demande à l'auteur des données devient précise

## [2026-09-17] gate | PORTE 02 FRANCHIE : dates de roulement obtenues du fournisseur par symbology.resolve (527, facturé 0,00 $), comparées AVANT adoption (compare_rolls.py) puis déposées au catalogue ; clause 3b réécrite sur les instruments réels ; L06, L07, L08 | gate_02_panel.py 43/43 ; détection empirique mesurée à 62,8 % de rappel et 67 faux positifs ; GC n'est pas mensuel (5,07/an) ; FDAX oscille ; phase courante = 03
