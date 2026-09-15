# D01 — Univers, données, métrique et tranches

**Date :** 2026-09-15
**Phase :** 01
**État :** prise
**Mesures à l'appui :** `scripts/out/a1_inventory.json`, `a2_roll_diagnostics.json`,
`a3_breadth.json`, `a4_regimes.json`, `a5_breadth_intraday.json`,
`a8_session_grid.json`. Corpus : `corpus/AMORCE.md`.

---

## La question

Sur quel univers, à quelle fréquence, contre quel corpus et avec quelle métrique
ce projet travaille-t-il ? Les données étant déjà acquises, la question ouverte
n'est pas « quoi acheter » mais « qu'est-ce que ce que j'ai permet réellement de
tester, et qu'est-ce que ça interdit ».

## Les options

Sept critères, chiffrés. Le critère « adéquation au moteur » est remplacé, suivant
`DECISION-00`, par le **coût d'obtention d'un moteur** capable de backtester cet
univers — le moteur attendu n'est pas en main et son adéquation ne se vérifiera
qu'à sa réception.

| Critère | **A — tel quel** | **B — acheter de la largeur** | **C — passer en journalier** |
|---|---|---|---|
| Intégrité point-in-time | **acquise et testée.** Séries brutes, recollées, historique stable ; porte 01 passée | identique pour l'existant ; inconnue pour la 2ᵉ échéance | identique à A |
| Coût annuel | **0 €** | Databento : usage `$/GB` non publié ; abonnements **199 $/mois** (Standard), **1 750 $/mois** (Plus), **4 500 $/mois** (Unlimited) — soit **2 388 à 54 000 $/an** pour un budget de **0 €** | 0 € |
| Largeur effective | **4,22** à 15 min · **12,40** en sommant les trois séances · médiane réalisée **3,74** par séance | +1 à +2 paris (le carry est orthogonal au momentum de prix) | **4,03**, et ~1 060 paris/an contre ~3 100 |
| Corpus implémentable | **12 références, 5 à 6 idées indépendantes** | ouvre carry et structure de terme : Koijen et al. (2018), Gorton et al. (2013) — famille majeure et orthogonale | ouvre le corpus CTA mensuel (Moskowitz et al. 2012), déjà bien exploré, et ferme tout l'intraday |
| Coût d'un moteur | intégration du moteur attendu : **inconnue, 1 à 2 semaines si son squelette dit vrai** ; repli « construire » : **3 à 5 semaines** à 20 h/semaine pour un moteur intraday à clôture forcée, coûts par cellule et fenêtres de séance | identique à A | plus simple : **1 à 2 semaines** à construire, un moteur journalier étant trivial à côté |
| Frictions, notionnel | écart d'un tick **mesuré** : 0,21 bp (NQ) à 1,55 bp (CL) ; coût/mouvement 15 min de **0,06 à 0,35** | inchangé | frictions négligeables, mais ~1 A/R par semaine |
| Délai au premier IC | phases 02 et 03 : **4 à 6 semaines** | + délai d'accès, inconnu | identique |

**Option B, précisions.** Elle n'est pas actionnable aujourd'hui : le budget est
nul, et je n'ai pas d'accès Databento. Le volume marginal est pourtant modeste —
les neuf séries existantes pèsent environ **475 Mo**, la deuxième échéance des
neuf racines en pèserait autant. Deux réserves, dont la seconde est la vraie.
Premièrement, l'accès lui-même est une **inconnue à lever**, pas un acquis :
l'auteur des données possède peut-être une licence. Deuxièmement, et
indépendamment du prix : **le carry est un signal de plusieurs jours à plusieurs
mois** ; il ne se loge pas dans une grille intraday à clôture forcée. Même
gratuite, la deuxième échéance n'apporterait rien à l'horizon retenu. Elle
redeviendrait décisive si l'horizon changeait.

