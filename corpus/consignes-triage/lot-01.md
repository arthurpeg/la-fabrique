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

## LES PAPIERS — lot 1 sur 4

### id `789a134c-96af-447d-a1ae-8bd17d36a582`

**A complex systems approach to constructing better models for managing financial markets and the economy** — J. Doyne Farmer, Mauro Gallegati, Cars Hommes, Alan Kirman, 2012

> Eur.Phys.J.SpecialTopics 214,295–324(2012) ©TheAuthor(s)2012.Thisarticleispublished withopenaccessat Springerlink.com DOI:10.1140/epjst/e2012-01696-9 THE EUROPEAN PHYSICAL JOURNAL SPECIAL TOPICS RegularArticle A complex systems approach to constructing better models for managing ﬁnancial markets and the economy J.DoyneFarmer 1,M.Gallegati 2,C.Hommes 3,A.Kirman 4,P .Ormerod5, S.Cincotti 6,A.Sanchez 7,andD.Helbing 8 1 SantaFeInstitute,1399HydeParkRoad,SantaFe,NM87501,USA 2 DiSES,UniversitPolitecnicadelleMarche,Ancona,Italy 3 CeNDEF,UniversityofAmsterdam,TheNetherlands 4 GREQAM,AixMarseilleUniversit´e,EHESS,France 5 VolterraPartners,LondonandUniversityofDurham,UK 6 DIME-DOGE.I,UniversityofGenoa,Italy 7 GISC,UniversidadCarlosIIIdeMadrid,Spain 8 ETH,Z¨urich Received1August2012/Receivedinﬁnalform9October2012 Publishedonline5December2012 Abstract. Weoutlineavisionforanambitiousprogramtounderstand theeconomyandﬁnancialmarketsasacomplexevolvingsystemof couplednetworksofinteractingagents.Thisisacompletelydiﬀerent visionfromthatcurrentlyusedinmosteconomicmodels.Thisview impliesnewchallengesando

### id `d57399a7-7f1b-4560-bdd2-32bc1e7de475`

**Accounting for Macro-Finance Trends: Market Power, Intangibles, and Risk Premia** — Emmanuel Farhi, Gourio François, 2018

> 147 EMMANUEL FARHI Harvard University FRANÇOIS GOURIO Federal Reserve Bank of Chicago Accounting for Macro-Finance Trends: Market Power, Intangibles, and Risk Premia ABSTRACT Real risk-free interest rates have trended down over the past 30 years. Puzzlingly, in light of this decline, (1) the return on private capital has remained stable or even increased, creating an increasing wedge with safe interest rates; (2) stock market valuation ratios have increased only moder - ately; (3) and investment has been lackluster. We use a simple extension of the neoclassical growth model to diagnose the nexus of forces that jointly accounts for these developments. We find that rising market power, rising unmeasured intangibles, and rising risk premia play a crucial role, over and above the traditional culprits of increasing savings supply and technological growth slowdown. D uring the past 30 years, most developed economies have experienced large declines in risk-free interest rates and increases in asset prices such as housing or stock prices, with occasional sudden crashes. At the same time, exc

### id `121ffd18-f964-4f1d-be6c-3f0f13d250ce`

**Allocation, allocation, allocation! The political economy of the development of the European Union Emissions Trading System** — Misato Sato, Ryan Rafaty, Raphael Calel, Michael J. Grubb, 2022

> Sato, Misato , Rafaty , Ryan, Calel, Raphael & Grubb, Michael (2022) Allocation, allocation, allocation! The political economy of the development of the European Union Emissions T rading System. Wiley Interdisciplinary Reviews: Climate Change, 13(5). https://doi.org/10.1002/wcc.796 https://researchonline.lse.ac.uk/id/eprint/115431/ Version: Published Version Licence: Creative Commons: Attribution 4.0 LSE Research Online is the repository for research produced by the London School of Economics and Political Science. For more information, please refer to our Policies page or contact lseresearchonline@lse.ac.uk OVERVIEW Allocation, allocation, allocation! The political economy of the development of the European Union Emissions Trading System Misato Sato1 | Ryan Rafaty 2,3 | Raphael Calel 4 | Michael Grubb 5 1Grantham Research Institute on Climate Change and the Environment, London School of Economics and Political Science, London, UK 2Climate Econometrics, Nuffield College, University of Oxford, Oxford, UK 3Institute for New Economic Thinking at the Oxford Martin School, Oxford, UK 4McC

### id `44eaac42-7001-4407-a5e4-3e224a0abedd`

**An intertemporal CAPM with stochastic volatility** — John Y. Campbell, Stefano Giglio, Christopher Polk, Robert Turley, 2018

