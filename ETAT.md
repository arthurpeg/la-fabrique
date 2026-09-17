# ÉTAT

**Phase courante :** 06 — contrôles automatiques et réplication (**ouverte, non franchie**)
**Date de dernière mise à jour :** 2026-09-17
**Dernière porte franchie :** **05**, le 2026-09-17 — `scripts/gate_05_signal_api.py`,
29 vérifications. Les trois look-ahead injectés (`sandbox/tainted.py`) sont
**attrapés**, chacun pour la raison écrite d'avance ; les deux étalons passent
16 sondes sans une divergence.
**État de la porte 06 :** sa **clause 1** est franchie — `gate_06_controls.py`,
25 vérifications, quatre signaux dégénérés rejetés sans consommer une ligne de
registre. Sa **clause 2**, la réplication d'un résultat publié, ne l'est pas, et
la porte reste donc **ouverte** : une porte à moitié franchie est une porte non
franchie.
**Décision la plus récente :** `decisions/DECISION-08-controles-automatiques.md` —
les contrôles de dégénérescence vivent dans `harness/controls.py`, empreintés avec
le harnais, et s'exécutent **avant** que le jeton soit pris : un signal rejeté ne
consomme aucune ligne. Le détecteur de « trop beau pour être vrai » signale sans
bloquer. Le harnais a changé, donc **tous les résultats antérieurs sont périmés**
— coût nul pour la dernière fois, `counted_tests()` vaut encore 0.
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

**Finir la phase 06.** Sa clause 1 est franchie ; deux choses restent, et elles
sont de natures différentes.

### 1. Mesurer `H01` et `H02` — les deux premiers tests comptés du projet

Tout est prêt : les hypothèses sont pré-enregistrées depuis le 2026-09-17, les
étalons passent la porte 05, et les contrôles tournent devant le harnais. Il
suffit d'appeler `evaluate()` avec `hypothesis_ref="H01"` puis `"H02"`.

**C'est irréversible.** `counted_tests()` passera de **0 à 2**, et ces deux lignes
compteront dans le dénominateur de toutes les corrections de tests multiples
jusqu'à la phase 15. Elles sont corrélées — même cible, prédicteurs différents —
et `H02` le dit : **elles ne sont jamais comptées comme deux tests indépendants**.

Deux choses à savoir avant de lancer :
- les étalons rendent **88,6 %** d'observations pour leurs scores, et `6A × US`
  seulement 30 % (`L10`, exemption écrite dans `check_signals.py`) ;
- le coût restera un **plancher étiqueté** tant que `fee_bp` et `slippage_bp`
  sont `null` : l'IC net lu sera un **majorant de performance**. L'IC brut, lui,
  ne dépend pas des frais.

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
1. la **convention de provenance** des valeurs externes (`validate.py` refuse une
   valeur externe sans `source_url` + date + valeur citée) — jamais écrite ;
2. les **multiplicateurs** relevés sur les fiches contrat CME ;
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
