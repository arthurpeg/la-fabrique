# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 8 sur 11)

Tu es un lecteur isolé. Ta seule source est ce fichier : ne lis aucun autre
fichier, aucune commande, aucun accès web.

Pour **chaque** papier ci-dessous (titre et début du texte), rends :

- `mecanisme` : **une phrase de 15 mots au plus**, en français, qui dit **la
  cause et l'effet sur le prix** — par exemple « le rendement de la première
  demi-heure prédit celui de la dernière, dans le même sens », ou « un
  mouvement journalier extrême est suivi d'un retour partiel le lendemain ».
  Écris la cause **générale**, sans nom de pays ni de marché, pour que deux
  papiers sur le même mécanisme reçoivent des phrases proches. Si le papier ne
  propose aucun mécanisme de prix (méthode, mesure de volatilité), dis-le
  ainsi : « pas de mécanisme de prix : <ce qu'il mesure> ».
- `effet` : ce que le papier **annonce** pour ce mécanisme, un seul mot parmi
  `positif_chiffre` (un effet trouvé, avec un chiffre : rendement, Sharpe, t,
  R²), `positif_qualitatif` (un effet trouvé, sans chiffre visible ici),
  `nul_ou_negatif` (pas d'effet, ou l'effet inverse), `non_dit` (le début du
  texte ne le dit pas).
- `chiffre` : pour `positif_chiffre`, la phrase du texte qui porte le chiffre,
  **recopiée à la lettre** ; sinon `null`.

Juge sur le texte, rien d'autre. Ne devine pas un chiffre absent.