> An Intertemporal CAPM with Stochastic V olatility John Y. Campbell, Stefano Giglio, Christopher Polk, and Robert T urley 1 First draft: October 2011 This version: January 2017 Abstract This paper studies the pricing of volatility risk using the rst-order conditions of a long-term equity investor who is content to hold the aggregate equity market rather than overweighting value stocks and other equity portfolios that are attractive to short-term investors. W e show that a conservative long-term investor will avoid such overweights in order to hedge against two types of deterioration in investment opportunities: declining expected stock returns, and increasing volatility. Empirically, we present novel evidence that low-frequency movements in equity volatility, tied to the default spread, are priced in the cross-section of stock returns. 1Campbell: Department of Economics, Littauer Center, Harvard University, Cambridge MA 02138, and NBER. Email john_campbell@harvard.edu. Phone 617-496-6448. Giglio: Booth School of Business, Univer- sity of Chicago, 5807 S. Woodlawn Ave, Chicago IL 60637

### id `de4d7b5a-4b23-4344-b993-3af462385dbe`

**Are Analysts’ Recommendations Informative? Intraday Evidence on the Impact of Time Stamp Delays** — Daniel Bradley, Jonathan Clarke, Suzanne Lee, Chayawat Ornthanalai, 2013

> TSpace Research Repository tspace.library.utoronto.ca Are Analysts’ Recommendations Informative? Intraday Evidence on the Impact of Time Stamp Delays Daniel Bradley, Jonathan Clarke, Suzanne Lee & Chayawat Ornthanalanai Version Post-print or Accepted manuscript Citation (published version) Christoffersen, P., Jacobs, K., & Ornthanalai, C. (2012). Dynamic jump intensities and risk premiums: Evidence from S&P500 returns and options. Journal of Financial Economics, 106(3), 447-472. Publisher’s Statement This is the peer reviewed version of the following article: Christoffersen, P., Jacobs, K., & Ornthanalai, C. (2012). Dynamic jump intensities and risk premiums: Evidence from S&P500 returns and options. Journal of Financial Economics, 106(3), 447-472, which has been published in final form at https://doi.org/10.1111/jofi.12107. This article may be used for non-commercial purposes in accordance with Wiley Terms and Conditions for Use of Self-Archived Versions. How to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track

### id `968555a2-fa6c-4fc8-b847-93342d939244`

**Asset Management Contracts and Equilibrium Prices** — Andrea M Buffa, Dimitri Vayanos, Paul Woolley, 2022

> Buffa, Andrea M., Vayanos, Dimitri & Woolley , Paul (2022) Asset management contracts and equilibrium prices. Journal of Political Economy , 130 (12), 3146 - 3201. https://doi.org/10.1086/720515 https://researchonline.lse.ac.uk/id/eprint/113889/ Version: Published Version Licence: Creative Commons: Attribution-Noncommercial 4.0 LSE Research Online is the repository for research produced by the London School of Economics and Political Science. For more information, please refer to our Policies page or contact lseresearchonline@lse.ac.uk Asset Management Contracts and Equilibrium Prices Andrea M. Buffa University of Colorado Boulder Dimitri Vayanos London School of Economics, Center for Economic and Policy Research, and National Bureau of Economic Research Paul Woolley London School of Economics We model asset management as a continuum between active and pas- sive: managers can deviate from benchmark indices to exploit noise trader–induced distortions, but agency frictions constrain these devi- ations. Because constraints force managers to buy assets that they un- derweight when these 

### id `606c948e-a7ee-4264-b212-64c7d11205d1`

**Bank fragility and contagion: Evidence from the bank CDS market** — Laura Ballester, Barbara Casu, Ana González‐Urteaga, 2016

> 1 Bank Fragility and Contagion: Evidence from the bank CDS market Laura Ballester (Laura.Ballester@uv.es) University of Valencia, Valencia, Spain Barbara Casu (b.casu@city.ac.uk) Cass Business School, City University London, UK Ana González-Urteaga (ana.gonzalezu@unavarra.es) Public University of Navarre, Pamplona, Spain This version: 18 December 2015 Abstract Understanding how contagion works among financial institutions is a top priority for regulators and policy makers who aim to foster financial stability and to prevent financial crises. Using bank credit default swap (CDS) data, we provide a framework for the evaluation of contagion among banks in different countries and regions during a period of prolonged financial distress. We measure contagion in terms of return spillovers, following a Generalized VAR (GVAR) approach. In addition, we propose an innovative framework to distinguish between two types of contagion: systematic (linked to global factors), and idiosyncratic (linked to bank specific factors). We find evidence of both types of contagion, although the spillover dynami

### id `84b56ff8-147d-41b8-a710-cd55c3a9bd4a`

