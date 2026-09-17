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
- **nœud**, **moule** — vocabulaire du moteur tiers, utile pour le lire, sans
  autorité sur nos propres schémas. Voir `reference/rsl-squelette-v1.json`.

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
panel/         la couche de données point-in-time. Un Panel s'ouvre à une date
               et ne lit jamais une barre postérieure. Voir DECISION-03.
harness/       le harnais d'évaluation. Code figé, versionné, protégé.
signals/       les implémentations de signaux, une par signal.
registry/      SCHEMA.md et tests.jsonl. Append-only. Irremplaçable.
scripts/       outils ponctuels : portes, inventaires, vérifications.
reference/     documents externes en lecture seule, datés.
wiki/          la mémoire entre sessions, tenue par l'agent. Dérivée, sans
               autorité. Voir « Wiki » ci-dessous et wiki/SCHEMA.md.
```

---

## Wiki

`wiki/` est la mémoire du projet entre les sessions : un wiki en markdown que
**l'agent écrit et tient lui-même**. Il existe parce qu'une session arrive froide
et redécouvre sinon ce qui a déjà été payé. Établi par
`decisions/DECISION-02-wiki.md` ; ses conventions internes sont dans
`wiki/SCHEMA.md`.

### Les deux règles permanentes

**Avant de commencer un travail de fond** — lire `wiki/index.md` **et**
`wiki/Failed Ideas/ledger.md`. Le second en entier : c'est le registre des idées
déjà essayées et abandonnées, avec la raison. Il est là pour t'empêcher de
repayer un cul-de-sac.

**Avant de finir** — mettre à jour la ou les pages concernées, **ajouter une
ligne datée à `wiki/log.md`**, et **ajouter une ligne à
`wiki/Failed Ideas/ledger.md` pour tout abandon**, avec sa raison.

Ces deux règles **s'ajoutent** à la séquence de démarrage et de fin de session
ci-dessous ; elles n'en remplacent aucune étape.

### Le wiki n'a aucune autorité

Il **lie** vers la source — données, code, sorties, décisions, registre — et n'en
recopie jamais le contenu comme source de vérité. Si une page et sa source se
contredisent, **la source gagne** et la page est corrigée.

En particulier, et cela découle des invariants III et IV :

- **aucun IC, t-stat ou Sharpe n'est écrit dans le wiki** autrement que recopié
  d'un rapport d'IC officiel, avec son `test_id`. Une page de wiki n'est jamais
  un chemin de production d'IC ;
- **une page de wiki ne vaut pas hypothèse pré-enregistrée.** Elle la référence ;
- `wiki/log.md` est **append-only**, comme `registry/tests.jsonl` et `LECONS.md` ;
- `wiki/hot.md` est **généré** par `wiki/update_hot.py` : ne pas l'éditer, hors
  du bloc « Prochaines actions » prévu pour ça ;
- `wiki/lessons.md` **synthétise** `LECONS.md`, qui reste seul autoritatif.

Le lint mécanique se passe par `python wiki/update_hot.py --lint`.

**Obsidian réécrit `.obsidian/graph.json` pendant qu'il tourne.** Ne modifier ce
fichier que **fenêtre fermée**, sans quoi la modification est perdue au prochain
enregistrement d'Obsidian.

---

## Conventions

**Langue.** Prose et documents en français. Code, noms de champs et clés de
schéma en anglais, sans exception — y compris dans le catalogue YAML et les
fiches JSON. Les clés sont choisies pour elles-mêmes, claires et régulières :
**aucun vocabulaire externe ne s'impose au nôtre**, faute de contrainte
d'interopérabilité (voir `decisions/DECISION-00-moteur-externe.md`).

**Le moteur de backtest est un composant tiers, et nous ne l'avons pas encore.**
Il est attendu ; d'ici là, aucune ligne de code de ce projet n'en dépend, et son
mode d'attache — sous-module, dépendance installée, reprise du code — sera
tranché en phase 10 par une décision écrite. S'il n'arrive pas, la phase 10
devient « construire un moteur ».
`reference/rsl-squelette-v1.json` n'est pas ce moteur et n'en est pas
l'auto-description : c'est la référence de conception d'un moteur tiers, datée et
en lecture seule. Les chiffres qu'elle contient sont les constats d'un tiers, sur
ses données : ils disent quoi vérifier, jamais ce qui est vrai ici. Voir
`reference/README.md`.

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

0. Lis `wiki/index.md`, puis `wiki/Failed Ideas/ledger.md` **en entier**, puis
   `wiki/hot.md` pour l'état courant. Voir « Wiki » ci-dessus.
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
tu as appris quelque chose qui vaut d'être payé une seule fois. Puis mets à jour
les pages de `wiki/` que tu as touchées, ajoute une ligne à `wiki/log.md`, et une
ligne au registre des idées abandonnées si tu as abandonné quelque chose.