## Ce que tu rends

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-08.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W4391217845`

**A blending ensemble learning model for crude oil price forecasting**

> https://doi.org/10.1007/s10479-023-05810-8 ORIGINAL RESEARCH A blending ensemble learning model for crude oil price forecasting Mahmudul Hasan 1 · Mohammad Zoynul Abedin 2 · Petr Hajek 3 · Kristof Coussement 4 · Md. Nahid Sultan 1 · Brian Lucey 5 Received: 4 January 2023 / Accepted: 19 December 2023 © Crown 2024 Abstract To efﬁciently capture diverse ﬂuctuation proﬁles in forecasting crude oil prices, we here pro- pose to combine heterogenous predictors for forecasting the prices of crude oil. Speciﬁcally, a forecasting model is developed using blended ensemble learning that combines various machine learning methods, including k-nearest neighbor regression, regression trees, linear regression, ridge regression, and support vector regression. Data for Brent and WTI crude oil prices at various time series frequencies are used to validate the proposed blending ensemble learning approach. To show the validity of the proposed model, its performance is further benchmarked against existing individual and ensemble learning methods used for predicting crude oil price, such as lasso regression

### id `W2952456832`

**Mean-reversion and optimization**

> arXiv:1408.2217v3 [q-fin.PM] 12 Feb 2016 Mean-Reversion and Optimization Zura Kakushadze §†‡ 1 § Quantigic® Solutions LLC 1127 High Ridge Road #135, Stamford, CT 06905 2 † Department of Physics, University of Connecticut 1 University Place, Stamford, CT 06901 ‡ Free University of Tbilisi, Business School & School of Phys ics 240, David Agmashenebeli Alley, Tbilisi, 0159, Georgia (August 9, 2014; revised September 22, 2014) Abstract The purpose of these notes is to provide a systematic quantit ative frame- work – in what is intended to be a “pedagogical” fashion – for d iscussing mean-reversion and optimization. We start with pair tradin g and add com- plexity by following the sequence “mean-reversion via deme aning → regression → weighted regression → (constrained) optimization → factor models”. We discuss in detail how to do mean-reversion based on this appr oach, including common pitfalls encountered in practical applications, su ch as the diﬀerence between maximizing the Sharpe ratio and minimizing an objec tive function when trading costs are included. We also discuss explicit al

### id `W2582533304`

**Mean-Reverting Portfolio With Budget Constraint**

> arXiv:1701.05016v1 [q-fin.PM] 18 Jan 2017 Submitted paper 1 Mean-Reverting Portfolio Design with Budget Constraint Ziping Zhao, Student Member, IEEE, and Daniel P. Palomar, Fellow, IEEE Abstract—This paper considers the mean-reverting portfolio design problem arising from statistical arbitrage in the ﬁn an- cial markets. We ﬁrst propose a general problem formulation aimed at ﬁnding a portfolio of underlying component assets by optimizing a mean-reversion criterion characterizing t he mean-reversion strength, taking into consideration the va riance of the portfolio and an investment budget constraint. Then several speciﬁc problems are considered based on the genera l formulation, and efﬁcient algorithms are proposed. Numeri cal results on both synthetic and market data show that our proposed mean-reverting portfolio design methods can generate cons istent proﬁts and outperform the traditional design methods and th e benchmark methods in the literature. Index Terms—Portfolio optimization, mean-reversion, cointe- gration, pairs trading, statistical arbitrage, algorithm ic trading, quant

### id `W3021426570`

**Testing Market Efficiency, Predictability and Profitability at Pakistan Stock Exchange Using Firm-level Data**

> Journal of Accounting and Finance in Emerging Economies Vol. 6, No 1, 2020 1 Volume and Issues Obtainable at Center for Sustainability Research and Consultancy Journal of Accounting and Finance in Emerging Economies ISSN: 2519-0318 ISSN (E) 2518-8488 Volume 6: Issue 1 March 2020 Journal homepage: www.publishing.globalcsrc.org/jafee Testing Market Efficiency, Predictability and Profitability at Pakistan Stock Exchange Using Firm-level Data 1 Syed Arshad Ali Shah, 2Naimat Ullah Khan, 3 Muhammad Daud Ali 1 PhD Scholar at Institute of Management Studies, University of Peshawar Pakistan Email: arshad@bkuc.edu.pk 2 Assistant Professor at Institute of Management Studies, University of Peshawar ,Pakistan: Email: naimatims@yahoo.com 3 Assistant Professor Department of Management Sciences, University of Haripur, Pakistan: Email: dr.daud@uoh.edu.pk ARTICLE DETAILS ABSTRACT History Revised format: February 2020 Available Online: March 2020 This study examines market efficiency in the light of the simple moving average technical trading rules on daily closing share prices of 100 companies listed 

### id `W2976667200`

**HUELUM Trading System: A Low-Frequency Algorithm Proposal**

> Revista Mexicana de Economía y Finanzas Nueva Época Volumen 14 Número 4, Octubre - Diciembre 2019, pp. 651-669 DOI: https://doi.org/10.21919/remef.v14i4.435 Huelum Trading System: A Low-Frequency Algorithm Proposal Ana Lorena Jiménez Preciado 1 Instituto Politécnico Nacional, México Segundo Lugar, Categoría Investigación Financiera Empresarial, XXXIV Premio de Investigación Financiera IMEF-EY 2018 Salvador Cruz Aké 2 Instituto Politécnico Nacional, México César Gurrola Ríos 3 Universidad Juárez del Estado de Durango, México (Recepción: 18/marzo/2018, aceptado: 29/julio/2018) Abstract This paper aims to build a set of algorithmic trading strategies to capture the persistence of ﬁnancial series. HUELUM Trading System is proposed to make algorithmic trading in a low-frequency environment and is tested with the Exchange Traded Fund (ETF) iSha- res NAFTRAC daily prices. HUELUM Trading System includes one mean and one trend technical analysis indicators which are compared to a buy hold strategy as a benchmark. The strategy’s implementation is recommended for moderate-high risk proﬁles and 

### id `W3122943125`

**Short-Term Price Overreactions: Identification, Testing, Exploitation**

> Comput Econ (2018) 51:913–940 https://doi.org/10.1007/s10614-017-9651-2 Short-Term Price Overreactions: Identiﬁcation, Testing, Exploitation Guglielmo Maria Caporale 1,2,3 · Luis Gil-Alana4 · Alex Plastun5 Accepted: 18 January 2017 / Published online: 7 February 2017 © The Author(s) 2017. This article is published with open access at Springerlink.com Abstract This paper examines short-term price reactions after one-day abnormal price changes and whether they create exploitable proﬁt opportunities in various ﬁnan- cial markets. Statistical tests conﬁrm the presence of overreactions and also suggest that there is an “inertia anomaly”, i.e. after an overreaction day prices tend to move in the same direction for some time. A trading robot approach is then used to test two trading strategies aimed at exploiting the detected anomalies to make abnormal proﬁts. The results suggest that a strategy based on counter-movements after overreactions does not generate proﬁts in the FOREX and the commodity markets, but in some cases it can be proﬁtable in the US stock market. By contrast, a strategy 

### id `W2772611570`

**A computing platform for pairs-trading online implementation via a blended Kalman-HMM filtering approach**

> A computing platform for pairs‑trading online implementation via a blended Kalman‑HMM filtering approach Anton Tenyakov1 and Rogemar Mamon2* Introduction Pairs trading is an investment strategy used to exploit financial markets that are out of equilibrium. It consists of a long position in one security and a short position in another security at a predetermined ratio; see Elliott et al. [ 1]. Traders bet on the direction of the stocks relative to each other. Such a trading strategy is typically employed by hedge fund companies. Deviations in prices are monitored closely and used as basis for chang - ing positions, taking advantage of market inefficiencies to obtain some profits. Hence, financial computing technologies with algorithmic trading capability, such as the one Abstract This paper addresses the problem of designing an efficient platform for pairs-trading implementation in real time. Capturing the stylised features of a spread process, i.e., the evolution of the differential between the returns from a pair of stocks, exhibiting a heavy-tailed mean-reverting process is also de

### id `W3091830451`

**What Can Machine Learning Tell Us About Intraday Price Patterns in a Frontier Stock Market?**

> http://ijfr.sciedupress.com International Journal of Financial Research V ol. 11, No. 5; 2020 Published by Sciedu Press 205 ISSN 1923-4023 E-ISSN 1923-4031 What Can Machine Learning Tell Us About Intraday Price Patterns in a Frontier Stock Market? Dan Gabriel Anghel1 1 Department of Money and Banking, The Bucharest University of Economic Studies, Romania Correspondence: Dan Gabriel Anghel , Department of Money and Banking, The Bucharest University of Economic Studies, Romania. Tel: 40-723-155-148. E-mail: dan.anghel@fin.ase.ro Received: June 15, 2020 Accepted: July 30, 2020 Online Published: October 4, 2020 doi:10.5430/ijfr.v11n5p205 URL: https://doi.org/10.5430/ijfr.v11n5p205 Abstract Quite a lot. On the one hand, it enables us to classify intraday patterns into 6 unique classes and to show how each class is related to several important market state variables. On the other hand, it enables us to identify the relevant set of variables and define a better model of the drivers of intraday patterns in a frontier stock market. Overall, our results show that intraday patterns in returns i

### id `W2764060935`

**The Nepalese Stock Market: Efficient and Calendar Anomalies**

> ECONOMIC REVIEW 40 The Nepalese Stock Market: Efficient and Calendar Anomalies Dr. Fatta Bahadur K.C.∗ and Nayan Krishna Joshi♣ After describing the various forms of efficiency and calendar anomalies observed in many developed and emerging markets according to the existing literature, the present study examines this phenomenon empirically in the Nepalese stock market for daily data of Nepal Stock Exchange Index from February 1, 1995 to December 31, 2004 covering approximately ten years. Using regression model with dummies, we find persistent evidence of day-of-the- week anomaly but disappearing holiday effect, turn-of-the-month effect and time-of- the-month effect. We also document no evidence of month-of-the-year anomaly and half-month effect. Our result for the month-of-the-year anomaly is consistent to the finding observed for the Jordanian stock market and that for the day-of-the-week anomaly to the Greek stock market .In addition, our finding regarding half-month effect is consistent with the US market. For the rest, we find inconsistent results with that in the international ma

### id `W2096575092`

**The near-extreme density of intraday log-returns**

> arXiv:1106.0039v1 [q-fin.ST] 31 May 2011 The near-extreme density of intraday log-returns Mauro Politi a,b,c, Nicolas Millot b, Anirban Chakraborti b aSSRI & Department of Economics and Business, International Christian University, 3-10-2 Osawa, Mitaka, Tokyo, 181-8585 Japan bChaire de Finance Quantitative, Laboratoire de Math´ ematiques Appliqu´ ees aux Syst` emes, ´Ecole Centrale Paris, 92290 Chˆ atenay-Malabry, France cBasque Center for Applied Mathematics, Bizkaia Technology Park, Building 500, E48160, Derio, Spain Abstract The extreme event statistics plays a very important role in the theo ry and practice of time series analysis. The reassembly of classical theore tical results is often undermined by non-stationarity and dependence between increments. Furthermore, the convergence to the limit distributions can be slow , requir- ing a huge amount of records to obtain signiﬁcant statistics, and th us limiting its practical applications. Focussing, instead, on the closely relate d density of “near-extremes” – the distance between a record and the maxima l value – can render the st

