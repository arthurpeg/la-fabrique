"""The point-in-time data layer. Phase 02.

    from panel import Panel
    p = Panel.open(asof="2021-06-15 20:00", slice="pool")
    p.close("NQ")            # raw prices, up to that instant, never beyond
    p.truncate(end=earlier)  # a panel that knows less
    p.adjusted("NQ")         # RollDatesMissing, until the roll dates arrive
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
    "Slice",
    "SliceExceeded",
    "load_catalogue",
]