**Option C.** Écartée sur ordre, et les chiffres le confirment : diviser par
~1 350 le nombre d'observations pour gagner **zéro** paris — 4,03 en journalier
contre 4,22 à 15 minutes — ferait passer l'IC requis pour un IR de 1 de 0,018 à
0,031.

## Le choix

**Option A, restreinte à la grille des cellules négociables.** Neuf futures CME,
barres 1 minute, trois fenêtres de séance disjointes, 25 cellules retenues sur
27. Zéro euro engagé. FDAX exclu de l'univers de travail, fichier conservé.

## Pourquoi

Parce que la contrainte qui mord n'est ni le nombre d'instruments ni la
fréquence : c'est **le corpus et la largeur**, et aucune des deux options
alternatives ne les améliore à un coût payable. B est fermée par le budget et,
plus profondément, par l'horizon. C détruit 1 350 fois les observations sans rien
rendre.

Ce qui est sacrifié : toute la famille carry/structure de terme, c'est-à-dire la
seule famille vraiment orthogonale au momentum de prix. Le projet repose donc sur
un socle plus étroit qu'il n'y paraît — voir le verdict de `corpus/AMORCE.md`.

---

## Ce que ça verrouille

### 1. L'univers, et le sort de FDAX

Univers de travail : **NQ, ES, YM, GC, CL, 6E, 6B, 6J, 6A**.

**FDAX est exclu**, le fichier reste. Trois motifs, tous mesurés : 1,46 an contre
10,65 (L02), donc **absent de la totalité de la tranche de recherche** ; une
corrélation de **0,70 à 0,76** avec NQ/ES/YM sur sa propre fenêtre, donc **aucun
pari supplémentaire** ; et une horloge d'échange différente (EUREX), qui
imposerait une seconde définition de séance pour zéro apport. Il est conservé
parce qu'il ne coûte rien et qu'il servira de témoin hors univers.

### 2. La métrique — contrainte sur la phase 03, pas une remarque

La largeur mesurée est de **4,03 en journalier, 4,22 à 15 minutes**. Neuf
instruments portant quatre paris, **l'IC transversal n'a aucun sens ici** : on ne
classe pas neuf actifs en déciles, et un rang transversal sur quatre blocs
corrélés mesure surtout le bruit d'estimation de la matrice de corrélation.

Le rapport d'évaluation de la phase 03 sera donc bâti sur l'**IC en série
temporelle, poolé entre instruments et entre cellules**, avec :

- une statistique de test robuste à la corrélation contemporaine entre
  instruments — les résidus sont corrélés en coupe, un t de Student naïf serait
  surévalué d'un facteur proche de `sqrt(9 / 4,2) ≈ 1,46` ;
- le *pooling* entre instruments justifié par Bollerslev et al. (2018), qui
  documente la similarité des dynamiques de volatilité **au sein et entre**
  classes d'actifs sur 50+ futures (`AMORCE.md`, entrée 12) ;
- un seuil de FDR appliqué **dès le premier test**, jamais un t-stat à 2 ; la
  référence de calibrage est Harvey, Liu & Zhu (2016), t > 3,0.

**Ordre de grandeur à viser.** Avec 12,40 paris par jour sur 252 séances, soit
~3 100 par an, l'IC requis pour un IR de 1 est de **0,018**. Si les trois
fenêtres ne sont pas indépendantes pour une même famille de signaux — et elles ne
le seront probablement pas — le compte retombe vers ~1 060 paris/an et l'IC requis
vers **0,031**. La cible est donc **entre 0,018 et 0,031**, et le rapport d'IC
doit afficher les deux bornes, jamais la plus flatteuse seule.

### 3. La grille actif × séance

Trois fenêtres, **disjointes par construction**, ancrées à l'horloge locale de la
place — `America/New_York` pour les neuf instruments, tous sur CME Globex — et
non à UTC. Ancrer à UTC ferait dériver les fenêtres d'une heure deux fois par an,
à des dates que personne n'a choisies ; la disjonction, qui était l'objet de
l'exigence UTC, est préservée dans la seule horloge où elle peut l'être.

