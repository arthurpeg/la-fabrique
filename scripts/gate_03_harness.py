"""Gate 03 -- the IC harness, calibrated by hand. The harness freezes once this passes.

The gate of D01 2 and of ETAT: the harness reproduces, BY HAND and on a known
case, an IC verified independently. Five things are asked.

1. A KNOWN CASE. A score that IS the forward return must give an IC of exactly 1,
   cell by cell. Nothing else does: an off-by-one in the alignment, a return
   borrowed from the next window, a score shifted by a bar -- all of them land
   below 1 and are caught here rather than four months from now.

2. AN INDEPENDENT VERIFICATION. The forward returns and the rank correlation of
   one cell are recomputed by a second implementation written differently --
   position by position, no groupby -- and must agree to 1e-12.

3. NOISE IS NOT SIGNAL. A score independent of the future gives an IC near zero
   and a final t that no threshold would accept. A harness that finds signal in
   noise is worse than no harness.

4. THE T IS DEFLATED TWICE, by sqrt(horizon) for the overlap and by
   sqrt(instruments / effective breadth) for the cross-section, and the report
   carries BOTH targets of D01 2.

5. THE COST IS A FLOOR THAT SAYS SO, and one evaluation writes exactly ONE line
   to the registry -- not one per cell (D01 4).

    python scripts/gate_03_harness.py

Exit code 1 and the divergence named, on any failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from harness import (  # noqa: E402
    TARGET_IC_DEPENDENT_WINDOWS,
    TARGET_IC_INDEPENDENT_WINDOWS,
    evaluate,
    registry,
)
from harness.metric import forward_returns  # noqa: E402
from panel import Panel  # noqa: E402
from panel.sessions import session_date, window_labels  # noqa: E402

ASOF = "2018-06-15 20:00"
HORIZON = "30min"
# Les 25 cellules retenues, pas trois : un harnais juste sur trois cellules est
# un harnais dont on ignore le comportement sur les vingt-deux autres.
HAND_CHECK_CELL = ("NQ", "US")


def cell_series(panel: Panel, root: str, window: str):
    """The adjusted closes of one cell, with its session and window labels."""
    adjusted = panel.adjusted(root, columns=["close"])["close"]
    labels = window_labels(adjusted.index, panel.catalogue)
    sessions = session_date(adjusted.index, panel.catalogue)
    mask = (labels == window).to_numpy()
    return adjusted[mask], sessions[mask], labels[mask]


def forward_returns_by_hand(close, sessions, windows, bars, positions):
    """The same quantity, computed differently on purpose: position by position, no groupby."""
    index, values = close.index, close.to_numpy()
    session_values, window_values = sessions.to_numpy(), windows.to_numpy()
    out: dict[pd.Timestamp, float] = {}
    for i in positions:
        j = i + bars
        if j >= len(index):
            continue
        if session_values[i] != session_values[j] or window_values[i] != window_values[j]:
            continue
        out[index[i]] = values[j] / values[i] - 1.0
    return pd.Series(out, dtype=float)


def main() -> int:
    panel = Panel.open(ASOF)
    failures: list[str] = []
    checked = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checked
        checked += 1
        if not condition:
            failures.append(message)

    bars = 30
    cells = tuple(panel.cells())
    series = {cell: cell_series(panel, *cell) for cell in cells}

    print("1. un cas connu : le score EST le rendement futur, l'IC doit valoir 1")
    perfect = {}
    for cell, (close, sessions, windows) in series.items():
        perfect[cell] = forward_returns(close, sessions, windows, bars)
    report_perfect = evaluate(
        perfect, panel, HORIZON,
        signal_id="calibration-parfaite",
        stage="03-calibration",
    )
    for measured in report_perfect.cells:
        check(
            abs(measured.ic - 1.0) < 1e-9,
            f"{measured.root} x {measured.window}: IC {measured.ic:.9f} au lieu de 1 "
            f"pour un score qui est le rendement futur",
        )
    check(
        abs(report_perfect.ic - 1.0) < 1e-9,
        f"IC poolé {report_perfect.ic:.9f} au lieu de 1 sur le cas parfait",
    )
    print(f"   IC poolé {report_perfect.ic:.9f} sur {len(report_perfect.cells)} cellules, "
          f"{report_perfect.observations:,} observations".replace(",", " "))

    print("2. vérification indépendante, seconde implémentation")
    cell = HAND_CHECK_CELL
    close, sessions, windows = series[cell]
    rng = np.random.default_rng(20260917)
    positions = sorted(rng.choice(len(close) - bars - 1, size=400, replace=False).tolist())
    by_hand = forward_returns_by_hand(close, sessions, windows, bars, positions)
    by_harness = forward_returns(close, sessions, windows, bars).reindex(by_hand.index)
    check(
        len(by_hand) > 100,
        f"seulement {len(by_hand)} rendements recalculés à la main, échantillon trop court",
    )
    check(
        float((by_hand - by_harness).abs().max()) < 1e-12,
        f"les rendements à la main et ceux du harnais diffèrent de "
        f"{float((by_hand - by_harness).abs().max()):.3e}",
    )
    scores_hand = pd.Series(rng.normal(size=len(close)), index=close.index)
    joined = pd.concat(
        [scores_hand.rename("s"), forward_returns(close, sessions, windows, bars).rename("r")],
        axis=1,
    ).dropna()
    ic_hand = float(stats.spearmanr(joined["s"], joined["r"]).statistic)
    report_noise = evaluate(
        {cell: scores_hand}, panel, HORIZON,
        signal_id="calibration-bruit",
        stage="03-calibration",
    )
    check(
        abs(report_noise.cells[0].ic - ic_hand) < 1e-12,
        f"IC du harnais {report_noise.cells[0].ic:.12f} contre {ic_hand:.12f} à la main",
    )
    print(f"   {len(by_hand)} rendements et l'IC de {cell[0]} x {cell[1]} reproduits à 1e-12")

    print("3. le bruit ne doit pas devenir un signal")
    check(
        abs(report_noise.ic) < 0.02,
        f"IC {report_noise.ic:+.5f} sur un score indépendant du futur",
    )
    check(
        abs(report_noise.t["final"]) < 3.0,
        f"t final {report_noise.t['final']:+.2f} sur du bruit — le seuil de Harvey est 3,0",
    )
    print(f"   IC {report_noise.ic:+.5f}, t final {report_noise.t['final']:+.2f} "
          f"(t naïf {report_noise.t['naive']:+.2f})")

    print("4. les deux déflations du t, et les deux cibles")
    factors = report_noise.t
    check(
        abs(factors["overlap_factor"] - np.sqrt(bars)) < 1e-9,
        f"facteur de recouvrement {factors['overlap_factor']:.4f} au lieu de sqrt({bars})",
    )
    expected_cross = np.sqrt(report_noise.instruments / report_noise.breadth)
    check(
        abs(factors["cross_section_factor"] - expected_cross) < 1e-9,
        f"facteur transversal {factors['cross_section_factor']:.4f} au lieu de "
        f"{expected_cross:.4f}",
    )
    check(
        abs(factors["final"]) <= abs(factors["naive"]) + 1e-12,
        "le t final n'est pas plus sévère que le t naïf",
    )
    rendered = report_noise.render()
    for target in (TARGET_IC_INDEPENDENT_WINDOWS, TARGET_IC_DEPENDENT_WINDOWS):
        check(f"{target:.3f}" in rendered, f"la cible {target:.3f} n'apparaît pas dans le rapport")
    print(f"   recouvrement ÷{factors['overlap_factor']:.2f}, transversal "
          f"÷{factors['cross_section_factor']:.2f} "
          f"({report_noise.instruments} instruments pour {report_noise.breadth:.2f} paris) ; "
          f"cibles 0,018 et 0,031 présentes")

    print("5. le coût est un plancher étiqueté, et une évaluation = une ligne")
    check(report_perfect.cost_floor_bp > 0, "le plancher de coût est nul ou absent")
    check(
        "fee_bp" in report_perfect.unknown_cost_components,
        "les frais ne sont pas signalés comme inconnus alors qu'ils sont null",
    )
    check(
        "slippage_bp" in report_perfect.unknown_cost_components,
        "le glissement n'est pas signalé comme inconnu",
    )
    before = len(registry.REGISTRY.read_text(encoding="utf-8").splitlines())
    evaluate(
        perfect, panel, HORIZON,
        signal_id="calibration-comptage",
        stage="03-calibration",
    )
    after = len(registry.REGISTRY.read_text(encoding="utf-8").splitlines())
    check(
        after - before == 1,
        f"une évaluation sur {len(cells)} cellules a écrit {after - before} lignes au registre, "
        f"pas 1 (D01 §4)",
    )
    check(
        registry.counted_tests() == 0,
        f"{registry.counted_tests()} tests comptés alors que tout est calibration",
    )
    print(f"   plancher {report_perfect.cost_floor_bp:.2f} bp, manquent "
          f"{', '.join(report_perfect.unknown_cost_components)} ; "
          f"{after} lignes au registre, {registry.counted_tests()} test compté")

    print("\n--- rapport d'IC, cas bruit ---")
    print(report_noise.render())

    print(f"\n{checked} vérifications")
    if failures:
        print("PORTE 03 : NON FRANCHIE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("PORTE 03 : FRANCHIE — le harnais est figé à partir d'ici")
    return 0


if __name__ == "__main__":
    sys.exit(main())
