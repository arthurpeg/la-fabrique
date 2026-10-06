# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 7 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-07.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W2394439017`

**Pairs trading with partial cointegration**

> Clegg, Matthew; Krauss, Christopher Working Paper Pairs trading with partial cointegration FAU Discussion Papers in Economics, No. 05/2016 Provided in Cooperation with: Friedrich-Alexander University Erlangen-Nuremberg, Institute for Economics Suggested Citation: Clegg, Matthew; Krauss, Christopher (2016) : Pairs trading with partial cointegration, FAU Discussion Papers in Economics, No. 05/2016, Friedrich-Alexander-Universität Erlangen-Nürnberg, Institute for Economics, Nürnberg This Version is available at: https://hdl.handle.net/10419/140632 Standard-Nutzungsbedingungen: Die Dokumente auf EconStor dürfen zu eigenen wissenschaftlichen Zwecken und zum Privatgebrauch gespeichert und kopiert werden. Sie dürfen die Dokumente nicht für öffentliche oder kommerzielle Zwecke vervielfältigen, öffentlich ausstellen, öffentlich zugänglich machen, vertreiben oder anderweitig nutzen. Sofern die Verfasser die Dokumente unter Open-Content-Lizenzen (insbesondere CC-Lizenzen) zur Verfügung gestellt haben sollten, gelten abweichend von diesen Nutzungsbedingungen die in der dort genannten Lizenz gewä

### id `W3083166940`

**Conditional Volatility Targeting**

> Full Terms & Conditions of access and use can be found at https://www.tandfonline.com/action/journalInformation?journalCode=ufaj20 Financial Analysts Journal ISSN: 0015-198X (Print) 1938-3312 (Online) Journal homepage: https://www.tandfonline.com/loi/ufaj20 Conditional Volatility Targeting Dion Bongaerts, Xiaowei Kang & Mathijs van Dijk To cite this article: Dion Bongaerts, Xiaowei Kang & Mathijs van Dijk (2020): Conditional Volatility Targeting, Financial Analysts Journal, DOI: 10.1080/0015198X.2020.1790853 To link to this article: https://doi.org/10.1080/0015198X.2020.1790853 © 2020 The Author(s). Published with license by Taylor & Francis Group, LLC. View supplementary material Published online: 04 Sep 2020. Submit your article to this journal Article views: 702 View related articles View Crossmark data Financial Analysts Journal | A Publication of CFA Institute Research PL Credits: 2.0 Volume 76 Number 4 © 2020 The Author(s). Published with license by Taylor & Francis, LLC. 1 https:/ /doi.org/10.1080/0015198X.2020.1790853 Conditional Volatility Targeting Dion Bongaerts , Xiaowei 

### id `W2951233714`

**OPTIMAL MEAN REVERSION TRADING WITH TRANSACTION COSTS AND STOP-LOSS EXIT**

> arXiv:1411.5062v3 [q-fin.TR] 14 May 2015 Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit ∗ Tim Leung † Xin Li ‡ May 15, 2015 Abstract Motivated by the industry practice of pairs trading, we study the o ptimal timing strategies for trading a mean-reverting price spread. An optimal double stopping problem is formulated to analyze the timing to start and subsequently liquidate the position subject t o transaction costs. Modeling the price spread by an Ornstein-Uhlenbeck process, we apply a probab ilistic methodology and rigorously derive the optimal price intervals for market entry and exit. As an e xtension, we incorporate a stop-loss constraint to limit the maximum loss. We show that the entry region is c haracterized by a bounded price interval that lies strictly above the stop-loss level. As for the exit timing, a higher stop-loss level always implies a lower optimal take-proﬁt level. Both analytical and nu merical results are provided to illustrate the dependence of timing strategies on model paramet ers such as transaction costs and stop-loss level. Keywor

### id `W3159205941`

**Pre-selection in cointegration-based pairs trading**

> Vol.:(0123456789) Statistical Methods & Applications (2023) 32:1611–1640 https://doi.org/10.1007/s10260-023-00702-4 1 3 ORIGINAL PAPER Pre‑selection in cointegration‑based pairs trading Marianna Brunetti1 · Roberta De Luca2 Accepted: 10 April 2023 / Published online: 22 May 2023 © The Author(s) 2023 Abstract The paper compares the final profitability of a cointegration-based pairs trading strategy when pairs of stocks are pre-selected by means of seven different meas- ures. Some of the measures considered have been extensively used in the pairs trad- ing literature, while others represent a novelty in this type of application. We find that pre-selection matters, since the excess returns remarkably vary, in terms of both average and variability, depending on the metrics used. Differences in profitability by pre-selection metrics are retrieved even after considering commissions and cut rules, market impact, a stricter definition of the Spread reversion to the equilibrium and alternative cointegration tests. Besides, the pairs trading profitability is found to be heterogeneous across th

