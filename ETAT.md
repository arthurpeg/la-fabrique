# ÉTAT

**Phase courante :** 06 — contrôles automatiques et réplication (**ouverte, non franchie**)
**Date de dernière mise à jour :** 2026-09-18
**Dernière porte franchie :** **05**, le 2026-09-17 — `scripts/gate_05_signal_api.py`,
29 vérifications. Les trois look-ahead injectés (`sandbox/tainted.py`) sont
**attrapés**, chacun pour la raison écrite d'avance ; les deux étalons passent
16 sondes sans une divergence.
**État de la porte 06 :** sa **clause 1** est franchie — `gate_06_controls.py`,
25 vérifications, quatre signaux dégénérés rejetés sans consommer une ligne de
registre. **`H01` et `H02` sont mesurées** depuis le 2026-09-18 :
`counted_tests()` vaut **4 pour deux hypothèses** (mesure puis reprise sous
`D11`), et les deux sont dans le bruit (`t` final de référence −1,56 et −0,63). Sa **clause 2**, la réplication d'un résultat publié, ne l'est pas, et
la porte reste donc **ouverte** : une porte à moitié franchie est une porte non
franchie. Le **premier maillon** de la chaîne qui la débloque est posé depuis le
2026-09-18 — la convention de provenance (`D09`) ; le deuxième, les
multiplicateurs, attend que `cmegroup.com` réponde.
**Décision la plus récente :**
`decisions/DECISION-12-cible-de-replication.md` — la clause 2 de la porte 06
**change de cible**. Mesfin (2026), lu et fiché le 2026-09-18, ne convient pas :
son critère est un `t` sur des **rendements nets par trade**, le nôtre un **IC**,
et deux de ses trois plis hors échantillon tombent dans le `holdout` scellé. La
nouvelle cible est **Heston, Korajczyk & Sadka (2010)**, dont le résultat est une
corrélation et un **motif de signes** — donc lisible par notre instrument et
robuste à la transposition d'univers. `H03` est pré-enregistrée.
**Décision précédente :**
`decisions/DECISION-11-deflation-de-recouvrement.md` — la déflation de
recouvrement se **mesure** sur l'écart réel entre observations au lieu d'être
supposée égale à `√h`. `H01` et `H02` scorent une fois par séance : leurs
observations sont espacées de 415 barres pour un horizon de 30 et ne se
recouvrent pas ; le harnais leur retirait un facteur **5,48** sans raison.
Empreinte `e9ef2087` → `9ac3e45e`, portes 03 à 06 rejouées vertes, `H01` et `H02`
remesurées. Voir `L13`.
**Décision précédente :**
`decisions/DECISION-10-empreinte-du-harnais.md` — `registry.code_hash()` empreinte
désormais le **contenu** et non les octets (fins de ligne repliées), et
`.gitattributes` fixe `eol=lf` sur tous les postes. L'empreinte passe **une fois**
de `12f9b2c1` à `e9ef2087` ; les 53 lignes antérieures sont réputées périmées,
pour un coût **nul** — aucune n'est un test compté, et c'est la dernière fois que
ce sera gratuit. Portes 03, 04, 05 et 06 rejouées vertes.
**Décision précédente :**
`decisions/DECISION-09-provenance-des-valeurs-externes.md` — toute valeur du
catalogue est **mesurée** (notre code, nos données), **décidée** (un fichier de
`decisions/`) ou **externe** (recopiée d'un tiers) ; une valeur externe n'entre
qu'accompagnée de sa source, citation comprise, et `catalogue/validate.py` §8
refuse le catalogue sinon. Le harnais n'est pas touché : **aucun résultat
antérieur n'est périmé** par elle.
**Décision pertinente pour la phase courante :** `D08` § Ce qui reste ouvert (le
magasin de scores des signaux déjà testés, renvoyé en phase 11) et `D06` § Ce qui
reste ouvert (la mesure de `H01` et `H02`, qui appartient à cette phase).

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
| 06 | Contrôles automatiques et réplication | Le harnais réplique un résultat publié connu, contrôles compris, sans intervention. Première cible : la falsification de Mesfin (2026) rejouée avec notre modèle de coût (`corpus/AMORCE.md`, entrée 7). | **NON FRANCHIE** — clause 1 (dégénérescence) franchie 2026-09-17, `gate_06_controls.py` ; clause 2 (réplication) bloquée, voir ci-dessous |
| 07 | Triage et extraction sur 20 papiers connus | 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict humain de référence. Point de départ : `corpus/AMORCE.md`. | à faire |
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
