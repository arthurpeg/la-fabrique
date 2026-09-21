# D16 — Le seuil de l'extraction : la fidélité à la source, pas la ressemblance à l'étalon

**Date :** 2026-09-20
**Phase :** 07
**État :** prise

## La question

À quoi reconnaît-on qu'une fiche **produite automatiquement** est bonne ? `D14`
fixe ce qu'une fiche doit contenir, et `corpus/validate_fiches.py` le garde ;
aucun des deux ne dit à quelle condition l'extracteur a réussi. C'est la moitié
extraction de la porte 07, et elle n'a pas de juge.

## Les options

**1. Apparier à l'étalon, comme `D15` l'a fait pour le triage.** Trois fiches
sont écrites à la main — Mesfin, Heston, Andersen & Bollerslev — et pourraient
servir d'étalon. **Écartée comme condition principale**, et il faut dire
pourquoi : l'étalon du triage portait **20 verdicts** et l'on pouvait écrire un
seuil en effectifs qui veuille dire quelque chose. Ici le dénominateur est
**3**. Un seuil sur trois fiches ne distingue pas un extracteur correct d'un
extracteur chanceux, et un seuil en pourcentage sur trois items est ce que `F37`
a déjà refusé : un effectif mal déguisé.

**2. Comparer les champs de prose — `claim`, `transposability` — par
ressemblance de texte.** Écartée. Deux formulations justes d'une même hypothèse
ne se ressemblent pas ; deux formulations fausses peuvent se ressembler
beaucoup. On mesurerait le style et l'on croirait mesurer la justesse.

**3. Juger sur la fidélité à la source, mécaniquement, sans étalon.** Retenue.
Ce qui peut échouer gravement dans une fiche produite par un LLM n'est pas
l'imprécision : c'est la **citation fabriquée** et le **chiffre inventé**. Or
les deux se vérifient sans aucun étalon, **contre le texte du papier lui-même**,
et avec une tolérance de zéro.

**4. Un juge humain relisant chaque fiche.** Écartée comme condition de porte :
elle ne s'automatise pas, et la phase 09 demandera 30 à 50 fiches. Conservée
comme **diagnostic** — voir § Ce que le juge imprime sans en faire une
condition.

## Le choix

**Une fiche produite est acceptée quand elle est fidèle à son papier, pas quand
elle ressemble à la fiche que nous aurions écrite** : cinq conditions
mécaniques, toutes à **tolérance zéro**, dont la principale est que chaque
`quoted` se retrouve **mot pour mot** dans le texte du papier. L'accord avec une
fiche de référence est mesuré et imprimé, mais ne conditionne la porte que sur
les champs **factuels**, où « différent » veut dire « contradictoire » et non
« formulé autrement ».

Le juge est `corpus/score_extraction.py`, écrit et vérifié **avant que
l'extracteur existe**.

## Pourquoi

**L'interdit constitutionnel dit déjà ce qu'il faut attraper.** `CLAUDE.md`
§ Les interdits : *ne jamais inventer une valeur de données* — *une valeur
plausible inventée devient indétectable en aval ; un `null` est bruyant*. Un
extracteur LLM est exactement la machine à produire des valeurs plausibles
inventées. La fiche Mesfin cite « *2.0 points ($4.00 per micro contract)* » ; un
extracteur qui aurait écrit 2,5 au lieu de 2,0 aurait produit une fiche
parfaitement conforme au schéma, parfaitement vraisemblable, et fausse. Rien en
aval ne l'aurait rattrapée — `L14` a montré ce que coûte un ordre de grandeur
recopié sans être vérifié, et il ne s'agissait là que d'un facteur 10 lu dans
notre propre wiki.

`D14` avait déjà posé la moitié du garde : une `value` numérique doit se
retrouver dans sa `quoted`. **Il manquait l'autre moitié, et c'est la plus
importante** : que la `quoted` elle-même existe dans le papier. Un extracteur
qui fabrique la citation *et* le chiffre qu'elle contient passe `D14` sans une
faute. Le contrôle se referme ici.

