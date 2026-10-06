# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 6 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-06.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W4390499283`

**The factor structure of exchange rates volatility: global and intermittent factors**

> Empirical Economics (2024) 67:31–45 https://doi.org/10.1007/s00181-023-02542-3 The factor structure of exchange rates volatility: global and intermittent factors Massimiliano Caporin 1 · C. Vladimir Rodríguez-Caballero 2 · Esther Ruiz 3 Received: 13 May 2023 / Accepted: 27 November 2023 / Published online: 2 January 2024 © The Author(s) 2024 Abstract In this paper, we consider a fractionally integrated multi-level dynamic factor model (FI-ML-DFM) to represent commonalities in the hourly evolution of realized volatili- ties of several international exchange rates. The FI-ML-DFM assumes common global factors active during the 24 h of the day, accompanied by intermittent factors, which are active at mutually exclusive times. We propose determining the number of global factors using a distance among the intermittent loadings. We show that although the bulk of common dynamics of exchange rates realized volatilities can be attributed to global factors, there are non-negligible effects of intermittent factors. The effect of the COVID-19 on the realized volatility comovements is stronger on 

### id `W2735257685`

**Asymmetry in spillover effects: Evidence for international stock index futures markets**

> University of Huddersfield Repository Yarovaya, Larisa, Brzeszczynski, Janusz and Lau, Marco Chi Keung Asymmetry in Spillover Effects: Evidence for International Stock Index Futures Markets Original Citation Yarovaya, Larisa, Brzeszczynski, Janusz and Lau, Marco Chi Keung (2017) Asymmetry in Spillover Effects: Evidence for International Stock Index Futures Markets. International Review of Financial Analysis, 53. pp. 94-111. ISSN 1057-5219 This version is available at http://eprints.hud.ac.uk/id/eprint/33879/ The University Repository is a digital collection of the research output of the University, available on Open Access. Copyright and Moral Rights for the items on this site are retained by the individual author and/or other copyright owners. Users may access full items free of charge; copies of full text items generally can be reproduced, displayed or performed and given to third parties in any format or medium for personal research or study, educational or not-for-profit purposes without prior permission or charge, provided: • The authors, title and full bibliographic details is 

### id `W4206034658`

**Effectiveness of Moving Average Rules During COVID-19 Pandemic: Evidence from Malaysian Stock Market**

> Effectiveness of Moving Average Rules During COVID-19 Pandemic: Evidence from Malaysian Stock Market (Keberkesanan Peraturan Purata Bergerak Semasa Pandemik COVID-19: Bukti dari Pasaran Saham Malaysia) Kelvin Lee Yong Ming Universiti Malaysia Sarawak Mohamad Jais Universiti Malaysia Sarawak ABSTRACT The COVID-19 outbreak significantly impacted the Malaysian stock market. To some extent, the Movement Control Order (MCO) implemented in the country affected the financial performance of listed companies. In consequence investors were quite uncertain of future movements of the stock market. Effective analysis techniques are thus required to study the market movements. Investors shall rely on signals emitted by technical indicators for their investment decisions making. The aim of this study is to examine the performance of the MA rules in Malaysian stock market during the different stages of the MCO. The sample used comprised 30 largest market capitalization stocks listed in the stock market. The period of study spanned 2 January 2020 to 30 August 2020. More than 50% of the buy signals em

### id `W2225627977`

**Can risk explain the profitability of technical trading in currency markets?**

> Can risk explain the profitability of technical trading in currency markets? ECONOMIC RESEARCH FEDERAL RESERVE BANK OF ST. LOUIS WORKING PAPER SERIES Authors Matthew Famiglietti, Yuliya Ivanova, Christopher J. Neely, and Paul A. Weller Working Paper Number 2014-033I Revision Date September 2020 Citable Link https://doi.org/10.20955/wp.2014.033 Suggested Citation Famiglietti, M., Ivanova, Y., Neely, C.J., Weller, P.A., 2020; Can risk explain the profitability of technical trading in currency markets?, Federal Reserve Bank of St. Louis Working Paper 2014-033. URL https://doi.org/10.20955/wp.2014.033 Federal Reserve Bank of St. Louis, Research Division, P.O. Box 442, St. Louis, MO 63166 The views expressed in this paper are those of the author(s) and do not necessarily reflect the views of the Federal Reserve System, the Board of Governors, or the regional Federal Reserve Banks. Federal Reserve Bank of St. Louis Working Papers are preliminary materials circulated to stimulate discussion and critical comment. Can risk explain the profitability of technical trading in currency markets?* Y

