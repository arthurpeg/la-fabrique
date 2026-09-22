# D20 — Le moissonnage du corpus : une requête écrite, un automate qui ne juge pas

**Date :** 2026-09-22
**Phase :** 07 (construit), 09 (utilisé)
**État :** prise

## La question

`AMORCE.md` porte 20 entrées, 19 atteignables. La phase 09 en demande **30 à
50**. D'où viennent les suivantes, et qui décide lesquelles ?

## Les options

**1. Continuer à la main**, comme la table `ALTERNATES` de
`probe_acquisition.py`. Écartée : c'est précisément le geste manuel qui a coûté
le plus cher au recensement, et il ne passe pas à l'échelle. Il a pourtant
**fonctionné** — il a fait passer l'atteignable de 5 à 19 — et c'est lui qu'on
automatise ici, pas autre chose.

**2. Un moissonneur qui cherche ET filtre par pertinence** — une IA qui lit
titres et résumés et retient « ce qui ressemble à du momentum sur futures ».
**Écartée, et c'est l'option dangereuse.** Elle fusionne le moissonnage et le
**triage**, qui est la moitié de la porte 07 et possède déjà son juge
(`score_triage.py`) et son étalon (`AMORCE.md`, 20 verdicts humains écrits en
phase 01). Un filtre de pertinence non jugé écarterait des papiers sans que rien
ne mesure **ce qu'il écarte à tort** : son silence ressemblerait à une absence,
ce qui est `L05` mot pour mot.

**3. Un moissonneur déterministe, sans jugement, sur une requête
pré-enregistrée.** Retenue.

**4. Ne pas moissonner et requalifier la phase 09 à 19 papiers.** Écartée : le
« 30 à 50 » de la phase 09 n'a pas été examiné ici, et le baisser pour éviter un
travail serait ajuster un seuil en le voyant — l'inverse de ce que `D15` et
`D16` ont fait.

## Le choix

**Le moissonneur ratisse et ne juge pas.** `corpus/harvest.py` interroge des
catalogues publics sur une **requête écrite ici, avant d'être lancée**, sonde
les PDF libres avec le critère de preuve de `D17`, et les enregistre. Il ne
classe pas, ne note pas, n'écarte rien pour sa pertinence. Le tri de
l'implémentable reste au **trieur**, qui existe et qui est jugé.

**Son produit alimente la phase 09. Il n'entre pas dans `G1`–`G4`.**
`corpus/harvest.json` n'a **aucune autorité** sur `corpus/acquisition.json` :
la porte 07 se juge sur les 19 atteignables d'`AMORCE.md` et sur rien d'autre.
C'est `F47` du registre des idées abandonnées, et cette décision ne la rouvre
pas — elle la **date**.

## La requête, écrite avant d'être lancée

Six familles, reprises des **sections A à F d'`AMORCE.md`**, qui sont déjà la
taxonomie du projet. Contrainte au domaine — sans quoi « overnight » ramène la
littérature médicale et « trend following » ramène tout.

| | Famille | Recherche |
|---|---|---|
| A | momentum intra-journalier | `"intraday momentum" OR "market intraday momentum"` |
| B | overnight contre intraday | `"overnight return" OR "overnight drift" OR "tug of war"` |
| C | périodicité et volatilité | `"intraday periodicity" OR "realized volatility" OR "HAR model"` |
| D | annonces macroéconomiques | `"macroeconomic announcements" OR "FOMC announcement drift"` |
| E | carry et structure de terme | `"carry trade" OR "commodity futures" OR "term structure of futures"` |
| F | momentum en série temporelle | `"time series momentum" OR "trend following" OR "managed futures"` |

**Filtre commun, identique pour les six** : articles, publiés depuis le
**1995-01-01**, sous-champs OpenAlex **2002** (Economics and Econometrics) ou
**2003** (Finance), en accès libre (`is_oa:true`).

**Tri** : `cited_by_count:desc`. **Plafond** : ~~25~~ **60** candidats par
famille, soit 360 avant dédoublonnage — porté de 25 à 60 le 2026-09-22, voir
§ Journal, passage 2. Le chiffre d'origine est conservé barré : il dit ce que le
passage 1 avait devant lui.

**Ce que la requête pèse, mesuré le 2026-09-22 avant d'être figée** :

| Famille | travaux | dont libres |
|---|---|---|
| A | 118 | 90 |
| B | 999 | 876 |
| C | 5 874 | 4 518 |
| D | 1 088 | 889 |
| E | 7 958 | 6 450 |
| F | 2 137 | 1 611 |

Le plafond en retient donc **une petite fraction**, et `harvest.json` inscrit
pour chaque famille le total annoncé par le catalogue — sans quoi on ne saurait
pas ce qu'on n'a pas regardé.