| Fenêtre | Heure locale (New York) | Ce qu'elle couvre |
|---|---|---|
| `ASIA` | 19:00 → 03:00 | réouverture Globex, matinée de Tokyo |
| `EUROPE` | 03:00 → 09:30 | Francfort et Londres, avant New York |
| `US` | 09:30 → 16:00 | la séance de cotation américaine |

16:00 → 19:00 n'appartient à aucune fenêtre : règlement, arrêt quotidien, l'heure
la plus mince de la journée. **Au plus une stratégie vivante par actif à un
instant donné**, par construction.

**Cellules écartées : 2 sur 27.** `6B × ASIA` (42,4 % de barres sous 10 contrats
la minute, et un coût estimé à 35 % du mouvement médian de 15 minutes) et
`YM × ASIA` (34,6 % de barres minces, 15 contrats/minute). Règle de rétention,
posée avant lecture des chiffres : volume médian ≥ 10 contrats/minute, barres
minces ≤ 25 %, aller-retour estimé ≤ ⅓ du mouvement médian de 15 minutes.

**Note contre une intuition.** `NQ × ASIA` était annoncé comme un cas d'exclusion
évident. La mesure dit le contraire : 41 contrats/minute, 11,6 % de barres
minces, un coût à **7 %** du mouvement médian — la meilleure cellule asiatique de
la grille. Elle est retenue.

**Largeur par fenêtre**, sur rendements 15 minutes : `ASIA` **4,43** (7
instruments), `EUROPE` **4,10**, `US` **3,87**. Le gain vient de la structure de
blocs, pas du nombre : en séance asiatique le bloc devises **se dissout** — 6E,
6J et 6A deviennent trois blocs séparés — alors qu'il est soudé en Europe et aux
États-Unis. L'estimation *a priori* de sept à neuf paris par jour est donc
**dépassée** : la somme des trois fenêtres donne **12,40**, sous l'hypothèse que
les fenêtres sont indépendantes entre elles. Elles sont disjointes dans le temps ;
elles ne sont pas indépendantes pour autant, une tendance traversant les trois.
Le rapport d'IC devra donc porter les deux comptes.

### 4. Le comptage des tests — règle contraignante pour le registre

- Un signal évalué sur la grille produit **UN test** au registre : la statistique
  poolée sur les cellules retenues. La ventilation par cellule est un
  **diagnostic**, jamais une série de tests indépendants. Compter 25 tests par
  famille ferait exploser le seuil de FDR pour une raison purement mécanique.
- Les **plis d'un même schéma de walk-forward comptent pour UN test**, pas k.
- **Sélectionner après coup la cellule qui marche le mieux est interdit.** Si une
  cellule seule est retenue plutôt que la grille, c'est une **hypothèse
  distincte, pré-enregistrée avant de voir les résultats**, et elle compte comme
  un test supplémentaire.

### 5. Les tranches

Le découpage en trois blocs contigus est abandonné : deux ans de validation
composés d'un unique régime baissier (2022-2023, NQ à +2,0 % de dérive contre
+20,9 % en recherche) ne valident qu'une chose.

| Tranche | Période | Durée | Statut |
|---|---|---|---|
| `pool` (recherche + validation) | 2016-01-03 → 2023-12-31 | 8,0 ans | walk-forward purgé, plusieurs plis, embargo aux frontières |
| `holdout` | 2024-01-01 → 2026-08-28 | 2,7 ans | **scellé jusqu'à la phase 15** |

**Le holdout est typé, et ce type est connu maintenant, avant lecture** : envolée
de l'or (+48,4 % en 2025, volatilité passant de 14,2 % en moyenne de pool à
30,8 % en 2026), choc pétrolier en 2026 (volatilité 61,7 %, dérive +55,4 %),
actions calmes et haussières (NQ +20,2 %/an, volatilité 20,9 %). Le pool, lui,
contient le COVID (2020, NQ à 34,9 % de volatilité, CL à 95,9 %) et le marché
baissier de 2022. Un holdout décevant sur l'or ou le pétrole devra être lu à la
lumière de ce typage — **écrit avant, pas découvert après**.

