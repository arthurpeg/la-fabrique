"""H01 -- the first half-hour of a window predicts its last half-hour.

Gao, Han, Li & Zhou (2018), "Market intraday momentum", JFE 129(2):394-414
(corpus/AMORCE.md, entry 1). A reference signal, hand-written, whose expected
answer is known BEFORE it is measured: the sign is positive (hypotheses/H01).

It is an etalon, not a candidate for production (D06). What it is for: giving
gates 05, 06 and 08 a subject -- a look-ahead to inject and catch, a signal to
degrade, an implementation for an agent to reproduce.

THE TRANSPOSITION, AND WHAT IT COSTS. Gao et al. work on a US equity session:
first half-hour against last half-hour of one trading day. Our grid holds three
disjoint windows per session (D01 3), so "the day" becomes "the window", and the
claim is made three times over -- once per window -- rather than once. That is a
stronger claim than the paper's, not a weaker one, and the per-cell breakdown is
where it will show if only the US window carries it.
"""

from __future__ import annotations

import pandas as pd

from panel.panel import Panel
from signals import _common

SIGNAL_ID = "gao-2018-intraday-momentum"
HYPOTHESIS = "H01"
PAPER = "Gao, Han, Li & Zhou (2018), Market intraday momentum, JFE 129(2):394-414"
EXPECTED_SIGN = +1

FIRST_BARS = 30


def _first_half_hour(closes: pd.Series, position: int) -> float | None:
    """The return of the window's first thirty minutes. Reads nothing past `position`."""
    if position < FIRST_BARS:
        return None
    opening = float(closes.iloc[0])
    if opening <= 0:
        return None
    thirty = float(closes.iloc[FIRST_BARS - 1])
    return thirty / opening - 1.0


def scores(panel: Panel, cells=None, horizon_bars: int = 30) -> dict[tuple[str, str], pd.Series]:
    """One score per session and per cell, at the bar that predicts the window's close."""
    return _common.run(panel, _first_half_hour, cells=cells, horizon_bars=horizon_bars)
