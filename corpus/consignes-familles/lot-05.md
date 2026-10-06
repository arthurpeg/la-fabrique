# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 5 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-05.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W2183809648`

**betategarch: Simulation, Estimation and Forecasting of Beta-Skew-t-EGARCH Models**

> CONTRIBUTED RESEARCH ARTICLES 137 betategarch: Simulation, Estimation and Forecasting of Beta-Skew-t-EGARCH Models by Genaro Sucarrat Abstract This paper illustrates the usage of the betategarch package, a package for the simulation, estimation and forecasting of Beta-Skew-t-EGARCH models. The Beta-Skew-t-EGARCH model is a dynamic model of the scale or volatility of ﬁnancial returns. The model is characterised by its robustness to jumps or outliers, and by its exponential speciﬁcation of volatility. The latter enables richer dynamics, since parameters need not be restricted to be positive to ensure positivity of volatility. In addition, the model also allows for heavy tails and skewness in the conditional return (i.e. scaled return), and for leverage and a time-varying long-term component in the volatility speciﬁcation. More generally, the model can be viewed as a model of the scale of the error in a dynamic regression. Introduction It is well known that ﬁnancial returns are characterised by volatility clustering: Large returns in absolute value are likely to be followed by other lar

### id `W2969876630`

**Flow toxicity of high‐frequency trading and its impact on price volatility: Evidence from the KOSPI 200 futures market**

> A peer reviewed, accepted author manuscript of the following forthcoming research article: Kang, J., Kwon, K. Y ., & Kim, W. (Accepted/In press). Flow toxicity of high frequency trading and its impact on price volatility : evidence from the KOSPI 200 futures market. Journal of Futures Markets. Flow Toxicity of High Frequency Trading and Its Impact on Price Volatility: Evidence from the KOSPI 200 Futures Market Jangkoo Kang* Kyung Yoon Kwon† Wooyeon Kim‡ Abstract We examine the relations among high frequency trading, flow toxicity, and short-term volatility during both normal and stressful times. Using transaction data from the KOSPI 200 futures market , we find that the volume-synchronized probability of informed t rading (VPIN) well measures flow toxicity in that it strongly predicts short-term volatility. We further show that high frequency trading is negatively related to VPIN and short-term volatility in normal times, but turns to be positively related in stressful times. Finally, we advocate to use bulk volume classification (BVC) by presenting evidence that the initiator identi

### id `W1572967710`

**Testing the weak-form efficiency of the WTI crude oil futures market**

> arXiv:1211.4686v1 [q-fin.ST] 20 Nov 2012 Testing the weak-form eﬃciency of the WTI crude oil futures market Zhi-Qiang Jianga,b, Wen-Jie Xiea,b,c, Wei-Xing Zhoua,b,c,d,∗ aSchool of Business, East China University of Science and Tec hnology, Shanghai 200237, China bResearch Center for Econophysics, East China University of Science and Technology, Shanghai 200237, China cDepartment of Mathematics, East China University of Scienc e and Technology, Shanghai 200237, China dKey Laboratory of Coal Gasiﬁcation and Energy Chemical Engi neering (MOE), East China University of Science and Technol ogy, Shanghai 200237, China Abstract We perform detrending moving average analysis (DMA) and det rended ﬂuctuation analysis (DFA) of the WTI crude oil future s prices (1983-2012) to investigate its eﬃciency. We further put forward a strict statistical test in the spirit of bootstrapping to verify the weak-form market eﬃciency hypothesis by employing the DMA (or DFA) exponent as t he statistic. We verify the weak-form eﬃciency of the crude oil futures market when the whole period is considered. When we b

### id `W2263719050`

**Intraday Stochastic Volatility in Discrete Price Changes: The Dynamic Skellam Model**

