# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 9 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-09.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W1967758914`

**Forecasting Volatility of Gold Price Using Markov Regime Switching and Trading Strategy**

> Journal of Mathematical Finance, 2012, 2, 121-131 http://dx.doi.org/10.4236/jmf.2012.21014 Published Online February 2012 (http://www.SciRP.org/journal/jmf) Forecasting Volatility of Gold Price Using Markov Regime Switching and Trading Strategy Nop Sopipan1, Pairote Sattayatham1, Bhusana Premanode2 1School of Mathematics Suranaree, University of Technology, Nakhon Ratchasima, Thailand 2Institute of Biomedical Engineering, Imperial College South Kensington Campus, London, UK Email: {nopsopipan, bhusana}@gmail.com, pairote@sut.ac.th Received October 24, 2011; revised December 1, 2011; accepted December 15, 2011 ABSTRACT In this paper, we forecast the volatility of gold prices using Markov Regi me Switching GARCH (MRS-GARCH) mod- els. These models allow volatility to have different dynami cs according to unobserved regi me variables. The main pur- pose of this paper is to find out whether MRS-GARCH models are an improvement on the GARCH type models in terms of modeling and forecasting gold price volatility. The MRS-GARCH is best performance model for gold price volatility in some loss f

### id `W2029888734`

**Estimation of the lead-lag parameter from non-synchronous data**

> Bernoulli 19(2), 2013, 426–461 DOI: 10.3150/11-BEJ407 Estimation of the lead-lag parameter from non-synchronous data M. HOFFMANN 1,M .R O S E N B A U M2 and N. YOSHIDA 3 1ENSAE – CREST and CNRS UMR 8050, Timbre J120, 3, avenue Pierre Larousse, 92245 Malakoff Cedex, France. E-mail: marc.hoffmann@ensae.fr 2LPMA – Université Pierre et Marie Curie (Paris 6) and CREST, 4 Place Jussieu, 75252 Paris Cedex 05, France. E-mail: mathieu.rosenbaum@polytechnique.edu 3University of Tokyo and Japan Science and Technology Agency, Graduate School of Mathematical Sci- ences, University of Tokyo, 3-8-1 Komaba, Meguro-ku, Tokyo 153-8914, Japan. E-mail: nakahiro@ms.u-tokyo.ac.jp We propose a simple continuous time model for modeling the lead-lag effect between two ﬁnancial assets. A two-dimensional process (Xt,Yt) reproduces a lead-lag effect if, for some time shift ϑ ∈ R, the process (Xt,Yt+ϑ) is a semi-martingale with respect to a certain ﬁltration. The value of the time shift ϑ is the lead-lag parameter. Depending on the underlying ﬁltration, the standard no-arbitrage case is obtained for ϑ = 0. We st

### id `W3049511937`

**A Learning System Integrating Temporal Convolution and Deep Learning for Predictive Modeling of Crude Oil Price**

> “© 2020 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.” 1 Tong Niu, et al., A Learning System Integrating Temporal Convolution and Deep Learning for Predictive Modeling of Crude Oil Price Abstract—Accurately crude oil price prediction remains challenging so far. Despite the abundant research achievements of crude oil price prediction, most of them emphasize the linear and deterministic modeling, which cannot adequately capture the complex nonlinear characteristics and uncertainties involved, thus impeding further developments in the field. In this study, a novel learning system with the aim of obtaining deterministic and probabilistic predictions is presented to model the nonlinear dynamics in crude oil price, composed by the modules of recurrence analysis, ou

### id `W4380681488`

**A New Approach to Technical Analysis of Oil Prices**

> Turk. J. Math. Comput. Sci. 15(1)(2023) 145–156 © MatDer DOI : 10.47000/tjmcs.1117784 A New Approach to Technical Analysis of Oil Prices M¨ucahit Akbıyık1,∗ , Seda Yamac¸ Akbıyık2 , ¨Umit Tura3 , Elif Erer4 , Mehtap C ¸alıs¸5 , Ferudun Kaya3 1 Department of Mathematics, Beykent University, Istanbul, Turkey. 2 Department of Computer Engineering, Istanbul Gelisim University, Istanbul, Turkey. 3 Department of Management and Organisation, Bolu Abant Izzet Baysal University, Bolu, Turkey. 4 Independent Researcher, Izmir, Turkey. 5 Independent Researcher, Bolu, Turkey. Received: 17-05-2022 • Accepted: 02-05-2023 Abstract. The aim of this study is to investigate the oil prices, which have crucial impact of an economy, using new ratios called Nickel ratios instead of the golden ratios on technical analysis. The Nickel ratios are developed considering Nickel Fibonacci sequence. This study is the ﬁrst to use Nickel ratios in technical analysis in economics and ﬁnance. In this study, graphs comprising of weekly, daily, 4−hour and 30−minute periods are analyzed using Nickel ratios in Fibonacci r

