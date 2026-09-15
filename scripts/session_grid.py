"""A8 -- The instrument x session grid: which cells are tradable, and at what cost.

Three windows, disjoint by construction, anchored to the EXCHANGE's local clock
rather than to UTC. Anchoring to UTC would make the windows drift by an hour
against the real sessions twice a year, on dates nobody chose; anchoring to the
local clock keeps "the London morning" the London morning all year. Disjointness
is what the UTC requirement was protecting -- and it is preserved, in the only
clock where it can be: the instrument's own.

  ASIA    19:00 -> 03:00 (next day)   Globex reopen, Tokyo morning
  EUROPE  03:00 -> 09:30              Frankfurt and London, before New York
  US      09:30 -> 16:00              the US cash session

16:00 -> 19:00 belongs to no window: settlement, the daily halt, and the thinnest
hour of the day. Nothing is traded there.

Per cell the script measures liquidity (volume, thin bars), the size of the move
worth capturing, and a spread estimate -- Corwin & Schultz (2012), a high/low
estimator, since OHLCV carries no quotes. It is an ESTIMATOR, not a measurement
of the real spread, and it is labelled as such everywhere it appears.

    python scripts/session_grid.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from _common import load, series_index, write_json

# All nine retained instruments trade on CME Globex: one clock for the grid.
# FDAX sits on EUREX and would need its own (see A6 / LECONS L02); it is out of
# the universe anyway.
GRID_TZ = "America/New_York"
EXCLUDED = ["FDAX"]
WINDOWS = {
    "ASIA": (19 * 60, 27 * 60),  # 19:00 -> 03:00 next day, in minutes from midnight
    "EUROPE": (3 * 60, 9 * 60 + 30),
    "US": (9 * 60 + 30, 16 * 60),
}
THIN_VOLUME = 10  # contracts per minute below which a bar is "thin"


def window_of(index: pd.DatetimeIndex) -> pd.Series:
    local = index.tz_convert(GRID_TZ)
    minutes = local.hour * 60 + local.minute
    labels = pd.Series("OFF", index=index, dtype="object")
    for name, (start, end) in WINDOWS.items():
        if end > 24 * 60:  # window wraps past midnight
            mask = (minutes >= start) | (minutes < end - 24 * 60)
        else:
            mask = (minutes >= start) & (minutes < end)
        labels[mask] = name
    return labels


def corwin_schultz(high: pd.Series, low: pd.Series) -> pd.Series:
    """Estimated proportional spread from two consecutive bars' high/low range.

    Corwin, S. and Schultz, P. (2012), "A Simple Way to Estimate Bid-Ask Spreads
    from Daily High and Low Prices", Journal of Finance 67(2). Applied here to
    one-minute bars. Negative estimates are set to zero, as the paper prescribes.
    """
    beta = (np.log(high / low) ** 2).rolling(2).sum()
    high2 = high.rolling(2).max()
    low2 = low.rolling(2).min()
    gamma = np.log(high2 / low2) ** 2
    denominator = 3 - 2 * np.sqrt(2)
    alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / denominator - np.sqrt(gamma / denominator)
    spread = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
    return spread.clip(lower=0.0)


def observed_tick(close: pd.Series) -> float:
    """The smallest price increment the series actually shows.

    Measured, not declared: the contract's tick size is a data value we are
    forbidden to invent, but the minimum non-zero price change over eleven years
    of one-minute bars is an observation. It is the floor of any spread -- a
    market cannot be tighter than one tick.
    """
    changes = close.diff().abs()
    positive = changes[changes > 0]
    return float(positive.min())


def measure(entry: dict) -> dict:
    frame = load(entry, columns=["open", "high", "low", "close", "volume"])
    labels = window_of(frame.index)
    returns = np.log(frame["close"]).diff()
    spread = corwin_schultz(frame["high"], frame["low"])
    move_15 = np.log(frame["close"]).diff(15).abs()  # what a 15-minute move is worth
    tick = observed_tick(frame["close"])

    cells = {}
    total_volume = float(frame["volume"].sum())
    for name in WINDOWS:
        mask = labels == name
        block = frame[mask]
        if block.empty:
            continue
        tick_bp = float(tick / block["close"].median()) * 1e4
        corwin = float(spread[mask].median()) * 1e4
        cells[name] = {
            "tick_observed": tick,
            "tick_bp": round(tick_bp, 2),
            "corwin_schultz_median_bp": round(corwin, 2),
            "corwin_schultz_zero_share": round(float((spread[mask] <= 0).mean()), 3),
            # A spread cannot be narrower than one tick; the estimator collapsing
            # to zero on one-minute bars is a limit of the estimator, not a free
            # market. The floor is what the cost model uses.
            "spread_floor_bp": round(max(corwin, tick_bp), 2),
            "zero_return_bar_share": round(float((returns[mask] == 0).mean()), 3),
            "bars": int(len(block)),
            "share_of_volume": round(float(block["volume"].sum() / total_volume), 3),
            "median_volume_per_minute": round(float(block["volume"].median()), 1),
            "p10_volume_per_minute": round(float(block["volume"].quantile(0.10)), 1),
            "share_thin_bars": round(float((block["volume"] < THIN_VOLUME).mean()), 3),
            "median_abs_1min_return_bp": round(float(returns[mask].abs().median()) * 1e4, 2),
            "median_abs_15min_move_bp": round(float(move_15[mask].median()) * 1e4, 1),
            "median_bar_range_bp": round(
                float((np.log(block["high"] / block["low"])).median()) * 1e4, 2
            ),
        }
    return {"root": entry["racine"], "tick_observed": tick, "cells": cells}


def breadth_per_window(retained: pd.DataFrame) -> dict:
    """How many independent bets each window carries, on 15-minute returns."""
    panels: dict[str, pd.DataFrame] = {}
    for entry in series_index():
        root = entry["racine"]
        if root in EXCLUDED:
            continue
        frame = load(entry, columns=["close"])
        closes = frame["close"].resample("15min", label="right", closed="right").last().dropna()
        block = pd.DataFrame({"ret": np.log(closes).diff(), "window": window_of(closes.index)})
        for name in WINDOWS:
            series = block.loc[block["window"] == name, "ret"]
            panels.setdefault(name, pd.DataFrame())[root] = series

    out = {}
    for name, panel in panels.items():
        members = retained.loc[
            (retained["window"] == name) & retained["retained"], "root"
        ].tolist()
        frame = panel[members].dropna()
        correlation = frame.corr()
        eigenvalues = np.clip(np.sort(np.linalg.eigvalsh(correlation.to_numpy()))[::-1], 1e-12, None)
        out[name] = {
            "instruments": members,
            "observations": int(len(frame)),
            "mean_abs_correlation": round(
                float(np.abs(correlation.to_numpy()[np.triu_indices(len(members), 1)]).mean()), 3
            ),
            "participation_ratio": round(
                float(eigenvalues.sum() ** 2 / (eigenvalues**2).sum()), 2
            ),
            "blocks_above_0.5": [
                sorted(group)
                for group in _blocks(correlation)
            ],
        }
    return out


def _blocks(correlation: pd.DataFrame) -> list[list[str]]:
    from scipy.cluster import hierarchy
    from scipy.spatial.distance import squareform

    distance = np.clip(1.0 - correlation.to_numpy(), 0.0, 2.0)
    np.fill_diagonal(distance, 0.0)
    labels = hierarchy.fcluster(
        hierarchy.linkage(squareform(distance, checks=False), method="average"),
        t=0.5,
        criterion="distance",
    )
    grouped: dict[int, list[str]] = {}
    for name, label in zip(correlation.index, labels, strict=True):
        grouped.setdefault(int(label), []).append(str(name))
    return sorted(grouped.values(), key=len, reverse=True)


def main() -> None:
    report = {}
    for entry in series_index():
        if entry["racine"] in EXCLUDED:
            continue
        report[entry["racine"]] = measure(entry)
        print(f"  {entry['racine']:5s} measured", flush=True)

    rows = []
    for root, block in report.items():
        for window, cell in block["cells"].items():
            # A round trip crosses the spread once in and once out: one full
            # spread. Exchange and clearing fees are NOT here -- they are a data
            # value we do not have, and inventing one is forbidden. The decision
            # records them as null with an open todo.
            round_trip = cell["spread_floor_bp"]
            rows.append(
                {
                    "root": root,
                    "window": window,
                    "vol/min": cell["median_volume_per_minute"],
                    "%volume": cell["share_of_volume"],
                    "thin%": round(100 * cell["share_thin_bars"], 1),
                    "move15_bp": cell["median_abs_15min_move_bp"],
                    "tick_bp": cell["tick_bp"],
                    "CS_bp": cell["corwin_schultz_median_bp"],
                    "spread_bp": cell["spread_floor_bp"],
                    "RT_cost_bp": round(round_trip, 2),
                    "cost/move": round(round_trip / max(cell["median_abs_15min_move_bp"], 1e-9), 2),
                }
            )
    table = pd.DataFrame(rows)

    print("\n=== A8 -- the instrument x session grid ===")
    for column in ("vol/min", "thin%", "move15_bp", "tick_bp", "CS_bp", "spread_bp", "cost/move"):
        print(f"\n{column}")
        print(table.pivot(index="root", columns="window", values=column).to_string())

    # Retention rule, stated before the numbers are read, and arbitrated by the
    # written decision -- not by this script.
    table["retained"] = (
        (table["vol/min"] >= THIN_VOLUME)
        & (table["thin%"] <= 25.0)
        & (table["cost/move"] <= 0.33)
    )
    print("\nretention rule: median volume >= 10 contracts/min, thin bars <= 25%, "
          "estimated round trip <= 1/3 of the median 15-minute move")
    print(table.pivot(index="root", columns="window", values="retained").to_string())
    print(f"\ncells retained: {int(table['retained'].sum())} / {len(table)}")

    print("\n  measuring breadth inside each window", flush=True)
    windows_breadth = breadth_per_window(table)
    print("\n=== A8 -- independent bets per window (15-minute returns) ===")
    total = 0.0
    for name, block in windows_breadth.items():
        total += block["participation_ratio"]
        print(f"  {name:7s} {len(block['instruments'])} instruments, "
              f"{block['observations']:6d} obs, mean|corr| {block['mean_abs_correlation']:.3f}, "
              f"participation {block['participation_ratio']:.2f}")
        print(f"          blocks: {block['blocks_above_0.5']}")
    print(f"\n  sum across the three windows: {total:.2f} bets per day")
    print("  (sum assumes the windows are independent of one another -- they are")
    print("   disjoint in time, but a trend can obviously run across all three)")

    write_json(
        "a8_session_grid.json",
        {
            "breadth_per_window": windows_breadth,
            "windows_local": {k: [v[0] / 60, v[1] / 60] for k, v in WINDOWS.items()},
            "grid_timezone": GRID_TZ,
            "thin_volume_threshold": THIN_VOLUME,
            "spread_estimator": "Corwin & Schultz (2012), high/low, on 1-minute bars",
            "per_instrument": report,
            "cells": table.to_dict("records"),
        },
    )
    print("\nwritten: scripts/out/a8_session_grid.json")


if __name__ == "__main__":
    main()
