# Amorce du corpus — littérature intraday sur futures

**Date :** 2026-09-15 · **Phase :** 01 · **Univers visé :** 9 futures CME, barres 1 min,
grille actif × séance, détention intraday avec clôture forcée.

Périmètre de la recherche, fixé avant de chercher : momentum intra-journalier,
opening range, saisonnalité intra-séance, overnight contre intraday, périodicité
de la volatilité, effets d'heure, comportement autour des annonces macro.
**Exclus :** microstructure de carnet (je n'ai que de l'OHLCV), et anomalies
transversales sur actions à fréquence mensuelle (ne transfèrent pas à neuf
futures portant quatre paris indépendants).

Colonne « implémentable » : **oui** = calculable avec `open/high/low/close/volume`
à la minute, sur mes neuf instruments, sans donnée extérieure · **partiel** =
exige une donnée que je n'ai pas mais qui est gratuite et obtenable (calendrier
d'annonces), ou un univers différent dont la méthode se transpose · **non** =
exige une donnée que je n'ai pas et qui coûte.

---

## A. Momentum intra-journalier et effets d'heure

| # | Référence | Ce qu'il prédit | Fréquence / univers | Données exigées | Accès | Implémentable |
|---|---|---|---|---|---|---|
| 1 | **Gao, Han, Li & Zhou (2018)**, « Market intraday momentum », *JFE* 129(2):394-414 | Le rendement de la première demi-heure prédit **positivement** celui de la dernière demi-heure ; plus fort les jours volatils, à gros volume, et les jours d'annonce macro | 30 min, SPY 1993-2013 + 10 autres ETF | prix intraday | [SSRN 2440866](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866) | **oui** |
| 2 | **Baltussen, Da, Lammers & Martens (2021)**, « Hedging demand and market intraday momentum », *JFE* 142(1) | Le rendement du reste de la journée prédit celui des 30 dernières minutes ; mécanisme = couverture de gamma court (options, ETF à levier) ; réversion les jours suivants | intraday, **60+ futures** actions, taux, matières premières, devises, 1974-2020 | prix intraday futures | [SSRN 3760365](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365) · [PDF](https://www3.nd.edu/~zda/intramom.pdf) | **oui** — c'est exactement mon univers |
| 3 | **Heston, Korajczyk & Sadka (2010)**, « Intraday patterns in the cross-section of stock returns », *JF* 65(4):1369-1407 | Continuation du rendement aux intervalles de demi-heure **multiples exacts d'une journée** ; persiste 40 séances | 13 intervalles de 30 min, actions US | prix intraday | [SSRN 1107590](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1107590) | **oui** en série temporelle par cellule (le test transversal, lui, ne transfère pas) |
| 4 | **Zarattini, Barbon & Aziz (2024)**, « Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY) » | Position de suivi dès qu'un déséquilibre anormal apparaît dans le prix intraday ; 19,6 %/an, Sharpe 1,33, net de coûts, 2007-2024 | intraday, SPY / ES | prix intraday | [SSRN 4824172](https://ssrn.com/abstract=4824172) | **oui** — mais préprint non arbitré, résultat à traiter comme une hypothèse |
| 5 | **Zarattini & Aziz (2023)**, ORB 5 minutes sur QQQ, SSRN 4416622 ; **Zarattini, Barbon & Aziz (2024)**, « A Profitable Day Trading Strategy For The U.S. Equity Market », SSRN 4729284 | Cassure de l'opening range | 5 min, QQQ / NQ | prix intraday | [SSRN 4729284](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4729284) | **oui** — voir l'avertissement de réplication ci-dessous |
| 6 | **Wen, Gong, Ma & Xu (2021)**, « Intraday momentum and return predictability: evidence from the crude oil market », *Economic Modelling* 95:374-384 | Le motif de Gao et al. transposé au pétrole | intraday, WTI | prix intraday | Economic Modelling | **oui** — porte directement sur CL |
| 7 | **Mesfin (2026)**, « Structural Limits of OHLCV-Based Intraday Signals in MNQ Futures: A Systematic Falsification Study », arXiv:2605.04004 | **Résultat négatif.** 14 familles de signaux prix/volume, aucune ne survit à un coût d'aller-retour réaliste ; rendement brut de 0,07 à 1,50 point par trade contre 2 points de friction supposés | 5 min, MNQ, 947 séances 2021-2025 | OHLCV seul | [arXiv](https://arxiv.org/abs/2605.04004) | **oui** — et c'est le calibrage d'attente le plus proche de ma situation |

