# D31 — 500 papiers SSRN par actif, versés dans la base avec leur seul résumé

**Date :** 2026-09-28
**Phase :** 09
**État :** prise — complète `D20`, `D21`, `D22` et `D30`

## La question

L'opérateur demande 500 papiers SSRN sur quatre actifs — **pétrole, or,
bitcoin, devises** — versés dans la base. Le texte intégral d'un papier SSRN
n'est pas récupérable par un robot (`D30`, `F60`). Qu'est-ce qui peut entrer
dans la base, sous quelle étiquette, et par quelle requête écrite d'avance ?

## Ce qui est mesuré, le 2026-09-28

Crossref, sur le préfixe `10.2139` (SSRN), ne nous bride pas, et recense :
**9 897** dépôts pour « crude oil », **2 642** pour « gold », **2 505** pour
« bitcoin cryptocurrency », **17 277** pour « foreign exchange currency ». Sur
un échantillon de 5 notices bitcoin, **4 portent leur résumé** (`abstract`),
de 779 à 1 238 caractères. Le résumé est une métadonnée que SSRN dépose
lui-même chez Crossref : le lire ne touche pas ssrn.com.

## Les options

1. **Verser titre, auteurs, année, DOI et résumé, étiquetés comme tels.**
   Retenue. Nouvelle valeur de `papers.text_source` : `abstract`. Un seul
   morceau par papier : le résumé.
2. **Les étiqueter `harvest`.** Écartée : `harvest` dit « texte lu du PDF »
   (`D22`). Un résumé sous cette étiquette serait indiscernable d'un texte
   intégral — exactement la confusion que `D22` a mise dans la donnée pour
   l'interdire.
3. **Attendre le texte intégral.** Écartée comme préalable : il n'existe, par
   robot, que pour les papiers ayant une autre version libre (`D30`). Il reste
   la voie suivante, pas la condition d'entrée.
4. **Relever le plafond de 60 par axe.** Écartée : `D20` le fixe pour tous les
   axes, `check_harvest` (`H1`, `H9`) le garde, et `D21` prévoit la voie
   d'élargissement — **ajouter des axes**. 500 papiers se demandent donc en
   dix axes de 60 au plus, chacun sous un angle réellement distinct.

## Le choix

Dix axes Crossref sur le préfixe SSRN, déclarés ici **avant** le lancement,
mêmes filtre de date (1995), tri (`is-referenced-by-count`) et plafond (60) que
tous les autres :

| Axe | Recherche |
|---|---|
| `ssrn:oil-futures` | `crude oil futures returns volatility` |
| `ssrn:oil-shocks` | `oil price shocks stock returns` |
| `ssrn:oil-forecasting` | `oil price forecasting predictability` |
| `ssrn:gold-returns` | `gold price returns volatility` |
| `ssrn:gold-hedge` | `gold safe haven hedge inflation` |
| `ssrn:bitcoin-returns` | `bitcoin returns volatility predictability` |
| `ssrn:crypto-trading` | `cryptocurrency trading strategy market efficiency` |
| `ssrn:fx-predictability` | `exchange rate returns predictability forecasting` |
| `ssrn:fx-carry-momentum` | `currency carry trade momentum returns` |
| `ssrn:fx-microstructure` | `foreign exchange intraday order flow` |

Le résumé Crossref est conservé dans `harvest.json` (balises JATS retirées) ;
les papiers qui en ont un sont versés dans la base avec `text_source =
'abstract'` et un morceau unique. Le nombre versé est celui que ces dix
requêtes rendent, dédoublonné — **il n'est pas forcé à 500**.

## Pourquoi

Un résumé dit ce que le papier affirme, sur quel actif, à quel horizon — ce
dont la recherche dans la base a besoin, et ce que le trieur de `D15` reçoit
déjà sous une autre forme (une ligne de tableau, `F41`). Il ne dit **pas** ce
que le papier a mesuré, mot pour mot : une fiche ne se bâtit pas dessus.

**Ce qui est sacrifié, et doit se lire partout où ces papiers apparaissent.**

- **Aucune fiche ne peut venir d'un papier `abstract`.** `F2` vérifie les
  citations contre le texte qui fait foi (`D18`) ; un résumé n'en est pas un.
  Pour ficher un de ces papiers, il faut d'abord son texte intégral — autre
  version (`D30`) ou dépôt manuel — puis `D18`.
