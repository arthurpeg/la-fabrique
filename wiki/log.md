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

## [2026-09-17] gate | PORTE 03 FRANCHIE : D04 écrite, paquet harness/ (IC Spearman par cellule, poolé par observations, t déflaté de √h puis de √(9/4,224), coût rendu comme plancher étiqueté, écriture au registre à chaque IC) et gate_03_harness.py | 19/19 ; score parfait -> IC 1.000000000, seconde implémentation à 1e-12, bruit -> IC +0,00108 et t final +0,06 ; harnais FIGÉ ; phase courante = 04

## [2026-09-17] audit | Vérification des phases 02 et 03 : couverture des portes étendue de 3-4 instruments à l'univers entier (porte 02 : 103 vérifications, 9/9 ; porte 03 : 41, 25/25 cellules, IC parfait sur 5 958 995 observations) ; contournement de l'invariant III démontré et l'IC produit inscrit au registre (stage 04-audit) | les deux portes tiennent sur tout l'univers ; deux trous nommés : slippage_bp jamais déclaré (D01 §7), et evaluate() contournable — porte 04

## [2026-09-17] audit | Reprise du travail poussé depuis le second poste, rejoué de zéro sur celui d'Arthur (RSL_DATA_DIR = D:\quant-data\Cotations) : uv sync, validateur du catalogue, portes 01, 02 et 03 ; corrections de péremption — la note « sur cette machine » de [[reference/ou-trouver-les-donnees]] devenue fausse à deux postes, et les deux todos du catalogue qui bloquaient encore « la calibration du harnais, phase 03 » alors que la porte 03 est franchie | rien ne manquait : catalogue VALIDE, portes 01/02/03 franchies aux mêmes comptes (103 et 41 vérifications), registre 22 -> 25 lignes (3 calibrations, 0 test compté) ; restent ouverts le moteur tiers (phase 10) et les deux todos multipliers/fees

## [2026-09-17] gate | PORTE 04 FRANCHIE : D05 écrite (le nombre n'existe pas avant sa ligne — jeton délivré par le registre, `_pool` et `_deflated_t` privées, écriture par la fonction qui produit la valeur), jeton de descellage du holdout dans panel/unseal.py, registry/SCHEMA.md appliqué à l'écriture, gate_04_registry.py ; harnais modifié donc porte 03 rejouée | 1 484 vérifications ; 6 contournements essayés et refusés, 5 refus sur le holdout, 27 modules passés à l'AST ; code_hash 8c1b6512 -> 5d6ce982, les 25 lignes antérieures périmées pour un coût nul (counted_tests = 0) ; porte 03 rejouée à l'identique (IC +0,00108, t +0,06) ; L09, F15, F16 ; phase courante = 05

## [2026-09-17] decision | Banc d'essai des portes 05, 06 et 08 : D06 écrite (deux étalons, pas cinq), hypotheses/ créé avec H01 et H02 pré-enregistrées AVANT toute mesure, signals/ implémenté à la main — gao_2018 (première demi-heure) et baltussen_2021 (reste de la fenêtre), tous deux prédisant la dernière demi-heure ; scripts/check_signals.py pour les contrôles | 257 vérifications : 25 cellules sur 25, 15 822 scores chacun, médiane 633 observations par cellule, causalité vérifiée (panel tronqué = mêmes scores), accord de signe 58,3 % entre les deux ; AUCUN IC calculé, counted_tests toujours 0 ; F17, F18 ; porte 04 rejouée, 32 modules à l'AST
