"""Gate 02 -- the point-in-time Panel. Phase 02 does not close unless this passes.

Three checks, one per clause of the gate.

1. REPRODUCIBILITY. The same as-of, asked twice, answers the same thing. And a
   panel opened later then truncated back to T answers exactly what a panel
   opened at T answers -- the past does not depend on when it is asked about.

2. NO FUTURE. No bar later than the as-of is ever returned; the universe at a
   past date is the universe of that date; moving an as-of forward, opening the
   sealed slice, or reaching into the holdout from the research path are all
   refused rather than allowed quietly.

3. BACK-ADJUSTMENT. The back-adjusted series must use only the splices <= t
   (D01 6). It cannot be built, let alone checked, without the authoritative
   roll dates -- which are not in the catalogue. This check therefore FAILS,
   and the gate stays shut. That is the intended outcome, not an accident:
   a gate is never crossed "provisionally".

    python scripts/gate_02_panel.py

Exit code 1 while anything is unverified.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from panel import (  # noqa: E402
    HoldoutLocked,
    LookaheadRefused,
    Panel,
    RollDatesMissing,
    SliceExceeded,
    load_catalogue,
)

EARLY = "2017-03-15 20:00"
MIDDLE = "2021-06-15 20:00"
LATE = "2023-06-14 20:00"
FIRST_BAR = "2016-01-03 23:00"
BEFORE_FIRST_BAR = "2016-01-03 22:59"
INSIDE_HOLDOUT = "2025-06-02 20:00"
SAMPLE = ("NQ", "GC", "6J")


def main() -> int:
    catalogue = load_catalogue()
    failures: list[str] = []
    checked = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checked
        checked += 1
        if not condition:
            failures.append(message)

    def refuses(expected, call, label: str) -> None:
        nonlocal checked
        checked += 1
        try:
            call()
        except expected:
            return
        except Exception as error:  # noqa: BLE001 - the wrong refusal is still a failure
            failures.append(f"{label}: raised {type(error).__name__}, expected {expected.__name__}")
            return
        failures.append(f"{label}: was allowed, expected {expected.__name__}")

    print("1. reproductibilité")
    first, second = Panel.open(MIDDLE), Panel.open(MIDDLE)
    for root in SAMPLE:
        check(
            first.fingerprint(root) == second.fingerprint(root),
            f"{root}: two panels opened at {MIDDLE} disagree",
        )
    late = Panel.open(LATE)
    truncated = late.truncate(end=MIDDLE)
    for root in SAMPLE:
        check(
            truncated.fingerprint(root) == first.fingerprint(root),
            f"{root}: the panel truncated from {LATE} back to {MIDDLE} does not answer "
            f"what a panel opened at {MIDDLE} answers",
        )
    print(f"   {len(SAMPLE)} instruments, empreintes identiques à {MIDDLE} par deux chemins")

    print("2. aucune ligne visible avant son horodatage")
    for asof in (EARLY, MIDDLE, LATE):
        panel = Panel.open(asof)
        for root in SAMPLE:
            bars = panel.bars(root, columns=["close"])
            check(
                bars.index[-1] <= panel.asof,
                f"{root}: a bar at {bars.index[-1]} is visible from a panel as of {panel.asof}",
            )
    check(
        Panel.open(BEFORE_FIRST_BAR).universe() == (),
        f"the universe is not empty at {BEFORE_FIRST_BAR}, before the first bar exists",
    )
    check(
        len(Panel.open(FIRST_BAR).universe()) == len(catalogue.universe()),
        f"the universe at {FIRST_BAR} does not hold every instrument",
    )
    check(
        Panel.open(EARLY).universe() == late.truncate(end=EARLY).universe(),
        f"the universe at {EARLY} changes depending on when the question is asked",
    )
    refuses(LookaheadRefused, lambda: first.truncate(end=LATE), "truncate vers le futur")
    refuses(HoldoutLocked, lambda: Panel.open(MIDDLE, slice="holdout"), "ouverture du holdout")
    refuses(SliceExceeded, lambda: Panel.open(INSIDE_HOLDOUT), "as-of dans le holdout")
    print("   aucune barre postérieure ; univers invariant ; look-ahead, holdout et "
          "tranche refusés")

    print("3. série ajustée à rebours, recollements <= t")
    blocked = [r for r, i in catalogue.instruments.items() if i.roll_dates is None]
    for root in SAMPLE:
        refuses(RollDatesMissing, lambda root=root: first.adjusted(root), f"adjusted({root})")
    if blocked:
        failures.append(
            f"NON VÉRIFIABLE : dates de roulement absentes du catalogue pour "
            f"{len(blocked)} instruments ({', '.join(blocked)}). Intrant attendu de "
            f"l'auteur des données (todo roll-dates). Sans elles, la série ajustée à "
            f"rebours ne peut être ni construite ni vérifiée."
        )

    print(f"\n{checked} vérifications")
    if failures:
        print("PORTE 02 : NON FRANCHIE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("PORTE 02 : FRANCHIE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
