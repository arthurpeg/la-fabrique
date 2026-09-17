# ÉTAT

**Phase courante :** 06 — contrôles automatiques et réplication (pas encore commencée)
**Date de dernière mise à jour :** 2026-09-17
**Dernière porte franchie :** **05**, le 2026-09-17 — `scripts/gate_05_signal_api.py`,
29 vérifications. Les trois look-ahead injectés (`sandbox/tainted.py`) sont
**attrapés**, chacun pour la raison écrite d'avance ; les deux étalons passent
16 sondes sans une divergence. Avant elle, **04** le même jour —
`gate_04_registry.py`, 1 843 vérifications, fin de l'Acte I.
**Décision la plus récente :** `decisions/DECISION-07-contrat-de-signal.md` — un
signal est un module qui expose `SIGNAL_ID`, `HYPOTHESIS`, `PAPER`,
`EXPECTED_SIGN` et `scores(panel, cells, horizon_bars)` ; il est refusé s'il
importe hors liste blanche ; et il n'est causal que si, pour chaque barre scorée,
tronquer le panel juste après elle rend **exactement** le même score, index
compris.
**Décision pertinente pour la phase courante :** `D07` § Ce qui reste ouvert —
les contrôles de dégénérescence (signal constant, 99 % de NaN, doublons) sont
explicitement renvoyés à la phase 06, c'est sa porte. Et `D06`, pour les deux
étalons sur lesquels ces contrôles s'exerceront.

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
| 05 | API de signal, sandbox, test de causalité | Un signal qui tente de lire le futur échoue au test de causalité, automatiquement. | **franchie 2026-09-17** — `gate_05_signal_api.py`, 3 tricheurs sur 3 attrapés, `D07` |
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

**Phase 06 — contrôles automatiques et réplication.** L'Acte II est ouvert : le
juge est incontournable, le signal a un contrat, et un look-ahead injecté se fait
attraper. Ce qui manque maintenant est le filtre qui refuse un signal *avant*
qu'il atteigne le harnais.

Ce que la porte 06 exige :

1. **Les contrôles de dégénérescence.** Un signal constant, ou à 99 % de NaN, est
   rejeté **avant** d'atteindre le harnais — donc avant de consommer une ligne de
   registre. `D07` les a explicitement renvoyés ici.
2. **Couverture, dispersion, autocorrélation, doublons par corrélation.** Une
   partie existe déjà dans `scripts/check_signals.py` et demande à devenir un
   contrôle automatique plutôt qu'un script qu'on lance à la main.
3. **Le détecteur de « trop beau pour être vrai »** : tout IC au-dessus de 0,10
   déclenche un rapport de suspicion (`hypotheses/README.md`).
4. **La réplication**, et c'est la vraie difficulté : rejouer la falsification de
   Mesfin (2026) avec **notre** modèle de coût (`corpus/AMORCE.md`, entrée 7).
   C'est la référence la plus proche de notre situation — même univers, même
   granularité, même pauvreté de données — et sa friction supposée vaut 8 à 15 bp
   quand notre tick mesuré en vaut 0,21.

**C'est ici que `H01` et `H02` seront mesurés pour la première fois**, et ce
seront les deux premiers tests comptés du projet : `counted_tests()` passera de 0
à 2. Ne pas les mesurer avant que les contrôles ci-dessus tournent — c'est
exactement l'ordre que `D06` a fixé.

**Un avertissement pour la session qui mesurera.** Les étalons produisent
13 876 observations pour 15 669 scores : 88,6 %. Les 11,4 % perdus sont des
ancres dont l'horizon de trente barres ne tient pas dans la dernière demi-heure
de leur fenêtre, et `6A × US` n'en garde que 30 % — inscrit comme exemption
écrite dans `check_signals.py`, pas comme seuil abaissé. Voir `L10`.
