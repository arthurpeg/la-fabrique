---
type: hub
updated: 2026-09-18
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-18.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 07 — triage et extraction sur 20 papiers connus |
| **Dernière porte franchie** | **06**, le 2026-09-18 — les deux clauses. Clause 1 (dégénérescence) : `gate_06_controls.py`, 25 vérifications. Clause 2 (réplication) : `scripts/measure_h04.py`, 19 vérifications, `H04` pré-enregistrée |
| **Décision la plus récente** | `decisions/DECISION-13-ce-que-la-clause-2-peut-etre.md` — après l'échec de deux cibles, la clause 2 est satisfaite quand **la chaîne reproduit un fait publié sur |
| **Tests au registre** | 130 |
| **Idées abandonnées recensées** | 34 |
| **Entrées au journal** | 23 |

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
   renseignée à la main sur 24 entrées : **c'est le verdict humain de référence**,
   et il existe déjà. Il a été écrit en phase 01, avant tout ce qui suit, donc
   sans connaître les résultats — ce qui en fait un étalon honnête.

### Ce qu'il faudra trancher par écrit avant de coder

- **Le schéma de fiche.** Les trois fiches manuelles ne suivent pas exactement la
  même structure ; l'une porte `incompatibilities`, une autre `transposability`.
  Un schéma versionné doit être écrit, et `D09` étendu aux fiches : une valeur
  recopiée d'un papier est une **valeur externe**, et elle devrait porter sa
  citation comme les valeurs du catalogue.
- **Ce que « le triage écarte ce qu'il doit écarter » veut dire en chiffres** —
  rappel et précision contre la colonne d'`AMORCE.md`, avec un seuil écrit avant
  de mesurer. `L06` s'applique mot pour mot : *un compte juste n'est pas un compte
  de choses justes*.

