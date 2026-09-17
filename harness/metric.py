"""The measurement itself: a time-series IC per cell, pooled, and a t that is corrected twice.

Three things are computed here and nowhere else.

FORWARD RETURNS THAT STAY INSIDE THEIR WINDOW. The three session windows are
disjoint and at most one strategy is alive per asset at a time (D01 3), so a
return is only defined when its end falls in the SAME window of the SAME session.
A horizon that would run past the close produces NaN, not a return borrowed from
the next window. Returns are taken on the back-adjusted series: the ASIA window
contains 00:00 UTC, which is where the splices land (L08), and a raw return
across one of those is an artefact, not a move.

THE IC. Spearman, per cell, over time -- never across the nine instruments, which
carry about four independent bets (D01 2, ledger F03). Rank correlation because
one-minute returns have heavy tails and because a signal's score may arrive on
any scale.

THE T, DEFLATED TWICE. A naive t is wrong here in two independent ways, and both
corrections are applied by the code rather than recommended to the reader:

  overlap        h-bar forward returns sampled every bar share h-1 bars, so
                 neighbouring observations are not independent. The effective
                 count is about n / h, hence a division by sqrt(h).
  cross-section  nine instruments hold ~4.2 independent bets, so pooling them
                 buys less than it appears: a division by sqrt(9 / 4.22), the
                 factor D01 2 names, computed from the phase-01 measurement.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass(frozen=True)
class CellIC:
    """One cell's diagnostic. Never a test on its own (D01 4)."""

    root: str
    window: str
    ic: float
    observations: int
    horizon_median_minutes: float
    horizon_p99_minutes: float


def forward_returns(
    close: pd.Series,
    session: pd.Series,
    window: pd.Series,
    horizon_bars: int,
) -> pd.Series:
    """The return from each bar to `horizon_bars` later, within the same window and session.

    The horizon is counted in BARS, not in minutes: 99.4 % of the bars are one
    minute apart, but not all of them. The realised horizon is measured and
    reported beside every IC rather than assumed -- see `cell_ic`.
    """
    key = pd.Series(list(zip(session, window, strict=True)), index=close.index)
    future = close.groupby(key, sort=False).shift(-horizon_bars)
    return future / close - 1.0


def realised_horizon(
    index: pd.DatetimeIndex, starts: pd.DatetimeIndex, horizon_bars: int
) -> tuple[float, float]:
    """How many minutes the horizon actually spans, over the pairs that BECOME a return.

    Measured on `starts` -- the bars that produced an observation -- and not on
    every bar of the cell. A cell's index jumps from one session close to the
    next session open, so spanning the whole index would report gaps of days for
    a thirty-minute horizon, which is alarming and meaningless: those pairs are
    exactly the ones `forward_returns` drops.
    """
    positions = index.get_indexer(starts)
    ends = positions + horizon_bars
    keep = (positions >= 0) & (ends < len(index))
    if not keep.any():
        return float("nan"), float("nan")
    spans = (index[ends[keep]] - index[positions[keep]]).total_seconds() / 60
    return float(np.median(spans)), float(np.quantile(spans, 0.99))


def cell_ic(scores: pd.Series, returns: pd.Series, index: pd.DatetimeIndex,
            root: str, window: str, horizon_bars: int) -> CellIC | None:
    """The Spearman IC of one cell, or None when there is nothing to measure."""
    frame = pd.concat([scores.rename("score"), returns.rename("ret")], axis=1).dropna()
    frame = frame[np.isfinite(frame["score"]) & np.isfinite(frame["ret"])]
    if len(frame) < 30 or frame["score"].nunique() < 2 or frame["ret"].nunique() < 2:
        return None
    ic = float(stats.spearmanr(frame["score"], frame["ret"]).statistic)
    median_span, p99_span = realised_horizon(index, frame.index, horizon_bars)
    return CellIC(
        root=root,
        window=window,
        ic=ic,
        observations=int(len(frame)),
        horizon_median_minutes=median_span,
        horizon_p99_minutes=p99_span,
    )


def pool(cells: list[CellIC]) -> tuple[float, int]:
    """The pooled IC: cells weighted by their observations, and the total count.

    A plain average would give `6B x EUROPE` the weight of `NQ x US`. The pooled
    figure is THE result; the per-cell values stay a diagnostic (D01 4).
    """
    if not cells:
        return float("nan"), 0
    weights = np.array([c.observations for c in cells], dtype=float)
    values = np.array([c.ic for c in cells], dtype=float)
    return float((values * weights).sum() / weights.sum()), int(weights.sum())


def deflated_t(ic: float, observations: int, horizon_bars: int,
               instruments: int, effective_breadth: float) -> dict[str, float]:
    """The naive t, then the same t once the two dependencies are paid for."""
    if observations < 3 or not np.isfinite(ic) or abs(ic) >= 1:
        return {"naive": float("nan"), "overlap": float("nan"), "final": float("nan"),
                "overlap_factor": float("nan"), "cross_section_factor": float("nan")}
    naive = ic * np.sqrt(observations - 2) / np.sqrt(1 - ic**2)
    overlap_factor = np.sqrt(max(horizon_bars, 1))
    cross_factor = np.sqrt(instruments / effective_breadth)
    after_overlap = naive / overlap_factor
    return {
        "naive": float(naive),
        "overlap": float(after_overlap),
        "final": float(after_overlap / cross_factor),
        "overlap_factor": float(overlap_factor),
        "cross_section_factor": float(cross_factor),
    }
