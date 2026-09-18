# H01 — La première demi-heure d'une séance prédit sa dernière

**Écrite le :** 2026-09-17, avant toute mesure sur nos données
**Signal :** `gao-2018-intraday-momentum` (`signals/gao_2018_intraday_momentum.py`)
**Origine :** Gao, Han, Li & Zhou (2018), « Market intraday momentum », *JFE*
129(2):394-414 — `corpus/AMORCE.md`, entrée 1
**Statut :** **testée le 2026-09-18** — voir « Le résultat » en fin de fichier.
L'affirmation ci-dessous n'a pas été touchée d'un mot depuis le 2026-09-17.

## Ce qui est affirmé

Dans une fenêtre de séance donnée, le rendement des **trente premières minutes**
prédit **positivement** le rendement des **trente dernières minutes** de la même
fenêtre, sur le même instrument.

Le signe est **positif**. C'est l'affirmation principale, et c'est elle qui se
teste en premier : sur 4,22 paris indépendants, un signe inversé coûte plus cher
qu'une magnitude mal estimée.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), pas trois.
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre et de la séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule** — la barre dont l'horizon de
  30 minutes se termine à la clôture de la fenêtre.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | entre **0,01 et 0,05** en IC de Spearman |
| Cible `D01` §2 | 0,018 (fenêtres indépendantes) et 0,031 (dépendantes) |

La borne haute de 0,05 n'est pas une prédiction : c'est le plafond au-delà duquel
il faudra chercher l'erreur avant de chercher le profit. Gao et al. rapportent un
R² de l'ordre de 1 % sur SPY, ce qui correspond à une corrélation d'environ 0,10
— **sur un ETF d'actions, en journalier, sur 1993-2013**. Nous mesurons autre
chose, sur autre chose : rien ne justifie d'attendre le même chiffre.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de 2 en valeur absolue : le
  motif existe mais à l'envers, et l'hypothèse est fausse telle qu'écrite.
- Un IC poolé dont le `t` **final** (déflaté deux fois, `D04`) reste sous 2 : rien
  à distinguer du bruit sur cet univers.
- Un IC positif porté par **une seule cellule** sur les 25, les autres étant
  nulles ou négatives : ce ne serait pas le motif de Gao et al., ce serait un
  accident d'instrument, et la ventilation par cellule le montrera.
- Un IC net négatif une fois le coût d'aller-retour complet — ce qui exige les
  frais, encore `null` au catalogue.

## Ce qui n'est pas affirmé ici

Gao et al. affirment aussi que l'effet est **plus fort les jours volatils, à gros
volume, et les jours d'annonce macro**. C'est une hypothèse conditionnelle
distincte, qui appartient aux régimes (phase 13), et qui devra être
pré-enregistrée séparément. La tester en même temps que celle-ci et retenir la
meilleure des deux serait exactement ce que le registre est là pour rendre
visible.

---

## Le résultat

**Mesuré le 2026-09-18**, test `T-20260918T064151-bc4048` au registre. Tranche `pool`, as-of
2023-12-29, 25 cellules, 45 908 observations, harnais `e9ef2087`. Recopié du
rapport d'IC officiel ; le registre fait foi.

| | |
|---|---|
| IC poolé | **−0,01061** |
| t naïf | −2,27 |
| t recouvrement | −0,42 (÷ 5,48) |
| **t final** | **−0,28** (÷ 1,46) |

**Verdict, selon les critères écrits avant la mesure.** Le signe observé est
négatif là où le signe attendu était positif — mais la clause qui s'applique
n'est pas « le motif existe à l'envers », qui exigeait un `t` final **au-delà de
2** en valeur absolue. C'est la clause suivante : *« un IC poolé dont le `t`
final reste sous 2 : rien à distinguer du bruit sur cet univers »*.

**L'hypothèse n'est pas confirmée. Elle n'est pas non plus retournée.** Il n'y a
rien ici, et c'est un résultat.

Ce qui emporte le chiffre est la **double déflation** de `D04` : un `t` naïf de
−2,27 — qu'un calcul sans précaution aurait appelé significatif — devient −0,28
après division par 5,48 (recouvrement de 30 barres) puis par 1,46 (9 instruments
pour 4,22 paris). Un facteur 8. C'est la première fois qu'on la voit mordre.

La ventilation par cellule est un **diagnostic, pas 25 tests** (`D01` §4) : 15
cellules négatives, 10 positives, la plus forte à −0,049 (`ES × ASIA`). Aucune
cellule ne porte le résultat ; il n'y a pas de résultat à porter.

**Ce que ça n'autorise pas.** Retester le même signal à un autre horizon, ou sur
un sous-ensemble de cellules, après avoir vu ceci, serait une nouvelle hypothèse
— pré-enregistrée avant, et comptée en plus.
