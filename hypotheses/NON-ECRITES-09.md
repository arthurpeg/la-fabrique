# Les 31 fiches du lot 09 sans hypothèse, et pourquoi

**Écrit le :** 2026-09-29, par la session qui a écrit `D40` et les dix hypothèses.
**Statut : constat, pas décision.** Rien n'est retiré du lot — il est **clos**
depuis le 2026-09-28 (`D25` `C2`, `D27`) et une session ne le rétrécit pas seule.
Ce fichier dit seulement **pourquoi** dix hypothèses ont pu s'écrire et
trente et une pas, pour que la décision qui viendra parte d'un compte et non d'une
impression.

**Ce document n'a aucune autorité.** `hypotheses/LOT-09.json` fait foi pour la
composition du lot, `scripts/gate_09.py` pour ce que la porte exige.

---

## Les trois écrans, et lequel est mécanique

**`E1` — la fiche ne porte aucune prédiction de rendement.** Notre juge corrèle un
score à un **rendement** futur (`D01` §2). Un papier qui prévoit une volatilité
réalisée, une matrice de connectedness ou un estimateur de covariance n'affirme
rien que ce juge puisse tester. **Sept de ces fiches le disent dans leurs propres
mots** — « descriptif, pas prédictif », « pas de prédiction de rendement », « rien
de ce papier ne se réplique comme signal de rendement ». Écrire une hypothèse de
rendement à partir d'elles serait inventer une affirmation que le papier ne fait
pas, c'est-à-dire la faute que `D23` `S5` nomme pour les constantes et que
l'interdit constitutionnel nomme pour les valeurs de données.

**`E2` — l'horizon ne tient pas dans une fenêtre de séance.** Et cet écran **n'est
pas une opinion** : `harness/metric.py` calcule le rendement futur en groupant par
couple *(séance, fenêtre)* **avant** de décaler, donc un horizon qui franchit une
frontière de séance ne produit **aucune observation**, jamais. Le harnais est figé
(invariant I). Un papier mensuel, hebdomadaire ou à six mois de détention n'a pas
d'hypothèse mesurable ici — c'est exactement la catégorie « horizon incompatible »
que `D27` a créée pour écarter Moskowitz, sauf que `corpus/lot_phase09.py` ne l'a
appliquée qu'aux `partiel` d'`AMORCE.md` et **jamais aux moissonnées**.

Un retard peut toujours vivre dans le **score**, qui lit librement le passé : c'est
ainsi que `H10` et `H11` sont écrites. Ce que l'écran interdit, c'est un horizon
**de détention** qui sorte de la fenêtre.

**`E3` — le signal exige une donnée ou une constante que nous n'avons pas.** Nos
barres portent `open`, `high`, `low`, `close`, `volume` à la minute, et rien
d'autre : ni carnet, ni sens des transactions. Et une constante absente de la
fiche ne s'invente pas (`D23` `S5`).

**Deux fiches sont à la frontière de `E1` et `E2`** —
`searching-for-safe-haven-assets` et `the-day-of-the-week-effect` — selon qu'on
lise leur objet ou leur horizon. Le **total de 31 ne dépend pas de ce choix** ; la
répartition par écran, si.

---

## `E1` — aucune prédiction de rendement (20)

| Fiche | Ce que le papier prédit |
|---|---|
| `andersen-bollerslev-1997-periodicity` | la **forme** de la volatilité intra-journalière. Déjà répliquée par `H04` sous `D13`, **sans aucun IC** |
| `bitcoin-is-not-the-new-gold-…` | rien : *« le papier est descriptif : il ne construit ni ne teste aucun signal prédictif »* |
| `bollerslev-2018-risk-everywhere` | une RV à 20 jours. La fiche : *« rien de ce papier ne se réplique comme signal de rendement »* |
| `corsi-2009-har-realized-volatility` | la RV du jour suivant (cascade HAR) |
| `dynamic-connectedness-between-stock-markets-…` | des spillovers de variance entre huit indices |
| `dynamic-spillovers-between-the-term-structure-…` | rien : *« papier descriptif, pas prédictif »* |
| `forecasting-oil-price-realized-volatility-…` | la RV du Brent, horizons 1 à 66 jours |
| `from-the-bird-s-eye-to-the-microscope-…` | rien : *« survey descriptif, sans stratégie ni test prédictif propre »* |
| `intraday-volatility-transmission-among-precious-…` | rien : *« descriptif, pas prédictif »* |
| `measuring-the-frequency-dynamics-of-financial-co-…` | une méthode de décomposition de connectedness par bandes de fréquence |
| `measuring-volatility-with-the-realized-range-…` | une volatilité à un jour, par un estimateur |
| `multifractal-analysis-of-financial-markets-…` | rien : c'est une **revue** |
| `on-covariance-estimation-of-non-synchronously-ob-…` | le biais d'un estimateur de covariance |
| `patton-sheppard-2015-good-volatility-bad-volatility` | la volatilité future, par semi-variances signées |
| `realized-power-variation-and-stochastic-volatili-…` | rien : *« papier de théorie des probabilités, pas de prédiction de rendement »* |
| `return-connectedness-across-asset-classes-…` | la connectedness des rendements (TVP-VAR), sans prévision |
| `scaling-properties-of-foreign-exchange-volatilit-…` | une loi d'échelle de la volatilité |
| `searching-for-safe-haven-assets-…` | le **statut de valeur refuge**, c'est-à-dire une corrélation en détresse — frontière `E1`/`E2` |
| `the-day-of-the-week-effect-on-stock-market-volat-…` | la **volatilité** conditionnelle par jour de semaine — frontière `E1`/`E2` |
| `the-impact-of-covid-19-on-g7-stock-markets-volat-…` | des régimes de volatilité GARCH |