### id `W4391033276`

**Improving Cointegration-Based Pairs Trading Strategy with Asymptotic Analyses and Convergence Rate Filters**

> Vol.:(0123456789) Computational Economics (2024) 64:2717–2745 https://doi.org/10.1007/s10614-023-10539-4 Improving Cointegration‑Based Pairs Trading Strategy with Asymptotic Analyses and Convergence Rate Filters Yen‑Wu Ti1 · Tian‑Shyr Dai2,3 · Kuan‑Lun Wang4 · Hao‑Han Chang2 · You‑Jia Sun2 Accepted: 14 December 2023 / Published online: 19 January 2024 © The Author(s) 2024 Abstract A pairs trading strategy (PTS) constructs a mean-reverting portfolio whose loga- rithmic value moves back and forth around a mean price level. It makes profits by longing (or shorting) the portfolio when it is underpriced (overpriced) and closing the portfolio when its value converges to the mean price level. The cointegration- based PTS literature uses the historical sample mean and variance to establish their open/close thresholds, which results in bias thresholds and less converged trades. We derive the asymptotic mean around which the portfolio value oscillates. Revised open/close thresholds determined by our asymptotic mean and standard deriva- tions significantly improve PTS performance. The derivatio

### id `W3023266558`

**Review of stochastic differential equations in statistical arbitrage pairs trading**

> 71 Managerial Economics 2019, vol. 20, No. 2, pp. 71–118 https://doi.org/10.7494/manage.2019.20.2.71 Sylvia Endres* Review of stochastic differential equations in statistical arbitrage pairs trading 1. Introduction Since the seminal studies of Thiele (1880), Bachelier (1900), Einstein (1905) and von Smoluchowski (1906), the use of stochastic differential equations in science, engineering and economics has expanded rapidly (Bodo et al. 1987, Sharp 1990). More recently, in statistical arbitrage pairs trading, interest in ad- vanced time-series modeling with stochastic differential equations has grown strongly, mainly due to increased activity on ﬁnancial markets, the steady growth of computing power, and immense amounts of data at higher frequencies. The statistical arbitrage pairs trading strategy was introduced by Gatev et al. (1999) and Gatev et al. (2006) and consists of two time periods – formation and trading. In the formation period, pairs of strongly related stocks are formed by methods of time-series analysis. In the trading period, these pairs are monitored to detect any pote

### id `W2901281638`

**Estimation of Ornstein–Uhlenbeck process using ultra-high-frequency data with application to intraday pairs trading strategy**

> Estimation of Ornstein–Uhlenbeck Process Using Ultra-High-Frequency Data with Application to Intraday Pairs Trading Strategy Vladimír Holý Prague University of Economics and Business Winston Churchill Square 4, 130 67 Prague 3, Czech Republic vladimir.holy@vse.cz Petra T omanová Prague University of Economics and Business Winston Churchill Square 4, 130 67 Prague 3, Czech Republic petra.tomanova@vse.cz Abstract:When stock prices are observed at high frequencies, more information can be utilized in estimation of parameters of the price process. However, high-frequency data are contaminated by the market microstructure noise which causes significant bias in parameter estimation when not taken into account. We propose an estimator of the Ornstein–Uhlenbeck process based on the maximum likelihood which is robust to the noise and utilizes irregularly spaced data. We also show that the Ornstein–Uhlenbeck process contaminated by the independent Gaussian white noise and observed at discrete equidistant times follows an ARMA(1,1) process. To illustrate benefits of the proposed noise-robust ap

### id `W2952304022`

**Do co-jumps impact correlations in currency markets?**