> **Sur l'entrée 7.** C'est la référence la plus utile de la liste et la plus
> inconfortable : même univers, même granularité, même pauvreté de données. Deux
> réserves qui ne l'annulent pas mais la bornent. Préprint d'un auteur seul, non
> arbitré. Et surtout sa friction : 2 points d'indice, rapportés au niveau du
> Nasdaq sur 2021-2025 que **mes propres données mesurent** (13 000 à 25 000),
> valent de **8 à 15 bp** l'aller-retour — une quinzaine de fois l'écart d'un
> tick mesuré sur NQ (0,21 bp).
> Une hypothèse de coût quinze fois trop lourde tue n'importe quel signal
> intraday : le résultat mesure peut-être davantage l'hypothèse que les signaux.
> À rejouer avec mon propre modèle de coût — c'est une réplication à inscrire au
> programme de la phase 06.
>
> **CORRECTION DU 2026-09-18 — la seconde réserve ci-dessus est fausse d'un
> facteur 10, et elle est retirée.** Le calcul a été refait sur nos données au
> lieu d'être cité (`scripts/check_mesfin_premise.py`) : 2 points d'indice au
> niveau médian de NQ mesuré sur la tranche `pool` 2021-2023 (**14 688**) valent
> **1,36 bp**, pas 8 à 15. Vérifié par une seconde route depuis le papier
> lui-même : 4,00 $ sur un notionnel MNQ de 29 376 $ font 1,36 bp. Sa friction
> vaut donc **1,7×** notre plancher `NQ × US` (0,79 bp) et **0,9×** notre pire
> cellule (1,55 bp) — et la comparaison lui est encore défavorable à tort, car le
> papier dit en toutes lettres que ses 2 points couvrent « bid-ask spread,
> NinjaTrader exchange fees, and conservative slippage », quand notre plancher est
> un **écart seul**, `fee_bp` et `slippage_bp` étant `null`.
>
> **Son verdict est donc transportable**, et l'entrée 7 doit être lue comme le
> scénario inconfortable annoncé plus bas, pas comme une objection écartée. La
> plage « 13 000 à 25 000 » citée ci-dessus comme mesurée sur mes données ne
> correspond pas non plus à la tranche `pool`, dont le centile 99 est à 17 556.
> La première réserve — préprint d'un auteur seul, non arbitré — tient toujours.
> Voir `LECONS.md` L14 et `corpus/fiches/mesfin-2026-ohlcv-falsification.json`.