**Pourquoi la tolérance est zéro et non « peu ».** Les seuils de `D15` étaient
en effectifs parce qu'un désaccord de triage est une **différence de jugement**,
et qu'un juge peut raisonnablement différer. Une citation absente du papier
n'est pas un désaccord : c'est une fabrication. Il n'y a pas de dose acceptable,
donc pas de seuil à écrire — seulement un compte, qui doit valoir zéro.

**Ce que ça sacrifie, et c'est réel.** Ce juge ne sait pas dire qu'une fiche est
*creuse*. Un extracteur qui recopierait fidèlement trois citations
insignifiantes et laisserait de côté le résultat central du papier passerait les
cinq conditions. La fidélité est vérifiée ; la **pertinence** ne l'est pas, et
aucun code déterministe ne la vérifiera. C'est le prix de n'avoir que trois
fiches de référence, et il est payé les yeux ouverts : le diagnostic imprime de
quoi le voir, le § Journal l'enregistre, et la phase 09 — trente à cinquante
fiches — sera le premier moment où cette question aura un dénominateur.

## Les cinq conditions

Elles valent **ensemble**, par fiche produite. Trois sur cinq ne franchissent
rien — la règle de `D15`, inchangée.

| | Condition | Tolérance |
|---|---|---|
| **F1** | la fiche passe `corpus/validate_fiches.py` — le schéma de `D14` | 0 faute |
| **F2** | chaque citation de `reported_results` se retrouve **mot pour mot** dans le texte du papier, normalisation faite — voir le **Complément du 2026-09-20**, qui introduit la réparation déclarée `quoted_source` / `quoted_repair` | 0 citation introuvable |
| **F3** | chaque `value` numérique se retrouve dans la citation **qui fait foi**, sauf `derived` ou `spelled_out` déclarés — voir le Complément | 0 faute |
| **F4** | `source.pdf` désigne un fichier **présent**, et `source.source_url` est l'adresse d'où il vient | 0 faute |
| **F5** | sur les champs **factuels**, aucune **contradiction** avec la fiche de référence, quand il en existe une | 0 contradiction |

**La normalisation de `F2`**, écrite ici parce qu'elle décide de ce qui passe :
espaces multiples repliés, tirets et guillemets typographiques ramenés à leur
forme simple, casse ignorée. Elle ne va pas plus loin. Une citation dont les
**mots** diffèrent est introuvable, et c'est voulu : une paraphrase n'est pas une
citation, et `quoted` promet une citation.

**Les champs factuels de `F5`**, limitativement : `source.year`,
`source.amorce_entry`, `source.peer_reviewed`, et la **valeur** de `horizon`
quand les deux fiches en donnent une. Rien d'autre. `claim`, `universe`,
`signal_construction`, `what_is_missing` et les trois sous-champs de
`transposability` sont de la prose : ils sont **imprimés côte à côte** et
n'entrent dans aucune condition.

**Ce que `F5` ne compte pas comme contradiction** : l'absence. Une fiche produite
qui reste muette là où la référence parle n'est pas en contradiction avec elle —
elle est plus pauvre, ce que le diagnostic dira. `F5` n'attrape que deux valeurs
présentes et incompatibles.

## Ce que le juge imprime sans en faire une condition

Parce que `L06` vaut ici mot pour mot — *un compte juste n'est pas un compte de
choses justes* — le juge imprime, et l'on regarde :

- les `name` de `reported_results` présents dans la référence et **absents** de
  la fiche produite, et l'inverse ; c'est la mesure la plus directe de la
  **pertinence**, celle qu'aucune condition ne porte ;
- les champs de prose côte à côte, référence et production ;
- le nombre de `null` justifiés — un extracteur qui répond `null` à tout est
  irréprochable au sens des cinq conditions et sans valeur.

Ces trois sorties **ne franchissent ni ne bloquent rien**. Elles sont là pour
être lues, et ce qu'on y lit s'inscrit au § Journal.

## Qui peut être l'extracteur

**La même règle que `D15` § Complément, pour la même raison, et elle n'est pas
théorique** : une session qui a lu la fiche de référence d'un papier ne peut pas
être l'extracteur de ce papier. Elle ne lirait pas le PDF, elle recopierait la
fiche — et `F2` passerait triomphalement, les citations venant de la fiche qui a
servi d'étalon.