> Do co-jumps impact correlations in currency markets? Jozef Barunika,∗, Lukas Vachaa,b aInstitute of Economic Studies, Charles University in Prague, Opletalova 26, 110 00 Prague, Czech Republic bInstitute of Information Theory and Automation, The Czech Academy of Sciences, Pod Vodarenskou Vezi 4, 182 00 Prague, Czech Republic Abstract We quantify how co-jumps impact correlations in currency markets. To disentangle the continuous part of quadratic covariation from co-jumps, and study the inﬂuence of co-jumps on correlations, we propose a new wavelet-based estimator. The pro- posed estimation framework is able to localize the co-jumps very precisely through wavelet coeﬃcients and identify statistically signiﬁcant co-jumps. Empirical ﬁndings reveal the diﬀerent behaviors of co-jumps during Asian, European and U.S. trading sessions. Importantly, we document that co-jumps signiﬁcantly inﬂuence correlation in currency markets. Keywords: co-jumps, currency markets, realized covariance, wavelets, bootstrap JEL: C14, C53, G17 $We are grateful to the editor Tarun Chordia and an anonymous refere

### id `W2972608260`

**Additional Limit Conditions for Breakout Trading Strategies**

> Informatica Economică vol. 23, no. 2/2019 25 DOI: 10.12948/issn14531305/23.2.2019.03 Additional Limit Conditions for Breakout Trading Strategies Cristian PĂUNA Economic Informatics Doctoral School Bucharest Academy of Economic Studies cristian.pauna@ie.ase.ro One of the most popular trading methods used in financial markets is the Turtle strategy. Long time passed since the middle of 1983 when Richard Dennis and Bill Eckhardt disputed about whether great traders were born or made. To decide the matter, they rec ruited and trained some traders (the Turtles) and give them real accounts and a complete trading strategy to see which idea is right. That was a breakout trading strategy, meaning they bought when the price exceeded the maximum 20 or 50 days value, and sold when the price fell below the minimum of the same interval. Since then many changes have occurred in financial markets. Electronic trading was widespread released and financial trading has become accessible to everyone. Algorithmic trading became the sig nificant part of the trading decision systems and high - frequency tra

### id `W2117306570`

**Impact of jumps on returns and realised variances: econometric analysis of time-deformed Lévy processes**

> Impact of jumps on returns and realised variances: econometric analysis of time-deformed Levy processes Ole E. Barndorff-Nielsen Department of Mathematical Sciences, University of Aarhus, Ny Munkegade, DK-8000 Aarhus C, Denmark oebn@imf.au.dk Neil Shephard Nueld College, University of Oxford, Oxford OX1 1NF, U.K. neil.shephard@nuf.ox.ac.uk First circulated April 2003. This draft April 2004 Abstract In order to assess the e ect of jumps on realised variance calculations, we study some of the econometric properties of time-changed Levy processes. We show that in general realised variance is an inconsistent estimator of the time-change, however we can derive the second order properties of realised variances and use these to estimate the parameters of such models. Our analytic results give a rst indication of the degrees of inconsistency of realised variance as an estimator of the time-change in the non-Brownian case. Further, our results suggest volatility is even more predictable than has been shown by the recent econometric work on realised variance. Keywords: Kalman lter, Levy pr

### id `W2907103057`

**Time-varying risk aversion and realized gold volatility**

> Time-varying risk aversion and realized gold volatility Riza Demirera, Konstantinos Gkillasb, Rangan Guptac, Christian Pierdziochd Submission: December 2018 Resubmission: April 2019 2nd Resubmission: June 2019 Abstract We study the in- and out-of-sample predictive value of time-varying risk aversion for real- ized volatility of gold returns via extended heterogeneous autoregressive realized volatility (HAR-RV) models. Our ﬁndings suggest that time-varying risk aversion possesses predic- tive value for gold volatility both in- and out-of-sample. Time-varying risk aversion is found to absorb the in-sample predictive power of economic uncertainty at a short forecasting hori- zon. We also study the out-of-sample predictive power of time-varying risk aversion in the presence of realized higher-moments, jumps, gold returns, a leverage effect as well as eco- nomic policy uncertainty in the forecasting model. In addition, we study the role of the shape of the loss function used to evaluate losses from forecast errors for the role of time- varying risk aversion as a predictor of realized vola

### id `W2014525211`

**RESEARCH ON FUTURES TREND TRADING STRATEGY BASED ON SHORT TERM CHART PATTERN**

