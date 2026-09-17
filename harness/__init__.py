"""The evaluation harness. Frozen and versioned; changed only by a written decision.

    from harness import evaluate
    report = evaluate(scores, panel, "30min", signal_id="...", hypothesis_ref="...")

Every IC it produces is written to registry/tests.jsonl on the way out
(invariant III). Since D05 that is no longer a property of this door being the
only one used: `pool` and `deflated_t` are private, a pooled IC needs a ticket
issued by the registry, and the line is written by the call that produces the
number. Importing `harness.metric` is not a way around this module.
"""

from harness.costs import CellCost, cell_cost, costs_for
from harness.evaluate import evaluate, horizon_to_bars
from harness.metric import CellIC, cell_ic, forward_returns, record_pooled
from harness.registry import (
    RegistryBypass,
    Ticket,
    code_hash,
    counted_tests,
    open_test,
    settle,
    validate_record,
)
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
    "RegistryBypass",
    "Ticket",
    "cell_cost",
    "cell_ic",
    "code_hash",
    "costs_for",
    "counted_tests",
    "effective_breadth",
    "evaluate",
    "forward_returns",
    "horizon_to_bars",
    "open_test",
    "record_pooled",
    "settle",
    "validate_record",
]
