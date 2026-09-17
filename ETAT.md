# ÉTAT

**Phase courante :** 03 — le harnais d'IC calibré à la main (pas encore commencée)
**Date de dernière mise à jour :** 2026-09-17
**Dernière porte franchie :** **02**, le 2026-09-17 — `scripts/gate_02_panel.py`
passe ses 43 vérifications. La porte 01 a été rejouée le même jour : empreintes
identiques à la ligne de base du 2026-09-15.
**Décision la plus récente :** `decisions/DECISION-03-panel-et-catalogue.md` — le
paquet `panel/`, la coupe poussée dans le lecteur Parquet, le catalogue et son
validateur, l'ajustement des roulements. Deux compléments datés du 2026-09-17.
**Décision pertinente pour la phase courante :**
`decisions/DECISION-01-univers-et-donnees.md` **§2** (IC en série temporelle
poolé, statistique robuste, FDR dès le premier test) et **§7** (le modèle de
coûts par cellule, de première classe dès la phase 03).

> Ce fichier est lu en premier par chaque session et mis à jour en dernier.
> Les phases ci-dessous suivent **l'ordre de construction** (le juge avant
> l'accusé), pas l'ordre d'exécution de la chaîne. Voir `CLAUDE.md`, « Les deux
> ordres ».

---

## Acte I — Le socle

| # | Phase | Porte | État |
|---|---|---|---|
| 01 | La décision données | `decisions/DECISION-01` fixe univers, grille, métrique, tranches ; `gate_01_pit.py` passe. | **franchie 2026-09-15** |
| 02 | Le Panel point-in-time | Un panel se charge, est reproductible ; aucune ligne n'est visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements ≤ t (D01 §6). | **franchie 2026-09-17** — `gate_02_panel.py`, 43 vérifications |
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
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | barèmes publics, à dépouiller | calibration du harnais, phase 03 |

## Prochaine action

**Phase 03 — le harnais d'IC, calibré à la main.** C'est le juge, et la porte la
plus importante du projet : à partir d'elle, le harnais est **figé et versionné**.

Ce qu'elle exige, et que `D01` impose déjà : IC en **série temporelle, poolé**
entre instruments et entre cellules (l'IC transversal est refusé, ledger F03) ;
une statistique robuste à la corrélation contemporaine — un t de Student naïf
serait surévalué d'un facteur proche de `sqrt(9 / 4,2) ≈ 1,46` ; un **FDR dès le
premier test**, jamais un t-stat à 2 (Harvey, Liu & Zhu : `t > 3,0`) ; les **deux
comptes de largeur** affichés, donc les deux cibles d'IC — 0,018 et 0,031 —
jamais la plus flatteuse seule ; et le **modèle de coûts par cellule** en
première classe (`D01` §7).

La porte se franchit en reproduisant **à la main**, sur un cas connu, un IC que
le harnais retrouve indépendamment.

**Ce qui manquera en route :** les frais CME/EUREX et les multiplicateurs de
contrat, `null` et `todo` au catalogue. Ils ne bloquent pas l'écriture du
harnais ; ils bloquent sa **calibration en coûts**. Ne pas les deviner.
