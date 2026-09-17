"""Compare the authoritative roll dates with the empirical detection of phase 01.

D01 6 requires this comparison BEFORE the vendor list is adopted: the gap is the
only measurement of what the detector was worth, and it is the one occasion to
take it. Once the list is in the catalogue the question can no longer be asked.

The detector looked for isolated level shifts at the splice minute
(scripts/roll_diagnostics.py). It found a roll where there was one, missed some,
and may have flagged some that were not rolls. All three are counted here.

    python scripts/compare_rolls.py [--tolerance-days 0]

Nothing is written. This prints a measurement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from panel.catalogue import load_catalogue  # noqa: E402

DIAGNOSTICS = REPO / "scripts" / "out" / "a2_roll_diagnostics.json"


def detected_dates(payload: dict) -> list:
    """The dates the phase-01 detector dated, whatever its confidence."""
    return sorted({pd.Timestamp(row["ts_utc"]).date() for row in payload.get("rolls", [])})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tolerance-days", type=int, default=0)
    arguments = parser.parse_args()

    catalogue = load_catalogue()
    diagnostics = json.loads(DIAGNOSTICS.read_text(encoding="utf-8"))
    tolerance = pd.Timedelta(days=arguments.tolerance_days)

    print(f"tolérance {arguments.tolerance_days} jour(s)\n")
    columns = ("vendeur", "détecté", "trouvés", "manqués", "en trop")
    header = f"{'':5s}" + "".join(f"{name:>9s}" for name in columns)
    print(header)
    print("-" * len(header))

    totals = {"authoritative": 0, "detected": 0, "hit": 0, "missed": 0, "spurious": 0}
    per_root: dict[str, dict] = {}

    for root, instrument in catalogue.instruments.items():
        payload = diagnostics.get(root)
        if payload is None or instrument.roll_dates is None:
            continue
        authoritative = sorted({pd.Timestamp(value).date() for value in instrument.roll_dates})
        detected = detected_dates(payload)

        hit = [
            date
            for date in authoritative
            if any(abs(pd.Timestamp(date) - pd.Timestamp(other)) <= tolerance for other in detected)
        ]
        spurious = [
            date
            for date in detected
            if not any(
                abs(pd.Timestamp(date) - pd.Timestamp(other)) <= tolerance
                for other in authoritative
            )
        ]
        missed = [date for date in authoritative if date not in hit]

        per_root[root] = {
            "authoritative": len(authoritative),
            "detected": len(detected),
            "hit": len(hit),
            "missed": missed,
            "spurious": spurious,
        }
        for key, value in (
            ("authoritative", len(authoritative)),
            ("detected", len(detected)),
            ("hit", len(hit)),
            ("missed", len(missed)),
            ("spurious", len(spurious)),
        ):
            totals[key] += value
        counts = (len(authoritative), len(detected), len(hit), len(missed), len(spurious))
        print(f"{root:5s}" + "".join(f"{value:9d}" for value in counts))

    print("-" * len(header))
    print(
        f"{'tous':5s}"
        + "".join(f"{totals[key]:9d}" for key in ("authoritative", "detected", "hit",
                                                  "missed", "spurious"))
    )
    recall = totals["hit"] / totals["authoritative"] if totals["authoritative"] else 0.0
    print(f"\nrappel du détecteur : {recall:.1%} des roulements réels")

    worst = sorted(per_root.items(), key=lambda item: -len(item[1]["missed"]))[:3]
    print("\nles trois pires racines, et les années où ça manque :")
    for root, stats in worst:
        years = pd.Series([date.year for date in stats["missed"]]).value_counts().sort_index()
        spread = ", ".join(f"{year}:{count}" for year, count in years.items()) or "aucun"
        print(f"  {root:5s} {len(stats['missed']):3d} manqués — {spread}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