Les trois fiches de référence sont **versionnées et lues par toute session qui
ouvre `corpus/fiches/`**. L'extracteur reçoit donc le **texte du papier**, le
schéma `corpus/SCHEMA.md`, et rien d'autre du corpus. Chaque passage s'inscrit au
§ Journal avec qui a extrait et ce qu'il avait vu, comme pour le triage.

**Et la leçon `L17` s'applique à ce fichier même** : aucun exemple de ce document
ni de `corpus/SCHEMA.md` ne doit porter le contenu réel d'une fiche de référence.
Le schéma en porte déjà — la citation d'Andersen & Bollerslev et le rapport 1,91
y figurent en exemple. **C'est une fuite du même genre que celle de
`corpus/TRIAGE.md`**, et elle est nommée ici plutôt que corrigée à la hâte : elle
ne concerne qu'un papier sur les trois, et la corriger demande de décider ce
qu'un schéma peut montrer sans montrer une réponse. Ouvert ci-dessous.

## Ce que ça verrouille

- **La porte 07, moitié extraction**, se vérifie désormais par
  `corpus/score_extraction.py` et ses cinq conditions. Les changer est une
  décision écrite, et **tout résultat d'extraction antérieur devient périmé** —
  la règle du harnais, appliquée à l'extracteur, comme `D15` l'a appliquée au
  trieur.
- **Les trois fiches de `corpus/fiches/` deviennent des références gelées** au
  même titre que la colonne d'`AMORCE.md` : on ne les réécrit plus pour les
  rapprocher d'une sortie d'extracteur. Une erreur qu'on y trouverait s'inscrit
  en note datée.
- **Le texte source devient une pièce du dépôt.** `F2` n'est vérifiable que si
  le texte extrait du PDF est conservé et reproductible. Les PDF restent hors
  dépôt (`.gitignore`) ; le **texte** dont les citations sont vérifiées doit être
  atteignable, et la forme de ce stockage est ouverte ci-dessous.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Où vit le texte source** dont `F2` vérifie les citations : à côté du PDF hors dépôt, ou versionné comme résultat. Tant que ce n'est pas tranché, `F2` se vérifie sur un fichier texte passé en argument | avant la première extraction réelle |
| **La fuite de `corpus/SCHEMA.md`** : ses exemples portent le contenu réel de la fiche Andersen & Bollerslev (`L17`). Un extracteur qui lit le schéma reçoit une réponse sur trois | avant la première extraction réelle |
| **Combien de fiches la porte 07 demande**, et depuis quel corpus : `AMORCE.md` n'en rend pas 20 atteignables. Question distincte de celle-ci, et elle n'est pas tranchée ici | décision suivante, avant de ficher en série |
| **La pertinence d'une fiche** — qu'elle retienne ce qui compte dans le papier — qu'aucune des cinq conditions ne porte | phase 09, premier dénominateur réel |
| **`validate_fiches.py` ignore `quoted_source`** et vérifie le chiffre contre `quoted` : sur une entrée réparée, `F1` est plus laxiste que `F3`. Le garde de `D14` doit l'apprendre | avant la première extraction réelle |
| ~~**Les trois fiches de référence ne passent pas `F2`**~~ **Fait le 2026-09-21 : les trois passent les cinq conditions.** Six entrées touchées, et **Heston n'en a demandé aucune** — voir le Complément du 2026-09-21 | **fait** |
| **La qualité de l'extraction de texte** — et la question a **changé de nature le 2026-09-21** : le défaut de `pypdf` abîme aussi un PDF **né numérique** (Heston), et son mode `layout` répare les trois fiches sans en toucher une. **Quel mode fait foi** est donc une décision à écrire, et elle conditionne toute `quoted_source` | **avant la première extraction réelle**, remontée |

## Complément du 2026-09-20 — `F2` rencontre trois vrais papiers, et sa prémisse casse

