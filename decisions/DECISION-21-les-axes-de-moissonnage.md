# D21 — Les axes de moissonnage : une taxonomie ouverte, mais déclarée

**Date :** 2026-09-22
**Phase :** 07 (construit), 09 (utilisé)
**État :** prise — amende `D20` § La requête

## La question

`D20` fige **six familles**, reprises des sections A–F d'`AMORCE.md`. C'est trop
rigide pour chercher : on veut viser par **classe d'actif** (futures, devises,
matières premières), par **méthode** (volatilité réalisée, étude d'événement,
apprentissage automatique), par **anomalie** (momentum, retournement, carry,
saisonnalité). Comment ouvrir la recherche sans rouvrir le bouton que `D20`
ferme ?

## Les options

**1. Garder les six familles figées.** Écartée : elles mélangent trois axes
incompatibles — `A` est une anomalie, `C` une méthode, `E` une famille d'actifs
— et on ne peut ni croiser ni raffiner.

**2. Une requête libre en ligne de commande.** Écartée, et c'est l'option
dangereuse. `python harvest.py --search "momentum futures"` rendrait le
périmètre du corpus **non écrit**, donc réglable jusqu'à ce que la moisson
plaise. Le compte de la phase 09 n'aurait plus de dénominateur : on ne saurait
plus combien de requêtes ont été essayées avant celle qu'on garde. C'est le
`p-hacking` déplacé du signal vers le corpus.

**3. Une taxonomie d'axes déclarés, ouverte à l'ajout, fermée à la
retouche.** Retenue.

**4. Laisser une IA choisir les requêtes** à partir de ce qui a bien marché.
Écartée pour la même raison que l'option 2 de `D20`, en pire : la sélection
serait non seulement non écrite, mais **adaptative aux résultats**.

## Le choix

**Les axes vivent dans `corpus/harvest_axes.yaml`, versionné.** Chacun porte un
identifiant `<axe>:<nom>`, une recherche, et **la date où il a été déclaré**.

**Ajouter un axe est libre. En modifier un qui a déjà servi ne l'est pas.**
`harvest.json` enregistre, pour chaque axe utilisé, **la chaîne de recherche
exacte au moment du passage** ; `check_harvest.py` compare et refuse un écart.
On peut donc ouvrir autant de pistes qu'on veut, mais aucune ne se réécrit après
avoir vu ce qu'elle a rendu.

Quatre axes : `asset`, `method`, `anomaly`, et `family` — ce dernier ne
contenant que les six familles de `D20`, **conservées telles quelles avec leur
date d'origine**, pour que les passages 1 et 2 restent lisibles.

## Pourquoi

**C'est la distinction que `D20` § Passage 2 avait déjà posée**, généralisée :
ce qui doit être figé, c'est **ce qui décide quels papiers peuvent apparaître**.
Un axe ajouté ne modifie aucun axe existant — il ouvre une piste **à côté**,
datée, et les papiers qu'il ramène portent la trace de l'axe qui les a fait
entrer. Un axe réécrit, lui, change rétroactivement le sens de ce qui a déjà
été moissonné : c'est le seul geste interdit.

**Le dénominateur de la phase 09 reste tenable** parce que `harvest.json` porte
la liste complète des axes, avec leurs dates. La question « combien de requêtes
avez-vous essayées avant de garder celle-là ? » a une réponse écrite : toutes
celles du fichier, aucune supprimée.

**Un papier peut entrer par plusieurs axes**, et c'est enregistré. `momentum
intra-journalier sur futures` apparaît sous `anomaly:intraday-momentum` et sous
`asset:futures` ; savoir lequel l'a amené n'a pas d'intérêt, savoir **qu'il est
au croisement de deux pistes** en a.

**Le moissonneur ne juge toujours pas.** Un axe est un périmètre de recherche,
pas un verdict d'implémentabilité. Le tri reste au trieur, jugé contre
`AMORCE.md` (`D15`), et `harvest.json` **n'entre toujours pas dans `G1`–`G4`**
(`F47`, `D20`).

**Ce qui est sacrifié.** La taxonomie est la nôtre et n'a aucune autorité
externe : `asset:futures` est un mot que nous avons choisi, pas une catégorie
d'OpenAlex. Elle décrit **notre intention de recherche**, ce qui est exactement
ce qu'on veut garder trace, et rien de plus.

## Ce que ça verrouille

- **`corpus/harvest_axes.yaml` devient une pièce du dépôt**, au même titre que
  `catalogue/catalogue.yaml`. On y ajoute ; on n'y réécrit pas une ligne qui a
  servi.
- **`check_harvest.py` gagne `H10`** : tout axe présent dans `harvest.json` doit
  exister dans le YAML **avec la même chaîne de recherche**.
- **`D20` § La requête est amendée** : les six familles ne sont plus la requête,
  elles sont **un axe parmi quatre**. Le filtre de domaine, la fenêtre de dates,
  le tri et le plafond de `D20` restent inchangés et communs à tous les axes.
- **Le compte de corpus de la phase 09 devra citer les axes utilisés**, avec
  leurs dates, comme la phase 15 citera `counted_tests()`.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Croiser deux axes dans une seule requête** (`asset:futures` ET `anomaly:carry`). Aujourd'hui les axes s'additionnent, ils ne se multiplient pas | si le rendement d'un axe seul devient trop bruité |
| **Retirer un axe qui ne rend rien** — jamais par suppression, seulement par une ligne `retired:` datée, le texte d'origine conservé | au premier axe stérile |
| **SSRN reste inaccessible et le restera.** `ACQUISITION.md` l'a constaté deux fois ; aucun axe ne change cela, et aucun contournement ne sera écrit. La route sanctionnée pour ce fonds est l'API *Text and Data Mining* d'Elsevier, qui demande un accès institutionnel | hors de ce dépôt |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Axes lancés | Candidats après | PDF |
|---|---|---|---|---|
| — | 2026-09-22 | décision écrite ; les 6 familles de `D20` reversées en `family:A`–`family:F` | 319 | 123 |
