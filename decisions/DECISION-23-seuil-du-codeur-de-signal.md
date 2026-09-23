# D23 — Le seuil du codeur de signal, écrit avant qu'il existe

**Date :** 2026-09-23
**Phase :** 08
**État :** prise

## La question

`ETAT.md` pose la porte 08 : *« Une fiche produit un signal exécutable qui passe
la sandbox, sans retouche manuelle. »* Trois mots y sont flous — **exécutable**,
**passe**, et surtout **produit** : à quoi reconnaît-on qu'un signal code bien
*cette* fiche plutôt qu'une autre ?

## Ce que la situation impose, et qui n'était pas prévu

`D06` désigne deux étalons pour cette porte : Gao et al. (2018), entrée 1, et
Baltussen et al. (2021), entrée 2 — implémentés à la main dans `signals/`.
L'idée était de comparer le signal produit par un agent à l'implémentation
humaine du même papier.

**Aucun des deux n'a de fiche.** L'entrée 1 est devenue **inatteignable** le
2026-09-22 : l'URL qui la servait désignait un autre papier (`L20`), et aucune
copie libre du vrai Gao 2018 n'existe. L'entrée 2 est encore **à ficher**.

Le codeur prend une **fiche** en entrée. Il ne peut donc, au mieux, être
comparé à une implémentation humaine que sur **un seul papier** — et `F43` a
déjà tranché qu'un seuil sur trois items ne distingue pas un automate correct
d'un automate chanceux. Sur un item, la question ne se pose même plus.

## Les options

**1. La corrélation à l'implémentation humaine comme seuil.** Écartée par ce
qui précède : un seul sujet disponible, et il n'est pas encore fiché.

**2. Une relecture humaine de chaque signal produit.** Écartée pour la raison
de `F45` : elle ne s'automatise pas, et la phase 09 en demandera trente à
cinquante.

**3. L'IC du signal produit comme critère.** Écartée, et c'est la plus
dangereuse. Juger un codeur sur l'IC qu'il obtient, c'est **sélectionner le
code sur son résultat** — la définition même du surajustement. Et chaque essai
consommerait une ligne de registre, gonflant le dénominateur de la phase 15
avec des tentatives de codage qui ne sont pas des hypothèses.

**4. La fidélité à la fiche, vérifiable sans étalon.** Retenue.

## Le choix

**Un signal produit est jugé sur six conditions, toutes à tolérance zéro, qui
valent ENSEMBLE.** `scripts/score_signal.py` les vérifie.

| | Condition | Vérifié par |
|---|---|---|
| **S1** | le module satisfait le contrat de `D07` — `SIGNAL_ID`, `HYPOTHESIS`, `PAPER`, `EXPECTED_SIGN`, `scores(panel, cells, horizon_bars)` | `sandbox/contract.py` |
| **S2** | il n'importe rien hors de la liste blanche | `sandbox/scan.py` |
| **S3** | **il est causal** — score identique sur panel tronqué et panel entier | `sandbox/causality.py` |
| **S4** | il n'est pas dégénéré, et ses scores tombent sur des barres **mesurables** | `harness/controls.py`, `L10` |
| **S5** | **toute constante numérique du code se retrouve dans la fiche** | nouveau |
| **S6** | **zéro retouche manuelle** après production | protocole |

**Aucun IC n'est calculé pour franchir cette porte.** Comme la clause 1 de la
porte 06, le jugement se fait **avant** le harnais et **sans consommer de ligne
de registre**.

**La corrélation aux étalons est une calibration, pas un seuil.** Quand l'entrée
2 sera fichée, on fera coder Baltussen et on inscrira la corrélation obtenue au
§ Journal. Elle **ne conditionne rien** : elle dit ce que le codeur sait faire
sur un sujet connu, comme la porte 03 calibre le harnais à la main.

## Pourquoi

**`S5` est la condition qui porte la décision**, et elle est l'exacte transposée
de `F2`.

`F2` exige qu'une citation soit **mot pour mot** dans le texte du papier, parce
que sans cela un extracteur qui fabrique la citation *et* le chiffre qu'elle
contient passait `D14` sans une faute. Le même trou existe ici : un codeur qui
écrit `fenetre = 30` alors que la fiche dit quarante-cinq minutes produit un
signal **qui tourne, qui est causal, qui n'est pas dégénéré** — et qui ne code
pas ce papier. Rien ne l'attraperait.

Exiger que chaque nombre du code se retrouve dans la fiche ferme cela sans
étalon, et **c'est l'interdit constitutionnel appliqué au code** : *ne jamais
inventer une valeur de données*. Un paramètre qui n'est pas dans la fiche est
un paramètre inventé.

