# D40 — Ce qu'une hypothèse du lot 09 contient, et qui l'écrit

> **Renumérotée le 2026-09-30 : `D33` → `D40`.** Deux décisions portaient le numéro
> `D33`, écrites le même jour sur deux lignes de travail parallèles. La ligne
> distante le garde (`D33` — la pertinence de la base), comme `D27` avait été
> gardé par la plus ancienne lors de la renumérotation `D27` → `D36`. Toute
> mention de « `D33` » à propos du **format d'une hypothèse** — dans les fichiers
> append-only (`wiki/log.md`, `wiki/Failed Ideas/ledger.md` § `F61`) et
> l'historique git — désigne celle-ci.

**Date :** 2026-09-29
**Phase :** 09
**État :** prise

## La question

`D25` `C2` exige que les 41 fiches du lot soient désignées et **leurs hypothèses
pré-enregistrées** avant la première mesure. `hypotheses/README.md` pose cinq
règles de fond ; **aucun document ne dit ce qu'un fichier d'hypothèse contient,
qui a le droit de l'écrire, ni comment on vérifie qu'il ne triche pas.**
`gate_09.py` se contente de constater qu'un fichier `H<NN>-*.md` existe.

## Les options

**1. Produire les 41 hypothèses sur le modèle de `H01`, sans format écrit.**
Écartée, et c'est l'option par défaut si on ne décide pas. `H01` à `H04` ont été
écrites à la main, une par une, dans des phases où elles étaient le sujet unique
de la session. Quarante et une écrites d'affilée sans garde dérivent : la
première est soignée, la trentième récite. Le dépôt a déjà refusé cette forme
d'argument pour les fiches (`D16`, « une fiche creuse passe les cinq
conditions ») et pour les signaux (`D23`, `S5`).

**2. Juger les hypothèses par relecture humaine.** Écartée pour la raison de
`F45`, mot pour mot : une condition qui ne tient qu'à la patience d'un relecteur
n'est pas une condition. Quarante et une hypothèses, c'est l'échelle exacte à
laquelle `F45` a été écartée pour les fiches.

**3. Faire écrire chaque hypothèse par une session isolée**, sur le modèle de
`D16` (extracteur) et `D23` (codeur). Écartée **sur le motif**, pas sur le
principe. L'isolement de `D16` et `D23` protège d'une fuite précise : le verdict
du juge, ou la fiche de référence. Ici il n'y a **rien à fuir** — aucun IC
n'existe pour aucune fiche du lot (vérifié : l'intersection entre les
`signal_id` du registre et les 41 fiches est **vide**, `D28`). L'isolement
coûterait 41 sessions pour fermer un canal qui n'est pas ouvert.

**4. Écrire le format, écrire son juge, puis produire les 41.** Retenue.

## Le choix

**Une hypothèse du lot 09 est un fichier `hypotheses/H<NN>-<slug>.md` portant un
en-tête à champs fixes et six sections obligatoires, dont une table qui rattache
chaque chiffre du papier à l'entrée `reported_results` de la fiche qui le porte.
`hypotheses/score_hypothese.py` la juge mécaniquement, et il est écrit avant la
première hypothèse.**

L'en-tête porte, un champ par ligne :

| Champ | Contenu |
|---|---|
| `Écrite le` | la date, `AAAA-MM-JJ` |
| `fiche` | le `fiche_id`, qui doit exister sur disque |
| `signal` | le `signal_id` — **égal au `fiche_id`**, convention constatée sur `baltussen-2021-hedging-demand-intraday-momentum` |
| `signe attendu` | `+1` ou `−1`, jamais autre chose (`D25` `C1`, `D07`) |
| `tranche` | `pool`, `asof` 2023-12-29 20:00 UTC — la valeur exacte qu'exige `D29` |
| `écrite par` | qui, et **ce qu'il avait vu** |
| `Statut` | `pré-enregistrée, non mesurée` tant que le registre est muet |

Les six sections : **Ce qui est affirmé** · **Le domaine** · **Ce qui est
attendu, en chiffres** · **Ce que le papier annonce, et d'où ça vient** · **Ce
qui la contredirait** · **Ce qui n'est pas affirmé ici**.

