# La Fabrique — constitution

Ce fichier est lu au début de chaque session. Il est la seule chose qui traverse
les sessions. Il se modifie rarement, et jamais sans une décision écrite dans
`decisions/`.

---

## Le but

La Fabrique transforme un corpus de papiers académiques en une poignée de
signaux dont les chiffres tiennent. Une IA lit les papiers, en extrait des
hypothèses testables, les implémente ; du code déterministe les juge. Le produit
final n'est pas une bibliothèque de signaux : c'est un petit nombre de signaux
survivants, accompagnés d'un compte honnête du nombre de tests qu'il a fallu
pour les trouver.

Pour un opérateur seul, qui exécutera lui-même les stratégies retenues, et qui
préfère trois signaux dont il connaît la fragilité à trente dont il ignore tout.

---

## Les cinq invariants

**I.** Le LLM propose, le code déterministe tranche. Le harnais d'évaluation est
figé, versionné, et aucun agent n'a le droit d'écriture dessus.

**II.** Le look-ahead est empêché par construction, jamais par vigilance. Le code
de signal n'a structurellement pas accès au futur.

**III.** Tout IC calculé est inscrit dans un registre append-only. Sans ce
compteur, tous les chiffres finaux sont faux.

**IV.** Toute hypothèse — régime, combinaison — est écrite et horodatée avant de
voir son résultat.

**V.** Le holdout n'est ouvert qu'une fois, à la toute fin. S'il est rouvert, il
n'est plus un holdout.

---

## Les deux ordres

Il y a deux séquences dans ce projet, et elles vont en sens contraire. Les
confondre est l'erreur la plus fréquente d'une session qui arrive froide.

**L'ordre d'exécution** — ce que fait la chaîne une fois construite, de l'étape
00 à l'étape 10 :

| Étape | |
|---|---|
| 00 | triage des données |
| 01 | extraction (papier → fiche) |
| 02 | codage du signal |
| 03 | contrôles |
| 04 | rapport d'IC |
| 05 | régimes |
| 06 | taxonomie |
| 07 | présélection de combinaisons |
| 08 | arbitrage |
| 09 | stratégie |
| 10 | backtest |

**L'ordre de construction** — dans quel ordre on fabrique ces étapes : *l'inverse*.
L'évaluation avant la production. Le juge avant l'accusé. On n'automatise jamais
la production de quelque chose qu'on ne sait pas encore juger. C'est cet ordre-là
que suit `ETAT.md`, phases 01 à 15.

Autrement dit : l'étape 04 de l'ordre d'exécution (le rapport d'IC) se construit
en phase 03, bien avant l'étape 02 (le codage du signal), qui se construit en
phase 08. Si tu te retrouves à écrire un signal alors que `ETAT.md` annonce la
phase 03, tu as confondu les deux ordres — arrête-toi.

---

## Les interdits

Ce ne sont pas des recommandations.

- **Ne jamais écrire de code de stratégie ou de backtest** avant que le harnais
  d'IC existe et soit calibré (porte 03).
- **Ne jamais calculer un IC hors de la fonction d'évaluation officielle.** Il ne
  doit exister aucun chemin de code qui produise un IC sans écrire au registre.
  Pas de corrélation calculée à la main dans un notebook, pas de « juste pour
  voir ».
- **Ne jamais lire la tranche `holdout`.** Aucune exception, aucune
  justification, aucune « simple vérification ».
- **Ne jamais inventer une valeur de données** — multiplicateur, tick, frais,
  fuseau, lag de publication. La valeur est `null` et une entrée `todo` est
  ouverte. Une valeur plausible inventée devient indétectable en aval ; un
  `null` est bruyant.
- **Ne jamais modifier le harnais pour faire passer un signal.** Le harnais est
  figé et versionné. S'il doit changer, c'est une décision écrite dans
  `decisions/`, et **tous les résultats antérieurs sont réputés périmés**.
- **Ne jamais supprimer ni réécrire une ligne** de `registry/tests.jsonl` ou de
  `LECONS.md`.
- **Ne jamais franchir une porte « provisoirement, on y reviendra ».** Une porte
  à moitié franchie est une porte non franchie.
- **Aucune dépendance accédant au réseau** dans le chemin de calcul d'un signal.

---

## Le vocabulaire

Les sessions successives emploient ces mots, et seulement ceux-là.

- **fiche** — le JSON structuré extrait d'un papier : hypothèse, univers,
  horizon, construction du signal, résultats annoncés, ce qui manque.
- **signal** / **score** — la fonction qui, à une date et pour un instrument,
  produit un nombre. Le *score* est sa sortie.
