# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 4 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-04.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W2148517125`

**The Intraday Pattern of Trading Activity, Return Volatility and Liquidity: Evidence from the Emerging Tunisian Stock Exchange**

> www.ccsenet.org/ijef International Journal of Economics and Finance V ol. 4, No. 5; May 2012 ISSN 1916-971X E-ISSN 1916-9728 156 The Intraday Pattern of Trading Activity, Return Volatility and Liquidity: Evidence from the Emerging Tunisian Stock Exchange Kais Tissaoui Faculty of Law Sciences, Economic Sciences and Management of Jendouba, BP 8153 Elmelga Jendouba, Tunisia The International Finance Group, Tunisia, Manar University Tel: 216-25-700-645 E-mail: kaistissaoui@yahoo.fr Received: Febriary 10, 2012 Accepted: March 14, 2012 Published: May 1, 2012 doi:10.5539/ijef.v4n5p156 URL: http://dx.doi.org/10.5539/ijef.v4n5p156 Abstract The purpose of this paper is to investigate the intraday pattern of trading activity, liquidity and return volatility in the emerging Tunisian Stock Market (TSE) which is an order-driven market using intraday data covering the period October 2008 to June 2009. To achieve this objective, we have applied two methods: the temporal analysis that consists to estimate a dichotomy model for each variable by following the methodological approach of Vo (2007) and th

### id `W4404980787`

**Improving realised volatility forecast for emerging markets**

> Journal of Economics and Finance https://doi.org/10.1007/s12197-024-09701-x Improving realised volatility forecast for emerging markets Mesias Alfeus 1,2 · Justin Harvey 1 · Phuthehang Maphatsoe 1 Accepted: 13 November 2024 © The Author(s) 2024 Abstract Accurate forecasting of realised volatility is essential for ﬁnancial risk management and investment decision-making in emerging markets, taking the South African ﬁnan- cial market as a benchmark. This study examines the predictive performance of four prominent models: HAR (Heterogeneous AutoRegressive), realised GARCH (Generalized AutoRegressive Conditional Heteroscedasticity), Recurrent Conditional Heteroskedasticity (RECH), and the Rough Fractional Stochastic V olatility (RFSV) models. These models are speciﬁcally tailored to capture the complex dynamics and long-range dependence observed in ﬁnancial time series. We illustrate the challenges and limitations of these models outside the context of established markets. Our empir- ical ﬁndings reveal unique strengths for each model. The HAR model excels in capturing long-term volatilit

### id `W3166986981`

**Forecasting oil and gold volatilities with sentiment indicators under structural breaks**

> Forecasting Oil and Gold Volatilities with Sentiment Indicators Under Structural Breaks Jiawen Luo*, Riza Demirer **, Rangan Gupta***, Qiang Ji **** Abstract: This paper contributes to the literature on forecasting the realized volatility of oil and gold by (i) utilizing the Infinite Hidden Markov (IHM) switching model within the Heterogeneous Autoregressive (HAR) framework to accommodate structural breaks in the data and (ii) incorporating, for the first time in the literature, various sentiment indicators that proxy for the speculative and hedging tendencies of investors in these markets as predictors in the forecasting models. We show that accounting for structural breaks and incorporating sentiment- related indicators in the forecasting model does not only improve the out-of-sample forecasting performance of volatility models but also has significant economic implications, offering improved risk-adjusted returns for investors, particularly for short-term and mid-term forecasts. We also find evidence of significant cross-market information spilling over across the oil, gold, and s

### id `W4293250349`

**Analysis of market efficiency and fractal feature of NASDAQ stock exchange: Time series modeling and forecasting of stock index using ARMA-GARCH model**

