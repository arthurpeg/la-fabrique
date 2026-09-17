"""Sessions: which window a bar belongs to, and which session it belongs to.

Two conventions, both declared in the catalogue rather than hard-coded here.

WINDOWS are anchored to the exchange's local clock, not to UTC: anchoring to
UTC would drift the windows by an hour twice a year, on dates nobody chose
(D01 3). The three windows are disjoint, and 16:00 -> 19:00 belongs to none of
them -- a bar there gets no window at all, which is the point.

The SESSION DATE labels a session by the calendar date of its US window. A
session opens at 19:00 the evening before, so shifting the local clock by
+6 hours puts a whole session on a single date.
"""

from __future__ import annotations

import pandas as pd

from panel.catalogue import Catalogue, Window


def local(index: pd.DatetimeIndex, timezone: str) -> pd.DatetimeIndex:
    """The same instants, read on the exchange's clock."""
    return index.tz_convert(timezone)


def _local_hour(index: pd.DatetimeIndex, timezone: str) -> pd.Series:
    clock = local(index, timezone)
    return pd.Series(clock.hour + clock.minute / 60, index=index, name="local_hour")


def in_window(index: pd.DatetimeIndex, timezone: str, window: Window) -> pd.Series:
    """Boolean mask: does each bar fall inside this session window?"""
    hour = _local_hour(index, timezone)
    if window.crosses_midnight:
        return (hour >= window.start_hour) | (hour < window.end_hour)
    return (hour >= window.start_hour) & (hour < window.end_hour)


def window_labels(index: pd.DatetimeIndex, catalogue: Catalogue) -> pd.Series:
    """The window each bar belongs to, or None for the uncovered 16:00 -> 19:00."""
    labels = pd.Series(None, index=index, dtype=object, name="window")
    for window in catalogue.windows.values():
        labels[in_window(index, catalogue.timezone, window)] = window.name
    return labels


def session_date(index: pd.DatetimeIndex, catalogue: Catalogue) -> pd.Series:
    """The session each bar belongs to, as a date."""
    shifted = local(index, catalogue.timezone) + pd.Timedelta(
        hours=catalogue.session_shift_hours
    )
    return pd.Series(shifted.date, index=index, name="session_date")


def session_date_of(timestamp: pd.Timestamp, catalogue: Catalogue):
    """The session a single instant belongs to. Used to place an as-of in a slice."""
    shifted = timestamp.tz_convert(catalogue.timezone) + pd.Timedelta(
        hours=catalogue.session_shift_hours
    )
    return shifted.date()