Écrit **le jour même**, avant tout passage d'extracteur : le § Journal ci-dessous
est vide, et ce complément ne rattrape aucun résultat. Il corrige une **prémisse
fausse**, pas un seuil qui gênait.

**La prémisse.** `F2` supposait que « le texte du papier » est une chaîne bien
définie, et qu'une citation exacte s'y retrouve. Les trois PDF de référence ont
été récupérés et le juge lancé sur eux. **`F2` casse sur les trois**, et pour
trois raisons différentes — dont une seule est une faute.

| Papier | Ce que `F2` a trouvé | Qui a tort |
|---|---|---|
| Andersen & Bollerslev (1997) | le PDF est un **scan** : son texte dit « the **fight** part » pour « right part », « pa » pour ρ, « ]rt,,,] » pour \|R\| | **le texte**. La fiche cite le papier tel qu'un humain le lit |
| Mesfin (2026) — `walk_forward_folds` | la citation vient d'un **tableau**, que l'extraction rend en cellules à la file | **personne**. La fiche a mis le tableau en prose, ce qui est fidèle et non citable |
| Mesfin (2026) — `acceptance_criteria` | `quoted` annonce « t-statistic >= 2.0 on out-of-sample net returns, **>= 30 trades** » ; le papier écrit « t-statistic of at least 2.0 on out-of-sample (oos) net returns » | **la fiche**. C'est une **paraphrase** appelée citation |

**Ce troisième cas est ce que `F2` est fait pour attraper**, et il l'a attrapé
dans une fiche écrite à la main, par une session qui avait lu le papier. Le
mécanisme est donc juste ; c'est son entrée qui n'est pas ce qu'on croyait.

### Ce qui change : la réparation **déclarée**

Une entrée de `reported_results` peut porter **deux** chaînes :

- `quoted` — lisible, ce que le papier dit ;
- `quoted_source` — **mot pour mot dans le texte extrait**, et c'est elle que
  `F2` cherche ;
- `quoted_repair` — **pourquoi** les deux diffèrent, dans une liste **close** :
  `ocr`, `math_notation`, `table`.

C'est le geste de `D14` avec `spelled_out`, repris à l'identique : **on nomme la
réparation humaine au lieu de la cacher**. Et comme `D09`, la liste est close —
une échappatoire nommée, jamais une échappatoire générique.

**Ce qui ne change pas, et c'est l'essentiel** : il faut toujours **une chaîne
présente à la lettre** dans le texte. Une réparation déplace ce qui est cherché,
jamais ce qui est exigé. Une paraphrase ne fournit aucune chaîne, donc
`acceptance_criteria` reste une faute — et doit le rester.

Trois garde-fous, vérifiés :

- `quoted_source` sans `quoted_repair` valide → faute ;
- `quoted_repair` sans `quoted_source` → faute ;
- `quoted_repair` hors de la liste close → faute.

**Et `F3` suit la chaîne qui fait foi.** Le chiffre est cherché dans
`quoted_source` quand elle existe, sinon dans `quoted`. Sans cela, la réparation
deviendrait exactement l'endroit où loger un nombre que le papier ne porte pas.

### Ce que ce complément a découvert sur le garde de `D14`

`validate_fiches.py` ignore `quoted_source` et vérifie le chiffre contre
`quoted`. **Sur une entrée réparée, `F3` est donc plus strict que `F1`** : une
valeur logée dans la version lisible et absente de la source passe `D14` et casse
`F3`. Vérifié. Le garde de `D14` doit apprendre `quoted_source` — ouvert
ci-dessous, et non corrigé ici : `D14` n'est pas ma décision à amender en
passant.

### Ce que les trois fiches de référence doivent devenir

Elles ne passent pas `F2` aujourd'hui. **Elles ne seront pas réécrites en
silence** — `D15` a posé la règle pour l'étalon du triage et elle vaut ici : une
erreur trouvée dans une référence gelée s'inscrit en **note datée**, sous
l'entrée d'origine, jamais par réécriture. Trois gestes distincts, et il faut les
distinguer :

1. Andersen & Bollerslev et le pli de Mesfin : ajouter `quoted_source` +
   `quoted_repair`. La fiche ne change pas de sens, elle déclare sa réparation.
