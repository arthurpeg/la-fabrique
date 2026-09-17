"""What the reference signals share: one cell's bars, grouped by session.

A score here is produced at ONE bar per session and per cell -- the bar whose
`horizon_bars`-long forward return ends exactly on the window's close. Everywhere
else the score is absent, which is not a gap but the shape of the claim: both
reference hypotheses are about the LAST half-hour of a window, so a score at any
other bar would be an assertion nobody made.

Absent means absent: `evaluate` reindexes the scores on the cell's bars and drops
what is not finite, so an unscored bar produces no observation rather than a zero.

ON LOOK-AHEAD. Nothing here has access to the future -- the panel already refuses
it (invariant II) -- but a signal can still look forward WITHIN what the panel
shows, by reading a bar later than the one it scores. The whole discipline of
this module is in one line: a predictor is handed the closes of its session and
the POSITION of the bar being scored, and it may read nothing past that position.
Phase 05 will make that a test rather than a sentence.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from panel.panel import Panel
from panel.sessions import session_date, window_labels


def cell_bars(panel: Panel, root: str, window: str) -> tuple[pd.Series, pd.Series]:
    """The back-adjusted closes of one cell, and the session each bar belongs to.

    Back-adjusted, like the returns the harness measures against: the ASIA window
    contains 00:00 UTC, where the splices land, and a raw move across one is an
    artefact (L08).
    """
    adjusted = panel.adjusted(root, columns=["close"])["close"]
    labels = window_labels(adjusted.index, panel.catalogue)
    sessions = session_date(adjusted.index, panel.catalogue)
    mask = (labels == window).to_numpy()
    return adjusted[mask], sessions[mask]


def score_at_window_end(
    close: pd.Series,
    sessions: pd.Series,
    horizon_bars: int,
    predictor: Callable[[pd.Series, int], float | None],
) -> pd.Series:
    """One score per session, at the bar whose horizon ends on the window's close.

    `predictor(closes_of_this_session, position)` may read `closes.iloc[:position + 1]`
    and nothing beyond. Returning None declines the session.
    """
    scored: dict[pd.Timestamp, float] = {}
    for _, group in close.groupby(sessions, sort=False):
        position = len(group) - 1 - horizon_bars
        # The predictor needs at least `horizon_bars` bars behind the scored one,
        # so a truncated session -- a holiday close, a data gap -- is declined
        # rather than scored on whatever happens to be there.
        if position < horizon_bars:
            continue
        value = predictor(group, position)
        if value is None or value != value:
            continue
        scored[group.index[position]] = float(value)
    if not scored:
        return pd.Series(dtype=float)
    return pd.Series(scored, dtype=float).sort_index()


def run(
    panel: Panel,
    predictor: Callable[[pd.Series, int], float | None],
    cells=None,
    horizon_bars: int = 30,
) -> dict[tuple[str, str], pd.Series]:
    """Apply one predictor to every retained cell of the panel."""
    wanted = tuple(cells) if cells is not None else panel.cells()
    out: dict[tuple[str, str], pd.Series] = {}
    for root in sorted({r for r, _ in wanted}):
        for window in sorted({w for r, w in wanted if r == root}):
            close, sessions = cell_bars(panel, root, window)
            if close.empty:
                continue
            series = score_at_window_end(close, sessions, horizon_bars, predictor)
            if not series.empty:
                out[(root, window)] = series
    return out
