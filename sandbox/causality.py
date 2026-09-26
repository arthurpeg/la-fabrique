"""The test. A signal that needed the future stops producing the same thing without it.

THE IDEA. Take a bar the signal scored, at instant `t`. Truncate the panel AT
`t` -- so the scored bar is still there, and nothing that follows it is. Ask
the signal again. An honest signal gives the identical score: everything it used
was at or before `t`. A signal that read ahead either gives a different number,
or gives none at all, because what it leaned on is gone.

WHY THE PROBES SIT ON THE SCORED BARS. Anywhere else, a cheat is invisible: in
the middle of the panel the future it reads is available on both sides, so both
runs agree and the test learns nothing. The discriminating instant is the edge,
and the edge has to be PUT where the signal works. A causality test that samples
at random is a test that passes everything.

WHY THE INDEX IS COMPARED, NOT ONLY THE VALUES. A signal reading `close[t+30]`
does not return a wrong number on a truncated panel -- it returns nothing there,
the bar being absent. Comparing only shared timestamps would let it through. So a
score the full panel produces and the truncated panel does not is itself the
violation.

WHY AT `t` AND NOT ONE MINUTE LATER (D27). A bar is stamped at its OPEN: the bar
`ts_event = t` closes at t+1min. Truncating at t+1min kept the bar t+1, whose
close is known only at t+2min, so a signal reading ONE bar ahead scored the same
on both panels. Measured: a one-bar cheat passed 14 probes out of 16, caught only
where the quotes had a hole. At a 30-bar horizon that one minute correlates
~0.18 with the target -- ten times the IC this project is looking for.

WHAT THIS DOES NOT PROVE (D07). That the signal is causal everywhere. Only that
it was causal at the instants probed. The proof is empirical, the probes are many
and spread, and `scan.py` stands behind as a second curtain.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from panel.panel import Panel


@dataclass(frozen=True)
class Divergence:
    """One instant at which the signal did not survive losing its future."""

    cell: tuple[str, str]
    probe: pd.Timestamp
    kind: str          # "disparu" | "apparu" | "valeur"
    detail: str

    def __str__(self) -> str:
        root, window = self.cell
        return f"{root}x{window} @ {self.probe} — {self.kind} : {self.detail}"


def probe_instants(
    scores: dict[tuple[str, str], pd.Series], count: int
) -> list[tuple[tuple[str, str], pd.Timestamp]]:
    """Scored bars spread over the cells and over time. Deterministic, no RNG.

    Round-robin over the cells so one instrument cannot carry the whole test, and
    an even stride inside each cell so the probes are not all in the same season.
    """
    cells = sorted(scores)
    if not cells:
        return []
    picked: list[tuple[tuple[str, str], pd.Timestamp]] = []
    per_cell = max(1, count // len(cells))
    for rank, cell in enumerate(cells):
        index = scores[cell].index
        if len(index) == 0:
            continue
        # on évite la toute dernière barre scorée : tronquer après elle ne retire
        # rien, et la sonde ne distinguerait alors personne.
        usable = index[:-1] if len(index) > 1 else index
        # le décalage par cellule étale les sondes dans le TEMPS autant que sur
        # les cellules : sans lui, chaque cellule serait sondée à sa première
        # barre scorée et toutes les sondes tomberaient dans le même mois.
        offset = int(len(usable) * (rank + 0.5) / len(cells))
        stride = max(1, len(usable) // per_cell)
        for step in range(per_cell):
            position = (offset + step * stride) % len(usable)
            picked.append((cell, usable[position]))
            if len(picked) >= count:
                return picked
    return picked


def check(
    module,
    panel: Panel,
    probes: int = 32,
    horizon_bars: int = 30,
    full: dict[tuple[str, str], pd.Series] | None = None,
) -> list[Divergence]:
    """Probe the signal. An empty list is the only acceptable verdict."""
    reference = module.scores(panel, horizon_bars=horizon_bars) if full is None else full
    divergences: list[Divergence] = []

    for cell, instant in probe_instants(reference, probes):
        truncated = panel.truncate(end=instant)
        again = module.scores(truncated, cells=[cell], horizon_bars=horizon_bars)

        expected = reference[cell]
        expected = expected[expected.index <= truncated.asof]
        observed = again.get(cell, pd.Series(dtype=float))

        missing = expected.index.difference(observed.index)
        if len(missing):
            divergences.append(Divergence(
                cell, instant, "disparu",
                f"{len(missing)} score(s) que le panel complet produit disparaissent "
                f"quand on retire le futur, à partir de {missing[0]}",
            ))
        extra = observed.index.difference(expected.index)
        if len(extra):
            divergences.append(Divergence(
                cell, instant, "apparu",
                f"{len(extra)} score(s) apparaissent sur le panel tronqué, à partir de {extra[0]}",
            ))

        shared = expected.index.intersection(observed.index)
        if len(shared):
            left = expected.reindex(shared).to_numpy(dtype=float)
            right = observed.reindex(shared).to_numpy(dtype=float)
            gap = np.abs(left - right)
            worst = int(np.argmax(gap)) if gap.size else 0
            if gap.size and gap[worst] > 1e-12:
                divergences.append(Divergence(
                    cell, instant, "valeur",
                    f"le score du {shared[worst]} vaut {right[worst]:+.6g} sans le futur "
                    f"et {left[worst]:+.6g} avec — écart {gap[worst]:.3g}",
                ))
    return divergences
