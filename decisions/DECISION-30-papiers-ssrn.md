# D30 — Les papiers SSRN : chercher leur autre version, ou les déposer à la main

**Date :** 2026-09-28
**Phase :** 09
**État :** prise — complète `D20` (le moissonneur) et `D21` (les axes)

## La question

Le moissonneur connaît 60 papiers SSRN (axe `ssrn:intraday-momentum`, découverts
par Crossref sur le préfixe `10.2139` sans toucher à ssrn.com). **Aucun n'a été
sondé**, et le résolveur existant ne pouvait rien pour eux : il cherche le PDF
**du DOI SSRN**, dont la seule copie est sur ssrn.com, qui sert un contrôle
anti-robot. Comment en récupérer le texte sans rien contourner ?

## Ce qui est mesuré

- **SSRN refuse les robots**, et ce projet ne contourne pas un contrôle
  anti-robot (`D17`, `F53`, `refus_robot`). Rien ci-dessous n'y touche.
- **Un papier SSRN vit souvent ailleurs sous le même titre** — version publiée en
  libre accès, NBER, arXiv, RePEc, dépôt d'université. OpenAlex range ces
  versions sous un AUTRE identifiant que le dépôt SSRN. Sondage du 2026-09-28,
  par titre : **3 papiers sur 8** ayant répondu ont une autre version en libre
  accès (*Momentum Crashes* au JFE, un papier bitcoin en revue libre, *Risk and
  Return in High Frequency Trading* sur RePEc). Échantillon trop petit pour un
  taux, suffisant pour dire que la piste existe.
