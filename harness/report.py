"""The IC report: the official output of the harness, and the only source of IC in the project.

It carries, always and inseparably:

  - the pooled IC and the t that has been deflated twice;
  - BOTH targets of D01 2 -- 0.018 if the three windows are independent, 0.031 if
    they are not -- because showing the flattering one alone is how a project
    talks itself into a signal;
  - the round-trip cost floor and the components it could not price;
  - the per-cell breakdown, marked as a diagnostic, never as a set of tests;
  - the registry id of the line this report wrote, and the hash of the harness
    that produced it.

Nothing here can be printed without the rest: a caller gets the whole object.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from harness.costs import CellCost
from harness.metric import CellIC

BREADTH_FILE = Path(__file__).resolve().parents[1] / "scripts" / "out" / "a5_breadth_intraday.json"

# D01 2: the IC needed for an IR of 1, under the two breadth counts. Both, always.
TARGET_IC_INDEPENDENT_WINDOWS = 0.018
TARGET_IC_DEPENDENT_WINDOWS = 0.031


def effective_breadth(frequency: str = "15min") -> float:
    """Measured in phase 01, never assumed: the participation ratio of the universe."""
    payload = json.loads(BREADTH_FILE.read_text(encoding="utf-8"))
    return float(payload[frequency]["participation_ratio"])


@dataclass(frozen=True)
class ICReport:
    test_id: str
    signal_id: str
    hypothesis_ref: str | None
    stage: str
    data_slice: str
    asof: str
    horizon: str
    horizon_bars: int
    ic: float
    observations: int
    t: dict[str, float]
    cells: tuple[CellIC, ...]
    costs: tuple[CellCost, ...]
    instruments: int
    breadth: float
    code_hash: str
    counted_tests: int
    # Les contrôles de la phase 06. Les avertissements ne bloquent rien et
    # voyagent avec le chiffre : un résultat gênant se lit, il ne se cache pas
    # (D08). Les cellules refusées sont nommées, pour qu'un IC calculé sur sept
    # cellules au lieu de vingt-cinq ne passe pas pour un IC sur vingt-cinq.
    warnings: tuple[str, ...] = ()
    refused_cells: tuple = ()

    @property
    def cost_floor_bp(self) -> float:
        return max((cost.floor_bp for cost in self.costs), default=float("nan"))

    @property
    def unknown_cost_components(self) -> tuple[str, ...]:
        seen: list[str] = []
        for cost in self.costs:
            for name in cost.unknown:
                if name not in seen:
                    seen.append(name)
        return tuple(seen)

    def render(self) -> str:
        lines: list[str] = []
        add = lines.append
        add(f"RAPPORT D'IC — {self.signal_id} — horizon {self.horizon} "
            f"({self.horizon_bars} barres)")
        add(f"test {self.test_id} · tranche {self.data_slice} · as-of {self.asof} · "
            f"harnais {self.code_hash}")
        add(f"hypothèse : {self.hypothesis_ref or '— (calibration, hors dénominateur FDR)'}")
        add("")
        add(f"IC poolé          {self.ic:+.5f}   sur {self.observations:,} observations, "
            f"{len(self.cells)} cellules".replace(",", " "))
        add(f"t naïf            {self.t['naive']:+.2f}")
        gap = self.t.get("sampling_gap_bars", float("nan"))
        shared = max(0.0, self.horizon_bars - gap)
        add(f"t recouvrement    {self.t['overlap']:+.2f}   "
            f"(÷ {self.t['overlap_factor']:.2f} ; horizon {self.horizon_bars} barres, "
            f"observations espacées de {gap:.0f} — "
            f"{'aucun recouvrement' if shared <= 0 else f'{shared:.0f} barres partagées'})")
        add(f"t final           {self.t['final']:+.2f}   "
            f"(÷ {self.t['cross_section_factor']:.2f}, {self.instruments} instruments pour "
            f"{self.breadth:.2f} paris)")
        add("")
        add("cibles de D01 §2, les deux, jamais l'une seule :")
        for label, target in (
            ("fenêtres indépendantes  ~3 100 paris/an", TARGET_IC_INDEPENDENT_WINDOWS),
            ("fenêtres dépendantes    ~1 060 paris/an", TARGET_IC_DEPENDENT_WINDOWS),
        ):
            ratio = self.ic / target if target else float("nan")
            verdict = "atteinte" if self.ic >= target else "non atteinte"
            add(f"  {label}   cible {target:.3f}   {ratio:+.2f}× la cible   {verdict}")
        add("")
        floor = self.cost_floor_bp
        add(f"coût d'aller-retour : plancher {floor:.2f} bp (pire cellule) — "
            f"INCOMPLET, manquent : {', '.join(self.unknown_cost_components)}")
        add("  un IC net calculé là-dessus serait un MINORANT de coût, "
            "donc un MAJORANT de performance.")
        add("")
        if self.refused_cells:
            add(f"cellules refusées par les contrôles (D08) : {len(self.refused_cells)} — "
                "l'IC ci-dessus ne porte PAS sur elles")
            for verdict in self.refused_cells:
                root, window = verdict.cell
                add(f"  {root:5s} {window:7s} {verdict.reason}")
            add("")
        for warning in self.warnings:
            add(f"AVERTISSEMENT — {warning}")
        if self.warnings:
            add("")
        add(f"tests comptés au registre (hors calibrations) : {self.counted_tests}")
        add("")
        add("ventilation par cellule — DIAGNOSTIC, pas des tests (D01 §4) :")
        for cell in sorted(self.cells, key=lambda c: -abs(c.ic)):
            add(f"  {cell.root:5s} {cell.window:7s} IC {cell.ic:+.5f}  "
                f"n={cell.observations:>8,}  horizon réalisé {cell.horizon_median_minutes:.0f} min "
                f"(p99 {cell.horizon_p99_minutes:.0f})".replace(",", " "))
        return "\n".join(lines)
