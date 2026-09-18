# H04 — La périodicité intra-journalière de la volatilité

**Écrite le :** 2026-09-18, **avant toute mesure sur nos données**
**Instrument :** `scripts/measure_h04.py` — à écrire ; il ne produit **aucun IC**
**Origine :** Andersen & Bollerslev (1997), « Intraday periodicity and volatility
persistence in financial markets », *J. Empirical Finance* 4(2-3):115-158 —
`corpus/AMORCE.md` entrée 11, fiche
`corpus/fiches/andersen-bollerslev-1997-periodicity.json`
**Rôle :** cible de la **clause 2 de la porte 06** (`D13`)
**Statut :** **testée le 2026-09-18** — voir « Le résultat » en fin de fichier.
L'affirmation ci-dessous n'a pas été touchée d'un mot depuis sa rédaction.

## Ce qui est affirmé

La volatilité varie systématiquement au cours de la séance, selon un motif si
fort qu'il domine la dynamique des rendements haute fréquence.

Trois clauses, qui valent ensemble :

| | Clause | Prédiction |
|---|---|---|
| **A — la forme en U** | `|r|` moyen par tranche horaire, sur `ES × US` | **creux au milieu**, sommets aux deux extrémités |
| **B — le rapport** | sommet / creux de ce motif | **entre 1,4 et 3,0** |
| **C — la périodicité** | autocorrélation de `|r|` aux décalages multiples de la séance | **positive**, et **supérieure** aux décalages voisins non multiples |

Et une clause de généralité :

| **D — trois indices** | Le motif A tient sur `NQ × US`, `ES × US` et `YM × US` — pas sur une seule cellule |

## Pourquoi ces bornes, et pas d'autres

**Le rapport plutôt que les niveaux.** Les auteurs rapportent, sur les futures
S&P 500, un `|r|` moyen de **0,095 %** le matin, **0,055 %** vers midi et
**0,105 %** en fin de séance — soit un rapport sommet/creux de **1,91**. Leurs
barres font **cinq minutes**, les nôtres **une** : les niveaux ne sont pas
comparables, le rapport l'est. La fourchette 1,4–3,0 est délibérément large
autour de leur 1,91 : elle doit pouvoir accueillir trente ans d'écart et un
changement de microstructure sans être satisfaite par n'importe quoi. Un rapport
sous 1,4 n'est plus un U ; au-dessus de 3,0, ce serait un autre phénomène et il
faudrait chercher l'erreur avant de chercher la confirmation.

**Un J compte comme un U.** Les auteurs notent que la branche droite dépasse
parfois la gauche, surtout les jours volatils. C'est une variante du motif, pas
une contradiction : la clause A demande un **creux au milieu**, pas la symétrie.

## Le domaine

- **Cellules :** `NQ × US`, `ES × US`, `YM × US` pour les clauses A, B et D —
  c'est la fenêtre 09:30-16:00, la séance de bourse américaine, celle des figures
  du papier. La clause C porte sur les mêmes trois cellules.
- **Grandeur :** rendement absolu à la barre d'une minute, ajusté des roulements.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Aucun IC n'est calculé.** L'instrument mesure une propriété des données ;
  `counted_tests()` ne bouge pas (`D13`).

## Ce qui la contredirait

- **Pas de creux.** Un profil plat, ou monotone, sur les trois cellules : le fait
  le mieux établi de la littérature intraday serait absent de nos données, et ce
  serait notre dépôt qu'il faudrait soupçonner, pas le papier.
- **Un rapport hors de [1,4 ; 3,0]** sur la majorité des trois cellules.
- **Pas de périodicité** dans l'autocorrélation de `|r|` : les décalages
  multiples de la séance ne se distinguent pas de leurs voisins.
- **Le motif sur une seule cellule** : ce ne serait pas la périodicité
  intra-journalière, ce serait un accident d'instrument — même clause que `H01`
  et `H03`.

## Ce que franchir ou ne pas franchir veut dire — écrit avant de regarder

**Si les quatre clauses tiennent :** la clause 2 de la porte 06 est franchie. Ce
qui est validé est **la chaîne de données et la discipline de mesure** — pas le
harnais d'IC, qui reste garanti par sa seule calibration à la main (`D13`
§ Pourquoi, premier paragraphe). Aucune session ne doit lire cette porte comme
davantage.

