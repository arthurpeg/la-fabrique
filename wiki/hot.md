---
type: hub
updated: 2026-09-21
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-21.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 07 — triage et extraction sur 20 papiers connus |
| **Dernière porte franchie** | **06**, le 2026-09-18 — les deux clauses. Clause 1 (dégénérescence) : `gate_06_controls.py`, 25 vérifications. Clause 2 (réplication) : `scripts/measure_h04.py`, 19 vérifications, `H04` pré-enregistrée |
| **Décision la plus récente** | `decisions/DECISION-17-ce-que-la-porte-07-demande.md` — la porte 07 ne demande plus **20 fiches** : elle demande un **extracteur jugé sur tout le corpus |
| **Tests au registre** | 135 |
| **Idées abandonnées recensées** | 47 |
| **Entrées au journal** | 30 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action — reflet de `ETAT.md`

**La phase 07 est ouverte** : construire le **triage** et l'**extraction**, et les
juger contre un verdict humain de référence.

### Ce qui existe déjà, et qui est le banc d'essai — pas le produit

Trois fiches ont été écrites **à la main** le 2026-09-18, parce que la clause 2
exigeait de lire les papiers qu'elle visait :

| Fiche | Rôle |
|---|---|
| `corpus/fiches/mesfin-2026-ohlcv-falsification.json` | résultat négatif, calibrage d'attente |
| `corpus/fiches/heston-2010-intraday-periodicity.json` | cible écartée, motif absent (`H03`) |
| `corpus/fiches/andersen-bollerslev-1997-periodicity.json` | cible retenue, porte franchie (`H04`) |

Elles sont à la phase 07 ce que `H01` et `H02` étaient aux portes 05 et 06 : un
**sujet connu** pour juger l'automate. Écrire l'extracteur d'abord et vérifier
ensuite inverserait l'ordre de construction. Voir `D06`, qui a tranché la même
question pour les signaux.

### Ce que la porte 07 demande

*« 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict
humain de référence. »* Deux choses distinctes, et la seconde est la plus dure :

1. **L'extraction** — d'un PDF à une fiche structurée. Les trois fiches manuelles
   donnent le schéma et le niveau de détail attendu ; il n'est écrit nulle part
   ailleurs, et il devrait l'être.
2. **Le triage** — décider qu'un papier est implémentable sur neuf futures
   intraday. `corpus/AMORCE.md` porte déjà une colonne « implémentable »
   renseignée à la main sur 20 entrées : **c'est le verdict humain de référence**,
   et il existe déjà. Il a été écrit en phase 01, avant tout ce qui suit, donc
   sans connaître les résultats — ce qui en fait un étalon honnête.

### Le premier maillon est posé — `D14`, le 2026-09-18

Le **schéma de fiche** est écrit, et il n'est pas tiré des trois fiches
manuelles : elles divergeaient, et aucune n'avait de champ `horizon`. Il reprend
les **six champs que `CLAUDE.md` § Le vocabulaire nomme depuis le premier jour**,
plus la `source` et la `transposability` que la pratique a rendues
indispensables. `corpus/SCHEMA.md` le pose, `corpus/validate_fiches.py` le garde,
`corpus/check_fiches_guard.py` montre ce garde **refuser 11 fautes**, chacune
pour la raison prévue.

**`D09` est étendu aux fiches.** Un résultat recopié d'un papier est une valeur
externe : il porte sa citation, et `value_in_quote` — le garde même du catalogue
— vérifie que la valeur s'y retrouve. Deux échappatoires **nommées** plutôt que
cachées : `derived` pour un nombre que nous avons calculé, `spelled_out` pour un
nombre que le papier écrit en toutes lettres. Ce second cas n'était pas prévu :
le garde l'a trouvé sur Mesfin, qui écrit « *Eleven signal families fail* ».

Les trois fiches ont été **réécrites** au schéma. C'était le test du schéma
autant que des fiches : s'il n'avait pas su exprimer ce qu'elles disaient, c'est
lui qui aurait été faux.

### Le seuil du triage est écrit, et le juge existe — `D15`, le 2026-09-19

