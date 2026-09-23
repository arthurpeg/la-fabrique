# D25 — Le budget de tests de la phase 09

**Date :** 2026-09-23
**Phase :** 09
**État :** prise

## La question

La phase 09 est la première qui **dépense des tests** : chaque signal mesuré
écrit une ligne au registre, et ce nombre sert à dégonfler le résultat final en
phase 15. Trois choses doivent être fixées **avant** de lancer quoi que ce soit —
combien d'essais, quel seuil, quelle règle d'arrêt — faute de quoi elles seront
choisies par accident, et après coup.

## Ce que les données imposent, et qui n'était pas su

Deux mesures faites le 2026-09-23, avant toute délibération.

**La conversion IC → `t` est fixée par nos données**, et elle se vérifie sur le
registre. Avec 45 908 observations poolées et la déflation transversale de `D11`
(÷ √(9/4,224) = ÷1,460 ; le recouvrement est **neutre** pour un score par
séance, écart 390 > horizon 30) :

```
t = IC × 146,8
```

*Vérification : `H01` inscrite au registre avec IC = −0,0106 et `t` = −1,5579 ;
la formule donne −1,5559.*

**La cible économique et le seuil statistique tombent au même endroit**, et c'est
le fait le plus utile de cette décision. `D01` §2 fixe l'IC requis pour un IR de
1 entre **0,018** et **0,031** selon l'indépendance des fenêtres. Traduit :

| IC | `t` |
|---|---|
| 0,018 (optimiste, ~3 100 paris/an) | **2,64** |
| 0,031 (pessimiste, ~1 060 paris/an) | **4,55** |

Il n'y a donc **pas d'arbitrage** entre « statistiquement solide » et
« économiquement utile » : c'est la même fenêtre. Un signal à `t` = 2,0 n'est pas
un signal faible mais réel — il est **économiquement sans intérêt** de toute
façon.

## Les options

**1. Un seuil plat, `t > 3`.** C'est la recommandation de Harvey, Liu & Zhu
(2016), déjà citée par `wiki/concepts/comptage-des-tests.md`. Écartée comme
**règle de décision**, gardée comme repère : un seuil plat ne dépend pas du
nombre d'essais, donc il est trop laxiste si on en fait mille et trop sévère si
on en fait dix. Il ne répond pas à la question posée.

**2. Bonferroni — contrôler la probabilité de la MOINDRE fausse découverte.**
Écartée, et c'est l'option que l'intuition suggère. Mesurée par simulation le
2026-09-23, 4 000 répétitions, test unilatéral :

| N | vrais signaux trouvés, Bonferroni | vrais signaux trouvés, BH |
|---|---|---|
| 20 | 0,87 | **1,28** |
| 50 | 1,63 | **2,94** |
| 100 | 2,61 | **5,74** |
| 200 | 4,04 | **11,39** |

*(10 % de vrais signaux, effet vrai `t` = 2,64 — la cible optimiste de `D01`.)*

À 100 essais, Bonferroni en trouve **2,6 quand il y en a 10** ; `BH` en trouve
**5,7**. Bonferroni protège contre une faute qu'on ne cherche pas à éviter à tout
prix — une seule fausse découverte sur une poignée retenues est acceptable, dès
lors qu'on la compte.

**3. Benjamini–Hochberg (FDR) à `q` fixé.** Retenue.

**4. Ne pas fixer de budget et « voir venir ».** Écartée. C'est celle qui se
choisit toute seule quand on ne décide pas, et elle est la pire : le
dénominateur devient le nombre qu'on se rappelle, pas celui qu'on a dépensé.

## Le choix

**La phase 09 contrôle le taux de fausses découvertes par Benjamini–Hochberg à
`q` = 0,10, en test unilatéral au signe pré-enregistré, sur un lot de `N` = 50
signaux fixé et clos avant la première mesure.**

Quatre clauses, qui valent ensemble.

**C1 — Le test est unilatéral, au signe déclaré.** `D07` exige déjà
`EXPECTED_SIGN` ∈ {+1, −1}, écrit **avant** toute mesure. Un test bilatéral
jetterait cette information et coûterait environ 20 % de puissance pour rien. Un
signal dont l'IC est significatif **à l'envers du signe prédit** n'est pas une
découverte : c'est une réfutation, inscrite comme telle.

**C2 — Le lot est clos avant la première mesure.** Les 50 fiches sont désignées,
leurs hypothèses pré-enregistrées, **puis** tout est mesuré, **puis** `BH` est
appliqué sur les 50 `p` ensemble. Regarder un résultat au milieu et décider de
continuer ou d'arrêter casse la procédure : `BH` n'est valide que sur une
famille close.

**C3 — `q` = 0,10.** Sur les signaux retenus, un sur dix sera faux en moyenne. À
trois ou quatre survivants, cela veut dire *« il y a de fortes chances qu'ils
soient tous vrais, et il n'est pas exclu qu'un soit du bruit »*. C'est le niveau
qu'un opérateur seul peut assumer, parce que la phase 10 le vérifiera encore par
un backtest, et la phase 15 par le holdout.

**C4 — Le dénominateur de la phase 15 reste le registre ENTIER.** `BH` contrôle
la **sélection** à l'intérieur du lot ; le Sharpe dégonflé de la phase 15
contrôle **l'affirmation finale** et compte tous les tests jamais écrits, les 56
antérieurs compris. Deux corrections, deux moments, deux objets. Aucune ne
remplace l'autre.

### Ce que ça donne concrètement

Échelle de `BH` pour `N` = 50, `q` = 0,10 :

