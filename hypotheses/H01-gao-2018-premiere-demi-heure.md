# H01 — La première demi-heure d'une séance prédit sa dernière

**Écrite le :** 2026-09-17, avant toute mesure sur nos données
**Signal :** `gao-2018-intraday-momentum` (`signals/gao_2018_intraday_momentum.py`)
**Origine :** Gao, Han, Li & Zhou (2018), « Market intraday momentum », *JFE*
129(2):394-414 — `corpus/AMORCE.md`, entrée 1
**Statut :** pré-enregistrée, **non testée**

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
