# D02 — Un wiki tenu par l'agent, et ce qu'il n'a pas le droit d'être

**Date :** 2026-09-16
**Phase :** 02
**État :** prise

---

## La question

Chaque session arrive froide et reconstruit le même contexte : pourquoi FDAX est
dehors, pourquoi l'IC transversal est refusé, ce qui bloque la phase 02. Ce
savoir tient aujourd'hui dans quatre fichiers denses qu'il faut relire en entier.
Faut-il une mémoire accumulée entre sessions, et si oui, comment l'empêcher de
devenir une seconde source de vérité concurrente du registre ?

## Les options

| | **A — statu quo** | **B — wiki tenu par l'agent** | **C — étendre `ETAT.md`** |
|---|---|---|---|
| Coût de démarrage d'une session | relire `CLAUDE.md` + `ETAT.md` + `LECONS.md` + la dernière décision, ~12 000 mots | lire `wiki/index.md` + `wiki/hot.md`, puis descendre au besoin | intermédiaire |
| Risque de source de vérité concurrente | nul | **réel — c'est le danger central** | faible |
| Accumulation entre sessions | aucune : ce qui n'est pas écrit dans une décision est perdu | oui, par pages liées | limitée : un fichier plat ne tient pas 15 phases |
| Prévention des culs-de-sac déjà payés | `LECONS.md` seul, qui ne recense que les erreurs *coûteuses* | registre explicite des idées abandonnées, y compris celles abandonnées à raison et sans douleur | non |

L'option C a été écartée en une ligne : `ETAT.md` est un tableau de bord, pas une
mémoire ; le gonfler détruirait sa propriété d'être lu en entier en deux minutes.

## Le choix

Un wiki en markdown sous `wiki/`, écrit et tenu **par l'agent**, lu au début de
chaque session et mis à jour avant la fin — **strictement dérivé**, jamais
autoritatif.

## Pourquoi

Parce que la charge qui tue les wikis est la tenue à jour, et qu'elle est quasi
nulle pour un agent. Et parce que le coût réel de ce projet n'est pas d'écrire du
code : c'est de redécouvrir. Le registre des idées abandonnées
(`wiki/Failed Ideas/ledger.md`) vaut à lui seul la construction : il empêche de
repayer un cul-de-sac dont personne ne se souvient qu'il en était un.

Ce qui est sacrifié : un répertoire de plus à maintenir, et un risque nouveau et
sérieux — qu'une page du wiki soit lue comme un fait alors qu'elle n'est qu'un
résumé. D'où la clause de subordination ci-dessous, qui est la vraie substance de
cette décision.

## Ce que ça verrouille

### 1. La subordination — le wiki n'a aucune autorité

Le wiki **pointe** vers la source autoritative ; il n'en recopie jamais le contenu
comme vérité. En cas de contradiction entre une page du wiki et sa source, **la
source gagne, toujours, sans discussion**, et la page est corrigée.

| Sujet | Autorité | Le wiki a le droit de |
|---|---|---|
| Les invariants, les interdits | `CLAUDE.md` | lier, résumer en signalant le résumé |
| Phase, porte, prochaine action | `ETAT.md` | lier, refléter |
| Les leçons numérotées | `LECONS.md` | lier, synthétiser transversalement |
| Un choix structurant | `decisions/DNN` | lier, router |
| **Tout IC, t-stat, compte de tests** | `registry/tests.jsonl` via le harnais | **lier uniquement** |
| Les chiffres mesurés | `scripts/out/*.json` | citer avec le fichier source nommé |

### 2. Ce qui devient interdit, en plus des interdits existants

- **Aucun chiffre d'IC, de t-stat ou de Sharpe n'est écrit dans le wiki** autrement
  que recopié d'un rapport d'IC officiel, avec son `test_id`. Une page du wiki
  n'est jamais un chemin de production d'IC (invariant III).
- Le wiki **ne contient aucune donnée de marché**, aucun extrait de série.
- Une page du wiki **ne vaut pas hypothèse pré-enregistrée** au sens de
  l'invariant IV. Une hypothèse s'écrit là où l'invariant IV le prévoit ; le wiki
  la référence.
- `wiki/hot.md` est **généré** par `wiki/update_hot.py`. Aucune main humaine ni
  agentique ne l'édite, hors du bloc « Prochaines actions » explicitement réservé.
- `wiki/log.md` est **append-only**, comme le registre et `LECONS.md`.

### 3. Ce qui change dans `CLAUDE.md`

Une section « Wiki » est ajoutée, portant les deux règles permanentes de lecture
et de mise à jour, et la règle d'immuabilité ci-dessus. C'est la seule
modification de la constitution autorisée par cette décision.

### 4. Automatisation

`.claude/settings.json` porte trois crochets, tous *best-effort* et incapables de
faire échouer une session : `git pull --ff-only` au démarrage, régénération de
`wiki/hot.md` à l'arrêt, commit et poussée horodatés à l'arrêt.

## Ce qui reste ouvert

| Point | Échéance | Statut |
|---|---|---|
| Un moteur de recherche sur le wiki (type `qmd`) | quand `wiki/index.md` cessera de suffire, ~100 pages | non tranché, inutile aujourd'hui |
| Une page par signal (`wiki/signaux/`) | phase 08 | dossier créé, vide et assumé vide |
| Le commit automatique à l'arrêt | à surveiller | il commite l'arbre entier, travail en cours compris. À restreindre si ça gêne. |
