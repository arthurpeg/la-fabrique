---
type: hub
updated: 2026-09-24
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-24.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 09 — premier passage complet sur 30 à 50 papiers |
| **Dernière porte franchie** | **08**, le 2026-09-23 — `scripts/gate_08.py`. Un signal produit par une session de codage séparée tient les **six conditions de `D23` au premier essai**, et aucun signal produit n'a été retouché à la main. |
| **Décision la plus récente** | `decisions/DECISION-26-encadrement-des-frais.md` — les frais par contrat sont |
| **Tests au registre** | 169 |
| **Idées abandonnées recensées** | 55 |
| **Entrées au journal** | 66 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais par contrat — **encadrés par `D26`**, champ laissé `null` jusqu'à ce que le harnais sache les lire ; multiplicateur FDAX | **nous** — les **neuf multiplicateurs CME sont déposés** depuis le 2026-09-24 (`catalogue.yaml` § provenance) ; les frais restent `null` | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action — reflet de `ETAT.md`

**LES PORTES 07 ET 08 SONT FRANCHIES. LA PHASE 09 EST OUVERTE — et c'est la
première qui dépense des tests.**

Relancer plutôt que recopier (`L21`) :

```
python scripts/gate_07.py      # G1 = G2 = G3 = G4 = 0
python scripts/gate_08.py      # 1 signal, 6/6, aucune retouche
```

### SI TU ARRIVES SUR UNE AUTRE MACHINE — à lancer en premier

Une question ouverte depuis le 2026-09-24 : **l'extraction peut-elle passer à un
modèle local et gratuit ?** Elle ne se tranche pas en lisant, elle se mesure, et
**le matériel décide avant le modèle**. Première commande, avant toute
discussion :

```
python corpus/bench_local_extractor.py --machine
```

Elle relève GPU, VRAM, RAM et disque de **cette** machine-ci, les compare au
poste de référence (mesuré, daté, nommé — c'est un fait d'un poste, jamais un
fait du dépôt) et rend un verdict. Les seuils, calculés depuis le poids de
Qwen3-8B (5,2 Go) et son cache KV (~144 ko/token) :

| VRAM | Ce que ça permet |
|---|---|
| **≥ 12 Go** | Qwen3-8B tient pour **tout** le lot, `num_ctx` 40 960 compris |
| **8 à 12 Go** | les **petits** papiers seulement ; les gros s'inscrivent `contexte_depasse` |
| **< 8 Go** | comme la référence — un **4B** est le maximum réaliste |

