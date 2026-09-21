# D17 — Ce que la porte 07 demande : un extracteur jugé, pas un corpus compté

**Date :** 2026-09-20
**Phase :** 07
**État :** prise

## La question

La porte 07 demande « **20 fiches produites** ». `corpus/AMORCE.md` ne rend pas
20 papiers atteignables, et ce n'est pas une question de temps : **6 entrées
n'ont aucun lien**, 2 sont derrière un péage, et rien ne garantit les autres. Le
chiffre 20 est-il ce que la porte teste, ou l'accident du document qui l'a
inspirée ?

## Les options

**1. Tenir les 20 d'`AMORCE.md`.** Aller chercher les 6 sans lien et les 2
payants par accès institutionnel, versions de travail, ou demande aux auteurs.
Écartée : le plus fidèle à la lettre, et de loin le plus lent — avec la
certitude de bloquer une phase entière sur deux ou trois papiers introuvables,
pour une raison qui n'a rien à voir avec ce que la porte vérifie.

**2. Élargir le corpus au-delà d'`AMORCE.md`** jusqu'à 20 papiers librement
disponibles. Écartée : ces papiers n'ont **aucun verdict humain de triage**. Ils
élargiraient l'extraction sans élargir l'étalon, et il faudrait écrire qu'ils ne
comptent pas pour la moitié triage — une complication ajoutée pour préserver un
chiffre qui n'a pas de fondement.

**3. Requalifier la porte sur ce qu'elle teste réellement.** Retenue.

## Le choix

**La porte 07 est franchie quand un extracteur produit, sans retouche manuelle,
des fiches qui passent les cinq conditions de `D16` sur tous les papiers
réellement atteignables — et que le compte de ceux qui ne l'étaient pas est
écrit.** Le nombre de fiches n'est plus une condition ; l'exhaustivité du corpus
atteignable en est une.

Quatre conditions, en **effectifs** — `F37`, et la même discipline que `D15` :

| | Condition | Effectif |
|---|---|---|
| **G1** | papiers atteignables **non fichés** | 0 |
| **G2** | fiches produites ne passant pas les cinq conditions de `D16` | 0 |
| **G3** | fiches ayant demandé une **retouche manuelle** après production | 0 |
| **G4** | papiers **inatteignables non recensés**, avec la raison | 0 |

Les quatre valent ensemble. **`G1` est la condition qui empêche de tricher** :
sans elle, « tous les papiers atteignables » se satisferait d'un seul.

Un papier est **atteignable** quand son texte est obtenu sans péage ni démarche
auprès d'un tiers. Le constat est daté et inscrit : un papier inatteignable
aujourd'hui pourra l'être demain, et le § Journal le dira.

## Pourquoi

**Le 20 n'a jamais rien testé.** Il vient du nombre d'entrées notées
d'`AMORCE.md` — lui-même le produit d'une session de phase 01 qui recensait ce
qu'elle avait sous la main. Aucun raisonnement ne le relie à la question que la
porte pose : *une fiche produit-elle un signal exécutable sans retouche ?* Vingt
fiches médiocres ne répondent pas mieux que six bonnes, et le contraire est faux
aussi.

**Ce que la porte teste, c'est l'automate, pas la bibliothèque.** L'ordre de
construction de `CLAUDE.md` le dit : *on n'automatise jamais la production de
quelque chose qu'on ne sait pas encore juger*. La phase 07 fabrique le juge
(`D16`) et l'automate ; la **quantité** de corpus est le sujet de la phase 09,
« premier passage complet sur 30 à 50 papiers », qui a son propre compte.

**`G3` est la condition qui porte la vraie exigence**, et elle est plus dure que
le chiffre qu'elle remplace. La porte écrite disait déjà « *une fiche produit un
signal exécutable **sans retouche manuelle*** » pour la phase 08 ; l'appliquer à
l'extraction ferme la faille par laquelle une phase se franchit en corrigeant à
la main ce que l'automate a raté. Un extracteur dont on répare les sorties n'est
pas un extracteur.

**Ce que ça sacrifie.** Le corpus de la phase 07 sera **petit** — vraisemblablement
entre 6 et 14 fiches selon ce que SSRN consent. Un extracteur vert sur 6 papiers
est moins éprouvé qu'un extracteur vert sur 20, et le dire ici évite de le
découvrir en phase 09. **La porte 07 ne prétendra pas avoir éprouvé
l'extracteur ; elle prétendra l'avoir jugé sur tout ce qui était à portée.** Le
verdict cite le compte des deux côtés — fichés et inatteignables — comme la
phase 15 citera `counted_tests()`.

