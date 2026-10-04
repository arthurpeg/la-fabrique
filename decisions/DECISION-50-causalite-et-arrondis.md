# D50 — Le test de causalité juge l'écart relativement à l'échelle du score

**Date :** 2026-10-03
**Phase :** 09
**État :** prise — demande de l'opérateur (« répare aussi le contrôle de
causalité pour les arrondis ») ; modifie `sandbox/causality.py`, hors du
harnais : aucune ligne du registre n'est périmée (même cas que `D27`)

## La question

`S3` refusait tout score qui différait de plus de **1e-12 en absolu** entre le
panel complet et le panel tronqué. Le 2026-10-03, le témoin de
bollerslev-2018 a été refusé trois fois sur des écarts de 1e-12 à 1e-8, et la
fiche a été écartée pour ce motif. Était-ce du bruit d'arrondi ou une vraie
fuite, et quel seuil sépare les deux ?

## Ce qui a été mesuré, avant de choisir

- **La source du bruit.** Le panel tronqué n'a pas les mêmes roulements
  futurs. Ses clôtures recollées passées sont donc **les mêmes à un facteur
  constant près** (×0,98714 pour 6A, ×0,99186 pour ES, ×1,03420 pour 6J), et
  leurs log-rendements diffèrent d'**au plus 8,9e-16** pour un rendement
  typique de 1e-4. Un calcul mal conditionné, comme une régression sur quatre
  moyennes exponentielles colinéaires, amplifie ce bruit jusqu'à 1e-8 en
  relatif. Le seuil absolu de 1e-12 l'attrapait.
- **Les signaux honnêtes de la session** s'écartent de 1e-13 à **4e-8** en
  relatif.
- **Les quatre tricheurs de `sandbox/tainted.py`**, mesurés sur 16 sondes :
  `forward_return` et `next_bar` sont attrapés par « disparu » à 16 sondes sur
  16 ; `full_sample_zscore` par la valeur à 16/16, écart relatif médian 0,26 ;
  `window_close` par la valeur à 13/16, écart relatif médian 1,0. Les trois
  sondes restantes de `window_close` ne montrent que du bruit (~1e-13) et
  n'étaient déjà pas attrapées sous l'ancien seuil.

## Les options

1. **Garder 1e-12 en absolu.** Cela refuse des signaux honnêtes dès qu'ils
   calculent de façon un peu instable, et pousse les codeurs vers des
   contournements comme le passage en float32 (`L28`, vu le 2026-10-03).
2. **Rendre les prix passés identiques au bit près**, en recollant vers
   l'avant. C'est causal par construction, mais cela change le Panel (`D03`)
   et les niveaux de prix de tous les signaux : trop large pour ce problème.
3. **Une tolérance relative à l'échelle du score**, en gardant le plancher
   absolu d'origine.

## Le choix

L'option 3. Un écart n'est une divergence que s'il dépasse **à la fois**
1e-12 en absolu **et** 1e-6 en relatif. L'échelle relative est le plus grand
de |score complet|, |score tronqué| et la médiane des |scores| de la cellule.

## Pourquoi

Il y a dix ordres de grandeur de marge : le bruit honnête va jusqu'à 4e-8,
les vrais tricheurs commencent à 5e-2. Rejoué sur la porte 05, chaque
tricheur est attrapé à exactement les mêmes sondes qu'avant. Un score qui
bouge de plus d'un millionième quand seule l'échelle des prix passés change
n'est pas reproductible, et il reste refusé : c'était le cas du témoin
bollerslev au 2ᵉ essai, à 1,9e-5.

Le plancher absolu est conservé. Sans lui, dans une cellule dont la médiane
des scores vaut 0, un score nul contre 1e-17 ferait 100 % d'écart relatif.

**Ce qui est sacrifié.** Un tricheur délibéré pourrait cacher une information
future dans les décimales au-delà du millionième, et s'en servir pour
départager des scores à égalité dans un IC de rang. C'est contrefait, aucun
codeur isolé n'a de raison de le faire, et `scan.py` reste le second rideau.
C'est écrit pour que personne ne prétende l'impossibilité (`F16`).

## Ce que ça verrouille

`sandbox/causality.py` (`RELATIVE_TOLERANCE`). La porte 05, rejouée, est
franchie, 32 vérifications. Le juge de `D23` (`S3`) et la porte 08 en
héritent.

## Ce qui reste ouvert

- **bollerslev-2018** a été écartée le 2026-10-03 avec la preuve « juge »,
  sur un refus que `D50` lève. Rejugés après `D50`, ses deux codages sont
  verts, et son tour 2 de double codage reste **DISCORDANT** (ρ 0,725,
  couverture 0,184). L'écart tient, mais son motif réel est la concordance.
  `LOT-09.json` ne se réécrit pas à la main.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-03 | décision prise et appliquée | porte 05 FRANCHIE (32 vérifications, tricheurs attrapés aux mêmes sondes) ; bollerslev témoin et principal verts ; tour 2 DISCORDANT ρ 0,725 couv 0,184 ; registre 187 → 187 |
