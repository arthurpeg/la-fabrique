# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 1 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-01.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W4307368010`

**Exploring the predictability of intraday returns in China's stock market**

> BCP Business & Management FMEME 2022 Volume 30 (2022) 735 Exploring the predictability of intraday returns in China's stock market Yanbing Xu* Nanjing University of Science and Technology, Jiangsu, China *Corresponding author: 1067615488@qq.com Abstract. With the rapid development of high-frequency trading, intraday trading has become more and more popular due to its important role in understanding the efficiency of the intraday market and capturing more trading opportunities. This article explores whether there is momentum effect and reversal effect in China’s stock market by studying the correlation and predictability between half - hour returns. The results show that there is an intraday momentum effect between the first half-hour and full -day returns. After the investment strategy, it is found that this effect has economic significance, but after considering the transaction costs, the momentum effect cannot make investors obtain excess returns. These costs are the reason for the long-term predictability of intraday returns. Keywords: Intraday returns predictability, Trading cost

### id `W3149462930`

**Gold and oil prices: abnormal returns, momentum and contrarian effects**

> Vol.:(0123456789) Financial Markets and Portfolio Management (2021) 35:353–368 https://doi.org/10.1007/s11408-021-00380-w 1 3 Gold and oil prices: abnormal returns, momentum and contrarian effects Guglielmo Maria Caporale1 · Alex Plastun2 Accepted: 6 February 2021 / Published online: 5 April 2021 © The Author(s) 2021 Abstract This paper explores price (momentum and contrarian) effects and their timing parameters on the days characterised by abnormal returns and the following ones in two commodity markets. Specifically, using daily gold and oil price data over the period 01.01.2009–31.03.2020 the following hypotheses are tested: (H1) there is a time gap between the detection of an abnormal return day and the end of that day, (H2) there are price effects on the day after abnormal returns occur; (H3) price effects after 1-day abnormal returns have identifiable timing parameters; (H4) the detected timing parameters can be used to “beat the market”. For these purposes average analysis, t tests, CAR and trading simulation approaches are used. The main results can be summarised as follows. 

### id `W3121499907`

**Intraday time series momentum: Global evidence and links to market characteristics**

> Intraday time series momentum: global evidence and links to market characteristics Article Accepted Version Creative Commons: Attribution-Noncommercial-No Derivative Works 4.0 Li, Z., Sakkas, A. and Urquhart, A. ORCID: https://orcid.org/0000-0001-8834-4243 (2022) Intraday time series momentum: global evidence and links to market characteristics. Journal of Financial Markets, 57. 100619. ISSN 1386-4181 doi: 10.1016/j.finmar.2021.100619 Available at https://centaur.reading.ac.uk/95566/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1016/j.finmar.2021.100619 Publisher: Elsevier All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Central Archive at the University of Reading Reading’s research outputs online

### id `W2133491221`

**Measuring volatility with the realized range**

> Measuring volatility with the realized range ∗ Martin Martens † Econometric Institute Erasmus University Rotterdam Dick van Dijk ‡ Econometric Institute Erasmus University Rotterdam Econometric Institute Report EI 2006-10 February 2006 Abstract Realized variance, being the summation of squared intra-da y returns, has quickly gained popularity as a measure of daily volatility. Following Parkinson (1980) we replace each squared intra-day return by the high- low range for that period to create a novel and more eﬃcient estimator call ed the realized range. In addition we suggest a bias-correction procedure t o account for the eﬀects of microstructure frictions based upon scaling the r ealized range with the average level of the daily range. Simulation experiment s demonstrate that for plausible levels of non-trading and bid-ask bounce the realized range has a lower mean squared error than the realized variance, in cluding variants thereof that are robust to microstructure noise. Empirical analysis of the S&P500 index-futures and the S&P100 constituents conﬁrm th e potential of the realiz

### id `W4388535504`

**Performance of Time-series Momentum Strategy: US Evidence**