> Full Terms & Conditions of access and use can be found at http://www.tandfonline.com/action/journalInformation?journalCode=uasa20 Journal of the American Statistical Association ISSN: 0162-1459 (Print) 1537-274X (Online) Journal homepage: http://www.tandfonline.com/loi/uasa20 Intraday Stochastic Volatility in Discrete Price Changes: The Dynamic Skellam Model Siem Jan Koopman, Rutger Lit & André Lucas To cite this article: Siem Jan Koopman, Rutger Lit & André Lucas (2017) Intraday Stochastic Volatility in Discrete Price Changes: The Dynamic Skellam Model, Journal of the American Statistical Association, 112:520, 1490-1503, DOI: 10.1080/01621459.2017.1302878 To link to this article: https://doi.org/10.1080/01621459.2017.1302878 © 2017 The Author(s). Published with license by Taylor & Francis© Siem Jan Koopman, Rutger Lit, and André Lucas View supplementary material Accepted author version posted online: 05 Sep 2017. Published online: 05 Sep 2017. Submit your article to this journal Article views: 515 View related articles View Crossmark data JOURNALOFTHEAMERICANSTATISTICALASSOCIATION 

### id `W2614466292`

**Volatility‐Managed Portfolios**

> NBER WORKING PAPER SERIES VOLATILITY MANAGED PORTFOLIOS Alan Moreira Tyler Muir Working Paper 22208 http://www.nber.org/papers/w22208 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 April 2016 We thank Matthew Baron, Jonathan Berk, Olivier Boguth, John Campbell, John Cochrane, Kent Daniel, Peter DeMarzo, Wayne Ferson, Marcelo Fernandes, Stefano Giglio, William Goetzmann, Mark Grinblatt, Ben Hebert, Steve Heston, Jon Ingersoll, Ravi Jagannathan, Bryan Kelly, Ralph Koijen, Serhiy Kosak, Hanno Lustig, Justin Murfin, Stefan Nagel, David Ng, Lubos Pastor, Myron Scholes, Ivan Shaliastovich, Ken Singleton, Tuomo Vuoltenahoo, Jonathan Wallen, Lu Zhang, and participants at Yale SOM, UCLA Anderson, Stanford GSB, Michigan Ross, Chicago Booth, Ohio State, Baruch College, Cornell, the NYU Five Star conference, the Colorado Winter Finance Conference, the Jackson Hole Winter Finance Conference, the ASU Sonoran Conference, the UBC winter conference, the NBER, the Paul Woolley Conference, the SFS Calvacade, and Arrowstreet Capital for comments. We especially thank N

### id `W1450805766`

**The Effect of the Underlying Distribution in Hurst Exponent Estimation**

> RESEARCH ARTICLE The Effect of the Underlying Distribution in Hurst Exponent Estimation Miguel Ángel Sánchez1‡, Juan E. Trinidad2‡, José García2‡, Manuel Fernández3*‡ 1 Department of Mathematics, Universidad de Almería, Almería, Spain, 2 Department of Economics, Universidad de Almería, Almería, Spain, 3 University Centre of Defence at the Spanish Air Force Academy, MDE-UPCT, Santiago de la Ribera, Murcia, Spain ‡ These authors contributed equally to this work. * fmm124@gmail.com Abstract In this paper, a heavy-tailed distribution approach is considered in order to explore the be- havior of actual financial time series. We show that this kind of distribution allows to properly fit the empirical distribution of the stocks from S&P500 index. In addition to that, we explain in detail why the underlying distribution of the random process under study should be taken into account before using its self-similarity exponent as a reliable tool to state whether that fi- nancial series displays long-range dependence or not. Finally, we show that, under this model, no stocks from S&P500 index show

### id `W2890265597`

**Heterogeneous Information Arrivals and Return Volatility Dynamics: Uncovering the Long-Run in High Frequency Returns**

> NBER WORKING PAPER SERIES HETEROGENEOUS INFORMATION ARRIVALS AND RETURN VOLATILITY DYNAMICS : UNCOVERING THE LONG-RUN IN HIGH FREQUENCY RETURNS Torben G. Andersen Tim Bollerslev Working Paper 5752 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 September 1996 We gratefully acknowledge the financial support provided by a research grant from the Institute for Quantitative Research in Finance (the Q-Group). We would also like to thank Olsen and Associates for providing the intradaily exchange rates and Reuter’s news tape analyzed in the paper. This paper is part of NBER’s research program in Asset Pricing. Any opinions expressed are those of the authors and not those of the National Bureau of Economic Research. O 1996 by Torben G, Andersen and Tim Bollerslev. All rights reserved. Short sections of text, not to exceed two paragraphs, may be quoted without explicit permission provided that full credit, including O notice, is given to the source. NBER Working Paper 5752 September 1996 HETEROGENEOUS INFORMATION ARRIVALS AND RETURN VOLATILITY DYNAMICS : UNC