> Journal of Business Economics and Management ISSN 1611-1699 print / ISSN 2029-4433 online 2012 Volume 13(5): 915–930 doi:10.3846/16111699.2012.705252 Copyright © 2012 Vilnius Gediminas Technical University (VGTU) Press Technika http://www.tandfonline.com/TBEM RESEARCH ON FUTURES TREND TRADING STRATEGY BASED ON SHORT TERM CHART PATTERN Saulius Masteika1, Aleksandras Vytautas Rutkauskas2 Faculty of Business Management, Department of Finance Engineering, Vilnius Gediminas Technical University, Saulėtekio al. 11, LT-10223 Vilnius, Lithuania E-mails: 1saulius.masteika@vgtu.lt (corresponding author); 2aleksandras.rutkauskas@vgtu.lt Received 16 February 2012; accepted 19 June 2012 Abstract. The main task of this paper is to examine a short term trend trading strategy in futures market based on chart pattern recognition, time series and computational analysis. Speciﬁ cations of historical data for technical analysis and equations for futures pro ﬁ t- ability calculations together with position size measurement are also discussed in the paper. A contribution of this paper lies in a novel char

### id `W2745822063`

**Market efficiency and technical analysis during different market phases: further evidence from Malaysia**

> “Market efficiency and technical analysis during different market phases: further evidence from Malaysia” AUTHORS Safwan Mohd Nor https://orcid.org/0000-0003-0791-2363 Guneratne Wickremasinghe https://orcid.org/0000-0001-6946-0660 ARTICLE INFO Safwan Mohd Nor and Guneratne Wickremasinghe (2017). Market efficiency and technical analysis during different market phases: further evidence from Malaysia. Investment Management and Financial Innovations, 14(2-2), 359-366. doi:10.21511/imfi.14(2-2).2017.07 DOI http://dx.doi.org/10.21511/imfi.14(2-2).2017.07 RELEASED ON Monday, 21 August 2017 RECEIVED ON Monday, 12 June 2017 ACCEPTED ON Wednesday, 12 July 2017 LICENSE This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License JOURNAL "Investment Management and Financial Innovations" ISSN PRINT 1810-4967 ISSN ONLINE 1812-9358 PUBLISHER LLC “Consulting Publishing Company “Business Perspe ctives” FOUNDER LLC “Consulting Publishing Company “Business Perspe ctives” NUMBER OF REFERENCES 26 NUMBER OF FIGURES 0 NUMBER OF TABLES 3 © The author(s) 2026. This publi

### id `W2151526656`

**Are There Structural Breaks in Realized Volatility?**

> University of Toronto Department of Economics December 18, 2007 By Chun Liu and John M Maheu Are there Structural Breaks in Realized Volatility? Working Paper 304 Are there Structural Breaks in Realized Volatility? Chun Liu School of Economics and Management Tsinghua University John M. Maheu ∗ Dept. of Economics University of Toronto November 2007 Abstract Constructed from high-frequency data, realized volatility (R V) provides an eﬃ- cient estimate of the unobserved volatility of ﬁnancial markets. This paper uses a Bayesian approach to investigate the evidence for structural breaks in reduced form time-series models of R V. We focus on the popular heterogeneous autoregressive (HAR) models of the logarithm of realized volatility. Using Monte Carlo simula- tions we demonstrate that our estimation approach is eﬀective in identifying and dating structural breaks. Applied to daily S&P 500 data from 1993-2004, we ﬁnd strong evidence of a structural break in early 1997. The main eﬀect of the break is a reduction in the variance of log-volatility. The evidence of a break is robust to diﬀere

### id `W1969173997`

**DAILY CRUDE OIL PRICE FORECASTING MODEL USING ARIMA, GENERALIZED AUTOREGRESSIVE CONDITIONAL HETEROSCEDASTIC AND SUPPORT VECTOR MACHINES**

