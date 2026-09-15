"""A1 -- Measure every parquet file and confront the measurements with the manifest.

The manifest and the README are a third party's declarations about their own
work: they say what to check, never what is true here. Every divergence is
printed, none is silently arbitrated.

    python scripts/inventory_data.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from _common import load, series_index, session_date, write_json

PRICE_COLUMNS = ["open", "high", "low", "close"]


def measure(entry: dict) -> dict:
    frame = load(entry)
    index = frame.index
    if index.tz is None:
        raise SystemExit(f"{entry['racine']}: index carries no timezone")

    deltas = index.to_series().diff().dropna()
    delta_minutes = deltas.dt.total_seconds() / 60.0
    sessions = session_date(index)
    per_session = sessions.groupby(sessions).size()

    non_positive = {
        column: int((frame[column] <= 0).sum())
        for column in PRICE_COLUMNS
        if column in frame.columns
    }
    inconsistent_ohlc = 0
    if set(PRICE_COLUMNS).issubset(frame.columns):
        high_ok = (frame["high"] >= frame[["open", "close", "low"]].max(axis=1)).to_numpy()
        low_ok = (frame["low"] <= frame[["open", "close", "high"]].min(axis=1)).to_numpy()
        inconsistent_ohlc = int((~(high_ok & low_ok)).sum())

    measured = {
        "root": entry["racine"],
        "file": entry["fichier"],
        "index_name": index.name,
        "index_tz": str(index.tz),
        "columns": {column: str(dtype) for column, dtype in frame.dtypes.items()},
        "bars": int(len(frame)),
        "start": index.min(),
        "end": index.max(),
        "years": round((index.max() - index.min()).total_seconds() / (365.25 * 86400), 2),
        "median_delta_minutes": float(np.median(delta_minutes)),
        "delta_minutes_quantiles": {
            q: float(delta_minutes.quantile(q)) for q in (0.5, 0.9, 0.99, 0.999)
        },
        "share_delta_eq_1min": float((delta_minutes == 1).mean()),
        "gaps_over_3_days": int((delta_minutes > 3 * 24 * 60).sum()),
        "largest_gap_days": float(delta_minutes.max() / (24 * 60)),
        "duplicated_timestamps": int(index.duplicated().sum()),
        "monotonic_index": bool(index.is_monotonic_increasing),
        "nan_cells": {c: int(frame[c].isna().sum()) for c in frame.columns},
        "non_positive_prices": non_positive,
        "inconsistent_ohlc_bars": inconsistent_ohlc,
        "zero_volume_share": float((frame["volume"] <= 0).mean())
        if "volume" in frame.columns
        else None,
        "median_volume": float(frame["volume"].median()) if "volume" in frame.columns else None,
        "sessions": int(per_session.size),
        "bars_per_session_median": float(per_session.median()),
        "bars_per_session_p05": float(per_session.quantile(0.05)),
        "bars_per_session_p95": float(per_session.quantile(0.95)),
        "bars_per_session_max": int(per_session.max()),
    }
    return measured


def divergences(entry: dict, measured: dict) -> list[str]:
    found: list[str] = []

    def compare(label, declared, observed, tolerance=0):
        if declared is None:
            return
        if abs(float(observed) - float(declared)) > tolerance:
            found.append(f"{label}: manifest {declared} vs measured {observed}")

    compare("bars", entry.get("barres"), measured["bars"])
    compare("median_volume", entry.get("volume_median"), measured["median_volume"])
    compare("years", entry.get("annees"), measured["years"], tolerance=0.02)
    compare("gaps_over_3_days", entry.get("trous_sup_3j"), measured["gaps_over_3_days"])
    compare(
        "zero_volume_share_pct",
        entry.get("pct_barres_volume_nul"),
        measured["zero_volume_share"] * 100.0,
        tolerance=0.005,
    )
    if str(measured["start"])[:10] != entry.get("debut"):
        found.append(f"start: manifest {entry.get('debut')} vs measured {measured['start']}")
    if str(measured["end"])[:10] != entry.get("fin"):
        found.append(f"end: manifest {entry.get('fin')} vs measured {measured['end']}")
    declared_columns = entry.get("colonnes") or []
    if list(measured["columns"]) != list(declared_columns):
        found.append(f"columns: manifest {declared_columns} vs measured {list(measured['columns'])}")
    if entry.get("fuseau", "").upper() != str(measured["index_tz"]).upper():
        found.append(f"timezone: manifest {entry.get('fuseau')} vs measured {measured['index_tz']}")
    return found


def main() -> None:
    rows, report = [], {}
    for entry in series_index():
        measured = measure(entry)
        gaps = divergences(entry, measured)
        measured["divergences_vs_manifest"] = gaps
        report[entry["racine"]] = measured
        rows.append(
            {
                "root": measured["root"],
                "bars": measured["bars"],
                "start": str(measured["start"])[:16],
                "end": str(measured["end"])[:16],
                "years": measured["years"],
                "sessions": measured["sessions"],
                "bars/sess": round(measured["bars_per_session_median"]),
                "1min%": round(100 * measured["share_delta_eq_1min"], 1),
                "vol=0%": round(100 * (measured["zero_volume_share"] or 0), 3),
                "dupes": measured["duplicated_timestamps"],
                "bad_ohlc": measured["inconsistent_ohlc_bars"],
                "diverge": len(gaps),
            }
        )
        print(f"  {measured['root']:5s} done", flush=True)

    table = pd.DataFrame(rows).set_index("root")
    print("\n=== A1 -- measured inventory ===")
    print(table.to_string())

    print("\n=== divergences vs manifest ===")
    any_gap = False
    for root, measured in report.items():
        for line in measured["divergences_vs_manifest"]:
            any_gap = True
            print(f"  {root:5s} {line}")
    if not any_gap:
        print("  none")

    path = write_json("a1_inventory.json", report)
    print(f"\nwritten: {path.relative_to(path.parents[2])}")


if __name__ == "__main__":
    main()
