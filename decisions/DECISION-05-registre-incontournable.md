# D05 — Le registre incontournable, et le descellage du holdout

**Date :** 2026-09-17
**Phase :** 04
**État :** prise

## La question

L'invariant III est vrai aujourd'hui *par construction du seul point d'entrée* :
`evaluate()` écrit au registre. Mais rien n'empêche d'importer `harness.metric`
et d'obtenir un IC sans laisser de trace — l'audit du 2026-09-17 l'a fait, et la
ligne produite figure au registre sous `stage: 04-audit`. La porte 04 exige
davantage : qu'on **essaie délibérément et qu'on n'y arrive pas**. Même question
pour le `holdout`, que le Panel refuse mais sans jeton de descellage.

## Les options

1. **Documenter l'interdit et s'y tenir.** Écartée : c'est l'état actuel, et
   c'est exactement ce que la porte refuse. Un registre qu'on alimente « avec
   discipline » n'est pas un registre.

2. **Un garde hors de `harness/`** — un crochet d'import, un `sitecustomize`, un
   lint qui refuse `from harness.metric import ...`. Écartée pour la raison qui a
   déjà fait écarter F13 : le nombre resterait calculable dans le processus, et
   seule une couche extérieure l'en tiendrait éloigné. De la vigilance déguisée
   en architecture.

3. **Le nombre n'existe pas avant la ligne.** Retenue. La fonction qui produit un
   IC poolé exige un **jeton** que seul le registre délivre, et **écrit la ligne
   elle-même** avant de rendre la valeur. Il n'y a plus de « calculer puis
   enregistrer » : c'est un seul geste, dans `harness/`, pas au-dessus.

## Le choix

`harness.metric` ne publie plus aucune fonction rendant un IC : `pool` et
`deflated_t` deviennent privées, et le seul chemin public — `settle(cells,
ticket, ...)` — réclame un jeton délivré par `registry.open_test()`, écrit la
ligne, puis rend la valeur ; le `holdout` ne s'ouvre qu'avec un jeton de
descellage produit par un geste explicite, tracé au registre.

## Pourquoi

Parce que l'ordre compte. Tant que « calculer » et « enregistrer » sont deux
gestes, il existe un état du monde où le premier a eu lieu sans le second — et
c'est précisément cet état que l'invariant III interdit. En les fusionnant, l'état
interdit cesse d'être atteignable par le code de ce dépôt.

**Ce que ça sacrifie, et c'est réel :** `harness/` est figé depuis la porte 03, et
cette décision le modifie. Le `code_hash` change, donc **tous les résultats
antérieurs sont réputés périmés** — c'est la règle, elle s'applique. Le coût exact
est mesurable : le registre contient 25 lignes, **toutes des calibrations**,
`counted_tests()` rend **0**. Aucun test d'hypothèse n'est perdu, parce qu'aucun
n'a encore été fait. Le même changement après le premier lot de signaux coûterait
le lot entier. C'est maintenant qu'il est gratuit, et il ne le sera plus jamais.

**Ce que ça ne prétend pas.** Python n'a pas d'encapsulation réelle : qui écrit
`from harness.metric import _pool` obtient encore un nombre. Cette décision ne
fabrique donc pas une impossibilité physique, elle fabrique **l'impossibilité de
le faire sans un geste délibéré et visible** — un nom privé, dans un dépôt où la
porte 04 vérifie par analyse syntaxique qu'aucun module ne le fait. Prétendre
davantage serait le genre de confort que ce projet refuse.

## Ce que ça verrouille

- `harness/metric.py`, `harness/registry.py`, `harness/evaluate.py` : signatures
  changées. `harness/__init__.py` cesse d'exporter `pool` et `deflated_t`.
- `panel/panel.py` : `Panel.open(slice="holdout")` réclame un `UnsealToken`.
- `registry/SCHEMA.md` : types, valeurs permises et validation, appliqués à
  l'écriture — plus une intention, une contrainte.
- `scripts/gate_03_harness.py` doit être rejoué sous le nouveau `code_hash` : la
  calibration ne vaut que pour le harnais qui l'a produite.
- En changer plus tard coûtera tout ce qui aura été mesuré entre-temps.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| Le contenu exact du geste de descellage (qui, quand, quoi écrire) | phase 15, et pas avant : le décider maintenant serait le répéter |
| L'empreinte du **code de signal**, distincte de celle du harnais | phase 05, avec l'API de signal |
| Le seuil de FDR appliqué au dénominateur du registre | phase 09 (`D04`) |
