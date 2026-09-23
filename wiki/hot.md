---
type: hub
updated: 2026-09-23
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-23.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 08 — le codeur de signal |
| **Dernière porte franchie** | **07**, le 2026-09-23 — les quatre effectifs de `D17` à zéro, mesurés par `scripts/gate_07.py` (**relancer, ne pas recopier** — `L21`). **17 fiches, 450 résultats cités**, produites par **sept sessions |
| **Décision la plus récente** | `decisions/DECISION-24-atteignable-et-fichable.md` — *atteignable* et *fichable* sont deux choses. Le premier dit ce que le monde nous consent, le |
| **Tests au registre** | 160 |
| **Idées abandonnées recensées** | 54 |
| **Entrées au journal** | 53 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action — reflet de `ETAT.md`

**LA PORTE 07 EST FRANCHIE. LA PHASE 08 EST OUVERTE, ET SON JUGE EXISTE DÉJÀ.**

`D23` a écrit le seuil du codeur avant que le codeur existe, et
`scripts/score_signal.py` le tient — 25 vérifications, une faute fabriquée par
condition. **Ce qui manque est l'accusé** : `code_signal.py`, la session qui
reçoit une fiche et rend un module de signal.

Il a maintenant de quoi travailler : **17 fiches** là où il y en avait 10 ce
matin.

### Ce que la phase 08 demande, dans l'ordre

1. ~~Le harnais du codeur.~~ **Fait le 2026-09-23 : `scripts/code_signal.py`** —
   à côté de son juge, comme `extract_fiche.py` est à côté du sien.
   `--prepare` écrit la consigne, `--record` fige l'état de production pour
   `S6`, `--judge` appelle `score_signal.py`. **Le codeur ne voit ni `signals/`,
   qui contient trois implémentations écrites à la main, ni `hypotheses/`, qui
   contient les réponses attendues** — même parade que pour le trieur et
   l'extracteur. Il voit en revanche **l'interface** de `signals/_common.py`,
   résumée à la main et non recopiée : lui refuser l'outillage partagé
   l'obligerait à réécrire une mécanique d'horloge dont `S5` lui compterait
   ensuite les constantes.
2. **`signals/PRODUCED.json`** — sans lui, `S6` est `sans objet` exactement comme
   `G3` l'était ce matin, et la porte 08 ne peut pas se franchir. `L22`.
3. **Le premier signal produit**, jugé sur les six conditions.

### Ce que la phase 08 ne demande PAS, et qu'il faut se retenir de faire

**Aucun IC.** `D23` § Pourquoi : juger un codeur sur son IC le sélectionnerait
sur son résultat, et surtout le nombre de tests est la seule chose que la phase
15 ne peut pas recalculer. Un IC dépensé pour savoir si du code compile est perdu
pour toujours.

### Ce qui reste dû par ailleurs, et qui n'a pas bougé

| Point | Pourquoi ça compte |
|---|---|
| **Frais CME / EUREX, multiplicateurs** — tous `null` | tant qu'ils le sont, `harness/costs.py` ne rend qu'un **plancher étiqueté**, donc tout IC net est un **majorant de performance** |
| **`slippage_bp` à déclarer** | même famille |
| **`scripts/gate_06_controls.py` ÉCRIT au registre** — une ligne de calibration par passage (`porte-06-cellule-morte`, `hypothesis_ref: null`) | Légitime : le registre est append-only et `counted_tests` ne bouge pas, une calibration n'étant pas un test. Mais **le passer dans une revue de gardes n'est pas gratuit** — `registry/tests.jsonl` est irremplaçable, et il a gagné une ligne le 2026-09-23 pour cette seule raison. Les autres gardes (`gate_07`, `score_*`, `validate_*`, `check_*`) n'écrivent rien |
| **`ruff format harness/`** reformaterait 4 fichiers | le harnais est **figé et versionné** ; le reformater changerait son empreinte et **périmerait les 56 tests comptés**. Ne pas lancer |
| **Le texte qui fait foi pour le HTML** | `D24` § Ce qui reste ouvert. Si `D18` s'étend au HTML, l'entrée 9 redevient fichable, `G1` repasse à 1, et **la porte 07 est réputée non franchie jusqu'à ce qu'elle soit fichée** |