> **Sur l'entrée 5.** Une réplication indépendante de l'ORB sur QQQ
> ([dépôt public](https://github.com/giovannibrusco/zarattini-2023-orb-qqq))
> conclut au seuil de rentabilité vers 2,2 ¢/action de slippage, et note que
> **76 % du PnL du filtre de confirmation NQ vient de la seule année 2022**. Un
> signal dont les trois quarts du résultat tiennent à une année n'est pas un
> signal, c'est un régime.

## B. Overnight contre intraday

| # | Référence | Ce qu'il prédit | Fréquence / univers | Accès | Implémentable |
|---|---|---|---|---|---|
| 8 | **Boyarchenko, Larsen & Whelan (2023)**, « The overnight drift », *RFS* 36(9):3502-3547 | Près de **100 % de la prime de risque actions US** est gagnée dans une fenêtre d'**une heure, 02:00–03:00 ET** (ouverture européenne) ; lié aux déséquilibres d'ordres de la clôture précédente | horaire, **futures E-mini S&P**, 24 h sur 24 | [SSRN 3560269](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3560269) · [RFS](https://academic.oup.com/rfs/article-abstract/36/9/3502/7076616) | **oui** — futures, intraday, horaire : directement dans ma cellule EUROPE |
| 9 | **Federal Reserve Bank of New York (2026)**, « The disappearing overnight drift », Liberty Street Economics, juillet 2026 | L'effet ci-dessus **a disparu** | — | [Liberty Street](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/) | **oui** — à lire avant, pas après, le test de l'entrée 8 |
| 10 | **Lou, Polk & Skouras (2019)**, « A tug of war: Overnight versus intraday expected returns », *JFE* 134(1) | Les composantes overnight et intraday d'un même actif portent des primes de signe opposé et persistantes | journalier, actions US | *JFE* | **partiel** — univers actions, mécanisme transposable à une décomposition overnight/intraday de mes futures |

## C. Périodicité et prévision de la volatilité

| # | Référence | Ce qu'il prédit | Fréquence / univers | Accès | Implémentable |
|---|---|---|---|---|---|
| 11 | **Andersen & Bollerslev (1997)**, « Intraday periodicity and volatility persistence in financial markets », *J. Empirical Finance* 4(2-3):115-158 | La périodicité intra-journalière de la volatilité est si forte que **toute dynamique intraday estimée sans l'en purger est fausse** | intraday, change et actions | [PDF](https://finance.martinsewell.com/stylized-facts/volatility/AndersenBollerslev1997b.pdf) | **oui** — et ce n'est pas un signal, c'est un prérequis de normalisation pour tous les autres |
| 12 | **Bollerslev, Hood, Huss & Pedersen (2018)**, « Risk everywhere: modeling and managing volatility », *RFS* 31(7):2729-2773 | Les motifs de volatilité réalisée sont très semblables **au sein et entre classes d'actifs** ; une estimation en panel bat les modèles individuels hors échantillon | intraday, **50+ futures** matières premières, devises, indices, taux, 20+ ans | [PDF](https://public.econ.duke.edu/~boller/Published_Papers/rfs_18.pdf) | **oui** — mon univers, et la justification directe du *pooling* entre instruments |
| 13 | **Patton & Sheppard (2015)**, « Good volatility, bad volatility: signed jumps and the persistence of volatility », *REStat* 97(3):683-697 | La volatilité future dépend davantage de la volatilité des rendements **négatifs** ; un saut négatif élève la volatilité future, un saut positif l'abaisse | intraday, S&P 500 + 105 actions | [PDF](https://public.econ.duke.edu/~ap172/Patton_Sheppard_REStat_2015.pdf) | **oui** — semi-variances réalisées calculables sur barres 1 min |
| 14 | **Corsi (2009)**, « A simple approximate long-memory model of realized volatility », *J. Financial Econometrics* 7(2):174-196 | Modèle HAR : la volatilité réalisée journalière, hebdomadaire et mensuelle prédisent la suivante | journalier à partir d'intraday | *JFE* | **oui** — référence de base pour toute cible de volatilité (**à vérifier** : citation de mémoire, non confirmée en ligne dans cette session) |

## D. Annonces macroéconomiques

| # | Référence | Ce qu'il prédit | Fréquence / univers | Accès | Implémentable |
|---|---|---|---|---|---|
| 15 | **Lucca & Moench (2015)**, « The pre-FOMC announcement drift », *JF* 70(1):329-371 | **+49 bp en moyenne dans les 24 h précédant** une annonce FOMC, 1994-2011, soit l'essentiel du rendement annuel ; absent des Treasuries et des futures monétaires | horaire, actions US et indices internationaux | [SSRN 1923197](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1923197) | **partiel** — exige le calendrier FOMC, gratuit et public, mais absent de mes fichiers : entrée `todo` |
| 16 | **Kurov, Sancetta, Strasser & Wolfe (2021)**, « The disappearing pre-FOMC announcement drift », *Finance Research Letters* | L'effet ci-dessus s'est fortement atténué après 2011 | — | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1544612320315956) | **partiel** — même remarque, et même leçon que l'entrée 9 |
| 17 | **Andersen, Bollerslev, Diebold & Vega (2003)**, « Micro effects of macro announcements: real-time price discovery in foreign exchange », *AER* 93(1):38-62 | Les surprises d'annonce produisent des sauts de moyenne conditionnelle ; **asymétrie** : la mauvaise nouvelle frappe plus fort que la bonne | intraday, change | [AEA](https://www.aeaweb.org/articles?id=10.1257/000282803321455151) | **partiel** — exige calendrier **et surprises** (consensus contre réalisé), donnée payante en pratique |

## E. Carry et structure de terme — la famille que mes données ferment

| # | Référence | Ce qu'il prédit | Données exigées | Implémentable |
|---|---|---|---|---|
| 18 | **Koijen, Moskowitz, Pedersen & Vrugt (2018)**, « Carry », *JFE* 127(2):197-225 | Le carry prédit les rendements en coupe et en série temporelle dans **toutes** les classes d'actifs ; cadre unificateur | **au moins la deuxième échéance** de chaque contrat | **non** |
| 19 | **Gorton, Hayashi & Rouwenhorst (2013)**, « The fundamentals of commodity futures returns », *Review of Finance* 17(1) | Base et stocks expliquent la prime des matières premières | deuxième échéance, données de stocks | **non** |

## F. Momentum en série temporelle — le fond de la littérature CTA

| # | Référence | Ce qu'il prédit | Fréquence | Implémentable |
|---|---|---|---|---|
| 20 | **Moskowitz, Ooi & Pedersen (2012)**, « Time series momentum », *JFE* 104(2):228-250 | Le rendement des 12 derniers mois prédit positivement le suivant, sur 58 futures | mensuel | **partiel** — l'horizon retenu est intraday ; sert de témoin, pas de signal |

## G. Méthode — contraignant pour les phases 03 et 04, pas des signaux

| # | Référence | Ce qu'il impose |
|---|---|---|
| 21 | **Harvey, Liu & Zhu (2016)**, « …and the cross-section of expected returns », *RFS* 29(1):5-68 | Un facteur nouveau doit franchir **t > 3,0**, pas 2,0, une fois les tests multiples pris en compte. [SSRN 2249314](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2249314) |
| 22 | **Bailey & López de Prado (2014)**, « The deflated Sharpe ratio », *JPM* 40(5):94-107 | Le Sharpe doit être dégonflé du **nombre d'essais**, de la non-normalité et de la longueur d'échantillon. [SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) |
| 23 | **Benjamini & Hochberg (1995)**, « Controlling the false discovery rate », *JRSS-B* 57(1):289-300 | La procédure de contrôle du FDR elle-même |
| 24 | **Corwin & Schultz (2012)**, « A simple way to estimate bid-ask spreads from daily high and low prices », *JF* 67(2):719-760 | L'estimateur d'écart employé au bloc A8 — et sa limite : il s'effondre à zéro sur barres 1 min |

---

## Verdict

**24 références, dont 12 directement implémentables** avec mes données telles
qu'elles sont (entrées 1 à 8, 11 à 14), 5 partiellement, 3 fermées, 4 de méthode.

Le seuil de dix est franchi. **Je ne m'en satisfais pas, et voici pourquoi.**

Compter les papiers flatte le résultat. Comptées en **idées indépendantes**, les
douze entrées implémentables se ramènent à **cinq ou six** :

1. le momentum intra-journalier — entrées 1, 2, 4, 6, et la 5 comme variante ;
2. la périodicité des rendements à retard fixe — entrée 3 ;
3. la dérive nocturne par heure — entrée 8, *dont on nous dit déjà qu'elle a disparu* ;
4. la normalisation par la périodicité de la volatilité — entrée 11, qui n'est pas un signal mais une hygiène ;
5. la prévision de volatilité réalisée, sauts signés compris — entrées 12, 13, 14 ;
6. le comportement autour des annonces — entrées 15 à 17, toutes **partielles**,
   toutes suspendues à un calendrier que je n'ai pas encore.

Trois conséquences que je préfère écrire maintenant.

**La famille 1 porte presque tout.** Si le momentum intra-journalier ne survit pas
à mes contrôles, le corpus implémentable se réduit à de la prévision de
volatilité — utile pour dimensionner une position, incapable d'en décider le
sens. Le projet aurait alors un problème de matière première, pas de méthode.

**Deux des six familles sont déjà annoncées mortes** par la littérature
elle-même : la dérive pré-FOMC (entrée 16) et la dérive nocturne (entrée 9). Ce
n'est pas une raison de ne pas les tester — c'en est une de les tester en
sachant, avant de regarder, que le résultat attendu est nul. C'est exactement ce
que l'invariant IV demande.

**La seule famille vraiment orthogonale aux autres est fermée par les données.**
Carry et structure de terme (entrées 18, 19) ne partagent ni mécanisme ni
horizon avec le momentum intraday, et c'est précisément ce qui en ferait le
meilleur complément. Il manque la deuxième échéance. Voir l'option B de la
décision — et sa contre-objection : le carry est un signal de plusieurs jours,
qui ne se loge pas dans une grille intraday à clôture forcée.

---

*Sources vérifiées en ligne le 2026-09-15, sauf l'entrée 14, citée de mémoire et
marquée à vérifier. Aucune référence de cette liste n'a été lue intégralement :
les fiches de la phase 07 restent à produire, et ce sont elles, pas ce tableau,
qui feront foi.*
