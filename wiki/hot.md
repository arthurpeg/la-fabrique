---
type: hub
updated: 2026-09-19
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-19.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 07 — triage et extraction sur 20 papiers connus |
| **Dernière porte franchie** | **06**, le 2026-09-18 — les deux clauses. Clause 1 (dégénérescence) : `gate_06_controls.py`, 25 vérifications. Clause 2 (réplication) : `scripts/measure_h04.py`, 19 vérifications, `H04` pré-enregistrée |
| **Décision la plus récente** | `decisions/DECISION-15-seuil-du-triage.md` — le seuil du trieur, écrit **avant** que le trieur existe : appariement entrée par entrée à la colonne |
| **Tests au registre** | 135 |
| **Idées abandonnées recensées** | 42 |
| **Entrées au journal** | 26 |

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

### Prochaine action : un trieur NON CONTAMINÉ, et un seul passage

**La condition que `D15` ne portait pas, et que la mise en œuvre a trouvée** :
une session qui a **lu la colonne** ne peut pas être le trieur. Elle ne trierait
pas, elle réciterait — et sa matrice serait parfaite pour la pire des raisons
(`L15` : le résultat conforme est celui que personne n'examine). La session du
2026-09-19 s'est **disqualifiée elle-même** à ce titre : elle a compté la colonne
entrée par entrée pour établir le dénominateur de `D15`.

Le piège est **structurel** : la séquence de démarrage de `CLAUDE.md` conduit
toute session à lire `ETAT.md`, le wiki, puis le corpus — donc l'étalon. **Une
session arrive contaminée par défaut, et celle-ci l'est dès qu'elle a lu ce
paragraphe.**

Donc, concrètement : le trieur est une session ou un agent qui **n'a vu ni la
colonne, ni le § Verdict d'`AMORCE.md`, ni `D15` § Sur l'étalon, ni la présente
section**. Il reçoit `corpus/triage_input.json`, la règle de classement et nos
contraintes de données — tout est dans `corpus/TRIAGE.md` — et rend un JSON de
20 verdicts **avec un motif chacun**. Puis :

```
python corpus/score_triage.py verdicts.json
```

**Le premier passage fait foi.** Un trieur retouché après lecture de sa matrice
est un trieur ajusté à son étalon. Tout passage s'inscrit au § Journal de `D15`
avec **qui a trié, ce qu'il avait vu**, et ce qui a changé depuis le précédent ;
le verdict final cite le nombre de passages — comme la phase 15 citera
`counted_tests()`.

Et la garde de `L06`, qui s'applique mot pour mot : *un compte juste n'est pas un
compte de choses justes*. C'est ainsi que la détection de roulements avait paru
bonne à 90 % en n'étant juste qu'à 62,8 % — d'où la matrice entière, et le motif
exigé de chaque verdict.

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

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-19 | `outil` | Phase 07, l'entrée du trieur et son protocole : corpus/make_triage_input.py fabrique déterministiquement corpus/triage_input.json (les 20 lignes d'AMORCE.md privées de leur colonne verdict, TITRES DE SECTION NON REPRIS — le titre E dit « la famille que mes données ferment », c'est le verdict lui-même) et l'audite ; corpus/TRIAGE.md pose le protocole ; D15 reçoit un § Complément daté, écrit AVANT tout passage | LA MISE EN ŒUVRE A TROUVÉ UNE CONDITION QUE D15 NE PORTAIT PAS : une session qui a LU la colonne ne peut pas être le trieur — elle réciterait, et sa matrice serait parfaite pour la pire des raisons (L15 : le résultat conforme est celui que personne n'examine). Le piège est structurel — la séquence de démarrage de CLAUDE.md conduit toute session à lire l'étalon, donc une session arrive CONTAMINÉE PAR DÉFAUT. La session du jour s'est disqualifiée elle-même comme trieur (F42) plutôt que de produire un résultat flatteur. Ce n'est pas une impossibilité par construction — on n'empêche pas un lecteur de lire, et F13/F15/F16/F25 ont déjà refusé la vigilance déguisée en architecture — donc la règle est ÉCRITE et le § Journal de D15 note pour chaque passage qui a trié et ce qu'il avait vu. État : entrée fabriquée et auditée (20 entrées, 3 à 5 champs selon la section), juge vert sur 10 vérifications, IL MANQUE UN TRIEUR NON CONTAMINÉ |
| 2026-09-19 | `decision` | D15 écrite AVANT que le trieur existe : le seuil du triage, en EFFECTIFS et non en pourcentages (sur 13 `oui`, un item vaut 7,7 points de rappel — un seuil en % est un effectif mal déguisé, F37) ; trois classes et matrice de confusion entière, `partiel` NON replié (le replier effacerait la distinction qui a écarté Mesfin et cadré Heston, F38) ; quatre conditions — A ≤ 1 `oui` manqué sur 13, B = 0 `non` promu `oui`, C ≤ 2 `partiel` en désaccord sur 5, D = 0 désaccord de deux crans ; ce que le trieur VOIT est fixé : la ligne d'AMORCE.md privée de sa colonne verdict, exactement ce que l'auteur humain avait en phase 01, pas le PDF (F41) ; corpus/score_triage.py écrit et vérifié avant l'accusé | L'ÉTALON A DÛ ÊTRE COMPTÉ AVANT D'ÊTRE UTILISÉ, et il ne l'avait pas été : ETAT.md annonçait 24 entrées notées et six `partiel`, la colonne en porte 20 — 13 `oui` / 5 `partiel` / 2 `non`, les 4 entrées de la section G n'ayant pas cette colonne ; et AMORCE.md se contredisait lui-même — son § Verdict compte 12/5/3, l'écart portant sur l'entrée 9 (billet FRBNY), que la colonne marque `oui` et que le résumé range parmi les fermées. D15 tranche que LA COLONNE FAIT FOI (F39), l'entrée 9 n'est pas retirée (F40), et le § Verdict reçoit une note datée — texte d'origine conservé, comme pour l'entrée 7. score_triage.py : 10 vérifications vertes, huit sorties de trieur fabriquées rendant chacune le verdict que D15 écrit, et deux mutations d'AMORCE.md que le garde de l'étalon refuse. Le premier passage du trieur fera foi ; tout passage ultérieur s'inscrit au § Journal de D15 avec ce qui a changé. ETAT.md, hypotheses/README.md (counted_tests disait encore 4 pour deux hypothèses, c'est 56 pour trois) et la page de phase corrigés. Six portes rejouées vertes ce jour ; registre 130 -> 135 lignes, toutes des calibrations, counted_tests inchangé à 56 |
| 2026-09-18 | `decision` | Phase 07, premier maillon : D14 écrite — le schéma de fiche n'est PAS tiré des trois fiches manuelles (elles divergent, F35) mais des six champs que CLAUDE.md § Le vocabulaire nomme depuis le premier jour, plus source et transposability ; corpus/SCHEMA.md, corpus/validate_fiches.py, corpus/check_fiches_guard.py ; D09 étendu aux fiches — un résultat recopié d'un papier est une VALEUR EXTERNE, il porte sa citation, et value_in_quote (le garde du catalogue) vérifie que la valeur s'y retrouve | les trois fiches manuelles REFUSÉES par leur propre schéma puis réécrites — c'était le test du schéma autant que des fiches ; aucune n'avait de champ `horizon`, la construction du signal portait deux noms différents ; le garde a attrapé un cas réel que je n'avais pas prévu — Mesfin écrit « Eleven signal families fail » en toutes lettres, donc aucun chiffre à retrouver : ajouté `spelled_out`, qui vérifie le MOT et NOMME la conversion comme un geste humain plutôt que de la cacher derrière `derived` (F36) ; check_fiches_guard.py : 23 vérifications, 11 fautes refusées chacune pour la raison prévue, fiche intacte acceptée ; reste la seconde moitié de la porte 07 — le triage, avec un seuil chiffré à écrire AVANT mesure (L06) |
| 2026-09-18 | `gate` | PORTE 06 FRANCHIE — les deux clauses. D13 écrite AVANT la mesure (comme H03 l'exigeait) : après l'échec de deux cibles, la clause 2 est satisfaite quand la CHAÎNE reproduit un fait publié sur nos données, et non quand le harnais d'IC reproduit un IC publié. Cible : Andersen & Bollerslev (1997), papier récupéré, lu, fiché ; H04 pré-enregistrée ; scripts/measure_h04.py écrit dans scripts/ et NON dans harness/ — y ajouter un fichier périmerait les 56 lignes comptées | 19 vérifications, LES QUATRE CLAUSES TIENNENT : forme en U sur NQ/ES/YM, ouverture et clôture au-dessus du milieu, creux au milieu de séance, rapports sommet/creux 2,05 / 1,74 / 1,89 tous dans [1,4 ; 3,0] écrit d'avance — et ES x US, LE MÊME CONTRAT que leur figure, rend 1,74 contre leur 1,91 trente ans plus tard ; AUCUN IC calculé, counted_tests reste à 56. Deux défauts trouvés par le premier passage de l'instrument : (1) le garde interdisait aux paires d'autocorrélation d'enjamber la séance, ce qu'un décalage à la fréquence journalière fait PAR DÉFINITION — la clause C n'était pas mesurée et le script concluait quand même « les quatre clauses tiennent » ; (2) le témoin de la clause C était placé à ±15/30 min du multiple, presque à la MÊME PHASE du cycle : écart +0,006 à +0,010, contre +0,046 à +0,068 à phase opposée (diagnostic non pré-enregistré). La clause mesurait un PLANCHER de l'effet. L16 ; phase courante = 07 |
| 2026-09-18 | `mesure` | H03 MESURÉE — 52 décalages (40 dents m=1..40, 12 creux j=1..12), tranche pool, as-of 2023-12-29, 25 cellules, ~650 000 observations par décalage, harnais 9ac3e45e ; counted_tests 4 -> 56 pour UNE hypothèse | LE PEIGNE N'EST PAS LÀ. Le script annonçait « séparation OUI » (+0,00177, p=0,030) et il avait tort : les seaux de H03 SE RECOUVRAIENT — creux j=1..12 contenant le retournement court j=1..3. Creux nettoyés (j=4..12) : dents +0,00065 contre creux +0,00056, séparation +0,00009, Mann-Whitney p=0,247. Aucune dent ne ressort : plus grand t +3,01 sur 40, quand la sélection seule rend un 95e centile de 3,22. Entre les multiples la réponse n'est pas « largement négative » : 5 positives sur 9. SEUL effet net : le retournement court, j=1 IC -0,01150 t -6,14 et j=2 -0,00815 t -4,35 — la préface du motif, pas le motif. CLAUSE 2 DE LA PORTE 06 NON FRANCHIE, comme H03 l'avait écrit d'avance ; il faut une nouvelle cible par décision écrite. Non vérifié faute de l'avoir inscrit : la ventilation par cellule (défaut du script, coûterait 52 lignes de plus et ne pourrait qu'affaiblir le motif). L15, F33, F34 |
| 2026-09-18 | `signal` | Signal heston-2010-periodicity implémenté à la main (signals/heston_2010_periodicity.py) : un score par intervalle de demi-heure et non un par séance — le mécanisme de _common.run ne convenait pas et n'est pas réutilisé ; décalage paramétré EN SÉANCES pour les dents (traduit en intervalles par fenêtre depuis le catalogue) et EN INTERVALLES pour les creux ; rendement d'intervalle défini en BARRES, même définition que la cible du harnais ; scripts/check_heston.py et scripts/measure_h03.py écrits, H03 précisée sur ce point AVANT le lancement | contrôles verts : périodes P = 16/13/13 lues au catalogue et non espérées, liste blanche 0 refus, contrat conforme, CAUSALITÉ 0 divergence sur 16 sondes, écart d'échantillonnage mesuré à 30,0 barres donc étalement 1,00 — pas de déflation de recouvrement, ce que D11 doit faire pour des demi-heures disjointes ; pré-vol : 658 582 scores et 657 470 observations à m=1, soit 99,8 % de mesurabilité, aucune cellule mince ; le signal est tenu HORS de REFERENCE (les étalons de D06) et placé dans REPLICATION, pour que les portes gardent le sujet que D06 leur a donné |
| 2026-09-18 | `decision` | D12 écrite — la clause 2 CHANGE DE CIBLE : Mesfin ne convient pas (son critère est un t sur des rendements nets par trade, le nôtre un IC ; onze de ses quatorze familles échouent par amplitude sous friction, ce qu'un IC ne voit pas ; et deux de ses trois plis hors échantillon tombent dans le holdout scellé). Nouvelle cible : Heston, Korajczyk & Sadka (2010), JF 65(4) — papier récupéré d'arXiv (1005.3535), lu, fiché ; H03 PRÉ-ENREGISTRÉE avant toute mesure | le résultat visé est une CORRÉLATION et un MOTIF DE SIGNES, pas une valeur : continuation aux décalages multiples d'une séance (dents), retournement aux premiers décalages, rien de positif entre les deux (creux) — le peigne porte son propre témoin négatif ; période dictée par le catalogue et non par le résultat : P = 13 demi-heures pour US et EUROPE (6,5 h), P = 16 pour ASIA (8 h), donc DEUX motifs distincts à retrouver ; aucune magnitude du papier n'est reprise comme attendue (sa mesure est transversale avec effet de marché retiré, il le dit lui-même) ; H03 = UNE hypothèse pour ~100 lignes de registre, et l'échec du motif ne franchirait PAS la porte — écrit avant de regarder ; Mesfin reste calibrage d'attente, fiché |
| 2026-09-18 | `research` | Mesfin (2026) LU — PDF récupéré d'arXiv dans corpus/pdf/, texte extrait, fiche écrite à la main dans corpus/fiches/ (première fiche du projet, hors extracteur qui n'existe pas) ; corpus/AMORCE.md corrigé par une note datée, le texte d'origine conservé | les 14 familles nommées depuis la source (ORB x3, Asia expansion, Asia liquidity grab, gap fill, gap continuation, volume spike, volume dry-up, VVG x3, event day trend, MGC OU) ; sa friction CITÉE : « 2.0 points ($4.00 per micro contract), covering bid-ask spread, NinjaTrader exchange fees, and conservative slippage » — TOUT COMPRIS, et 4,00 $ sur 29 376 $ de notionnel = 1,36 bp, seconde route confirmant L14 ; DEUX OBSTACLES STRUCTURELS à la réplication, aucun lié aux frais : (1) son critère est un t sur RENDEMENTS NETS PAR TRADE, le nôtre un IC — onze familles échouent par amplitude sous friction, ce qu'un IC ne voit pas ; (2) ses plis hors échantillon testent 2023/2024/2025 et le holdout scellé couvre 2024-2026, donc SEUL LE PLI 1 est reproductible |

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