### id `W4280527399`

**Detecting the lead–lag effect in stock markets: definition, patterns, and investment strategies**

> Detecting the lead–lag effect in stock markets: definition, patterns, and investment strategies Yongli Li1* , Tianchen Wang1, Baiqing Sun1* and Chao Liu1,2 Introduction The lead–lag phenomenon, a phenomenon in which a security leads the price movement of another with some time delay, has been empirically evidenced as widely existing in financial markets (Gong et al. 2016). Although the “lead–lag effect” concept has been adopted in many studies (Kobayashi and Takaguchi 2018), few have provided a formal definition of this concept, and its underlying meaning is not always consistent. Some studies have focused on how to generate greater stock returns by utilizing the “lead–lag phenomenon” (Stübinger 2019) but have often failed to mine its embedded features. To this end, this study aims to answer the following questions: (1) Are there several stable patterns in stock markets that are characterized by the lead–lag phenomenon? (2) How can we formally define the lead–lag effect to provide a solid foundation for detecting Abstract Human activities widely exhibit a power-law distribution. Cons

### id `W2136215272`

**Econometrics of Testing for Jumps in Financial Economics Using Bipower Variation**

> Econometrics of testing for jumps in nancial economics using bipower variation Ole E. Barndorff-Nielsen The Centre for Mathematical Physics and Stochastics (MaPhySto), University of Aarhus, Ny Munkegade, DK-8000 Aarhus C, Denmark oebn@imf.au.dk Neil Shephard Nueld College, University of Oxford, Oxford OX1 1NF, UK neil.shephard@nuf.ox.ac.uk September 2, 2004 Abstract In this paper we provide an asymptotic distribution theory for some non-parametric tests of the hypothesis that asset prices have continuous sample paths. We study the behaviour of the tests using simulated data and see that certain versions of the tests have good nite sample behaviour. We also apply the tests to exchange rate data and show that the null of a continuous sample path is frequently rejected. Most of the jumps the statistics identify are associated with governmental macroeconomic announcements. Keywords: Bipower variation; Jump process; Quadratic variation; Realized variance; Semi- martingales; Stochastic volatility. 1 Introduction In this paper we will show how to use a time series of prices recorded at sho