### id `W2131375261`

**The cross-quantilogram: Measuring quantile dependence and testing directional predictability between time series**

> The Cross-Quantilogram: Measuring Quantile Dependence and Testing Directional Predictability between Time Series∗ Heejoon Han† Oliver Linton‡ Tatsushi Oka§ Yoon-Jae Whang¶ March 14, 2016 Abstract This paper proposes the cross-quantilogram to measure the quantile dependence between two time series. We apply it to test the hypothesis that one time series has no directional predictability to another time series. We establish the asymptotic dis- tribution of the cross-quantilogram and the corresponding test statistic. The limiting distributions depend on nuisance parameters. To construct consistent conﬁdence in- tervals we employ a stationary bootstrap procedure; we establish consistency of this bootstrap. Also, we consider a self-normalized approach, which yields an asymptoti- cally pivotal statistic under the null hypothesis of no predictability. We provide simu- lation studies and two empirical applications. First, we use the cross-quantilogram to detect predictability from stock variance to excess stock return. Compared to existing tools used in the literature of stock return predict

### id `W4411355321`

**A Comprehensive Methodology for Pairs Trading Strategy and Performance Evaluation**

> Proceedings of ICEMGD 2025 Symposium: The 4th International Conference on Applied Economics and Policy Studies DOI: 10.54254/2754-1169/2025.BJ24017 © 2025 The Authors. This is an open access article distributed under the terms of the Creative Commons Attribution License 4.0 (https://creativecommons.org/licenses/by/4.0/). 53 A Comprehensive Methodology for Pairs Trading Strategy and Performance Evaluation Shizhuo Liao Faculty of Arts and Sciences, University of Toronto, Toronto, Canada shizhuo.liao@mail.utoronto.ca Abstract: This study outlines some integrated approaches for pairs trading and portfolio analysis, focusing on the performance in generating consistent returns under varying market conditions over one year. The relationships between returns and some relevant factors are also explored. Steps for pairs trading involve selecting securities with strong historical associations or return correlations, normalizing their price series, calculating related price statistics, and employing a strategy based on Z -score to identify trading opportunities. Regression a nalysis of performan

### id `W2897308859`

**Portfolio management with targeted constant market volatility**

> Portfolio management with targeted constant market volatility Author: Doan, B; Papageorgiou, N; Reeves, JJ; Sherris, M; Doan, Bao Publication details: Insurance Mathematics and Economics v. 83 pp. 134 - 147 0167-6687 (ISSN); 1873-5959 (ISSN) Publication Date: 2018-11-01 Publisher DOI: https://doi.org/10.1016/j.insmatheco.2018.09.010 License: https://creativecommons.org/licenses/by-nc-nd/4.0/ Link to license to see what you are allowed to do with this resource. Downloaded from http://hdl.handle.net/1959.4/unsworks_54255 in https:// unsworks.unsw.edu.au on 2026-09-30 Portfolio Management with Targeted Constant Market Volatility Bao Doan∗, Nicolas Papageorgiou†, Jonathan J. Reeves‡and Michael Sherris§ July 9, 2018 Abstract Managing equity volatility exposure is fundamental to fund managers, insurance companies and pension funds. This is especially important for product developments including target-date portfolios and variable annuities where volatility management is critical. Empirical evidence shows asymmetry between equity market return and volatility, with returns and conditional vo

### id `W2337520758`

**Fourier Spot Volatility Estimator: Asymptotic Normality and Efficiency with Liquid and Illiquid High-Frequency Data**

> RESEARCH ARTICLE Fourier Spot Volatility Estimator: Asymptotic Normality and Efficiency with Liquid and Illiquid High-Frequency Data Maria Elvira Mancino1☯, Maria Cristina Recchioni2☯* 1 Department of Economics and Management, University of Florence, Florence, Italy, 2 Department of Management, Polytechnical University of Marche, Ancona, Italy ☯ These authors contributed equally to this work. * m.c.recchioni@univpm.it Abstract The recent availability of high frequency data has permitted more efficient ways of comput- ing volatility. However, estimation of volatility from asset price observations is challenging because observed high frequency data are generally affected by noise-microstructure effects. We address this issue by using the Fourier estimator of instantaneous volatility introduced in Malliavin and Mancino 2002. We prove a central limit theorem for this estima- tor with optimal rate and asymptotic variance. An extensive simulation study shows the accuracy of the spot volatility estimates obtained using the Fourier estimator and its robust- ness even in the presence of diffe

### id `W3195128978`

**Optimal pairs trading with dynamic mean-variance objective**

> Mathematical Methods of Operations Research (2021) 94:145–168 https://doi.org/10.1007/s00186-021-00751-z ORIGINAL ARTICLE Optimal pairs trading with dynamic mean-variance objective Dong-Mei Zhu 1 · Jia-Wen Gu 2 · Feng-Hui Yu 3 · Tak-Kuen Siu 4 · Wai-Ki Ching 5 Received: 20 June 2019 / Revised: 3 June 2021 / Accepted: 1 August 2021 / Published online: 25 August 2021 © The Author(s) 2021 Abstract Pairs trading is a typical example of a convergence trading strategy. Investors buy relatively under-priced assets simultaneously, and sell relatively over-priced assets to exploit temporary mispricing. This study examines optimal pairs trading strate- gies under symmetric and non-symmetric trading constraints. Under the assumption that the price spread of a pair of correlated securities follows a mean-reverting Ornstein-Uhlenbeck(OU) process, analytical trading strategies are obtained under a mean-variance(MV) framework. Model estimation and empirical studies on trading strategies have been conducted using data on pairs of stocks and futures traded on China’s securities market. These results 

### id `W2097880690`

**Pairs trading: A copula approach**

> Original Article Pairs trading: A copula approach Received (in revised form): 22nd January 2013 Rong Qi Liew is a student studying Mathematics and Economics at School of Physical and Mathematical Sciences, Nanyang Technological University (NTU), Singapore. Yuan Wu is an Associate Professor in the Division of Banking and Finance, Nanyang Business School, NTU, Singapore. His research interests are in Actuarial Science, Data Mining, Application of Statistics to Business and Finance. Correspondence: Rong Qi Liew, Nanyang Technological University (NTU), Block 48 Bendemeer Road #11-1487, 330048, Singapore. ABSTRACT Pairs trading is a technique that is widely practiced in the financial industry . Its relevance has been constantly tested with updated samples, and its profitability is acknowledged among practitioners and academics. Y et in pairs trading, the notion of correlation is central, and the use of correlation or cointegration as a measure of depen- dency is ultimately its Achilles’ heel. T o overcome this limitation, this article employs the use of copulas, which is much more realist

### id `W4414040773`

**MODELING JUMPS IN INTRADAILY FINANCIAL DATA: A REVIEW OF METHODS AND APPLICATIONS**

> AUGUST, 2025 EDITIONS. INTERNATIONAL JOURNAL OF: TIJSRAT SCIENCE RESEARCH AND TECHNOLOGY VOL. 9 31 E-ISSN 3026-8796 P-ISSN 3027-1991 ODELING JUMPS IN INTRADAILY FINANCIAL DATA: A REVIEW OF METHODS AND APPLICATIONS *BOLARINWA, B.T., **YAHAYA, H.U., **ADEHI, M.U.; & **RAUF, R.I. *Department of Statistics, t he Fed eral Polytechnic, Bida, Nigeria. **Department of Statistics, University of Abuja, Abuja, Nigeria Corresponding Author: bolarinwa.temilola@fedpolybida.edu.ng DOI: https://doi.org/10.70382/tijsrat.v09i9.055 INTRODUCTION n many financial markets, intradaily data recorded at the level of minutes or seconds reveals sudden, occasionally large discontinuities in asset prices or returns commonly referred to as jumps. These jumps are often triggered by macroeconomic announcements, firm -specific news, or shifts in liquidity conditions, including intensified trading during computer-to-computer execution (see Boudt and Petitjean, 2014; Lee and Mykland, 2008). Identification and accurate modeling of such jumps is critical for understanding market microstructure effects , risk management,

### id `W3132304208`

**Covariance matrix forecasting using support vector regression**

> Covariance matrix forecasting using support vector regression Piotr Fiszeder1,2 & Witold Orzeszko3 Accepted: 13 January 2021 # The Author(s) 2021 Abstract Support vector regression is a promising m ethod for time-series prediction, as it has good generalisability and an overall stable behaviour. Recent studies have shown that it can describe the dynamic characteristics of financial processes and make more accurate forecasts than other machine learning techniques. The first main contribution of this paper is to propose a methodology for dynamic modelling and forecasting covariance matrices based on support vector regression using the Cholesky decomposition. The proce- dure is applied to range-based covariance matrices of returns, which are estimated on the basis of low and high prices. Such prices are most often available with closing pricesfor many financial series and contain more information about volatility and relationships between returns. The methodology guarantees the positive definiteness of the forecasted covariance matrices and is flexible, as it can be applied to different

### id `W2952727064`

**Forecasting stock market returns over multiple time horizons**

> Forecasting stock market returns over multiple time horizons Dimitri Kroujiline*1, Maxim Gusev2, Dmitry Ushanov3, Sergey V. Sharov4 and Boris Govorkov2 Abstract I n t h i s p a p e r w e s e e k t o d e m o n s t r a t e t h e p r e d i c t a b i l i t y o f s t o ck m a r k e t r e t u r n s a n d e x p l a i n t h e nature of this return predictability. To this end, we introduce i n v e s t o r s w i t h d i f f e r e n t i n v e s t m e n t horizons into the news‐driven, analytic, agent‐based market mod el developed in Gusev et al. (2015). This heterogeneous framework enables us to capture dynamics at multiple timescales, expanding the model’s applications and improving precision. We study the heterogeneous model theoretically and empirically to highlight essential mechanisms underlying certain market behaviors, such as t r a n s i t i o n s b e t w e e n b u l l ‐ a n d b e a r m a r k e t s a n d t h e s e l f ‐ s i m i l a r b e h a v i o r o f p r i c e c h a n g e s . M o s t importantly, we apply this model to show that the stock market is nearly efficient on intraday timesc

### id `W2001312805`

**It's all about volatility of volatility: Evidence from a two-factor stochastic volatility model**

> Grassi, Stefano and Santucci de Magistris, Paolo (2015) It’s all about volatility of volatility: evidence from a two-factor stochastic volatility model. Journal of Empirical Finance, 30 . pp. 62-78. ISSN 0927-5398. Kent Academic Repository Downloaded from https://kar.kent.ac.uk/49295/ The University of Kent's Academic Repository KAR The version of record is available from https://doi.org/10.1016/j.jempfin.2014.11.007 This document version Author's Accepted Manuscript DOI for this version Licence for this version UNSPECIFIED Additional information Versions of research works Versions of Record If this version is the version of record, it is the same as the published version available on the publisher's web site. Cite as the published version. Author Accepted Manuscripts If this document is identified as the Author Accepted Manuscript it is the version after peer review but before type setting, copy editing or publisher branding. Cite as Surname, Initial. (Year) 'Title of article'. To be published in Title of Journal , Volume and issue numbers [peer-reviewed accepted version]. Available

### id `W2951433598`

**Semi-parametric Conditional Quantile Models for Financial Returns and Realized Volatility**

> Semiparametric Conditional Quantile Models for Financial Returns and Realized Volatility ∗ Filip ˇZikeˇ s† Jozef Barun´ ık‡ First version: 9 December 2010 This version: 20 August 2013 Abstract This paper investigates how the conditional quantiles of future returns and volatility of ﬁnancial assets vary with various measures of ex-post variation in asset prices as well as option-implied volatility. We work in the ﬂexible quantile regression framework and rely on recently developed model-free measures of integrated variance, upside and downside semivariance, and jump variation. Our results for the S&P 500 and WTI Crude Oil futures contracts show that simple linear quantile regressions for returns and heterogenous quantile autoregressions for realized volatility perform very well in capturing the dynamics of the respective conditional distributions, both in absolute terms as well as relative to a couple of well-established benchmark models. The models can therefore serve as useful risk management tools for investors trading the futures contracts themselves or various derivative contract

### id `W2085213774`

**Adaptive trend estimation in financial time series via multiscale change-point-induced basis recovery**

> Statistics and Its InterfaceVolume 6 (2013) 449–461 Adaptive trend estimation in ﬁnancial time series via multiscale change-point-induced basis recovery Anna Louise Schr¨oder and Piotr Fryzlewicz∗ Low-frequency ﬁnancial returns can be modelled as centered around piecewise-constant trend functions which change at certain points in time. We propose a new stochas- tic time series framework which captures this feature. The main ingredient of our model is a hierarchically-ordered os- cillatory basis of simple piecewise-constant functions. It dif- fers from the Fourier-like bases traditionally used in time series analysis in that it is determined by change-points, and hence needs to be estimated from the data before it can be used. The resulting model enables easy simulation and provides interpretable decomposition of nonstationarity into short- and long-term components. The model permits consistentestimationofthemultiscalechange-point-induced basis via binary segmentation, which results in a variable- span moving-average estimator of the current trend, and allows for short-term forecastin

### id `W3048585901`

**Impact of COVID-19 outbreak on asymmetric multifractality of gold and oil prices**

> Resources Policy 69 (2020) 101829 Available online 12 August 2020 0301-4207/© 2020 Elsevier Ltd. All rights reserved. Impact of COVID-19 outbreak on asymmetric multifractality of gold and oil prices Walid Mensi a , b , Ahmet Sensoy c , Xuan Vinh Vo d , Sang Hoon Kang e , * a Department of Economics and Finance, College of Economics and Political Science, Sultan Qaboos University, Muscat, Oman b Institute of Business Research, University of Economics Ho Chi Minh City, Viet Nam c Bilkent University, Faculty of Business Administration, Turkey d Institute of Business REsearch and CFVG, University of Economics Ho Chi Minh City, Viet Nam e Department of Business Administration, Pusan National University, Republic of Korea ARTICLE INFO JEL classification: G14 Keywords: Gold Crude oil High frequency COVID-19 Hurst exponent A-MF-DFA ABSTRACT This paper examines the impacts of COVID-19 on the multifractality of gold and oil prices based on upward and downward trends. We apply the Asymmetric Multifractal Detrended Fluctuation Analysis (A-MF-DFA) approach to 15-min interval intraday data. The re

### id `W2610452110`

**The time-varying GARCH-in-mean model**

> General Rights Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognize and abide by the legal requirements associated with these rights. • Users may download and print one copy of any publication from the public portal for the purpose of private study or research. • You may not further distribute the material or use it for any profit-making activity or commercial gain • You may freely distribute the URL identifying the publication in the public portal If you believe that this document breaches copyright please contact us providing details, and we will remove access to the work immediately and investigate your claim. If the document is published under a Creative Commons license, this applies instead of the general rights. This coversheet template is made available by AU Library Version 2.0, December 2017 Coversheet This is the accepted manuscript (post-print version) of the article. Contentwise, the accepted manuscript version is i

### id `W3214686610`

**Effects of idiosyncratic jumps and co-jumps on oil, gold, and copper markets**

> Eﬀects of Idiosyncratic Jumps and Co-jumps on Oil, Gold, and Copper Markets November 16, 2021 Abstract Using one-minute oil, gold and copper futures price from September 27, 2009, to July 1, 2020, this paper examines the eﬀects of systematic and idiosyncratic (market-speciﬁc risk) jumps on intraday correlations, portfolio allocation decisions, and diversiﬁcation beneﬁts. We identify that these commodities contain high proportions of market-speciﬁc price discontinuities, which do not translate into systematic jumps. Co-jumps in the same direction lead to higher correlations and imply reduction in diversiﬁcation beneﬁts, while co-jumps in the opposite direction reduce correlations and positively aﬀect diversiﬁcation, similar to the idiosyncratic jumps. The results also demonstrate that the risk-averse investor’s gold portfolio allocations are not aﬀected by co-jumps and are free from the non-diversiﬁable risks in oil and copper markets. However, idiosyncratic jumps in oil and copper markets increase allocations to gold. In contrast, allocations to copper and oil are signiﬁcantly aﬀecte

### id `W3107519650`

**Collective dynamics of stock market efficiency**

> 1 Vol.:(0123456789)Scientific Reports | (2020) 10:21992 | https://doi.org/10.1038/s41598-020-78707-2 www.nature.com/scientificreports Collective dynamics of stock market efficiency Luiz G. A. Alves 1, Higor Y. D. Sigaki 2, Matjaž Perc 3,4,5* & Haroldo V. Ribeiro 2 Summarized by the efficient market hypothesis, the idea that stock prices fully reflect all available information is always confronted with the behavior of real-world markets. While there is plenty of evidence indicating and quantifying the efficiency of stock markets, most studies assume this efficiency to be constant over time so that its dynamical and collective aspects remain poorly understood. Here we define the time-varying efficiency of stock markets by calculating the permutation entropy within sliding time-windows of log-returns of stock market indices. We show that major world stock markets can be hierarchically classified into several groups that display similar long-term efficiency profiles. However, we also show that efficiency ranks and clusters of markets with similar trends are only stable for a few months a

### id `W1966704902`

**Financial earthquakes, aftershocks and scaling in emerging stock markets**

> Available online at www.sciencedirect.com Physica A 333 (2004) 306–316 www.elsevier.com/locate/physa Financial earthquakes, aftershocks and scaling in emerging stock markets Faruk Selx@8Kcuk∗ Department of Economics, Bilkent University, Bilkent, Ankara 06800, Turkey Received 14 October 2003 Abstract This paper provides evidence for scaling laws in emerging stock markets. Estimated parameters using dixY%erent dex““nitions of volatility show that the empirical scaling law in every stock market is a power law. This power law holds from 2 to 240 business days (almost 1 year). The scaling parameter in these economies changes after a change in the dex““nition of volatility. This x““nding indicates that the stock returns may have a multifractal nature. Another scaling property of stock returns is examined by relating the time after a main shock to the number of aftershocks per unit time. The empirical x““ndings show that after a major fall in the stock returns, the stock market volatility above a certain threshold shows a power law decay, described by Omori’s law. c⃝ 2003 Elsevier B.V. All 

### id `W4409237431`

**A Test of Market Efficiency: A Supervised Machine Learning Approach to Binary Options Trading**

> J Sen Net Data Comm, 2025 Volume 5 | Issue 1 | 1 A Test of Market Efficiency: A Supervised Machine Learning Approach to Binary Options Trading Research Article Joe Wayne Byers*, Ioannis Evgeniou and Anand Ravindra Manjrekar *Corresponding Author Joe Wayne Byers, WorldQuant University, New Orleans, Louisiana, United States of America. Submitted: 2025, Jan 06; Accepted: 2025, Feb 17; Published: 2025, Feb 27 Citation: Byers, J. W., Evgeniou, I., Manjrekar, A. R. (2025). A Test of Market Efficiency: A Supervised Machine Learning Approach to Binary Options Trading. J Sen Net Data Comm, 5(1), 01-23. Abstract There has been significant progress in automating binary options trading and in developing more sophisticated trading strategies. Most of these tools rely on historical data of shorter time frames; often without verifying the presence of any predictable patterns. These trading systems lack robust predictive analytics, which results in exposing the retail traders to a significant risk. This study attempts to address this loophole through a comprehensive analysis using large datasets to 

### id `W1923001224`

**Optimal switching for the pairs trading rule: A viscosity solutions approach**

> Optimal switching for pairs trading rule: a viscosity solutions approach Minh-Man NGO John von Neumann (JVN) Institute Vietnam National University Ho-Chi-Minh City, man.ngo at jvn.edu.vn Huyˆ en PHAM Laboratoire de Probabilit´ es et Mod` eles Al´ eatoires, CNRS UMR 7599 Universit´ e Paris 7 Diderot, CREST-ENSAE, and JVN Institute pham at math.univ-paris-diderot.fr December 25, 2014 Abstract This paper studies the problem of determining the optimal cut-oﬀ for pairs trading rules. We consider two correlated assets whose spread is modelled by a mean-reverting process with stochastic volatility, and the optimal pair trading rule is formulated as an optimal switching problem between three regimes: ﬂat position (no holding stocks), long one short the other and short one long the other. A ﬁxed commission cost is charged with each transaction. We use a viscosity solutions approach to prove the existence and the explicit characterization of cut-oﬀ points via the resolution of quasi-algebraic equations. We illustrate our results by numerical simulations. Keywords: pairs trading, optimal switch

### id `W4391296634`

**A hybrid econometrics and machine learning based modeling of realized volatility of natural gas**

> Open Access © The Author(s) 2024. Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the mate- rial. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http:// creat iveco mmons. org/ licen ses/ by/4. 0/. RESEARCH Kristjanpoller Financial Innovation (2024) 10:45 https://doi.org/10.1186/s40854-023-00577-0 Financial Innovation A hybrid econometrics and machine learning based modeling of realized volatility of

### id `W2981994528`

**Predicting Time-Lag Stock Return Using Tactical Asset Allocation Trading Strategies Across Global Stock Indices**

> http://ijfr.sciedupress.com International Journal of Financial Research V ol. 11, No. 1; 2020 Published by Sciedu Press 115 ISSN 1923-4023 E-ISSN 1923-4031 Predicting Time-Lag Stock Return Using Tactical Asset Allocation Trading Strategies Across Global Stock Indices Fahim Afzal1, Pan Haiying1, Farman Afzal2 & Faisal Ghafoor Bhatti3 1 Business School of Hohai University, Nanjing, China 2 School of Management and Economics, University of Electronic Science and Technology of China , Chengdu, China 3 Edith Cowan University, Western Australia Correspondence: Fahim Afzal, Business School of H ohai University, Nanjing 210098, Jiangsu, China. Tel: 152-6185-8637. Received: September 11, 2019 Accepted: October 12, 2019 Online Published: October 21, 2019 doi:10.5430/ijfr.v11n1p115 URL: https://doi.org/10.5430/ijfr.v11n1p115 Abstract This paper investigates the effectiveness of different tactical asset allocation trading strategies on global stock market indices in order to better forecast the returns. It has been revealed that timing model strategies are appeared to be the best performing one 

### id `W4220944393`

**Oil tail risk and the tail risk of the US Dollar exchange rates**

> 1 Oil tail risk and the tail risk of the US Dollar Exchange rates Afees A. Salisu1,2,3, Abeeb Olaniran4 and Jean Paul Tchankam5 Highlights  The predictive value of oil tail risk for the tail risk of US Dollar exchange rates is evaluated.  The conditional autoregressive value at risk (CAViaR) is used to estimate the tail risks under 1% and 5% VaRs.  The analysis is conducted for USD/CAD, USD/GBP and USD/JPY for both the in- sample and out-of-sample forecasts.  The relationship is positive for USD/CAD, USD/GBP while it is negative for USD/JPY albeit at 5% VaR.  Oil market risk causes instabilities in USD/CAD and USD/GBP while USD/JPY can be used to hedge against such instabilities. 1 Centre for Econometrics and Applied Research, Ibadan, Nigeria. Email: adebare1@yahoo.com 2 Department of Economics, University of Pretoria, Private Bag X20, Hatfield 0028, South Africa. 3 Corresponding Author 4 Centre for Econometrics and App lied Research, Ibadan, Nigeria. Email: olaniranabeeb464@gmail.com 5 Kedge Business School Bordeaux, 680 cours de la liberation, 33 405 Talence cedex, France. Ema

### id `W4245208017`

**Predicting future Brent oil price on global markets**

> Acta Montanistica Slovaca , Volume 25 (2020), Predicting future Brent oil price on global markets MarekVOCHOZKA 1*, JakubHORÁK Authors’ affiliations and addresses: 1 School of Expertness and Valuation, Institute of Technology and Business, Okruzni 517/10, 37001 Ceske Budejovice, Czech Republic e-mail: vochozka@mail.vstecb.cz 2 University of Žilina, Faculty of Operation and Economics of Transport and Communications Univerzitna 8215/1, 01026 Zilina , Slovakia e-mail: horak@mail.vstecb.cz 3 University of Žilina, Faculty of Operation and Economics of Transport and Communications Univerzitna 8215/1, 01026 Zilina, Slovakia e-mail: krulicky@mail.vstecb.cz 4 Polytechnic Institute of Setúbal, Business and Management School, Campus do IPS – Estefanilha, 2910-761, Setúbal, Portugal e-mail: pedro.pardal@esce.ips.pt *Correspondence: Marek Vochozka, School of Expertness and Valuation, Institute of Technology and Business, Okruzni 517/10, 37001 Ceske Budejovice, Czech Republic e-mail: vochozka@mail.vstecb.cz How to cite this article: Vochozka, M., Horák, J., Krul ický, T. and Pardal, P. (2020). Pre

### id `W1851893625`

**Trading strategies with copulas**

> Journal of Economic and Financial Sciences | JEF | April 2013 6(1), pp. 83-108 83 TRADING STRATEGIES WITH COPULAS Yolanda Stander* University of Johannesburg Yolanda.Stander@gmail.com Daniël Marais# Prevision danielmarais@mweb.co.za Ilse Botha+ University of Johannesburg ilseb@uj.ac.za February 2012 Abstract A new approach is proposed to identify trading opportunities in the equity market by using the information contained in the bivariate dependence structure of two equities. The relationships between the equity pairs are modelled with bivariate copulas and the fitted copula structures are utilised to identify the trading opportunities. Two trading strategies are considered that take advantage of the relative mispricing between a pair of correlated stocks and involve taking a position on the stocks when they diverge from their historical relationship. The position is then reversed when the two stocks revert to their historical relationship. Only stock -pairs with relatively high correlations are considere d. The dependence structures of the chosen stock -pairs very often exhibited b

### id `W1917667607`

**Optimal closing of a pair trade with a model containing jumps**

> arXiv:1004.2947v1 [q-fin.CP] 17 Apr 2010 OPTIMAL CLOSING OF A P AIR TRADE WITH A MODEL CONT AINING JUMPS STIG LARSSON 1, CARL LINDBERG, AND MARCUS W ARFHEIMER 2 Abstract. A pair trade is a portfolio consisting of a long position in on e asset and a short position in another, and it is a widely applied inv estment strategy in the ﬁnancial industry. Recently, Ekstr¨ om, Lindberg and Tysk studied the problem of optimally closing a pair trading strategy when th e diﬀerence of the two assets is modelled by an Ornstein-Uhlenbeck process. In this paper we study the same problem, but the model is generalized to also i nclude jumps. More precisely we assume that the above diﬀerence is an Ornst ein-Uhlenbeck type process, driven by a L´ evy process of ﬁnite activity. W eprove a veriﬁcation theorem and analyze a numerical method for the associated fr ee boundary problem. W e prove rigorous error estimates, which are used t o draw some conclusions from numerical simulations. 1. Introduction A portfolio which consists of a positive position in one asset, and a neg ative position in another is cal

### id `W2015887577`

**Adaptive pairs trading strategy performance in Turkish derivatives exchange with the companies listed on Istanbul stock exchange**

> Original Article Adaptive pairs trading strategy performance in Turkish derivatives exchange with the companies listed on Istanbul stock exchange Received (in revised form): 30th January 2012 Kaan Evren Bolgu¨ n has 20 years of an academic and professional experience in finance. He has project knowledge on treasury management, derivatives pricing, international finance and risk management. He had taken responsibility in the integration of risk measurement and treasury product MIS projects. He is working as a managing partner in Notus Asset Management company, Istanbul. He has published researches in the journal of Applied Financial Issues and Economics, Global Journal of Economics and Finance, Corporate Investor, Vobjektif, Isletme & Finans, Active, E-Sosder. Engin Kurun is a General Manager at Ziraat Asset Management Inc. Previously, he held various positions with Takasbank Inc. He graduated from the University of I˙stanbul, Faculty of Economics. He has an MS in capital markets and a PhD in finance, both from the University of Istanbul. He is the Lecturer of an MSc program in Intern

