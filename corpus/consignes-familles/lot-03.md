# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 3 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-03.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W4404328539`

**Forecasting the volatility of crude oil futures: New evidence from jump-induced volatility**

> Forecasting the volatility of crude oil futures: New evidence from jump-induced volatility Anupam Dutta a , * , Elie Bouri b a School of Accounting and Finance, University of Vaasa, Finland b School of Business, Lebanese American University, Lebanon ARTICLE INFO Handling editor: Mark Howells Keywords: Crude oil futures Realized volatility Jump-induced volatility OVX Leverage effects HAR-RV models ABSTRACT This paper proposes an augmented heterogenous autoregressive (HAR) model with time-varying jumps to forecast the realized volatility (RV) of crude oil futures. Jump-induced volatility of crude oil futures is obtained from a GARCH-jump process, then used to augment the HAR model. The results based on both the in-sample and out-of-sample analyses suggest that jumps offer added information for forecasting the RV of crude oil futures, surpassing the incremental information contained in the crude oil implied volatility index (OVX). Various robustness tests confirm these findings. Our findings have key implications for energy market investors, risk managers, and policymakers. 1. Introduct

### id `W2942897576`

**Is the diurnal pattern sufficient to explain intraday variation in volatility? A nonparametric assessment**

> Is the diurnal pattern sufficient to explain intraday variation in volatility? A nonparametric assessment ∗ Kim Christensen† Ulrich Hounyo‡,† Mark Podolskij§,† March, 2018 Abstract In this paper, we propose a nonparametric way to test the hypothesis that time-variation in intraday volatility is caused solely by a deterministic and recurrent diurnal pattern. We assume that noisy high-frequency data from a discretely sampled jump-diffusion process are available. The test is then based on asset returns, which are deflated by the seasonal component and therefore homoskedastic under the null. To construct our test statistic, we extend the concept of pre-averaged bipower variation to a general Itˆ o semimartingale setting via a truncation device. We prove a central limit theorem for this statistic and construct a positive semi- definite estimator of the asymptotic covariance matrix. Thet-statistic (after pre-averaging and jump-truncation) diverges in the presence of stochastic volatility and has a standard normal distribution otherwise. We show that replacing the true diurnal factor with a

### id `W2589169537`

**Asset allocation with time series momentum and reversal**

> Asset Allocation with Time Series Momentum and Reversal He, X.-Z., Li, K., & Li, Y. (2018). Asset Allocation with Time Series Momentum and Reversal. Journal of Economic Dynamics and Control, 91, 441-457. https://doi.org/10.1016/j.jedc.2018.02.004 Published in: Journal of Economic Dynamics and Control Document Version: Peer reviewed version Queen's University Belfast - Research Portal: Link to publication record in Queen's University Belfast Research Portal Publisher rights Copyright 2018 Elsevier. This manuscript is distributed under a Creative Commons Attribution-NonCommercial-NoDerivs License (https://creativecommons.org/licenses/by-nc-nd/4.0/), which permits distribution and reproduction for non-commercial purposes, provided the author and source are cited. General rights Copyright for the publications made accessible via the Queen's University Belfast Research Portal is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that users recognise and abide by the legal requirements associated with these rights. Take down poli

### id `W3047613430`

**Spillovers in Higher-Order Moments of Crude Oil, Gold, and Bitcoin**

> 1 Spillovers in Higher-Order Moments of Crude Oil, Gold, and Bitcoin Konstantinos Gkillas Department of Business Administration, University of Patras, Patras, Greece. Email: gillask@upatras.gr Elie Bouri USEK Business School, Holy Spirit University of Kaslik, Jounieh, Lebanon. Email: eliebouri@usek.edu.lb Rangan Gupta Department of Economics, University of Pretoria, South Africa. E-mail: rangan.gupta@up.ac.za David Roubaud Montpellier Business School, Montpellier, France. Email: d.roubaud@montpellier-bs.com Highlights  We analyze spillovers in jumps and realized second, third, and fourth moments among crude oil, gold, and Bitcoin markets  We use Granger causality and generalized impulse response analyses  Results suggest evidence of pre dictability and emphasize, among o t h e r s , t h e need of jointly modeling linkages across those three markets with higher-order moments Abstract We extend existing studies by considering the higher-order mome nts relationships among crude oil, gold, and Bitcoin markets. Using high-frequency data from December 2, 2014 to June 10, 2018, we analyz

