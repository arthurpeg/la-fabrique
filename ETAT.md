# ÉTAT

**Phase courante :** 07 — triage et extraction sur 20 papiers connus
**Date de dernière mise à jour :** 2026-09-18
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
`decisions/DECISION-13-ce-que-la-clause-2-peut-etre.md` — après l'échec de deux
cibles, la clause 2 est satisfaite quand **la chaîne reproduit un fait publié sur
nos données**, et non quand le harnais d'IC reproduit un IC publié. Écrite
**avant** la mesure de `H04`, comme `H03` l'exigeait.
**Décisions pertinentes pour la phase courante :** `D06` (les fiches écrites à la
main sont un banc d'essai, pas le produit de la phase 07) et `D09` (la provenance
des valeurs externes, qui s'étendra aux fiches).

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
| 07 | Triage et extraction sur 20 papiers connus | 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict humain de référence. Point de départ : `corpus/AMORCE.md`. | **PHASE COURANTE** — 3 fiches écrites à la main servent de banc d'essai |
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
