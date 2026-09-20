# D15 — Ce que « le triage écarte ce qu'il doit écarter » veut dire en chiffres

**Date :** 2026-09-19
**Phase :** 07
**État :** prise

## La question

La porte 07 exige que le triage « écarte ce qu'il doit écarter, sur un verdict
humain de référence ». Cette phrase ne se vérifie pas : il faut dire **contre
quoi** le trieur est apparié, **ce qu'il voit** pour décider, et **quel écart**
le fait échouer — le tout écrit avant de coder le trieur, comme `L06` l'exige.

## Les options

### Sur l'étalon

1. **La colonne « implémentable » d'`AMORCE.md` telle qu'elle est.** Retenue.
   Elle porte **20 verdicts** — entrées 1 à 20, sections A à F — répartis en
   **13 `oui`, 5 `partiel`, 2 `non`**. Les entrées 21 à 24 (section G, méthode)
   n'ont pas cette colonne et sortent de l'étalon.

2. **Le § Verdict d'`AMORCE.md`** — « 12 directement implémentables, 5
   partiellement, 3 fermées ». Écartée. Il se contredit avec la colonne sur
   l'**entrée 9** (billet FRBNY, « la dérive nocturne a disparu ») : la colonne
   la marque `oui`, le résumé l'exclut. C'est la colonne que `D14`, `ETAT.md` et
   `wiki/phases/phase-07` désignent depuis le début, c'est l'artefact rempli
   **ligne à ligne** plutôt que résumé de mémoire, et son `oui` se défend au
   fond : l'affirmation « l'effet a disparu » se teste sur nos données, par le
   calcul même de l'entrée 8. Le § Verdict reçoit une note datée de correction,
   comme l'entrée 7 en a reçu une le 2026-09-18.

3. **Retirer l'entrée 9 de l'étalon.** Écartée. Un étalon dont on retire les
   lignes gênantes n'est plus un étalon, et celle-ci n'est pas gênante une fois
   lue.

### Sur la notation

4. **Trois classes, matrice de confusion entière.** Retenue.

5. **Binaire, `partiel` replié sur `oui` ou sur `non`.** Écartée. Replier fait
   disparaître la distinction qui a **écarté Mesfin** de la porte 06 — sa
   métrique ne transpose pas — et qui a **cadré Heston** — seul le motif
   transposait. C'est le champ `transposability` de `D14` sous un autre nom :
   l'effacer du triage serait effacer ce que la phase 06 a payé pour apprendre.

6. **`partiel` hors dénominateur, noté sur 15.** Écartée. Elle ne mesure rien
   sur le seul cas difficile.

### Sur la forme du seuil

7. **Un seuil en pourcentage** — « rappel ≥ 90 % ». Écartée. Sur **13 `oui`**, un
   seul item vaut **7,7 points** de rappel : un seuil en pourcentage est un
   effectif déguisé, et il déguise mal. Il invite en plus à lire un score quand
   `L06` demande de lire des appariements.

8. **Un seuil en effectifs, par classe.** Retenue.

## Le choix

Le trieur est apparié **entrée par entrée** à la colonne « implémentable »
d'`AMORCE.md` (20 entrées, 13 `oui` / 5 `partiel` / 2 `non`), en **trois
classes**, et la porte est franchie si et seulement si les **quatre** conditions
suivantes tiennent, écrites ici avant toute mesure :

