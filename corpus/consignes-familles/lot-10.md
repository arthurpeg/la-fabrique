# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 10 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-10.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W4392564092`

**Gold price prediction by a CNN-Bi-LSTM model along with automatic parameter tuning**

> RESEA RCH ARTICL E Gold price prediction by a CNN-Bi-LSTM model along with automatic parameter tuning Amirhossein Amini 1 , Robab Kalantari ID 2 * 1 Faculty of Industria l Engineeri ng, Department of Financial System, Khatam University , Tehran, Iran, 2 Faculty of Finance, Departme nt of Financial Engineeri ng, Khatam University , Tehran, Iran * r.kalanta ri@khatam. ac.ir Abstract Banking and stock markets consider gold to be an important componen t of their economic and financial status. There are various factors that influence the gold price trend and its fluc- tuations. Accurate and reliable prediction of the gold price is an essential part of financial and portfolio management . Moreover, it could provide insights about potential buy and sell points in order to prevent financial damages and reduce the risk of investment. In this paper, different architectures of deep neural network (DNN) have been proposed based on long short-term memory (LSTM) and convolutional-ba sed neural networks (CNN) as a hybrid model, along with automatic parameter tuning to increase the accuracy, coeffic

### id `W2312414574`

**Unraveling the cause-effect relation between time series**

> PHYSICAL REVIEW E 90, 052150 (2014) Unraveling the cause-effect relation between time series X. San Liang* School of Marine Sciences, Nanjing University of Information Science and Technology (Nanjing Institute of Meteorology), Nanjing 210044 and China Institute for Advanced Study, Central University of Finance and Economics, Beijing 100081, China (Received 8 June 2014; revised manuscript received 14 October 2014; published 24 November 2014) Given two time series, can one faithfully tell, in a rigorous and quantitative way, the cause and effect between them? Based on a recently rigorized physical notion, namely, information ﬂow, we solve an inverse problem and give this important and challenging question, which is of interest in a wide variety of disciplines, a positive answer. Here causality is measured by the time rate of information ﬂowing from one series to the other. The resulting formula is tight in form, involving only commonly used statistics, namely, sample covariances; an immediate corollary is that causation implies correlation, but correlation does not imply causation. It 

### id `W2552863143`

**An Overview of FIGARCH and Related Time Series Models**

> AUSTRIAN JOURNAL OF STATISTICS V olume 41 (2012), Number 3, 175–196 An Overview of FIGARCH and Related Time Series Models Maryam Tayeﬁ and T. V . Ramanathan Department of Statistics and Centre for Advanced Studies University of Pune, India Abstract: This paper reviews the theory and applications related to fraction- ally integrated generalized autoregressive conditional heteroscedastic (FIGA- RCH) models, mainly for describing the observed persistence in the volatility of a time series. The long memory nature of FIGARCH models allows to be a better candidate than other conditional heteroscedastic models for modeling volatility in exchange rates, option prices, stock market returns and inﬂation rates. We discuss some of the important properties of FIGARCH models in this review. We also compare the FIGARCH with the autoregressive frac- tionally integrated moving average (ARFIMA) model. Problems related to parameter estimation and forecasting using a FIGARCH model are presented. The application of a FIGARCH model to exchange rate data is discussed. We brieﬂy introduce some other models,

### id `W3152597534`

**UNIT ROOT TEST WITH HIGH-FREQUENCY DATA**