### id `W2890124632`

**Covariance forecasting in equity markets**

> Electronic copy available at: https://ssrn.com/abstract=3203283 Covariance Forecasting in Equity Markets∗ Efthymia Symitsi, Lazaros Symeonidis, Apostolos Kourtis, and Raphael Markellos Norwich Business School, University of East Anglia, UK Current version: June 25, 2018 Abstract We compare the performance of popular covariance forecasting models in the context of a portfolio of major European equity indices. We ﬁnd that models based on high-frequency data oﬀer a clear advantage in terms of statistical accuracy. They also yield more theoretically consistent predictions from an empirical asset pricing perspective, and, lead to superior out-of-sample portfolio performance. Overall, a parsimonious Vector Heterogeneous Autoregressive (VHAR) model that involves lagged daily, weekly and monthly realised covariances achieves the best performance out of the competing models. A promising new simple hybrid covariance estimator is developed that exploits option–implied information and high–frequency data while adjusting for the volatility risk-premium. Relative model performance does not change 

### id `W3124872017`

**Do high-frequency measures of volatility improve forecasts of return distributions?**

> TSpace Research Repository tspace.library.utoronto.ca Do high-frequency measures of volatility improve forecasts of return distributions? John M. Maheu, Thomas H. McCurdy Version Post-print/Accepted Manuscript Citation (published version) Maheu, J. M., & McCurdy, T. H. (2011). Do high-frequency measures of volatility improve forecasts of return distributions?. Journal of Econometrics, 160(1), 69-76. doi: 10.1016/j.jeconom.2010.03.016 Copyright/License This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/. How to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page. This article was made openly acc

### id `W2009959303`

**Dynamic spillovers between commodity and currency markets**

> Dynamic Spillovers between Commodity and Currency Markets Antonakakis, Nikolaos; Kizys, Renatas Published in: International Review of Financial Analysis DOI: 10.1016/j.irfa.2015.01.016 Published: 01/01/2015 Document Version: Peer reviewed version Document License: Other Link to publication Citation for published version (APA): Antonakakis, N., & Kizys, R. (2015). Dynamic Spillovers between Commodity and Currency Markets. International Review of Financial Analysis. https://doi.org/10.1016/j.irfa.2015.01.016 Download date: 28. Sep 2026 Dynamic Spillovers between Commodity and Currency Markets Nikolaos Antonakakisa,b,c,∗, Renatas Kizys b aVienna University of Economics and Business, Department of Economics, Institute for International Economics, Welthandelsplatz 1, 1020, Vienna, Austria. bUniversity of Portsmouth, Department of Economics and Finance, Portsmouth Business School, Portland Street, Portsmouth, PO1 3DE, United Kingdom. cJohannes Kepler University, Department of Economics, Altenberger Strasse 69, 4040 Linz-Auhof, Austria. Abstract In this study, we examine the dynamic link be

### id `W4412055715`

**Market efficiency across intra-daily sampling frequencies for Brent crude oil futures**

> Contents lists available at ScienceDirect International Review of Financial Analysis journal homepage: www.elsevier.com/locate/irfa Market efficiency across intra-daily sampling frequencies for Brent crude oil futures Erik Smith-Meyer a , Erik Haugom a ,∗, Christian Oliver Ewald a,b,c a Department of Business Administration, Inland School of Business and Social Sciences, University of Inland Norway, Lillehammer, 2604, Norway b Adam Smith Business School—Economics, University of Glasgow, Glasgow, G12 8QQ, UK c Department of Mathematics and Mathematical Statistics, Umeå University, Umeå, 90187, Sweden A R T I C L E I N F O Keywords: Intercontinental Exchange (ICE) Market efficiency Sample frequency Adjusted market inefficiency magnitude A B S T R A C T We study market efficiency for high-frequency Brent Crude oil futures prices across intra-daily sampling frequencies ranging from one minute to two hours using a sample period from 2006 to 2021. The efficiency dynamics of Brent crude oil futures prices are scrutinized over time using rolling estimation windows. We also propose to study i

