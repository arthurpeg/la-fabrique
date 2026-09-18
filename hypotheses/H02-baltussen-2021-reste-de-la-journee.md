# H02 — Le reste de la séance prédit sa dernière demi-heure

**Écrite le :** 2026-09-17, avant toute mesure sur nos données
**Signal :** `baltussen-2021-intraday-momentum`
(`signals/baltussen_2021_intraday_momentum.py`)
**Origine :** Baltussen, Da, Lammers & Martens (2021), « Hedging demand and market
intraday momentum », *JFE* 142(1) — `corpus/AMORCE.md`, entrée 2
**Statut :** **testée le 2026-09-18** — voir « Le résultat » en fin de fichier.
L'affirmation ci-dessous n'a pas été touchée d'un mot depuis le 2026-09-17.

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement accumulé **depuis l'ouverture de
la fenêtre jusqu'à trente minutes de sa clôture** prédit **positivement** le
rendement des **trente dernières minutes**.

Le signe est **positif**.

Le prédicteur diffère de [H01](H01-gao-2018-premiere-demi-heure.md) : là où Gao
et al. ne regardent que les trente premières minutes, Baltussen et al. regardent
**tout ce qui précède**. Les deux hypothèses portent sur la même cible et sont
donc corrélées — c'est voulu, et c'est ce qui les rend utiles comme paire
d'étalons. Elles ne seront **jamais comptées comme deux tests indépendants**.

## Pourquoi cette référence pèse plus que l'autre

Baltussen et al. mesurent sur **60 et quelques futures** — actions, taux,
matières premières, devises, 1974-2020. C'est notre classe d'actifs, notre
granularité, et un univers dont le nôtre est un sous-ensemble. Et ils avancent un
**mécanisme** : la couverture de gamma court des vendeurs d'options et des ETF à
levier, qui force des achats en fin de séance dans le sens du mouvement du jour.
Une hypothèse avec un mécanisme se falsifie mieux qu'une régularité nue : si le
motif existe sans le mécanisme, il faut s'en méfier davantage, pas moins.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3).
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre et de la séance.
- **Tranche :** `pool` uniquement.
- **Une observation par séance et par cellule.**

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | entre **0,01 et 0,05** en IC de Spearman |
| Par rapport à H01 | **au moins aussi fort**, le prédicteur portant plus d'information |

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de 2 en valeur absolue.
- Un `t` final sous 2 : indistinguable du bruit sur cet univers.
- Un IC **franchement inférieur à celui de H01** : le prédicteur le plus riche
  ferait moins bien que le plus pauvre, ce qui contredirait le mécanisme avancé
  autant que le résultat publié.
- Un effet présent sur les indices actions et **absent partout ailleurs** : le
  mécanisme invoqué — options et ETF à levier — est propre aux actions, donc ce
  résultat ne contredirait pas le papier, mais il contredirait sa transposition à
  nos neuf instruments, et c'est elle qui est écrite ici.

## Ce qui n'est pas affirmé ici

Baltussen et al. rapportent aussi une **réversion les jours suivants**. Elle est
hors de notre grille : notre horizon est intraday à clôture forcée (`D01` §3), et
une hypothèse de réversion à plusieurs jours n'y a pas de place. Elle n'est pas
écartée — elle est **hors domaine**, et le redeviendrait si l'horizon changeait
(ledger F04, F05).

---

## Le résultat

**Mesuré le 2026-09-18**, test `T-20260918T064409-acc2e3` au registre. Tranche `pool`, as-of
2023-12-29, 25 cellules, 45 911 observations, harnais `e9ef2087`. Recopié du
rapport d'IC officiel ; le registre fait foi.

| | |
|---|---|
| IC poolé | **−0,00432** |
| t naïf | −0,92 |
| t recouvrement | −0,17 (÷ 5,48) |
| **t final** | **−0,12** (÷ 1,46) |

**Verdict, selon les critères écrits avant la mesure.** Comme pour
[H01](H01-gao-2018-premiere-demi-heure.md) : signe négatif contre signe positif
attendu, mais `t` final très en deçà de 2. **Rien à distinguer du bruit.**

**Et la prédiction relative est démentie.** `H02` affirmait être « **au moins
aussi forte** que `H01`, le prédicteur portant plus d'information ». Elle est
**plus faible** : |−0,00432| contre |−0,01061|. Regarder tout ce qui précède
plutôt que la seule première demi-heure n'a rien ajouté — sur notre univers, à
cet horizon, dans cette tranche.

C'est la partie du résultat qui apprend quelque chose. Les deux nombres étant
dans le bruit, l'écart entre eux l'est aussi : on ne peut pas conclure que le
prédicteur large est *pire*, seulement qu'il n'est pas meilleur, et que la raison
avancée pour l'attendre meilleur ne s'est pas manifestée.

**Comptage.** `H01` et `H02` portent sur la même cible. Le registre porte deux
lignes parce que deux IC ont été calculés ; toute correction de tests multiples
devra traiter la paire comme **corrélée, jamais indépendante**.
