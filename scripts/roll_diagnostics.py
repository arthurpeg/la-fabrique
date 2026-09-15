"""A2 -- Are the continuous series spliced (raw) or back-adjusted? And when do they roll?

Method, in three steps.

1. A roll is an ISOLATED level shift: one large one-minute return surrounded by
   ordinary volatility. A news move is large too, but sits inside a burst of
   volatility. `ratio = |return| / local volatility` separates the two.
2. A continuous symbol switches contract at a fixed moment. So the splice minute
   is found empirically: among mid-session minutes-of-day, the one whose ratio
   distribution has by far the fattest tail. Session-boundary minutes are
   excluded -- a gap there is an overnight move, not a splice.
3. At that minute only, the detector is turned up (a much lower threshold) and
   the largest event of each quarter (or month) is kept. That dates the rolls.

Verdict: isolated jumps concentrated on one minute and on a roll cycle => the
series is RAW (spliced), and the history is stable. No such structure => the
series is probably back-adjusted, and every past price can be rewritten behind
us -- which would have to be frozen in a dated snapshot.

    python scripts/roll_diagnostics.py

Empirical detection only. The data's author can state the rule and the dates
authoritatively; when that answer arrives it supersedes this, and the gap
between the two is what measures this method.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from _common import load, series_index, write_json

LOCAL_WINDOW = 61  # minutes, centred: the neighbourhood a jump is compared with
ISOLATION = 8.0  # |return| / local vol above which a move is "isolated"
MATERIAL = 0.0025  # 25 bp: what a calendar spread is worth, at least
SENSITIVE = 6.0  # threshold used at the splice minute only
QUARTERLY_MONTHS = (3, 6, 9, 12)
TOP_N = 100


def prepare(entry: dict) -> pd.DataFrame:
    frame = load(entry, columns=["close"])
    index = frame.index
    ret = frame["close"].astype("float64").pct_change()
    # Robust local volatility, centred. The centre bar is one of 61 observations,
    # so a single huge return barely moves the median: no need to punch a hole.
    local = ret.abs().rolling(LOCAL_WINDOW, center=True, min_periods=31).median() * 1.4826
    table = pd.DataFrame(
        {
            "ret": ret,
            "ratio": (ret.abs() / local.replace(0.0, np.nan)).replace([np.inf, -np.inf], np.nan),
            "gap_minutes": index.to_series().diff().dt.total_seconds() / 60.0,
            "tod": index.strftime("%H:%M"),
        },
        index=index,
    ).dropna(subset=["ret", "ratio"])
    table["abs_ret"] = table["ret"].abs()
    return table


VENDOR_MINUTE = "00:00"  # hypothesis: the continuous symbol switches at UTC midnight


def minute_profile(table: pd.DataFrame) -> pd.DataFrame:
    grouped = table.groupby("tod")
    profile = pd.DataFrame(
        {
            "n": grouped.size(),
            "median_gap": grouped["gap_minutes"].median(),
            "p999_ratio": grouped["ratio"].quantile(0.999),
            "max_ratio": grouped["ratio"].max(),
        }
    )
    return profile[(profile["n"] > 200) & (profile["median_gap"] == 1)]


def tail_lift(table: pd.DataFrame, minute: str) -> float:
    at_minute = table[table["tod"] == minute]["ratio"]
    background = table[table["tod"] != minute]["ratio"]
    if at_minute.empty:
        return 0.0
    return float(at_minute.quantile(0.999) / max(background.quantile(0.999), 1e-9))


def splice_minute(table: pd.DataFrame) -> tuple[str, str, pd.DataFrame]:
    """Which minute-of-day carries the splice.

    Two candidates are compared: the vendor hypothesis (UTC midnight) and the
    mid-session minute whose isolation ratio has the fattest tail. The vendor
    hypothesis wins whenever it is actually supported on this instrument —
    it is one global property of the symbology, not ten independent accidents.
    """
    profile = minute_profile(table).sort_values("p999_ratio", ascending=False)
    searched = str(profile.index[0])
    flagged_at_vendor = int(
        (table[table["tod"] == VENDOR_MINUTE]["ratio"] >= SENSITIVE).sum()
    )
    if flagged_at_vendor >= 10 and tail_lift(table, VENDOR_MINUTE) >= 2.0:
        return VENDOR_MINUTE, "vendor hypothesis (00:00 UTC), supported", profile.head(5)
    return searched, "searched (00:00 UTC unsupported here)", profile.head(5)


def rolls_at(table: pd.DataFrame, minute: str) -> tuple[str, pd.DataFrame, float]:
    flagged = table[(table["tod"] == minute) & (table["ratio"] >= SENSITIVE)]
    if flagged.empty:
        return "unknown", flagged, 0.0

    quarterly_share = float(flagged.index.month.isin(QUARTERLY_MONTHS).mean())
    cycle = "quarterly" if quarterly_share >= 0.60 else "monthly"

    naive = flagged.index.tz_convert("UTC").tz_localize(None)
    period = naive.to_period("Q") if cycle == "quarterly" else naive.to_period("M")
    # One roll per period: the most isolated event of that period.
    keep = flagged.assign(period=period)
    rolls = keep.loc[keep.groupby("period")["ratio"].idxmax()].sort_index()
    return cycle, rolls, quarterly_share


def diagnose(entry: dict) -> dict:
    table = prepare(entry)
    minute, how, profile = splice_minute(table)
    cycle, rolls, quarterly_share = rolls_at(table, minute)

    isolated = table[(table["ratio"] >= ISOLATION) & (table["abs_ret"] >= MATERIAL)]
    by_size = table.nlargest(TOP_N, "abs_ret")

    roll_rows = [
        {
            "period": str(row["period"]),
            "ts_utc": str(ts),
            "ret_bp": round(float(row["ret"]) * 1e4, 1),
            "ratio": round(float(row["ratio"]), 1),
            "confident": bool(row["ratio"] >= 20.0),
        }
        for ts, row in rolls.iterrows()
    ]

    return {
        "root": entry["racine"],
        "splice_minute_utc": minute,
        "splice_minute_chosen_by": how,
        "splice_minute_evidence": profile.round(2).to_dict("index"),
        "splice_tail_lift_vs_other_minutes": round(tail_lift(table, minute), 1),
        "cycle": cycle,
        "share_of_flagged_in_MJSD": round(quarterly_share, 3),
        "rolls_detected": len(roll_rows),
        "rolls_confident": sum(1 for r in roll_rows if r["confident"]),
        "roll_median_size_bp": (
            round(float(np.median([abs(r["ret_bp"]) for r in roll_rows])), 1) if roll_rows else None
        ),
        "roll_positive_share": (
            round(float(np.mean([r["ret_bp"] > 0 for r in roll_rows])), 2) if roll_rows else None
        ),
        "rolls": roll_rows,
        "mad_sigma_bp": round(float(table["abs_ret"].median() * 1.4826) * 1e4, 2),
        "largest_abs_return_bp": round(float(table["abs_ret"].max()) * 1e4, 1),
        "isolated_material_events": int(len(isolated)),
        "top100_month_histogram": by_size.index.month.value_counts().sort_index().to_dict(),
        "top100_hour_utc_histogram": by_size.index.hour.value_counts().sort_index().to_dict(),
        "top100_share_at_session_gap": round(float((by_size["gap_minutes"] > 1).mean()), 2),
        "top25_by_size": [
            {
                "ts_utc": str(ts),
                "ret_bp": round(float(row["ret"]) * 1e4, 1),
                "ratio": round(float(row["ratio"]), 1),
                "gap_minutes": float(row["gap_minutes"]),
            }
            for ts, row in by_size.head(25).iterrows()
        ],
    }


def verdict(result: dict) -> str:
    structured = (
        result["splice_tail_lift_vs_other_minutes"] >= 2.0
        and result["rolls_confident"] >= 3
        and result["roll_median_size_bp"] is not None
    )
    return "RAW (spliced)" if structured else "inconclusive -- inspect"


def main() -> None:
    report, rows = {}, []
    for entry in series_index():
        result = diagnose(entry)
        result["verdict"] = verdict(result)
        report[result["root"]] = result
        years = max(1.0, len({r["period"][:4] for r in result["rolls"]}))
        rows.append(
            {
                "root": result["root"],
                "splice_utc": result["splice_minute_utc"],
                "tail_lift": result["splice_tail_lift_vs_other_minutes"],
                "cycle": result["cycle"],
                "%MJSD": result["share_of_flagged_in_MJSD"],
                "rolls": result["rolls_detected"],
                "confident": result["rolls_confident"],
                "/yr": round(result["rolls_detected"] / years, 1),
                "median_bp": result["roll_median_size_bp"],
                "share+": result["roll_positive_share"],
                "verdict": result["verdict"],
            }
        )
        print(f"  {result['root']:5s} {result['verdict']}", flush=True)

    print("\n=== A2 -- splice detection ===")
    print(pd.DataFrame(rows).set_index("root").to_string())
    print(
        f"\nisolation ratio = |return| / MAD over {LOCAL_WINDOW} centred minutes;"
        f" splice minute searched among mid-session minutes only;"
        f" threshold {SENSITIVE} at the splice minute, one roll kept per period."
    )

    for root, result in report.items():
        print(f"\n--- {root} -- rolls detected at {result['splice_minute_utc']} UTC ---")
        for roll in result["rolls"]:
            mark = "" if roll["confident"] else "   (weak)"
            print(f"  {roll['period']:8s} {str(roll['ts_utc'])[:16]}  "
                  f"{roll['ret_bp']:+8.1f} bp  ratio {roll['ratio']:6.1f}{mark}")

    path = write_json("a2_roll_diagnostics.json", report)
    print(f"\nwritten: {path}")


if __name__ == "__main__":
    main()
