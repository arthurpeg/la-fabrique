# Le recensement des atteignables — `G4` de `D17`

**Fait le 2026-09-21.** Source de vérité : `corpus/acquisition.json`, produit par
`corpus/probe_acquisition.py` et vérifié par `corpus/check_acquisition.py`
(11 vérifications, vert). Ce document explique ; **le JSON fait foi**.

---

## Ce que `D17` demande, mot pour mot

> Un papier est **atteignable** quand son texte est obtenu sans péage ni démarche
> auprès d'un tiers. Le constat est daté et inscrit.

Et `G4` : **zéro papier inatteignable non recensé, avec la raison**. Sans ce
recensement, `G1` — *zéro papier atteignable non fiché* — ne veut rien dire,
puisqu'on choisirait après coup ce qui était à portée.

## Le résultat

| | Effectif |
|---|---|
| **atteignables** | **19 / 20** — 18 en PDF, 1 en HTML seulement |
| **inatteignables** | **1** — entrée 6, `refus_robot` |

Le seuil de `D17` — *« si le corpus atteignable descend sous 5 papiers, rouvrir
l'option 2 »* — est **largement écarté**, et il avait été écrit avant le
recensement, ce qui est la seule façon pour un seuil de valoir quelque chose.

## Ce que `D17` prévoyait, et pourquoi elle se trompait

`D17` écrivait : *« le corpus de la phase 07 sera petit — vraisemblablement entre
6 et 14 fiches selon ce que SSRN consent »*. Le recensement rend **19**, au-dessus
de sa borne haute — et **SSRN n'a rien consenti** : il sert un contrôle
anti-robot et nous a refusés partout.

La prévision était fausse parce qu'elle prenait **le lien qu'`AMORCE.md` porte
pour le papier lui-même**. Or presque tous ces papiers vivent ailleurs aussi :
rapports de la Fed, documents de travail du NBER, pages personnelles d'auteurs,
dépôts universitaires. SSRN était traité comme la porte ; il n'était qu'une
porte parmi d'autres.

**Le recensement l'a appris en marchant, et c'est inscrit dans le script.** S'en
tenir aux liens d'`AMORCE.md` rendait **5 atteignables sur 20**. L'entrée 3
(Heston) le montrait déjà sans qu'on le voie : `AMORCE.md` n'en donne qu'un lien
SSRN, et son PDF est sur le disque depuis le 2026-09-20 — obtenu d'arXiv. Un
recensement qui aurait rendu 5 aurait été faux, et `G1` l'aurait rendu
**invisible**, puisqu'on n'aurait fiché que ce que le lien rendait.

## Comment le constat est fait

**Une URL qui répond `200` ne prouve rien.** Une page de résumé répond `200`
derrière un péage. Le texte est réputé obtenu quand le corps est un
`application/pdf` d'au moins 20 000 octets dont les cinq premiers octets sont
`%PDF-`. La preuve est conservée par entrée dans le champ `evidence`.

**Les sources hors d'`AMORCE.md` portent leur provenance** — champ `source_via`,
qui dit comment l'URL a été trouvée et quand. C'est `D09` appliqué à une URL :
une valeur qui vient du dehors ne s'écrit pas sans dire d'où elle vient. Le garde
refuse un atteignable sans provenance (`A4`).

**Rien n'a été contourné.** SSRN sert un contrôle anti-robot — vérifié deux fois,
par client automatique (`403`) et dans un vrai navigateur (page « Vérification de
sécurité en cours », qui ne se résout pas). C'est inscrit `refus_robot` et rien
n'a été tenté pour passer outre : un corpus obtenu en forçant une porte est un
corpus que la session suivante ne sait pas reproduire.

## Les raisons d'inatteignabilité — liste CLOSE

Comme les listes closes de `D09`, `D14` et `D16`. Une raison hors liste est un
trou dans le recensement, et `check_acquisition.py` la refuse (`A3`).

| Raison | Ce qu'elle dit |
|---|---|
| `peage` | le texte est derrière un péage |
| `refus_robot` | le site sert un contrôle anti-robot, non contourné |
| `sans_source_libre` | aucune version libre trouvée au recensement |

**« Inatteignable » sans motif serait l'endroit où ranger ce qu'on n'a pas
essayé.** D'où la liste close, et d'où `A3`.

## Le seul inatteignable — entrée 6

