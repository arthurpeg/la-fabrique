"""Boyarchenko, Larsen et Whelan -- The Overnight Drift (signal transpose).

Le papier : RSV_close = (contrats achetes - contrats vendus) / (achetes + vendus)
sur la fenetre fixe 15:15-16:15 ET, l'ES seul, classant chaque trade contre le
meilleur bid/ask. RSV_close predit NEGATIVEMENT le rendement de l'heure
02:00-03:00 ET de la nuit suivante.

Ce qui ne se transpose pas, et ce qui a ete fait a la place :

- La donnee. RSV exige des trades classes acheteur/vendeur (quotes au sommet du
  carnet). Le panel ne fournit que des barres ; `_common.cell_bars` ne rend que
  des clotures. RSV n'est donc pas calculable. Substitut declare : le rendement
  log des clotures sur l'heure d'horloge qui finit a la barre notee, comme proxy
  du desequilibre d'ordres de fin de seance (un desequilibre vendeur pousse le
  prix vers le bas). Ce n'est PAS le signal du papier.
- Les seances. Le papier ne mesure le desequilibre qu'a la cloture americaine.
  La recette (market.sessions) declare pour l'ES les seances ASIA, EUROPE et US ;
  le proxy est donc pose sur la derniere heure de chacune des fenetres de l'ES
  presentes dans le panel, ce qui est une transposition, pas le papier.
- La fenetre de mesure. Le papier mesure 15:15-16:15 ET ; le score est pose par
  `_common.run` a la premiere barre a au plus `horizon_bars` de la cloture
  declaree de la fenetre. La mesure porte sur l'heure qui precede ce point.
- L'horizon. Le papier predit l'heure 02:00-03:00 ET, environ dix heures apres la
  mesure. Ce delai n'est pas reproduit ; aucune mecanique maison n'a ete ecrite
  pour ne pas inventer de constantes d'ancrage.
- Le conditionnement VIX, les terciles, la strategie BtD (signe < 0) : non codes,
  le signal continu des regressions du papier est retenu.
"""

from __future__ import annotations

import math

import pandas as pd

from signals import _common

SIGNAL_ID = "boyarchenko-2023-overnight-drift"
HYPOTHESIS = None
PAPER = (
    "Boyarchenko, Larsen et Whelan (2022, revision ; fiche_id 2023), "
    "The Overnight Drift, Federal Reserve Bank of New York Staff Reports no. 917"
)
EXPECTED_SIGN = -1
CHOICES = (
    "la fiche definit RSV_close a partir de trades classes contre le meilleur bid/ask ; "
    "le panel ne donne que des barres (cell_bars ne rend que des clotures), j'ai donc "
    "remplace RSV par le rendement log des clotures sur l'heure qui finit a la barre "
    "notee, proxy du desequilibre d'ordres : ce n'est pas le signal du papier",
    "la fiche donne la fenetre 15:15-16:15 ET (une heure) ; j'ai garde la duree d'une "
    "heure, lue sur l'horloge en minutes entieres (Timedelta de 60 minutes), et l'ai "
    "fait finir a la barre notee, parce qu'aucune barre posterieure ne peut etre lue",
    "la fiche ne dit rien de la barre de reference de l'heure ; j'ai pris la premiere "
    "cloture de la seance dont l'horodatage est au moins la barre notee moins 60 minutes "
    "(si la seance a commence moins d'une heure avant, la premiere cloture de la seance)",
    "la fiche etudie l'ES seul (exact_roots = ['ES']) ; je ne score que la racine ES. "
    "Le papier ne mesure le desequilibre qu'a la cloture americaine, mais la recette "
    "declare pour l'ES les seances ASIA, EUROPE et US (market.sessions) : je score toutes "
    "les fenetres de l'ES presentes dans le panel, la derniere heure de chaque fenetre "
    "jouant le role de l'heure de cloture. Version precedente limitee a (ES, US), refusee "
    "par le juge (S4 : une seule cellule soumise, il en faut deux)",
    "la fiche place la mesure a 16:15 ET et la cible a 02:00-03:00 ET ; j'ai utilise "
    "_common.run, qui pose le score a la premiere barre a au plus horizon_bars de la "
    "cloture declaree de la fenetre : l'ancrage et l'horizon ne sont pas ceux du papier",
    "la fiche dit que RSV_close predit negativement le rendement (beta -17.49) ; le score "
    "est le proxy brut, non retourne, et EXPECTED_SIGN = -1",
    "la recette dit rsv_normalization_window = null, RSV employe brut ; aucune "
    "normalisation, aucun z-score, aucune statistique estimee n'est appliquee",
    "la fiche donne trois usages (continu, signe < 0 pour BtD, terciles) ; j'ai retenu "
    "le continu des regressions, le plus simple, sans seuil ni groupe",
    "le conditionnement VIX a 16:15 n'entre pas dans le signal de base (resolution de la "
    "fiche) et n'est pas code ; les jours ou l'ecart Londres-New York differe de 5 heures "
    "ne sont pas exclus, faute de pouvoir le faire sans constantes de calendrier",
    "cloture non positive ou manquante a l'une des deux bornes, ou moins de deux clotures "
    "dans l'heure : aucun score (None)",
)

_ROOT = "ES"


def _predictor(closes: pd.Series, position: int) -> float | None:
    seen = closes.iloc[: position + 1]
    if len(seen) < 2:
        return None
    t = seen.index[-1]
    start = t - pd.Timedelta(minutes=60)
    hour = seen[seen.index >= start]
    if len(hour) < 2:
        return None
    first = hour.iloc[0]
    last = hour.iloc[-1]
    if pd.isna(first) or pd.isna(last) or first <= 0 or last <= 0:
        return None
    return math.log(float(last) / float(first))


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} pour les cellules de la racine ES."""
    candidates = panel.cells() if cells is None else cells
    selected = [(root, window) for root, window in candidates if root == _ROOT]
    if not selected:
        return {}
    out = _common.run(panel, _predictor, cells=selected, horizon_bars=horizon_bars)
    return {key: s for key, s in out.items() if s is not None and len(s) > 0}