### Ce qui reste ouvert par ailleurs

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
  qu'affaiblir un motif déjà absent. Noté plutôt que payé.

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-18 | `gate` | PORTE 06 FRANCHIE — les deux clauses. D13 écrite AVANT la mesure (comme H03 l'exigeait) : après l'échec de deux cibles, la clause 2 est satisfaite quand la CHAÎNE reproduit un fait publié sur nos données, et non quand le harnais d'IC reproduit un IC publié. Cible : Andersen & Bollerslev (1997), papier récupéré, lu, fiché ; H04 pré-enregistrée ; scripts/measure_h04.py écrit dans scripts/ et NON dans harness/ — y ajouter un fichier périmerait les 56 lignes comptées | 19 vérifications, LES QUATRE CLAUSES TIENNENT : forme en U sur NQ/ES/YM, ouverture et clôture au-dessus du milieu, creux au milieu de séance, rapports sommet/creux 2,05 / 1,74 / 1,89 tous dans [1,4 ; 3,0] écrit d'avance — et ES x US, LE MÊME CONTRAT que leur figure, rend 1,74 contre leur 1,91 trente ans plus tard ; AUCUN IC calculé, counted_tests reste à 56. Deux défauts trouvés par le premier passage de l'instrument : (1) le garde interdisait aux paires d'autocorrélation d'enjamber la séance, ce qu'un décalage à la fréquence journalière fait PAR DÉFINITION — la clause C n'était pas mesurée et le script concluait quand même « les quatre clauses tiennent » ; (2) le témoin de la clause C était placé à ±15/30 min du multiple, presque à la MÊME PHASE du cycle : écart +0,006 à +0,010, contre +0,046 à +0,068 à phase opposée (diagnostic non pré-enregistré). La clause mesurait un PLANCHER de l'effet. L16 ; phase courante = 07 |
| 2026-09-18 | `mesure` | H03 MESURÉE — 52 décalages (40 dents m=1..40, 12 creux j=1..12), tranche pool, as-of 2023-12-29, 25 cellules, ~650 000 observations par décalage, harnais 9ac3e45e ; counted_tests 4 -> 56 pour UNE hypothèse | LE PEIGNE N'EST PAS LÀ. Le script annonçait « séparation OUI » (+0,00177, p=0,030) et il avait tort : les seaux de H03 SE RECOUVRAIENT — creux j=1..12 contenant le retournement court j=1..3. Creux nettoyés (j=4..12) : dents +0,00065 contre creux +0,00056, séparation +0,00009, Mann-Whitney p=0,247. Aucune dent ne ressort : plus grand t +3,01 sur 40, quand la sélection seule rend un 95e centile de 3,22. Entre les multiples la réponse n'est pas « largement négative » : 5 positives sur 9. SEUL effet net : le retournement court, j=1 IC -0,01150 t -6,14 et j=2 -0,00815 t -4,35 — la préface du motif, pas le motif. CLAUSE 2 DE LA PORTE 06 NON FRANCHIE, comme H03 l'avait écrit d'avance ; il faut une nouvelle cible par décision écrite. Non vérifié faute de l'avoir inscrit : la ventilation par cellule (défaut du script, coûterait 52 lignes de plus et ne pourrait qu'affaiblir le motif). L15, F33, F34 |
| 2026-09-18 | `signal` | Signal heston-2010-periodicity implémenté à la main (signals/heston_2010_periodicity.py) : un score par intervalle de demi-heure et non un par séance — le mécanisme de _common.run ne convenait pas et n'est pas réutilisé ; décalage paramétré EN SÉANCES pour les dents (traduit en intervalles par fenêtre depuis le catalogue) et EN INTERVALLES pour les creux ; rendement d'intervalle défini en BARRES, même définition que la cible du harnais ; scripts/check_heston.py et scripts/measure_h03.py écrits, H03 précisée sur ce point AVANT le lancement | contrôles verts : périodes P = 16/13/13 lues au catalogue et non espérées, liste blanche 0 refus, contrat conforme, CAUSALITÉ 0 divergence sur 16 sondes, écart d'échantillonnage mesuré à 30,0 barres donc étalement 1,00 — pas de déflation de recouvrement, ce que D11 doit faire pour des demi-heures disjointes ; pré-vol : 658 582 scores et 657 470 observations à m=1, soit 99,8 % de mesurabilité, aucune cellule mince ; le signal est tenu HORS de REFERENCE (les étalons de D06) et placé dans REPLICATION, pour que les portes gardent le sujet que D06 leur a donné |
| 2026-09-18 | `decision` | D12 écrite — la clause 2 CHANGE DE CIBLE : Mesfin ne convient pas (son critère est un t sur des rendements nets par trade, le nôtre un IC ; onze de ses quatorze familles échouent par amplitude sous friction, ce qu'un IC ne voit pas ; et deux de ses trois plis hors échantillon tombent dans le holdout scellé). Nouvelle cible : Heston, Korajczyk & Sadka (2010), JF 65(4) — papier récupéré d'arXiv (1005.3535), lu, fiché ; H03 PRÉ-ENREGISTRÉE avant toute mesure | le résultat visé est une CORRÉLATION et un MOTIF DE SIGNES, pas une valeur : continuation aux décalages multiples d'une séance (dents), retournement aux premiers décalages, rien de positif entre les deux (creux) — le peigne porte son propre témoin négatif ; période dictée par le catalogue et non par le résultat : P = 13 demi-heures pour US et EUROPE (6,5 h), P = 16 pour ASIA (8 h), donc DEUX motifs distincts à retrouver ; aucune magnitude du papier n'est reprise comme attendue (sa mesure est transversale avec effet de marché retiré, il le dit lui-même) ; H03 = UNE hypothèse pour ~100 lignes de registre, et l'échec du motif ne franchirait PAS la porte — écrit avant de regarder ; Mesfin reste calibrage d'attente, fiché |
| 2026-09-18 | `research` | Mesfin (2026) LU — PDF récupéré d'arXiv dans corpus/pdf/, texte extrait, fiche écrite à la main dans corpus/fiches/ (première fiche du projet, hors extracteur qui n'existe pas) ; corpus/AMORCE.md corrigé par une note datée, le texte d'origine conservé | les 14 familles nommées depuis la source (ORB x3, Asia expansion, Asia liquidity grab, gap fill, gap continuation, volume spike, volume dry-up, VVG x3, event day trend, MGC OU) ; sa friction CITÉE : « 2.0 points ($4.00 per micro contract), covering bid-ask spread, NinjaTrader exchange fees, and conservative slippage » — TOUT COMPRIS, et 4,00 $ sur 29 376 $ de notionnel = 1,36 bp, seconde route confirmant L14 ; DEUX OBSTACLES STRUCTURELS à la réplication, aucun lié aux frais : (1) son critère est un t sur RENDEMENTS NETS PAR TRADE, le nôtre un IC — onze familles échouent par amplitude sous friction, ce qu'un IC ne voit pas ; (2) ses plis hors échantillon testent 2023/2024/2025 et le holdout scellé couvre 2024-2026, donc SEUL LE PLI 1 est reproductible |
| 2026-09-18 | `audit` | Prémisse de la clause 2 vérifiée au lieu d'être citée — scripts/check_mesfin_premise.py, NQ tranche pool 2021-01-01 -> 2023-12-31 (le reste de la fenêtre de Mesfin est dans le holdout scellé), aucun IC, aucun test dépensé | LA PRÉMISSE NE TIENT PAS : 2 points d'indice valent 1,36 bp à la médiane NQ mesurée (14 688), pas les « 8 à 15 bp » écrits dans wiki/research/mesfin-2026-falsification depuis le 2026-09-16 — erreur d'un FACTEUR 10 ; sa friction vaut 1,7x notre plancher NQ x US (0,79) et 0,9x notre pire cellule (1,55), en comparant son coût TOUT COMPRIS à notre écart SEUL ; son verdict est TRANSPORTABLE et la réserve du projet tombe ; la plage « 13 000 à 25 000 » citée comme mesurée chez nous ne correspond pas au pool (c99 = 17 556) ; page corrigée (la source gagne), L14, F31, F32 |
| 2026-09-18 | `decision` | D11 écrite et appliquée — la déflation de recouvrement se MESURE : facteur = sqrt(n / n_eff) avec n_eff = somme des n_c / max(1, h / écart_c), l'écart_c étant l'écart médian en barres entre deux observations de la cellule ; CellIC porte sampling_gap_bars, le rapport dit l'écart mesuré ; deux assertions périmées corrigées dans les portes 03 et 06 (elles exigeaient counted_tests == 0, vrai avant H01/H02 et faux depuis — elles vérifient désormais que LA PORTE ne dépense rien) | découvert à partir d'une question sur les anomalies mono-actif ; H01 et H02 scorent une fois par séance, observations espacées de 415 barres pour un horizon de 30, AUCUN recouvrement — le harnais leur retirait un facteur 5,48 ; empreinte e9ef2087 -> 9ac3e45e, portes 03/04/05/06 rejouées vertes, H01 et H02 REMESURÉES : IC inchangés (-0,01061 et -0,00432), t final -0,28 -> -1,56 et -0,11 -> -0,63, CONCLUSION INCHANGÉE (les deux sous 2) ; counted_tests 2 -> 4 pour DEUX hypothèses — la phase 15 compte des hypothèses, pas des lignes ; tests de référence T-20260918T065822-2b3e5d et T-20260918T070041-18cf25 ; L13, F29, F30 |
| 2026-09-18 | `mesure` | H01 ET H02 MESURÉES — les deux premiers tests comptés du projet ; scripts/measure_h01_h02.py, tranche pool, as-of 2023-12-29, 25 cellules, ~45 900 observations chacune, harnais e9ef2087 ; pré-vol d'abord (scores et mesurabilité 89,9 %, aucune cellule sous les seuils, AUCUN IC) | counted_tests 0 -> 2 ; H01 IC -0,01061 t final -0,28, H02 IC -0,00432 t final -0,12 : signe négatif contre signe positif attendu, mais la clause qui s'applique est « t final sous 2 : rien à distinguer du bruit » — NON CONFIRMÉES, PAS RETOURNÉES ; H02 s'annonçait au moins aussi forte que H01 et est plus faible ; la DOUBLE DÉFLATION de D04 mord pour la première fois — t naïf -2,27 (significatif à 5 % sans précaution) devient -0,28, facteur 8 ; garde ajouté au script contre une ré-exécution ; ouverture notée à ETAT : répliquer un résultat NÉGATIF ne demande que la direction négative, donc la clause 2 est peut-être bloquée par le budget de tests et non par fee_bp |

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
