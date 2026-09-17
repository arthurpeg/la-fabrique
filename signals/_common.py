"""What the reference signals share: one cell's bars, and the bar that gets scored.

A score here is produced at ONE bar per session and per cell -- the first bar of
the window's last half-hour. Everywhere else the score is absent, which is not a
gap but the shape of the claim: both reference hypotheses are about the LAST half
hour of a window, so a score at any other bar would be an assertion nobody made.

Absent means absent: `evaluate` reindexes the scores on the cell's bars and drops
what is not finite, so an unscored bar produces no observation rather than a zero.

THE ANCHOR IS READ OFF THE CLOCK, NOT OFF THE DATA. This is the whole causality
of these signals, and the first version got it wrong. Taking "thirty bars before
the last bar of the group" needs to know where the group ENDS -- which, in a live
window, is not yet knowable. A signal built that way is fine in a backtest and
wrong in production, and the difference is invisible unless something looks for
it. So the anchor is the first bar whose distance to the window's close, as the
catalogue declares it (D01 3), is at most the horizon. That is a property each
bar carries by itself: no later bar is consulted to decide whether this one is
the anchor.

What it costs: when the last half-hour is thin, `forward_returns` runs out of
bars inside the window and the observation is dropped. That loss is real and it
is the honest price of a signal that could be run live.

ON LOOK-AHEAD more generally. The panel already refuses the future (invariant II),
but a signal can still look forward WITHIN what the panel shows, by reading a bar
later than the one it scores. The discipline is in one line: a predictor gets the
closes of its session and the POSITION of the bar being scored, and may read
nothing past that position. `sandbox/` turns that sentence into a test.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

from panel.panel import Panel
from panel.sessions import local, session_date, window_labels

MINUTES = 60.0


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


def minutes_to_close(index: pd.DatetimeIndex, panel: Panel, window: str) -> pd.Series:
    """How long each bar is from its window's close, on the exchange's clock.

    A property of the bar alone. Nothing later than it is consulted.

    IN WHOLE MINUTES, and that is not a detail. Computed in fractional hours,
    15:29 against a 16:00 close gives 31.000000000000004 -- so `<= 31` is false,
    the anchor slides one bar late, and the horizon falls one bar outside the
    window. The symptom was brutal and silent: NQ x US, the densest cell of the
    grid, produced 615 scores and ZERO measurable observations (L10).
    """
    window_end = panel.catalogue.windows[window].end_hour
    end_minutes = int(round(window_end * MINUTES))
    clock = local(index, panel.catalogue.timezone)
    minutes = clock.hour * 60 + clock.minute
    return pd.Series((end_minutes - minutes) % (24 * 60), index=index, dtype="int64")


def score_at_window_end(
    close: pd.Series,
    sessions: pd.Series,
    remaining: pd.Series,
    horizon_bars: int,
    predictor: Callable[[pd.Series, int], float | None],
) -> pd.Series:
    """One score per session, at the first bar of the window's last half-hour.

    `predictor(closes_of_this_session, position)` may read `closes.iloc[:position + 1]`
    and nothing beyond. Returning None declines the session.
    """
    scored: dict[pd.Timestamp, float] = {}
    for _, group in close.groupby(sessions, sort=False):
        left = remaining.reindex(group.index).to_numpy(dtype=float)
        # `horizon_bars + 1`, et le +1 n'est pas cosmétique. La barre située à
        # exactement `horizon` minutes de la clôture a `horizon` barres APRÈS
        # elle, donc son rendement à `horizon` barres tombe une barre au-delà de
        # la fenêtre : le harnais le jette, et le signal produit des milliers de
        # scores pour zéro observation. On prend donc la dernière barre qui
        # laisse la place au horizon tout entier.
        eligible = np.flatnonzero(left <= horizon_bars + 1)
        if eligible.size == 0:
            continue
        position = int(eligible[0])
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
            remaining = minutes_to_close(close.index, panel, window)
            series = score_at_window_end(
                close, sessions, remaining, horizon_bars, predictor
            )
            if not series.empty:
                out[(root, window)] = series
    return out