### id `W3186579595`

**Volatility spillovers and contagion between energy sector and financial assets during COVID-19 crisis period**

> Vol.:(0123456789) Eurasian Economic Review (2021) 11:449–467 https://doi.org/10.1007/s40822-021-00181-6 1 3 ORIGINAL PAPER Volatility spillovers and contagion between energy sector and financial assets during COVID‑19 crisis period Achraf Ghorbel1 · Ahmed Jeribi2 Received: 2 December 2020 / Revised: 3 June 2021 / Accepted: 7 June 2021 / Published online: 21 July 2021 © Eurasia Business and Economics Society 2021 Abstract In this paper, we examine the relationship between the volatilities of the energy index, crude oil, gas prices, and financial assets (Gold, Bitcoin, and G7 stock indexes), especially during the coronavirus crisis. The study tests the presence of regime changes in the GARCH volatility dynamics of the G7 stock indexes, Bitcoin, Gold, and energy assets (energy index, oil, and gas) by using the Markov–Switch- ing GARCH model. It estimates the dynamic correlation and volatility spillover between energy and financial assets, by using the multivariate MSGARCH models. The estimation results of the Markov-Switching-BEKK-GARCH prove the volatil- ity spillover from energy asset

### id `W3121299458`

**HARK the SHARK: Realized Volatility Modeling with Measurement Errors and Nonlinear Dependencies**

> Copyright and Reuse: Copyright and Moral Rights remain with the author(s) and/or copyright holders. Copies of full items can be used for personal research or study, educational, or not-for-profit purposes without prior permission or charge, unless otherwise indicated, provided that the authors, title and full bibliographic details are credited, a hyperlink and/or URL is given for the original metadata page and the content is not changed in any way. For full details of reuse please refer to City Research Online policy. City Research Online: http://openaccess.city.ac.uk/ publications@citystgeorges.ac.uk Citation: Buccheri, G. & Corsi, F. (2021). HARK the SHARK: Realized Volatility Modeling with Measurement Errors and Nonlinear Dependencies. Journal of Financial Econometrics, 19(4), pp. 614-649. doi: 10.1093/jjfinec/nbz025 This is the accepted version of the paper. This version of the publication may differ from the final published version. To cite this item please consult the publisher's version. Permanent repository link: https://openaccess.city.ac.uk/id/eprint/23156/ Link to publishe

### id `W1830787149`

**An Empirical Analysis of the Relationships between Crude Oil,Gold and Stock Markets**

> arXiv:1510.07599v2 [q-fin.ST] 24 May 2016 An empirical analysis of the relationships between crude oil, gold and stock markets Semei Coronado a,, Rebeca Jim´ enez-Rodr ´ ıguezb,, Omar Rojas c, aDepartment of Quantitative Methods, Universidad de Guadal ajara, Guadalajara, Mexico bDepartment of Economics, IME, University of Salamanca, Sal amanca, Spain cSchool of Business and Economics, Universidad Panamerican a, Guadalajara, Mexico Abstract This paper analyzes the direction of the causality between c rude oil, gold and stock markets for the largest economy in the world with re spect to such markets, the US. To do so, we apply non-linear Granger ca usality tests. We ﬁnd a nonlinear causal relationship among the thre e markets considered, with the causality going in all directions, whe n the full sample and diﬀerent subsamples are considered. However, we ﬁnd a uni directional nonlinear causal relationship between the crude oil and gol d market (with the causality only going from oil price changes to gold price changes) when the subsample runs from the ﬁrst date of any year between the m

### id `W3124635921`

**Time reversal invariance in finance**

> arXiv:0708.4022v1 [q-fin.ST] 29 Aug 2007 Time reversal invariance in ﬁnance Gilles Zumbach RiskMetrics, Av des Morgines 12, 1213 Petit-Lancy, Switzerland. e-mail: gilles.zumbach@riskMetrics.com and Consulting in Financial Research, Ch. Charles Baudouin 8, 1228 Saconnex d’Arve, Switzerland. e-mail: gilles.zumbach@bluewin.ch January 2007 Abstract Time reversal invariance can be summarised as follows: no di fference can be measured if a sequence of events is run forward or backward in time. Becaus e price time series are domi- nated by a randomness that hides possible structures and ord ers, the existence of time reversal invariance requires care to be investigated. Different statistics are constructed with the property to be zero for time series which are time reversal invariant; they all show that high-frequency empirical foreign exchange prices are not invariant. The sa me statistics are applied to math- ematical processes that should mimic empirical prices. Mon te Carlo simulations show that only some ARCH processes with a multi-timescales structure can reproduce the empirical ﬁnd- 

