---
type: hub
updated: 2026-09-16
status: actif
sources: [CLAUDE.md, decisions/DECISION-02-wiki.md]
---

# SCHEMA — le règlement du wiki

> Ce fichier dit **comment** le wiki est écrit. Il ne dit rien du projet.
> Pour le projet, l'autorité est `CLAUDE.md`. Voir `decisions/DECISION-02-wiki.md`.

---

## 0. La clause qui prime sur tout le reste

**Le wiki est dérivé. Il n'a aucune autorité.**

Il **lie** vers la source ; il n'en recopie jamais le contenu comme vérité. Si une
page et sa source se contredisent, **la source gagne** et la page est corrigée
dans la foulée, sans débat.

| Sujet | Source autoritative |
|---|---|
| Invariants, interdits, vocabulaire | `CLAUDE.md` |
| Phase courante, portes, prochaine action | `ETAT.md` |
| Leçons numérotées | `LECONS.md` |
| Choix structurants | `decisions/DNN-*.md` |
| **IC, t-stat, comptes de tests** | `registry/tests.jsonl`, via le harnais |
| Chiffres mesurés | `scripts/out/*.json` |
| Papiers | `corpus/AMORCE.md`, `corpus/fiches/*.json` |

**Interdits propres au wiki**, en plus de ceux de `CLAUDE.md` :

- Aucun IC, t-stat ou Sharpe écrit ici autrement que **recopié d'un rapport d'IC
  officiel, avec son `test_id`**. Une page de wiki n'est jamais un chemin de
  production d'IC (invariant III).
- Aucune donnée de marché, aucun extrait de série.
- Une page de wiki **ne vaut pas hypothèse pré-enregistrée** (invariant IV). Elle
  la référence, elle ne la tient pas.
- `wiki/hot.md` est généré. On ne l'édite pas à la main, hors du bloc
  « Prochaines actions » explicitement réservé.
- `wiki/log.md` est **append-only**, comme le registre et `LECONS.md`.

**Attention au faux ami :** `wiki/reference/` (pages-routeurs, § 1.6) n'a rien à
voir avec `reference/` à la racine (documents tiers datés, en lecture seule,
décrits par `reference/README.md`).

---

## 1. Les gabarits de page

Toute page porte un frontmatter YAML. Les **clés sont en anglais**, la **prose en
français** — convention de `CLAUDE.md`. Les dates sont ISO, `AAAA-MM-JJ`.

Clés communes à tous les types :

| Clé | Obligatoire | Contenu |
|---|---|---|
| `type` | oui | `hub`, `phase`, `signal`, `concept`, `research`, `router` |
| `updated` | oui | date de la dernière modification réelle du contenu |
| `status` | oui | voir la valeur permise par type, ci-dessous |
| `sources` | oui | liste de chemins du dépôt faisant autorité pour cette page |

### 1.1 Entrée d'`index.md`

Une ligne, pas une page :

```
- [[chemin/page|Titre]] — une phrase de quoi il retourne. `status`
```

Ordre : par dossier, puis alphabétique. Une page absente de l'index est orpheline
et sera relevée au lint.

### 1.2 `type: phase` — `wiki/phases/`

L'unité de travail **courante** : une phase de construction, une porte.

```markdown
---
type: phase
updated: AAAA-MM-JJ
status: a-faire | en-cours | bloquee | franchie
phase: NN
gate: la condition de passage, en une phrase
blocked_by: ce qui manque, ou null
sources: [ETAT.md, decisions/DNN-....md]
---

# Phase NN — titre

## La porte
La condition exacte, reprise de `ETAT.md`. Binaire.

## Pourquoi cette phase existe
Deux à cinq lignes. Ce que le projet ne peut pas faire tant qu'elle n'est pas
franchie.

## Ce qui est acquis
Puces, chacune liée à sa source.

## Ce qui manque
Puces. Un `null` ouvert est une puce, pas un silence.

## Pièges connus
Liens vers `LECONS.md` et vers [[Failed Ideas/ledger]].

## Voir aussi
Wikilinks.
```

