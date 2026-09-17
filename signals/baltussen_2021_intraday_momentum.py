"""H02 -- everything the window has done so far predicts its last half-hour.

Baltussen, Da, Lammers & Martens (2021), "Hedging demand and market intraday
momentum", JFE 142(1) (corpus/AMORCE.md, entry 2). A reference signal,
hand-written, sign known before measurement: positive (hypotheses/H02).

Of the two etalons this is the heavier reference: 60+ futures, our asset class
and our granularity, and a stated mechanism -- short-gamma hedging by option
sellers and levered ETFs, which forces end-of-session buying in the direction of
the day's move. It shares H01's target, so the two are correlated on purpose and
are never counted as two independent tests.
"""

from __future__ import annotations

import pandas as pd

from panel.panel import Panel
from signals import _common

SIGNAL_ID = "baltussen-2021-intraday-momentum"
HYPOTHESIS = "H02"
PAPER = (
    "Baltussen, Da, Lammers & Martens (2021), Hedging demand and market "
    "intraday momentum, JFE 142(1)"
)
EXPECTED_SIGN = +1


def _rest_of_the_window(closes: pd.Series, position: int) -> float | None:
    """The return from the window's open to the scored bar. Reads nothing past it."""
    opening = float(closes.iloc[0])
    if opening <= 0:
        return None
    return float(closes.iloc[position]) / opening - 1.0


def scores(panel: Panel, cells=None, horizon_bars: int = 30) -> dict[tuple[str, str], pd.Series]:
    """One score per session and per cell, at the bar that predicts the window's close."""
    return _common.run(panel, _rest_of_the_window, cells=cells, horizon_bars=horizon_bars)
