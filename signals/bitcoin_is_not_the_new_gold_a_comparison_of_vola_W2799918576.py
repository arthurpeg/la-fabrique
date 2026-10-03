"""Klein, Thu & Walther (2018), Bitcoin is not the New Gold.

Ce papier ne construit AUCUN signal predictif (fiche : `signal_construction`
et `horizon` valent null). Il decrit des volatilites conditionnelles
(APARCH/FIAPARCH), des correlations BEKK contemporaines, et un test de
couverture ex post (poids de variance minimale et VaR calcules sur tout
l'echantillon : look-ahead par construction, intransposable tel quel).

Ce qui manquait, et ce qui a ete fait a la place :
- aucune formule de score, aucun horizon, aucun signe predictif : la seule
  brique calculable et causale de la recette est l'etape (1), le rendement
  log x100 (`return_scaling` = 100). Le module la transpose en rendement log
  x100 de la seance jusqu'a la barre notee, sur les racines que la recette
  nomme exactement (ES, GC, CL) ;
- horizon absent de la fiche : aucun nombre n'est ecrit ici, l'ancrage par
  defaut de `_common.run` est utilise quand l'appelant n'en fournit pas ;
- BEKK, poids de variance minimale, VaR plein echantillon, lissage de
  Savitzky-Golay : non codes (parametres non publies ou look-ahead) ;
- le signe attendu n'est pas donne par le papier : choix declare dans CHOICES.

Signal honnetement diminue : il ne code que la part transposable.
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
    "la fiche dit signal_construction = null (aucun signal predictif) ; j'ai code "
    "la seule brique causale de la recette, le rendement log x100 (formule etape 1, "
    "parametre return_scaling = 100), parce que tout le reste (BEKK, poids de "
    "variance minimale, VaR plein echantillon) est in-sample ou non publie",
    "la fiche donne des rendements journaliers clot-a-clot ; j'ai pris le rendement "
    "log x100 de la premiere cloture de la seance a la cloture de la barre notee, "
    "parce que _common.run ne fournit que les clotures d'une seance et que c'est "
    "l'equivalent intraday le plus simple, sans nombre nouveau",
    "horizon = null dans la fiche ; horizon_bars vaut None par defaut dans la "
    "signature (aucune constante absente de la fiche) : s'il est fourni il est "
    "transmis a _common.run, sinon _common.run applique son propre defaut",
    "EXPECTED_SIGN : le papier n'annonce aucun signe predictif ; j'ai choisi +1 "
    "(continuation du rendement de seance), par defaut et sans appui dans le papier, "
    "ce qui est une interpretation et non un resultat du papier",
    "univers : la recette nomme exact_roots ES, GC, CL ; je ne note que ces racines "
    "(intersection avec les cellules du panel et avec `cells` si fourni)",
    "sessions = null dans la recette (clot-a-clot couvre 24 h) ; je n'ai filtre "
    "aucune fenetre : toutes les fenetres des racines retenues sont notees",
    "barre notee en premiere position de seance, ou cloture non positive ou manquante : "
    "aucun score (None), plutot qu'un zero fabrique",
    "l'effet de levier inverse (or, argent, Bitcoin) et le regime de correlation "
    "or-actions en detresse ne sont pas codes : ils portent sur la volatilite ou "
    "sur une correlation contemporaine, pas sur un rendement futur, et le regime "
    "releve d'un hybride, hors du perimetre d'un signal simple",
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


def scores(panel, cells=None, horizon_bars=None):
    """Rend {(root, window): pd.Series}."""
    available = list(cells) if cells is not None else list(panel.cells())
    selected = [cell for cell in available if cell[0] in _ROOTS]
    if not selected:
        return {}
    if horizon_bars is None:
        return _common.run(panel, _predictor, cells=selected)
    return _common.run(panel, _predictor, cells=selected, horizon_bars=horizon_bars)
