---
type: hub
updated: 2026-09-26
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-26.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 09 — premier passage complet sur 30 à 50 papiers |
| **Dernière porte franchie** | **08**, le 2026-09-23 — `scripts/gate_08.py`. Un signal produit par une session de codage séparée tient les **six conditions de `D23` au premier essai**, et aucun signal produit n'a été retouché à la main. |
| **Décision la plus récente** | `decisions/DECISION-29-plis-du-walk-forward.md` — **pas de plis en phase 09.** Rien n'y est ajusté sur le `pool` : les constantes viennent de la fiche (`S5`), |
| **Tests au registre** | 169 |
| **Idées abandonnées recensées** | 59 |
| **Entrées au journal** | 82 |

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
python corpus/bench_extractor.py --machine
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
fichier d'échange).

**Et le banc a tourné, sur 5 papiers — voir `F56`.** Résultat mesuré le
2026-09-24 avec Qwen3-4B, le maximum que ce poste tienne : **5 h 21 de calcul,
ZÉRO fiche produite.** Quatre papiers sur cinq **expirent à une heure** sans
rien rendre ; le cinquième épuise ses trois essais en **80,5 minutes** et
**aucun ne rend un objet JSON lisible**. L'échec n'est donc **même pas `F2`** :
le modèle n'atteint jamais la citation mot pour mot, il échoue à la **forme**.
Sur ce poste, la question est close ; sur une autre machine, elle se rouvre par
la mesure ci-dessus.

Si ta machine est au-dessus du seuil, la mesure qui manque est celle-ci — un
papier, le même juge, la même consigne :