**Le poste de référence est sous le seuil** : GTX 1650, 4 Go de VRAM. Qwen3-8B y
a été téléchargé, constaté inutilisable et **retiré** ; un `num_ctx` plat à
40 960 y a fait tomber le disque de 12 Go à **1,4 Go** (Windows gonfle son
fichier d'échange), et un seul essai sur le plus petit papier a dépassé
**25 minutes** sans rendre la main.

Si ta machine est au-dessus du seuil, la mesure qui manque est celle-ci — un
papier, le même juge, la même consigne :

```
ollama pull qwen3:8b
python corpus/bench_local_extractor.py --run performance-of-time-series-momentum-strategy-us-W4388535504 --model qwen3:8b
python corpus/bench_local_extractor.py --report
```

**La règle de décision est écrite AVANT la mesure**, comme le veut l'invariant IV :

| Résultat | Conclusion |
|---|---|
| vert en ≤ 2 essais | le local gagne — l'extraction bascule, ~3 M de tokens économisés |
| vert en 3 essais | utilisable pour dégrossir, à re-juger |
| `F2` cassé à chaque essai | la citation mot pour mot ne passe pas à cette taille — c'est non |
| `contexte_depasse` | la VRAM ne suffit pas pour ce papier |

**Référence à battre, mesurée et non recopiée** : **1,33 essai par fiche**,
6 fiches vertes sur 6, par un modèle de frontière (`corpus/PRODUCED_harvest.json`).

### Deuxième poste mesuré — le 2026-09-24, et il est sous le seuil lui aussi

`python corpus/bench_local_extractor.py --machine` sur le poste **mathis** :

```
GPU     NVIDIA GeForce RTX 4050 Laptop GPU
VRAM    6.0 Go        RAM 15.3 Go        disque libre 55.5 Go
VERDICT SOUS LE SEUIL : 6.0 Go ne tient pas les 5,2 Go de poids du 8B.
```

**Deux postes sur deux sont sous le seuil**, donc la mesure que cette section
demandait — `qwen3:8b` — **n'a pu être faite sur aucun des deux**. Ce n'est pas
un échec de protocole : c'est le fait que le matériel devait trancher, et il a
tranché.

**Ce qui a été mesuré à la place : `qwen3:4b`**, le maximum réaliste ici et le
défaut de `bench_local_extractor.py`. Un papier, la même consigne, le même juge.

| | |
|---|---|
| chargement | 5,7 Go, réparti **27 % CPU / 73 % GPU** — même un 4B déborde à `num_ctx` 18 432 |
| essai 1 | **1 853,8 s — 30,9 minutes.** Invite 13 355 tokens, sortie 5 577 |
| verdict essai 1 | **`prose, accolades illisibles`** — `Extra data: line 9 column 1` |
| essai 2 | **tué à 50 minutes cumulées**, sans avoir rendu |

**Le modèle n'a pas échoué sur `F2` : il a échoué AVANT.** La consigne demande
*« un seul objet JSON, rien avant, rien après »* ; il a rendu de la prose autour.
La citation mot pour mot n'a jamais été atteinte, donc **cette mesure ne dit rien
de la capacité du 4B à citer** — elle dit qu'il ne suit pas le format de sortie.

**La table de décision de cette section n'a pas de ligne pour ce cas**, et c'est
honnête de l'écrire plutôt que de le ranger de force dans « `F2` cassé ». Ce qui
est acquis :

- **30,9 min par essai** contre **5 à 6,6 min** pour le modèle de frontière
  (durées relevées des sessions du lot du 2026-09-24). À 1,33 essai par fiche,
  les 29 candidats restants coûteraient **~20 heures** en local contre
  **~40 minutes** — et en série, le parallélisme étant exclu puisque le modèle
  sature déjà la carte seul.
- **Le banc n'a rien inscrit** : tué pendant l'essai 2, `corpus/bench_local/`
  et `results.json` sont vides. Les chiffres ci-dessus viennent de sa sortie
  console, et **une relance de 31 minutes par essai est le prix à payer** pour
  les réinscrire proprement.

**Ce qui resterait à mesurer, si quelqu'un veut trancher pour de bon** : un
modèle local de taille comparable **avec sortie JSON contrainte** (`format:
json` d'ollama, ou un modèle entraîné à l'appel d'outil). L'essai ci-dessus ne
l'avait pas, et c'est peut-être tout ce qui manquait.

### Ce que la phase 09 demande

> La chaîne tourne de bout en bout ; le registre compte tous les tests ; un
> rapport d'IC existe pour chaque signal.

Les trois maillons existent maintenant et sont jugés chacun par son propre
script : trieur (`D15`), extracteur (`D16`, `D17`, `D24`), codeur (`D23`).
**Ce que la phase 09 ajoute est le premier IC**, et c'est un changement de
nature : jusqu'ici aucune porte n'a dépensé une ligne de registre.

### ~~Ce qu'il faut trancher avant de lancer quoi que ce soit~~ — **tranché le 2026-09-23 par `D25`**

**Benjamini–Hochberg à `q` = 0,10**, unilatéral au signe pré-enregistré, lot de
**50 clos avant la première mesure**. Le dénominateur de la phase 15 reste le
registre **entier**, les 56 tests antérieurs compris.

Échelle concrète du lot :

| Rang retenu | `t` requis | IC requis |
|---|---|---|
| le 1ᵉʳ | **2,88** | 0,0196 |
| le 3ᵉ | 2,51 | 0,0171 |
| le 5ᵉ | 2,33 | 0,0158 |

*(Bonferroni aurait exigé 3,09 pour tous.)*

### Ce qui bloque la phase 09, maintenant que le budget est fixé

1. **Il manque 33 fiches.** `D25` engage un lot de 50 ; le corpus en porte **17**.
   **La matière existe désormais** : le triage du 2026-09-23 a retenu 39
   papiers moissonnés sur 119 (10 `oui`, 29 `partiel`,
   `corpus/triage_harvest_verdicts.json`), et `corpus/promote_harvest.py`
   (2026-09-24) les a fait passer par `D18` — **35 ont leur texte qui fait foi**
   (default+layout) dans `corpus/text/`, `text_source` basculé à
   `authoritative` pour 34 d'entre eux dans la base (`D22` § Journal, passage
   2). Un exclu (bug `pypdf` reproductible sur un PDF précis, non contourné),
   un doublon du `gao-2018` déjà connu (`L20`). **L'outil de préparation/jugement
   existe** — `corpus/extract_fiche_harvest.py`, sœur d'`extract_fiche.py` mais
   avec un **stockage séparé** (`corpus/fiches_harvest/`,
   `corpus/PRODUCED_harvest.json`) : `gate_07.py` juge G2/G3 sur TOUT
   `corpus/fiches/*.json` et TOUT `corpus/PRODUCED.json` sans filtrer par
   population, donc une fiche moissonnée écrite au mauvais endroit aurait pu
   repasser la porte 07 à NON FRANCHIE sans qu'aucune décision ne l'ait voulu.
   **Circuit validé de bout en bout, le 2026-09-24, sur un vrai papier** :
   session isolée (Agent, lisant UNIQUEMENT la consigne) → fiche → `--record`
   → `--judge` → refus sur 2 citations (espace inséré au milieu d'un chiffre
   par l'extraction PDF, `"2. 564"`) → renvoyé à la MÊME session (pas une
   retouche manuelle) → **les cinq conditions de `D16` tiennent, essai 2**.
   Même schéma que Patton & Sheppard en phase 07 (2 itérations).
   **Premier lot de 5 produit le 2026-09-24** : 5 sessions isolées en
   parallèle, **4 vertes au premier essai**, la cinquième refusée sur
   `signal_construction.value absent` — **cinquième occurrence indépendante de
   la même faute**, ce qui renforce le point 9 de la liste ci-dessous (c'est un
   défaut du schéma ou de la consigne, pas cinq erreurs) — puis verte après
   repassage. **6 fiches sur 35 candidats, 29 restantes.**
   **`L26` est sortie de ce lot** : l'isolement de l'extracteur a un plafond que
   personne n'avait écrit — `CLAUDE.md` est injecté dans toute session de ce
   dossier, et une fiche a cité `D01` §5 qui n'est ni dans sa consigne ni dans
   `corpus/SCHEMA.md`. Les 17 fiches de la phase 07 ont été produites dans la
   même condition. Aucune fuite de verdict ni de fiche ; le cadre, oui.
   **Un candidat est bloqué** : `market-intraday-momentum-apac-evidence` n'a pas
   de texte `D18` **sous son propre nom** — son PDF est le doublon d'octets de
   `gao-2018-market-intraday-momentum.pdf`, donc son texte qui fait foi existe
   sous le nom d'un AUTRE papier (`L20` qui resurgit). L'outil refuse plutôt que
   de deviner. À trancher à part : renommer touche des artefacts liés à
   l'entrée 1, donc à la population `G1`-`G4`.

   **Réserve non tranchée sur ce triage, et elle n'est écrite qu'ici.** Le
   lot 1 a rendu **0 `oui`** quand le lot 3 en a rendu **4**. Les lots sont
   ordonnés par titre, donc l'écart peut venir du contenu autant que de la
   sévérité du trieur. **Personne ne l'a départagé**, et il ne faut pas le
   supposer : si le rendement en fiches vertes diffère nettement d'un lot à
   l'autre, c'est là qu'il faudra regarder.
2. **La matrice de corrélation des 50 signaux** doit être produite **avant**
   d'appliquer `BH` : la procédure suppose une dépendance positive, et plusieurs
   papiers d'intraday momentum donneront des signaux corrélés.
   `scripts/calibrate_coder.py` sait déjà mesurer une corrélation entre deux
   signaux. Format attendu par la porte : `scripts/out/lot_09_correlations.json`,
   voir l'en-tête de `scripts/gate_09.py`.
3. ~~`scripts/gate_09.py` n'existe pas.~~ **Écrit le 2026-09-23**, avant le lot —
   le juge avant l'accusé, comme `score_triage.py` et `score_signal.py` avant
   lui. Il applique `BH` (unilatéral, signe pré-enregistré via `EXPECTED_SIGN`)
   et refuse tout verdict tant que : le lot n'est pas déclaré dans
   `hypotheses/LOT-09.json` (format fixé par ce script, faute d'exister
   ailleurs), que chaque hypothèse n'a pas son fichier dans `hypotheses/`, que
   la matrice de corrélation n'existe pas ou ne couvre pas exactement les
   signaux du lot, ou qu'une hypothèse n'a pas exactement une mesure au
   registre sous le harnais courant. **12 vérifications** (`--check`), vert —
   elles relisent le tableau de seuils de `D25` à l'envers (`t`=2,88 → `p`
   ≤0,0020, etc.) et vérifient le pas de `BH` lui-même. Lancé sans lot, il
   répond correctement NON FRANCHIE : c'est l'état attendu, pas une panne.
   **Zéro hypothèse retenue sera un résultat VALIDE de la porte**, pas un
   échec — elle juge que le protocole a été suivi, pas que la pêche a été
   bonne.

