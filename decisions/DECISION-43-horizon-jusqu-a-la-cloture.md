# D43 — Le harnais mesure aussi l'horizon « jusqu'à la clôture de la fenêtre »

**Date :** 2026-10-01
**Phase :** 09
**État :** prise le 2026-10-01 — patch appliqué par un agent **sur instruction explicite de l'opérateur** (« rajoute au harnais les différents horizons »), qui lève pour ce seul geste la règle de l'invariant I. Ferme le point ouvert de `D42`.

## La question

`D42` fait mesurer chaque hypothèse à son propre horizon intraday. Le harnais ne
savait mesurer que des horizons **fixes**, comptés en barres (`15min`, `2h`). Or
quatre hypothèses du lot (`H07`, `H11`, `H13`, `H14`) ont pré-enregistré un
horizon **variable** : de la barre notée jusqu'à la clôture de sa fenêtre. Les
mesurer à un horizon fixe aurait mesuré d'autres hypothèses.

## Le choix

1. **`forward_returns(..., horizon_bars=None)`** rend, pour chaque barre, le
   rendement jusqu'à la **dernière barre de sa fenêtre et de sa séance** ; la
   dernière barre, sans avenir dans sa fenêtre, ne donne aucun rendement.
   `bars_to_close` dit combien de barres restent avant la clôture.
2. **L'horizon s'écrit `cloture`** : `horizon_to_bars("cloture")` rend `None`,
   le registre l'accepte (`HORIZON`), la mesure du lot le lit dans l'entrée.
3. **La déflation du t pour le recouvrement** (`D11`) demande un horizon en
   barres. Pour chaque cellule, c'est la **médiane** des barres restant jusqu'à
   la clôture depuis ses barres notées ; pour la ligne poolée, la **plus longue**
   de ces médianes — le sens qui dégonfle le plus, jamais celui qui flatte.
4. **La porte 03 le vérifie** (`4 bis`) : le score parfait « rendement jusqu'à
   la clôture » donne un IC de 1 sur chaque cellule mesurée ; une seconde
   implémentation, barre par barre, retrouve les rendements à 10⁻¹² ; le rapport
   porte l'horizon et son nombre de barres.

## Pourquoi

Parce qu'une hypothèse se mesure à l'horizon qu'elle a écrit (invariant IV), et
que l'horizon « jusqu'à la clôture » est celui de plusieurs papiers d'intraday
(Zarattini, Lou, Xu) : la position se tient jusqu'à la fin de la séance.

**Ce qui est sacrifié.** Une modification de plus du harnais, avant la mesure
du lot, donc sans rien en périmer ; seules les lignes de calibration écrites sous
`94b495fa7525d3b8` passent périmées. Et la déflation par la plus longue médiane
est sévère pour les cellules dont la clôture est plus proche : c'est voulu.

**Constat au passage.** Sur le score artificiel « rendement jusqu'à la clôture »,
6 cellules sur 25 sont refusées par le contrôle de dégénérescence (`D08`, moins
de 10 % de valeurs distinctes : les prix avancent par ticks). C'est le contrôle
qui fait son travail sur un signal fabriqué ; les cellules refusées sont nommées
dans le rapport.

## Ce que ça verrouille

- `harness/metric.py` (`forward_returns`, `bars_to_close`),
  `harness/evaluate.py` (`HORIZON_TO_CLOSE`, `horizon_to_bars`, la déflation),
  `harness/registry.py` (`HORIZON`) — empreinte `94b495fa7525d3b8` →
  `bfcfcae68c20a212` ;
- `scripts/gate_03_harness.py` (`4 bis`), `scripts/measure_lot.py`
  (`HARNAIS_DU_LOT`, plus de refus de `cloture`).

Patch : `decisions/DECISION-43-horizon-jusqu-a-la-cloture.patch`.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-01 | patch préparé dans une copie isolée, puis appliqué au dépôt | empreinte `bfcfcae68c20a212` ; porte 03 FRANCHIE (73 vérifications, dont `4 bis` : IC 1 sur 19 cellules, 243 rendements reproduits à 10⁻¹², déflation sur 237 barres) ; portes 04 et 06 franchies ; registre 181 → 187 (calibrations seulement), 56 tests comptés |
