"""Gate 02 -- the point-in-time Panel. Phase 02 does not close unless this passes.

Three checks, one per clause of the gate.

1. REPRODUCIBILITY. The same as-of, asked twice, answers the same thing. And a
   panel opened later then truncated back to T answers exactly what a panel
   opened at T answers -- the past does not depend on when it is asked about.

2. NO FUTURE. No bar later than the as-of is ever returned; the universe at a
   past date is the universe of that date; moving an as-of forward, opening the
   sealed slice, or reaching into the holdout from the research path are all
   refused rather than allowed quietly.

3a. THE ADJUSTMENT ALGORITHM, on a synthetic series whose answer is known:
   the artificial jumps go, the returns survive, and a series built at t agrees
   with one built later up to a uniform factor. The part the algorithm cannot
   separate -- the real move during the splice minute -- is measured here rather
   than hoped away.

3b. THE REAL SERIES. The machinery above is useless without the authoritative
   roll dates, which are not in the catalogue. This check therefore FAILS, and
   the gate stays shut. That is the intended outcome, not an accident: a gate is
   never crossed "provisionally". What is missing is data, not code.

    python scripts/gate_02_panel.py

Exit code 1 while anything is unverified.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from panel import (  # noqa: E402
    HoldoutLocked,
    LookaheadRefused,
    Panel,
    RollDatesMissing,
    SliceExceeded,
    back_adjust,
    load_catalogue,
    visible_rolls,
)

EARLY = "2017-03-15 20:00"
MIDDLE = "2021-06-15 20:00"
LATE = "2023-06-14 20:00"
FIRST_BAR = "2016-01-03 23:00"
BEFORE_FIRST_BAR = "2016-01-03 22:59"
INSIDE_HOLDOUT = "2025-06-02 20:00"
SAMPLE = ("NQ", "GC", "6J")


def synthetic(splice_minute_move_bp: float = 0.0):
    """A series whose answer is known: a true price, spliced twice on purpose.

    The raw series is the true one multiplied by 1.05 after the first splice and
    by 0.97 more after the second -- two jumps that no market made. Whether the
    market moved during the splice minute itself is the parameter, because that
    is precisely the part the adjustment cannot tell apart from the artefact.
    """
    length, first_roll, second_roll = 300, 100, 200
    index = pd.date_range("2020-06-01 00:00", periods=length, freq="1min", tz="UTC")
    steps = 0.0001 * np.sin(np.arange(length))
    steps[first_roll] = steps[second_roll] = splice_minute_move_bp / 10_000
    truth = pd.Series(100 * np.cumprod(1 + steps), index=index, name="close")

    raw = truth.to_numpy().copy()
    raw[first_roll:second_roll] *= 1.05
    raw[second_roll:] *= 1.05 * 0.97
    frame = pd.DataFrame({"close": raw}, index=index)
    return frame, truth, [index[first_roll], index[second_roll]]


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
    refuses(SliceExceeded, lambda: first.truncate(end="2015-06-01"), "truncate avant la tranche")
    refuses(HoldoutLocked, lambda: Panel.open(MIDDLE, slice="holdout"), "ouverture du holdout")
    refuses(SliceExceeded, lambda: Panel.open(INSIDE_HOLDOUT), "as-of dans le holdout")
    print("   aucune barre postérieure ; univers invariant ; look-ahead, holdout et "
          "tranche refusés")

    print("3a. l'algorithme d'ajustement, sur un cas synthétique dont la réponse est connue")
    flat, truth, rolls = synthetic(splice_minute_move_bp=0.0)
    adjusted = back_adjust(flat, rolls)
    ratio = adjusted["close"] / truth
    check(
        float(ratio.max() - ratio.min()) < 1e-9,
        f"the adjusted series is not a uniform multiple of the true one "
        f"(spread {float(ratio.max() - ratio.min()):.3e})",
    )
    check(
        float((adjusted["close"].pct_change() - truth.pct_change()).abs().max()) < 1e-12,
        "the adjusted returns differ from the true returns",
    )

    midpoint = flat.index[150]
    early = back_adjust(flat.loc[flat.index <= midpoint], visible_rolls(rolls, midpoint))
    late_view = adjusted.loc[adjusted.index <= midpoint, "close"]
    drift = late_view / early["close"]
    check(
        len(visible_rolls(rolls, midpoint)) == 1,
        "a splice later than the as-of is visible to the adjustment",
    )
    check(
        float(drift.max() - drift.min()) < 1e-9,
        "the series built at t and the series built later disagree by more than a uniform factor",
    )
    check(
        float((early["close"].pct_change() - late_view.pct_change()).abs().max()) < 1e-12,
        "the returns depend on when the series was built",
    )

    # The gap can only be read as the one-minute return at the splice, so it carries
    # whatever the market did in that minute. Measured here rather than hoped away.
    injected_bp = 5.0
    moved, moved_truth, moved_rolls = synthetic(splice_minute_move_bp=injected_bp)
    steps = (back_adjust(moved, moved_rolls)["close"] / moved_truth).round(12).unique()
    absorbed = [steps[i] / steps[i + 1] - 1 for i in range(len(steps) - 1)]
    check(
        len(steps) == 3 and all(abs(a * 10_000 - injected_bp) < 1e-6 for a in absorbed),
        f"the absorbed move is {[round(a * 10_000, 4) for a in absorbed]} bp, "
        f"expected {injected_bp} bp at each of the two splices",
    )
    print(f"    jumps retirés, rendements préservés, propriété d'échelle vérifiée ; "
          f"l'ajustement absorbe exactement le mouvement réel de la minute de recollement "
          f"({injected_bp} bp injectés, {round(absorbed[0] * 10_000, 4)} bp absorbés)")

    print("3b. la série ajustée des instruments réels")
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
