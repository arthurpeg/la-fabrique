# Consigne de triage — papiers moissonnés

Tu rends **un verdict par papier** : ce papier est-il implémentable comme signal
sur **notre univers**, et sur rien d'autre ?

## Notre univers, qui est la seule chose qui compte ici

- **9 contrats à terme** : NQ, ES, YM (indices actions US), GC (or), CL (pétrole),
  6E, 6B, 6J, 6A (devises).
- **Barres d'une minute, OHLCV seulement** : ouverture, haut, bas, clôture,
  volume. **Rien d'autre.** Pas de carnet d'ordres, pas de données d'options,
  pas de fondamentaux, pas de positions de traders, pas de nouvelles.
- **Horizon intrajournalier**, jusqu'à quelques jours.
- Historique 2016 → 2023 pour la recherche.

## L'échelle, et elle a trois crans

| Verdict | Quand |
|---|---|
| `oui` | la recette du papier se calcule **entièrement** sur nos 9 contrats en OHLCV |
| `partiel` | l'idée transfère mais il manque quelque chose — un autre
univers, une donnée partiellement absente, un horizon à adapter |
| `non` | infaisable chez nous : donnée absente, univers incompatible
(actions individuelles, obligations, crypto), ou ce n'est pas un signal de prix |

**Sois franc sur `non`.** Un papier d'économie, de politique monétaire, de
comportement du consommateur, de régulation, de macro : c'est `non`, sans
hésiter. Le moissonneur ratisse large **exprès** et n'a jamais prétendu juger.

**Et sois franc sur `oui`.** Un `non` promu `oui` coûte un papier lu, une fiche
écrite et un signal codé pour rien. Un `oui` manqué coûte un papier de moins,
et ça se rattrape.

## Ce que tu rends

**Un seul tableau JSON**, rien avant, rien après :

```json
[
  {"id": "<l'id donné>", "verdict": "oui|partiel|non", "raison": "<une phrase>"},
  ...
]
```

Une ligne par papier, **dans l'ordre donné**, aucune omise. La `raison` dit ce
qui décide — la donnée manquante, l'univers incompatible, ou ce qui rend la
recette calculable chez nous.

---

## LES PAPIERS — lot 4 sur 4

### id `15a389b0-f0cf-4163-9bf0-8c25a40b3778`

**Scaling properties of foreign exchange volatility** — Ramazan Gençay, Faruk Selçuk∥, Brandon Whitcher, 2001

