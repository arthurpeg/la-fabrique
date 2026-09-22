---
type: hub
updated: 2026-09-22
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-22.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 07 — triage et extraction sur 20 papiers connus |
| **Dernière porte franchie** | **06**, le 2026-09-18 — les deux clauses. Clause 1 (dégénérescence) : `gate_06_controls.py`, 25 vérifications. Clause 2 (réplication) : `scripts/measure_h04.py`, 19 vérifications, `H04` pré-enregistrée |
| **Décision la plus récente** | `decisions/DECISION-20-le-moissonnage-du-corpus.md` — le moissonneur **ratisse et ne juge pas**. Requête écrite avant d'être lancée, six familles reprises des |
| **Tests au registre** | 159 |
| **Idées abandonnées recensées** | 54 |
| **Entrées au journal** | 45 |

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
`corpus/score_extraction.py`, **32 vérifications**, vert — 21 à l'écriture de
`D16`, portées à 32 par le correctif de `D17`. Compté en lançant
`python corpus/score_extraction.py --check`, non recopié.

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

1. ~~Le recensement des atteignables.~~ **Fait le 2026-09-21 : 19 atteignables
   sur 20**, dont 18 en PDF. `corpus/acquisition.json`, produit par
   `corpus/probe_acquisition.py`, gardé par `corpus/check_acquisition.py`
   (11 vérifications, vert), expliqué par `corpus/ACQUISITION.md`. **`D17` s'est
   trompee sur ce point et son § Journal le dit** : elle prévoyait 6 à 14 « selon
   ce que SSRN consent » ; SSRN n'a rien consenti (contrôle anti-robot, non
   contourné) et le compte est plus haut quand même, parce que ces papiers vivent
   aussi au NBER, à la Fed, sur des pages d'auteurs et dans des dépôts
   universitaires. S'en tenir aux liens d'`AMORCE.md` aurait rendu **5**.
2. ~~Télécharger les 15 PDF atteignables absents du disque.~~ **Fait le
   2026-09-21 : 18 PDF sur 18 sont dans `corpus/pdf/`**, par
   `corpus/fetch_pdfs.py`, chacun vérifié après écriture (`%PDF-` et taille).
   Les 18 rendent du texte à `pypdf` — **ce qui ne dit pas que ce texte est
   juste** : l'entrée 11 en rend 2 787 caractères par page et `D17` a montré
   que ce sont ceux d'un scan fautif. Aucun n'est vide ; la qualité reste
   l'affaire de `F2`.
3. ~~Réparer les trois fiches de référence.~~ **Fait le 2026-09-21 : les trois
   passent les cinq conditions de `D16`.** Six entrées touchées et non trois — le
   juge a trouvé une faute que `D16` n'avait pas vue (`families_failing_below_friction`,
   un point là où le papier écrit deux points). **Heston n'a demandé aucune
   réparation** : ses cinq échecs venaient de l'extracteur de texte, pas de sa
   fiche. Voir `D16` § Complément du 2026-09-21.
4. ~~Trancher quel mode d'extraction fait foi.~~ **Fait le 2026-09-21 : `D18`.**
   Le texte qui fait foi est l'**union de deux extractions fixées d'avance et
   identiques pour tous les papiers** — `pypdf` par défaut et `layout` —
   produites par `corpus/extract_text.py` et **versionnées** dans `corpus/text/`
   (36 fichiers, 6,2 Mo, empreintes au manifeste). Un mode par papier a été
   **écarté** : ce serait un bouton qu'on tourne jusqu'à ce que la fiche passe.
5. ~~Apprendre `quoted_source` à `validate_fiches.py`.~~ **Fait le 2026-09-21.**
   L'asymétrie que `D16` avait nommée est fermée : le schéma contrôle désormais
   le chiffre contre **la chaîne qui fait foi**. `check_fiches_guard` passe de 23
   à **31 vérifications**, 15 fautes refusées.
6. ~~La fuite de `corpus/SCHEMA.md`.~~ **Fermée le 2026-09-21**, et c'était un
   préalable à l'extracteur, pas un nettoyage : le schéma illustrait ses exemples
   avec le contenu **réel** d'une fiche de référence, et c'est le seul document du
   corpus que l'extracteur a le droit de lire. Exemples refaits sur un papier
   fictif ; la réparation déclarée y est désormais documentée, faute de quoi un
   extracteur devant un texte abîmé paraphraserait.
7. **L'extracteur existe** — `corpus/extract_fiche.py`, harnais **sans
   intelligence d'extraction** : il prépare la consigne et juge la sortie.
   L'extracteur est une **session séparée** qui reçoit le schéma, le texte du
   papier, et **rien d'autre du corpus**. **Passage 1 tenu le 2026-09-21** sur
   l'entrée 13 (Patton & Sheppard) : **les cinq conditions tiennent**,
   25 résultats, 7 réparations déclarées, 2 itérations, **aucune citation
   refusée** — le seul échec portait sur la forme (`F1`), pas sur la fidélité.
   `D16` § Journal dit ce qu'il a appris.