**Si elles ne tiennent pas :** la porte reste fermée, et le soupçon porte sur
**nous**. Un fait aussi robuste absent de nos données désignerait la couche de
données — définition des séances, ajustement des roulements, filtrage des
barres — avant de désigner le papier. Ce serait une découverte coûteuse et utile,
et il faudrait la traiter comme telle plutôt que chercher une cinquième cible.

C'est la différence avec `H01`, `H02` et `H03` : leur échec était un résultat sur
le monde. Un échec ici serait un résultat sur **notre dépôt**.

## Ce qui n'est pas affirmé ici

Le modèle périodique explicite de leur section 5 — la procédure qui *purge* la
périodicité — n'est pas testé. Il servira en phase 09, si la normalisation des
scores en a besoin. Et rien n'est affirmé sur les fenêtres `ASIA` et `EUROPE` :
leurs figures portent sur la séance américaine, et transposer leur forme à des
fenêtres qu'ils n'ont pas étudiées serait inventer une prédiction pour pouvoir la
vérifier.

---

## Le résultat

**Mesuré le 2026-09-18**, `scripts/measure_h04.py`, tranche `pool`, as-of
2023-12-29, fenêtre `US`, ~790 000 barres par instrument. Sortie complète dans
`scripts/out/h04_periodicity.json`. **Aucun IC n'a été calculé ;
`counted_tests()` vaut toujours 56.**

### A, B et D — la forme en U

| | ouverture | milieu | clôture | creux | sommet | **rapport** |
|---|---|---|---|---|---|---|
| `NQ × US` | 0,0467 % | 0,0299 % | 0,0328 % | 0,0269 % | 0,0553 % | **2,05** |
| `ES × US` | 0,0335 % | 0,0238 % | 0,0282 % | 0,0217 % | 0,0376 % | **1,74** |
| `YM × US` | 0,0326 % | 0,0222 % | 0,0261 % | 0,0202 % | 0,0381 % | **1,89** |

Ouverture et clôture au-dessus du milieu sur les **trois** ; creux au milieu de
la séance (tranches 6 à 8 sur 12) ; rapports **tous** dans la fourchette
`[1,4 ; 3,0]` écrite d'avance.

Et la comparaison qui compte : les auteurs rapportent **1,91** sur les futures
S&P 500 en 1986-1989. Notre `ES × US` — **le même contrat, la même fenêtre,
trente ans plus tard** — rend **1,74**.

### C — la périodicité de l'autocorrélation de `|r|`

| | multiples de séance | voisins ±15/30 min | écart |
|---|---|---|---|
| `NQ` | +0,2524 | +0,2420 | **+0,0104** |
| `ES` | +0,2740 | +0,2682 | +0,0059 |
| `YM` | +0,2900 | +0,2844 | +0,0055 |

La clause tient sur les trois. **Mais son témoin était mal placé**, et il faut le
dire : à 15 et 30 minutes d'un multiple, on est presque à la **même phase** du
cycle intra-journalier, donc le témoin ne pouvait presque rien détecter.

Un **diagnostic non pré-enregistré**, ajouté après coup et n'entrant dans aucune
clause, place le témoin à une **demi-séance** — phase opposée :

| | multiples | phase opposée | écart |
|---|---|---|---|
| `NQ` | +0,2524 | +0,1840 | **+0,0684** |
| `ES` | +0,2740 | +0,2283 | **+0,0457** |
| `YM` | +0,2900 | +0,2381 | **+0,0518** |

**Cinq à sept fois l'écart mesuré par la clause.** C'est le « U déformé dans le
corrélogramme » que décrivent les auteurs. La clause C mesurait donc un
**plancher** de l'effet, pas l'effet. Leçon `L16`.

### Le verdict

**Les quatre clauses tiennent. La clause 2 de la porte 06 est franchie**, et la
porte 06 avec elle — sa clause 1 l'était depuis le 2026-09-17.

**Ce qui est validé, et rien de plus.** La **chaîne de données** et la discipline
de mesure : définition des séances, horloge de la place, ajustement des
roulements, filtrage des barres. Un fait publié depuis 1997 sur le même contrat
se retrouve dans nos données, au bon endroit et à la bonne amplitude.

**Ce qui n'est PAS validé.** Le harnais d'IC. `D13` § Pourquoi le dit sans
détour : il reste garanti par sa seule **calibration à la main** (porte 03, IC
reproduit à 1e-12 sur un cas connu), et c'est une garantie plus faible. Aucune
session ne doit lire cette porte comme davantage.
