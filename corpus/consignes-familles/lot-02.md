# Consigne — le mécanisme et l'effet annoncé de 30 papiers (lot 2 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-02.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W4292756288`

**Realised volatility and industry momentum returns**

> ARTICLE Realised volatility and industry momentum returns Xiaoyue Chen 1 ✉, Bin Li 1 & Andrew C. Worthington 1 Motivated by the importance of industry volatility and the pro ﬁtability of industry momentum strategy, this study investigates the relationship between realised volatility and industry momentum returns. The analysis uses daily return data for 48 US industries from July 1969 to June 2021 to calculate realised volatility and to gauge the raw return effect on short- and medium-horizon double-sort momentum-trading strategies. The ﬁndings show that past volatility positively relates to industry momentum and that this relationship is stronger after controlling for common risk factors (market, size, value, investment, and pro ﬁtability). Decomposing the realised total volatility into idiosyncratic and systematic components, this study reveals that both decomposed components are positively related to industry momentum returns. The ﬁndings are robust to alternative measures of volatility. https://doi.org/10.1057/s41599-022-01309-y OPEN 1 Department of Accounting, Finance and Economi

### id `W3028843255`

**Return connectedness across asset classes around the COVID-19 outbreak**

> Return connectedness across asset classes around the COVID-19 outbreak Elie Bouri †, Oguzhan Cepni ‡, David Gabauer §, and Rangan Gupta Λ †Holy Spirit University of Kaslik (USEK), USEK Business School, Jounieh, Lebanon. ‡Central Bank of the Republic of Turkey, Ankara, Turkey. §Software Competence Center Hagenberg, Data Analysis Systems, Softwarepark 21, 4232 Hagenberg, Austria. Λ Department of Economics, University of Pretoria, Pretoria, 0002, South Africa. ∗Corresponding Author. Abstract In this paper, we show evidence of a dramatic change in the structure and time-varying patterns of return connectedness across various assets (gold, crude oil, world equities, currencies, and bonds) around the COVID-19 outbreak. Using the TVP-VAR connectedness approach, the results show that the dynamic total connectedness across the ﬁve assets was moderate and quite stable until early 2020. After that, the total connectedness spikes and the structure of the network of connectedness alters, which concurs with the COVID-19 outbreak. The equity and USD indices are the primary transmitters of shocks be

### id `W3026661449`

**Searching for safe-haven assets during the COVID-19 pandemic**

> SEARCHING FOR SAFE-HA VEN ASSETS DURING THE COVID-19 PANDEMIC QIANG JI1, DAYONG ZHANG2, YUQIAN ZHAO 3 1Center for Energy and Environmental Policy Research, Institutes of Science and Development, Chinese Academy of Sciences 2Research Institute of Economics and Management, Southwestern University of Finance and Economics, China 3Essex Business School, University of Essex, UK Abstract. The ongoing COVID-19 pandemic has shaken the global ﬁnancial system and caused great turmoil. Facing unprecedented risks in the markets, people have in- creasing needs to ﬁnd a safe haven for their investments. Given that the nature of this crisis is a combination of multiple problems, it is substantially diﬀerent from all other ﬁnancial crises known to us. It is therefore urgent to re-evaluate the safe-haven role of some traditional asset types, namely, gold, cryptocurrency, foreign exchange and com- modities. This paper introduces a sequential monitoring procedure to detect changes in the left-quantiles of asset returns, and to assess whether a tail change in the eq- uity index can be oﬀset by introduci

### id `W2053795282`

**Short-Term Momentum Effect: a Case of Middle East Stock Markets**

> Copyright © 2015 The Authors. Published by VGTU Press. This is an open­access article distributed under the terms of the Creative Commons Attribution­NonCommercial 4.0 (CC BY ­NC 4.0) license, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited. The material cannot be used for commercial purposes. Verslas: Teorija ir prakTika / Business: Theory and pracTice issn 1648-0627 / eissn 1822-4202 http://www.btp.vgtu.lt 2015 16(1): 104–112 doi:10.3846/btp.2015.438 short-term momentum effeCt: a Case of middle east stoCK marKets abdullah ejaz1, petr polaK2 School of Business and Economics, Universiti Brunei Darussalam, Gadong, Brunei E­mails: 112h1301@ubd.edu.bn; 2petr.polak@ubd.edu.bn (corresponding author) Received 01 March 2013; accepted 15 June 2014 Abstract. The objective of this paper is to find short­term momentum effect in stock markets of the Middle East and to examine whether short­term momentum profits can be explained by risk­based CAPM model. Seven major stock markets from the Middle East were selected.

