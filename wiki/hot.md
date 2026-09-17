---
type: hub
updated: 2026-09-17
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-17.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 06 — contrôles automatiques et réplication (pas encore commencée) |
| **Dernière porte franchie** | **05**, le 2026-09-17 — `scripts/gate_05_signal_api.py`, 29 vérifications. Les trois look-ahead injectés (`sandbox/tainted.py`) sont |
| **Décision la plus récente** | `decisions/DECISION-07-contrat-de-signal.md` — un signal est un module qui expose `SIGNAL_ID`, `HYPOTHESIS`, `PAPER`, `EXPECTED_SIGN` et `scores(panel, cells, horizon_bars)` ; il est refusé s'il |
| **Tests au registre** | 39 |
| **Idées abandonnées recensées** | 21 |
| **Entrées au journal** | 12 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action — reflet de `ETAT.md`

**Phase 06 — contrôles automatiques et réplication.** L'Acte II est ouvert : le
juge est incontournable, le signal a un contrat, et un look-ahead injecté se fait
attraper. Ce qui manque maintenant est le filtre qui refuse un signal *avant*
qu'il atteigne le harnais.

Ce que la porte 06 exige :

1. **Les contrôles de dégénérescence.** Un signal constant, ou à 99 % de NaN, est
   rejeté **avant** d'atteindre le harnais — donc avant de consommer une ligne de
   registre. `D07` les a explicitement renvoyés ici.
2. **Couverture, dispersion, autocorrélation, doublons par corrélation.** Une
   partie existe déjà dans `scripts/check_signals.py` et demande à devenir un
   contrôle automatique plutôt qu'un script qu'on lance à la main.
3. **Le détecteur de « trop beau pour être vrai »** : tout IC au-dessus de 0,10
   déclenche un rapport de suspicion (`hypotheses/README.md`).
4. **La réplication**, et c'est la vraie difficulté : rejouer la falsification de
   Mesfin (2026) avec **notre** modèle de coût (`corpus/AMORCE.md`, entrée 7).
   C'est la référence la plus proche de notre situation — même univers, même
   granularité, même pauvreté de données — et sa friction supposée vaut 8 à 15 bp
   quand notre tick mesuré en vaut 0,21.

**C'est ici que `H01` et `H02` seront mesurés pour la première fois**, et ce
seront les deux premiers tests comptés du projet : `counted_tests()` passera de 0
à 2. Ne pas les mesurer avant que les contrôles ci-dessus tournent — c'est
exactement l'ordre que `D06` a fixé.