> Arashi and Rounaghi Future Business Journal https://doi.org/10.1186/s43093-022-00125-9 RESEARCH Analysis of market efficiency and fractal feature of NASDAQ stock exchange: Time series modeling and forecasting of stock index using ARMA-GARCH model Mohammad Arashi1 and Mohammad Mahdi Rounaghi2* Abstract The multi-fractal analysis has been applied to investigate various stylized facts of the financial market including mar- ket efficiency, financial crisis, risk evaluation and crash prediction. This paper examines the daily return series of stock index of NASDAQ stock exchange. Also, in this study, we test the efficient market hypothesis and fractal feature of NASDAQ stock exchange. In the previous studies, most of the technical analysis methods for stock market, including K-line chart, moving average, etc. have been used. These methods are generally based on statistical data, while the stock market is in fact a nonlinear and chaotic system which depends on political, economic and psychological fac- tors. In this research we modeled daily stock index in NASDAQ stock exchange using ARMA-G

### id `W1970034577`

**Does the day of the week effect exist once transaction costs have been accounted for? Evidence from the UK**

> 1 ------------------------------------------------------------------------ Does The Day Of The Week Effect Exist Once Transaction Costs Have Been Accounted For? Evidence From The UK ------------------------------------------------------------------------ THIS ARTICLE HAS BEEN PUBLISHED IN: APPLIED FINANCIAL ECONOMICS, 2004, Vol. 14, pp. 215–220 A. GREGORIOU, A. KONTONIKAS and N. TSITSIANIS DEPARTMENT OF ECONOMICS AND FINANCE, BRUNEL UNIVERSITY, UXBRIDGE, MIDDLESEX, UB8 3PH, UK ======================================================================================= This article investigates the day of the week anomaly in the FTSE 100 Share Index over an 11-year time period from 1 January 1986 to 31 December 1997. Its focus is to assess whether the day of the week effect continues to persist once transactions costs are considered. Unlike previous literature it uses the bid–ask spread as a proxy for transactions costs. It finds that once returns become robust to transactions costs the anomaly appears to fade away. It then extends the research by looking at the time-varying volatility of 

### id `W2061691990`

**Weak-Form Market Efficiency: Evidence from the Brazilian Stock Market**

> www.ccsenet.org/ijef International Journal of Ec onomics and Finance V ol. 4, No. 7; July 2012 ISSN 1916-971X E-ISSN 1916-9728 22 Weak-Form Market Efficiency: Evidence from the Brazilian Stock Market Chien-Ping Chen1 & Massoud Metghalchi1 1 School of Business Administration, University of Houston-Victoria, Victoria, Texas, USA Correspondence: Chien-Ping Chen, 14000 University Blvd, Sugar Land, TX 77479, USA. Tel: 1-281-275-8811. E-mail: chenc@uhv.edu Received: April 25, 2012 Accepted: May 14, 2012 Published: July 1, 2012 doi:10.5539/ijef.v4n7p22 URL: http://dx.doi.org/10.5539/ijef.v4n7p22 Abstract We investigate the predictive power of various trading rules with different combinations of the most popular indicators in technical analysis for the Brazilian stock index (BOVESPA) over the period of 5/1/1996 to 3/1/2011, or 14.83 years. The empirical results show that all the buy- sell differences under single, double and triple-indicator combinations are insignificant in t-test; that is, techni cal trading models cannot beat the buy and hold strategy. Although few multiple-indicator trad

### id `W2280474718`

**Time-dependent scaling patterns in high frequency financial data**

> Time-dependent scaling patterns in high frequency ﬁnancial data Noemi Navaa,1, T. Di Matteo b, Tomaso Astea,1 aDepartment of Computer Science, University College London, Gower Street, London, WC1E 6BT, UK bDepartment of Mathematics, King’s College London, The Strand, London, WC2R 2LS, UK Abstract We measure the inﬂuence of diﬀerent time-scales on the dynamics of ﬁnancial market data. This is obtained by decomposing ﬁnancial time series into simple oscillations associated with distinct time-scales. We propose two new time-varying measures: 1) an amplitude scaling exponent and 2) an entropy- like measure. We apply these measures to intraday, 30-second sampled prices of various stock indices. Our results reveal intraday trends where diﬀerent time-horizons contribute with variable relative amplitudes over the course of the trading day. Our ﬁndings indicate that the time series we analysed have a non-stationary multifractal nature with predominantly persistent behaviour at the middle of the trading session and anti-persistent behaviour at the open and close. We demonstrate that these devi