### 1.3 `type: signal` — `wiki/signaux/`

L'unité de travail **du produit fini**. Un signal implémenté et jugé. Aucune page
avant la phase 08.

```markdown
---
type: signal
updated: AAAA-MM-JJ
status: propose | code | evalue | retenu | abandonne
signal_id: l'identifiant utilisé par le registre
hypothesis_ref: la référence de l'hypothèse pré-enregistrée
fiche: corpus/fiches/....json
test_ids: [liste des test_id du registre]
sources: [signals/..., registry/tests.jsonl]
---

# signal_id — titre lisible

## L'hypothèse
Ce qui était prédit, **tel qu'écrit avant le test**. Jamais reformulé après coup.

## La construction
Comment le score est calculé, en prose. Le code fait foi, pas ce paragraphe.

## Verdict
Renvoi au rapport d'IC par `test_id`. **Les chiffres ne sont pas retapés ici**
hors de ce renvoi ; une seule ligne de synthèse est tolérée, citant son `test_id`.

## Ce qu'on a appris
Y compris quand le verdict est nul — surtout quand il est nul.

## Voir aussi
```

> Un signal qui passe en `status: abandonne` **exige** une ligne dans
> [[Failed Ideas/ledger]]. Ce n'est pas une option.

### 1.4 `type: concept` — `wiki/concepts/`

Un terme, une page. Pour qu'on entende la même chose.

```markdown
---
type: concept
updated: AAAA-MM-JJ
status: stable | provisoire | conteste
sources: [...]
---

# Terme

**En une phrase.**

## Ce que ça veut dire ici
Le sens dans *ce* projet, qui n'est pas forcément le sens usuel.

## Ce que ça ne veut pas dire
La confusion à éviter. Souvent la moitié utile de la page.

## Où c'est fixé
Lien vers la source autoritative.

## Voir aussi
```

### 1.5 `type: research` — `wiki/research/`

Un papier ou une source externe ingérée.

```markdown
---
type: research
updated: AAAA-MM-JJ
status: repere | lu | fiche | replique | ecarte
ref: Auteur (Année)
amorce_entry: le numéro dans corpus/AMORCE.md, ou null
fiche: corpus/fiches/....json, ou null
implementable: oui | partiel | non
sources: [corpus/AMORCE.md, ...]
---

# Auteur (Année) — titre

## Ce que le papier affirme

## Ce qu'il exige comme données
Et ce que nous avons, ou pas.

## Pourquoi ça nous concerne

## Réserves
Le préprint non arbitré, l'échantillon court, l'hypothèse de coût. Écrites
**avant** de tester, pas après.

## Statut chez nous
Fiche produite ? signal codé ? écarté, et pourquoi ?

## Voir aussi
```

> **`status: repere` n'est pas `lu`.** `corpus/AMORCE.md` le dit explicitement :
> aucune de ces références n'a été lue intégralement. Ne jamais promouvoir une
> page en `lu` sans l'avoir lue.

### 1.6 `type: router` — `wiki/reference/`

Une page-routeur **ne contient aucun fait**. Elle dit seulement où le fait est
écrit. Si tu te surprends à expliquer quelque chose dans un routeur,
l'explication appartient à une autre page.

```markdown
---
type: router
updated: AAAA-MM-JJ
status: actif
sources: [...]
---

# Où trouver : sujet

| Question | Autorité |
|---|---|
| … | `chemin/fichier.md` § section |

Rien d'autre. Pas de résumé, pas de chiffre.
```

---

## 2. Les enchaînements

### 2.1 Au démarrage d'une session — obligatoire

1. `wiki/index.md`
2. `wiki/Failed Ideas/ledger.md` — **en entier**
3. `wiki/hot.md` — l'état courant, généré
4. puis la séquence de `CLAUDE.md` § « Comment démarrer une session » :
   `ETAT.md`, `LECONS.md`, la décision pertinente

Le wiki **ajoute** une lecture, il n'en remplace aucune.

### 2.2 Avant de finir une session — obligatoire