```
ollama pull qwen3:8b
python corpus/bench_extractor.py --run performance-of-time-series-momentum-strategy-us-W4388535504 --model qwen3:8b
python corpus/bench_extractor.py --report
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

### Revue du 2026-09-26 — ce qui reste à traiter avant de mesurer

Une revue complète du dépôt (gardes relancés en lecture seule, registre 169 →
169) a trouvé huit points. **Le premier est corrigé (`D27`).** Les sept autres
sont ouverts, du plus grave au moins grave :

1. ~~Le test de causalité laissait passer une barre de futur.~~ **Corrigé, `D27`.**
2. ~~Des tests peuvent échapper au dénominateur.~~ **Corrigé côté porte 09,
   `D28`** ; le trou d'`extra` dans le harnais reste ouvert (voir `D28`). Une mesure avec
   `hypothesis_ref=None` compte comme calibration : `counted_tests()` l'ignore et
   `gate_09.py` ne cherche que les lignes portant la `ref` d'une hypothèse. À
   fermer dans `gate_09` : refuser tout signal du lot ayant une autre ligne au
   registre. Et `harness/registry.settle()` applique `extra` **après** les champs
   du ticket, donc peut écraser `hypothesis_ref` — à noter pour la prochaine
   décision qui touchera le harnais.
3. ~~Les plis du walk-forward ne sont tranchés nulle part.~~ **Tranché,
   `D29`** : pas de plis en phase 09, mesure unique sur tout le `pool` à un
   `asof` fixé et vérifié.
4. ~~11 fiches moissonnées sans trace de production.~~ **Refaites le
   2026-09-26** par 11 sessions isolées (consigne seule, anciennes fiches
   retirées du disque avant le lancement, `--record` avant tout `--judge`).
   **12 essais pour 11 fiches** : 10 vertes au premier essai, la dernière
   (`cryptocurrencies-and-momentum`) au second, après renvoi du verdict à la
   même session. Elle a contourné le bogue du point 5 par un `spelled_out` qui
   recopie le nombre tel que la citation l'écrit (`"17.71"`) — usage documenté
   par `corpus/SCHEMA.md` pour un texte abîmé, mais qui montre que `spelled_out`
   devient la soupape de toute faille de `value_in_quote` : corriger le point 5
   la rend inutile. **État : 18 fiches tracées, 17 vertes sur ce poste.**
   `bitcoin-is-not-the-new-gold` ne tient pas `F4` ici, et c'est voulu : le PDF
   de `corpus/pdf/harvest/` **ne rend pas le texte du manifeste** (empreintes
   `default` différentes), donc ce n'est pas le document dont le texte fait foi,
   et il n'a pas été copié. Même contrôle pour `intraday-volatility-transmission`
   : octets différents de ceux enregistrés à la promotion, **texte identique**,
   copié. Le bon PDF de `bitcoin-is-not-the-new-gold` est à reprendre sur le
   poste qui l'a promu. Les 33 autres PDF promus ont été copiés dans
   `corpus/pdf/` après vérification de leur empreinte.
5. ~~`value_in_quote` retire toutes les virgules.~~ **Corrigé le 2026-09-26**
   (`catalogue/validate.py`, `THOUSANDS`) : un séparateur n'est ôté que suivi
   d'exactement trois chiffres, derrière un entier. Onze cas ajoutés à
   `check_provenance.py` (44 vérifications), vus échouer avant la correction.
   Rejoué vert : catalogue, gardes des fiches, portes 07 et 08, 17 fiches
   `AMORCE` sur 17, 17 moissonnées sur 18. `L28` : le faux refus avait déjà
   poussé un extracteur vers la soupape `spelled_out`. **Reste ouvert** : le
   signe moins typographique `−` (U+2212), non lu comme signe par `NUMBER`.
6. ~~`extract_text.py --check` ne vérifiait que les PDF présents.~~ **Corrigé
   le 2026-09-26.** `--check` part du manifeste et nomme les entrées non
   vérifiables faute de PDF ; sans `--check`, ces entrées sont conservées telles
   quelles, et l'écriture est refusée si `pypdf` a changé alors que des entrées
   ne peuvent pas être reproduites (`D19`). Testé dans une copie isolée : 2 PDF
   sur 52, manifeste réécrit **identique au contenu** (100 entrées conservées) ;
   version changée → refus. Sur ce poste : **100 fichiers vérifiés sur 104**,
   non vérifiables `bitcoin-is-not-the-new-gold` (PDF local qui n'est pas le
   bon, point 4) et `gao-2018-market-intraday-momentum` (entrée 1, devenue
   inatteignable, `F53` — son texte versionné est celui du doublon APAC, `L20`).
   Au passage, les 34 PDF moissonnés copiés dans `corpus/pdf/` rendent
   exactement le texte du manifeste.
7. ~~Le piège `ruff format`.~~ **Désamorcé le 2026-09-26** dans
   `pyproject.toml` : `[tool.ruff.format] exclude = ["harness/**"]` et
   `force-exclude = true`, pour qu'un chemin nommé explicitement soit exclu lui
   aussi. Vérifié en lançant le formateur pour de bon sur une copie : `harness/`
   intact, empreinte `9ac3e45e` inchangée ; `ruff check` lit toujours le
   harnais. **`ruff check --fix` n'est pas couvert** : il ne toucherait rien
   aujourd'hui (le harnais passe le lint), mais une règle ajoutée demain le
   pourrait.
8. **Ce fichier retarde sur le dépôt** : point 9 de § Donc, dans l'ordre (le
   correctif de `signal_construction` est fait depuis le 2026-09-25), « 6 fiches
   sur 35 », « 36 fichiers » de texte (`--check` en compte 34), les fuites de
   `SCHEMA.md` à la fois fermées et ouvertes. Et `F55`–`F59` du ledger sont
   écrites **hors du tableau**, après « Voir aussi ».

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
   registre sous le harnais courant — et, depuis `D28`, qu'une autre ligne du
   registre touche le lot, et depuis `D29`, qu'une mesure ne porte pas sur tout
   le `pool` à l'`asof` fixé. **12 vérifications** à l'écriture, **21 depuis
   `D29`** (`--check`), vert —
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
| ~~**`ruff format harness/`** reformaterait 4 fichiers~~ | **désamorcé le 2026-09-26** (`pyproject.toml`, exclusion du formateur + `force-exclude`). Reste vrai pour `ruff check --fix` |
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
   **AGGRAVÉ LE 2026-09-25, ET CE POINT EST DEVENU LE PLUS RENTABLE DU PROJET.**
   Le banc l'a retrouvée chez **deux familles de modèles de plus** — Gemini 2.5
   Flash et `gpt-oss-120b` — soit **au moins 7 occurrences indépendantes sur
   trois familles** (sessions de frontière, Gemini, gpt-oss). Aucun extracteur
   n'a jamais vu les fautes des autres : c'est **le schéma ou la consigne** qui
   les induit, et plus aucune autre lecture ne tient.
   **Ce que ça bloque, chiffré.** L'extraction par morceaux récupérés
   (`corpus/recuperation.py`) sur `gpt-oss-120b` tient `F2`, `F3` **et** `F4` —
   citations mot pour mot, valeurs dans leur citation, PDF présent. Elle ne
   casse que sur `F1`, et uniquement sur des fautes de **forme** :
   `signal_construction` attendu objet, `what_is_missing` attendu liste. **La
   seule route gratuite qui franchit le mur des 8 000 tokens échoue donc sur
   notre propre documentation, pas sur sa fidélité.** Corriger la consigne coûte
   quelques lignes ; c'est peut-être ce qui sépare `F59` d'un `vert`.
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
| 2026-09-26 | `outillage` | **LE PIEGE `ruff format` EST DESAMORCE.** Septieme point de la revue du jour, signale dans `ETAT.md` depuis le 2026-09-19 et jamais ferme : `ruff format` reformaterait 4 des 7 fichiers de `harness/`, changerait l'empreinte (`code_hash` porte sur le contenu) et perimerait les 56 tests comptes | `pyproject.toml` : `[tool.ruff.format] exclude = ["harness/**"]` et `force-exclude = true` (un chemin nomme explicitement est exclu lui aussi). Verifie en lancant le formateur pour de bon sur une copie : harnais intact, empreinte `9ac3e45e` inchangee, 0 fichier de `harness/` parmi les 64 que `ruff format --check .` reformaterait. `ruff check` lit toujours le harnais. Non couvert : `ruff check --fix`. |
| 2026-09-26 | `correctif` | **`extract_text.py` PART DU MANIFESTE, PAS DU DISQUE.** Sixieme point de la revue du jour. `--check` ne verifiait que les PDF presents sur le poste et annoncait « conforme, 34 fichiers » quand le manifeste en portait 104 (`L21`) ; sans `--check`, le manifeste etait reecrit a partir du seul disque et un passage sur un poste incomplet aurait efface en silence les entrees des papiers absents | `--check` nomme les entrees NON VERIFIABLES faute de PDF et dit « N verifies sur M » ; l'ecriture CONSERVE ces entrees telles quelles, et refuse si `pypdf` a change alors que des entrees ne peuvent pas etre reproduites ici (`D19`). Teste dans une copie isolee du depot : 2 PDF presents, manifeste reecrit identique au contenu (100 entrees conservees), version changee -> refus. Sur ce poste : **100 verifies sur 104**, non verifiables `bitcoin-is-not-the-new-gold` (PDF local qui n'est pas le bon) et `gao-2018-market-intraday-momentum` (entree 1 inatteignable, `F53`, `L20`). Les 34 PDF moissonnes copies dans `corpus/pdf/` rendent exactement le texte du manifeste. Registre 169 -> 169. |
| 2026-09-26 | `correctif` | **`value_in_quote` N'OTE PLUS QUE LES SEPARATEURS DE MILLIERS.** Cinquieme point de la revue du jour. La fonction otait toutes les virgules avant de lire les nombres d'une citation : « `17.71,18.22` » (texte colle par l'extraction PDF) devenait `17.7118.22`, faux refus ; « `{12,6,1}` » devenait `1261`, faux accord possible. Onze cas ecrits d'abord dans `scripts/check_provenance.py` et vus echouer (7 sur 11) | `catalogue/validate.py`, `THOUSANDS` : un separateur (virgule, apostrophe, espace insecable) n'est ote que suivi d'exactement trois chiffres, derriere un entier. `check_provenance` : **44 verifications**, vert. Rejoue vert : catalogue, `validate_fiches`, `check_fiches_guard`, `score_extraction --check`, portes 07 et 08, 17 fiches `AMORCE` / 17, 17 moissonnees / 18 (la derniere pour `F4`). Aucune fiche ne reposait sur un faux accord. `D09` § Journal, `LECONS.md` `L28` : le faux refus avait deja pousse l'extracteur de la fiche crypto vers la soupape `spelled_out`. Reste ouvert : le signe moins `−` (U+2212). Registre 169 -> 169. |
| 2026-09-26 | `extraction` | **LES 11 FICHES MOISSONNEES SANS TRACE ONT ETE REFAITES PAR 11 SESSIONS ISOLEES.** Quatrieme point de la revue du jour : 18 fiches dans `corpus/fiches_harvest/`, 7 seulement dans `PRODUCED_harvest.json` — `G3` non mesurable pour 11 (`L22`), et `cryptocurrencies-and-momentum` cassait `F1`/`F3`. Protocole : anciennes fiches retirees du disque (elles restent dans l'historique git) AVANT le lancement, 11 consignes regenerees, 11 sessions en parallele ne lisant que leur consigne (limite `L26` inchangee : `CLAUDE.md` injecte), `--record` de chaque fiche AVANT tout `--judge`, verdict renvoye a la meme session en cas de refus | **12 essais pour 11 fiches** : 10 vertes au premier essai, `cryptocurrencies-and-momentum` au second — elle a contourne le bogue de `value_in_quote` (virgules collees, `17.71,18.22` -> `17.7118.22`) par un `spelled_out` recopiant le nombre de la citation, usage documente par `corpus/SCHEMA.md` mais qui fait de `spelled_out` la soupape de toute faille de `value_in_quote`. Etat : 18 fiches tracees, **17 vertes sur ce poste**. `bitcoin-is-not-the-new-gold` ne tient pas `F4` ici, volontairement : son PDF local ne rend pas le texte du manifeste, ce n'est pas le document qui fait foi, il n'a pas ete copie. 33 PDF promus copies dans `corpus/pdf/` apres controle d'empreinte ; `intraday-volatility-transmission` copie malgre des octets differents car son texte est identique au manifeste. Registre 169 -> 169. |
| 2026-09-26 | `decision` | **D29 — PAS DE PLIS EN PHASE 09 : UNE MESURE UNIQUE SUR TOUT LE `pool`.** Troisieme point de la revue du jour. `D04` renvoyait le nombre de plis du walk-forward a la phase 09 ; ni `D25` ni `gate_09` n'en parlaient. Un walk-forward protege d'un parametre AJUSTE sur les donnees ou on le juge ; en phase 09 rien ne l'est — constantes tirees de la fiche (`S5`), estimations au passe seulement (`S3`, resolution d'une barre depuis `D27`), ce qui est deja un walk-forward ancre a purge automatique | Chaque hypothese du lot est mesuree une fois, sur tout le `pool`, a `asof` = 2023-12-29 20:00 UTC : l'instant des 56 tests comptes, jusqu'ici simple convention, desormais exige par `gate_09.py` (`SLICE_REQUIRED`, `ASOF_REQUIRED` ; une mesure a un autre instant est hors protocole). `--check` : **21 verifications**, dont la fin de tranche relue dans le catalogue. Plis obligatoires au premier ajustement (phases 12-14). Sacrifies et ecrits : pas de diagnostic de stabilite par annee (a mettre au harnais avec `D26`/`D28`) ; le biais de publication, qu'aucun pli ne leverait — le holdout reste la seule mesure hors echantillon. Registre 169 -> 169. |
| 2026-09-26 | `decision` | **D28 — AUCUNE LIGNE DU REGISTRE NE TOUCHE LE LOT HORS DE SA MESURE OFFICIELLE.** Deuxieme point de la revue du jour. Une mesure faite par `evaluate()` sans `hypothesis_ref` est une calibration : elle ecrit sa ligne (invariant III tenu) mais `counted_tests()` l'ignore et `gate_09.py` ne cherchait que les lignes portant la `ref` d'une hypothese. Mesurer les signaux « en calibration », garder ceux qui plaisent et ne declarer qu'eux au lot aurait franchi la porte 09 sur un lot qui n'etait plus aveugle | `gate_09.py` : `lignes_hors_protocole()` refuse toute ligne portant le `signal_id` ou la `ref` d'une entree du lot sans en etre la mesure officielle (`09-passage`, harnais courant, `ref` et `signal_id` concordants). `--check` : 12 -> **19 verifications**, six fraudes fabriquees refusees. Branchement verifie hors depot sur un lot fabrique : propre -> FRANCHIE, avec une calibration du signal -> NON FRANCHIE. Consequence voulue : `H01`/`H02` ne peuvent pas entrer dans le lot. **Reste ouvert** : `registry.settle()` applique `extra` apres les champs du ticket et peut les ecraser — dans le harnais fige, a fermer dans la meme decision que l'integration des frais (`D26`). Registre 169 -> 169, harnais inchange. |
| 2026-09-26 | `correctif` | **LE TEST DE CAUSALITE LAISSAIT PASSER UNE BARRE DE FUTUR — `D27`.** Trouve en revue du depot. Les barres sont horodatees a leur OUVERTURE (`ts_event` Databento ; verifie sur `CL` : derniere barre 16:59 avant l'arret quotidien, premiere 18:00), et `sandbox/causality.py` tronquait a `t + 1 min` : le panel tronque gardait la barre `t+1`. Un tricheur lisant `close[t+1]` a passe **14 sondes sur 16** de la porte 05, attrape seulement sur `6A x US` et `6B x US` ou la barre suivante manquait. Enjeu : a 30 barres, une minute d'avance correle ~0,18 avec la cible, dix fois l'IC que cherche `D01` | Troncature a `t` ; quatrieme tricheur `tainted-next-bar` exige attrape a CHAQUE sonde (16/16, contre 2/16 avant). Rejoue : porte 05 franchie (32 verifications), porte 08 franchie (`S3` tenue), `check_signals` 261 verifications. `sandbox/` est hors de `harness/` : empreinte inchangee `9ac3e45e`, registre 169 -> 169, **aucune ligne perimee**. `LECONS.md` `L27`. |
| 2026-09-25 | `correctif` | **LE JUGE NOMME SA FAUTE AU LIEU DE LEVER** — `corpus/score_extraction.py`. Trois sites supposaient que chaque entree de `reported_results` est un objet : `check_f2`, `check_f3` et `diagnose`. Un modele ayant rendu deux entrees en JSON DOUBLEMENT ENCODE (des chaines), `res.get(...)` levait `AttributeError` | CE QUE LA PANNE COUTAIT, ET C'EST LE VRAI SUJET : la fiche etait deja rejetee (code non nul), mais **AUCUNE condition n'etait nommee** — un appelant qui compte les conditions cassees en trouvait ZERO et ecrivait « aucune condition cassee » SOUS UN REJET. `L24` exactement : un controle qui porte sur autre chose que ce qu'il annonce. ET `F1` ATTRAPAIT DEJA LA FAUTE : on ne la voyait jamais parce que `F2` plantait avant d'avoir imprime quoi que ce soit. LE DIAGNOSTIC NE DOIT JAMAIS FAIRE TOMBER LE VERDICT : il est imprime et ne conditionne rien (`D16` § Pourquoi), mais en levant il emportait les cinq conditions avec lui. Il ignore desormais les entrees mal formees — `F2` et `F3` les refusent et le DISENT. Le compte `n_results` porte toujours sur TOUT ce que la fiche declare : masquer une entree mal formee ferait mentir le compte (`L21`). **RIEN N'EST ASSOUPLI, ET C'EST VERIFIE** : le cas etait deja refuse, il est maintenant refuse AVEC SA RAISON, aucun seuil ne bouge. Non-regression complete — les **23 fiches reelles** rendent des verdicts **identiques** (figes avant le correctif, compares apres), les **32 verifications** du juge passent, les **31** du garde des fiches aussi, et la **porte 07 reste FRANCHIE**. TROISIEME SITE TROUVE APRES COUP : j'avais corrige `check_f2` et `check_f3` puis relance, et `diagnose` a plante a son tour — un `grep` de TOUS les sites d'un coup l'aurait donne du premier geste. C'est la lecon de la journee sous un quatrieme visage |

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