8. ~~Corriger `value_in_quote`.~~ **Fait le 2026-09-22, et la fonction est
   désormais UNIQUE.** Elle vivait en **deux exemplaires** — celui du catalogue
   (`D09`), importé par `F1`, et une copie dans `score_extraction` utilisée par
   `F3` — avec deux motifs de nombre différents. `score_extraction` importe
   maintenant celle du catalogue : **une règle, une implémentation**.
   Le motif n'a pas simplement reçu un signe : `(?:(?<![\w.])-)?\d+(?:\.\d+)?`,
   où un `-` n'est un **signe** que s'il ne colle pas à un mot ni à un chiffre.
   Un signe naïf aurait lu `115-158` (des pages), `0.25-0.50` (un intervalle) et
   `Nasdaq-100` comme des négatifs — or `D09` s'appuie précisément sur la
   citation `$20 x Nasdaq-100 Index`. **Effet mesuré : 5 fiches vertes → 7.**
   Gardes rejoués verts : catalogue, `check_provenance` (33 vérifications, 9
   fautes refusées), et **les six portes**, registre 135 → 140 lignes (des
   calibrations), `counted_tests` inchangé à 56, harnais inchangé `9ac3e45e`.
9. **Trancher `signal_construction` comme objet structuré.** **4 extracteurs
   indépendants sur 6 ont fait la même faute** : ils écrivent un objet
   (`sampling`, `components`, `model`…) sans la clé `value` que le schéma exige.
   Quatre fois la même erreur n'est pas quatre erreurs, c'est un défaut du
   schéma ou de la consigne.