## Pourquoi

**Le signe d'abord, et il est vérifié des deux côtés.** `gate_09` lit le signe
dans `module.EXPECTED_SIGN` du signal, pas dans l'hypothèse — et **rien ne
vérifiait que les deux concordent**. Un codeur qui oriente son score à l'envers
rendrait un `p` unilatéral calculé sur un signe que personne n'avait
pré-enregistré, et la porte le laisserait passer. `score_hypothese.py` compare
les deux dès que le module existe. C'est le seul trou de protocole que cette
décision **ferme** plutôt que documente.

**Les chiffres du papier se rattachent, ils ne se recopient pas.** La table de la
quatrième section nomme des entrées de `reported_results` et le juge relit leur
`value` dans la fiche. C'est `F2` et `S5` transposés à l'hypothèse : *un chiffre
du papier absent de la fiche est un chiffre inventé*. Une hypothèse qui n'invoque
aucun chiffre du papier écrit `aucun` et dit pourquoi — un silence ne passe pas
pour une absence (`L05`).

**La falsifiabilité est comptée, pas promise.** `## Ce qui la contredirait` doit
porter **au moins deux clauses et au moins un nombre**. Le seuil est bas exprès :
il n'attrape pas une hypothèse molle bien rédigée, il attrape la section vide et
la clause purement qualitative. Ce que `D16` dit de son propre juge s'applique
ici mot pour mot — il ne sait pas dire qu'une hypothèse est *creuse*.

**Ce que ça sacrifie.** Le juge vérifie la **forme et la traçabilité**, jamais la
pertinence. Une hypothèse fidèle à sa fiche, correctement signée, falsifiable sur
le papier et **sans intérêt** passe les conditions. La pertinence n'aura de
dénominateur qu'au verdict de la porte 09 lui-même, et c'est déjà ce que `D16`
avait accepté pour l'extraction.

**Qui écrit, et la contamination est déclarée, pas éliminée.** Les 41 hypothèses
sont écrites par une session qui a lu `ETAT.md`, le wiki et les fiches — donc qui
sait que `H01`, `H02` et `H03` sont **toutes les trois sans résultat**, et que
`wiki/hot.md` annonce le corpus implémentable « attendu mort ». Ce biais-là est
réel et va dans un sens nommable : il pousse à écrire des affirmations
prudentes, que rien ne pourrait contredire. C'est exactement ce que la quatrième
règle de `hypotheses/README.md` interdit, et c'est pourquoi la section
« Ce qui la contredirait » est comptée par le juge. Même régime que `D15`
§ Journal pour le trieur et que `F16` pour le périmètre de la porte 04 : on
déclare ce qu'on ne peut pas rendre impossible.

## Ce que ça verrouille

- **`hypotheses/score_hypothese.py` juge les 41 et leur couverture du lot** :
  une fiche du lot sans hypothèse, ou une hypothèse dont la fiche n'est pas au
  lot, est un refus. Le lot reste clos (`D25` `C2`) — cette décision ne lui
  ajoute ni ne lui retire une fiche.
- **`ref` et `signal_id` entrent dans `hypotheses/LOT-09.json`** par
  `score_hypothese.py --lier`, qui les **dérive des fichiers d'hypothèse** et
  refuse de toucher à quoi que ce soit d'autre. C'est `F54` qui impose ce sens :
  un champ écrit à la main dans un fichier qu'un script réécrit est un champ
  détruit en silence — `corpus/lot_phase09.py --ecrire` ne connaît que
  `fiche_id`, `verdict` et `motif`, et **le relancer effacerait le lien**. La
  source de vérité est le fichier d'hypothèse ; le lot n'en porte que le reflet,
  reconstructible à tout instant.
- **Le signe est figé par l'hypothèse**, et le signal doit s'y conformer. Un
  codeur qui rend l'autre signe ne « corrige » pas l'hypothèse : il échoue.