**Un avertissement pour la session qui mesurera.** Les étalons produisent
13 876 observations pour 15 669 scores : 88,6 %. Les 11,4 % perdus sont des
ancres dont l'horizon de trente barres ne tient pas dans la dernière demi-heure
de leur fenêtre, et `6A × US` n'en garde que 30 % — inscrit comme exemption
écrite dans `check_signals.py`, pas comme seuil abaissé. Voir `L10`.

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-17 | `gate` | PORTE 05 FRANCHIE : D07 écrite (contrat de signal, liste blanche, test de causalité par troncature), paquet sandbox/ — contract, scan, causality, signature, tainted — et gate_05_signal_api.py ; ancre des étalons refaite sur l'horloge du catalogue puis en minutes ENTIÈRES | 29 vérifications ; 3 look-ahead injectés sur 3 attrapés, chacun pour la raison écrite d'avance (disparu, valeur, valeur), les 2 étalons à 0 divergence sur 16 sondes ; deux défauts trouvés par la porte elle-même : le tricheur le plus grossier ne produisait aucun score, et NQ x US rendait 615 scores pour ZÉRO observation — comparaison d'horloge en flottants, 31.000000000000004 <= 31 faux ; mesurabilité 0 % -> 24 % -> 88,6 % ; L10, F19, F20, F21 ; phase courante = 06 |
| 2026-09-17 | `decision` | Banc d'essai des portes 05, 06 et 08 : D06 écrite (deux étalons, pas cinq), hypotheses/ créé avec H01 et H02 pré-enregistrées AVANT toute mesure, signals/ implémenté à la main — gao_2018 (première demi-heure) et baltussen_2021 (reste de la fenêtre), tous deux prédisant la dernière demi-heure ; scripts/check_signals.py pour les contrôles | 257 vérifications : 25 cellules sur 25, 15 822 scores chacun, médiane 633 observations par cellule, causalité vérifiée (panel tronqué = mêmes scores), accord de signe 58,3 % entre les deux ; AUCUN IC calculé, counted_tests toujours 0 ; F17, F18 ; porte 04 rejouée, 32 modules à l'AST |
| 2026-09-17 | `gate` | PORTE 04 FRANCHIE : D05 écrite (le nombre n'existe pas avant sa ligne — jeton délivré par le registre, `_pool` et `_deflated_t` privées, écriture par la fonction qui produit la valeur), jeton de descellage du holdout dans panel/unseal.py, registry/SCHEMA.md appliqué à l'écriture, gate_04_registry.py ; harnais modifié donc porte 03 rejouée | 1 484 vérifications ; 6 contournements essayés et refusés, 5 refus sur le holdout, 27 modules passés à l'AST ; code_hash 8c1b6512 -> 5d6ce982, les 25 lignes antérieures périmées pour un coût nul (counted_tests = 0) ; porte 03 rejouée à l'identique (IC +0,00108, t +0,06) ; L09, F15, F16 ; phase courante = 05 |
| 2026-09-17 | `audit` | Reprise du travail poussé depuis le second poste, rejoué de zéro sur celui d'Arthur (RSL_DATA_DIR = D:\quant-data\Cotations) : uv sync, validateur du catalogue, portes 01, 02 et 03 ; corrections de péremption — la note « sur cette machine » de [[reference/ou-trouver-les-donnees]] devenue fausse à deux postes, et les deux todos du catalogue qui bloquaient encore « la calibration du harnais, phase 03 » alors que la porte 03 est franchie | rien ne manquait : catalogue VALIDE, portes 01/02/03 franchies aux mêmes comptes (103 et 41 vérifications), registre 22 -> 25 lignes (3 calibrations, 0 test compté) ; restent ouverts le moteur tiers (phase 10) et les deux todos multipliers/fees |
| 2026-09-17 | `audit` | Vérification des phases 02 et 03 : couverture des portes étendue de 3-4 instruments à l'univers entier (porte 02 : 103 vérifications, 9/9 ; porte 03 : 41, 25/25 cellules, IC parfait sur 5 958 995 observations) ; contournement de l'invariant III démontré et l'IC produit inscrit au registre (stage 04-audit) | les deux portes tiennent sur tout l'univers ; deux trous nommés : slippage_bp jamais déclaré (D01 §7), et evaluate() contournable — porte 04 |
| 2026-09-17 | `gate` | PORTE 03 FRANCHIE : D04 écrite, paquet harness/ (IC Spearman par cellule, poolé par observations, t déflaté de √h puis de √(9/4,224), coût rendu comme plancher étiqueté, écriture au registre à chaque IC) et gate_03_harness.py | 19/19 ; score parfait -> IC 1.000000000, seconde implémentation à 1e-12, bruit -> IC +0,00108 et t final +0,06 ; harnais FIGÉ ; phase courante = 04 |
| 2026-09-17 | `gate` | PORTE 02 FRANCHIE : dates de roulement obtenues du fournisseur par symbology.resolve (527, facturé 0,00 $), comparées AVANT adoption (compare_rolls.py) puis déposées au catalogue ; clause 3b réécrite sur les instruments réels ; L06, L07, L08 | gate_02_panel.py 43/43 ; détection empirique mesurée à 62,8 % de rappel et 67 faux positifs ; GC n'est pas mensuel (5,07/an) ; FDAX oscille ; phase courante = 03 |
| 2026-09-17 | `mesure` | Deux vérifications : le raccord à 00:00 UTC tombe dans la fenêtre ASIA (19:00 NY en hiver, 20:00 en été) — pas dans la plage morte ; et les dates de roulement sont récupérables chez Databento par Historical.symbology.resolve (intervalles d0/d1/s, continuous -> raw_symbol), pas depuis nos fichiers | contrainte inscrite pour la phase 03 ; la demande à l'auteur des données devient précise |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 13 |
| `phases` | 5 |
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
