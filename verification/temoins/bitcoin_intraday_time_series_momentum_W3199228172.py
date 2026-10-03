"""Shen, Urquhart, Wang (2022) : momentum intraday du Bitcoin.

Part transposee : le predicteur secondaire r_SLH, anti-persistance de
l'avant-dernier demi-heure vers la derniere : r_SLH = p(cloture-30) /
p(cloture-60) - 1. Le papier est long si r_SLH < 0, short sinon : le score est
donc -r_SLH, et le signe attendu vers le rendement de la fin de fenetre est +1.

Part NON transposee : le predicteur principal r_ONFH (de la cloture 17:00 de la
veille a ouverture + 30 min). Il est connu en debut de seance alors que
`_common.run` pose le score a la fin de fenetre, et le predicteur ne recoit que
les clotures de la seance courante, pas celle de la veille ; l'heure d'ouverture
au pic de volume (Table 1) est propre a des plateformes crypto. Je ne le code
pas, plutot que de pretendre. La version combinee en depend aussi : omise.
Egalement non transposes : regression poolee, R2 OOS, terciles de volume ou de
volatilite, ecart de Corwin-Schultz, allocation moyenne-variance.
"""

from __future__ import annotations

import numpy as np

from signals import _common

SIGNAL_ID = "bitcoin-intraday-time-series-momentum-W3199228172"
HYPOTHESIS = None
PAPER = "Shen, Urquhart, Wang (2022), Bitcoin intraday time-series momentum, Financial Review"
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche donne deux predicteurs (r_ONFH, r_SLH) ; j'ai code seulement r_SLH, car r_ONFH exige la cloture de la veille et un score en debut de seance, ce que le predicteur de _common.run (clotures de la seance courante, ancrage en fin de fenetre) ne permet pas",
    "la fiche dit long si r_SLH < 0, short sinon ; j'ai compris score = -r_SLH, donc EXPECTED_SIGN = +1 (le score predit positivement le rendement de la fin de fenetre)",
    "la fiche dit r_SLH = p(cloture-30)/p(cloture-60) - 1 ; j'ai compris, sur des barres d'une minute, le rapport entre la cloture de la barre notee et celle 30 barres plus tot, la barre notee etant a au plus horizon_bars de la cloture de fenetre ; 30 vient de first_half_hour_minutes",
    "la barre notee est celle choisie par _common.run (premiere a distance de la cloture <= horizon_bars), faute d'heure de cloture EST applicable aux fenetres du panel ; l'heure d'ete et le pic de volume ne sont pas traites",
    "prix manquant ou non positif ou position < 30 : aucun score (None), sans remplissage",
    "l'hypothese que les barres sont d'une minute est mienne : le papier agrege en barres d'une minute",
)

_BARS = 30


def _predictor(closes, position):
    if position < _BARS:
        return None
    now = closes.iloc[position]
    before = closes.iloc[position - _BARS]
    if not (np.isfinite(now) and np.isfinite(before)) or before <= 0:
        return None
    return -(float(now) / float(before) - 1)


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series}."""
    return _common.run(panel, _predictor, cells=cells, horizon_bars=horizon_bars)