### id `W2238911472`

**FORECASTING REALIZED VOLATILITY WITH LINEAR AND NONLINEAR UNIVARIATE MODELS**

> DEPARTMENT OF ECONOMICS AND FINANCE COLLEGE OF BUSINESS AND ECONOMICS UNIVERSITY OF CANTERBURY CHRISTCHURCH, NEW ZEALAND Forecasting Realized Volatility with Linear and Nonlinear Univariate Models* Michael McAleer and Marcelo C. Medeiros WORKING PAPER No. 28/2010 Department of Economics and Finance College of Business and Economics University of Canterbury Private Bag 4800, Christchurch New Zealand 1 Forecasting Realized Volatility with Linear and Nonlinear Univariate Models* Michael McAleer Econometric Institute Erasmus School of Economics Erasmus University Rotterdam and Tinbergen Institute The Netherlands and Department of Economics and Finance University of Canterbury New Zealand Marcelo C. Medeiros Department of Economics Pontifical Catholic University of Rio de Janeiro May 2010 * The first author wishes to acknowledge the financial support of the Australian Research Council, National Science Council, Taiwan, Center for International Research on the Japanese Economy (CIRJE), Faculty of Economics, University of Tokyo, and a Visiting Erskine Fellowship, College of Business and Eco

### id `W2944624526`

**Futures-based forecasts: How useful are they for oil price volatility forecasting?**

> Futures-based forecasts: How useful are they for oil price volatility forecasting? Ioannis Chatziantoniou *, Stavros Degiannakis **,***, and George Filis ***,a *Economics and Finance Subject Group, University of Portsmouth, Portsmouth Business School, Portland Street, Portsmouth, PO1 3DE, United Kingdom. **Department of Economics and Regional Development, Panteion University of Social and Political Sciences, 136 Syggrou Avenue, 17671, Greece. ***Bournemouth University, Department of Accounting, Finance and Economics, Executive Business Centre, 89 Holdenhurst Road, BH8 8EB, Bournemouth, UK. aCorresponding author’s email: gﬁlis@bournemouth.ac.uk May 13, 2019 Abstract Oil price volatility forecasts have recently attracted the attention of many studies in the energy ﬁnance ﬁeld. The literature mainly concentrates its attention on the use of daily data, using GARCH-type models. It is only recently that eﬀorts to use more informative intra- day data to forecast oil price realized volatility have been made. Despite all these previous eﬀorts, no study has examined the usefulness of futures-b

### id `W3044191953`

**Modelling the volatility of crude oil returns: Jumps and volatility forecasts**

> This is a self -archived – parallel published version of this article in the publication archive of the University of Vaasa. It might differ from the original. Modelling the volatility of crude oil returns : Jumps and volatility forecasts Author(s): Dutta, Anupam; Bouri, Elie; Roubaud, David Title: Modelling the volatility of crude oil returns : Jumps and volatility forecasts Year: 2020 Version: Accepted version Copyright © 2020 John Wiley & Sons, Ltd. This is the peer reviewed version of the following article: Dutta, A., Bouri, E., Roubaud, D. (2020). Modelling the volatility of crude oil returns: Jumps and volatility forecasts. International Journal of Finance and Economics, 1– 9, which has been published in final form at https://doi.org/10.1002/ijfe.1826. This article may be used for non-commercial purposes in accordance with Wiley Terms and Conditions for Use of Self-Archived Versions. Please cite the original version: Dutta, A., Bouri, E. & Roubaud, D. (2020). Modelling the volatility of crude oil returns : Jumps and volatility forecasts. International Journal of Finance and Eco

### id `W4281682358`

**To jump or not to jump: momentum of jumps in crude oil price volatility prediction**

