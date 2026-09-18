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
| **Phase courante** | 06 — contrôles automatiques et réplication (**ouverte, non franchie**) |
| **Dernière porte franchie** | **05**, le 2026-09-17 — `scripts/gate_05_signal_api.py`, 29 vérifications. Les trois look-ahead injectés (`sandbox/tainted.py`) sont |
| **Décision la plus récente** | `decisions/DECISION-12-cible-de-replication.md` — la clause 2 de la porte 06 |
| **Tests au registre** | 77 |
| **Idées abandonnées recensées** | 32 |
| **Entrées au journal** | 21 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action — reflet de `ETAT.md`

### 0. ~~Le défaut d'empreinte du harnais~~ — **réparé le 2026-09-18**

`registry.code_hash()` empreintait les **octets sur disque** de `harness/*.py`,
fins de ligne comprises : le même harnais a porté quatre numéros sur deux postes
sans qu'une ligne de code bouge, et `gate_04` annonçait 53 lignes périmées qui ne
l'étaient pas. Vérifié en reproduisant les trois empreintes historiques à partir
des mêmes blobs git.

Réparé par `D10`, en deux gestes : `.gitattributes` fixe `* text=auto eol=lf`
(la cause, côté dépôt) et l'empreinte replie les fins de ligne avant de hacher
(l'invariant, indépendant de la configuration git). Vérifié invariant :
`e9ef2087` que les sept fichiers soient tous en LF ou tous en CRLF.

**L'empreinte est passée de `12f9b2c1` à `e9ef2087`.** Les 53 lignes antérieures
sont réputées périmées, à coût nul — `counted_tests()` valait 0. Portes 03, 04,
05 et 06 rejouées vertes (41, 2 002, 29 et 25 vérifications) ; le registre passe
à 58 lignes, toujours **0 test compté**. Voir `L12`.

### 1. ~~Mesurer `H01` et `H02`~~ — **fait le 2026-09-18**

`scripts/measure_h01_h02.py`, tranche `pool`, as-of 2023-12-29, 25 cellules,
~45 900 observations chacune. **`counted_tests()` : 0 → 2.**

| | IC poolé | t naïf | t final | Verdict pré-enregistré |
|---|---|---|---|---|
| `H01` (`T-20260918T065822-2b3e5d`) | **−0,01061** | −2,27 | **−1,56** | rien à distinguer du bruit |
| `H02` (`T-20260918T070041-18cf25`) | **−0,00432** | −0,92 | **−0,63** | rien à distinguer du bruit |

Chiffres **repris sous `D11`** le même jour : la première mesure déflatait le `t`
de 5,48 pour un recouvrement qui n'existe pas. L'IC n'a pas bougé, le verdict non
plus. `counted_tests()` vaut **4 pour deux hypothèses** — voir
`hypotheses/README.md` sur ce que la phase 15 doit compter.

Le signe est négatif là où les deux prédisaient positif, mais **ce n'est pas la
clause de falsification qui s'applique** : « le motif existe à l'envers »
exigeait un `t` final au-delà de 2. C'est « `t` final sous 2 : rien à distinguer
du bruit ». Les deux hypothèses sont **non confirmées, pas retournées**.

Et `H02`, qui s'annonçait « au moins aussi forte » que `H01`, est **plus
faible** — regarder tout ce qui précède plutôt que la seule première demi-heure
n'a rien ajouté.

**Ce que la déflation transversale coûte, et pourquoi c'est la bonne
nouvelle.** Le `t` naïf de `H01` vaut −2,27 : un calcul sans précaution l'aurait
déclaré significatif à 5 %, et le projet aurait tenu son premier « résultat ».
Divisé par 1,46 (9 instruments pour 4,22 paris), il vaut −1,56.

**Et ce que la déflation de recouvrement a failli coûter.** Elle retirait en plus
un facteur 5,48 — `t` final −0,28 — pour un recouvrement qui n'existe pas à cette
fréquence d'échantillonnage. Ici sans conséquence, les deux hypothèses étant dans
le bruit de toute façon ; sur un signal à `t` naïf de 4, elle aurait affiché 0,5
et l'aurait fait écarter sans bruit. Corrigé par `D11`, leçon `L13` : **« trop
sévère » n'est pas un côté sûr, un rejet ne se plaint pas.**

Détails dans `hypotheses/H01…` et `H02…` § Le résultat, recopiés des rapports
officiels avec leur `test_id`.

### 2. La clause 2 — réplication d'un résultat publié

**Sa prémisse a été vérifiée le 2026-09-18, et elle est tombée.**
`scripts/check_mesfin_premise.py`, aucun test dépensé.

Le plan portait un « raccourci honnête » : montrer que notre plancher mesuré est
un ordre de grandeur sous la friction supposée de Mesfin, et en conclure que son
résultat négatif n'est pas transportable. Le calcul, refait sur nos données au
lieu d'être cité, dit l'inverse.

| | bp d'aller-retour |
|---|---|
| friction de Mesfin — 2 points à la médiane NQ mesurée (14 688) | **1,36** |
| notre plancher `NQ × US` | 0,79 — sa friction vaut **1,7×** |
| notre **pire** cellule (CL) | 1,55 — sa friction vaut **0,9×** |

La page qui portait la réserve annonçait « 8 à 15 bp » : **faux d'un facteur
10**. Elle est corrigée, la réserve est retirée, et la leçon est `L14`. La
comparaison est en outre défavorable à tort : notre plancher est un **écart
seul**, quand ses 2 points sont une friction **tout compris**.

**Son verdict est transportable.** Le corpus implémentable doit donc être
considéré comme *attendu mort* jusqu'à preuve du contraire — ce que `corpus/AMORCE.md`
annonçait comme le scénario inconfortable.

**Et nos deux premiers tests vont dans le même sens.** `H01` et `H02` sont dans
le bruit **avant tout coût** : un IC brut nul n'a pas besoin qu'on lui retranche
des frais. La convergence n'est pas une preuve, mais elle n'est pas rien.

### Ce que la clause 2 demande, et la prochaine action

**La cible a changé le 2026-09-18** (`D12`). Le blocage n'a jamais été les frais ;
c'est la **métrique** qui ne correspondait pas, et cela ne s'est vu qu'en lisant
le papier.

La nouvelle cible est **Heston, Korajczyk & Sadka (2010)** — continuation du
rendement aux décalages multiples exacts d'une séance, retournement aux premiers
décalages, rien de positif entre les deux. Un **peigne**, qui porte son propre
témoin négatif : si les creux rendaient autant que les dents, il n'y aurait pas
de périodicité, seulement un biais.

Période dictée par le catalogue, pas par le résultat : **P = 13** demi-heures pour
`US` et `EUROPE` (6,5 h), **P = 16** pour `ASIA` (8 h). Deux motifs distincts à
retrouver. `H03` est **pré-enregistrée depuis le 2026-09-18**, avant toute mesure,
et dit aussi ce qui se passe si le motif est absent — l'échec ne s'achète pas en
redéfinissant la porte.

**Prochaine action : implémenter le signal `heston-2010-periodicity`** dans
`signals/`, à la main comme les étalons de `D06`, et le faire passer la porte 05
(contrat, liste blanche, test de causalité) avant toute mesure. Puis mesurer
`H03` : environ une centaine de lignes au registre pour **une** hypothèse.

### Ce qui reste ouvert par ailleurs

- les **multiplicateurs** CME (`cmegroup.com` injoignable depuis ce poste le
  2026-09-18) et la réponse de **Lucid** sur ses commissions ; requis pour toute
  lecture **nette** et pour la phase 10, mais ils ne bloquent plus la clause 2 ;
- une déclaration écrite de `slippage_bp`, pessimiste, comme `D04` l'exige ;
- **Mesfin reste le calibrage d'attente le plus proche**, désormais lu, fiché et
  **transportable** (`L14`) : le corpus implémentable doit être tenu pour
  *attendu mort* jusqu'à preuve du contraire. `H01` et `H02` vont déjà dans ce
  sens — dans le bruit, avant tout coût ;
- **Bollerslev et al. (2018)** comme cible ultérieure, quand un instrument de
  volatilité existera (phase 09 ou plus tard) ;
- **Mesfin au niveau du trade**, quand le moteur de backtest existera (phase 10).

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-18 | `signal` | Signal heston-2010-periodicity implémenté à la main (signals/heston_2010_periodicity.py) : un score par intervalle de demi-heure et non un par séance — le mécanisme de _common.run ne convenait pas et n'est pas réutilisé ; décalage paramétré EN SÉANCES pour les dents (traduit en intervalles par fenêtre depuis le catalogue) et EN INTERVALLES pour les creux ; rendement d'intervalle défini en BARRES, même définition que la cible du harnais ; scripts/check_heston.py et scripts/measure_h03.py écrits, H03 précisée sur ce point AVANT le lancement | contrôles verts : périodes P = 16/13/13 lues au catalogue et non espérées, liste blanche 0 refus, contrat conforme, CAUSALITÉ 0 divergence sur 16 sondes, écart d'échantillonnage mesuré à 30,0 barres donc étalement 1,00 — pas de déflation de recouvrement, ce que D11 doit faire pour des demi-heures disjointes ; pré-vol : 658 582 scores et 657 470 observations à m=1, soit 99,8 % de mesurabilité, aucune cellule mince ; le signal est tenu HORS de REFERENCE (les étalons de D06) et placé dans REPLICATION, pour que les portes gardent le sujet que D06 leur a donné |
| 2026-09-18 | `decision` | D12 écrite — la clause 2 CHANGE DE CIBLE : Mesfin ne convient pas (son critère est un t sur des rendements nets par trade, le nôtre un IC ; onze de ses quatorze familles échouent par amplitude sous friction, ce qu'un IC ne voit pas ; et deux de ses trois plis hors échantillon tombent dans le holdout scellé). Nouvelle cible : Heston, Korajczyk & Sadka (2010), JF 65(4) — papier récupéré d'arXiv (1005.3535), lu, fiché ; H03 PRÉ-ENREGISTRÉE avant toute mesure | le résultat visé est une CORRÉLATION et un MOTIF DE SIGNES, pas une valeur : continuation aux décalages multiples d'une séance (dents), retournement aux premiers décalages, rien de positif entre les deux (creux) — le peigne porte son propre témoin négatif ; période dictée par le catalogue et non par le résultat : P = 13 demi-heures pour US et EUROPE (6,5 h), P = 16 pour ASIA (8 h), donc DEUX motifs distincts à retrouver ; aucune magnitude du papier n'est reprise comme attendue (sa mesure est transversale avec effet de marché retiré, il le dit lui-même) ; H03 = UNE hypothèse pour ~100 lignes de registre, et l'échec du motif ne franchirait PAS la porte — écrit avant de regarder ; Mesfin reste calibrage d'attente, fiché |
| 2026-09-18 | `research` | Mesfin (2026) LU — PDF récupéré d'arXiv dans corpus/pdf/, texte extrait, fiche écrite à la main dans corpus/fiches/ (première fiche du projet, hors extracteur qui n'existe pas) ; corpus/AMORCE.md corrigé par une note datée, le texte d'origine conservé | les 14 familles nommées depuis la source (ORB x3, Asia expansion, Asia liquidity grab, gap fill, gap continuation, volume spike, volume dry-up, VVG x3, event day trend, MGC OU) ; sa friction CITÉE : « 2.0 points ($4.00 per micro contract), covering bid-ask spread, NinjaTrader exchange fees, and conservative slippage » — TOUT COMPRIS, et 4,00 $ sur 29 376 $ de notionnel = 1,36 bp, seconde route confirmant L14 ; DEUX OBSTACLES STRUCTURELS à la réplication, aucun lié aux frais : (1) son critère est un t sur RENDEMENTS NETS PAR TRADE, le nôtre un IC — onze familles échouent par amplitude sous friction, ce qu'un IC ne voit pas ; (2) ses plis hors échantillon testent 2023/2024/2025 et le holdout scellé couvre 2024-2026, donc SEUL LE PLI 1 est reproductible |
| 2026-09-18 | `audit` | Prémisse de la clause 2 vérifiée au lieu d'être citée — scripts/check_mesfin_premise.py, NQ tranche pool 2021-01-01 -> 2023-12-31 (le reste de la fenêtre de Mesfin est dans le holdout scellé), aucun IC, aucun test dépensé | LA PRÉMISSE NE TIENT PAS : 2 points d'indice valent 1,36 bp à la médiane NQ mesurée (14 688), pas les « 8 à 15 bp » écrits dans wiki/research/mesfin-2026-falsification depuis le 2026-09-16 — erreur d'un FACTEUR 10 ; sa friction vaut 1,7x notre plancher NQ x US (0,79) et 0,9x notre pire cellule (1,55), en comparant son coût TOUT COMPRIS à notre écart SEUL ; son verdict est TRANSPORTABLE et la réserve du projet tombe ; la plage « 13 000 à 25 000 » citée comme mesurée chez nous ne correspond pas au pool (c99 = 17 556) ; page corrigée (la source gagne), L14, F31, F32 |
| 2026-09-18 | `decision` | D11 écrite et appliquée — la déflation de recouvrement se MESURE : facteur = sqrt(n / n_eff) avec n_eff = somme des n_c / max(1, h / écart_c), l'écart_c étant l'écart médian en barres entre deux observations de la cellule ; CellIC porte sampling_gap_bars, le rapport dit l'écart mesuré ; deux assertions périmées corrigées dans les portes 03 et 06 (elles exigeaient counted_tests == 0, vrai avant H01/H02 et faux depuis — elles vérifient désormais que LA PORTE ne dépense rien) | découvert à partir d'une question sur les anomalies mono-actif ; H01 et H02 scorent une fois par séance, observations espacées de 415 barres pour un horizon de 30, AUCUN recouvrement — le harnais leur retirait un facteur 5,48 ; empreinte e9ef2087 -> 9ac3e45e, portes 03/04/05/06 rejouées vertes, H01 et H02 REMESURÉES : IC inchangés (-0,01061 et -0,00432), t final -0,28 -> -1,56 et -0,11 -> -0,63, CONCLUSION INCHANGÉE (les deux sous 2) ; counted_tests 2 -> 4 pour DEUX hypothèses — la phase 15 compte des hypothèses, pas des lignes ; tests de référence T-20260918T065822-2b3e5d et T-20260918T070041-18cf25 ; L13, F29, F30 |
| 2026-09-18 | `mesure` | H01 ET H02 MESURÉES — les deux premiers tests comptés du projet ; scripts/measure_h01_h02.py, tranche pool, as-of 2023-12-29, 25 cellules, ~45 900 observations chacune, harnais e9ef2087 ; pré-vol d'abord (scores et mesurabilité 89,9 %, aucune cellule sous les seuils, AUCUN IC) | counted_tests 0 -> 2 ; H01 IC -0,01061 t final -0,28, H02 IC -0,00432 t final -0,12 : signe négatif contre signe positif attendu, mais la clause qui s'applique est « t final sous 2 : rien à distinguer du bruit » — NON CONFIRMÉES, PAS RETOURNÉES ; H02 s'annonçait au moins aussi forte que H01 et est plus faible ; la DOUBLE DÉFLATION de D04 mord pour la première fois — t naïf -2,27 (significatif à 5 % sans précaution) devient -0,28, facteur 8 ; garde ajouté au script contre une ré-exécution ; ouverture notée à ETAT : répliquer un résultat NÉGATIF ne demande que la direction négative, donc la clause 2 est peut-être bloquée par le budget de tests et non par fee_bp |
| 2026-09-18 | `decision` | D10 écrite et appliquée — l'empreinte du harnais porte sur le CONTENU et non sur les octets : .gitattributes fixe `* text=auto eol=lf` (114 fichiers réécrits en LF, aucun contenu committé changé — les blobs étaient déjà en LF), et `registry.code_hash()` replie les fins de ligne avant de hacher ; seule modification de harness/ depuis D08 | empreinte 12f9b2c1 -> e9ef2087, vérifiée IDENTIQUE que les 7 fichiers soient tous en LF ou tous en CRLF ; les 53 lignes antérieures réputées périmées pour un coût NUL — dernière fois que ce sera gratuit ; portes 03/04/05/06 rejouées vertes (41, 2 002, 29, 25 vérifications), registre 53 -> 58 lignes, counted_tests toujours 0 ; F27, F28 ; prochaine action du projet = mesurer H01 et H02 |
| 2026-09-18 | `decision` | D09 écrite — provenance des valeurs externes : trichotomie mesurée/décidée/externe, liste CLOSE des externes corroborées, champs source/source_url/retrieved/quoted/applies_to ; validate.py §8, bloc `provenance:` au catalogue, source_url ajouté à roll_dates.json, scripts/check_provenance.py ; multiplicateurs CME NON relevés — cmegroup.com injoignable depuis le poste (timeout puis ECONNRESET sur 3 URLs) | 33 vérifications, 9 fautes refusées chacune pour la raison écrite d'avance ; le script a trouvé un défaut du garde lui-même — `12500` passait sous « 12,500,000 » par sous-chaîne — corrigé en comparaison numérique ; portes 01 et 02 rejouées vertes, registre inchangé à 53 lignes, counted_tests 0, aucun fichier de harness/ touché ; DÉCOUVERTE hors sujet mais sérieuse : `code_hash()` dépend des FINS DE LIGNE, les 3 empreintes du projet se reproduisent des mêmes blobs git — le harnais n'a jamais changé et gate_04 annonce 53 lignes périmées à tort ; L12, F25, F26 |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 13 |
| `phases` | 6 |
| `reference` | 3 |
| `research` | 6 |
| `signaux` | 1 |

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
> Bloc **editable a la main**. Le generateur le relit et le reinjecte tel quel.
> Tout ce qui est en dehors des marqueurs est ecrase a chaque regeneration.

- _(rien d'inscrit — voir « Prochaine action » ci-dessus, qui vient de `ETAT.md`)_
<!-- NEXT-ACTIONS:END -->

---

À lire au démarrage : [[index]] puis [[Failed Ideas/ledger]] — règles permanentes de `CLAUDE.md` § Wiki.