### id `W4390817011`

**REALIZED VOLATILITY PREDICTION OF THE US COMMODITY FUTURES DURING THE GLOBAL FINANCIAL CRISIS (GFC) AND COVID-19 PANDEMIC**

> 2023 Vol.27 No.2 POLISH JOURNAL OF MANAGEMENT STUDIES Oláh J., Noor T., Uddin S. 260 REALIZED VOLATILITY PREDICTION OF THE US COMMODITY FUTURES DURING THE GLOBAL FINANCIAL CRISIS (GFC) AND COVID-19 PANDEMIC Oláh J., Noor T., Uddin S. Abstract: This research aims to inspect the predictability of the realized volatility (RV) of the US Commodity futures market during the economic crisis period for the last 20 years. The economic crisis period includes the Global Financial Crisis (GFC) and the fina ncial crisis during COVID-19. This study extends its aim to show the forecasting comparison during the financial crisis period and the normal economic period. A standard predictive regression model from the weekly RV data is used to test the certainty of next week’s RV of the commodity futures. This study uses data from Q1 of 2000 to Q3 of 2020. It finds that platinum, palladium, gold, and crude oil have significant predictability for the RV forecast during the global financial crisis, whereas sugar, silver, and platinum have high and significant predictability to forecast the RV during the p

### id `W2078985570`

**Selecting volatility forecasting models for portfolio allocation purposes**

> This may be the author’s version of a work that was submitted/accepted for publication in the following source: Becker, Ralf, Clements, Adam, Doolan, Mark, & Hurn, Aubrey (2015) Selecting volatility forecasting models for portfolio allocation purposes. International Journal of Forecasting, 31(3), pp. 849-861. This ﬁle was downloaded from: https://eprints.qut.edu.au/70599/ © Consult author(s) regarding copyright matters This work is covered by copyright. Unless the document is being made available under a Creative Commons Licence, you must assume that re-use is limited to personal use and that permission from the copyright owner must be obtained for all other uses. If the docu- ment is available under a Creative Commons License (or other speciﬁed license) then refer to the Licence for details of permitted re-use. It is a condition of access that users recog- nise and abide by the legal requirements associated with these rights. If you believe that this work infringes copyright please provide details by email to qut.copyright@qut.edu.au Notice: Please note that this document may not be

### id `W1901577096`

**Information Flow, Trading Activity and Commodity Futures Volatility**

> This may be the author’s version of a work that was submitted/accepted for publication in the following source: Clements, Adam & Todorova, Neda (2016) Information ﬂow, trading activity and commodity futures volatility. Journal of Futures Markets, 36(1), pp. 88-104. This ﬁle was downloaded from: https://eprints.qut.edu.au/92612/ © Consult author(s) regarding copyright matters This work is covered by copyright. Unless the document is being made available under a Creative Commons Licence, you must assume that re-use is limited to personal use and that permission from the copyright owner must be obtained for all other uses. If the docu- ment is available under a Creative Commons License (or other speciﬁed license) then refer to the Licence for details of permitted re-use. It is a condition of access that users recog- nise and abide by the legal requirements associated with these rights. If you believe that this work infringes copyright please provide details by email to qut.copyright@qut.edu.au Notice: Please note that this document may not be the Version of Record (i.e. published versio

### id `W2820935738`

**Two are better than one: Volatility forecasting using multiplicative component GARCH‐MIDAS models**

> Received: 14 March 2018 Revised: 14 August 2019 DOI: 10.1002/jae.2742 RESEARCH ARTICLE Two are better than one: Volatility forecasting using multiplicative component GARCH-MIDAS models Christian Conrad Onno Kleen Department of Economics, Heidelberg University, Heidelberg, Germany Correspondence Onno Kleen, Department of Economics, Heidelberg University, Bergheimer Strasse 58, 69115 Heidelberg, Germany. Email: onno.kleen@awi.uni-heidelberg.de Summary We examine the properties and forecast performance of multiplicative volatility specifications that belong to the class of generalized autoregressive conditional heteroskedasticity–mixed-data sampling (GARCH-MIDAS) models suggested in Engle, Ghysels, and Sohn (Review of Economics and Statistics, 2013, 95, 776–797). In those models volatility is decomposed into a short-term GARCH component and a long-term component that is driven by an explanatory variable. We derive the kurtosis of returns, the autocorrelation function of squared returns, and the R2 of a Mincer–Zarnowitz regression and evaluate the QMLE and forecast performance of these m