### id `W3121081402`

**Speculation and lottery-like demand in cryptocurrency markets**

> Speculation and lottery-like demand in cryptocurrency markets Klaus Grobys a,⇑,1, Juha Junttila b,1 a University of Vaasa, School of Accounting and Finance, P.O. Box 700, FI-65101 Vaasa, Finland b University of Jyväskylä, School of Business and Economics, P.O. Box 35, FI-40014 Jyväskylä, Finland article info Article history: Received 18 May 2020 Accepted 6 January 2021 Available online 9 January 2021 JEL classiﬁcation: G01 G12 G14 Keywords: MAX Lottery-like demand Cryptocurrency Financial technology Gambling abstract This is the ﬁrst paper that explores lottery-like demand in cryptocurrency markets. Since recent research provides evidence that cryptocurrency returns appear to be short-memory processes, we modify Bali, Cakici and Whitelaw’s (2011) and Bali, Brown, Murray, and Tang’s (2017) MAX measure and employ a weekly forecast horizon and daily log-returns from the previous week to calculate the metric for our portfolio sorts. From an econometric point of view, this study proposes statistical tests that are robust to unknown dynamic dependency structures in the cryptocurrency data.

### id `W2604890964`

**The Momentum & Trend-Reversal as Temporal Market Anomalies**

> International Journal of Economics and Finance; V ol. 9, No. 5; 2017 ISSN 1916 -971X E-ISSN 1916 -9728 Published by Canadian Center of Science and Education 1 The Momentum & Trend-Reversal as Temporal Market Anomalies Vasiliki A. Basdekidou1 1 SRFA Aristotle University of Thessaloniki, Greece Correspondence: Vasiliki A. Basdekidou, Special Research Fund Account (ELKE), Aristotle University of Thessaloniki, Greece. Tel: 30-697-277-5475. E-mail: Vasiliki.Basdekidou@gmail.com Received: January 6, 2017 Accepted: March 8, 2017 Online Published: April 5, 2017 doi:10.5539/ijef.v9n5p1 URL: https://doi.org/10.5539/ijef.v9n5p1 Abstract The main goal of this paper is to introduce and discuss the temporal dimension and the subsequent (time-series) functionalities of two well-known technical market anomalies - the momentum anomaly and the trend-reversal anomaly. Our approach not only challenging the efficient-market hypothesis but also has a temporal dimension because it uses the “psychological time” at the beginning of a move, as a parameter in overnight post-market asset position trading strate

### id `W3037145595`

**The impact of Covid-19 on G7 stock markets volatility: Evidence from a ST-HAR model**

> Izzeldin, Marwan, Murado□lu, Gülnur, Pappas, Vasileios and Sivaprasad, Sheeja (2021) The impact of Covid-19 on G7 stock markets volatility: Evidence from a ST-HAR model. International Review of Financial Analysis, 74 . ISSN 1057-5219. Kent Academic Repository Downloaded from https://kar.kent.ac.uk/85238/ The University of Kent's Academic Repository KAR The version of record is available from https://doi.org/10.1016/j.irfa.2021.101671 This document version Author's Accepted Manuscript DOI for this version Licence for this version CC BY-NC-ND (Attribution-NonCommercial-NoDerivatives) Additional information Versions of research works Versions of Record If this version is the version of record, it is the same as the published version available on the publisher's web site. Cite as the published version. Author Accepted Manuscripts If this document is identified as the Author Accepted Manuscript it is the version after peer review but before type setting, copy editing or publisher branding. Cite as Surname, Initial. (Year) 'Title of article'. To be published in Title of Journal , Volume an

### id `W4381662042`

**The lead–lag relation between VIX futures and SPX futures**

