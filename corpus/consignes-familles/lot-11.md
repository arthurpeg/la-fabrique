# Consigne — le mécanisme et l'effet annoncé de 7 papiers (lot 11 sur 11)

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

Écris avec l'outil Write, à `C:/Users/Mathis/Documents/la-fabrique/corpus/consignes-familles/lot-11.json`, un tableau JSON et rien d'autre :

```json
[{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

### id `W3124324673`

**Return signal momentum**

> King’s Research Portal DOI: 10.1016/j.jbankfin.2021.106063 Document Version Peer reviewed version Link to publication record in King's Research Portal Citation for published version (APA): Papailias, F., Liu, J., & Thomakos, D. D. (2021). Return signal momentum. Journal of Banking and Finance, 124, Article 106063. Advance online publication. https://doi.org/10.1016/j.jbankfin.2021.106063 Citing this paper Please note that where the full-text provided on King's Research Portal is the Author Accepted Manuscript or Post-Print version this may differ from the final Published version. If citing, it is advised that you check and use the publisher's definitive version for pagination, volume/issue, and date of publication details. And where the final published version is provided on the Research Portal, if citing you are again advised to check the publisher's website for any subsequent corrections. General rights Copyright and moral rights for the publications made accessible in the Research Portal are retained by the authors and/or other copyright owners and it is a condition of accessing p

### id `W4309687100`

**Early prediction of Ibex 35 movements**

> RESEARCH ARTICLE Early prediction of Ibex 35 movements I. Marta Miranda García 1 | María-Jesús Segovia-Vargas 2 | Usue Mori 3 | José A. Lozano 3 1Department of Financial Economy and Accounting, Universidad Pablo de Olavide, Seville, Spain 2Department of Financial and Actuarial Economics and Statistics, Complutense University of Madrid, Campus de Somosaguas, Madrid, Spain 3Department of Computer Science and Artificial Intelligence, University of the Basque Country UPV/EHU, Leioa, Spain Correspondence I. Marta Miranda García, Department of Financial Economy and Accounting, Universidad Pablo de Olavide, Ctra. Utrera, Km. 1, 41013, Seville, Spain. Email: immirgar@upo.es Funding information This research was supported by a grant from the Santander-UCM research project, call 2019, with reference PR87/19-22586 and by Spanish Ministry of Science and Innovation research project, with reference PID2020-115700RB-I00. Abstract In this paper, we examine the early predictability of the market's directional movement using intraday high-frequency data (695,764 observations) from an stock index (Ibex

### id `W3123836508`

**Fact or friction: Jumps at ultra high frequency**

> Fact or friction: Jumps at ultra high frequency ∗ Kim Christensen † Roel C. A. Oomen ‡ Mark Podolskij § November 6, 2014 Abstract This paper shows that jumps in ﬁnancial asset prices are ofte n erroneously identiﬁed and are, in fact, rare events accounting for a very small proport ion of the total price variation. We apply new econometric techniques to a comprehensive set of u ltra high-frequency equity and foreign exchange tick data recorded at millisecond precisi on, allowing us to examine the price evolution at the individual order level. We show that in both theory and practice, traditional measures of jump variation based on lower-frequency data te nd to spuriously assign a burst of volatility to the jump component. As a result, the true pri ce variation coming from jumps is overstated. Our estimates based on tick data suggest that the jump variation is an order of magnitude smaller than typical estimates found in the exist ing literature. JEL classiﬁcation : C14; C80. Keywords: Jump variation; high-frequency data; microstructure noi se; pre-averaging; real- ized variation. ∗We 

### id `W7126140455`

**Price signatures**

> Roel Oomen Price signatures Article (Accepted version) (Refereed) Original citation: Oomen, Roel (2018) Price signatures. Quantitative Finance. ISSN 1469-7688 © 2018 Taylor & Francis This version available at: http://eprints.lse.ac.uk/90481/ Available in LSE Research Online: October 2018 LSE has developed LSE Research Online so that users may access research output of the School. Copyright © and Moral Rights for the papers on this site are retained by the individual authors and/or other copyright owners. Users may download and/or print one copy of any article(s) in LSE Research Online to facilitate their private study or for non-commercial research. You may not engage in further distribution of the material or use it for any profit-making activities or any commercial gain. You may freely distribute the URL ( http://eprints.lse.ac.uk) of the LSE Research Online website. This document is the author’s final accepted version of the journal article. There may be differences between this version and the publishe d version. You are advised to consult the publisher’s version if you wish to c

### id `W2997721561`

**BİST Şehir Endekslerinde Ay İçi ve Ay Dönümü Anomalilerinin İncelenmesi**

> [itobiad], 2019, 8 (4): 3114/3133 BİST Şehir Endekslerinde Ay İçi ve Ay Dönümü Anomalilerinin İncelenmesi Examining the Intra-month and Turn-of-the-Month Anomalies in BIST City Indices İhsan Erdem KAYRAL Dr. Öğr. Üyesi, Konya Gıda ve Tarım Üniversitesi, Sosyal ve Beşeri Bilimler Fakültesi, Ekonomi Bölümü Asst. Prof., Konya Food and Agriculture University, Faculty of Social Sciences and Humanities, Department of Economics erdem.kayral@gidatarim.edu.tr Orcid ID: 0000-0002-8335-8619 Nisa Şansel TANDOĞAN Arş. Gör., Konya Gıda ve Tarım Üniversitesi, Sosyal ve Beşeri Bilimler Fakültesi, Ekonomi Bölümü Research Assistant, Konya Food and Agriculture University, Faculty of Social Sciences and Humanities, Department of Economics sansel.tandogan@gidatarim.edu.tr Orcid ID: 0000-0002-5633-892X Makale Bilgisi / Article Information Makale Türü / Article Type : Araştırma Makalesi / Research Article Geliş Tarihi / Received : 16.10.2019 Kabul Tarihi / Accepted : 19.12.2019 Yayın Tarihi / Published : 23.12.2019 Yayın Sezonu : Ekim-Kasım-Aralık Pub Date Season : October-November-December Atıf/Cite as: K

### id `W3122180240`

**International Real Estate Review**

> Bias in Equally-Weighted Return Indexes of REITs 43 Bias in Equally-Weighted Return Indexes of REITs 43 INTERNATIONAL REAL ESTATE REVIEW 2012 Vol. 15 No. 1: pp. 43 – 71 Removing Biases in Computed Returns: An Analysis of Bias in Equally -Weighted Return Indexes of REITs Lawrence Fisher Department of Finance and Economics , Rutgers Business School , Rutgers University, 111 Washington Street, Newark, NJ 07102 Daniel G. Weaver Department of Finance and Economics , Rutgers Business School , Rutgers University, 94 Rockafeller Road , Piscataway, NJ 08854 -8054; Email : Daniel_Weaver@rbsmail.rutgers.edu Gwendolyn Webb The Bert W. Wasserman Department of Economics and Finance , Baruch College, Zicklin School of Business, One Bernard Baruch Way, Box B10-225 New York, New York 10010; Email: Gwendolyn.Webb@baruch.cuny.edu In this paper , we apply the method for removing the upward bias in returns in equally -weighted return indexes developed by Fisher, Weaver, and Webb (2010) to real estate investment trust (REIT) stocks in the US. While we find significant bias in this index, two trends are

### id `W3023213822`

**Reflecting on the VPIN dispute**

> Department of Economics and Business Aarhus University Fuglesangs Allé 4 DK-8210 Aarhus V Denmark Email: oekonomi@au.dk Tel: +45 8716 5515 Reflecting on the VPIN Dispute Torben G. Andersen and Oleg Bondarenko CREATES Research Paper 2013-42 Reﬂecting on the VPIN Dispute∗ Torben G. Andersen† and Oleg Bondarenko‡ Abstract In Andersen and Bondarenko (2014), using tick data for S&P 500 futures, we establish that the VPIN metric of Easley, L´opez de Prado, and O’Hara (ELO), by construction, will be correlated with trading volume and return volatility (innovations). Whether VPIN is more strongly correlated with volume or volatility depends on the exact implementation. Hence, it is crucial for the interpretation of VPIN as a harbinger of market turbulence or as a predictor of short-term volatility to control for current volume and volatility. Doing so, we ﬁnd no evidence of incremental predictive power of VPIN for future volatility. Likewise, VPIN does not attain unusual extremes prior to the ﬂash crash. Moreover, the properties of VPIN are strongly dependent on the underlying trade classiﬁc