> To jump or not to jump: momentum of jumps in crude oil price volatility prediction Yaojie Zhang1 , Yudong Wang1*, Feng Ma2 and Yu Wei3 Introduction The jump component is an essential and useful determinant in the prediction of the vol - atility dynamics of various asset prices, such as exchange rates, stock returns, and bond yields (see, e.g., Andersen et al. 2007; Corsi et al. 2010; Duong and Swanson 2015; Patton and Sheppard 2015; Clements and Liao 2017). However, an influential paper by Prokop - czuk et al. (2016) argues that explicitly using jumps cannot efficiently enhance the out- of-sample forecast accuracy for the volatility of the crude oil futures market. Prokopczuk et al. (2016) provide a plausible explanation that unpredictable events such as political unrest and natural disasters in oil-exporting countries always trigger jumps in oil prices. Theoretically, jumps do not occur at each point in time. When there is no jump in the oil price, incorporating the jump component into the predictive model will probably lead to overfitting, in which the in-sample forecasting perform

### id `W1885451613`

**REALIZED BETA GARCH: A MULTIVARIATE GARCH MODEL WITH REALIZED MEASURES OF VOLATILITY**

> Hi-Stat Discussion Paper Research Unit for Statistical and Empirical Analysis in Social Sciences (Hi-Stat) Hi-Stat Institute of Economic Research Hitotsubashi University 2-1 Naka, Kunitatchi Tokyo, 186-8601 Japan http://gcoe.ier.hit-u.ac.jp Global COE Hi-Stat Discussion Paper Series Research Unit for Statistical and Empirical Analysis in Social Sciences (Hi-Stat) December 2012 Realized Beta GARCH: A Multivariate GARCH Model with Realized Measures of Volatility and Covolatility Peter Reinhard Hansen Asger Lunde Valeri V oev 269 Realized Beta GARCH: A Multivariate GARCH Model with Realized Measures of Volatility and CoVolatility Peter Reinhard Hansena∗ Asger Lundeb Valeri Voevb aEuropean University Institute & CREATES bAarhus University, Department of Economics and Business, Fuglesangs Allé 4, 8210 Aarhus V, Denmark & CREATES December 14, 2012 Abstract We introduce a multivariate GARCH model that incorporates realized measures of volatility and covolatility. The realized measures extract information about the current level of volatility and covolatility from high-frequency data, which 

### id `W2915780587`

**Harnessing jump component for crude oil volatility forecasting in the presence of extreme shocks**

> This may be the author’s version of a work that was submitted/accepted for publication in the following source: Ma, Feng, Liao, Yin, Zhang, Y aojie, & Cao, Y ang (2019) Harnessing jump component for crude oil volatility forecasting in the pres- ence of extreme shocks. Journal of Empirical Finance, 52, pp. 40-55. This ﬁle was downloaded from: https://eprints.qut.edu.au/124773/ © Consult author(s) regarding copyright matters This work is covered by copyright. Unless the document is being made available under a Creative Commons Licence, you must assume that re-use is limited to personal use and that permission from the copyright owner must be obtained for all other uses. If the docu- ment is available under a Creative Commons License (or other speciﬁed license) then refer to the Licence for details of permitted re-use. It is a condition of access that users recog- nise and abide by the legal requirements associated with these rights. If you believe that this work infringes copyright please provide details by email to qut.copyright@qut.edu.au License: Creative Commons: Attribution-Noncom

### id `W2117821674`

**FRACTAL MARKETS HYPOTHESIS AND THE GLOBAL FINANCIAL CRISIS: SCALING, INVESTMENT HORIZONS AND LIQUIDITY**

> Fractal Markets Hypothesis and the Global Financial Crisis: Scaling, Investment Horizons and Liquidity Ladislav Kristoufek ∗ Abstract We investigate whether fractal markets hypothesis and its focus on liquidity and invest- ment horizons give reasonable predictions about dynamics of the ﬁnancial markets during the turbulences such as the Global Financial Crisis of late 2000s. Compared to the mainstream eﬃcient markets hypothesis, fractal markets hypothesis considers ﬁnancial markets as com- plex systems consisting of many heterogenous agents, which are distinguishable mainly with respect to their investment horizon. In the paper, several novel measures of trading activity at diﬀerent investment horizons are introduced through scaling of variance of the underlying processes. On the three most liquid US indices – DJI, NASDAQ and S&P500 – we show that predictions of fractal markets hypothesis actually ﬁt the observed behavior quite well. Keywords: Fractal markets hypothesis; Scaling; Fractality; Investment horizons; Eﬃcient markets hypothesis PACS: 05.45.Df, 89.65.Gh, 89.75.Da JEL: G01, 

