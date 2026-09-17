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
| **Phase courante** | 05 — API de signal, sandbox, test de causalité (pas encore commencée) |
| **Dernière porte franchie** | **04**, le 2026-09-17 — `scripts/gate_04_registry.py` passe ses 1 484 vérifications. Le registre est incontournable (six contournements essayés, six refusés), le holdout est scellé derrière un jeton qui s'écrit avant |
| **Décision la plus récente** | `decisions/DECISION-05-registre-incontournable.md` — le nombre n'existe pas avant sa ligne : `_pool` et `_deflated_t` sont privées, un IC poolé exige un jeton délivré par le registre, et la ligne est écrite par la |
| **Tests au registre** | 32 |
| **Idées abandonnées recensées** | 16 |
| **Entrées au journal** | 10 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | **nous** — barèmes publics, à dépouiller | la complétude du coût : tant qu'ils sont `null`, `harness/costs.py` ne rend qu'un **plancher** étiqueté, donc tout IC net est un **majorant de performance** (phase 10, et toute lecture nette d'ici là) |

## Prochaine action — reflet de `ETAT.md`

**Phase 05 — API de signal, sandbox, test de causalité.** L'Acte I est clos : le
juge existe, il est calibré, et on ne peut plus l'éviter. L'Acte II commence, et
c'est là que le premier agent entrera en scène — mais pas encore ici.

Ce qui existe déjà : le Panel refuse structurellement le futur (porte 02), et
`evaluate()` reçoit des **scores**, pas un signal — le harnais est délibérément
ignorant de ce qu'est un signal, et rien dans `D04` ne préjuge de cette interface.

Ce que la porte 05 exige, et qui n'existe pas :

1. **Le contrat de la fonction de signal.** Ce qu'elle reçoit (un Panel à une
   date, rien d'autre), ce qu'elle rend, et son empreinte propre — `D05` laisse
   ouvert le `code_hash` du **code de signal**, distinct de celui du harnais.
   C'est ici qu'il se fixe.
2. **Le scan AST et l'exécution isolée.** `gate_04_registry.py` §6 contient déjà
   le squelette d'un scan syntaxique du dépôt ; la sandbox de signal est un
   travail voisin, en plus strict.
3. **Le test de causalité** : recalculer le signal en ne lui donnant que le passé,
   et **attraper un look-ahead injecté exprès**. Un test qui n'a jamais rien
   attrapé n'est pas un test.

**Un point à trancher avant, et il n'est pas technique.** Le plan de montage fait
des « cinq signaux codés à la main dont tu connais déjà la réponse » le banc
d'essai de cette porte — et des portes 06 et 08. `signals/` est vide et ces
signaux n'existent pas (décision de l'opérateur, 2026-09-17). Il faut donc soit
coder deux à cinq signaux de référence intraday (`corpus/AMORCE.md`, entrées 1, 2
et 6 — Gao 2018, Baltussen 2021, Wen 2021), soit une décision écrite qui
redéfinit les portes 05, 06 et 08 sans vérité terrain. **Ne pas ouvrir la phase 05
avant d'avoir tranché ça** : c'est le banc d'essai qui définit la porte.