**Ce que `E1` ne dit pas.** Aucune de ces vingt fiches n'est sans valeur : plusieurs
portent des recettes que nous utiliserons (la construction de RV de Bollerslev et
al. est complète et déterministe ; les semi-variances de Patton & Sheppard aussi).
Elles n'ont pas d'**hypothèse d'IC**, ce qui est autre chose.

## `E2` — l'horizon ne tient pas dans une fenêtre (9)

| Fiche | Horizon déclaré par la fiche |
|---|---|
| `crude-oil-prices-and-clean-energy-stock-indices-…` | **hebdomadaire**, et le modèle principal est *contemporain*, pas prédictif |
| `cryptocurrencies-and-momentum-…` | **1 mois** de détention, rééquilibrage mensuel |
| `overnight-intraday-mispricing-of-chinese-energy-…` | **mensuel**, tri en déciles sur la composante du mois écoulé |
| `performance-of-time-series-momentum-strategy-…` | une période en avant sur données **journalières**, poids issus de régressions |
| `profitability-of-technical-trading-strategies-…` | **quotidien** — et son objet est le prix de clôture officiel contre le dernier échangé |
| `realised-volatility-and-industry-momentum-return-…` | **mensuel**, fenêtre d'estimation puis période de détention |
| `short-term-momentum-effect-…-middle-east` | formation **6 mois**, détention **6 mois** |
| `speculation-and-lottery-like-demand-in-cryptocur-…` | **une semaine** (effet MAX) |
| `the-lead-lag-relation-between-vix-futures-and-sp-…` | une **fraction de seconde** — sous la résolution de nos barres d'une minute |

Le dernier est l'image inverse des huit autres : trop court, pas trop long, et
tout aussi inatteignable. Le papier conclut lui-même que le délai est trop bref
pour être exploité.

## `E3` — donnée ou constante manquante (2)

| Fiche | Ce qui manque |
|---|---|
| `boyarchenko-2023-overnight-drift` | le signal est `RSV` = (achats − ventes)/(achats + ventes), la direction d'un trade étant donnée **par comparaison au meilleur bid/ask**. Nous n'avons ni carnet ni sens des transactions : la donnée n'existe pas ici. Le motif — un déséquilibre d'ordres de fin de séance prédisant négativement la vague de liquidité suivante — est pourtant l'un des mieux formés du lot, et il est **perdu faute de données**, pas faute d'idée |
| `the-momentum-trend-reversal-…` | *« strong trend »* n'est **jamais chiffré** et les paramètres du Parabolic SAR sont **absents** : la condition d'entrée n'est pas reproductible, et l'inventer violerait `D23` `S5`. Sa jambe rentable est en outre **overnight**, donc hors fenêtre (`E2`) |

---

## Les dix qui se sont écrites

| `ref` | Fiche | Signe |
|---|---|---|
| `H05` | `baltussen-2021-hedging-demand-intraday-momentum` | +1 |
| `H06` | `bitcoin-intraday-time-series-momentum-…` | +1 |
| `H07` | `exploring-the-predictability-of-intraday-returns-…` | +1 |
| `H08` | `high-frequency-return-and-risk-patterns-…` | **−1** |
| `H09` | `intraday-time-series-momentum-global-evidence-…` | +1 |
| `H10` | `investor-clientele-and-intraday-patterns-…` | +1 |
| `H11` | `lou-2019-tug-of-war` | +1 |
| `H12` | `the-impact-of-intraday-momentum-on-stock-returns-…` | +1 |
| `H13` | `zarattini-2024-beat-the-market-spy` | +1 |
| `H14` | `zarattini-2024-profitable-day-trading-us-equity` | +1 |

**Ce que ces dix ont en commun, et il faut le voir avant de mesurer.** Cinq
d'entre elles — `H05`, `H06`, `H09`, `H10`, `H12` — sont des variantes du **même
motif** : un rendement de début de fenêtre prédisant un rendement de fin de
fenêtre, ou un rendement de créneau prédisant le même créneau. Ce motif a déjà été
mesuré ici **deux fois** et n'y était pas : `H01` (`t` final −1,56) et `H03`
(`F33`, peigne absent, `p` = 0,25). Leurs signaux seront donc **fortement
corrélés**, ce qui est précisément la raison pour laquelle `D25` exige la matrice
de corrélation du lot **avant** d'appliquer `BH` : la procédure suppose une
dépendance positive, et sans la matrice le contrôle est une hypothèse non
vérifiée.

**Une seule hypothèse porte le signe −1** (`H08`), et une seule prend un score
**sans dimension** (`H13`, normalisé par la dispersion récente). C'est un lot
étroit, et l'étroitesse est le vrai résultat de ce recensement.

## Voir aussi

- `decisions/DECISION-40-ce-qu-une-hypothese-du-lot-contient.md` — le format, le juge, et le journal où ce recensement est daté
- `decisions/DECISION-27-le-lot-de-la-phase-09.md` — le critère du lot, et § Ce qui reste ouvert : *« à la première fiche mal classée »*
- `wiki/Failed Ideas/ledger.md` `F61` — ce que cette mesure a fermé