### id `W1496351558`

**Jumps and stochastic volatility in crude oil futures prices using conditional moments of integrated volatility**

> eprints@whiterose.ac.uk https://eprints.whiterose.ac.uk Universities of Leeds, Sheffield and York Deposited via The University of York. White Rose Research Online URL for this paper: https://eprints.whiterose.ac.uk/id/eprint/81392/ Version: Submitted Version Article: Baum, Christopher and Zerilli, Paola Z (2016) Jumps and stochastic volatility in crude oil futures prices using conditional moments of integrated volatility. Energy economics. pp. 175-181. ISSN: 0140-9883 https://doi.org/10.1016/j.eneco.2014.10.007 Reuse Items deposited in White Rose Research Online are protected by copyright, with all rights reserved unless indicated otherwise. They may be downloaded and/or printed for private study, or other acts as permitted by national copyright laws. The publisher or other rights holders may allow further reproduction and re-use of the full text version. This is indicated by the licence information on the White Rose Research Online record for the item. Takedown If you consider content in White Rose Research Online to be in breach of UK law, please notify us by emailing eprints@white

### id `W2972387379`

**Moments-based spillovers across gold and oil markets**

> 1 Moments-Based Spillovers across Gold and Oil Markets# Matteo Bonato (matteobonato@gmail.com) (Department of Economics and Econometrics, University of Johannesburg, Auckland Park, South Africa; IPAG Business School, 184 Boulevard Saint-Germain, 75006 Paris, France) Rangan Gupta (rangan.gupta@up.ac.za) (Department of Economics, University of Pretoria, Pretoria, 0002, South Africa; IPAG Business School, 184 Boulevard Saint- Germain, 75006 Paris, France) Chi Keung Marco Lau (c.lau@hud.ac.uk) (Huddersfield Business School, University of Huddersfield, Huddersfield, HD1 3DH, United Kingdom) Shixuan Wang (shixuan.wang@reading.ac.uk) (Department of Economics, University of Reading, Reading, RG6 6AA, United Kingdom) # We would like to thank two anonymous referees for many helpful comments. However, any remaining errors are solely ours. 2 Abstract In this paper, we use intraday futures market data on gold and oil to compute returns, realized volatility, volatility jumps, realized skewness and realized kurtosis. Using these daily metrics associated with two markets over the period of December 

### id `W4415762045`

**Crude oil, forex, and stock markets: unveiling the higher-order moment and cross-moment risk spillovers in times of turmoil**

> ARTICLE Crude oil, forex, and stock markets: unveiling the higher-order moment and cross-moment risk spillovers in times of turmoil Jinxin Cui 1, Aktham Maghyereh 2 ✉ & Salem Ziadat 3,4 This study employs an analytical framework that integrates realized moment measures with a TVP-VAR-based extended joint connectedness approach to examine higher-order moment and cross-moment risk spillovers among crude oil futures (CL), Dollar Index futures (DX), and S&P 500 E-mini futures (ES). The ﬁndings reveal that the interconnectedness between crude oil, stock, and forex markets is shaped by distributional moments, with realized vola- tility (RV) spillovers being signi ﬁcantly stronger than those of higher-order moments (RS, RK) and jumps (RJ). Crude oil consistently acts as a net transmitter across all measures, underscoring its dominant role, while the forex and stock markets emerge as the primary net recipients of volatility and kurtosis spillovers, respectively. Spillover dynamics exhibit time- varying behavior and high sensitivity to crises, including the crude oil price collapse, the US ‒ 

### id `W2130774119`

**Do Jumps Matter for Volatility Forecasting? Evidence from Energy Markets**

> Do jumps matter for volatility forecasting? Evidence from energy markets Article Accepted Version Prokopczuk, M., Symeonidis, L. and Wese Simen, C. (2016) Do jumps matter for volatility forecasting? Evidence from energy markets. Journal of Futures Markets, 36 (8). pp. 758- 792. ISSN 1096-9934 doi: 10.1002/fut.21759 Available at https://centaur.reading.ac.uk/48497/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . Published version at: http://dx.doi.org/10.1002/fut.21759 To link to this article DOI: http://dx.doi.org/10.1002/fut.21759 Publisher: Wiley All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Central Archive at the University of Reading Reading’s research outputs online