### id `W2919714849`

**Forecasting (downside and upside) realized exchange-rate volatility: Is there a role for realized skewness and kurtosis?**

> Forecasting (downside and upside) realized exchange-rate volatility: Is there a role for realized skewness and kurtosis? Konstantinos Gkillasa, Rangan Guptab, Christian Pierdziochc Submission: March 2019 Resubmission: May 2019 Abstract We use intraday data to construct measures of realized volatility, realized kurtosis, and realized skewness of returns of six major exchange rates vis-à- vis the dollar. The currencies under consideration are: (i) Australian dollar, (ii) Canadian dollar, (iii) Swiss franc, (iv) euro, (v) British pound, and (vi) Japanese yen. The period of the analysis spans from 1 July 2003 to 28 August 2015. We study in-sample and out-of-sample the predictive value of realized kurtosis and realized skewness for realized volatility, where we also differentiate between measures of upside realized volatility and downside realized volatility. We ﬁnd that both realized kurtosis and realized skewness have in-sample predictive value in several models being studied. The out-of- sample results show that it is mainly realized kurtosis that helps to improve accuracy of one-day-a

### id `W3164875660`

**Cryptocurrencies, gold, and WTI crude oil market efficiency: a dynamic analysis based on the adaptive market hypothesis**

> Cryptocurrencies, gold, and WTI crude oil market efficiency: a dynamic analysis based on the adaptive market hypothesis Majid Mirzaee Ghazani* and Mohammad Ali Jafari Introduction The substantial growth of cryptocurrencies has attracted considerable attention from investors and policymakers in recent years. As of June 5, 2019, this growth topped 2216 cryptocurrencies in market capitalization and volume of trade, and the top three coins, Bitcoin, Ethereum, and Ripple, together accounted for more than 70 percent of the mar - ket share (Cryptocurrency Market Capitalizations 2019). One of the critical issues yet to be analyzed is whether the dynamic behavior of crypto- currencies is predictable, which would be inconsistent with the efficient market hypoth - esis (EMH), according to which prices should follow a random walk (see Fama 1970). Long-memory techniques can be applied for this purpose. In the meantime, numerous studies have provided evidence of the persistent behavior of asset prices (see Caporale et al. 2016)1 and have also found that this behavior varies over time, but few stud

### id `W2038828613`

**Profitability of Technical Analysis in the Singapore Stock Market: before and after the Asian Financial Crisis**

> Journal of Economic Integration 24(1), March 2009; 135-150 Profitability of Technical Analysis in the Singapore Stock Market: before and after the Asian Financial Crisis James J. Kung Ming Chuan University Wing-Keung Wong Hong Kong Baptist University Abstract In the aftermath of the Asian financia l crisis, a series of reform and liberalization measures have been im plemented in Singapore to upgrade its financial markets. This study investigates whether these measures have led to less profitability for those investors who employ technical rules for trading stocks. Our results show that the three trading rules consistently generate higher annual returns for 1988-1996 than those for 1999-2007. Further, they generally perform better than the buy-and-hold (BH) strategy for 1988-1996 but perform no better than the BH strategy for 1999-2007. These findings suggest that the efficiency of the Singapore stock market has been considerably enhanced by the measures implemented after the crisis. • JEL Classification : G14, D92 • Key Words: Asian financial crisis, profitability, technical analysis

### id `W2802313218`

**Application of Hurst Exponent (H) and the R/S Analysis in the Classification of FOREX Securities**

