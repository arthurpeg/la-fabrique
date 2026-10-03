"""Boyarchenko, Larsen, Whelan - The Overnight Drift : RSV_close.

Part transposee : le desequilibre d'ordres relatif de la derniere heure
15:15-16:15 ET, RSV = (achats - ventes) / (achats + ventes), borne dans [-1, 1].
Le score est le RSV brut ; le papier le dit NEGATIVEMENT lie au rendement
suivant (EXPECTED_SIGN = -1).

Ce qui ne se transpose pas :
- Les trades classes acheteur/vendeur (quotes au sommet du carnet) n'existent
  pas dans un panel OHLCV, et le predicteur ne recoit que des clotures.
  Substitut declare : la variation de cloture d'une barre est prise comme
  volume signe de cette barre (positive = achats, negative = ventes), de sorte
  que RSV = somme des variations / somme des variations en valeur absolue.
  Ce n'est pas le signal du papier.
- La cible (rendement 02:00-03:00 ET du lendemain), le VIX, la strategie BtD
  (RSV < 0), l'asymetrie : non codes, le score est le RSV lui-meme.
- Seules les cellules dont la seance contient 15:15-16:15 ET produisent un
  score ; les autres s'omettent.
Manquait : aucun parametre de normalisation (le papier n'en applique pas).
"""

from __future__ import annotations

import pandas as pd

from signals import _common

SIGNAL_ID = "boyarchenko-2023-overnight-drift"
HYPOTHESIS = None
PAPER = "Boyarchenko, Larsen, Whelan (2022), The Overnight Drift, FRBNY Staff Reports no. 917"
EXPECTED_SIGN = -1

CHOICES = (
    "la fiche dit RSV sur trades classes par le sommet du carnet ; j'ai compris RSV = (achats - ventes)/(achats + ventes) ou la variation de cloture de chaque barre tient lieu de volume signe (hausse = achats, baisse = ventes), parce que le panel n'a que des clotures et que le simple comptage de barres donnait trop peu de valeurs distinctes (S4).",
    "RSV = somme des variations de cloture / somme de leurs valeurs absolues sur la fenetre : borne dans [-1, 1] comme dans le papier ; pas de volume en contrats disponible.",
    "la fenetre 15:15-16:15 ET est fixe (15.25 et 16.25 heures, converties en minutes entieres), heure de New York avec heure d'ete ; barre horodatee a l'ouverture, incluse si son ouverture est dans [15:15, 16:15[.",
    "le papier dit RSV negativement lie au rendement : le score est le RSV brut et EXPECTED_SIGN = -1, plutot que d'inverser le score.",
    "le score est calcule a la barre d'ancrage de _common.run, avec les seules barres de la seance jusqu'a cette position ; une cellule dont la seance ne couvre pas la fenetre n'a pas de score (None).",
    "aucune normalisation temporelle, aucun conditionnement VIX ni RSV < 0, aucun traitement de jours feries ou de roulement : la fiche n'en donne pas.",
    "la cible 02:00-03:00 ET / 01:30-03:30 n'est pas utilisee dans le score : elle est la cible du rendement, pas une entree.",
    "la premiere barre de la seance n'a pas de variation et n'est pas comptee ; la difference est prise entre clotures consecutives de la seance.",
)

_START = round(15.25 * 60)
_END = round(16.25 * 60)


def _predictor(closes: pd.Series, position: int):
    sub = closes.iloc[: position + 1]
    if len(sub) < 2:
        return None
    local = sub.index.tz_convert("America/New_York")
    minutes = local.hour * 60 + local.minute
    diff = sub.diff()
    in_win = (minutes >= _START) & (minutes < _END)
    d = diff[in_win].dropna()
    total = float(d.abs().sum())
    if total == 0:
        return None
    return float(d.sum()) / total


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series}."""
    return _common.run(panel, _predictor, cells=cells, horizon_bars=horizon_bars)
