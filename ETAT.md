# ÉTAT

**Phase courante :** 04 — le registre et le verrou du holdout (pas encore commencée)
**Date de dernière mise à jour :** 2026-09-17
**Dernière porte franchie :** **03**, le 2026-09-17 — `scripts/gate_03_harness.py`
passe ses 41 vérifications, sur les 25 cellules retenues. **Le harnais est figé à partir d'ici** : il ne change
que par une décision écrite, et tous les résultats antérieurs seraient alors
réputés périmés.
**Décision la plus récente :** `decisions/DECISION-04-harnais-ic.md` — IC de
Spearman en série temporelle, poolé par observations, `t` déflaté deux fois,
coût rendu comme plancher étiqueté, écriture au registre à chaque IC.
**Décision pertinente pour la phase courante :** `DECISION-04` §4 — l'invariant
III prend déjà effet (chaque IC écrit une ligne) ; la phase 04 doit en rendre le
**contournement impossible** et verrouiller le holdout. Et `registry/SCHEMA.md`,
dont les types et valeurs permises se fixent maintenant.

> Ce fichier est lu en premier par chaque session et mis à jour en dernier.
> Les phases ci-dessous suivent **l'ordre de construction** (le juge avant
> l'accusé), pas l'ordre d'exécution de la chaîne. Voir `CLAUDE.md`, « Les deux
> ordres ».

---

## Acte I — Le socle

| # | Phase | Porte | État |
|---|---|---|---|
| 01 | La décision données | `decisions/DECISION-01` fixe univers, grille, métrique, tranches ; `gate_01_pit.py` passe. | **franchie 2026-09-15** |
| 02 | Le Panel point-in-time | Un panel se charge, est reproductible ; aucune ligne n'est visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements ≤ t (D01 §6). | **franchie 2026-09-17** — `gate_02_panel.py`, 103 vérifications sur les 9 instruments |
| 03 | Le harnais d'IC calibré à la main | Le harnais reproduit à la main, sur un cas connu, un IC vérifié indépendamment. IC en série temporelle poolé, statistique robuste à la corrélation transversale, modèle de coûts par cellule (D01 §2 et §7). Figé et versionné à partir de là. | **franchie 2026-09-17** — `gate_03_harness.py`, 41 vérifications |
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
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action

**Phase 04 — le registre et le verrou du holdout.** Petite à écrire, impossible à
rattraper.

Ce qui existe déjà : `harness/registry.py` écrit une ligne à chaque IC, et
`counted_tests()` distingue les tests d'hypothèse des calibrations (`D04` §4).
Trois lignes de calibration y figurent, `hypothesis_ref: null`, hors dénominateur.

Ce que la porte exige **en plus**, et qui n'existe pas :

1. **Qu'aucun chemin de code ne puisse produire un IC sans écrire.** Aujourd'hui
   c'est vrai par construction du seul point d'entrée, mais rien ne l'empêche
   d'être contourné en important `harness.metric` directement. La porte demande
   qu'on **essaie délibérément** et qu'on n'y arrive pas.
2. **Que le holdout soit inaccessible depuis le chemin de recherche.** Le Panel
   lève déjà `HoldoutLocked` et `SliceExceeded` ; il manque le jeton de descellage
   et la preuve qu'il n'existe pas de détour.
3. **Que `registry/SCHEMA.md` fixe les types, les valeurs permises et la
   validation**, comme il annonce le faire en phase 04. Le champ `data_slice` y
   nomme encore trois tranches quand `D01` §5 n'en a laissé que deux.
