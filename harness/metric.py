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

  overlap        h-bar forward returns can share bars, and then neighbouring
                 observations are not independent. HOW MUCH they share is
                 measured, not assumed: each cell reports the median gap, in
                 bars, between two consecutive observations, and a cell whose
                 gap is at least h shares nothing. Scored every bar, the factor
                 is sqrt(h) as before; scored once a session, it is 1 (D11).
  cross-section  nine instruments hold ~4.2 independent bets, so pooling them
                 buys less than it appears: a division by sqrt(9 / 4.22), the
                 factor D01 2 names, computed from the phase-01 measurement.

AND NOTHING HERE HANDS OUT A NUMBER ON ITS OWN. Since phase 04 the pooling and
the deflation are private (`_pool`, `_deflated_t`); the only public way to a
pooled IC is `record_pooled`, which demands a ticket and writes the registry line
before it returns the value (D05). Importing this module is no longer a way
around `evaluate`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

from harness.registry import RegistryBypass, Ticket, settle


@dataclass(frozen=True)
class CellIC:
    """One cell's diagnostic. Never a test on its own (D01 4)."""

    root: str
    window: str
    ic: float
    observations: int
    horizon_median_minutes: float
    horizon_p99_minutes: float
    # The median distance, in bars of this cell's series, between two
    # consecutive observations. 1 means a score on every bar -- the fully
    # overlapping case D04 had in mind. It defaults to 1 so that a caller who
    # does not measure it gets the old, conservative treatment (D11).
    sampling_gap_bars: float = 1.0

    @property
    def overlap_ratio(self) -> float:
        """How many observations this cell's horizon spreads over. 1 = no overlap."""
        gap = self.sampling_gap_bars
        if not np.isfinite(gap) or gap <= 0:
            return 1.0
        return max(1.0, float(gap))


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


def sampling_gap(index: pd.DatetimeIndex, observed: pd.DatetimeIndex) -> float:
    """The median distance, in bars of this cell, between two observations.

    Measured on the cell's own series, which is the unit the horizon is counted
    in: a US window holds ~390 one-minute bars, so consecutive sessions sit 390
    apart and a thirty-bar horizon cannot reach from one to the next.

    Why this is measured and not declared: a signal that claimed not to overlap
    would buy a t multiplied by sqrt(h) on its word alone (D11, option 3).
    """
    if len(observed) < 2:
        return 1.0
    positions = index.get_indexer(observed)
    positions = positions[positions >= 0]
    if len(positions) < 2:
        return 1.0
    gaps = np.diff(np.sort(positions))
    gaps = gaps[gaps > 0]
    if not len(gaps):
        return 1.0
    return float(np.median(gaps))


def cell_ic(scores: pd.Series, returns: pd.Series, index: pd.DatetimeIndex,
            root: str, window: str, horizon_bars: int, ticket: Ticket) -> CellIC | None:
    """The Spearman IC of one cell, or None when there is nothing to measure.

    A cell IC is a diagnostic and never a test on its own (D01 4) -- but it is
    still an IC, so it is still unreachable without a live ticket. The ticket is
    not spent here: one ticket buys one POOLED number and the line that records
    it, whatever the number of cells that went into it.
    """
    if not isinstance(ticket, Ticket) or ticket.spent:
        raise RegistryBypass(
            "cell_ic needs a live Ticket from registry.open_test(). An IC that "
            "nothing will record is an IC that must not be computed (invariant III)."
        )
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
        sampling_gap_bars=sampling_gap(index, frame.index),
    )


def _pool(cells: list[CellIC]) -> tuple[float, int]:
    """The pooled IC: cells weighted by their observations, and the total count.

    A plain average would give `6B x EUROPE` the weight of `NQ x US`. The pooled
    figure is THE result; the per-cell values stay a diagnostic (D01 4).
    """
    if not cells:
        return float("nan"), 0
    weights = np.array([c.observations for c in cells], dtype=float)
    values = np.array([c.ic for c in cells], dtype=float)
    return float((values * weights).sum() / weights.sum()), int(weights.sum())


def _effective_observations(cells: list[CellIC], horizon_bars: int) -> tuple[float, float]:
    """How many independent observations the cells really hold, and the gap.

    Each cell contributes `n_c / f_c` with `f_c = max(1, h / gap_c)`: a cell
    scored every bar spreads its horizon over h observations, a cell scored once
    a session over one. Summing per cell is what keeps the mixed case honest --
    neither the most overlapping cell nor a plain average of factors decides for
    the others (D11).
    """
    total = sum(c.observations for c in cells)
    if not total:
        return 0.0, 1.0
    effective = 0.0
    for cell in cells:
        spread = max(1.0, horizon_bars / cell.overlap_ratio)
        effective += cell.observations / spread
    gaps = np.array([c.overlap_ratio for c in cells], dtype=float)
    weights = np.array([c.observations for c in cells], dtype=float)
    median_gap = float(np.sum(gaps * weights) / weights.sum())
    return effective, median_gap


def _deflated_t(ic: float, observations: int, cells: list[CellIC], horizon_bars: int,
                instruments: int, effective_breadth: float) -> dict[str, float]:
    """The naive t, then the same t once the two dependencies are paid for."""
    if observations < 3 or not np.isfinite(ic) or abs(ic) >= 1:
        return {"naive": float("nan"), "overlap": float("nan"), "final": float("nan"),
                "overlap_factor": float("nan"), "cross_section_factor": float("nan"),
                "sampling_gap_bars": float("nan")}
    naive = ic * np.sqrt(observations - 2) / np.sqrt(1 - ic**2)
    effective, gap = _effective_observations(cells, horizon_bars)
    overlap_factor = np.sqrt(observations / effective) if effective > 0 else 1.0
    cross_factor = np.sqrt(instruments / effective_breadth)
    after_overlap = naive / overlap_factor
    return {
        "naive": float(naive),
        "overlap": float(after_overlap),
        "final": float(after_overlap / cross_factor),
        "overlap_factor": float(overlap_factor),
        "cross_section_factor": float(cross_factor),
        "sampling_gap_bars": float(gap),
    }


def record_pooled(
    cells: list[CellIC],
    ticket: Ticket,
    *,
    horizon_bars: int,
    instruments: int,
    effective_breadth: float,
    extra: dict | None = None,
) -> dict:
    """Pool, deflate, WRITE, and only then return. The write is not a courtesy.

    This is the single public path from cell diagnostics to a pooled IC. It
    spends the ticket, so the number and its line come into existence together
    or not at all (invariant III, D05).
    """
    if not isinstance(ticket, Ticket):
        raise RegistryBypass(
            "record_pooled needs a Ticket from registry.open_test(); there is no "
            "other way to obtain a pooled IC."
        )
    ic, observations = _pool(cells)
    t = _deflated_t(ic, observations, cells, horizon_bars, instruments, effective_breadth)
    line = dict(extra or {})
    line["observations"] = observations
    test_id = settle(ticket, ic=ic, t_stat=t["final"], extra=line)
    return {"ic": ic, "observations": observations, "t": t, "test_id": test_id}
