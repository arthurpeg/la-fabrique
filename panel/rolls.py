"""Back-adjustment: making a spliced series comparable to itself across contracts.

A continuous future is a splicing of expiries. The price level jumps at each
splice, so any quantity computed over a window that straddles one is wrong over
its whole width -- realised volatility, moving averages, momentum (D01 6).
Neutralising the roll bar alone is necessary and nowhere near sufficient.

Two properties matter, and they drive every choice below.

MULTIPLICATIVE, NOT ADDITIVE. D01 6 states that the series built at t differs
from the one built at t+1 by a uniform SCALE factor, which leaves returns and
ratios untouched. That is the multiplicative convention: each segment before a
splice is multiplied by the gaps that follow it. An additive convention would
shift levels by a constant instead, and would not preserve returns.

ONLY THE SPLICES <= T. The adjustment of a panel as of t uses the rolls known at
t and no other. Adding a later roll multiplies the whole series by one more
factor -- uniformly -- so the two series agree on every return. That is what
makes the object point-in-time rather than merely truncated.

WHAT THE GAP ESTIMATE COSTS. With only a spliced OHLCV series, the jump can be
read in one place: the one-minute return at the splice minute. That return holds
the contract spread AND whatever the market genuinely did in that minute, and
nothing here can separate them. The adjustment therefore removes a little real
move along with the artefact. It is the same convention the phase-01 detector
used (scripts/roll_diagnostics.py), it is declared in D03, and it is the only
thing computable without contract-level data.
"""

from __future__ import annotations

from typing import NamedTuple

import pandas as pd

PRICE_COLUMNS = ("open", "high", "low", "close")


def parse_roll(value, splice_minute_utc: str = "00:00") -> pd.Timestamp:
    """A roll date, as given, turned into the instant of its splice.

    A bare date is combined with the splice minute declared in the catalogue;
    a full timestamp is taken as it stands.
    """
    text = str(value).strip()
    timestamp = pd.Timestamp(text if len(text) > 10 else f"{text} {splice_minute_utc}")
    return timestamp.tz_localize("UTC") if timestamp.tz is None else timestamp.tz_convert("UTC")


def visible_rolls(rolls, asof: pd.Timestamp, splice_minute_utc: str = "00:00") -> list:
    """The splices knowable at `asof`, sorted, deduplicated. The others do not exist yet."""
    parsed = {parse_roll(value, splice_minute_utc) for value in rolls or ()}
    return sorted(stamp for stamp in parsed if stamp <= asof)


class Splice(NamedTuple):
    """One roll, and where it actually lands in a series that has holes."""

    roll: pd.Timestamp  # the instant the vendor says the contract changed
    bar: pd.Timestamp  # the first bar at or after it -- where the jump is observed
    ratio: float  # that bar's price over the previous one


def splice_ratios(reference: pd.Series, rolls) -> list[Splice]:
    """The observed jump at each splice: first price of the new contract over the last of the old.

    A roll falling outside the data -- before the first bar, or after the last --
    has no observable gap and is skipped rather than guessed.

    WHEN THE MARKET WAS SHUT. The vendor dates a roll to a day; our series has a
    bar at that instant only if the market was open. It usually is: 292 of the
    333 rolls visible in mid-2023 fall on a bar at 00:00 UTC exactly. For the
    other 41 -- almost all CL (31%) and GC (29%), whose rolls can land on a
    weekend -- the first bar comes hours later, and the measured gap then spans
    the closure: median 44.9 bp against 28.5 bp for an on-bar splice, and up to
    3 648 bp. The adjustment absorbs that whole move. Applying it anyway is the
    lesser evil -- skipping leaves an artificial jump of the same order in the
    series -- but it is the widest form of the cost described above.
    """
    splices: list[Splice] = []
    index = reference.index
    for stamp in rolls:
        position = index.searchsorted(stamp, side="left")
        if position == 0 or position >= len(index):
            continue
        before = float(reference.iloc[position - 1])
        after = float(reference.iloc[position])
        if before <= 0 or after <= 0:
            continue
        splices.append(Splice(roll=stamp, bar=index[position], ratio=after / before))
    return splices


def adjustment_factors(reference: pd.Series, rolls) -> pd.Series:
    """One multiplier per bar: the product of every gap that comes after it."""
    factors = pd.Series(1.0, index=reference.index, name="adjustment")
    for splice in splice_ratios(reference, rolls):
        factors.loc[factors.index < splice.bar] *= splice.ratio
    return factors


def back_adjust(frame: pd.DataFrame, rolls, reference: str = "close") -> pd.DataFrame:
    """The frame with its price columns made comparable across contracts.

    The most recent segment keeps its raw prices; earlier segments are scaled by
    the gaps that follow them. Volume is left alone -- it is not a price.
    """
    if reference not in frame.columns:
        raise KeyError(
            f"back_adjust needs the {reference!r} column to measure the gaps; "
            f"the frame holds {', '.join(frame.columns)}"
        )
    factors = adjustment_factors(frame[reference], rolls)
    adjusted = frame.copy()
    for column in PRICE_COLUMNS:
        if column in adjusted.columns:
            adjusted[column] = adjusted[column] * factors
    return adjusted
