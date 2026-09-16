---
type: phase
updated: 2026-09-16
status: franchie
phase: 01
gate: D01 fixe univers, grille, métrique, tranches ; gate_01_pit.py passe
blocked_by: null
sources: [ETAT.md, decisions/DECISION-01-univers-et-donnees.md, scripts/gate_01_pit.py]
---

# Phase 01 — La décision données

**Franchie le 2026-09-15.**

## La porte

`decisions/DECISION-01-univers-et-donnees.md` fixe univers, grille, métrique et
tranches ; `scripts/gate_01_pit.py` passe, empreintes de préfixe déposées dans
`scripts/out/pit_fingerprints.json`.

## Pourquoi cette phase existe

La question n'était pas « quoi acheter » — les données étaient déjà là — mais
**ce que ces données permettent réellement de tester, et ce qu'elles
interdisent**. Sans cette réponse, on code des signaux contre un univers dont on
ignore la largeur, et l'appareil statistique de la phase 03 n'a pas de cible.

## Ce qui est acquis

- **L'univers** : NQ, ES, YM, GC, CL, 6E, 6B, 6J, 6A. Barres 1 minute. FDAX
  exclu, fichier conservé comme témoin hors univers (`D01` §1).
- **La grille** actif × séance : trois fenêtres disjointes ancrées à
  `America/New_York` — `ASIA` 19:00→03:00, `EUROPE` 03:00→09:30, `US`
  09:30→16:00. **25 cellules retenues sur 27** (`D01` §3).
- **La métrique** : IC en série temporelle poolé, jamais transversal. Cible d'IC
  entre 0,018 et 0,031 selon l'hypothèse d'indépendance des fenêtres — les deux
  bornes affichées, jamais la plus flatteuse seule (`D01` §2).
- **Les tranches** : `pool` 2016-01-03 → 2023-12-31 en walk-forward purgé ;
  `holdout` 2024-01-01 → 2026-08-28, **scellé jusqu'à la phase 15**, et son type
  décrit par écrit *avant* lecture (`D01` §5).
- **Le comptage des tests** : un signal sur la grille = **un** test ; les plis
  d'un walk-forward = **un** test ; sélectionner la meilleure cellule après coup
  est interdit (`D01` §4). Voir [[concepts/comptage-des-tests]].
- **Le socle du modèle de coût** : le tick de chaque contrat *mesuré* sur onze
  ans ; les frais et multiplicateurs restent `null` (`D01` §7).
- **L'intégrité point-in-time** vérifiée par empreintes de préfixe.

## Ce qui manque — ouvert volontairement

| Point | Échéance |
|---|---|
| Dates de roulement autoritatives | **bloque la phase 02** |
| Frais CME / EUREX par contrat | avant la phase 03, `null` + `todo` |
| Multiplicateurs de contrat | idem |
| Calendrier FOMC et annonces macro | phase 07 |
| Nombre et frontières des plis du walk-forward | phase 03, non tranché exprès |
| Taille de compte, positions simultanées | phase 10 — **plafonnera la largeur réellement récoltée**, qui peut retomber sous 4 |

## Pièges connus

Quatre des cinq leçons du projet viennent de cette phase : `LECONS.md` L01 à L04,
et L05 à sa charnière avec la 02. Sept des douze lignes du
[[Failed Ideas/ledger]] aussi. Avant de rouvrir quoi que ce soit ici, lire les
deux.

## Ce qui rouvrirait cette décision

`D01` § Condition de révision énumère cinq faits précis. Les deux à surveiller :
un accès Databento qui deviendrait disponible (mais voir
[[Failed Ideas/ledger]] F04 : le motif budget n'est pas le vrai motif), et des
dates de roulement autoritatives qui contrediraient le verdict « séries brutes ».

## Voir aussi

[[phases/phase-02-panel-pit]] · [[concepts/largeur-effective]] ·
[[concepts/tranche]] · [[concepts/cellule]] · [[reference/ou-trouver-les-donnees]]
