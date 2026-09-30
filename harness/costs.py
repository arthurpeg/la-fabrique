"""The round-trip cost: a floor, two fee bounds, a slippage grid, and its holes named.

D01 7 gives the shape and forbids the shortcut:

    round_trip_cost_bp(cell) = spread_floor_bp(cell)     measured
                             + fee_bp(instrument, size)   two bounds (D26, D35),
                                                          on the EXECUTED contract (D37)
                             + slippage_bp(cell)          declared, a grid (D35)

**The floor** is measured, not declared: the smallest non-zero price change
over eleven years gives each contract its tick, and no market is tighter than a
tick (L04). The catalogue holds it per cell.

**The fees** come in two bounds, per contract and per side, as D26 framed them:
the LOW bound is the broker's schedule alone (as if it were all-in), the HIGH
bound adds the exchange and the regulatory fees on top (as if nothing were
included). Each component is an external value with its own provenance in the
catalogue (D09); the sum is computed here and never deposited, because a sum is
nobody's quotation. A component still `null` leaves its bound unpriced, and
the bound is NAMED as missing -- never treated as zero.

**The slippage** is not a measurement and not a single guess: it is declared as
a GRID of 1 to 5 ticks per side (`SLIPPAGE_TICKS`, D35), so that a reader sees
how the cost moves with it instead of trusting one number. It is on top of the
floor: the floor pays for crossing the spread, the slippage for the ticks the
fill moves beyond it, on both sides of the round trip.

Everything is converted to basis points at the cell's MEDIAN RAW PRICE over the
evaluated sample -- the same reference `scripts/session_grid.py` used for the
floor -- so the three terms add up in one unit. Treating an unknown as zero
would produce a net figure that is wrong in the flattering direction, and a
flattering number that has circulated cannot be recalled.
"""

from __future__ import annotations

from dataclasses import dataclass

from panel.catalogue import Catalogue

# D35. Ticks of slippage PER SIDE. A grid, not a choice: the report shows all
# five, and nothing in the harness picks one.
SLIPPAGE_TICKS = (1, 2, 3, 4, 5)
BOUNDS = ("low", "high")


def _round_trip_bp(per_side: float, price: float) -> float:
    """Two sides, in basis points of the price."""
    return 2.0 * per_side / price * 1e4


@dataclass(frozen=True)
class CellCost:
    root: str
    window: str
    floor_bp: float
    # The reference price the bp are taken at, and one tick in bp of it.
    median_price: float | None
    tick_bp: float | None
    # Round-trip fees in bp, per bound; None when a component is still null.
    fee_low_bp: float | None
    fee_high_bp: float | None
    unknown: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not self.unknown

    def fee_bp(self, bound: str) -> float | None:
        return self.fee_low_bp if bound == "low" else self.fee_high_bp

    def slippage_bp(self, ticks: int) -> float | None:
        return None if self.tick_bp is None else 2.0 * ticks * self.tick_bp

    def round_trip_bp(self, ticks: int, bound: str) -> float:
        """Floor + slippage + fee. A missing fee is left OUT and named in `unknown`:
        the figure is then a floor, never a completed cost."""
        total = self.floor_bp + (self.slippage_bp(ticks) or 0.0)
        fee = self.fee_bp(bound)
        return total + (fee or 0.0)


def cell_cost(catalogue: Catalogue, root: str, window: str,
              median_price: float | None = None) -> CellCost:
    """What a round trip in this cell costs, as far as it can be priced."""
    instrument = catalogue.instrument(root)
    cell = instrument.cell(window)
    unknown: list[str] = []

    priced = median_price is not None and median_price == median_price and median_price > 0
    # D37 : les frais se rapportent au contrat EXÉCUTÉ (micro partout où Lucid
    # en propose), pas au contrat des données. Un micro vaut un dixième du
    # plein : à frais par contrat voisins, il coûte environ trois fois plus en bp.
    fee_multiplier = instrument.fee_multiplier
    notional = (fee_multiplier * median_price
                if priced and fee_multiplier is not None else None)
    tick_bp = (instrument.tick / median_price * 1e4
               if priced and instrument.tick is not None else None)
    if tick_bp is None:
        unknown.append("slippage_bp")

    broker = instrument.fee_broker_usd
    exchange = instrument.fee_exchange_usd
    regulatory = instrument.fee_regulatory_usd
    fee_low = fee_high = None
    if priced and fee_multiplier is None:
        unknown.append("execution_multiplier")
    if notional is None or broker is None:
        unknown.append("fee_bp")
    else:
        fee_low = _round_trip_bp(broker, notional)
        if exchange is None or regulatory is None:
            unknown.append("fee_high_bp")
        else:
            fee_high = _round_trip_bp(broker + exchange + regulatory, notional)

    return CellCost(
        root=root,
        window=window,
        floor_bp=float(cell.spread_floor_bp),
        median_price=float(median_price) if priced else None,
        tick_bp=tick_bp,
        fee_low_bp=fee_low,
        fee_high_bp=fee_high,
        unknown=tuple(unknown),
    )


def costs_for(catalogue: Catalogue, cells,
              prices: dict[tuple[str, str], float] | None = None,
              ) -> dict[tuple[str, str], CellCost]:
    prices = prices or {}
    return {(root, window): cell_cost(catalogue, root, window, prices.get((root, window)))
            for root, window in cells}
