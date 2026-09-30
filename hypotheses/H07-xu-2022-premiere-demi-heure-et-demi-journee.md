# H07 — Le rendement de la première demi-heure prédit le reste de la séance

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `exploring-the-predictability-of-intraday-returns-W4307368010` (`corpus/fiches_harvest/exploring-the-predictability-of-intraday-returns-W4307368010.json`)
**signal :** `exploring-the-predictability-of-intraday-returns-W4307368010` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches. Aucun IC ne porte sur ce signal au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement des **trente premières minutes**
prédit **positivement** le rendement du **reste de la même fenêtre** — de la fin
de cette première demi-heure jusqu'à la clôture forcée de la fenêtre — sur le
même instrument.

Le signe est **positif**.

**Ce qui distingue cette hypothèse de `H01`, et c'est la cible, pas le
prédicteur.** `H01` prédisait les **trente dernières** minutes ; celle-ci prédit
**tout le reste** de la fenêtre. C'est le « momentum demi-journée » du papier,
son seul résultat significatif à 1 % sur les trois indices, et c'est une cible
différente : elle agrège, là où `H01` isolait. Un même prédicteur peut être nul
sur un segment et non nul sur l'agrégat — ou l'inverse, et c'est précisément ce
que `H01` interdit de supposer.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
  Aucune action chinoise n'entre dans l'univers par cette hypothèse.
- **Horizon :** de la fin de la première demi-heure à la clôture de la fenêtre,
  soit **une durée variable selon la fenêtre**, fixée par le catalogue et jamais
  par le signal.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule.**
- **Données :** OHLCV à la minute. Le découpage du papier en **huit** demi-heures
  avec une pause déjeuner de 90 minutes est propre au marché chinois et n'a
  **aucun équivalent** chez nous : le rôle d'amorçage qu'il attribue à la
  cinquième demi-heure (reprise d'après-midi) n'est pas transposable et n'est pas
  testé.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **0 à 0,04** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

La borne haute est un cran au-dessus de celle de `H05` et `H06` parce que la
cible agrège une fenêtre plus longue, donc porte moins de bruit de
microstructure — ce n'est pas une prédiction d'effet plus fort, c'est une
prédiction de variance de mesure plus faible.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `half_day_momentum_coefficient_shanghai_composite` | 0.1294 |
| `r1_predicts_r5_coefficient_shanghai_composite` | 0.1011 |
| `mr_strategy_trades_per_year` | 115 |
| `round_trip_cost_pct` | 0.16 |
| `annual_cost_drag_pct` | 9.6 |
| `in_sample_trading_days` | 487 |

**Le papier est un résultat négatif déguisé en résultat positif, et la fiche le
dit.** La régression univariée significative en échantillon **échoue hors
échantillon** ; les stratégies battent le buy-and-hold à coût nul et **perdent
tout excès après frais** — 115 aller-retours par an à 0,16 % l'aller-retour font
**9,6 %** de traînée annuelle. L'auteur conclut que ce sont les coûts qui
expliquent la persistance du motif. Aucun de ces chiffres n'est un IC.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le motif existe à
  l'envers. Le papier lui-même trouve un **reversal** vers la plupart des autres
  demi-heures (`refined_model_r1_coefficient_largest_negative` = −0,1357), donc
  cette issue n'est pas invraisemblable et doit être écrite avant.
- Un `t` final sous **2** : rien à distinguer du bruit, et c'est l'issue que le
  propre échec hors échantillon du papier rend la plus probable.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument.
- Un IC net négatif au coût **borne haute** de `D26`. Le papier annonce
  **9,6 %** par an de coût sur son marché ; notre grille à clôture forcée fait
  **un** aller-retour par séance et par cellule, donc la question est du même
  ordre et ne peut pas être écartée.

## Ce qui n'est pas affirmé ici

Le modèle **enrichi** du papier ajoute le rendement overnight, le rendement de
la veille et des muettes **lundi / vendredi**. Trois choses distinctes, et
aucune n'est testée ici : les muettes de jour de semaine produiraient un score à
**cinq valeurs distinctes au plus**, que le contrôle de dégénérescence du harnais
rejetterait avant tout IC (`harness/controls.py`) — ce n'est pas un signal, c'est
un régime, et il appartient à la phase 13.

Le **reversal** vers les autres demi-heures est une hypothèse séparée, de signe
opposé, et la tester après avoir vu ce résultat serait une hypothèse nouvelle,
comptée en plus.
