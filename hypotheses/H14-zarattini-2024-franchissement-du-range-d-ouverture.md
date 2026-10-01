# H14 — Le sens des premières minutes prédit le reste de la fenêtre

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `zarattini-2024-profitable-day-trading-us-equity` (`corpus/fiches/zarattini-2024-profitable-day-trading-us-equity.json`)
**signal :** `zarattini-2024-profitable-day-trading-us-equity` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches. Aucun IC ne porte sur ce signal au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Le **sens de la première bougie de cinq minutes** d'une fenêtre de séance, combiné
au **franchissement du haut ou du bas de ce range d'ouverture**, prédit
**positivement** le rendement de la fenêtre jusqu'à sa clôture forcée, sur le même
instrument.

Le signe est **positif**.

**Et l'affirmation du papier est que ce signal-là ne rapporte rien.** C'est le
seul énoncé du lot dont le papier prédit lui-même l'échec : le PnL moyen par trade
de l'ORB **non conditionné** vaut **−0,02 R**, et il ne devient **+0,08 R** qu'une
fois restreint aux titres dont le volume d'ouverture est anormalement élevé. La
fiche le dit en une ligne : *« le Relative Volume est un conditionneur de régime,
pas un prédicteur de direction »*.

**Pourquoi l'écrire quand même, et pourquoi sous cette forme.** Parce que le
conditionnement est un **régime** (phase 13) et qu'un régime ne se teste pas avant
le signal qu'il conditionne : sans mesure du signal nu, on ne saurait pas si le
régime ajoute quelque chose ou s'il sélectionne du bruit. Cette hypothèse est donc
le **témoin** de la suivante, et elle est pré-enregistrée comme telle — attendue
**nulle**, pas attendue positive.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** de la barre scorée à la **clôture forcée de la fenêtre**,
  entièrement intra-fenêtre.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule.**
- **Données :** OHLCV à la minute. Le range d'ouverture, son sens et son
  franchissement ne demandent rien d'autre.
- **Ce qui ne transpose pas, et la fiche l'écrit :** la sélection transversale des
  **20 plus forts** Relative Volume du jour suppose des milliers de candidats.
  Neuf instruments ne font pas un « top 20 » (`F03`, 4,22 paris indépendants), et
  les filtres du papier — prix > 5 $, volume ≥ 1 000 000 actions, ATR > 0,50 $ —
  sont calibrés sur le nuage des actions américaines et n'ont aucun sens sur un
  contrat à terme.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **−0,01 à +0,015** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

La fourchette est **centrée sur zéro et mord le négatif**, parce que le papier
mesure **−0,02 R** par trade pour ce signal nu. Écrire une fourchette positive
serait écrire contre le chiffre même que la fiche rapporte.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `avg_pnl_per_trade_relvol_below_100pct_in_R` | -0.02 |
| `avg_pnl_per_trade_relvol_above_100pct_in_R` | 0.08 |
| `orb_base_sharpe` | 0.48 |
| `orb_base_alpha_annual_pct` | 3.26 |
| `orb_relvol_top20_sharpe` | 2.81 |
| `orb_base_hit_ratio_pct` | 41.4 |

**La bascule de signe entre les deux premières lignes est toute l'affirmation du
papier**, et c'est aussi ce qui rend son Sharpe de **2,81** non transposable : il
est obtenu sur une sélection transversale quotidienne de 20 titres parmi 7 000.

Deux manques que la fiche nomme, et ils sont graves : **aucune inférence
statistique** — pas une `t`-stat, pas une erreur standard, pas un intervalle nulle
part, alors que les alphas de 3,26 % et 36 % par an sont annoncés — et **le nombre
de trades n'est jamais donné**, ce qui rend les moyennes en R invalidables. Un
Sharpe de 2,81 sans effectif ni écart-type d'estimation n'est pas un résultat
contre lequel on se calibre.

**Une chose à savoir sur la période, et elle est rare.** L'échantillon du papier
va du 2016-01-01 au 2023-12-31, soit **exactement notre tranche `pool`**
(2016-01-03 → 2023-12-31). Il ne touche pas notre `holdout`, ce qui est une bonne
nouvelle pour l'invariant V — et une mauvaise pour le papier, dont rien n'a jamais
été testé hors de cette fenêtre.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le franchissement du
  range annonce le retour. Ce serait cohérent avec le **−0,02 R** du papier, en
  plus net, et l'hypothèse serait fausse telle qu'écrite.
- Un `t` final sous **2** : rien à distinguer du bruit — **l'issue que le papier
  lui-même prédit**, et donc la seule dont la réalisation ne serait pas une
  surprise.
- Un IC **positif** au-delà de **0,02** : ce serait contraire au papier, qui
  mesure ce signal nu non rentable. Il faudrait alors chercher l'erreur avant le
  profit, et en premier lieu vérifier que le score ne lit pas la barre du
  franchissement elle-même — un range d'ouverture dont on saurait déjà qu'il a été
  franchi est un look-ahead, et c'est exactement la faute que `D27` a corrigée
  dans le test de causalité.
- Un IC net négatif au coût **borne haute** de `D26`, avec un taux de réussite
  annoncé à **41,4 %** : une stratégie qui perd plus souvent qu'elle ne gagne paie
  le coût à chaque tentative.

## Ce qui n'est pas affirmé ici

Le **Relative Volume** — volume de la fenêtre d'ouverture divisé par la moyenne
des quatorze mêmes fenêtres précédentes — n'est **pas** dans ce score. C'est un
conditionneur de régime, il est calculable sur nos données, et il fera l'objet
d'une hypothèse séparée, **en phase 13**, qui citera celle-ci comme son témoin.
L'inclure ici reviendrait à tester deux choses et à retenir la meilleure.

Ne sont pas affirmés non plus : le **stop à 10 % de l'ATR**, le dimensionnement à
1 % du capital par position, le plafond de levier de 4×, ni les longueurs de range
alternatives (15, 30, 60 minutes). Les trois premiers sont de la stratégie
(phase 10) ; les dernières seraient **trois hypothèses de plus** au dénominateur,
et le papier mesure justement que la rentabilité décroît quand le range s'allonge.
