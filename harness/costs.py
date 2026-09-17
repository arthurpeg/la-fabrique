"""The round-trip cost, as a floor that says what it is missing.

D01 7 gives the shape and forbids the shortcut:

    round_trip_cost_bp(cell) = spread_floor_bp(cell)     measured
                             + fee_bp(instrument, size)   null -- todo
                             + slippage_bp(cell)          declared, pessimistic

Two of the three are unknown today. Treating an unknown as zero would produce a
net IC that is wrong in the flattering direction, and a flattering number that
has circulated cannot be recalled. So the harness returns a FLOOR and names every
component it could not price. A cost with a hole is not an unknown cost: it is a
lower bound, useful exactly as long as it is labelled as one.

The floor itself is measured, not declared: the smallest non-zero price change
over eleven years gives each contract its tick, and no market is tighter than a
tick (L04). The catalogue holds it per cell.
"""

from __future__ import annotations

from dataclasses import dataclass

from panel.catalogue import Catalogue


@dataclass(frozen=True)
class CellCost:
    root: str
    window: str
    floor_bp: float
    unknown: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not self.unknown


def cell_cost(catalogue: Catalogue, root: str, window: str) -> CellCost:
    """What a round trip in this cell costs, at least."""
    instrument = catalogue.instrument(root)
    cell = instrument.cell(window)

    unknown: list[str] = []
    if instrument.fee_per_contract_usd is None:
        unknown.append("fee_bp")
    # slippage_bp is a declared, pessimistic assumption that D04 leaves open until
    # the first real signal. Until it is written down it is missing, not zero.
    unknown.append("slippage_bp")

    return CellCost(
        root=root,
        window=window,
        floor_bp=float(cell.spread_floor_bp),
        unknown=tuple(unknown),
    )


def costs_for(catalogue: Catalogue, cells) -> dict[tuple[str, str], CellCost]:
    return {(root, window): cell_cost(catalogue, root, window) for root, window in cells}