### 6. Le traitement des roulements — contrainte sur la phase 02

Les séries sont **brutes (recollées)**, le raccord tombant à **00:00 UTC**, selon
un cycle trimestriel pour les indices et les devises, mensuel pour GC et CL.
Bonne nouvelle : l'historique ne se réécrira pas.

Neutraliser la barre de roulement est **nécessaire et très insuffisant**. Le
niveau de prix est discontinu : toute grandeur calculée sur une fenêtre qui
enjambe un recollement est fausse **sur toute sa largeur** — volatilité réalisée,
moyennes mobiles, momentum.

Le traitement est **au niveau du Panel, en phase 02, jamais au niveau du signal** :
à chaque date d'évaluation `t`, construire une série ajustée à rebours en
n'utilisant **que les recollements ≤ t**. Elle reste point-in-time : elle ne
diffère de celle construite en `t+1` que par un facteur d'échelle uniforme, qui
n'affecte ni les rendements ni les ratios. **Le prix brut reste disponible
séparément**, pour les niveaux et l'exécution.

**Conséquence de calendrier : les dates de roulement de l'auteur des données
deviennent un intrant BLOQUANT de la phase 02**, et non plus un confort. Ma
détection empirique en trouve 3,4 à 3,6 par an pour les indices là où il y en a 4,
et 8,5 pour CL là où il y en a 12 : elle manque les recollements des années à
taux zéro, dont l'écart de calendrier était trop petit pour émerger du bruit.
6A et FDAX ne sont pas tranchés du tout. À la réception des dates autoritatives,
**comparer avant d'adopter** ; l'écart mesure la méthode et fera l'objet d'une
entrée dans `LECONS.md`.

### 7. Le modèle de coûts — première classe dès la phase 03

Ce projet n'a pas de courtier et n'en vise pas. Il ne s'ensuit pas que les coûts
sont secondaires : **l'inverse**. Sans barème réel, le modèle doit être déclaré,
sourcé et pessimiste, dès la phase 03.

Structure, par cellule :

```
round_trip_cost_bp(cell) = spread_floor_bp(cell)      mesuré
                         + fee_bp(instrument, size)    null -- todo
                         + slippage_bp(cell)           hypothèse déclarée, pessimiste
```

**Ce qui est mesuré.** Le tick de chaque contrat est *observé* dans les données —
plus petite variation de prix non nulle sur onze ans — et non déclaré : NQ et ES
0,25 · YM 1,0 · GC 0,10 · CL 0,01 · 6E 0,00005 · 6B 0,0001 · 6J 0,0000005 ·
6A 0,00005. Rapporté au prix médian, l'écart plancher d'un tick vaut de **0,21 bp
(NQ) à 1,55 bp (CL)**. Un marché ne peut pas être plus serré qu'un tick : c'est
le plancher du modèle.