## Les 8 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-17 | `gate` | PORTE 04 FRANCHIE : D05 écrite (le nombre n'existe pas avant sa ligne — jeton délivré par le registre, `_pool` et `_deflated_t` privées, écriture par la fonction qui produit la valeur), jeton de descellage du holdout dans panel/unseal.py, registry/SCHEMA.md appliqué à l'écriture, gate_04_registry.py ; harnais modifié donc porte 03 rejouée | 1 484 vérifications ; 6 contournements essayés et refusés, 5 refus sur le holdout, 27 modules passés à l'AST ; code_hash 8c1b6512 -> 5d6ce982, les 25 lignes antérieures périmées pour un coût nul (counted_tests = 0) ; porte 03 rejouée à l'identique (IC +0,00108, t +0,06) ; L09, F15, F16 ; phase courante = 05 |
| 2026-09-17 | `audit` | Reprise du travail poussé depuis le second poste, rejoué de zéro sur celui d'Arthur (RSL_DATA_DIR = D:\quant-data\Cotations) : uv sync, validateur du catalogue, portes 01, 02 et 03 ; corrections de péremption — la note « sur cette machine » de [[reference/ou-trouver-les-donnees]] devenue fausse à deux postes, et les deux todos du catalogue qui bloquaient encore « la calibration du harnais, phase 03 » alors que la porte 03 est franchie | rien ne manquait : catalogue VALIDE, portes 01/02/03 franchies aux mêmes comptes (103 et 41 vérifications), registre 22 -> 25 lignes (3 calibrations, 0 test compté) ; restent ouverts le moteur tiers (phase 10) et les deux todos multipliers/fees |
| 2026-09-17 | `audit` | Vérification des phases 02 et 03 : couverture des portes étendue de 3-4 instruments à l'univers entier (porte 02 : 103 vérifications, 9/9 ; porte 03 : 41, 25/25 cellules, IC parfait sur 5 958 995 observations) ; contournement de l'invariant III démontré et l'IC produit inscrit au registre (stage 04-audit) | les deux portes tiennent sur tout l'univers ; deux trous nommés : slippage_bp jamais déclaré (D01 §7), et evaluate() contournable — porte 04 |
| 2026-09-17 | `gate` | PORTE 03 FRANCHIE : D04 écrite, paquet harness/ (IC Spearman par cellule, poolé par observations, t déflaté de √h puis de √(9/4,224), coût rendu comme plancher étiqueté, écriture au registre à chaque IC) et gate_03_harness.py | 19/19 ; score parfait -> IC 1.000000000, seconde implémentation à 1e-12, bruit -> IC +0,00108 et t final +0,06 ; harnais FIGÉ ; phase courante = 04 |
| 2026-09-17 | `gate` | PORTE 02 FRANCHIE : dates de roulement obtenues du fournisseur par symbology.resolve (527, facturé 0,00 $), comparées AVANT adoption (compare_rolls.py) puis déposées au catalogue ; clause 3b réécrite sur les instruments réels ; L06, L07, L08 | gate_02_panel.py 43/43 ; détection empirique mesurée à 62,8 % de rappel et 67 faux positifs ; GC n'est pas mensuel (5,07/an) ; FDAX oscille ; phase courante = 03 |
| 2026-09-17 | `mesure` | Deux vérifications : le raccord à 00:00 UTC tombe dans la fenêtre ASIA (19:00 NY en hiver, 20:00 en été) — pas dans la plage morte ; et les dates de roulement sont récupérables chez Databento par Historical.symbology.resolve (intervalles d0/d1/s, continuous -> raw_symbol), pas depuis nos fichiers | contrainte inscrite pour la phase 03 ; la demande à l'auteur des données devient précise |
| 2026-09-17 | `setup` | Emplacement des données fixé sur le poste de travail : RSL_DATA_DIR = C:\Users\Mathis\Desktop\Cotations (hors OneDrive) ; porte 01 rejouée sur les deux copies présentes | empreintes identiques à la ligne de base des deux côtés, catalogue valide, porte 02 inchangée (30/31) |
| 2026-09-17 | `phase` | Phase 02 complétée côté code : panel/rolls.py, l'ajustement multiplicatif à rebours (D01 §6), prouvé sur un cas synthétique — sauts retirés, rendements préservés, facteur d'échelle entre deux dates de construction, mouvement de la minute de raccord injecté et mesuré ; truncate() refuse aussi de sortir de la tranche par le bas | 30 vérifications sur 31 ; porte 02 toujours NON franchie — ce qui manque est de la donnée, pas du code |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 13 |
| `phases` | 4 |
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