### id `W2610044176`

**Forecasting the variance of stock index returns using jumps and cojumps**

> This may be the author’s version of a work that was submitted/accepted for publication in the following source: Clements, Adam & Liao, Yin (2017) Forecasting the variance of stock index returns using jumps and cojumps. International Journal of Forecasting, 33(3), pp. 729-742. This ﬁle was downloaded from: https://eprints.qut.edu.au/106774/ © Consult author(s) regarding copyright matters This work is covered by copyright. Unless the document is being made available under a Creative Commons Licence, you must assume that re-use is limited to personal use and that permission from the copyright owner must be obtained for all other uses. If the docu- ment is available under a Creative Commons License (or other speciﬁed license) then refer to the Licence for details of permitted re-use. It is a condition of access that users recog- nise and abide by the legal requirements associated with these rights. If you believe that this work infringes copyright please provide details by email to qut.copyright@qut.edu.au Notice: Please note that this document may not be the Version of Record (i.e. publ

### id `W3006513857`

**Risk aversion and the predictability of crude oil market volatility: A forecasting experiment with random forests**

> Risk aversion and the predictability of crude oil market volatility: A forecasting experiment with random forests Riza Demirera, Konstantinos Gkillasb, Rangan Guptac, Christian Pierdziochd September 2019 Abstract We analyze the predictive power of time-varying risk aversion for the real- ized volatility of crude oil returns based on high-frequency data. While the popular linear heterogeneous autoregressive realized volatility (HAR-RV) model fails to recognize the predictive power of risk aversion over crude oil volatility, we ﬁnd that risk aversion indeed improves forecast accuracy at all forecast horizons when we compute forecasts by means of random forests. The predictive power of risk aversion is robust to various covariates includ- ing realized skewness and realized kurtosis, various measures of jump inten- sity and leverage. The ﬁndings highlight the importance of accounting for nonlinearity in the data-generating process for forecast accuracy as well as the predictive power of non-cashﬂow factors over commodity-market uncer- tainty with signiﬁcant implications for the pricing a

### id `W2017412726`

**A Fourier transform method for nonparametric estimation of multivariate volatility**

> The Annals of Statistics 2009, V ol. 37, No. 4, 1983–2010 DOI: 10.1214/08-AOS633 © Institute of Mathematical Statistics, 2009 A FOURIER TRANSFORM METHOD FOR NONPARAMETRIC ESTIMA TION OF MULTIV ARIA TE VOLA TILITY BY PAUL MALLIA VIN AND MARIA ELVIRA MANCINO 1 Académie des Sciences, Institut de France and University of Firenze We provide a nonparametric method for the computation of instanta- neous multivariate volatility for continuous semi-martingales, which is based on Fourier analysis. The co-volatility is reconstructed as a stochastic function of time by establishing a connection between the Fourier transform of the prices process and the Fourier transform of the co-volatility process. A non- parametric estimator is derived given a discrete unevenly spaced and asyn- chronously sampled observations of the asset price processes. The asymptotic properties of the random estimator are studied: namely, consistency in prob- ability uniformly in time and convergence in law to a mixture of Gaussian distributions. 1. Introduction. The volatility is a key parameter in ﬁnancial economics- mat

### id `W3163475775`

**Intra-day co-movements of crude oil futures: China and the international benchmarks**

> Ji, Q., Zhang, D. and Zhao, Y. (2021) Intra-day co-movements of crude oil futures: China and the international benchmarks. Annals of Operations Research . ISSN 0254-5330. Kent Academic Repository Downloaded from https://kar.kent.ac.uk/93920/ The University of Kent's Academic Repository KAR The version of record is available from https://doi.org/10.1007/s10479-021-04097-x This document version Author's Accepted Manuscript DOI for this version Licence for this version UNSPECIFIED Additional information Versions of research works Versions of Record If this version is the version of record, it is the same as the published version available on the publisher's web site. Cite as the published version. Author Accepted Manuscripts If this document is identified as the Author Accepted Manuscript it is the version after peer review but before type setting, copy editing or publisher branding. Cite as Surname, Initial. (Year) 'Title of article'. To be published in Title of Journal , Volume and issue numbers [peer-reviewed accepted version]. Available at: DOI or URL (Accessed: date). Enquiries If 