L'étalon a d'abord dû être **compté**, et il ne l'avait pas été : `ETAT.md`
annonçait 24 entrées notées et six `partiel`. La colonne « implémentable »
d'`AMORCE.md` en porte **20** — entrées 1 à 20, sections A à F ; les quatre de la
section G (méthode) n'ont pas cette colonne — en **13 `oui` / 5 `partiel` /
2 `non`**. Et `AMORCE.md` se contredisait lui-même : son § Verdict compte
12 / 5 / 3, l'écart portant sur l'entrée 9. `D15` tranche que **la colonne fait
foi**, et le § Verdict a reçu une note datée — le texte d'origine conservé, comme
pour l'entrée 7.

**Le seuil, écrit avant toute mesure**, en effectifs et non en pourcentages : sur
13 `oui`, un seul item vaut 7,7 points de rappel, et un seuil en pourcentage
n'est qu'un effectif mal déguisé.

| | Condition | Effectif |
|---|---|---|
| A | `oui` classés autrement | ≤ 1 sur 13 |
| B | `non` classés `oui` | 0 sur 2 |
| C | `partiel` en désaccord | ≤ 2 sur 5 |
| D | désaccords de deux crans | 0 |

**Le juge est écrit avant l'accusé, ici aussi** : `corpus/score_triage.py`,
**10 vérifications**, vert — huit sorties de trieur fabriquées qui rendent
chacune le verdict que `D15` écrit, et deux mutations d'`AMORCE.md` que le garde
de l'étalon refuse. Le trieur, lui, n'existe pas encore.

### L'entrée du trieur est fabriquée et auditée — le 2026-09-19

`corpus/make_triage_input.py` produit **`corpus/triage_input.json`** : les
20 lignes d'`AMORCE.md` privées de leur colonne verdict, 3 à 5 champs selon la
section, et **sans les titres de section** — le titre E dit « la famille que mes
données ferment », ce qui est le verdict lui-même et rendrait la condition B
satisfaite d'avance. `corpus/TRIAGE.md` pose le protocole complet.

**Conséquence heureuse, et il faut la voir** : cette moitié de la porte se juge
**sans un seul PDF de plus**. Elle ne dépend pas du goulot d'acquisition qui
bloque l'autre moitié.

### La moitié triage est tenue — passage 1, le 2026-09-20

**Un trieur non contaminé a trié, une fois, et les quatre conditions de `D15`
tiennent.** Le passage est inscrit au § Journal de `D15` avec ce qu'il avait vu ;
ses 20 verdicts sont dans `corpus/triage_passage_01.json`. Il n'a coûté **aucun
test** : `counted_tests()` reste à 56, le registre à 135 lignes.

| | Condition | Mesuré | Plafond |
|---|---|---|---|
| A | `oui` de l'étalon classés autrement | **1** | ≤ 1 sur 13 |
| B | `non` de l'étalon classés `oui` | **0** | 0 sur 2 |
| C | `partiel` de l'étalon en désaccord | **2** | ≤ 2 sur 5 |
| D | désaccords de deux crans | **0** | 0 |

**Ce qu'il faut lire dans ces quatre chiffres, et ne pas arrondir** : `A` et `C`
sont **à leur maximum exact**. Un désaccord de plus sur un `oui` ou sur un
`partiel`, et rien ne passait. Ce n'est pas une marge, c'est une limite atteinte,
et le verdict de la porte 07 devra le citer tel quel avec le **numéro du
passage** — comme la phase 15 citera `counted_tests()`.

Les trois désaccords (entrées 3, 17, 20) sont examinés un par un au § Journal de
`D15`, avec le motif que le trieur a donné. **Aucun ne désigne une erreur de
l'étalon**, et l'étalon n'a pas été touché. Le plus instructif est l'entrée 3
(Heston) : le trieur la classe `partiel` parce que le test d'origine est
transversal et ne se transpose qu'en série temporelle — c'est **factuellement
vrai**, `H03` l'a fait — mais la règle réserve `partiel` à une **donnée**
manquante, pas à un travail de traduction. Le trieur a confondu difficulté de
transposition et absence de donnée.

**Comment le passage a été conduit, et ce qu'il a fallu contourner.** La session
qui l'a lancé était contaminée (elle avait lu cette section) ; le trieur était un
agent séparé, avec interdiction de lecture explicite, recevant
`corpus/triage_input.json` et rien d'autre du corpus.