>  Abstract—This paper presents the relationship between the Hurst Exponent (H) and the Rescaled Range Analysis (R/S) in the classification of Foreign Exchange Market (FOREX) time series by the supposition of the existence of a Fractal Market in an alternative to the traditional theory of Capital Markets. In such a way, the Hurst Exponent is a metric capable of providing information on correlation and persistence in a time series. Many systems can be described by self-similar fractals as Fractional Brownian Motion, which are well characterized by this statistic. Index Terms—Hurst exponent, R/S analysis, fractal analysis, financial time series, fractional. I. INTRODUCTION The necessity to anticipate and identify changes in events points to a new direction in line with the analysis of the fluctuations of prices of financial assets. This new direction leads us to argue about new alternatives in Finance Theory and Capital Markets. In the spirit of this contention the theory of fractals arises by innovating the argumentation [1]. Empirical studies, especially in Hydrology and Climatology, 

### id `W4200418554`

**Time series reversal in trend‐following strategies**

> Time series reversal in trend‐following strategies Liu, J., & Papailias, F. (2023). Time series reversal in trend‐following strategies. European Financial Management, 29(1), 76-108. https://doi.org/10.1111/eufm.12349 Published in: European Financial Management Document Version: Peer reviewed version Queen's University Belfast - Research Portal: Link to publication record in Queen's University Belfast Research Portal Publisher rights © 2021 John Wiley & Son. This work is made available online in accordance with the publisher’s policies. Please refer to any applicable terms of use of the publisher. General rights Copyright for the publications made accessible via the Queen's University Belfast Research Portal is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that users recognise and abide by the legal requirements associated with these rights. Take down policy The Research Portal is Queen's institutional repository that provides access to Queen's research output. Every effort has been made to ensure that content in the Re

### id `W2887718163`

**Modeling the Interactions between Volatility and Returns using EGARCH‐M**

> EUR Research Information Portal Modeling the Interactions between Volatility and Returns using EGARCH?M Published in: Journal of Time Series Analysis Publication status and date: Published: 29/06/2018 DOI (link to publisher): 10.1111/jtsa.12419 Document Version Publisher's PDF, also known as Version of record Document License/Available under: Article 25fa Dutch Copyright Act Citation for the published version (APA): Lange, R.-J., & Harvey, AC. (2018). Modeling the Interactions between Volatility and Returns using EGARCH?M. Journal of Time Series Analysis, 39, 909-919. https://doi.org/10.1111/jtsa.12419 Link to publication on the EUR Research Information Portal Terms and Conditions of Use Except as permitted by the applicable copyright law, you may not reproduce or make this material available to any third party without the prior written permission from the copyright holder(s). Copyright law allows the following uses of this material without prior permission: • you may download, save and print a copy of this material for your personal use only; • you may share the EUR portal link to t

### id `W3123297069`

**The skewness of commodity futures returns**

> Accepted Manuscript The Skewness of Commodity Futures Returns Adrian Fernandez-Perez , Bart Frijns , Ana-Maria Fuertes , Joelle Miffre PII: S0378-4266(17)30150-4 DOI: 10.1016/j.jbankﬁn.2017.06.015 Reference: JBF 5167 To appear in: Journal of Banking and Finance Received date: 10 November 2016 Revised date: 21 June 2017 Accepted date: 30 June 2017 Please cite this article as: Adrian Fernandez-Perez , Bart Frijns , Ana-Maria Fuertes , Joelle Miffre , The Skewness of Commodity Futures Returns, Journal of Banking and Finance (2017), doi: 10.1016/j.jbankﬁn.2017.06.015 This is a PDF ﬁle of an unedited manuscript that has been accepted for publication. As a service to our customers we are providing this early version of the manuscript. The manuscript will undergo copyediting, typesetting, and review of the resulting proof before it is published in its ﬁnal form. Please note that during the production process errors may be discovered which could affect the content, and all legal disclaimers that apply to the journal pertain. ACCEPTED MANUSCRIPT ACCEPTED MANUSCRIPT 1 The Skewness of Commodity

### id `W2979316084`

**Weekly momentum in the commodity futures market**

