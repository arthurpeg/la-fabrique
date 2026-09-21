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
| **Décision la plus récente** | `decisions/DECISION-18-le-texte-qui-fait-foi.md` — « le texte du papier » n'existe pas : il y a des **extractions**, qui diffèrent. Le texte qui fait foi |
| **Tests au registre** | 135 |
| **Idées abandonnées recensées** | 47 |
| **Entrées au journal** | 37 |

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
8. **Ficher les 14 papiers restants** — `G1` exige zéro atteignable non fiché.
   `python corpus/extract_fiche.py --list` dit lesquels.

### Ce qui reste ouvert par ailleurs

- **l'acquisition est recensée depuis le 2026-09-21** et ne bloque presque plus :
  **19 atteignables sur 20**, un seul inatteignable — l'entrée 6 (Wen et al.,
  pétrole), refusée par SSRN, péagée chez Elsevier, et sur ResearchGate seulement
  contre une demande à l'auteur, ce que `D17` exclut. Il reste que **3 PDF
  seulement sont sur le disque** ; les 15 autres sont obtenus et vérifiés, non
  enregistrés. Le compte de liens d'`AMORCE.md` — 14 avec lien, dont 12 libres —
  n'est plus le bon dénominateur : il décrit `AMORCE.md`, pas ce qui est à
  portée. **Les 18 PDF sont sur le disque depuis le 2026-09-21** — et cet
  énoncé-là se périme, `corpus/pdf/` étant ignoré par git : le vérifier se fait
  en lançant `python corpus/fetch_pdfs.py --verify` ;
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
| 2026-09-21 | `extraction` | PASSAGE 1 DE L'EXTRACTEUR — LES CINQ CONDITIONS DE `D16` TIENNENT. Entrée 13 (Patton & Sheppard 2015), extracteur = agent séparé avec interdiction de lecture explicite, n'ayant reçu que la consigne produite par `corpus/extract_fiche.py` — schéma, texte du papier, règles de rejet — et RIEN d'autre du corpus. Papier choisi SANS fiche de référence préexistante, donc aucune réponse à recopier. Inscrit au § Journal de `D16` ; fiche dans `corpus/fiches/patton-sheppard-2015-good-volatility-bad-volatility.json` | 25 résultats, 7 RÉPARATIONS DÉCLARÉES (5 `ocr`, 2 `table`), 2 ITÉRATIONS, ET AUCUNE CITATION REFUSÉE — le seul échec de la première itération était `F1` (`signal_construction` écrit comme objet structuré sans la clé `value` exigée). Le schéma a donc attrapé une faute de FORME et non de FIDÉLITÉ, ce qui est l'ordre souhaitable. `D18` VALIDÉE PAR LE RÉEL DÈS CE PASSAGE : la citation `spdr_first_autocorr_max` n'est présente que dans l'extraction `default`, `layout` la casse — sous l'option « layout seul », une citation JUSTE aurait été refusée ; l'union n'est pas une précaution théorique, elle a servi au premier essai. LES SEPT RÉPARATIONS VÉRIFIÉES À LA MAIN, après le juge et indépendamment de lui : chaque `quoted_source` littéralement présente dans au moins une extraction, et chaque valeur numérique présente dans la chaîne QUI FAIT FOI — le point où `D16` craignait qu'on loge un chiffre absent du papier. Motifs honnêtes : 4 ligatures, 1 césure de fin de ligne, 1 ligne éclatée par des exposants, 2 lignes de tableau mises à plat. CE QUE LE PASSAGE A OUVERT ET QUI N'EST PAS TRANCHÉ : le côté LISIBLE d'une réparation n'a aucune règle. `D16` définit `quoted_source` au caractère près et laisse `quoted` « lisible » ; sur les deux réparations `table`, « lisible » est devenu une GLOSE EN FRANÇAIS qui n'est plus une citation. Rien de mécanique n'en souffre, mais `quoted` est ce qu'un humain lit pour contrôler, et une glose n'est pas contrôlable contre le papier. LA FICHE N'A PAS ÉTÉ RETOUCHÉE — `G3` de `D17` exige zéro retouche manuelle, et corriger la sortie à la main serait exactement la faille que `G3` ferme ; s'il faut une règle, c'est une décision et l'extracteur sera relancé. Enfin l'extracteur a lui-même signalé que LE CHOIX DE SES 25 RÉSULTATS N'A ÉTÉ CONTRÔLÉ PAR PERSONNE : c'est la limite que `D16` § Pourquoi s'était donnée, la pertinence n'ayant de dénominateur qu'en phase 09. ÉTAT DE `G1` : 4 fichés, 14 à ficher, 2 hors d'atteinte. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e) |
| 2026-09-21 | `decision` | D18 ÉCRITE — LE TEXTE QUI FAIT FOI, plus trois verrous préalables à l'extracteur. « Le texte du papier » n'existe pas : il y a des EXTRACTIONS, qui diffèrent assez pour changer le verdict de `F2`. Le texte qui fait foi est désormais l'UNION DE DEUX EXTRACTIONS FIXÉES D'AVANCE ET IDENTIQUES POUR TOUS LES PAPIERS (`pypdf` défaut + `layout`), produites par `corpus/extract_text.py` et VERSIONNÉES dans `corpus/text/` — 36 fichiers, 6,2 Mo, empreinte sha256 de chacun au manifeste avec la version de `pypdf`, pour qu'une montée de version qui périmerait les `quoted_source` soit BRUYANTE | L'OPTION ÉCARTÉE EST LA PLUS INSTRUCTIVE : un mode déclaré PAR PAPIER transformerait le choix du texte en BOUTON — l'extracteur échoue, on change son mode, il passe ; c'est « modifier le harnais pour faire passer un signal » transposé au corpus. `layout` seul a aussi été écarté, et par la MESURE : il réduit d'un cinquième les lettres orphelines (11 622 -> 9 304 sur 18 papiers) MAIS PERD 6 % DU CONTENU NORMALISÉ, jusqu'à 20 % sur l'entrée 8 — et pour `F2` une perte de contenu est pire qu'un espace parasite, un espace se répare en le déclarant, un passage absent ne se répare pas. VÉRIFIÉ QUE L'UNION NE DISSOUT PAS LA LISTE CLOSE DE D16 : en retirant les réparations d'Andersen & Bollerslev, 3 citations redeviennent introuvables dans LES DEUX modes — `ocr`/`math_notation`/`table` gardent leur rôle et `L18` le sien. Coût corrigé en cours de rédaction : annoncé à 3,5 Mo, il vaut 6,2 — estimé sur la taille NORMALISÉE alors que `layout` pad avec des espaces ; inscrit au § Journal de D18 plutôt que corrigé en silence. TROIS VERROUS POSÉS LE MÊME JOUR, chacun préalable à l'extracteur : (1) `validate_fiches` connaît la réparation déclarée, l'asymétrie « F1 plus laxiste que F3 » nommée par D16 est fermée, garde 23 -> 31 vérifications et 15 fautes refusées ; (2) LA FUITE DE `corpus/SCHEMA.md` EST FERMÉE (L17) — ses exemples portaient le contenu RÉEL d'une fiche de référence et c'est le SEUL document du corpus que l'extracteur lit ; exemples refaits sur un papier fictif, et la réparation déclarée y est enfin documentée, faute de quoi un extracteur devant un texte abîmé paraphraserait ; (3) `corpus/extract_fiche.py`, harnais SANS INTELLIGENCE D'EXTRACTION — il prépare la consigne et juge la sortie, l'extraction étant faite par une session séparée qui reçoit le schéma, le texte, et rien d'autre du corpus. EFFET DE BORD TROUVÉ EN LANÇANT `--list` : il appariait fiche et papier PAR NOM DE FICHIER, or une fiche porte le nom de son sujet et le PDF celui de sa provenance — trois papiers fichés comptaient comme non fichés et `G1` aurait été déclaré rouge à tort ; appariement refait sur `source.pdf`. ÉTAT DE `G1` : 3 fichés, 15 à ficher, 2 hors d'atteinte (entrée 6 inatteignable, entrée 9 en HTML). Les 3 fiches de référence passent les cinq conditions avec le texte résolu par D18, Heston compris et SANS que sa fiche ait été touchée. Gardes : `score_extraction --check` 32, `check_fiches_guard` 31, `check_acquisition` 11/11, `validate_fiches` vert, `ruff check corpus/` vert. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e) |
| 2026-09-21 | `lecon` | L18 ÉCRITE — « Avant d'élargir une liste close, chercher si la cause n'est pas ailleurs ». Tirée du cas Heston du jour : cinq citations introuvables, le mécanisme de réparation déclarée de `D16` à portée de main, et la bonne réponse était de ne pas s'en servir | CE QUE LA RÉPARATION AURAIT COÛËTÉ, et c'est le cœur de la leçon : cinq `quoted_source` reproduisant fidèlement les fautes d'un extracteur mal réglé, une valeur de liste close inventée pour les couvrir, et une fiche de référence DÉGRADÉE POUR RESSEMBLER À UN DÉFAUT D'OUTIL — le tout VERT, soit la forme la plus coûteuse de l'erreur, celle qui passe la porte. `ocr`, la valeur la plus proche, aurait été un mensonge VÉRIFIABLE (métadonnées : LaTeX + Ghostscript, PDF né numérique) : une liste close ne vaut que si chacun de ses noms est vrai, et y loger un cas « à peu près » la vide de son sens plus sûrement que de l'élargir franchement. LE MOTIF GÉNÉRAL : une liste d'exceptions qui s'allonge est le symptôme d'une cause non cherchée, pas d'un monde irrégulier ; la question qui tranche est « si l'outil avait raison, la fiche aurait-elle tort ? ». COROLLAIRE, qui rejoint L17 : élargir la liste n'était PAS ma décision à prendre en passant (elle appartient à `D16`), donc chercher la cause était la seule chose que je pouvais faire sans excéder mon mandat — et c'est celle qui a résolu le problème. La contrainte a mieux travaillé que ne l'aurait fait la liberté. AU PASSAGE : `wiki/lessons.md` annonçait « 5 leçons (L01 → L05) » comme un état du projet alors que `LECONS.md` en porte 18. Compte corrigé, SYNTHÈSE NON REFAITE et déclarée en retard par un encadré daté : relire treize leçons pour en tirer les motifs communs est un travail en soi, et le bâcler produirait le résumé plausible que ce projet refuse. `LECONS.md` : 17 -> 18 leçons, append-only respecté, aucune ligne touchée |
| 2026-09-21 | `correction` | LES TROIS FICHES DE RÉFÉRENCE PASSENT LES CINQ CONDITIONS DE `D16`. Réparations faites selon le § Complément du 2026-09-20 : `quoted_source` + `quoted_repair` déclarés (3 entrées d'Andersen & Bollerslev en `ocr` — scan rendant « pA » pour rho, « ]Rt,,,] » pour | R\|, « fight part » pour « right part » ; `walk_forward_folds` de Mesfin en `table`), et deux citations corrigées par NOTE DATÉE avec le texte d'origine conservé mot pour mot, jamais par réécriture silencieuse \| SIX ENTRÉES TOUCHÉES LÀ OÙ `D16` EN ANNONÇAIT TROIS, ET L'UN DE SES TROIS ÉTAIT INUTILE. (1) Faute non vue par `D16` : `families_failing_below_friction` fermait sa citation par un POINT là où le papier écrit DEUX POINTS et poursuit — un caractère, et la citation est introuvable ; c'est la démonstration que `F2` ne pardonne rien. (2) `D16` SE TROMPAIT DE MOTIF sur `acceptance_criteria` : elle écrivait que « >= 30 trades » ne figure pas dans la phrase citée, or le résumé de Mesfin porte « at least 30 trades per OOS fold ». Le verdict (paraphrase, donc faute) tient entièrement, son motif était mal dit. ET LA FAUTE ÉTAIT PIRE QUE DITE : la citation était un COMPOSITE — seuil de permutation p < 0.001 pris au Tableau 3, reste de la phrase calqué sur le résumé qui écrit p < 0.05. LE PAPIER SE CONTREDIT LUI-MÊME et la fiche avait fondu les deux passages ; la citation du résumé est retenue verbatim, le désaccord interne inscrit en note comme un fait SUR LE PAPIER, non tranché. (3) LE PLUS IMPORTANT : HESTON N'AVAIT RIEN À RÉPARER. Ses cinq citations échouaient parce que `pypdf` INSÈRE DES ESPACES DANS LES MOTS — « multiples o f 13 », « half-hour inte rvals », « way is d ifferent ». Aucune valeur de la liste close ne nommait ce cas avec justesse et `ocr` aurait été UN MENSONGE : les métadonnées du PDF disent LaTeX + Ghostscript, il est NÉ NUMÉRIQUE. Plutôt que d'ouvrir la liste close en passant, l'hypothèse a été testée à la racine : `extraction_mode="layout"` rend Heston VERT SANS TOUCHER SA FICHE et ne casse aucune des deux autres ; les six `quoted_source` écrites ce jour résistent aux deux modes, vérifié. CONSÉQUENCE : la question ouverte « faut-il un OCR ? » n'était pas une question sur les SCANS — le défaut de `pypdf` abîme aussi un PDF propre. QUEL MODE D'EXTRACTION FAIT FOI devient une décision à écrire avant toute extraction réelle, puisqu'une `quoted_source` est définie CONTRE UN TEXTE ; non tranchée ici, ce n'est pas un seuil qu'on ajuste dans le geste qui l'applique. Gardes verts après coup : `validate_fiches` 3 fiches valides, `check_fiches_guard` 23 vérifications, `score_extraction --check` 32. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e). NOTE DE CONTAMINATION : cette session a lu les trois papiers et leurs fiches, elle NE PEUT PAS être l'extracteur de ces trois-là (`D16` § Qui peut être l'extracteur) |
| 2026-09-21 | `acquisition` | LES 18 PDF ATTEIGNABLES SONT ENREGISTRÉS — `corpus/fetch_pdfs.py`, 15 pris ce jour, 3 déjà là, **0 échec**, chacun vérifié APRÈS écriture (entête `%PDF-` et taille, fichier supprimé s'il ne passe pas). Le script ne lit que `corpus/acquisition.json` et ne télécharge que ce qui y est déjà inscrit atteignable : il n'a aucune autorité sur le recensement. Les noms de fichiers sont DÉCLARÉS dans une table explicite, pas déduits de la citation — un nom fabriqué par expression régulière se casse en silence sur la première citation mal formée et produit un fichier qu'aucune fiche ne retrouve. Les 3 fiches de référence gardent leur nom d'origine, le changer aurait cassé `F4` sur elles | LES 18 RENDENT DU TEXTE À `pypdf`, AUCUN N'EST VIDE — ET CELA NE PROUVE RIEN SUR LA JUSTESSE DE CE TEXTE, ce qui est écrit tel quel dans `ACQUISITION.md` plutôt que présenté comme un feu vert : l'entrée 11 rend 2 787 caractères par page et `D17` a établi que ce sont ceux d'un scan qui écrit « fight part » pour « right part ». Un compte de caractères ne distingue pas un texte d'un faux texte ; c'est `F2` qui juge, une citation à la fois. AUCUNE CONDITION DE GARDE N'A ÉTÉ AJOUTÉE SUR LA PRÉSENCE DES FICHIERS, et c'est délibéré : `corpus/pdf/` est ignoré par git, un garde qui exigerait leur présence serait rouge sur tout autre poste — c'est la péremption corrigée ce matin même, on ne la réinstalle pas sous forme de test. La vérification se lance (`fetch_pdfs.py --verify`), elle ne se lit pas. `F4` vérifié vert sur les 3 fiches de référence après coup ; `check_acquisition` toujours 11/11 ; `ruff check` vert sur les trois nouveaux scripts. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e). PROCHAINE ACTION DU PROJET : le corpus est prêt, l'extracteur n'existe pas |
| 2026-09-21 | `recensement` | LE RECENSEMENT DES ATTEIGNABLES EST FAIT — `G4` de `D17`. `corpus/probe_acquisition.py` sonde les 20 entrées d'`AMORCE.md` et écrit `corpus/acquisition.json` ; `corpus/check_acquisition.py` le garde (11 vérifications, vert, huit fautes fabriquées refusées chacune pour la raison prévue) ; `corpus/ACQUISITION.md` explique. Un papier n'est atteignable que si LE TEXTE ARRIVE : corps `application/pdf` d'au moins 20 000 octets commençant par `%PDF-`, preuve conservée par entrée. Les sources hors d'`AMORCE.md` portent leur provenance (`source_via`), `D09` appliqué à une URL | **19 ATTEIGNABLES SUR 20**, dont 18 en PDF et 1 en HTML. Un seul inatteignable : l'entrée 6 (Wen et al., pétrole) — SSRN refuse, Elsevier fait payer, ResearchGate demande une démarche à l'auteur que `D17` exclut. `D17` S'EST TROMPÉE ET SON § JOURNAL LE DIT : elle prévoyait « 6 à 14 selon ce que SSRN consent ». SSRN n'a RIEN consenti — contrôle anti-robot vérifié deux fois, en client automatique (403) et dans un vrai navigateur (« Vérification de sécurité en cours » qui ne se résout pas), NON CONTOURNÉ — et le compte est plus haut quand même. L'ERREUR ÉTAIT DE PRENDRE LE LIEN QU'`AMORCE.md` PORTE POUR LE PAPIER LUI-MÊME : s'en tenir à ces liens rendait 5 sur 20, chercher le papier en rend 19, car presque tous vivent aussi au NBER, dans les rapports de la Fed, sur des pages d'auteurs et dans des dépôts universitaires. L'entrée 3 le criait déjà — lien SSRN dans `AMORCE.md`, PDF venu d'arXiv et sur le disque depuis le 2026-09-20 — et personne ne l'avait lu ainsi. Le seuil de `D17` (rouvrir l'élargissement sous 5 atteignables), écrit AVANT le recensement, est largement écarté. DEUX ALERTES OUVERTES ET NON TRANCHÉES : entrée 9 libre mais en HTML — atteignable à la lettre de `D17`, infichable pour `F4` qui exige un `source.pdf` — et citation de l'entrée 16 apparemment fausse dans `AMORCE.md` (« Kurov, Sancetta, Strasser & Wolfe » contre Kurov, Wolfe & Gilbert pour le papier que son propre lien désigne) ; `AMORCE.md` N'A PAS ÉTÉ TOUCHÉ, c'est l'étalon du triage de `D15` et on ne retouche pas un étalon en passant. RESTE À FAIRE : les 15 PDF atteignables absents du disque sont OBTENUS ET VÉRIFIÉS, NON ENREGISTRÉS — geste distinct, non accompli. Aucun extracteur ; `G1`, `G2`, `G3` non mesurés. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e) |
| 2026-09-21 | `audit` | Les deux péremptions signalées à l'entrée précédente traitées — et l'une des deux N'EXISTAIT PAS. (1) RÉELLE : `ETAT.md` (trois endroits) et la page de phase 07 annonçaient « 21 vérifications » pour `corpus/score_extraction.py` ; le correctif de `D17` (la réparation déclarée) l'a porté à 32. Corrigé en 32, avec la mention de l'étape intermédiaire pour que l'historique reste lisible. (2) FAUSSE ALERTE : j'avais signalé « 14 dans `ETAT.md` contre 12 dans la page de phase » comme une contradiction à corriger | LE COMPTE A ÉTÉ REFAIT SUR `corpus/AMORCE.md` AU LIEU D'ÊTRE ARBITRÉ : **14 entrées sur 20 portent un lien** (1,2,3,4,5,7,8,9,11,12,13,15,16,17), **6 n'en portent aucun** (6,10,14,18,19,20), et **2 des 14 sont derrière un péage** (16 ScienceDirect, 17 AEA) — donc **12 liens LIBRES**. Les deux chiffres étaient JUSTES et comptaient des choses différentes : lien, et lien libre. Ma lecture était fausse, pas les pages. Les deux endroits portent désormais le dénominateur EXPLICITE — « 14 portent un lien dont 12 un lien libre » — pour qu'une session future ne rouvre pas la contradiction que j'ai cru voir. Le coût du faux positif était ici de deux minutes ; il aurait été d'un chiffre faux écrit dans `ETAT.md` si j'avais « corrigé » 14 en 12 sans compter. Vérification n° 1 faite de même, en lançant `score_extraction.py --check` : il répond 32. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e) |
| 2026-09-21 | `audit` | Péremption PDF corrigée dans `ETAT.md` et dans la page de phase 07 : les trois PDF de référence SONT sur ce poste depuis le 2026-09-20 (récupérés par la session de `D17`, qui l'inscrit à son § Le recensement), alors que `ETAT.md` affirmait encore « aucun PDF sur ce poste » en quatre endroits (cellule de la phase 07, section dédiée, prochaine action n° 1, point d'acquisition) | VÉRIFIÉ PAR LE JUGE LUI-MÊME et non affirmé : `check_f4` de `corpus/score_extraction.py` lancé sur les trois fiches, **F4 OK sur les trois**. LA PÉREMPTION A JOUÉ DANS LES DEUX SENS EN TROIS JOURS — « 3 PDF sur disque » écrit le 2026-09-18 depuis un autre poste, corrigé en « aucun PDF » le 2026-09-20 par `D16` dont le juge avait trouvé le fait faux tout seul, puis cette correction rattrapée QUELQUES HEURES PLUS TARD par la récupération des PDF, et restée fausse dans l'autre sens jusqu'à aujourd'hui. La leçon écrite dans `ETAT.md` n'est donc pas « il n'y avait pas de PDF » mais : l'état d'un dossier IGNORÉ PAR GIT n'est pas un fait du dépôt, il est vrai d'un poste et d'une heure, et le seul énoncé qui ne se périme pas est celui du juge lancé à l'instant. Aucun IC, aucun test dépensé : counted_tests reste à 56, registre à 135 lignes, harnais intouché (9ac3e45e). DEUX AUTRES PÉREMPTIONS VUES ET NON CORRIGÉES, hors du geste demandé : `ETAT.md` annonce encore « 21 vérifications » pour `score_extraction.py` là où `D17` le porte à 32, et le compte d'entrées à lien libre vaut 14 dans `ETAT.md` contre 12 dans la page de phase 07 |

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
