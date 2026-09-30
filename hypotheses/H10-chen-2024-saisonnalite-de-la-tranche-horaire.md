# H10 — Le rendement d'une tranche horaire revient à la même tranche le lendemain

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `investor-clientele-and-intraday-patterns-in-the-W4401073178` (`corpus/fiches_harvest/investor-clientele-and-intraday-patterns-in-the-W4401073178.json`)
**signal :** `investor-clientele-and-intraday-patterns-in-the-W4401073178` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches, **donc elle connaît `F33`** — le peigne de Heston, qui est ce motif exactement, a été mesuré absent sur nos données. Voir ci-dessous. Aucun IC ne porte sur ce signal-ci au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Le rendement d'une **demi-heure donnée à la séance précédente** prédit
**positivement** le rendement de la **même demi-heure de la séance courante**, sur
le même instrument.

Le signe est **positif**.

**Le retard est dans le score, jamais dans l'horizon.** `harness/metric.py`
groupe les rendements futurs par couple *(séance, fenêtre)*, donc un horizon
franchissant une frontière de séance ne produit **aucune observation**, et le
harnais est figé (invariant I). Le score est une quantité **passée** — le
rendement du même créneau hier — et la demi-heure prédite est celle
d'**aujourd'hui**, mesurée à l'intérieur de sa fenêtre. C'est la seule forme
mesurable de ce motif ici.

**Ce motif a été mesuré sur nos données et il n'y est pas.** `H03`,
pré-enregistrée puis mesurée le 2026-09-18, a testé le peigne de Heston sur
**52 décalages** et environ 650 000 observations par décalage. Résultat, inscrit
au ledger sous `F33` : dents à **+0,00065** de médiane contre creux hors
retournement court à **+0,00056**, séparation **+0,00009**, Mann-Whitney
`p` = **0,25**. Le plus grand `t` des 40 dents vaut **+3,01** quand la sélection
seule sur 40 tirages de bruit rend un 95ᵉ centile de **3,22**. Seul le
retournement court ressort, au décalage `j` = 1, **de signe négatif**
(IC −0,0115, `t` −6,14).

**Ce que cette hypothèse ajoute, et pourquoi elle coûte quand même un test.**
Elle est au **lot clos** (`D25` `C2`, `D27`), donc elle se mesure. Ce qui est neuf :
`H03` testait le peigne **entier** — 40 dents, 12 creux, un seul motif prédit — là
où cette fiche affirme le **décalage d'une séance** seul, celui que `H03` a trouvé
**négatif et fortement significatif**. L'affirmation du papier et la mesure du
dépôt sont donc **en opposition directe sur le même objet**, et c'est le cas le
plus intéressant du lot : le test unilatéral au signe `+1` de `D25` `C1` rendra un
`p` proche de 1 si notre mesure se répète, ce qui est une **réfutation**, pas un
signal manqué de peu.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** une demi-heure, **intra-fenêtre**. Le décalage d'une séance est
  dans le score (voir ci-dessus).
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance, par cellule et par tranche horaire retenue.**
- **Données :** OHLCV à la minute. Le papier calcule ses rendements sur le
  **point milieu bid-ask**, pour neutraliser le rebond d'écart ; nous n'avons
  **ni bid ni ask**. La transposition prend la clôture de barre, et l'écart de
  cotation reste donc dans le bruit du score — écrit avant la mesure, pas
  découvert après.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** (l'affirmation du papier) |
| Magnitude plausible | **−0,015 à +0,01** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

La fourchette est **centrée sur le négatif** parce que `H03` a mesuré −0,0115 au
décalage d'une séance. Écrire une fourchette positive après avoir lu ce chiffre
serait écrire contre une mesure connue ; garder le **signe pré-enregistré à +1**
est en revanche obligatoire, c'est celui du papier (`D25` `C1`).

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `us_hks2010_lag1_coefficient_pct` | 1.19 |
| `uk_lag1_coefficient_pct` | 1.82 |
| `china_all_a_shares_lag1_coefficient_pct` | 0.36 |
| `china_excl_first_last_halfhour_lag1_coefficient_pct` | 0.13 |
| `uk_hml_portfolio_lag1_bp` | 4 |

**La quatrième ligne est celle qui prédit le plus pour nous.** Une fois ôtées la
**première et la dernière** demi-heure de séance, le coefficient tombe de 0,36 à
**0,13** : l'effet vit presque entièrement aux deux extrémités de la séance. Nos
fenêtres de séance ont des extrémités elles aussi, mais ce sont celles du
catalogue, pas celles d'un marché d'actions à enchère d'ouverture.

Aucun de ces chiffres n'est un IC : ce sont des pentes de Fama-MacBeth en coupe
transversale sur des centaines à des milliers d'actions. **Neuf futures ne forment
pas cette coupe** (`F03`, 4,22 paris indépendants), et la transposition est
série-temporelle par instrument — c'est la fiche qui la nomme ainsi.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : le motif existe à
  l'envers. **C'est l'issue que `H03` rend la plus probable** (−0,0115, `t` −6,14
  au même décalage), et elle est écrite ici avant la mesure.
- Un `t` final sous **2** : rien à distinguer du bruit.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument.
- Un IC positif qui ne tiendrait qu'aux **tranches d'extrémité** de fenêtre :
  ce serait cohérent avec le **0,13** du papier hors extrémités, mais ce ne serait
  plus le motif affirmé — ce serait un effet d'ouverture et de clôture, et il
  faudrait une hypothèse séparée pour le dire.
- Un IC net négatif au coût **borne haute** de `D26`. Le papier annonce des
  rendements de portefeuille de **0,5 à 4 bp par demi-heure**, bruts, sur points
  milieux : l'aller-retour se paie à chaque demi-heure.

## Ce qui n'est pas affirmé ici

Les **décalages de 2 à 40 séances** ne sont pas testés : `H03` les a déjà couverts
et `F33` les a réputés absents. Les tester de nouveau serait 39 hypothèses
supplémentaires au dénominateur pour un motif déjà mesuré.

Le **mécanisme** n'est pas affirmé : composition particuliers / institutionnels,
règle T+1, limites de prix, inclusion MSCI — rien de cela n'est observable sur des
futures, et le papier y attache l'essentiel de son explication.

Le **renversement** au décalage de neuf demi-heures
(`china_same_interval_reversal_lag9_halfhours_coefficient_pct` = −0,58) est une
hypothèse distincte, de signe opposé, non testée ici.