Comme pour `F2`, il faudra une **liste close d'échappatoires nommées** — une
constante qui vient de `catalogue.yaml` (un tick, un multiplicateur), une
qui vient de `D01` (un horizon, une fenêtre de séance), une qui est une
convention de langage (`0`, `1`, `100` pour un pourcentage). Ce que la liste ne
couvre pas est refusé, et l'élargir est une décision — `L18`.

**Pourquoi aucun IC.** Deux raisons, et la seconde est la vraie.

La première : un codeur jugé sur l'IC est sélectionné sur le résultat. Après
vingt tentatives, on garderait celle qui mesure le mieux — c'est-à-dire du
surajustement déguisé en ingénierie.

La seconde : **le nombre de tests est la seule chose que la phase 15 ne peut pas
recalculer**. Un IC dépensé pour savoir si du code compile est un IC perdu pour
toujours. La porte 06 l'a déjà établi pour les signaux dégénérés — *« il n'a
produit aucun IC, il n'y a rien à inscrire, et un dénominateur gonflé de tests
qui n'ont jamais eu lieu est aussi faux qu'un dénominateur absent »*.

**`S6` reprend `G3` de `D17`**, qui est la condition la plus dure et la plus
utile : un automate dont on répare les sorties à la main n'est pas un automate,
et la phase 09 en a besoin trente à cinquante fois.

**`S5` est nécessaire, pas suffisante — et c'est mesuré.** En croisant les trois
signaux écrits à la main avec les dix fiches, `S5` **refuse 12 appariements sur
30, soit 40 %**. Elle en laisse donc passer 60 %, dont les mauvais : le signal
Heston passe `S5` contre la fiche Lou (2019), qui n'a rien à voir.

La raison n'est pas réparable, et il vaut mieux l'écrire que la poursuivre : deux
papiers d'un même domaine **partagent leurs paramètres**. `30` minutes est la
demi-heure de Gao, le décalage de Heston et la fenêtre de Patton & Sheppard à la
fois. Une constante juste pour le mauvais papier reste une constante juste.

Ce que `S5` attrape réellement, et que rien d'autre n'attrapait, c'est un
paramètre **inventé** — absent de toute recette. C'est exactement l'interdit
constitutionnel, et c'est tout ce qu'une vérification de fidélité peut promettre
sans étalon. Pousser `S5` plus loin la transformerait en vérification de
*pertinence*, qui par la présente décision n'a pas de juge automatique.

**Ce que ce juge ne saura PAS faire, et c'est écrit ici.** Il ne dira pas si le
signal est *le bon*. Un codeur qui produirait un signal fidèle à une fiche
creuse, ou fidèle à un aspect secondaire du papier, passerait les six
conditions. La pertinence n'a pas de juge automatique — `D16` le disait déjà de
l'extraction, et c'est la même limite un cran plus bas. Elle n'aura de
dénominateur qu'en phase 09.

## Ce que ça verrouille

- **`scripts/score_signal.py` devient le juge de la porte 08**, et se montre
  refusant chacune des six fautes sur des signaux fabriqués, comme
  `score_triage.py` et `score_extraction.py` le font pour les leurs.
- **La liste close des constantes admissibles** est une pièce du dépôt, au même
  titre que `REASONS` de `D17` et `REPAIRS` de `D16`.
- **Le codeur est une session séparée** qui reçoit la fiche, le contrat de
  `D07`, et **rien d'autre** — ni `signals/`, qui contiendrait la réponse, ni
  les hypothèses pré-enregistrées. Même parade que pour le trieur et
  l'extracteur.
- **Changer une condition périme tout signal produit avant**, comme `D16` pour
  les fiches et `D10` pour le harnais.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| ~~**La liste close des constantes admissibles**~~ — **fixée** le 2026-09-23 : `CONVENTIONS` = {0, 1, -1, 2}, `DU_DEPOT` = {60, 24, 9}, `CHAMPS_RECETTE` = les quatre champs où vit la recette, `MODULES_DU_DEPOT` = {`_common.py`}. `30` en est **exclu** — voir journal | close, l'élargir est une décision |
