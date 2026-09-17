"""`evaluate` -- the one door. An IC that did not come through here does not exist.

The harness is deliberately ignorant of what a signal is: it receives SCORES,
already computed, one series per cell. How a signal produces them without
touching the future is phase 05's problem, and nothing here prejudges that
interface.

What this function does, in order: take the back-adjusted prices the panel is
willing to show at its as-of, build forward returns that stay inside their own
window, rank-correlate them with the scores cell by cell, pool by observation
count, deflate the t twice, price the round trip as far as it can be priced --
and write the line to the registry before returning. The write is not at the end
as a courtesy: it is the reason the function exists (invariant III).
"""

from __future__ import annotations

import pandas as pd

from harness import registry
from harness.costs import costs_for
from harness.metric import CellIC, cell_ic, deflated_t, forward_returns, pool
from harness.report import ICReport, effective_breadth
from panel.panel import Panel
from panel.sessions import session_date, window_labels


def horizon_to_bars(horizon: str | int) -> int:
    """Bars are one minute here, so a horizon in minutes is a horizon in bars."""
    if isinstance(horizon, int):
        return horizon
    text = str(horizon).strip().lower()
    if text.endswith("min"):
        return int(text[:-3])
    if text.endswith("h"):
        return int(text[:-1]) * 60
    raise ValueError(f"unreadable horizon {horizon!r}: expected '30min', '2h' or a number of bars")


def evaluate(
    scores: dict[tuple[str, str], pd.Series],
    panel: Panel,
    horizon: str | int,
    *,
    signal_id: str,
    hypothesis_ref: str | None = None,
    stage: str = "04-rapport-ic",
) -> ICReport:
    """Evaluate scores against forward returns, register the IC, return the report."""
    bars = horizon_to_bars(horizon)
    catalogue = panel.catalogue
    retained = set(panel.cells())

    unknown = [cell for cell in scores if cell not in retained]
    if unknown:
        raise KeyError(
            f"scores given for cells that are not retained at this as-of: {unknown[:3]}. "
            f"The grid holds {len(retained)} cells (D01 3)."
        )

    cells: list[CellIC] = []
    for root in sorted({root for root, _ in scores}):
        adjusted = panel.adjusted(root, columns=["close"])["close"]
        labels = window_labels(adjusted.index, catalogue)
        sessions = session_date(adjusted.index, catalogue)
        for window in sorted({w for r, w in scores if r == root}):
            mask = (labels == window).to_numpy()
            close = adjusted[mask]
            if close.empty:
                continue
            returns = forward_returns(close, sessions[mask], labels[mask], bars)
            aligned = scores[(root, window)].reindex(close.index)
            measured = cell_ic(aligned, returns, close.index, root, window, bars)
            if measured is not None:
                cells.append(measured)

    ic, observations = pool(cells)
    instruments = len(panel.universe())
    breadth = effective_breadth()
    t = deflated_t(ic, observations, bars, instruments, breadth)

    test_id = registry.record_ic(
        ic=ic,
        t_stat=t["final"],
        horizon=str(horizon),
        data_slice=panel.slice.name,
        signal_id=signal_id,
        hypothesis_ref=hypothesis_ref,
        stage=stage,
        extra={"asof": str(panel.asof), "cells": len(cells), "observations": observations},
    )

    return ICReport(
        test_id=test_id,
        signal_id=signal_id,
        hypothesis_ref=hypothesis_ref,
        stage=stage,
        data_slice=panel.slice.name,
        asof=str(panel.asof),
        horizon=str(horizon),
        horizon_bars=bars,
        ic=ic,
        observations=observations,
        t=t,
        cells=tuple(cells),
        costs=tuple(costs_for(catalogue, sorted(scores)).values()),
        instruments=instruments,
        breadth=breadth,
        code_hash=registry.code_hash(),
        counted_tests=registry.counted_tests(),
    )
