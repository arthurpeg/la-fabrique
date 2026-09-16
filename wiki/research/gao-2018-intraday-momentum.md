---
type: research
updated: 2026-09-16
status: repere
ref: Gao, Han, Li & Zhou (2018)
amorce_entry: 1
fiche: null
implementable: oui
sources: [corpus/AMORCE.md]
---

# Gao, Han, Li & Zhou (2018) — Market intraday momentum

*JFE* 129(2):394-414. [SSRN 2440866](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866)

## Ce que le papier affirme

Le rendement de la **première demi-heure** prédit **positivement** celui de la
**dernière demi-heure**. Plus fort les jours volatils, à gros volume, et les jours
d'annonce macro. Barres 30 min, SPY 1993-2013 plus dix autres ETF.

## Ce qu'il exige comme données

Prix intraday. Nous les avons à la minute.

## Pourquoi ça nous concerne

C'est la tête de la **famille 1 du corpus — le momentum intra-journalier — qui
porte presque tout**. `corpus/AMORCE.md` compte 12 entrées implémentables mais
seulement **5 à 6 idées indépendantes**, et celle-ci en rassemble quatre
(entrées 1, 2, 4, 6, avec la 5 en variante).

Conséquence écrite d'avance : **si cette famille ne survit pas aux contrôles de la
phase 06, le corpus implémentable se réduit à de la prévision de volatilité** —
utile pour dimensionner une position, incapable d'en décider le sens. Le projet
aurait alors un problème de matière première, pas de méthode. C'est la cinquième
condition de révision de `D01`.

## Réserves — écrites avant de tester

- Univers ETF actions US, pas futures. La transposition est plausible mais n'est
  pas acquise ; [[research/baltussen-2021-hedging-demand]] est le test direct sur
  futures.
- Fenêtre de 30 minutes définie sur la séance de cotation américaine : chez nous,
  ça vit dans la cellule `US` uniquement ([[concepts/cellule]]).
- [[research/mesfin-2026-falsification]] teste 14 familles voisines sur MNQ et
  n'en retient aucune — à coût supposé, voir la réserve de coût.

## Statut chez nous

Non lu intégralement. Fiche à produire en phase 07.

## Voir aussi

[[research/baltussen-2021-hedging-demand]] ·
[[research/mesfin-2026-falsification]] · [[concepts/cellule]]
