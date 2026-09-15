"""A5 -- Effective breadth at intraday frequencies, and day by day.

Two questions the daily correlation matrix cannot answer.

1. Correlations usually fall as the sampling frequency rises. The breadth that
   matters for an intraday strategy is the one measured at 15 and 30 minutes,
   not at the session close.
2. An average breadth hides the days when it collapses. On a FOMC or payrolls
   day every instrument obeys the same impulse: nine instruments, one bet. That
   shows up as a fat tail in a PnL and never in an average IC. So breadth is
   also measured session by session, from the intraday cross-section.

    python scripts/breadth_intraday.py

FDAX is left out: 1.46 years against 10.65 cannot share a correlation matrix
with the rest (see LECONS L02).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from _common import load, series_index, session_date, write_json

FREQUENCIES = ["15min", "30min", "60min"]
EXCLUDED = ["FDAX"]
MIN_OBS_PER_SESSION = 24  # a session with fewer intraday returns says nothing


def panel(freq: str) -> pd.DataFrame:
    columns = {}
    for entry in series_index():
        if entry["racine"] in EXCLUDED:
            continue
        frame = load(entry, columns=["close"])
        closes = frame["close"].resample(freq, label="right", closed="right").last().dropna()
        columns[entry["racine"]] = np.log(closes).diff()
    return pd.DataFrame(columns).dropna(how="all")


def breadth(correlation: pd.DataFrame) -> dict:
    matrix = correlation.to_numpy()
    eigenvalues = np.sort(np.linalg.eigvalsh(matrix))[::-1]
    eigenvalues = np.clip(eigenvalues, 1e-12, None)
    weights = eigenvalues / eigenvalues.sum()
    return {
        "participation_ratio": float(eigenvalues.sum() ** 2 / (eigenvalues**2).sum()),
        "entropy_breadth": float(np.exp(-np.sum(weights * np.log(weights)))),
        "variance_explained_pc1": float(weights[0]),
        "mean_abs_correlation": float(
            np.abs(matrix[np.triu_indices(len(matrix), 1)]).mean()
        ),
    }


def main() -> None:
    report = {}
    rows = []

    for freq in FREQUENCIES:
        print(f"  building the {freq} panel", flush=True)
        returns = panel(freq).dropna()
        correlation = returns.corr()
        measured = breadth(correlation)
        measured["observations"] = int(len(returns))
        measured["correlation"] = correlation.round(3).to_dict()
        report[freq] = measured
        rows.append(
            {
                "freq": freq,
                "obs": measured["observations"],
                "mean|corr|": round(measured["mean_abs_correlation"], 3),
                "PC1%": round(100 * measured["variance_explained_pc1"], 1),
                "participation": round(measured["participation_ratio"], 2),
                "entropy": round(measured["entropy_breadth"], 2),
            }
        )

    print("\n=== A5 -- breadth against sampling frequency ===")
    print(pd.DataFrame(rows).set_index("freq").to_string())
    print("(daily, from A3: participation 4.03, entropy 5.28, PC1 39.6%)")

    # --- realised breadth, session by session, from the 15-minute cross-section
    print("\n  measuring session-by-session breadth", flush=True)
    returns = panel("15min").dropna()
    sessions = session_date(returns.index)
    daily = []
    for day, group in returns.groupby(sessions.to_numpy()):
        if len(group) < MIN_OBS_PER_SESSION:
            continue
        correlation = group.corr()
        if correlation.isna().to_numpy().any():
            continue
        measured = breadth(correlation)
        daily.append(
            {
                "session": str(day),
                "obs": int(len(group)),
                "participation_ratio": round(measured["participation_ratio"], 3),
                "variance_explained_pc1": round(measured["variance_explained_pc1"], 3),
                "abs_move_bp": round(float(group.sum().abs().mean()) * 1e4, 1),
            }
        )

    frame = pd.DataFrame(daily).set_index("session")
    quantiles = frame["participation_ratio"].quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95])
    worst = frame.nsmallest(15, "participation_ratio")

    print("\n=== A5 -- realised breadth, session by session (15-minute cross-section) ===")
    print(f"sessions measured: {len(frame)}")
    print("participation ratio, distribution across sessions:")
    for q, value in quantiles.items():
        print(f"  p{int(q * 100):02d}  {value:.2f}")
    print(f"  mean {frame['participation_ratio'].mean():.2f}")
    print(f"\nshare of sessions below 3 bets : "
          f"{(frame['participation_ratio'] < 3).mean():.1%}")
    print(f"share of sessions below 2 bets : "
          f"{(frame['participation_ratio'] < 2).mean():.1%}")
    print("\nthe 15 narrowest sessions (one impulse, nine instruments):")
    print(worst.to_string())

    report["per_session"] = {
        "sessions": int(len(frame)),
        "quantiles": {f"p{int(q * 100):02d}": round(float(v), 3) for q, v in quantiles.items()},
        "mean": round(float(frame["participation_ratio"].mean()), 3),
        "share_below_3": round(float((frame["participation_ratio"] < 3).mean()), 4),
        "share_below_2": round(float((frame["participation_ratio"] < 2).mean()), 4),
        "narrowest_sessions": worst.reset_index().to_dict("records"),
        "yearly_mean": {
            str(year): round(float(value), 3)
            for year, value in frame["participation_ratio"]
            .groupby(pd.to_datetime(frame.index).year)
            .mean()
            .items()
        },
    }
    print("\nmean realised breadth per year:")
    for year, value in report["per_session"]["yearly_mean"].items():
        print(f"  {year}  {value:.2f}")

    path = write_json("a5_breadth_intraday.json", report)
    print(f"\nwritten: {path}")


if __name__ == "__main__":
    main()