**Behavioral Economics and the Conduct of Benefit-Cost Analysis: Towards Principles and Standards** — Lisa A. Robinson, James K. Hammitt, 2011

> Volume 2, Issue 2 2011 Article 5 Journal of Benefit-Cost Analysis Behavioral Economics and the Conduct of Benefit-Cost Analysis: Towards Principles and Standards Lisa A. Robinson, Independent Consultant James K. Hammitt, Harvard University and Toulouse School of Economics Recommended Citation: Robinson, Lisa A. and Hammitt, James K. (2011) "Behavioral Economics and the Conduct of Benefit-Cost Analysis: Towards Principles and Standards," Journal of Benefit-Cost Analysis: Vol. 2: Iss. 2, Article 5. DOI: 10.2202/2152-2812.1059 https://doi.org/10.2202/2152-2812.1059 Downloaded from https://www.cambridge.org/core. ipmc cnrs, on 22 Sep 2026 at 07:10:09, subject to the Cambridge Core terms of use, available at https://www.cambridge.org/core/terms. Behavioral Economics and the Conduct of Benefit-Cost Analysis: Towards Principles and Standards Lisa A. Robinson and James K. Hammitt Abstract As traditionally conducted, benefit-cost analysis is rooted in neoclassical welfare economics, which, in its most simplified form, assumes that individuals act rationally and are primarily motivated by self

### id `3ece5eb7-08bf-4c4a-9137-ffd6338112bf`

**Behavioural finance and cryptocurrencies** — Antonis Ballis, Thanos Verousis, 2022

> 1 Behavioural finance and cryptocurrencies Antonis Ballis1 and Thanos Verousis2 Abstract The present study sets out to examine the empirical literature on the behavioural aspects of cryptocurrencies, showing the findings of related studies and discussing the various results. A systematic literature review of cryptocurrencies in behavioural finance seems to be timely and particularly i mportant in terms of providing a guide for future research. Key topics include an extent review on the issue of herding behaviour among cryptocurrencies, momentum effects and overreaction, contagion effect, sentiment and uncertainty, along with studies related to investment decision making, optimism bias, disposition, lottery and size effects. Keywords: Behavioural Finance; Bitcoin; Cryptocurrencies; Herding; Momentum; Sentiment JEL classification: G4; G1 1 Aston Business School, Aston University, Birmingham, UK. 2 Essex Business School, University of Essex, Colchester, Essex, UK. Electronic copy available at: https://ssrn.com/abstract=4119562 2 1. Introduction “It doesn’t do anything. It just sits ther

### id `d3a0f65c-f6ec-42e8-b650-f740dd9c4167`

**Bifurcation routes to volatility clustering under evolutionary learning** — Andrea Gaunersdorfer, Cars Hommes, Florian Wagener, 2007

