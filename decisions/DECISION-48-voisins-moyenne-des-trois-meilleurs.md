# D48 — Un voisin vaut la moyenne de ses trois meilleurs morceaux

**Date :** 2026-10-02
**Phase :** 09
**État :** prise — demande de l'opérateur (« améliore la recherche des voisins ») ; modifie `D45`, ne touche ni au harnais ni au registre

## La question

Au premier dossier (`D47`, Baltussen 2021), 7 voisins sur 8 parlaient du même
sujet sans décrire le même mécanisme. Comment mieux classer les voisins, et
comment le juger autrement qu'à l'œil ?

## Les options

L'étalon a été fixé **avant** de comparer les méthodes
(`scripts/banc_voisins.py`) : les fiches que les grappes de `D39` réunissent
doivent se retrouver mutuellement parmi leurs dix premiers voisins, soit
21 graines et 38 papiers-frères attendus. Résultats
(`scripts/out/banc_voisins.json`) :

| Méthode | Frères dans les 10 premiers | Rang médian | Jamais trouvés |
|---|---|---|---|
| 0. Un papier = son meilleur morceau (`D45`) | 0,29 | 32 | 1 |
| **1. Un papier = la moyenne de ses 3 meilleurs morceaux** | **0,37** | 21 | 1 |
| 2. Méthode 1 + préfixe de requête de `bge` | 0,37 | 21 | 3 |
| 3. Mécanisme et construction cherchés à part, fusionnés | 0,18 | 39 | 2 |
| 4. Méthode 3 + reclassement par cross-encodeur | 0,32 | 30 | 2 |
| 5. Moyenne des 5 meilleurs morceaux | 0,32 | 22 | 1 |
| 6. Méthode 1 + reclassement (`bge-reranker-base`, requête : la fiche) | 0,37 | 25 | 1 |
| 7. Méthode 1 + reclassement (requête : le mécanisme) | 0,34 | 23 | 1 |
| 8. Centroïde du papier graine contre centroïdes | 0,34 | 17 | 2 |
| 9. Fusion des méthodes 1 et 8 | 0,37 | 18 | 0 |

## Le choix

La méthode 1, dans `scripts/voisins.py` : au moins 600 morceaux tirés, un
papier noté par la moyenne de ses trois meilleurs morceaux (un manquant compte
zéro).

## Pourquoi

C'est elle qui porte le gain (0,29 → 0,37), pour un coût nul. Le
reclassement n'apporte rien et coûte environ une minute par recherche sur
processeur (0,76 s par paire). La fusion 9 est un peu meilleure sur le rang
et ne perd aucun frère, mais elle demande les centroïdes de tous les papiers :
3 minutes de calcul à chaque recherche, ou une table de plus. Sur 38 paires,
son avantage tient à un ou deux papiers. Sur Baltussen, les voisins
deviennent ceux du mécanisme : « A tug of war: Overnight versus intraday »,
« Beat the Market: An Effective Intraday Momentum Strategy », « Intraday
patterns in the cross-section of stock returns ».

**Ce qui est sacrifié.** L'étalon est biaisé : les grappes viennent de la même
représentation des fiches, et il est petit. Il dit si une méthode retrouve des
parents connus, pas si elle trouve les bons inconnus. La paire écrite à la
main (Baltussen → Gao 2018) n'a pas été retrouvée par son titre en base ; elle
n'est pas comptée.

## Ce que ça verrouille

`scripts/voisins.py` (`TOP`, `PLANCHER`), `scripts/banc_voisins.py`. Le dossier
d'une synthèse est désormais figé sous son propre nom
(`corpus/dossiers/synthese-dossier-<graine>.json`), et ne se re-prépare plus.
Un changement de méthode ne périme donc aucune synthèse déjà jugée.

## Ce qui reste ouvert

- La fusion avec les centroïdes (méthode 9), si une table de centroïdes par
  papier est un jour acceptée.
- Un étalon plus grand et indépendant des fiches, par exemple les références
  croisées entre papiers.