### id `W2891542969`

**Is gold a Sometime Safe Haven or an Always Hedge for equity investors? A Markov-Switching CAPM approach for US and UK stock indices**

> eprints@whiterose.ac.uk https://eprints.whiterose.ac.uk Universities of Leeds, Sheffield and York Deposited via The University of York. White Rose Research Online URL for this paper: https://eprints.whiterose.ac.uk/id/eprint/135932/ Version: Accepted Version Article: He, Zhen, O'Connor, Fergal and Thijssen, Jacco Johan Jacob (2018) Is gold a Sometime Safe Haven or an Always Hedge for Equity Investors? A Markov-Switching CAPM Approach for US and UK Stock Indices. International Review of Financial Analysis. pp. 30- 37. ISSN: 1057-5219 https://doi.org/10.1016/j.irfa.2018.08.010 Reuse This article is distributed under the terms of the Creative Commons Attribution-NonCommercial-NoDerivs (CC BY-NC-ND) licence. This licence only allows you to download this work and share it with others as long as you credit the authors, but you can’t change the article in any way or use it commercially. More information and the full terms of the licence here: https://creativecommons.org/licenses/ Takedown If you consider content in White Rose Research Online to be in breach of UK law, please notify us by em

### id `W2999543369`

**U.S. equity and commodity futures markets: Hedging or financialization?**

> Energy Economics 86 (2020) 104660 Contents lists available at ScienceDirect Energy Economics journal homepage: www.elsevier.com/locate/eneco U.S. equity and commodity futures markets: Hedging or ﬁnancialization?/H22845 Duc Khuong Nguyenab ,*, Ahmet Sensoyc, Ricardo M. Sousad,e, Gazi Salah Uddinf a IPAG Lab, IPAG Business School, Paris, France b Vietnam National University, International School, Hanoi, Vietnam c Bilkent University, Faculty of Business Administration, Ankara, Turkey d University of Minho, Department of Economics and Centre for Research in Economics and Management (NIPE), Braga, Portugal e LSE Alumni Association, London School of Economics and Political Science, London, United Kingdom f Linköping University, Linköping, Sweden ARTICLE INFO Article history: Received 16 August 2016 Received in revised form 4 December 2019 Accepted 11 December 2019 Available online 7 January 2020 JEL classiﬁcation: C58 G10 Keywords: Equity returns Commodity futures returns Hedging Financialization ABSTRACT In this paper, we investigate the hedging versus the ﬁnancialization nature of commod

