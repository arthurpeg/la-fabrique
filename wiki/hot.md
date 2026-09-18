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
| **Décision la plus récente** | `decisions/DECISION-10-empreinte-du-harnais.md` — `registry.code_hash()` empreinte désormais le **contenu** et non les octets (fins de ligne repliées), et |
| **Tests au registre** | 58 |
| **Idées abandonnées recensées** | 28 |
| **Entrées au journal** | 15 |

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

Le point 0 étant réparé, plus rien ne s'interpose : c'est **la prochaine
action du projet**. La fenêtre où un changement de harnais était gratuit se
referme ici.

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

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-18 | `decision` | D10 écrite et appliquée — l'empreinte du harnais porte sur le CONTENU et non sur les octets : .gitattributes fixe `* text=auto eol=lf` (114 fichiers réécrits en LF, aucun contenu committé changé — les blobs étaient déjà en LF), et `registry.code_hash()` replie les fins de ligne avant de hacher ; seule modification de harness/ depuis D08 | empreinte 12f9b2c1 -> e9ef2087, vérifiée IDENTIQUE que les 7 fichiers soient tous en LF ou tous en CRLF ; les 53 lignes antérieures réputées périmées pour un coût NUL — dernière fois que ce sera gratuit ; portes 03/04/05/06 rejouées vertes (41, 2 002, 29, 25 vérifications), registre 53 -> 58 lignes, counted_tests toujours 0 ; F27, F28 ; prochaine action du projet = mesurer H01 et H02 |
| 2026-09-18 | `decision` | D09 écrite — provenance des valeurs externes : trichotomie mesurée/décidée/externe, liste CLOSE des externes corroborées, champs source/source_url/retrieved/quoted/applies_to ; validate.py §8, bloc `provenance:` au catalogue, source_url ajouté à roll_dates.json, scripts/check_provenance.py ; multiplicateurs CME NON relevés — cmegroup.com injoignable depuis le poste (timeout puis ECONNRESET sur 3 URLs) | 33 vérifications, 9 fautes refusées chacune pour la raison écrite d'avance ; le script a trouvé un défaut du garde lui-même — `12500` passait sous « 12,500,000 » par sous-chaîne — corrigé en comparaison numérique ; portes 01 et 02 rejouées vertes, registre inchangé à 53 lignes, counted_tests 0, aucun fichier de harness/ touché ; DÉCOUVERTE hors sujet mais sérieuse : `code_hash()` dépend des FINS DE LIGNE, les 3 empreintes du projet se reproduisent des mêmes blobs git — le harnais n'a jamais changé et gate_04 annonce 53 lignes périmées à tort ; L12, F25, F26 |
| 2026-09-17 | `phase` | Phase 06 ouverte, CLAUSE 1 FRANCHIE : D08 écrite, harness/controls.py (dégénérescence avant le jeton, suspicion qui signale sans bloquer, comparateur de doublons score-contre-score), rapport portant avertissements et cellules refusées, gate_06_controls.py | 25 vérifications ; 4 signaux dégénérés rejetés sans consommer une ligne, 1 cellule morte isolée au milieu de vivantes et nommée dans le rapport, suspicion déclenchée à 0,35 et muette à 0,02 ; le plancher de 2 cellules a cassé la porte 03 (calibration à une cellule) -> dérogation écrite et vérifiée étroite ; L11, F22, F23, F24 ; harnais 5d6ce982 -> 12f9b2c1, portes 03/04/05 rejouées vertes ; CLAUSE 2 (réplication Mesfin) NON franchie et bloquée sur fee_bp/slippage_bp ; counted_tests toujours 0 |
| 2026-09-17 | `gate` | PORTE 05 FRANCHIE : D07 écrite (contrat de signal, liste blanche, test de causalité par troncature), paquet sandbox/ — contract, scan, causality, signature, tainted — et gate_05_signal_api.py ; ancre des étalons refaite sur l'horloge du catalogue puis en minutes ENTIÈRES | 29 vérifications ; 3 look-ahead injectés sur 3 attrapés, chacun pour la raison écrite d'avance (disparu, valeur, valeur), les 2 étalons à 0 divergence sur 16 sondes ; deux défauts trouvés par la porte elle-même : le tricheur le plus grossier ne produisait aucun score, et NQ x US rendait 615 scores pour ZÉRO observation — comparaison d'horloge en flottants, 31.000000000000004 <= 31 faux ; mesurabilité 0 % -> 24 % -> 88,6 % ; L10, F19, F20, F21 ; phase courante = 06 |
| 2026-09-17 | `decision` | Banc d'essai des portes 05, 06 et 08 : D06 écrite (deux étalons, pas cinq), hypotheses/ créé avec H01 et H02 pré-enregistrées AVANT toute mesure, signals/ implémenté à la main — gao_2018 (première demi-heure) et baltussen_2021 (reste de la fenêtre), tous deux prédisant la dernière demi-heure ; scripts/check_signals.py pour les contrôles | 257 vérifications : 25 cellules sur 25, 15 822 scores chacun, médiane 633 observations par cellule, causalité vérifiée (panel tronqué = mêmes scores), accord de signe 58,3 % entre les deux ; AUCUN IC calculé, counted_tests toujours 0 ; F17, F18 ; porte 04 rejouée, 32 modules à l'AST |
| 2026-09-17 | `gate` | PORTE 04 FRANCHIE : D05 écrite (le nombre n'existe pas avant sa ligne — jeton délivré par le registre, `_pool` et `_deflated_t` privées, écriture par la fonction qui produit la valeur), jeton de descellage du holdout dans panel/unseal.py, registry/SCHEMA.md appliqué à l'écriture, gate_04_registry.py ; harnais modifié donc porte 03 rejouée | 1 484 vérifications ; 6 contournements essayés et refusés, 5 refus sur le holdout, 27 modules passés à l'AST ; code_hash 8c1b6512 -> 5d6ce982, les 25 lignes antérieures périmées pour un coût nul (counted_tests = 0) ; porte 03 rejouée à l'identique (IC +0,00108, t +0,06) ; L09, F15, F16 ; phase courante = 05 |
| 2026-09-17 | `audit` | Reprise du travail poussé depuis le second poste, rejoué de zéro sur celui d'Arthur (RSL_DATA_DIR = D:\quant-data\Cotations) : uv sync, validateur du catalogue, portes 01, 02 et 03 ; corrections de péremption — la note « sur cette machine » de [[reference/ou-trouver-les-donnees]] devenue fausse à deux postes, et les deux todos du catalogue qui bloquaient encore « la calibration du harnais, phase 03 » alors que la porte 03 est franchie | rien ne manquait : catalogue VALIDE, portes 01/02/03 franchies aux mêmes comptes (103 et 41 vérifications), registre 22 -> 25 lignes (3 calibrations, 0 test compté) ; restent ouverts le moteur tiers (phase 10) et les deux todos multipliers/fees |
| 2026-09-17 | `audit` | Vérification des phases 02 et 03 : couverture des portes étendue de 3-4 instruments à l'univers entier (porte 02 : 103 vérifications, 9/9 ; porte 03 : 41, 25/25 cellules, IC parfait sur 5 958 995 observations) ; contournement de l'invariant III démontré et l'IC produit inscrit au registre (stage 04-audit) | les deux portes tiennent sur tout l'univers ; deux trous nommés : slippage_bp jamais déclaré (D01 §7), et evaluate() contournable — porte 04 |

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
