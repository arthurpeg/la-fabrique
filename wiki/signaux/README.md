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
| `gao-2018-intraday-momentum` | `H01` | Gao, Han, Li & Zhou (2018), *JFE* 129(2) — [[research/gao-2018-intraday-momentum]] | **+** | **oui, 2026-09-18 — dans le bruit** |
| `baltussen-2021-intraday-momentum` | `H02` | Baltussen, Da, Lammers & Martens (2021), *JFE* 142(1) — [[research/baltussen-2021-hedging-demand]] | **+** | **oui, 2026-09-18 — dans le bruit** |

Les deux prédisent la **dernière demi-heure** d'une fenêtre de séance, par des
prédicteurs différents : les trente premières minutes pour `H01`, tout le reste
de la fenêtre pour `H02`. Ils sont corrélés **exprès** — accord de signe mesuré à
58,3 % sur 15 822 paires — et ne seront jamais comptés comme deux tests
indépendants.

**Mesurés le 2026-09-18** — les deux premiers tests comptés du projet.
`counted_tests()` vaut **4 pour ces deux hypothèses** — mesure puis reprise sous
`D11`. Chiffres recopiés des rapports d'IC officiels, avec
leur `test_id` ; le registre fait foi.

| | IC poolé | `t` final | Verdict, écrit avant la mesure |
|---|---|---|---|
| `H01` (`T-20260918T065822-2b3e5d`) | −0,01061 | **−1,56** | rien à distinguer du bruit |
| `H02` (`T-20260918T070041-18cf25`) | −0,00432 | **−0,63** | rien à distinguer du bruit |

Chiffres repris sous `D11` le 2026-09-18 ; les premières mesures déflataient le
`t` d'un recouvrement qui n'existe pas à cette fréquence. L'IC est inchangé.

Le signe observé est **négatif** là où les deux prédisaient positif — mais la
clause qui s'applique n'est pas « le motif existe à l'envers », qui exigeait un
`t` final au-delà de 2. Les deux sont **non confirmées, pas retournées**. Et
`H02`, annoncée « au moins aussi forte » que `H01`, est plus faible.

Ce ne sont pas pour autant des idées abandonnées : rien n'a été tué, il n'y avait
rien. Voir `hypotheses/H01…` et `H02…` § Le résultat.

## Un troisième signal, qui n'est pas un étalon

`heston-2010-periodicity` a été écrit le 2026-09-18 pour la **réplication** de la
clause 2 (`D12`), et il est tenu **hors de `REFERENCE`** : les portes 05, 06 et 08
itèrent sur ce dictionnaire, et `D06` leur a donné leur sujet. Il vit dans
`REPLICATION`, avec ses propres contrôles (`scripts/check_heston.py`).

Il diffère des étalons par sa forme : **un score par intervalle de demi-heure**,
pas un par séance — 658 582 scores et 657 470 observations à `m = 1`, soit 99,8 %
de mesurabilité contre 88,6 % pour les étalons.

Son hypothèse `H03` a été mesurée le jour même, sur 52 décalages : **le peigne
n'est pas là**. Dents à +0,00065 contre creux à +0,00056 hors retournement court,
p = 0,25. Seul le retournement court ressort (`j=1` IC −0,0115, `t` −6,14), et
c'est la préface du motif, pas le motif. Voir [[lessons|L15]] et
[[Failed Ideas/ledger#F33]].

## Ce qui a été vérifié sur eux

`scripts/check_signals.py` — 261 vérifications, aucune corrélation calculée :
couverture (25 cellules sur 25, médiane de 633 scores par cellule), dispersion
non nulle, aucun score daté après l'as-of, causalité, et surtout **le nombre
d'observations réellement mesurables**.

Ce dernier contrôle est né en phase 05 et il a immédiatement payé : il répondait
**0 %**. L'ancre tombait trente barres avant la clôture — donc l'horizon sortait
de la fenêtre — à cause d'une comparaison d'horloge en flottants
([[lessons|L10]]). Corrigé, il rend **88,6 %** : 13 876 observations pour
15 669 scores.

Les 11,4 % perdus sont réels : des ancres dont l'horizon de trente **barres** ne
tient pas dans la dernière demi-heure de leur fenêtre, faute de barres. `6A × US`
n'en garde que 30 %, et c'est inscrit comme **exemption écrite** dans
`check_signals.py` plutôt que par un seuil abaissé — pour qu'une nouvelle cellule
qui tomberait sous la barre fasse échouer le contrôle.

Les deux étalons passent par ailleurs la porte 05 : 16 sondes de causalité
chacun, zéro divergence. Voir [[phases/phase-05-api-de-signal]].

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