### id `W3123801885`

**Pinning in the S&P 500 futures**

> Pinning in the S&P 500 futures $ Benjamin Golez a,1, Jens Carsten Jackwerth b,n a Mendoza College of Business, University of Notre Dame, Notre Dame, IN 46556, USA b University of Konstanz, PO Box 134, 78457 Konstanz, Germany JEL classiﬁcation: G11 G12 G13 Keywords: Pinning Futures Options Option expiration Hedging a b s t r a c t W e show that Standard & Poor’s (S&P) 500 futures are pulled towar d the at the money strike price on days when serial options on the S&P 500 futures expire (pinning) and are pushed away from the cost of carry adjusted at the money strike price right before the expiration of options on the S&P 500 index (anti cross pinning). These effects are driven by the interplay of market makers’ rebalancing of delta hedges due to the time decay of those hedges as well as in response to reselling (and early exercise) of in the money options by individual investors. The associated shift in notional futures value is at least $115 million per expiration day. 1. Introduction From ﬁrst principles, stock prices would be expected to be uniformly distributed on any small interva

### id `W2259110364`

**The synchronized and long-lasting structural change on commodity markets: Evidence from high frequency data**

> Munich Personal RePEc Archive The synchronized and long-lasting structural change on commodity markets: evidence from high frequency data Bicchetti, David and Maystre, Nicolas United Nations Conference on Trade and Development - UNCTAD 20 March 2012 Online at https://mpra.ub.uni-muenchen.de/37486/ MPRA Paper No. 37486, posted 20 Mar 2012 14:13 UTC The synchronized and long-lasting structural change on commodity markets: evidence from high frequency data David Bicchetti Nicolas Maystre 1 20 March 2012 Abstract This paper analyses the intraday co-movements betwe en returns on several commodity markets and on the stock market in the Un ited States over the 1997- 2011 period. By exploiting a new high frequency dat abase, we compute various rolling correlations at (i) 1-hour, (ii) 5-minute, (iii) 10-second, and (iv) 1-second frequencies. Using this database, we document a syn chronized structural break, characterized by a departure from zero, which start s in the course of 2008 and continues thereafter. This is consistent with the i dea that recent financial innovations on commodity futur

### id `W3122875290`

**Interpreting financial market crashes as earthquakes: A new Early Warning System for medium term crashes**

> TI 2014-067/III Tinbergen Institute Discussion Paper Interpreting Financial Market Crashes as Earthquakes: A New early Warning System for Medium Term Crashes Francine Gresnigt Erik Kole Philip Hans Franses Tinbergen Institute is the graduate school and research institute in economics of Erasmus University Rotterdam, the University of Amsterdam and VU University Amsterdam. More TI discussion papers can be downloaded at http://www.tinbergen.nl Tinbergen Institute has two locations: Tinbergen Institute Amsterdam Gustav Mahlerplein 117 1082 MS Amsterdam The Netherlands Tel.: +31(0)20 525 1600 Tinbergen Institute Rotterdam Burg. Oudlaan 50 3062 PA Rotterdam The Netherlands Tel.: +31(0)10 408 8900 Fax: +31(0)10 408 9031 Duisenberg school of finance is a collaboration of the Dutch financial sector and universities, with the ambition to support innovative research and offer top quality academic education in core areas of finance. DSF research papers can be downloaded at: http://www.dsf.nl/ Duisenberg school of finance Gustav Mahlerplein 117 1082 MS Amsterdam The Netherlands Tel.: +31(0)20 52

### id `W2801041858`

**Examination of the profitability of technical analysis based on moving average strategies in BRICS**

> R E S E A R C H Open Access Examination of the profitability of technical analysis based on moving average strategies in BRICS Matheus José Silva de Souza 1, Danilo Guimarães Franco Ramos 2, Marina Garcia Pena 2, Vinicius Amorim Sobreiro 2* and Herbert Kimura 2 * Correspondence: sobreiro@unb.br 2Department of Management, University of Brasília, Federal District, Brazil Full list of author information is available at the end of the article Abstract In this paper, we investigated the profitability of technical analysis as applied to the stock markets of the BRICS member nations. In addition, we searched for evidence that technical analysis and fundamental analysis can complement each other in these markets. To implement this research, we created a comprehensive portfolio containing the assets traded in the markets of each BRICS member. We developed an automated trading system that simulated transactions in this portfolio using technical analysis techniques. Our assessment updated the findings of previous research by including more recent data and adding South Africa, the latest member 