> Physica A 289 (2001) 249{266 www.elsevier.com/locate/physa Scaling properties of foreign exchange volatility Ramazan Gencaya;b; , Faruk Selcukb, Brandon Whitcherc aDepartment of Economics, University of Windsor, Windsor, 401, Sunset ONT Canada, N9B 3P4 bDepartment of Economics, Bilkent University, Bilkent 06533, Ankara, Turkey cEURANDOM, P.O. Box 513, 5600 MB Eindhoven, The Netherlands Received 14 June 2000 Abstract Inthispaper,weinvestigatethescalingpropertiesofforeignexchangevolatility.Ourmethod- ology is based on a wavelet multi-scaling approach which decomposes the variance of a time series and the covariance between two time series on a scale by scale basis through the appli- cation of a discrete wavelet transformation. It is shown that foreign exchange rate volatilities followdi erentscalinglawsatdi erenthorizons.Particularly,thereisasmallerdegreeofpersis- tence in intra-day volatility as compared to volatility at one day and higher scales. Therefore, a common practice in the risk management industry to convert risk measures calculated at shorter horizons into longer horizon

### id `6fafbf05-463c-4ade-8f9d-db3aa16b91e5`

**Searching for safe-haven assets during the COVID-19 pandemic** — Qiang Ji, Dayong Zhang, Yuqian Zhao, 2020

> SEARCHING FOR SAFE-HA VEN ASSETS DURING THE COVID-19 PANDEMIC QIANG JI1, DAYONG ZHANG2, YUQIAN ZHAO 3 1Center for Energy and Environmental Policy Research, Institutes of Science and Development, Chinese Academy of Sciences 2Research Institute of Economics and Management, Southwestern University of Finance and Economics, China 3Essex Business School, University of Essex, UK Abstract. The ongoing COVID-19 pandemic has shaken the global ﬁnancial system and caused great turmoil. Facing unprecedented risks in the markets, people have in- creasing needs to ﬁnd a safe haven for their investments. Given that the nature of this crisis is a combination of multiple problems, it is substantially diﬀerent from all other ﬁnancial crises known to us. It is therefore urgent to re-evaluate the safe-haven role of some traditional asset types, namely, gold, cryptocurrency, foreign exchange and com- modities. This paper introduces a sequential monitoring procedure to detect changes in the left-quantiles of asset returns, and to assess whether a tail change in the eq- uity index can be oﬀset by introduci

### id `44f6f148-dace-4db9-bbea-d43506e2dcf3`

**Self-fulfilling crises in the Eurozone: An empirical test** — Paul De Grauwe, Yuemei Ji, 2012

> Paul De Grauwe, Yuemei Ji Self-fulfilling crises in the Eurozone: an empirical test Article (Published version) (Refereed) Original citation: de Grauwe, Paul and Ji, Yuemei (2013) Self-fulfilling crises in the Eurozone: an empirical test. Journal of International Money and Finance, 34. pp. 15-36. ISSN 0261-5606 DOI: 10.1016/j.jimonfin.2012.11.003 © 2013 Elsevier Ltd This version available at: http://eprints.lse.ac.uk/49648/ Available in LSE Research Online: December 2014 Self-fulﬁlling crises in the Eurozone: An empirical test Paul De Grauwe a, c, *, Yuemei Ji b, c a The London School of Economics and Political Science, Houghton Street, London WC2A 2AE, UK b LICOS, University of Leuven, Waaistraat 6, Leuven, Belgium c Centre for European Policy Studies, 1 Place du Congres, Brussels, Belgium JEL classi ﬁcations: E4 E5 F3 G15 Keywords: Eurozone Government debt Interest rate Self-fulﬁlling crises Multiple equilibria Panel data Lender of last resort abstract We test the hypothesis that the government bond markets in the Eurozone are more fragile and more susceptible to self-ful ﬁlling li

### id `f2d6079f-6807-49b4-b2e6-0b2b16ab6e93`

**Short-Term Momentum Effect: a Case of Middle East Stock Markets** — Abdullah Ejaz, Petr Polák, 2015

> Copyright © 2015 The Authors. Published by VGTU Press. This is an open­access article distributed under the terms of the Creative Commons Attribution­NonCommercial 4.0 (CC BY ­NC 4.0) license, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited. The material cannot be used for commercial purposes. Verslas: Teorija ir prakTika / Business: Theory and pracTice issn 1648-0627 / eissn 1822-4202 http://www.btp.vgtu.lt 2015 16(1): 104–112 doi:10.3846/btp.2015.438 short-term momentum effeCt: a Case of middle east stoCK marKets abdullah ejaz1, petr polaK2 School of Business and Economics, Universiti Brunei Darussalam, Gadong, Brunei E­mails: 112h1301@ubd.edu.bn; 2petr.polak@ubd.edu.bn (corresponding author) Received 01 March 2013; accepted 15 June 2014 Abstract. The objective of this paper is to find short­term momentum effect in stock markets of the Middle East and to examine whether short­term momentum profits can be explained by risk­based CAPM model. Seven major stock markets from the Middle East were selected.

### id `179a2c64-d719-4354-9a86-21408c36d1e0`

**Social media and price discovery: The case of cross‐listed firms** — Rui Fan, Oleksandr Talavera, Vu Tran, 2022

> Social media and price discovery: the case of cross-listed firms Article Published Version Creative Commons: Attribution 4.0 (CC-BY) Open Access Fan, R., Talavera, O. and Tran, V. ORCID: https://orcid.org/0000-0001-9561-8118 (2023) Social media and price discovery: the case of cross-listed firms. Journal of Financial Research, 46 (1). pp. 151-167. ISSN 0270-2592 doi: 10.1111/jfir.12310 Available at https://centaur.reading.ac.uk/108181/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1111/jfir.12310 Publisher: Wiley All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Received: 23 March 2020 | Accepted: 5 October 2022 DOI: 10.1111/jfir.12310 ORIGINAL ARTICLE Social media and price discovery: The case of cross‐listed firms Rui Fan 1 | O

### id `a49010bd-961f-4b6b-a000-06a567323567`

**Speculation and lottery-like demand in cryptocurrency markets** — Klaus Grobys, Juha-Pekka Junttila, 2021

> Speculation and lottery-like demand in cryptocurrency markets Klaus Grobys a,⇑,1, Juha Junttila b,1 a University of Vaasa, School of Accounting and Finance, P.O. Box 700, FI-65101 Vaasa, Finland b University of Jyväskylä, School of Business and Economics, P.O. Box 35, FI-40014 Jyväskylä, Finland article info Article history: Received 18 May 2020 Accepted 6 January 2021 Available online 9 January 2021 JEL classiﬁcation: G01 G12 G14 Keywords: MAX Lottery-like demand Cryptocurrency Financial technology Gambling abstract This is the ﬁrst paper that explores lottery-like demand in cryptocurrency markets. Since recent research provides evidence that cryptocurrency returns appear to be short-memory processes, we modify Bali, Cakici and Whitelaw’s (2011) and Bali, Brown, Murray, and Tang’s (2017) MAX measure and employ a weekly forecast horizon and daily log-returns from the previous week to calculate the metric for our portfolio sorts. From an econometric point of view, this study proposes statistical tests that are robust to unknown dynamic dependency structures in the cryptocurrency data.

### id `544d6311-4397-4354-9bf9-7b8da94a9ced`

**Stock market integration between new EU member states and the Euro-zone** — Christos S. Savva, Nektarios Aslanidis, 2009

> Empir Econ (2010) 39:337–351 DOI 10.1007/s00181-009-0306-6 ORIGINAL PAPER Stock market integration between new EU member states and the Euro-zone Christos S. Savva · Nektarios Aslanidis Received: 24 August 2008 / Accepted: 8 May 2009 / Published online: 1 September 2009 © Springer-V erlag 2009 Abstract This paper measures the degree in stock market integration between ﬁve Eastern European countries and the Euro-zone. A potentially gradual transition in cor- relations is accommodated by smooth transition conditional correlation models. We ﬁnd that the Czech, Slovenian and Polish markets have increased their correlation to the Euro-zone from 1997 to 2008. However, this is not a broad-based phenomenon across Eastern Europe. The results also show that the increase in correlations is not a reﬂection of a world-wide phenomenon of ﬁnancial integration but is mainly driven by EU-related developments. Keywords Multivariate GARCH · Smooth transition conditional correlation · Stock return comovement · New EU members JEL Classiﬁcation C32 · C51 · F36 · G15 1 Introduction It is a well established

### id `aa71c194-60e6-47ea-a1ca-524d0ad6a83f`

**Survival, Look-Ahead Bias, and Persistence in Hedge Fund Performance** — Guillermo Baquero, Jenke ter Horst, Marno Verbeek, 2005

> Survival, Look-Ahead Bias and the Persistence in Hedge F und Performance Guillermo Baqueroy, Jenke ter Horst zand Marno V erbeekx August 30, 2004 The authors would like to thank Bing Liang, Stephen Brown (the Editor), Theo Nij- man, an anonymous referee, seminar participants at the University of Maastricht, and participants of the 2002 European Financial Management Association meetings, 2002 Eu- ropean Investment Review meetings, the 2002 Inquire meeting in Stockholm, and the 2003 European Finance Association meetings in Glasgow for helpful comments and suggestions. This paper was partly written while the rst author was at the Center for Economic Stud- ies, K.U.Leuven, Belgium. yDept. of Financial Management, Erasmus University Rotterdam, P.O.Box 1738, 3000 DR Rotterdam, The Netherlands; e-mail: G.Baquero@fbk.eur.nl. zDept. of Finance, Tilburg University, P.O. Box 90153, 5000 LE Tilburg, The Nether- lands. Tel : +31 13 4668211; fax : +31 13 4662875; email : j.r.terhorst@uvt.nl xCorresponding author. Dept. of Financial Management and Econometric Institute, F4-33, Erasmus University 

### id `6536a748-8583-4fa8-bed3-99d3f83962dd`

**The day of the week effect on stock market volatility and volume: International evidence** — Halil Kiymaz, Hakan Berument, 2003

> The day of the week effect on stock market volatility and volume: International evidence Halil Kiymaz a,*, Hakan Berument b aDepartment of Finance, School of Business and Public Administration, University of Houston-Clear Lake, Houston, TX 77058, USA bDepartment of Economics, Bilkent University, Ankara, Turkey Received 4 January 2001; received in revised form 7 February 2002; accepted 6 June 2003 Abstract This study investigates the day of the week effect on the volatility of major stock market indexes for the period of 1988 through 2002. Using a conditional variance framework, we find that the day of the week effect is present in both return and volatility equations. The highest volatility occurs on Mondays for Germany and Japan, on Fridays for Canada and the United States, and on Thursdays for the United Kingdom. For most of the markets, the days with the highest volatility also coincide with that market’s lowest trading volume. Thus, this paper supports the argument made by Foster and Viswanathan [Rev. Financ. Stud. 3 (1990) 593] that high volatility would be accompanied by low tr

### id `c4bad326-00d3-4134-97c6-44cb3076833c`

**The effects of institutional investor objectives on firm valuation and governance** — Paul Borochin, Jie Yang, 2017

> Finance and Economics Discussion Series Divisions of Research & Statistics and Monetary Aﬀairs Federal Reserve Board, Washington, D.C. The Eﬀects of Institutional Investor Objectives on Firm Valuation and Governance Paul Borochin and Jie Yang 2016-088 Please cite this paper as: Borochin, Paul and Jie Yang (2016). “The Eﬀects of Institutional Investor Ob- jectives on Firm Valuation and Governance,” Finance and Economics Discussion Se- ries 2016-088. Washington: Board of Governors of the Federal Reserve System, https://doi.org/10.17016/FEDS.2016.088. NOTE: Staﬀ working papers in the Finance and Economics Discussion Series (FEDS) are preliminary materials circulated to stimulate discussion and critical comment. The analysis and conclusions set forth are those of the authors and do not indicate concurrence by other members of the research staﬀ or the Board of Governors. References in publications to the Finance and Economics Discussion Series (other than acknowledgement) should be cleared with the author(s) to protect the tentative character of these papers. The Eﬀects of Institutional I

### id `46b66fcf-3108-4ad8-b29f-4665daebbe09`

**The heterogeneous expectations hypothesis: Some evidence from the lab** — Cars Hommes, 2010

> UvA-DARE is a service provided by the library of the University of Amsterdam (https://dare.uva.nl) UvA-DARE (Digital Academic Repository) The heterogeneous expectations hypothesis: Some evidence from the lab Hommes, C. DOI 10.1016/j.jedc.2010.10.003 Publication date 2011 Document Version Author accepted manuscript Published in Journal of Economic Dynamics & Control Link to publication Citation for published version (APA): Hommes, C. (2011). The heterogeneous expectations hypothesis: Some evidence from the lab. Journal of Economic Dynamics & Control, 35(1), 1-24. https://doi.org/10.1016/j.jedc.2010.10.003 General rights It is not permitted to download or to forward/distribute the text or part of it without the consent of the author(s) and/or copyright holder(s), other than for strictly personal, individual use, unless the work is under an open content license (like Creative Commons). Disclaimer/Complaints regulations If you believe that digital publication of certain material infringes any of your rights or (privacy) interests, please let the Library know, stating your reasons. In cas

### id `2041f4ca-fa8b-483d-9536-4cbec2476520`

**The impact of Covid-19 on G7 stock markets volatility: Evidence from a ST-HAR model** — Marwan Izzeldin, Yaz Gűlnur Muradoğlu, Vasileios Pappas, Sheeja Sivaprasad, 2021

> Izzeldin, Marwan, Murado□lu, Gülnur, Pappas, Vasileios and Sivaprasad, Sheeja (2021) The impact of Covid-19 on G7 stock markets volatility: Evidence from a ST-HAR model. International Review of Financial Analysis, 74 . ISSN 1057-5219. Kent Academic Repository Downloaded from https://kar.kent.ac.uk/85238/ The University of Kent's Academic Repository KAR The version of record is available from https://doi.org/10.1016/j.irfa.2021.101671 This document version Author's Accepted Manuscript DOI for this version Licence for this version CC BY-NC-ND (Attribution-NonCommercial-NoDerivatives) Additional information Versions of research works Versions of Record If this version is the version of record, it is the same as the published version available on the publisher's web site. Cite as the published version. Author Accepted Manuscripts If this document is identified as the Author Accepted Manuscript it is the version after peer review but before type setting, copy editing or publisher branding. Cite as Surname, Initial. (Year) 'Title of article'. To be published in Title of Journal , Volume an

### id `89b0eb37-73a3-4737-a92d-150d3cc8b415`

**The impact of COVID-19 on the evolution of online retail: The pandemic as a window of opportunity** — Levente Szász, Csaba Bálint, Ottó Csíki, Bálint Zsolt Nagy, 2022

> To cite this paper: Szász, L., Bálint, C., Csíki, O., Nagy, B. Z., Rácz, B. G., Csala, D., & Harris, L. C. (2022). The impact of COVID-19 on the evolution of online retail: The pandemic as a window of opportunity. Journal of Retailing and Consumer Services, Vol. 69, 103089. https://doi.org/10.1016/j.jretconser.2022.103089 The impact of COVID-19 on the evolution of online retail: The pandemic as a window of opportunity Levente Szásza,*1, Csaba Bálintb,a, Ottó Csíkia, Bálint Zsolt Nagya, Béla-Gergely Rácza, Dénes Csalac,a,d, Lloyd C. Harrise,a a Faculty of Economics and Business Administration, Babeș-Bolyai University, Romania 400591 Cluj-Napoca, Teodor Mihali str. 58-60, Romania b National Bank of Romania 030031 Bucharest, Lipscani str. 25, sector 3, Romania c Department of Engineering, Lancaster University, UK Engineering Building, Lancaster University, Lancaster LA1 4YW, United Kingdom d Economics Observatory, School of Economics, University of Bristol, UK Beacon House, Queens Road, Bristol BS8 1QU, United Kingdom e Alliance Manchester Business School, University of Manchester, UK B

### id `9e772479-b4fc-4f41-a26e-ce28f7b03242`

**THE IMPACT OF INTRADAY MOMENTUM ON STOCK RETURNS: EVIDENCE FROM S&P500 AND CSI300** — Saddam Hossain, Beáta Gavurová, Xianghui Yuan, Morshadul Hasan, 2021

> 124 2021, XXIV, 4 Finance 10.15240/tul/001/2021-4-008 THE IMPACT OF INTRADAY MOMENTUM ON STOCK RETURNS: EVIDENCE FROM S&P500 AND CSI300 Saddam Hossain 1, Beáta Gavurová 2, Xianghui Yuan3, Morshadul Hasan 4, Judit Oláh5 1 Xi’an Jiaotong University, School of Economics and Finance, China, ORCID: 0000-0001-5663-1643, saddam@stu.xjtu.edu.cn; 2 Tomas Bata University in Zlín, Faculty of Management and Economics, Center for Applied Economic Research, Czech Republic, ORCID: 0000-0002-0606-879X, gavurova@utb.cz; 3 Xi’an Jiaotong University, School of Economics and Finance, China, ORCID: 0000-0003-1466-5268, xhyuan@mail.xjtu.edu.cn (corresponding author); 4 University of Debrecen, Károly Ihrig Doctoral School, Hungary, ORCID: 0000-0001-9857-9265, mohammad.hasan@econ.unideb.hu; 5 WSB University, Faculty of Applied Sciences, Department of Management, Poland, ORCID: 0000-0003-2247-1711, juditdrolah@gmail.com. Abstract: This paper analyzes the statistical impact of COVID-19 on the S&P500 and the CSI300 intraday momentum. This study employs an empirical method, that is, the intraday momentum method

### id `e113e3a3-22c5-42a1-a152-af15a15c632d`

**The impact of the Russian-Ukrainian war on global financial markets** — Marwan Izzeldin, Yaz Gűlnur Muradoğlu, Vasileios Pappas, Athina Petropoulou, 2023

> Izzeldin, Marwan, Muradoğlu, Gülnur, Pappas, Vasileios, Petropoulou, Athina and Sivaprasad, Sheeja (2023) The Impact of the Russian-Ukrainian War on Global Financial Markets. International Review of Financial Analysis, 87 . ISSN 1057-5219. Kent Academic Repository Downloaded from https://kar.kent.ac.uk/100023/ The University of Kent's Academic Repository KAR The version of record is available from https://doi.org/10.1016/j.irfa.2023.102598 This document version Publisher pdf DOI for this version Licence for this version CC BY (Attribution) Additional information Versions of research works Versions of Record If this version is the version of record, it is the same as the published version available on the publisher's web site. Cite as the published version. Author Accepted Manuscripts If this document is identified as the Author Accepted Manuscript it is the version after peer review but before type setting, copy editing or publisher branding. Cite as Surname, Initial. (Year) 'Title of article'. To be published in Title of Journal , Volume and issue numbers [peer-reviewed accepted ver

### id `91d3dde4-9110-4b18-b65f-25bd17166b4a`

**The influence of the COVID-19 pandemic on asset-price discovery: Testing the case of Chinese informational asymmetry** — Shaen Corbet, Yang Hou, Yang Hu, Les Oxley, 2020

> The inﬂuence of the COVID-19 pandemic on asset-price discovery: Testing the case of Chinese informational asymmetry Shaen Corbeta,b, Yang (Greg) Houa∗, Yang Hua∗, Les Oxleya aSchool of Accounting, Finance and Economics, University of Waikato, New Zealand bDCU Business School, Dublin City University, Dublin 9, Ireland ∗Corresponding Authors: yang.hu@waikato.ac.nz (Y.Hu); greg.hou@waikato.ac.nz (G.Hou) Abstract The circumstances surrounding the outbreak of the COVID-19 pandemic have generated sub- stantial international political strain as governments attempt to mitigate the widespread associated social and economic repercussions. One theory has focused on the potential for Chinese informa- tional asymmetry. Using Chinese ﬁnancial market data, we attempt to establish the scale and direc- tion of information ﬂows during multiple distinct phases of the development of the pandemic. Two speciﬁc results are identiﬁed. Firstly, the majority of domestically-traded Chinese stocks present evidence of signiﬁcant information ﬂows at a far earlier stage than internationally-traded compar- atives, 

### id `a05f9555-d764-4b52-ba79-3c303a4c6043`

**The interpretive dimension of economics: Science, hermeneutics, and praxeology** — Don Lavoie, 2011

> The interpretive dimension of economics: Science, hermeneutics, and praxeology Don Lavoie Published online: 20 January 2011 # Springer Science+Business Media, LLC 2011 Keywords Hermeneutics . Praxeology . Interpretive dimension . Gadamer . Schutz 1 Introduction A crisis of the method of economic thinking is taking shape. The question arises, to what extent the style of economic thought which has been predominant for about half a century, at least in the Western World, can do justice to the problems of human action in a rapidly changing world, and, in particular, in a tempestuous epoch. Ludwig M. Lachmann ( 1984,p .1 ) This essay confronts three bodies of methodological literature with one another: the growth of knowledge literature on the methods of the sciences in general, the continental philosophy known as “hermeneutics” (or the science of interpretation) on the methods of the social sciences, and the methodology that the Austrian school economist Ludwig von Mises called “praxeology” (or the science of human action) on the methods of economics in particular. The upshot of this con

### id `158ab757-58ab-4beb-b2fe-e90722bc8971`

**The lead–lag relation between VIX futures and SPX futures** — Christine Bangsgaard, Thomas Kokholm, 2023

> Journal of Financial Markets 67 (2024) 100851 Available online 21 June 2023 1386-4181/© 2023 The Author(s). Published by Elsevier B.V. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/). Contents lists available at ScienceDirect Journal of Financial Markets journal homepage: www.elsevier.com/locate/finmar The lead–lag relation between VIX futures and SPX futures✩ Christine Bangsgaard a, Thomas Kokholma,b,∗ a Aarhus BSS, Aarhus University, Department of Economics and Business Economics, Denmark b Danish Finance Institute, Denmark A R T I C L E I N F O JEL classification: G11 G12 G13 G14 G23 Keywords: Lead–lag relation High-frequency data Cross-correlation Price discovery VIX futures hedging Cross-market activity A B S T R A C T We analyze the lead–lag relation between VIX futures and SPX futures. The two futures markets are weakly connected when market volatility is low. By contrast, when volatility is high, their prices are highly negatively correlated, with VIX futures leading SPX futures. However, the tightness of the lead–lag relat

### id `05504f12-3a0a-4751-b08f-347897ce1753`

**The Military and the Consolidation of Democracy: The Recent Turkish Experience** — Metiṅ Heper, Aylın Güney, 2000

> The Military and the Consolidation of Democracy: The Recent 1\irkish Experience METIN HEPER AND AYLIN GUNEY The significant differences among regions and even countries about the relations between governments and militaries make it impossible to develop an overarching theory of civil-military relations and the prospects for the consolidation of democracy. Prior to the transition to democracy, officers in Latin America functioned as political elites and exercised power in their own right; in contrast, officers in Eastern Europe were coopted by the communist parties and subjected to intense political indoctrination. Consequently, while in Latin America the consolidation of democracy required the demilitarization of politics, in Eastern Europe it required the depoliticization ofthe military.' In Latin America, at the time of the transition to democracy the military retained too many privileges.^ Thus politicians in that continent wished to have greater say about the resources previously controlled by the military so that they could pursue client-oriented policies to gamer votes,^ and th

### id `32d63d72-87ab-42aa-a12e-4396ee41dbc3`

**The Momentum & Trend-Reversal as Temporal Market Anomalies** — Vasiliki Basdekidou, 2017

> International Journal of Economics and Finance; V ol. 9, No. 5; 2017 ISSN 1916 -971X E-ISSN 1916 -9728 Published by Canadian Center of Science and Education 1 The Momentum & Trend-Reversal as Temporal Market Anomalies Vasiliki A. Basdekidou1 1 SRFA Aristotle University of Thessaloniki, Greece Correspondence: Vasiliki A. Basdekidou, Special Research Fund Account (ELKE), Aristotle University of Thessaloniki, Greece. Tel: 30-697-277-5475. E-mail: Vasiliki.Basdekidou@gmail.com Received: January 6, 2017 Accepted: March 8, 2017 Online Published: April 5, 2017 doi:10.5539/ijef.v9n5p1 URL: https://doi.org/10.5539/ijef.v9n5p1 Abstract The main goal of this paper is to introduce and discuss the temporal dimension and the subsequent (time-series) functionalities of two well-known technical market anomalies - the momentum anomaly and the trend-reversal anomaly. Our approach not only challenging the efficient-market hypothesis but also has a temporal dimension because it uses the “psychological time” at the beginning of a move, as a parameter in overnight post-market asset position trading strate

### id `28aecbf7-d005-4e53-b9df-ce4adc22ee53`

**The People’s Prince: Popular Politics in Early Modern Venice** — Maartje van Gelder, 2018

> UvA-DARE is a service provided by the library of the University of Amsterdam (https://dare.uva.nl) UvA-DARE (Digital Academic Repository) The People’s Prince: Popular Politics in Early Modern Venice van Gelder, M. DOI 10.1086/697401 Publication date 2018 Document Version Final published version Published in Journal of Modern History License Article 25fa Dutch Copyright Act (https://www.openaccess.nl/en/policies/open-access-in- dutch-copyright-law-taverne-amendment) Link to publication Citation for published version (APA): van Gelder, M. (2018). The People’s Prince: Popular Politics in Early Modern Venice. Journal of Modern History, 90(2), 249-291. https://doi.org/10.1086/697401 General rights It is not permitted to download or to forward/distribute the text or part of it without the consent of the author(s) and/or copyright holder(s), other than for strictly personal, individual use, unless the work is under an open content license (like Creative Commons). Disclaimer/Complaints regulations If you believe that digital publication of certain material infringes any of your rights or (pr

### id `788c3c4e-e452-4a37-90ad-52efd70aef92`

**The Predictive Power of Implied Volatility and GARCH Forecasted Volatility During the COVID-19 Pandemic: Evidence from China’s Stock Market** — Wei Zhang, 2023

> The Predictive Power of Implied V olatility and GARCH Forecasted V olatility During the COVID-19 Pandemic: Evidence from China’s Stock Market Wei Zhang1,a,* 1Wealth and Personal Banking Department, China Construction Bank, Beijing, 100053, China a. b0401352@hotmail.com *corresponding author Abstract: In this study, we explore how the performance of several popular historical and forward-looking forecasting measures for equity index volatility is affected by the COVID - 19 related uncer tainty. Our findings present convincing evidence for the advantages of implied volatility in predicting future volatility in the context of the COVID -19 pandemic. Our results also reveal that GARCH forecasted volatility contains unique information about market risk, but the information efficiency is sensitive to economic uncertainty. Therefore, the empirical evidence from China’s stock market is supportive of a popular theoretical view that GARCH and implied volatility capture different aspects of market un certainty and an appropriate com bination of both measures may perform best in terms of informa

### id `b2deb01a-e172-4e0d-8bc5-612cd4880bfb`

**The Price Impact of Order Book Events** — R. Cont, A. Kukanov, S. Stoikov, 2013

> The price impact of order book events Rama Cont, Arseniy Kukanov and Sasha Stoikov March 2011 Abstract We study the price impact of order book events - limit orders, market orders and can- celations - using the NYSE TAQ data for 50 U.S. stocks. We show that, over short time intervals, price changes are mainly driven by the order ﬂow imbalance, deﬁned as the imbal- ance between supply and demand at the best bid and ask prices. Our study reveals a linear relation between order ﬂow imbalance and price changes, with a slope inversely proportional to the market depth. These results are shown to be robust to seasonality eﬀects, and stable across time scales and across stocks. We argue that this linear price impact model, together with a scaling argument, implies the empirically observed “square-root” relation between price changes and trading volume. However, the relation between price changes and trade volume is found to be noisy and less robust than the one based on order ﬂow imbalance. Contents 1 Introduction 2 1.1 Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

### id `d82444a8-3590-4be0-83b0-535f9021de58`

**The spillover effects of US and Japanese public information news in advanced Asia-Pacific stock markets** — Suk‐Joong Kim, 2003

> The spillover effects of US and Japanese public information news in advanced Asia-Pacific stock markets Author: Kim, Suk-Joong Publication details: Pacific-Basin Finance Journal v. 11 pp. 611-630 Publication Date: 2003 Publisher DOI: http://dx.doi.org/10.1016/S0927-538X(03)00015-5 License: https://creativecommons.org/licenses/by-nc-nd/3.0/au/ Link to license to see what you are allowed to do with this resource. Downloaded from http://hdl.handle.net/1959.4/40154 in https:// unsworks.unsw.edu.au on 2026-09-22 Electronic copy of this paper is available at: http://ssrn.com/abstract=448120 The Spillover Effects of U.S. and Japanese Public Information News in Advanced Asia-Pacific Stock Markets Suk-Joong Kim School of Banking and Finance The University of New South Wales UNSW SYDNEY 2052 Australia Tel: +61 2 9385-4278 Fax: + 61 2 9385-6347 Email: s.kim@unsw.edu.au Abstract This paper investigates the nature of information leadership of the U.S. and Japan in the advanced Asia-Pacific stock markets. Instead of just relying on return and return volatility spillovers from major markets, specif

### id `c2007eb2-3362-49cc-b594-ee9fb29f2584`

**The Term Structure of Variance Swap Rates and Optimal Variance Swap Investments** — Daniel Egloff, Markus Leippold, Liuren Wu, 2010

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 45, No. 5, Oct. 2010, pp. 1279–1310 COPYRIGHT 2010, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109010000463 The T erm Structure of Variance Swap Rates and Optimal Variance Swap Investments Daniel Egloff, Markus Leippold, and Liuren Wu ∗ Abstract This paper performs speciﬁcation analysis on the term structure of variance swap rates on the S&P 500 index and studies the optimal investment decision on the variance swaps and the stock index. The analysis identiﬁes 2 stochastic variance risk factors, which govern the short and long end of the variance swap term structure variation, respectively. The highly negative estimate for the market price of variance risk makes it optimal for an investor to take short positions in a short-term variance swap contract, long positions in a long-term variance swap contract, and short positions in the stock index. I. Introduction The ﬁnancial market is becoming increasingly aware of the fact that the re- turn variance on stock indexes is stochastic 

### id `7999d2e2-4c40-4b48-9297-04e319d98b26`

**The VIX Premium** — Ing-Haw Cheng, 2018

> TSpace Research Repository tspace.library.utoronto.ca The VIX Premium Ing-Haw Cheng Version Post-print or accepted manuscript. Citation (published version) Cheng, I. H. (2019). The VIX premium. The Review of Financial Studies, 32(1), 180-227. DOI https://doi.org/10.1093/rfs/hhy062 Publisher’s Statement This article has been accepted for publication in the The Review of Financial Studies. Published by Oxford University Press. H ow to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page. This article was made openly accessible by U of T Faculty. Please tell us how this access benefits you. Your story matters. The VIX Premium Ing-Haw Cheng∗ May 2018 Ex-ante estimates of the volatility premium embedded in VIX futures, known as the VIX premium, fall

### id `e32ee8b3-edad-4f7a-82bd-3930621a039d`

**Trading and arbitrage in cryptocurrency markets** — Igor Makarov, Antoinette Schoar, 2019

> Makarov, Igor & Schoar, Antoinette (2020) Trading and arbitrage in cryptocurrency markets. Journal of Financial Economics, 135 (2), 293 - 319. https://doi.org/10.1016/j.jfineco.2019.07.001 https://researchonline.lse.ac.uk/id/eprint/100409/ Version: Accepted Version Licence: Creative Commons: Attribution-Noncommercial- No Derivative Works 4.0 This document is the author’s accepted version of the journal article. There may be differences between this version and the published version. Items deposited in LSE Research Online are protected by copyright, with all rights reserved unless indicated otherwise. They may be downloaded and/or printed for private study, or other acts as permitted by national copyright laws. LSE Research Online is the repository for research produced by the London School of Economics and Political Science. For more information, please refer to our Policies page or contact lseresearchonline@lse.ac.uk Trading and Arbitrage in Cryptocurrency Markets Igor Makarova,∗, Antoinette Schoarb,∗ aLondon School of Economics bMIT Sloan, NBER, CEPR Abstract Cryptocurrency markets

### id `5acb830b-c33c-4dfc-b54a-1bdc971b632d`

**Transmission of Information across International Equity Markets** — Jon Wongswan, 2006

> Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 759 February 2003 Transmission of Information Across International Equity Markets Jon Wongswan NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at www.federalreserve.gov/pubs/ifdp/. Transmission of Information Across International Equity Markets Jon Wongswan∗ Abstract: This paper provides evidence of transmission of information from the U.S. and Japan to Korean and Thai equity markets during the period from 1995 through 2000.Infor- mation is deﬁned as important macroeconomic announcements in the U.S., Japan, Korea, and Thailand. Using high-frequency intraday data, I focus the study on return volatility and trading volume because the implications of new information are much clearer than for r

### id `cfb7ca75-ca09-4c5c-95bb-61991ff4c135`

**U.S. unconventional monetary policy and transmission to emerging market economies** — David Bowman, Juan M. Londoño, Horacio Sapriza, 2015

> AUCUN TEXTE EXTRAIT — l'extraction du PDF n'a rien rendu. Juge sur le titre seul, et dis-le dans la raison.

