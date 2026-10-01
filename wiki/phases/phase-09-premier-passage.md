---
type: phase
updated: 2026-09-29
status: en-cours
sources: [ETAT.md, decisions/DECISION-25-budget-de-tests.md, decisions/DECISION-27-le-lot-de-la-phase-09.md, decisions/DECISION-40-ce-qu-une-hypothese-du-lot-contient.md, scripts/gate_09.py]
---

# Phase 09 — Le premier passage complet

> Page **dérivée, sans autorité**. `ETAT.md` fait foi pour l'état, `decisions/`
> pour les choix, `registry/tests.jsonl` pour les chiffres. En cas de
> contradiction, la source gagne.

## Ce que la porte demande

> La chaîne tourne de bout en bout ; le registre compte tous les tests ; un
> rapport d'IC existe pour chaque signal.

C'est la **première phase qui dépense des tests**. Les huit portes précédentes
n'ont coûté aucune ligne comptée : `counted_tests()` vaut **56** pour trois
hypothèses, toutes trois sans résultat.

## Les quatre décisions qui la gouvernent

| | |
|---|---|
| `D25` | le budget : **Benjamini–Hochberg à `q` = 0,10**, unilatéral au signe pré-enregistré, lot **clos** avant la première mesure. Le dénominateur de la phase 15 reste le registre **entier** |
| `D27` | le lot est un **critère, pas un nombre** : les fiches triées `oui`, plus les `partiel` par transposition d'univers. Jamais celles à donnée manquante ni à horizon incompatible |
| `D28` | **aucune ligne hors protocole** : un signal déjà mesuré ne peut pas entrer dans le lot |
| `D29` | **pas de plis** : une mesure unique sur tout le `pool`, à `asof` 2023-12-29 20:00 UTC |
| `D40` | ce qu'une **hypothèse** contient, et son juge — `hypotheses/score_hypothese.py` |

## Où ça en est, au 2026-09-29

Le lot est **figé** à `N` = 41 depuis le 2026-09-28
(`hypotheses/LOT-09.json`). **Dix hypothèses sont écrites** — `H05` à `H14` — et
passent les sept conditions de `D40`.

**Et trente et une fiches du lot n'ont pas d'hypothèse mesurable**, mesuré fiche
par fiche : 20 ne prédisent aucun **rendement**, 9 ont un horizon hors fenêtre,
2 exigent une donnée que nous n'avons pas. Le recensement est dans
`hypotheses/NON-ECRITES-09.md`, l'abandon au ledger sous
[[Failed Ideas/ledger#F61]].

**Le fait le plus dur à contourner n'est pas un jugement mais du code figé** :
`harness/metric.py` groupe le rendement futur par couple *(séance, fenêtre)*
avant de décaler. Un horizon qui franchit une frontière de séance ne produit
**aucune observation**. Un retard peut vivre dans le **score**, jamais dans
l'horizon.

## Ce qui reste, dans l'ordre

1. **Trancher le sort des 31** — décision de l'opérateur, le lot étant clos. Les
   trois issues sont chiffrées dans [[Failed Ideas/ledger#F61]].
2. **La matrice de corrélation** du lot, `scripts/out/lot_09_correlations.json`.
   Elle n'est pas décorative : **cinq des dix hypothèses portent le même motif**,
   déjà mesuré absent par `H01` et `H03`.
3. **Coder les signaux** — la porte 08 dit comment, et elle est franchie.
4. **Mesurer**, une fois par hypothèse, puis relancer `scripts/gate_09.py`.

**Zéro hypothèse retenue est un résultat VALIDE de la porte** : elle juge que le
protocole a été suivi, pas que la pêche a été bonne.

## Voir aussi

- [[phases/phase-08-codeur-de-signal|Phase 08 — Le codeur de signal]]
- [[concepts/comptage-des-tests|Comptage des tests]] · [[concepts/registre|Registre]] · [[concepts/ic|IC]]
- [[Failed Ideas/ledger]] — `F61`, et `F33` pour le peigne que deux de ces dix hypothèses frôlent