2. `acceptance_criteria` de Mesfin : la citation est **fausse**. Note datée, et
   la vraie citation mise à côté.
3. Rien d'autre.

**Aucun de ces trois gestes n'est fait ici.** Ils touchent des références gelées,
et les faire dans le mouvement qui écrit leur juge est ce que `L17` vient
d'apprendre à ne pas faire.

## Complément du 2026-09-21 — les réparations faites, et ce qu'elles ont corrigé de ce document

Les trois fiches de référence passent désormais les cinq conditions. Le § Journal
ci-dessous reste **vide** : aucune extraction n'a eu lieu, et ce complément ne
rattrape aucun résultat.

### Ce qui a été fait, et ce que le Complément du 2026-09-20 n'avait pas vu

Il annonçait **trois gestes**. Le juge, lancé sur les trois fiches, en a demandé
**six** — et un de ceux qu'il annonçait s'est révélé inutile.

| Fiche, entrée | Geste | Prévu par le Complément du 20 ? |
|---|---|---|
| A&B, `fx_first_order_autocorr_abs_returns` | `quoted_source` + `quoted_repair: ocr` (« pA » pour ρ, « 1/x/T » pour 1/√T) | oui, en gros |
| A&B, `fx_ljung_box_10` | idem (« ]Rt,,,] » pour \|R\|, « QA(10) » pour Q(10)) | oui, en gros |
| A&B, `shape_variant_j` | idem (« fight part » pour « right part ») | oui, en gros |
| Mesfin, `walk_forward_folds` | `quoted_source` + `quoted_repair: table` | **oui** |
| Mesfin, `acceptance_criteria` | citation corrigée, note datée, texte d'origine conservé | **oui** |
| Mesfin, `families_failing_below_friction` | citation corrigée, note datée | **non — faute non vue** |

`families_failing_below_friction` fermait sa citation par un **point** là où le
papier écrit deux points et poursuit. Un caractère, et la citation est
introuvable. Ce n'est pas une subtilité : c'est la démonstration que `F2` ne
pardonne rien, ce qui est sa raison d'être.

### Le motif donné pour `acceptance_criteria` était faux, le verdict tenait

Le Complément du 20 écrivait que le papier dit seulement
*« t-statistic of at least 2.0 on out-of-sample (oos) net returns »* et que
« >= 30 trades » **ne figure pas** dans la phrase citée. **C'est inexact.** Le
résumé de Mesfin poursuit : *« at least 30 trades per OOS fold »*. Le contenu
était dans le papier ; c'est la **formulation** que la fiche avait réécrite
(« >= » pour « at least », articles supprimés). Le verdict — paraphrase, donc
faute — tient entièrement ; son motif était mal dit.

**Et la faute était pire que dite.** La citation était un **composite** : son
seuil de permutation (`p < 0.001`) vient du **Tableau 3**, le reste de la phrase
vient du **résumé**, qui écrit `p < 0.05`. **Le papier se contredit lui-même**, et
la fiche avait silencieusement fondu les deux passages en un seul. La citation
retenue est celle du résumé, verbatim ; le désaccord interne du papier est
inscrit en note comme un **fait sur le papier**, non tranché.

### Heston n'avait rien à réparer — c'est l'extracteur qui avait tort

Ses **cinq** citations échouaient, et aucune n'était fautive. Le texte rendu par
`pypdf` insère des espaces à l'intérieur des mots : « multiples o f 13 »,
« half-hour inte rvals », « way is d ifferent ».

**Aucune valeur de la liste close ne nommait ce cas avec justesse.** `ocr` aurait
été un **mensonge** : les métadonnées du PDF disent *LaTeX with hyperref* et
*GPL Ghostscript* — il est **né numérique**, pas scanné. Plutôt que d'ouvrir la
liste close en passant, l'hypothèse a été testée à la racine, et elle tombe :

| | défaut | `extraction_mode="layout"` |
|---|---|---|
| Mesfin | `F2` tenue | `F2` tenue |
| Andersen & Bollerslev | `F2` tenue | `F2` tenue |
| Heston | **`F2` cassée (5)** | **`F2` tenue** |

