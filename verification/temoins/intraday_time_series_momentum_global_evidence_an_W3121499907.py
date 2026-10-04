"""Intraday time series momentum (Li, Sakkas, Urquhart) : rendement de la
premiere demi-heure, gap overnight inclus, comme predicteur de la derniere
demi-heure de la meme seance.

Score = rF_t = pfirst30,t / pclose,t-1 - 1 (le "score brut" de la recette),
pose a l'ancre de `_common.run` (une barre par seance et par cellule).

Ce qui ne se transpose pas, et ce qui manquait :
- les 16 indices au comptant, la conversion en dollars, les 18 portefeuilles
  globaux, le facteur TVC, l'ACP, les tris par liquidite (Corwin-Schultz) et
  par information discreteness ne sont pas codes : ce sont des regimes ou des
  constructions multi-marches, pas le signal de base ;
- le filtre de prix extremes (1.2 / 0.8 du plus haut / plus bas prix
  journalier de l'echantillon) exige une statistique sur la serie entiere :
  il lirait l'avenir, il n'est pas applique ;
- la cible rL_t (derniere demi-heure) est ce que le harnais mesure ; elle
  n'est pas calculee ici ;
- le papier ne dit pas quel champ (open/high/low/last) sert de prix par
  minute, ni comment traiter les encheres : on prend la cloture de barre.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "intraday-time-series-momentum-global-evidence-an-W3121499907"
HYPOTHESIS = None
PAPER = (
    "Li, Sakkas, Urquhart (2022), Intraday time series momentum: global "
    "evidence and links to market characteristics, Journal of Financial Markets"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche donne le score brut rF_t (continu) et une regle de signe "
    "(long si rF_t > 0, court sinon) ; j'ai pose le score continu rF_t, pas "
    "le signe, parce que la recette l'appelle 'le score brut' et que la "
    "regression predictive du papier est faite sur rF_t ; le signe se lit "
    "dans le score (un rF_t exactement nul donne un score nul, la ou la "
    "regle de trading le rangerait cote court)",
    "EXPECTED_SIGN = +1 : le papier annonce que la premiere demi-heure "
    "predit positivement la derniere (pente positive, long si le matin monte)",
    "la longueur de la premiere demi-heure est 30 minutes (interval_minutes "
    "de la recette) ; les barres comptees sont celles dont l'ouverture est "
    "a moins de 30 minutes entieres de la premiere barre de la seance, et le "
    "'dernier prix' est la cloture de la derniere de ces barres",
    "l'ouverture de la seance est l'horodatage de la premiere barre de la "
    "seance, conformement au papier (premiere observation du jour) ; les "
    "ecarts d'horloge sont compares en minutes entieres",
    "le dénominateur est la derniere cloture de la seance precedente de la "
    "meme cellule (cloture recollee de cell_bars), pour inclure le gap "
    "overnight comme le dit le papier ; une seance sans seance precedente "
    "dans les donnees n'a pas de score ; 'seance precedente' est la seance "
    "voisine dans la serie de la cellule, sans calendrier de jours feries",
    "sur des futures presque continus, le gap overnight n'a pas le sens du "
    "papier (indices qui ferment) ; je garde la definition du papier "
    "appliquee a la seance de la cellule, sans la corriger",
    "si la premiere demi-heure n'est pas entierement ecoulee a la barre "
    "notee (aucune barre visible au-dela de 30 minutes apres l'ouverture), "
    "le prédicteur ne rend rien plutot que d'utiliser une fenetre partielle",
    "le filtre de prix extremes du papier (1.2 et 0.8 du plus haut et plus "
    "bas prix journalier de l'echantillon) n'est pas applique : il demande "
    "une statistique sur la serie entiere, donc l'avenir",
    "les prix sont ceux du panel (pas de conversion en dollars, pas de "
    "devise locale a traiter) ; aucun cout, aucune taille de position, aucune "
    "normalisation par la volatilite (parametres null dans la recette)",
    "horizon_bars est transmis tel quel a _common.run, qui fixe l'ancre "
    "(une barre par seance et par cellule) ; les regimes (liquidite, "
    "information discreteness, crise) et le signal croise US ne sont pas "
    "codes",
)


def _previous_closes(closes: pd.Series, sessions: pd.Series) -> dict:
    """Pour chaque seance, l'horodatage de sa premiere barre -> derniere
    cloture de la seance precedente (passe seulement)."""
    ids = sessions.ne(sessions.shift(1)).cumsum()
    firsts = closes.index.to_series().groupby(ids.values, sort=True).first()
    lasts = closes.groupby(ids.values, sort=True).last()
    out = {}
    previous = None
    for key in firsts.index:
        if previous is not None:
            out[firsts.loc[key]] = previous
        previous = lasts.loc[key]
    return out


def scores(panel, cells=None, *, horizon_bars: int):
    """Rend {(root, window): pd.Series}."""
    targets = list(panel.cells()) if cells is None else list(cells)
    result = {}
    for cell in targets:
        root, window = cell
        closes, sessions = _common.cell_bars(panel, root, window)
        if len(closes) == 0:
            continue
        previous = _previous_closes(closes, sessions)
        window_len = pd.Timedelta(minutes=30)
        minute = pd.Timedelta(minutes=1)

        def predictor(session_closes, position, previous=previous):
            if len(session_closes) == 0 or position < 0:
                return None
            opening = session_closes.index[0]
            prev = previous.get(opening)
            if prev is None or not math.isfinite(prev) or prev == 0:
                return None
            visible = session_closes.iloc[: position + 1]
            elapsed = (visible.index - opening) // minute
            inside = np.asarray(elapsed < window_len // minute)
            if inside.all():
                return None
            last_price = visible.iloc[int(inside.sum()) - 1]
            if not math.isfinite(last_price):
                return None
            return float(last_price / prev - 1)

        produced = _common.run(
            panel, predictor, cells=[cell], horizon_bars=horizon_bars
        )
        for key, series in produced.items():
            if series is not None and len(series) > 0:
                result[key] = series
    return result
