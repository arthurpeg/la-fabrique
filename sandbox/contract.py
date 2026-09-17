"""What a signal IS. The shape, checked, before anything is measured on it.

The harness receives scores and is deliberately ignorant of what produced them
(D04). This module is the other half of that ignorance: it says what a signal
module must expose and what its output must look like, so that `evaluate` never
has to guess and never has to trust.

Nothing here is about whether a signal is any GOOD. It is about whether it is a
signal at all.
"""

from __future__ import annotations

import pandas as pd

from panel.panel import Panel

REQUIRED_ATTRS = ("SIGNAL_ID", "HYPOTHESIS", "PAPER", "EXPECTED_SIGN")


class ContractViolation(Exception):
    """The module does not meet the signal contract (D07)."""


def validate_module(module) -> list[str]:
    """What the module must declare about itself, before it is run."""
    bad: list[str] = []
    for attr in REQUIRED_ATTRS:
        if not hasattr(module, attr):
            bad.append(f"{attr} manquant")
    if not callable(getattr(module, "scores", None)):
        bad.append("scores(panel, cells, horizon_bars) manquant ou non appelable")

    signal_id = getattr(module, "SIGNAL_ID", None)
    if not isinstance(signal_id, str) or not signal_id.strip():
        bad.append(f"SIGNAL_ID vaut {signal_id!r} : une chaîne non vide est attendue")

    hypothesis = getattr(module, "HYPOTHESIS", None)
    if hypothesis is not None and not (
        isinstance(hypothesis, str) and hypothesis.startswith("H")
    ):
        bad.append(
            f"HYPOTHESIS vaut {hypothesis!r} : un identifiant de hypotheses/ (H01, H02...) "
            "ou None pour un signal qui n'affirme encore rien"
        )

    sign = getattr(module, "EXPECTED_SIGN", None)
    if sign not in (-1, +1):
        bad.append(
            f"EXPECTED_SIGN vaut {sign!r} : +1 ou -1, jamais 0 ni None. Un signal dont "
            "on n'attend aucun signe est un signal dont on n'attend rien (invariant IV)"
        )
    return bad


def validate_scores(scores, panel: Panel) -> list[str]:
    """What the output must look like, before the harness is allowed to see it."""
    bad: list[str] = []
    if not isinstance(scores, dict):
        return [f"scores() rend un {type(scores).__name__}, pas un dictionnaire"]
    if not scores:
        return ["scores() ne rend aucune cellule"]

    retained = set(panel.cells())
    for key, series in scores.items():
        if not (isinstance(key, tuple) and len(key) == 2):
            bad.append(f"clé {key!r} : une paire (root, window) est attendue")
            continue
        if key not in retained:
            bad.append(f"{key} n'est pas une cellule retenue à cet as-of (D01 3)")
        if not isinstance(series, pd.Series):
            bad.append(f"{key} : {type(series).__name__} au lieu d'une Series")
            continue
        if series.empty:
            bad.append(
                f"{key} : série vide — une cellule sans score s'omet, elle ne se déclare pas"
            )
            continue
        index = series.index
        if not isinstance(index, pd.DatetimeIndex) or index.tz is None:
            bad.append(f"{key} : l'index n'est pas un DatetimeIndex localisé")
            continue
        if not index.is_monotonic_increasing:
            bad.append(f"{key} : index non trié")
        if index.has_duplicates:
            bad.append(f"{key} : timestamps en double")
        if index.max() > panel.asof:
            bad.append(
                f"{key} : un score est daté {index.max()}, après l'as-of {panel.asof} — "
                "le Panel l'interdit, le signal ne devrait pas pouvoir le fabriquer"
            )
        values = pd.to_numeric(series, errors="coerce")
        if not values.notna().all():
            bad.append(f"{key} : score non numérique ou NaN — un score absent s'omet")
    return bad


def enforce(module, scores, panel: Panel) -> None:
    """Raise unless both halves of the contract hold."""
    bad = validate_module(module) + validate_scores(scores, panel)
    if bad:
        raise ContractViolation("; ".join(bad))
