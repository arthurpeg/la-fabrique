# D24 — *Atteignable* et *fichable* sont deux choses

**Date :** 2026-09-23
**Phase :** 07
**État :** prise

## La question

`D17` compte en `G1` les papiers **atteignables non fichés**, et exige zéro. Le
recensement du 2026-09-22 déclare l'entrée 9 — un billet de la Fed de New York —
`atteignable` : son texte s'obtient sans péage ni démarche. Mais `F4` de `D16`
exige un `source.pdf`, et `D18` ne fixe le texte qui fait foi que pour les PDF.
Ce papier est donc **atteignable et infichable à la fois**, et `G1` vaut 1 ou 0
selon la lecture — sans qu'aucune des deux soit fautive.

## Les options

**1. Étendre `D18` au HTML.** Une troisième extraction déclarée, et `F4` accepte
un `source.html`. Écartée : elle ficherait l'entrée 9 pour de bon, mais ouvre un
chantier disproportionné à un seul billet — quel extracteur HTML, figé à quelle
version, et un billet n'a ni pages ni sections, deux choses que le schéma de
morceaux et la pagination de `D18` tiennent pour acquises. Rien n'interdit d'y
venir ; rien ne justifie d'y venir maintenant.

**2. Laisser l'entrée 9 bloquer la porte.** Cohérent avec *« une porte à moitié
franchie est une porte non franchie »*. Écartée : la porte 07 juge **un
extracteur**, pas un inventaire. Un extracteur qui produit dix-sept fiches sans
une retouche a répondu à la question posée ; le bloquer sur un format de fichier
qu'il n'a jamais prétendu savoir lire mesure autre chose que ce qu'on voulait
mesurer.

**3. Distinguer *atteignable* de *fichable*.** Retenue.

**4. Retirer l'entrée 9 du recensement.** Écartée sans hésiter, et elle mérite
d'être écrite parce qu'elle est la tentation : un papier qu'on efface parce
qu'il gêne un compteur est exactement ce que `G4` existe pour empêcher.

## Le choix

**Un papier est `atteignable` quand son texte s'obtient sans péage ni démarche ;
il est `fichable` quand il existe, en plus, un texte qui fait foi au sens de
`D18`. `G1` ne compte que les papiers FICHABLES non fichés.** Le recensement
porte les deux états, et tout papier atteignable-mais-non-fichable est inscrit
avec **la raison** qui l'empêche — mêmes exigences que `G4`.

## Pourquoi

**Les deux notions répondent à deux questions différentes, et les confondre les
abîme toutes les deux.** *Atteignable* dit ce que le monde nous consent : c'est
un fait sur l'extérieur, daté, susceptible de changer — l'entrée 1 est devenue
inatteignable le 2026-09-22 (`L20`), une autre pourrait redevenir atteignable
demain. *Fichable* dit ce que **notre outillage** sait traiter : c'est un fait
sur nous. Mettre les deux sous un même mot fait dépendre un compte du monde
extérieur d'une limite de notre code, et réciproquement.

**Ce que ça coûte, et c'est le vrai prix.** `G1 = 0` ne voudra plus dire « tout
ce qu'on peut obtenir est fiché » mais « tout ce qu'on sait lire est fiché ». La
porte devient franchissable **en n'améliorant pas l'outillage**, ce qui est
précisément le genre de relâchement dont ce dépôt se méfie. La parade est que le
non-fichable ne disparaisse pas : il est **compté, nommé, et sa raison écrite**,
exactement comme l'inatteignable de `G4`. Un papier qui sort de `G1` entre dans
une colonne visible, jamais dans le silence.

**C'est la même forme que `D17` a déjà employée** en cessant d'exiger « 20
fiches » : ce qui compte n'est pas un nombre de papiers mais **ce que l'automate
sait faire de ce qu'on lui donne**. Un format que l'extracteur ne sait pas lire
n'est pas un échec de l'extracteur.

**Et c'est `L22` appliqué à l'envers.** `L22` dit qu'une condition sans moyen de
mesure n'est pas tenue mais absente. Ici, `G1` avait un moyen de mesure qui
mélangeait deux populations : il mesurait quelque chose, mais pas ce qu'il
annonçait. Un compteur juste sur la mauvaise population est un compteur faux.

## Ce que ça verrouille

- **`corpus/acquisition.json` porte désormais `fichable`** — un booléen — et
  `fichable_reason` quand il vaut faux. Le recensement est produit par
  `corpus/probe_acquisition.py` et gardé par `corpus/check_acquisition.py`.
- **`scripts/gate_07.py` compte `G1` sur les fichables**, et imprime les
  atteignables-non-fichables dans une colonne à part, avec leur raison. Il cesse
  d'imprimer deux lectures : il n'y en a plus qu'une.
- **`corpus/extract_fiche.py --list` et `gate_07.py` doivent s'accorder.** Leur
  désaccord du 2026-09-23 est ce qui a rendu cette décision nécessaire ; qu'ils
  divergent à nouveau est un symptôme, pas un détail.
- **En changer coûte peu aujourd'hui, cher plus tard** : si `D18` s'étend un jour
  au HTML, l'entrée 9 redevient fichable, `G1` repasse à 1, et **la porte 07 est
  réputée non franchie jusqu'à ce qu'elle soit fichée**. C'est écrit ici pour que
  personne n'ait à le redécouvrir.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Le texte qui fait foi pour le HTML** — quel extracteur, figé à quelle version, et ce que deviennent page et section pour un document qui n'en a pas | si un second papier non-PDF apparaît, ou en phase 09 |
| **Les autres formats** — un papier en `.tex`, une vidéo, un notebook. La présente décision ne dit rien d'eux : elle ouvre la colonne, pas la liste | à leur apparition |
| **Le seuil de tolérance** — combien de papiers atteignables-non-fichables avant que la limite d'outillage cesse d'être acceptable. Aucun nombre n'est fixé ici, et il en faudra un si la colonne grossit | quand elle dépassera deux |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | Atteignables | Fichables | Non fichables | `G1` |
|---|---|---|---|---|---|
| — | 2026-09-23 | 18 | 17 | 1 — entrée 9, `format_non_traite` | décision écrite |
| — | 2026-09-23 | 18 | 17 | 1 — entrée 9, `format_non_traite` | **`G1` = 0, PORTE 07 FRANCHIE** — `scripts/gate_07.py` et `corpus/extract_fiche.py --list` s'accordent |