### id `W2088102267`

**Forecasting realized volatility: a Bayesian model‐averaging approach**

> University of Toronto Department of Economics April 03, 2008 By Chun Liu and John M Maheu Forecasting Realized Volatility: A Bayesian Model Averaging Approach Working Paper 313 Forecasting Realized Volatility: A Bayesian Model Averaging Approach∗ Chun Liu School of Economics and Management Tsinghua University John M. Maheu Dept. of Economics University of Toronto This version: March 2008 Abstract How to measure and model volatility is an important issue in ﬁnance. Recent research uses high frequency intraday data to construct ex post measures of daily volatility. This paper uses a Bayesian model averaging approach to forecast realized volatility. Candidate models include autoregressive and heterogeneous autoregres- sive (HAR) speciﬁcations based on the logarithm of realized volatility, realized power variation, realized bipower variation, a jump and an asymmetric term. Applied to equity and exchange rate volatility over several forecast horizons, Bayesian model averaging provides very competitive density forecasts and modest improvements in point forecasts compared to benchmark model

### id `W2330475988`

**Nonparametric Estimation and Forecasting for Time-Varying Coefficient Realized Volatility Models**

> eprints@whiterose.ac.uk https://eprints.whiterose.ac.uk Universities of Leeds, Sheffield and York Deposited via The University of York. White Rose Research Online URL for this paper: https://eprints.whiterose.ac.uk/id/eprint/97244/ Version: Accepted Version Article: Xiangjin B., Chen,, Gao, Jiti, Li, Degui et al. (2018) Nonparametric Estimation and Forecasting for Time-Varying Coefficient Realized Volatility Models. Journal of Business and Economic Statistics. pp. 1-13. ISSN: 0735-0015 https://doi.org/10.1080/07350015.2016.1138118 Reuse Items deposited in White Rose Research Online are protected by copyright, with all rights reserved unless indicated otherwise. They may be downloaded and/or printed for private study, or other acts as permitted by national copyright laws. The publisher or other rights holders may allow further reproduction and re-use of the full text version. This is indicated by the licence information on the White Rose Research Online record for the item. Takedown If you consider content in White Rose Research Online to be in breach of UK law, please notify us by em

### id `W1979150730`

**On the volatility–volume relationship in energy futures markets using intraday data**

> On the volatility-volume relationship in energy futures markets using intraday data Université de Paris Ouest Nanterre La Défense (bâtiments T et G) 200, Avenue de la République 92001 NANTERRE CEDEX Tél et Fax : 33.(0)1.40.97.59.07 Email : nasam.zaroualete@u-paris10.fr Document de Travail Working Paper 2011-16 Julien Chevallier Benoît Sévi EconomiX http://economix.fr UMR 7235 On the volatility-volume relationship in energy futures markets using intraday data Julien Chevallier∗ Benoˆıt S ´evi† Universit´e Paris Dauphine Universit ´e de la M ´editerran´ee April 12, 2011 Abstract This paper investigates the relationship between trading v olume and price volatility in the crude oil and natural gas futures markets when using high-frequen cy data. By regressing various real- ized volatility measures (with/without jumps) on trading v olume and trading frequency, our re- sults feature a contemporaneous and largely positive relat ionship. Furthermore, we test whether the volatility-volume relationship is symmetric for energ y futures by considering positive and neg- ative realized semivarianc

### id `W2598243275`

**Does oil predict gold? A nonparametric causality-in-quantiles approach**

> Munich Personal RePEc Archive Does Oil Predict Gold? A Nonparametric Causality-in-Quantiles Approach Shahbaz, Muhammad and Balcilar, Mehmet and Ozdemir, Zeynel Abidin Montpellier Business School, Montpellier, France, Eastern Mediterranean University, Northern Cyprus, Turkey, Gazi University, Ankara, Turkey 1 March 2017 Online at https://mpra.ub.uni-muenchen.de/77324/ MPRA Paper No. 77324, posted 11 Mar 2017 01:53 UTC Does Oil Predict Gold? A Nonparametric Causality- in-Quantiles Approach* Muhammad Shahbaz a, Mehmet Balcilar a, b, Zeynel Abidin Ozdemir c a Montpellier Business School, Montpellier, France b Eastern Mediterranean University, Northern Cyprus, via Mersin 10, Turkey c Gazi University, Ankara, Turkey Abstract This paper examines the predictive power of oil pric e for gold price using the novel nonparametric causality-in-quantiles testing approa ch. The study uses weekly data over the April 1983-August 2016 period for both the spot and 1-month to 12-month futures markets. The new approach, the causality-in-quantile, allows o ne to test for causality-in-mean and causality-in-

