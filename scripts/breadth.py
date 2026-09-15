"""A3 -- How many independent bets does this universe actually carry?

Nine or ten instruments are not nine or ten bets. Daily returns are aggregated
from the one-minute bars, the correlation matrix is measured, and the effective
breadth is read off its eigenvalues two ways:

  participation ratio   (sum L)^2 / sum L^2      -- how many eigenvalues matter
  entropy breadth       exp(-sum p log p)        -- same question, softer

Both are reported because they disagree on purpose: the first is dominated by
the largest factor, the second counts the long tail. The truth is between them.

    python scripts/breadth.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

from _common import load, series_index, session_date, write_json

SHORT_HISTORY_YEARS = 5.0  # below this an instrument is measured apart, never blended


def daily_closes() -> pd.DataFrame:
    columns = {}
    for entry in series_index():
        frame = load(entry, columns=["close"])
        sessions = session_date(frame.index)
        closes = frame["close"].groupby(sessions.to_numpy()).last()
        closes.index = pd.to_datetime(closes.index)
        columns[entry["racine"]] = closes
        print(f"  {entry['racine']:5s} {len(closes):5d} sessions", flush=True)
    return pd.DataFrame(columns).sort_index()


def breadth(returns: pd.DataFrame) -> dict:
    correlation = returns.corr()
    eigenvalues = np.sort(np.linalg.eigvalsh(correlation.to_numpy()))[::-1]
    weights = eigenvalues / eigenvalues.sum()
    entropy = float(-np.sum(weights * np.log(weights)))

    distance = np.clip(1.0 - correlation.to_numpy(), 0.0, 2.0)
    np.fill_diagonal(distance, 0.0)
    linkage = hierarchy.linkage(squareform(distance, checks=False), method="average")
    blocks = {}
    for threshold in (0.5, 0.7):  # cut at correlation 0.5 and 0.3
        labels = hierarchy.fcluster(linkage, t=threshold, criterion="distance")
        grouped: dict[int, list[str]] = {}
        for name, label in zip(correlation.index, labels, strict=True):
            grouped.setdefault(int(label), []).append(str(name))
        blocks[f"corr_above_{1 - threshold:.1f}"] = sorted(grouped.values(), key=len, reverse=True)

    return {
        "instruments": list(correlation.index),
        "observations": int(len(returns)),
        "period": [str(returns.index.min())[:10], str(returns.index.max())[:10]],
        "correlation": correlation.round(3).to_dict(),
        "mean_abs_correlation": round(
            float(
                np.abs(correlation.to_numpy()[np.triu_indices(len(correlation), 1)]).mean()
            ),
            3,
        ),
        "eigenvalues": [round(float(v), 3) for v in eigenvalues],
        "variance_explained_pc1": round(float(weights[0]), 3),
        "variance_explained_pc1_to_pc3": round(float(weights[:3].sum()), 3),
        "participation_ratio": round(
            float(eigenvalues.sum() ** 2 / (eigenvalues**2).sum()), 2
        ),
        "entropy_breadth": round(float(np.exp(entropy)), 2),
        "blocks": blocks,
    }


def main() -> None:
    print("aggregating one-minute bars into session closes")
    closes = daily_closes()
    returns = np.log(closes).diff()

    spans = {
        column: (closes[column].dropna().index.max() - closes[column].dropna().index.min()).days
        / 365.25
        for column in closes.columns
    }
    long_history = [c for c, years in spans.items() if years >= SHORT_HISTORY_YEARS]
    short_history = [c for c in closes.columns if c not in long_history]

    report = {
        "history_years": {k: round(v, 2) for k, v in spans.items()},
        "long_history": long_history,
        "short_history_excluded": short_history,
        "full_universe_long_history": breadth(returns[long_history].dropna()),
    }
    if short_history:
        overlap = returns.dropna()
        report["with_short_history_on_its_own_window"] = breadth(overlap)

    main_block = report["full_universe_long_history"]
    print("\n=== A3 -- correlation of daily returns ===")
    print(pd.DataFrame(main_block["correlation"]).round(2).to_string())
    print(f"\nobservations: {main_block['observations']} sessions, "
          f"{main_block['period'][0]} -> {main_block['period'][1]}")
    print(f"mean |correlation| off-diagonal : {main_block['mean_abs_correlation']}")
    print(f"variance explained by PC1       : {main_block['variance_explained_pc1']:.1%}")
    print(f"variance explained by PC1..PC3  : {main_block['variance_explained_pc1_to_pc3']:.1%}")
    print(f"participation ratio             : {main_block['participation_ratio']}")
    print(f"entropy breadth                 : {main_block['entropy_breadth']}")
    print("\nblocks:")
    for cut, groups in main_block["blocks"].items():
        print(f"  {cut}: {groups}")

    if "with_short_history_on_its_own_window" in report:
        short = report["with_short_history_on_its_own_window"]
        print(f"\n--- same measure on the window where {short_history} exists "
              f"({short['observations']} sessions) ---")
        print(f"participation ratio {short['participation_ratio']}, "
              f"entropy breadth {short['entropy_breadth']}")

    path = write_json("a3_breadth.json", report)
    print(f"\nwritten: {path}")


if __name__ == "__main__":
    main()