### id `W2157988689`

**The Disappearing Calendar Anomalies in the Singapore Stock Market**

> The Lahore Journal of Economics 11 : 2 (Winter 2006) pp. 123-139 The Disappearing Calendar Anomalies in the Singapore Stock Market Wing-Keung Wong*, Aman Agarwal** and Nee-Tat Wong*** Abstract This paper investigates the calendar anomalies in the Singapore stock market over the recent period from 1993-2005. Specifically, changes in stock index returns are examined surrounding January (the January effect), on different days of the week (the day-of-the-week effect), around the turn of the month (the turn-of-the-month effect) and before holidays (the pre-holiday effect). The findings reveal that these anomalies have largely disappeared from the Singapore stock market in recent years. The disappearance of these anomalies has important implications for the efficient market hypothesis and the trading behavior of investors. JEL Code: C10, G12, G15 Keywords: Calendar anomalies, January effe ct, day-of-the-week effect, turn- of-the-month effect, pre-holiday effect. I. Introduction Extensive evidence has been provided on the existence of calendar anomalies in the US and many other countries. T

### id `W2585265408`

**The January Effect: Evidence from Four Arabic Market Indices**

> 144 International Journal of Academic Research in Accounting, Finance and Management Sciences Vol. 7, No.1, January 2017, pp. 144–150 E-ISSN: 2225-8329, P-ISSN: 2308-0337 © 2017 HRMARS www.hrmars.com The January Effect: Evidence from Four Arabic Market Indices Omar GHARAIBEH Department of Finance and Banking, Al al-Bayt University, P.O.BOX 130040, Mafraq 25113, Jordan, E-mail: omar_k_gharaibeh@yahoo.com Abstract This study examines the existence o f January effect in four Arabic market indices for the recent time period, February 1988 to May 2014. These market indices include Jordan, Egypt, Lebanon and Morocco. Using the OLS and GARCH (1, 1) approach, the results of this paper indicate that January returns provide positive profits and highly statistical significant, especially in Jordanian and Moroccan market indices. For the Egyptian and Lebanese market indices, the current study documents a large economic profit in January month. These results are useful to investors who can formulate their investment strategies accordingly. This study is the first to conduct a comprehensive Januar

### id `W2949695413`

**Volatility Is Rough**

> Volatility is rough Jim Gatheral Baruch College, City University of New York jim.gatheral@baruch.cuny.edu Thibault Jaisson∗ CMAP, ´Ecole Polytechnique Paris thibault.jaisson@polytechnique.edu Mathieu Rosenbaum LPMA, Universit´ e Pierre et Marie Curie (Paris 6) mathieu.rosenbaum@upmc.fr October 14, 2014 Abstract Estimating volatility from recent high frequency data, we revisit the question of the smoothness of the volatility process. Our main result is that log-volatility behaves essentially as a fractional Brownian motion with Hurst exponent H of order 0 .1, at any reasonable time scale. This leads us to adopt the fractional stochastic volatility (FSV) model of Comte and Renault [16]. We call our model Rough FSV (RFSV) to underline that, in contrast to FSV, H < 1/2. We demonstrate that our RFSV model is remarkably consistent with ﬁnancial time series data; one application is that it enables us to obtain improved forecasts of realized volatility. Furthermore, we ﬁnd that although volatility is not long memory in the RFSV model, classical statistical procedures aiming at detecting vola

### id `W2912238300`

**Expiration day effects on European trading volumes**

> Empirical Economics (2020) 58:1603–1638 https://doi.org/10.1007/s00181-019-01627-2 Expiration day effects on European trading volumes Bogdan Batrinca 1 · Christian W. Hesse 1 · Philip C. Treleaven 1 Received: 25 July 2016 / Accepted: 18 October 2018 / Published online: 22 January 2019 © The Author(s) 2019 Abstract This study investigates the effect of periodic events, such as the stock index futures and options expiration days and the Morgan Stanley Capital International (MSCI) quar- terly index reviews, on the trading volume in the pan-European equity markets. The motivation of this study stems from anecdotal evidence of increased trading volume in the equity markets during the run-up to the index options and futures expiration days and MSCI rebalances. This study investigates this phenomenon in more detail and analyses the trading volumes of seven European stock indices and the MSCI Interna- tional Pan-Euro Price Index. The analysis features a multi-step ahead volume forecast, which is important for practitioners in order to plan multi-day trades while looking to minimise the marke