| **La calibration sur Baltussen** — impossible tant que l'entrée 2 n'est pas fichée. C'est `G1` qui la débloque | après `G1` |
| **Gao, entrée 1** — étalon désigné par `D06` et devenu inatteignable. `D06` n'est pas rouverte ici : si une copie libre réapparaît, la calibration se fera sur deux sujets au lieu d'un | si l'entrée 1 redevient atteignable |
| **Que faire d'un signal qui passe les six conditions mais dont la fiche est creuse** — la question de la pertinence, renvoyée à la phase 09 comme `D16` l'a fait | phase 09 |
| **Le budget d'itérations d'une boucle de génération** — combien d'essais, quel seuil ajusté à ce nombre, quelle règle d'arrêt. La présente décision juge UN signal ; elle ne dit rien d'une recherche automatique qui en produirait des milliers | avant toute boucle |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Signal | S1–S6 | Verdict |
|---|---|---|---|---|
| — | 2026-09-23 | décision écrite, aucun codeur n'existe | — | seuil posé, juge à écrire |
| — | 2026-09-23 | `scripts/score_signal.py` écrit, 25/25 fautes fabriquées refusées | — | juge en place |
| — | 2026-09-23 | `S5` mesurée : 3 signaux × 10 fiches, **refuse 12/30 = 40 %** | — | nécessaire, pas suffisante — écrit au § Pourquoi |
| 1 | 2026-09-23 | `baltussen-2021-hedging-demand-intraday-momentum`, produit par une session séparée à partir de la seule fiche | **6/6 au premier essai** | **PASSE** — `scripts/code_signal.py --judge`, aucun IC calculé |

## La calibration sur Baltussen — faite le 2026-09-23

`D23` la prévoyait dès sa rédaction : *« Quand l'entrée 2 sera fichée, on fera
coder Baltussen et on inscrira la corrélation obtenue au § Journal. Elle ne
conditionne rien. »* L'entrée 2 a été fichée le matin même ; la mesure a pu être
faite le soir. `scripts/calibrate_coder.py` la produit.

**Corrélation poolée : 0,5334**, sur 15 644 paires et 25 cellules, entre le
module produit par le codeur et `signals/baltussen_2021_intraday_momentum.py`,
écrit à la main.

**Ce n'est pas un IC**, et la distinction n'est pas cosmétique : aucun rendement
n'entre dans ce calcul, aucune ligne n'est écrite au registre, et le script casse
si le compte a bougé. Il est resté à **160 lignes, 56 tests comptés**.

**La dispersion par cellule dit plus que la moyenne**, et c'est pourquoi elle est
inscrite ici :

| Fenêtre | Corrélation |
|---|---|
| `ES`, `NQ`, `YM` en **US** | 0,76 · 0,80 · 0,76 |
| `ES`, `NQ`, `YM` en **ASIA** / **EUROPE** | 0,28 à 0,41 |
| devises et matières premières | 0,28 à 0,73 |

Les deux lectures se rejoignent **là où le papier parle** — la séance américaine
des indices actions — et divergent ailleurs. Ce n'est pas surprenant : le module
produit code `r_ROD`, le rendement depuis la clôture de la veille, qui franchit
une frontière de séance ; l'implémentation humaine code la première demi-heure de
la fenêtre. Ce sont deux recettes différentes tirées du même papier.

**Ce que ce chiffre ne dit pas.** Que le codeur a raison. L'implémentation
humaine n'est pas la vérité, c'est une lecture — une corrélation basse peut
signifier que le codeur a dévié, ou que l'humain avait simplifié. C'est
exactement pourquoi `D23` en a fait une calibration et non un seuil.

## Journal des calibrations de la liste close

*Ce que les cas réels ont forcé à changer, et pourquoi. `L18` : avant d'élargir
une liste close, chercher si la cause n'est pas ailleurs.*

**2026-09-23 — `_common.py` exempté, plutôt que `24` ajouté à `DU_DEPOT`.**
`S5` signalait `signals/_common.py:74` pour la constante `24` dans
`(end_minutes - minutes) % (24 * 60)`. La cause n'était pas la liste mais le
**périmètre** : `_common.py` est du dépôt, écrit à la main, et n'est pas la
sortie du codeur. D'où `MODULES_DU_DEPOT`. Le trou apparent — un codeur qui
cacherait ses paramètres dans un utilitaire partagé — est fermé ailleurs : le
codeur produit exactement un module, et toucher un fichier du dépôt casse `S6`.

**2026-09-23 — `30` RETIRÉ de `DU_DEPOT`, et la recherche restreinte à quatre
champs.** `S5` passait contre *n'importe quelle* fiche. Mesuré plutôt que
supposé, pour deux causes cumulées :

- une fiche entière porte **41 à 194 nombres distincts** — `reported_results`
  est plein de t-stats, de Sharpes et de tailles d'échantillon qui ne
  paramètrent aucun code — contre **2 à 25** pour `signal_construction`. Sur la
  seule fiche Heston, **19 des 101 entiers de 0 à 100** s'y trouvaient par
  hasard. D'où `CHAMPS_RECETTE` ;
- `30` était exempté comme horizon de grille (`D01` §2). Or c'est aussi le
  **seul paramètre** du signal de référence Gao. L'exempter rendait invisible
  exactement ce que `S5` existe pour voir. Un horizon légitime se retrouve dans
  le champ `horizon` de la fiche, qui est fouillé — l'exemption était inutile
  autant que nuisible.