| Rang du signal retenu | `p` max | `t` requis | IC requis |
|---|---|---|---|
| le 1ᵉʳ | 0,0020 | **2,88** | 0,0196 |
| le 2ᵉ | 0,0040 | 2,65 | 0,0181 |
| le 3ᵉ | 0,0060 | 2,51 | 0,0171 |
| le 5ᵉ | 0,0100 | 2,33 | 0,0158 |

À comparer : Bonferroni exigerait `t` = 3,09 pour le premier, **et autant pour
tous les suivants**.

La propriété qui justifie le choix : **plus il y a de vrais signaux, plus la
barre descend**. C'est exactement ce qu'on veut d'une procédure qui doit
« maximiser les vrais résultats sans se faire avoir par le hasard ».

## Pourquoi

**Le budget n'est pas un plafond, c'est un protocole** — et c'est le
retournement que cette décision opère.

L'intuition dit : « chaque test supplémentaire me coûte, donc j'en fais le moins
possible ». Elle est **juste sous Bonferroni et fausse sous FDR**. La simulation
le montre sans ambiguïté : sous `BH`, le nombre de vrais signaux trouvés croît
**proportionnellement à `N`** (1,28 → 2,94 → 5,74 → 11,39 pour N = 20, 50, 100,
200) pendant que la proportion de fausses découvertes reste **plate à ~9 %**.

Tester plus de papiers ne dégrade donc pas la qualité de ce qu'on retient. Ce qui
la dégraderait, c'est de tester des papiers **moins bons** — la proportion de
vrais signaux chute, et avec elle le rendement de la procédure. **Le vrai budget
porte sur la qualité du corpus, pas sur le nombre de lignes du registre.**

**Pourquoi 50 et pas 200.** Non pas pour économiser des tests, mais parce que le
corpus ne porte pas 200 fiches : 17 existent, `D24` en fixe la population
atteignable, et la base vectorielle compte 136 papiers moissonnés dont tous ne
sont pas implémentables sur neuf futures intraday. Fixer 200 serait annoncer un
lot qu'on ne clôturerait pas, et `C2` tomberait.

**Pourquoi `q` = 0,10 et pas 0,05.** Parce que notre puissance est mince et que
nous le savons : avec `t` = IC × 146,8, un signal à la cible optimiste de `D01`
(IC 0,018) produit un `t` attendu de 2,64, donc passe le premier échelon de `BH`
**une fois sur deux environ**. Serrer `q` à 0,05 sacrifierait des vrais signaux
qu'aucune donnée supplémentaire ne viendra jamais racheter — la tranche `pool`
est finie, et le holdout ne s'ouvre qu'une fois.

**Ce que ce choix sacrifie, et il faut le dire.** Avec `q` = 0,10 et trois
survivants, **il y a environ une chance sur trois qu'un des trois soit du
bruit**. Ce n'est pas un détail rassurant qu'on pourra oublier : c'est le prix
payé pour ne pas jeter les vrais. La parade n'est pas statistique, elle est
séquentielle — la phase 10 backteste, la phase 15 dégonfle sur le registre
entier, et le holdout tranche une fois.

**La dépendance entre tests est la faiblesse connue de ce choix.** `BH` est
valide sous indépendance et sous dépendance positive ; plusieurs papiers
d'intraday momentum produiront des signaux corrélés. La simulation ci-dessus
suppose l'indépendance, donc elle est **optimiste**. C'est pourquoi la clause de
mesure ci-dessous existe : `scripts/calibrate_coder.py` sait déjà mesurer la
corrélation entre deux signaux, et cette matrice doit être produite et inscrite
**avant** d'appliquer `BH`. Si la dépendance se révèle négative ou erratique, la
variante Benjamini–Yekutieli (÷ Σ 1/i ≈ ÷4,5 à N = 50) s'impose, et ce sera une
décision écrite.

## Ce que ça verrouille

- **`scripts/gate_09.py`** appliquera `BH` et refusera de rendre un verdict si le
  lot n'est pas clos, si une hypothèse manque, ou si un `p` a été calculé hors
  du harnais.
- **La matrice de corrélation des signaux du lot** est produite avant `BH` et
  inscrite. Sans elle, le contrôle `BH` est une hypothèse non vérifiée.
- **Le lot de 50 est déclaré par écrit** — une liste de `fiche_id`, datée, avant
  la première mesure. L'ajouter après serait la faute que `C2` ferme.
- **Aucune mesure isolée « juste pour voir » pendant la phase 09.** Elle
  écrirait au registre et gonflerait le dénominateur sans entrer dans le lot,
  donc sans profiter à personne.
- **En changer périme le lot.** Si `q`, `N` ou le caractère unilatéral bougent
  après la première mesure, tous les résultats du lot sont réputés exploratoires
  et la phase 09 recommence sur un lot neuf.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **La dépendance réelle entre signaux** — mesurée, pas supposée ; elle peut imposer Benjamini–Yekutieli | avant d'appliquer `BH`, phase 09 |
| **La liste nominative des 50 fiches** — le corpus n'en porte que 17 ; il faut en produire 33 de plus, ou réduire `N` par un amendement écrit à cette décision | avant la première mesure |
| **Le sort d'un signal à l'envers du signe prédit** — réfutation inscrite, mais compte-t-elle pour la phase 13 (régimes) ? | phase 13 |
| **Le seuil économique après coûts** — les frais CME/EUREX sont `null`, donc tout IC net est un majorant. Un signal retenu par `BH` peut ne pas survivre aux vrais frais | quand les barèmes seront dépouillés |
| **Le budget des phases 11 à 14** — combinaisons et régimes multiplient les tests bien plus vite que la phase 09. La présente décision ne dit rien d'eux | avant la phase 11 |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | `N` du lot | `q` | Retenus | Note |
|---|---|---|---|---|---|
| — | 2026-09-23 | — | — | — | décision écrite ; aucun lot n'existe encore |
