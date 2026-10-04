# D41 — Une seule façon d'écrire les hypothèses du lot : celle de D40

**Date :** 2026-10-01
**Phase :** 09
**État :** prise — choix de l'opérateur (« on garde son format ») ; réconcilie `D40` (arthurpeg) avec `D34`, `D36`, `D38` et la réaction en chaîne

## La question

Deux lignes de travail parallèles écrivaient les hypothèses du lot 09 :

- `D40` : un format à en-tête fixe et six sections, un juge
  (`hypotheses/score_hypothese.py`, sept conditions et la bijection avec le lot),
  et dix hypothèses écrites le 2026-09-29 (`H05` à `H14`), avant le codage ;
- `scripts/hypotheses_lot.py` : des hypothèses rédigées mécaniquement après le
  double codage (`D34`), avec l'univers de `D38`, appelées par `avancer.py`.

La réaction en chaîne aurait écrit une **seconde** hypothèse, dans un format que
le juge de `D40` refuse, pour des fiches qui en avaient déjà une.

## Le choix

**Le format et le juge de `D40` font foi.** `scripts/hypotheses_lot.py` n'écrit
plus aucune hypothèse (`--write` refuse) ; il **relie** au lot celles que le juge
de `D40` accepte (`ref`, `signal_id`, univers), et dit celles qui restent à écrire.

1. **Qui écrit, et quand.** Une hypothèse s'écrit au format de `D40`, avant
   toute mesure — avant ou après le codage, comme `D40` le permet. La commande
   `/fabriquer-signaux` l'écrit quand une fiche est vérifiée et n'en a pas.
2. **L'univers (`D38`).**
   - Une hypothèse écrite **avant `D38`**, ou qui déclare « les 25 cellules »,
     est mesurée **sur la grille entière** : c'est ce qu'elle a pré-enregistré, et
     une hypothèse ne se réécrit pas (invariant IV). C'est le cas de `H05` à `H14`.
   - Une hypothèse écrite **depuis** est mesurée sur l'actif du papier et sa
     classe, tirés de la recette ; sa section « Le domaine » doit nommer chaque
     actif du papier (`hypotheses_lot.py --domaine` en donne le paragraphe), sans
     quoi elle n'est pas reliée.
3. **Écarter une fiche qui a déjà son hypothèse.** Puisque l'hypothèse peut
   précéder le codage, avoir une `ref` ne prouve plus que le codage a réussi.
   `ecarter_du_lot.py` décide sur le codage réel (refus si le double codage est
   CONCORDANT) et n'écarte jamais pour son marché une hypothèse pré-enregistrée
   sur la grille. L'hypothèse d'une fiche écartée reste, pour mémoire, et sort de
   la bijection `B1` (`score_hypothese.ecartees_du_lot`).
4. **La mesure exige le juge de `D40`** : `measure_lot.py` refuse tant qu'une
   faute de `score_hypothese.py` subsiste, bijection comprise.

## Pourquoi

**Parce qu'une hypothèse ne s'écrit qu'une fois.** Deux formats pour un même
objet, c'est deux pré-enregistrements possibles pour une même fiche, et la
tentation de garder celui qui arrange. `D40` existait, avait son juge et dix
hypothèses ; la ligne mécanique n'en avait écrit aucune.

**Ce qui est sacrifié.** L'écriture n'est plus mécanique : une hypothèse de `D40`
demande une rédaction, et son juge ne dit pas si elle est creuse (`D40`, comme
`D16`). Et `H05` à `H14`, écrites avant `D38`, se mesurent sur la grille entière,
y compris `H06` (bitcoin), que `D38` aurait écartée — on respecte ce qui a été
pré-enregistré plutôt que de le réécrire.

## Ce que ça verrouille

`scripts/hypotheses_lot.py` (`--lier`, `--domaine`, `--status`),
`scripts/avancer.py` (étape 3), `scripts/ecarter_du_lot.py`,
`scripts/measure_lot.py`, `hypotheses/score_hypothese.py`
(`ecartees_du_lot`), `.claude/commands/fabriquer-signaux.md`.

## Ce qui reste ouvert

- **Les 31 fiches sans hypothèse** (`hypotheses/NON-ECRITES-09.md`) : beaucoup ne
  portent aucune prédiction de rendement. Elles s'écarteront ou recevront leur
  hypothèse ; c'est une décision à prendre avant la mesure, sur ce compte.
- **`corpus/lot_phase09.py --ecrire`** reconstruit le lot à partir de rien
  (`F54`) : il effacerait `ref`, `universe` et `ecartees_codage`. Il ne doit plus
  être relancé sur le lot 09 sans les préserver.
