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
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from panel.catalogue import load_catalogue  # noqa: E402
from panel.paths import CATALOGUE, data_dir  # noqa: E402

RETRIEVED = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NUMBER = re.compile(r"\d+(?:\.\d+)?")

INVENTORY = REPO / "scripts" / "out" / "a1_inventory.json"
GRID = REPO / "scripts" / "out" / "a8_session_grid.json"

# What phase 01 measured, and what the catalogue is allowed to copy from it.
CELL_FIELDS = {
    "spread_floor_bp": "spread_bp",
    "median_volume_per_minute": "vol/min",
    "median_abs_15min_move_bp": "move15_bp",
    "round_trip_over_move": "cost/move",
}

# D09. Every value in the catalogue is one of three things, and which one it is
# says how it gets checked:
#
#   measured  our code, from our data     -- re-derived below, sections 4 and 5
#   decided   our choice, written down    -- a file in decisions/
#   external  copied from a third party   -- contradicted by nothing in the repo
#
# The external ones below carry a provenance entry, or they do not enter.
EXTERNAL_FIELDS = ("multiplier", "fee_per_contract_usd")

# External too, but corroborated: one of our own measurements can contradict
# them, so they already have a judge and need no entry. The list is CLOSED
# (D09) -- nothing joins it by resembling it.
#
#   instruments[*].roll.cycle      against the observed roll rate, section 5b.
#                                  That check is what caught D01 6 declaring
#                                  gold monthly when it rolls 5.07 a year (L07)
#   instruments[*].file, .bars,    against the provider manifest, section 7
#   .exchange, .databento_dataset
PROVENANCE_FIELDS = ("source", "source_url", "retrieved", "quoted", "applies_to")


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
    for key in ("data", "grid", "session_date", "slices", "retention_rule",
                "instruments", "todos", "provenance"):
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
    rolls_payload = None
    rolls_file = REPO / "catalogue" / "roll_dates.json"
    check(rolls_file.exists(), "roll_dates.json is missing but the catalogue points at it")
    if rolls_file.exists():
        rolls = rolls_payload = json.loads(rolls_file.read_text(encoding="utf-8"))
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

    # 8. Provenance: an external value never enters the catalogue alone (D09).
    failures.extend(provenance_failures(raw, rolls_payload))

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


def provenance_failures(raw: dict, rolls: dict | None) -> list[str]:
    """Every external value, against the entry that vouches for it (D09).

    Split out of main() because this is the one section that has to be shown
    REFUSING: scripts/check_provenance.py feeds it deliberately broken
    catalogues and reads what comes back. A guard that has never turned
    anything away is a guard nobody has tested.
    """
    failures: list[str] = []
    entries = raw.get("provenance")
    if entries is None:
        return ["missing top-level key 'provenance' (D09)"]
    if not isinstance(entries, list):
        return [f"provenance is a {type(entries).__name__}, expected a list (D09)"]

    instruments = {spec["root"]: spec for spec in raw["instruments"]}

    # Which external fields are actually filled, and so owe a provenance.
    filled = {
        f"instruments.{root}.{field}"
        for root, spec in instruments.items()
        for field in EXTERNAL_FIELDS
        if spec.get(field) is not None
    }

    seen_ids: set[str] = set()
    covered: dict[str, str] = {}
    for position, entry in enumerate(entries):
        name = entry.get("id") or f"#{position}"
        if not entry.get("id"):
            failures.append(f"provenance {name}: no id")
        elif entry["id"] in seen_ids:
            failures.append(f"provenance {entry['id']}: duplicate id")
        else:
            seen_ids.add(entry["id"])

        for field in PROVENANCE_FIELDS:
            value = entry.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                failures.append(f"provenance {name}: {field} is empty (D09)")
        if not str(entry.get("source_url", "")).startswith("http"):
            failures.append(f"provenance {name}: source_url is not a URL")
        if not RETRIEVED.match(str(entry.get("retrieved", ""))):
            failures.append(
                f"provenance {name}: retrieved is {entry.get('retrieved')!r}, "
                f"expected AAAA-MM-JJ"
            )

        quoted = str(entry.get("quoted", ""))
        for path in entry.get("applies_to") or []:
            if path in covered:
                failures.append(
                    f"provenance {name}: {path} is already covered by {covered[path]}"
                )
                continue
            covered[path] = name

            parts = str(path).split(".")
            if len(parts) != 3 or parts[0] != "instruments":
                failures.append(
                    f"provenance {name}: {path!r} is not instruments.<ROOT>.<field>"
                )
                continue
            _, root, field = parts
            if root not in instruments:
                failures.append(f"provenance {name}: {path} names no instrument")
                continue
            if field not in EXTERNAL_FIELDS:
                failures.append(
                    f"provenance {name}: {field} is not an external field "
                    f"{EXTERNAL_FIELDS} -- a measured or decided value is checked "
                    f"against its source, never vouched for (D09)"
                )
                continue
            value = instruments[root].get(field)
            if value is None:
                # Dead provenance, refused like a dead todo: it vouches for a
                # hole, and the next session reads it as a filled value.
                failures.append(f"provenance {name}: {path} is null -- close the entry")
            elif not value_in_quote(value, quoted):
                failures.append(
                    f"provenance {name}: {path} holds {value!r}, which is nowhere in "
                    f"the quoted source {quoted[:60]!r} (D09)"
                )

    for path in sorted(filled - set(covered)):
        failures.append(f"{path} is filled but no provenance vouches for it (D09)")

    # A third-party FILE is stored as received and carries its provenance inside
    # itself. Same requirement, same refusal.
    if rolls is not None:
        for field in ("source", "source_url", "retrieved"):
            if not str(rolls.get(field, "")).strip():
                failures.append(f"roll_dates.json: {field} is empty (D09)")

    return failures


def value_in_quote(value, quoted: str) -> bool:
    """Is the deposited value findable in the words of the source?

    The comparison is on NUMBERS, not on substrings: the quote is split into
    its numeric tokens and each is compared to the value. Substring matching
    looked equivalent and was not -- "12500" sits inside "12500000", so a
    multiplier short of three zeros passed under a quote that said 12,500,000.
    scripts/check_provenance.py caught it, and keeps that case.

    Thousands separators are stripped from the quote, never from the value, so
    "12,500,000 Japanese yen" vouches for 12500000 and "$20 x Nasdaq-100 Index"
    for 20 -- the units stay in the third party's own words.

    What this catches is the transcription slip, which stays a plausible number
    forever once deposited. It is not proof: a number that appears anywhere in
    the quote will vouch, so `quoted` holds the contract-unit line itself and
    not a page dump. It does not catch a determined liar, and D09 does not
    claim that it does.
    """
    flat = quoted.replace(",", "").replace("\u00a0", "").replace("'", "")
    for token in NUMBER.findall(flat):
        try:
            if float(token) == float(value):
                return True
        except (TypeError, ValueError):
            continue
    return False


def pd_next_day(date_text: str):
    import pandas as pd

    return (pd.Timestamp(date_text) + pd.Timedelta(days=1)).date()


def pd_date(value):
    import pandas as pd

    return pd.Timestamp(value).date()


if __name__ == "__main__":
    sys.exit(main())
