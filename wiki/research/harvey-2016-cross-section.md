---
type: research
updated: 2026-09-16
status: repere
ref: Harvey, Liu & Zhu (2016)
amorce_entry: 21
fiche: null
implementable: oui
sources: [corpus/AMORCE.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Harvey, Liu & Zhu (2016) — …and the cross-section of expected returns

*RFS* 29(1):5-68.
[SSRN 2249314](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2249314)

## Ce que le papier affirme

Un facteur nouveau doit franchir **t > 3,0**, pas 2,0, une fois les tests
multiples pris en compte.

## Pourquoi ça nous concerne

C'est une **référence de méthode, contraignante**, pas un signal. `D01` §2 en fait
le calibrage du seuil de FDR, appliqué **dès le premier test** — jamais un t-stat
à 2. C'est ce qui donne son sens au [[concepts/registre]] : sans le compte des
tests, le seuil n'est pas calculable.

Avec [[research/bailey-2014-deflated-sharpe]] et Benjamini & Hochberg (1995), ce
sont les trois références qui contraignent les phases 03 et 04 plutôt que de
proposer quoi que ce soit à tester.

## Réserves

- Le `t > 3,0` est calibré sur la littérature *transversale actions*, avec son
  propre compte de tests publiés. Notre compte à nous est celui du registre, et il
  est différent. Reprendre le seuil tel quel est un point de départ raisonnable,
  pas un résultat transporté — à trancher explicitement en phase 03.
- Notre métrique est en **série temporelle poolée**, pas transversale
  ([[concepts/ic]]). L'esprit transfère ; l'arithmétique demande vérification.

## Statut chez nous

Non lu intégralement. Comme [[research/bollerslev-2018-risk-everywhere]], c'est
une lecture qui devrait précéder la phase 03, pas la suivre.

## Voir aussi

[[concepts/comptage-des-tests]] · [[concepts/registre]] · [[concepts/ic]] ·
[[phases/phase-03-harnais-ic]]
