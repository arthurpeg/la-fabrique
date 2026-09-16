---
type: phase
updated: 2026-09-16
status: bloquee
phase: 02
gate: un panel se charge et est reproductible ; aucune ligne visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements <= t
blocked_by: dates de roulement autoritatives, demandées à l'auteur des données
sources: [ETAT.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Phase 02 — Le Panel point-in-time

**Phase courante.** Bloquée sur un intrant externe.

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
- La définition de séance sera **déclarée par instrument au catalogue**, avec son
  horloge de référence, pas déduite d'une constante globale (`D01` §8).

## Ce qui manque

- **Les dates de roulement autoritatives**, et la confirmation « brutes ou
  ajustées », demandées à l'auteur des données. **Intrant bloquant.**
- Le calendrier de séance par instrument au catalogue (`catalogue/` est vide).
- La structure du panel elle-même.

## Ce qui est faisable maintenant, sans débloquer la porte

Chargement, calendrier de séance par instrument, structure du panel. **Mais la
porte ne peut pas être franchie sans les dates** : la série ajustée à rebours en
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
