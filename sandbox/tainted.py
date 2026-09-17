"""Three signals that cheat on purpose. They exist so the test has something to catch.

A test that has never caught anything is not a test -- it is a habit. These three
are the deliberate look-aheads the gate injects, and the gate fails if any of them
survives `causality.check`.

They are in `sandbox/`, not in `signals/`, and they have no hypothesis and no
paper. Nothing may ever measure them.

  forward-return     reads the very return it is supposed to predict. The crudest
                     cheat, and the one a careless `shift(-h)` produces.
  full-sample-zscore honest predictor, then normalised by the mean and the
                     deviation of the WHOLE cell -- future included. Contains no
                     forward shift at all, which is exactly why a syntactic scan
                     is not enough (D07).
  window-close       reads the window's closing price to score a bar half an hour
                     before it. The subtle one: it looks like ordinary indexing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from panel.panel import Panel
from signals import _common

HORIZON_BARS = 30


# -- 1. lire le rendement qu'on prétend prédire ---------------------------------

def _forward_return(closes: pd.Series, position: int) -> float | None:
    ahead = position + HORIZON_BARS
    if ahead >= len(closes):
        return None
    here = float(closes.iloc[position])
    if here <= 0:
        return None
    return float(closes.iloc[ahead]) / here - 1.0


class forward_return:  # noqa: N801 -- un module-objet, pour tenir dans un fichier
    SIGNAL_ID = "tainted-forward-return"
    HYPOTHESIS = None
    PAPER = "aucun. Ce signal triche, et c'est son seul emploi."
    EXPECTED_SIGN = +1
    __file__ = __file__

    @staticmethod
    def scores(panel: Panel, cells=None, horizon_bars: int = HORIZON_BARS):
        return _common.run(panel, _forward_return, cells=cells, horizon_bars=horizon_bars)


# -- 2. normaliser en plein échantillon -----------------------------------------

def _first_half_hour(closes: pd.Series, position: int) -> float | None:
    if position < HORIZON_BARS:
        return None
    opening = float(closes.iloc[0])
    if opening <= 0:
        return None
    return float(closes.iloc[HORIZON_BARS - 1]) / opening - 1.0


class full_sample_zscore:  # noqa: N801
    SIGNAL_ID = "tainted-full-sample-zscore"
    HYPOTHESIS = None
    PAPER = "aucun. Ce signal triche, et c'est son seul emploi."
    EXPECTED_SIGN = +1
    __file__ = __file__

    @staticmethod
    def scores(panel: Panel, cells=None, horizon_bars: int = HORIZON_BARS):
        raw = _common.run(panel, _first_half_hour, cells=cells, horizon_bars=horizon_bars)
        out = {}
        for cell, series in raw.items():
            values = series.to_numpy(dtype=float)
            deviation = values.std()
            if deviation == 0 or not np.isfinite(deviation):
                out[cell] = series
                continue
            out[cell] = pd.Series(
                (values - values.mean()) / deviation, index=series.index, dtype=float
            )
        return out


# -- 3. regarder la clôture de la fenêtre ---------------------------------------

def _peek_at_close(closes: pd.Series, position: int) -> float | None:
    here = float(closes.iloc[position])
    if here <= 0:
        return None
    return float(closes.iloc[-1]) / here - 1.0


class window_close:  # noqa: N801
    SIGNAL_ID = "tainted-window-close"
    HYPOTHESIS = None
    PAPER = "aucun. Ce signal triche, et c'est son seul emploi."
    EXPECTED_SIGN = +1
    __file__ = __file__

    @staticmethod
    def scores(panel: Panel, cells=None, horizon_bars: int = HORIZON_BARS):
        return _common.run(panel, _peek_at_close, cells=cells, horizon_bars=horizon_bars)


TAINTED = (forward_return, full_sample_zscore, window_close)