> Weekly Momentum in the Commodity Futures Market Kyung Yoon Kwon‡, Jangkoo Kang†, and Jaesun Yun⁎ Abstract This paper investigates commodity futures momentum s with various ranking periods in a weekly basis. Unlike in equity markets, strong short -term momentum, instead of short -term reversal, is observed in commodity futures markets. The weekly momentum remains highly significant even after controlling for vario us factors, such as carry, equity momentum, or hedging pressure. Our results suggest that the anomalous returns from the traditional 12-month momentum strategy in the commodity futures markets mainly stem from the strong predictability of the past week’s r eturn. Lastly, we suggest that the weekly momentum is closely related to the speculative activity in the commodity futures market. JEL classification: G10 Keywords: Commodity Futures; Momentum; Weekly Momentum; Speculators; Hedgers ‡ Department of Accounting and Finance, Strathclyde Business School, University of Strathclyde ; 199 Cathedral street, Glasgow, G4 0QU, Scotland, UK; tel: +44-141-548-3935; e-mail: arari1115@gma

### id `W2795048783`

**The time-varying asymmetry of exchange rate returns: A stochastic volatility – stochastic skewness model**

> Faculty of Economics and Business Administration Campus Tweekerken, Tweekerkenstraat 2, 9000 Ghent - BELGIUM D/2018/7012/02 WORKING PAPER THE TIME-VARYING ASYMMETRY OF EXCHANGE RATE RETURNS: A STOCHASTIC VOLATILITY – STOCHASTIC SKEWNESS MODEL Martin Iseringhausen March 2018 (revised June 2020) 2018/944 The Time-Varying Asymmetry of Exchange Rate Returns: A Stochastic Volatility - Stochastic Skewness Model Martin Iseringhausen ∗ Ghent University June 2020 Abstract While the time-varying volatility of ﬁnancial returns has been extensively modelled, most existing stochastic volatility models either assume a constant degree of return shock asymme- try or impose symmetric model innovations. However, accounting for time-varying asymmetry as a measure of crash risk is important for both investors and policy makers. This paper ex- tends a standard stochastic volatility model to allow for time-varying skewness of the return innovations. We estimate the model by extensions of traditional Markov Chain Monte Carlo (MCMC) methods for stochastic volatility models. When applying this model to the r

### id `W2957514510`

**Incorporating overnight and intraday returns into multivariate GARCH volatility models**

