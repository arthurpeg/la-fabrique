---
type: phase
updated: 2026-09-17
status: en-cours
phase: 02
gate: un panel se charge et est reproductible ; aucune ligne visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements <= t
blocked_by: dates de roulement autoritatives, demandées à l'auteur des données
sources: [ETAT.md, decisions/DECISION-01-univers-et-donnees.md, decisions/DECISION-03-panel-et-catalogue.md]
---

# Phase 02 — Le Panel point-in-time

**Phase courante.** Construite aux deux tiers ; la porte reste fermée sur un
intrant externe. `scripts/gate_02_panel.py` le dit par un code de sortie.

## La porte

Un panel se charge, est reproductible ; **aucune ligne n'est visible avant son
horodatage** ; la série ajustée à rebours n'utilise que les recollements ≤ `t`
(`D01` §6).

## Pourquoi cette phase existe

L'invariant II : *le look-ahead est empêché par construction, jamais par
vigilance*. Le Panel est l'endroit où cette impossibilité se fabrique. Si le
futur est accessible ici, aucune discipline en aval ne le rattrapera — et rien ne
lèvera d'exception. Voir [[concepts/point-in-time]].

## Ce qui est acquis

- Les séries sont **brutes (recollées)**, le raccord à 00:00 UTC ; cycle
  trimestriel pour indices et devises, mensuel pour GC et CL. **L'historique ne
  se réécrira pas** (`D01` §6).
- L'empreinte de préfixe de la phase 01 (`scripts/out/pit_fingerprints.json`)
  donne le moyen de détecter une réécriture d'historique — `gate_01_pit.py` est à
  rejouer, pas à croire sur parole.
- La définition de séance est **déclarée par instrument au catalogue**, avec son
  horloge de référence, pas déduite d'une constante globale (`D01` §8).
- La porte 01 a été **rejouée le 2026-09-17** : empreintes identiques à celles du
  2026-09-15. L'historique ne s'est pas réécrit.

## Ce qui a été construit — 2026-09-17, `D03`

- `catalogue/catalogue.yaml` : 10 instruments, 9 dans l'univers, 25 cellules
  retenues, 3 `todos` ouverts. Chaque nombre y est recopié d'une mesure, et
  `catalogue/validate.py` le re-dérive de sa source à chaque exécution — il
  **réapplique la règle de rétention** au lieu de croire le drapeau.
- `panel/` : un Panel s'ouvre à une date. La coupe est **poussée dans le lecteur
  Parquet**, donc le futur n'entre jamais dans le processus ; `truncate` ne va
  que vers le passé ; le holdout et les bornes de tranche lèvent.
  Voir [[concepts/panel]].
- `scripts/gate_02_panel.py` : les trois clauses de la porte, 24 vérifications.

## Ce qui manque — et c'est tout ce qui manque

- **Les dates de roulement autoritatives**, et la confirmation « brutes ou
  ajustées », demandées à l'auteur des données. **Intrant bloquant.**
  `panel.adjusted()` existe et lève `RollDatesMissing` en les nommant.

**La porte ne peut pas être franchie sans elles** : la série ajustée à rebours en
dépend. `CLAUDE.md` § Les interdits : *ne jamais franchir une porte
« provisoirement, on y reviendra »*.

## Pièges connus

- **`LECONS.md` L05** — la détection empirique des recollements a des trous
  **systématiques et corrélés au régime** (3,4–3,6/an pour les indices là où il y
  en a 4 ; 8,5 pour CL là où il y en a 12 ; 6A pas tranché du tout). Elle ne sera
  jamais autoritative : voir [[Failed Ideas/ledger]] F09.
- **Neutraliser la barre de roulement est nécessaire et très insuffisant.** Le
  niveau de prix est discontinu : toute grandeur calculée sur une fenêtre qui
  **enjambe** un recollement est fausse *sur toute sa largeur* — volatilité
  réalisée, moyennes mobiles, momentum (`D01` §6).
- Le traitement est **au niveau du Panel, jamais au niveau du signal**. Un signal
  qui corrige lui-même un roulement est un bug d'architecture, pas une astuce.
- Le prix **brut reste disponible séparément**, pour les niveaux et l'exécution.

## À faire à la réception des dates

**Comparer avant d'adopter.** L'écart entre la liste reçue et la détection
empirique mesure la méthode et fera l'objet d'une entrée dans `LECONS.md`
(`D01` §6). Ne pas écraser silencieusement : c'est la seule occasion de chiffrer
ce que vaut le détecteur.

## Voir aussi

[[phases/phase-01-decision-donnees]] · [[phases/phase-03-harnais-ic]] ·
[[concepts/point-in-time]] · [[concepts/roulement]] · [[concepts/tranche]]
