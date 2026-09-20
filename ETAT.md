# ÉTAT

**Phase courante :** 07 — triage et extraction sur 20 papiers connus
**Date de dernière mise à jour :** 2026-09-20
**Dernière porte franchie :** **06**, le 2026-09-18 — les deux clauses.
Clause 1 (dégénérescence) : `gate_06_controls.py`, 25 vérifications. Clause 2
(réplication) : `scripts/measure_h04.py`, 19 vérifications, `H04` pré-enregistrée
puis mesurée — la forme en U de la volatilité intra-journalière est retrouvée sur
`NQ`, `ES` et `YM`, avec un rapport sommet/creux de **1,74 à 2,05** contre
**1,91** chez Andersen & Bollerslev (1997) sur le même contrat.

**Ce que la porte 06 valide, et rien de plus.** La **chaîne de données** et la
discipline de mesure. **Pas le harnais d'IC**, qui reste garanti par sa seule
calibration à la main (porte 03). `D13` § Pourquoi l'écrit sans détour, et aucune
session ne doit lire cette porte comme davantage.

**Décision la plus récente :**
`decisions/DECISION-15-seuil-du-triage.md` — le seuil du trieur, écrit **avant**
que le trieur existe : appariement entrée par entrée à la colonne
« implémentable » d'`AMORCE.md` (20 entrées, 13 `oui` / 5 `partiel` / 2 `non`),
trois classes, quatre conditions en **effectifs** et non en pourcentages.
**Décisions pertinentes pour la phase courante :** `D14` (le schéma de fiche),
`D06` (les fiches écrites à la main sont un banc d'essai, pas le produit de la
phase 07) et `D09` (la provenance des valeurs externes, étendue aux fiches).
`D13` reste la référence pour ce que la porte 06 valide — et ne valide pas.

**Les tests comptés :** `counted_tests()` vaut **56 pour trois hypothèses** —
`H01` et `H02` (deux lignes chacune : mesure puis reprise sous `D11`), `H03`
(52 lignes, un seul motif prédit). `H04` n'a produit **aucun IC** et n'a rien
coûté. **Les trois hypothèses mesurées sont sans résultat.**

> Ce fichier est lu en premier par chaque session et mis à jour en dernier.
> Les phases ci-dessous suivent **l'ordre de construction** (le juge avant
> l'accusé), pas l'ordre d'exécution de la chaîne. Voir `CLAUDE.md`, « Les deux
> ordres ».

---

## Acte I — Le socle

| # | Phase | Porte | État |
|---|---|---|---|
| 01 | La décision données | `decisions/DECISION-01` fixe univers, grille, métrique, tranches ; `gate_01_pit.py` passe. | **franchie 2026-09-15** |
| 02 | Le Panel point-in-time | Un panel se charge, est reproductible ; aucune ligne n'est visible avant son horodatage ; la série ajustée à rebours n'utilise que les recollements ≤ t (D01 §6). | **franchie 2026-09-17** — `gate_02_panel.py`, 103 vérifications sur les 9 instruments |
| 03 | Le harnais d'IC calibré à la main | Le harnais reproduit à la main, sur un cas connu, un IC vérifié indépendamment. IC en série temporelle poolé, statistique robuste à la corrélation transversale, modèle de coûts par cellule (D01 §2 et §7). Figé et versionné à partir de là. | **franchie 2026-09-17** — `gate_03_harness.py`, 41 vérifications |
| 04 | Le registre et le verrou du holdout | Aucun chemin de code ne produit un IC sans écrire au registre ; la tranche `holdout` (2024-01-01 → 2026-08-28) est inaccessible par construction. | **franchie 2026-09-17** — `gate_04_registry.py`, 1 933 vérifications, `D05` |

## Acte II — Automatiser le jugement

| # | Phase | Porte | État |
|---|---|---|---|
| 05 | API de signal, sandbox, test de causalité | Un signal qui tente de lire le futur échoue au test de causalité, automatiquement. | **franchie 2026-09-17** — `gate_05_signal_api.py`, 3 tricheurs sur 3 attrapés, `D07` |
| 06 | Contrôles automatiques et réplication | Un signal dégénéré est rejeté avant le harnais ; la chaîne reproduit un fait publié sur nos données. La cible a changé deux fois : Mesfin (métrique incompatible, `D12`), Heston (motif absent, `H03`), puis Andersen & Bollerslev (`D13`). | **franchie 2026-09-18** — `gate_06_controls.py` (25) et `scripts/measure_h04.py` (19) |
| 07 | Triage et extraction sur 20 papiers connus | 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict humain de référence. Point de départ : `corpus/AMORCE.md`. | **PHASE COURANTE, NON FRANCHIE** — moitié **triage** tenue au **passage 1** du 2026-09-20 (A/B/C/D = 1/0/2/0, deux conditions à leur maximum exact) ; moitié **extraction** bloquée sur l'acquisition, 3 PDF pour 20 fiches |
| 08 | Le codeur de signal | Une fiche produit un signal exécutable qui passe la sandbox, sans retouche manuelle. | à faire |

## Acte III — Fermer la boucle une fois

| # | Phase | Porte | État |
|---|---|---|---|
| 09 | Premier passage complet sur 30 à 50 papiers | La chaîne tourne de bout en bout ; le registre compte tous les tests ; un rapport d'IC existe pour chaque signal. | à faire |
| 10 | Une stratégie, un backtest | Un signal survivant devient une stratégie backtestée. Une décision écrite fixe l'attache du moteur tiers — ou, s'il n'est pas arrivé, requalifie la phase en « construire un moteur » (3 à 5 semaines estimées, D01). | à faire |

## Acte IV — Étendre par risque croissant

| # | Phase | Porte | État |
|---|---|---|---|
| 11 | Taxonomie data-driven | Les familles de signaux sont déduites des données, pas postulées. | à faire |
| 12 | Combinaisons | Toute combinaison testée a une hypothèse écrite et horodatée avant son résultat. | à faire |
| 13 | Régimes | Idem pour les hybrides. Le nombre de régimes est justifié, pas ajusté après coup. | à faire |
| 14 | Générateur d'hypothèses | Le générateur s'alimente de `LECONS.md` et du registre ; ses propositions passent les mêmes portes. | à faire |
| 15 | Le holdout | Ouvert une fois. Sharpe dégonflé du nombre de tests du registre. Fin. | à faire |

---

## Ce qui bloque, et qui n'est pas de notre ressort

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action

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

### Prochaine action : l'extraction, ou la requalification de la porte

La moitié qui reste est l'**extraction**, et elle ne bute pas sur du code mais
sur l'**acquisition** : **3 PDF sur disque pour 20 fiches demandées**. La
question à trancher **par écrit, et pas au quinzième papier** : élargir le corpus
au-delà d'`AMORCE.md`, ou requalifier ce que la porte 07 demande.

### Ce qui reste ouvert par ailleurs

- **l'extraction** — l'autre moitié de la porte 07 — bute sur l'**acquisition** :
  **3 PDF** sur disque pour **20 fiches** demandées. Des 20 entrées notées, 12 ont
  un lien libre, 2 sont derrière un péage (16, 17), et **6 n'ont aucun lien**
  (6, 10, 14, 18, 19, 20 — la 14 étant en outre citée de mémoire, non vérifiée).
  Que devient la porte si les 20 fiches ne sont pas atteignables depuis
  `AMORCE.md` ? Élargir le corpus, ou requalifier la porte — **par écrit, et pas
  au quinzième papier** ;
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