> Incorporating overnight and intraday returns into multivariate GARCH volatility models Geert Dhaene∗ Jianbin Wu† January 17, 2019 Abstract We propose and evaluate mixed-frequency multivariate GARCH models for forecasting low- frequency (weekly) volatility based on high-frequency intraday returns (at 5-minute in- tervals) and on the overnight returns. The low-frequency conditional volatility matrix is modelled as a weighted sum of an intraday and an overnight component. The components are specified as multivariate GARCH processes of the BEKK type, adapted to the mixed- frequency data setting, and may enter the model as two separate components or as a single one. The models may further be extended by a nonparametrically estimated slowly-varying long-run volatility matrix. We evaluate the models in and out of sample using the 5-minute and overnight returns on four DJIA stocks (AXP, GE, HD, and IBM) from January 1988 to November 2014 and find that they systematically dominate a variety of models that only use lower-frequency data (weekly, daily, or close-to-open and open-to-close returns

### id `W2036327890`

**Volatility timing: How best to forecast portfolio exposures**

> This may be the author’s version of a work that was submitted/accepted for publication in the following source: Clements, Adam & Silvennoinen, Annastiina (2013) Volatility timing: How best to forecast portfolio exposures. Journal of Empirical Finance, 24, pp. 108-115. This ﬁle was downloaded from: https://eprints.qut.edu.au/220174/ © Consult author(s) regarding copyright matters This work is covered by copyright. Unless the document is being made available under a Creative Commons Licence, you must assume that re-use is limited to personal use and that permission from the copyright owner must be obtained for all other uses. If the docu- ment is available under a Creative Commons License (or other speciﬁed license) then refer to the Licence for details of permitted re-use. It is a condition of access that users recog- nise and abide by the legal requirements associated with these rights. If you believe that this work infringes copyright please provide details by email to qut.copyright@qut.edu.au License: Creative Commons: Attribution-Noncommercial-No Derivative Works 2.5 Notice: Pleas

### id `W2595639289`

**Directional predictability from stock market sector indices to gold: A cross-quantilogram analysis**

> Munich Personal RePEc Archive Directional predictability from stock market sector indices to gold: A cross-quantilogram analysis Baumöhl, Eduard and Lyócsa, Štefan University of Economics in Bratislava 25 January 2017 Online at https://mpra.ub.uni-muenchen.de/76915/ MPRA Paper No. 76915, posted 18 Feb 2017 14:17 UTC Directional predictability from stock market sector indices to gold: A cross-quantilogram analysis Eduard Baumöhla* – Štefan Lyócsaa Abstract We address the safe haven properties of gold relative to US stock market sector indices using the bivariate cross-quantilogram of Han et al. (2016). Splitting our sample into pre- and post-crisis periods, our results show that the safe haven properties of gold have a changing nature. Before and after the financial crisis, we find only limited quantile dependence and that gold can be considered a safe haven for most of the sectors, except Industrials. On a full sample (1999-2016), there are only three sectors – Healthcare, IT, and Telecommunication services – for which gold can be considered a safe haven. Keywords: stock market secto

### id `W2924657543`

**Forecasting volatility with a stacked model based on a hybridized Artificial Neural Network**

> Forecasting volatility with a stacked model based on a hybridized Artiﬁcial Neural Network Eduardo Ramos-P´ erez(1), Pablo J. Alonso-Gonz´ alez(2), Jos´ e Javier N´ u˜ nez-Vel´ azquez(2) (1) Ph D Student (Economics and Management Program). Universidad de Alcal´ a. (2) Economics Department. Universidad de Alcal´ a.∗† Abstract An appropriate calibration and forecasting of volatility and market risk are some of the main challenges faced by companies that have to manage the uncertainty inherent to their investments or funding operations such as banks, pension funds or insurance companies. This has become even more evident after the 2007- 2008 Financial Crisis, when the forecasting models assessing the market risk and volatility failed. Since then, a signiﬁcant number of theoretical developments and methodologies have appeared to improve the accuracy of the volatility fore- casts and market risk assessments. Following this line of thinking, this paper introduces a model based on using a set of Machine Learning techniques, such as Gradient Descent Boosting, Random Forest, Support Vector Ma

### id `W4379932342`

**Predicting the state of synchronization of financial time series using cross recurrence plots**

> ORIGINAL ARTICLE Predicting the state of synchronization of financial time series using cross recurrence plots Mostafa Shabani 1 • Martin Magris 1 • George Tzagkarakis 2,3 • Juho Kanniainen 4 • Alexandros Iosiﬁdis 1 Received: 25 November 2022 / Accepted: 10 May 2023 / Published online: 8 June 2023 /C211The Author(s) 2023 Abstract Cross-correlation analysis is a powerful tool for understanding the mutual dynamics of time series. This study introduces a new method for predicting the future state of synchronization of the dynamics of two ﬁnancial time series. To this end, we use the cross recurrence plot analysis as a nonlinear method for quantifying the multidimensional coupling in the time domain of two time series and for determining their state of synchronization. We adopt a deep learning framework for methodologically addressing the prediction of the synchronization state based on features extracted from dynamically sub- sampled cross recurrence plots. We provide extensive experiments on several stocks, major constituents of the S &P100 index, to empirically validate our approach. 

### id `W2308517403`

**An International Comparison of Implied, Realized, and GARCH Volatility Forecasts**

> 1 An International Comparison of Implied, Realized and GARCH Volatility Forecasts * Apostolos Kourtis, Raphael N. Markellos and Lazaros Symeonidis† Abstract We compare the predictive ability and economic value of implied, realized and GARCH volatility models for 13 equity indices from 10 countries. Model ranking is similar across countries, but varies with the forecast horizon. At the daily horizon, th e Heterogeneous Autoregressive model offers the most accurate predictions while an implied volatility model that corrects for the volatility risk premium is superior at the monthly horizon . Widely used GARCH models have inferior performance in almost all cases considered. All methods perform significantly worse over the 2008-09 crisis period. Finally, implied volatility offers significant improvements against historical methods for international portfolio diversification. JEL codes: G15; G17; G01; G11 Keywords: Implied Volatility; Realized Volatility; Volatility Risk Premium; Financial Crisis; International Diversification * We would like to thank two anonymous referees, the editor Ro

### id `W2163488659`

**Technical Analysis of the Taiwanese Stock Market**

> www.ccsenet.org/ijef Intern ational Journal of Economics and Finance V ol. 4, No. 1; January 2012 ISSN 1916-971X E-ISSN 1916-9728 90 Technical Analysis of the Taiwanese Stock Market Massoud Metghalchi School of Business, University of Houston-Victoria, Texas, USA Yung-Ho Chang (Corresponding author) Chang is from Department of Finance, Tunghai University, Taiwan E-mail: changy@thu.edu.tw Xavier Garza-Gomez School of Business, University of Houston-Victoria, Texas, USA Received: September 10, 2011 Accepted: November 20, 2011 Published: January 1, 2012 doi:10.5539/ijef.v4n1p90 URL: http://dx.doi.org/10.5539/ijef.v4n1p90 Abstract We study the profitability of technical trading rules based on 9 popular tech nical indicators. To further examine whether investors can design technical tr ading strategies that can beat the buy -and-hold strategy, we establish 13 trading models based on one indicator, 25 models based on two indicators, and 28 models based on three indicators. The empirical results show that 58 out of 66 models rej ect the null hypothesis of e quality of the mean returns betwe

### id `W1998667138`

**Forecasting return volatility: Level shifts with varying jump probability and mean reversion**

> F orecasting Return V olatility: Level Shifts with V arying Jump Probability and Mean Reversion Jiawen Xuy Shanghai University of Finance and Economics and Key Laboratory of Mathematical Economics Pierre Perronz Boston University March 1, 2013; Revised November 28, 2013. Abstract We extend the random level shift (RLS) model of Lu and Perron (2010) for the volatility of asset prices, which consists of a short memory process and a random level shift component. Motivated by empirical features a) we specify a time-varying probability of shifts as a function of large negative lagged returns; b) we incorporate a mean reverting mechanism so that the sign and magnitude of the jump component change according to the deviations of past jumps from their long run mean. This allows the possibility of forecasting the sign and magnitude of the jumps. We estimate the model using twelve di¤erent series. We compare its forecasting performance with a variety of competing models at various horizons. A striking feature is that the modi ed RLS model has the smallest mean square forecast errors in 64 out o