Et un **défaut du protocole a été trouvé là** : `corpus/TRIAGE.md` § Ce que le
trieur rend illustre le format avec **deux entrées réelles et leur verdict
juste** — entrée 1 `oui`, entrée 18 `non` — or l'entrée 18 est l'un des **deux
seuls `non`**, donc la moitié de la condition B. Le passage 1 n'a pas reçu ce
fichier : la règle et les contraintes lui ont été recopiées, avec un exemple de
format neutre. Il a classé l'entrée 18 `non` sans l'indice. **`TRIAGE.md` reste à
corriger avant tout passage 2** — il ne l'a pas été pendant le passage, corriger
le protocole dans le geste qui l'applique étant précisément ce que « le premier
passage fait foi » interdit.

### La moitié extraction a son juge — `D16`, le 2026-09-20

**Écrit avant que l'extracteur existe**, comme `D15` l'a été avant le trieur.
`corpus/score_extraction.py`, **21 vérifications**, vert.

Ce qu'il juge n'est **pas** la ressemblance à une fiche écrite à la main. Il n'y
en a que trois, et un seuil sur trois items ne distingue pas un extracteur
correct d'un extracteur chanceux — c'est `F37` à nouveau, l'effectif mal
déguisé. Il juge la **fidélité à la source**, qui se vérifie sans étalon :

| | Condition | Tolérance |
|---|---|---|
| F1 | la fiche passe `validate_fiches.py` | 0 |
| F2 | chaque `quoted` est **mot pour mot** dans le texte du papier | 0 |
| F3 | chaque `value` numérique est dans sa citation | 0 |
| F4 | le PDF désigné **existe**, `source_url` est une URL | 0 |
| F5 | aucune **contradiction** factuelle avec la référence, s'il en existe une | 0 |

**Ce que `F2` ferme, et qui était grand ouvert.** `D14` vérifiait qu'une `value`
se retrouve dans sa `quoted` ; rien ne vérifiait que la `quoted` existe. Un
extracteur qui fabrique **la citation et le chiffre qu'elle contient** passait
`D14` sans une faute — et c'est précisément la machine à produire des valeurs
plausibles inventées que l'interdit constitutionnel vise.

**Ce que ce juge ne sait pas faire, et c'est écrit dans `D16` § Pourquoi** : dire
qu'une fiche est *creuse*. Un extracteur qui recopierait fidèlement trois
citations insignifiantes passerait les cinq conditions. Le diagnostic imprime de
quoi le voir — les résultats de la référence laissés de côté — mais ne
conditionne rien. La pertinence n'aura de dénominateur qu'en phase 09.

### Les trois PDF de référence sont sur ce poste — et ce paragraphe s'est périmé deux fois

**État au 2026-09-21, vérifié par le juge lui-même** (`check_f4` de
`corpus/score_extraction.py`, lancé sur les trois fiches) : `corpus/pdf/`
contient les trois PDF — Mesfin (`2605.04004`), Heston (`1005.3535`),
Andersen & Bollerslev — récupérés le 2026-09-20 par la session de `D17`, qui
l'inscrit à son § Le recensement. **`F4` passe sur les trois.**

**Ce que ce paragraphe disait avant, et pourquoi il reste écrit.** Le
2026-09-18, `ETAT.md` annonçait « 3 PDF sur disque » : vrai sur le poste où ils
avaient été récupérés, faux ici, `corpus/pdf/` étant dans `.gitignore`. Le
2026-09-20, `D16` a lancé son juge et **`F4` a cassé sur les trois fiches** — le
juge a trouvé le fait faux tout seul, ce qui est la bonne façon de l'apprendre.
La correction écrite ce jour-là a été rattrapée par la récupération des PDF
quelques heures plus tard, **dans la même journée** — et elle est restée fausse
dans l'autre sens jusqu'à aujourd'hui.

**La leçon n'est donc pas « il n'y avait pas de PDF ».** Elle est que l'état
d'un dossier ignoré par git **n'est pas un fait du dépôt** : il est vrai d'un
poste et d'une heure, et ce fichier ne devrait pas l'affirmer sans le vérifier.
Le seul énoncé qui ne se périme pas est celui du juge, qui répond à l'instant
où on le lance. Même péremption que la note « sur cette machine » corrigée le
2026-09-17, et deux fois plutôt qu'une.