### id `W2060330010`

**Analysis of Intra-Day Volatility under Economic Crisis Conditions**

> www.ccsenet.org/ijef International Journal of Economics and Finance V ol. 3, No. 4; September 2011 ISSN 1916-971X E-ISSN 1916-9728 60 Analysis of Intra-Day Volatility under Economic Crisis Conditions Michalis Glezakos Department of Insurance and Statistics, University of Piraeus 80 Karaoli & Dimitriou, 185 34, Piraeus, Greece E-mail: migl@unipi.gr Konstantinos Vafiadis Bank of Greece 4 Ag. Stefanou, Neapolis, 56727, Thessalonica, Greece E-mail: kvafiadis@bankofgreece.gr; kostasbaf@yahoo.com John Mylonakis (Corresponding Author) 10, Nikiforou str., Glyfada, 166 75, Athens, Greece E-mail: imylonakis@vodafone.net.gr Received: February 10, 2011 Accepted: Fe bruary 24, 2011 doi:10.5539 /ijef.v3n4p60 Abstract The purpose of this paper is to examine intra-day volatility of the Athens (GI), Frankfurt (DAX) and New York (DJ) Stock Markets under conditions of economic crisis. After utilizing 5 minutes intervals of the periods September – December of 2008 and 2009, a U-shaped intra-day volatility pattern was obser ved for DJ and an L-shaped one for DAX and GI. The results indicate a sharp spike

### id `W2046574432`

**Hurst exponent and prediction based on weak-form efficient market hypothesis of stock markets**

> arXiv:0712.1624v1 [q-fin.ST] 11 Dec 2007 Hurst exponent and prediction based on weak-form eﬃcient market hypothesis of stock markets Cheoljun Eom and Sunghoon Choi Division of Business Administration, Pusan National University, Busan 609-735, Republic of Kore a Gabjin Oh NCSL, Department of Physics, Pohang University of Science a nd Technology, Pohang, Gyeongbuk, 790-784, Republic of Korea & Asia Paciﬁc Center f or Theoretical Physics, Pohang, Gyeongbuk, 790-784, Republic of Korea Woo-Sung Jung Center for Polymer Studies and Department of Physics, Boston University, Boston, MA 02215, USA (Dated: November 26, 2024) Abstract We empirically investigated the relationships between the degree of eﬃciency and the predictabil- ity in ﬁnancial time-series data. The Hurst exponent was use d as the measurement of the degree of eﬃciency, and the hit rate calculated from the nearest-ne ighbor prediction method was used for the prediction of the directions of future price changes . We used 60 market indexes of various countries. We empirically discovered that the relationshi p between the degree o

### id `W4385781358`

**The predictive ability of technical trading rules: an empirical analysis of developed and emerging equity markets**

> Vol.:(0123456789) Financial Markets and Portfolio Management (2023) 37:403–456 https://doi.org/10.1007/s11408-023-00433-2 1 3 The predictive ability of technical trading rules: an empirical analysis of developed and emerging equity markets Kevin Rink1 Accepted: 10 May 2023 / Published online: 12 August 2023 © The Author(s) 2023 Abstract We investigate the predictability of leading equity indices of 23 developed and 18 emerging markets with a set of 6406 technical trading rules over up to 66 years. Using a state-of-the-art test for superior predictive ability to control for data snooping bias, we find in-sample evidence for technical heuristics with significant outperformance over a simple buy-and-hold strategy in the major - ity of markets. The proportion of heuristics with superior performance is much higher among emerging market indices, and the predictability diminishes drasti- cally over time in all markets. In particular, markets turn unpredictable in the last years of our sample. Moreover, the results are very sensitive to the intro- duction of moderate transaction costs. An ou

### id `W2103781827`

**Are there Monday effects in stock returns: A stochastic dominance approach**

