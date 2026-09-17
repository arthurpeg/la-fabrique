# ÉTAT

**Phase courante :** 05 — API de signal, sandbox, test de causalité (pas encore commencée)
**Date de dernière mise à jour :** 2026-09-17
**Dernière porte franchie :** **04**, le 2026-09-17 — `scripts/gate_04_registry.py`
passe ses 1 484 vérifications. Le registre est incontournable (six contournements
essayés, six refusés), le holdout est scellé derrière un jeton qui s'écrit avant
de s'obtenir, et `registry/SCHEMA.md` est appliqué à l'écriture. **Fin de
l'Acte I.**
**Décision la plus récente :** `decisions/DECISION-05-registre-incontournable.md`
— le nombre n'existe pas avant sa ligne : `_pool` et `_deflated_t` sont privées,
un IC poolé exige un jeton délivré par le registre, et la ligne est écrite par la
fonction qui produit la valeur. Le harnais a changé, donc **tous les résultats
antérieurs sont périmés** — coût réel nul, `counted_tests()` valait 0.
**Décision pertinente pour la phase courante :** `decisions/DECISION-06-signaux-de-reference.md`
— les deux étalons contre lesquels les portes 05, 06 et 08 se démontrent, et
l'interface provisoire `scores(panel, cells)` que la phase 05 doit formaliser.
Et `D05` § Ce qui reste ouvert, pour l'empreinte du **code de signal**, distincte
de celle du harnais.

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
| 04 | Le registre et le verrou du holdout | Aucun chemin de code ne produit un IC sans écrire au registre ; la tranche `holdout` (2024-01-01 → 2026-08-28) est inaccessible par construction. | **franchie 2026-09-17** — `gate_04_registry.py`, 1 484 vérifications, `D05` |

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

**Phase 05 — API de signal, sandbox, test de causalité.** L'Acte I est clos : le
juge existe, il est calibré, et on ne peut plus l'éviter. L'Acte II commence, et
c'est là que le premier agent entrera en scène — mais pas encore ici.

Ce qui existe déjà : le Panel refuse structurellement le futur (porte 02), et
`evaluate()` reçoit des **scores**, pas un signal — le harnais est délibérément
ignorant de ce qu'est un signal, et rien dans `D04` ne préjuge de cette interface.

Ce que la porte 05 exige, et qui n'existe pas :

1. **Le contrat de la fonction de signal.** Ce qu'elle reçoit (un Panel à une
   date, rien d'autre), ce qu'elle rend, et son empreinte propre — `D05` laisse
   ouvert le `code_hash` du **code de signal**, distinct de celui du harnais.
   C'est ici qu'il se fixe.
2. **Le scan AST et l'exécution isolée.** `gate_04_registry.py` §6 contient déjà
   le squelette d'un scan syntaxique du dépôt ; la sandbox de signal est un
   travail voisin, en plus strict.
3. **Le test de causalité** : recalculer le signal en ne lui donnant que le passé,
   et **attraper un look-ahead injecté exprès**. Un test qui n'a jamais rien
   attrapé n'est pas un test.

**Le banc d'essai existe depuis le 2026-09-17** — c'était le préalable, il est
levé. `D06` a tranché : **deux étalons**, pas cinq, tirés du corpus et écrits à la
main — `gao-2018-intraday-momentum` (`H01`) et
`baltussen-2021-intraday-momentum` (`H02`), avec leurs hypothèses
pré-enregistrées dans `hypotheses/` **avant** toute mesure.

**Aucun IC n'a été calculé sur eux** et `counted_tests()` vaut toujours 0 :
`scripts/check_signals.py` ne vérifie que couverture, dispersion et causalité —
257 vérifications, 25 cellules sur 25, médiane de 633 observations par cellule.
La mesure de `H01` et `H02` attend les contrôles automatiques de la phase 06.
Les cinq signaux du plan de montage (momentum 12-1, book-to-price…) sont écartés
pour de bon : transversaux, mensuels, sur actions — ledger F17.
