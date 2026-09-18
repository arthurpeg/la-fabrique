"""La mesure de `H04` — la périodicité intra-journalière de la volatilité.

Cible de la clause 2 de la porte 06 (`D13`). `H04` est pré-enregistrée depuis le
2026-09-18, avant toute mesure.

**AUCUN IC N'EST CALCULÉ ICI, et c'est structurel.** Cet instrument mesure une
propriété des *données* — la forme de la volatilité au fil de la séance — et non
le pouvoir prédictif d'un signal. L'invariant III porte sur les IC ; il ne
s'applique pas, `counted_tests()` ne bouge pas, et le dénominateur des
corrections de tests multiples reste à 56.

**IL VIT DANS `scripts/` ET NON DANS `harness/`**, et la raison est chiffrée :
`registry.code_hash()` n'empreinte que `harness/*.py`, donc y ajouter un fichier
périmerait les 56 lignes comptées, dont trois hypothèses mesurées. Le critère de
`D08` reste celui-ci : ce qui juge un signal entre dans l'empreinte, ce qui
mesure les données n'y entre pas (`D13` § Ce que ça verrouille).

Les quatre clauses, telles que `H04` les pose :

    A  forme en U      |r| moyen par tranche horaire : creux au milieu
    B  rapport         sommet / creux entre 1,4 et 3,0
    C  périodicité     autocorrélation de |r| plus forte aux multiples de séance
    D  généralité      A tient sur NQ, ES et YM, pas sur une seule cellule

La sortie porte en plus un DIAGNOSTIC de phase, ajouté après la première mesure
et n'entrant dans aucune clause : l'autocorrélation aux décalages situés à une
DEMI-séance des multiples, donc à phase opposée du cycle. Le témoin de `H04` est
à 15 et 30 minutes du multiple, presque à la même phase, et mesure de ce fait un
plancher de l'effet plutôt que l'effet (`L16`).

    python scripts/measure_h04.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from panel import Panel  # noqa: E402
from panel.sessions import local, session_date, window_labels  # noqa: E402

ASOF = "2023-12-29 20:00"
WINDOW = "US"
ROOTS = ("NQ", "ES", "YM")
BUCKET_MINUTES = 30

# Les bornes de H04, écrites avant la mesure. Elles ne bougent pas ici.
RATIO_MIN, RATIO_MAX = 1.4, 3.0
OUT = REPO / "scripts" / "out" / "h04_periodicity.json"


def cell_returns(panel: Panel, root: str, window: str):
    """Les rendements d'une minute d'une cellule, et la séance de chaque barre.

    Ajustés des roulements, comme la cible du harnais : la fenêtre US ne contient
    pas 00:00 UTC, mais l'ajustement reste la bonne base de comparaison (L08).
    Le premier rendement de chaque séance est écarté — il enjamberait la nuit.
    """
    adjusted = panel.adjusted(root, columns=["close"])["close"]
    labels = window_labels(adjusted.index, panel.catalogue)
    sessions = session_date(adjusted.index, panel.catalogue)
    mask = (labels == window).to_numpy()
    close = adjusted[mask]
    day = sessions[mask]

    returns = close.groupby(day, sort=False).pct_change()
    keep = returns.notna() & np.isfinite(returns)
    return returns[keep], day[keep], close.index[keep]


def bucket_profile(returns: pd.Series, index: pd.DatetimeIndex, panel: Panel):
    """Le |r| moyen par tranche de trente minutes, sur l'horloge de la place."""
    clock = local(index, panel.catalogue.timezone)
    minutes = clock.hour * 60 + clock.minute
    start = int(round(panel.catalogue.windows[WINDOW].start_hour * 60))
    bucket = ((minutes - start) % (24 * 60)) // BUCKET_MINUTES
    frame = pd.DataFrame({"abs": returns.abs().to_numpy(), "bucket": bucket})
    return frame.groupby("bucket")["abs"].agg(["mean", "count"])


