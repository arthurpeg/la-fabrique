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

## LES PAPIERS — lot 2 sur 4

### id `a5bb4d9f-98a7-49f7-aa3d-f9a8776cae49`

**Ex-dividend day trading: Who, how, and why?** — Elias Henrikki Rantapuska, 2008

> HELSINKI SCHOOL OF ECONOMICS WORKING PAPERS W-392 Elias Rantapuska Ex-d I v I d EN d d A y t RA d ING : WHO , HOW , AN d WH y? W-392 ISSN 1235-5674 ISBN 951-791-978-6 (Electronic working paper) 2005 Elias Rantapuska Ex-dividEnd day tRading: who, how, and why? Finance november 2005 hELSingin KaUPPaKoRKEaKoULU hELSinKi SChooL oF EConoMiCS woRKing PaPERS w-392 © Elias Rantapuska and helsinki School of Economics iSSn 1235-5674 iSBn 951-791-978-6 (Electronic working paper) helsinki School of Economics - hSE Print 2005 hELSingin KaUPPaKoRKEaKoULU hELSinKi SChooL oF EConoMiCS PL 1210 Fin-00101 hELSinKi FinLand

### id `1f7493c7-e862-450a-82e6-ee8e2aa5356c`

**Exchange rate puzzles: A tale of switching attractors** — Paul De Grauwe, Marianna Grimaldi, 2004

> SVERIGES RIKSBANK WORKING PAPER SERIES Exchange Rate Puzzles: A Tale of Switching Attractors Paul De Grauwe and Marianna Grimaldi MAY 2004 163 WORKING PAPERS ARE OBTAINABLE FROM Sveriges Riksbank • Information Riksbank • SE-103 37 Stockholm Fax international: +46 8 787 05 26 Telephone international: +46 8 787 01 00 E-mail: info@riksbank.se The Working Paper series presents reports on matters in the sphere of activities of the Riksbank that are considered to be of interest to a wider public. The papers are to be regarded as reports on ongoing studies and the authors will be pleased to receive comments. The views expressed in Working Papers are solely the responsibility of the authors and should not to be interpreted as reflecting the views of the Executive Board of Sveriges Riksbank. Exchange rate puzzles: A tale of switching attractors Paul De Grauwe University of Leuven Marianna Grimaldi∗† Sveriges Riksbank Sveriges Riksbank W orking Paper Series No. 163 May 2004 Abstract The rational expectations e ﬃcient market model of the exchange rate has failed empirically. In this paper we de

### id `621c8800-eee3-45c6-9141-d87e086cac9b`

**Expectations and bubbles in asset pricing experiments** — Cars Hommes, Joep Sonnemans, Jan Tuinstra, Henk van de Velden, 2007