L'estimateur de Corwin & Schultz (2012) a été calculé et **n'est pas utilisable
seul ici** : sur barres 1 minute il s'effondre à zéro sur 6A, 6B, 6J et toutes les
cellules asiatiques. C'est une limite de l'estimateur, pas un marché gratuit. Il
est conservé comme borne haute là où il dépasse le tick (CL en séance US : 1,08 bp
contre 1,55 bp de tick ; NQ en US : 0,79 bp contre 0,21 bp de tick — c'est-à-dire
que NQ paie en réalité **plus** qu'un tick aux heures actives).

**Ce qui est null et ouvert en `todo`.** Les frais d'échange et de compensation.
Sources à dépouiller, jamais à deviner : barème CME
(<https://www.cmegroup.com/company/clearing-fees.html>, *Non-Member Fee Finder*,
et le PDF daté du barème) et liste de prix EUREX. Tentative faite dans cette
session : la page CME n'a pas répondu dans le délai, et les montants par contrat
ne figurent pas dans les résultats de recherche. **Aucun chiffre n'est donc
inscrit.** Idem pour les **multiplicateurs**, qui restent hors du dépôt jusqu'à
confirmation sur les fiches contrat.

**Plein contre micro, l'écart est structurel.** Un frais fixe de `F` dollars par
contrat vaut `F / (P × M) × 10 000` bp. Si le multiplicateur micro vaut un
dixième du plein — à vérifier — alors **la part fixe pèse exactement dix fois
plus lourd en micro**, à prix égal. C'est de l'arithmétique, pas une hypothèse :
le modèle devra afficher les deux tailles côte à côte, et c'est probablement là
que se joue la viabilité d'une stratégie à 1 ou 2 allers-retours par cellule et
par jour.

### 8. La définition de séance est propre à chaque instrument

Les neuf instruments retenus sont tous sur CME Globex et partagent donc l'horloge
de New York, ce qui rend la grille homogène. **Ce n'est pas une propriété
générale** : FDAX est sur EUREX en heures européennes, et mes données commencent
à 23:00 UTC le dimanche, soit l'ouverture Globex — pas la séance américaine. La
définition de séance sera donc **déclarée par instrument au catalogue**, avec
mention de l'horloge de référence, et non déduite d'une constante globale.

### 9. Ce qui découle de l'objectif « engager du vrai capital »

- contrôle du FDR **dès le premier test**, jamais un seuil de t-stat à 2 ;
- coûts et capacité en première classe **dès la phase 03**, pas ajoutés en 10 ;
- Sharpe **dégonflé** du nombre total de tests au registre, à la fin
  (Bailey & López de Prado, 2014) ;
- le holdout est sacré : **une ouverture, aucune dérogation**, quelle que soit la
  qualité apparente du résultat ;
- **aucune voie rapide** pour une idée « manifestement bonne ».

---

## Ce qui reste ouvert

| Point | Échéance | Statut |
|---|---|---|
| Dates de roulement autoritatives | **bloquant pour la phase 02** | demandées à l'auteur des données |
| Frais CME et EUREX par contrat | avant la calibration du harnais, phase 03 | `null`, `todo`, sources nommées |
| Multiplicateurs de contrat | idem | `null`, `todo`, hors dépôt |
| Calendrier FOMC et annonces macro | phase 07, familles 15 à 17 du corpus | gratuit, non encore récupéré |
| Nombre et frontières des plis du walk-forward | phase 03 | non tranché ici volontairement |
| Taille de compte et nombre de positions simultanées | phase 10 | inconnue déclarée — elle **plafonnera la largeur réellement récoltée**, qui peut retomber sous 4 |

## Condition de révision

Cette décision est rouverte, et remplacée, si l'un de ces faits précis survient :

1. **Un accès Databento devient disponible** — budget débloqué, ou licence de
   l'auteur des données utilisable. L'option B redevient évaluable, et avec elle
   la famille carry, sous réserve de l'objection d'horizon.
2. **Les dates de roulement autoritatives contredisent la détection empirique**
   au point de changer le verdict « séries brutes » — par exemple si une partie
   des séries s'avérait ajustée.
3. **`gate_01_pit.py` échoue** sur l'empreinte de préfixe : l'historique aurait
   été réécrit, et toute l'intégrité point-in-time serait à reconstruire.
4. **L'horizon de détention change** et cesse d'être intraday. La grille, la
   métrique, le comptage des tests et le verdict sur l'option B tombent ensemble.
5. **La famille « momentum intra-journalier » ne survit pas aux contrôles de la
   phase 06.** Elle porte l'essentiel du corpus implémentable ; son échec est un
   problème de matière première, qui obligerait à rouvrir le choix d'univers.
