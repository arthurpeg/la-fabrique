"""Shen, Urquhart, Wang (2022) : momentum intraday du bitcoin, part transposable.

Transposition declaree :
- Le predicteur principal r_ONFH exige la cloture du jour t-1 a 17:00 et le prix
  a ouverture+30 min du jour t : il traverse deux seances. Un predicteur de
  `_common.run` ne recoit que les clotures d'UNE seance : r_ONFH n'est pas code.
- Les terciles de volume/volatilite, la regression poolee, le R2 hors echantillon
  et l'allocation moyenne-variance ne se transposent pas (pas de volume en
  entree du predicteur, pas d'IC dans le papier) : non codes.
- Est code le predicteur secondaire r_SLH = p(cloture-30) / p(cloture-60) - 1,
  evalue a la barre d'ancrage de `_common.run` (au plus `horizon_bars` minutes
  avant la cloture declaree), soit le debut de la derniere demi-heure.
  Le prix a cloture-60 est la cloture de la barre situee `horizon_bars` barres
  avant la barre notee. Le score est r_SLH brut ; le papier lui donne un effet
  negatif (anti-persistance), d'ou EXPECTED_SIGN = -1.
"""

from __future__ import annotations

from signals import _common

SIGNAL_ID = "bitcoin-intraday-time-series-momentum-W3199228172"
HYPOTHESIS = None
PAPER = (
    "Shen, Urquhart, Wang (2022), Bitcoin intraday time-series momentum, "
    "Financial Review"
)
EXPECTED_SIGN = -1
CHOICES = (
    "la fiche laisse le choix entre r_ONFH, r_SLH et leur combinaison ; j'ai "
    "retenu r_SLH, parce que r_ONFH demande la cloture de la veille (hors de la "
    "seance unique que recoit le predicteur) et que r_SLH est calculable "
    "causalement dans la seance.",
    "le papier donne un beta_SLH negatif (anti-persistance) ; le score est r_SLH "
    "brut et EXPECTED_SIGN vaut -1 (long si r_SLH < 0, short sinon).",
    "r_SLH = p(cloture-30)/p(cloture-60) - 1 : j'ai pris la barre notee comme "
    "p(cloture-30) (ancrage de _common.run, distance a la cloture au plus "
    "horizon_bars) et la barre horizon_bars barres plus tot comme p(cloture-60), "
    "en supposant des barres d'une minute (bar_size = 1) ; aucun nombre nouveau.",
    "prix = cloture de la barre d'une minute (le papier ne precise pas : dernier "
    "prix, VWAP) ; minute sans transaction : barre recollee telle que fournie.",
    "heure d'ete, week-ends, heures d'ouverture par plateforme, detection du "
    "pic de volume : sans objet pour r_SLH ; l'horloge de la fenetre ancre le "
    "score, je ne code aucune heure en dur.",
    "terciles de volume/volatilite, regression poolee, R2 hors echantillon, "
    "allocation gamma = 5 : non codes (non transposables ou non causaux).",
)


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} de r_SLH a la barre d'ancrage."""

    def predictor(closes, position):
        if position < horizon_bars:
            return None
        now = closes.iloc[position]
        before = closes.iloc[position - horizon_bars]
        if not (before > 0) or not (now == now):
            return None
        return float(now / before - 1)

    return _common.run(panel, predictor, cells=cells, horizon_bars=horizon_bars)
