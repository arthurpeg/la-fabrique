# D11 — La déflation de recouvrement se mesure, elle ne se déclare pas

**Date :** 2026-09-18
**Phase :** 06
**État :** prise

## La question

`D04` déflate le `t` de `√h` au motif que « deux observations voisines partagent
`h−1` barres ». `H01` et `H02` produisent **une observation par séance et par
cellule** : leurs observations voisines sont séparées d'environ 390 barres pour
un horizon de 30, et ne partagent rien. La déflation leur a été appliquée quand
même, divisant leur `t` par 5,48 sans raison.

## Les options

1. **Ne rien changer, et appeler ça de la prudence.** Écartée. Une prudence qui
   ne sait pas *de quoi* elle se protège n'est pas de la prudence : ici elle
   rejetterait un signal réel à `t` naïf de 4 en affichant 0,5, sans que rien ne
   le signale. La conservativité doit être un choix, pas un effet de bord.

2. **Retirer la déflation de recouvrement.** Écartée, évidemment : elle est
   juste pour un signal scoré à chaque barre, et un tel signal viendra.

3. **Un drapeau déclaré par le signal** — « je me recouvre » / « je ne me
   recouvre pas ». Écartée : c'est une valeur déclarée là où une mesure est
   disponible, et le projet a déjà tranché ce genre de question dans l'autre
   sens (`L04`, le tick mesuré plutôt que l'écart deviné). Un signal qui se
   déclare non chevauchant à tort achète un `t` multiplié par 5,48.

4. **Mesurer l'écart d'échantillonnage sur les observations elles-mêmes.**
   Retenue.

## Le choix

Le facteur de recouvrement vaut `√(n / n_eff)`, avec
`n_eff = Σ_c n_c / f_c` et `f_c = max(1, h / écart_c)`, où `écart_c` est
**l'écart médian, en barres, entre deux observations consécutives de la
cellule** `c`.

## Pourquoi

**Il redonne exactement l'ancien comportement là où l'ancien avait raison.** Un
signal scoré à chaque barre a `écart_c = 1`, donc `f_c = h`, donc un facteur
`√h` : c'est le cas que `D04` avait en tête, et la porte 03 le calibre sur un
score tiré sur **toutes** les barres — elle passe sans être touchée.

**Il devient neutre là où il n'y a rien à corriger.** `écart_c ≥ h` donne
`f_c = 1`. Pour `H01` et `H02` : écart 390, horizon 30, facteur **1**.

**Il traite le cas mixte sans arbitraire.** Un `n_eff` pondéré par cellule est la
seule forme qui ne fasse dépendre le résultat ni de la cellule la plus
chevauchante ni de la moyenne des facteurs — deux choix qu'on aurait dû
justifier. `√(n/n_eff)` se déduit, il ne se pose pas.

**Ce qu'on sacrifie.** Le harnais change, donc **tous les résultats antérieurs
sont périmés** — et cette fois ils comprennent **deux tests comptés**. Ce n'est
plus gratuit. Le coût est jugé faible et payé volontairement : `H01` et `H02`
sont des étalons dont la conclusion est « rien », et cette conclusion **tient
dans les deux lectures** (`t` −0,28 ou −1,55 ; −0,11 ou −0,63, tous sous 2). On
paie deux lignes pour cesser de rejeter des signaux pour une mauvaise raison.

## Ce que ça verrouille

**Une règle de comptage, à retenir pour la phase 15.** Le registre compte une
ligne par IC calculé, et il a raison. Mais après cette décision, `H01` et `H02`
porteront **deux lignes chacune** — l'ancienne, périmée, et la nouvelle — pour
**une seule hypothèse chacune**. La correction de tests multiples de la phase 15
compte des **hypothèses éprouvées**, pas des lignes écrites : une reprise après
changement du harnais n'est pas une recherche supplémentaire. Sans cette règle,
le dénominateur enflerait à chaque réparation, et on finirait par éviter de
réparer.

C'est la deuxième fois que `L11` se vérifie — le harnais a plusieurs sortes de
clients, et une règle écrite pour l'un fausse l'autre. La première fois c'était
le plancher de deux cellules contre la calibration ; ici c'est le recouvrement
contre la fréquence d'échantillonnage.

**Fichiers.** `harness/metric.py` (`CellIC` gagne `sampling_gap_bars`, `cell_ic`
le mesure, `_deflated_t` s'en sert) et `harness/report.py` (le rapport dit
l'écart mesuré au lieu d'affirmer un recouvrement). Portes 03 à 06 rejouées.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| L'écart **médian** suppose un échantillonnage régulier. Un signal qui scorerait en rafales — dix barres voisines puis rien pendant un mois — serait mal décrit par sa médiane | à la première forme de ce genre ; le rapport porte l'écart, donc ça se verra |
| La déflation reste **une forme dite**, pas un Newey-West, comme `D04` l'assumait déjà | inchangé |
| `f_c` ne regarde que l'écart et l'horizon, pas l'autocorrélation réelle des scores. Un signal lent produira des observations dépendantes même espacées | phase 09, quand plusieurs signaux auront été vus ; `harness/controls.py` signale déjà l'autocorrélation |
