"""Klein, Thu & Walther (2018), "Bitcoin is not the New Gold".

Ce que le papier donne : AUCUN signal prédictif. La fiche le dit
(`signal_construction` = null, `horizon` = null) : tout y est contemporain ou
ex post (paramètres APARCH/FIAPARCH, corrélations BEKK lissées par un filtre
bilatéral, seuils de VaR et poids de variance minimale calculés sur
l'échantillon entier).

Ce qui ne se transpose pas : BEKK (paramètres non publiés, fenêtre
d'estimation non dite), lissage de Savitzky-Golay (bilatéral, fenêtre non
donnée), VaR plein échantillon (look-ahead par construction), portefeuille de
variance minimale ex post, Bitcoin / argent / MSCI (absents de l'univers).

Part transposée, déclarée diminuée : la seule grandeur de base du papier, le
rendement logarithmique ×100, r = 100 × log(P_t / P_{t-1}), appliqué aux
seuls sous-jacents que le papier mesure et que l'univers couvre (ES, GC, CL),
calculé de la première clôture de la séance à la barre notée. Le papier
n'utilisant que des clôtures journalières sans heure ni fenêtre, aucune
séance n'est privilégiée.

Paramètres manquants : horizon (null) -> celui du harnais ; séance (null) ->
toutes les fenêtres ; signe (aucune prévision dans le papier) -> +1 par
convention, voir CHOICES.
"""

from __future__ import annotations

import math

from signals import _common

SIGNAL_ID = "bitcoin-is-not-the-new-gold-a-comparison-of-vola-W2799918576"
HYPOTHESIS = None
PAPER = (
    "Klein, T., Thu, H. P., & Walther, T. (2018), Bitcoin is not the New Gold - "
    "A comparison of volatility, correlation, and portfolio performance, "
    "International Review of Financial Analysis, 59, 105-116"
)
EXPECTED_SIGN = +1
CHOICES = (
    "la fiche dit que le papier ne construit aucun signal (signal_construction = null) ; "
    "j'ai codé la seule grandeur de base qu'il calcule, le rendement log ×100 "
    "r = 100 × log(P_t/P_{t-1}), parce que c'est la seule part transposable sans "
    "estimation plein échantillon ni paramètre inventé",
    "la fiche travaille en clôtures journalières de clôture à clôture ; j'ai pris le "
    "rendement de la première clôture de la séance à la clôture de la barre notée, parce "
    "que le prédicteur de _common.run ne reçoit que les clôtures d'une séance",
    "la fiche donne exact_roots = ES, GC, CL ; je ne note que ces racines, parce que "
    "Bitcoin, argent, MSCI World, MSCI EM50 et CRIX n'ont aucun équivalent dans l'univers",
    "la fiche donne sessions = null ; je note toutes les fenêtres présentes pour ces "
    "racines, sans en privilégier aucune, faute d'heure de clôture dans le papier",
    "la fiche donne horizon = null ; j'ai gardé horizon_bars du harnais et l'ancrage "
    "d'horloge de _common.run, sans nombre nouveau",
    "le papier ne prétend à aucune prévision, donc aucun signe ; j'ai pris EXPECTED_SIGN = +1, "
    "le signe de la grandeur elle-même (un rendement bas = la détresse du papier, "
    "r_t < VaR_q), choix conventionnel et non une affirmation du papier",
    "le seuil de détresse VaR_q (1 %, 5 %, 10 %) n'est pas codé : calculé sur "
    "l'échantillon entier dans le papier, il serait du look-ahead, et sa version "
    "glissante demanderait une fenêtre que le papier ne donne pas",
    "BEKK, lissage de Savitzky-Golay, APARCH/FIAPARCH et poids de variance minimale ne "
    "sont pas codés : paramètres non publiés, fenêtres absentes (null dans la recette), "
    "ou estimation ex post",
    "une barre à la position 0, ou une clôture non positive ou manquante, ne produit "
    "aucun score (None) plutôt qu'une valeur remplie",
)

_ROOTS = ("ES", "GC", "CL")
_RETURN_SCALING = 100


def _predictor(closes, position: int):
    if position < 1:
        return None
    first = closes.iloc[0]
    last = closes.iloc[position]
    if first is None or last is None:
        return None
    first = float(first)
    last = float(last)
    if not (math.isfinite(first) and math.isfinite(last)):
        return None
    if first <= 0 or last <= 0:
        return None
    return _RETURN_SCALING * math.log(last / first)


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series}."""
    available = list(panel.cells())
    if cells is None:
        cells = available
    retained = [c for c in cells if c in available and c[0] in _ROOTS]
    if not retained:
        return {}
    result = _common.run(panel, _predictor, cells=retained, horizon_bars=horizon_bars)
    return {k: v for k, v in result.items() if v is not None and len(v) > 0}