- **Le tri par citations** favorise les papiers anciens et généraux ; « oil »
  ramènera aussi des papiers de finance d'entreprise. Le moissonneur ne juge
  pas (`F50`) : c'est le trieur qui écartera.
- **Un papier sans résumé chez Crossref** entre dans `harvest.json` mais pas
  dans la base : il n'a aucun texte à y verser.

## Ce que ça verrouille

- `corpus/harvest_axes.yaml` : les dix axes ci-dessus. Une fois lancés, ils ne
  se réécrivent plus (`D21`, `H10`).
- `corpus/harvest.py` : `crossref_url` demande `abstract` ; la découverte
  Crossref le conserve (`abstract` dans chaque travail).
- `vectordb/migrations/003_text_source_abstract.sql` : `text_source` accepte
  `abstract`. `vectordb/vector_db.py` : `TextSource` idem.
- `vectordb/ingest.py --abstracts` : verse les papiers SSRN portant un résumé.

## Ce qui reste ouvert

- **Le texte intégral** de ceux que le trieur retiendra : `D30` (autre version
  avec `HARVEST_MAILTO`, ou dépôt manuel).
- **Le trieur sur résumé.** Son étalon (`D15`) a été rempli sur des lignes de
  tableau, pas sur des résumés ; un résumé est plus riche qu'une ligne. S'en
  servir sur ces papiers demandera de le dire, comme `F41` l'a dit pour le PDF.

## Journal

- **2026-09-28** — décision prise. Résultats du passage ci-dessous.
- **2026-09-28, premier passage — dix axes, tri par citations.** 352 papiers
  nouveaux (fort recoupement entre axes : 55 sur 60 pour `ssrn:gold-returns`),
  304 avec résumé. **Seuls 74 à 110 portent sur l'un des quatre actifs** (mot-clé
  dans le titre ou le résumé ; l'écart tient à la liste de mots-clés, `carry`
  seul ou `carry trade`) ; les autres sont des papiers généraux très cités sur
  les actions ou les taux. Cause : Crossref accepte n'importe quel mot de la
  requête, et le tri par citations fait passer les papiers généraux devant.
- **2026-09-28, second passage déclaré AVANT d'être lancé — huit axes, tri par
  pertinence** (`sort: relevance`, score Crossref), deux par actif, même
  plafond de 60 : `ssrn:oil-price` (`crude oil price`), `ssrn:oil-market`
  (`oil futures market`), `ssrn:gold-price` (`gold price`), `ssrn:gold-market`
  (`gold market investment`), `ssrn:bitcoin-price` (`bitcoin price`),
  `ssrn:crypto-market` (`cryptocurrency market`), `ssrn:fx-dynamics`
  (`exchange rate dynamics`), `ssrn:fx-trading` (`currency market trading`).
  **Ce que ce tri coûte** : le score de pertinence de Crossref est opaque et
  peut bouger d'un jour à l'autre, là où le compte de citations de `D20` est un
  critère externe et lisible. Il est donc restreint à ces axes, inscrit dans
  chaque axe (`sort`), et `check_harvest` (`H10`) refuse désormais qu'un tri
  change sur un axe déjà lancé.
- **2026-09-28, résultat du second passage** : 472 papiers nouveaux, presque
  sans recoupement, **383 sur l'un des quatre actifs (81 %)** contre 21 % au
  premier passage ; 327 avec résumé.
- **2026-09-28, bilan des dix-huit axes** : **824 dépôts SSRN** découverts,
  **631 avec résumé**, 457 portant sur l'un des actifs (dont 308 avec résumé) —
  devises 231, bitcoin et crypto 145, pétrole 121, or 79 (un papier peut
  compter pour deux). Le compte « sur un actif » est un indice par mot-clé,
  pas un tri : il n'a filtré aucune entrée.
- **2026-09-28, versement** : migration `003` appliquée à la base (contrainte
  élargie, 136 papiers existants intacts), puis `ingest.py --abstracts` :
  **609 papiers versés** (`text_source = 'abstract'`, un morceau chacun), 22
  déjà en base sous le même titre ou DOI. La base passe de 136 à **745
  papiers**. Tous les 631 ont été versés sans filtre de pertinence (`F50`) :
  c'est au trieur d'écarter.
