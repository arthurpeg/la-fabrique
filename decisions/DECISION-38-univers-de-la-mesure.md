# D38 — On mesure une hypothèse sur le marché de son papier, pas sur toute la grille

**Date :** 2026-09-30
**Phase :** 09
**État :** prise — précise `D01` §4 pour le lot ; complète `D34` (la recette) et `D36` (le lot) ; ne touche pas au harnais

## La question

Chaque hypothèse du lot était mesurée sur les 25 cellules de la grille, même
quand son papier n'étudie qu'un seul actif. L'opérateur l'a relevé le
2026-09-30 : un effet réel sur le pétrole seul se **dilue** dans un IC poolé où
CL pèse un neuvième des observations, et la ventilation par cellule ne peut pas
le rattraper ensuite, puisque choisir une cellule après coup est interdit
(`D01` §4). Sur quelles cellules mesure-t-on une hypothèse ?

## Les options

1. **Toute la grille, toujours.** Écartée : c'était le défaut des outils
   (`hypotheses_lot.py`), pas une règle ; il teste autre chose que ce que le
   papier affirme.
2. **L'actif exact du papier seul.** Écartée : le plus fidèle, mais le moins de
   données.
3. **L'actif exact plus sa classe, lus à part dans les résultats.** Retenue
   (choix de l'opérateur).
4. **L'actif exact et la grille, deux tests.** Écartée : deux tests par papier
   rendent le seuil du lot plus sévère pour tous.

Pour un papier dont le marché n'est **aucun** de nos instruments (actions
individuelles, indices étrangers, bitcoin, obligations) : le mesurer sur toute
la grille, ou sur « la classe la plus proche », ou **l'écarter du lot**.
Écarter est retenu (choix de l'opérateur).

## Le choix

**1. La recette déclare le marché** (`scripts/recette.py`, champ `market`) :
ce que le papier étudie, cité mot pour mot ; `exact_roots`, ceux de nos neuf
instruments qui **sont** ce marché ou son équivalent direct (liste close :
`INSTRUMENTS`) ; `sessions`, les fenêtres que ses données couvrent, citées, ou
`null` avec raison. La session de recette ne rapproche rien « par
ressemblance » : un marché absent donne `exact_roots: []`.

**2. Le code dérive l'univers** (`codage_verifie.univers_de`) :

| | |
|---|---|
| actif du papier | `exact_roots` |
| même classe | les autres instruments de la même `asset_class` du catalogue — indices actions (NQ, ES, YM), or seul, pétrole seul, devises (6E, 6B, 6J, 6A) |
| fenêtres | celles du papier ; les trois s'il ne les donne pas |

**3. L'hypothèse l'écrit, avant toute mesure** (`hypotheses_lot.py`), et le lot
le porte (`universe` de chaque entrée). La mesure (`measure_lot.py`) et la
matrice de corrélation (`lot_correlations.py`) ne lisent que ces cellules. **Un
seul test par hypothèse**, comme avant : l'IC poolé sur son univers.

**4. On lit à part l'actif du papier et sa classe**, dans le rapport gardé
(`scripts/out/rapports/`, champ `universe`) et au tableau de bord : les IC par
cellule, recopiés du rapport officiel, sont groupés en « actif du papier » et
« même classe ». Aucun IC partiel n'est recalculé : ce sont des diagnostics
(`D01` §4), seul l'IC poolé de l'univers est le test.

**5. Un marché absent écarte la fiche**, avant tout codage :
`ecarter_du_lot.py --preuve univers`, qui vérifie que la recette dit bien
`exact_roots: []`. La fiche apparaît au tableau de bord parmi les écartés, avec
sa raison.

**6. La porte 09 et la mesure refusent** une entrée sans univers déclaré
(`codage_verifie.fautes_univers`).

## Pourquoi

**Parce qu'une hypothèse teste ce que son papier affirme.** Le papier sur
l'or affirme quelque chose de l'or ; l'IC poolé sur les devises n'en dit rien.
La classe est ajoutée parce qu'elle partage le mécanisme (deux indices actions
américains réagissent aux mêmes flux) et qu'elle double ou triple les données ;
elle est lue à part pour qu'un effet propre à l'actif du papier ne se cache pas
derrière elle.

**Ce qui est sacrifié.** De la puissance : moins de cellules, donc un effet plus
fort est nécessaire pour passer le seuil. Et des fiches : celles dont le marché
nous est absent sortent du lot — l'idée aurait pu se transposer, mais la tester
ailleurs serait tester une autre hypothèse. Le lot rétrécit, sans que le compte
de tests par hypothèse change.

**Ce que ça ne change pas.** Le harnais (aucune empreinte ne bouge), le contrat
de signal (un signal note toujours toute la grille ; c'est la mesure qui
restreint), le double codage (`D34`), les seuils de `D25`.

## Ce que ça verrouille

- `scripts/recette.py` (champ `market`, liste close `INSTRUMENTS`) ;
- `scripts/codage_verifie.py` (`univers_de`, `cellules_de`, `fautes_univers`) ;
- `scripts/hypotheses_lot.py`, `scripts/measure_lot.py`,
  `scripts/lot_correlations.py`, `scripts/gate_09.py`,
  `scripts/ecarter_du_lot.py` (preuve `univers`) ;
- `scripts/tableau_de_bord.py` et `.html` ;
- `scripts/CODAGE-DES-SIGNAUX.md` § 2.1.

**La recette de `baltussen-2021-hedging-demand-intraday-momentum`**, écrite
avant `D38`, ne déclare pas de marché : elle se refait (nouvel essai) avant que
son hypothèse puisse s'écrire. Son double codage reste valable.

## Ce qui reste ouvert

- **Le rapprochement « équivalent direct »** repose sur la session de recette,
  citée mais non jugée par un étalon. Un désaccord se verra au tableau de bord.
- **Des papiers multi-marchés** (Baltussen : des dizaines de futures) déclarent
  plusieurs `exact_roots` ; la classe s'ajoute pour chacun.
