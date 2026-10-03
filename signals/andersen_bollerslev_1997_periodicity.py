"""Andersen & Bollerslev (1997) -- periodicite intra-journaliere de la volatilite.

Ce papier ne propose AUCUN signal (signal_construction = null, horizon = null).
Il mesure une grandeur descriptive : la moyenne, par intervalle intraday n, de
|R_t,n|, le rendement logarithmique absolu de 5 minutes du future S&P 500, et
montre la persistance de |R| (autocorrelation d'ordre un 0,309 sur le change).

Part transposable codee ici, et declaree comme diminuee : le score d'une
seance est |R_t,n|, la valeur absolue du rendement logarithmique sur
`bar_minutes` = 5 minutes qui se termine a la barre notee (ancree par
`_common.run`, sur l'horloge de la fenetre). C'est la grandeur meme sur
laquelle porte le motif en U et le correlogramme du papier.

Ce qui ne se transpose pas, et n'est pas code :
- le papier decrit (et predit, au mieux) une VARIANCE, pas un rendement signe ;
  le score ci-dessous dit l'amplitude, pas la direction ;
- le modele periodique de la section 5 / annexe B (forme de Fourier flexible,
  J = 1, P = 2, indicatrices 78/79/80) est estime en une passe sur tout
  l'echantillon et normalise sur tout l'echantillon : look-ahead par
  construction, donc non code ;
- sigma_t (MA(1)-GARCH(1,1) journalier) : date de disponibilite et fenetre
  d'estimation non donnees par le papier, donc non code.

Horizon : la fiche n'en donne aucun (horizon.value = null). Le module n'ecrit
donc aucune valeur d'horizon ; si l'appelant n'en passe pas, c'est le defaut
de `_common.run` qui s'applique.
"""

from __future__ import annotations

import numpy as np

from signals import _common

SIGNAL_ID = "andersen-bollerslev-1997-periodicity"
HYPOTHESIS = None
PAPER = (
    "Torben G. Andersen, Tim Bollerslev (1997), Intraday periodicity and "
    "volatility persistence in financial markets, Journal of Empirical "
    "Finance 4(2-3):115-158"
)
EXPECTED_SIGN = +1

CHOICES = (
    "La fiche ne propose aucun signal (signal_construction et horizon a null) ; "
    "j'ai code la seule grandeur que la recette mesure, |R_t,n|, le rendement "
    "logarithmique absolu de 5 minutes, parce que c'est la part transposable "
    "(formula.statement et inputs absolute_five_minute_return).",
    "La recette donne bar_minutes = 5 ; nos barres sont a 1 minute (fiche, "
    "transposability) : j'ai pris R comme log(close[t]) - log(close[t-5]), "
    "les 5 barres de 1 minute qui se terminent a la barre notee, sans rien "
    "lire apres elle.",
    "Valeur absolue plutot que carre : la recette cite le papier, qui trouve la "
    "dependance plus marquee sur les rendements absolus.",
    "EXPECTED_SIGN = +1 : la fiche porte claim.direction = positive, et le "
    "papier montre une forte persistance positive de |R| (rho = 0,309) ; un "
    "|R| eleve annonce donc une amplitude future elevee. Le papier ne dit rien "
    "de la direction du rendement : si le harnais mesure contre un rendement "
    "signe, ce signal n'a pas d'equivalent dans le papier, et je le declare.",
    "Pas de purge par la composante periodique s_t,n : le papier l'estime en "
    "une passe sur tout l'echantillon (look-ahead). A une position d'horloge "
    "fixe dans la seance (ce que fait _common.run), s_n est le meme chaque jour "
    "et diviser par lui ne changerait pas l'ordre des scores d'une cellule.",
    "Pas de sigma_t (GARCH journalier) : ni sa date de disponibilite ni sa "
    "fenetre d'estimation ne sont donnees (ambiguite resolution = null).",
    "Horizon : la fiche n'en donne aucun (horizon.value = null) ; le defaut "
    "de horizon_bars dans la signature est None et non un nombre ecrit ici. "
    "Si l'appelant passe un horizon, il est transmis tel quel a _common.run ; "
    "sinon _common.run applique son propre defaut. Ainsi aucune constante "
    "d'horizon absente de la fiche n'est ecrite dans ce module.",
    "Ancrage : celui de _common.run, une barre par seance a la distance horaire "
    "de la cloture de fenetre ; la recette ne donne pas de rang d'intervalle "
    "(u_shape_interval_positions = null).",
    "Cellules : toutes celles que le panel retient via _common.run (cells=None "
    "par defaut) ; la recette vise ES x US, mais restreindre l'univers n'est "
    "pas demande par le contrat et je n'ai pas filtre.",
    "Moins de 5 barres disponibles dans la seance avant la barre notee, ou "
    "cloture non positive ou manquante : aucun score (None).",
    "Pas de suppression explicite du premier rendement de la seance ni des "
    "rendements overnight : les clotures fournies sont celles d'une seule "
    "seance, donc R ne traverse jamais la nuit.",
)

_BAR_MINUTES = 5


def _predictor(closes, position: int):
    if position < _BAR_MINUTES:
        return None
    p_now = float(closes.iloc[position])
    p_then = float(closes.iloc[position - _BAR_MINUTES])
    if not (np.isfinite(p_now) and np.isfinite(p_then)):
        return None
    if p_now <= 0 or p_then <= 0:
        return None
    return float(abs(np.log(p_now) - np.log(p_then)))


def scores(panel, cells=None, horizon_bars: int | None = None):
    """Rend {(root, window): pd.Series} : |R| de 5 minutes a la barre ancree."""
    if horizon_bars is None:
        return _common.run(panel, _predictor, cells=cells)
    return _common.run(panel, _predictor, cells=cells, horizon_bars=horizon_bars)