> Performance of Time-series Momentum Strategy: US Evidence Siyao Duan1,a,* 1University of Glasgow, Glasgow G12 8QQ, UK a. 2803501d@student.gla.ac.uk *corresponding author Abstract: This paper examines the effectiveness of the time series momentum strategy in generating positive returns in the US stock market, with a focus on exploring its dynamics and performance using different moving average methods. The author conducted an empirical analysis of the time series momentum strategy u sing S&P500 data from 2000 to 2022. A regression model was applied to estimate the expected returns and volatility of each as -set, and then an evaluation of momentum trading strategy based on different moving average methods was developed. The author evalu ates the performance of the strategy with and without transaction costs. The study contributes to the literature by providing empirical evidence on the effectiveness of the time series momentum strategy in the US stock market and by exploring the performance of different moving average methods on the strategy. The findings of this study can provide insi

### id `W2007910409`

**Realized power variation and stochastic volatility models**

> Realized power variation and stochastic volatility models OLE E. BARNDORFF-NIELSEN 1 and NEIL SHEPHARD 2 1Centre for Mathematical Physics and Stochastics (MaPhySto), University of Aarhus, Ny Munkegade, DK-8000 Aarhus C, Denmark. E-mail: oebn@mi.aau.dk 2Nufﬁeld College, Oxford OX1 1NF , UK. E-mail: neil.shephard@nuf.ox.ac.uk Limit distribution results on realized power variation, that is, sums of absolute powers of increments of a process, are derived for certain types of semimartingale with continuous local martingale component, in particular for a class of ﬂexible stochastic volatility models. The theory covers, for example, the cases of realized volatility and realized absolute variation. Such results should be helpful in, for example, the analysis of volatility models using high-frequency information. Keywords: absolute returns; mixed asymptotic normality; p-variation; quadratic variation; realized volatility; semimartingale 1. Introduction Stochastic volatility processes play an important role in ﬁnancial economics, generalizing Brownian motion to allow the scale of the increment

### id `W2068585979`

**Scaling properties of foreign exchange volatility**