def autocorrelation(returns: pd.Series, lags: list[int]) -> dict[int, float]:
    """L'autocorrélation de |r| sur la série de fenêtre CONCATÉNÉE.

    La première version interdisait aux paires d'enjamber la séance. C'était
    faux, et d'une façon qui vidait la clause C de son objet : un décalage à la
    fréquence journalière enjambe la nuit PAR DÉFINITION — c'est ce que « même
    heure, séance suivante » veut dire. Le garde interdisait exactement ce que la
    clause cherche, et aucune paire ne survivait.

    Le montage correct est celui des auteurs : leur corrélogramme court sur la
    série continue des rendements de cinq minutes du S&P, **rendements overnight
    exclus**, et le décalage 80 y vaut la même heure le lendemain. Chez nous
    l'exclusion est déjà faite en amont — `cell_returns` calcule les rendements
    par séance, donc le premier de chaque séance, celui qui enjamberait la nuit,
    n'existe pas. La concaténation est alors légitime, et c'est la leur.
    """
    values = returns.abs().to_numpy(dtype=float)
    out: dict[int, float] = {}
    for lag in lags:
        if lag >= len(values) - 100:
            continue
        a, b = values[lag:], values[:-lag]
        if a.std() == 0 or b.std() == 0:
            continue
        out[lag] = float(np.corrcoef(a, b)[0, 1])
    return out


