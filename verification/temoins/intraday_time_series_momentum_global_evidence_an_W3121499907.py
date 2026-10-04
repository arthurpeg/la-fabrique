"""Intraday time series momentum (Li, Sakkas, Urquhart) -- signal temoin.

Le score est rF_t, le rendement de la premiere demi-heure de la seance, rapporte
a la cloture de la seance precedente (gap overnight inclus) :

    rF_t = pfirst30,t / pclose,t-1 - 1

Le papier prend la position sur la derniere demi-heure selon le SIGNE de rF_t
(longue si rF_t > 0, courte sinon). Le score rendu est rF_t brut (recette :
« score = rF_t ») ; le signe est porte par le score, la cible est rL_t.

Lecture causale : le predicteur ne lit que les clotures de la seance jusqu'a la
position de la barre notee. La cloture de la veille vient de la seance
precedente, deja entierement passee.

Ce qui ne se transpose pas, ou manque :
- le papier traite 16 indices au comptant en dollars US ; ici des futures
  intraday en OHLCV, dans la devise de la cellule, sans conversion ;
- le papier ne donne pas la regle exacte du « dernier prix des 30 premieres
  minutes » ; on prend la cloture de la derniere barre ouverte dans les 30
  premieres minutes ;
- toute la moitie internationale (portefeuilles globaux, TVC, ACP), la
  regression predictive, les tris de liquidite et d'information discreteness
  ne sont pas codes : ils ne sont pas des scores par instrument et par barre ;
- aucun cout de transaction (le papier n'en donne pas).
"""

from __future__ import annotations

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
    "la fiche dit que rF_t est le rendement des 30 premieres minutes rapporte a "
    "la cloture de la veille ; j'ai code score = rF_t brut (sans normalisation "
    "par la volatilite, la recette n'en applique aucune), avec la cloture de la "
    "derniere barre de la seance precedente comme denominateur, parce que le "
    "papier inclut explicitement le gap overnight",
    "la fiche donne interval_minutes = 30 ; j'ai pris comme « dernier prix des "
    "30 premieres minutes » la cloture de la derniere barre dont l'horodatage "
    "d'ouverture est strictement a moins de 30 minutes de l'ouverture de la "
    "premiere barre de la seance, car une barre est horodatee a son ouverture",
    "la fiche ne dit pas ce qui se passe si la barre notee tombe avant la fin des "
    "30 premieres minutes ; je ne rends alors aucun score (None), plutot que de "
    "lire une fenetre tronquee",
    "la fiche donne la regle de signe (long si rF_t > 0, court si rF_t <= 0) "
    "comme regle de position ; le score rendu est rF_t lui-meme, dont le signe "
    "porte cette regle, et EXPECTED_SIGN = +1 car rF_t predit positivement rL_t",
    "la fiche utilise la premiere observation du jour comme ouverture ; j'ai pris "
    "la premiere barre de la seance de la cellule comme ouverture, et la derniere "
    "barre de la seance precedente (recollee, via _common.cell_bars) comme "
    "cloture de la veille ; premiere seance de l'historique sans veille : omise",
    "la fiche travaille en dollars US sur indices au comptant ; la conversion de "
    "devise n'est pas faite, les clotures recollees de la cellule sont utilisees "
    "telles quelles",
    "la pause dejeuner et l'heterogeneite des horaires ne sont pas traitees (le "
    "papier ne dit pas comment) : les 30 minutes sont comptees sur l'horloge des "
    "horodatages des barres",
    "l'ancrage du score est celui de _common.run, avec horizon_bars transmis tel "
    "que recu, sans valeur par defaut",
)

INTERVAL_MINUTES = 30


def _previous_closes(panel, root, window):
    """Pour chaque seance, cle = horodatage de sa premiere barre, valeur =
    derniere cloture de la seance precedente (seances deja terminees)."""
    closes, sessions = _common.cell_bars(panel, root, window)
    out = {}
    current = None
    current_first = None
    last_close_of_prev = None
    last_close = None
    for ts, close, sess in zip(closes.index, closes.to_numpy(), sessions.to_numpy()):
        if current is None or sess != current:
            if current is not None:
                last_close_of_prev = last_close
            current = sess
            current_first = ts
            out[current_first] = last_close_of_prev
        last_close = close
    return out


def _make_predictor(prev_by_open):
    span = pd.Timedelta(minutes=INTERVAL_MINUTES)

    def predictor(closes, position):
        sub = closes.iloc[: position + 1]
        if len(sub) == 0:
            return None
        start = sub.index[0]
        inside = (sub.index - start) < span
        if inside.all():
            return None
        first30 = sub[inside].iloc[-1]
        prev = prev_by_open.get(start)
        if prev is None or pd.isna(prev) or prev == 0:
            return None
        return float(first30 / prev - 1)

    return predictor


def scores(panel, cells=None, *, horizon_bars: int):
    """Rend {(root, window): pd.Series}."""
    if cells is None:
        cells = list(panel.cells())
    out = {}
    for cell in cells:
        root, window = cell
        prev_by_open = _previous_closes(panel, root, window)
        predictor = _make_predictor(prev_by_open)
        res = _common.run(panel, predictor, cells=[cell], horizon_bars=horizon_bars)
        for key, series in res.items():
            if series is not None and len(series) > 0:
                out[key] = series
    return out
