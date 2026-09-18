"""Contrôles sur le signal de `H03` — et pas une corrélation.

Même rôle que `scripts/check_signals.py` pour les deux étalons : vérifier que le
signal est *utilisable* avant qu'un IC soit calculé sur lui. Il ne mesure **aucun
IC**, et n'écrit rien au registre.

Ce qu'il vérifie, dans l'ordre où ça coûte le moins cher :

1. la **période du peigne** est bien celle du catalogue, pas celle qu'on espère ;
2. la **liste blanche** d'importations (`sandbox/scan.py`) ;
3. le **contrat** de module et de sortie (`sandbox/contract.py`) ;
4. la **causalité** par troncature du panel (`sandbox/causality.py`) ;
5. l'**écart d'échantillonnage**, qui décide de la déflation de `D11` ;
6. le nombre d'**observations mesurables**, et pas seulement de scores (`L10`).

    python scripts/check_heston.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from harness.metric import forward_returns, sampling_gap  # noqa: E402 -- jamais un IC
from panel import Panel  # noqa: E402
from panel.sessions import session_date, window_labels  # noqa: E402
from sandbox import causality, contract, scan  # noqa: E402
from signals import _common  # noqa: E402
from signals import heston_2010_periodicity as heston  # noqa: E402

ASOF = "2018-06-15 20:00"
INTERVAL_BARS = 30
MIN_OBSERVATIONS = 30

# Ce que le catalogue impose, et qu'aucun résultat ne doit pouvoir changer.
EXPECTED_PERIOD = {"ASIA": 16, "EUROPE": 13, "US": 13}


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    panel = Panel.open(asof=ASOF, slice="pool")
    print(f"panel ouvert au {panel.asof}, tranche {panel.slice.name}, "
          f"{len(panel.cells())} cellules\n")

    print("1. la période du peigne vient du catalogue")
    for window, expected in EXPECTED_PERIOD.items():
        got = heston.intervals_per_session(panel, window)
        check(got == expected, f"{window} : période {got}, attendue {expected}")
        print(f"   {window:7s} P = {got} intervalles")

    print("\n2. liste blanche d'importations")
    source = (REPO / "signals" / "heston_2010_periodicity.py").read_text(encoding="utf-8")
    refusals = scan.scan_source(source, "signals/heston_2010_periodicity.py")
    check(not refusals, f"importations refusées : {refusals}")
    print(f"   {len(refusals)} refus")

    print("\n3. contrat de module et de sortie")
    bad = contract.validate_module(heston)
    check(not bad, f"contrat de module : {bad}")
    teeth = heston.scores(panel, lag_sessions=1)
    bad = contract.validate_scores(teeth, panel)
    check(not bad, f"contrat de sortie : {bad}")
    check(len(teeth) == len(panel.cells()),
          f"{len(teeth)} cellules scorées sur {len(panel.cells())}")
    print(f"   module conforme, {len(teeth)} cellules, "
          f"{sum(len(s) for s in teeth.values()):,} scores".replace(",", " "))

    print("\n4. causalité — le panel tronqué rend-il les mêmes scores ?")
    divergences = causality.check(heston, panel, probes=16)
    check(not divergences, f"{len(divergences)} divergence(s) : {divergences[:2]}")
    print(f"   {len(divergences)} divergence(s) sur 16 sondes")

    print("\n5. écart d'échantillonnage — ce qui décide de la déflation (D11)")
    for cell in (("NQ", "US"), ("NQ", "ASIA"), ("CL", "EUROPE")):
        close, _ = _common.cell_bars(panel, *cell)
        gap = sampling_gap(close.index, teeth[cell].index)
        factor = max(1.0, INTERVAL_BARS / gap) if gap > 0 else 1.0
        check(abs(gap - INTERVAL_BARS) < 1e-9,
              f"{cell} : écart {gap}, attendu {INTERVAL_BARS} — des demi-heures "
              f"disjointes ne se recouvrent pas")
        print(f"   {cell[0]:3s} x {cell[1]:6s} écart {gap:.0f} barres, "
              f"étalement {factor:.2f}")

    print("\n6. observations mesurables, pas seulement des scores (L10)")
    for label, kwargs in (("dent m=1", {"lag_sessions": 1}),
                          ("creux j=1", {"lag_intervals": 1})):
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
                returns = forward_returns(close, sessions[mask], labels[mask], INTERVAL_BARS)
                aligned = scores[(root, window)].reindex(close.index)
                both = int((aligned.notna() & returns.notna()).sum())
                measurable += both
                if both < MIN_OBSERVATIONS:
                    thin.append(f"{root}x{window} ({both})")
        rate = measurable / produced if produced else 0.0
        check(rate > 0.5, f"{label} : {rate:.1%} de mesurabilité seulement")
        check(not thin, f"{label} : cellules sous {MIN_OBSERVATIONS} observations : {thin}")
        print(f"   {label:10s} {produced:>8,} scores · {measurable:>8,} observations "
              f"({rate:.1%})".replace(",", " "))

    print(f"\n{checks} vérifications")
    if failures:
        print("SIGNAL H03 : NON UTILISABLE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("SIGNAL H03 : utilisable — aucun IC n'a été calculé ici")
    return 0


if __name__ == "__main__":
    sys.exit(main())
