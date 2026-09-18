---
type: phase
updated: 2026-09-18
status: en-cours
phase: 07
gate: 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict humain de référence
sources: [ETAT.md, corpus/AMORCE.md, decisions/DECISION-06-signaux-de-reference.md]
---

# Phase 07 — Triage et extraction

**Ouverte le 2026-09-18**, à la fermeture de la porte 06. C'est la première phase
de l'Acte II qui produit quelque chose que le projet consommera ensuite : des
**fiches**.

## La porte

> 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict
> humain de référence. Point de départ : `corpus/AMORCE.md`.

Deux choses distinctes, et la seconde est la plus dure.

**L'extraction** — d'un PDF à une fiche structurée : hypothèse, univers, horizon,
construction du signal, résultats annoncés, ce qui manque
([[index|vocabulaire de `CLAUDE.md`]]). **Le schéma est écrit** depuis le
2026-09-18 : `corpus/SCHEMA.md`, gardé par `corpus/validate_fiches.py`.

**Le triage** — décider qu'un papier est implémentable sur neuf futures intraday,
en OHLCV, sans donnée extérieure.

## Le banc d'essai existe déjà, et ce n'est pas le produit

Trois fiches ont été écrites **à la main** le 2026-09-18, parce que la clause 2
de la porte 06 exigeait de lire les papiers qu'elle visait :

| Fiche | Ce qu'elle a servi |
|---|---|
| `mesfin-2026-ohlcv-falsification.json` | résultat négatif, calibrage d'attente ([[research/mesfin-2026-falsification]]) |
| `heston-2010-intraday-periodicity.json` | cible écartée — motif absent (`H03`) |
| `andersen-bollerslev-1997-periodicity.json` | cible retenue — porte franchie (`H04`) |

Elles sont à la phase 07 ce que `H01` et `H02` étaient aux portes 05, 06 et 08 :
un **sujet dont la réponse est connue**, pour juger l'automate. Écrire
l'extracteur d'abord et vérifier ensuite inverserait l'ordre de construction —
`D06` a tranché exactement cette question pour les signaux
([[Failed Ideas/ledger#F18]]).

## Le verdict humain de référence existe aussi, et il est honnête

`corpus/AMORCE.md` porte une colonne « implémentable » renseignée à la main sur
**24 entrées** — `oui`, `partiel`, `non` — avec le motif de chacune. Elle a été
écrite en **phase 01**, avant le harnais, avant les signaux, avant le moindre
résultat. C'est ce qui en fait un étalon utilisable : son auteur ne pouvait pas
savoir ce que les mesures diraient.

## Ce qu'il faudra trancher par écrit avant de coder

~~**Le schéma de fiche.**~~ **Fait le 2026-09-18** — `D14`, `corpus/SCHEMA.md`,
`corpus/validate_fiches.py`. Le schéma n'est pas tiré des trois fiches manuelles,
qui divergeaient ([[Failed Ideas/ledger#F35]]) : il reprend les **six champs que
`CLAUDE.md` § Le vocabulaire nomme depuis le premier jour** — hypothèse, univers,
horizon, construction du signal, résultats annoncés, ce qui manque — plus la
`source` et la `transposability`, que la pratique a rendues indispensables. Les
trois fiches ont été **réécrites** au schéma : c'était le test du schéma autant
que des fiches.

~~**`D09` étendu aux fiches.**~~ **Fait le même jour.** Chaque résultat annoncé
porte sa citation, et le validateur vérifie que **la valeur s'y retrouve**, en
réutilisant `value_in_quote` — le garde même du catalogue. Deux échappatoires
nommées plutôt que cachées : `derived` pour un nombre que *nous* avons calculé,
`spelled_out` pour un nombre que le papier écrit en toutes lettres
([[Failed Ideas/ledger#F36]]). `corpus/check_fiches_guard.py` montre le garde
refuser **11 fautes**, chacune pour la raison prévue.

**Ce que « écarte ce qu'il doit écarter » veut dire en chiffres.** Rappel et
précision contre la colonne d'`AMORCE.md`, avec un seuil écrit **avant** de
mesurer. `L06` s'applique mot pour mot : *un compte juste n'est pas un compte de
choses justes* — un trieur jugé sur « combien il en trouve » plutôt que sur
« lesquels » doit être supposé faux jusqu'à appariement.

## Ce qu'on sait déjà du produit de cette phase

**Le corpus implémentable est attendu mort.** Mesfin (2026) est transportable
depuis `L14` ; `H01`, `H02` et `H03` n'ont rien trouvé. La phase 07 doit être
construite en sachant que sa sortie a de fortes chances d'être une liste de
signaux nuls.

Ce n'est pas un problème : c'est le but écrit dans `CLAUDE.md` — *un petit nombre
de signaux survivants, accompagnés d'un compte honnête du nombre de tests qu'il a
fallu pour les trouver*. Un compte honnête de zéro survivant reste un résultat.

## Voir aussi

[[phases/phase-06-controles-et-replication]] · [[research/mesfin-2026-falsification]] ·
[[concepts/comptage-des-tests]] · [[Failed Ideas/ledger]]