> Physica A 289 (2001) 249{266 www.elsevier.com/locate/physa Scaling properties of foreign exchange volatility Ramazan Gencaya;b; , Faruk Selcukb, Brandon Whitcherc aDepartment of Economics, University of Windsor, Windsor, 401, Sunset ONT Canada, N9B 3P4 bDepartment of Economics, Bilkent University, Bilkent 06533, Ankara, Turkey cEURANDOM, P.O. Box 513, 5600 MB Eindhoven, The Netherlands Received 14 June 2000 Abstract Inthispaper,weinvestigatethescalingpropertiesofforeignexchangevolatility.Ourmethod- ology is based on a wavelet multi-scaling approach which decomposes the variance of a time series and the covariance between two time series on a scale by scale basis through the appli- cation of a discrete wavelet transformation. It is shown that foreign exchange rate volatilities followdi erentscalinglawsatdi erenthorizons.Particularly,thereisasmallerdegreeofpersis- tence in intra-day volatility as compared to volatility at one day and higher scales. Therefore, a common practice in the risk management industry to convert risk measures calculated at shorter horizons into longer horizon

### id `W4200303559`

**THE IMPACT OF INTRADAY MOMENTUM ON STOCK RETURNS: EVIDENCE FROM S&P500 AND CSI300**

> 124 2021, XXIV, 4 Finance 10.15240/tul/001/2021-4-008 THE IMPACT OF INTRADAY MOMENTUM ON STOCK RETURNS: EVIDENCE FROM S&P500 AND CSI300 Saddam Hossain 1, Beáta Gavurová 2, Xianghui Yuan3, Morshadul Hasan 4, Judit Oláh5 1 Xi’an Jiaotong University, School of Economics and Finance, China, ORCID: 0000-0001-5663-1643, saddam@stu.xjtu.edu.cn; 2 Tomas Bata University in Zlín, Faculty of Management and Economics, Center for Applied Economic Research, Czech Republic, ORCID: 0000-0002-0606-879X, gavurova@utb.cz; 3 Xi’an Jiaotong University, School of Economics and Finance, China, ORCID: 0000-0003-1466-5268, xhyuan@mail.xjtu.edu.cn (corresponding author); 4 University of Debrecen, Károly Ihrig Doctoral School, Hungary, ORCID: 0000-0001-9857-9265, mohammad.hasan@econ.unideb.hu; 5 WSB University, Faculty of Applied Sciences, Department of Management, Poland, ORCID: 0000-0003-2247-1711, juditdrolah@gmail.com. Abstract: This paper analyzes the statistical impact of COVID-19 on the S&P500 and the CSI300 intraday momentum. This study employs an empirical method, that is, the intraday momentum method

### id `W2110141348`

**The day of the week effect on stock market volatility and volume: International evidence**

> The day of the week effect on stock market volatility and volume: International evidence Halil Kiymaz a,*, Hakan Berument b aDepartment of Finance, School of Business and Public Administration, University of Houston-Clear Lake, Houston, TX 77058, USA bDepartment of Economics, Bilkent University, Ankara, Turkey Received 4 January 2001; received in revised form 7 February 2002; accepted 6 June 2003 Abstract This study investigates the day of the week effect on the volatility of major stock market indexes for the period of 1988 through 2002. Using a conditional variance framework, we find that the day of the week effect is present in both return and volatility equations. The highest volatility occurs on Mondays for Germany and Japan, on Fridays for Canada and the United States, and on Thursdays for the United Kingdom. For most of the markets, the days with the highest volatility also coincide with that market’s lowest trading volume. Thus, this paper supports the argument made by Foster and Viswanathan [Rev. Financ. Stud. 3 (1990) 593] that high volatility would be accompanied by low tr

### id `W3199228172`

**Bitcoin intraday time series momentum**

> Bitcoin intraday time-series momentum Article Accepted Version Shen, D., Urquhart, A. ORCID: https://orcid.org/0000-0001- 8834-4243 and Wang, P. (2022) Bitcoin intraday time-series momentum. Financial Review, 57 (2). pp. 319-344. ISSN 1540- 6288 doi: 10.1111/fire.12290 Available at https://centaur.reading.ac.uk/100181/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1111/fire.12290 Publisher: Wiley All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Central Archive at the University of Reading Reading’s research outputs online 1 Bitcoin Intraday Time-Series Momentum Abstract This study examines intraday time -series momentum in Bitcoin. Unlike stock markets, Bitcoin trades 24 hours a day and therefore has not got a clear opening and 

### id `W2799918576`

**Bitcoin is not the New Gold – A comparison of volatility, correlation, and portfolio performance**

> Bitcoin is not the New Gold – A comparison of volatility, correlation, and portfolio performance Klein, T., Thu, H. P., & Walther, T. (2018). Bitcoin is not the New Gold – A comparison of volatility, correlation, and portfolio performance. International Review of Financial Analysis, 59, 105-116. https://doi.org/10.1016/j.irfa.2018.07.010 Published in: International Review of Financial Analysis Document Version: Peer reviewed version Queen's University Belfast - Research Portal: Link to publication record in Queen's University Belfast Research Portal Publisher rights Copyright 2018 Elsevier. This manuscript is distributed under a Creative Commons Attribution-NonCommercial-NoDerivs License (https://creativecommons.org/licenses/by-nc-nd/4.0/), which permits distribution and reproduction for non-commercial purposes, provided the author and source are cited General rights Copyright for the publications made accessible via the Queen's University Belfast Research Portal is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that us

### id `W3082678610`

**Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression**

> This is a self -archived – parallel published version of this article in the publication archive of the University of Vaasa. It might differ from the original. Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression Author(s): Dawar, Ishaan; Dutta, Anupam; Bouri, Elie; Saeed, Tareq Title: Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression Year: 2021 Version: Accepted manuscript Copyright ©2021 Elsevier. This manuscript version is made available under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International (CC BY–NC–ND 4.0) license, https://creativecommons.org/licenses/by-nc-nd/4.0/ Please cite the original version: Dawar, I., Dutta, A., Bouri, E. & Saeed, T. (2021). Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression. Renewable Energy 163, 288-299. https://doi.org/10.1016/j.renene.2020.08.162 1 Crude oil prices and clean energy stock indices: lagged and asymmetric effects 1 with quantile regression 2 3 4 5 6 7 

### id `W2930793690`

**Cryptocurrencies and momentum**

> This is a self -archived – parallel published version of this article in the publication archive of the University of Vaasa. It might differ from the original. Cryptocurrencies and momentum Author(s): Grobys, Klaus; Sapkota, Niranjan Title: Cryptocurrencies and momentum Year: 2019 Version: Publisher’s PDF Copyright ©2019 The Authors. Published by Elsevier B.V. Open access article under the Creative Commons Attribution– NonCommercial–NoDerivatives 4.0 International (CC BY–NC– ND) license, http://creativecommons.org/licenses/by-nc- nd/4.0/ Please cite the original version: Grobys, K ., & Sapkota, N ., (2019). Cryptocurrencies and momentum. Economics letters 180(July), 6–10. https://doi.org/10.1016/j.econlet.2019.03.028 EconomicsLetters180(2019)6–10 Contents lists available at ScienceDirect EconomicsLetters journal homepage: www.elsevier.com/locate/ecolet Cryptocurrenciesandmomentum KlausGrobys1,NiranjanSapkota ∗,1 DepartmentofAccountingandFinance,UniversityofVaasa,Wolffintie34,65200Vaasa,Finland h i g h l i g h t s • Weexplorewhethermomentumdoesexistincryptocurrencymarkets. • Wefindtha

### id `W3134867108`

**Dynamic connectedness between stock markets in the presence of the COVID-19 pandemic: does economic policy uncertainty matter?**

> Dynamic connectedness between stock markets in the presence of the COVID‑19 pandemic: does economic policy uncertainty matter? Manel Youssef1, Khaled Mokni1,2* and Ahdi Noomen Ajmi3,4 Introduction Academics, policymakers, and investors have heated discussions over analyzing the con- nectedness between financial markets, but this analysis was recently reinforced by math- ematical and econometric tool development. These tools increased its importance by providing a comprehensive picture of market risk, credit risk, and macroeconomic and system risk evaluation (Gong et al. 2019) to support better decision-making (Kou et al. 2014). Furthermore, analyzing connectedness between financial assets, especially stocks, Abstract This study investigates the dynamic connectedness between stock indices and the effect of economic policy uncertainty (EPU) in eight countries where COVID-19 was most widespread (China, Italy, France, Germany, Spain, Russia, the US, and the UK) by implementing the time-varying VAR (TVP-VAR) model for daily data over the period spanning from 01/01/2015 to 05/18/2020. Resu

### id `W3187800371`

**Dynamic spillovers between the term structure of interest rates, bitcoin, and safe-haven currencies**

> Dynamic spillovers between the term structure of interest rates, bitcoin, and safe‑haven currencies David Y. Aharon1, Zaghum Umar2,3* and Xuan Vinh Vo3 Introduction The outbreak of the COVID-19 pandemic in early 2020 reinvigorated the search for use - ful risk management, hedging strategies, and investors’ demand for safe-haven assets. Although traditionally major currencies have been regarded as safe-haven assets, several financial market downturns, such as the 2008 subprime crisis and the 2011 sovereign Abstract This study examines the connectedness between the US yield curve components (i.e., level, slope, and curvature), exchange rates, and the historical volatility of the exchange rates of the main safe-haven fiat currencies (Canada, Switzerland, EURO, Japan, and the UK) and the leading cryptocurrency, the Bitcoin. Results of the static analysis show that the level and slope of the yield curve are net transmitters of shocks to both the exchange rate and its volatility. The exchange rate of the Euro and the volatility of the Euro and the Canadian dollar exchange rate are net tran

### id `W4385076709`

**Exploiting the dynamics of commodity futures curves**

> 1 Exploiting the dynamics of commodity futures curves Robert J. Bianchia, John Hua Fana, Joëlle Miffreb,c,, Tingxi Zhangd a. Griffith Business School, Griffith University, Brisbane, Australia b. Audencia Business School, 8 Route de la Jonelière, 44300, Nantes, France c. Louis Bachelier Fellow, Paris, France d. Curtin University, Perth, Australia Abstract The Nelson-Siegel framework is employed to model the term structure of commodity futures prices. Exploiting the information embedded in the level, slope and curvature parameters, we develop novel investment strategies that assume short -term continuation of recent parallel, slope or butterfly movements of futures curves. Systematic strategies based on the change in the slope generate significant profits that are unrelated to previously documented risk factors and can survive reasonable transaction costs. Further analysis demonstrates that t he profitability of the slope strategy increases with investor sentiment and is in part a compensation for the drawdowns incurred during economic slowdowns. The profitability can also be magnifie

### id `W2617434451`

**Forecasting oil price realized volatility using information channels from other asset classes**

> 1 Forecasting oil price realized volatility using information channels from other asset classes Stavros Degiannakis1,2 and George Filis1,3,* 1Department of Economics and Regional Development, Panteion University of Social and Political Sciences, 136 Syggrou Avenue, 17671, Greece. 2Postgraduate Department of Business Administration, Hellenic Open University, Aristotelous 18, 26 335, Greece. 3Department of Accounting, Finance and Economics, Bournemouth University, BH8 8EB, United Kingdom. *Corresponding author: email: gfilis@bournemouth.ac.uk Abstract Motivated from Ross (1989) who maintains that asset volatilities are synonymous to the information flow, we claim that cross -market volatility transmission effects are synonymous to cross -market information flows or “information channels” from one market to another. Based on this assertion we assess whether cross-market volatility flows contain important information that can improve the accuracy of oil price realized volatility forecasting . We concentrate on realized volatilities derived from the intra-day prices of the Brent crude oil

### id `W1969306056`

**From the bird's eye to the microscope: A survey of new stylized facts of the intra-daily foreign exchange markets**

> Finance Stochast. 1, 95–129 (1997) c⃝ Springer-V erlag 1997 From the bird’s eye to the microscope: A survey of new stylized facts of the intra-daily foreign exchange markets ⋆ Dominique M. Guillaume 1, Michel M. Dacorogna 2, Rakhal R. Dav ´e2, Ulrich A. M ¨uller2, Richard B. Olsen 2, Olivier V. Pictet 2 1 Financial Markets Group, London School of Economics and C.S.A.E. Institute of Economics and Statistics, University of Oxford, St. Cross Building, Manor Road, Oxford OX1 3UL, United Kingdom (e-mail: dominique.guillaume@economics.ox.ac.uk) 2 Olsen & Associates, Research Institute for Applied Economics, CH-8008 Z ¨urich, Switzerland Abstract. This paper presents stylized facts concerning the spot intra-daily for- eign exchange markets. It ﬁrst describes intra-daily data and proposes a set of deﬁnitions for the variables of interest. Empirical regularities of the foreign ex- change intra-daily data are then grouped under three major topics: the distribution of price changes, the process of price formation and the heterogeneous structure of the market. The stylized facts surveyed in this

### id `W4301430573`

**High Frequency Return and Risk Patterns in U.S. Sector ETFs during COVID-19**

> International Journal of Energy Economics and Policy | V ol 12 • Issue 5 • 2022 441 International Journal of Energy Economics and Policy ISSN: 2146-4553 available at http: www.econjournals.com International Journal of Energy Economics and Policy, 2022, 12(5), 441-456. High Frequency Return and Risk Patterns in U.S. Sector ETFs during COVID-19 Ikhlaas Gurrib1*, Firuz Kamalov2, Elgilani E. Alshareif3 1Faculty of Management, School of Graduate Studies, Canadian University Dubai, UAE, 2Faculty of Engineering and Architecture, Canadian University Dubai, UAE, 3Faculty of Management, School of Graduate Studies, Canadian University Dubai, UAE. *Email: ikhlaas@cud.ac.ae Received: 22/03/2022 Accepted: 25/07/2022 DOI: https://doi.org/10.32479/ijeep.13045 ABSTRACT This study investigates intraday patterns in the eleven sectors of the United States (U.S.). Key contributions are (i) risk and return patterns at specific trading periods on the New Y ork Stock Exchange (NYSE), (ii) whether a specific day return model can predict the next 15-min positive return, and (iii) the impact of the first vacci

### id `W3124547477`

**Information leadership in the advanced Asia–Pacific stock markets: Return, volatility and volume information spillovers from the US and Japan**

> Information leadership in the advanced Asia-Pacific stock markets: Return, volatility and volume information spillovers from the US and Japan Author: Kim, Suk-Joong Publication details: Journal of the Japanese and International Economies v. 19 Chapter No. 3 pp. 338-365 0889-1583 (ISSN) Publication Date: 2005 Publisher DOI: http://dx.doi.org/10.1016/j.jjie.2004.03.002 License: https://creativecommons.org/licenses/by-nc-nd/3.0/au/ Link to license to see what you are allowed to do with this resource. Downloaded from http://hdl.handle.net/1959.4/40149 in https:// unsworks.unsw.edu.au on 2026-09-22 Information leadership in the advanced Asia-Pacific stock markets: Return, volatility and volume information spillovers from the U.S. and Japan Suk-Joong Kim School of Banking and Finance The University of New South Wales UNSW SYDNEY NSW 2052 Australia Tel: +61 2 9385-4278 Fax: + 61 2 9385-6347 Email: s.kim@unsw.edu.au Abstract: This paper investigates the nature of the stock ma rket linkages in the advanced Asia-Pacific stock markets of Australia, Hong Kong, Japan and Singapore with the U.S an

### id `W3153001253`

**Intraday volatility transmission among precious metals, energy and stocks during the COVID-19 pandemic**

> RaY Research at the University of York St John For more information please contact RaY at ray@yorksj.ac.uk Farid, Saqib, Mujtaba, Ghulam, Abubakr Naeem, Muhammad and Jawad Hussain Shahzad, Syed (2021) Intraday volatility transmission among precious metals, energy and stocks during the COVID-19 pandemic. Resources Policy, 72 (102101). Downloaded from: https://ray.yorksj.ac.uk/id/eprint/10039/ The version presented here may differ from the published version or version of record. If you intend to cite from the work you are advised to consult the publisher's version: http://dx.doi.org/10.1016/j.resourpol.2021.102101 Research at York St John (RaY) is an institutional repository. It supports the principles of open access by making the research outputs of the University available in digital form. Copyright of the items stored in RaY reside with the authors and/or other copyright owners. Users may access full text items free of charge, and may download a copy for private study or non-commercial research. For further reuse terms, see licence terms governing individual outputs. Institutional R

### id `W7143269026`

**Investor clientele and intraday patterns in the cross section of stock returns**

> Investor Clientele and Intraday Patterns in the Cross Section of Stock Returns January 5, 2024 Abstract This paper examines the existence of a well documented Heston, Korajczyk, and Sadka (2010) (hereafter HKS (2010)) intraday momentum pattern in the cross section of stock returns for three previously un-examined markets outside the US - UK, China and Brazil. While the stocks in UK and Brazil exhibit the pattern, the evidence from China is lacklustre. We utlitlize the presence of dual listed A-shares(dominated by domestic retail investors) and their B- and H-share counterparts (dominated by foreign institutional investors) of the same firms which provide a natural experiment setting to analyse the impact of investor clientele on the proliferation of HKS (2010) pattern. Our findings indicate that pattern is much weaker in A-shares (owned mostly by domestic retail investors) as compared to their B- and H- share counterparts. As a further robustness test we examine the impact of an exogenous shock that leads to an increase in institutional ownership namely the partial index inclusion of

### id `W2949333925`

**Measuring the Frequency Dynamics of Financial Connectedness and Systemic Risk***

> Measuring the frequency dynamics of ﬁnancial connectedness and systemic risk∗† Jozef Barun´ıka,b‡, and Tom´ aˇ sKˇrehl´ıka,b a Institute of Economic Studies, Charles University, Opletalova 26, 110 00, Prague, Czech Republic b Department of Econometrics, IITA, The Czech Academy of Sciences, Pod Vodarenskou Vezi 4, 182 00, Prague, Czech Republic December 20, 2017 Abstract We propose a new framework for measuring connectedness among ﬁnancial variables that arises due to heterogeneous frequency responses to shocks. To estimate connectedness in short-, medium-, and long-term ﬁnancial cycles, we introduce a framework based on the spec- tral representation of variance decompositions. In an empirical application, we document the rich time-frequency dynamics of volatility connectedness in US ﬁnancial institutions. Economically, periods in which connectedness is created at high frequencies are periods when stock markets seem to process information rapidly and calmly, and a shock to one asset in the system will have an impact mainly in the short term. When the connectedness is created at lower 

### id `W2799948621`

**Multifractal analysis of financial markets: a review**

> arXiv:1805.04750v1 [q-fin.ST] 12 May 2018 Multifractal analysis of ﬁnancial markets Zhi-Qiang Jianga,b,1, Wen-Jie Xiea,b,1, Wei-Xing Zhoua,b,c,∗, Didier Sornette d,e aResearch Center for Econophysics, East China University of Science and Technology, Shanghai 200237, China bDepartment of Finance, School of Business, East China Unive rsity of Science and Technology, Shanghai 200237, China cDepartment of Mathematics, School of Science, East China Un iversity of Science and Technology, Shanghai 200237, China dDepartment of Management, Technology and Economics, ETH Zu rich, Zurich, Switzerland eSwiss Finance Institute, c/o University of Geneva, 40 blvd. Du Pont d’Arve, CH 1211 Geneva 4, Switzerland Abstract Multifractality is ubiquitously observed in complex natur al and socioeconomic systems. Multifractal analysis pro- vides powerful tools to understand the complex nonlinear na ture of time series in diverse ﬁelds. Inspired by its striking analogy with hydrodynamic turbulence, from which the idea of multifractality originated, multifractal anal y- sis of ﬁnancial markets has bloomed, for

### id `W2094859553`

**On covariance estimation of non-synchronously observed diffusion processes**

> On covariance estimation of non-synchronously observed diffusion processes TAKAKI HA YASHI 1 and NAKAHIRO YOSHIDA 2 1Department of Statistics, Columbia Universi ty, 1255 Amsterdam Avenue, New York NY 10027, USA. E-mail: hayashi@stat.columbia.edu 2Graduate School of Mathematical Sciences, University of Tokyo, 3-8-1 Komaba, Meguro-ku, Tokyo 153-8914, Japan. E-mail : nakahiro@ms.u-tokyo.ac.jp We consider the problem of estimating the covariance of two diffusion processes when they are observed only at discrete times in a non-synchronous manner. The modern, popular approach in the literature, the realized covariance estimator, which is based on (regularly spaced) synchronous data, is problematic because the choice of regular interval size and data interpolation scheme may lead to unreliable estimation. We propose a new estimator which is free of any ‘synchronization’ processing of the original data, hence free of bias or other problems caused by it. Keywords: diffusions; discrete-time observations; high-frequency data; mathematical ﬁnance; non- synchronous trading; quadratic variation; r

### id `W4214609326`

**Overnight-Intraday Mispricing of Chinese Energy Stocks: A View from Financial Anomalies**

> Overnight-Intraday Mispricing of Chinese Energy Stocks: A View from Financial Anomalies Min Zhou 1 and Xiaoqun Liu 2* 1School of Design and Art, Hunan Institute of Technology, Hengyang, China, 2School of Economics, Hainan University, Haikou, China We verify the existence of ﬁrm-level “intraday return vs. overnight return ” pattern and overnight-intraday effect of nine ﬁnancial anomalies of Chinese energy industry stocks of the Chinese stock market. Though energy ﬁnance has been an independent research area, we also take Chinese A-shares stocks as samples for empirical analysis to avoid the so- called sample selection bias. Speci ﬁcally, it veri ﬁes that the overnight returns are strongly negative and intraday returns are positive for energy industry stocks, which is totally contrary to the American stock markets. In addition, alphas of the zero-cost strategies based on nine classic ﬁnancial anomalies are almost earned at night for energy industry stocks. Finally, it is risk-related anomalies that occur overnight for energy industry stocks, while both four risk-related anomalies and t

### id `W3123640941`

**Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open**

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 47, No. 4, Aug. 2012, pp. 715–741 COPYRIGHT 2012, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109012000270 Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open Henk Berkman, Paul D. Koch, Laura Tuttle, and Ying Jenny Zhang∗ Abstract We ﬁnd a strong tendency for positive returns during the overnight period followed by reversals during the trading day. This behavior is driven by an opening price that is high relative to intraday prices. It is concentrated among stocks that have recently attracted the attention of retail investors, it is more pronounced for stocks that are difﬁcult to value and costly to arbitrage, and it is greater during periods of high overall retail investor sentiment. The additional implicit transaction costs for retail traders who buy high-attention stocks near the open frequently exceed the effective half spread. I. Introduction Behavioral ﬁnance theories assume that individual investors are subject to sentiment that makes them willi

### id `W3122856157`

**Premium for heightened uncertainty: Explaining pre-announcement market returns**

> NBER WORKING PAPER SERIES PREMIUM FOR HEIGHTENED UNCERTAINTY: EXPLAINING PRE-ANNOUNCEMENT MARKET RETURNS Grace Xing Hu Jun Pan Jiang Wang Haoxiang Zhu Working Paper 25817 http://www.nber.org/papers/w25817 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 May 2019, Revised March 2021 An earlier draft of this paper was circulated under the title “Premium for Heightened Uncertainty: Solving the FOMC Puzzle.” We are grateful to Brad Barber, Ricardo Caballero, Peter Carr, Zhanhui Chen, Ing-Haw Cheng, Darrell Duffie, Ken French, Valentin Haddard, Toomas Laarits, David Lucca, Ian Martin, Annette Vissing-Jorgensen, Clara Vega, Kumar Venkataraman, Jessica Wachter, as well as seminar participants at the 2019 NBER Asset Pricing Program Spring Meeting, the 2019 ABFER Annual Meeting, the 2019 China International Conference in Finance, the 2019 Eastern Conference on Financial Mathematics, the 2019 Summer Institute in Finance, the 2020 AFA annual meeting, Tsinghua University, Shanghai Jiao Tong University, Peking University, Chinese University of Hong Kong, Cheung K

### id `W3123373742`

**Price Drift Before U.S. Macroeconomic News: Private Information about Public Announcements?**

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANAL YSIS Vol. 54, No. 1, Feb. 2019, pp. 449–479 COPYRIGHT 2018, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109018000625 Price Drift Before U.S. Macroeconomic News: Private Information about Public Announcements? Alexander Kurov, Alessio Sancetta, Georg Strasser, and Marketa Halova Wolfe* Abstract We examine stock index futures and Treasury futures around the release time of 30 U.S. macroeconomic announcements. Nine of the 20 announcements that move markets show evidence of substantial informed trading before the ofﬁcial release time. Prices begin to move in the “correct” direction approximately 30 minutes before the release time. The preannouncement price drift accounts on average for approximately 40% of the total price adjustment. This implies that some traders have private information about macroeconomic fundamentals. Preannouncement drift might originate from a combination of information leakage and superior forecasting that incorporates proprietary data. I. Introduction Macroeconomic n

### id `W4205498289`

**Profitability of technical trading strategies under market manipulation**

> Profitability of technical trading strategies under market manipulation Alfred Ma1,2* Introduction The closing price is important in finance. It is the most commonly used financial data in both academia and industry. Given its importance, it is also exposed to market manipu - lation which is defined as stock prices being artificially influenced (Allen and Gale 1992). However, most quantitative trading strategies use the official closing price as their input. This study examines the profitability impact of closing price market manipulation on technical trading strategies. Putniņš (2012) and Thoppan and Punniyamoorthy (2013) provide comprehensive sur - veys on market manipulation. Allen and Gale (1992) are early pioneers to start studies on market manipulation and formalize the study. They also introduce the concept of trade-based and information-based manipulation to classify cases of market manipula - tion. Aggarwal and Wu (2006) investigate cases of stock market manipulation and con - clude that market manipulation alters stock returns as a result. Market manipulation is not a probl

