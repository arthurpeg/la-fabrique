---
type: research
updated: 2026-09-16
status: repere
ref: Bollerslev, Hood, Huss & Pedersen (2018)
amorce_entry: 12
fiche: null
implementable: oui
sources: [corpus/AMORCE.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Bollerslev, Hood, Huss & Pedersen (2018) — Risk everywhere: modeling and managing volatility

*RFS* 31(7):2729-2773.
[PDF](https://public.econ.duke.edu/~boller/Published_Papers/rfs_18.pdf)

## Ce que le papier affirme

Les motifs de volatilité réalisée sont **très semblables au sein et entre classes
d'actifs**, et une estimation **en panel** bat les modèles individuels hors
échantillon. Intraday, 50+ futures — matières premières, devises, indices, taux —
sur plus de 20 ans.

## Ce qu'il exige comme données

Prix intraday de futures. Notre univers.

## Pourquoi ça nous concerne — et c'est structurel, pas thématique

C'est **la justification directe du *pooling* entre instruments** retenu par
`D01` §2 pour la métrique de la phase 03. Sans elle, pooler l'IC entre neuf
instruments serait une commodité de calcul ; avec elle, c'est un choix documenté.

Cette page est donc citée depuis [[concepts/ic]] et
[[phases/phase-03-harnais-ic]] : si elle tombe, la métrique du projet est à
rouvrir.

## Réserves — écrites avant de tester

- Le papier porte sur la **volatilité**, pas sur le rendement attendu. La
  similarité des dynamiques de volatilité entre actifs ne démontre pas la
  similarité des dynamiques de signal. Le *pooling* de l'IC s'appuie dessus par
  analogie, et cette analogie est une hypothèse, pas un résultat du papier.
- L'estimation en panel gagne hors échantillon *en moyenne*. Ça ne dit rien du
  comportement dans la queue, là où notre largeur réalisée tombe sous 3 paris
  ([[concepts/largeur-effective]]).

## Statut chez nous

Non lu intégralement — et c'est la référence de méthode qu'il faudrait lire en
premier, puisqu'une contrainte de la phase 03 en dépend.

## Voir aussi

[[concepts/ic]] · [[phases/phase-03-harnais-ic]] ·
[[research/harvey-2016-cross-section]]