### id `W2270906211`

**Are the S&P 500 index and crude oil, natural gas and ethanol futures related for intra-day data?**

> Are the S&P 500 Index and Crude Oil, Natural Gas and Ethanol Futures Related for Intra-Day Data? * EI2016-02 Massimiliano Caporin Department of Economics and Management “Marco Fanno” University of Padova, Italy Chia-Lin Chang Department of Applied Economics Department of Finance National Chung Hsing University, Taiwan Michael McAleer Department of Quantitative Finance National Tsing Hua University, Taiwan and Econometric Institute Erasmus School of Economics Erasmus University Rotterdam and Tinbergen Institute, The Netherlands and Department of Quantitative Economics Complutense University of Madrid, Spain Revised: February 2016 * For financial support, the second author wishes to thank the National Science Council, Taiwan, and the third author wishes to acknowledge the Australian Research Council and the National Science Council, Taiwan. 1 Abstract The energy sector is one of the most important in the world, so that time series fluctuations in leading energy sources have been analysed widely . As the leading energy commodities are traded on international stock exchanges, the analysi

### id `W2140456315`

**Following a trend with an exponential moving average: Analytical results for a Gaussian model**

> arXiv:1308.5658v1 [q-fin.ST] 26 Aug 2013 Following a Trend with an Exponential Moving Average: Analytical Results for a Gaussian Model Denis S. Grebenkov Laboratoire de Physique de la Mati` ere Condens´ ee, CNRS – Ecole Polytechnique, 91128 Palaiseau, France Jeremy Serror John Locke Investment, 38 Avenue Franklin Roosevelt, 77210 Fontainebleau-Avon, France Abstract We investigate how price variations of a stock are transformed into proﬁts and losses (P&Ls) of a trend following strategy. In the frame of a G aus- sian model, we derive the probability distribution of P&Ls and analyze it s moments (mean, variance, skewness and kurtosis) and asymptot ic behavior (quantiles). We show that the asymmetry of the distribution (with o ften small losses and less frequent but signiﬁcant proﬁts) is reminiscent to trend following strategies and less dependent on peculiarities of price varia tions. At short times, trend following strategies admit larger losses than o ne may anticipate from standard Gaussian estimates, while smaller losses ar e ensured at longer times. Simple explicit formulas charac

### id `W2278302635`

**Dealing with Stochastic Volatility in Time Series Using the R Package stochvol**

> JSS Journal of Statistical Software February 2016, Volume 69, Issue 5. doi:10.18637/jss.v069.i05 Dealing with Stochastic Volatility in Time Series Using the R Package stochvol Gregor Kastner WU Vienna University of Economics and Business Abstract The R package stochvolprovides a fully Bayesian implementation of heteroskedasticity modeling within the framework of stochastic volatility. It utilizes Markov chain Monte Carlo (MCMC) samplers to conduct inference by obtaining draws from the posterior distribution of parameters and latent variables which can then be used for predicting future volatilities. The package can straightforwardly be employed as a stand-alone tool; moreover, it allows for easy incorporation into other MCMC samplers. The main focus of this paper is to show the functionality ofstochvol. In addition, it provides a brief mathematical description of the model, an overview of the sampling schemes used, and several illustrative examples using exchange rate data. Keywords: Bayesian inference, Markov chain Monte Carlo (MCMC), auxiliary mixture sam- pling, ancillarity-suﬃcie

### id `W4293801774`

**EFFICIENCY OF THE STOCK MARKETS AFTER THE 2008 FINANCIAL CRISIS: EVIDENCE FROM THE FOUR ASIAN DRAGONS**

> Eurasian Journal of Business and Management, 10(2), 2022, 101-115 DOI: 10.15604/ejbm.2022.10.02.002 EURASIAN JOURNAL OF BUSINESS AND MANAGEMENT www.eurasianpublications.com EFFICIENCY OF THE STOCK MARKETS AFTER THE 2008 FINANCIAL CRISIS: EVIDENCE FROM THE FOUR ASIAN DRAGONS Ka Po Kung National University of Singapore, Singapore E-mail: kckung@u.nus.edu Received: May 1, 2022 Accepted: June 24, 2022 Abstract The efficient market hypothesis (EMH) claims that in an efficient market where prices of securities fully reflect their intrinsic values, it is not possible to make excess returns with any investment tools or strategies. A natural question then to ask is: has the EMH claim become obsolete or irrelevant after the 2008 financial crisis? To address this issue, this study employs three popular technical trading rules to investigate, using the 10 -year daily price data after the crisis, t he efficiency of the stock markets of Hong Kong, Korea, Singapore, and Taiwan — jointly known as the four Asian dragons. Our rationale for using these rules is that if they are effective in exploiting 

### id `W4390618228`

**Variance of entropy for testing time-varying regimes with an application to meme stocks**

> Decisions in Economics and Finance (2024) 47:215–258 https://doi.org/10.1007/s10203-023-00427-9 Variance of entropy for testing time-varying regimes with an application to meme stocks Andrey Shternshis 1,3 · Piero Mazzarisi 1,2 Received: 27 February 2023 / Accepted: 7 December 2023 / Published online: 5 January 2024 © The Author(s) 2024 Abstract Shannon entropy is the most common metric for assessing the degree of random- ness of time series in many ﬁelds, ranging from physics and ﬁnance to medicine and biology. Real-world systems are typically non-stationary, leading to entropy val- ues ﬂuctuating over time. This paper proposes a hypothesis testing procedure to test the null hypothesis of constant Shannon entropy in time series data. The alternative hypothesis is a signiﬁcant variation in entropy between successive periods. To this end, we derive an unbiased sample entropy variance, accurate up to the order O(n −4) with n the sample size. To characterize the variance of the sample entropy, we ﬁrst provide explicit formulas for the central moments of both binomial and multinomial dis

### id `W3125574934`

**Technical market indicators: An overview**

> Edinburgh Research Explorer Technical Market Indicators: An Overview Citation for published version: Fang, J, Qin, Y & Jacobsen, B 2014, 'Technical Market Indicators: An Overview' Journal of Behavioral and Experimental Finance, vol. 4, pp. 25-56. DOI: 10.1016/j.jbef.2014.09.001 Digital Object Identifier (DOI): 10.1016/j.jbef.2014.09.001 Link: Link to publication record in Edinburgh Research Explorer Document Version: Peer reviewed version Published In: Journal of Behavioral and Experimental Finance Publisher Rights Statement: © Fang, J., Qin, Y., & Jacobsen, B. (2014). Technical Market Indicators: An Overview. Journal of Behavioral and Experimental Finance. 10.1016/j.jbef.2014.09.001 General rights Copyright for the publications made accessible via the Edinburgh Research Explorer is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that users recognise and abide by the legal requirements associated with these rights. Take down policy The University of Edinburgh has made every reasonable effort to ensure that Edinburgh Rese

### id `W4409842951`

**High-frequency dynamics of the Vietnam stock market**

> VNU Journal of Economics and Business, Vol. 5, No. 2 (2025) 51-59 51 Original Article High-frequency dynamics of the Vietnam stock market Tran Manh Ha*, Tran Ngoc Mai Banking Academy of Vietnam No. 12 Chua Boc Street, Dong Da District, Hanoi, Vietnam Received: March 4, 2025 Revised: April 10, 2025; Accepted: April 25, 2025 Abstract: This study examines the high-frequency dynamics of the VNINDEX by utilizing 1-minute data over a sample of 160,677 observations from February 2022 to February 2025 to assess market efficiency, the volume -price relationship and the intraday volatility pattern. Our findings suggest delayed information diffusion and liquidity constraints, reflecting inefficiencies typical of Vietnam stock markets with retail-heavy participation. This paper offers opportunities for momentum trading and highlights the need to enhance market depth to mitigate speculative spikes, contributing to the understanding of high-frequency behavior in the Vietnam stock market. Keywords: High-frequency data, market efficiency, high frequency trading. 1. Introduction* The VNINDEX, trackin

### id `W2943226912`

**Seasonal anomalies in the market for American depository receipts**

> Seasonal anomalies in the market for American depository receipts Júlio Lobão Faculdade de Economia, Universidade do Porto, Porto, Portugal Abstract Purpose – The literature provides extensive evidence for seasonality in stock market returns, but is almost non-existent concerning the potential seasonality in American depository receipts (ADRs). To ﬁll this gap, this paper aims to examine a number of seasonal effects in the market for ADRs. Design/methodology/approach – The paper examines four ADRs for the period from April 1999 to March 2017 to look for signs of eight important seasonal anomalies. The authors follow the standard methodology of using dummy variables for the time period of interest to capture excess returns. For comparison, the same analysis on two US stock market indices is conducted. Findings – The results show the presence of a highly signiﬁcant pre-holiday effect in all return series, which does not seem to be justiﬁed by risk. Moreover, turn-of-the-month effects, monthly effects and day-of-the-week effects were detected in some of the ADRs. The seasonality pattern

### id `W2291549641`

**Searching for Inefficiencies in Exchange Rate Dynamics**

> Comput Econ (2017) 49:405–432 DOI 10.1007/s10614-016-9567-2 Searching for Inefﬁciencies in Exchange Rate Dynamics Guglielmo Maria Caporale1 · Luis Gil-Alana2 · Alex Plastun3 Accepted: 17 February 2016 / Published online: 27 February 2016 © The Author(s) 2016. This article is published with open access at Springerlink.com Abstract This paper develops a new pair trading method to detect inefﬁciencies in exchange rates movements and arbitrage opportunities using a convergence/divergence indicator (CDI) belonging to the oscillatory class. The proposed technique is applied to 11 exchange rates over the period 2010–2015, and trading rules based on CDI signals are obtained. The CDI indicator is shown to outperform others of the oscillatory class and in some cases (for EURAUD and AUDJPY) to generate proﬁts. The suggested approach is of general interest and can be applied to different ﬁnancial markets and assets. Keywords Pair trading · Oscillator · Trading strategy · Convergence/divergence indicator (CDI) · Exchange rates JEL Classiﬁcation G12 · C63 1 Introduction Pair trading is a technique

### id `W2078705704`

**Applying Approximate Entropy (ApEn) to Speculative Bubble in the Stock Market**

> Munich Personal RePEc Archive Applying approximate entropy (ApEn) to speculative bubble in the stock market Saumitra, Bhaduri Madras School of Economics, Chennai, India 10 April 2012 Online at https://mpra.ub.uni-muenchen.de/38015/ MPRA Paper No. 38015, posted 11 Apr 2012 13:30 UTC A Short Note on Approximate Entropy (ApEn)- a Measure to trace Speculative Bubble in Stock Markets Saumita N Bhaduri1 Abstract The paper introduces an order statistic, Appr oximate Entropy (ApEn) , to investigate the presence of speculative bubbles in the equity market. In contrast to the traditional duration dependence test, the paper using Approximate Entropy examines three major events of stock market crash in US, Japa n, and India. In addi tion, the paper also investigates the 1997 Asian cris is using weekly data from seven major Asian indices which includes Hong Kong, Malaysia, Singapore, Korea, Taiwan, Indonesia and Japan. The evidences presented in this study show that there are strong “tale-tell” signs which point to a substantially lower level of ApEn during these crash events. 1 Professor, Madras

### id `W2142632737`

**Economic significance of commodity return forecasts from the fractionally cointegrated VAR model**

> General Rights Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognize and abide by the legal requirements associated with these rights. • Users may download and print one copy of any publication from the public portal for the purpose of private study or research. • You may not further distribute the material or use it for any profit-making activity or commercial gain • You may freely distribute the URL identifying the publication in the public portal If you believe that this document breaches copyright please contact us providing details, and we will remove access to the work immediately and investigate your claim. If the document is published under a Creative Commons license, this applies instead of the general rights. This coversheet template is made available by AU Library Version 2.0, December 2017 Coversheet This is the accepted manuscript (post-print version) of the article. Contentwise, the accepted manuscript version is i

### id `W4400698552`

**Deep learning systems for forecasting the prices of crude oil and precious metals**

> Deep learning systems for forecasting the prices of crude oil and precious metals Parisa Foroutan1 and Salim Lahmiri1* Abstract Commodity markets, such as crude oil and precious metals, play a strategic role in the economic development of nations, with crude oil prices influencing geopoliti- cal relations and the global economy. Moreover, gold and silver are argued to hedge the stock and cryptocurrency markets during market downsides. Therefore, accu- rate forecasting of crude oil and precious metals prices is critical. Nevertheless, due to the nonlinear nature, substantial fluctuations, and irregular cycles of crude oil and precious metals, predicting their prices is a challenging task. Our study contributes to the commodity market price forecasting literature by implementing and compar- ing advanced deep-learning models. We address this gap by including silver along- side gold in our analysis, offering a more comprehensive understanding of the pre- cious metal markets. This research expands existing knowledge and provides valuable insights into predicting commodity prices. In this 

### id `W2779466657`

**Predicting Future Gold Rates using Machine Learning Approach**

> (IJACSA) International Journal of Advanced Computer Science and Applications, Vol. 8, No. 12, 2017 92 | P a g e www.ijacsa.thesai.org Predicting Future Gold Rates using Machine Learning Approach Iftikhar ul Sami, Khurum Nazir Junejo Graduate School of Science and Engineering Karachi Institute of Economics & Technology Karachi, Pakistan Abstract—Historically, gold was used for supporting trade transactions around the world besides other modes o f payment. Various states maintain ed and enhanced their gold reserves and were recognized as wealthy and progressive states . In present times, precious metals like gold are held with central banks of all countries to guarantee re-payment of foreign debts, and also to control inflation. Moreover, it also reflects the financial strength of the country. Beside s government agencies, various multi - national companies and individuals have also invested in gold reserves. In traditional events of Asian countries , gold is also presented as gifts/souvenirs and in marriages , gold ornaments are presented as Dowry in India, Pakistan and other countrie

### id `W3036413167`

**Does short-term technical trading exist in the Vietnamese stock market?**

> Full Length Article Does short-term technical trading exist in the Vietnamese stock market? Duc Khuong Nguyen a,b, Ahmet Sensoy c,*, Dinh-Tri V o a,d, Hans-J €org von Mettenheim a,e a IPAG Business School, Paris, France b International School, Vietnam National University, Hanoi, Viet Nam c Faculty of Business Administration, Bilkent University, Ankara, Turkey d University of Economics Ho Chi Minh City, Viet Nam e Oxford-Man Institute, University of Oxford, Oxford, United Kingdom Received 15 January 2020; revised 9 April 2020; accepted 28 May 2020 Available online ▪▪▪ Abstract The Vietnamese stock market provides an interesting and enriching test ﬁeld for the application of trading expert systems as its economy is opening up, has high growth rate and may offer risk diversiﬁcation opportunities. This paper examines the question of whether this frontier emerging market offers possibilities for statistical arbitrage through a ﬁnancial expert system. Based on a sample of the most liquid stocks in the VN30 benchmark index, our results indicate that the index itself and some of its componen

### id `W4200212090`

**Gold Price Forecasting Using LSTM, Bi-LSTM and GRU**

> Avrupa Bilim ve Teknoloji Dergisi Sayı 31 (Ek Sayı 1), S. 341-347, Aralık 2021 © Telif hakkı EJOSAT’a aittir Araştırma Makalesi www.ejosat.com ISSN:2148-2683 European Journal of Science and Technology No. 31 (Supp. 1), pp. 341-347, December 2021 Copyright © 2021 EJOSAT Research Article http://dergipark.gov.tr/ejosat 341 Gold Price Forecasting Using LSTM, Bi-LSTM and GRU Mustafa Yurtsever1* 1* Dokuz Eylül Üniversitesi, Departmant of Information Technology, İzmir, Turkey, (ORCID: 0000-0003-2232-0542), mustafa.yurtsever@deu.edu.tr (First received 29 June 2021 and in final form 6 December 2021) (DOI: 10.31590/ejosat.959405) ATIF/REFERENCE: Yurtsever, M. (2021). Gold Price Forecasting Using LSTM, Bi -LSTM and GRU. European Journal of Science and Technology, (31), 341-347. Abstract Due to the multifactorial and non -linear nature of the gold market, it is difficult to predict the gold price. The gold price is affected by many external factors, such as market environment, economic crises, oil price increases, tax advantages and interest rates. Therefore, multivariate models can better predi

### id `W2117019869`

**What good is a volatility model?**

> WHAT GOOD IS A VOLATILITY MODEL?* Robert F. Engle and Andrew J. Patton Department of Finance, NYU Stern School of Business, and Department of Economics, University of California, San Diego, 9500 Gilman Drive, La Jolla, CA 92093 -0508, USA 29 January, 2001. ABSTRACT A volatility model must be able to forecast volatility; this is the central requirement in almost all financial applications. In this paper we outline some stylised facts about volatility that should be incorporated in a model; pronounc ed persistence and mean - reversion, asymmetry such that the sign of an innovation also affects volatility and the possibility of exogenous or pre-determined variables influencing volatility. We use data on the Dow Jones Industrial index to illustrate these stylised facts, and the ability of GARCH-type models to capture these features. We conclude with some challenges for future research in this area. Keywords: volatility modelling, ARCH, GARCH, volatility forecasting. JEL Classification Code : C22 * Please send comments or questions to rengle@stern.nyu.edu. 2 1. INTRODUCTION A volatility m

### id `W3122860764`

**Losing Sleep at the Market: The Daylight Saving Anomaly**

> Losing Sleep at the Market: The Daylight Saving Anomaly By MARK J. KAMSTRA,L ISA A. KRAMER, AND MAURICE D. LEVI* We have all struggled through the day after a poor night’s sleep, weighed down by weariness, ﬁghting lethargy, and perhaps even facing de- spondency. Fortunately, few people suffer from acute sleeping disorders that, according to sleep researchers, can destroy motivation and cause deep depression and even death. 1 Nevertheless, even relatively minor sleep imbalances have been shown to cause errors in judgment, anxi- ety, impatience, less efﬁcient processing of in- formation, and loss of attention. Indeed, it has been argued that an important thread connecting the nuclear accident at Chernobyl, the near meltdown at Three Mile Island, the massive oil spill from the Exxon Valdez, and the explosion of the space shuttle Challenger, is people mak- ing mistakes because of workshift changes and consequent imbalances of sleep. 2 Equally tragic but less publicized consequences of sleep- related errors have resulted from accidents, which each year “cost the United States over $56 bil

### id `W4391216288`

**Deep Transformer-Based Asset Price and Direction Prediction**

> Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000. Digital Object Identifier 10.1 109/ACCESS.2023.0322000 Deep Transformer-based Asset Price and Direction Prediction Batur Gezici 1, (Member, IEEE), and Emre Sefer 1(Member, IEEE) 1Computer Science Department, Ozyegin University, Istanbul, Turkey Corresponding author: Emre Sefer (e-mail: emre.sefer@ozyegin.edu.tr). ABSTRACT The field of algorithmic trading, driven by deep learning methodologies, has garnered substantial attention in recent times. Within this domain, transformers, convolutional neural networks, and patch embedding- based techniques have emerged as popular choices within the computer vision community. Here, inspired by the latest cutting-edge computer vision methodologies and the existing work showing the capability of image-like conversion for time-series datasets, we apply more advanced transformer-based and patch- based approaches for predicting asset prices and directional price movements. The employed transformer models include Vision Transformer (ViT), Data Efficient Image Transformers (DeiT)

### id `W2950144632`

**Testing for jumps in a discretely observed process**

> The Annals of Statistics 2009, V ol. 37, No. 1, 184–222 DOI: 10.1214/07-AOS568 © Institute of Mathematical Statistics, 2009 TESTING FOR JUMPS IN A DISCRETELY OBSERVED PROCESS BY YACINE AÏT-SAHALIA 1 AND JEAN JACOD Princeton University and Université Pierre et Marie Curie We propose a new test to determine whether jumps are present in asset returns or other discretely sampled processes. As the sampling interval tends to 0, our test statistic converges to 1 if there are jumps, and to another deter- ministic and known value (such as 2) if there are no jumps. The test is valid for all Itô semimartingales, depends neither on the law of the process nor on the coefﬁcients of the equation which it solves, does not require a prelim- inary estimation of these coefﬁcients, and when there are jumps the test is applicable whether jumps have ﬁnite or inﬁnite-activity and for an arbitrary Blumenthal–Getoor index. We ﬁnally implement the test on simulations and asset returns data. 1. Introduction. The problem of deciding whether the continuous-time process which models an economic or ﬁnancial time s

### id `W4376129538`

**Using Heatmap Visualization to assess the performance of the DJ30 and NASDAQ100 Indices under diverse VMA trading rules**

> RESEA RCH ARTICL E Using Heatmap Visualization to assess the performance of the DJ30 and NASDAQ100 Indices under diverse VMA trading rules Yuhsin Chen 1 , Paoyu Huang 2 , Min-Yuh Day 3 , Yensen Ni ID 4 *, Mei-Chu Liang 5 1 Department of Accountin g, Chung Yuan Christian Univers ity, Taoyuan, Taiwan, 2 Department of Interna tional Business, Soochow University , Taipei, Taiwan, 3 Graduate Institute of Informatio n Managemen t, National Taipei University, New Taipei, Taiwan, 4 Department of Managemen t Sciences, Tamkang Univers ity, New Taipei, Taiwan, 5 Department of Banking and Finance, Tamkang University, New Taipei, Taiwan * ysniysni @gmail.com Abstract We investigate whether using various VMA trading rules would improve investment perfor- mance due to the flexibility of VMA trading rules and the aid of Heatmap Visualization. Previ- ously, investors frequently chose the best performanc e derived from limited VMA trading rules. However, our new design, which can display all results using Heatmap Visualization, shows that the NASDAQ100 index outperforms the DJ30 index and that weekly 

### id `W4316174806`

**Weighted-indexed semi-Markov model: calibration and application to financial modeling**

> Weighted‑indexed semi‑Markov model: calibration and application to financial modeling Riccardo De Blasis* Introduction The general approach to studying financial time series is mostly based on applying econometric tools in time series analysis, in which the observed price is considered a noisy representation of an unobserved price. This approach is generally referred to as the macro-to-micro approach. However, in recent years, a new strand of literature has emerged. This new area deals with these problems by looking at the opposite perspective called the micro-to-macro approach, which directly models observable quantities and exploits point processes (Fodra and Pham 2015). Among this new area of the literature, one of the first attempts to model financial time series using a semi-Markov chain is from D’Amico and Petroni (2012a), followed by an extension of the model by introducing a memory index (D’Amico and Petroni 2011). Abstract We address the calibration issues of the weighted-indexed semi-Markov chain (WISMC) model applied to high-frequency financial data. Specifically, we propo

### id `W3163252593`

**Technical analysis profitability and Persistence: A discrete false discovery approach on MSCI indices**

> 1 Technical Analysis Profitability and Persistence: A Discrete False Discovery Approach on MSCI Indices Abstract We investigate the performance of more than 21,000 technical trading rules on 12 categorical and country-specific markets over the 2004 -2015 study period. For this purpose, we apply a discrete false discovery rate approach in more than 240,000 hypotheses and examine the profitability, persistence and robustness of technical analysis. In terms of our results, technical analysis has short -term value and its profitability is mainly driven by short-term momentum. Financial stress seems to have a strong negative effect in technical analysis profitability for US markets and a strong positive effect for emerging and other advanced markets. Keywords: False Discovery Rate; Technical Analysis, Trading; Bootstrap/resampling; JEL codes: C12; C15; C53; G11; G15; G17 2 1. Introduction In this study , we re-evaluate the profitability of T echnical Analysis (TA) and we examine its persistence through a novel Discrete False Discovery Rate (DFDR +/-) framework. More specifically, we inves

### id `W1566435334`

**Normalizing the causality between time series**

> PHYSICAL REVIEW E 92, 022126 (2015) Normalizing the causality between time series X. San Liang* Nanjing University of Information Science and Technology (Nanjing Institute of Meteorology), Nanjing 210044, and China Institute for Advanced Study, Central University of Finance and Economics, Beijing 100081, China (Received 18 January 2015; revised manuscript received 31 May 2015; published 17 August 2015) Recently, a rigorous yet concise formula was derived to evaluate information ﬂow, and hence the causality in a quantitative sense, between time series. To assess the importance of a resulting causality, it needs to be normalized. The normalization is achieved through distinguishing a Lyapunov exponent-like, one-dimensional phase-space stretching rate and a noise-to-signal ratio from the rate of information ﬂow in the balance of the marginal entropy evolution of the ﬂow recipient. It is veriﬁed with autoregressive models and applied to a real ﬁnancial analysis problem. An unusually strong one-way causality is identiﬁed from IBM (International Business Machines Corporation) to GE (Genera

### id `W1527151125`

**A test of the adaptive market hypothesis using a time-varying AR model in Japan**

> arXiv:1207.1842v4 [q-fin.ST] 21 Jan 2016 A Test of the Adaptive Market Hypothesis using a Time-Varying AR Model in Japan Akihiko Noda a,b ∗ a Faculty of Economics, Kyoto Sangyo University, Motoyama, K amigamo, Kita-ku, Kyoto 603-8555, Japan b Keio Economic Observatory, Keio University, 2-15-45 Mita, Minato-ku, Tokyo 108-8345, Japan Abstract: This study examines the adaptive market hypothesis (AMH) in Japanese stock markets (TOPIX and TSE2). In particular, we measure th e degree of market eﬃ- ciency by using a time-varying model approach. The empirica l results show that (1) the degree of market eﬃciency changes over time in the two market s, (2) the level of market eﬃciency of the TSE2 is lower than that of the TOPIX in most per iods, and (3) the market eﬃciency of the TOPIX has evolved, but that of the TSE2 has not. We conclude that the results support the AMH for the more qualiﬁed stock m arket in Japan. Keywords: The Adaptive Market Hypothesis; The Eﬃcient Market Hypothe sis; Time- Varying Model Approach; Degree of Market Eﬃciency. JEL Classiﬁcation Numbers: C22; G14. ∗ Correspond

### id `W2136931955`

**Statistical analysis of the overnight and daytime return**

> arXiv:0903.0993v1 [q-fin.ST] 5 Mar 2009 Statistical analysis of the overnight and daytime return Fengzhong Wang,1 Shwu-Jane Shieh, 1, 2 Shlomo Havlin, 1, 3 and H. Eugene Stanley 1 1Center for Polymer Studies and Department of Physics, Boston University, Boston, MA 02215 USA 2Department of International Business, National Cheng-Chi University, Taipei, Taiwan, R.O.C. 3Minerva Center and Department of Physics, Bar-Ilan University, Ramat-Gan 52900, Israel (Dated: 4 March 2009 wshs.tex) Abstract We investigate the two components of the total daily return ( close-to-close), the overnight return (close-to-open) and the daytime return (open-to-close), a s well as the corresponding volatilities of the 2215 NYSE stocks from 1988 to 2007. The tail distribution of the volatility, the long-term memory in the sequence, and the cross-correlation between d iﬀerent returns are analyzed. Our results suggest that: (i) The two component returns and vola tilities have similar features as that of the total return and volatility. The tail distribution fo llows a power law for all volatilities, and long-ter

### id `W2028649666`

**Toward a theory of marginally efficient markets**

> arXiv:cond-mat/9901243v1 [cond-mat.stat-mech] 22 Jan 1999 Toward a Theory of Marginally Eﬃcient Markets ∗ Yi-Cheng Zhang Institut de Physique Th´ eorique, Universit´ e de Fribourg,P´ erolles, Fribourg CH-1700, Switzerland Empirical evidence suggests that even the most competitive markets are not strictly eﬃcient. Price histories can be used to predict near future returns wi th a probability better than random chance. Many markets can be considered as favorable games , in the sense that there is a small probabilistic edge that smart speculators can exploit. We p ropose to identify this probability using conditional entropy concept. A perfect random walk has this entropy maximized, and departure from the maximal value represents a price history’s predictabil ity. We propose that market participants should be divided into two categories: producers and specul ators. The former provides the negative entropy into the price, upon which the latter feed. We show th at the residual negative entropy can never be arbitraged away: inﬁnite arbitrage capital is need ed to make the price a perfect r