- **Les API publiques brident l'anonyme.** Sur les 60 titres, OpenAlex a rendu
  `503`/`429` pour 52, Semantic Scholar a refusé presque tout. Sans
  `HARVEST_MAILTO` (file « polie » d'OpenAlex), cette voie ne passe pas à
  l'échelle.
- **La plupart des 60 sont hors sujet** (retraites, scolarité, lobbying) : la
  requête Crossref ramène tout ce qui contient « return ». Ce n'est pas au
  moissonneur d'en juger (`F50`) — le trieur le fera — mais c'est à savoir avant
  d'y dépenser du temps humain.

## Les options

1. **Chercher l'autre version par le titre.** Retenue. OpenAlex, recherche par
   titre ; ne sont gardés que les travaux au **titre identique après
   normalisation** (règle de `nber_urls`), **d'un autre DOI que SSRN**, et
   partageant **au moins un nom d'auteur** avec la notice Crossref. CORE, pour
   ces papiers, est interrogé par titre **avec la même vérification du titre**.
   La sonde de `D17` tranche ensuite, comme pour tout candidat.
2. **Le dépôt manuel.** Retenue, en complément. L'opérateur, dans SON
   navigateur, télécharge sur SSRN les papiers qu'il choisit — SSRN consent à un
   lecteur humain ce qu'il refuse à un robot ; c'est un geste de lecteur, pas un
   contournement. Il les dépose dans `corpus/pdf/manual/`, nommés par leur
   numéro SSRN (`1363476.pdf`). Le moissonneur les fait entrer par la même porte
   que les autres : `%PDF-`, taille minimale, dédoublonnage par empreinte.
3. **Contourner le contrôle de SSRN** (navigateur automatisé, relais, cookies
   récupérés). Écartée, sans discussion : c'est exactement ce que `refus_robot`
   inscrit comme non fait, et ce que ce projet refuse depuis `D17`.
4. **Demander aux auteurs.** Écartée par `D17` dès l'origine.

## Le choix

Pour les travaux au DOI SSRN : le résolveur cherche leur **autre version** par
titre (vérifiée : titre identique, autre DOI, un auteur commun), et un **dépôt
manuel** reçoit ce que l'opérateur télécharge lui-même. Le moissonneur ne touche
jamais à ssrn.com.

## Pourquoi

Parce que le mur n'est pas le papier, c'est l'hôte. Le recensement d'`AMORCE.md`
l'a déjà montré : chercher le LIEN rendait 5 atteignables sur 20, chercher le
PAPIER en rendait 19. SSRN n'est qu'un hôte de plus qui refuse les robots.

**La vérification du titre n'est pas une preuve** (`L20`, `F52`) : un papier en
cite un autre, deux versions peuvent différer. Elle est exigée **identique**,
jamais « proche », et doublée d'un auteur commun — la règle la plus stricte
disponible sans lire le texte. La lecture vient ensuite : le trieur, puis
l'extracteur, jugent le texte qu'ils reçoivent, et `F2` le vérifie mot pour mot.

**Le dépôt manuel est un geste humain, et il est inscrit comme tel** :
`source_via` le dit, avec la date. Cacher une étape humaine derrière un statut
automatique est ce que le dépôt refuse (`F36`).

**Ce qui est sacrifié.** Le dépôt manuel coûte du temps d'opérateur, et il ne
passe pas à l'échelle : c'est une voie pour la dizaine de papiers SSRN qui
comptent, pas pour les 60. Et aucun papier absent de `harvest.json` ne peut y
entrer : la population reste celle de la requête écrite d'avance (`D20`).

## Ce que ça verrouille

- `corpus/harvest.py` : `openalex_siblings()`, appelé par `pdf_candidates()`
  pour les DOI `10.2139` ; CORE interrogé par titre vérifié pour ces mêmes
  travaux ; `RESOLVERS` passe à `2026-09-28 : … + siblings`, ce qui **périme les
  refus antérieurs** (jamais les réussites) — `--probe --retry` les reprend.
- `--ssrn-list` : les papiers SSRN non atteignables, avec l'adresse de leur page
  SSRN pour l'opérateur. N'ouvre aucune connexion.
- `--ingest-manual` : fait entrer `corpus/pdf/manual/<numéro>.pdf`. Refuse tout
  fichier dont le numéro ne correspond à aucun travail de `harvest.json`.
- Le produit reste hors de `G1`–`G4` (`F47`).

## Ce qui reste ouvert

- **`HARVEST_MAILTO`**, sans lequel la recherche des autres versions reste
  bridée. C'est une donnée personnelle envoyée à un tiers : à renseigner par
  l'opérateur, pas par une session.
- **Le choix des papiers SSRN à déposer à la main.** Le moissonneur ne juge pas
  (`F50`) ; l'opérateur choisit, et son choix n'est pas un triage — les papiers
  déposés passeront par le trieur comme les autres.

## Journal

- **2026-09-28** — décision prise et appliquée. Sondage préalable noté ci-dessus.
- **2026-09-28, premier passage** (`harvest.py --probe --ssrn`, sans
  `HARVEST_MAILTO`). **5 atteignables sur 59** : *Momentum Crashes* par sa
  version NBER (mais **doublon d'octets** d'un travail que le moissonneur avait
  déjà par OpenAlex), un par l'autre version sur RePEc, trois par CORE au titre
  vérifié. **4 papiers réellement nouveaux, tous hors sujet** (retraites,
  scolarité, rentabilité des fonds propres, prévisibilité macroéconomique).
  **Les 54 autres n'ont PAS été jugés** : OpenAlex refusait alors la majorité
  des requêtes (`503`, 2 sur 3 à l'instant du constat), et la première version
  du code inscrivait ce refus comme `sans_source_libre` — un silence pris pour
  une absence (`L05`). Corrigé le jour même : quand la recherche des autres
  versions n'a pas pu avoir lieu et qu'aucun PDF n'a été trouvé, le travail
  reste **non sondé** (`REPORTE`) ; les 54 refus ont été remis à « non sondé ».
  **À relancer avec `HARVEST_MAILTO` renseigné.**
- **2026-09-28, défaut trouvé par le `--fetch` qui a suivi** : 33 papiers
  promus marqués doublons **d'eux-mêmes**. `promote_harvest.py` copie par
  conception les PDF promus dans `corpus/pdf/`, que le dédoublonnage de
  `--fetch` lit : chaque PDF y retrouvait sa propre copie. Les 33 sont des
  papiers fichés, que `duplicate_of` aurait écartés de la chaîne. Corrigé dans
  `do_fetch` (un fichier du même nom n'est pas un doublon), les 33 marques
  annulées, vérifié : aucune fiche marquée. `LECONS.md` `L29`.
