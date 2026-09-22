# D19 — La version de l'extracteur de texte est épinglée

**Date :** 2026-09-22
**Phase :** 07
**État :** prise

## La question

`D18` a fixé *quelles* extractions font foi — `pypdf` en mode par défaut et en
mode `layout`, versionnées dans `corpus/text/`. Elle n'a pas fixé **avec quelle
version de `pypdf`**. Le 2026-09-22, `extract_text.py --check` a trouvé
**31 fichiers sur 36** divergents. Que fait-on quand le garde de `D18` se
déclenche ?

## Ce qui s'est passé, et ce qui n'est pas en cause

`uv.lock` porte `pypdf 6.19.0` depuis le commit du **2026-09-20**. Le texte qui
fait foi a été produit le **2026-09-21** avec **6.14.2** — donc par un
environnement **en retard sur le verrou commité**, et personne ne l'a vu. Le
manifeste l'inscrivait pourtant : `"pypdf": "6.14.2"`.

**Deux causes possibles ont été séparées avant de trancher.** Les 15 PDF
manquants ayant été repris le 2026-09-22, une divergence pouvait venir du
*fichier* et non de la *version*. Le même corpus ré-extrait sous 6.14.2 rend
**36 fichiers sur 36 conformes au manifeste** : les PDF repris sont identiques à
ceux du 21, l'acquisition est reproductible, et **la version est seule en
cause**.

## Les options

**1. Épingler `pypdf==6.14.2`.** Retenue. Le texte qui fait foi reste ce qu'il
est ; aucune `quoted_source` n'est périmée ; le manifeste n'est pas touché.

**2. Régénérer le texte sous 6.19.0** et remettre le manifeste à jour. Écartée
sur son coût comparé à son gain — voir ci-dessous. Elle reste faisable, et
`D18` § Ce qui reste ouvert la prévoyait.

**3. Ne comparer les empreintes que si les versions concordent.** Écartée, et
c'est la plus dangereuse : elle transforme un garde en commentaire. Le jour où
le texte changerait pour une *autre* raison, rien ne le dirait. C'est
« modifier le harnais pour faire passer un signal », appliqué au garde plutôt
qu'au résultat.

**4. Ne rien épingler et accepter la dérive.** Écartée sans discussion : `F2`
cherche une chaîne **à la lettre**, donc un texte qui bouge est un verdict qui
bouge.

## Le choix

**La version de l'extracteur fait partie de la définition du texte qui fait
foi.** `pypdf` est épinglé à `==6.14.2` dans `pyproject.toml` — la version qui a
produit `corpus/text/`. En changer est une **décision écrite** qui régénère les
36 fichiers, met le manifeste à jour, et **re-vérifie `F2` sur toutes les fiches
existantes** avant d'être acquise.

## Pourquoi

**Ni l'une ni l'autre version n'est meilleure, et c'est mesuré.** Sur les
18 papiers, 6.14.2 → 6.19.0 :

| | contenu normalisé | lettres orphelines |
|---|---|---|
| mode `default` | 1 792 017 → 1 792 904 (**+0,05 %**) | 13 860 → 13 753 (**−0,8 %**) |
| mode `layout` | 1 679 086 → 1 690 244 (**+0,66 %**) | 11 576 → 12 966 (**+12,0 %**) |

6.19.0 récupère marginalement plus de contenu et **dégrade de 12 % le découpage
des mots en mode `layout`** — exactement le symptôme (« multiples **o f** 13 »)
pour lequel `D18` avait retenu ce mode en complément du défaut. Le gain et la
perte sont du même petit ordre, en sens contraires. **Aucun argument de qualité
ne départage**, et c'est le résultat le plus utile de la mesure : il retire au
choix tout enjeu autre que le coût.

**Le coût, lui, départage nettement.** L'option 1 coûte une ligne de
`pyproject.toml`. L'option 2 coûte 36 fichiers régénérés, un manifeste réécrit,
et la re-vérification de toutes les fiches — pour un texte qui n'est pas
meilleur.

**Ce que la mesure dit aussi, et qui compte pour plus tard** : sous 6.19.0,
**aucune des 47 citations des 4 fiches ne casse** — `F2` rend 0 faute sur les
quatre, des deux côtés. L'épinglage n'est donc pas un mur : une montée future
est peu risquée sur le corpus actuel. Elle reste une décision écrite, parce que
« peu risquée » se vérifie à chaque fois et ne se suppose jamais.

**C'est `D10` transposée.** Le harnais est figé et empreinté ; en changer périme
tous les résultats antérieurs. L'extracteur de texte est à `F2` ce que le
harnais est à l'IC : l'outil déterministe dont dépend le verdict. Il reçoit le
même traitement, pour la même raison.

**Ce qui est sacrifié.** Le dépôt reste sur un `pypdf` qui vieillira, et
n'aura pas ses corrections de lecture de PDF sans une décision. C'est le prix
d'un texte rejouable, et `D18` l'avait déjà payé en versionnant 6,2 Mo.

## Ce que ça verrouille

- **`pyproject.toml` porte `pypdf==6.14.2`**, et le verrou est recommité. Un
  `uv sync` ramène désormais la version qui reproduit `corpus/text/`.
- **`corpus/text/MANIFEST.json` devient contraignant et non plus seulement
  descriptif.** Il disait déjà la version ; il la **fixe** maintenant, par
  `pyproject.toml`.
- **Toute montée de `pypdf` est une décision écrite** qui doit, dans l'ordre :
  régénérer les 36 fichiers, mettre le manifeste à jour, re-lancer
  `corpus/score_extraction.py` sur **chaque** fiche, et inscrire au § Journal de
  `D18` les citations qui ont bougé.
- **Le même raisonnement vaudra pour toute dépendance dont la sortie est
  versionnée comme un résultat.** Aucune autre n'est dans ce cas aujourd'hui :
  `numpy`, `pandas` et `scipy` servent au harnais, qui est empreinté par son
  propre code (`D10`) et ne versionne pas ses sorties.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Monter `pypdf` délibérément**, une fois le corpus fiché et stable, pour ne pas traîner une version figée indéfiniment. La mesure du 2026-09-22 dit que le corpus actuel y survivrait sans une casse | après la porte 07 |
| **Un corpus élargi** (moissonnage) ré-ouvrira la question : de nouveaux PDF peuvent être mieux lus par une version récente. Le seuil est le même que celui de `D18` pour une troisième extraction — il faut un papier que la version épinglée rend illisible | au premier cas rencontré |
| **La vérification n'est pas automatique dans une porte.** `extract_text.py --check` existe et doit être lancé ; aucune porte ne l'exige encore | à la construction de la porte 07 |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Ce qui a changé | Effet mesuré |
|---|---|---|---|
| 1 | 2026-09-22 | décision prise ; `pypdf` épinglé à `==6.14.2` | `extract_text.py --check` repasse vert, 36 fichiers conformes ; les 4 fiches gardent leurs 47 citations ; aucun texte régénéré |
