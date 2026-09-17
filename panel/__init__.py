"""The point-in-time data layer. Phase 02.

    from panel import Panel
    p = Panel.open(asof="2021-06-15 20:00", slice="pool")
    p.close("NQ")            # raw prices, up to that instant, never beyond
    p.truncate(end=earlier)  # a panel that knows less
    p.adjusted("NQ")         # back-adjusted, splices <= t only

The sealed slice takes a key nobody holds by accident: `unseal_holdout` writes
the gesture down before it hands one over (phase 04, D05).
"""

from panel.catalogue import Catalogue, Cell, Instrument, Slice, load_catalogue
from panel.panel import (
    HoldoutLocked,
    LookaheadRefused,
    NotInUniverse,
    Panel,
    PanelError,
    RollDatesMissing,
    SliceExceeded,
)
from panel.rolls import back_adjust, splice_ratios, visible_rolls
from panel.unseal import SealRefused, UnsealToken, times_opened, unseal_holdout

__all__ = [
    "Catalogue",
    "Cell",
    "HoldoutLocked",
    "Instrument",
    "LookaheadRefused",
    "NotInUniverse",
    "Panel",
    "PanelError",
    "RollDatesMissing",
    "SealRefused",
    "Slice",
    "SliceExceeded",
    "UnsealToken",
    "back_adjust",
    "load_catalogue",
    "splice_ratios",
    "times_opened",
    "unseal_holdout",
    "visible_rolls",
]
