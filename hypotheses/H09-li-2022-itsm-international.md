# H09 — Le momentum intraday de Gao, retesté sur une affirmation internationale

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `intraday-time-series-momentum-global-evidence-an-W3121499907` (`corpus/fiches_harvest/intraday-time-series-momentum-global-evidence-an-W3121499907.json`)
**signal :** `intraday-time-series-momentum-global-evidence-an-W3121499907` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D33`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches, **donc elle connaît le résultat de `H01`, qui porte sur le même motif.** Voir ci-dessous — c'est la chose la plus importante de ce fichier. Aucun IC ne porte sur ce signal-ci au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement des **trente premières minutes**
prédit **positivement** le rendement des **trente dernières minutes** de la même
fenêtre, sur le même instrument.

Le signe est **positif**.

**Ce motif a déjà été mesuré sur nos données, et il n'y était pas.** `H01`,
pré-enregistrée le 2026-09-17 et mesurée le 2026-09-18, affirmait exactement
cela : IC poolé **−0,01061**, `t` final **−1,56** après la reprise sous `D11`
(`T-20260918T065822-2b3e5d`). Le verdict était : ni confirmée, ni retournée,
rien à distinguer du bruit.

**Alors pourquoi cette hypothèse existe-t-elle, et ce qu'elle coûte.** Elle
existe parce que la fiche est au **lot clos** du 2026-09-28 (`D25` `C2`, `D27`) et
qu'un lot clos ne se rétrécit pas après coup. Elle coûte **une ligne de registre
et une unité au dénominateur de `BH`**, et cette dépense est le prix de la
clôture — pas un oubli. Ce qui est neuf par rapport à `H01` : le papier affirme
le motif sur **16 marchés développés** et sur des **futures d'indices**, pas sur
un ETF américain unique ; le signal sera écrit par une session de codage isolée
depuis la fiche, sans voir `H01` ni son résultat.

**L'attente écrite avant la mesure est donc : nulle.** L'écrire autrement après
avoir vu `H01` serait malhonnête, et ne pas l'écrire du tout laisserait croire
que le dépôt a oublié `H01`.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre de séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule** — la barre dont l'horizon de
  30 minutes se termine à la clôture forcée de la fenêtre.
- **Données :** OHLCV à la minute. Le prédicteur du papier inclut le **gap
  overnight** (`pfirst30,t / pclose,t-1 − 1`) ; chez nous la « clôture de la
  veille » est celle de la **fenêtre précédente du catalogue**, un future à
  session électronique quasi continue n'ayant pas de gap au même sens. La fiche
  nomme cette difficulté elle-même.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **−0,015 à +0,02** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

**La fourchette inclut délibérément le négatif**, et c'est le seul endroit de ces
onze hypothèses où elle le fait : `H01` a mesuré −0,01061 sur le même motif, et
une fourchette qui exclurait cette valeur serait une fourchette écrite en
ignorant une mesure connue. Le **signe pré-enregistré reste +1** — c'est
l'affirmation du papier, et `D25` `C1` exige que le test soit unilatéral au signe
annoncé, pas au signe espéré.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `pooled_first_half_hour_slope` | 2.86 |
| `pooled_first_half_hour_tstat` | 7.53 |
| `markets_with_significant_in_sample_predictability` | 12 |
| `countries_with_positive_oos_r2` | 5 |
| `gitsm_sharpe_max` | 1.77 |

**Le chiffre qui compte est le quatrième, et il n'est pas celui du résumé.** Le
papier annonce **12 marchés sur 16** significatifs *en échantillon* ; **5 sur 16**
seulement ont un R² **hors échantillon** positif. C'est un rapport de 12 à 5 entre
ce qui tient en échantillon et ce qui survit dehors, sur le motif même que nous
allons mesurer. Aucun de ces chiffres n'est un IC.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le motif existe à
  l'envers sur nos contrats. `H01` a rendu −1,56, donc **cette issue est à un
  cran de ce qui a déjà été observé** et doit être prévue.
- Un `t` final sous **2** : rien à distinguer du bruit — l'issue attendue.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument. Le papier l'annonce large (**12** marchés), la ventilation par
  cellule dira si c'est le cas ici ; elle reste un diagnostic, pas 25 tests
  (`D01` §4).
- Un IC net négatif au coût **borne haute** de `D26`. Le papier ne déduit
  **aucun** coût — ni spread, ni commission, ni slippage — alors que sa stratégie
  fait un aller-retour par jour et par marché.

## Ce qui n'est pas affirmé ici

Le papier affirme que l'effet est **plus fort en crise et en récession**
(`pooled_slope_crisis` = 3,71 contre `pooled_slope_non_crisis` = 2,09), plus fort
quand la **liquidité est faible**, et plus fort quand l'information est absorbée
**continûment**. Ce sont trois hypothèses conditionnelles : elles appartiennent
aux régimes (phase 13) et devront être pré-enregistrées séparément. Les tester en
même temps que celle-ci et retenir la meilleure serait exactement ce que le
registre existe pour rendre visible.

Le **portefeuille global** du papier — 18 pondérations, Sharpe jusqu'à 1,77 — n'est
pas affirmé ici : il suppose une allocation transversale que 4,22 paris
indépendants ne soutiennent pas (`F03`).