---

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
| 2026-09-23 | `decision` | **D24 ECRITE ET LA PORTE 07 FRANCHIE.** *Atteignable* et *fichable* sont deux choses : le premier dit ce que le monde nous consent, le second ce que NOTRE OUTILLAGE sait traiter. `G1` ne compte que les fichables. Les quatre effectifs tombent a zero : **G1 = G2 = G3 = G4 = 0**, 17 fiches, 450 resultats cites | LE POINT QUI BLOQUAIT NE SE TRANCHAIT PAS EN PROGRAMMANT, et c'est pour ca qu'il a fallu une decision. L'entree 9 — billet HTML de la Fed de New York — est `atteignable` (obtenue sans peage, donc `D17` la compte) ET infichable (`F4` exige un `source.pdf`, `D18` ne traite que les PDF). Ni lecture n'etait fautive. Les deux options ecartees sont ecrites dans `D24` : etendre `D18` au HTML ouvrait un chantier disproportionne a un seul billet (quel extracteur, fige a quelle version, et un billet n'a ni pages ni sections, deux choses que `D18` tient pour acquises) ; laisser l'entree bloquer la porte mesurait autre chose que ce qu'on voulait mesurer, la porte 07 jugeant UN EXTRACTEUR et non un inventaire. Une quatrieme option est ecrite bien qu'evidemment mauvaise, parce qu'elle est la tentation : retirer l'entree 9 du recensement — un papier qu'on efface parce qu'il gene un compteur est exactement ce que `G4` existe pour empecher. CE QUE LA DECISION COUTE, ET C'EST ECRIT AU § POURQUOI : `G1 = 0` ne veut plus dire « tout ce qu'on peut obtenir est fiche » mais « tout ce qu'on sait lire est fiche ». La porte devient franchissable EN N'AMELIORANT PAS L'OUTILLAGE. La parade est que le non-fichable ne disparaisse pas — il est compte, nomme, et sa raison ecrite dans sa propre colonne, `gate_07.py` la refusant si elle manque. Et si `D18` s'etend un jour au HTML, l'entree 9 redevient fichable, `G1` repasse a 1, et **la porte 07 est reputee non franchie jusqu'a ce qu'elle soit fichee** : ecrit dans `D24` pour que personne ne le redecouvre. LA CAUSE PROFONDE DU DESACCORD EST INSTRUCTIVE : `extract_fiche.py --list` et `gate_07.py` REDEDUISAIENT chacun de son cote ce qu'etait un papier traitable, l'un par `text_format != pdf`, l'autre par `status`. Deux deductions paralleles de la meme chose finissent toujours par differer. Desormais `corpus/acquisition.json` porte `fichable` et les deux le LISENT. ETAT.md passe en phase 08, dont le juge (`score_signal.py`, `D23`) existe deja et dont l'accuse (`code_signal.py`) manque — avec `signals/PRODUCED.json`, sans lequel `S6` sera `sans objet` exactement comme `G3` l'etait ce matin (`L22`). Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13 |
| 2026-09-23 | `outil` | LA PORTE 07 TIENT A UN SEUL POINT, ET CE POINT EST UNE DECISION. `scripts/gate_07.py` compte les quatre effectifs, qui n'avaient AUCUN compteur la ou les portes 01 a 06 en ont chacune un. Mesure : **G1 = 1, G2 = 0, G3 = 0, G4 = 0**. Le corpus passe de 10 a **17 fiches, 450 resultats cites**, produites par SEPT SESSIONS SEPAREES qui n'ont vu que leur consigne (`D16` § Qui peut etre l'extracteur) | `G3` ETAIT INMESURABLE, ET C'EST CE QUI MANQUAIT VRAIMENT. La condition la plus dure de `D17` — « aucune fiche retouchee a la main apres production » — n'avait aucun registre d'etat d'origine : rien ne permettait de savoir si une fiche avait bouge. `corpus/PRODUCED.json` l'etablit, sur le patron de `signals/PRODUCED.json` pour `S6` de `D23`. Empreinte OCTET POUR OCTET et non JSON normalise : une reindentation EST une retouche, et normaliser avant de hacher laisserait passer exactement le geste qu'on compte. `--judge` refuse desormais une fiche qui a bouge depuis sa production, sans quoi une session pourrait corriger, rejuger, voir du vert, et croire la porte franchie alors que `G3` vient de casser. UNE REPRODUCTION N'EST PAS UNE RETOUCHE, et les confondre fausse `G3` DANS LES DEUX SENS : quand l'extracteur repasse sur sa propre sortie apres un verdict rouge, rien n'a ete repare a la main. Deux fiches ont casse sur un point de schema — `signal_construction.value` absent chez Baltussen, `what_is_missing` qui n'etait pas une liste chez Zarattini — et elles ont ete RENVOYEES A LEUR EXTRACTEUR plutot que reparees par moi ; les reparer aurait ete precisement la faute que `G3` existe pour compter. Mais le NOMBRE D'ESSAIS est lui-meme un resultat, donc chaque passage est inscrit et la porte l'imprime : **9 essais pour 7 fiches, 1,29 par fiche**. « Produit sans retouche » au cinquieme essai ne dit pas la meme chose qu'au premier, et une porte qui tait ce nombre laisse croire a une precision qu'elle n'a pas mesuree. LE SEUL POINT RESTANT NE SE TRANCHE PAS EN PROGRAMMANT : l'entree 9 est un billet HTML de la Fed de New York, `atteignable` pour `D17` (obtenu sans peage) et INFICHABLE pour `F4` (qui exige un `source.pdf`, et `D18` ne traite que les PDF). `extract_fiche.py --list` l'ecarte et annonce `G1 = 0` ; `gate_07.py`, lecture litterale de `D17`, annonce 1. Le compteur IMPRIME LES DEUX LECTURES et retient la plus exigeante, au lieu d'en choisir une en silence. Trois issues, toutes defendables : etendre `D18` au HTML, distinguer *atteignable* de *fichable* dans `D17`, ou assumer par ecrit qu'un billet de blog bloque une phase entiere. CE QUE LES EXTRACTEURS ONT TROUVE ET QUE JE N'AURAIS PAS VU : Gorton 2013 definit son seuil de stocks par un filtre Hodrick-Prescott BILATERAL calcule sur l'echantillon complet — look-ahead structurel, invariant II — et les auteurs reconnaissent ne pas controler le delai de publication des stocks ; la correlation entre leurs portefeuilles High Basis et High Momentum vaut **0,87**, donc base et momentum 12 mois ne sont pas deux paris independants. Boyarchenko 2023 : Sharpe 1,1 avant couts, **-0,5 apres spread**. Koijen 2018 sur matieres premieres — la classe la plus proche de nos neuf futures — donne `c = 0,01` avec `t = 0,13`. Trois papiers sur sept portent un conflit d'annee entre le `fiche_id` et le texte (working papers NBER), signale dans `source.note` plutot que masque. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13 |
| 2026-09-23 | `mesure` | `G1` ET `G2` RELANCES PLUTOT QUE RECOPIES, a la question « c'est quoi G1 et G2 ». **`G2` = 3**, conforme a `ETAT.md` (Andersen 2003, Corsi 2009, Lou 2019). **`G1` = 8, la ou `ETAT.md` annoncait 7** ; le recensement vaut **18 atteignables sur 20 (17 PDF, 1 HTML)**, la ou `ETAT.md` annoncait 19 et 18. Trois chiffres corriges a la source. Nouvelle lecon **`L21`** | L'ENTREE 9 MANQUAIT AU COMPTE, ET LA RAISON VAUT D'ETRE PAYEE UNE SEULE FOIS : le rapprochement entre « atteignables » et « fiches produites » se fait par NOM DE PDF, et l'entree 9 — un billet HTML de la Fed de New York — n'en a pas (`pdf: null`). La cle du rapprochement excluait SILENCIEUSEMENT le seul element qui ne la possede pas, c'est-a-dire exactement celui dont l'absence etait le sujet. Aucune erreur levee, et l'ecart va du cote qui arrange. Le controle qui l'attrape est de compter la POPULATION ENTIERE et de verifier que les deux moities la reconstituent (`atteignables = fiches + non fiches`), pas de compter les non fiches directement. Le « 19 sur 20, 18 PDF » datait du recensement du 2026-09-21 et etait reste ecrit apres que `L20` a fait basculer l'entree 1 en `inatteignable` le 2026-09-22. L'entree 9 est de surcroit INFICHABLE EN L'ETAT — `F4` exige un `source.pdf` et `D18` ne traite que les PDF, ce que `D18` laisse ouvert a son § Ce qui reste ouvert — mais elle compte dans `G1` quand meme : une condition qu'on n'a pas les moyens de tenir reste non tenue. AU PASSAGE, UNE ERREUR DE MA PART QUI A FAILLI DEVENIR UN FAIT : j'ai d'abord compte `G2 = 4`, heston cassant `F2`, en passant le fichier `.default.txt` en argument au juge. Or `D18` fait foi sur l'UNION des deux extractions, et `score_extraction.py` la resout LUI-MEME depuis la fiche — l'argument texte n'existe que pour les essais et imprime « hors D18, le verdict ne fait pas foi ». J'avais ignore l'avertissement que le juge imprimait. Relance correctement : heston est VERTE, `G2 = 3`. TROISIEME CONSTAT : `G1`–`G4` n'ont AUCUN COMPTEUR UNIQUE — pas de `scripts/gate_07.py`, la ou les portes 01 a 06 en ont un. Un effectif sans script est un effectif qu'on recopie, et c'est la troisieme fois qu'un chiffre de `ETAT.md` se revele faux en le mesurant. Ce que les 3 fiches rouges cassent, pour memoire : `signal_construction.value absent` sur les trois (schema), et des valeurs introuvables dans leur citation parce que l'EXTRACTION DU PDF les abime — « −3 . 02% » avec des espaces autour du point, « containingT5 » pour 496512. **`F2` tient sur les dix fiches : aucune citation inventee.** Aucun IC, aucun test depense : counted_tests **56** |
| 2026-09-23 | `outil` | LE JUGE DE LA PORTE 08 EST ECRIT — `scripts/score_signal.py`, **25 verifications**, refuse chacune des six fautes de `D23` sur des signaux fabriques. Il accepte un CHEMIN comme un nom pointe. **AUCUN IC N'EST CALCULE**, et le rendu l'imprime | `S5` A ETE MESUREE SUR LES CAS REELS, PAS SUPPOSEE, et elle s'est reveleee VIDE deux fois de suite avant d'etre reparee. (1) Elle signalait `signals/_common.py:74` pour le `24` de `(end_minutes - minutes) % (24 * 60)`. La cause n'etait PAS la liste close mais le PERIMETRE — `_common.py` est du depot, ecrit a la main, pas la sortie du codeur — d'ou `MODULES_DU_DEPOT`, et non un `24` ajoute a `DU_DEPOT` (`L18` : chercher la cause ailleurs avant d'elargir). Le trou apparent, un codeur qui cacherait ses parametres dans un utilitaire partage, est ferme AILLEURS : le codeur produit exactement UN module, et toucher un fichier du depot casse `S6`. (2) PLUS GRAVE — `S5` passait contre N'IMPORTE QUELLE FICHE. Mesure : une fiche entiere porte **41 a 194 nombres distincts** (`reported_results` est plein de t-stats et de tailles d'echantillon qui ne parametrent aucun code) contre **2 a 25** pour `signal_construction` ; sur la seule fiche Heston, **19 des 101 entiers de 0 a 100** s'y trouvaient par hasard. Deux corrections : la recherche est bornee a `CHAMPS_RECETTE` (`signal_construction`, `horizon`, `universe`, `cost_model`), et **`30` est RETIRE de `DU_DEPOT`** — il etait exempte comme horizon de grille (`D01` §2) alors qu'il est AUSSI le seul parametre du signal de reference Gao, donc l'exempter rendait invisible exactement ce que `S5` existe pour voir. CE QUE `S5` VAUT VRAIMENT, CHIFFRE : 3 signaux x 10 fiches, elle **refuse 12/30 = 40 %** et laisse passer 60 %, dont les mauvais — le signal Heston passe `S5` contre la fiche Lou 2019. La raison n'est pas reparable et c'est ecrit dans `D23` § Pourquoi : deux papiers d'un meme domaine PARTAGENT leurs parametres, `30` minutes etant la demi-heure de Gao, le decalage de Heston et la fenetre de Patton & Sheppard a la fois. **`S5` est NECESSAIRE, PAS SUFFISANTE** : elle attrape un parametre INVENTE, ce que rien d'autre n'attrapait, et pas un parametre juste pour le mauvais papier. La pousser plus loin la transformerait en verification de PERTINENCE, qui par `D23` n'a pas de juge automatique et attend la phase 09. Deux autres gardes qui tiennent : `nombres_du_texte` compare NUMERIQUEMENT et non par sous-chaine (`F26` s'est fait prendre sur `12500` contre « 12,500,000 »), et `constantes_du_code` passe par `ast`, donc un nombre en commentaire ou en docstring ne justifie RIEN. `D23` gagne un § Journal des calibrations qui inscrit les deux reparations avec leur mesure. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13. RESTE : `code_signal.py` — et `G1`/`G2` de la porte 07 le precedent, un codeur sans fiches n'ayant rien a coder |
| 2026-09-23 | `decision` | D23 ECRITE — LE SEUIL DE LA PORTE 08, avant que le codeur existe, comme `D15` avant le trieur et `D16` avant l'extracteur. Six conditions a tolerance ZERO qui valent ENSEMBLE : `S1` contrat de `D07`, `S2` liste blanche, `S3` causalite, `S4` non-degenerescence et scores tombant sur des barres MESURABLES (`L10`), `S5` **fidelite a la fiche**, `S6` zero retouche manuelle. `scripts/score_signal.py` les verifiera ; il reste a ecrire | CE QUE LA SITUATION A IMPOSE, ET QUI N'ETAIT PAS PREVU : `D06` designait DEUX etalons pour cette porte — Gao (entree 1) et Baltussen (entree 2), implementes a la main — et **AUCUN DES DEUX N'A DE FICHE**. L'entree 1 est devenue INATTEIGNABLE le 2026-09-22 (`L20` : l'URL servait un autre papier, aucune copie libre du vrai Gao 2018 n'existe), l'entree 2 est encore a ficher. Or le codeur prend une FICHE en entree : il ne pourrait donc etre compare a une implementation humaine que sur UN SEUL papier, et `F43` a deja tranche qu'un seuil sur trois items ne distingue pas un automate correct d'un automate chanceux. La corrélation aux etalons devient donc une CALIBRATION inscrite au journal, jamais un seuil — exactement le raisonnement de `D16` face a ses trois fiches. `S5` EST LA CONDITION QUI PORTE LA DECISION, et c'est `F2` transpose au code : un codeur qui ecrit `fenetre = 30` la ou la fiche dit quarante-cinq minutes produit un signal QUI TOURNE, QUI EST CAUSAL, QUI N'EST PAS DEGENERE — et qui ne code pas ce papier ; rien ne l'attraperait. Exiger que chaque constante du code se retrouve dans la fiche ferme ce trou SANS ETALON, et c'est l'interdit constitutionnel applique au code : un parametre absent de la fiche est un parametre invente. Il faudra une liste CLOSE d'echappatoires nommees (constante du catalogue, de `D01`, convention de langage), et l'elargir sera une decision — `L18`. AUCUN IC N'EST CALCULE POUR FRANCHIR CETTE PORTE, et c'est la seconde raison qui compte : juger un codeur sur son IC le selectionnerait sur son RESULTAT (surajustement deguise en ingenierie), mais surtout le nombre de tests est LA SEULE CHOSE QUE LA PHASE 15 NE PEUT PAS RECALCULER — un IC depense pour savoir si du code compile est perdu pour toujours. Meme regle que la clause 1 de la porte 06. CE QUE CE JUGE NE SAURA PAS FAIRE, et c'est ecrit : dire si le signal est LE BON. Un signal fidele a une fiche creuse passerait les six conditions ; la pertinence n'aura de denominateur qu'en phase 09. AU PASSAGE, deux peremptions de `ETAT.md` corrigees en LANCANT les juges plutot qu'en recopiant : `G1` annoncait 8 papiers a ficher, il en reste **7** (entrees 2, 5, 8, 12, 18, 19, 20) ; `G2` annoncait 5 fiches rouges, il y en a **3** — Andersen 2003, Corsi 2009, Lou 2019, toutes sur `F1` et `F3`, **aucune sur `F2`**. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13 |
| 2026-09-23 | `outil` | LA CHAINE EST COMPLETE — PDF -> texte qui fait foi -> morceaux -> VECTEURS -> recherche. Dimension migree de 1536 a **768**, embeddings calcules **localement et gratuitement** par `BAAI/bge-base-en-v1.5` via `fastembed` (ONNX, sans `torch`, 0,21 Go, licence MIT). **17 papiers, 1 594 morceaux, 1 594 vectorises** en 14,4 min a ~1,7 morceaux/s sur processeur. Cout total : 0 EUR, aucune cle, aucun reseau apres le telechargement du modele | POURQUOI 768 ET PAS 1536 : verifie, pas suppose — `fastembed` offre les dimensions [256, 384, 512, 768, 1024] et **aucun modele libre ne fait 1536**, chiffre propre a OpenAI. Le choix etait donc payer une cle ou migrer la colonne ; migrer tant qu'elle etait VIDE ne coutait rien, apres coup il aurait fallu tout recalculer. Effets mesures : un vecteur passe de 6 144 a **3 072 octets**, l'index HNSW ~2x plus leger, la recherche plus rapide. La qualite ne suit PAS la dimension mais l'entrainement : `bge-base-en-v1.5` est entraine pour la RECUPERATION DOCUMENTAIRE la ou `text-embedding-3-small` est generaliste. LA DEMONSTRATION QUI COMPTE, sur le corpus reel : « carry commodity futures roll yield » rend **0 resultat en plein texte** (semantique ET, le papier n'a pas les quatre mots ensemble) et **0.768 sur `Carry` de Koijen en vectoriel** — c'est exactement ce que les embeddings achetent. LIMITE TROUVEE EN TESTANT ET NON SUPPOSEE : le modele est ANGLAIS. Meme question en francais puis en anglais — 0.477 sur le mauvais papier contre **0.733 sur le bon**, 0.565 contre **0.706**. Le corpus etant anglais, il s'interroge en anglais ; un modele multilingue existe en 768 (donc sans migration) mais imposerait de tout recalculer. PIEGE DES PREFIXES `bge`, cable et documente : un PASSAGE et une REQUETE ne s'encodent pas pareil (`Represent this sentence for searching relevant passages: `), et les confondre degrade la recuperation SANS RIEN CASSER DE VISIBLE. LE TEST A CASSE DEUX FOIS POUR LA MEME RAISON DE FOND — il se croyait proprietaire de la base : d'abord le plein texte touchait des morceaux reels, puis ses 4 vecteurs aleatoires ont cesse de remonter parmi 1 594 morceaux tous vectorises. Ses 14 assertions sont desormais bornees a ses propres papiers, avec un `match_count` assez large pour les contenir. `fastembed` ajoute a `pyproject.toml` : 28 paquets, **aucun torch**, et **pypdf reste a 6.14.2** (`D19`) — verifie. Gardes verts : test_vector_db **36/36**, `extract_text --check` conforme, `ruff` propre sur vectordb/ et corpus/. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13. RESTE OUVERT : les 123 PDF moissonnes, dont le texte n'est pas versionne — ce serait une decision au sens de `D18` |
| 2026-09-22 | `outil` | LA BASE VECTORIELLE EST BRANCHEE SUR LE CORPUS — `vectordb/` : migration PostgreSQL+pgvector (3 tables, 3 fonctions de recherche, HNSW cosinus, GIN plein texte, RLS en refus par defaut), client `vector_db.py`, `setup_env.py`, `ingest.py`, et un test de bout en bout a **36 verifications**. Migre et teste sur Supabase reel (PostgreSQL 17.6, pgvector 0.8.2) ET sur un PostgreSQL local jetable (16.2, pgvector 0.6.2). **17 papiers, 1 594 morceaux ingeres**, embeddings laisses a NULL | TROIS DEFAUTS TROUVES EN EXECUTANT, qu'aucune analyse statique n'aurait vus. (1) L'API PARLAIT DEUX LANGUES : `insert_paper` rendait `str`, les recherches `uuid.UUID`, donc `row['paper_id'] == paper_id` valait **False en silence** ; corrige a la source, les trois recherches normalisent. (2) LE PLUS GRAVE — en mode non-autocommit, la PREMIERE LECTURE ouvre une transaction implicite, et le `conn.transaction()` qui suit n'est plus qu'un SAVEPOINT. Comme `insert_paper` commence par `find_existing_paper`, **toutes les ecritures devenaient des savepoints d'une transaction jamais validee**, annulee au `close()` : l'ingestion annoncait quatre papiers inseres, la base en contenait ZERO. Le test ne pouvait pas le voir — il relisait sur la MEME connexion, qui voit ses propres ecritures non validees. Corrige par `autocommit=True`, et une verification AJOUTEE au test : relire depuis une SECONDE connexion. Une ecriture n'est ecrite que lorsqu'un AUTRE la voit. (3) `pypdf` produit des octets NUL (10 sur 17 papiers) que PostgreSQL refuse dans un champ texte ; retires de la COPIE de recherche, comptes et annonces, `corpus/text/` intouche. LES PAGES SONT RECONSTRUITES PUIS VERIFIEES : `corpus/text/` recolle les pages avec `\n` et perd leurs frontieres, donc l'ingestion re-extrait page par page sous le `pypdf` epingle par `D19` et EXIGE que le recollage redonne exactement le fichier qui fait foi — sinon elle s'arrete, une pagination approximative placant les citations sur les mauvaises pages (`L20`). Verifie sur les 17. LA SECTION EST UNE HEURISTIQUE FAIBLE, ET C'EST DIT : deux en-tetes trouves sur les 98 pages de Boyarchenko, aucun sur Andersen 2003 dont l'extraction ecrase les espaces. Deux garde-fous : sous deux sections distinctes le papier reste entierement `other`, et ce qui SUIT la conclusion redevient `other` (sans quoi 101 morceaux sur 171 etaient `conclusion`, annexes comprises). `psycopg` ajoute a `pyproject.toml` — verifie que le verrou ne deplace QUE lui et que **pypdf reste a 6.14.2** (`D19`), `extract_text --check` vert apres coup. Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13. RESTE : les embeddings (aucune cle, aucun modele choisi) et les 123 PDF moissonnes, dont le texte n'est pas versionne — ce serait une decision au sens de `D18` |
| 2026-09-22 | `moisson` | PASSAGE 2 DU MOISSONNEUR — **319 candidats, 123 PDF, 0 echec, 147 Mo**. Plafond porte de 25 a 60 par famille, par un amendement ECRIT au § Journal de `D20` AVANT d'etre applique. Le moissonnage devient INCREMENTAL : `--search` ajoute au lieu de remplacer, les 132 candidats du passage 1 gardent statut, preuve et date de constat | LA REVISION EST LICITE ET LA RAISON EST ECRITE : la recherche, le domaine, la fenetre de dates et le tri ne bougent PAS, donc les 25 premiers de chaque famille sont le PREFIXE EXACT des 60 premiers et rien n'est re-selectionne en voyant ce que le passage 1 a rendu. L'interdit de `D20` vise le choix qu'on referait EN VOYANT LE RESULTAT — changer un mot-cle parce que la moisson deplait ; creuser plus profond dans une liste figee et changer la liste sont deux gestes differents, et seul le second est un bouton. Le plafond decide COMBIEN on regarde, les mots-cles decident LESQUELS peuvent apparaitre. RESULTAT : la cible de 50-100 est depassee, et le rendement monte de 34 % a 39 % (123 sur 314 sondes) sans qu'aucun critere ait change — simple effet de la profondeur. Famille A EPUISEE : 60 pris sur 90 libres, 28 PDF ; famille E la plus pauvre (11 PDF sur 43), `carry trade` et `commodity futures` etant largement publies chez des editeurs payants. Refus : 110 `peage`, 53 `sans_source_libre`, 28 `refus_robot` — le peage domine, coherent avec la finance academique. UN `429` A CASSE LE PREMIER ESSAI : sans `HARVEST_MAILTO` les requetes passent par le pool COMMUN d'OpenAlex, qui limite plus tot ; 0,25 s entre appels suffisait au plafond de 25, pas a celui de 60. Repare par un RECUL PROGRESSIF (5, 10, 20, 40 s, puis abandon borne) et une pause portee a 1,5 s — la reponse juste a un `429` est de RALENTIR, c'est l'inverse d'un contournement : le serveur dit « trop vite », on obeit. TROU DU GARDE TROUVE EN FAISANT LE CHANGEMENT : `check_harvest` comparait le plafond A LUI-MEME — le JSON declarait son propre `per_family` et `H9` verifiait qu'il le respectait, donc un `--per-family 500` passait sans un mot ; `H1` le compare desormais a la valeur declaree dans le code, qui est la copie de travail de `D20`. Garde : 16 -> **17 verifications**. RESTE SUR LA TABLE : `HARVEST_MAILTO` toujours pas renseigne, donc Unpaywall JAMAIS interroge — seul levier connu restant, et il appartient a l'utilisateur, l'adresse etant une donnee personnelle envoyee a un tiers. Gardes verts : check_harvest 17/17, check_acquisition 11/11, extract_text --check 34 fichiers sous pypdf 6.14.2, ruff corpus/ propre. `harvest.json` N'ENTRE PAS DANS G1-G4 (`F47`). Aucun IC, aucun test depense : counted_tests **56**, harnais 9ac3e45ed8413e13 |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 13 |
| `phases` | 8 |
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