| # | Condition | Effectif |
|---|---|---|
| A | `oui` de l'étalon classés autrement | **≤ 1** sur 13 |
| B | `non` de l'étalon classés `oui` | **0** sur 2 |
| C | `partiel` de l'étalon en désaccord | **≤ 2** sur 5 |
| D | désaccords de **deux crans** (`oui` ↔ `non`, dans un sens ou l'autre) | **0** |

Soit **au plus 3 désaccords sur 20**, dont aucun grave. Les quatre valent
ensemble ; trois sur quatre ne franchissent rien (`CLAUDE.md` § Les interdits,
« jamais provisoirement »).

**B est un sous-ensemble de D**, et c'est écrit plutôt que caché : un `non` promu
`oui` est aussi un désaccord de deux crans, donc B ne peut être rompue sans que D
le soit. Les deux restent parce qu'elles **nomment deux coûts distincts** — B
celui d'un signal codé sur une donnée que nous n'avons pas, D celui d'une panne
de lecture — et parce qu'une condition qui se déduit d'une autre ne coûte rien à
vérifier. Une grille de notation dont une case est redondante sans le dire est
une grille qu'on relira mal.

## Pourquoi

**Ce que le trieur voit est la moitié de la question, et elle n'avait pas été
posée.** Le trieur reçoit **la ligne d'`AMORCE.md` privée de sa colonne
verdict** : référence, ce qu'il prédit, fréquence et univers, données exigées,
accès. Ni plus, ni moins — **c'est exactement ce que l'auteur humain avait sous
les yeux** en phase 01. Lui donner le PDF le rendrait mieux informé que son
étalon et l'écart ne mesurerait plus rien ; lui donner moins le condamnerait
d'avance.

Deux conséquences qu'il faut écrire franchement. La première est un **cadeau** :
le triage se construit et se juge **aujourd'hui, sans un seul PDF de plus** — il
ne dépend pas du goulot d'acquisition qui bloque l'autre moitié de la porte. La
seconde est un **aveu** : la colonne « données exigées » contient déjà presque la
réponse pour les entrées 18 et 19 (« au moins la deuxième échéance »). Le trieur
n'accomplit donc pas un exploit ; il applique **nos** contraintes de données à
une description, de façon reproductible. C'est pour cela que le seuil est
**sévère** — un exercice facile mérite une barre haute. La généralisation depuis
un PDF est un autre problème, et c'est la phase 09.

**Pourquoi B est à zéro et A tolère un.** Les deux erreurs ne coûtent pas la même
chose. Un `oui` manqué coûte **un papier non fiché** — récupérable, et visible.
Un `non` promu `oui` coûte un papier lu, une fiche écrite, et au bout de la
chaîne **un signal codé sur une donnée que nous n'avons pas** : l'erreur descend
dans la chaîne au lieu de s'arrêter. `D01` a fermé la famille carry pour cette
raison précise ; un trieur qui la rouvre par distraction défait une décision
écrite.

**Pourquoi D existe séparément.** Un désaccord `partiel`/`oui` est une nuance ; un
désaccord `oui`/`non` est une panne de lecture. Les compter dans le même total
laisserait trois nuances et une panne passer pour le même résultat que quatre
nuances. C'est `L06` appliquée à notre propre grille de notation : **un compte
juste n'est pas un compte de choses justes.**

**Le juge est écrit avant l'accusé, ici aussi.** `corpus/score_triage.py` — qui
apparie, dresse la matrice et rend le verdict — est écrit et vérifié **contre des
sorties fabriquées** avant que le trieur existe. C'est l'ordre de construction de
`CLAUDE.md` appliqué à l'intérieur d'une phase, et c'est ce que `D06` a fait pour
les signaux.

**Le nombre de passages est inscrit, comme un IC.** Un trieur qu'on retouche après
avoir vu sa matrice est un trieur ajusté à son étalon, et l'étalon est brûlé sans
que rien ne le signale. Le **premier passage fait foi**. Tout passage ultérieur
est inscrit au § Journal ci-dessous avec **ce qui a changé entre les deux**, et le
verdict final cite le nombre de passages — de la même façon que la phase 15
citera `counted_tests()`. Un trieur qui passe au quatrième essai est un résultat
différent d'un trieur qui passe au premier, et le lecteur doit pouvoir faire la
différence.

**Ce qu'on sacrifie.** Vingt entrées ne portent aucune statistique : aucun
intervalle de confiance ne sortira d'ici, et il ne faut pas en écrire. Cette
porte vérifie **un accord entrée par entrée sur un petit ensemble connu**, rien
de plus — la même modestie que la calibration à la main de la porte 03. Et
l'étalon lui-même est faillible : il a été écrit en une session, par une personne
seule, sans avoir lu les papiers. Un désaccord peut désigner **le trieur ou
l'étalon**, et le § Journal doit dire lequel, sans jamais corriger l'étalon après
coup.

## Complément du 2026-09-19 — qui peut être le trieur

Écrit le jour même, **avant tout passage**, parce que la mise en œuvre a révélé
une condition que le corps de la décision ne portait pas.

**Une session qui a lu la colonne ne peut pas être le trieur.** Elle ne trierait
pas, elle réciterait — et sa matrice serait parfaite pour la pire des raisons. La
session qui a écrit cette décision est dans ce cas : elle a compté la colonne
entrée par entrée pour en établir le dénominateur. **Elle est donc disqualifiée
comme trieur**, et le dit ici plutôt que de produire un résultat flatteur.

Le piège est structurel, pas accidentel : la séquence de démarrage de `CLAUDE.md`
conduit toute session à lire `ETAT.md`, le wiki, puis le corpus — donc l'étalon.
Une session arrive **contaminée par défaut**.

Trois conséquences, toutes écrites dans `corpus/TRIAGE.md` :

1. Le trieur reçoit **`corpus/triage_input.json`** — fabriqué par
   `corpus/make_triage_input.py`, les 20 lignes privées de leur colonne verdict —
   et **jamais `AMORCE.md`**, qui porte la réponse deux fois : dans la colonne, et
   dans son § Verdict.
2. **Les titres de section ne sont pas repris.** Le titre E dit « Carry et
   structure de terme — *la famille que mes données ferment* » : c'est le verdict
   lui-même, de la même main et du même jour. Le donner rendrait la condition B
   satisfaite d'avance.
3. Le § Journal note, pour chaque passage, **qui a trié et ce qu'il avait vu**.

**Ce n'est pas une impossibilité par construction, et il faut le dire.** On
n'empêche pas un lecteur de lire. `F13`, `F15`, `F16` et `F25` ont toutes écarté
un garde extérieur au motif qu'il déguisait la vigilance en architecture ; ici
l'architecture n'est pas disponible, donc la règle est **écrite et déclarée**
plutôt que promise. C'est le même périmètre honnête que la porte 04 : aucun
chemin public, et une déclaration pour le reste.

## Ce que ça verrouille

- **La porte 07, moitié triage**, se vérifie désormais par
  `corpus/score_triage.py` et ses quatre conditions. Les changer est une décision
  écrite, et **tout résultat de triage antérieur devient périmé** — la règle du
  harnais, appliquée au trieur.
- **L'étalon est gelé** : la colonne « implémentable » d'`AMORCE.md` ne se touche
  plus. Une erreur qu'on y trouverait s'inscrit en **note datée**, sous la ligne
  d'origine, comme la correction du 2026-09-18 sur l'entrée 7 — jamais par
  réécriture.
- **Le § Verdict d'`AMORCE.md` reçoit une note de correction** : ses comptes
  (12 / 5 / 3) ne sont pas ceux de sa propre colonne (13 / 5 / 2).
- **`ETAT.md` disait 24 entrées et six `partiel`** ; les deux sont faux, corrigés
  le 2026-09-19 en 20 entrées et cinq `partiel`. Le dénominateur d'un seuil se
  compte avant d'écrire le seuil.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **L'extraction** — l'autre moitié de la porte 07 — n'est pas ici. Elle bute sur l'acquisition : 3 PDF sur les 20 fiches demandées, 6 entrées sans lien, 2 derrière un péage | décision suivante, avant de ficher en série |
| Le **niveau de détail** d'une fiche produite automatiquement, que `corpus/SCHEMA.md` borne sans le fixer | même décision |
| Ce que devient la porte si les 20 fiches ne sont **pas atteignables** depuis `AMORCE.md` — élargir le corpus, ou requalifier la porte par écrit | même décision, et pas au quinzième papier |
| Le trieur jugé depuis un **PDF** plutôt que depuis une ligne de tableau — la vraie généralisation | phase 09 |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

Chaque ligne dit **qui a trié et ce qu'il avait vu** (§ Complément).

| # | Date | Trieur, et ce qu'il avait vu | Ce qui a changé depuis le passage précédent | A/B/C/D | Verdict |
|---|---|---|---|---|---|
| **1** | 2026-09-20 | Agent `general-purpose` (Opus 5) lancé depuis une session contaminée, avec interdiction de lecture explicite. **A vu :** `corpus/triage_input.json` seul, plus la règle de classement et les contraintes de données recopiées dans sa consigne. **N'a vu ni** `AMORCE.md`, ni `TRIAGE.md`, ni `score_triage.py`, ni `ETAT.md`, ni `LECONS.md`, ni `wiki/`, ni `decisions/`, ni `registry/`, ni les fiches ou les PDF ; aucun accès web. **Réserve déclarée par lui-même :** `CLAUDE.md` lui a été injecté automatiquement — il ne porte aucun verdict de triage. | *(premier passage)* | 1 / 0 / 2 / 0 | **les quatre conditions tiennent** — 3 désaccords sur 20, verdicts dans `corpus/triage_passage_01.json` |

**Ce que le passage 1 a donné, et ce qu'il n'a pas donné.** Il tient, mais **A et
C sont à leur maximum exact** (1 sur 1, 2 sur 2) : un désaccord de plus sur un
`oui` ou sur un `partiel`, et la moitié triage ne passait pas. Ce n'est pas une
marge, c'est une limite atteinte, et le verdict de la porte doit le citer tel
quel.

Les trois désaccords, avec le motif du trieur, parce que `D15` demande qu'ils
soient examinés et non comptés (`L06`) :

| Entrée | Étalon | Trieur | Le motif, et ce qu'il désigne |
|---|---|---|---|
| 3 — Heston, Korajczyk & Sadka (2010) | `oui` | `partiel` | *« le test d'origine est un tri transversal sur des milliers d'actions : à 4,22 paris effectifs il faut le retranscrire en série temporelle par instrument »*. **Le trieur a raison sur les faits et l'étalon sur la classe.** La transposition a réellement eu lieu — `H03` l'a implémentée en autocorrélation par instrument et mesurée (52 lignes de registre, motif absent). Or une méthode qu'on transpose sans donnée extérieure reste `oui` au sens de la règle : c'est `partiel` qui exige une donnée manquante, pas un travail de traduction. Le trieur a confondu *difficulté de transposition* et *donnée absente*. |
| 17 | `partiel` | `non` | *« le consensus d'analystes est une donnée payante dont nous ne disposons pas »*. Désaccord de fond sur ce que coûte la donnée, non sur la règle. |
| 20 — Moskowitz et al. | `partiel` | `non` | *« douze mois de mémoire supposent une série roulée sur plusieurs échéances, que l'échéance unique interdit »*. Le trieur invoque une contrainte que la consigne lui a donnée telle quelle ; l'étalon la tenait pour transposable. |

Aucun de ces trois ne désigne une erreur de l'étalon, et **l'étalon n'est pas
touché** — la règle du § Ce que ça verrouille s'applique.

La session du 2026-09-19 qui a écrit cette décision **a lu la colonne** et ne peut
donc pas trier. L'entrée du trieur est fabriquée et auditée
(`corpus/triage_input.json`, 20 entrées, colonne verdict retirée) ; le juge est
vert sur 10 vérifications ; il manque un trieur non contaminé.

> **Note du 2026-09-20.** Ce dernier point n'est plus vrai : le passage 1
> ci-dessus a été trié par un agent non contaminé, lancé depuis une session qui,
> elle, l'était. Le texte d'origine est conservé — il dit l'état du 2026-09-19.
>
> **Un défaut du protocole a été trouvé en lançant ce passage, et contourné sans
> modifier le protocole.** `corpus/TRIAGE.md` § Ce que le trieur rend illustre le
> format de sortie avec **deux entrées réelles et leur verdict juste** —
> `{"entry": 1, "verdict": "oui"}` et `{"entry": 18, "verdict": "non"}`. L'entrée
> 18 est l'un des **deux seuls `non`** de l'étalon, donc la moitié de la
> condition B. Donner `TRIAGE.md` au trieur revient à lui donner deux réponses
> sur vingt. Le passage 1 ne l'a **pas** reçu : la règle de classement et les
> contraintes de données lui ont été recopiées dans sa consigne, avec un exemple
> de format **neutre** (numéro et verdict en gabarit). Il a classé l'entrée 18
> `non` sans l'indice.
>
> `TRIAGE.md` n'a pas été corrigé pendant le passage : corriger le protocole dans
> le geste même qui l'applique est exactement ce que le § Le premier passage fait
> foi interdit. **La correction est due**, et elle est à faire avant le passage 2.