### id `W3215294658`

**Realized volatility spillovers between energy and metal markets: a time-varying connectedness approach**

> Open Access © The Author(s) 2024. Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the mate- rial. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http:// creativecommons.org/licenses/by/4.0/. RESEARCH Cunado et al. Financial Innovation (2024) 10:12 https://doi.org/10.1186/s40854-023-00554-7 Financial Innovation Realized volatility spillovers between energy and metal markets: a time-varying connectedne

### id `W2985561311`

**Volatility spillovers in commodity markets: A large t-vector autoregressive approach**

> Energy Economics 85 (2020) 104555 Contents lists available at ScienceDirect Energy Economics jou rn al hom epage: www.elsevier.com/locate/eneeco Volatility spillovers in commodity markets: A large t-vector autoregressive approach Luca Barbagliaa,b,∗, Christophe Crouxc, Ines Wilmsd a European Commission, Joint Research Centre (JRC), Ispra, Italy b Faculty of Economics and Business, KU Leuven, Belgium c EDHEC Business School, Lille, France d Department of Quantitative Economics, Maastricht University, The Netherlands a r t i c l e i n f o Article history: Received 11 February 2019 Received in revised form 26 August 2019 Accepted 18 October 2019 Available online 2 November 2019 JEL classiﬁcation: C58 C32 Q02 Keywords: Commodities Forecasting Lasso Multivariate t-distribution Vector autoregressive model Volatility spillover a b s t r a c t Prices of commodities have shown large ﬂuctuations. A high volatility of one commodity today may impact the volatility of another commodity tomorrow. As such, agricultural and energy commodities are closely dependent due to the expansion of the biofuel

