"""La mesure de `H03` — le peigne de Heston, Korajczyk & Sadka (2010).

Cible de la clause 2 de la porte 06 (`D12`). `H03` est pré-enregistrée depuis le
2026-09-18, avant toute mesure, et affirme un **motif de signes** :

    A — les dents    décalage de m séances, même intervalle, m = 1..40   POSITIF
    B — les creux    décalage de j intervalles, j = 1..12                NÉGATIF ou nul
    C — le court     décalage de j = 1, 2, 3                             NÉGATIF

et, liant les trois : `IC(dents) > IC(creux)`.

**UNE hypothèse, une cinquantaine de lignes.** Chaque décalage mesuré écrit sa
ligne au registre — c'est ce qu'exige l'invariant III, un IC calculé est un IC
inscrit. Mais `H03` reste **une** hypothèse : ce n'est pas une recherche du
meilleur décalage, c'est la vérification d'un motif prédit en entier avant d'être
vu (`D11` et `D12` § Ce que ça verrouille). La phase 15 compte des hypothèses
éprouvées, pas des lignes écrites.

**Garde-fou, écrit d'avance dans `H03`.** Aucun décalage ne peut être retenu
comme signal sur la foi de cette mesure, même s'il ressort nettement.

    python scripts/measure_h03.py --dry-run   # pré-vol : mesurabilité, aucun IC
    python scripts/measure_h03.py             # la mesure
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402

from harness import evaluate, registry  # noqa: E402
from harness.metric import forward_returns  # noqa: E402  -- des rendements, jamais un IC
from panel import Panel  # noqa: E402
from panel.sessions import session_date, window_labels  # noqa: E402
from signals import heston_2010_periodicity as heston  # noqa: E402

ASOF = "2023-12-29 20:00"  # la dernière séance de la tranche pool
HORIZON = "30min"
HYPOTHESIS = "H03"

TEETH = range(1, 41)      # m séances, clause A
GAPS = range(1, 13)       # j intervalles, clause B (et C pour j = 1, 2, 3)


def preflight(panel: Panel) -> int:
    """Ce que le signal produit, et ce qui en devient mesurable. Aucun IC."""
    print("PRÉ-VOL — aucun IC calculé, aucun test dépensé\n")
    for window in ("ASIA", "EUROPE", "US"):
        print(f"  {window:7s} P = {heston.intervals_per_session(panel, window)} intervalles")
    print()

    for label, kwargs in (
        ("dent m=1", {"lag_sessions": 1}),
        ("dent m=40", {"lag_sessions": 40}),
        ("creux j=1", {"lag_intervals": 1}),
        ("creux j=12", {"lag_intervals": 12}),
    ):
        scores = heston.scores(panel, **kwargs)
        produced = sum(len(s) for s in scores.values())
        measurable = 0
        thin = []
        for root in sorted({r for r, _ in scores}):
            adjusted = panel.adjusted(root, columns=["close"])["close"]
            labels = window_labels(adjusted.index, panel.catalogue)
            sessions = session_date(adjusted.index, panel.catalogue)
            for window in sorted({w for r, w in scores if r == root}):
                mask = (labels == window).to_numpy()
                close = adjusted[mask]
                returns = forward_returns(close, sessions[mask], labels[mask], 30)
                aligned = scores[(root, window)].reindex(close.index)
                both = int((aligned.notna() & returns.notna()).sum())
                measurable += both
                if both < 30:
                    thin.append(f"{root}x{window} ({both})")
        rate = measurable / produced if produced else 0.0
        print(f"  {label:10s} {len(scores):2d} cellules · {produced:>8,} scores · "
              f"{measurable:>8,} observations ({rate:.1%})".replace(",", " "))
        if thin:
            print(f"             cellules sous 30 observations : {', '.join(thin)}")
    print("\nAucun IC n'a été calculé.")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    panel = Panel.open(asof=ASOF, slice="pool")
    print(f"panel au {panel.asof}, tranche {panel.slice.name}, "
          f"{len(panel.cells())} cellules retenues\n")

    if "--dry-run" in argv:
        return preflight(panel)

    before = registry.counted_tests()
    planned = len(TEETH) + len(GAPS)
    if before > 4 and "--force" not in argv:
        print(f"REFUSÉ — {before} lignes déjà comptées ; H03 semble déjà mesurée.")
        print("  Relancer écrirait ~52 lignes de plus. Si c'est voulu : --force.")
        return 1

    print(f"{planned} décalages à mesurer, {len(TEETH)} dents et {len(GAPS)} creux ; "
          f"harnais {registry.code_hash()}\n")

    teeth: list[tuple[int, float, float]] = []
    gaps: list[tuple[int, float, float]] = []

    for m in TEETH:
        scores = heston.scores(panel, lag_sessions=m)
        report = evaluate(scores, panel, HORIZON,
                          signal_id=f"{heston.SIGNAL_ID}-dent-m{m:02d}",
                          hypothesis_ref=HYPOTHESIS)
        teeth.append((m, report.ic, report.t["final"]))
        print(f"  dent  m={m:2d}   IC {report.ic:+.5f}   t {report.t['final']:+6.2f}   "
              f"n={report.observations:>8,}".replace(",", " "))

    print()
    for j in GAPS:
        scores = heston.scores(panel, lag_intervals=j)
        report = evaluate(scores, panel, HORIZON,
                          signal_id=f"{heston.SIGNAL_ID}-creux-j{j:02d}",
                          hypothesis_ref=HYPOTHESIS)
        gaps.append((j, report.ic, report.t["final"]))
        print(f"  creux j={j:2d}   IC {report.ic:+.5f}   t {report.t['final']:+6.2f}   "
              f"n={report.observations:>8,}".replace(",", " "))

    verdict(teeth, gaps, before)
    return 0


def verdict(teeth, gaps, counted_before: int) -> None:
    """Le motif, confronté aux trois clauses écrites avant la mesure."""
    tooth_ic = np.array([ic for _, ic, _ in teeth])
    gap_ic = np.array([ic for _, ic, _ in gaps])
    short_ic = np.array([ic for j, ic, _ in gaps if j <= 3])

    print("\n" + "=" * 72)
    print("LE MOTIF, CONFRONTÉ AUX CLAUSES ÉCRITES AVANT LA MESURE")
    print(f"  A — dents  (m=1..40)  IC médian {np.median(tooth_ic):+.5f}   "
          f"{int((tooth_ic > 0).sum())}/{len(tooth_ic)} positifs")
    print(f"  B — creux  (j=1..12)  IC médian {np.median(gap_ic):+.5f}   "
          f"{int((gap_ic < 0).sum())}/{len(gap_ic)} négatifs")
    print(f"  C — court  (j=1..3)   IC médian {np.median(short_ic):+.5f}   "
          f"{int((short_ic < 0).sum())}/{len(short_ic)} négatifs")
    print()
    separated = np.median(tooth_ic) > np.median(gap_ic)
    print(f"  séparation dents > creux : {'OUI' if separated else 'NON'}   "
          f"({np.median(tooth_ic):+.5f} contre {np.median(gap_ic):+.5f})")
    print()
    print("  Le verdict de porte ne se lit pas ici : il se lit dans H03, qui dit")
    print("  ce que chaque clause exige et ce qu'un motif absent signifierait.")
    after = registry.counted_tests()
    print(f"\nlignes comptées : {counted_before} -> {after}  (+{after - counted_before}) "
          f"pour UNE hypothèse")


if __name__ == "__main__":
    sys.exit(main())
