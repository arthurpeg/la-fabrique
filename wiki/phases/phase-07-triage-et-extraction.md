---
type: phase
updated: 2026-09-19
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
**20 entrées** (les 4 de la section G, méthode, n'ont pas de colonne) —
13 `oui`, 5 `partiel`, 2 `non` — avec le motif de chacune. Elle a été
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

~~**Ce que « écarte ce qu'il doit écarter » veut dire en chiffres.**~~ **Fait le
2026-09-19** — `D15`, `corpus/score_triage.py`. Le seuil est écrit en
**effectifs**, pas en pourcentages : sur 13 `oui`, un seul item vaut 7,7 points
de rappel, donc « rappel ≥ 90 % » ne dit rien de plus que « au plus un manqué »
et le dit moins bien ([[Failed Ideas/ledger#F37]]).

| | Condition | Effectif |
|---|---|---|
| A | `oui` classés autrement | ≤ 1 sur 13 |
| B | `non` classés `oui` | 0 sur 2 |
| C | `partiel` en désaccord | ≤ 2 sur 5 |
| D | désaccords de deux crans | 0 |

Trois classes, **`partiel` non replié** : le replier effacerait la distinction
qui a écarté Mesfin et cadré Heston ([[Failed Ideas/ledger#F38]]). `L06`
s'applique mot pour mot — *un compte juste n'est pas un compte de choses justes*
— d'où la **matrice entière** et le motif exigé de chaque verdict.

**Et l'étalon a dû être compté avant d'être utilisé.** `ETAT.md` annonçait
24 entrées notées et six `partiel` ; la colonne en porte **20**, en
13 / 5 / 2. `AMORCE.md` se contredisait en plus lui-même — son § Verdict compte
12 / 5 / 3, l'écart portant sur l'entrée 9. `D15` tranche que **la colonne fait
foi** ([[Failed Ideas/ledger#F39]]), sans retirer l'entrée
([[Failed Ideas/ledger#F40]]), et le § Verdict a reçu une note datée.

**Le juge avant l'accusé, ici aussi.** `corpus/score_triage.py` rend
**10 vérifications** vertes — huit sorties de trieur fabriquées, deux mutations
d'`AMORCE.md` que le garde de l'étalon refuse — et le trieur n'existe pas encore.

**Ce que le trieur verra** est fixé : la ligne d'`AMORCE.md` privée de sa colonne
verdict, exactement ce que l'auteur humain avait en phase 01. Pas le PDF, qui le
rendrait mieux informé que son étalon ([[Failed Ideas/ledger#F41]]) — et, effet
de bord heureux, cette moitié de la porte se juge **sans un seul PDF de plus**.

**Le premier passage fait foi** ; tout passage ultérieur s'inscrit au § Journal
de `D15` avec ce qui a changé, et le verdict final cite le nombre de passages.

## Ce qui bloque l'autre moitié : l'acquisition

**3 PDF sur disque, 20 fiches demandées.** Des 20 entrées notées, 12 ont un lien
libre, 2 sont derrière un péage (16, 17) et **6 n'ont aucun lien** (6, 10, 14,
18, 19, 20 — la 14 étant en outre citée de mémoire et non vérifiée). Ce que
devient la porte si les 20 fiches ne sont pas atteignables depuis `AMORCE.md` —
élargir le corpus, ou requalifier la porte — se tranche **par écrit, et pas au
quinzième papier**.

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
