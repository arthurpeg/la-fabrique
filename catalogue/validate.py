"""The guard of the catalogue. It re-derives every number the catalogue copies.

A catalogue is a declaration, and a declaration drifts: a measurement is redone,
a file is replaced, a null is quietly filled with something plausible. So every
figure written in catalogue.yaml is checked here against the source it came
from, and every null is checked against the todo that owes it a value.

    python catalogue/validate.py

Exit code 1 and the divergence named, on any disagreement.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from panel.catalogue import load_catalogue  # noqa: E402
from panel.paths import CATALOGUE, data_dir  # noqa: E402

INVENTORY = REPO / "scripts" / "out" / "a1_inventory.json"
GRID = REPO / "scripts" / "out" / "a8_session_grid.json"

# What phase 01 measured, and what the catalogue is allowed to copy from it.
CELL_FIELDS = {
    "spread_floor_bp": "spread_bp",
    "median_volume_per_minute": "vol/min",
    "median_abs_15min_move_bp": "move15_bp",
    "round_trip_over_move": "cost/move",
}


def main() -> int:
    raw = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))
    catalogue = load_catalogue()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    grid = json.loads(GRID.read_text(encoding="utf-8"))
    cells = {(c["root"], c["window"]): c for c in grid["cells"]}
    root_dir = data_dir()

    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    # 1. Shape.
    check(raw.get("schema_version") == 1, f"schema_version is {raw.get('schema_version')}, not 1")
    for key in ("data", "grid", "session_date", "slices", "retention_rule", "instruments", "todos"):
        check(key in raw, f"missing top-level key {key!r}")

    # 2. The grid: three disjoint windows, as measured in phase 01.
    measured_windows = grid["windows_local"]
    check(
        catalogue.timezone == grid["grid_timezone"],
        f"grid timezone {catalogue.timezone} != measured {grid['grid_timezone']}",
    )
    for name, window in catalogue.windows.items():
        start, end = measured_windows[name]
        end = end - 24 if end > 24 else end
        check(
            window.start_hour == start and window.end_hour == end,
            f"window {name}: catalogue [{window.start_hour}, {window.end_hour}) "
            f"!= measured [{start}, {end})",
        )
    hours = sorted(
        (w.start_hour, w.end_hour, w.crosses_midnight) for w in catalogue.windows.values()
    )
    covered = sum((24 - s + e) if crosses else (e - s) for s, e, crosses in hours)
    check(covered == 21.0, f"the three windows cover {covered} h, expected 21 h of 24")

    # 3. The slices: two, contiguous, the second sealed.
    pool, holdout = catalogue.slice("pool"), catalogue.slice("holdout")
    check(not pool.sealed, "the pool slice is marked sealed")
    check(holdout.sealed, "the holdout slice is NOT marked sealed")
    check(
        str(pd_next_day(pool.end)) == holdout.start,
        f"slices are not contiguous: pool ends {pool.end}, holdout starts {holdout.start}",
    )

    # 4. Every instrument: the file exists, and the history is the measured one.
    for root, instrument in catalogue.instruments.items():
        path = root_dir / instrument.file
        check(path.exists(), f"{root}: {instrument.file} not found under {root_dir}")

        measured = inventory.get(root)
        if measured is None:
            failures.append(f"{root}: absent from {INVENTORY.name}")
            continue
        for field, value, expected in (
            ("history.start", instrument.start, measured["start"]),
            ("history.end", instrument.end, measured["end"]),
            ("history.bars", instrument.bars, measured["bars"]),
            ("history.years", instrument.years, measured["years"]),
        ):
            check(value == expected, f"{root}: {field} is {value!r}, measured {expected!r}")

        per_instrument = grid["per_instrument"].get(root)
        if per_instrument is None:
            check(
                instrument.tick is None and not instrument.cells,
                f"{root}: has a tick or cells but was never measured on the grid",
            )
            continue
        # The measured tick carries float-subtraction noise (1860.3 - 1860.2 is
        # 0.09999999999945), so the catalogue holds the round value D01 7 declares
        # and the comparison is relative, never exact.
        measured_tick = per_instrument["tick_observed"]
        check(
            abs(instrument.tick - measured_tick) <= 1e-6 * measured_tick,
            f"{root}: tick is {instrument.tick}, measured {measured_tick}",
        )

        # 5. Each cell: the copied numbers, and the retention rule applied to them.
        rule = raw["retention_rule"]
        for window, cell in instrument.cells.items():
            source = cells[(root, window)]
            for field, key in CELL_FIELDS.items():
                value = getattr(cell, field)
                check(
                    value == source[key],
                    f"{root} x {window}: {field} is {value}, measured {source[key]}",
                )
            check(
                cell.share_thin_bars == round(source["thin%"] / 100, 4),
                f"{root} x {window}: share_thin_bars is {cell.share_thin_bars}, "
                f"measured {round(source['thin%'] / 100, 4)}",
            )
            passes = (
                cell.median_volume_per_minute >= rule["median_volume_per_minute_min"]
                and cell.share_thin_bars <= rule["share_thin_bars_max"]
                and cell.round_trip_over_move <= rule["round_trip_over_move15_max"]
            )
            check(
                cell.retained == passes,
                f"{root} x {window}: retained={cell.retained} but the retention rule says "
                f"{passes} (volume {cell.median_volume_per_minute}, thin "
                f"{cell.share_thin_bars}, cost/move {cell.round_trip_over_move})",
            )
            check(
                cell.retained == bool(source["retained"]),
                f"{root} x {window}: retained={cell.retained}, measured "
                f"{bool(source['retained'])}",
            )

    retained = len(catalogue.retained_cells())
    check(retained == 25, f"{retained} retained cells, expected 25 (D01 3)")

    # 5b. The roll dates: received from the vendor, so checked like any other claim.
    rolls_file = REPO / "catalogue" / "roll_dates.json"
    check(rolls_file.exists(), "roll_dates.json is missing but the catalogue points at it")
    if rolls_file.exists():
        rolls = json.loads(rolls_file.read_text(encoding="utf-8"))
        # A rate far from the declared cycle means one of the two is wrong. It caught
        # GC, declared monthly by D01 6 and rolling 5.07 times a year (L07).
        bounds = {"quarterly": (3.5, 4.5), "monthly": (11.0, 13.0)}
        for root, instrument in catalogue.instruments.items():
            if instrument.roll_dates is None:
                continue
            check(
                root in rolls["dates"],
                f"{root}: points at roll_dates.json, which does not hold it",
            )
            dates = [pd_date(value) for value in instrument.roll_dates]
            check(dates == sorted(set(dates)), f"{root}: roll dates are unsorted or duplicated")
            start, end = pd_date(instrument.start[:10]), pd_date(instrument.end[:10])
            outside = [str(d) for d in dates if not start <= d <= end]
            check(not outside, f"{root}: roll dates outside the history: {outside[:3]}")
            check(
                rolls["splice_minute_utc"] == instrument.splice_minute_utc,
                f"{root}: splice minute {instrument.splice_minute_utc} != "
                f"{rolls['splice_minute_utc']} in roll_dates.json",
            )
            window = bounds.get(instrument.roll_cycle)
            if window is not None:
                rate = len(dates) / instrument.years
                check(
                    window[0] <= rate <= window[1],
                    f"{root}: {rate:.2f} rolls a year, outside {window} for a "
                    f"{instrument.roll_cycle} cycle",
                )

    # 6. Every null is owed by a todo, and every todo owes a real null.
    todos = {entry["id"]: entry for entry in raw["todos"]}
    missing = catalogue.missing()
    for todo_id, roots in missing.items():
        if roots:
            check(todo_id in todos, f"{len(roots)} null values with no todo {todo_id!r}")
    for todo_id in todos:
        check(
            bool(missing.get(todo_id)),
            f"todo {todo_id!r} is open but nothing is null any more -- close it",
        )

    # 7. The provider manifest: a declaration, checked, never arbitrated silently.
    manifest = json.loads((root_dir / "manifeste.json").read_text(encoding="utf-8"))
    declared = {entry["racine"]: entry for entry in manifest["series"]}
    for root, instrument in catalogue.instruments.items():
        entry = declared.get(root)
        if entry is None:
            failures.append(f"{root}: absent from the provider manifest")
            continue
        check(
            entry["barres"] == instrument.bars,
            f"{root}: the manifest declares {entry['barres']} bars, the catalogue holds "
            f"{instrument.bars}",
        )
        check(
            entry["fichier"] == instrument.file,
            f"{root}: the manifest points at {entry['fichier']}, the catalogue at "
            f"{instrument.file}",
        )

    total_rolls = sum(
        len(i.roll_dates) for i in catalogue.instruments.values() if i.roll_dates is not None
    )
    print(f"catalogue : {len(catalogue.instruments)} instruments, "
          f"{len(catalogue.universe())} dans l'univers, {retained} cellules retenues, "
          f"{total_rolls} dates de roulement")
    for todo_id, roots in missing.items():
        if roots:
            print(f"  todo {todo_id:12s} ouvert sur {len(roots)} instruments "
                  f"({todos[todo_id]['blocks']})")

    if failures:
        print("\nCATALOGUE : INVALIDE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("\nCATALOGUE : VALIDE -- chaque nombre recopié correspond à sa source")
    return 0


def pd_next_day(date_text: str):
    import pandas as pd

    return (pd.Timestamp(date_text) + pd.Timedelta(days=1)).date()


def pd_date(value):
    import pandas as pd

    return pd.Timestamp(value).date()


if __name__ == "__main__":
    sys.exit(main())
