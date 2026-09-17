"""The catalogue, read once and turned into plain frozen objects.

Nothing here computes anything: it reads a declaration. The catalogue is the
only place that knows which instruments exist, when each history starts, which
cells are retained, and -- just as important -- what is still unknown. A field
whose value is unknown is None here, exactly as it is null in the YAML; it is
never replaced by a plausible default.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from panel.paths import CATALOGUE


@dataclass(frozen=True)
class Cell:
    """One (instrument, session window) pair, and what phase 01 measured on it."""

    root: str
    window: str
    retained: bool
    spread_floor_bp: float
    median_volume_per_minute: float
    share_thin_bars: float
    median_abs_15min_move_bp: float
    round_trip_over_move: float


@dataclass(frozen=True)
class Instrument:
    root: str
    name: str
    symbol: str
    asset_class: str
    file: str
    exchange: str
    clock: str | None
    in_universe: bool
    start: str
    end: str
    bars: int
    years: float
    tick: float | None
    multiplier: float | None
    fee_per_contract_usd: float | None
    roll_rule: str
    roll_cycle: str | None
    splice_minute_utc: str
    roll_dates: list[str] | None
    cells: dict[str, Cell]

    def cell(self, window: str) -> Cell:
        try:
            return self.cells[window]
        except KeyError:
            raise KeyError(f"{self.root}: no cell measured for window {window!r}") from None


@dataclass(frozen=True)
class Slice:
    name: str
    start: str
    end: str
    sealed: bool
    unseal_phase: int | None


@dataclass(frozen=True)
class Window:
    name: str
    start_hour: float
    end_hour: float
    crosses_midnight: bool


@dataclass(frozen=True)
class Catalogue:
    path: Path
    timezone: str
    session_shift_hours: int
    windows: dict[str, Window]
    slices: dict[str, Slice]
    instruments: dict[str, Instrument]

    def instrument(self, root: str) -> Instrument:
        try:
            return self.instruments[root]
        except KeyError:
            known = ", ".join(self.instruments)
            raise KeyError(f"unknown instrument {root!r}; the catalogue holds {known}") from None

    def universe(self) -> tuple[str, ...]:
        """Every instrument the project works on. Membership at a date is the Panel's job."""
        return tuple(r for r, i in self.instruments.items() if i.in_universe)

    def retained_cells(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (root, window)
            for root in self.universe()
            for window, cell in self.instruments[root].cells.items()
            if cell.retained
        )

    def slice(self, name: str) -> Slice:
        try:
            return self.slices[name]
        except KeyError:
            known = ", ".join(self.slices)
            raise KeyError(f"unknown slice {name!r}; the catalogue holds {known}") from None

    def missing(self) -> dict[str, list[str]]:
        """Every field still null, by todo id. A null without a todo is a bug."""
        holes: dict[str, list[str]] = {"roll-dates": [], "multipliers": [], "fees": []}
        for root, inst in self.instruments.items():
            if inst.roll_dates is None:
                holes["roll-dates"].append(root)
            if inst.multiplier is None:
                holes["multipliers"].append(root)
            if inst.fee_per_contract_usd is None:
                holes["fees"].append(root)
        return holes


def _hour(text: str) -> float:
    hours, minutes = text.split(":")
    return int(hours) + int(minutes) / 60


@lru_cache(maxsize=4)
def load_catalogue(path: Path = CATALOGUE) -> Catalogue:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))

    windows = {
        name: Window(
            name=name,
            start_hour=_hour(spec["start"]),
            end_hour=_hour(spec["end"]),
            crosses_midnight=bool(spec["crosses_midnight"]),
        )
        for name, spec in raw["grid"]["windows"].items()
    }

    slices = {
        name: Slice(
            name=name,
            start=str(spec["start"]),
            end=str(spec["end"]),
            sealed=spec["status"] == "sealed",
            unseal_phase=spec.get("unseal_phase"),
        )
        for name, spec in raw["slices"].items()
    }

    instruments: dict[str, Instrument] = {}
    for spec in raw["instruments"]:
        root = spec["root"]
        cells = {
            window: Cell(
                root=root,
                window=window,
                retained=bool(cell["retained"]),
                spread_floor_bp=cell["spread_floor_bp"],
                median_volume_per_minute=cell["median_volume_per_minute"],
                share_thin_bars=cell["share_thin_bars"],
                median_abs_15min_move_bp=cell["median_abs_15min_move_bp"],
                round_trip_over_move=cell["round_trip_over_move"],
            )
            for window, cell in (spec.get("cells") or {}).items()
        }
        instruments[root] = Instrument(
            root=root,
            name=spec["name"],
            symbol=spec["symbol"],
            asset_class=spec["asset_class"],
            file=spec["file"],
            exchange=spec["exchange"],
            clock=spec["clock"],
            in_universe=bool(spec["in_universe"]),
            start=spec["history"]["start"],
            end=spec["history"]["end"],
            bars=int(spec["history"]["bars"]),
            years=float(spec["history"]["years"]),
            tick=spec["tick"],
            multiplier=spec["multiplier"],
            fee_per_contract_usd=spec["fee_per_contract_usd"],
            roll_rule=spec["roll"]["rule"],
            roll_cycle=spec["roll"]["cycle"],
            splice_minute_utc=spec["roll"]["splice_minute_utc"],
            roll_dates=spec["roll"]["authoritative_dates"],
            cells=cells,
        )

    return Catalogue(
        path=path,
        timezone=raw["grid"]["timezone"],
        session_shift_hours=int(raw["session_date"]["anchor_shift_hours"]),
        windows=windows,
        slices=slices,
        instruments=instruments,
    )
