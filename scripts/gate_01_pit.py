"""Gate 01 -- point-in-time integrity. Phase 01 does not close unless this passes.

Three checks, each answering a different way the history could betray us.

1. TRUNCATION. Pick an arbitrary past date. Answer, from the full files: which
   instruments existed that day, and what price was known for each. Answer again
   from copies truncated at that date. The two answers must be identical -- if
   they are not, the reading path consulted the future.

2. FINGERPRINT. Record a checksum of every instrument's history BEFORE the cut.
   That prefix must never change again. A back-adjusted series silently rewrites
   its own past on each regeneration; a spliced one does not. Truncation alone
   cannot see this -- it compares a file with itself -- so the fingerprint is
   what actually protects us, from the second run onwards.

3. MONOTONY. No duplicated and no out-of-order timestamps, which would make
   "the last bar known at T" ambiguous.

    python scripts/gate_01_pit.py [--asof 2021-06-15] [--rebaseline]

Exit code 1 and the offending instrument named, on any divergence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd

from _common import OUT, data_dir, series_index

# Arbitrary, fixed, inside the pool slice (2016-2023, see DECISION-01).
# Arbitrary is the point:
# nothing about this date is special, so nothing can be tuned to it.
DEFAULT_ASOF = "2021-06-15 20:00:00+00:00"
BASELINE = OUT / "pit_fingerprints.json"


def answer_from(frame: pd.DataFrame, cutoff: pd.Timestamp) -> dict:
    """What was knowable at the cutoff, and nothing else."""
    visible = frame.loc[frame.index <= cutoff]
    if visible.empty:
        return {"in_universe": False, "bars": 0, "last_ts": None, "last_close": None,
                "fingerprint": None}
    payload = b"".join(
        (
            visible.index.asi8.tobytes(),
            visible["close"].to_numpy("float64").tobytes(),
        )
    )
    return {
        "in_universe": True,
        "bars": int(len(visible)),
        "last_ts": str(visible.index[-1]),
        "last_close": float(visible["close"].iloc[-1]),
        "fingerprint": hashlib.sha256(payload).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asof", default=DEFAULT_ASOF)
    parser.add_argument(
        "--rebaseline",
        action="store_true",
        help="overwrite the stored fingerprints. Only legitimate when the data "
        "provider is knowingly replaced, and it belongs in a written decision.",
    )
    args = parser.parse_args()
    cutoff = pd.Timestamp(args.asof)
    if cutoff.tz is None:
        cutoff = cutoff.tz_localize("UTC")

    root = data_dir()
    failures: list[str] = []
    answers: dict[str, dict] = {}

    workspace = Path(tempfile.mkdtemp(prefix="gate01_"))
    try:
        for entry in series_index():
            name = entry["racine"]
            frame = pd.read_parquet(root / entry["fichier"], columns=["close"])

            if not frame.index.is_monotonic_increasing:
                failures.append(f"{name}: timestamps are not monotonically increasing")
            if bool(frame.index.duplicated().any()):
                failures.append(f"{name}: duplicated timestamps")

            full = answer_from(frame, cutoff)

            # A copy of the file holding nothing after the cutoff.
            truncated_path = workspace / f"{name}.parquet"
            frame.loc[frame.index <= cutoff].to_parquet(truncated_path)
            truncated = answer_from(pd.read_parquet(truncated_path), cutoff)

            if full != truncated:
                differing = [k for k in full if full[k] != truncated[k]]
                failures.append(
                    f"{name}: truncated copy answers differently on {differing} "
                    f"(full={ {k: full[k] for k in differing} }, "
                    f"truncated={ {k: truncated[k] for k in differing} })"
                )

            answers[name] = full
            state = "in universe" if full["in_universe"] else "NOT YET LISTED"
            close = f"{full['last_close']:.5f}" if full["last_close"] is not None else "-"
            print(f"  {name:5s} {state:14s} last known {str(full['last_ts'])[:16]:16s} "
                  f"close {close:>10s}  bars {full['bars']:>9d}")
    finally:
        shutil.rmtree(workspace, ignore_errors=True)

    stored = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else None
    if stored is None or args.rebaseline:
        OUT.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(
            json.dumps({"asof": str(cutoff), "answers": answers}, indent=1, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nbaseline {'rewritten' if args.rebaseline else 'established'}: {BASELINE}")
    elif stored["asof"] != str(cutoff):
        print(f"\nbaseline holds asof {stored['asof']}, not {cutoff}: fingerprints not compared")
    else:
        for name, recorded in stored["answers"].items():
            current = answers.get(name)
            if current is None:
                failures.append(f"{name}: present in the baseline, absent from the data")
            elif current["fingerprint"] != recorded["fingerprint"]:
                failures.append(
                    f"{name}: the history BEFORE {cutoff} has changed since the baseline "
                    f"(bars {recorded['bars']} -> {current['bars']}, "
                    f"last close {recorded['last_close']} -> {current['last_close']}). "
                    f"The series is being rewritten behind us."
                )
        for name in answers:
            if name not in stored["answers"]:
                print(f"  note: {name} is new since the baseline, nothing to compare")
        if not failures:
            print(f"\nfingerprints match the baseline of {stored['asof']}")

    print()
    if failures:
        print("GATE 01: FAILED")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("GATE 01: PASSED -- point-in-time integrity holds at " + str(cutoff))
    return 0


if __name__ == "__main__":
    sys.exit(main())
