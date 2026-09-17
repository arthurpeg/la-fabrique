"""The Panel: the only way this project reads market data.

Invariant II says the look-ahead is prevented BY CONSTRUCTION, never by
vigilance. This module is where that construction happens, and it rests on one
idea: a Panel is opened AS OF an instant, and there is no public path through
it to a bar stamped later than that instant. The future is not filtered out
after the fact -- it is never read from disk at all (the cutoff is pushed down
into the parquet reader), so a signal cannot reach it even by accident.

Four things are refused, loudly, rather than approximated:

  LookaheadRefused   asking a panel for a moment after its own as-of.
  SliceExceeded      an as-of outside the slice being worked on.
  HoldoutLocked      the sealed slice, which opens once, in phase 15.
  RollDatesMissing   the back-adjusted series, until the authoritative roll
                     dates arrive. A silent approximation here would be wrong
                     over the whole width of every window that straddles a
                     splice (D01 6), and nothing would raise.

The raw price stays available throughout: it is what execution and levels need.
"""

from __future__ import annotations

import hashlib

import pandas as pd

from panel.catalogue import Catalogue, Slice, load_catalogue
from panel.paths import data_dir
from panel.sessions import session_date, session_date_of, window_labels

INDEX_NAME = "ts_event"


class PanelError(Exception):
    """Anything the Panel refuses to do."""


class LookaheadRefused(PanelError):
    """A moment later than the as-of of the panel was asked for."""


class SliceExceeded(PanelError):
    """The as-of falls outside the slice being worked on."""


class HoldoutLocked(PanelError):
    """The sealed slice. It opens once, in phase 15, and never again."""


class RollDatesMissing(PanelError):
    """The back-adjusted series cannot be built: the roll dates are not known."""


class NotInUniverse(PanelError):
    """The instrument exists in the catalogue but not in the working universe."""


def _as_utc(value) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    return timestamp.tz_localize("UTC") if timestamp.tz is None else timestamp.tz_convert("UTC")


class Panel:
    """Market data as it was knowable at `asof`, and nothing else."""

    def __init__(self, asof: pd.Timestamp, slice_: Slice, catalogue: Catalogue) -> None:
        self.asof = asof
        self.slice = slice_
        self.catalogue = catalogue
        self._frames: dict[tuple[str, tuple[str, ...] | None], pd.DataFrame] = {}

    # -- opening -----------------------------------------------------------

    @classmethod
    def open(cls, asof, slice: str = "pool", catalogue: Catalogue | None = None) -> Panel:
        catalogue = catalogue or load_catalogue()
        wanted = catalogue.slice(slice)

        if wanted.sealed:
            raise HoldoutLocked(
                f"slice {wanted.name!r} is sealed until phase {wanted.unseal_phase}. "
                "It is opened once, at the very end, and a reopened holdout is no "
                "longer a holdout (invariant V)."
            )

        asof = _as_utc(asof)
        session = session_date_of(asof, catalogue)
        start, end = pd.Timestamp(wanted.start).date(), pd.Timestamp(wanted.end).date()
        if not start <= session <= end:
            raise SliceExceeded(
                f"as-of {asof} sits in session {session}, outside slice "
                f"{wanted.name!r} ({wanted.start} -> {wanted.end})."
            )
        return cls(asof=asof, slice_=wanted, catalogue=catalogue)

    def truncate(self, end) -> Panel:
        """The same panel, knowing less. It can never know more."""
        end = _as_utc(end)
        if end > self.asof:
            raise LookaheadRefused(
                f"truncate(end={end}) would move the as-of forward, from {self.asof}. "
                "A panel loses its future, it never gains one."
            )
        return Panel(asof=end, slice_=self.slice, catalogue=self.catalogue)

    # -- what exists at this instant ---------------------------------------

    def universe(self) -> tuple[str, ...]:
        """The instruments listed at `asof`. The answer depends on the as-of, on nothing else."""
        return tuple(
            root
            for root in self.catalogue.universe()
            if _as_utc(self.catalogue.instrument(root).start) <= self.asof
        )

    def cells(self) -> tuple[tuple[str, str], ...]:
        listed = set(self.universe())
        return tuple(cell for cell in self.catalogue.retained_cells() if cell[0] in listed)

    # -- reading ------------------------------------------------------------

    def bars(self, root: str, columns: list[str] | None = None, window: str | None = None):
        """OHLCV up to `asof`, raw (spliced) prices. Never a row stamped later."""
        if root not in self.universe():
            instrument = self.catalogue.instrument(root)
            reason = (
                "not in the working universe"
                if not instrument.in_universe
                else f"not listed yet at {self.asof} (history starts {instrument.start})"
            )
            raise NotInUniverse(f"{root}: {reason}.")

        frame = self._read(root, columns)
        if window is not None:
            if window not in self.catalogue.windows:
                known = ", ".join(self.catalogue.windows)
                raise KeyError(f"unknown window {window!r}; the grid holds {known}")
            frame = frame[window_labels(frame.index, self.catalogue) == window]
        return frame

    def close(self, root: str) -> pd.Series:
        return self.bars(root, columns=["close"])["close"]

    def sessions(self, root: str) -> pd.Series:
        return session_date(self.bars(root, columns=["close"]).index, self.catalogue)

    def windows(self, root: str) -> pd.Series:
        return window_labels(self.bars(root, columns=["close"]).index, self.catalogue)

    def adjusted(self, root: str):
        """The back-adjusted series. Blocked, on purpose, until the roll dates arrive."""
        instrument = self.catalogue.instrument(root)
        if instrument.roll_dates is None:
            raise RollDatesMissing(
                f"{root}: no authoritative roll dates in the catalogue (todo roll-dates, "
                "owed by the data author). The back-adjusted series must use only the "
                "splices <= as-of (D01 6); the empirical detector is not authoritative "
                "and its holes are systematic (L05, F09). Raw prices remain available "
                "through bars()."
            )
        raise NotImplementedError(
            f"{root}: roll dates are present but the back-adjustment is not written yet."
        )

    def fingerprint(self, root: str) -> str:
        """A checksum of everything this panel can see of one instrument."""
        frame = self.bars(root, columns=["close"])
        payload = b"".join(
            (frame.index.asi8.tobytes(), frame["close"].to_numpy("float64").tobytes())
        )
        return hashlib.sha256(payload).hexdigest()

    # -- internals -----------------------------------------------------------

    def _read(self, root: str, columns: list[str] | None) -> pd.DataFrame:
        key = (root, tuple(columns) if columns else None)
        cached = self._frames.get(key)
        if cached is not None:
            return cached

        path = data_dir() / self.catalogue.instrument(root).file
        frame = pd.read_parquet(path, columns=columns, filters=[(INDEX_NAME, "<=", self.asof)])
        if len(frame) and frame.index[-1] > self.asof:
            raise LookaheadRefused(
                f"{root}: the reader returned a bar at {frame.index[-1]}, later than "
                f"the as-of {self.asof}. The cutoff was not applied -- stop here."
            )
        self._frames[key] = frame
        return frame

    def __repr__(self) -> str:
        return (
            f"Panel(asof={self.asof}, slice={self.slice.name!r}, "
            f"instruments={len(self.universe())})"
        )