1. Mettre à jour la ou les pages touchées, et leur `updated:`.
2. Ajouter la ou les lignes manquantes à `wiki/index.md`.
3. **Ajouter une ligne à `wiki/log.md`** — append-only, format § 2.6.
4. Si quoi que ce soit a été abandonné : **une ligne dans
   [[Failed Ideas/ledger]]**, avec la raison.
5. Mettre à jour `ETAT.md` (règle de `CLAUDE.md`, inchangée).
6. `wiki/hot.md` se régénère tout seul au crochet `Stop`. Ne pas l'écrire.

### 2.3 Ingérer un papier

1. Lire la source. Si elle n'est pas lue, le statut reste `repere`.
2. Créer `wiki/research/auteur-annee-motclef.md` au gabarit § 1.5.
3. Créer la page de concept manquante pour tout terme employé qui n'en a pas.
4. Mettre à jour les pages de phase et de concept que le papier touche.
5. Ligne d'index, ligne de log.
6. La **fiche** JSON (`corpus/fiches/`) reste l'artefact autoritatif de la phase
   07. La page de wiki ne la remplace pas ; elle la commente et la lie.

### 2.4 Franchir une porte

1. Passer la page de phase en `status: franchie`, dater.
2. Créer la page de la phase suivante si elle n'existe pas.
3. Ligne de log de type `gate`.
4. `ETAT.md` fait foi. La page de wiki le reflète, jamais l'inverse.

### 2.5 Abandonner une idée

Une ligne dans [[Failed Ideas/ledger]]. **Avec la raison, et le lien vers la
mesure ou la décision qui l'a tuée.** Une raison du genre « ça ne marchait pas »
est une ligne inutile : elle ne dissuade personne de recommencer.

Si l'abandon a coûté quelque chose — du temps, un résultat faux, un test gaspillé
— alors il relève aussi de `LECONS.md`, qui est prioritaire et fait foi. Le
ledger le référence alors, il ne le double pas.

### 2.6 Le format du log

Une ligne, jamais éditée :

```
## [AAAA-MM-JJ] <type> | <ce qui s'est passé> | <résultat>
```

`<type>` parmi : `setup`, `ingest`, `gate`, `decision`, `measure`, `signal`,
`lint`, `query`, `abandon`.

Le préfixe est fixe pour rester greppable :

```
grep "^## \[" wiki/log.md | tail -5
```

---

## 3. Le lint

À passer quand le wiki a grossi, ou sur demande — pas à chaque session.
`python wiki/update_hot.py --lint` en fait la part mécanique ; le reste demande
de lire.

### 3.1 Mécanique

| Contrôle | Ce qu'on cherche |
|---|---|
| **Orphelines** | page présente sur le disque, absente d'`index.md` et citée par aucun wikilink |
| **Liens morts** | `[[cible]]` sans page correspondante |
| **Frontmatter** | `type`, `updated`, `status`, `sources` manquants ou hors valeurs permises |
| **Périmées** | `updated` antérieur à la dernière modification d'une source citée |
| **Log** | ligne ne respectant pas `## [date] type \| … \| …` |

### 3.2 De jugement — en lisant

| Contrôle | Ce qu'on cherche |
|---|---|
| **Contradictions** | deux pages qui affirment l'inverse ; une page qui contredit `ETAT.md`, `LECONS.md` ou une décision |
| **Supersession** | une page qu'une décision plus récente a rendue fausse sans que personne l'ait rouverte |
| **Concepts manquants** | un terme employé dans trois pages ou plus et sans page à lui |
| **Autorité usurpée** | un chiffre écrit dans le wiki sans citation de sa source — **le défaut le plus grave**, à traiter avant tous les autres |
| **Ledger muet** | un `status: abandonne` sans ligne dans le ledger |
| **Trous** | une question posée deux fois en session et toujours sans page |

### 3.3 Ce que le lint n'est pas

Il ne réécrit pas `LECONS.md`, ne touche pas au registre, ne « range » pas le log.
Il produit une liste de corrections à faire, et une ligne de log `lint`.
