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

## LES PAPIERS — lot 3 sur 4

### id `59ae65b7-9acf-4369-84db-06fb3ed62b3f`

**Limits of arbitrage and their impact on market efficiency: Evidence from China** — Jian Chen, Ahmad Haboub, Ali Shakil Khan, 2023

> Global Finance Journal 59 (2024) 100916 Available online 30 November 2023 1044-0283/Â© 2023 The Authors. Published by Elsevier Inc. This is an open access article under the CC BY-NC-ND license ( http://creativecommons.org/licenses/by-nc-nd/4.0/). Limits of arbitrage and their impact on market efficiency: Evidence from China Jian Chen a , * , Ahmad Haboub b , Ali Khan b a Nottingham University Business School, Department of Finance, Risk and Banking, C-23, South Building, Jubilee Campus, Nottingham, United Kingdom b Faculty of Business and Law, Accounting and Finance Division, Northampton NN1 5PH, United Kingdom ARTICLE INFO JEL classification: E44 F65 G12 G14 G15 and G23 Keywords: Limits of arbitrage Market efficiency Chinese stock market Intraday return predictability And high-frequency trading ABSTRACT This paper examines the impact of limits of arbitrage (LOA) on market efficiency by considering a large sample of Chinese stocks. Intraday market efficiency is measured using two widely used measures: the intraday return predictability measure and the variance ratio measure. We find 

### id `a0b6608d-111c-46b6-8955-9ee1dbb87cb4`

**Market intraday momentum: APAC evidence** — Manapon Limkriangkrai, Daniel Chai, Gaoping Zheng, 2023

> Pacific-Basin Finance Journal 80 (2023) 102086 Available online 4 July 2023 0927-538X/© 2023 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY-NC-ND license (http://creativecommons.org/licenses/by-nc-nd/4.0/). Market intraday momentum: APAC evidence Manapon Limkriangkrai a , * , Daniel Chai b , Gaoping Zheng b a Department of Banking & Finance, Monash University, Melbourne, VIC, Australia b School of Economics, Finance & Marketing, RMIT University, Melbourne, VIC, Australia ARTICLE INFO JEL classification: G11 G14 G17 Keywords: Intraday momentum Return predictability Asia-Pacific (APAC) markets COVID crisis ABSTRACT This study examines the market intraday momentum, where the first half-hour return predicts the last half-hour return, in exchange-traded funds (ETFs) from the selected Asia-Pacific (APAC) markets including China, Hong Kong SAR, Japan, Singapore and South Korea. Intraday mo - mentum is mainly evident in China and Japan. There is weak evidence of the momentum effect in South Korea, while Hong Kong SAR and Singapore appear to have no int

### id `7ce52535-e732-4d96-971c-662fe8d28de3`

**Market Skewness Risk and the Cross Section of Stock Returns** — Bo Young Chang, Peter Christoffersen, Kris Jacobs, 2013

> TSpace Research Repository utoronto.scholaris.ca Market Skewness Risk and the Cross-Section of Stock Returns Peter Christoffersen, Kris Jacobs, Bo Young Chang Version Accepted Manuscript Citation (published version) Christoffersen, P., Chang, B.Y., and Jacobs, K. (2013) Market Skewness Risk and the Cross-Section of Stock Returns. https://doi.org/10.1016/j.jfineco.2012.07.002 Copyright/License This work is licensed under the Creative Commons Attribution- NonCommercial-NoDerivatives 4.0 International License. To view a copy of this license, visit Creative Commons BY NC ND 4.0 License. How to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page. Electronic copy available at: http://ssrn.com/abstract=1480332 Market Skewness Risk and the Cross-Secti

### id `0224fb02-1037-4f36-84dd-7ef0639badd0`

**Measuring the Frequency Dynamics of Financial Connectedness and Systemic Risk*** — Jozef Baruník, Tomáš Křehlík, 2018

> Measuring the frequency dynamics of ﬁnancial connectedness and systemic risk∗† Jozef Barun´ıka,b‡, and Tom´ aˇ sKˇrehl´ıka,b a Institute of Economic Studies, Charles University, Opletalova 26, 110 00, Prague, Czech Republic b Department of Econometrics, IITA, The Czech Academy of Sciences, Pod Vodarenskou Vezi 4, 182 00, Prague, Czech Republic December 20, 2017 Abstract We propose a new framework for measuring connectedness among ﬁnancial variables that arises due to heterogeneous frequency responses to shocks. To estimate connectedness in short-, medium-, and long-term ﬁnancial cycles, we introduce a framework based on the spec- tral representation of variance decompositions. In an empirical application, we document the rich time-frequency dynamics of volatility connectedness in US ﬁnancial institutions. Economically, periods in which connectedness is created at high frequencies are periods when stock markets seem to process information rapidly and calmly, and a shock to one asset in the system will have an impact mainly in the short term. When the connectedness is created at lower 

### id `d362fcb7-7c33-4cda-8ed5-0eb91d6f66d3`

**Measuring volatility with the realized range** — Martin Martens, Dick van Dijk, 2006

> Measuring volatility with the realized range ∗ Martin Martens † Econometric Institute Erasmus University Rotterdam Dick van Dijk ‡ Econometric Institute Erasmus University Rotterdam Econometric Institute Report EI 2006-10 February 2006 Abstract Realized variance, being the summation of squared intra-da y returns, has quickly gained popularity as a measure of daily volatility. Following Parkinson (1980) we replace each squared intra-day return by the high- low range for that period to create a novel and more eﬃcient estimator call ed the realized range. In addition we suggest a bias-correction procedure t o account for the eﬀects of microstructure frictions based upon scaling the r ealized range with the average level of the daily range. Simulation experiment s demonstrate that for plausible levels of non-trading and bid-ask bounce the realized range has a lower mean squared error than the realized variance, in cluding variants thereof that are robust to microstructure noise. Empirical analysis of the S&P500 index-futures and the S&P100 constituents conﬁrm th e potential of the realiz

### id `c6a67ec8-8251-4c28-bada-3c96d0e257b7`

**Medicaid and Mortality: New Evidence From Linked Survey and Administrative Data** — Sarah Miller, Norman F. Johnson, Laura Wherry, 2021

> NBER WORKING PAPER SERIES MEDICAID AND MORTALITY: NEW EVIDENCE FROM LINKED SURVEY AND ADMINISTRATIVE DATA Sarah Miller Norman Johnson Laura R. Wherry Working Paper 26081 http://www.nber.org/papers/w26081 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 July 2019, Revised January 2021 The authors gratefully acknowledge the help of J. Clint Carter and John Sullivan in accessing restricted-use Census data. The authors would also like to thank Andrew Goodman-Bacon, Jonathan Gruber, Alex Hollingsworth, Lawrence Katz, Helen Levy, Kosali Simon, Benjamin Sommers, and four anonymous reviewers for helpful comments. The authors also thank conference and seminar participants at the American Society of Health Economics, Federal Reserve Bank of Chicago, Federal Reserve Board of Governors, Imperial College, Midwest Health Economics Conference, NBER Summer Institute Health Care, NYU Wagner, Princeton University, UC Riverside, and the University of Chicago. Laura Wherry benefited from facilities and resources provided by the California Center for Population Research 

### id `9365ef76-6d8d-42de-96cb-0c07a2e382f3`

**Missing Events in Event Studies: Identifying the Effects of Partially Measured News Surprises** — Refet S. Gürkaynak, Burçin Kısacıkoğlu, Jonathan H. Wright, 2020

> American Economic Review 2020, 110(12): 3871–3912 https://doi.org/10.1257/aer.20181470 3871 Missing Events in Event Studies: Identifying the Effects of P artially Measured News Surprises† By Refet S. Gürkaynak, Burçin Kısacıkog ˘lu, and Jonathan H. Wright* Macroeconomic news announcements are elaborate and multi- dimensional. We consider a framework in which jumps in asset prices around announcements reflect both the response to observed sur - prises in headline numbers and to latent factors, reflecting other news in the release. Non-headline ne ws, for which there are no expecta- tions surveys, is unobservable to the econometrician but nonetheless elicits a market response. We estimate the model by the Kalman filter, which efficiently combines OLS and heter oskedasticity-based event study estimators in one step. With the inclusion of a single latent surprise factor, essentially all yield curve variance in event windows are explained by news. (JEL C51, E43, E52, G12, G14) Macroeconomic news announcements are complex and multidimensional. We argue that recognizing this multidimensiona

### id `f3550197-6692-480d-b040-75525e6e1fcf`

**Monetary Policy Response to Oil Price Shocks** — Jean-Marc Natal, 2012

> FEDERAL RESERVE BANK OF SAN FRANCISCO WORKING PAPER SERIES Working Paper 2009-16 http://www.frbsf.org/publications/economics/papers/2009/wp09-16bk.pdf The views in this paper are solely the responsibility of the authors and should not be interpreted as reflecting the views of the Federal Reserve Bank of San Francisco or the Board of Governors of the Federal Reserve System. Monetary Policy Response to Oil Price Shocks Jean-Marc Natal Swiss National Bank August 2009 Monetary Policy Response to Oil Price Shocks Jean-Marc Natali This draft: August 5, 2009 Abstract How should monetary authorities react to an oil price shock? The New Keyne- sian literature has concluded that ensurin g complete price stability is the optimal thing to do. In contrast, this paper argues that a meaningful trade-oﬀ between stabilizing in ﬂation and the welfare relevant output gap arises in a distorted economy once one recognizes ( i) that oil (energy) cannot be easily substituted by other factors in the short-run, ( ii) that there is no ﬁscal transfer available to policymakers to neutralize the steady-state dis

### id `ca3a7b66-612f-40d2-a177-c3ef1b335626`

**Monetary policy uncertainty** — Lucas F. Husted, John H. Rogers, Bo Sun, 2019

> K.7 Monetary Policy Uncertainty Husted, Lucas, John Rogers, and Bo Sun International Finance Discussion Papers Board of Governors of the Federal Reserve System Number 1215 October 2017 Please cite paper as: Husted, Lucas, John Rogers, and Bo Sun (2017). Monetary Policy Uncertainty. International Finance Discussion Papers 1215. https://doi.org/10.17016/IFDP.2017.1215 Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 1215 October 2017 Monetary Policy Uncertainty Lucas Husted, John Rogers, and Bo Sun NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References in publications to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at https://www.federalreserve.gov/econres/ifdp/. This paper can be downloaded without charge from Social Science Research Network electronic library at http://www.sssrn.com. Monetary

### id `0f5b866a-0016-4c70-a465-db35e18aaf49`

**Multifractal analysis of financial markets: a review** — Zhi‐Qiang Jiang, Wen-Jie Xie, Wei‐Xing Zhou, Didier Sornette, 2019

> arXiv:1805.04750v1 [q-fin.ST] 12 May 2018 Multifractal analysis of ﬁnancial markets Zhi-Qiang Jianga,b,1, Wen-Jie Xiea,b,1, Wei-Xing Zhoua,b,c,∗, Didier Sornette d,e aResearch Center for Econophysics, East China University of Science and Technology, Shanghai 200237, China bDepartment of Finance, School of Business, East China Unive rsity of Science and Technology, Shanghai 200237, China cDepartment of Mathematics, School of Science, East China Un iversity of Science and Technology, Shanghai 200237, China dDepartment of Management, Technology and Economics, ETH Zu rich, Zurich, Switzerland eSwiss Finance Institute, c/o University of Geneva, 40 blvd. Du Pont d’Arve, CH 1211 Geneva 4, Switzerland Abstract Multifractality is ubiquitously observed in complex natur al and socioeconomic systems. Multifractal analysis pro- vides powerful tools to understand the complex nonlinear na ture of time series in diverse ﬁelds. Inspired by its striking analogy with hydrodynamic turbulence, from which the idea of multifractality originated, multifractal anal y- sis of ﬁnancial markets has bloomed, for

### id `caa57e01-77ee-4821-96a1-82bdb29b1b24`

**Necessity as the mother of invention: monetary policy after the crisis** — Alan S. Blinder, Michael Ehrmann, Jakob de Haan, David‐Jan Jansen, 2017

> NBER WORKING PAPER SERIES NECESSITY AS THE MOTHER OF INVENTION: MONETARY POLICY AFTER THE CRISIS Alan S. Blinder Michael Ehrmann Jakob de Haan David-Jan Jansen Working Paper 22735 http://www.nber.org/papers/w22735 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 October 2016 Prepared for the 64th Panel Meeting of Economic Policy in Florence, 14-15 October 2016. The paper presents results from a survey among heads of central banks and academic economists. We are very grateful for all their contributions. We also thank the editors, our referees, Ben Bernanke, Chris Sims, Christiaan Pattipeilohy, Gabriele Galati, Jan Willem van den End, Klaus Adam, Marcel Fratzscher, Mark Watson, Mervyn King, and Richhild Moessner as well as seminar and conference participants at the Bank of Canada, de Nederlandsche Bank, the European Central Bank, the 48th MMF Group Annual Conference, Brunel University and the University of Lisbon for thoughtful comments. We thank Henk van Kerkhoff and Mario Cannella for statistical assistance. This paper was written before the second 

### id `6583e24a-f647-4efe-8a31-396ebeffe301`

**NONLINEARITIES IN THE OIL PRICE–OUTPUT RELATIONSHIP** — Lutz Kilian, Robert J. Vigfusson, 2011

> Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 1013 January 2011 Nonlinearities in the Oil Price-Output Relationship Lutz Kilian and Robert J. Vigfusson NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References in publications to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at www.federalreserve.gov/pubs/ifdp/. 0 Nonlinearities in the Oil Price-Output Relationship Lutz Kilian Robert J. Vigfusson University of Michigan Federal Reserve Board CEPR November 28, 2010 Abstract: It is customary to suggest that the asymmetry in the transmission of oil price shocks to real output is well established. Much of the empirical work cited as being in support of asymmetries, however, has not directly tested the hypothesis of an asymmetric transmission of oil price innovations. Moreover, many of the papers qua

### id `3effc002-44fa-408a-a18d-cb72d7b130fb`

**On covariance estimation of non-synchronously observed diffusion processes** — Takaki Hayashi, Nakahiro Yoshida, 2005

> On covariance estimation of non-synchronously observed diffusion processes TAKAKI HA YASHI 1 and NAKAHIRO YOSHIDA 2 1Department of Statistics, Columbia Universi ty, 1255 Amsterdam Avenue, New York NY 10027, USA. E-mail: hayashi@stat.columbia.edu 2Graduate School of Mathematical Sciences, University of Tokyo, 3-8-1 Komaba, Meguro-ku, Tokyo 153-8914, Japan. E-mail : nakahiro@ms.u-tokyo.ac.jp We consider the problem of estimating the covariance of two diffusion processes when they are observed only at discrete times in a non-synchronous manner. The modern, popular approach in the literature, the realized covariance estimator, which is based on (regularly spaced) synchronous data, is problematic because the choice of regular interval size and data interpolation scheme may lead to unreliable estimation. We propose a new estimator which is free of any ‘synchronization’ processing of the original data, hence free of bias or other problems caused by it. Keywords: diffusions; discrete-time observations; high-frequency data; mathematical ﬁnance; non- synchronous trading; quadratic variation; r

### id `48ec4927-238b-4d71-915d-cd55adff08ba`

**Option valuation with long-run and short-run volatility components☆** — Peter Christoffersen, Kris Jacobs, Chayawat Ornthanalai, Y WANG, 2008

> TSpace Research Repository tspace.library.utoronto.ca Option Valuation with Long-Run and Short- Run Volatility Components Peter Christoffersen, Kris Jacobs, Chayawat Ornthanalai & Yintian Wang Version Accepted Manuscript Citation (published version) Christoffersen, P., Jacobs, K., Ornthanalai, C., & Wang, Y. (2008). Option valuation with long-run and short-run volatility components. Journal of Financial Economics, 90(3), 272-297. DOI https://doi.org/10.1016/j.jfineco.2007.12.003 Copyright/License This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. To view a copy of this license, visit Creative Commons BY NC ND 4.0 License. How to cite TSpace items Always cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page

### id `ce32eee8-1982-4bfa-be03-490232a4cb5f`

**Overnight-Intraday Mispricing of Chinese Energy Stocks: A View from Financial Anomalies** — Min Zhou, Xiaoqun Liu, 2022

> Overnight-Intraday Mispricing of Chinese Energy Stocks: A View from Financial Anomalies Min Zhou 1 and Xiaoqun Liu 2* 1School of Design and Art, Hunan Institute of Technology, Hengyang, China, 2School of Economics, Hainan University, Haikou, China We verify the existence of ﬁrm-level “intraday return vs. overnight return ” pattern and overnight-intraday effect of nine ﬁnancial anomalies of Chinese energy industry stocks of the Chinese stock market. Though energy ﬁnance has been an independent research area, we also take Chinese A-shares stocks as samples for empirical analysis to avoid the so- called sample selection bias. Speci ﬁcally, it veri ﬁes that the overnight returns are strongly negative and intraday returns are positive for energy industry stocks, which is totally contrary to the American stock markets. In addition, alphas of the zero-cost strategies based on nine classic ﬁnancial anomalies are almost earned at night for energy industry stocks. Finally, it is risk-related anomalies that occur overnight for energy industry stocks, while both four risk-related anomalies and t

### id `29bc9d28-aca6-44fa-aaf8-58b4677ff65a`

**Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open** — Henk Berkman, Paul D. Koch, Laura A. Tuttle, Ying Jenny Zhang, 2012

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 47, No. 4, Aug. 2012, pp. 715–741 COPYRIGHT 2012, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109012000270 Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open Henk Berkman, Paul D. Koch, Laura Tuttle, and Ying Jenny Zhang∗ Abstract We ﬁnd a strong tendency for positive returns during the overnight period followed by reversals during the trading day. This behavior is driven by an opening price that is high relative to intraday prices. It is concentrated among stocks that have recently attracted the attention of retail investors, it is more pronounced for stocks that are difﬁcult to value and costly to arbitrage, and it is greater during periods of high overall retail investor sentiment. The additional implicit transaction costs for retail traders who buy high-attention stocks near the open frequently exceed the effective half spread. I. Introduction Behavioral ﬁnance theories assume that individual investors are subject to sentiment that makes them willi

### id `31f13a33-0d57-4f83-a720-6419f8ccb79b`

**Performance of Time-series Momentum Strategy: US Evidence** — Siyao Duan, 2023

> Performance of Time-series Momentum Strategy: US Evidence Siyao Duan1,a,* 1University of Glasgow, Glasgow G12 8QQ, UK a. 2803501d@student.gla.ac.uk *corresponding author Abstract: This paper examines the effectiveness of the time series momentum strategy in generating positive returns in the US stock market, with a focus on exploring its dynamics and performance using different moving average methods. The author conducted an empirical analysis of the time series momentum strategy u sing S&P500 data from 2000 to 2022. A regression model was applied to estimate the expected returns and volatility of each as -set, and then an evaluation of momentum trading strategy based on different moving average methods was developed. The author evalu ates the performance of the strategy with and without transaction costs. The study contributes to the literature by providing empirical evidence on the effectiveness of the time series momentum strategy in the US stock market and by exploring the performance of different moving average methods on the strategy. The findings of this study can provide insi

### id `54c89264-c7b3-4fa4-93f5-4d54a4ee1bd4`

**Prediction and Allocation of Stocks, Bonds, and REITs in the US Market** — Ana Sofia Monteiro, Hélder Sebastião, Nuno Miguel Barateiro Gonçalves Silva, 2024

> Vol.:(0123456789) Computational Economics (2025) 65:1191–1230 https://doi.org/10.1007/s10614-024-10589-2 Prediction and Allocation of Stocks, Bonds, and REITs in the US Market Ana Sofia Monteiro1 · Helder Sebastião1 · Nuno Silva1 Accepted: 11 March 2024 / Published online: 13 April 2024 © The Author(s) 2024 Abstract This study employs dynamic model averaging and selection of Vector Autoregressive and Time-Varying Parameters Vector Autoregressive models to forecast out-of- sample monthly returns of US stocks, bonds, and Real Estate Investment Trusts (REITs) indexes from October 2006 to December 2021. The models were recursively estimated using 17 additional predictors chosen by a genetic algorithm applied to an initial list of 155 predictors. These forecasts were then used to dynamically choose portfolios formed by these assets and the riskless asset proxied by the 3-month US treasury bills. Although we did not find any predictability in the stock market, positive results were obtained for REITs and especially for bonds. The Bayesian- based approaches applied to just the returns of th

### id `d9e2bf38-d1d9-436c-a3e7-d02b3b48f382`

**Premium for heightened uncertainty: Explaining pre-announcement market returns** — Grace Xing Hu, Jun Pan, Jiang Wang, Haoxiang Zhu, 2021

> NBER WORKING PAPER SERIES PREMIUM FOR HEIGHTENED UNCERTAINTY: EXPLAINING PRE-ANNOUNCEMENT MARKET RETURNS Grace Xing Hu Jun Pan Jiang Wang Haoxiang Zhu Working Paper 25817 http://www.nber.org/papers/w25817 NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 May 2019, Revised March 2021 An earlier draft of this paper was circulated under the title “Premium for Heightened Uncertainty: Solving the FOMC Puzzle.” We are grateful to Brad Barber, Ricardo Caballero, Peter Carr, Zhanhui Chen, Ing-Haw Cheng, Darrell Duffie, Ken French, Valentin Haddard, Toomas Laarits, David Lucca, Ian Martin, Annette Vissing-Jorgensen, Clara Vega, Kumar Venkataraman, Jessica Wachter, as well as seminar participants at the 2019 NBER Asset Pricing Program Spring Meeting, the 2019 ABFER Annual Meeting, the 2019 China International Conference in Finance, the 2019 Eastern Conference on Financial Mathematics, the 2019 Summer Institute in Finance, the 2020 AFA annual meeting, Tsinghua University, Shanghai Jiao Tong University, Peking University, Chinese University of Hong Kong, Cheung K

### id `a7f2298e-d85d-4145-8025-2001c3b225f0`

**Price Drift Before U.S. Macroeconomic News: Private Information about Public Announcements?** — Alexander Kurov, Alessio Sancetta, Georg H. Strasser, Marketa Halova Wolfe, 2018

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANAL YSIS Vol. 54, No. 1, Feb. 2019, pp. 449–479 COPYRIGHT 2018, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109018000625 Price Drift Before U.S. Macroeconomic News: Private Information about Public Announcements? Alexander Kurov, Alessio Sancetta, Georg Strasser, and Marketa Halova Wolfe* Abstract We examine stock index futures and Treasury futures around the release time of 30 U.S. macroeconomic announcements. Nine of the 20 announcements that move markets show evidence of substantial informed trading before the ofﬁcial release time. Prices begin to move in the “correct” direction approximately 30 minutes before the release time. The preannouncement price drift accounts on average for approximately 40% of the total price adjustment. This implies that some traders have private information about macroeconomic fundamentals. Preannouncement drift might originate from a combination of information leakage and superior forecasting that incorporates proprietary data. I. Introduction Macroeconomic n

### id `20ff392c-ebdf-48b8-8c50-a3835bf208e9`

**Price Reaction to Information with Heterogeneous Beliefs and Wealth Effects: Underreaction, Momentum, and Reversal** — Marco Ottaviani, Peter Norman Sørensen, 2015

> /u.sc/n.sc/i.sc/v.sc/e.sc/r.sc/s.sc/i.sc/t.sc/y.sc /o.sc/f.sc /c.sc/o.sc/p.sc/e.sc/n.sc/h.sc/a.sc/g.sc/e.sc/n.sc Københavns Universitet Price Reaction to Information with Heterogeneous Beliefs and Wealth Effects: Underreaction, Momentum, and Reversal Sørensen, Peter Norman; Ottaviani, Marco Published in: American Economic Review DOI: 10.1257/aer.20120881 Publication date: 2015 Document version Publisher's PDF, also known as Version of record Citation for published version (APA): Sørensen, P. N., & Ottaviani, M. (2015). Price Reaction to Information with Heterogeneous Beliefs and Wealth Effects: Underreaction, Momentum, and Reversal. American Economic Review, 105(1), 1-34. https://doi.org/10.1257/aer.20120881 Download date: 22. Sep. 2026 American Economic Review 2015, 105(1): 1–34 http://dx.doi.org/10.1257/aer.20120881 1 Price Reaction to Information with Heterogeneous Beliefs and Wealth Effects: Underreaction, Momentum, and Reversal † By Marco Ottaviani and Peter Norman Sørensen * This paper analyzes how asset prices in a binary mark et react to information when traders have heteroge

### id `df6e7e07-9ed5-473a-bec4-350b81c27f1d`

**Price revelation from insider trading: Evidence from hacked earnings news** — Pat Akey, Vincent Grégoire, Charles Martineau, 2022

> TSpace Research Repository tspace.library.utoronto.ca P rice revelation from insider trading: Evidence from hacked earnings news P at Akey, Vincent Grégoire, & Charles Martineau Version Accepted Manuscript Citation (published version) Akey, P., Grégoire, V., & Martineau, C. (2022). Price revelation from insider trading: Evidence from hacked earnings news. Journal of Financial Economics, 143(3), 1162-1184. https://doi.org/10.1016/j.jfineco.2021.12.006 Copyright/License This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. To view a copy of this license, visit Creative Commons BY NC ND 4.0 License. How to cite TSpace items A lways cite the published version, so the author(s) will receive recognition through services that track citation counts, e.g. Scopus. If you need to cite the page number of the author manuscript from TSpace because you cannot access the published version, then cite the TSpace version in addition to the published version using the permanent URI (handle) found on the record page. This article was made open

### id `562e10b0-6838-464a-9949-877918f5b8ac`

**Profitability of technical trading strategies under market manipulation** — Alfred Ma, 2022

> Profitability of technical trading strategies under market manipulation Alfred Ma1,2* Introduction The closing price is important in finance. It is the most commonly used financial data in both academia and industry. Given its importance, it is also exposed to market manipu - lation which is defined as stock prices being artificially influenced (Allen and Gale 1992). However, most quantitative trading strategies use the official closing price as their input. This study examines the profitability impact of closing price market manipulation on technical trading strategies. Putniņš (2012) and Thoppan and Punniyamoorthy (2013) provide comprehensive sur - veys on market manipulation. Allen and Gale (1992) are early pioneers to start studies on market manipulation and formalize the study. They also introduce the concept of trade-based and information-based manipulation to classify cases of market manipula - tion. Aggarwal and Wu (2006) investigate cases of stock market manipulation and con - clude that market manipulation alters stock returns as a result. Market manipulation is not a probl

### id `c1b61065-dcee-4887-8a9b-4359f9daa2ac`

**Realised volatility and industry momentum returns** — Xiaoyue Chen, Bin Li, Andrew C. Worthington, 2022

> ARTICLE Realised volatility and industry momentum returns Xiaoyue Chen 1 ✉, Bin Li 1 & Andrew C. Worthington 1 Motivated by the importance of industry volatility and the pro ﬁtability of industry momentum strategy, this study investigates the relationship between realised volatility and industry momentum returns. The analysis uses daily return data for 48 US industries from July 1969 to June 2021 to calculate realised volatility and to gauge the raw return effect on short- and medium-horizon double-sort momentum-trading strategies. The ﬁndings show that past volatility positively relates to industry momentum and that this relationship is stronger after controlling for common risk factors (market, size, value, investment, and pro ﬁtability). Decomposing the realised total volatility into idiosyncratic and systematic components, this study reveals that both decomposed components are positively related to industry momentum returns. The ﬁndings are robust to alternative measures of volatility. https://doi.org/10.1057/s41599-022-01309-y OPEN 1 Department of Accounting, Finance and Economi

### id `b908971d-741f-454c-bc98-fb930600cd15`

**Realized power variation and stochastic volatility models** — Ole E. Barndorff–Nielsen, Neil Shephard, 2003

> Realized power variation and stochastic volatility models OLE E. BARNDORFF-NIELSEN 1 and NEIL SHEPHARD 2 1Centre for Mathematical Physics and Stochastics (MaPhySto), University of Aarhus, Ny Munkegade, DK-8000 Aarhus C, Denmark. E-mail: oebn@mi.aau.dk 2Nufﬁeld College, Oxford OX1 1NF , UK. E-mail: neil.shephard@nuf.ox.ac.uk Limit distribution results on realized power variation, that is, sums of absolute powers of increments of a process, are derived for certain types of semimartingale with continuous local martingale component, in particular for a class of ﬂexible stochastic volatility models. The theory covers, for example, the cases of realized volatility and realized absolute variation. Such results should be helpful in, for example, the analysis of volatility models using high-frequency information. Keywords: absolute returns; mixed asymptotic normality; p-variation; quadratic variation; realized volatility; semimartingale 1. Introduction Stochastic volatility processes play an important role in ﬁnancial economics, generalizing Brownian motion to allow the scale of the increment

### id `6bd9682e-c645-4b06-b3cc-131d5acf049b`

**Resolving a Paradox: Retail Trades Positively Predict Returns but Are Not Profitable** — Brad M. Barber, Shengle Lin, Terrance Odean, 2023

> JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 59, No. 6, Sep. 2024, pp. 2547 –2581 © The Author(s), 2023. Published by Cambridge University Press on behalf of the Michael G. Foster School of Business, University of Washington. This is an Open Access article, distributed under the terms of the Creative Commons Attribution licence ( https://creativecommons.org/licenses/by/4.0), which permits unrestricted re-use, distribution and reproduction, provided the original article is properly cited. doi:10.1017/S0022109023000601 Resolving a Paradox: Retail Trades Positively Predict Returns but Are Not Profitable Brad M. Barber University of California Davis Graduate School of Management bmbarber@ucdavis.edu Shengle Lin San Francisco State University Lam Family College of Business sf@sfsu.edu (corresponding author) Terrance Odean University of California Berkeley Haas School of Business odean@berkeley.edu Abstract Retail order imbalance positively predicts returns, but on average retail investor trades lose money. Why? Order imbalance tests equal-weighted stocks, but retail purchases conce

### id `cb11a872-2723-4c09-b34f-918f0e830178`

**Return connectedness across asset classes around the COVID-19 outbreak** — Elie Bouri, Oğuzhan Çepni, David Gabauer, Rangan Gupta, 2020

> Return connectedness across asset classes around the COVID-19 outbreak Elie Bouri †, Oguzhan Cepni ‡, David Gabauer §, and Rangan Gupta Λ †Holy Spirit University of Kaslik (USEK), USEK Business School, Jounieh, Lebanon. ‡Central Bank of the Republic of Turkey, Ankara, Turkey. §Software Competence Center Hagenberg, Data Analysis Systems, Softwarepark 21, 4232 Hagenberg, Austria. Λ Department of Economics, University of Pretoria, Pretoria, 0002, South Africa. ∗Corresponding Author. Abstract In this paper, we show evidence of a dramatic change in the structure and time-varying patterns of return connectedness across various assets (gold, crude oil, world equities, currencies, and bonds) around the COVID-19 outbreak. Using the TVP-VAR connectedness approach, the results show that the dynamic total connectedness across the ﬁve assets was moderate and quite stable until early 2020. After that, the total connectedness spikes and the structure of the network of connectedness alters, which concurs with the COVID-19 outbreak. The equity and USD indices are the primary transmitters of shocks be

### id `65188448-37d9-41cf-8cd7-16dd0ea1b8fc`

**Rise of the Machines: Algorithmic Trading in the Foreign Exchange Market** — Alain Chaboud, Benjamin Chiquoine, Erik Hjalmarsson, Clara Vega, 2014

> Board of Governors of the Federal Reserve System International Finance Discussion Papers Number 980 October 2009 Rise of the Machines: Algorithmic Trading in the Foreign Exchange Market Alain Chaboud, Benjamin Chiquoine, Erik Hjalmarsson, Clara Vega NOTE: International Finance Discussion Papers are preliminary materials circulated to stimulate discussion and critical comment. References in publications to International Finance Discussion Papers (other than an acknowledgment that the writer has had access to unpublished material) should be cleared with the author or authors. Recent IFDPs are available on the Web at www.federalreserve.gov/pubs/ifdp/. This paper can be downloaded without charge from Social Science Research Network electronic library at http://www.ssrn.com/. Rise of the Machines: Algorithmic T rading in the F oreign Exchange Market Alain Chaboud Benjamin Chiquoine Erik Hjalmarsson Clara V ega  September 29, 2009 Abstract We study the impact that algorithmic trading, computers directly interfacing at high frequency with trading platforms, has had on price discovery and v

### id `3799c0b2-16e6-41ed-9a80-34621aa6fa4c`

**Rise of the machines? Intraday high-frequency trading patterns of cryptocurrencies** — Alla A. Petukhina, Raphael C. G. Reule, Wolfgang Karl Härdle, 2020

> Rise of the Machines? Intraday High-Frequency Trading Patterns of Cryptocurrencies Alla A. Petukhina Humboldt-Universit¨ at zu Berlin. Firamis GmbH, Germany. alla.petukhina[at]wiwi.hu-berlin.de Raphael C. G. Reule Humboldt-Universit¨ at zu Berlin. irtg1792.wiwi[at]wiwi.hu-berlin.de Wolfgang Karl H¨ ardle Humboldt-Universit¨ at zu Berlin, IRTG 1792, Dorotheenstr. 1, 10117 Berlin, Germany School of Business, Singapore Management University, 50 Stamford Road, Singapore 178899 Faculty of Mathematics and Physics, Charles University, Ke Karlovu 3, 121 16 Prague, Czech Republic Department of Information Management and Finance, National Chiao Tung University, Taiwan, ROC haerdle[at]wiwi.hu-berlin.de September 10, 2020 Abstract This research analyses high-frequency data of the cryptocurrency market in re- gards to intraday trading patterns related to algorithmic trading and its impact on the European cryptocurrency market. We study trading quantitatives such as returns, traded volumes, volatility periodicity, and provide summary statistics of return correlations to CRIX (CRyptocurrency IndeX)

### id `41e3b4d5-e5ba-4979-8b36-7ab14a28f459`

**Russia–Ukraine crisis: The effects on the European stock market** — Shaker Ahmed, Mostafa Monzur Hasan, Md Rajib Kamal, 2022

> DOI: 10.1111/eufm.12386 ORIGINAL ARTICLE Russia–Ukraine crisis: The effects on the European stock market Shaker Ahmed 1 | Mostafa M. Hasan 2 | Md Rajib Kamal 3,4 1School of Accounting and Finance, University of Vaasa, Vaasa, Finland 2Department of Accounting and Corporate Governance, Macquarie Business School, Macquarie University, Sydney, New South Wales, Australia 3NTNU Business School, Norwegian University of Science and Technology, Trondheim, Norway 4Department of Management and Finance, Faculty of Agribusiness Management, Sher‐e‐Bangla Agricultural University, Dhaka, Bangladesh Correspondence Mostafa M. Hasan, Department of Accounting and Corporate Governance, Macquarie Business School, Macquarie University, Sydney, NSW 2109, Australia. Email: mostafa.hasan@mq.edu.au Abstract We examine the effect of the Russia –Ukraine crisis on the European stock markets. Because of increased political uncertainty, geographic proximity and the ramifications of the fresh sanctions imposed on Russia, the European stock markets tended to react negatively to this crisis. We find that on 21 Februar