## Pourquoi

**La requête est le filtre, et elle est pré-enregistrée pour cette raison.** Le
périmètre d'un corpus décide de ce qui pourra être trouvé ; le laisser se
former en cours de route serait un bouton qu'on tourne jusqu'à ce que le corpus
plaise. Écrite ici, elle est contestable et rejouable. La changer est une
nouvelle décision, et le § Journal dira ce qui a bougé.

**Le tri par citations est un choix, et il a un biais qu'il faut nommer.** Il
favorise les papiers établis et **sous-échantillonne le récent** — un papier de
2025 n'a pas eu le temps d'être cité. Retenu quand même parce qu'il est
**externe, stable et lisible**, là où le score de pertinence d'un moteur est
opaque et bouge à chaque mise à jour d'index. Le biais va d'ailleurs dans le
sens du projet : il ramène les affirmations **célèbres**, celles qui valent
d'être testées. Un second passage trié par date est prévu au § Ce qui reste
ouvert.

**Le moissonneur ne contient aucune IA, et c'est délibéré.** Chercher, résoudre
une URL, vérifier qu'un octet est `%PDF-` : rien là-dedans ne demande de
jugement, et tout gagne à être déterministe, gratuit et rejouable. L'IA
intervient **après**, là où elle était déjà prévue — le trieur, puis
l'extracteur. Dit autrement : *l'IA ne cherche pas les papiers, elle les lit
ensuite.*

**Le critère d'atteignabilité est celui de `D17`, sans une virgule de plus.** Ni
péage ni démarche auprès d'un tiers ; le texte est réputé obtenu quand le corps
est un `application/pdf` d'au moins **20 000 octets** commençant par `%PDF-`.
Les constantes sont **importées** de `probe_acquisition.py`, pas recopiées : deux
seuils qui dérivent l'un de l'autre, c'est deux définitions de l'atteignable.

**Une annonce de PDF libre n'est pas un PDF libre**, et la sonde du 2026-09-22
l'a montré avant qu'une ligne soit écrite : OpenAlex rend
`oa_status=bronze` avec un `pdf_url` pointant vers **ScienceDirect**. Toute URL
est sondée ; aucune n'est crue.

**Rien n'est contourné.** Un contrôle anti-robot est inscrit `refus_robot` et
reste là. Requêtes espacées, `mailto` et `User-Agent` qui nous identifient. Un
corpus obtenu en forçant une porte est un corpus que la session suivante ne sait
pas reproduire — c'est déjà écrit dans `ACQUISITION.md`, et ça vaut ici.

**La liste close des raisons n'est pas élargie.** `peage`, `refus_robot`,
`sans_source_libre` couvrent tout ce que le moissonnage rencontre. Le
dédoublonnage n'est **pas** une raison d'inatteignabilité : c'est un champ
distinct, `duplicate_of`, parce qu'un doublon est atteignable — il est
simplement déjà là. `L18` : on ne loge pas un cas nouveau dans une liste close
parce que le mécanisme est à portée.

**Le nom de fichier est dérivé d'un identifiant stable, pas d'une citation.**
`fetch_pdfs.py` a raison d'écrire qu'un nom fabriqué par expression régulière se
casse en silence — mais sa parade, une table écrite à la main, ne tient pas à
100 papiers. Le nom est donc `<titre-abrégé>-<identifiant OpenAlex>.pdf` :
l'identifiant garantit l'unicité **par construction**, le titre garde la
lisibilité, et une collision est refusée bruyamment plutôt que résolue.

**Ce que ça coûte, et c'est assumé** : un corpus dont une bonne part sera hors
sujet. La sonde ramène « Behavioural finance and cryptocurrencies » en septième
position de la famille A. **C'est le fonctionnement correct, pas un défaut** :
un moissonneur qui ne ramènerait que de l'implémentable aurait trié en cachette,
et le trieur n'aurait plus rien à écarter.

## Ce que ça verrouille

- **`corpus/harvest.json` est un constat daté, pas une fonction rejouable.**
  L'index d'OpenAlex bouge ; la même requête rendra autre chose demain. Chaque
  entrée porte sa date, comme `acquisition.json`.
- **La requête ci-dessus est figée.** En changer — un mot-clé, une famille, le
  filtre de domaine, le tri, le plafond — est une décision écrite, et tout
  comptage de corpus antérieur devient périmé.
- **`harvest.json` n'entre pas dans `G1`–`G4`** et ne modifie pas le verdict de
  la porte 07.
- **Le corpus moissonné entre au dénominateur de la phase 09**, et son compte
  devra être cité tel quel — combien cherchés, combien obtenus, combien triés
  implémentables — comme la phase 15 citera `counted_tests()`.
