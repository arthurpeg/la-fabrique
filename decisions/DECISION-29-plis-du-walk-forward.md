# D29 — Pas de plis en phase 09 : une mesure unique sur toute la tranche `pool`

**Date :** 2026-09-26
**Phase :** 09
**État :** prise — tranche le point que `D04` § Ce qui reste ouvert renvoyait à
la phase 09 ; précise `D01` §5 pour la phase 09 sans le réécrire

## La question

`D01` §5 définit la tranche `pool` comme « walk-forward purgé, plusieurs plis,
embargo aux frontières ». `D04` a renvoyé le nombre et les frontières des plis à
la phase 09. Ni `D25` ni `gate_09.py` n'en parlent, et le harnais évalue à une
seule date. Avant de mesurer le lot : la phase 09 a-t-elle besoin de plis, et
sinon, qu'est-ce qui fixe l'échantillon mesuré ?

## Ce que fait un walk-forward, et ce qu'il n'y a pas ici

Un walk-forward protège d'**un** danger : qu'un paramètre soit **ajusté** sur les
données où on le juge. On apprend sur un pli, on juge sur le suivant, on purge et
on met un embargo aux frontières pour que les étiquettes d'apprentissage ne
débordent pas sur la période jugée.

**En phase 09, aucune étape n'ajuste quoi que ce soit sur le `pool`**, et ce
n'est pas une promesse, c'est vérifié :

- **les constantes viennent de la fiche** — `D23` `S5` : toute constante
  numérique du code se retrouve dans la fiche, donc dans le papier. Aucun
  paramètre n'est choisi sur nos données ;
- **ce qui est estimé sur les données l'est au passé** — `D23` `S3`, le test de
  causalité, avec la résolution d'une barre depuis `D27`. Un signal qui estime
  une moyenne, une volatilité ou un coefficient ne peut le faire que sur les
  barres `<= t`. C'est déjà un walk-forward **ancré, réestimé à chaque barre**,
  et la purge y est **automatique** : les rendements qui servent à l'estimation
  sont réalisés au plus tard à la clôture de `t`, là où le rendement à prédire
  commence. Rien ne déborde ;
- **la sélection entre signaux** est la seule sélection de la phase, et elle est
  payée ailleurs : `BH` sur un lot clos avant la première mesure (`D25`), sans
  regard préalable (`D28`).

Des plis n'apporteraient donc **aucune** protection de plus. Pour un signal à
paramètres fixes, l'IC poolé sur k plis ne diffère de l'IC sur la tranche entière
que par le découpage des rangs de Spearman — aucun pli n'est « hors
échantillon » d'un autre, puisque rien n'y a été appris — et `D01` §4 compte déjà les plis d'un même schéma pour **un**
test.

## Les options

1. **Une mesure unique sur toute la tranche `pool`, à un instant fixé.**
   Retenue.
2. **k plis dans le harnais**, avec purge et embargo. Écartée pour la phase 09 :
   c'est une modification du harnais figé (tous les tests comptés périmés) pour
   une protection dont le danger n'existe pas encore. Elle devient **obligatoire**
   au premier ajustement (§ Ce que ça verrouille).
3. **Laisser chaque hypothèse choisir sa date d'évaluation.** Écartée : c'est un
   bouton. Raccourcir l'échantillon jusqu'à ce qu'un signal passe est un
   surajustement sur la période, aussi réel qu'un surajustement de paramètre, et
   il n'apparaîtrait nulle part.

## Le choix

Chaque hypothèse du lot de la phase 09 est mesurée **une fois**, par `evaluate`,
sur la tranche `pool` entière, avec `asof = 2023-12-29 20:00 UTC` — la dernière
séance ouvrée du `pool`, et l'instant de **tous** les 56 tests comptés avant
elle (`scripts/measure_h01_h02.py`, `scripts/measure_h03.py`). Pas de plis.
`gate_09.py` refuse toute mesure du lot faite à un autre instant ou sur une autre
tranche.

## Pourquoi

Parce que la question « faut-il des plis ? » se ramène à « qu'est-ce qui est
ajusté, et sur quoi ? », et que la réponse, en phase 09, est : rien, sur rien. Le
seul degré de liberté qui restait sur l'échantillon — la date d'évaluation —
n'était fixé que par une **convention d'usage** : les 56 tests l'ont respectée,
mais aucune ligne ne l'exigeait. `L22` : une condition que rien ne vérifie n'est
pas tenue, elle est absente. Elle est maintenant vérifiée.

**Ce qui est sacrifié.** Deux choses, et la seconde compte.

- **Aucun diagnostic de stabilité dans le temps.** Un signal dont tout l'IC
  viendrait de 2020 (COVID) passerait la porte 09 comme un signal régulier. Un
  IC par année serait le bon diagnostic, mais il ne peut être calculé **que par
  le harnais** — un IC par sous-période calculé à la main est exactement ce que
  `CLAUDE.md` interdit. Il est donc renvoyé à la décision qui modifiera le
  harnais (§ Ce qui reste ouvert). D'ici là, la phase 10 (backtest) et la phase
  15 (holdout) restent les seules vérifications de stabilité.
- **Le biais de publication n'est pas levé, et aucun pli ne le lèverait.** Les
  paramètres d'une fiche ont été choisis par ses auteurs, souvent sur des données
  qui recouvrent notre `pool` (2016-2023). Retrouver l'effet sur le `pool`, c'est
  en partie le retrouver là où il a été trouvé. Des plis ne changent rien : le
  paramètre n'est pas réajusté, il est hérité. **Le holdout (2024 →) est la seule
  mesure hors échantillon du projet**, et c'est ce que l'invariant V protège.

## Ce que ça verrouille

- `scripts/gate_09.py` : une mesure officielle porte `data_slice = "pool"` et
  `asof = "2023-12-29 20:00:00+00:00"` (`SLICE_REQUIRED`, `ASOF_REQUIRED`). Toute
  autre mesure d'un signal du lot est refusée comme hors protocole (`D28`).
  `--check` relit la fin de tranche dans le catalogue et vérifie que l'instant
  est bien sur la dernière séance ouvrée. **21 vérifications.**
- **Les plis deviennent obligatoires au premier ajustement sur le `pool`** :
  pondérations d'une combinaison (phase 12), seuils d'un régime (phase 13),
  toute proposition du générateur qui choisit un paramètre sur nos données
  (phase 14). Leur schéma — nombre, frontières, purge, embargo — sera écrit
  **avant** le premier ajustement, et le harnais qui les porte sera une décision.
- `D01` §5 (« walk-forward purgé, plusieurs plis ») reste la règle **pour ce qui
  s'ajuste** ; il n'est pas réécrit.

## Ce qui reste ouvert

- **Un diagnostic de stabilité par sous-période dans le rapport d'IC.** À ajouter
  au harnais **dans la même décision** que les frais (`D26`) et la fermeture du
  trou d'`extra` (`D28`) : une seule modification du harnais, une seule
  péremption des tests comptés. Diagnostic seulement, comme la ventilation par
  cellule : jamais un test de plus.
- **La période d'échantillon du papier.** Pour lire le biais de publication, il
  faudrait savoir, par hypothèse, jusqu'à quand le papier a regardé. Les fiches
  ne le portent pas de façon structurée. À décider avant la lecture des
  résultats du lot, pas après.

## Journal

- **2026-09-26** — décision prise et appliquée. `gate_09.py --check` : 21
  vérifications, 0 échec. Vérifié hors dépôt sur un lot fabriqué : une mesure à
  `asof = 2019-12-31` est refusée et nommée. Registre 169 → 169, harnais
  inchangé.