**Wen, Gong, Ma & Xu (2021)**, *Intraday momentum and return predictability:
evidence from the crude oil market*, *Economic Modelling* 95:374-384.

`AMORCE.md` ne lui donne aucun lien. Le recensement a trouvé trois routes, et
aucune n'ouvre : SSRN 3553682 (`refus_robot`), ScienceDirect (péage Elsevier),
ResearchGate (demande à l'auteur — une **démarche auprès d'un tiers**, exclue par
la définition même). Constat daté du 2026-09-21 ; **il pourra changer**, et le
§ Journal le dira.

C'est l'entrée que `AMORCE.md` décrit comme *« le motif de Gao et al. transposé
au pétrole »* — donc la perte porte sur une **transposition** d'un papier que
nous avons par ailleurs (entrée 1, atteignable). La perte est réelle mais
bornée ; elle n'est pas invoquée ici pour se consoler, elle est écrite pour que
`G1` soit lisible.

## Les deux alertes — ce que le recensement a vu et n'a pas tranché

**Entrée 9 — texte libre, mais en HTML.** Le billet *The disappearing overnight
drift* (Liberty Street Economics) est en accès libre et sans démarche : **par la
lettre de `D17`, il est atteignable**. Mais `F4` de `D16` exige un `source.pdf`
qui existe, et `F2` cherche ses citations dans « le texte du papier ». Le cas
n'est pas tranché et **demande une décision écrite avant tout fichage**. Il
rejoint la question que `D16` laissait déjà ouverte : *où vit le texte source*.

**Entrée 16 — la citation d'`AMORCE.md` paraît fausse.** Elle porte
« Kurov, Sancetta, Strasser & Wolfe (2021) », mais le papier de *Finance Research
Letters* 40 (2021) que son propre lien ScienceDirect désigne
(`S1544612320315956`) est de **Kurov, Wolfe & Gilbert**. Le PDF obtenu est la
version de travail de **ce** papier-là — titre et date de révision concordants.
La liste d'auteurs paraît mélangée avec un autre papier de Kurov.

**Non corrigé ici, et délibérément.** `AMORCE.md` est l'étalon du triage (`D15`),
et on ne retouche pas un étalon en passant — a fortiori après qu'un passage a
été jugé contre lui. Si correction il y a, c'est par note datée, texte d'origine
conservé, comme pour les entrées 7 et 9.

## Ce que ce recensement ne dit pas

**Il ne dit pas qu'un papier est utile.** Il dit que son texte est à portée.
Le triage (`D15`, passage 1) a déjà jugé l'implémentabilité ; la pertinence des
fiches n'aura de dénominateur qu'en phase 09, comme `D16` l'écrit.

**Il ne dit pas que les PDF sont sur le disque.** Ils y sont — les 18, depuis
le 2026-09-21, par `corpus/fetch_pdfs.py` — mais c'est un **geste distinct**,
et l'énoncé se périme : `corpus/pdf/` est ignoré par git. On le vérifie en
lançant `python corpus/fetch_pdfs.py --verify`, jamais en lisant cette page.

**Il ne dit pas que les textes sont exploitables.** Les 18 rendent du texte à
`pypdf`, aucun n'est vide — et cela ne prouve rien sur la **justesse** de ce
texte. L'entrée 11 en rend 2 787 caractères par page, et `D17` a établi que ce
sont ceux d'un scan qui écrit « fight part » pour « right part ». Un compte de
caractères ne distingue pas un texte d'un faux texte ; c'est `F2` qui juge, une
citation à la fois.

**Il se périme.** Un constat d'accès est vrai d'un poste et d'une heure — la
leçon du 2026-09-21 sur `corpus/pdf/`. D'où le champ `checked` par entrée, et
d'où le fait que ce document renvoie au JSON plutôt que de recopier ses chiffres.

## Journal

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Atteignables | Inatteignables | Notes |
|---|---|---|---|---|
| 1 | 2026-09-21 | 19 / 20 (18 PDF, 1 HTML) | 1 — entrée 6, `refus_robot` | premier recensement ; SSRN refuse partout, sans conséquence sauf sur l'entrée 6 ; alertes ouvertes sur 9 et 16 |
| — | 2026-09-21 | *(enregistrement, pas un recensement)* | — | **18 PDF écrits dans `corpus/pdf/`** par `fetch_pdfs.py`, 15 pris ce jour, 0 échec, chacun vérifié après écriture ; les 3 fiches de référence passent toujours `F4` |