> Econometric Theory, 38, 2022, 113–171. doi:10.1017/S0266466621000098 UNIT ROOT TEST WITH HIGH-FREQUENCY DATA SÉBASTIEN LAURENT Aix-Marseille University (Aix-Marseille School of Economics) CNRS & EHESS Aix-Marseille Graduate School of Management–IAE, France SHUPING SHI Macquarie University Deviations of asset prices from the random walk dynamic imply the predictability of asset returns and thus have important implications for portfolio construction and risk management. This paper proposes a real-time monitoring device for such deviations using intraday high-frequency data. The proposed procedures are based on unit root tests with in-fill asymptotics but extended to take the empirical features of high-frequency financial data (particularly jumps) into consideration. We derive the limiting distributions of the tests under both the null hypothesis of a random walk with jumps and the alternative of mean reversion/explosiveness with jumps. The limiting results show that ignoring the presence of jumps could potentially lead to severe size distortions of both the standard left-sided (against

### id `W2948872054`

**Exploring price gap anomaly in the Ukrainian stock market**

> “Exploring price gap anomaly in the Ukrainian stock market” AUTHORS Alex Plastun https://orcid.org/0000-0001-8208-7135 https://publons.com/researcher/1449372/alex-plastun/ Inna Makarenko https://orcid.org/0000-0001-7326-5374 http://www.researcherid.com/rid/AAE-8453-2020 Lyudmila Khomutenko http://orcid.org/0000-0002-9443-4330 http://www.researcherid.com/rid/P-6162-2014 Svitlana Shcherbak http://orcid.org/0000-0002-3969-2062 Olha Tryfonova http://orcid.org/0000-0002-7980-636X ARTICLE INFO Alex Plastun, Inna Makarenko, Lyudmila Khomutenko, Svitlana Shcherbak and Olha Tryfonova (2019). Exploring price gap anomaly in the Ukrainian stock market. Investment Management and Financial Innovations, 16(2), 150-158. doi:10.21511/imfi.16(2).2019.13 DOI http://dx.doi.org/10.21511/imfi.16(2).2019.13 RELEASED ON Wednesday, 05 June 2019 RECEIVED ON Monday, 20 May 2019 ACCEPTED ON Thursday, 30 May 2019 LICENSE This work is licensed under a Creative Commons Attribution 4.0 International License JOURNAL "Investment Management and Financial Innovations" ISSN PRINT 1810-4967 ISSN ONLINE 1812-9358 PUBLISHE

### id `W3011772139`

**Real-time prediction of Bitcoin bubble crashes**

> 1 Real-time Prediction of Bitcoin Bubble Crashes Min Shu1, 2, *, Wei Zhu1, 2 1 Department of Applied Mathematics & Statistics, Stony Brook University, Stony Brook, NY, USA 2 Center of Excellence in Wireless & Information Technology, Stony Brook University, Stony Brook, NY, USA Abstract In the past decade, Bitcoin as an emerging asset class has gained widespread public attention because of their extraordinary returns in phases of extreme price growth and their unpredictable massive crashes. We apply the log-periodic power law singularity (LPPLS) confidence indicator as a diagnostic tool for identifying bubbles using the daily data on Bitcoin price in the past two years. We find that the LPPLS confidence indicator based on the daily Bitcoin price data fails to provide effective warnings for detecting the bubbles when the Bitcoin price suffers from a large fluctuation in a short time, es pecially for positive bubbles. In order to diagnose the existence of bubbles and accurately predict the bubble crashes in the cryptocurrency market, this study proposes an adaptive multilevel time serie

### id `W2951066907`

**Limit theorems for moving averages of discretized processes plus noise**

> arXiv:1010.0335v1 [math.ST] 2 Oct 2010 The Annals of Statistics 2010, Vol. 38, No. 3, 1478–1545 DOI: 10.1214/09-AOS756 c⃝ Institute of Mathematical Statistics , 2010 LIMIT THEOREMS FOR MOVING A VERAGES OF DISCRETIZED PROCESSES PLUS NOISE By Jean Jacod, Mark Podolskij and Mathias Vetter 1 UPMC (Universit´ e Paris-6), ETH Z¨ urich and Ruhr-Universit¨ at Bochum This paper presents some limit theorems for certain functio n- als of moving averages of semimartingales plus noise which a re ob- served at high frequency. Our method generalizes the pre-av eraging approach (see [Bernoulli 15 (2009) 634–658, Stochastic Process. Appl. 119 (2009) 2249–2276]) and provides consistent estimates for v arious characteristics of general semimartingales. Furthermore , we prove the associated multidimensional (stable) central limit theor ems. As ex- pected, we ﬁnd central limit theorems with a convergence rat e n−1/4, if n is the number of observations. 1. Introduction. The last years have witnessed a considerable develop- ment of the statistics of processes observed at very high fre quency due to the rec

### id `W2530258413`

**Price gaps: Another market anomaly?**

> Full Terms & Conditions of access and use can be found at https://www.tandfonline.com/action/journalInformation?journalCode=riaj20 Investment Analysts Journal ISSN: 1029-3523 (Print) 2077-0227 (Online) Journal homepage: www.tandfonline.com/journals/riaj20 Price gaps: Another market anomaly? Guglielmo Maria Caporale & Alex Plastun To cite this article: Guglielmo Maria Caporale & Alex Plastun (2017) Price gaps: Another market anomaly?, Investment Analysts Journal, 46:4, 279-293, DOI: 10.1080/10293523.2017.1333563 To link to this article: https://doi.org/10.1080/10293523.2017.1333563 © 2017 The Author(s). Published by Informa UK Limited, trading as Taylor & Francis Group Published online: 02 Jul 2017. Submit your article to this journal Article views: 5738 View related articles View Crossmark data Citing articles: 3 View citing articles Price gaps: Another market anomaly? Guglielmo Maria Caporale a and Alex Plastun b aBrunel University London, CESifo and DIW Berlin; bSumy State University, Sumy, Ukraine ABSTRACT This paper analyses price gaps in financial markets, also known as trading,

### id `W3111589756`

**Can Oil Prices Predict Japanese Yen?**

> Peer-reviewed research Can Oil Prices Predict Japanese Yen? Can Oil Prices Predict Japanese Yen? Neluka Devpura 1 a 1 Department of Statistics, Faculty of Applied Sciences, University of Sri Jayewardenepura, Sri Lanka Keywords: exchange rate, predictability, time-varying, japanese yen, oil price 10.46557/001c.17964 Asian Economics Letters In this paper, we examine the relationship between Japanese Yen (vis-à-vis the US dollar) and the crude oil futures price. The novelty is that we use high frequency (intraday hourly) data to examine time-varying predictability. We find limited evidence that oil prices predict the Yen. There is no time-varying predictability relationship. I. Introduction I. Introduction The literature has shown the relevance of exchange rates for asset prices, particularly during the COVID-19 period. P. K. Narayan et al. (2020), for instance, show that the Yen ex- change rate predic ts Japanese stock returns. P. K. Narayan (2020a) show that the Y en has bec ome more resilient to shocks during the C OVID-19 period. P. K. Narayan (2020b) shows that bubble ac tivity in 

### id `W2401355877`

**Learning zero-cost portfolio selection with pattern matching**

> RESEA RCH ARTICL E Learning zero-cost portfolio selection with pattern matching Fayyaaz Loonat 1 , Tim Gebbie 1,2 * 1 School of Computer Science and Applied Mathematics , University of the Witwatersra nd, Johanne sburg, WITS 2050, South Africa, 2 Department of Statistical Sciences, Univers ity of Cape Town, Cape Town, Rondebosc h 7701, South Africa * tim.gebbie @uct.ac.za Abstract We replicate and extend the adversarial expert based learning approach of Gyo ¨ rfi et al to the situation of zero-cost portfolio selection implemented with a quadratic approximation derived from the mutual fund separation theorems. The algorithm is applied to daily sampled sequential Open-High-Lo w-Close data and sequential intraday 5-minute bar-data from the Johannesburg Stock Exchange (JSE). Statistical tests of the algorithms are considered. The algorithms are directly compared to standard NYSE test cases from prior literature. The learning algorithm is used to select parameters for experts generated by pattern matching past dynamics using a simple nearest-neighbour search algorithm. It is shown that th

### id `W4405765089`

**The market impact of leveraged ETFs: A Survey of the literature**

> https://www.aimspress.com/journal/QFE QFE, 8(4): 815–840. DOI: 10.3934/QFE.2024031 Received: 24 September 2024 Revised: 06 December 2024 Accepted: 17 December 2024 Published: 23 December 2024 Review The market impact of leveraged ETFs: A Survey of the literature Stephen L. Lenkey* Smeal College of Business, Pennsylvania State University, University Park, PA, 16802, USA * Correspondence: Email: slenkey@psu.edu; Tel: 814-867-5795. Abstract: I survey the literature related to the potential for leveraged and inverse ETFs to influence late-day asset prices. The literature consistently reports statistically significant associations between ETF rebalancing demand and late-day returns and volatility. However, most of the available papers suffer from potentially serious methodological errors, and the economic associations appear to be insignificant. Moreover, the broader literature suggests that the market provides enough liquidity to satisfy LETF rebalancing demand with an insignificant degradation of market quality. Despite the potential for LETF rebalancing to affect late-day market condit

### id `W2556409592`

**Looking for Psychological Barriers in nine European Stock Market Indices**

> *Correspondence to: jlobao@fep.up.pt, pereiracristiano@outlook.com Dutch Journal of Finance and Management, 1:1 (2016), 39 ISSN: 2468-211X Looking for Psychological Barriers in nine European Stock Market Indices Júlio Lobão*, Cristiano Pereira*, Universidade do Porto, PORTUGAL ABSTRACT 1. INTRODUCTION In this paper we examine nine European stock market indices for indication of psychological barriers at round numbers. We test for uniformity in the trailing digits of the indices and use regression and GARCH analysis to assess the differential impact of being above or below a possible barrier. Despite having rejected uniformity for all data series, we only found significant psycholo gical barriers in the stock markets of Germany, Finland and the Netherlands . Moreover, we document that the relationship between risk and return tends to be weaker at the proximity of round numbers which poses a challenge to the traditional equilibrium models. Keywords ------------------------------ psychological barriers, M-values, stock market indices, market psychology, round numbers -------------------

### id `W2010431117`

**Economic significance of market timing rules in the Forward Freight Agreement markets**

> Copyright and Reuse: Copyright and Moral Rights remain with the author(s) and/or copyright holders. Copies of full items can be used for personal research or study, educational, or not-for-profit purposes without prior permission or charge, unless otherwise indicated, provided that the authors, title and full bibliographic details are credited, a hyperlink and/or URL is given for the original metadata page and the content is not changed in any way. For full details of reuse please refer to City Research Online policy. City Research Online: http://openaccess.city.ac.uk/ publications@citystgeorges.ac.uk Citation: Nomikos, N. & Doctor, K. (2013). Economic significance of market timing rules in the Forward Freight Agreement markets. Transportation Research Part E: Logistics and Transportation Review, 52, pp. 77-93. doi: 10.1016/j.tre.2012.11.009 This is the accepted version of the paper. This version of the publication may differ from the final published version. To cite this item please consult the publisher's version. Permanent repository link: https://openaccess.city.ac.uk/id/eprint/7

### id `W4244083731`

**Realized Skewness**

> Copyright and Reuse: Copyright and Moral Rights remain with the author(s) and/or copyright holders. Copies of full items can be used for personal research or study, educational, or not-for-profit purposes without prior permission or charge, unless otherwise indicated, provided that the authors, title and full bibliographic details are credited, a hyperlink and/or URL is given for the original metadata page and the content is not changed in any way. For full details of reuse please refer to City Research Online policy. City Research Online: http://openaccess.city.ac.uk/ publications@citystgeorges.ac.uk Citation: Neuberger, A. (2012). Realized Skewness. The Review of Financial Studies, 25(11), pp. 3423-3455. doi: 10.1093/rfs/hhs101 This is the accepted version of the paper. This version of the publication may differ from the final published version. To cite this item please consult the publisher's version. Permanent repository link: https://openaccess.city.ac.uk/id/eprint/15210/ Link to published version: https://doi.org/10.1093/rfs/hhs101 City Research Online City St George’s, Univers

### id `W2121891463`

**Asymptotic Theory of Range-Based Multipower Variation**

> Asymptotic theory of range-based multipower variation Kim Christensen* Mark Podolskij† This version: October, 2011 Abstract In this paper, we present a realized range-based multipower variation theory, which can be used to es- timate return variation and draw jump-robust inference abo ut the diffusive volatility component, when a high-frequency record of asset prices is available. The sta ndard range-statistic – routinely used in ﬁnancial economics to estimate the variance of securities prices – is shown to be biased when the price process con- tains jumps. We outline how the new theory can be applied to re move this bias by constructing a hybrid range-based estimator. Our asymptotic theory also reveals that when high-frequency data are sparsely sam- pled, as is often done in practice due to the presence of micro structure noise, the range-based multipower variations can produce signiﬁcant efﬁciency gains over com parable subsampled return-based estimators. The analysis is supported by a simulation study and we illust rate the practical use of our framework on some recent TAQ equity 

### id `W2071611747`

**Analysis of high-resolution foreign exchange data of USD-JPY for 13 years**

> arXiv:cond-mat/0211162v1 [cond-mat.stat-mech] 8 Nov 2002 Analysis of high-resolution foreign exchange data of USD-JPY for 13 years Takayuki Mizunoa 1, Shoko Kurihara a, Misako Takayasub, Hideki Takayasuc aDepartment of Physics, Faculty of Science and Engineering, Chuo University, Kasuga, Bunkyo-ku, Tokyo 112-8551, Japan bDepartment of Complex Systems, Future University-Hakodate , 116-2 Kameda-Nakano-cho, Hakodate, Hokkaido 041-8655, Japan cSony Computer Science Laboratories Inc., 3-14-13 Higashigot anda, Shinagawa-ku, Tokyo 141-0022, Japan Abstract We analyze high-resolution foreign exchange data consisti ng of 20 million data points of USD-JPY for 13 years to report ﬁrm statistical laws in distributions and correlations of exchange rate ﬂuctuations. A conditional p robability density analysis clearly shows the existence of trend-following movements a t time scale of 8-ticks, about 1 minute. Key words: Econophysics, Foreign exchange, Fat-tail, Correlation PACS: 02.50.Fz; 05.90.+m 1 Introduction In the case of transactions of stocks, the places and times for tr ading are limited, but 

### id `W2143495973`

**Do Leveraged ETFs Increase Volatility**

> Technology and Investment, 2010, 1, 215-220 doi:10.4236/ti.2010.13026 Published Online August 2010 (http://www.SciRP.org/journal/ti) C o p y r i g h t © 2 0 1 0 S c i R e s . TI Do Leveraged ETFs Increase Volatility William J. Trainor Jr. East Tennessee State University, Johnson City, USA E-mail: trainor@etsu.edu Received May 5, 2010; revised June 30, 2010; accepted July 3, 2010 Abstract The 2008 financial crisis has produced volatility levels not seen since the 1987 stock market crash more than 20 years ago. During that time, the culprit was thought to be index futures and program trading. This time, leveraged ETFs and their rebalancing trades have been singled out by some to explain both the spike in vola- tility and the appearance of large price swings at the end of the trading day. This study examines the merit of these accusations and whether the incr ease in volatility and end of the day price momentum is indeed linked to leveraged ETFs and their rebalanci ng trades. For the S&P 500, the rela tionship appears to be a spurious coincidence. Keywords: Leveraged ETFs, Volatility, M

### id `W2613481507`

**The Halloween effect on the agricultural commodities markets**

> 441 Agric. Econ. – Czech, 63, 2017 (10): 441–448 Original Paper doi: 10.17221/45/2016-AGRICECON The global financial markets are in a permanent development. Although the technologies and financial instruments evolve and change over time, some as- pects of financial markets remain almost unchanged. To these aspects, there belong also various calendar anomalies. The calendar anomalies are the cyclical anomalies in returns that tend to repeating according to various calendar patterns. Although the strength of the anomalies is variable, they can be tracked back to the 18 th century. Some of the best known anomalies are the January effect, the day of the week effect, the month of the year effect, the turn of the week/month/ year effects and the Halloween effect. Not all of the anomalies are present on all of the markets. Most attention has been paid to the calendar anomalies on share markets (Lakonishok and Smidt 1988; Haggard et al. 2015), but some of the authors investigated also the presence of calendar anomalies on the commodity markets (Milonas 1991; Borowski 2015). The existence of 

### id `W2924331493`

**Time Series Forecasting Based on Complex Network Analysis**

> Received March 2, 2019, accepted March 16, 2019, date of publication March 19, 2019, date of current version April 9, 2019. Digital Object Identifier 10.1 109/ACCESS.2019.2906268 Time Series Forecasting Based on Complex Network Analysis SHENGZHONG MAO 1 AND FUYUAN XIAO 2 1School of Hanhong, Southwest University, Chongqing 400715, China 2School of Computer and Information Science, Southwest University, Chongqing 400715, China Corresponding author: Fuyuan Xiao (doctorxiaofy@hotmail.com) This work was supported by the Chongqing Overseas Scholars Innovation Program under Grant cx2018077. ABSTRACT Time series forecasting, especially from the perspective of the network, has been a hot research topic. In this paper, based on the analysis of complex network, a novel method is proposed for more accurate time series predictions. First, time series data are mapped into a network by visibility graph. Then, the link prediction method is adopted to calculate the similarity index. Considering that node distance is an important factor in the network, we take that into account to determine the weight

### id `W3123576289`

**How does trading volume affect financial return distributions?**

> How does trading volume affect financial return distributions? Hung Doa, Robert Brooksa, Sirimon Treepongkarunab, Eliza Wuc1 aDepartment of Econometrics and Business Statistics, Monash University, Australia bAccounting and Finance, UWA Business School, The University of Western Australia, Australia cFinance Discipline Group, UTS Business School, University of Technology Sydney, Australia ABSTRACT We assess investors' reaction to new information arrivals in financial markets by examining the relationships between trading volume and the higher moments of returns in 18 international equity and currency markets. Our volume-volatility results support extant information theories and further contribute new evidence of cross market relations between volume and volatility. We also find that the direct impact of volume on the level of negative skewness is less significant for more diversified regional portfolios. Furthermore, the negative interaction between volume and kurtosis can be explained by the differences of opinion in financial markets. We observe stronger interdependence among higher

### id `W2963998209`

**Clarifications to questions and criticisms on the Johansen–Ledoit–Sornette financial bubble model**

> arXiv:1107.3171v3 [q-fin.GN] 10 Jun 2013 Clariﬁcations to Questions and Criticisms on the Johansen-Ledoit-Sornette Financial Bubble Model Didier Sornette, 1, 2, ∗ Ryan Woodard, 1, † Wanfeng Yan,1, ‡ and Wei-Xing Zhou 3, § 1Department of Management, Technology and Economics, ETH Zurich, Kreuzplatz 5, CH-8032 Zurich, Switzerland 2Swiss Finance Institute, c/o University of Geneva, 40 blvd. Du Pont d’Arve, CH-1211 Geneva 4, Switzerland 3School of Business, East China University of Science and Tech nology, Shanghai 200237, China The Johansen-Ledoit-Sornette (JLS) model of rational expe ctation bubbles with ﬁnite-time singular crash hazard rates has been developed t o describe the dynamics of ﬁnancial bubbles and crashes. It has been applied success fully to a large variety of ﬁnancial bubbles in many diﬀerent markets. Having been dev eloped over a decade ago, the JLS model has been studied, analyzed, used and criti cized by several re- searchers. Much of this discussion is helpful for advancing the research. However, several serious misconceptions seem to be present within th is literatur

### id `W3096561984`

**Did Bubble Activity Intensify During COVID-19?**

> Peer-reviewed research Did Bubble Activity Intensify During COVID-19? Did Bubble Activity Intensify During COVID-19? Paresh Kumar Narayan 1 a 1 Deakin Business School, Deakin university, Australia Keywords: covid-19, exchange rates, bubbles https://doi.org/10.46557/001c.17654 Asian Economics Letters Vol. 1, Issue 2, 2020 In this note, we utilize hourly exchange rate data for Japanese Yen, Canadian dollar, European Euro and the British pound to search for possible bubble type behavior. We identify evidence that bubble activity characterizes all four exchange rates more so in the COVID-19 period. We also show that bubble activity intensified during the COVID-19 period, implying markets became relatively more inefficient compared to the pre-COVID-19 period. I. Introduction I. Introduction Searching for bubble ac tivity or bubble t ype behavior in asset prices has occupied historical interest, beginning with the Dutch tulipmania in 1634-1637 (Garber, 1989). Bubbles have been documented in rec ent work; such as, inter alia, Phillips et al. (2011) , Phillips et al. (2015) , Bettendorf & Ch

### id `W3123639445`

**Betting against beta**

> NBER WORKING PAPER SERIES BETTING AGAINST BETA Andrea Frazzini Lasse H. Pedersen Working Paper 16601 http://www.nber.org/papers/w16601 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 December 2010 We thank Cliff Asness, Aaron Brown, John Campbell, Kent Daniel, Gene Fama, Nicolae Garleanu, John Heaton (discussant), Michael Katz, Owen Lamont, Michael Mendelson, Matt Richardson, Tuomo Vuolteenaho and Robert Whitelaw for helpful comments and discussions as well as seminar participants at Columbia University, New York University, Yale University, Emory University, University of Chicago Booth, Kellogg School of Management, Harvard University, NBER Behavioral Economics 2010, and the 2010 Annual Management Conference at University of Chicago Booth School of Business. The authors are affiliated with AQR Capital Management, a global asset management firm that may apply some of the principles discussed in this research in some of its investment products. The views expressed herein are those of the authors and do not necessarily reflect the views of the Nationa

### id `W774369827`

**Eurusd Intraday Price Reversal**

> EURUSD INTRADAY PRICE REVERSAL Marta Wiśniewska, Ph.D. Gdansk School of Banking Dolna Brama 8, 80-821 Gdańsk, Poland e-mail: marta@witor.biz Received 23 September 2014, Accepted 24 October 2014 Abstract The study investigates the mean reversion in 1-minute EURUSD. Intraday patters in FX seem of particular interest as more and more trades in the FX market are automated high frequency trades (HFT). The study reveals that the mean reversion is present in the intraday EURUSD. ADF test rejects unit root. The average of the deviation of EURUSD from its (moving) mean is close to zero. Furthermore when short and long positions are simultaneously open, the average maximum return achieved through 24 hour period is similar, providing yet another evidence for mean reversion and lack of weak form of market efficiency. Keywords: high frequency, intraday, price, EURUSD, reversal, mean, market efficiency. JEL classification: G11, G14. Folia Oeconomica Stetinensia DOI: 10.1515/foli-2015-0014 EURUSD Intraday Price Reversal 153 Introduction Foreign exchange (FX) market is the most liquid market in the 

### id `W4410338087`

**Democratising Technical Analysis**

> INTERNATIONAL JOURNAL OF FINANCE & BANKING STUDIES 14 (2) (2025) 138-146 © 2025 by the authors. Hosting by SSBFNET. Peer review under responsibility of Center for Strategic Studies in Business and Finance. * Corresponding author. https://doi.org/10.20525/ijfbs.v14i2.4219 Democratising Technical Analysis: How Large Language Models Support Retail Breakout Strategies Under Random Walk Constraints Dmitrii Gimmelberg (a,b*), Marta Głowacka (b), Alexey Belinskiy (b,c), Valentin Artamov (b), Max Gimmelberg (b) (a) RISEBA University of Applied Sciences, Faculty of Business and Economics Latvia. (b) Aestima SIA, Research and Development, Latvia. (c) SBS Swiss Business School, Doctorate Studies, Switzerland. A R T I C L E I N F O Article history: Received 12 April 2025 Received in rev. form 11 May 2025 Accepted 11 May 2025 Keywords: Technical analysis, LLM, Large Language Models, Retail Investors, Momentum JEL Classification: G11, G14, C45 A B S T R A C T This study examines whether Large Language Models (LLMs) can support momentum-based breakout strategies for retail investors by analysing te

### id `W4289522162`

**Momentum: what do we know 30 years after Jegadeesh and Titman’s seminal paper?**

> Financial Markets and Portfolio Management (2023) 37:95–114 https://doi.org/10.1007/s11408-022-00417-8 Momentum: what do we know 30 years after Jegadeesh and Titman’s seminal paper? Tobias Wiest 1 Accepted: 20 June 2022 / Published online: 2 August 2022 © The Author(s) 2022 Abstract For over 30 years, extensive research has found corroborating evidence that past win- ners continue to yield higher returns than past losers. This momentum effect is robust across various asset classes and across the globe and presents perhaps the most perva- sive contradiction of the efﬁcient market hypothesis. This article reviews three strands of literature on momentum. First, I outline the construction of momentum strategies, emphasizing improvements and alternatives such as time-series momentum, residual momentum, and risk-managed momentum. Second, I summarize the most prominent behavioral-based and risk-based explanations for the origin of momentum. Finally, I present in detail the ﬁndings on commonality in stock momentum, namely on industry and factor momentum. Keywords Momentum · Asset pricing · F

### id `W2775498257`

**Does the January Effect Still Exists?**

> http://ijfr.sciedupress.com International Journal of Financial Research V ol. 9, No. 1; 2018 Published by Sciedu Press 50 ISSN 1923-4023 E-ISSN 1923-4031 Does the January Effect Still Exists? Gerardo “Gerry” Alfonso Perez1 1 University of Cambridge, UK Correspondence: Gerardo “Gerry” Alfonso Perez, University of Cambridge, UK. Received: August 24, 2017 Accepted: October 2, 2017 Online Published: December 3, 2017 doi:10.5430/ijfr.v9n1p50 URL: https://doi.org/10.5430/ijfr.v9n1p50 Abstract The issue of the January Effect has attracted a lot of interest by both practitioners and researchers. The idea that stock returns in January are statistically bigger than in other months was first presented several decades ago. This study analyzes the issue of the January effect in a systematic and global way of studying the performance of 106 indexes in 86 countries and jurisdictions. It was observed that while this effect can still be appreciated in some markets it would appear that it is decreasing globally over time. It was also found that there appears to be an Inverted January Effect in several

### id `W3131621821`

**Global factor premiums**

> EUR Research Information Portal Global factor premiums Published in: Journal of Financial Economics Publication status and date: Published: 01/07/2021 DOI (link to publisher): 10.1016/j.jfineco.2021.06.030 Document Version Version created as part of publication process; publisher's layout; not normally made publicly available Document License/Available under: CC BY Citation for the published version (APA): Baltussen, G., Swinkels, L., & Van Vliet, P. (2021). Global factor premiums. Journal of Financial Economics, 142(3), 1128- 1154. https://doi.org/10.1016/j.jfineco.2021.06.030 Link to publication on the EUR Research Information Portal Terms and Conditions of Use Except as permitted by the applicable copyright law, you may not reproduce or make this material available to any third party without the prior written permission from the copyright holder(s). Copyright law allows the following uses of this material without prior permission: • you may download, save and print a copy of this material for your personal use only; • you may share the EUR portal link to this material. In case the

### id `W3121782217`

**Safe Haven Currencies**

> Zurich Open Repository and Archive University of Zurich University Library Strickhofstrasse 39 CH-8057 Zurich www.zora.uzh.ch Year: 2010 Safe Haven Currencies Ranaldo, Angelo ; Söderlind, Paul Abstract: We study high-frequency exchange rates over the period 1993–2008. Based on the recent literature on volatility and liquidity risk premia, we use a factor model to capture linear and non-linear linkages between currencies, stock and bond markets as well as proxies for market volatility and liquidity. We document that the Swiss franc and Japanese yen appreciate against the US dollar when US stock prices decrease and US bond prices and FX volatility increase. These safe haven properties materialise over different time granularities (from a few hours to several days) and non-linearly with the volatility factor and during crises. The latter effects were particularly discernible for the yen during the recent financial crisis. Copyright 2010, Oxford University Press. DOI: https://doi.org/10.1093/rof/rfq007 Posted at the Zurich Open Repository and Archive, University of Zurich ZORA URL: https

### id `W2528063373`

**The Drift Burst Hypothesis**

> The drift burst hypothesis Kim Christensen Roel Oomen Roberto Renò * November 2020 Abstract The drift burst hypothesis postulates the existence of short-lived locally explosive trends in the price paths of ﬁ- nancial assets. The recent U.S. equity and treasury ﬂash crashes can be viewed as two high-proﬁle manifestations of such dynamics, but we argue that drift bursts of varying ma gnitude are an expected and regular occurrence in ﬁnancial markets that can arise through established mechan isms of liquidity provision. We show how to build drift bursts into the continuous-time Itô semimartingale m odel, discuss the conditions required for the process to remain arbitrage-free, and propose a nonparametric test statistic that identiﬁes drift bursts from noisy high- frequency data. We apply the test and demonstrate that driftbursts are a stylized fact of the price dynamics across equities, ﬁxed income, currencies and commodities. Drift b ursts occur once a week on average, and the majority of them are accompanied by subsequent price reversion and can thus be regarded as “ﬂash crashes.” The

