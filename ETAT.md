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
`counted_tests()` vaut **2**, et les deux sont dans le bruit (`t` final −0,28 et
−0,12). Sa **clause 2**, la réplication d'un résultat publié, ne l'est pas, et
la porte reste donc **ouverte** : une porte à moitié franchie est une porte non
franchie. Le **premier maillon** de la chaîne qui la débloque est posé depuis le
2026-09-18 — la convention de provenance (`D09`) ; le deuxième, les
multiplicateurs, attend que `cmegroup.com` réponde.
**Décision la plus récente :**
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
| `H01` | **−0,01061** | −2,27 | **−0,28** | rien à distinguer du bruit |
| `H02` | **−0,00432** | −0,92 | **−0,12** | rien à distinguer du bruit |

Le signe est négatif là où les deux prédisaient positif, mais **ce n'est pas la
clause de falsification qui s'applique** : « le motif existe à l'envers »
exigeait un `t` final au-delà de 2. C'est « `t` final sous 2 : rien à distinguer
du bruit ». Les deux hypothèses sont **non confirmées, pas retournées**.

Et `H02`, qui s'annonçait « au moins aussi forte » que `H01`, est **plus
faible** — regarder tout ce qui précède plutôt que la seule première demi-heure
n'a rien ajouté.

**Ce que la double déflation vient de coûter, et pourquoi c'est la bonne
nouvelle.** Le `t` naïf de `H01` vaut −2,27 : un calcul sans précaution l'aurait
déclaré significatif à 5 %, et le projet aurait tenu son premier « résultat ».
Après division par 5,48 (recouvrement) puis 1,46 (9 instruments pour 4,22 paris),
il vaut −0,28. **Un facteur 8.** C'est exactement ce pour quoi `D04` existe, et
la première fois qu'on le voit mordre.

Détails dans `hypotheses/H01…` et `H02…` § Le résultat, recopiés des rapports
officiels avec leur `test_id`.

### 2. La clause 2 — réplication d'un résultat publié

**Bloquée, et pas seulement par du travail à faire.** La cible nommée est la
falsification de Mesfin (2026) : 14 familles de signaux OHLCV, aucune ne survit à
2 points d'indice de friction supposée. La rejouer « avec notre modèle de coût »
suppose de connaître notre coût — or `harness/costs.py` ne rend qu'un **plancher**,
`fee_bp` et `slippage_bp` étant ouverts.

Conséquence précise, à ne pas contourner : on peut conclure « ne survit pas même
au plancher » (conclusion **négative**, valide), jamais « survit sous nos coûts »
(conclusion **positive**, hors de portée tant que le coût est incomplet).

Il faut donc, dans cet ordre :
1. ~~la **convention de provenance** des valeurs externes~~ — **faite** le
   2026-09-18, `D09` ; `catalogue/validate.py` §8 refuse désormais une valeur
   externe sans `source_url`, date et valeur citée, et
   `scripts/check_provenance.py` le démontre sur neuf fautes ;
2. les **multiplicateurs** relevés sur les fiches contrat CME — **tentés le
   2026-09-18, `cmegroup.com` injoignable** depuis ce poste (timeout puis
   ECONNRESET sur trois URLs). Les neuf champs restent `null`, `todo multipliers`
   reste ouvert. À reprendre dès que le site répond ; le bloc `provenance:` du
   catalogue porte la forme exacte de l'entrée à déposer ;
3. la réponse de **Lucid** sur le caractère all-in de ses commissions, et le
   barème micro ou mini selon ce qui sera tradé ;
4. une déclaration écrite de `slippage_bp`, pessimiste, comme `D04` l'exige ;
5. **alors seulement** l'implémentation des familles de Mesfin, qui est du gros
   travail et dépensera beaucoup de tests comptés — à pré-enregistrer.

Un raccourci honnête existe et ne coûte presque rien : montrer que notre
**plancher mesuré** (0,79 bp sur `NQ × US`, 1,55 bp sur la pire cellule) est déjà
un ordre de grandeur sous les 8 à 15 bp que vaut sa friction supposée sur nos
données. Ce n'est pas la réplication, c'en est la prémisse — et elle se vérifie
sans dépenser un seul test.

### Une ouverture, apparue avec le résultat de `H01` et `H02`

**Le blocage de la clause 2 est peut-être plus étroit qu'écrit ci-dessus, et il
faut le vérifier avant de continuer à attendre les frais.**

Le raisonnement tenu jusqu'ici : on ne peut pas conclure « survit sous nos coûts »
tant que le coût est incomplet. C'est vrai. Mais **le résultat de Mesfin est
négatif** — aucune des 14 familles ne survit. Répliquer un résultat négatif ne
demande que la direction négative, et notre plancher est **plus bas** que sa
friction supposée : si une famille ne survit pas même à un coût plus faible que
le sien, sa conclusion est reproduite *a fortiori*.

Mieux : `H01` et `H02` viennent de montrer qu'un signal peut être écarté **sans
que le coût intervienne du tout** — un IC brut dans le bruit n'a pas besoin
d'être diminué des frais pour être nul.

Si cela tient, le vrai coût de la clause 2 n'est pas `fee_bp` : c'est le **budget
de tests** (14 familles, 14 hypothèses à pré-enregistrer, 14 lignes au
dénominateur) et le travail d'implémentation. Ce qui est une tout autre
conversation, et une décision à écrire.

**À trancher avant d'implémenter quoi que ce soit**, et sans dépenser un test.
