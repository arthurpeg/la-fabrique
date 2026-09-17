---
type: phase
updated: 2026-09-17
status: franchie
phase: 02
gate: un panel se charge et est reproductible ; aucune ligne visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements <= t
closed: 2026-09-17
sources: [ETAT.md, decisions/DECISION-01-univers-et-donnees.md, decisions/DECISION-03-panel-et-catalogue.md]
---

# Phase 02 — Le Panel point-in-time

**Franchie le 2026-09-17**, `scripts/gate_02_panel.py`, 103 vérifications sur les neuf instruments.
Les dates de roulement sont arrivées le jour même et la porte s'est fermée
derrière elles. Voir [[phases/phase-03-harnais-ic]] pour la suite.

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
- `panel/rolls.py` : l'ajustement à rebours, **multiplicatif** (`D01` §6 impose un
  facteur d'échelle uniforme ; l'additif ne préserverait pas les rendements —
  [[Failed Ideas/ledger]] F14). L'écart ne se lit qu'au rendement d'une minute à la
  minute de raccord : il emporte donc un peu de mouvement réel, **mesuré** par la
  porte (5,0 bp injectés, 5,0 bp absorbés) plutôt que passé sous silence.
- `scripts/gate_02_panel.py` : les clauses de la porte, 103 vérifications, tout l'univers.

## Ce qui manque — et c'est tout ce qui manque

Plus rien. Les dates sont au catalogue (`catalogue/roll_dates.json`, 527
roulements), obtenues par `symbology.resolve` chez le fournisseur, **facturé
0,00 $**. `panel.adjusted()` construit la série ; `RollDatesMissing` ne se lève
plus que pour un instrument dont les dates manqueraient.

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

## Par où les dates s'obtiennent — vérifié le 2026-09-17

Elles ne sont récupérables ni des fichiers (le parquet ne porte que
`open, high, low, close, volume, ts_event` et une métadonnée de 104 caractères :
**aucune identité de contrat par ligne**), ni du dépôt de données (deux commits,
aucun script de génération), ni d'une règle de calendrier — `.v.0` roule au
**basculement de volume**, pas à une date.

Mais elles existent chez le fournisseur. Databento expose
`Historical.symbology.resolve` : pour un symbole et une fenêtre de dates, il rend
une liste d'intervalles `{d0, d1, s}` — début effectif, fin effective, symbole
résolu. Avec `stype_in=continuous` (`NQ.v.0`) et `stype_out=raw_symbol` sur
2016-01-03 → 2026-08-28, **chaque `d0` est une date de roulement** et `s` nomme
l'échéance. C'est une requête de symbologie, pas un téléchargement de données.

À demander à l'auteur des données, qui a la clé d'API. **L'endpoint est documenté
comme facturé $0.00** — Databento mètre les données au volume livré, pas la
symbologie ni les métadonnées ; obtenir les dates ne rouvre donc pas le budget de
[[Failed Ideas/ledger]] F04. Réserve restante : la longueur de fenêtre acceptée en
un appel. En cas de doute, `metadata.get_cost` chiffre une requête avant de la
lancer.

Détail utile pour la comparaison : Databento classe les échéances **par le volume
de la veille**, donc la bascule prend effet le jour suivant le croisement. Le
raccord, lui, tombe à 00:00 UTC (`scripts/out/a2_roll_diagnostics.json`,
« vendor hypothesis, supported », queue 20 à 25 fois plus lourde qu'aux autres
minutes).

## Ce que la comparaison a donné — fait le 2026-09-17

`scripts/compare_rolls.py`, exécuté **avant** l'adoption comme `D01` §6 l'exige.
Le détecteur de la phase 01 retrouve **331 des 527 roulements — 62,8 %** — et
date **67 événements qui n'en sont pas**. De 97,6 % (6E) à 38 % (6B) et 0 %
(FDAX). Le compte annuel le faisait paraître à 90 % parce que manques et faux
positifs se compensent (`LECONS.md` **L06**).

Deux corrections de fait en sont sorties : GC ne roule pas mensuellement mais
5,07 fois par an (**L07**), et FDAX **oscille** — 24 retours à une échéance déjà
quittée. Et un coût plus large qu'annoncé : 41 des 333 roulements visibles à
mi-2023 tombent hors barre, et l'ajustement y absorbe une fermeture entière —
jusqu'à 3 648 bp (**L08**).

## Voir aussi

[[phases/phase-01-decision-donnees]] · [[phases/phase-03-harnais-ic]] ·
[[concepts/point-in-time]] · [[concepts/roulement]] · [[concepts/tranche]]