### Prochaine action : deux choses, et la seconde demande une décision

1. ~~Récupérer les trois PDF de référence.~~ **Fait le 2026-09-20** — Mesfin
   (arXiv), Heston (arXiv 1005.3535), Andersen & Bollerslev (lien direct) sont
   dans `corpus/pdf/`, et `F4` passe sur les trois fiches.
2. ~~Trancher par écrit ce que la porte 07 demande.~~ **Fait le 2026-09-20 :
   `D17`.** La porte ne demande plus 20 fiches mais un extracteur jugé sur tout
   le corpus atteignable, `G1`–`G4`.

### Donc, dans l'ordre, ce qui vient maintenant

1. **Le recensement des atteignables** — `G4` l'exige, et sans lui `G1` ne veut
   rien dire puisqu'on choisirait après coup ce qui était à portée. 14 entrées
   sur 20 portent un lien ; SSRN et ScienceDirect n'ont pas été essayés. C'est
   peu de travail et ça décide de la taille de tout le reste.
2. **Réparer les trois fiches de référence** — deux `quoted_source` à déclarer,
   et **une citation fausse** dans Mesfin (`acceptance_criteria`) à corriger par
   note datée. `D16` § Complément dit quoi faire et pourquoi ce n'est pas fait.
3. **Apprendre `quoted_source` à `validate_fiches.py`**, faute de quoi `F1` reste
   plus laxiste que `F3` sur une entrée réparée.
4. **Écrire l'extracteur** — et il devra être **non contaminé** : une session qui
   a lu la fiche de référence d'un papier ne peut pas l'extraire, elle
   recopierait. Même piège que le trieur, même parade.

### Ce qui reste ouvert par ailleurs

- **l'acquisition** : 3 PDF sur ce poste, les trois de référence et aucun autre ;
  14 entrées sur 20 portant un lien,
  2 derrière un péage (16, 17), 6 sans aucun lien (6, 10, 14, 18, 19, 20 — la 14
  étant en outre citée de mémoire, non vérifiée). Voir la prochaine action ;
- **deux fuites du même genre que celle de `TRIAGE.md`**, nommées par `D16` et
  non encore corrigées : `corpus/SCHEMA.md` illustre ses exemples avec le
  **contenu réel** de la fiche Andersen & Bollerslev, donc un extracteur qui lit
  le schéma reçoit une réponse sur trois ; et **où vit le texte source** dont
  `F2` vérifie les citations n'est pas tranché ;
- les **multiplicateurs** CME (`cmegroup.com` injoignable depuis ce poste le
  2026-09-18) et la réponse de **Lucid** ; requis pour toute lecture **nette** et
  pour la phase 10 ;
- une déclaration écrite de `slippage_bp`, pessimiste, comme `D04` l'exige ;
- **le corpus implémentable est attendu mort.** Mesfin est transportable (`L14`),
  et `H01`, `H02`, `H03` n'ont rien trouvé. La phase 07 doit être construite en
  sachant que son produit a de fortes chances d'être une liste de signaux nuls —
  ce qui reste le but : *un petit nombre de signaux survivants, accompagnés d'un
  compte honnête du nombre de tests qu'il a fallu pour les trouver* ;
- **la ventilation par cellule de `H03`** n'a pas été inscrite (défaut de
  `scripts/measure_h03.py`) ; la combler coûterait 52 lignes et ne pourrait
  qu'affaiblir un motif déjà absent. Noté plutôt que payé ;