> UvA-DARE is a service provided by the library of the University of Amsterdam (https://dare.uva.nl) UvA-DARE (Digital Academic Repository) Bifurcation routes to volatility clustering under evolutionary learning Gaunersdorfer, A.; Hommes, C.H.; Wagener, F.O.O. DOI 10.1016/j.jebo.2007.07.004 Publication date 2008 Document Version Author accepted manuscript Published in Journal of Economic Behavior & Organization Link to publication Citation for published version (APA): Gaunersdorfer, A., Hommes, C. H., & Wagener, F. O. O. (2008). Bifurcation routes to volatility clustering under evolutionary learning. Journal of Economic Behavior & Organization, 67(1), 27-47. https://doi.org/10.1016/j.jebo.2007.07.004 General rights It is not permitted to download or to forward/distribute the text or part of it without the consent of the author(s) and/or copyright holder(s), other than for strictly personal, individual use, unless the work is under an open content license (like Creative Commons). Disclaimer/Complaints regulations If you believe that digital publication of certain material infringes any 

### id `be7a2d37-c714-40ed-a3c1-dd76dea09fd1`

**Bitcoin intraday time series momentum** — Dehua Shen, Andrew Urquhart, Pengfei Wang, 2021

> Bitcoin intraday time-series momentum Article Accepted Version Shen, D., Urquhart, A. ORCID: https://orcid.org/0000-0001- 8834-4243 and Wang, P. (2022) Bitcoin intraday time-series momentum. Financial Review, 57 (2). pp. 319-344. ISSN 1540- 6288 doi: 10.1111/fire.12290 Available at https://centaur.reading.ac.uk/100181/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1111/fire.12290 Publisher: Wiley All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur CentAUR Central Archive at the University of Reading Reading’s research outputs online 1 Bitcoin Intraday Time-Series Momentum Abstract This study examines intraday time -series momentum in Bitcoin. Unlike stock markets, Bitcoin trades 24 hours a day and therefore has not got a clear opening and 

### id `861f7e22-40ea-4b23-a9fe-e307a1610fe2`

**Bitcoin is not the New Gold – A comparison of volatility, correlation, and portfolio performance** — Tony Klein, Hien Pham Thu, Thomas Walther, 2018

> Bitcoin is not the New Gold – A comparison of volatility, correlation, and portfolio performance Klein, T., Thu, H. P., & Walther, T. (2018). Bitcoin is not the New Gold – A comparison of volatility, correlation, and portfolio performance. International Review of Financial Analysis, 59, 105-116. https://doi.org/10.1016/j.irfa.2018.07.010 Published in: International Review of Financial Analysis Document Version: Peer reviewed version Queen's University Belfast - Research Portal: Link to publication record in Queen's University Belfast Research Portal Publisher rights Copyright 2018 Elsevier. This manuscript is distributed under a Creative Commons Attribution-NonCommercial-NoDerivs License (https://creativecommons.org/licenses/by-nc-nd/4.0/), which permits distribution and reproduction for non-commercial purposes, provided the author and source are cited General rights Copyright for the publications made accessible via the Queen's University Belfast Research Portal is retained by the author(s) and / or other copyright owners and it is a condition of accessing these publications that us

### id `6f5c6741-140b-4f7d-81ec-789b7af2b5fc`

**BORÇLANMA ARAÇLARI PİYASASINDA ÖĞLE ARASININ KALDIRILMASININ GÜNİÇİ GETİRİ, VOLATİLİTE VE İŞLEM HACMİNE ETKİSİ** — Eyüp Kadıoğlu, Nurcan ÖCAL, Faruk Bostanci, 2020

> 937 Balıkesir University The Journal of Social Sciences Institute Volume: 23 - Issue: 44, December 2020 Borçlanma Araçları Piyasasında Öğle Arasının Kaldırılmasının Güniçi Getiri, Volatilite ve İşlem Hacmine Etkisi Araştırma Makalesi / Research Article BORÇLANMA ARAÇLARI PİYASASINDA ÖĞLE ARASININ KALDIRILMASININ GÜNİÇİ GETİRİ, VOLATİLİTE VE İŞLEM HACMİNE ETKİSİ* Effect of Removing Lunch Break on Intraday Return, Volatility and Trading Volume in Debt Securities Market * Bu çalışmada, yöntem olarak insan ve hayvanlar deneysel ya da diğer bilimsel amaçlarla kullanılmadığı için etik kurul iznine ihtiyaç duyulmamıştır. ** Sorumlu Yazar / Corresponding Author 1 Doç. Dr., Sermaye Piyasası Kurulu/Yatırımcı Tazmin Merkezi, eyup.kadioglu@gmail.com, https://orcid.org/0000-0001-7836-868X 2 Dr., Sermaye Piyasası Kurulu/Yatırımcı Tazmin Merkezi, nurcan.ocal@spk.gov.tr, https://orcid.org/0000-0002-5870-2844 3 Dr., Bağımsız Araştırmacı, faruk.bostanci@gmail.com, https://orcid.org/0000-0002-4151-7618 Gönderim Tarihi / Received: 05.06.2020 Kabul Tarihi / Accepted: 03.09.2020 Doi: https://doi.org/10.31

### id `c6a3fd26-e1bd-4756-929f-87f436ccc346`

**Bubbles, crashes and intermittency in agent based market models** — Irene Giardina, J. P. Bouchaud, 2003

> arXiv:cond-mat/0206222v2 5 Jul 2002 BUBBLES, CRASHES AND INTERMITTENCY IN AGENT BASED MARKET MODELS Irene Giardina 1,2 and Jean-Philippe Bouchaud 3,4 1 Service de Physique Th´ eorique, Centre d’´ etudes de Saclay, Orme des Merisiers, 91191 Gif-sur-Yvette Cedex, France 2 Dipartimento di Fisica, Universit` a di Roma La Sapienza, Piazzale Aldo Moro 2, 00185 Roma, Italy 3 Service de Physique de l’ ´Etat Condens´ e, Centre d’´ etudes de Saclay, Orme des Merisiers, 91191 Gif-sur-Yvette Cedex, France 4 Science & Finance, CFM, 109-111 rue Victor-Hugo, 92532 Fran ce September 25, 2018 Abstract We deﬁne and study a rather complex market model, inspired fr om the Santa Fe artiﬁcial market and the Minority Game. Agents have diﬀerent strategies among which they can choose, according to their r elative prof- itability, with the possibility of not participating to the market. The price is updated according to the excess demand, and the wealth of t he agents is properly accounted for. Only two parameters play a signiﬁca nt role: one describes the impact of trading on the price, and the other de scri

### id `6a155e65-d6a2-42d0-8a3b-831fccb25dfc`

**Capital flows to emerging market economies: A brave new world?** — Shaghil Ahmed, Andrei Zlate, 2014

> Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 1081 June 2013 Capital Flows to Emerging Market Economies: A Brave New World? Shaghil Ahmed Andrei Zlate NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at www.federalreserve.gov/pubs/ifdp/. This paper can be downloaded without charge from the Social Science Research Network electronic library at www.ssrn.com. Capital Flows to Emerging Market Economies: A Brave New W orld?  Shaghil Ahmed Andrei Zlate Board of Governors of the F ederal Reserve System June 2013 Abstract We examine the determinants of net private capital in ows to emerging market economies. These in ows are computed from quarterly balance-of-payments data from 2002:Q1 to 2012:Q2. Our main ndings are: First, growth and inter

### id `7ac5f4bd-2d23-4d52-9f58-6f3e951356c1`

**Changes in consumers’ awareness and interest in cosmetic products during the pandemic** — Yeong-Hyeon Choi, Seong Eun Kim, Kyu‐Hye Lee, 2022

> Changes in consumers’ awareness and interest in cosmetic products during the pandemic Yeong‑Hyeon Choi1, Seong Eun Kim2 and Kyu‑Hye Lee1* Introduction The coronavirus disease‑19 (COVID‑19) is an infectious disease caused by the severe acute respiratory syndrome coronavirus‑2 (SARS ‑CoV‑2) (Babu, 2020). As the number of confirmed cases of COVID‑19 increased, the World Health Organization (WHO) announced a pandemic on March 11th, 2020. In an attempt to slow the pandemic, the WHO announced personal hygiene guidelines. Governments all over the world have induced people to follow the guidelines, which include regularly washing hands, social distancing, and wearing a medical mask (Cartaud et al., 2020). As the period of social Abstract This research investigates the impact of the COVID‑19 pandemic on consumers’ per‑ spectives of beauty and individual cosmetic products. Since the first confirmed case of COVID‑19 was announced on December 31st, 2019, the search volumes of Google News have been updated and information on confirmed cases of the disease has been collected. This study used Pytho

### id `73864b77-f4cc-4178-b9c7-a05361a96471`

**Complementarities, Multiplicity, and Supply Information** — Jayant Vivek Ganguli, Liyan Yang, 2009

> TSpace Research Repository tspace.library.utoronto.ca Complementarities, Multiplicity, and Supply Information Ja yant V. Ganguli & Liyan Yang Version Accepted Manuscript Citation (published version) Ganguli, J. V., & Yang, L. (2009). Complementarities, multiplicity, and supply information. Journal of the European Economic Association, 7(1), 90- 115. DOI https://doi.org/10.1162/JEEA.2009.7.1.90 Publisher’s Statement This article has been accepted for publication in the Journal of the European Economic Association. Published by Oxford University Press. Ho w to cite TSpace items A lways cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page. This article was made openly accessible by U of T Faculty. Please tell us how this access benefits you. Your story matters. Complement

### id `9ad47eb0-25bc-4c8d-9077-f6f369922774`

**Complexity theory and financial regulation** — Stefano Battiston, J. Doyne Farmer, Andreas Flache, Diego Garlaschelli, 2016

> UvA-DARE is a service provided by the library of the University of Amsterdam (https://dare.uva.nl) UvA-DARE (Digital Academic Repository) Complexity theory and financial regulation: economic policy needs interdisciplinary network analysis and behavioral modeling Battiston, S.; Farmer, J.D.; Flache, A.; Garlaschelli, D.; Haldane, A.G.; Heesterbeek, H.; Hommes, C.; Jaeger, C.; May, R.; Scheffer, M. DOI 10.1126/science.aad0299 Publication date 2016 Document Version Final published version Published in Science License Article 25fa Dutch Copyright Act (https://www.openaccess.nl/en/policies/open-access-in- dutch-copyright-law-taverne-amendment) Link to publication Citation for published version (APA): Battiston, S., Farmer, J. D., Flache, A., Garlaschelli, D., Haldane, A. G., Heesterbeek, H., Hommes, C., Jaeger, C., May, R., & Scheffer, M. (2016). Complexity theory and financial regulation: economic policy needs interdisciplinary network analysis and behavioral modeling. Science, 351(6275), 818-819. https://doi.org/10.1126/science.aad0299 General rights It is not permitted to download or t

### id `3a233eae-abaf-4c33-9765-cd367176048f`

**Contagion, Spillover, and Interdependence** — Roberto Rigobón, 2019

> 6 9 Contagion, Spillover, and Interdependence ABSTRACT This paper reviews the empirical literature on international spillovers and conta- gion. Theoretical models of spillover and contagion imply that the reduced-form observable variables suffer from two possible sources of bias: endogeneity and omitted variables. These econometric problems, in combination with the heteroskedasticity that plagues the data, produce time-varying biases. Several empirical methodologies are evaluated from this perspec- tive: nonparametric techniques, such as correlations and principal components; and parametric methods, such as OLS, V AR, event studies, ARCH, and nonlinear regressions. The paper con- cludes that there is no single technique that can solve the full-fledged problem and discusses three methodologies that can partially address some of the questions in the literature. JEL Codes: C30, F32, C10 Keywords: Identification, heteroskedasticity, contagion A lmost every paper on contagion starts with a definition of what exactly the author means by contagion and spillover. I would like this paper to b

### id `85ba9ae5-bc01-477b-bd4b-3c041652d0a1`

**Corporate Climate Risk: Measurements and Responses** — Qing Li, Hongyu Shan, Yuehua Tang, Vincent Wenxiong Yao, 2024

> © 2024 The Author(s). Published by Oxford University Press Disclaimer: This is the Author Accepted Manuscript (AAM) version . This version has been peer-reviewed and accepted, but has not been copyedited, formatted, or typeset by the publisher. The final published version may differ from this manuscript. This AAM is made available in accordance with the publisher’s self-archiving policy under the terms of CC BY- NC-ND 4.0 international license, solely for personal, non-commercial use. Under this license, you must give appropriate attribution, and reuse is restricted to non-commercial purposes with no derivatives permitted. Any commercial use requires prior permission from the copyright holder(s). CEIBS Institutional Repository Corporate Climate Risk: Measurements and Responses Qing Li, Hongyu Shan, Yuehua Tang, Vincent Yao Review of Financial Studies January 16, 2024 DOI: https://doi.org/10.1093/rfs/hhad094 This Author Accepted Manuscript is available from CEIBS Institutional Repository at https://repository.ceibs.cn/en/publications/corporate-climate-risk-measurements-and-responses/ 

### id `e45aa5e0-44d5-4fb9-abef-9837fd6e6500`

**Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression** — Ishaan Dawar, Anupam Dutta, Elie Bouri, Tareq Saeed, 2020

> This is a self -archived – parallel published version of this article in the publication archive of the University of Vaasa. It might differ from the original. Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression Author(s): Dawar, Ishaan; Dutta, Anupam; Bouri, Elie; Saeed, Tareq Title: Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression Year: 2021 Version: Accepted manuscript Copyright ©2021 Elsevier. This manuscript version is made available under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International (CC BY–NC–ND 4.0) license, https://creativecommons.org/licenses/by-nc-nd/4.0/ Please cite the original version: Dawar, I., Dutta, A., Bouri, E. & Saeed, T. (2021). Crude oil prices and clean energy stock indices: Lagged and asymmetric effects with quantile regression. Renewable Energy 163, 288-299. https://doi.org/10.1016/j.renene.2020.08.162 1 Crude oil prices and clean energy stock indices: lagged and asymmetric effects 1 with quantile regression 2 3 4 5 6 7 

### id `51a00669-7e8b-42c8-aa52-7734b6e3fcff`

**Cryptocurrencies and momentum** — Klaus Grobys, Niranjan Sapkota, 2019

> This is a self -archived – parallel published version of this article in the publication archive of the University of Vaasa. It might differ from the original. Cryptocurrencies and momentum Author(s): Grobys, Klaus; Sapkota, Niranjan Title: Cryptocurrencies and momentum Year: 2019 Version: Publisher’s PDF Copyright ©2019 The Authors. Published by Elsevier B.V. Open access article under the Creative Commons Attribution– NonCommercial–NoDerivatives 4.0 International (CC BY–NC– ND) license, http://creativecommons.org/licenses/by-nc- nd/4.0/ Please cite the original version: Grobys, K ., & Sapkota, N ., (2019). Cryptocurrencies and momentum. Economics letters 180(July), 6–10. https://doi.org/10.1016/j.econlet.2019.03.028 EconomicsLetters180(2019)6–10 Contents lists available at ScienceDirect EconomicsLetters journal homepage: www.elsevier.com/locate/ecolet Cryptocurrenciesandmomentum KlausGrobys1,NiranjanSapkota ∗,1 DepartmentofAccountingandFinance,UniversityofVaasa,Wolffintie34,65200Vaasa,Finland h i g h l i g h t s • Weexplorewhethermomentumdoesexistincryptocurrencymarkets. • Wefindtha

### id `ad97afbb-777d-426a-9516-61f169df9ad6`

**Decomposing socioeconomic inequalities in depressive symptoms among the elderly in China** — Yongjian Xu, Jinjuan Yang, Jianmin Gao, Zhongliang Zhou, 2016

> R E S E A R C H A R T I C L E Open Access Decomposing socioeconomic inequalities in depressive symptoms among the elderly in China Yongjian Xu 1, Jinjuan Yang 2, Jianmin Gao 1*, Zhongliang Zhou 1, Tao Zhang 3, Jianping Ren 3, Yanli Li 1, Yuyan Qian 2, Sha Lai 1 and Gang Chen 4* Abstract Background: Accelerated population ageing brings about un precedented challenges to the health system in China. This study aimed to measure the prevalence and the income-related inequality of depressive symptoms, and also identify the determinants of depressive symptom inequality among the elderly in China. Methods: Data were drawn from the second wave of the China Health and Retirement Longitudinal Study (CHARLS). Depressive symptoms were assessed wit h a 10-item Center for Epidemiologic Studies – Depression Scale (CES-D), which was preselected in CHARLS. The conce ntration index was used to measure the magnitude of income-related inequality in depressive symptoms. A de composition analysis, based on the logit model, was employed to quantify the contribution of each determinant to total inequality. R

### id `30f6cc8d-7105-4d2a-9072-e72ee4a636b8`

**Derivatives and Market (Il)liquidity** — Shiyang Huang, Bart Zhou Yueshen, Cheng Zhang, 2023

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 59, No. 1, Feb. 2024, pp. 157 – 194 © THE AUTHOR(S), 2023. PUBLISHED BY CAMBRIDGE UNIVERSITY PRESS ON BEHALF OF THE MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON doi:10.1017/S0022109023000224 Derivatives and Market (Il)liquidity Shiyang Huang The University of Hong Kong Faculty of Business and Economics huangsy@hku.hk Bart Z. Yueshen INSEAD b@yueshen.me Cheng Zhang University of Denver Daniels College of Business cheng.zhang161@du.edu (corresponding author) Abstract We study how derivatives (with nonlinear payoffs) affect the underlying asset ’s liquidity. In a rational expectations equilibrium, informed investors expect low conditional volatility and sell derivatives to the others. These derivative trades affect different investors ’ utility differently, possibly amplifying liquidity risk. As investors delta hedge their derivative positions, price impact in the underlying drops, suggesting improved liquidity, because informed trading is diluted. In contrast, effects on price reversal are ambiguous, depending on inv

### id `02438803-3309-486d-a80c-50751242ba5b`

**Do Energy Prices Respond to U.S. Macroeconomic News? A Test of the Hypothesis of Predetermined Energy Prices** — Lutz Kilian, Clara Vega, 2010

> Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 957 November 2008 Do Energy Prices Respond to U.S. Macroeconomic News? A Test of the Hypothesis of Predetermined Energy Prices Lutz Kilian and Clara Vega NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References in publications to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at ww.federalreserve.gov/pubs/ifdp/. This paper can be downloaded without charge from Social Science Research Network electronic library at http://www.sssrn.com. 2 Do Energy Prices Respond to U.S. Macroeconomic News? A Test of the Hypothesis of Predetermined Energy Prices Lutz Kilian Clara Vega University of Michigan and CEPR Federal Reserve Board November, 2008 Abstract: Models that treat innovations to the price of energy as predetermined with respect to U.S. macroeconomic a

### id `a95efdd6-a6cb-4975-9cb5-6f7b06eb8dc8`

**Does global economic uncertainty matter for the volatility and hedging effectiveness of Bitcoin?** — Libing Fang, Elie I. Bouri, Rangan Gupta, David Roubaud, 2018

> 1 Does Global Economic Uncertainty Matter for the Volatility and Hedging Effectiveness of Bitcoin?* Libing Fang School of Management and Engineering, Nanjing University, Nanjing, Jiangsu, China. Email: lbfang@nju.edu.cn Elie Bouri# USEK Business School, Holy Spirit University of Kaslik, Jounieh, Lebanon. Email: eliebouri@usek.edu.lb Rangan Gupta Department of Economics, University of Pretoria, Pretoria, 0002, South Africa. Email: rangan.gupta@up.ac.za David Roubaud Montpellier Business School, Montpellier, France. Email: d.roubaud@montpellier-bs.com Abstract We assess whether the long-run volatilities of Bitcoin, global equities, commodities, and bonds are affected by global economic policy uncertainty. Empirical results provide evidence supporting that, except fo r the case of bonds. We further examine whether the correlation between Bitcoin a nd global equities, commodities, and bonds are affected by global economic policy uncertain ty and the results reveal that global economic policy uncertainty has a negative si gnificant impact on the Bitcoin-bonds correlation, and a positive i

### id `34913c7d-75a4-48b8-ae87-ff2cb85fda27`

**Dynamic connectedness between stock markets in the presence of the COVID-19 pandemic: does economic policy uncertainty matter?** — Manel Youssef, Khaled Mokni, Ahdi Noomen Ajmi, 2021

> Dynamic connectedness between stock markets in the presence of the COVID‑19 pandemic: does economic policy uncertainty matter? Manel Youssef1, Khaled Mokni1,2* and Ahdi Noomen Ajmi3,4 Introduction Academics, policymakers, and investors have heated discussions over analyzing the con- nectedness between financial markets, but this analysis was recently reinforced by math- ematical and econometric tool development. These tools increased its importance by providing a comprehensive picture of market risk, credit risk, and macroeconomic and system risk evaluation (Gong et al. 2019) to support better decision-making (Kou et al. 2014). Furthermore, analyzing connectedness between financial assets, especially stocks, Abstract This study investigates the dynamic connectedness between stock indices and the effect of economic policy uncertainty (EPU) in eight countries where COVID-19 was most widespread (China, Italy, France, Germany, Spain, Russia, the US, and the UK) by implementing the time-varying VAR (TVP-VAR) model for daily data over the period spanning from 01/01/2015 to 05/18/2020. Resu

### id `76a8b843-2a24-4625-9fb3-bf87ca618b5d`

**Dynamic estimation of volatility risk premia and investor risk aversion from option-implied and realized volatilities** — Tim Bollerslev, Michael S. Gibson, Hao Zhou, 2010

> Finance and Economics Discussion Series Divisions of Research & Statistics and Monetary Affairs Federal Reserve Board, Washington, D.C. Dynamic Estimation of Volatility Risk Premia and Investor Risk Aversion from Option-Implied and Realized Volatilities Tim Bollerslev, Michael Gibson, and Hao Zhou 2004-56 NOTE: Staff working papers in the Finance and Economics Discussion Series (FEDS) are preliminary materials circulated to stimulate discussion and critical comment. The analysis and conclusions set forth are those of the authors and do not indicate concurrence by other members of the research staff or the Board of Governors. References in publications to the Finance and Economics Discussion Series (other than acknowledgement) should be cleared with the author(s) to protect the tentative character of these papers. Dynamic Estimation of Volatility Risk Premia and Investor Risk Aversion from Option-Implied and Realized Volatilities Tim Bollerslevy Michael Gibsonz Hao Zhoux First Draft: September 2004 The work of Bollerslev was supported by a grant from the National Science Foundation 

### id `006fa4dc-5406-4603-b43e-0d185a4dbd22`

**Dynamic spillovers between the term structure of interest rates, bitcoin, and safe-haven currencies** — David Y. Aharon, Zaghum Umar, Xuan Vinh Vo, 2021

> Dynamic spillovers between the term structure of interest rates, bitcoin, and safe‑haven currencies David Y. Aharon1, Zaghum Umar2,3* and Xuan Vinh Vo3 Introduction The outbreak of the COVID-19 pandemic in early 2020 reinvigorated the search for use - ful risk management, hedging strategies, and investors’ demand for safe-haven assets. Although traditionally major currencies have been regarded as safe-haven assets, several financial market downturns, such as the 2008 subprime crisis and the 2011 sovereign Abstract This study examines the connectedness between the US yield curve components (i.e., level, slope, and curvature), exchange rates, and the historical volatility of the exchange rates of the main safe-haven fiat currencies (Canada, Switzerland, EURO, Japan, and the UK) and the leading cryptocurrency, the Bitcoin. Results of the static analysis show that the level and slope of the yield curve are net transmitters of shocks to both the exchange rate and its volatility. The exchange rate of the Euro and the volatility of the Euro and the Canadian dollar exchange rate are net tran

### id `2f830f72-5dc1-4f35-9e8c-f1eab969d281`

**Empirical cross-sectional asset pricing: a survey** — Amit Goyal, 2011

> Financ Mark Portf Manag (2012) 26:3–38 DOI 10.1007/s11408-011-0177-7 Empirical cross-sectional asset pricing: a survey Amit Goyal Published online: 24 December 2011 © Swiss Society for Financial Market Research 2011 Abstract I review the state of empirical asset pricing devoted to understanding cross- sectional differences in average rates of return. Both methodologies and empirical evidence are surveyed. Tremendous progress has been made in understanding return patterns. At the same time, there is a need to synthesize the huge amount of collected evidence. Keywords Empirical asset pricing · Factor models · Time-series regressions · Cross-sectional regressions · Anomalies JEL Classiﬁcation G12 · G14 1 Introduction One of the central questions in ﬁnance is why different assets earn different rates of return. It has long been understood that while most of the day-to-day variation in returns may be due to constant arrival of information, asset pricing models can contribute to our understanding of why the average rates of return vary across secu- rities. All asset pricing models agree on

