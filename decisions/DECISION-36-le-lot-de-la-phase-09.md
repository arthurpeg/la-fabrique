# D36 — Le lot de la phase 09 est un critère, pas un nombre

> **Renumérotée le 2026-09-30 : D27 → D36.** Deux décisions portaient le numéro
> `D27` ; la plus ancienne (l'instant de troncature, 2026-09-26) le garde. Toute
> mention de « `D27` » à propos du lot, dans les fichiers append-only
> (`LECONS.md`, `wiki/log.md`) et l'historique git, désigne celle-ci.

**Date :** 2026-09-28
**Phase :** 09
**État :** prise — amende `D25` § Le choix, clause `C2`

## La question

`D25` engage un lot de **50 signaux clos avant la première mesure**. Ce chiffre
a été écrit le 2026-09-23, quand le corpus portait **17 fiches** : c'était une
estimation de ce qu'on espérait atteindre, pas une mesure. Le corpus en porte
**51** aujourd'hui et le moissonné est **épuisé**. Il faut dire ce qu'est le lot
avant de coder le premier signal, faute de quoi il sera composé après coup.

## Ce que le corpus porte réellement, mesuré le 2026-09-28

Chaque papier fiché a été **trié**, et ce triage a lui-même été jugé contre un
étalon humain (`D15`, quatre conditions en effectifs). Le compte par classe :

| Classe | Compte | Ce que `D15` en dit |
|---|---|---|
| `oui` | **16** | calculable en OHLCV seul, sans donnée extérieure |
| `partiel` — transposition d'univers | **24** | la méthode se transpose ; le papier étudiait un autre marché |
| `partiel` — donnée manquante | 2 | exige un calendrier, une échéance : **non codable** |
| `partiel` — sans raison écrite | 5 | l'étalon humain ne porte pas de motif : **indécidable** |
| `non` | 2 | fichées, hors sujet |

**50 ne tient pas**, et n'y tiendrait qu'en versant dans le lot des papiers qui
exigent une donnée que nous n'avons pas.

## Les options

**1. Tenir `N` = 50 en complétant le lot.** Écartée, et c'est celle qu'il faut
écarter explicitement parce qu'elle se choisit toute seule quand on ne décide
pas. Les seuls candidats restants sont les `partiel` à donnée manquante et les
`non` : on ne peut pas en écrire le signal. Le lot serait nominalement plein et
réellement creux.

**2. Relancer un moissonnage** (`D20`, `D21`) pour élargir jusqu'à 50. Écartée
**pour l'instant**, pas sur le fond : elle reste ouverte et c'est même la voie
d'un élargissement futur. Mais elle retarde la phase d'autant, et rien ne dit
que la seconde récolte vaudra la première — `D25` prévient que le rendement
chute quand on ajoute des papiers **moins bons**.

**3. Fixer un `N` plus petit**, 32 ou 40. Écartée sur la **forme**. Un nombre
rond se justifie après coup, et personne ne saura dans six mois s'il a été
choisi avant ou après avoir regardé les fiches. C'est `F37` : un seuil en
effectif déguisé en chiffre.

**4. Remplacer le nombre par un critère vérifiable.** Retenue.

## Le choix

**Le lot de la phase 09 est l'ensemble des fiches dont le papier a été trié
`oui`, plus celles triées `partiel` dont la raison écrite est une transposition
d'univers — jamais celles dont le `partiel` tient à une donnée manquante, ni
celles dont l'horizon est incompatible avec la grille intraday.**

**La troisième catégorie a été trouvée en appliquant la décision**, le jour même :
Moskowitz (2012) n'exige aucune donnée manquante — le signe d'un rendement passé
est du pur OHLCV — mais son horizon est mensuel de bout en bout, look-back de
12 mois et détention de 1 mois, quand notre grille est intraday **à clôture
forcée** (`D01` §3). Ce n'est ni une donnée manquante ni une transposition : la
ranger dans l'une des deux aurait menti sur la raison (`L18`). C'est le motif
qui avait déjà écarté la famille carry en phase 01 (`F04`, `F05`).

`corpus/lot_phase09.py` applique ce critère et écrit `hypotheses/LOT-09.json`.
Au 2026-09-28 il rend **`N` = 40**, et **ce nombre se relance** (`L21`) : toute
prose de ce dépôt qui le porte sans l'avoir recalculé est périmée.

Les quatre clauses de `D25` sont **inchangées** : `BH` unilatéral au signe
pré-enregistré (`C1`), lot **clos** avant la première mesure (`C2`), `q` = 0,10
(`C3`), et le dénominateur de la phase 15 reste le **registre entier** (`C4`).

## Pourquoi

**Parce que `D25` le dit elle-même.** Son § Pourquoi : *« Ce qui la dégraderait,
c'est de tester des papiers **moins bons**. Le vrai budget porte sur la
**qualité du corpus**, pas sur le nombre de lignes du registre. »* Compléter le
lot jusqu'à 50 avec des papiers dont le signal ne peut pas s'écrire est
exactement ce dont elle met en garde. Le 50 n'était pas un objectif à tenir ;
c'était une estimation, et elle s'est révélée fausse dans le bon sens — le
corpus est plus riche en fiches et plus pauvre en codables.

**Parce qu'un critère se vérifie et qu'un nombre se justifie.** Le critère
s'applique par un script, sur des verdicts écrits **avant** que quiconque ait vu
une fiche. La session qui compose le lot a lu les fiches : elle ne peut plus les
trier sans biais (`F42`), et le critère la dispense d'avoir à le faire.

**Ce que ça coûte à la puissance, chiffré.** L'échelle de `BH` se resserre à
peine :

| | `N` = 50 (`D25`) | **`N` = 40 (ici)** |
|---|---|---|
| `t` requis pour le 1ᵉʳ retenu | 2,88 | **2,81** |
| pour le 3ᵉ | 2,51 | **2,43** |
| pour le 5ᵉ | 2,33 | **2,24** |

La barre **descend**. Ce qu'on perd n'est pas la sévérité du seuil mais le
nombre d'occasions : `D25` a mesuré que sous FDR les vrais signaux trouvés
croissent proportionnellement à `N`. Dix papiers de moins, c'est
proportionnellement moins de découvertes possibles — et c'est le vrai coût de
cette décision.

**Ce qu'on sacrifie aussi, et qui est réparable.** Cinq fiches d'`AMORCE.md`
sortent du lot pour une raison qui ne leur est pas imputable : l'étalon humain
de phase 01 **ne porte pas de motif écrit**, donc leur `partiel` est indécidable
au regard du critère. Les lire une par une et inscrire leur motif est un geste
humain légitime, qui les ferait rentrer ; il s'inscrira au § Journal, avec la
date et qui l'a fait.

## Ce que ça verrouille

- **`hypotheses/LOT-09.json` est écrit par `corpus/lot_phase09.py --ecrire`**, et
  porte sa date. Dès qu'une mesure a eu lieu, **l'élargir casse `BH`** (`D25`
  `C2`) : la famille doit être close pour que la procédure soit valide.
- **`scripts/gate_09.py` lit ce fichier** et refuse tout verdict si le lot est
  mal formé, si une hypothèse manque, ou si une mesure manque.
- **Le compte ne se recopie jamais.** `L21` s'applique : `gate_09` et toute
  prose citant `N` doivent le relancer.
- **En changer le critère périme le lot.** Si la règle bouge après la première
  mesure, tous les résultats deviennent exploratoires et la phase 09 recommence
  sur un lot neuf — même clause que `D25` pour `q`, `N` et l'unilatéralité.
- **Un moissonnage ultérieur ne rouvre pas un lot clos.** Il ouvrirait un
  **second** lot, avec sa propre correction, et le dénominateur de la phase 15
  les compterait tous les deux (`C4`).

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Les 5 `partiel` d'`AMORCE` sans motif écrit** — les lire et inscrire leur raison les ferait rentrer dans le lot | avant `--ecrire`, ou jamais |
| **La liste `DONNEE_MANQUANTE` du script** est close et volontairement large : dans le doute la fiche sort. Un faux exclu coûte une hypothèse, un faux inclus coûte un signal qu'on découvre inécrivable au moment de le coder | à la première fiche mal classée |
| **La matrice de corrélation** des signaux du lot, exigée par `D25` avant d'appliquer `BH` | avant la première mesure |
| **Un second moissonnage**, qui ouvrirait un second lot plutôt que d'élargir celui-ci | après la phase 09 |

## Journal des passages

*Un passage par ligne, écrit après coup, jamais effacé.*

| # | Date | `N` rendu | Note |
|---|---|---|---|
| — | 2026-09-28 | **40** | critère écrit ; lot non encore figé |
| 1 | 2026-09-28 | **41** | **Les 5 `partiel` d'`AMORCE` sans motif ont été LUS**, fiche par fiche, et leur raison inscrite dans `corpus/motifs_amorce_partiel.json`. Une entre (`lou-2019-tug-of-war` : décomposition intraday/overnight en pur OHLCV ; seul le tri en déciles ne transpose pas). Trois sortent pour **donnée manquante** — `andersen-2003` exige la médiane des prévisions MMS, `kurov-2021` et `lucca-moench-2015` le calendrier FOMC. Une sort pour **horizon incompatible**, catégorie créée à cette occasion. **Lu par une session qui avait déjà lu les fiches** : elle n'a pas rejugé le `partiel` de l'étalon, seulement classé sa raison ; le biais est déclaré dans le fichier, comme `D15` § Journal le fait pour le trieur. **LOT FIGÉ** le 2026-09-28 par `--ecrire` : `hypotheses/LOT-09.json`, `N` = 41. Il est **clos** — l'élargir après une mesure casse `BH` (`D25` C2). |