> UvA-DARE is a service provided by the library of the University of Amsterdam (https://dare.uva.nl) UvA-DARE (Digital Academic Repository) Expectations and bubbles in asset pricing experiments Hommes, C.; Sonnemans, J.; Tuinstra, J.; van de Velden, H. DOI 10.1016/j.jebo.2007.06.006 Publication date 2008 Document Version Author accepted manuscript Published in Journal of Economic Behavior & Organization Link to publication Citation for published version (APA): Hommes, C., Sonnemans, J., Tuinstra, J., & van de Velden, H. (2008). Expectations and bubbles in asset pricing experiments. Journal of Economic Behavior & Organization, 67(1), 116-133. https://doi.org/10.1016/j.jebo.2007.06.006 General rights It is not permitted to download or to forward/distribute the text or part of it without the consent of the author(s) and/or copyright holder(s), other than for strictly personal, individual use, unless the work is under an open content license (like Creative Commons). Disclaimer/Complaints regulations If you believe that digital publication of certain material infringes any of your rights or

### id `9991119b-97fb-4e24-a8ed-f2bb0fdec651`

**Exploiting the dynamics of commodity futures curves** — Robert J. Bianchi, John Hua Fan, Joëlle Miffre, Tingxi Zhang, 2023

> 1 Exploiting the dynamics of commodity futures curves Robert J. Bianchia, John Hua Fana, Joëlle Miffreb,c,, Tingxi Zhangd a. Griffith Business School, Griffith University, Brisbane, Australia b. Audencia Business School, 8 Route de la Jonelière, 44300, Nantes, France c. Louis Bachelier Fellow, Paris, France d. Curtin University, Perth, Australia Abstract The Nelson-Siegel framework is employed to model the term structure of commodity futures prices. Exploiting the information embedded in the level, slope and curvature parameters, we develop novel investment strategies that assume short -term continuation of recent parallel, slope or butterfly movements of futures curves. Systematic strategies based on the change in the slope generate significant profits that are unrelated to previously documented risk factors and can survive reasonable transaction costs. Further analysis demonstrates that t he profitability of the slope strategy increases with investor sentiment and is in part a compensation for the drawdowns incurred during economic slowdowns. The profitability can also be magnifie

### id `e556381b-06a7-44d0-aad5-a1cd9802e0db`

**Exploring the predictability of intraday returns in China's stock market** — Yanbing Xu, 2022

> BCP Business & Management FMEME 2022 Volume 30 (2022) 735 Exploring the predictability of intraday returns in China's stock market Yanbing Xu* Nanjing University of Science and Technology, Jiangsu, China *Corresponding author: 1067615488@qq.com Abstract. With the rapid development of high-frequency trading, intraday trading has become more and more popular due to its important role in understanding the efficiency of the intraday market and capturing more trading opportunities. This article explores whether there is momentum effect and reversal effect in China’s stock market by studying the correlation and predictability between half - hour returns. The results show that there is an intraday momentum effect between the first half-hour and full -day returns. After the investment strategy, it is found that this effect has economic significance, but after considering the transaction costs, the momentum effect cannot make investors obtain excess returns. These costs are the reason for the long-term predictability of intraday returns. Keywords: Intraday returns predictability, Trading cost

### id `1ec821cc-2b62-4cb8-95e7-ecd6a2600bea`

**Financial Exchange Rates and International Currency Exposures** — Philip R. Lane, Jay Shambaugh, 2010

> NBER WORKING PAPER SERIES FINANCIAL EXCHANGE RATES AND INTERNATIONAL CURRENCY EXPOSURES Philip Lane Jay C. Shambaugh Working Paper 13433 http://www.nber.org/papers/w13433 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 September 2007 We thank Patrick Honohan, Ted Truman, Pinar Yesin and the participants in the CGFS workshop on "The Use of BIS International Financial Statistics," the Dartmouth College Junior Seminar, NBER IFM Lunch Group and seminars at the Bank of England, European Central Bank, University of California - Davis, University of Siena and the University of Wisconsin. We are grateful to Philippe Mesny and Dennis Petre for the provision of data from the BIS and Ted Truman for generously sharing his data on reserves and helpful comments. Agustin Benetrix, Vahagn Galstyan and Barbara Pels provided excellent research assistance. Lane's work on this paper is supported by the HEA-PRTLI grant to the IIIS. This work began while Shambaugh was a visiting scholar at the IIIS and his work on this paper is supported by the Rockefeller Center at Dart

### id `200375ba-be5e-4b05-837b-76cc336aae54`

**Forecasting oil price realized volatility using information channels from other asset classes** — Stavros Degiannakis, George Filis, 2017

> 1 Forecasting oil price realized volatility using information channels from other asset classes Stavros Degiannakis1,2 and George Filis1,3,* 1Department of Economics and Regional Development, Panteion University of Social and Political Sciences, 136 Syggrou Avenue, 17671, Greece. 2Postgraduate Department of Business Administration, Hellenic Open University, Aristotelous 18, 26 335, Greece. 3Department of Accounting, Finance and Economics, Bournemouth University, BH8 8EB, United Kingdom. *Corresponding author: email: gfilis@bournemouth.ac.uk Abstract Motivated from Ross (1989) who maintains that asset volatilities are synonymous to the information flow, we claim that cross -market volatility transmission effects are synonymous to cross -market information flows or “information channels” from one market to another. Based on this assertion we assess whether cross-market volatility flows contain important information that can improve the accuracy of oil price realized volatility forecasting . We concentrate on realized volatilities derived from the intra-day prices of the Brent crude oil

### id `b69200a9-5bd9-4d95-b552-26a8cff4de13`

**Foreign Safe Asset Demand and the Dollar Exchange Rate** — Zhengyang Jiang, Arvind Krishnamurthy, Hanno Lustig, 2021

> NBER WORKING PAPER SERIES FOREIGN SAFE ASSET DEMAND AND THE DOLLAR EXCHANGE RATE Zhengyang Jiang Arvind Krishnamurthy Hanno Lustig Working Paper 24439 http://www.nber.org/papers/w24439 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 March 2018 We thank Chloe Peng and Ziqing Wang for excellent research assistance. We also thank Mark Aguiar, Mike Chernov, Magnus Dahlquist, Wenxin Du (discussant), Greg Du□ee, Charles Engel, Emmanuel Farhi, Maury Obstfeld (discussant), Pierre-Olivier Gourinchas (discussant), Ben Hébert, Zhiguo He (discussant), Oleg Itskhoki, Matteo Maggiori, Brent Neiman, Alexi Savov, Jesse Schreger (discussant), Lukas Schmid (discussant), Dongho Song (discussant), Jeremy Stein, Adrien Verdelhan and Stanley Zin for helpful discussions, and seminar participants at the BIS, Carnegie Mellon, Chicago Booth, Columbia, Harvard Business School, Northwestern Kellogg, New York Fed, NYU, Ohio State, San Francisco Fed, Stanford, UT-Austin and UC-Boulder as well as the participants at CESifo Area Conference, the NBER SI IFM 2018, Vienna Symposium o

### id `1f5e4cfb-9ad5-468c-a4d3-0ffb5df5508e`

**From the bird's eye to the microscope: A survey of new stylized facts of the intra-daily foreign exchange markets** — Dominique Guillaume, Michel M. Dacorogna, Rakhal Dave, Ulrich Müller, 1997

> Finance Stochast. 1, 95–129 (1997) c⃝ Springer-V erlag 1997 From the bird’s eye to the microscope: A survey of new stylized facts of the intra-daily foreign exchange markets ⋆ Dominique M. Guillaume 1, Michel M. Dacorogna 2, Rakhal R. Dav ´e2, Ulrich A. M ¨uller2, Richard B. Olsen 2, Olivier V. Pictet 2 1 Financial Markets Group, London School of Economics and C.S.A.E. Institute of Economics and Statistics, University of Oxford, St. Cross Building, Manor Road, Oxford OX1 3UL, United Kingdom (e-mail: dominique.guillaume@economics.ox.ac.uk) 2 Olsen & Associates, Research Institute for Applied Economics, CH-8008 Z ¨urich, Switzerland Abstract. This paper presents stylized facts concerning the spot intra-daily for- eign exchange markets. It ﬁrst describes intra-daily data and proposes a set of deﬁnitions for the variables of interest. Empirical regularities of the foreign ex- change intra-daily data are then grouped under three major topics: the distribution of price changes, the process of price formation and the heterogeneous structure of the market. The stylized facts surveyed in this

### id `e45a0f06-858e-46b1-aefd-ebabc6177f23`

**Gamma positioning and market quality** — Boyd Buis, Mary Pieterse-Bloem, Willem F. C. Verschoor, Remco C. J. Zwinkels, 2024

> EUR Research Information Portal Gamma positioning and market quality Published in: Journal of Economic Dynamics and Control Publication status and date: Published: 01/07/2024 DOI (link to publisher): 10.1016/j.jedc.2024.104880 Document Version Publisher's PDF, also known as Version of record Document License/Available under: CC BY Citation for the published version (APA): Buis, B., Pieterse-Bloem, M., Verschoor, W. F. C., & Zwinkels, R. C. J. (2024). Gamma positioning and market quality. Journal of Economic Dynamics and Control, 164, Article 104880. https://doi.org/10.1016/j.jedc.2024.104880 Link to publication on the EUR Research Information Portal Terms and Conditions of Use Except as permitted by the applicable copyright law, you may not reproduce or make this material available to any third party without the prior written permission from the copyright holder(s). Copyright law allows the following uses of this material without prior permission: • you may download, save and print a copy of this material for your personal use only; • you may share the EUR portal link to this materia

### id `568d53c1-189d-46c2-b869-d84c6b05e510`

**GIS and spatial data analysis: Converging perspectives** — Michael F. Goodchild, Robert Haining, 2003

> © Investigaciones Regionales. 6 – Páginas 175 a 201 Sección PANORAMA Y DEBATES SIG y análisis espacial de datos: perspectivas convergentes* Michael F. Goodchild1 y Robert P. Haining2 RESUMEN: En este artículo se identifican algunos de los desarrollos más importan- tes experimentados por los SIG y el análisis espacial de datos desde los inicios de los 50. Aunque tanto los SIG como el análisis espacial de datos comenzaron como dos áreas de investigación y aplicación más o menos separadas, han crecido unidos estre- chamente a lo largo del tiempo. En el trabajo se mantiene que estas dos disciplinas se unen en el terreno de la Ciencia de la Información Geográfica, proporcionando cada una de ellas apoyo o añadiendo valor a la otra. El artículo comienza proporcionando una visión crítica retrospectiva de los desarrollos que han tenido lugar en los últimos cincuenta años. A continuación, se reflexiona acerca de los desafíos actuales y se es- pecula sobre el futuro. Por último se comenta el potencial de convergencia del desa- rrollo de los SIG y del análisis espacial de datos bajo la rubrica d

### id `665f3cdc-7773-4e43-9dc8-d1e6fcbf6e23`

**Gold and oil prices: abnormal returns, momentum and contrarian effects** — Guglielmo Maria Caporale, Alex Plastun, 2021

> Vol.:(0123456789) Financial Markets and Portfolio Management (2021) 35:353–368 https://doi.org/10.1007/s11408-021-00380-w 1 3 Gold and oil prices: abnormal returns, momentum and contrarian effects Guglielmo Maria Caporale1 · Alex Plastun2 Accepted: 6 February 2021 / Published online: 5 April 2021 © The Author(s) 2021 Abstract This paper explores price (momentum and contrarian) effects and their timing parameters on the days characterised by abnormal returns and the following ones in two commodity markets. Specifically, using daily gold and oil price data over the period 01.01.2009–31.03.2020 the following hypotheses are tested: (H1) there is a time gap between the detection of an abnormal return day and the end of that day, (H2) there are price effects on the day after abnormal returns occur; (H3) price effects after 1-day abnormal returns have identifiable timing parameters; (H4) the detected timing parameters can be used to “beat the market”. For these purposes average analysis, t tests, CAR and trading simulation approaches are used. The main results can be summarised as follows. 

### id `ea408397-9c90-4885-a35a-3a82fc55d137`

**Hedging emerging market stock prices with oil, gold, VIX, and bonds: A comparison between DCC, ADCC and GO-GARCH** — Syed Abul Basher, Perry Sadorsky, 2015

> Munich Personal RePEc Archive Hedging emerging market stock prices with oil, gold, VIX, and bonds: A comparison between DCC, ADCC and GO-GARCH Syed Abul, Basher and Perry, Sadorsky 6 December 2015 Online at https://mpra.ub.uni-muenchen.de/68231/ MPRA Paper No. 68231, posted 08 Dec 2015 09:21 UTC 1 Hedging emerging market stock prices with oil, gold, VIX, and bonds: A comparison between DCC, ADCC and GO-GARCH Syed Abul Basher Department of Economics, East West University, Plot No-A/2, Aftabnagar Main Road, Dhaka 1219, Bangladesh and Fikra Research & Policy, P.O. Box 2664, Doha, Qatar Email: syed.basher@gmail.com Perry Sadorsky Schulich School of Business York University 4700 Keele Street Toronto, Ontario, Canada M3J 1P3 Email: psadorsk@schulich.yorku.ca Telephone: +1 416 736 5067 Fax: +1 416 736 5687 October 2014, revised June 2015 Abstract While much research uses multivariate GARCH to model volatility dynamics and risk measures, one particular type of multivariate GARCH model, GO-GARCH, has been underutilized. This paper uses DCC, ADCC and GO-GARCH to model volatilities and conditio

### id `92254437-6808-478d-b857-e3f0520728e1`

**High Frequency Return and Risk Patterns in U.S. Sector ETFs during COVID-19** — Ikhlaas Gurrib, Firuz Kamalov, Elgilani E. Alshareif, 2022

> International Journal of Energy Economics and Policy | V ol 12 • Issue 5 • 2022 441 International Journal of Energy Economics and Policy ISSN: 2146-4553 available at http: www.econjournals.com International Journal of Energy Economics and Policy, 2022, 12(5), 441-456. High Frequency Return and Risk Patterns in U.S. Sector ETFs during COVID-19 Ikhlaas Gurrib1*, Firuz Kamalov2, Elgilani E. Alshareif3 1Faculty of Management, School of Graduate Studies, Canadian University Dubai, UAE, 2Faculty of Engineering and Architecture, Canadian University Dubai, UAE, 3Faculty of Management, School of Graduate Studies, Canadian University Dubai, UAE. *Email: ikhlaas@cud.ac.ae Received: 22/03/2022 Accepted: 25/07/2022 DOI: https://doi.org/10.32479/ijeep.13045 ABSTRACT This study investigates intraday patterns in the eleven sectors of the United States (U.S.). Key contributions are (i) risk and return patterns at specific trading periods on the New Y ork Stock Exchange (NYSE), (ii) whether a specific day return model can predict the next 15-min positive return, and (iii) the impact of the first vacci

### id `6c07d710-e89c-447f-accb-85e7baa42929`

**High frequency volatility co-movements in cryptocurrency markets** — Paraskevi Katsiampa, Shaen Corbet, Brian M. Lucey, 2019

> High frequency volatility co-movements in cryptocurrency markets Paraskevi Katsiampaa, Shaen Corbetb∗, Brian Luceyc,d,e aSheﬃeld University Management School, The University of Sheﬃeld, Conduit road, Sheﬃeld, S10 1FL, UK bDCU Business School, Dublin City University, Dublin 9 cTrinity Business School, Trinity College Dublin, Dublin 2 dUniversity of Sydney Business School, H70, Abercrombie St & Codrington St, Darlington NSW 2006, Australia eInstitute of Business Research, University of Economics Ho Chi Minh City, 59C Nguyen Dinh Chieu, Ward 6, District 3, Ho Chi Minh City, Vietnam Abstract Through the application of Diagonal BEKK and Asymmetric Diagonal BEKK method- ologies to intra-day data for eight cryptocurrencies, this paper investigates not only condi- tional volatility dynamics of major cryptocurrencies, but also their volatility co-movements. We ﬁrst provide evidence that all conditional variances are signiﬁcantly aﬀected by both previous squared errors and past conditional volatility. It is also shown that both method- ologies indicate that cryptocurrency investors pay the mos

### id `93b20069-4e88-4117-8e40-583b840c1831`

**How online discussion board activity affects stock trading: the case of GameStop** — André Betzer, Jan Philipp Harries, 2022

> Financial Markets and Portfolio Management (2022) 36:443–472 https://doi.org/10.1007/s11408-022-00407-w How online discussion board activity affects stock trading: the case of GameStop André Betzer 1 · Jan Philipp Harries 1 Accepted: 7 February 2022 / Published online: 30 March 2022 © The Author(s) 2022 Abstract In January 2021, the stock price of NASDAQ-listed GameStop Corporation surged more than twenty-fold for no discernible economic reason. Many observers attributed this broadly covered rise to retail investors, organizing themselves in Reddit’s WallStreetBets community. While Social Media-organized trading is not a new phe- nomenon, the magnitude of the resulting swings in the share price and surge in trading volume of GameStop is unprecedented. Using ﬁnancial data, as well as an exten- sive dataset of Reddit posts, we provide empirical evidence for the relationship of Reddit posts and GameStop (retail) trading. While we ﬁnd a signiﬁcant and positive relationship between Reddit posts and various trading measures in the following 30- min window in accordance with an attention-ba

### id `1374d099-f7d5-4c9a-b7f6-af0526a649d1`

**Impact of COVID-19 Pandemic on Financial Markets: a Global Perspective** — Sabeeh Ullah, 2022

> Vol:.(1234567890) Journal of the Knowledge Economy (2023) 14:982–1003 https://doi.org/10.1007/s13132-022-00970-7 1 3 Impact of COVID‑19 Pandemic on Financial Markets: a Global Perspective Sabeeh Ullah1 Received: 28 September 2021 / Accepted: 22 January 2022 / Published online: 3 February 2022 © The Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature 2022 Abstract This study aims to examine the influence of the COVID-19 outbreak on daily mar - ket returns in most affected developed and emerging markets. For this purpose, panel data of 30 most affected developed and emerging markets over the period Jan- uary 1, 2020, to December 12, 2020, were analyzed by using panel estimated gen- eralized least square (panel-EGLS) and panel quantile regression approaches. The results confirm that the new COVID-19 daily cases and deaths adversely impact daily market returns around the globe. Also, the positive rate of new COVID-19 cases has also negatively influenced market returns. Further, the number of new COVID-19 daily tests conducted has a positive

### id `dd4ec88c-3778-436d-916d-d84d4aebc41c`

**Impact of trading hours extensions on foreign exchange volatility: intraday evidence from the Moscow exchange** — Michael Frömmel, Eyüp Kadıoğlu, 2023

> Open Access © The Author(s) 2023. Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the mate- rial. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http:// creat iveco mmons. org/ licen ses/ by/4. 0/. RESEARCH Frömmel and Kadioglu Financial Innovation (2023) 9:95 https://doi.org/10.1186/s40854-023-00500-7 Financial Innovation Impact of trading hours extensions on foreign exchange volatility: intraday ev

### id `dda01a65-ed88-4981-b59c-fbd224152a37`

**Information Flows in Foreign Exchange Markets: Dissecting Customer Currency Trades** — Lukas Menkhoff, Lucio Sarno, Maik Schmeling, Andreas Schrimpf, 2016

> Copyright and Reuse: Copyright and Moral Rights remain with the author(s) and/or copyright holders. Copies of full items can be used for personal research or study, educational, or not-for-profit purposes without prior permission or charge, unless otherwise indicated, provided that the authors, title and full bibliographic details are credited, a hyperlink and/or URL is given for the original metadata page and the content is not changed in any way. For full details of reuse please refer to City Research Online policy. City Research Online: http://openaccess.city.ac.uk/ publications@citystgeorges.ac.uk Citation: Menkhoff, L., Sarno, L., Schmeling, M. & Schrimpf, A. (2016). Information flows in foreign exchange markets: Dissecting customer currency trades. Journal of Finance, 71(2), pp. 601-634. doi: 10.1111/jofi.12378 This is the accepted version of the paper. This version of the publication may differ from the final published version. To cite this item please consult the publisher's version. Permanent repository link: https://openaccess.city.ac.uk/id/eprint/13781/ Link to published v

### id `27a6d2e5-17d1-4a6b-b555-b12e0652dd24`

**Information leadership in the advanced Asia–Pacific stock markets: Return, volatility and volume information spillovers from the US and Japan** — Suk‐Joong Kim, 2004

> Information leadership in the advanced Asia-Pacific stock markets: Return, volatility and volume information spillovers from the US and Japan Author: Kim, Suk-Joong Publication details: Journal of the Japanese and International Economies v. 19 Chapter No. 3 pp. 338-365 0889-1583 (ISSN) Publication Date: 2005 Publisher DOI: http://dx.doi.org/10.1016/j.jjie.2004.03.002 License: https://creativecommons.org/licenses/by-nc-nd/3.0/au/ Link to license to see what you are allowed to do with this resource. Downloaded from http://hdl.handle.net/1959.4/40149 in https:// unsworks.unsw.edu.au on 2026-09-22 Information leadership in the advanced Asia-Pacific stock markets: Return, volatility and volume information spillovers from the U.S. and Japan Suk-Joong Kim School of Banking and Finance The University of New South Wales UNSW SYDNEY NSW 2052 Australia Tel: +61 2 9385-4278 Fax: + 61 2 9385-6347 Email: s.kim@unsw.edu.au Abstract: This paper investigates the nature of the stock ma rket linkages in the advanced Asia-Pacific stock markets of Australia, Hong Kong, Japan and Singapore with the U.S an

### id `f94a74c7-f3d8-4b6c-9eb8-db822ec41e48`

**Information Shocks, Liquidity Shocks, Jumps, and Price Discovery: Evidence from the U.S. Treasury Market** — George J. Jiang, Ingrid Lo, Adrien Verdelhan, 2010

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 46, No. 2, Apr. 2011, pp. 527–551 COPYRIGHT 2011, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109010000785 Information Shocks, Liquidity Shocks, Jumps, and Price Discovery: Evidence from the U.S. T reasury Market George J. Jiang, Ingrid Lo, and Adrien Verdelhan ∗ Abstract In this paper, we identify jumps in U.S. Treasury-bond (T-bond) prices and investigate what causes such unexpected large price changes. In particular, we examine the relative importance of macroeconomic news announcements versus variation in market liquidity in explaining the observed jumps in the U.S. Treasury market. We show that while jumps oc- cur mostly at prescheduled macroeconomic announcement times, announcement surprises have limited power in explaining bond price jumps. Our analysis further shows that pre- announcement liquidity shocks, such as changes in the bid-ask spread and market depth, have signiﬁcant predictive power for jumps. The predictive power is signiﬁcant even after controlling for infor

### id `53e0f935-b290-4ac4-b4b7-a82db05f1444`

**Informed and Strategic Order Flow in the Bond Markets** — Paolo Pasquariello, Clara Vega, 2007

> Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 874 September 2006 Informed and Strategic Order Flow in the Bond Markets Paolo Pasquariello and Clara Vega NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References in publications to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at www.federalreserve.gov/pubs/ifdp/. Informed and Strategic Order Flow in the Bond Markets Paolo Pasquariello and Clara Vega* Abstract We study the role played by private and public info rmation in the process of price formation in the U.S. Treasury bond market. To guide our analysis, we develop a parsimonious model of speculative trading in the presence of two realistic market frictions – info rmation heterogeneity and imperfect competition among informed traders – and a public signal. We test its equilibrium implication

### id `ed543af4-64af-4338-a84d-261738c13992`

**Intermediary asset pricing: New evidence from many asset classes** — Zhiguo He, Bryan Kelly, Asaf Manela, 2017

> NBER WORKING PAPER SERIES INTERMEDIARY ASSET PRICING: NEW EVIDENCE FROM MANY ASSET CLASSES Zhiguo He Bryan Kelly Asaf Manela Working Paper 21920 http://www.nber.org/papers/w21920 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 January 2016 We thank Markus Brunnermeier, Ian Dew-Becker, Valentin Haddad, Arvind Krishnamurthy, Alan Moreira, Tyler Muir, Lasse Pedersen, Alexi Savov, Rob Vishny, seminar participants at Stanford University, Penn State University, University of Iowa, Emory University, London School of Economics, London Business School, University of Houston, University of Washington, University of Oklahoma, Washington University, Gerzensee Summer School 2015, CITE 2015, NBER AP 2015, and Chicago Booth Asset Pricing Conference 2015 for helpful comments. The views expressed herein are those of the authors and do not necessarily reflect the views of the National Bureau of Economic Research. NBER working papers are circulated for discussion and comment purposes. They have not been peer- reviewed or been subject to the review by the NBER Board of

### id `12f0893f-df7b-4c7b-803d-0582615b0f71`

**Intraday analysis of regulation change in microstructure: evidence from an emerging market** — Eyüp Kadıoğlu, 2021

> International Journal of Emerging Markets Intraday Analysis of Regulation Change in Microstructure: Evidence from an Emerging Market Journal: International Journal of Emerging Markets Manuscript ID IJOEM-11-2020-1310.R2 Manuscript Type: Research Article Keywords: intraday trading volume, intraday volatility, intraday pattern, market microstructures, mixture of distribution hypothesis, Borsa Istanbul Equity Market http://mc.manuscriptcentral.com/ijoem International Journal of Emerging Markets International Journal of Emerging MarketsIntraday Analysis of Regulation Change in Microstructure: Evidence from an Emerging Market Abstract Purpose: This study investigates the impact that simultaneously replacing both midday single-price call auction and lunch break with multi-price continuous trading had on intraday volatility-volume patterns as well as the intraday volatility-volume nexus. Methodology: The analysis utilizes 150 million tick-by-tick transaction data related to 333 stocks traded on Borsa Istanbul Equity Market covering period of 2 months prior to and following the change. In ad

### id `e0d1d45e-6c9e-464a-b88c-d69613addbca`

**Intraday time series momentum: Global evidence and links to market characteristics** — Zeming Li, Αθανάσιος Σάκκας, Andrew Urquhart, 2021

> Intraday time series momentum: global evidence and links to market characteristics Article Accepted Version Creative Commons: Attribution-Noncommercial-No Derivative Works 4.0 Li, Z., Sakkas, A. and Urquhart, A. ORCID: https://orcid.org/0000-0001-8834-4243 (2022) Intraday time series momentum: global evidence and links to market characteristics. Journal of Financial Markets, 57. 100619. ISSN 1386-4181 doi: 10.1016/j.finmar.2021.100619 Available at https://centaur.reading.ac.uk/95566/ It is advisable to refer to the publisher’s version if you intend to cite from the work. See Guidance on citing . To link to this article DOI: http://dx.doi.org/10.1016/j.finmar.2021.100619 Publisher: Elsevier All outputs in CentAUR are protected by Intellectual Property Rights law, including copyright law. Copyright and IPR is retained by the creators or other copyright holders. Terms and conditions for use of this material are defined in the End User Agreement . www.reading.ac.uk/centaur Intraday Time Series Momentum: International Evidence Zeming Lia,∗, Athanasios Sakkasb, Andrew Urquhart c aSouthampt

### id `4be26a7b-0e0e-4c2d-899d-55092d7184ff`

**Intraday volatility transmission among precious metals, energy and stocks during the COVID-19 pandemic** — Saqib Farid, Ghulam Mujtaba, Muhammad Abubakr Naeem, Syed Jawad Hussain Shahzad, 2021

> RaY Research at the University of York St John For more information please contact RaY at ray@yorksj.ac.uk Farid, Saqib, Mujtaba, Ghulam, Abubakr Naeem, Muhammad and Jawad Hussain Shahzad, Syed (2021) Intraday volatility transmission among precious metals, energy and stocks during the COVID-19 pandemic. Resources Policy, 72 (102101). Downloaded from: https://ray.yorksj.ac.uk/id/eprint/10039/ The version presented here may differ from the published version or version of record. If you intend to cite from the work you are advised to consult the publisher's version: http://dx.doi.org/10.1016/j.resourpol.2021.102101 Research at York St John (RaY) is an institutional repository. It supports the principles of open access by making the research outputs of the University available in digital form. Copyright of the items stored in RaY reside with the authors and/or other copyright owners. Users may access full text items free of charge, and may download a copy for private study or non-commercial research. For further reuse terms, see licence terms governing individual outputs. Institutional R

### id `5ad30fc1-2e3e-4f99-9b3e-38414c8bfc41`

**Investor clientele and intraday patterns in the cross section of stock returns** — Jian Chen, Ahmad Haboub, Ali Shakil Khan, Syed F. Mahmud, 2024

> Vol.:(0123456789) Review of Quantitative Finance and Accounting https://doi.org/10.1007/s11156-024-01319-8 ORIGINAL RESEARCH Investor clientele and intraday patterns in the cross section of stock returns Jian Chen1 · Ahmad Haboub2 · Ali Khan2 · Syed Mahmud3 Accepted: 20 June 2024 © The Author(s) 2024 Abstract This paper examines the existence of a well documented (Heston et al. in J Finance 65:1369–1407) (hereafter HKS 2010) intraday momentum pattern in the cross section of stock returns for three previously un-examined markets outside the US—UK, China and Brazil. While the stocks in UK and Brazil exhibit the pattern, the evidence from China is lacklustre. We utlitlize the presence of dual listed A-shares (dominated by domestic retail investors) and their B- and H-share counterparts (dominated by foreign institutional inves- tors) of the same firms which provide a natural experiment setting to analyse the impact of investor clientele on the proliferation of HKS (2010) pattern. Our findings indicate that pat- tern is much weaker in A-shares (owned mostly by domestic retail investors) 

### id `7f13914b-f743-43bf-84db-6cfb8572a49f`

**Investor sentiment and the cross-section of stock returns: new theory and evidence** — Wenjie Ding, Khelifa Mazouz, Qingwei Wang, 2018

> Vol.:(0123456789) Review of Quantitative Finance and Accounting (2019) 53:493–525 https://doi.org/10.1007/s11156-018-0756-z 1 3 ORIGINAL RESEARCH Investor sentiment and the cross‑section of stock returns: new theory and evidence Wenjie Ding1,3 · Khelifa Mazouz1 · Qingwei Wang1,2 Published online: 8 October 2018 © The Author(s) 2018 Abstract We extend the noise trader risk model of Delong et al. (J Polit Econ 98:703–738, 1990) to a model with multiple risky assets to demonstrate the effect of investor sentiment on the cross-section of stock returns. Our model formally demonstrates that market-wide senti - ment leads to relatively higher contemporaneous returns and lower subsequent returns for stocks that are more prone to sentiment and difficult to arbitrage. Our extended model is consistent with the existing empirical evidence on the relationship between sentiment and cross-sectional stock returns. Guided by the extended model, wen also decompose investor sentiment into long- and short-run components and predict that long-run sentiment nega - tively associates with the cross-sectiona

### id `8a226735-84d5-4ad8-9708-686d47f93761`

**Is the Potential for International Diversification Disappearing? A Dynamic Copula Approach** — Peter Christoffersen, Vihang R. Errunza, Kris Jacobs, Hugues Langlois, 2012

> TSpace Research Repository tspace.library.utoronto.ca Is the Potential for International Diversification Disappearing? A Dynamic Copula Approach Peter Christoffersen, Vihang Errunza, Kris Jacobs, Huges Langlois Version Accepted Manuscript Citation (published version) Christoffersen, P., Errunza, V., Jacobs, K., Langlois, H. (2012). Is the Potential for International Diversification Disappearing? A Dynamic Copula Approach, The Review of Financial Studies, Volume 25, Issue 12. Pages 3711-3751, https://doi.org/10.1093/rfs/hhs104 DOI https://doi.org/10.1093/rfs/hhs104 Publisher’s Statement This article has been accepted for publication in The Review of Financial Studies Published by Oxford University Press. How to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found 

### id `90e259ed-ff32-47da-89fd-6ba487c5ea53`

**LEARNING IN COBWEB EXPERIMENTS** — Cars Hommes, Joep Sonnemans, Jan Tuinstra, Henk van de Velden, 2007

> Macroeconomic Dynamics, 11 (Supplement 1), 2007, 8–33. Printed in the United States of America. DOI: 10.1017/S1365100507060208 ARTICLES LEARNING IN COBWEB EXPERIMENTS CARS HOMMES,J OEP SONNEMANS,J AN TUINSTRA, AND HENK VAN DE VELDEN University of Amsterdam Different theories of expectation formation and learning usually yield different outcomes for realized market prices in dynamic models. The purpose of this paper is to investigate expectation formation and learning in a controlled experimental environment. Subjects are asked to predict the next period’s aggregate price in a dynamic commodity market model with feedback from individual expectations. Subjects have no information about underlying market equilibrium equations, but can learn by observing past price realizations and predictions. We conduct a stable, an unstable, and a strongly unstable treatment. In the stable treatment, rational expectations (RE) yield a good description of observed aggregate price ﬂuctuations: prices remain close to the RE steady state. In the unstable treatments, prices exhibit large ﬂuctuations around

