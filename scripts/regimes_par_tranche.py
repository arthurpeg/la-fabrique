"""A4 -- Volatility and trend, year by year and slice by slice.

The point is not to characterise the market. It is to document, before anything
is fitted, how different the research / validation / holdout slices are from one
another -- so that a disappointing holdout in phase 15 can be read for what it
is, instead of being discovered then.

    python scripts/regimes_par_tranche.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from _common import load, series_index, session_date, write_json

# Proposed slices, to be confirmed or corrected by DECISION-01. Measuring them
# is not adopting them.
SLICES = {
    "research": ("2016-01-03", "2021-12-31"),
    "validation": ("2022-01-01", "2023-12-31"),
    "holdout": ("2024-01-01", "2026-08-28"),
}
TRADING_DAYS = 252


def daily_returns() -> pd.DataFrame:
    columns = {}
    for entry in series_index():
        frame = load(entry, columns=["close"])
        sessions = session_date(frame.index)
        closes = frame["close"].groupby(sessions.to_numpy()).last()
        closes.index = pd.to_datetime(closes.index)
        columns[entry["racine"]] = np.log(closes).diff()
        print(f"  {entry['racine']:5s} aggregated", flush=True)
    return pd.DataFrame(columns).sort_index()


def statistics(returns: pd.Series) -> dict:
    returns = returns.dropna()
    if len(returns) < 20:
        return {"sessions": int(len(returns))}
    equity = returns.cumsum()
    drawdown = float((equity - equity.cummax()).min())
    volatility = float(returns.std(ddof=1) * np.sqrt(TRADING_DAYS))
    drift = float(returns.mean() * TRADING_DAYS)
    return {
        "sessions": int(len(returns)),
        "vol_annualised_pct": round(100 * volatility, 1),
        "drift_annualised_pct": round(100 * drift, 1),
        "sharpe_naive": round(drift / volatility, 2) if volatility else None,
        "max_drawdown_pct": round(100 * drawdown, 1),
        "worst_day_pct": round(100 * float(returns.min()), 1),
        "best_day_pct": round(100 * float(returns.max()), 1),
        "kurtosis": round(float(returns.kurtosis()), 1),
        "share_days_over_2sd": round(
            float((returns.abs() > 2 * returns.std(ddof=1)).mean()), 3
        ),
    }


def main() -> None:
    print("aggregating one-minute bars into session returns")
    returns = daily_returns()

    per_year = {}
    for root in returns.columns:
        series = returns[root].dropna()
        per_year[root] = {
            str(year): statistics(group) for year, group in series.groupby(series.index.year)
        }

    per_slice = {}
    for name, (start, end) in SLICES.items():
        window = returns.loc[start:end]
        per_slice[name] = {
            "period": [start, end],
            "years": round(len(window) / TRADING_DAYS, 2),
            "instruments": {root: statistics(window[root]) for root in window.columns},
        }

    print("\n=== A4 -- annualised volatility, % per year ===")
    vol_table = pd.DataFrame(
        {
            root: {year: stats.get("vol_annualised_pct") for year, stats in years.items()}
            for root, years in per_year.items()
        }
    )
    print(vol_table.to_string())

    print("\n=== A4 -- annualised drift, % per year ===")
    drift_table = pd.DataFrame(
        {
            root: {year: stats.get("drift_annualised_pct") for year, stats in years.items()}
            for root, years in per_year.items()
        }
    )
    print(drift_table.to_string())

    print("\n=== A4 -- proposed slices ===")
    rows = []
    for name, block in per_slice.items():
        for root, stats in block["instruments"].items():
            if stats.get("vol_annualised_pct") is None:
                continue
            rows.append(
                {
                    "slice": name,
                    "root": root,
                    "sessions": stats["sessions"],
                    "vol%": stats["vol_annualised_pct"],
                    "drift%": stats["drift_annualised_pct"],
                    "maxDD%": stats["max_drawdown_pct"],
                    "kurt": stats["kurtosis"],
                }
            )
    slice_table = pd.DataFrame(rows)
    print(slice_table.pivot(index="root", columns="slice", values="vol%").to_string())
    print("\ndrift, % annualised")
    print(slice_table.pivot(index="root", columns="slice", values="drift%").to_string())

    summary = {
        name: {
            "period": block["period"],
            "median_vol_pct": round(
                float(
                    np.nanmedian(
                        [
                            stats.get("vol_annualised_pct", np.nan)
                            for stats in block["instruments"].values()
                        ]
                    )
                ),
                1,
            ),
            "sessions": max(
                (stats.get("sessions", 0) for stats in block["instruments"].values()), default=0
            ),
        }
        for name, block in per_slice.items()
    }
    print("\nmedian annualised volatility across instruments, by slice")
    for name, block in summary.items():
        print(f"  {name:11s} {block['period'][0]} -> {block['period'][1]}  "
              f"{block['sessions']:5d} sessions  median vol {block['median_vol_pct']}%")

    path = write_json(
        "a4_regimes.json", {"per_year": per_year, "per_slice": per_slice, "summary": summary}
    )
    print(f"\nwritten: {path}")


if __name__ == "__main__":
    main()