### Ce qui reste dû par ailleurs, et qui n'a pas bougé

| Point | Pourquoi ça compte |
|---|---|
| **Frais par contrat** — `null` sur les dix, **encadrés par `D26`** (relevé CME à refaire après le 2026-10-01 ; l'intégration au harnais, avec `slippage_bp`, sera UNE décision qui périme les 56 tests une seule fois). *Multiplicateurs : déposés le 2026-09-24 pour les neuf CME, avec provenance `D09` ; FDAX reste `null` (unité en EUR, hors univers)* | tant que les frais le sont, `harness/costs.py` ne rend qu'un **plancher étiqueté**, donc tout IC net est un **majorant de performance**. La phase 09 produit justement des IC |
| **`slippage_bp` à déclarer** | même famille |
| **`ruff format harness/`** reformaterait 4 fichiers | le harnais est **figé et versionné** ; le reformater changerait son empreinte et **périmerait les 56 tests comptés**. Ne pas lancer |
| **`scripts/gate_06_controls.py` ÉCRIT au registre** | une ligne de calibration par passage. Légitime (`counted_tests` ne bouge pas) mais **pas gratuit** — le passer dans une revue de gardes coûte une ligne irremplaçable. **Correction du 2026-09-24 : `gate_03_harness.py` (3 lignes de calibration) et `gate_04_registry.py` (1 ligne, `porte-04-chemin-legitime`) écrivent AUSSI** — relancés ce jour sur la foi de la phrase précédente, ils ont ajouté 4 lignes non comptées (`counted_tests` reste 56). Voir `L25` |
| **Le texte qui fait foi pour le HTML** | `D24` § Ce qui reste ouvert. Si `D18` s'étend au HTML, l'entrée 9 redevient fichable, `G1` repasse à 1, et la porte 07 est réputée non franchie |

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
| 2026-09-24 | `mesure` | **L'EXTRACTEUR LOCAL NE PASSE PAS SUR UN DEUXIEME POSTE SOUS LE SEUIL.** `bench_local_extractor.py --machine` sur le poste mathis : RTX 4050 Laptop, **6,0 Go de VRAM** — sous le seuil de 8 Go, comme le poste de reference (GTX 1650, 4 Go). **Deux postes sur deux**, donc la mesure que `ETAT.md` demandait (`qwen3:8b`) n'a pu etre faite sur aucun des deux | MESURE FAITE SUR `qwen3:4b`, le maximum realiste ici et le defaut du banc. **Essai 1 : 1 853,8 s, soit 30,9 MINUTES**, invite 13 355 tokens, sortie 5 577 — et le verdict est `prose, accolades illisibles` (`Extra data: line 9 column 1`). **LE MODELE N'A PAS ECHOUE SUR `F2`, IL A ECHOUE AVANT** : la consigne demande « un seul objet JSON, rien avant, rien apres », il a rendu de la prose autour. La citation mot pour mot n'a jamais ete atteinte, donc cette mesure NE DIT RIEN de la capacite du 4B a citer — elle dit qu'il ne suit pas le format de sortie. Essai 2 tue a 50 minutes cumulees sans avoir rendu. **LA TABLE DE DECISION DE `ETAT.md` N'A PAS DE LIGNE POUR CE CAS**, et c'est ecrit comme tel plutot que range de force dans « `F2` casse » — l'invariant IV veut une regle ecrite AVANT la mesure, pas une regle etiree apres. DETAIL MATERIEL QUI EXPLIQUE LE RESTE : `qwen3:4b` pese 5,7 Go une fois `num_ctx` 18 432 alloue, contre 6,0 Go de VRAM ; ollama en pousse **27 % sur le CPU**, et c'est ce tiers qui coute tout. LE CHIFFRE QUI TRANCHE EN PRATIQUE : **30,9 min par essai en local contre 5 a 6,6 min** pour le modele de frontiere (durees relevees des sept sessions d'extraction du 2026-09-23 : 302, 319, 319, 360, 379, 383, 397 s). A 1,33 essai par fiche, les 29 candidats restants coutent **~20 h en serie** en local — le parallelisme etant exclu, le modele saturant la carte seul — contre **~40 min**. Facteur ~30. **LE BANC N'A RIEN INSCRIT** : tue pendant l'essai 2, `corpus/bench_local/` et `results.json` sont vides ; les chiffres viennent de sa sortie console, et les reinscrire proprement coute 31 minutes par essai. CE QUI RESTERAIT A MESURER POUR TRANCHER POUR DE BON : un modele local avec **sortie JSON contrainte** (`format: json` d'ollama, ou un modele entraine a l'appel d'outil). L'essai n'en avait pas, et c'est peut-etre tout ce qui manquait. Aucun IC, aucun test depense : counted_tests **56** |
| 2026-09-24 | `outillage` | **BANC D'ESSAI DE L'EXTRACTEUR LOCAL** — `corpus/bench_local_extractor.py`. Question posee apres avoir chiffre le cout de l'extraction : le projet ne fait tourner EN LOCAL qu'une seule chose, `BAAI/bge-base-en-v1.5` via `fastembed` pour les embeddings ; les trois etapes de raisonnement (trieur `D15`, extracteur `D16`, codeur `D23`) ont toujours ete des sessions d'un modele de frontiere, et personne ne l'avait ecrit. L'invariant I dit « le LLM propose, le code deterministe tranche » — il ne dit pas LEQUEL, et l'extraction est l'etape la mieux placee pour un modele faible puisque `score_extraction.py` la juge a tolerance zero : un extracteur faible echoue BRUYAMMENT et recommence | EXPERIENCE CONTROLEE : meme consigne octet pour octet, meme juge, meme boucle de reprise — seul le modele change. Reference a battre, mesuree : **1,33 essai par fiche**, 6 vertes sur 6. LE MATERIEL A TRANCHE AVANT LE MODELE. Poste : GTX 1650, **4 Go de VRAM**, 16 Go de RAM. Qwen3-8B pese 5,2 Go : il n'y tient meme pas SANS cache KV. Telecharge, constate, **retire**. INCIDENT CAUSE PAR MA PREMIERE CONFIGURATION, et inscrit parce qu'il coute : un `num_ctx` PLAT a 40960 impose un cache KV de ~5,9 Go quel que soit le papier (~144 ko/token pour Qwen3-4B) — Windows a gonfle son fichier d'echange a 11 Go, **le disque est tombe de 12 Go a 1,4 Go libres**, et un seul appel sur le PLUS PETIT papier n'avait pas rendu la main apres 25 minutes. Corrige : le contexte se calcule PAR PAPIER (18432 a 40960), le garde de troncature reste inconditionnel — une invite rabotee ferait echouer `F2` pour une raison qui n'est pas celle du modele, et on conclurait faux. DEUX MESURES A VIDE : ~8 tokens/s en generation, et **Qwen3 ignore `think: false` COMME `/no_think`** — il deverse son raisonnement dans la reponse, ce que l'extracteur JSON tolere mais qui double le temps. MODE `--machine` AJOUTE : il releve GPU/VRAM/RAM/disque et les compare au poste de reference, **date et nomme**, parce que c'est un fait D'UN POSTE et que le depot s'est deja trompe trois fois en ecrivant l'un pour l'autre (`L20`, `L21`). Seuils calcules : >= 12 Go de VRAM pour tout le lot, 8-12 Go pour les petits papiers, en dessous un 4B est le maximum. La regle de decision est ecrite AVANT la mesure (invariant IV) et vit dans `ETAT.md` § Si tu arrives sur une autre machine |
| 2026-09-24 | `extraction` | **PREMIER LOT DE 5 FICHES MOISSONNEES**, cinq sessions isolees lancees en parallele, chacune ne lisant que sa consigne et ecrivant sa fiche elle-meme (le JSON ne transite pas par la session qui orchestre — economie de contexte, et une transcription en moins ou se glisser une retouche) | **4 VERTES AU PREMIER ESSAI**, la cinquieme refusee sur `signal_construction.value absent` puis verte apres repassage de sa propre session. Total : 6 fiches sur 35 candidats, 29 restantes. LA FAUTE DU CINQUIEME EST LA CINQUIEME OCCURRENCE INDEPENDANTE DE LA MEME : `ETAT.md` notait deja « 4 extracteurs independants sur 6 » ecrivant un objet structure sans la cle `value` que le schema exige. Cinq fois la meme faute chez cinq sessions qui ne se sont jamais parle n'est pas cinq erreurs — c'est un defaut du schema ou de la consigne, et il attend toujours sa decision. UN CANDIDAT BLOQUE, et l'outil a refuse plutot que de deviner : `market-intraday-momentum-apac-evidence` n'a pas de texte `D18` sous son propre nom, son PDF etant le doublon d'octets de `gao-2018-market-intraday-momentum.pdf` — son texte qui fait foi existe donc sous le nom d'un AUTRE papier. C'est `L20` qui resurgit ; le renommage touche des artefacts de l'entree 1, donc la population `G1`-`G4`, et se tranche a part. CONTENU : le lot porte 28, 19, 18, 19 et 20 resultats cites. Le plus fort est Li, Sakkas & Urquhart (2022), replication internationale de Gao et al. sur 16 marches — pente poolee 2,86, `t` = 7,53, significatif dans 12 marches sur 16. Trois des cinq annoncent leur propre mort apres couts, ce qui est une information et non un echec. **`L26` EST SORTIE DE CE LOT** : une fiche cite `D01` §5, absent de sa consigne ET de `corpus/SCHEMA.md` (`grep -c` = 0 sur les deux) — la source est `CLAUDE.md`, injecte automatiquement dans TOUTE session de ce dossier, lignes 119-120. Aucun agent n'a desobei ; l'isolement que `D16` decrit a un plafond que personne n'avait ecrit, et **les 17 fiches de la phase 07 ont ete produites dans la meme condition**. Les trois fuites que `D16` nomme (verdict de triage, fiches, resultats des papiers) restent fermees |
| 2026-09-24 | `outillage` | `corpus/extract_fiche_harvest.py` ECRIT — soeur d'`extract_fiche.py` pour la population moissonnee (35 candidats promus). DECOUVERTE CRITIQUE avant d'ecrire une seule fiche : `gate_07.py` juge `G2` sur TOUT `corpus/fiches/*.json` et `G3` sur TOUT `corpus/PRODUCED.json`, SANS filtrer par population — une fiche moissonnee au mauvais endroit aurait pu repasser la porte 07 (franchie le 2026-09-23) a NON FRANCHIE sans qu'aucune decision ne l'ait demande. Stockage separe donc : `corpus/fiches_harvest/`, `corpus/PRODUCED_harvest.json`, `corpus/consignes_harvest/` (gitignore etendu). Le JUGE reste le meme (`score_extraction.py`, D16) — il juge une fiche seule, jamais un repertoire | CIRCUIT VALIDE DE BOUT EN BOUT sur un vrai papier (`measuring-volatility-with-the-realized-range-W2133491221`, Martens & van Dijk 2006). Session Agent isolee, lisant UNIQUEMENT le fichier consigne (verifie : 4 appels Read, rien d'autre). Premier essai : F1/F3 CASSEES sur 2 citations — l'extraction pypdf `default` insere un espace au milieu d'un chiffre ("2. 564" au lieu de "2.564", "0 .443" au lieu de "0.443"), confirme par grep direct sur `corpus/text/*.default.txt` (le mode `layout` les a PROPRES). Le juge refuse a bon droit meme avec `quoted_repair: math_notation` : la reparation couvre la notation abimee autour du chiffre, pas le chiffre lui-meme devenu illisible par la regex `value_in_quote`. Renvoye a la MEME session (pas une retouche manuelle, D16) avec le verdict exact du juge : elle a retire les deux `quoted_source`/`quoted_repair` et recite proprement. **Essai 2 : les cinq conditions de D16 tiennent.** Meme schema que Patton & Sheppard en phase 07 (2 iterations). `extract_fiche_harvest.py --list` : 1 fichee sur 35, 34 restantes. Cout mesure sur cette seule fiche : 2 appels Agent, ~220K tokens de sous-agent — a extrapoler avant de lancer les 34 autres |
| 2026-09-24 | `donnees` | **Chatbot Lucid interroge par l'operateur** (tout compris ? meme bareme en live ?) : il reformule le centre d'aide — le tableau « ne dit pas » si les frais CME, clearing ou NFA sont inclus — et ne tranche rien. Ce n'est pas une reponse, c'est la meme source relue. `D26` inchangee, `todo fees` ouvert. Voie restante : un humain du support, par ticket ou e-mail, avec une reponse ecrite citable | — |
| 2026-09-24 | `decision` | **D26 ECRITE — LES FRAIS SONT ENCADRES, PAS DEVINES.** Borne basse = bareme Lucid seul (cout complet sur compte simule) ; borne haute = Lucid + CME non-membre (Fee Finder, « clearing and trading ») + NFA 0,02/side (Bylaw 1301, taux 2027). Toute lecture nette qui conditionne un choix se fait a la borne haute. Releves CME : NQ/ES/YM 1,38, GC 1,65, CL 1,50, devises 1,60, micros indices 0,35, MGC 0,70, MCL 0,50 par side. Rapport micro/plein verifie a 1/10 sur les fiches contrat (D01 §7 le laissait a verifier). INDICE, PAS PREUVE : Lucid >= CME sur les 14 contrats, egal sur MCL — forme d'une repercussion. En bp (`scripts/fee_bracket.py`, pool) : borne haute 0,37 (NQ) a 1,18 (CL) en plein, du meme ordre que le plancher d'ecart ; 1,03 a 3,43 en micro. **`fee_per_contract_usd` RESTE null EXPRES** : `harness/costs.py` ne le lit que pour sa nullite, le remplir effacerait `fee_bp` des manques sans l'ajouter au cout — `F55`. Ouvert : frais CME changent le 2026-10-01 (SER-9799R, PDF non lu), a relever de nouveau ; integration au harnais + `slippage_bp` en UNE decision. Aucun IC, harnais intact, counted_tests **56** | — |
| 2026-09-24 | `outillage` | `corpus/promote_harvest.py` ECRIT ET LANCE — le pont mecanique que `D22` exigeait avant qu'un papier `harvest` devienne fichable, applique au triage du 2026-09-23 (39 papiers retenus sur 119, `corpus/triage_harvest_verdicts.json`). Reutilise les fonctions de `harvest.py` (filename, sha256, known_hashes, load/save) plutot que de les reecrire ; correspondance par TITRE NORMALISE (`triage_harvest_verdicts.json` porte l'uuid Postgres, `harvest.json` l'openalex_id, les deux espaces ne se recoupent pas) | 39 apparies sans manquant. 36 PDF promus au premier passage, 3 echecs reseau dont 1 recupere au second (2 pages HTML servies a la place du PDF, NON contournees). UN BUG PYPDF REPRODUCTIBLE TROUVE ET NON CONTOURNE : `ZeroDivisionError` en mode `layout`, page 30, sur un PDF precis — isole par relecture directe de la page, exclu de la promotion (retire de `corpus/pdf/` et de `harvest_promoted.json`) plutot que route autour. Un doublon sha256 avec `gao-2018-market-intraday-momentum.pdf` (deja `authoritative` depuis `L20` — c'est LE MEME papier APAC, retrouve une seconde fois par la meme methode). `corpus/extract_text.py` relance sur le lot propre : **104 fichiers, pypdf 6.14.2, manifeste conforme** (`--check` vert). `text_source` bascule `harvest -> authoritative` pour 34 papiers (D22 § Journal, passage 2) : la base porte desormais 51 `authoritative` contre 85 `harvest`. Un orphelin trouve et nettoye : le `.default.txt` du papier exclu, ecrit avant le crash, ne figurait plus au manifeste. `extract_fiche.py --list` INCHANGE (17 fichees, G1-G4 ne bougent pas — F47) : ce travail ne fiche rien, il rend fichable. **Reste : un outil de preparation pour ces 35 papiers (hors `corpus/acquisition.json`, qui reste la population des 20 d'AMORCE.md) et 33 sessions separees, une par papier, n'ayant vu que leur consigne (D16)** |
| 2026-09-24 | `donnees` | **FRAIS LUCID : RECHERCHE SANS CONCLUSION.** Bareme relu (inchange), centre d'aide, FAQ officielle, un blog tiers : aucune source ne dit si les montants par side sont all-in. Un resume de recherche affirmant « exchange fees separate » confondait avec les abonnements de donnees -- verifie sur la page, pas suppose. ETABLI : pas de micro devises au bareme (6E/6B/6J/6A en plein format seulement, 2,40) ; evaluation et sim-funded sont SIMULES, le montant debite est celui que Lucid configure ; le bareme live n'est pas publie ; cloture forcee 16:45 ET, regle microscalping (5 s) sans effet a 30 min. Consigne dans `todo fees` (`catalogue.yaml`), aucune valeur deposee. Voie restante : un releve d'execution du compte de l'operateur, qui rend la valeur MESUREE. counted_tests **56** | — |

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