def main() -> int:
    panel = Panel.open(asof=ASOF, slice="pool")
    period = int(round(
        (panel.catalogue.windows[WINDOW].end_hour
         - panel.catalogue.windows[WINDOW].start_hour) * 60
    ))
    print(f"panel au {panel.asof}, tranche {panel.slice.name}")
    print(f"fenêtre {WINDOW} : {period} minutes de séance\n")
    print("AUCUN IC n'est calculé ici. counted_tests() ne bougera pas.\n")

    results: dict[str, dict] = {}
    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    print("A et B — la forme en U, et son rapport")
    for root in ROOTS:
        returns, day, index = cell_returns(panel, root, WINDOW)
        profile = bucket_profile(returns, index, panel)
        means = profile["mean"].to_numpy(dtype=float)
        n_buckets = len(means)
        edge = max(1, n_buckets // 4)
        opening = float(means[:edge].mean())
        closing = float(means[-edge:].mean())
        middle_slice = means[edge:-edge] if n_buckets > 2 * edge else means
        middle = float(middle_slice.mean())
        trough = float(means.min())
        peak = float(means.max())
        ratio = peak / trough if trough > 0 else float("nan")
        trough_at = int(np.argmin(means))

        check(opening > middle, f"{root} : ouverture {opening:.5%} <= milieu {middle:.5%}")
        check(closing > middle, f"{root} : clôture {closing:.5%} <= milieu {middle:.5%}")
        check(
            RATIO_MIN <= ratio <= RATIO_MAX,
            f"{root} : rapport {ratio:.2f} hors de [{RATIO_MIN} ; {RATIO_MAX}]",
        )
        interior = 0 < trough_at < n_buckets - 1
        check(interior, f"{root} : le creux est au bord (tranche {trough_at}), pas au milieu")

        results[root] = {
            "buckets": n_buckets,
            "observations": int(profile["count"].sum()),
            "opening_abs_return": opening,
            "middle_abs_return": middle,
            "closing_abs_return": closing,
            "trough_abs_return": trough,
            "peak_abs_return": peak,
            "ratio_peak_over_trough": ratio,
            "trough_bucket": trough_at,
            "profile": [float(v) for v in means],
        }
        print(f"  {root}  ouverture {opening:.4%} · milieu {middle:.4%} · "
              f"clôture {closing:.4%}")
        print(f"      creux {trough:.4%} (tranche {trough_at}/{n_buckets - 1}) · "
              f"sommet {peak:.4%} · rapport {ratio:.2f} · "
              f"{int(profile['count'].sum()):,} barres".replace(",", " "))

    print("\nC — la périodicité de l'autocorrélation de |r|")
    multiples = [period * m for m in (1, 2, 3)]
    neighbours = [lag + offset for lag in multiples for offset in (-30, -15, 15, 30)]
    for root in ROOTS:
        returns, day, index = cell_returns(panel, root, WINDOW)
        acf = autocorrelation(returns, sorted(set(multiples + neighbours)))
        on = [acf[lag] for lag in multiples if lag in acf]
        off = [acf[lag] for lag in neighbours if lag in acf]
        # Une clause qu'on ne parvient pas à mesurer ne se saute pas : elle
        # échoue. Le premier passage de cet instrument les a sautées toutes les
        # trois et a conclu « les quatre clauses tiennent » -- un verdict de
        # porte prononcé sur trois clauses sur quatre.
        check(bool(on) and bool(off),
              f"{root} : clause C NON MESURÉE — {len(on)} multiples et "
              f"{len(off)} voisins exploitables")
        if not on or not off:
            results[root]["acf_note"] = "décalages inexploitables"
            continue
        check(np.median(on) > np.median(off),
              f"{root} : ACF aux multiples {np.median(on):+.4f} <= voisins {np.median(off):+.4f}")
        results[root]["acf_multiples"] = {str(k): acf[k] for k in multiples if k in acf}
        results[root]["acf_neighbours"] = {str(k): acf[k] for k in neighbours if k in acf}

        # DIAGNOSTIC, ajouté APRÈS la première mesure et n'entrant dans AUCUNE
        # clause. Le témoin de H04 est placé à 15 et 30 minutes du multiple,
        # c'est-à-dire presque à la MÊME PHASE du cycle intra-journalier : il ne
        # pouvait presque rien détecter. À phase opposée -- une demi-séance --
        # l'écart est cinq à sept fois plus grand. La clause C telle qu'écrite
        # mesure donc un PLANCHER de l'effet, pas l'effet (L16).
        opposite = [lag + offset for lag in multiples
                    for offset in (-period // 2, period // 2)]
        acf_far = autocorrelation(returns, sorted(set(opposite)))
        far = [acf_far[lag] for lag in opposite if lag in acf_far]
        results[root]["acf_opposite_phase"] = {
            str(k): acf_far[k] for k in opposite if k in acf_far
        }
        print(f"  {root}  multiples {np.median(on):+.4f} · "
              f"voisins {np.median(off):+.4f} (écart {np.median(on) - np.median(off):+.4f}) · "
              f"phase opposée {np.median(far):+.4f} "
              f"(écart {np.median(on) - np.median(far):+.4f}, diagnostic)")

    print("\nD — le motif tient-il sur les trois indices ?")
    holds = [r for r in ROOTS
             if results[r]["opening_abs_return"] > results[r]["middle_abs_return"]
             and results[r]["closing_abs_return"] > results[r]["middle_abs_return"]]
    check(len(holds) == len(ROOTS),
          f"la forme en U ne tient que sur {len(holds)}/{len(ROOTS)} cellules : {holds}")
    print(f"  {len(holds)}/{len(ROOTS)} : {', '.join(holds) if holds else 'aucune'}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "written": "2026-09-18",
        "hypothesis": "H04",
        "asof": str(panel.asof),
        "slice": panel.slice.name,
        "window": WINDOW,
        "session_minutes": period,
        "bucket_minutes": BUCKET_MINUTES,
        "ratio_bounds": [RATIO_MIN, RATIO_MAX],
        "cells": results,
        "failures": failures,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{checks} vérifications · sortie dans {OUT.relative_to(REPO)}")
    if failures:
        print("H04 : LES CLAUSES NE TIENNENT PAS — la clause 2 reste NON franchie")
        for line in failures:
            print(f"  - {line}")
        print("\n  H04 § Ce que franchir ou ne pas franchir veut dire : le soupçon")
        print("  porte d'abord sur NOTRE dépôt, pas sur le papier.")
        return 1
    print("H04 : les quatre clauses tiennent")
    print("  Ce qui est validé est la CHAÎNE DE DONNÉES et la discipline de mesure,")
    print("  pas le harnais d'IC — qui reste garanti par sa seule calibration à la")
    print("  main, porte 03 (D13).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