- **`corpus/check_harvest.py` garde le fichier**, sur le modèle de
  `check_acquisition.py`.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Un second passage trié par date**, pour corriger le biais du tri par citations contre les papiers récents | avant la phase 09 |
| **Le trieur n'a été jugé qu'une fois, sur 20 entrées, avec `A` et `C` à leur maximum exact.** L'appliquer à 100 papiers est une extrapolation d'un juge calibré à la limite — à écrire, pas à supposer | avant de trier le corpus moissonné |
| **Les papiers en HTML seulement**, que `F4` refuse. Même question ouverte que l'entrée 9 dans `D18` | au premier cas qu'on veuille ficher |
| **Les sources autres qu'OpenAlex et Unpaywall** — arXiv, NBER, RePEc, CORE — sondées et fonctionnelles le 2026-09-22, non câblées. À ajouter si le rendement en PDF est insuffisant | à la mesure du premier passage |
| **Le dédoublonnage contre `AMORCE.md` est fait par titre normalisé et par empreinte du PDF.** Un même papier sous deux titres (version de travail contre version publiée) peut passer au travers | à la première collision constatée |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Candidats | Atteignables | PDF enregistrés | Note |
|---|---|---|---|---|---|
| — | 2026-09-22 | — | — | — | décision écrite, requête figée, aucun passage encore lancé |
| 1 | 2026-09-22 | **132** (dont 5 déjà dans `AMORCE.md`) | **43** | **43**, 0 échec | `HARVEST_MAILTO` non renseigné, donc **Unpaywall sauté** |
| 2 | 2026-09-22 | **319** (plafond porté à 60) | **123** | **123**, 0 échec | incrémental : les 132 du passage 1 conservés avec leur constat |

**Le passage 2 atteint la cible** : 123 PDF, au-dessus des 50 à 100 visés, et
**le rendement monte de 34 % à 39 %** (123 sur 314 sondés) sans qu'aucun critère
ait changé — simple effet de la profondeur.

| | Famille | travaux | libres | pris | PDF |
|---|---|---|---|---|---|
| A | momentum intra-journalier | 118 | 90 | 60 | **28** |
| B | overnight contre intraday | 999 | 876 | 58 | 21 |
| C | périodicité et volatilité | 5 876 | 4 521 | 54 | 20 |
| D | annonces macroéconomiques | 1 088 | 889 | 51 | 21 |
| E | carry et structure de terme | 7 959 | 6 451 | 43 | 11 |
| F | momentum en série temporelle | 2 137 | 1 611 | 53 | 22 |

La famille A est **épuisée** : 60 pris sur 90 libres, et le plafond y mord à
peine. La famille E rend le moins (11 PDF sur 43) — `carry trade` et
`commodity futures` sont largement publiés chez des éditeurs payants.

**Répartition des refus** : 110 `peage`, 53 `sans_source_libre`, 28
`refus_robot`. Le péage domine, ce qui est cohérent avec la finance académique.

**Un `429` a cassé le premier essai du passage 2.** Sans `HARVEST_MAILTO`, les
requêtes passent par le pool **commun** d'OpenAlex, qui limite plus tôt : 0,25 s
entre appels suffisait au plafond de 25, pas à celui de 60. La réponse juste à
un `429` est de **ralentir** — pause portée à 1,5 s et **recul progressif** (5,
10, 20, 40 s, puis abandon). C'est l'inverse d'un contournement : le serveur dit
« trop vite », on obéit.

**Ce qui reste sur la table** : `HARVEST_MAILTO` n'est toujours pas renseigné,
donc **Unpaywall n'a jamais été interrogé**. C'est le seul levier connu restant,
et il appartient à l'utilisateur — l'adresse est une donnée personnelle envoyée à
un tiers, et ce geste ne se pose pas à sa place.

**Ce que le passage 1 a rendu**, par famille — « pris » est le plafond effectif
après dédoublonnage inter-familles, « PDF » ce qui a été obtenu :

| | Famille | travaux | libres | pris | PDF |
|---|---|---|---|---|---|
| A | momentum intra-journalier | 118 | 90 | 25 | 9 |
| B | overnight contre intraday | 999 | 876 | 24 | 8 |
| C | périodicité et volatilité | 5 874 | 4 518 | 24 | 5 |
| D | annonces macroéconomiques | 1 088 | 889 | 19 | 8 |
| E | carry et structure de terme | 7 958 | 6 450 | 19 | 6 |
| F | momentum en série temporelle | 2 137 | 1 611 | 21 | 7 |