10. **Ficher les 8 papiers restants** — `G1` exige zéro atteignable non fiché.
    `python corpus/extract_fiche.py --list` dit lesquels. Chacun demande une
    **session séparée** qui n'a pas lu `corpus/fiches/`. **Sauf l'entrée 1 :
    son PDF est le mauvais papier** (voir l'alerte ci-dessous, `L20`) — la ficher
    avant de l'avoir réparée produirait une fiche fidèle à un texte qui n'est pas
    celui qu'elle annonce, et les cinq conditions n'y verraient rien.
11. **Réparer les 3 fiches refusées** — andersen-2003, corsi-2009, lou-2019.
    Elles se **refont**, elles ne se retouchent pas (`G3`).

### Trois cassures trouvées et réparées le 2026-09-22

Une session de vérification a lancé **tout ce qui est exécutable** dans le
dépôt — six portes, les gardes du corpus et du catalogue, le lint du wiki.
**Tout ce qui devait passer passait**, à trois exceptions, et les trois tenaient
à la même cause de fond : *un fait vrai d'un poste, écrit comme un fait du
dépôt*.

| | Ce qui cassait | Réparé par |
|---|---|---|
| 1 | **15 PDF sur 18 absents** du disque, `ETAT.md` les annonçant présents | `corpus/fetch_pdfs.py` — 15 repris, 0 échec, 18 sur 18 vérifiés |
| 2 | La fiche **Patton & Sheppard** échouait `F4`, son PDF étant absent | conséquence de 1 ; les cinq conditions tiennent à nouveau |
| 3 | `extract_text.py --check` : **31 fichiers sur 36 divergents** | `D19` — `pypdf` épinglé à `==6.14.2` |

**La troisième est la seule qui ait appris quelque chose**, et elle est
inscrite en `L19`. `uv.lock` portait `pypdf 6.19.0` depuis le 2026-09-20 ; le
texte qui fait foi a été produit le 2026-09-21 avec **6.14.2**, par un
environnement en retard sur le verrou commité. Le manifeste le notait
fidèlement — **noter n'est pas contraindre**.

Deux causes possibles ont été séparées avant de trancher, les PDF venant d'être
repris : le même corpus ré-extrait sous 6.14.2 rend **36 sur 36 conformes**, donc
la version était seule en cause. Et la mesure a **retourné l'intuition** :
6.19.0 récupère +0,05 % / +0,66 % de contenu mais **dégrade de 12 %** les
lettres orphelines en mode `layout`. Aucune des deux versions n'est meilleure ;
le choix s'est décidé sur le coût.

**Ce qui n'a pas bougé** : le harnais (`9ac3e45ed8413e13`), `counted_tests()` à
**56**, les six portes vertes après réparation. `uv lock` n'a déplacé que
`pypdf` — `numpy`, `pandas`, `scipy` et `pyarrow` sont inchangés, donc aucun
résultat de harnais n'est concerné.

### RÉPARÉE le 2026-09-22 — l'entrée 1 désignait le mauvais papier

**Trouvée le 2026-09-22 par le moissonneur, et c'est `L20`.**
`corpus/pdf/gao-2018-market-intraday-momentum.pdf` — déclaré par
`acquisition.json` comme *Gao, Han, Li & Zhou (2018), « Market intraday
momentum », JFE 129(2):394-414* — est en réalité **Limkriangkrai, Chai & Zheng
(2023), « Market intraday momentum: APAC evidence », *Pacific-Basin Finance
Journal* 80:102086**. Treize pages, une autre revue, d'autres auteurs.

Le recensement prouvait qu'**un** PDF arrivait, jamais que c'était **le bon**.
Et les deux vérifications automatiques évidentes échouent toutes les deux : le
titre attendu est une **sous-chaîne** du titre réel, et le papier APAC **cite**
Gao et al. (2018) dès son résumé. Ce qui l'a attrapée est une **collision
d'empreinte `sha256`** entre deux affirmations indépendantes sur les mêmes
octets.

**Ce que ça touche :**

| | État |
|---|---|
| `corpus/text/gao-2018-*.txt` | **faux** — c'est le texte du papier APAC sous le nom de Gao, et il est commité |
| fiches | **aucune** ne s'en sert : les 4 fiches sont Andersen & Bollerslev, Heston, Mesfin, Patton. Rien en aval n'est contaminé |
| `G1` | l'entrée 1 reste comptée atteignable ; sa réparation ne change pas le compte, seulement le fichier |

**Réparée le 2026-09-22.** Le vrai Gao 2018 a été cherché par cinq routes
indépendantes, et **il n'a aucune copie libre atteignable** :

| Route | Verdict |
|---|---|
| OpenAlex, par DOI `10.1016/j.jfineco.2018.05.009` | `oa_status=closed`, **0 emplacement libre** |
| Semantic Scholar | `isOpenAccess=False`, `openAccessPdf: CLOSED` |
| SSRN 2440866, le lien d'`AMORCE.md` | **403**, contrôle anti-robot, **non contourné** |
| la seule copie libre indexée par un moteur | **`AccessDenied`**, y compris dans un vrai navigateur — index périmé |
| ScienceDirect | péage Elsevier |

**L'entrée 1 passe donc d'`atteignable` à `inatteignable`, raison
`refus_robot`** — même situation et même étiquette que l'entrée 6, dont le
recensement d'origine avait déjà tranché ainsi. Le recensement passe de **19 à
18 atteignables**, très au-dessus du seuil de 5 que `D17` avait écrit pour
rouvrir l'élargissement du corpus.

**Ce qui a été fait, dans l'ordre :** l'URL Monash retirée d'`ALTERNATES` et
remplacée par la prépublication SSRN, pour que le refus soit **inscrit comme
preuve** plutôt que supposé ; `ALERTES[1]` écrit ; le recensement re-sondé en
entier et **diffé contre sa sauvegarde — l'entrée 1 est le seul changement de
statut** ; le PDF erroné supprimé du disque ; **les deux fichiers de
`corpus/text/` supprimés du dépôt** et le manifeste `D18` reconstruit (17 PDF,
34 fichiers, **0 texte réécrit**, donc les 34 autres sont intacts).

**Un défaut latent trouvé en réparant, et il aurait mordu n'importe qui.** Le
champ `pdf` de `acquisition.json` — le seul chemin par lequel `extract_fiche.py`
relie une entrée à son fichier — **n'était écrit par aucun script**. Un
`probe_acquisition.py --write` le détruisait donc en silence, et
`extract_fiche --list` tombait sur un `KeyError`. Le champ est désormais produit
par le recensement, depuis la table **déclarée** de `fetch_pdfs.NAMES`, avec un
refus bruyant si un nom manque.

**État de `G1` après réparation** : **10 fichées, 7 à ficher** (entrées 2, 5, 8,
12, 18, 19, 20), **3 hors d'atteinte** (1 et 6 `refus_robot`, 9 en HTML).

### Le moissonneur existe — `D20`, le 2026-09-22

`corpus/harvest.py` et son garde `corpus/check_harvest.py`
(**16 vérifications**). Il **ratisse et ne juge pas** : le tri de
l'implémentable reste au trieur, qui a son juge et son étalon. Il ne contient
**aucune IA** — chercher et vérifier qu'un octet est `%PDF-` ne demande aucun
jugement.

**Passage 1** : 132 candidats, 127 sondés, **43 PDF enregistrés, 0 échec**,
6 doublons. Sous la cible de 50 à 100, et la cause est réparable —
`HARVEST_MAILTO` n'était pas renseigné, donc **Unpaywall n'a pas été interrogé**.

**Son produit n'entre pas dans `G1`–`G4`** et ne fait pas bouger la porte 07
d'un pouce : c'est `F47`, et `D20` la date plutôt que de la rouvrir.

### Ce qui reste ouvert par ailleurs

- **l'acquisition est recensée depuis le 2026-09-21** et ne bloque presque plus :
  **19 atteignables sur 20**, un seul inatteignable — l'entrée 6 (Wen et al.,
  pétrole), refusée par SSRN, péagée chez Elsevier, et sur ResearchGate seulement
  contre une demande à l'auteur, ce que `D17` exclut. Le compte de liens
  d'`AMORCE.md` — 14 avec lien, dont 12 libres — n'est plus le bon
  dénominateur : il décrit `AMORCE.md`, pas ce qui est à portée. **Ne jamais
  écrire ici combien de PDF sont sur le disque** : `corpus/pdf/` est ignoré par
  git, l'énoncé est vrai d'un poste et d'une heure, et il s'est déjà périmé
  trois fois — les 2026-09-18, 09-20 et 09-22. Le seul énoncé qui tient est
  celui du garde, lancé à l'instant où on en a besoin :
  `python corpus/fetch_pdfs.py --verify`. Ce qui, lui, est un fait du dépôt :
  **les 18 PDF sont re-téléchargeables** — le 2026-09-22, les 15 absents ont été
  repris depuis `acquisition.json` sans une seule source morte, et le texte
  ré-extrait est **identique au manifeste** (`D19`), donc les sources sont
  stables et l'acquisition est reproductible ;
