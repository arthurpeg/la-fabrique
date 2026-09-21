---
type: phase
updated: 2026-09-21
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

**L'entrée du trieur est fabriquée et auditée** : `corpus/make_triage_input.py`
produit `corpus/triage_input.json` — 20 lignes, 3 à 5 champs selon la section,
**titres de section non repris** (le titre E dit « la famille que mes données
ferment », c'est le verdict lui-même). `corpus/TRIAGE.md` pose le protocole.

**Et la mise en œuvre a trouvé une condition que `D15` ne portait pas** : une
session qui a **lu la colonne** ne peut pas être le trieur — elle réciterait, et
sa matrice serait parfaite pour la pire des raisons. Le piège est structurel : la
séquence de démarrage de `CLAUDE.md` mène toute session à l'étalon, donc **une
session arrive contaminée par défaut**. Celle du 2026-09-19 s'est disqualifiée
elle-même ([[Failed Ideas/ledger#F42]]). Ce n'est pas une impossibilité par
construction — `F13`, `F15`, `F16`, `F25` ont déjà refusé la vigilance déguisée
en architecture — donc la règle est **écrite**, et le § Journal de `D15` note pour
chaque passage qui a trié et ce qu'il avait vu.

**Le premier passage fait foi** ; tout passage ultérieur s'inscrit au § Journal
de `D15` avec ce qui a changé, et le verdict final cite le nombre de passages.

**Il manque donc un trieur non contaminé.** Le reste est prêt : entrée auditée,
juge vert sur 10 vérifications, protocole écrit.

## Le passage 1 — 2026-09-20 : la moitié triage tient, à la limite exacte

Le trieur a été un **agent séparé**, lancé depuis une session contaminée avec
interdiction de lecture explicite, ne recevant que `corpus/triage_input.json`
plus la règle et les contraintes recopiées dans sa consigne. Le passage est
inscrit au § Journal de `D15` — la source fait foi, cette page ne fait que la
refléter — et ses verdicts sont archivés dans `corpus/triage_passage_01.json`.

**Les quatre conditions tiennent : A/B/C/D = 1/0/2/0.** Mais `A` et `C` sont **à
leur maximum exact** (1 sur 1, 2 sur 2) : un désaccord de plus sur un `oui` ou
sur un `partiel`, et rien ne passait. La porte le citera tel quel, avec le numéro
du passage.

Trois désaccords sur 20 (entrées 3, 17, 20), **aucun ne désignant une erreur de
l'étalon**, qui n'a pas été touché. Le plus instructif est l'entrée 3 (Heston) :
le trieur la classe `partiel` parce que le test d'origine est transversal et ne
se transpose qu'en série temporelle par instrument — c'est **vrai**, `H03` l'a
fait — mais la règle réserve `partiel` à une **donnée** manquante, pas à un
travail de traduction. Confusion entre difficulté de transposition et absence de
donnée.

**Un défaut du protocole a été trouvé en le lançant.** `corpus/TRIAGE.md` § Ce
que le trieur rend illustre le format de sortie avec **deux entrées réelles et
leur verdict juste** — entrée 1 `oui`, entrée 18 `non` — et l'entrée 18 est l'un
des **deux seuls `non`**, donc la moitié de la condition B. Quiconque reçoit ce
fichier reçoit deux réponses sur vingt. Le passage 1 ne l'a pas reçu et a classé
l'entrée 18 `non` sans l'indice. `TRIAGE.md` **n'a pas été corrigé pendant le
passage** — corriger le protocole dans le geste qui l'applique est ce que « le
premier passage fait foi » interdit — et la correction **est due avant tout
passage 2**.

Le passage n'a coûté **aucun test** : `counted_tests()` reste à 56.

## La moitié extraction a son juge — `D16`, le 2026-09-20

Écrit **avant que l'extracteur existe**. `corpus/score_extraction.py`,
**32 vérifications**, vert — 21 à l'écriture de `D16`, portées à 32 par le
correctif de `D17`. La source fait foi :
`decisions/DECISION-16-seuil-de-l-extraction.md` et son § Complément.

Il ne juge **pas** la ressemblance aux trois fiches écrites à la main — trois
items ne portent aucun seuil, et un seuil en pourcentage sur trois items est
[[Failed Ideas/ledger#F37]] à nouveau. Il juge la **fidélité à la source** :
cinq conditions à tolérance zéro, dont `F2`, qui exige que chaque `quoted` se
retrouve **mot pour mot** dans le texte du papier.

**Ce que `F2` ferme.** `D14` vérifiait qu'une `value` se retrouve dans sa
`quoted` ; rien ne vérifiait que la `quoted` existe. Un extracteur qui fabrique
**la citation et le chiffre qu'elle contient** passait `D14` sans une faute —
exactement la valeur plausible inventée que `CLAUDE.md` § Les interdits nomme.

**Ce qu'il ne sait pas faire** : dire qu'une fiche est *creuse*. Le diagnostic
l'imprime, aucune condition ne le porte. Écrit dans `D16` § Pourquoi, et renvoyé
à la phase 09, premier dénominateur réel.

Trois options écartées et consignées : [[Failed Ideas/ledger#F43]] (apparier à
l'étalon), [[Failed Ideas/ledger#F44]] (ressemblance de texte),
[[Failed Ideas/ledger#F45]] (relecture humaine comme condition de porte).

## Ce que `F2` a trouvé en rencontrant trois vrais papiers — 2026-09-20

Les trois PDF de référence ont été récupérés et le juge lancé sur eux. **`F2`
casse sur les trois**, pour trois raisons dont une seule est une faute. La
source fait foi : `D16` § Complément du 2026-09-20.

| Papier | Ce qui cloche | Qui a tort |
|---|---|---|
| Andersen & Bollerslev (1997) | c'est un **scan** : le texte extrait dit « the **fight** part » pour « right part » | **le texte** |
| Mesfin (2026), `walk_forward_folds` | la citation vient d'un **tableau**, rendu en cellules | personne |
| Mesfin (2026), `acceptance_criteria` | `quoted` est une **paraphrase**, pas une citation | **la fiche** |

Le troisième est exactement ce que `F2` est fait pour attraper — et il l'a
attrapé dans une fiche **écrite à la main** par une session qui avait lu le
papier. Le mécanisme est juste ; c'est sa prémisse qui était trop simple.

D'où la **réparation déclarée** : `quoted_source` (mot pour mot dans le texte) et
`quoted_repair` dans une liste close — `ocr`, `math_notation`, `table`. Le geste
de `D14` avec `spelled_out`, repris : on **nomme** la réparation humaine au lieu
de la cacher. Ce qui ne bouge pas : il faut toujours une chaîne présente à la
lettre, donc la paraphrase reste une faute.

## La porte est requalifiée — `D17`, le 2026-09-20

Elle ne demande plus **20 fiches**. Le 20 venait du nombre d'entrées notées
d'`AMORCE.md`, pas d'une exigence : il ne testait rien. Elle demande un
**extracteur jugé sur tout le corpus atteignable**, avec le recensement écrit de
ce qui ne l'était pas — `G1` à `G4`, dont **`G3` : zéro retouche manuelle**, plus
dure que le chiffre qu'elle remplace.

Écartées et consignées : [[Failed Ideas/ledger#F46]] (tenir les 20),
[[Failed Ideas/ledger#F47]] (élargir le corpus — **rouverte** si l'atteignable
tombe sous 5 papiers, seuil écrit avant le recensement).

## L'acquisition est recensée — `G4`, le 2026-09-21

> [!note] **À jour au 2026-09-21 : les trois PDF de référence sont sur ce poste,
> et `F4` passe sur les trois fiches.** Ils ont été récupérés le 2026-09-20 par la
> session de `D17`. Cette page a porté successivement les deux erreurs inverses :
> « 3 PDF sur disque » écrit depuis un autre poste, puis « aucun PDF » gardé
> après leur récupération le jour même. `corpus/pdf/` est dans `.gitignore`,
> **son état n'est donc pas un fait du dépôt** : il ne se lit pas ici, il se
> vérifie en lançant `corpus/score_extraction.py`. La source fait foi :
> `ETAT.md` § Les trois PDF de référence sont sur ce poste.

**19 atteignables sur 20**, dont 18 en PDF. La source fait foi :
`corpus/acquisition.json`, gardé par `corpus/check_acquisition.py`
(11 vérifications) et expliqué par `corpus/ACQUISITION.md`.

| | Effectif |
|---|---|
| atteignables | **19 / 20** — 18 PDF, 1 HTML |
| inatteignables | **1** — entrée 6, `refus_robot` |
| PDF **sur le disque** | **18 / 18** depuis le 2026-09-21 — `corpus/fetch_pdfs.py --verify` le vérifie, cette page ne le prouve pas |

**`D17` avait prévu 6 à 14 « selon ce que SSRN consent », et elle se trompait
deux fois.** SSRN n'a rien consenti — contrôle anti-robot, vérifié en client
automatique (`403`) et dans un vrai navigateur, **non contourné**. Et le compte
est plus haut quand même, parce que la prévision prenait **le lien qu'`AMORCE.md`
porte pour le papier lui-même**. S'en tenir à ces liens rendait **5 sur 20** ;
chercher le papier en rend 19. L'entrée 3 le montrait déjà : `AMORCE.md` n'en
donne qu'un lien SSRN, et son PDF vient d'arXiv.

Le seuil de `D17` — *rouvrir l'élargissement du corpus sous 5 atteignables* — est
**largement écarté**, et il avait été écrit avant le recensement.

**Deux alertes, ouvertes et non tranchées.** L'entrée 9 est libre mais en HTML :
atteignable à la lettre de `D17`, infichable pour `F4` qui exige un `source.pdf`.
Et la citation de l'entrée 16 paraît fausse dans `AMORCE.md` — « Kurov,
Sancetta, Strasser & Wolfe » quand le papier que son propre lien désigne est de
Kurov, Wolfe & Gilbert. `AMORCE.md` **n'a pas été touché** : c'est l'étalon du
triage (`D15`).

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
