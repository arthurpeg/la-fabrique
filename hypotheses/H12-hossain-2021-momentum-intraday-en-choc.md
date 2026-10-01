# H12 — Le momentum intraday, affirmé sur huit mois et demi de choc

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `the-impact-of-intraday-momentum-on-stock-returns-W4200303559` (`corpus/fiches_harvest/the-impact-of-intraday-momentum-on-stock-returns-W4200303559.json`)
**signal :** `the-impact-of-intraday-momentum-on-stock-returns-W4200303559` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches, donc elle connaît le résultat de `H01` sur ce motif. Aucun IC ne porte sur ce signal-ci au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement des **trente premières minutes**
prédit **positivement** le rendement des **trente dernières minutes** de la même
fenêtre, sur le même instrument.

Le signe est **positif**.

**C'est le troisième énoncé de ce lot à affirmer ce motif**, après `H09` (preuve
internationale) et, sous une forme voisine, `H06` (BTC au comptant). Et c'est le
même que `H01`, mesuré ici le 2026-09-18 : IC **−0,01061**, `t` final **−1,56**
(`T-20260918T065822-2b3e5d`). **L'attente écrite avant la mesure est nulle.**

**Ce que la corrélation entre ces trois hypothèses implique, et `D25` l'exigeait.**
Trois signaux qui lisent la même première demi-heure pour prédire la même
dernière demi-heure seront fortement corrélés. C'est exactement pourquoi `D25`
demande la **matrice de corrélation du lot avant d'appliquer `BH`** : la
procédure suppose une dépendance positive, et sans la matrice le contrôle est une
hypothèse non vérifiée. Cette hypothèse-ci est une des trois qui rendent cette
matrice indispensable plutôt que décorative.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre de séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule.**
- **Données :** OHLCV à la minute.
- **Et une chose que ce papier impose de dire :** son échantillon va du
  2020-01-01 au 2020-09-11, **huit mois et demi d'un unique régime de choc**.
  C'est le défaut même que `D01` §5 reproche au bloc `validation` abandonné, et
  que `F07` a inscrit au ledger : *deux ans d'un unique régime ne valident qu'un
  régime*. Notre `pool` couvre 2016-2023, donc ce sous-intervalle y est **noyé**,
  et l'hypothèse porte sur les huit ans, pas sur les huit mois.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **−0,015 à +0,02** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

La fourchette est celle de `H09`, pour la même raison : elle doit contenir le
−0,01061 déjà mesuré sur ce motif.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `sp500_first_half_hour_slope_insample` | 0.102 |
| `sp500_r2_first_half_hour_insample` | 0.048 |
| `csi300_r2_first_half_hour_insample` | 0.005 |
| `sp500_monday_first_half_hour_tstat` | 4.11 |
| `sp500_half_hour_intervals_per_day` | 13 |

**Le chiffre le plus instructif est le troisième.** Le même motif, testé la même
année sur le CSI300, rend un R² de **0,005** contre **0,048** sur le S&P500 : un
facteur dix entre deux marchés, sur huit mois et demi. Un effet qui varie autant
d'un marché à l'autre sur un échantillon aussi court n'annonce pas un effet
stable sur neuf futures et huit ans.

Et la fiche ajoute ce qui achève de dater ces chiffres : *« aucun test hors
échantillon »*, les auteurs écrivant eux-mêmes que leur base est courte et
intégralement en échantillon. Aucun de ces chiffres n'est un IC.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le motif existe à
  l'envers. `H01` a rendu −1,56, donc cette issue est à un cran de l'observé.
- Un `t` final sous **2** : rien à distinguer du bruit — l'issue attendue.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument. Ici la suspicion doit porter en particulier sur `ES`, `NQ` et
  `YM` en fenêtre US, seuls proches de l'objet du papier ; un effet qui n'y
  vivrait que là serait le résultat du papier, pas une généralité.
- Un IC positif qui ne tiendrait qu'en **2020** : ce serait la confirmation du
  papier **et** la démonstration qu'il ne se transpose pas hors de son régime.
  La ventilation par année est un diagnostic que `D29` a explicitement renvoyé au
  harnais et qui n'existe pas encore — donc ce contrôle-là ne pourra pas être
  fait à cette mesure, et il faut l'écrire plutôt que de le supposer disponible.
- Un IC net négatif au coût **borne haute** de `D26`.

## Ce qui n'est pas affirmé ici

Les trois conditionnements du papier — **signe** du rendement du premier segment
(pente 0,219 quand il est positif contre 0,102 en général), **terciles de
volatilité et de volume**, et le **lundi matin** — ne sont pas testés. Ils
appartiennent aux régimes (phase 13) et devront être pré-enregistrés séparément.
Le « lundi matin » est en outre un sous-échantillon dont la fiche note que **la
taille n'est jamais donnée**.

L'**avant-dernière demi-heure** comme prédicteur n'est pas affirmée : le papier la
trouve sans pouvoir prédictif sur le S&P500, ce qui en fait au mieux une
hypothèse nulle pré-enregistrée, et elle n'est pas dans ce lot.
