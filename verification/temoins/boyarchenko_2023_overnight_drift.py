"""Boyarchenko, Larsen, Whelan - The Overnight Drift (RSV_close).

Part transposee : le desequilibre d'ordres relatif de fin de seance US,
RSV = (achats - ventes) / (achats + ventes), borne dans [-1, 1], mesure sur la
fenetre horloge 15:15-16:15 ET, lu a la barre d'ancrage de `_common.run`.

Ce qui ne se transpose pas, et ce qui manquait :
- le papier classe des TRADES tick-by-tick contre le meilleur bid/ask ; la
  couche de donnees ne donne que des clotures de barres. Substitut (pas le
  signal du papier) : les variations de cloture de la fenetre ; la somme des
  hausses joue les achats, la somme des baisses (en valeur absolue) joue les
  ventes, RSV = (hausses - baisses) / (hausses + baisses), dans [-1, 1]. Ce
  sont des mouvements de prix, pas des contrats.
- le papier mesure le rendement 02:00-03:00 ET ; ce module ne produit que le
  score de fin de seance, il ne code ni la fenetre cible, ni BtD, ni le VIX.
- aucun parametre de normalisation : RSV est brut, comme dans le papier.
"""

from __future__ import annotations

import pandas as pd

from signals import _common

SIGNAL_ID = "boyarchenko-2023-overnight-drift"
HYPOTHESIS = None
PAPER = "Boyarchenko, Larsen, Whelan (2022), The Overnight Drift, Federal Reserve Bank of New York Staff Reports no. 917"
EXPECTED_SIGN = -1

CHOICES = (
    "la fiche dit que RSV_close negatif predit un rendement 02:00-03:00 positif ; j'ai garde RSV brut comme score et EXPECTED_SIGN = -1, parce que le papier emploie RSV tel quel et que son coefficient est negatif (pas d'inversion de signe dans le score).",
    "la fiche classe les trades contre le meilleur bid/ask ; la couche ne donne que des clotures de barres, j'ai donc pris comme achats la somme des hausses de cloture et comme ventes la somme des baisses en valeur absolue, RSV = (hausses - baisses) / (hausses + baisses) ; ce sont des mouvements de prix et non des contrats, ce n'est pas le signal du papier, faute de trades et de cotes. Une version qui compte les barres donnait trop peu de valeurs distinctes (S4), d'ou la somme des variations, qui garde la borne [-1, 1].",
    "la fiche mesure sur 15:15-16:15 ET (minutes 915 a 975) ; j'ai pris les variations dont la barre a une heure ET, en minutes entieres, dans [915, 975] et une position au plus egale a la barre notee, parce que le predicteur ne lit rien au-dela de sa position.",
    "la fiche ne mesure que la cloture US de l'ES ; j'ai pose un score uniquement sur les cellules de fenetre US, pour toutes les racines demandees, parce que le papier ne dit rien des autres instruments ; l'ancrage est celui de _common.run (horizon_bars avant la cloture declaree), donc la fenetre est tronquee a l'ancre, et non lue jusqu'a 16:15.",
    "la fiche donne une fenetre en heure ET qui suit l'heure d'ete americaine ; j'ai converti l'index en America/New_York, parce que le papier convertit UT en ET.",
    "la fiche ne dit rien du denominateur nul ; j'ecris aucun score (None) si hausses + baisses vaut 0, plutot que d'inventer 0.",
    "la fiche n'applique aucune standardisation de RSV (rsv_normalization_window null) ; aucune normalisation, aucun seuil BtD, aucun conditionnement VIX dans le score.",
    "la fiche ne dit pas comment traiter les jours feries ou seances raccourcies ; je ne les traite pas, la fenetre d'horloge peut etre vide et alors aucun score n'est ecrit.",
)

_DEBUT = 915
_FIN = 975
_FENETRE_CELLULE = "US"


def _rsv(closes: pd.Series, position: int):
    vus = closes.iloc[: position + 1]
    heures = vus.index.tz_convert("America/New_York")
    minutes = heures.hour * 60 + heures.minute
    dans = (minutes >= _DEBUT) & (minutes <= _FIN)
    pas = vus.diff()
    achats = float(pas.where((pas > 0) & dans, 0.0).sum())
    ventes = float(-pas.where((pas < 0) & dans, 0.0).sum())
    brut = achats + ventes
    if brut == 0:
        return None
    return (achats - ventes) / brut


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} pour les cellules de fenetre US."""
    base = list(panel.cells()) if cells is None else list(cells)
    retenues = [c for c in base if c[1] == _FENETRE_CELLULE]
    if not retenues:
        return {}
    return _common.run(panel, _rsv, cells=retenues, horizon_bars=horizon_bars)
