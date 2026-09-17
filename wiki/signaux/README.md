---
type: hub
updated: 2026-09-17
status: actif
sources: [ETAT.md, wiki/SCHEMA.md, signals/, decisions/DECISION-06-signaux-de-reference.md]
---

# Signaux — deux étalons, et aucun candidat

`signals/` n'est plus vide, et cela ne veut **pas** dire que la production de
signaux a commencé. Ce qui s'y trouve depuis le 2026-09-17, ce sont **deux
étalons** : des signaux écrits à la main, dont la réponse attendue est connue
d'avance, et dont le seul rôle est de donner un sujet aux portes 05, 06 et 08.
Voir `decisions/DECISION-06-signaux-de-reference.md`.

> **Écrire un étalon à la main n'est pas confondre les deux ordres.** L'étape 02
> de la chaîne — le codage *automatique* d'un signal par un agent — se construit
> en **phase 08** et reste interdite d'ici là. Voir [[concepts/les-deux-ordres]].

## Les deux étalons

| Signal | Hypothèse | Papier | Signe attendu | Mesuré ? |
|---|---|---|---|---|
| `gao-2018-intraday-momentum` | `H01` | Gao, Han, Li & Zhou (2018), *JFE* 129(2) — [[research/gao-2018-intraday-momentum]] | **+** | **non** |
| `baltussen-2021-intraday-momentum` | `H02` | Baltussen, Da, Lammers & Martens (2021), *JFE* 142(1) — [[research/baltussen-2021-hedging-demand]] | **+** | **non** |

Les deux prédisent la **dernière demi-heure** d'une fenêtre de séance, par des
prédicteurs différents : les trente premières minutes pour `H01`, tout le reste
de la fenêtre pour `H02`. Ils sont corrélés **exprès** — accord de signe mesuré à
58,3 % sur 15 822 paires — et ne seront jamais comptés comme deux tests
indépendants.

**Aucun IC n'a été calculé sur eux**, et `counted_tests()` vaut toujours 0. Les
implémenter et les mesurer sont deux gestes ; seul le premier a eu lieu. La
mesure attend les contrôles automatiques de la phase 06 (`D06` § Ce qui reste
ouvert).

## Ce qui a été vérifié sur eux

`scripts/check_signals.py` — 257 vérifications, aucune corrélation calculée :
couverture (25 cellules sur 25, médiane de 633 observations par cellule),
dispersion non nulle, aucun score daté après l'as-of, et la **causalité** — un
panel tronqué rend exactement les mêmes scores qu'un panel qui en sait plus.
Ce dernier contrôle est un avant-goût de la porte 05, pas la porte elle-même :
il constate, il n'attrape rien encore.

## Quand un vrai signal arrivera

Une page par signal, au gabarit `type: signal` de `wiki/SCHEMA.md` § 1.3, portant
son `signal_id`, sa `hypothesis_ref`, sa fiche d'origine et ses `test_ids`.

Rappels du gabarit, parce qu'ils sont faciles à enfreindre :

- **L'hypothèse est recopiée telle qu'écrite avant le test.** Jamais reformulée
  après coup (invariant IV). Elle vit dans `hypotheses/`.
- **Les chiffres ne sont pas retapés ici.** Renvoi au rapport d'IC par `test_id`.
  Une page de wiki n'est jamais une source d'IC (`wiki/SCHEMA.md` § 0).
- **Un signal abandonné exige une ligne** dans [[Failed Ideas/ledger]], avec la
  raison. Ce n'est pas une option.
- Les verdicts nuls ont une page comme les autres — **surtout** eux : le produit
  du projet est *un petit nombre de signaux survivants, accompagnés d'un compte
  honnête du nombre de tests qu'il a fallu pour les trouver*.

## Les autres candidats repérés

Aucun n'est un signal tant qu'il n'a pas de fiche et de code.

- [[research/mesfin-2026-falsification]] — la réplication de la phase 06, pas un
  signal

## Voir aussi

[[phases/phase-04-registre-et-holdout]] · [[concepts/registre]] ·
[[concepts/comptage-des-tests]] · [[index]]