- **En changer le format après la première mesure ne périme rien** — ces fichiers
  ne sont pas dans `harness/` et ne produisent aucun IC. Mais **réécrire une
  hypothèse** en périme une : elle meurt et donne lieu à une nouvelle, qui cite
  la précédente (`hypotheses/README.md`).

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Deux décisions portent le numéro `D27`** — `DECISION-27-l-instant-de-troncature.md` et `DECISION-27-le-lot-de-la-phase-09.md`. `gate_09.DECISIONS_ADMISES` admet `"D27"` et `LOT-09.json` le nomme : le lot s'autorise d'un numéro qui désigne deux textes. Non tranché ici — renuméroter touche `ETAT.md`, `wiki/log.md` (append-only) et le lot figé | avant la première mesure du lot |
| **`baltussen-2021-hedging-demand-intraday-momentum` a son signal AVANT son hypothèse** — produit le 2026-09-23 pour franchir la porte 08. Son `EXPECTED_SIGN` est donc lu, pas dicté ; le juge vérifiera la concordance au lieu de l'imposer. Aucun IC n'a été calculé dessus, donc rien n'est vu d'un résultat | constaté, sans échéance |
| **Le juge ne sait pas dire qu'une hypothèse est creuse** — même limite que `D16` pour les fiches | au verdict de la porte 09 |
| **Une fiche du lot peut se révéler inécrivable en signal** au moment de la coder — `D27` § Ce qui reste ouvert l'annonçait (« un faux inclus coûte un signal qu'on découvre inécrivable »). L'hypothèse est écrite quand même : c'est elle qui rend le refus visible plutôt que silencieux | à la première |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Note |
|---|---|---|
| — | 2026-09-29 | format écrit, juge écrit, aucune hypothèse produite encore. `python hypotheses/score_hypothese.py --check` : **28 vérifications, 0 échec** — chacune des sept conditions vue **refuser** le cas qu'elle vise, sur des fichiers fabriqués, le lot et les fiches réelles n'étant jamais lus |
| 1 | 2026-09-29 | **DIX HYPOTHÈSES ÉCRITES, `H05` À `H14`, ET TRENTE ET UNE QUI NE POUVAIENT PAS L'ÊTRE.** Les dix passent les sept conditions et la bijection est refusée pour les 31 autres, ce qui est le comportement voulu : la porte 09 **nomme** les fiches non couvertes au lieu de les oublier. Le recensement des 31, fiche par fiche avec sa raison, est dans `hypotheses/NON-ECRITES-09.md` ; il est inscrit au ledger sous **`F61`**. Trois écrans, dont un **mécanique** : `E1` 20 fiches ne prédisent aucun rendement (7 l'écrivent elles-mêmes), `E2` 9 ont un horizon hors fenêtre — et ce n'est pas une opinion, `harness/metric.py` groupe le rendement futur par *(séance, fenêtre)* avant de décaler, donc un horizon franchissant une séance ne rend **aucune** observation —, `E3` 2 exigent une donnée absente (`RSV` de Boyarchenko : le sens des transactions) ou une constante jamais chiffrée (le « strong trend » de Basdekidou). **CE QUE ÇA A APPRIS SUR LE FORMAT, et qui a corrigé deux fichiers déjà écrits** : `H10` et `H11` disaient d'abord « prédit la même fenêtre à la séance suivante », ce que le harnais ne sait pas mesurer. Elles sont reformulées — **le retard vit dans le score, jamais dans l'horizon** — et cette phrase est la seule façon dont un motif de saisonnalité intra-journalière est mesurable ici. **CE QUI RESTE ENTRE LES MAINS DE L'OPÉRATEUR** : le lot est **clos** (`D25` `C2`) et une session ne le rétrécit pas seule. Les trois issues possibles sont chiffrées dans `F61`. **UNE OBSERVATION SUR LES DIX**, écrite avant toute mesure : cinq d'entre elles (`H05`, `H06`, `H09`, `H10`, `H12`) sont des variantes du même motif, déjà mesuré absent ici par `H01` (`t` final −1,56) et `H03` (`F33`, `p` = 0,25). Leurs signaux seront corrélés, et c'est exactement ce que la matrice de corrélation de `D25` doit montrer avant `BH` |