**Le mode `layout` répare Heston sans toucher une ligne de sa fiche, et ne casse
aucune des deux autres.** Les six `quoted_source` écrites ce jour résistent aux
deux modes, vérifié.

**Ce que cela déplace.** La question ouverte « faut-il un OCR, un autre
extracteur ? » n'était pas une question sur les **scans** : le défaut de `pypdf`
abîme aussi un PDF propre. **Quel mode d'extraction fait foi** devient une
décision à écrire avant toute extraction réelle — elle conditionne chaque
`quoted_source` du projet, puisqu'une réparation déclarée est définie **contre un
texte**. Elle n'est pas tranchée ici : ce n'est pas un seuil qu'on ajuste dans le
geste qui l'applique.

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

Chaque ligne dit **qui a extrait, ce qu'il avait vu**, et ce que le diagnostic a
montré.

| # | Date | Papier | Extracteur, et ce qu'il avait vu | F1–F5 | Ce que le diagnostic a montré |
|---|---|---|---|---|---|
| 1 | 2026-09-21 | entrée 13, Patton & Sheppard (2015) | agent séparé, interdiction de lecture explicite ; n'a reçu que `corpus/consignes/entree-13-*.md` — schéma, texte du papier, consigne. **Aucune fiche de référence n'existait pour ce papier** | **les cinq tiennent** | 25 résultats, **7 réparations déclarées** (5 `ocr`, 2 `table`), 2 itérations — voir ci-dessous |

### Ce que le passage 1 a appris

**Aucune citation n'a été refusée.** `F2` et `F3` sont passées du premier coup.
Le seul échec de la première itération était `F1` — `signal_construction` écrit
comme un objet structuré sans la clé `value` que le schéma exige. Le schéma a
donc attrapé une faute de **forme**, pas de **fidélité**, ce qui est l'ordre
souhaitable.

**`D18` a été validée par le réel dès ce passage.** La citation
`spdr_first_autocorr_max` n'est présente que dans l'extraction **`default`** :
`layout` la casse. Sous l'option 2 de `D18` — `layout` seul — cette citation
juste aurait été refusée. L'union n'est pas une précaution théorique ; elle a
servi au premier essai.

**Les sept réparations ont été vérifiées à la main**, après le juge et
indépendamment de lui : chaque `quoted_source` est littéralement présente dans
au moins une extraction, et **chaque valeur numérique est dans la chaîne qui fait
foi** — le point où `D16` craignait qu'on loge un chiffre absent du papier. Les
motifs sont honnêtes : quatre ligatures `ﬁ`, une césure de fin de ligne, une
ligne éclatée par des exposants, deux lignes de tableau mises à plat.

### Ce que ce passage a ouvert, et qui n'est pas tranché

**Le côté *lisible* d'une réparation n'a aucune règle.** `D16` définit
`quoted_source` au caractère près et laisse `quoted` « lisible ». Sur les deux
réparations `table`, « lisible » est devenu une **glose en français** —
« *Table 5, ligne h = 66 : la statistique DM du SPDR pour...* » — qui n'est plus
une citation du tout. Rien de mécanique n'en souffre, `F2` et `F3` suivant
`quoted_source`. Mais `quoted` est ce qu'un humain lit pour contrôler la fiche,
et une glose n'est pas contrôlable contre le papier.

**La fiche n'a PAS été retouchée**, et c'est `G3` de `D17` : zéro retouche
manuelle. Corriger la sortie de l'extracteur à la main serait exactement la
faille que `G3` ferme. Le constat est inscrit ici ; s'il faut une règle, c'est
une décision, et l'extracteur sera relancé.

**Et la limite que `D16` s'était donnée s'est vérifiée** : l'extracteur a
lui-même fait remarquer que le choix de ses 25 résultats n'a été contrôlé par
personne. Les cinq conditions sont mécaniques ; la **pertinence** n'aura de
dénominateur qu'en phase 09, comme § Pourquoi l'écrit.

Le juge est vert sur ses propres vérifications (`python
corpus/score_extraction.py --check`) et **l'extracteur n'existe pas encore**.