### id `W4207056946`

**A residual driven ensemble machine learning approach for forecasting natural gas prices: analyses for pre-and during-COVID-19 phases**

> https://doi.org/10.1007/s10479-021-04492-4 ORIGINAL RESEARCH A residual driven ensemble machine learning approach for forecasting natural gas prices: analyses for pre-and during-COVID-19 phases Rabin K. Jana 1 · Indranil Ghosh 2 Accepted: 7 December 2021 © The Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature 2021 Abstract The natural gas price is an essential ﬁnancial variable that needs periodic modeling and predictive analysis for many practical implications. Macroeconomic euphoria and external uncertainty make its evolutionary patterns highly complex. We propose a two-stage granular framework to perform predictive analysis of the natural gas futures for the USA (NGF- USA) and the UK natural gas futures for the EU (NGF-UK) for pre-and during COVID-19 phases. The residuals of the previous stage are introduced as a new explanatory feature along with standard technical indicators to perform predictive tasks. The importance of the new feature is explained through the Boruta feature evaluation methodology. Maximal Overlap Discrete Wavel

### id `W4402809305`

**Downside risk reduction using regime-switching signals: a statistical jump model approach**

> Downside Risk Reduction Using Regime-Switching Signals: A Statistical Jump Model Approach∗ Yizhan Shu† Chenyu Yu† John M. Mulvey† ‡ August 24, 2024 Abstract This article investigates a regime-switching investment strategy aimed at mitigating downside risk by reducing market exposure during anticipated unfavorable market regimes. We highlight the statistical jump model (JM) for market regime identification, a recently developed robust model that distinguishes itself from traditional Markov-switching models by enhancing regime persistence through a jump penalty applied at each state transition. Our JM utilizes a feature set comprising risk and return measures derived solely from the return series, with the optimal jump penalty selected through a time-series cross-validation method that directly optimizes strategy performance. Our empirical analysis evaluates the realistic out-of-sample performance of various strategies on major equity indices from the US, Germany, and Japan from 1990 to 2023, in the presence of transaction costs and trading delays. The results demonstrate the consisten

### id `W4292713980`

**TRADING STOCK MARKET INDICES. A SIMPLE APPROACH**

> Revista Economică 73:1 (2021) 64 TRADING STOCK MARKET INDICES. A SIMPLE APPROACH Adrian MOROȘAN1 Lucian Blaga University of Sibiu, Romania Abstract In this article we will present a simple model that can be used by the people that don't have profound financial knowledge and, despite that , could be tempted to try to obtain gains on different financial markets without paying a professional. In fact, the model presented here is developed on some ideas that we presented before in an article on the sports betting industry, adapted to the financial markets. The general ideea that we will present in detail in this article is that someone can start and stop trading market indices looking at just one indicator that can be found everywhere: the trading volume. The position that should be taken is, i n our opinion, in the opposite way of the last trend that that was ended by the high market volume. In the end, the following article represents just a case study made on the general principles presented here taking into consideration a concrete market. We will try to present the model that we dev

### id `W1996897705`

**Pinpoint and synergistic trading strategies of candlesticks**

> www.ccsenet.org/ijef International Journal of Economics and Finance V ol. 3, No. 1; February 2011 ISSN 1916-971X E-ISSN 1916-9728 234 Pinpoint and Synergistic Trading Strategies of Candlesticks Yung-Ming Shiu Department of Business Administration, National Cheng Kung University No.1, University Road, Tainan City 701, Taiwan (R.O.C.) Tel: 886-6-275-7575 ext.53330 E-mail: yungming@mail.ncku.edu.tw Tsung-Hsun Lu (corresponding author) Department of Business Administration, National Cheng Kung University No.1, University Road, Tainan City 701, Taiwan (R.O.C.) Tel: 886-6-208-0137 E-ma il: r4895107@mail.ncku.edu.tw Abstract The candlestick trading strategy is a very popular technical method to convey the growth and decline of the demand and supply in the financial market. In this paper, we aim to investigate the predic tive power of the candlestick two-day patterns, and to determine the key factors to improve performance. The data set of this study includes daily opening, high, low, and closing prices, and daily volumes of all electronic securities in the Taiwan Stock Exchange between 1998

### id `W2017515609`

**Oil Price Volatility, Global Financial Crisis and The Month-of-the-Year Effect**

