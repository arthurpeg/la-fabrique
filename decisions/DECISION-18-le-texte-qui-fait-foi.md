# D18 — Le texte qui fait foi : deux extractions déclarées, versionnées

**Date :** 2026-09-21
**Phase :** 07
**État :** prise

## La question

`F2` exige qu'une citation se retrouve **mot pour mot dans le texte du papier**.
Mais « le texte du papier » n'existe pas : il y a des **extractions** d'un PDF,
qui diffèrent. Laquelle fait foi, et où vit-elle ?

## Les options

**1. Le mode par défaut de `pypdf`.** Écartée par la mesure : il insère des
espaces à l'intérieur des mots — « multiples **o f** 13 », « way is **d
ifferent** » — y compris sur des PDF **nés numériques**. Il casse `F2` sur 5
citations justes de la fiche Heston.

**2. Le mode `layout` seul.** Tentante, et insuffisante. Il réduit d'un cinquième
les lettres orphelines (11 622 → 9 304 sur les 18 papiers) **mais perd 6 % du
contenu normalisé**, et jusqu'à **20 %** sur l'entrée 8 et **16 %** sur l'entrée
15. Or pour `F2`, une perte de contenu est pire qu'un espace parasite : un
espace rend une citation introuvable et se répare en la déclarant ; **un passage
absent ne se répare pas du tout**. Et le gain n'est pas uniforme — 5 papiers sur
18 ont *plus* de lettres orphelines en `layout`.

**3. L'union de deux extractions déclarées.** Retenue.

**4. Un mode déclaré par papier**, dans la fiche. Écartée, et c'est la plus
dangereuse des quatre : elle transforme le choix du texte en **bouton**. Un
extracteur qui échoue sur un papier verrait son mode changé jusqu'à ce qu'il
passe. C'est « modifier le harnais pour faire passer un signal », transposé au
corpus — l'interdit constitutionnel, sous un autre nom.

## Le choix

**Le texte qui fait foi est l'union de deux extractions fixées d'avance et
identiques pour tous les papiers** — `pypdf` en mode par défaut et en mode
`layout` — produites par `corpus/extract_text.py`, **versionnées** dans
`corpus/text/`, et la version de `pypdf` est inscrite dans
`corpus/text/MANIFEST.json` — **hors** des fichiers de texte, pour ne pas polluer
ce que `F2` fouille.
`F2` tient une citation pour trouvée quand elle est présente à la lettre dans
**au moins une** des deux.

## Pourquoi

**L'union répare la classe « défaut d'outil » sans toucher à l'exigence.** Il
faut toujours une chaîne présente **à la lettre** dans une extraction réelle du
PDF réel. On n'assouplit pas ce qui est exigé ; on cesse de faire dépendre le
verdict d'un réglage que personne n'avait choisi.

**Et elle ne dissout pas la liste close de `D16`** — c'est la vérification qui
décide. En retirant les réparations déclarées d'Andersen & Bollerslev, l'union
rend **3 citations introuvables** : le scan de 1997 écrit « fight part » pour
« right part » dans les *deux* modes. `ocr`, `math_notation` et `table` gardent
donc exactement le rôle que `D16` leur a donné, et `L18` garde le sien : on ne
les élargit pas pour couvrir un défaut d'outil.

**Le nombre d'extractions est fermé, et le même pour tous.** C'est ce qui
distingue l'union de l'option 4 : aucun papier n'a de réglage propre, donc aucun
réglage ne peut être ajusté en voyant un résultat. Ajouter une troisième
extraction — un OCR, un autre moteur — est une décision écrite, pas un geste.

**Le texte est versionné parce que `F2` doit être rejouable sans les PDF.** Les
PDF restent hors dépôt (`.gitignore`, et `L18` bis : leur présence n'est pas un
fait du dépôt). Le texte, lui, est un **résultat** — au même titre que les
fiches, que `CLAUDE.md` versionne pour cette raison exacte. Sans lui, une session
qui n'a pas les PDF ne peut ni vérifier ni contester une `quoted_source`.

**Ce que ça coûte.** **6,2 Mo** de texte au dépôt pour 18 papiers — chiffre
**mesuré après production** ; la première rédaction annonçait 3,5 Mo, estimés sur
la taille *normalisée*, alors que le mode `layout` garde l'alignement des
colonnes en espaces et occupe donc bien plus de place sur le disque qu'il n'en
pèse pour `F2`. Et un
doublement du travail de `F2` à chaque vérification — négligeable, la recherche
étant une sous-chaîne sur quelques centaines de milliers de caractères. Coût
réel et assumé : **deux extractions à maintenir** au lieu d'une, et une montée de
version de `pypdf` qui changerait le texte périme les `quoted_source` — d'où le
manifeste, qui porte la version et l'empreinte de chaque fichier pour que la
péremption soit **bruyante** au lieu d'être silencieuse.

**Le moment est le moins cher possible.** `D16` pose que changer une condition
périme tout résultat d'extraction antérieur. Le § Journal de `D16` est **vide** :
il n'y en a aucun. Comme `D10` en son temps, c'est la dernière fois que ce
changement est gratuit.

## Ce que ça verrouille

- **`F2` change de définition**, donc `corpus/score_extraction.py` change. Les
  cinq conditions restent cinq ; c'est leur entrée qui est désormais nommée.
- **`corpus/text/` devient une pièce du dépôt**, produite par un script et jamais
  à la main. Un texte édité à la main serait un endroit où loger une citation.
- **Toute `quoted_source` du projet est définie contre ces deux extractions-là**,
  à cette version de `pypdf`. En changer périme les réparations déclarées, et le
  § Journal devra le dire.
- **La question « faut-il un OCR » est tranchée par la négative pour l'instant**,
  et rouvrable : le scan de 1997 reste lisible via réparation déclarée, ce qui
  suffit tant qu'un papier n'est pas illisible au point que `F2` ne trouve rien.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Un papier dont le texte n'est pas un PDF** — l'entrée 9 est un billet HTML, atteignable pour `D17` et infichable pour `F4` qui exige un `source.pdf`. La présente décision ne traite que des PDF | avant de ficher l'entrée 9 |
| **Un papier atteignable mais illisible** — scan si dégradé que `F2` ne trouve rien même réparé. Aucun cas rencontré à ce jour | au premier cas rencontré |
| **Ajouter une troisième extraction** (OCR, autre moteur) si un papier l'impose. Le seuil est écrit ici : il faut un papier dont l'union des deux modes ne rend **aucune** citation vérifiable | au premier cas rencontré |
| **La montée de version de `pypdf`** : elle peut changer le texte et périmer les `quoted_source`. Le rejeu de `corpus/extract_text.py --check` le dira | à chaque montée |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Ce qui a changé | Effet mesuré |
|---|---|---|---|
| 1 | 2026-09-21 | décision prise ; `corpus/text/` produit, `F2` cherche dans l'union | les 3 fiches de référence tiennent `F2` ; sans les réparations d'Andersen & Bollerslev, 3 citations redeviennent introuvables — la liste close garde son rôle |
| 2 | 2026-09-21 | correction d'un chiffre de la présente décision : le coût en disque était annoncé à 3,5 Mo, il vaut **6,2 Mo** | estimé sur la taille normalisée au lieu de la taille du fichier ; le mode `layout` pad avec des espaces. Le choix ne change pas, son coût était sous-évalué de 77 % |