**Et le corpus est attendu mort, ce qui change ce que la taille vaut.** Mesfin
est transportable (`L14`), `H01`, `H02` et `H03` n'ont rien trouvé. Le produit
de la phase 07 a de fortes chances d'être une liste de signaux nuls. Dépenser
des semaines à porter un corpus de 14 à 20 pour mieux établir une liste nulle
serait un mauvais emploi du seul temps dont dispose un opérateur seul.

## Ce que ça verrouille

- **La porte 07 se vérifie désormais par `D16` (par fiche) et `G1`–`G4` (sur le
  corpus).** Les changer est une décision écrite, et tout résultat d'extraction
  antérieur devient périmé — la règle du harnais, appliquée ici comme `D15` et
  `D16` l'ont appliquée.
- **Le recensement des inatteignables devient une pièce du dépôt**, pas une
  remarque : `G4` exige qu'il existe, daté, avec la raison par papier. Sans lui,
  `G1` ne veut rien dire, puisqu'on choisirait après coup ce qui était
  atteignable.
- **La phase 09 hérite de la question de taille**, et son compte de 30 à 50
  papiers n'est pas modifié par la présente décision.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| ~~**Combien de papiers sont réellement atteignables**~~ **Répondu le 2026-09-21 : 19 sur 20**, dont 18 en PDF. SSRN refuse partout (contrôle anti-robot), et c'est sans conséquence : les papiers vivent aussi ailleurs. Voir `corpus/ACQUISITION.md` et le § Journal ci-dessous | **fait** |
| **Ce que devient un papier atteignable mais illisible** — scan trop dégradé pour que `F2` trouve quoi que ce soit, même avec réparation déclarée (`D16` § Complément) : inatteignable, ou fiché sans citation ? | au premier cas rencontré |
| **Ce que devient un papier atteignable dont le texte n'est pas un PDF** — l'entrée 9 est un billet de blog en HTML, libre et sans démarche, donc atteignable à la lettre de la présente décision ; mais `F4` de `D16` exige un `source.pdf` qui existe. **Cas rencontré le 2026-09-21** | avant de ficher l'entrée 9 |
| ~~**Si le corpus atteignable descend sous 5 papiers**~~ **Écarté le 2026-09-21 : 19 atteignables.** Le seuil avait été écrit avant le recensement, ce qui est la seule façon pour un seuil de valoir quelque chose | **fait** |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Corpus atteignable | Fiches produites | G1/G2/G3/G4 | Verdict |
|---|---|---|---|---|---|
| — | 2026-09-21 | **19 / 20** (18 PDF, 1 HTML) | — | `G4` tenu, le reste non mesuré | recensement seul, pas un passage de porte |

**Le recensement de `G4` est fait — le 2026-09-21.** `corpus/acquisition.json`,
produit par `corpus/probe_acquisition.py` et gardé par
`corpus/check_acquisition.py` (**11 vérifications**, vert). Le détail et ce
qu'il a coûté d'apprendre sont dans `corpus/ACQUISITION.md`.

**Ce que la présente décision avait prévu, et où elle se trompait.** Elle
écrivait *« entre 6 et 14 fiches selon ce que SSRN consent »*. Le recensement
rend **19**, au-dessus de la borne haute, et **SSRN n'a rien consenti** : il
refuse tout client automatique, vérifié deux fois. La prévision prenait le lien
qu'`AMORCE.md` porte pour le papier lui-même ; s'en tenir à ces liens rendait
**5 sur 20**. Presque tous ces papiers vivent aussi au NBER, dans les rapports
de la Fed, sur des pages d'auteurs ou dans des dépôts universitaires.

**Les 18 PDF atteignables sont enregistrés** — le 2026-09-21, par
`corpus/fetch_pdfs.py`, 15 pris ce jour-là, aucun échec, chacun vérifié après
écriture. Les noms de fichiers sont **déclarés** dans le script et non déduits
d'une citation, faute de quoi une citation mal formée produirait en silence un
fichier qu'aucune fiche ne retrouverait.

**Ce qui reste à faire et ne l'est pas** : il n'y a toujours **aucun
extracteur**, et `G1`, `G2`, `G3` ne sont pas mesurés. Le corpus est prêt ;
l'automate qui doit le lire n'existe pas.