**Rendement : 43 PDF sur 127 candidats sondés, soit 34 %.** Sous la cible de
50 à 100, et la cause principale est connue et réparable : `HARVEST_MAILTO`
n'était pas renseigné, donc **Unpaywall n'a pas été interrogé du tout**. Un
second passage avec cette adresse est le premier geste à tenter avant d'élargir
la requête.

**Une erreur d'étiquetage trouvée et corrigée dans le passage même.** La
première version de `verdict()` testait le code HTTP **avant** l'hôte : 64
entrées sur 65 sortaient `refus_robot`, alors que 56 des 67 tentatives refusées
venaient d'hôtes d'**éditeurs** — Wiley 27, ScienceDirect 14, OUP 8, AEA 4. Un
éditeur qui répond `403` sur son propre PDF ne « sert pas un contrôle
anti-robot » : il garde son texte. L'ordre corrigé rend **55 `peage` / 10
`refus_robot` / 19 `sans_source_libre`**, et les 10 restants sont bien des
dépôts (Hull, BYU, CBS, Édimbourg, Nottingham, PMC). La liste close n'a **pas**
été élargie (`L18`) ; c'est l'ordre des tests qui était faux, et `refused_by`
inscrit désormais hôte et code pour que la raison soit vérifiable. `F51`.

**La correction n'a coûté aucune requête réseau** : `--reverdict` recalcule les
verdicts sur les tentatives déjà enregistrées. Les tentatives sont le fait
observé ; le verdict n'en est que la lecture, et une lecture fausse se refait
sans redéranger cent hôtes.

**Et le passage 1 a trouvé une faute qui n'était pas la sienne — voir `L20`.**
Le dédoublonnage par `sha256` a établi que le PDF enregistré sous le nom de
l'**entrée 1 d'`AMORCE.md`** (Gao, Han, Li & Zhou 2018, *JFE*) est en réalité
**Limkriangkrai, Chai & Zheng (2023), « Market intraday momentum: APAC
evidence », *Pacific-Basin Finance Journal* 80:102086**. Le recensement prouvait
qu'**un** PDF arrivait, jamais que c'était **le bon**. **Non corrigé ici** : la
réparation demande de retrouver le vrai Gao 2018, de re-sonder l'entrée et de
régénérer son texte `D18` — c'est un acte distinct, et on ne retouche pas un
recensement en passant. **Fait le 2026-09-22** : aucune copie libre n'existe,
l'entrée 1 est passée `inatteignable` / `refus_robot`, et le recensement est
descendu de 19 à 18 atteignables (`ETAT.md`, `F53`).

### Passage 2 — le plafond passe de 25 à 60, et pourquoi c'est licite

**Le passage 1 a rendu 43 PDF**, sous la cible de 50 à 100 que la phase 09
impose. Et 43 est un compte de PDF **bruts** : le triage en écartera une bonne
part, puisque le moissonneur ne juge pas. Le plafond est donc porté à **60 par
famille**.

**Ce qui bouge, et ce qui ne bouge pas.** La recherche, le domaine, la fenêtre
de dates et le tri sont **inchangés**. Seule la profondeur de lecture d'une
liste déjà ordonnée augmente. Conséquence vérifiable : **les 25 premiers de
chaque famille sont le préfixe exact des 60 premiers**, et les 132 candidats du
passage 1 sont tous conservés avec leur statut et leur date de constat.

**Pourquoi ce n'est pas l'ajustement que `D20` interdit.** L'interdit vise le
choix qu'on referait **en voyant le résultat** — changer un mot-clé parce que la
moisson déplaît, ajouter une famille parce qu'une autre déçoit. Rien de tel ici :
aucun papier n'est re-sélectionné, aucun critère de contenu ne change, et
l'ajout est **strictement additif**. Creuser plus profond dans une liste figée
et changer la liste sont deux gestes différents, et seul le second est un bouton.

**Ce qui reste interdit sans une nouvelle décision** : un mot-clé, une famille,
le filtre de domaine, la fenêtre de dates, le tri. Ceux-là décident **quels**
papiers peuvent apparaître ; le plafond ne décide que **combien** on en regarde.

**Un trou du garde trouvé en faisant ce changement.** `check_harvest` comparait
le plafond **à lui-même** — le JSON déclarait son propre `per_family` et `H9`
vérifiait qu'il le respectait, donc un `--per-family 500` passait sans un mot.
`H1` le compare désormais à la valeur déclarée dans le code, qui est la copie de
travail de la présente décision.

**Le moissonnage devient incrémental.** `--search` **ajoute** au lieu de
remplacer : les travaux déjà sondés gardent statut, preuve et date. Sans quoi
approfondir obligerait à tout re-sonder, et effacerait le constat daté du
passage précédent — qui est une pièce du dossier, pas un brouillon.