### id `W4390952869`

**Higher-order moment connectedness between stock and commodity markets and portfolio management**

> Resources Policy 89 (2024) 104647 Available online 17 January 2024 0301-4207/© 2024 Elsevier Ltd. All rights reserved. Higher-order moment connectedness between stock and commodity markets and portfolio management Walid Mensi a , b , Hee-Un Ko c , Ahmet Sensoy d , e , Sang Hoon Kang f , g , * a Department of Economics and Finance, College of Economics and Political Science, Sultan Qaboos University, Muscat, Oman b Department of Finance and Accounting, University of Tunis El Manar and IFGT, Tunisia c Jeonbuk Institute, Jeollabuk-do, South Korea d Bilkent University, Faculty of Business Administration, Ankara, Turkey e Adnan Kassar School of Business, Lebanese American University, Beirut, Lebanon f School of Business, Pusan National University, Busan, South Korea g UniSA Business, University of South Australia, Adelaide, Australia ARTICLE INFO Keywords: High-order moments Realized volatility Jumps Realized skewness Realized kurtosis stock markets Commodity markets ABSTRACT This study examines the spillover in high-order moments for major stock markets in Europe, Japan, the UK, and the 

### id `W3123996677`

**Nonlinearity everywhere: implications for empirical finance, technical analysis and value at risk**

> Nonlinearity everywhere: implications for empirical finance, technical analysis and value at risk Article Published Version Creative Commons: Attribution 4.0 (CC-BY) Open Access Amini, S., Hudson, R., Urquhart, A. ORCID: https://orcid.org/0000-0001-8834-4243 and Wang, J. (2021) Nonlinearity everywhere: implications for empirical finance, technical analysis and value at risk. European Journal of Finance, 27 (13). pp. 1326-1349. ISSN 1466-4364 doi: 10.1080/1351847X.2021.1900888 Available at https://centaur.reading.ac.uk/95565/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1080/1351847X.2021.1900888 Publisher: Taylor and Francis All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Central Archive at the University of Reading Reading’s 

### id `W2734563065`

**Information transmission across stock indices and stock index futures: International evidence using wavelet framework**

> University of Huddersfield Repository Aloui, Chaker, Hkiri, Besma, Lau, Marco Chi Keung and Yarovaya, Larisa Information Transmission Across Stock Indices and Stock Index Futures: International Evidence Using Wavelet Framework Original Citation Aloui, Chaker, Hkiri, Besma, Lau, Marco Chi Keung and Yarovaya, Larisa (2017) Information Transmission Across Stock Indices and Stock Index Futures: International Evidence Using Wavelet Framework. Research in International Business and Finance. ISSN 0275-5319 This version is available at http://eprints.hud.ac.uk/id/eprint/33881/ The University Repository is a digital collection of the research output of the University, available on Open Access. Copyright and Moral Rights for the items on this site are retained by the individual author and/or other copyright owners. Users may access full items free of charge; copies of full text items generally can be reproduced, displayed or performed and given to third parties in any format or medium for personal research or study, educational or not-for-profit purposes without prior permission or charge, pro

### id `W4393075052`

**Sentiment and energy price volatility: A nonlinear high frequency analysis**

