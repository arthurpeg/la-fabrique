"""The evaluation harness. Frozen and versioned once gate 03 is crossed.

    from harness import evaluate
    report = evaluate(scores, panel, "30min", signal_id="...", hypothesis_ref="...")

Every IC it produces is written to registry/tests.jsonl on the way out
(invariant III). There is no other way to obtain one.
"""

from harness.costs import CellCost, cell_cost, costs_for
from harness.evaluate import evaluate, horizon_to_bars
from harness.metric import CellIC, cell_ic, deflated_t, forward_returns, pool
from harness.registry import code_hash, counted_tests, record_ic
from harness.report import (
    TARGET_IC_DEPENDENT_WINDOWS,
    TARGET_IC_INDEPENDENT_WINDOWS,
    ICReport,
    effective_breadth,
)

__all__ = [
    "TARGET_IC_DEPENDENT_WINDOWS",
    "TARGET_IC_INDEPENDENT_WINDOWS",
    "CellCost",
    "CellIC",
    "ICReport",
    "cell_cost",
    "cell_ic",
    "code_hash",
    "costs_for",
    "counted_tests",
    "deflated_t",
    "effective_breadth",
    "evaluate",
    "forward_returns",
    "horizon_to_bars",
    "pool",
    "record_ic",
]
