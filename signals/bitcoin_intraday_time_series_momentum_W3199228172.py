"""Shen, Urquhart & Wang (2022), Bitcoin intraday time-series momentum.

Predicteur principal du papier, transpose a nos cellules (root, window) :

    r_ONFH,t = p(ouverture + 30 min, t) / p(cloture, t-1) - 1

ou la "cloture de la veille" est la derniere cloture de la seance precedente
de la meme cellule, et "l'ouverture" est la premiere barre de la seance
courante. Le score est pose par `_common.run` a la premiere barre dont la
distance a la cloture declaree de la fenetre est au plus `horizon_bars`
(30 par defaut : le debut de la derniere demi-heure, comme la position du
papier ouverte a 16:30 et fermee a 17:00). Signe attendu positif : long sur
la derniere demi-heure si r_ONFH > 0, short sinon.

Ce qui manquait et ce qui a ete fait a la place :
- la regle de "pic de volume" fixant l'ouverture n'est pas chiffree (null) :
  l'ouverture est la premiere barre de la seance de la cellule ;
- la cloture 17:00 EST est propre au bitcoin (pause CME) : elle est remplacee
  par la cloture declaree de chaque fenetre, via l'ancrage de `_common.run` ;
- le traitement des week-ends n'est pas dit : t-1 est la seance precedente
  disponible de la cellule ;
- le prix a un instant n'est pas precise : cloture de la barre d'une minute ;
- le predicteur secondaire r_SLH, la combinaison, les terciles de volume et
  de volatilite et la variante moyenne-variance ne sont pas codes ici.
"""

from __future__ import annotations

import math

import pandas as pd

from signals import _common

SIGNAL_ID = "bitcoin-intraday-time-series-momentum-W3199228172"
HYPOTHESIS = None
PAPER = (
    "Shen, D., Urquhart, A., Wang, P. (2022), Bitcoin intraday time-series "
    "momentum, Financial Review 57(2), 319-344"
)
EXPECTED_SIGN = +1
CHOICES = (
    "la recette laisse ouvert le choix entre r_ONFH, r_SLH et leur combinaison "
    "(resolution null) ; j'ai code r_ONFH seul, parce que le resume et la fiche "
    "le presentent comme le predicteur principal, avec le signe positif que la "
    "recette lui donne ; r_SLH et la combinaison ne sont pas codes",
    "r_ONFH inclut la nuit (resolution de la recette) : le point de depart est "
    "la derniere cloture disponible strictement avant la premiere barre de la "
    "seance courante, dans les clotures recollees de la meme cellule "
    "(_common.cell_bars) ; c'est la cloture de la seance precedente, donc "
    "deja passee au moment du score",
    "la cloture 17:00 EST du papier (pause CME du bitcoin) ne se transpose pas : "
    "la cloture de reference est celle de la fenetre de la cellule, et le score "
    "est pose par _common.run a horizon_bars de cette cloture, soit le debut de "
    "la derniere demi-heure quand horizon_bars vaut 30",
    "la regle de detection du pic de volume (ouverture) est null : l'ouverture "
    "est la premiere barre de la seance de la cellule, sans estimation de profil "
    "de volume (qui serait d'ailleurs ex post dans le papier)",
    "fin de r_ONFH : ouverture+30 min (equation 1) plutot qu'au pic de volume "
    "(conclusion), ambiguite non resolue ; j'ai suivi l'equation 1",
    "prix a ouverture+30 min : cloture de la barre d'indice "
    "first_window_minutes / bar_size - 1 (barres d'une minute, horodatees a "
    "leur ouverture : la 30e barre se clot a ouverture+30 min) ; je suppose des "
    "barres d'une minute comme la recette, sans le verifier sur le panel",
    "si la barre ouverture+30 min est posterieure a la barre notee, ou s'il n'y "
    "a pas de seance precedente, ou si un prix manque ou n'est pas positif, "
    "aucun score n'est ecrit (None)",
    "week-ends et jours feries non traites par le papier : t-1 est simplement "
    "la seance precedente disponible de la cellule, quel que soit l'ecart",
    "heure d'ete non precisee par le papier : sans objet ici, l'ancrage se fait "
    "sur l'horloge de la fenetre via _common.run",
    "score = r_ONFH brut, sans normalisation ni seuil : le papier trade sur le "
    "signe et la regression lineaire utilise le rendement brut",
    "conditionnement par terciles de volume / volatilite non code : formes par "
    "annee ou sur tout l'echantillon dans le papier, donc non point-in-time",
)

FIRST_WINDOW_MINUTES = 30
BAR_SIZE_MINUTES = 1
_OPEN_PLUS_WINDOW_INDEX = FIRST_WINDOW_MINUTES // BAR_SIZE_MINUTES - 1


def _make_predictor(all_closes: pd.Series):
    """Predicteur r_ONFH pour une cellule dont on connait les clotures."""

    index = all_closes.index

    def predictor(closes: pd.Series, position: int):
        if position < _OPEN_PLUS_WINDOW_INDEX:
            return None
        if len(closes) <= _OPEN_PLUS_WINDOW_INDEX:
            return None
        if not isinstance(closes.index, pd.DatetimeIndex):
            return None
        session_start = closes.index[0]
        i = index.searchsorted(session_start, side="left")
        if i == 0:
            return None
        prev_close = float(all_closes.iloc[i - 1])
        p_open_window = float(closes.iloc[_OPEN_PLUS_WINDOW_INDEX])
        if math.isnan(prev_close) or math.isnan(p_open_window):
            return None
        if prev_close <= 0:
            return None
        return p_open_window / prev_close - 1

    return predictor


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} du score r_ONFH."""
    selected = list(panel.cells()) if cells is None else list(cells)
    out = {}
    for root, window in selected:
        all_closes, _sessions = _common.cell_bars(panel, root, window)
        if all_closes is None or len(all_closes) == 0:
            continue
        predictor = _make_predictor(all_closes)
        result = _common.run(
            panel, predictor, cells=[(root, window)], horizon_bars=horizon_bars
        )
        for key, series in result.items():
            if series is not None and len(series) > 0:
                out[key] = series
    return out