- **harnais** — le code déterministe qui évalue un signal. Figé, versionné, non
  modifiable par un agent.
- **rapport d'IC** — la sortie officielle du harnais : IC, t-stat, décomposition,
  contrôles. Seule source d'IC du projet.
- **registre** — `registry/tests.jsonl`, append-only, une ligne par IC calculé.
- **tranche** — découpe temporelle des données : `research` (on y travaille),
  `validation` (on y confirme, parcimonieusement), `holdout` (scellé jusqu'à la
  phase 15).
- **porte** — condition explicite de passage d'une phase à la suivante. Binaire.
- **hybride** — un signal conditionné à un régime.
- **nœud**, **moule** — vocabulaire du moteur RSL. Voir
  `reference/rsl-squelette-v1.json`.

---

## Où trouver quoi

```
CLAUDE.md      ce fichier. La constitution.
ETAT.md        phase courante, portes, prochaine action. À lire en premier,
               à mettre à jour en dernier.
LECONS.md      les erreurs apprises. Numérotées, jamais supprimées.
decisions/     une décision structurante par fichier, suivant TEMPLATE.md.
corpus/        pdf/ les papiers (ignoré par git) ; fiches/ les JSON extraits
               (versionnés — ce sont des résultats, pas des données).
catalogue/     catalogue.yaml : l'inventaire des instruments et de leurs
               métadonnées point-in-time, et son validateur.
harness/       le harnais d'évaluation. Code figé, versionné, protégé.
signals/       les implémentations de signaux, une par signal.
registry/      SCHEMA.md et tests.jsonl. Append-only. Irremplaçable.
scripts/       outils ponctuels : portes, inventaires, vérifications.
reference/     documents externes en lecture seule, datés.
```

---

## Conventions

**Langue.** Prose et documents en français. Code, noms de champs et clés de
schéma en anglais, sans exception — y compris dans le catalogue YAML et les
fiches JSON. **Une seule dérogation :** les champs imposés par RSL gardent le nom
que RSL leur donne (`close_stamp`, `granularity_minutes`,
`publication_lag_minutes`, `known_in_advance`, `root`, …), y compris quand ce nom
est irrégulier.

**Le moteur de backtest est externe** à ce dépôt. Son mode d'attache — sous-module,
dépendance installée, copie — sera tranché en phase 10 par une décision écrite.
`reference/rsl-squelette-v1.json` n'est pas le moteur : c'est une photographie
datée de son vocabulaire, en lecture seule, que le catalogue doit respecter au
mot près.

**Données.** Elles vivent hors du dépôt, à l'emplacement donné par la variable
d'environnement `RSL_DATA_DIR` (voir `.env`, non versionné ; `.env.example` l'est).
Aucun chemin absolu en dur dans le code.

**Python 3.13, `uv`, `ruff`** pour le format et le lint. Le verrou de dépendances
est commité.

**Git.** Travail solo, branches légères. Le dépôt distant est privé et sert de
sauvegarde : `registry/tests.jsonl` et `LECONS.md` sont append-only et
irremplaçables. Perdre le code coûte du temps ; perdre le registre coûte la
validité statistique de tout ce qui a été fait avant.

---

## Comment on prend une décision

Toute décision structurante — univers, fournisseur de données, métrique,
définition d'une tranche, changement du harnais, attache du moteur — donne lieu à
un fichier dans `decisions/`, suivant `decisions/TEMPLATE.md`, numéroté et daté.

**Une décision non écrite n'existe pas.** Si une session future ne trouve pas
trace écrite d'un choix, elle a le droit — et le devoir — de le rouvrir.

---

## Comment démarrer une session

Tu arrives froid. Tu ne sais rien de ce qui précède. Dans l'ordre :

1. Lis `ETAT.md`. Il te dit la phase courante, la dernière porte franchie, et la
   prochaine action.
2. Lis `LECONS.md` en entier. Il est court, et il est là pour t'éviter de refaire
   une erreur déjà payée.
3. Lis la décision la plus récente dans `decisions/`, et toute décision que
   `ETAT.md` désigne comme pertinente pour la phase courante.

**Ne commence pas à coder avant de savoir quelle phase est en cours et quelle
porte est ouverte.** Si `ETAT.md` et ce que tu lis dans le dépôt se contredisent,
arrête-toi et signale la contradiction — ne tranche pas seul.

En fin de session : mets `ETAT.md` à jour, et ajoute une entrée à `LECONS.md` si
tu as appris quelque chose qui vaut d'être payé une seule fois.