- **un piège, trouvé le 2026-09-19 et non désamorcé : `ruff format .` à la racine
  réécrirait 4 des 7 fichiers de `harness/`.** L'empreinte porte sur le contenu
  (`harness/registry.py`, `code_hash`), donc un formatage machinal **périme les
  56 tests comptés** et tout ce que `D05` en déduit. `ruff check harness/` passe ;
  c'est le **formateur** qui diverge. Les 11 erreurs de lint réelles sont toutes
  dans `scripts/` et se corrigent sans risque — **en excluant `harness/`
  explicitement**. Ne jamais lancer `ruff format` sans chemin.

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-21 | `audit` | Péremption PDF corrigée dans `ETAT.md` et dans la page de phase 07 : les trois PDF de référence SONT sur ce poste depuis le 2026-09-20 (récupérés par la session de `D17`, qui l'inscrit à son § Le recensement), alors que `ETAT.md` affirmait encore « aucun PDF sur ce poste » en quatre endroits (cellule de la phase 07, section dédiée, prochaine action n° 1, point d'acquisition) | VÉRIFIÉ PAR LE JUGE LUI-MÊME et non affirmé : `check_f4` de `corpus/score_extraction.py` lancé sur les trois fiches, **F4 OK sur les trois**. LA PÉREMPTION A JOUÉ DANS LES DEUX SENS EN TROIS JOURS — « 3 PDF sur disque » écrit le 2026-09-18 depuis un autre poste, corrigé en « aucun PDF » le 2026-09-20 par `D16` dont le juge avait trouvé le fait faux tout seul, puis cette correction rattrapée QUELQUES HEURES PLUS TARD par la récupération des PDF, et restée fausse dans l'autre sens jusqu'à aujourd'hui. La leçon écrite dans `ETAT.md` n'est donc pas « il n'y avait pas de PDF » mais : l'état d'un dossier IGNORÉ PAR GIT n'est pas un fait du dépôt, il est vrai d'un poste et d'une heure, et le seul énoncé qui ne se périme pas est celui du juge lancé à l'instant. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e). DEUX AUTRES PÉREMPTIONS VUES ET NON CORRIGÉES, hors du geste demandé : `ETAT.md` annonce encore « 21 vérifications » pour `score_extraction.py` là où `D17` le porte à 32, et le compte d'entrées à lien libre vaut 14 dans `ETAT.md` contre 12 dans la page de phase 07 |
| 2026-09-20 | `decision` | D17 ecrite — LA PORTE 07 REQUALIFIEE, et D16 CORRIGEE par le reel. D17 : la porte ne demande plus « 20 fiches » — le 20 venait du nombre d'entrees d'AMORCE.md, pas d'une exigence — mais un EXTRACTEUR JUGE SUR TOUT LE CORPUS ATTEIGNABLE, avec le recensement ecrit de ce qui ne l'etait pas. G1 zero papier atteignable non fiche, G2 zero fiche cassant D16, G3 ZERO RETOUCHE MANUELLE, G4 zero inatteignable non recense. Options ecartees : tenir les 20 (F46), elargir le corpus (F47, rouverte si l'atteignable tombe sous 5). Les 3 PDF de reference recuperes (arXiv x2, lien direct), pypdf ajoute aux dependances | D16 A RENCONTRE TROIS VRAIS PAPIERS ET SA PREMISSE A CASSE : F2 supposait que « le texte du papier » est une chaine bien definie. Elle ne l'est pas. Andersen & Bollerslev 1997 est un SCAN — son texte extrait dit « fight part » pour « right part », « pa » pour rho, « ]rt,,,] » pour \|R\| : le texte a tort, la fiche a raison. Mesfin : un tableau rendu en prose (personne n'a tort), et UNE VRAIE PARAPHRASE APPELEE CITATION dans acceptance_criteria — « >= 30 trades » ne figure pas dans la phrase citee. F2 a donc attrape, des son premier contact avec le reel, un defaut d'une fiche ECRITE A LA MAIN par une session qui avait lu le papier. Correctif ecrit AVANT tout passage (journal vide) : la REPARATION DECLAREE — `quoted_source` (mot pour mot dans le texte) + `quoted_repair` dans une liste CLOSE (ocr, math_notation, table), sur le modele de spelled_out de D14 : on NOMME la reparation au lieu de la cacher. Ce qui ne change pas : il faut toujours UNE chaine presente a la lettre, donc la paraphrase reste une faute. F3 suit desormais la chaine qui fait foi, sans quoi la reparation serait l'endroit ou loger un chiffre absent du papier. DECOUVERTE AU PASSAGE : validate_fiches (D14) ignore quoted_source et verifie le chiffre contre `quoted` — sur une entree reparee, F3 est PLUS STRICT que F1. Note, non corrige : D14 n'est pas ma decision a amender en passant. Les 3 fiches de reference ne passent PAS F2 aujourd'hui et ne sont PAS reecrites en silence (L17) — deux reparations a declarer, une citation fausse a corriger par note datee. Juge : 21 -> 32 verifications, vert. counted_tests reste a 56, harnais intouche (9ac3e45e). F46, F47 |
| 2026-09-20 | `decision` | D16 écrite — LE SEUIL DE L'EXTRACTION, avant que l'extracteur existe. Une fiche produite est jugée sur sa FIDÉLITÉ À LA SOURCE et non sur sa ressemblance aux trois fiches écrites à la main : trois items ne portent aucun seuil (F43), et comparer la prose par ressemblance de texte mesurerait le style en croyant mesurer la justesse (F44). Cinq conditions à tolérance ZÉRO — F1 schéma de D14, F2 chaque `quoted` MOT POUR MOT dans le texte du papier, F3 chaque `value` dans sa citation, F4 le PDF désigné existe, F5 aucune CONTRADICTION factuelle avec la référence (l'absence n'en est pas une). corpus/score_extraction.py, et corpus/TRIAGE.md corrigé de sa fuite | CE QUE F2 FERME ÉTAIT GRAND OUVERT : D14 vérifiait qu'une `value` se retrouve dans sa `quoted`, rien ne vérifiait que la `quoted` EXISTE — un extracteur qui fabrique la citation ET le chiffre qu'elle contient passait D14 sans une faute, soit exactement la valeur plausible inventée que CLAUDE.md interdit. Juge vert sur 21 vérifications, dont une qui m'a corrigé : j'attendais F3 seule cassée sur une valeur absente de sa citation, F1 l'attrape aussi — le recouvrement est réel et c'est l'attente qui était fausse. LE JUGE A TROUVÉ UN FAIT FAUX DÈS SON PREMIER ESSAI SUR UNE VRAIE FICHE : F4 casse sur les TROIS fiches de référence, car corpus/pdf/ EST VIDE sur ce poste — le dossier est gitignoré et ETAT.md annonçait « 3 PDF sur disque » depuis le 2026-09-18, vrai sur l'autre poste seulement. Même péremption que la note « sur cette machine » du 2026-09-17. Corrigé dans ETAT.md et la page de phase. D16 nomme deux fuites du genre de L17 qu'elle NE corrige PAS : corpus/SCHEMA.md illustre ses exemples avec le contenu RÉEL de la fiche Andersen & Bollerslev (une réponse sur trois donnée à qui lit le schéma), et où vit le texte source de F2 n'est pas tranché. Ce que D16 assume et écrit : le juge ACCEPTE une fiche creuse — la fidélité est vérifiée, la PERTINENCE ne l'est pas, et elle n'aura de dénominateur qu'en phase 09. F43, F44, F45 ; aucun test dépensé, counted_tests reste à 56, harnais intouché |
| 2026-09-20 | `mesure` | PASSAGE 1 DU TRIEUR — la moitié triage de la porte 07 est tenue. Trieur = agent general-purpose séparé, lancé depuis une session contaminée, avec interdiction de lecture explicite ; il n'a reçu que corpus/triage_input.json plus la règle de classement et les contraintes de données recopiées dans sa consigne. Inscrit au § Journal de D15 avec ce qu'il avait vu ; verdicts archivés dans corpus/triage_passage_01.json | LES QUATRE CONDITIONS TIENNENT, A/B/C/D = 1/0/2/0 — mais A ET C SONT À LEUR MAXIMUM EXACT (1 sur 1, 2 sur 2) : un désaccord de plus et rien ne passait. Trois désaccords sur 20, aucun ne désignant une erreur de l'étalon, qui n'a pas été touché. Le plus instructif est l'entrée 3 (Heston) : le trieur la classe `partiel` parce que le test d'origine est transversal et ne se transpose qu'en série temporelle — factuellement VRAI, H03 l'a fait — mais la règle réserve `partiel` à une DONNÉE manquante, pas à un travail de traduction ; confusion entre difficulté de transposition et absence de donnée. DÉFAUT DU PROTOCOLE TROUVÉ EN LE LANÇANT : corpus/TRIAGE.md § Ce que le trieur rend illustre le format avec DEUX ENTRÉES RÉELLES ET LEUR VERDICT JUSTE (entrée 1 `oui`, entrée 18 `non`), et l'entrée 18 est l'un des DEUX SEULS `non` — donc la moitié de la condition B donnée d'avance à quiconque reçoit ce fichier. Le passage 1 ne l'a PAS reçu et a classé l'entrée 18 `non` sans l'indice ; TRIAGE.md n'a PAS été corrigé pendant le passage (corriger le protocole dans le geste qui l'applique est ce que « le premier passage fait foi » interdit) — correction due avant tout passage 2. AUCUN test dépensé : counted_tests reste à 56, registre à 135 lignes. Reste la moitié EXTRACTION, bloquée sur l'acquisition (3 PDF pour 20 fiches) |
| 2026-09-19 | `outil` | Phase 07, l'entrée du trieur et son protocole : corpus/make_triage_input.py fabrique déterministiquement corpus/triage_input.json (les 20 lignes d'AMORCE.md privées de leur colonne verdict, TITRES DE SECTION NON REPRIS — le titre E dit « la famille que mes données ferment », c'est le verdict lui-même) et l'audite ; corpus/TRIAGE.md pose le protocole ; D15 reçoit un § Complément daté, écrit AVANT tout passage | LA MISE EN ŒUVRE A TROUVÉ UNE CONDITION QUE D15 NE PORTAIT PAS : une session qui a LU la colonne ne peut pas être le trieur — elle réciterait, et sa matrice serait parfaite pour la pire des raisons (L15 : le résultat conforme est celui que personne n'examine). Le piège est structurel — la séquence de démarrage de CLAUDE.md conduit toute session à lire l'étalon, donc une session arrive CONTAMINÉE PAR DÉFAUT. La session du jour s'est disqualifiée elle-même comme trieur (F42) plutôt que de produire un résultat flatteur. Ce n'est pas une impossibilité par construction — on n'empêche pas un lecteur de lire, et F13/F15/F16/F25 ont déjà refusé la vigilance déguisée en architecture — donc la règle est ÉCRITE et le § Journal de D15 note pour chaque passage qui a trié et ce qu'il avait vu. État : entrée fabriquée et auditée (20 entrées, 3 à 5 champs selon la section), juge vert sur 10 vérifications, IL MANQUE UN TRIEUR NON CONTAMINÉ |
| 2026-09-19 | `decision` | D15 écrite AVANT que le trieur existe : le seuil du triage, en EFFECTIFS et non en pourcentages (sur 13 `oui`, un item vaut 7,7 points de rappel — un seuil en % est un effectif mal déguisé, F37) ; trois classes et matrice de confusion entière, `partiel` NON replié (le replier effacerait la distinction qui a écarté Mesfin et cadré Heston, F38) ; quatre conditions — A ≤ 1 `oui` manqué sur 13, B = 0 `non` promu `oui`, C ≤ 2 `partiel` en désaccord sur 5, D = 0 désaccord de deux crans ; ce que le trieur VOIT est fixé : la ligne d'AMORCE.md privée de sa colonne verdict, exactement ce que l'auteur humain avait en phase 01, pas le PDF (F41) ; corpus/score_triage.py écrit et vérifié avant l'accusé | L'ÉTALON A DÛ ÊTRE COMPTÉ AVANT D'ÊTRE UTILISÉ, et il ne l'avait pas été : ETAT.md annonçait 24 entrées notées et six `partiel`, la colonne en porte 20 — 13 `oui` / 5 `partiel` / 2 `non`, les 4 entrées de la section G n'ayant pas cette colonne ; et AMORCE.md se contredisait lui-même — son § Verdict compte 12/5/3, l'écart portant sur l'entrée 9 (billet FRBNY), que la colonne marque `oui` et que le résumé range parmi les fermées. D15 tranche que LA COLONNE FAIT FOI (F39), l'entrée 9 n'est pas retirée (F40), et le § Verdict reçoit une note datée — texte d'origine conservé, comme pour l'entrée 7. score_triage.py : 10 vérifications vertes, huit sorties de trieur fabriquées rendant chacune le verdict que D15 écrit, et deux mutations d'AMORCE.md que le garde de l'étalon refuse. Le premier passage du trieur fera foi ; tout passage ultérieur s'inscrit au § Journal de D15 avec ce qui a changé. ETAT.md, hypotheses/README.md (counted_tests disait encore 4 pour deux hypothèses, c'est 56 pour trois) et la page de phase corrigés. Six portes rejouées vertes ce jour ; registre 130 -> 135 lignes, toutes des calibrations, counted_tests inchangé à 56 |
| 2026-09-18 | `decision` | Phase 07, premier maillon : D14 écrite — le schéma de fiche n'est PAS tiré des trois fiches manuelles (elles divergent, F35) mais des six champs que CLAUDE.md § Le vocabulaire nomme depuis le premier jour, plus source et transposability ; corpus/SCHEMA.md, corpus/validate_fiches.py, corpus/check_fiches_guard.py ; D09 étendu aux fiches — un résultat recopié d'un papier est une VALEUR EXTERNE, il porte sa citation, et value_in_quote (le garde du catalogue) vérifie que la valeur s'y retrouve | les trois fiches manuelles REFUSÉES par leur propre schéma puis réécrites — c'était le test du schéma autant que des fiches ; aucune n'avait de champ `horizon`, la construction du signal portait deux noms différents ; le garde a attrapé un cas réel que je n'avais pas prévu — Mesfin écrit « Eleven signal families fail » en toutes lettres, donc aucun chiffre à retrouver : ajouté `spelled_out`, qui vérifie le MOT et NOMME la conversion comme un geste humain plutôt que de la cacher derrière `derived` (F36) ; check_fiches_guard.py : 23 vérifications, 11 fautes refusées chacune pour la raison prévue, fiche intacte acceptée ; reste la seconde moitié de la porte 07 — le triage, avec un seuil chiffré à écrire AVANT mesure (L06) |
| 2026-09-18 | `gate` | PORTE 06 FRANCHIE — les deux clauses. D13 écrite AVANT la mesure (comme H03 l'exigeait) : après l'échec de deux cibles, la clause 2 est satisfaite quand la CHAÎNE reproduit un fait publié sur nos données, et non quand le harnais d'IC reproduit un IC publié. Cible : Andersen & Bollerslev (1997), papier récupéré, lu, fiché ; H04 pré-enregistrée ; scripts/measure_h04.py écrit dans scripts/ et NON dans harness/ — y ajouter un fichier périmerait les 56 lignes comptées | 19 vérifications, LES QUATRE CLAUSES TIENNENT : forme en U sur NQ/ES/YM, ouverture et clôture au-dessus du milieu, creux au milieu de séance, rapports sommet/creux 2,05 / 1,74 / 1,89 tous dans [1,4 ; 3,0] écrit d'avance — et ES x US, LE MÊME CONTRAT que leur figure, rend 1,74 contre leur 1,91 trente ans plus tard ; AUCUN IC calculé, counted_tests reste à 56. Deux défauts trouvés par le premier passage de l'instrument : (1) le garde interdisait aux paires d'autocorrélation d'enjamber la séance, ce qu'un décalage à la fréquence journalière fait PAR DÉFINITION — la clause C n'était pas mesurée et le script concluait quand même « les quatre clauses tiennent » ; (2) le témoin de la clause C était placé à ±15/30 min du multiple, presque à la MÊME PHASE du cycle : écart +0,006 à +0,010, contre +0,046 à +0,068 à phase opposée (diagnostic non pré-enregistré). La clause mesurait un PLANCHER de l'effet. L16 ; phase courante = 07 |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 13 |
| `phases` | 7 |
| `reference` | 3 |
| `research` | 7 |
| `signaux` | 1 |

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
> Bloc **editable a la main**. Le generateur le relit et le reinjecte tel quel.
> Tout ce qui est en dehors des marqueurs est ecrase a chaque regeneration.

- _(rien d'inscrit — voir « Prochaine action » ci-dessus, qui vient de `ETAT.md`)_
<!-- NEXT-ACTIONS:END -->

---

À lire au démarrage : [[index]] puis [[Failed Ideas/ledger]] — règles permanentes de `CLAUDE.md` § Wiki.
