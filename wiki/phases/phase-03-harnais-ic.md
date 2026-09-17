---
type: phase
updated: 2026-09-17
status: a-faire
phase: 03
gate: le harnais reproduit à la main, sur un cas connu, un IC vérifié indépendamment ; figé et versionné à partir de là
blocked_by: frais et multiplicateurs (calibration des coûts seulement)
sources: [ETAT.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Phase 03 — Le harnais d'IC calibré à la main

## La porte

Le harnais reproduit **à la main**, sur un cas connu, un IC vérifié
indépendamment. IC en série temporelle poolé, statistique robuste à la
corrélation transversale, modèle de coûts par cellule (`D01` §2 et §7). **Figé et
versionné à partir de là.**

## Pourquoi cette phase existe

C'est le juge, et l'ordre de construction veut le juge avant l'accusé
(`CLAUDE.md` § Les deux ordres). Tant qu'elle n'est pas franchie, il est
**interdit** d'écrire du code de stratégie ou de backtest. Voir
[[concepts/porte]].

## Ce que D01 impose déjà — contraintes, pas suggestions

- **IC en série temporelle, poolé** entre instruments et entre cellules.
  L'IC transversal est refusé : neuf instruments ne portent que ~4 paris
  ([[Failed Ideas/ledger]] F03).
- **Statistique robuste à la corrélation contemporaine.** Les résidus sont
  corrélés en coupe ; un t de Student naïf serait surévalué d'un facteur proche
  de `sqrt(9 / 4,2) ≈ 1,46`.
- Le *pooling* entre instruments est justifié par Bollerslev et al. (2018) —
  [[research/bollerslev-2018-risk-everywhere]].
- **FDR dès le premier test**, jamais un t-stat à 2. Calibrage :
  [[research/harvey-2016-cross-section]], `t > 3,0`.
- Le rapport d'IC affiche **les deux comptes de largeur** (12,40 si les trois
  fenêtres sont indépendantes, ~1 060 paris/an sinon), donc **les deux cibles
  d'IC** — 0,018 et 0,031 — jamais la plus flatteuse seule.
- **Le modèle de coût est de première classe dès ici**, pas ajouté en phase 10 :
  `spread_floor_bp` mesuré + `fee_bp` **`null`** + `slippage_bp` déclaré et
  pessimiste. Voir [[concepts/cout-aller-retour]].

## Ce qui manque

- ~~La phase 02 (le Panel)~~ — **franchie le 2026-09-17**. Le harnais lit
  désormais par [[concepts/panel]] : `Panel.open(asof=...)`, `bars()`, `adjusted()`.
- **Les frais CME / EUREX par contrat** — `null`, `todo`, sources nommées dans
  `D01` §7. Ne pas deviner : `CLAUDE.md` § Les interdits.
- **Les multiplicateurs de contrat** — idem.
- Le nombre et les frontières des plis du walk-forward, non tranchés exprès en
  phase 01.

## Pièges connus

- **Plein contre micro.** Un frais fixe de `F` dollars par contrat vaut
  `F / (P × M) × 10 000` bp. Si le multiplicateur micro vaut un dixième du plein,
  la part fixe pèse **dix fois plus lourd** en micro, à prix égal. C'est de
  l'arithmétique. Le rapport doit afficher les deux tailles côte à côte.
- **Le harnais figé est figé.** S'il doit changer, c'est une décision écrite, et
  **tous les résultats antérieurs sont réputés périmés** (`CLAUDE.md`).
- Un IC calculé hors du harnais n'existe pas — et ne doit pas pouvoir exister
  (invariant III). Voir [[concepts/registre]].

## Voir aussi

[[phases/phase-02-panel-pit]] · [[concepts/ic]] · [[concepts/comptage-des-tests]] ·
[[concepts/cout-aller-retour]] · [[reference/metrique-et-comptage]]