> Are there Monday e¤ ects in Stock Returns: A Stochastic Dominance Approach Y oung-Hyun Choy Korea University Oliver Lintonz London School of Economics Y oon-Jae Whangx Seoul National University September 29, 2006 Abstract We provide a test of the Monday e¤ect in daily stock index returns. Unlike previous studies we de ne the Monday e¤ect based on the stochastic dominance criterion. This is a stronger criterion than those based on comparing means used in previous work and has a well de ned economic meaning. We apply our test to a number of stock indexes including large caps and small caps as well as UK and Japanese indexes. We nd strong evidence of a Monday e¤ect in many cases under this stronger criterion. The e¤ect has reversed or weakened in the Dow Jones and S&P 500 indexes post 1987, but is still strong in more broadly based indexes like the NASDAQ, the Russell 2000 and the CRSP. Keywords: E¢ cient Markets; stock market anomalies; subsampling JEL Classification: C12,C14,C15,G13,G14 Thanks to Franz Palm, Andrew Patton, and a referee for comments. Thanks especially to Anisha Ghos

### id `W2106497381`

**Technical Trading Rules in Australian Financial Markets**

> International Journal of Economics and Finance; V ol. 6, No. 10; 2014 ISSN 1916-971X E-ISSN 1916-9728 Published by Canadian Center of Science and Education 67 Technical Trading Rules in Australian Financial Markets Jung Soo Park1 & Chris Heaton1 1 Department of Economics, Macquarie University, North Ryde, Australia Correspondence: Chris Heaton, Department of Economics, Macquarie University, North Ryde NSW 2109, Australia. Tel: 61-2-9850-9921. Email: chris.heaton@.mq.edu.au Received: July 17, 2014 Accepted: July 31, 2014 Online Published: September 25, 2014 doi:10.5539/ijef.v6n10p67 URL: http://dx.doi.org/10.5539/ijef.v6n10p67 Abstract In this paper, we apply the 7,846 technical trading rules considered by Sullivan et al. (1999) to a stock index, some individual stocks, some currencies and some inte rest rate futures contracts traded in the Australian financial markets, and test for profitability relative to a buy-and-hold strategy. Size distortions due to data-snooping are avoided by using the Reality Check te st of White (2000) and the Superior Predictive Ability test of Hansen (200

### id `W3121421590`

**A Machine Learning Approach to Volatility Forecasting**

> A machine learning approach to volatility forecasting ∗ Kim Christensen † Mathias Siggaard † Bezirgen Veliyev† May, 2022 Abstract We inspect how accurate machine learning (ML) is at forecast ing realized variance of the Dow Jones Industrial Average index constituents. We compar e several ML algorithms, includ- ing regularization, regression trees, and neural networks , to multiple Heterogeneous AutoRe- gressive (HAR) models. ML is implemented with minimal hyper parameter tuning. In spite of this, ML is competitive and beats the HAR lineage, even whe n the only predictors are the daily, weekly, and monthly lags of realized variance. The fo recast gains are more pronounced at longer horizons. We attribute this to higher persistence in the ML models, which helps to approximate the long-memory of realized variance. ML als o excels at locating incremental information about future volatility from additional predi ctors. Lastly, we propose a ML mea- sure of variable importance based on accumulated local eﬀect s. This shows that while there is agreement about the most important predictors, t

### id `W3152658926`

**The persistence of financial volatility after COVID-19**

> Finance Research Letters 44 (2022) 102056 Available online 19 April 2021 1544-6123/© 2021 The Author(s). Published by Elsevier Inc. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/). The persistence of financial volatility after COVID-19 J. Eduardo Vera-Vald ´es a , b a Department of Mathematical Sciences, Aalborg University, Skjernvej 4A, Aalborg Ø st 9210, Denmark b CREATES, Denmark ARTICLE INFO JEL classification: G01 G15 C22 Keywords: COVID-19 Pandemic Volatility VIX Realized variance Persistence change ABSTRACT This paper analyzes the long-term effects of COVID-19 on financial volatility. We estimate the long memory parameters before and after COVID-19 for the VIX and realized variances for several international markets. Our results show that volatility measures for most countries experienced increases in the degrees of memory following the pandemic. Moreover, several volatility measures became nonstationary, signaling the start of a period with higher and more persistent financial volatility. We show that these changes in the d