> Journal of Financial Markets 67 (2024) 100851 Available online 21 June 2023 1386-4181/© 2023 The Author(s). Published by Elsevier B.V. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/). Contents lists available at ScienceDirect Journal of Financial Markets journal homepage: www.elsevier.com/locate/finmar The lead–lag relation between VIX futures and SPX futures✩ Christine Bangsgaard a, Thomas Kokholma,b,∗ a Aarhus BSS, Aarhus University, Department of Economics and Business Economics, Denmark b Danish Finance Institute, Denmark A R T I C L E I N F O JEL classification: G11 G12 G13 G14 G23 Keywords: Lead–lag relation High-frequency data Cross-correlation Price discovery VIX futures hedging Cross-market activity A B S T R A C T We analyze the lead–lag relation between VIX futures and SPX futures. The two futures markets are weakly connected when market volatility is low. By contrast, when volatility is high, their prices are highly negatively correlated, with VIX futures leading SPX futures. However, the tightness of the lead–lag relat

### id `W2095808707`

**The day of the week effect on stock market volatility**

> JOURNAL OF ECONOMICS AND FINANCE • Volume 25 • Number 2 • Summer 2001 181 The Day of the Week Effect on Stock Market Volatility Hakan Berument and Halil Kiymaz * Abstract This study tests the presence of the day of the week effect on stock market volatility by using the S&P 500 market index during the period of January 1973 and October 1997. The findings show that the day of the week effect is present in both volatility and return equations. While the highest and lowest returns are observed on Wednesday and Monday, the highest and the lowest volatility are observed on Friday and Wednesday, respectively. Further investigation of sub-periods reinforces our findings that the volatility pattern across the days of the week is statistically different. ( JEL G10, G12, C22) Introduction The presence of calendar anomalies has been documented extensively for the last two decades in financial markets. The most common ones are the January Effect and the Day of the Week Effect. The day of the week patterns have been investigated extensively in different markets. Studies (Cross 1973; French 1980; 

### id `W2990924896`

**Intraday time‐series momentum: Evidence from China**

> Intraday Time-series Momentum: Evidence from China Jin, M., Kearney, F., Li, Y., & Yang, Y. C. (2019). Intraday Time-series Momentum: Evidence from China. Journal of Futures Markets, 40(4), 632. Advance online publication. https://doi.org/10.1002/fut.22084 Published in: Journal of Futures Markets Document Version: Peer reviewed version Queen's University Belfast - Research Portal: Link to publication record in Queen's University Belfast Research Portal Publisher rights © 2019 Wiley Periodicals, Inc. This work is made available online in accordance with the publisher’s policies. Please refer to any applicable terms of use of the publisher. General rights Copyright for the publications made accessible via the Queen's University Belfast Research Portal is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that users recognise and abide by the legal requirements associated with these rights. Take down policy The Research Portal is Queen's institutional repository that provides access to Queen's research output. Every effort has

### id `W1988283816`

**Stock market return and volatility: day-of-the-week effect**

> Stock market return and volatility: day-of-the-week effect M. Hakan Berument & Nukhet Dogan Published online: 9 January 2010 # Springer Science+Business Media, LLC 2010 Abstract This paper examines the stock market returns and volatility relationship using US daily returns from May 26, 1952 to September 29, 2006. The empirical evidence reported here does not support the proposition that the return-volatility relationship is present and the same for each day of the week. Keywords Day-of-the-Week Effect . Return-V olatility Relation. Time V arying Risk Premia. EGARCH JEL Classification G10 . G12 . C22 1 Introduction Finding any systematic pattern in the behavior of stock market returns is an important research topic in financial economics. Two of the most commonly investigated patterns are (1) the relationship between stock market returns and stock market volatility (or variance), and (2) the difference in expected returns across the days of the week. While there does not seem to be universal agreement on the issue, the positive relationship between stock market returns and volatility 

### id `W2021525848`

**On Asymmetry, Holiday and Day-of-the-week Effects in Volatility of Daily Stock Returns: The Case of Japan**

> J. Japan Statist. Soc. Vol. 34 No. 2 2004 129–152 ON ASYMMETRY, HOLIDAY AND DAY-OF-THE-WEEK EFFECTS IN VOLATILITY OF DAILY STOCK RETURNS: THE CASE OF JAPAN Hisashi Tanizaki* In this paper, we investigate volatility in Japanese stock returns, using the state- space model. The daily data of Nikkei 225 stock average from January 4, 1985 to June 10, 2004are utilized and the stochastic volatility model is assumed for the noise component. We examine whether there are asymmetry, holiday and day-of-the-week eﬀects in volatility. Moreover, we see whether U.S. stock price change inﬂuences the volatility in Japanese stock price, which is called U.S. stock price change eﬀect in this paper (note that this is the asymmetry eﬀect caused by U.S. stock market). It is also examined whether we have volatility transmission from U.S. to Japan. As a result, we empirically ﬁnd that the asymmetry, holiday, U.S. stock price volatility transmission and Tuesday eﬀects strongly inﬂuence the volatility in Japanese stock returns. Moreover, it is shown that both volatility and level in Japanese stock returns depen

### id `W2285598489`

**The Monthly Effect and the Day of the Week Effect in the American Stock Market**

> http://ijfr.sciedupress.com International Journal of Financial Research V ol. 7, No. 2; 2016 Published by Sciedu Press 1 1 ISSN 1923-4023 E-ISSN 1923-4031 The Monthly Effect and the Day of the Week Effect in the American Stock Market Bing Xiao1 1 Management Science, Université d’Auvergne, CRCGM EA 38 49 Université d’Auvergne, Auvergne, France Correspondence: Bing Xiao, PhD in Management Science, Université d’Auvergne, CRCGM EA 38 49 Université d’Auvergne, Auvergne, France. Received: January 2, 2016 Accepted: January 17, 201 6 Online Pu blished: February 17, 2016 doi:10.5430/ijfr.v7n2p11 URL: http://dx.doi.org/10.5430/ijfr.v7n2p11 Abstract This paper examine the recent evolution of seasonal anomalies in the American stock market. This study was based on daily data from the Russell 3000 index over the 2000-2015 period. We examine the recent evolution of the week effect and the monthly effect, and we investigate seasonal patterns in economically favourable times and unfavourable times. We use a UCM model and ARCH model. We find evidence for fixed seasonality with a positive and signific

### id `W2081845631`

**Realized range-based estimation of integrated variance**

> Realized range-based estimation of integrated variance ∗ Kim Christensen † Mark Podolskij ‡ November 7, 2006 Abstract We provide a set of probabilistic laws for estimating the qua dratic variation of continuous semimartingales with realized range-based variance - a sta tistic that replaces every squared return of realized variance with a normalized squared range. If the entire sample path of the process is available, and under a set of weak conditions, our statistic is consistent and has a mixed Gaussian limit, whose precision is ﬁve times greater than that of real ized variance. In practice, of course, inference is drawn from discrete data and true ranges are uno bserved, leading to downward bias. We solve this problem to get a consistent, mixed normal estim ator, irrespective of non-trading eﬀects. This estimator has varying degrees of eﬃciency over realized variance, depending on how many observations that are used to construct the high-lo w. The methodology is applied to TAQ data and compared with realized variance. Our ﬁndings su ggest that the empirical path of quadratic variat

### id `W4205198170`

**A Review of the Fractal Market Hypothesis for Trading and Market Price Prediction**

> Technological University Dublin Technological University Dublin ARROW@TU Dublin ARROW@TU Dublin Articles Dublin Energy Lab 2021 A Review of the Fractal Market Hypothesis for Trading and Market A Review of the Fractal Market Hypothesis for Trading and Market Price Prediction Price Prediction Jonathan Blackledge Technological University Dublin, jonathan.blackledge@tudublin.ie Marc Lamphiere Technological University Dublin, marc.lamphiere@gmail.com Follow this and additional works at: https://arrow.tudublin.ie/dubenart Part of the Mathematics Commons Recommended Citation Recommended Citation Blackledge J, Lamphiere M. A Review of the Fractal Market Hypothesis for Trading and Market Price Prediction. Mathematics. 2022; 10(1):117. DOI: 10.3390/math10010117 This Article is brought to you for free and open access by the Dublin Energy Lab at ARROW@TU Dublin. It has been accepted for inclusion in Articles by an authorized administrator of ARROW@TU Dublin. For more information, please contact arrow.admin@tudublin.ie, aisling.coyne@tudublin.ie, gerard.connolly@tudublin.ie. This work is licensed

### id `W2136429322`

**DAY OF THE WEEK EFFECT IN CENTRAL EUROPEAN STOCK MARKETS**

> Munich Personal RePEc Archive Day of the week eﬀect in central European stock markets Stavarek, Daniel and Heryan, Tomas Silesian University - School of Business Administration 28 April 2012 Online at https://mpra.ub.uni-muenchen.de/38431/ MPRA Paper No. 38431, posted 30 Apr 2012 01:27 UTC 1 Day of the Week Effect in Central European Stock Markets Daniel Stavárek, Tomáš Heryán Silesian University in Opava School of Business Administration in Karviná Department of Finance Univerzitní nám. 1934/3 733 40 Karviná Czech Republic E-mail: stavarek@opf.slu.cz E-mail: heryan@opf.slu.cz Abstract The aim of the paper is to estimate the day of the week effect in the stock markets in the Czech Republic, Hungary and Poland over the period 2006 – 2012. The entire period of estimation is divided to six sub-periods capturing individual phases of the financial and economic crisis. We separately estimate a modified GARCH-M (1,1) model for each country and each sub- period using daily returns of the major national stock market indices. The day of the week effect is measured for both daily returns and co

### id `W2096393777`

**Day of the Week Effect of Stock Returns: Empirical Evidence from Colombo Stock Exchange**

> 16 Day of the Week Effect of Stock Returns: Empirical Evidence from Colombo Stock Exchange S C THUSHARA Lecturer, Department of Commerce and Financial Management, Faculty of Commerce and Management Studies,Univeristy of Kelaniya, Kelaniya, Sri Lanka scthushara@kln.ac.lk PRABATH PERERA Assistant Lecturer, Department of Accountancy, Faculty of Commerce and Management Studies,Univeristy of Kelaniya, Kelaniya, Sri Lanka prabathperera@yahoo.com Abstract Many empirical studies have been carried out both in the developed and developing economies to test the presence of anomalies in stock returns and volatility. The most commonly tested seasonal anomalies are day of the week effect, month of the year effect, holiday effect, Monday effect and Friday effect. Previous studies strongly support the existence of seasonal anomalies. Existence of seasonal anomalies let the investors to earn abnormal returns by trading on past information. This study attempts to test whether the day of the week effect is present in the stock returns of the Colombo Stock Exchange. For this purpose, stock returns based

### id `W2304447118`

**Exponential GARCH Modeling With Realized Measures of Volatility**

> General Rights Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognize and abide by the legal requirements associated with these rights. • Users may download and print one copy of any publication from the public portal for the purpose of private study or research. • You may not further distribute the material or use it for any profit-making activity or commercial gain • You may freely distribute the URL identifying the publication in the public portal If you believe that this document breaches copyright please contact us providing details, and we will remove access to the work immediately and investigate your claim. This coversheet template is made available by AU Library Version 1.0, October 2016 Coversheet This is the accepted manuscript (post-print version) of the article. Contentwise, the post-print version is identical to the final published version, but there may be differences in typography and layout. How to cite this publ

### id `W4409085085`

**Market time-series reversal: evidence from China’s market**

> This is an Open Access article distributed under the terms of the Creative Commons Attribution License (http://creativecommons.org/ licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited. Copyright © 2025 The Author(s). Published by Vilnius Gediminas Technical University TECHNOLOGICAL and ECONOMIC DEVELOPMENT of ECONOMY ISSN: 2029-4913 / eISSN: 2029-4921 MARKET TIME -SERIES REVERSAL: EVIDENCE FROM CHINA’S MARKET Yun XIANG1, 2, Longang LUO3, Xisheng YU4 1 School of Finance, China Big Data Laboratory On Financial Security and Behavior, Southwestern University of Finance and Economics, Sichuan, Chengdu, China 2 China Engineering Research Center of Intelligent Finance, Ministry of Education, Chengdu, China 3 School of Management, University Sains Malaysia, Penang, Malaysia 4 School of Mathematics, Southwestern University of Finance and Economics, Sichuan, Chengdu, China Article History: Abstract. Upon high-frequency data of China Securities Index 300 (CSI 300) exchange-traded fund and index fut

### id `W2017266726`

**Day-of-the-Week-Effects in West African Regional Stock Market**

> www.ccsenet.org/ijef International Journal of Ec onomics and Finance V ol. 2, No. 4; November 2010 Published by Canadian Center of Science and Education 167 Day-of-the-Week-Effects in West African Regional Stock Market Aboudou Maman Tachiwou (Corresponding author) S/C MAMAN - WATARA Gaouzou, Cabinet Maitre AYEV A 05. BP. 769 Lomé Agbalépédogan. LOME – TOGO E-mail: amtwatara@hotmail.com Abstract This paper provides the first evidence for the presence of the day of the week effects in West African regional stock market in the sample for the period September 1998 to December 2007.The observed daily patterns exhibiting lower daily means and lower standard deviations. In local currency terms, a pattern of lower returns around the middle of the week, Tuesday and then Wednesday; and a higher pa ttern towards the end of the week, Thursday and then Friday, are observed. The results have useful implications fo r international portfolio diversification. This may be of particular interest for the global investor. Keywords: Day of the week effects, West African regional markets, Brvm 1. Introduct

### id `W263913495`

**Gold, Oil, and Stocks: Dynamic Correlations**

> econstor www.econstor.eu Der Open-Access-Publikationsserver der ZBW – Leibniz-Informationszentrum Wirtschaft The Open Access Publication Server of the ZBW – Leibniz Information Centre for Economics Standard-Nutzungsbedingungen: Die Dokumente auf EconStor dürfen zu eigenen wissenschaftlichen Zwecken und zum Privatgebrauch gespeichert und kopiert werden. Sie dürfen die Dokumente nicht für öffentliche oder kommerzielle Zwecke vervielfältigen, öffentlich ausstellen, öffentlich zugänglich machen, vertreiben oder anderweitig nutzen. Sofern die Verfasser die Dokumente unter Open-Content-Lizenzen (insbesondere CC-Lizenzen) zur Verfügung gestellt haben sollten, gelten abweichend von diesen Nutzungsbedingungen die in der dort genannten Lizenz gewährten Nutzungsrechte. Terms of use: Documents in EconStor may be saved and copied for your personal and scholarly purposes. You are not to copy documents for public or commercial purposes, to exhibit the documents publicly, to make them publicly available on the internet, or to distribute or otherwise use the documents in public. If the documents have

### id `W2132987867`

**Fractal Markets Hypothesis and the Global Financial Crisis: Wavelet Power Evidence**

> Fractal Markets Hypothesis and the Global Financial Crisis: Wavelet Power Evidence Ladislav Kristoufek1,2 1Institute of Economic Studies, Faculty of Social Sciences, Charles University in Prague, Opletalova 26, 110 00, Prague, Czech Republic, EU,2Institute of Information Theory and Automation, Academy of Sciences of the Czech Republic, Pod Vodarenskou vezi 4, 182 08, Prague, Czech Republic, EU. We analyze whether the prediction of the fractal markets hypothesis about a dominance of specific investment horizons during turbulent times holds. To do so, we utilize the continuous wavelet transform analysis and obtained wavelet power spectra which give the crucial information about the variance distribution across scales and its evolution in time. We show that the most turbulent times of the Global Financial Crisis can be very well characterized by the dominance of short investment horizons which is in hand with the assertions of the fractal markets hypothesis. C ritical events and turbulences on the financial markets have always attracted attention of financial researchers as these are th

### id `W2132696906`

**On covariation estimation for multivariate continuous Itô semimartingales with noise in non-synchronous observation schemes**

> On covariation estimation for multivariate continuous Itˆo semimartingales with noise in non-synchronous observation schemes Kim Christensen ∗ Mark Podolskij † Mathias Vetter ‡ March, 2013 Abstract This paper presents a Hayashi-Yoshida type estimator for the cov ariation matrix of continuous Itˆ o semi- martingales observed with noise. The coordinates of the multivariat e process are assumed to be observed at highly frequent non-synchronous points. The estimator of the co variation matrix is designed via a certain combination of the local averages and the Hayashi-Yoshida estimat or. Our method does not require any synchronization of the observation scheme (as e.g. previous tick m ethod or refreshing time method) and it is robust to some dependence structure of the noise process. We s how the associated central limit theorem for the proposed estimator and provide a feasible asymptotic result. O ur proofs are based on a blocking technique and a stable convergence theorem for semimartingales. Finally, we s how simulation results for the proposed estimator to illustrate its ﬁnite sample 

### id `W2149603780`

**On forecasting daily stock volatility: The role of intraday information and market conditions**

> Lancaster University Management School Working Paper 2008/006 On Forecasting Daily Stock Volatility: the Role of Intraday Information and Market Conditions Ana-Maria Fuertes, Marwan Izzeldin and Elena Kalotychou The Department of Economics Lancaster University Management School Lancaster LA1 4YX UK © Ana-Maria Fuertes, Marwan Izzeldin and Elena Kalotychou All rights reserved. Short sections of text, not to exceed two paragraphs, may be quoted without explicit permission, provided that full acknowledgement is given. The LUMS Working Papers series can be accessed at http://www.lums.lancs.ac.uk/publications/ LUMS home page: http://www.lums.lancs.ac.uk/ On F orecasting Daily Stock V olatility: the Role of Intraday Information and Market Conditions Ana-Maria F uertesa;, Marwan Izzeldinb, Elena Kalotychoua aFaculty of Finance, Cass Business School bDepartment of Economics, Lancaster University Management School First draft - October 2007. This version - April 2008. Abstract Several recent studies advocate the use of nonparametric estimators of daily price vari- ability that exploit intrad

### id `W2952970437`

**Modeling and forecasting time series of precious metals: a new approach to multifractal data**

> R E S E A R C H Open Access Modeling and forecasting time series of precious metals: a new approach to multifractal data Emrah Oral 1* and Gazanfer Unal 2 * Correspondence: emrahoral@ gmail.com 1Faculty of Economy and Administrative Sciences, Istanbul Aydin University, Istanbul, Turkey Full list of author information is available at the end of the article Abstract We introduce a novel approach to multifractal data in order to achieve transcended modeling and forecasting performances by extracting time series out of local Hurst exponent calculations at a specified scale. First, the long range and co-movement dependencies of the time series are scrutinized on time-frequency space using multiple wavelet coherence analysis. Then, the multifractal behaviors of the series are verified by multifractal de-trended fluctuation analysis and its local Hurst exponents are calculated. Additionally, root mean squares of residuals at the specified scale are procured from an intermediate step during local Hurst exponent calculations. These internally calculated series have been used to estimate the p

### id `W3026224604`

**On realized volatility of crude oil futures markets: Forecasting with exogenous predictors under structural breaks**

> On realized volatility of crude oil futures markets: Forecasting with exogenous predictors under structural breaks Luo, J., Ji, Q., Klein, T., Todorova, N., & Zhang, D. (2020). On realized volatility of crude oil futures markets: Forecasting with exogenous predictors under structural breaks. Energy Economics. https://doi.org/10.1016/j.eneco.2020.104781 Published in: Energy Economics Document Version: Peer reviewed version Queen's University Belfast - Research Portal: Link to publication record in Queen's University Belfast Research Portal Publisher rights Copyright 2020 Elsevier. This manuscript is distributed under a Creative Commons Attribution-NonCommercial-NoDerivs License (https://creativecommons.org/licenses/by-nc-nd/4.0/), which permits distribution and reproduction for non-commercial purposes, provided the author and source are cited. General rights Copyright for the publications made accessible via the Queen's University Belfast Research Portal is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that users recogn

### id `W2786045909`

**PROFITABILITY OF TECHNICAL TRADING RULES IN THE BRAZILIAN STOCK MARKET**

> Revista Evidenciação Contábil & Finanças, ISSN 2318-1001, João Pessoa, v.6, n.2, p.133-150, mai./ago. 2018. 133 REVISTA EVIDENCIAÇÃO CONTÁBIL & FINANÇAS João Pessoa, v.6, n.2, p.133-150, mai./ago. 2018. ISSN 2318-1001 DOI:10.18405/recfin20180208 Available at: http://periodicos.ufpb.br/ojs2/index.php/recfin PROFITABILITY OF TECHNICAL TRADING RULES IN THE BRAZILIAN STOCK MARKET1 Jose Luis Miralles-Quiros2 Ph.D in Economics from Universidad de Extremadura Professor at Universidad de Extremadura miralles@unex.es http://orcid.org/0000-0002-6591-1783 Maria del Mar Miralles-Quiros Ph.D in Economics from Universidad de Extremadura Professor at Universidad de Extremadura marmiralles@unex.es http://orcid.org/0000-0003-0255-2661 Luis Miguel Valente Gonçalves Ph.D student at Universidad de Extremadura lvalente@alumnos.unex.es https://orcid.org/0000-0001-6103-7251 ABSTRACT Objective: The objective of this paper has been to analyze different trading strategies for the Brazil- ian stock market. This analysis is focused on the comparison and combination of different active rules against the passive 

### id `W3034373639`

**Trends, reversion, and critical phenomena in financial markets**

> Trends, Reversion, and Critical Phenomena in Financial Markets Christof Schmidhuber Zurich University of Applied Sciences School of Engineering, Technikumstrasse 9 CH-8401 Winterthur, Switzerland christof@schmidhuber.ch December 14, 2020 arXiv:2006.07847v4 [q-fin.ST] 11 Dec 2020 Abstract Financial markets across all asset classes are known to exhibit trends, which have been exploited by traders for decades. However, a closer look at the data reveals that those trends tend to revert when they become too strong. Here, we empirically measure the interplay between trends and reversion in detail, based on 30 years of daily futures prices for equity indices, interest rates, currencies and commodities. We ﬁnd that trends tend to revert before they become statistically signiﬁcant. Our key observation is that tomorrow’s expected return follows a cubic polynomial of to- day’s trend strength. The positive linear term of this polynomial represents trend persistence, while its negative cubic term represents trend reversal. Their precise co- eﬃcients determine the critical trend strength, beyond w

### id `W3122463731`

**Nonlinear Features of Realized FX Volatility**

> TSpace Research Repository tspace.library.utoronto.ca Nonlinear Features of Realized FX Volatility John M. Maheu, Thomas H. McCurdy Version Post-print/ accepted manuscript Citation (published version) Maheu, J. M., & McCurdy, T. H. (2002). Nonlinear features of realized FX volatility. Review of Economics and Statistics, 84(4), 668-681. https://doi.org/10.1162/003465302760556486 Publisher’s Statement The final publication is available at MIT Press through https://doi.org/10.1162/003465302760556486. How to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page. This article was made openly accessible by U of T Faculty. Please tell us how this access benefits you. Your story matters. Montréal Juin 2001 Série Scientifique Scientific Series 2001s-42 N

### id `W4213278807`

**Modeling and Forecasting Commodity Futures Prices: Decomposition Approach**

> Received January 27, 2022, accepted February 8, 2022, date of publication February 17, 2022, date of current version March 16, 2022. Digital Object Identifier 10.1 109/ACCESS.2022.3152694 Modeling and Forecasting Commodity Futures Prices: Decomposition Approach EMMANUEL ANTWI 1, EMMANUEL NUMAPAU GYAMFI 2, KWABENA A. KYEI 1, RYAN GILL 3, AND ANOKYE MOHAMMED ADAM 4 1Department of Statistics, University of V enda, Thohoyandou 0950, South Africa 2Department of Finance and Accounting, Ghana Institute of Management and Public Administration, Accra, Ghana 3Department of Mathematics, University of Louisville, Louisville, KY 40292, USA 4Department of Finance, University of Cape Coast, Cape Coast, Ghana Corresponding author: Emmanuel Antwi (antwiemmanuel432@gmail.com) This work was supported in part by the University of V enda under Grant SMNS/18/STA/90. ABSTRACT Price instability is a paramount concern since commodity prices are associated with the livelihood and the economy of a nation as a whole; any extraordinary price ﬂuctuation in the futures market shows that forecasts in commodities is

