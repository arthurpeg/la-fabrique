# H06 — Le rendement d'ouverture prédit la dernière demi-heure, hors crypto

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `bitcoin-intraday-time-series-momentum-W3199228172` (`corpus/fiches_harvest/bitcoin-intraday-time-series-momentum-W3199228172.json`)
**signal :** `bitcoin-intraday-time-series-momentum-W3199228172` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches. Aucun IC ne porte sur ce signal au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement accumulé **depuis la clôture de
la fenêtre précédente jusqu'à trente minutes après son ouverture** prédit
**positivement** le rendement des **trente dernières minutes** de la même
fenêtre, sur le même instrument.

Le signe est **positif**.

**La transposition, et ce qu'elle coûte.** Le papier travaille sur du BTC/USD au
comptant, sur cinq plateformes ouvertes 24 h sur 24, dont il fabrique une séance
« conventionnelle » : ouverture à l'heure du **pic de volume** (9:00-9:40 EST
selon la plateforme), clôture à 17:00 EST. Nos neuf contrats ont de **vraies**
fenêtres de séance, fixées par `D01` §3 et lues au catalogue. La transposition
remplace donc une séance inventée par une séance réelle — c'est ce que le lot
appelle une transposition d'univers (`D27`), et c'est **une amélioration des
conditions du test**, pas une dégradation : l'ancre n'est plus un artefact.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
  **Aucune crypto n'est dans l'univers** et aucune n'y entre par cette hypothèse.
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre de séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule.**
- **Données :** OHLCV à la minute. L'écart de Corwin-Schultz que le papier
  utilise pour son mécanisme est calculable, mais il n'est **pas** dans cette
  hypothèse : `F08` a mesuré que sa médiane est **exactement zéro** sur nos
  barres d'une minute pour six cellules.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **0 à 0,03** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

**Pourquoi la borne haute est basse.** Le motif est celui de la famille que
`H01` a déjà mesurée nulle sur ces mêmes contrats (`t` final −1,56,
`T-20260918T065822-2b3e5d`). Un papier de plus sur un autre actif ne rend pas le
motif plus probable **ici**.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `beta_onfh_pooled_insample` | 0.968 |
| `tstat_onfh_pooled_insample_newey_west` | 4.38 |
| `r2oos_onfh_alone_pct` | 1.09 |
| `breakeven_cost_onfh_no_leverage_bp` | 3 |
| `bitstamp_trading_fee_bp` | 25 |

**Le chiffre à lire est le couple des deux derniers, et il est écrasant.** Le
coût mort de la stratégie du papier est de **3 bp** ; les frais de la plateforme
sur laquelle il mesure sont de **25 bp**. Par ses propres chiffres, le motif
n'est pas exploitable **là où il a été trouvé**. Aucun de ces chiffres n'est un
IC, et rien ici ne doit être lu comme une prédiction d'IC.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le motif existe à
  l'envers.
- Un `t` final sous **2** : rien à distinguer du bruit. C'est l'issue attendue,
  la même famille ayant rendu `t` = −1,56 ici.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument, pas le motif du papier, qui l'annonce sur cinq plateformes.
- Un IC net négatif au coût **borne haute** de `D26` — et le papier lui-même
  échoue à ce test sur son propre marché, avec **3** bp de marge contre **25** bp
  de frais.

## Ce qui n'est pas affirmé ici

Le papier affirme aussi que **l'avant-dernière demi-heure prédit négativement**
la dernière (`beta_slh_alone_insample` = −9,778), que l'effet est **concentré les
jours de fort volume ou de forte volatilité d'ouverture**, et qu'il est **porté
surtout par la composante nocturne**. Trois hypothèses distinctes : la première
est un signal séparé de signe opposé, les deux autres sont des conditionnements
qui appartiennent aux régimes (phase 13). Aucune n'est testée ici. Les tester
après avoir vu ce résultat serait, chacune, une hypothèse nouvelle, comptée en
plus au registre.
