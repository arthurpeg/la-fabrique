"""The controls. What is refused before an IC is ever computed, and what is only flagged.

They live in `harness/` and not beside it, for a reason that is easy to miss:
`registry.code_hash()` fingerprints `harness/*.py` only. A threshold changed one
directory away would change which signals are refused without changing the hash,
and two incomparable results would carry the same judge's number (D08).

THE ORDER MATTERS. `evaluate` runs these BEFORE taking its ticket. A degenerate
signal has produced no IC, so there is nothing to register: refusing it must not
consume a line, or the FDR denominator fills up with tests that never happened.

THE THRESHOLDS ARE WRITTEN BEFORE ANYTHING HAS BEEN SEEN, and they are about the
SIGNAL, never about its result. A threshold adjusted afterwards to let through a
signal one likes is the gentlest form of cheating and the hardest to see later.

AND "99 % OF NaN" IS NOT "99 % OF BARS UNSCORED". The reference signals score one
bar per session out of about 390: 99.7 % of bars carry no score, and that is the
shape of the hypothesis, not a degeneracy. What counts is how many OBSERVATIONS
result. A control written without that distinction would reject the only two
signals the project has.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# Les seuils. Écrits en phase 06, avant la première mesure d'hypothèse.
MIN_OBSERVATIONS = 30        # sous ce compte, le harnais ne mesure pas la cellule
MIN_DISTINCT_SHARE = 0.10    # un score qui prend trois valeurs sur six cents séances
MIN_SURVIVING_CELLS = 2      # un signal sur une seule cellule n'est pas un signal ici
SUSPICIOUS_IC = 0.10         # D01 2 vise 0,018 et 0,031 : au-delà, on cherche l'erreur
PERSISTENT_SCORES = 0.95     # une autocorrélation pareille gonfle l'échantillon effectif
DUPLICATE_RHO = 0.95         # deux signaux corrélés à ce point ne sont pas deux tests


class Degenerate(Exception):
    """The signal was refused before any IC was computed. Nothing was registered."""


@dataclass(frozen=True)
class CellVerdict:
    cell: tuple[str, str]
    kept: bool
    reason: str = ""


def screen(
    scores: dict[tuple[str, str], pd.Series], *, is_test: bool = True
) -> tuple[dict, list[CellVerdict]]:
    """Drop the degenerate cells, refuse the signal if too little survives.

    Returns the surviving scores and one verdict per cell, kept or not, with the
    reason written out. Raises `Degenerate` when there is not enough left to
    measure -- and raises it BEFORE the caller has taken a ticket.

    `is_test` is false for a calibration, and then ONE cell is enough. The
    two-cell floor exists to stop a per-cell diagnostic being promoted into a
    result (D01 4); a calibration promotes nothing -- gate 03 reproduces exactly
    one cell by hand, at 1e-12, and that is the whole point of it. The carve-out
    buys nobody anything either: a calibration carries no hypothesis and never
    reaches the denominator.
    """
    verdicts: list[CellVerdict] = []
    kept: dict[tuple[str, str], pd.Series] = {}

    for cell in sorted(scores):
        series = scores[cell]
        values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
        finite = values[np.isfinite(values)]
        distinct = len(np.unique(finite))

        if len(finite) < MIN_OBSERVATIONS:
            verdicts.append(CellVerdict(
                cell, False,
                f"{len(finite)} scores finis, moins de {MIN_OBSERVATIONS}",
            ))
        elif distinct < 2:
            verdicts.append(CellVerdict(cell, False, "score constant"))
        elif distinct / len(finite) < MIN_DISTINCT_SHARE:
            verdicts.append(CellVerdict(
                cell, False,
                f"{distinct} valeurs distinctes pour {len(finite)} scores, "
                f"moins de {MIN_DISTINCT_SHARE:.0%}",
            ))
        else:
            verdicts.append(CellVerdict(cell, True))
            kept[cell] = series

    floor = MIN_SURVIVING_CELLS if is_test else 1
    if len(kept) < floor:
        refused = [f"{c.cell}: {c.reason}" for c in verdicts if not c.kept]
        detail = (
            f"Refusées : {refused[:5]}" if refused
            else f"Aucune cellule refusée : il n'en a été soumis que {len(scores)}"
        )
        raise Degenerate(
            f"{len(kept)} cellule(s) survivent aux contrôles, il en faut {floor}. "
            f"Aucun IC n'a été calculé et rien n'a été inscrit au registre (D08). {detail}"
        )
    return kept, verdicts


def warnings_for(ic: float, scores: dict[tuple[str, str], pd.Series]) -> tuple[str, ...]:
    """What the report must say out loud. None of it blocks anything.

    Refusing a result because it is too good would be deciding it before seeing
    it. It is computed, registered, and flagged -- an inconvenient number one
    prevents from existing is a number one can no longer explain.
    """
    said: list[str] = []
    if np.isfinite(ic) and abs(ic) > SUSPICIOUS_IC:
        said.append(
            f"IC de {ic:+.4f}, au-delà de {SUSPICIOUS_IC:.2f} : les cibles de D01 2 "
            "valent 0,018 et 0,031. Un tel chiffre appelle une recherche d'erreur "
            "avant une recherche de profit"
        )
    persistent = []
    for cell, series in sorted(scores.items()):
        values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
        rho = _autocorrelation(values)
        if np.isfinite(rho) and rho > PERSISTENT_SCORES:
            persistent.append(f"{cell[0]}x{cell[1]} ({rho:.2f})")
    if persistent:
        said.append(
            "scores très persistants d'une observation à la suivante — "
            f"{', '.join(persistent[:4])} : l'échantillon effectif est plus petit "
            "qu'il n'en a l'air"
        )
    return tuple(said)


def _autocorrelation(values: np.ndarray) -> float:
    finite = values[np.isfinite(values)]
    if len(finite) < 3 or len(np.unique(finite)) < 2:
        return float("nan")
    left, right = finite[:-1], finite[1:]
    if left.std() == 0 or right.std() == 0:
        return float("nan")
    return float(np.corrcoef(left, right)[0, 1])


def duplicate_of(
    scores: dict[tuple[str, str], pd.Series],
    other: dict[tuple[str, str], pd.Series],
) -> float:
    """How alike two signals are, on their shared bars. A rank correlation.

    SCORE AGAINST SCORE, never score against return: this is not an IC and it
    writes nothing. Two signals correlated beyond DUPLICATE_RHO are not two
    tests, and counting them as two would understate the denominator.

    The comparator is here; the store of past signals' scores is not, and D08
    leaves it to phase 11 where the taxonomy needs the same thing.
    """
    left_all: list[np.ndarray] = []
    right_all: list[np.ndarray] = []
    for cell in sorted(set(scores) & set(other)):
        shared = scores[cell].index.intersection(other[cell].index)
        if len(shared) < MIN_OBSERVATIONS:
            continue
        left_all.append(scores[cell].reindex(shared).to_numpy(dtype=float))
        right_all.append(other[cell].reindex(shared).to_numpy(dtype=float))
    if not left_all:
        return float("nan")
    left = _ranks(np.concatenate(left_all))
    right = _ranks(np.concatenate(right_all))
    if left.std() == 0 or right.std() == 0:
        return float("nan")
    return float(np.corrcoef(left, right)[0, 1])


def _ranks(values: np.ndarray) -> np.ndarray:
    order = values.argsort()
    ranks = np.empty(len(values), dtype=float)
    ranks[order] = np.arange(len(values), dtype=float)
    return ranks