- **deux alertes ouvertes par le recensement**, et aucune tranchée : l'entrée 9
  est libre mais en **HTML**, donc atteignable pour `D17` et infichable pour `F4`
  qui exige un `source.pdf` ; et la citation de l'**entrée 16** paraît fausse dans
  `AMORCE.md` — elle dit « Kurov, Sancetta, Strasser & Wolfe », le papier que son
  propre lien désigne est de **Kurov, Wolfe & Gilbert**. `AMORCE.md` n'a pas été
  touché : c'est l'étalon du triage (`D15`), et on ne retouche pas un étalon en
  passant ;
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
| 2026-09-22 | `correction` | ENTREE 1 REPAREE — elle passe `atteignable` -> `inatteignable`, raison `refus_robot`. Le vrai Gao, Han, Li & Zhou (2018) a ete cherche par CINQ ROUTES INDEPENDANTES et aucune n'ouvre : OpenAlex par DOI rend `oa_status=closed` avec 0 emplacement libre, Semantic Scholar rend `openAccessPdf: CLOSED`, SSRN 2440866 (le lien d'`AMORCE.md`) rend 403, ScienceDirect est peage Elsevier, et la seule copie libre indexee par un moteur rend `AccessDenied` Y COMPRIS DANS UN VRAI NAVIGATEUR — index perime. RIEN N'A ETE CONTOURNE. Meme etiquette que l'entree 6 dans la meme situation. Recensement : **19 -> 18 atteignables**, tres au-dessus du seuil de 5 de `D17` | FAIT DANS L'ORDRE, ET CHAQUE PAS VERIFIE : l'URL Monash retiree d'`ALTERNATES` et remplacee par la prepublication SSRN — pour que le refus soit INSCRIT COMME PREUVE plutot que suppose ; `ALERTES[1]` ecrit avec tout ce qui a ete constate ; le recensement re-sonde EN ENTIER puis **diffe contre sa sauvegarde**, et l'entree 1 est le SEUL changement de statut (un re-sondage complet pouvait degrader une autre entree sur un incident reseau, et ne pas le verifier aurait ete supposer) ; le PDF errone supprime ; LES DEUX FICHIERS DE `corpus/text/` SUPPRIMES DU DEPOT — c'est la partie delicate, ce sont des artefacts qui FONT FOI au sens de `D18` — et le manifeste reconstruit : 17 PDF, 34 fichiers, **0 texte reecrit**, donc les 34 autres sont intacts et `pypdf` est bien celui que `D19` epingle. DEFAUT LATENT TROUVE EN REPARANT (F54) : le champ `pdf` de `acquisition.json`, SEUL chemin par lequel `extract_fiche.py` relie une entree a son fichier, etait present dans 18 entrees au dernier commit et **ecrit par aucun script** ; mon `--write` l'a donc detruit en silence et `extract_fiche --list` est tombe sur un `KeyError`. Trouve PAR ACCIDENT — personne n'avait relance le recensement depuis. Repare a la source : le champ est produit par le recensement depuis la table DECLAREE `fetch_pdfs.NAMES`, avec refus bruyant si un nom manque ; import differe, `fetch_pdfs` important deja ce module. ETAT DE `G1` : **10 fichees, 7 a ficher** (2, 5, 8, 12, 18, 19, 20), 3 hors d'atteinte (1 et 6 `refus_robot`, 9 en HTML). GARDES VERTS APRES COUP : check_acquisition 11/11, check_harvest 16/16, check_fiches_guard, score_triage 10, score_extraction 32, catalogue valide, extract_text --check 34 fichiers, fetch_pdfs --verify 17/17, ruff corpus/ propre. TROIS FICHES RESTENT ROUGES et ne sont PAS de mon fait — andersen-2003, corsi-2009, lou-2019, arrivees par la fusion de la session parallele, cassant `F1` (schema) et `F3` (valeur dans sa citation), aucune sur `F2` donc aucune citation inventee ; `ETAT.md` les signale deja comme « 2 par un faux rejet du garde ». Non touchees : c'est du travail en cours qui n'est pas le mien. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13. F53, F54 |
| 2026-09-22 | `fusion` | DEUX SESSIONS PARALLÈLES RÉUNIES — le distant portait 3 commits d'une autre session sur la même phase 07 (`D19` épinglant `pypdf==6.14.2`, `D20` et le moissonneur, `L19`, `L20`), notre local en portait 2 (unification de `value_in_quote`, 10 fiches jugées). Aucune contradiction : leur travail REPART DU NÔTRE — `D19` répond au garde de `D18` qui s'est déclenché, `D20` automatise pour la phase 09 la table `ALTERNATES` que j'avais écrite à la main. Fusion, pas arbitrage | LES TROIS FICHIERS APPEND-ONLY RÉSOLUS PAR UNION VÉRIFIÉE, jamais par choix d'un côté. Registre : les deux côtés n'avaient qu'AJOUTÉ depuis l'ancêtre (135), aucun `test_id` commun, union contrôlée ligne à ligne. ET LA PORTE 04 A REFUSÉ MA PREMIÈRE UNION : je l'avais ordonnée CHRONOLOGIQUEMENT, donc leurs 10 lignes de 06:24 AVANT nos 7 de 07:33 — ce qui « réécrivait » 5 lignes déjà commitées. Le garde a dit exactement lesquelles ([136..140]). REFAIT dans l'ordre qui préserve le préfixe commité INTACT : l'append-only prime sur la chronologie, une ligne déjà commitée ne se déplace pas, même pour bien faire. C'est la porte qui m'a corrigé, pas ma vigilance — exactement ce pour quoi elle existe. `wiki/log.md` uni de même (37 -> 43 entrées), `LECONS.md` sans conflit (notre `L18` était déjà dans l'ancêtre, ils ont ajouté `L19` et `L20`). `ETAT.md` : LES DEUX RÉCITS CONSERVÉS, seul leur point « ficher les 14 » a été absorbé par notre « ficher les 8 », que notre avancement périmait. `wiki/hot.md` régénéré. ALERTE HÉRITÉE ET PROPAGÉE DANS `ETAT.md` : `L20` dit que le PDF de l'entrée 1 est LE MAUVAIS PAPIER ; notre point 10 interdit désormais de la ficher avant réparation — une fiche fidèle à un texte qui n'est pas celui qu'elle annonce passerait les cinq conditions sans que rien ne le voie. VÉRIFICATION COMPLÈTE DE L'ARBRE FUSIONNÉ : les SIX PORTES franchies, `extract_text --check` 36/36 conformes sous `pypdf 6.14.2` (la version épinglée par `D19` est bien celle installée), gardes du corpus, du catalogue, de la provenance et de la moisson (16/16) verts, lint wiki vert. counted_tests INCHANGÉ à 56, harnais INCHANGÉ à 9ac3e45e. Filet posé avant la fusion : l'étiquette `secours-avant-fusion-2026-09-22` |
| 2026-09-22 | `correction` | `value_in_quote` CORRIGÉE ET UNIFIÉE — elle vivait en DEUX EXEMPLAIRES, celui du catalogue (`D09`) importé par `F1` et une copie dans `score_extraction` utilisée par `F3`, avec deux motifs de nombre différents. `score_extraction` importe désormais celle du catalogue : UNE règle, UNE implémentation | LE MOTIF N'A PAS SIMPLEMENT REÇU UN SIGNE, et c'est tout le sujet. Un `-?` naïf aurait lu `115-158` (pages), `0.25-0.50` (intervalle) et `Nasdaq-100` comme des négatifs — or `D09` s'appuie précisément sur la citation `$20 x Nasdaq-100 Index` pour cautionner 20, et aurait perdu le 100. Motif retenu : un `-` n'est un SIGNE que s'il ne colle ni à un mot ni à un chiffre. Vérifié sur 9 cas construits AVANT le changement, dont le piège d'origine de `D09` (12500 contre « 12,500,000 ») qui reste attrapé. EFFET MESURÉ : 5 fiches vertes -> 7 ; kurov et zarattini n'étaient refusées QUE par ce faux rejet. GARDES REJOUÉS VERTS : catalogue valide, `check_provenance` 33 vérifications et 9 fautes refusées, garde des fiches 15 fautes, juge 32 vérifications, ET LES SIX PORTES (01 à 06, toutes franchies) — registre 135 -> 140 lignes, uniquement des calibrations, counted_tests INCHANGÉ à 56, empreinte du harnais INCHANGÉE à 9ac3e45e. SECOND DÉFAUT DU MÊME GENRE CORRIGÉ : `validate_fiches` plantait comme le juge sur un `UnicodeEncodeError` (console cp1252, signe moins venu d'un PDF) — j'avais réparé le juge la veille SANS voir que le garde avait le même défaut, alors que je venais d'écrire qu'un juge qui plante ne juge pas. Les deux impriment désormais en remplaçant À L'AFFICHAGE seulement. CE QUI RESTE, et qui est RÉEL cette fois : 3 fiches refusées — `signal_construction.value absent` (3 fois, le défaut systématique déjà noté), deux nombres d'andersen-2003 logis dans des citations abîmées (`containingT5`, `J9512`) qui demandaient `derived`, et UN CAS QUI OUVRE UNE QUESTION : lou-2019 porte -3.02 contre une source où le NOMBRE LUI-MÊME est mangé (`?3 . 02`). `D16` exige que la valeur soit dans la chaîne qui fait foi, précisément pour qu'une réparation ne serve pas à loger un chiffre inventé ; mais quand l'extraction détruit le chiffre, un négatif légitime devient inexprimable autrement que par `derived`. Noté, non tranché. AUCUNE FICHE RETOUCHÉE À LA MAIN (`G3`) |
| 2026-09-22 | `extraction` | 14 EXTRACTIONS LANCÉES, TOUTES COUPÉES PAR UNE LIMITE DE SESSION (429) — mais 6 agents avaient déjà écrit leur fiche avant d'être tués, AUCUN n'avait pu s'auto-vérifier. Les 10 fiches du dépôt ont donc été jugées ici, une par une | RÉSULTAT : 5 VERTES sur 10 (les 3 références + Patton & Sheppard + Lucca & Moench), 5 refusées. ET LE JUGE LUI-MÊME AVAIT DEUX DÉFAUTS, trouvés en l'utilisant. (1) IL PLANTAIT : `UnicodeEncodeError` sur une ligature ou un signe moins venu du PDF, la console Windows étant en cp1252 — deux fiches ne rendaient AUCUN verdict, traceback à la place. Un juge qui plante ne juge pas ; sortie rendue increvable (remplacement À L'AFFICHAGE seulement, la comparaison ayant lieu bien avant sur le texte en mémoire). J'avais moi-même contourné ce plantage plus tôt dans la session avec `PYTHONIOENCODING`, en le prenant pour une gêne locale au lieu d'un défaut du juge — c'est exactement la vigilance déguisée en architecture que le projet refuse. (2) `value_in_quote` REJETTE À TORT TOUT NOMBRE NÉGATIF : `F1` importe la fonction du CATALOGUE, dont le motif est `\d+(?:\.\d+)?` SANS SIGNE, tandis que `F3` a la sienne, `-?\d+(?:[.,]\d+)?`. DEUX IMPLÉMENTATIONS D'UNE MÊME RÈGLE, et elles divergent : sur les 10 fautes de `F1` relevées, 5 SONT DE FAUX REJETS, tous sur un nombre négatif, et DEUX FICHES (kurov, zarattini) ne sont refusées QUE pour cette raison. Dans cette littérature un coefficient négatif est la règle. NON CORRIGÉ, DÉLIBÉRÉMENT : la fonction est celle de `D09`, partagée avec le catalogue et `check_provenance`, et la changer en fin de session sous limite de débit sans pouvoir rejouer leurs gardes serait franchir une porte « provisoirement ». Noté comme prochaine action. (3) TROISIÈME CONSTAT, sur les extracteurs cette fois : 4 SUR 6 ONT FAIT LA MÊME FAUTE — `signal_construction` écrit comme objet structuré sans la clé `value` exigée. Quatre fois la même erreur par quatre sessions indépendantes n'est pas quatre erreurs, c'est un défaut du schéma ou de la consigne. AUCUNE FICHE N'A ÉTÉ RETOUCHÉE À LA MAIN : `G3` de `D17` l'interdit, une sortie d'extracteur se REFAIT, elle ne se répare pas. État de la porte : `G1` non tenu (8 papiers non fichés), `G2` non tenu (5 fiches cassent `D16`). Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e) |
| 2026-09-22 | `lecon` | L20 ECRITE — « Verifier qu'un PDF est arrive ne verifie pas que c'est le bon papier ». LE MOISSONNEUR A TROUVE UNE FAUTE QUI N'ETAIT PAS LA SIENNE, des son premier passage : `corpus/pdf/gao-2018-market-intraday-momentum.pdf`, que `acquisition.json` declare comme Gao, Han, Li & Zhou (2018) « Market intraday momentum » (JFE 129(2):394-414), est en realite **Limkriangkrai, Chai & Zheng (2023), « Market intraday momentum: APAC evidence », Pacific-Basin Finance Journal 80:102086** — treize pages, une autre revue, d'autres auteurs, cinq ans d'ecart | CE QUI L'A ATTRAPEE EST UNE COLLISION D'EMPREINTE `sha256` entre deux affirmations independantes sur LES MEMES OCTETS : le moissonneur dedoublonne par empreinte, et le PDF servi pour le travail OpenAlex « APAC evidence » etait le meme fichier que celui enregistre sous le nom de Gao. Deux sources, deux noms, un seul fichier : au moins l'une a tort. LES DEUX VERIFICATIONS AUTOMATIQUES EVIDENTES ECHOUENT TOUTES LES DEUX, et je les ai ecrites et vues echouer (F52) : le titre attendu est une SOUS-CHAINE du titre reel (« Market intraday momentum » dans « ... : APAC evidence »), et le papier APAC CITE Gao et al. (2018) des son resume, donc auteur ET annee sont presents. Un papier ressemble a un autre papier et le nom du bon apparait dans le mauvais — c'est la regle en litterature academique, ou l'on cite ce qu'on prolonge. CE QUE LA CHAINE AURAIT VALIDE : l'entree 1 n'est pas encore fichee, mais si elle l'avait ete, `F2` ET `F4` auraient ete VERTES — les citations existent bien dans ce texte-la, le PDF designe existe bien — et le garde le plus strict du projet aurait valide une fiche sur le mauvais papier sans une faute a signaler. Meme forme que `L18` : l'erreur qui passe la porte. ARTEFACT VERSIONNE DEJA FAUX : `corpus/text/gao-2018-*.txt`, le texte qui FAIT FOI au sens de `D18`, est celui du papier APAC sous le nom de Gao, et il est commite ; il a traverse `D17`, `D18`, `D19` et deux gardes sans etre vu. Aucune des 4 fiches ne s'en sert, donc rien en aval n'est contamine. NON CORRIGE, delibarement : reparer demande de retrouver le vrai Gao 2018, corriger `ALTERNATES`, re-sonder, re-telecharger et REGENERER le texte `D18` — un acte distinct, et on ne retouche pas un recensement en passant. Inscrit en ALERTE dans `ETAT.md`, a faire avant de ficher l'entree 1. CE QUE CA GENERALISE : une preuve repond a LA QUESTION QU'ELLE POSE et jamais a celle qu'on croit poser ; devant un garde, demander non pas « que verifie-t-il ? » mais « qu'est-ce qui passerait quand meme ? ». Le seul controle qui a marche est REDONDANT PAR CONSTRUCTION — deux sources independantes nommant le meme objet, comparees — meme motif que la seconde implementation de la porte 03 et que `L12`. `LECONS.md` : 19 -> 20 lecons |
| 2026-09-22 | `decision` | D20 ECRITE ET LE MOISSONNEUR CONSTRUIT — `corpus/harvest.py` (`--search` / `--probe` / `--reverdict` / `--fetch` / `--report`) et son garde `corpus/check_harvest.py`, **16 verifications**. Le moissonneur RATISSE ET NE JUGE PAS : requete de six familles reprises des sections A-F d'`AMORCE.md`, ECRITE DANS D20 AVANT D'ETRE LANCEE, contrainte aux sous-champs OpenAlex 2002/2003, triee par citations, plafonnee a 25 par famille. Critere de preuve IMPORTE de `probe_acquisition.py`, jamais recopie. Passage 1 : **132 candidats, 43 PDF, 0 echec** | L'OPTION ECARTEE EST LA DANGEREUSE (F50) : loger le filtre de pertinence DANS le moissonneur fusionnerait moissonnage et TRIAGE — lequel est la moitie de la porte 07 et possede deja juge et etalon — et ecarterait des papiers sans que rien ne mesure ce qu'il ecarte A TORT (`L05`). Le filtre est donc la REQUETE, pre-enregistree ; le jugement reste au trieur. CONSEQUENCE ASSUMEE ET VISIBLE DANS LES RESULTATS : la moisson ramene « Medicaid and Mortality » et « The Purchasing Power Parity Debate ». C'est le fonctionnement CORRECT — un moissonneur qui ne ramenerait que de l'implementable aurait trie en cachette, et le trieur n'aurait plus rien a ecarter. LE MOISSONNEUR NE CONTIENT AUCUNE IA, et c'est ecrit : chercher, resoudre une URL, verifier qu'un octet est `%PDF-` ne demande aucun jugement ; l'IA vient APRES (trieur, puis extracteur). SONDE AVANT D'ECRIRE UNE LIGNE, et elle a servi : OpenAlex rend `oa_status=bronze` avec un `pdf_url` pointant vers SCIENCEDIRECT — une annonce de PDF libre n'est pas un PDF libre, toute URL est sondee. Et le filtre de domaine a du etre trouve par essais (`fields/20`, pas 2002) : sans lui « overnight » ramene la litterature medicale, famille B passant de 999 a 14 833 travaux. ERREUR D'ETIQUETAGE TROUVEE ET CORRIGEE DANS LE PASSAGE MEME (F51) : tester le code HTTP AVANT l'hote faisait sortir 64 entrees sur 65 en `refus_robot`, alors que 56 des 67 tentatives refusees venaient d'hotes d'EDITEURS (Wiley 27, ScienceDirect 14, OUP 8, AEA 4) ; l'ordre corrige rend 55 `peage` / 10 `refus_robot`, et les 10 restants sont bien des depots. La liste close de `D17` N'A PAS ete elargie (`L18`, deuxieme fois) et `refused_by` inscrit hote et code pour que la raison soit VERIFIABLE. La correction n'a coute AUCUNE requete reseau : `--reverdict` relit les tentatives deja enregistrees. RENDEMENT 34 % (43/127), sous la cible de 50-100, cause connue et reparable — `HARVEST_MAILTO` non renseigne, donc Unpaywall pas interroge du tout ; l'adresse n'est PAS ecrite en dur (donnee personnelle envoyee a un tiers), elle est documentee dans `.env.example`. `harvest.json` N'ENTRE PAS DANS G1-G4 : `D20` DATE `F47` au lieu de la rouvrir. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13 |
| 2026-09-22 | `decision` | D19 ÉCRITE — LA VERSION DE L'EXTRACTEUR DE TEXTE EST ÉPINGLÉE. `D18` avait fixé QUELLES extractions font foi, pas AVEC QUELLE VERSION de `pypdf`. `uv.lock` portait 6.19.0 depuis le 2026-09-20 ; le texte qui fait foi a été produit le 2026-09-21 avec **6.14.2**, par un environnement EN RETARD SUR LE VERROU COMMITÉ. `pypdf==6.14.2` dans `pyproject.toml` ; en changer est une décision écrite qui régénère les 36 fichiers et re-vérifie `F2` sur TOUTES les fiches | LE GARDE DE `D18` A FONCTIONNÉ EXACTEMENT COMME PRÉVU — elle avait écrit « la montée de version peut périmer les `quoted_source`, le rejeu de `--check` le dira », et il l'a dit, bruyamment, sur 31 fichiers. Ce qui manquait n'était pas le garde mais qu'une version soit FIXÉE plutôt que seulement INSCRITE : le manifeste notait fidèlement `"pypdf": "6.14.2"`, et NOTER N'EST PAS CONTRAINDRE. DEUX CAUSES SÉPARÉES AVANT DE TRANCHER, les 15 PDF venant d'être repris le matin même : une divergence pouvait venir du FICHIER autant que de la VERSION, et conclure d'emblée aurait été une conclusion non mesurée. Le même corpus ré-extrait sous 6.14.2 dans un environnement jetable rend **36 sur 36 conformes** — la version était seule en cause, ET AU PASSAGE la preuve est faite que les PDF repris sont identiques à ceux du 21. LA MESURE A RETOURNÉ L'INTUITION : 6.19.0 récupère +0,05 % de contenu en mode `default` et +0,66 % en `layout`, mais DÉGRADE DE 12,0 % les lettres orphelines en `layout` (11 576 -> 12 966) — le symptôme même de `L18`. Ni meilleure ni pire ; le choix s'est donc décidé sur le COÛT (une ligne contre 36 fichiers régénérés), pas sur la qualité. ET CE QUI COMPTE POUR PLUS TARD : sous 6.19.0, AUCUNE des 47 citations des 4 fiches ne casse (F2 rend 0 faute des deux côtés), donc l'épinglage n'est pas un mur. Options écartées : rendre la comparaison d'empreintes CONDITIONNELLE à la version (F48 — transformer un garde en commentaire, quatrième fois que cette raison sert après F15/F16/F25) et tenir une version récente pour meilleure (F49). `uv lock` n'a déplacé QUE `pypdf` : numpy, pandas, scipy, pyarrow inchangés, donc aucun résultat de harnais concerné — les six portes rejouées vertes après coup. `LECONS.md` : 18 -> 19 leçons (L19, « un verrou de dépendances commité ne garantit pas l'environnement qui a tourné »). counted_tests **56**, harnais 9ac3e45ed8413e13 |
| 2026-09-22 | `audit` | TOUT CE QUI EST EXÉCUTABLE A ÉTÉ LANCÉ — six portes (01 à 06), les gardes du corpus et du catalogue, `check_provenance`/`check_signals`/`check_heston`/`check_mesfin_premise`, le lint du wiki, `ruff check`. Tout ce qui devait passer passait, À TROIS EXCEPTIONS, et les trois tenaient à la même cause de fond : un fait vrai d'un poste écrit comme un fait du dépôt | (1) **15 PDF SUR 18 ABSENTS** du disque alors qu'`ETAT.md` les annonçait présents — TROISIÈME péremption du même énoncé, après les 2026-09-18 et 09-20, et cette fois dans le sens « annoncés présents, absents ». Repris par `corpus/fetch_pdfs.py` : 15 pris, **0 échec**, 18/18 vérifiés — donc AUCUNE SOURCE MORTE en un jour, et `acquisition.json` tient. (2) CONSÉQUENCE DIRECTE : la fiche Patton & Sheppard, déclarée verte au passage 1 du 2026-09-21, ÉCHOUAIT `F4` ici — F1/F2/F3 tenaient (le texte est versionné), seul le PDF manquait ; revenue verte sans qu'elle soit touchée. (3) `extract_text.py --check` : **31 fichiers sur 36 divergents**, voir l'entrée `decision` suivante. CORRECTIF ÉCRIT DANS `ETAT.md` PLUTÔT QUE LE CHIFFRE CORRIGÉ UNE QUATRIÈME FOIS : il est désormais interdit d'y écrire combien de PDF sont sur le disque, et ce qui est inscrit à la place est le fait qui NE se périme pas — les 18 sont re-téléchargeables, prouvé le 2026-09-22. `ruff check` : 11 erreurs, toutes dans `scripts/`, inchangées et non corrigées (hors du geste demandé). LE PIÈGE DU FORMATEUR EST TOUJOURS ARMÉ : `ruff format --check harness/` dit « 4 files would be reformatted » — le lancer périmerait les 56 tests comptés. Harnais intouché (9ac3e45ed8413e13), counted_tests **56**, registre 135 -> 145 lignes, toutes des calibrations de portes |

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