> Energy Economics 133 (2024) 107465 Available online 22 March 2024 0140-9883/© 2024 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY license ( http://creativecommons.org/licenses/by/4.0/). Sentiment and energy price volatility: A nonlinear high frequency analysis Fredj Jawadi a , * , David Bourghelle a , Philippe Rozin a , Abdoulkarim Idi Cheffou b , Gazi Salah Uddin c a Univ. Lille, ULR 4999 - LUMEN, F-59000 Lille, France b ISG International Business School, Paris, France c Department of Management & Engineering, Link ¨oping University, Link ¨oping, Sweden ARTICLE INFO JEL: C22 G10 G15 Q4 Keywords: Commodity volatility Investor sentiment Realized volatility Continuous volatility Jump Nonlinearity ABSTRACT This study investigates the volatility dynamics of oil and gas prices in an environment characterized by post- coronavirus disease 2019 recovery, uncertainty, high inflation, and geopolitical tensions. Unlike previous studies, we examine a long-run series of high-frequency data on gas and oil prices from July 2007 to May 2022, which provides mor

### id `W2040088269`

**Modelling and forecasting stock returns: exploiting the futures market, regime shifts and international spillovers**

> Modelling and Forecasting Stock Returns: Exploiting the Futures Market, Regime Shifts and International Spillovers¤ Lucio Sarno University of Warwick and Centre for Economic Policy Research (CEPR) Giorgio Valente University of Warwick This draft: November 2001 Abstract A large empirical literature has reported that the futures market contains valuable information for explaining stock returns and that stock returns display signi¯cant cross-correlations internationally. A parallel literature has recorded evidence that the distribution of stock returns is close to a mixture of normal distributions and that Markov switching models may therefore provide an ad- equate characterization of stock returns data. This paper ties together these strands of research in that we propose a vector equilibrium correction model of stock returns that exploits the information in the futures market, while also allowing for regime-switching behavior and international spillovers across stock market indices. Using data for three major stock market indices since 1988, we ¯nd that our model signi¯cantly outperfo

### id `W1965968531`

**Dynamic spillover effects in futures markets: UK and US evidence**

> Dynamic Spillover Effects in Futures Markets: UK and US Evidence Antonakakis, Nikolaos; Kizys, Renatas; Floros, Christos Published in: International Review of Financial Analysis DOI: 10.1016/j.irfa.2015.03.008 Published: 12/03/2016 Document Version: Peer reviewed version Document License: Other Link to publication Citation for published version (APA): Antonakakis, N., Kizys, R., & Floros, C. (2016). Dynamic Spillover Effects in Futures Markets: UK and US Evidence. International Review of Financial Analysis, 48, 406-418. https://doi.org/10.1016/j.irfa.2015.03.008 Download date: 29. Sep 2026 Dynamic Spillover Eﬀects in Futures Markets: UK and US Evidence Nikolaos Antonakakisa,b,∗, Christos Floros c,d, Renatas Kizys b aVienna University of Economics and Business, Department of Economics, Institute for International Economics, Welthandelsplatz 1, 1020, Vienna, Austria. bUniversity of Portsmouth, Economics and Finance Subject Group, Portsmouth Business School, Portland Street, Richmond Building, Portsmouth, PO1 3DE, United Kingdom cTechnological Educational Institute of Crete, Department 

### id `W1908764166`

**Intra- and inter-regional return and volatility spillovers across emerging and developed markets: Evidence from stock indices and stock index futures**

> University of Huddersfield Repository Yarovaya, Larisa, Brzeszczynski, Janusz and Lau, Marco Chi Keung Intra- and Inter-Regional Return and V olatility Spillovers Across Emerging and Developing Markets: Evidence from Stock Indices and Stock Index Futures Original Citation Yarovaya, Larisa, Brzeszczynski, Janusz and Lau, Marco Chi Keung (2016) Intra- and Inter- Regional Return and V olatility Spillovers Across Emerging and Developing Markets: Evidence from Stock Indices and Stock Index Futures. International Review of Financial Analysis, 43. pp. 96- 114. ISSN 1057-5219 This version is available at http://eprints.hud.ac.uk/id/eprint/33891/ The University Repository is a digital collection of the research output of the University, available on Open Access. Copyright and Moral Rights for the items on this site are retained by the individual author and/or other copyright owners. Users may access full items free of charge; copies of full text items generally can be reproduced, displayed or performed and given to third parties in any format or medium for personal research or study, educatio

### id `W2760722486`

**Trading volume and volatility patterns across selected Central European stock markets from microstructural perspective**

> 87 Managerial Economics 2017, vol. 18, no. 1, pp. 87–101 http://dx.doi.org/10.7494/manage.2017.18.1.87 Henryk Gurgul*, Robert Syrek** Trading volume and volatility patterns across selected Central European stock markets from microstructural perspective 1. Introduction Market microstructure can be deﬁned as speciﬁc local rules in a given market and/or anomalies reﬂecting patterns in price, trading volume, or volatility and more data from a stock market that is relevant with respect to trading activity. Nowadays, there has been a revival of this notion in the context of electronic trading and the numerical capacities of fast comput ers supporting trading. One of the most-important topics in empirical stock market studies in the framework of microstructure is recognizing patterns of volati lity and trading volume sea- sonality. This is an important issue with respect t o risk management, arbitrage, and speculation. Based on the patterns in the past, market participants can try to maximize their returns and minimize risk. In addition, knowledge of market microstructure can help the marke

### id `W2189860660`

**Forecasting volatility in oil prices with a class of nonlinear volatility models: smooth transition RBF and MLP neural networks augmented GARCH approach**

> ORIGINAL PAPER Forecasting volatility in oil prices with a class of nonlinear volatility models: smooth transition RBF and MLP neural networks augmented GARCH approach Melike Bildirici 1 • O¨ zgu¨ r Ersin 2 Received: 24 January 2014 / Published online: 23 July 2015 /C211 The Author(s) 2015. This article is published with open access at Springerlink.com Abstract In this study, the forecasting capabilities of a new class of nonlinear econometric models, namely, the LSTAR-LST-GARCH-RBF and MLP models are evalu- ated. The models are utilized to model and to forecast the daily returns of crude oil prices. Many ﬁnancial time series are subjected to leptokurtic distribution, heavy tails, and nonlinear conditional volatility. This characteristic feature leads to deterioration in the forecast capabilities of tradi- tional models such as the ARCH and GARCH models. According to the empirical ﬁndings, the oil prices and their daily returns could be classiﬁed as possessing nonlinearity in the conditional mean and conditional variance processes. Several model groups are evaluated: (i) the models p

### id `W3124256151`

**Leverage effect in energy futures**

> Leverage eﬀect in energy futures Ladislav Kristoufeka,b aInstitute of Information Theory and Automation, Academy of Sciences of the Czech Republic, Pod Vodarenskou Vezi 4, 182 08, Prague, Czech Republic, EU bInstitute of Economic Studies, Faculty of Social Sciences, Charles University in Prague, Opletalova 26, 110 00, Prague, Czech Republic, EU Abstract We propose a comprehensive treatment of the leverage eﬀect, i.e. the relationship between returns and volatility of a speciﬁc asset, focusing on energy commodities futures, namely Brent and WTI crude oils, natural gas and heating oil. After estimating the volatility process without assuming any speciﬁc form of its behavior, we ﬁnd the volatility to be long- term dependent with the Hurst exponent on a verge of stationarity and non-stationarity. Bypassing this using by using the detrended cross-correlation and the detrending moving- average cross-correlation coeﬃcients, we ﬁnd the standard leverage eﬀect for both crude oil. For heating oil, the eﬀect is not statistically signiﬁcant, and for natural gas, we ﬁnd the inverse leverage eﬀect

### id `W1545012815`

**Long memory and volatility clustering: Is the empirical evidence consistent across stock markets?**

> arXiv:0709.2178v3 [q-fin.ST] 14 Mar 2008 Long Memory and Volatility Clustering: is the empirical evidence consistent across stock markets? Snia R. Bentes*, Rui Menezes**, Diana A. Mendes** *Iscal, Av. Miguel Bombarda, 20, 1069-035 Lisboa Portugal, so niabentes@clix.pt; **ISCTE, Av. Forcas Armadas, 1649-025 Lisboa, Portugal Abstract Long memory and volatility clustering are two stylized fact s frequently related to ﬁnancial markets. Traditionally, these phenomena have bee n studied based on con- ditionally heteroscedastic models like ARCH, GARCH, IGARC H and FIGARCH, inter alia. One advantage of these models is their ability to capture nonlinear dy- namics. Another interesting manner to study the volatility phenomena is by using measures based on the concept of entropy. In this paper we inv estigate the long memory and volatility clustering for the SP 500, NASDAQ 100 a nd Stoxx 50 in- dexes in order to compare the US and European Markets. Additi onally, we compare the results from conditionally heteroscedastic models wit h those from the entropy measures. In the latter, we examine Sha

### id `W4296126235`

**A GMM approach to estimate the roughness of stochastic volatility**

> A GMM approach to estimate the roughness of stochastic volatility∗ Anine E. Bolko † Kim Christensen† Mikko S. Pakkanen‡,† Bezirgen Veliyev† September 7, 2022 Abstract We develop a GMM approach for estimation of log-normal stochastic volatility models driven by a fractional Brownian motion with unrestricted Hurst exponent. We show that a parameter estimator based on the integrated variance is consistent and, under stronger conditions, asymptotically normally distributed. We inspect the behavior of our procedure when integrated variance is replaced with a noisy measure of volatility calculated from discrete high-frequency data. The realized estimator contains sampling error, which skews the fractal coefficient toward “illusive roughness.” We construct an analytical approach to control the impact of measurement error without introducing nuisance parameters. In a simulation study, we demonstrate convincing small sample properties of our approach based both on integrated and realized variance over the entire memory spectrum. We show the bias correction attenuates any systematic deviance i

### id `W2886725919`

**Co-Existence of Trend and Value in Financial Markets: Estimating an Extended Chiarella Model**

> Co-existence of Trend and Value in Financial Markets: Estimating an Extended Chiarella Model Adam A. Majewski, Stefano Ciliberti and Jean-Philippe Bouchaud ∗ Capital Fund Management 23 rue de l’Université Paris 75007, France August 1, 2018 Abstract Trend and Value are pervasive anomalies, common to all ﬁnancial markets. We address the problem of their co-existence and interaction within the frame- work of Heterogeneous Agent Based Models (HABM). More speciﬁcally, we extend the Chiarella (1992) model by adding noise traders and a non-linear demand of fundamentalists. We use Bayesian ﬁltering techniques to calibrate the model on time series of prices across a variety of asset classes since 1800. The fundamental value is an output of the calibration, and does not require the use of an external pricing model. Our extended model reproduces many em- pirical observations, including the non-monotonic relation between past trends and future returns. The destabilizing activity of trend-followers leads to a qual- itative change of mispricing distribution, from unimodal to bimodal, meaning that 

### id `W2946970269`

**The performance of technical trading rules in Socially Responsible Investments**

> The performance of technical trading rules in Socially Responsible Investments Article Accepted Version Creative Commons: Attribution-Noncommercial-No Derivative Works 4.0 Urquhart, A. ORCID: https://orcid.org/0000-0001-8834-4243 and Zhang, H. (2019) The performance of technical trading rules in Socially Responsible Investments. International Review of Economics and Finance, 63. pp. 397-411. ISSN 1059-0560 doi: 10.1016/j.iref.2019.05.002 Available at https://centaur.reading.ac.uk/83820/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1016/j.iref.2019.05.002 Publisher: Elsevier All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Central Archive at the University of Reading Reading’s research outputs online

### id `W4401965983`

**Designing Efficient Pair-Trading Strategies for the Technology Stock Market**

> Designing Efficient Pair-Trading Strategies for the Technology Stock Market Yangxuan Liu1,a, Mingyuan Gao 2,b,∗, Yiyang Guo3,c, Yichen Qiao4,d 1Marshall School of Business, University of Southern California, Los Angeles, California, 90089, USA 2Fu Foundation School of Engineering and Applied Science, Columbia University, New York, New York, 10019, USA 3Warwick Business School, University of Warwick, Coventry, 200093, UK 4Zhiyuan College, Shanghai Jiao Tong University, Shanghai, 200240, China a. liuyangx@usc.edu, b. mg4504@columbia.edu c. yiyang.Guo@Warwick.ac.uk, d. yichen1@sjtu.edu.cn *corresponding author Abstract: Pairs trading is a quantitative trading approach that exploits instances of financial markets exhibiting disequilibrium. Through the identification of a pair of stocks with a his- torical pattern of correlated movement, and under the assumption that their price differentials will return to a central tendency, an investor can seek to gain from this mean-reversion by establishing a long position in the designated pair. Throughout the years, numerous trading frameworks and 