> www.ccsenet.org/ijbm International Journal of Business and Management V ol. 5, No. 11; November 2010 ISSN 1833-3850 E-ISSN 1833-8119 156 Oil Price Volatility, Global Financial Crisis and The Month-of-the-Year Effect Olowe, Rufus Ayodeji Department of Finance, University of Lagos, Lagos, Nigeria Tel: 234-80-2229-3985 E-mail: raolowe@yahoo.co.uk Abstract This paper investigates the mont h-of-the-year effect in the UK Bren t crude oil market using the GARCH (1,5) and GJR-GARCH (1,5) models in the light of Asian financ ial crisis and the global financial crisis using daily data over the period, January 4, 1988 and May 27, 2009. The result shows the presence of the month-of-the-year effect in volatility but not in the return in the oil market. Ho wever, the pattern of significance of monthly effect in volatility is affected by the choice of model. The significant month-of-the-year effect on volatility may be in line with information availability theory The result shows that the Asian financial crisis has an impact on the oil price return series while the global financial crisis has no imp

### id `W2060211884`

**Should Individual Investors Use Technical Trading Rules to Attempt to Beat the Market?**

> American Journal of Economics and Business Administ ration 2 (3): 201-209, 2010 ISSN 1945-5488 © 2010 Science Publications Corresponding Author: Thomas S. Coe, Department of Finance, Quinnipiac University, 275 Mount Carmel Ave., Hamden, CT 06518 USA 201 Should Individual Investors Use Technical Trading Rules to Attempt to Beat the Market? 1Thomas S. Coe and 2Kittipong Laosethakul 1Department of Finance, Quinnipiac University, 275 Mount Carmel Ave. Hamden, CT 06518 USA 2Department of Accounting and Information Systems, Sacred Heart University, 5151 Park Ave., Fairfield, CT 06825 USA Abstract: Problem statement: Despite widespread academic acceptance of the Effic ient Markets Hypothesis, some stock traders still use technical trading rules in an attempt to beat the market. Approach: This study looked at four trading rules, namely, t he arithmetic moving average, the relative strength index, a stochastic oscillator an d its moving average. These trading rules compare the relationship of current prices to past price pa tterns to generate a signal when to buy and sell stocks. The trading 

### id `W2623588343`

**A Review on the Evolution of Calendar Anomalies**

> Studies in Business and Economics no. 12(1)/2017 - 95 - DOI 10.1515/sbe-2017-0008 A REVIEW ON THE EVOLUTION OF CALENDAR ANOMALIES KUMAR Satish IBS Hyderabad (ICFAI Foundation for Higher Education), India Abstract: In this article, we provide a detailed review on the behavior of calendar anomalies (day– of–the–week, January and turn–of–m onth in particular) to understand their evolution over time. The research in the area of stock market i ndicates negative returns on Monday and positive returns on Friday; however, in the currency markets, results are opposite, that is, the returns on Monday are positive and higher than the returns on Friday which show negative returns. For the January (TOM) effect, the literature suggest that the returns during January (TOM trading days) are higher (lower) than the returns during rest of the year (non–TOM trading days). Further, these calendar anomalies were stronger during the 1980s and 1990s and have gradually diminished in the recent times which indicate t hat the markets have achieved a higher degree of efficiency. Key words: Calendar anomalies; 

### id `W2994035987`

**High-Frequency Lead-Lag Effects and Cross-Asset Linkages: A Multi-Asset Lagged Adjustment Model**

> Copyright and Reuse: Copyright and Moral Rights remain with the author(s) and/or copyright holders. Copies of full items can be used for personal research or study, educational, or not-for-profit purposes without prior permission or charge, unless otherwise indicated, provided that the authors, title and full bibliographic details are credited, a hyperlink and/or URL is given for the original metadata page and the content is not changed in any way. For full details of reuse please refer to City Research Online policy. City Research Online: http://openaccess.city.ac.uk/ publications@citystgeorges.ac.uk Citation: Buccheri, G., Corsi, F. & Peluso, S. (2021). High-Frequency Lead-Lag Effects and Cross-Asset Linkages: A Multi-Asset Lagged Adjustment Model. Journal of Business & Economic Statistics, 39(3), pp. 605-621. doi: 10.1080/07350015.2019.1697699 This is the accepted version of the paper. This version of the publication may differ from the final published version. To cite this item please consult the publisher's version. Permanent repository link: https://openaccess.city.ac.uk/id/epr