> American Journal of Applied Sciences 11 (3): 425-432, 2014 ISSN: 1546-9239 ©2014 Science Publication doi:10.3844/ajassp.2014.425.432 Published Online 11 (3) 2014 (http://www.thescipub.com/ajas.toc) Corresponding Author: Ani Bin Shabril, Department of Mathematical Sciences, Universiti, Teknologi Malaysia, Skudai, Johor, 81310, Malaysia 425 Science Publications AJAS DAILY CRUDE OIL PRICE FORECASTING MODEL USING ARIMA, GENERALIZED AUTOREGRESSIVE CONDITIONAL HETEROSCEDASTIC AND SUPPORT VECTOR MACHINES 1Rana Abdullah Ahmed and 2Ani Bin Shabri 1,2Department of Mathematical Sciences, Universiti Teknologi Malaysia, Skudai, Johor, 81310, Malaysia 1Department of Mathematics, College of Basic Education, University of Mousl, Mousl, Iraq Received 2013-11-09; Revised 2013-11-19; Accepted 2014-01-11 ABSTRACT Crude oil price forecasting is gaining increased interest globally. This interest is due mainly to the economic value attached to the product. For this reason, new forecasting methods are proposed in the literature . This paper proposes a novel technique for forecasting cr ude oil price based o

### id `W2911858053`

**Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets**

> Received January 1, 2019, accepted January 13, 2019, date of publication February 13, 2019, date of current version March 25, 2019. Digital Object Identifier 10.1 109/ACCESS.2019.2899177 Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets YI-CHENG TSAI1,2, MU-EN WU 3, JIA-HAO SYU 1,4, CHIN-LAUNG LEI 2, CHUNG-SHU WU 5, JAN-MING HO 1,6, AND CHUAN-JU WANG 6 1Institute of Information Science, Academia Sinica, Taipei 11529, Taiwan 2Department of Electrical Engineering, National Taiwan University, Taipei 10617, Taiwan 3Department of Information and Finance Management, National Taipei University of Technology, Taipei 10608, Taiwan 4Department of Computer Science and Information Engineering, National Taiwan University, Taipei 10617, Taiwan 5Chung-Hua Institution for Economic Research, Taipei 10672, Taiwan 6Research Center of Information Technology Innovation, Academia Sinica, Taipei 11529, Taiwan Corresponding author: Chuan-Ju Wang (cjwang@citi.sinica.edu.tw) ABSTRACT This paper presents a timely open range breakout (TORB) strategies for index futures market

### id `W4396746500`

**Are simple technical trading rules profitable in bitcoin markets?**

> Are simple technical trading rules proﬁtable in bitcoin markets? Niek Deprez1,, Michael Fr¨ ommel1 Ghent University, Department of Economics, Sint-Pietersplein 5, 9000 Ghent, Belgium Abstract This paper examines the proﬁtability of simple technical trading rules in bitcoin markets comprehensively, by taking into account realistic investor behavior and transaction costs, and data mining problems. Realistic investor behavior is replicated by ﬁrst employing 75,360 simple technical trading rules, divided over 6 commonly used trading rule classes and daily and intraday frequencies. Next, we select the best performing rules after transaction costs using a multiple hypothesis procedure. Finally, we form portfolios combining the selected rules and analyse their out-of-sample performance. We ﬁnd that, especially risk-return wise, simple technical trading rules can outperform a buy-and-hold strategy in the bitcoin market out-of-sample. Keywords: Bitcoin, Technical Analysis, False discovery rate, Intraday JEL: G11, G14, G17 1. Introduction In 2008 in the midst of the global ﬁnancial crisis and 

### id `W3125658236`

**The predictive capacity of GARCH-type models in measuring the volatility of crypto and world currencies**

> RESEA RCH ARTICL E The predictive capacity of GARCH-type models in measuring the volatility of crypto and world currencies Viviane Naimy 1 , Omar Haddad 1 , Gema Ferna ´ ndez-Avile ´ s ID 2 *, Rim El Khoury 1 1 Department of Accountin g and Finance, Faculty of Business Administr ation and Economics , Notre Dame University – Louaize, Zouk Mosbeh, Lebano n, 2 Faculty of Law and Social Sciences, University of Castilla-La Mancha, Toledo, Spain * Gema.fav iles@uclm.es Abstract This paper provides a thorough overview and further clarification surrounding the volatility behavior of the major six cryptocurrencie s (Bitcoin, Ripple, Litecoin, Monero, Dash and Dogecoin) with respect to world currencies (Euro, British Pound, Canadian Dollar, Austra- lian Dollar, Swiss Franc and the Japanese Yen), the relative performance of diverse GARCH-type specifications namely the SGARCH, IGARCH (1,1), EGARCH (1,1), GJR- GARCH (1,1), APARCH (1,1), TGARCH (1,1) and CGARCH (1,1), and the forecasting per- formance of the Value at Risk measure. The sampled period extends from October 13 th 2015 till November 18

### id `W2127470911`

**Intraday Anomalies and Market Efficiency: A Trading Robot Analysis**

> 1 Centre for International Capital Markets Discussion Papers ISSN 1749-3412 INTRADAY ANOMALIES AND MARKET EFFICIENCY: A TRADING ROBOT ANALYSIS Guglielmo Maria Caporale, Luis Gil-Alana, Alex Plastun, Inna Makarenko No 2014-09 2 INTRADAY ANOMALIES AND MARKET EFFICIENCY: A TRADING ROBOT ANALYSIS Guglielmo Maria Caporale* Brunel University, London, CESifo and DIW Berlin Luis Gil-Alana University of Navarra Alex Plastun Ukrainian Academy of Banking Inna Makarenko Ukrainian Academy of Banking March 2014 Abstract One of the leading c riticisms of the Efficient Market Hypothesis ( EMH) is the presence of so-called “anomalies”, i.e. empirical evidence of abnormal behaviour of asset prices which is inconsistent with market effici ency. However, most studies do not take into account transaction costs. Their existence implies that in fact traders might not be able to make abnormal profits. This paper examines whether or not anomalies such as intraday or time of the day effects give rise to exploitable profit opportunities by replicating the actions of traders. Specifically, the analysis is based

### id `W2904422942`

**Improving forecasting accuracy of crude oil prices using decomposition ensemble model with reconstruction of IMFs based on ARIMA model**

> Aamir et al. / Malaysian Journal of Fundamental and Applied Sciences Vol. 14, No. 4 (2018) 471-483 471 Improving forecasting accuracy of crude oil price using decomposition ensemble model with reconstruction of IMFs based on ARIMA model Muhammad Aamir a, c,*, Ani Shabri a, Muhammad Ishaq b a Department of Mathematical Sciences, Faculty of Science, Universiti Teknologi Malaysia, Skudai 81310, Johor, Malaysia b School of Natural Sciences, National University of Sciences and Technology, Islamabad, Pakistan c Department of Statistics, Abdul Wali Khan University Mardan, Pakistan * Corresponding author: amuhammad29@live.utm.my Article history Received 31 January 2018 Revised 22 Mac 2018 Accepted 12 June 2018 Published Online 3 December 2018 Graphical abstract Input EEMD IMF 1 IMF 2 IMF 3 IMF k… Order of ARIMA model Order of ARIMA model Order of ARIMA model Order of ARIMA model… IMFs Reconstruction IMF 1 IMF 2 IMF 3 IMF k-n… ARIMA Forecasting model ARIMA Forecasting model ARIMA Forecasting model ARIMA Forecasting model … ∑ Prediction Results Prediction Results Output Abstract The accuracy o

### id `W4398617872`

**A crisis like no other? Financial market analogies of the COVID-19-cum-Ukraine war crisis**

> North American Journal of Economics and Finance 74 (2024) 102194 Available online 23 May 2024 1062-9408/© 2024 The Author(s). Published by Elsevier Inc. This is an open access article under the CC BY-NC license (http://creativecommons.org/licenses/by-nc/4.0/). A crisis like no other? Financial market analogies of the COVID-19-cum-Ukraine war crisis Juli ´an Andrada-F ´elix a , Fernando Fern ´andez-Rodríguez a , Sim ´on Sosvilla-Rivero b , * a Department of Quantitative Methods in Economics and Management, Universidad de Las Palmas de Gran Canaria, Campus de Tafira, E-35017 Las Palmas de Gran Canaria, Spain b Instituto Complutense de An ´alisis Econ ´omico, Universidad Complutense de Madrid, Campus de Somosaguas, 28223 Pozuelo de Alarc ´on, Spain ARTICLE INFO JEL CODES: C12 E32 G14 Keywords: COVID-19 pandemic Ukraine war Financial crisis Stock markets Analogies ABSTRACT In this paper, we examine the dynamic behaviour of the US stock market due to the subsequent impact of the COVID-19 outbreak and the war in Ukraine. To that end, we analyse daily data of Dow Jones Industrial Average re

### id `W1986467742`

**Are Random Trading Strategies More Successful than Technical Ones?**

> arXiv:1303.4351v4 [q-fin.ST] 14 Jul 2013 1 Are random trading strategies more successful than technic al ones? A.E.Biondo1,∗, A.Pluchino 2, A.Rapisarda 2, D.Helbing 3 1 Dipartimento di Economia e Impresa - Universit´ a di Catani a, Corso Italia 55, 95129 Catania, Italy 2 Dipartimento di Fisica e Astronomia, Universit` a di Catan ia and INFN sezione di Catania, Via S. Soﬁa 64, 95123 Catania, Italy 3 ETH Zurich, Clausiustrasse 50, 8092 Zurich, Switzerland ∗ E-mail: ae.biondo@unict.it Abstract In this paper we explore the speciﬁc role of randomness in ﬁnancial m arkets, inspired by the beneﬁcial role of noise in many physical systems and in previous applications to c omplex socio-economic systems. After a short introduction, we study the performance of some of the most used trading strategies in predicting the dynamics of ﬁnancial markets for diﬀerent internat ional stock exchange indexes, with the goal of comparing them to the performance of a completely random strategy. In this respect, historical data for FTSE-UK, FTSE-MIB, DAX, and S&P500 indexes are taken into account for a period 

### id `W1655310703`

**Preholiday returns and volatility in the Thai stock market**

> Asian Journal of Finance & Accounting ISSN 1946-­‐052X 2010, Vol. 2, No. 2, X: E3 41 www.macrothink.org/ajfa Preholiday Returns and Volatility in Thai stock market Nopphon Tangjitprom Martin de Tours School of Management and Economics, Assumption University Bangkok, Thailand Tel: (66) 8-5815-6177 Email: tnopphon@gmail.com Received: 2010-12-07 Accepted: 2011-04-28 doi:10.5296/ajfa.v2i2.525 Abstract The purpose of this paper is to examine the holiday effect in Thailand. The holiday effect is the phenomenon in which the stock returns are abnormally high before holidays. There is no complete explanation for this phenomenon though there are many studies that state that the holiday effect has existed in the stock markets all over the world. Although there are many studies that have addressed the existence of abnormal returns during holiday periods a few studies have provided specific reasons for the existence of this phenomenon. This paper aims to study the holiday effect in returns and volatility of the Stock Exchange of Thailand. Moreover, this study examines whether the abnormal stock r

### id `W2952447090`

**Forecasting risk measures using intraday data in a generalized autoregressive score framework**

> InternationalJournalofForecasting36(2020)1057–1072 Contents lists available at ScienceDirect InternationalJournalofForecasting journal homepage: www.elsevier.com/locate/ijforecast Forecastingriskmeasuresusingintradaydatainageneralized autoregressivescoreframework ✩ EmeseLazar ∗,XiaohanXue ICMACentre,HenleyBusinessSchool,UniversityofReading,Reading,RG66BA,UK a r t i c l e i n f o Keywords: Valueatrisk Expectedshortfall Generalizedautoregressivescoredynamics Realizedmeasures Intradaydata Riskforecasting a b s t r a c t A new framework for the joint estimation and forecasting of dynamic value at risk (VaR)andexpectedshortfall(ES)isproposedbyourincorporatingintradayinformation intoageneralizedautoregressivescore(GAS)modelintroducedbyPattonetal.,2019 to estimate risk measures in a quantile regression set-up. We consider four intraday measures: the realized volatility at 5-min and 10-min sampling frequencies, and the overnightreturnincorporatedintothesetworealizedvolatilities.Inaforecastingstudy, thesetofnewlyproposedsemiparametricmodelsareappliedtofourinternationalstock marketindices(S&P5

### id `W2959922025`

**A hybrid Bayesian-network proposition for forecasting the crude oil price**

> R E S E A R C H Open Access A hybrid Bayesian-network proposition for forecasting the crude oil price Babak Fazelabdolabadi Correspondence: fazelb@ripi.ir Center for Exploration and Production Studies and Research, Research Institute of Petroleum Industry (RIPI), 14665-1998, Tehran, Iran Abstract This paper proposes a hybrid Bayesian Network (BN) method for short-term forecasting of crude oil prices. The method performed is a hybrid, based on both the aspects of classification of influencing factors as well as the regression of the out-of- sample values. For the sake of performance comparison, several other hybrid methods have also been devised using the methods of Markov Chain Monte Carlo (MCMC), Random Forest (RF), Support Vector Machine (SVM), neural networks (NNET) and generalized autoregressive conditional heteroskedasticity (GARCH). The hybrid methodology is primarily reliant upon constructing the crude oil price forecast from the summation of its Intrinsic Mode Functions (IMF) and its residue, extracted by an Empirical Mode Decomposition (EMD) of the original crude price signa

### id `W3177624315`

**Implementation of the SutteARIMA method to predict short-term cases of stock market and COVID-19 pandemic in USA**

> Implementation of the SutteARIMA method to predict short - term cases of stock market and COVID - 19 pandemic in USA by Ansari Saleh Ahmar Submission date: 07-May-2023 04:02PM (UTC-0500) Submission ID: 2086739536 File name: 2 Singh2021_Article_ImplementationOfTheSutteARIMAM.pdf (681.48K) Word count: 4745 Character count: 23084 6 8 8 1 2 1 5 1 7 2 2 2 5 2 6 3 2 3 4

### id `W2899672784`

**Timing the market: the economic value of price extremes**

> R E S E A R C H Open Access Timing the market: the economic value of price extremes Haibin Xie 1 and Shouyang Wang 2* * Correspondence: sywang@amss.ac.cn 2Academy of Mathematics and Systems Science, Chinese Academy of Sciences, Beijing 100190, China Full list of author information is available at the end of the article Abstract By decomposing asset returns into potential maximum gain (PMG) and potential maximum loss (PML) with price extremes, th is study empirically investigated the relationships between PMG and PML. We fo und significant asymmetry between PMG and PML. PML significantly contributed to forecasting PMG but not vice versa. We further explored the power of this asymmetry for predicting asset returns and found it could significantly improve asset return predict ability in both in-sample and out-of-sample forecasting. Investors who incorporate this asymmetry into their investment decisions can get substantial utility gains. This asymmetry remains significant even when controlling for macroeconomic variables, technical indic ators, market sentiment, and skewness. Moreover, 

### id `W7202283207`

**Information Arrival as a Stochastic Clock for Intraday Trading**

> Financial Economics Letters 2026 5(3) 75–88 Financial Economics Letters Homepage: https://www.anserpress.org/journal/fel Information Arrival as a Stochastic Clock for Intraday Trading Benjamin Van Vlieta,* a Stuart School of Business, Illinois Institute of Technology, Chicago, IL, USA ABSTRACT Financial markets do not evolve uniformly through calendar time. Periods of intense information arrival accelerate market activity, while information-poor periods produce the familiar intraday lull in trading. We propose a stochastic clock framework in which business time is generated by the information arrival process, providing a unified explanation for intraday trading intensity, volume, realized volatility, and execution risk. To formalize this idea, we develop a compound Hawkes model consisting of a deterministic bathtub- shaped baseline intensity, a marked linear trade-feedback component, and a squared-mark news channel that treats equal-magnitude positive and negative information symmetrically at the event level. The same signed news mark enters expected price changes linearly but enters

### id `W2980100207`

**Forecasting Crude Oil Price Using Kalman Filter Based on the Reconstruction of Modes of Decomposition Ensemble Model**

> Received September 28, 2019, accepted October 7, 2019, date of publication October 11, 2019, date of current version October 28, 2019. Digital Object Identifier 10.1 109/ACCESS.2019.2946992 Forecasting Crude Oil Price Using Kalman Filter Based on the Reconstruction of Modes of Decomposition Ensemble Model WEI GAO 1, MUHAMMAD AAMIR 2, ANI BIN SHABRI 3, RAIMI DEWAN 4, AND ADNAN ASLAM 5 1School of Information Science and Technology, Y unnan Normal University, Kunming 650500, China 2Department of Statistics, Abdul Wali Khan University Mardan, Mardan 23200, Pakistan 3Mathematical Sciences Department, Faculty of Science, Universiti Teknologi Malaysia, Johor Bahru 81310, Malaysia 4Institute of Electronics and Telecommunications of Rennes, University of Rennes 1, 35000 Rennes, France 5Department of Natural Sciences and Humanities, University of Engineering and Technology, Lahore 54000, Pakistan Corresponding author: Adnan Aslam (adnanaslam15@yahoo.com) ABSTRACT The modes’ reconstruction into the stochastic and deterministic components is proposed for forecasting the crude oil prices with the

### id `W2798018066`

**Application of continuous - time random walk to statistical arbitrage**

> Journal of Engineering Science and Technology Review 8 (1) (2015) 91 - 95 Special Issue on Econophysics Conference Article Application of continuous-time random walk to statistical arbitrage Sergey Osmekhin* and Fr´ed´eric D´el`eze Department of Finance and Statistics, Hanken School of Economics, P.O. Box 479, FI-00101, Helsinki, Finland ___________________________________________________________________________________________ Abstract An analytical statistical arbitrage strategy is proposed, where the distribution of the spread is modelled as a continuous-time random walk. Optimal boundaries, computed as a function of the mean and variance of the first-passage time of the spread, maximises an objective function. The predictability of the trading strategy is analysed and contrasted for two forms of continuous-time random walk processes. We found that the waiting-time distribution has a significant impact on the prediction of the expected profit for intraday trading Keywords: optimal trading strategy, high frequency trading, econophysics, continuous-time random walk, non-Markovian mo

