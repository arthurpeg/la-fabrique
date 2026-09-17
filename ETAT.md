# ÉTAT

**Phase courante :** 02 — le Panel point-in-time (commencée ; porte fermée)
**Date de dernière mise à jour :** 2026-09-17
**Dernière porte franchie :** **01**, le 2026-09-15 — `scripts/gate_01_pit.py`
passe, empreintes de préfixe déposées dans `scripts/out/pit_fingerprints.json`.
Rejouée le 2026-09-17 sur la machine courante : empreintes identiques.
**Décision la plus récente :** `decisions/DECISION-03-panel-et-catalogue.md` — le
paquet `panel/`, la coupe poussée dans le lecteur Parquet, le catalogue et son
validateur. Ouvre la phase 02 sans franchir sa porte.
**Décision pertinente pour la phase courante :**
`decisions/DECISION-01-univers-et-donnees.md` — univers, grille actif × séance,
métrique, tranches, traitement des roulements — et `DECISION-03`.

> Ce fichier est lu en premier par chaque session et mis à jour en dernier.
> Les phases ci-dessous suivent **l'ordre de construction** (le juge avant
> l'accusé), pas l'ordre d'exécution de la chaîne. Voir `CLAUDE.md`, « Les deux
> ordres ».

---

## Acte I — Le socle

| # | Phase | Porte | État |
|---|---|---|---|
| 01 | La décision données | `decisions/DECISION-01` fixe univers, grille, métrique, tranches ; `gate_01_pit.py` passe. | **franchie 2026-09-15** |
| 02 | Le Panel point-in-time | Un panel se charge, est reproductible ; aucune ligne n'est visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements ≤ t (D01 §6). **Bloqué par** les dates de roulement autoritatives, demandées à l'auteur des données. | **en cours** — `panel/` et le catalogue écrits ; `scripts/gate_02_panel.py` passe les deux premières clauses, échoue sur la troisième |
| 03 | Le harnais d'IC calibré à la main | Le harnais reproduit à la main, sur un cas connu, un IC vérifié indépendamment. IC en série temporelle poolé, statistique robuste à la corrélation transversale, modèle de coûts par cellule (D01 §2 et §7). Figé et versionné à partir de là. | à faire |
| 04 | Le registre et le verrou du holdout | Aucun chemin de code ne produit un IC sans écrire au registre ; la tranche `holdout` (2024-01-01 → 2026-08-28) est inaccessible par construction. | à faire |

## Acte II — Automatiser le jugement

| # | Phase | Porte | État |
|---|---|---|---|
| 05 | API de signal, sandbox, test de causalité | Un signal qui tente de lire le futur échoue au test de causalité, automatiquement. | à faire |
| 06 | Contrôles automatiques et réplication | Le harnais réplique un résultat publié connu, contrôles compris, sans intervention. Première cible : la falsification de Mesfin (2026) rejouée avec notre modèle de coût (`corpus/AMORCE.md`, entrée 7). | à faire |
| 07 | Triage et extraction sur 20 papiers connus | 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict humain de référence. Point de départ : `corpus/AMORCE.md`. | à faire |
| 08 | Le codeur de signal | Une fiche produit un signal exécutable qui passe la sandbox, sans retouche manuelle. | à faire |

## Acte III — Fermer la boucle une fois

| # | Phase | Porte | État |
|---|---|---|---|
| 09 | Premier passage complet sur 30 à 50 papiers | La chaîne tourne de bout en bout ; le registre compte tous les tests ; un rapport d'IC existe pour chaque signal. | à faire |
| 10 | Une stratégie, un backtest | Un signal survivant devient une stratégie backtestée. Une décision écrite fixe l'attache du moteur tiers — ou, s'il n'est pas arrivé, requalifie la phase en « construire un moteur » (3 à 5 semaines estimées, D01). | à faire |

## Acte IV — Étendre par risque croissant

| # | Phase | Porte | État |
|---|---|---|---|
| 11 | Taxonomie data-driven | Les familles de signaux sont déduites des données, pas postulées. | à faire |
| 12 | Combinaisons | Toute combinaison testée a une hypothèse écrite et horodatée avant son résultat. | à faire |
| 13 | Régimes | Idem pour les hybrides. Le nombre de régimes est justifié, pas ajusté après coup. | à faire |
| 14 | Générateur d'hypothèses | Le générateur s'alimente de `LECONS.md` et du registre ; ses propositions passent les mêmes portes. | à faire |
| 15 | Le holdout | Ouvert une fois. Sharpe dégonflé du nombre de tests du registre. Fin. | à faire |

---

## Ce qui bloque, et qui n'est pas de notre ressort

| Attendu | De qui | Bloque |
|---|---|---|
| Dates de roulement autoritatives, et confirmation « brutes ou ajustées » | auteur des données | **phase 02** |
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | barèmes publics, à dépouiller | calibration du harnais, phase 03 |

## Prochaine action

**Phase 02, ce qui est fait** (2026-09-17, `DECISION-03`) : le catalogue
(`catalogue/catalogue.yaml`, 9 instruments dans l'univers, 25 cellules, 3 `todos`
ouverts) et son validateur ; le paquet `panel/` — un Panel s'ouvre à une date, la
coupe est poussée dans le lecteur Parquet, `truncate` ne va que vers le passé, le
holdout et la tranche sont verrouillés ; `scripts/gate_02_panel.py`, qui exécute
les trois clauses de la porte.

**Ce qui reste, et qui n'est pas de notre ressort :** la troisième clause — la
série ajustée à rebours — est **non vérifiable** tant que les dates de roulement
autoritatives ne sont pas au catalogue. `panel.adjusted()` lève
`RollDatesMissing` en les nommant. `gate_02_panel.py` sort en 1. La porte n'est
pas franchie, et ne le sera pas « provisoirement ».

**À la réception des dates :** comparer avant d'adopter — l'écart avec la
détection empirique mesure la méthode et fera une entrée dans `LECONS.md`
(`D01` §6).
