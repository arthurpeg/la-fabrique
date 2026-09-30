# H11 — Le rendement d'un segment de séance persiste dans le même segment

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `lou-2019-tug-of-war` (`corpus/fiches/lou-2019-tug-of-war.json`)
**signal :** `lou-2019-tug-of-war` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches, donc elle connaît `F33` — le peigne de Heston, qui est le motif voisin, **n'est pas sur nos données**. Aucun IC ne porte sur ce signal au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Le rendement de la **fenêtre de séance précédente** d'un instrument prédit
**positivement** le rendement de la **fin de la fenêtre courante** — de la barre
scorée jusqu'à la clôture forcée de cette fenêtre — sur le même instrument.

Le signe est **positif**.

**Pourquoi c'est formulé ainsi et pas « la même fenêtre demain ».** Parce que le
harnais ne sait mesurer que cela : `harness/metric.py` groupe les rendements
futurs par couple *(séance, fenêtre)* avant de décaler, donc **un horizon qui
franchit une frontière de séance ne produit aucune observation**. Le harnais est
figé (invariant I). Le retard vit donc dans le **score**, qui est libre de lire
tout le passé, et jamais dans l'horizon, qui reste intra-fenêtre. Ce n'est pas un
contournement : c'est la seule forme sous laquelle la persistance d'un créneau
horaire est mesurable ici, et l'écrire après la mesure aurait été un bouton.

**La transposition, et qui l'a autorisée.** Le papier est **mensuel** : formation
à la fin du mois, détention le mois suivant, tri en déciles d'actions
américaines. Rien de cela n'entre dans une grille intraday à clôture forcée, et
`D27` exclut précisément les fiches à horizon incompatible. Cette fiche a
pourtant été **lue une par une le 2026-09-28** par la session qui a figé le lot,
qui a tranché — et l'a écrit dans `D27` § Journal — que *« sa décomposition
intraday/overnight est du pur OHLCV, volume compris ; ce qui ne transpose pas est
le tri en DÉCILES, c'est-à-dire le TEST du papier, pas son SIGNAL »*. La fiche
nomme elle-même la cible de réplication : *le découpage du rendement de chacun de
nos neuf contrats par segment, puis un signal de continuation par composante,
évalué en IC par le harnais*.

Ce qui est affirmé ici est donc **le motif, à notre horizon** : la persistance
d'un rendement à l'intérieur d'un même créneau horaire. Ce n'est pas le résultat
mensuel du papier, et cela ne doit pas être lu comme tel.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
  La fenêtre de séance du catalogue **remplace** la frontière ouverture/clôture
  du papier : `D01` §12 a déjà tranché que ces fenêtres sont ancrées sur
  `America/New_York`, pas sur une convention inventée par le signal (`F12`).
- **Horizon :** intra-fenêtre, jusqu'à la clôture forcée. Le **retard d'une
  séance est dans le score**, pas dans l'horizon (voir ci-dessus).
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule.**
- **Données :** OHLCV à la minute. Le **VWAP de la première demi-heure**, qui
  définit le prix d'ouverture chez les auteurs, **n'est pas disponible** : nos
  barres portent un volume et une clôture, pas un prix moyen pondéré. La
  transposition prend la clôture de barre, et ce n'est pas la même chose — c'est
  écrit ici avant la mesure, pas découvert après.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **0 à 0,03** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

**Pourquoi si bas, alors que le papier annonce des `t` de 16,83.** Parce que
`F33` a mesuré le motif voisin — la continuation d'un rendement au même créneau,
d'une séance sur l'autre, sur 52 décalages et ~650 000 observations par décalage
— et n'a rien trouvé : dents à **+0,00065** de médiane contre creux à
**+0,00056**, Mann-Whitney `p` = **0,25**. Le peigne de Heston et la persistance
intra-segment de Lou ne sont pas le même papier, mais ils reposent sur la même
idée de clientèle qui revient à la même heure. Ignorer `F33` en écrivant cette
fourchette serait repayer un cul-de-sac.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `tsmom_overnight_capm_alpha_monthly_pct` | 1.4 |
| `tsmom_close_to_close_capm_alpha_monthly_pct` | 1.29 |
| `tsmom_overnight_row_stdev_monthly_pct` | 4.24 |
| `tsmom_intraday_row_stdev_monthly_pct` | 4.85 |
| `tsmom_futures_universe_size` | 22 |
| `market_open_share_of_24h_pct` | 27 |

**Ces six lignes sont les seules du papier qui portent sur des futures**, et
c'est la raison pour laquelle elles sont citées plutôt que les alphas en actions
(3,47 % par mois, `t` = 16,83) : sur les **22** futures d'indices actions, la
prime de momentum temporel est **entièrement overnight** (1,40 % contre 1,29 % en
close-to-close) pour une volatilité **presque deux fois moindre** (4,24 % contre
7,30 %). Aucun de ces chiffres n'est un IC, et la fiche écrit que *« rien dans le
papier ne se lit directement comme notre métrique »*.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le segment se
  retourne au lieu de persister. Le papier annonce précisément un **renversement
  croisé** entre segments (alpha intraday **−3,02 %** par mois sur un tri
  overnight), donc cette issue est prévue par le papier lui-même sur l'autre
  segment.
- Un `t` final sous **2** : rien à distinguer du bruit — l'issue que `F33` rend la
  plus probable.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument. Et une concentration sur les **devises** serait particulièrement
  suspecte, les auteurs écrivant eux-mêmes que les notions d'intraday et
  d'overnight sont *« much more well-defined for equity markets »* que pour un
  future de change.
- Un IC net négatif au coût **borne haute** de `D26`. La stratégie implicite du
  papier fait environ **21** aller-retours par mois et il n'en chiffre **aucun**
  coût ; la nôtre en fait un par séance et par cellule.

## Ce qui n'est pas affirmé ici

Le signal **TugOfWar** lui-même — l'écart entre deux EWMA de demi-vie 60 mois —
n'est pas testé : sa demi-vie dépasse notre `pool` entier ramené à l'échelle de la
séance, et le papier **n'écrit jamais la valeur numérique de son lambda**
(`reason_lambda` de la fiche), donc l'implémenter exigerait d'inventer une
constante absente de la fiche — ce que `D23` `S5` interdit.

Le **renversement croisé** entre segments (un segment prédisant négativement
l'autre) est une hypothèse séparée, de signe opposé, et elle est plus proche du
cœur du papier que celle-ci. Elle n'est pas testée ici et devra être
pré-enregistrée à part si elle l'est un jour.

Rien du **mécanisme** n'est affirmé : détention institutionnelle 13-F,
comomentum, active weight et taille des ordres TAQ ne sont pas observables sur des
futures.
