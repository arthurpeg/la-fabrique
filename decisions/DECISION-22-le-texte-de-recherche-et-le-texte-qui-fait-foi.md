# D22 — Le texte de recherche n'est pas le texte qui fait foi

**Date :** 2026-09-23
**Phase :** 07 (construit), 09 (utilisé)
**État :** prise — précise la portée de `D18`

## La question

La base vectorielle doit contenir les 123 papiers moissonnés pour être utile.
Leur texte n'est pas versionné dans `corpus/text/`. Faut-il l'y verser — 246
fichiers, ~40 Mo — ou peut-on l'ingérer sans lui donner ce statut ?

## Les options

**1. Verser les 123 dans `corpus/text/`.** Écartée pour l'instant. `D18` a pesé
6,2 Mo pour 18 papiers ; 40 Mo pour un corpus dont on ne sait pas encore ce
qu'il vaut, c'est payer d'avance. Et le versionner reviendrait à dire que `F2`
peut s'en servir, ce qui est faux tant que rien ne l'a vérifié.

**2. Ne pas les ingérer.** Écartée : la base ne sert alors à rien pour la
phase 09, qui demande 30 à 50 papiers.

**3. Les ingérer en disant, DANS LA DONNÉE, que leur texte ne fait pas foi.**
Retenue.

**4. Les ingérer sans le dire.** Écartée, et c'est la seule vraiment
dangereuse. Une fois en base, un morceau de papier moissonné est
indiscernable d'un morceau de papier `D18`. Quelqu'un — une session future,
l'extracteur — en tirerait une citation en croyant qu'elle a été vérifiée.

## Le choix

**Les deux textes coexistent, et la table le dit.** `papers.text_source` vaut
`authoritative` ou `harvest`, sans défaut : tout appelant doit trancher.

| | `authoritative` | `harvest` |
|---|---|---|
| Origine | `corpus/text/`, versionné, empreinte au manifeste | le PDF, lu à l'ingestion |
| Reproductible depuis le dépôt | **oui** | **non** — `corpus/pdf/` est ignoré par git |
| `F2` peut s'en servir | **oui** | **non** |
| Sert à chercher | oui | oui |

**Un papier `harvest` qui devient fiché doit d'abord passer par `D18`** : son
texte est versionné, son empreinte inscrite au manifeste, et sa ligne repasse
à `authoritative`. C'est l'ordre, et il n'a pas d'exception.

## Pourquoi

**Chercher et juger ne demandent pas la même chose.** `corpus/text/` existe
parce que `F2` vérifie une citation **lettre par lettre** : il lui faut un
texte figé, versionné, reproductible sous un `pypdf` épinglé (`D19`). Trouver
un passage n'exige rien de tel — un texte approximatif retrouve le bon papier.

Appliquer l'exigence du juge à l'outil de recherche coûterait 40 Mo et
n'achèterait rien. L'inverse — laisser croire que le texte de recherche fait
foi — coûterait une citation fausse, invisible.

**La distinction vit dans la DONNÉE, pas dans la prose.** Une note de README
ne protège personne : elle n'est lue ni par une requête SQL, ni par une session
future qui interroge la base. Une colonne, si. C'est le même raisonnement que
`embedding_model`, qui empêche de mélanger deux modèles en silence.

**Sans défaut, délibérément.** `text_source` n'a pas de valeur par défaut :
insérer un papier oblige à dire d'où vient son texte. Un défaut ferait passer
l'oubli pour un choix.

**Ce qui est sacrifié.** Le corpus moissonné n'est pas rejouable : `corpus/pdf/`
est ignoré par git, donc une autre session ne reconstruira pas ces morceaux à
l'identique. Assumé — c'est un index de recherche, pas une pièce du dossier.
`corpus/harvest.json`, lui, est versionné et dit comment retrouver chaque PDF.

## Ce que ça verrouille

- **`papers.text_source` devient obligatoire**, migration `002`.
- **`F2` ne lit jamais la base** — il lit `corpus/text/`, et rien d'autre. La
  base n'est pas un chemin de vérification.
- **Ficher un papier `harvest` exige de verser son texte dans `corpus/text/`
  d'abord**, avec son empreinte, sous le `pypdf` de `D19`.
- **Le compte de la phase 09 devra distinguer les deux** : un corpus de
  50 papiers dont 40 `harvest` n'est pas un corpus de 50 papiers vérifiables.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Verser tout ou partie des moissonnés dans `corpus/text/`** si la phase 09 en retient beaucoup. Le coût en dépôt se réévaluera alors sur un compte connu, pas sur une hypothèse | à la sélection de la phase 09 |
| **La qualité du texte moissonné n'est pas mesurée.** Les 18 PDF d'`AMORCE` ont été vus un par un ; les 123 non. Un scan illisible produira des morceaux illisibles, et seule leur inutilité en recherche le révélera | au premier papier moissonné qu'on veut ficher |
| **Un marqueur par MORCEAU** plutôt que par papier, si un jour un papier mélange les deux origines. Aucun cas aujourd'hui | au premier cas |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Ce qui a changé | Effet |
|---|---|---|---|
| 1 | 2026-09-23 | décision prise ; migration `002`, les 17 papiers existants passent à `authoritative` | — |
| 2 | 2026-09-24 | phase 09, sélection : le triage du 2026-09-23 a retenu 39 papiers moissonnés sur 119 (`oui`+`partiel`). `corpus/promote_harvest.py` écrit — télécharge le PDF de chaque retenu (déjà sondé `atteignable` par `harvest.py`), le copie dans `corpus/pdf/` où `extract_text.py` le trouve, sans toucher `corpus/acquisition.json` (`F47`, la population `G1`-`G4` reste les 20 d'`AMORCE.md`). `corpus/extract_text.py` relancé, `pypdf` `6.14.2` épinglé (`D19`) | 36 promus ; 1 exclu — bug `pypdf` reproductible (`ZeroDivisionError`, mode `layout`, page 30) sur un PDF précis, non contourné, retiré de `corpus/pdf/` et de `harvest_promoted.json` ; 1 doublon sha256 avec `gao-2018-market-intraday-momentum.pdf` (déjà `authoritative` depuis `L20`) — non recopié. **35 papiers avec texte D18 complet (default+layout)**, `text_source` basculé `harvest -> authoritative` pour 34 (le doublon partage déjà le statut de `gao-2018`). `corpus/text/` : 104 fichiers, manifeste conforme. `G1`-`G4` inchangés (`extract_fiche.py --list` toujours 17 fichées) |
