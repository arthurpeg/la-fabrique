# H05 — Le rendement du reste de la journée prédit la dernière demi-heure

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `baltussen-2021-hedging-demand-intraday-momentum` (`corpus/fiches/baltussen-2021-hedging-demand-intraday-momentum.json`)
**signal :** `baltussen-2021-hedging-demand-intraday-momentum` (`signals/baltussen_2021_hedging_demand_intraday_momentum.py`, produit le 2026-09-23 par la porte 08)
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D33`. Contamination déclarée : cette session a lu `ETAT.md`, le wiki et les fiches, donc elle sait que `H01`, `H02` et `H03` sont sans résultat. Elle n'a vu **aucun IC** portant sur ce signal — le registre n'en porte aucun (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement accumulé **depuis la clôture de
la fenêtre précédente jusqu'à trente minutes avant la clôture** prédit
**positivement** le rendement des **trente dernières minutes** de la même
fenêtre, sur le même instrument.

Le signe est **positif**. C'est l'affirmation principale, et c'est elle qui se
teste : sur 4,22 paris indépendants, un signe inversé coûte plus cher qu'une
magnitude mal estimée (`hypotheses/README.md`).

**Ce que cette hypothèse ajoute à `H02`, qui portait déjà sur ce papier.** `H02`
prenait pour prédicteur le **reste de la journée** au sens du papier sur un seul
découpage ; elle a été mesurée le 2026-09-18 (IC −0,00432, `t` final −0,63,
`T-20260918T070041-18cf25`) et n'a rien trouvé. Elle ne peut pas entrer au lot,
`D28` l'interdisant pour un signal déjà mesuré. Le signal du lot est un **autre
module**, écrit par une session de codage isolée depuis la **fiche** et non
depuis `H02`, et jamais mesuré. **L'attente a priori est donc basse** : la même
famille a déjà rendu zéro sur ces neuf contrats, et il faut l'écrire avant de
regarder plutôt que de l'expliquer après.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre de séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule** — la barre dont l'horizon de
  30 minutes se termine à la clôture forcée de la fenêtre.
- **Données :** OHLCV à la minute, rien d'autre. Le mécanisme avancé par le
  papier (gamma négatif des teneurs de marché, ETF à effet de levier) n'est
  **pas** observable ici et n'est pas testé.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **0 à 0,03** en IC de Spearman |
| Cible `D01` §2 | 0,018 (fenêtres indépendantes) et 0,031 (dépendantes) |
| Seuil `BH` de `D25`/`D27` | `t` ≈ 2,8 pour le premier retenu |

La borne haute de 0,03 est délibérément plus basse que celle de `H01` (0,05) :
la famille a déjà été mesurée nulle ici. Au-delà de **0,10**, un rapport de
suspicion est déclenché (`hypotheses/README.md`), et il faudra chercher l'erreur
avant le profit.

## Ce que le papier annonce, et d'où ça vient

Recopié de `reported_results` de la fiche, au nom et à la valeur.

| Résultat | Valeur |
|---|---|
| `equity_pooled_rod_tstat` | 7.29 |
| `equity_pooled_rod_oos_r2_pct` | 2.88 |
| `equity_pooled_onfh_oos_r2_pct` | -1.71 |
| `n_futures_covered` | 60 |
| `equity_contracts_with_positive_significant_oos_r2` | 14 |

**Aucun de ces chiffres n'est une prédiction d'IC**, et la fiche le dit : le
papier mesure des `t` de régression poolée, des R² hors échantillon et des
Sharpe de portefeuilles 1/N de 8 à 21 contrats. Nous en avons neuf, et notre
juge rend un IC. Le seul chiffre qui porte une information transposable est
`equity_contracts_with_positive_significant_oos_r2` = **14 contrats sur 17** :
l'effet serait large plutôt que porté par un instrument.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** en valeur absolue :
  le motif existe à l'envers, et l'hypothèse est fausse telle qu'écrite.
- Un IC poolé dont le `t` **final** — déflaté deux fois, `D04`, `D11` — reste
  sous **2** : rien à distinguer du bruit sur cet univers. C'est l'issue qu'il
  faut attendre, `H02` ayant rendu `t` = −0,63 sur la même famille.
- Un IC positif porté par **une ou deux cellules sur 25**, les autres étant
  nulles ou négatives : ce ne serait pas le motif du papier, qui le trouve sur
  **14 contrats sur 17**, mais un accident d'instrument. La ventilation par
  cellule le montrera, et elle est un **diagnostic, pas 25 tests** (`D01` §4).
- Un IC net négatif au coût d'aller-retour **borne haute** de `D26`. Tant que
  `fee_per_contract_usd` est `null`, tout IC net lu est un **majorant**.

## Ce qui n'est pas affirmé ici

Le papier affirme aussi que l'effet est **plus fort quand le gamma net des
teneurs de marché est négatif** (`nge_interaction_coefficient` = −123,04), et
que la pression de prix **se retourne sur un à trois jours**
(`equity_two_day_reversal_coefficient` = −29,05). Ce sont deux hypothèses
distinctes : la première exige une donnée d'options que nous n'avons pas, la
seconde est un horizon multi-séances hors de notre grille à clôture forcée
(`D01` §3). Ni l'une ni l'autre n'est testée ici, et les tester après avoir vu
ce résultat serait une nouvelle hypothèse, pré-enregistrée avant et comptée en
plus.

Le **comparatif** du papier — `r_ROD` bat `r_ONFH` de Gao et al. — n'est pas
affirmé ici non plus. Il demanderait de mesurer les deux et de comparer, donc
deux tests et une troisième hypothèse sur leur différence.
