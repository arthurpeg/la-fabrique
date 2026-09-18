"""H03 -- continuation aux décalages multiples exacts d'une séance.

Heston, Korajczyk & Sadka (2010), "Intraday Patterns in the Cross-section of
Stock Returns", JF 65(4):1369-1407 (corpus/AMORCE.md entrée 3, fiche
corpus/fiches/heston-2010-intraday-periodicity.json). Cible de la clause 2 de la
porte 06 (D12).

CE QUI CHANGE PAR RAPPORT AUX DEUX ÉTALONS. `gao_2018` et `baltussen_2021`
produisent UN score par séance, à l'ancre de fin de fenêtre : leur hypothèse
porte sur la dernière demi-heure. Celle-ci porte sur TOUTES les demi-heures, donc
le score est produit à chaque début d'intervalle de trente minutes -- treize par
séance en US et EUROPE, seize en ASIA. Le mécanisme de `_common.run` ne convient
pas et n'est pas réutilisé.

LE MOTIF, ET POURQUOI IL EST MESURÉ PAR UN PARAMÈTRE DE DÉCALAGE. Ce qui est
affirmé n'est pas un IC mais un PEIGNE : positif aux décalages multiples d'une
séance, négatif aux tout premiers, et rien de positif entre les deux. Le même
code sert donc les trois clauses de H03, en changeant seulement le décalage :

    scores(panel, lag_sessions=m)     les dents   -- attendu POSITIF
    scores(panel, lag_intervals=j)    les creux   -- attendu NÉGATIF ou nul

`lag_sessions` compte en séances et se traduit en intervalles PAR FENÊTRE : la
période est celle du catalogue, 13 demi-heures pour une fenêtre de 6,5 h et 16
pour une de 8 h. Elle est dictée par la grille et non par le résultat, et un
ajustement après coup se verrait (H03 § Ce qui est affirmé).

LE RENDEMENT D'INTERVALLE EST DÉFINI EN BARRES, PAS EN MINUTES. Le harnais
mesure sa cible par `shift(-horizon_bars)` à l'intérieur de la séance et de la
fenêtre, soit trente BARRES. Un score construit sur trente MINUTES d'horloge
mesurerait autre chose dès qu'une minute manque, et l'écart serait invisible.
La même définition est donc reprise ici, à la barre près.

CAUSALITÉ. Le score de l'intervalle `n` est le rendement de l'intervalle `n - k`,
strictement antérieur. Il lit au plus la barre qui ouvre l'intervalle `n` --
celle qu'il score --, jamais au-delà. `sandbox/causality.py` le vérifie en
tronquant le panel.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from panel.panel import Panel
from panel.sessions import local
from signals import _common

SIGNAL_ID = "heston-2010-periodicity"
HYPOTHESIS = "H03"
PAPER = (
    "Heston, Korajczyk & Sadka (2010), Intraday Patterns in the Cross-section "
    "of Stock Returns, JF 65(4):1369-1407"
)
# Le signe de la clause A, celle qui porte le nom du papier. La clause B attend
# l'inverse au même titre -- c'est le motif entier qui est affirmé, pas un signe.
EXPECTED_SIGN = +1

INTERVAL_BARS = 30
MINUTES = 60.0


def minutes_from_open(index: pd.DatetimeIndex, panel: Panel, window: str) -> pd.Series:
    """Combien de minutes séparent chaque barre de l'ouverture de sa fenêtre.

    En minutes ENTIÈRES, et pour la raison de L10 : calculée en heures
    fractionnaires, la comparaison d'horloge décale l'ancre d'une barre sans
    lever la moindre exception.

    Le modulo porte la fenêtre ASIA, qui enjambe minuit : 02:00 est à 420 minutes
    d'une ouverture à 19:00, pas à -1 020.
    """
    start = panel.catalogue.windows[window].start_hour
    start_minutes = int(round(start * MINUTES))
    clock = local(index, panel.catalogue.timezone)
    minutes = clock.hour * 60 + clock.minute
    return pd.Series((minutes - start_minutes) % (24 * 60), index=index, dtype="int64")


def intervals_per_session(panel: Panel, window: str) -> int:
    """La période du peigne, lue sur le catalogue -- 13 pour 6,5 h, 16 pour 8 h."""
    spec = panel.catalogue.windows[window]
    span = (24 - spec.start_hour + spec.end_hour) if spec.crosses_midnight else (
        spec.end_hour - spec.start_hour
    )
    return int(round(span * MINUTES / INTERVAL_BARS))


def _interval_returns(
    close: pd.Series, sessions: pd.Series, window_minutes: pd.Series
) -> tuple[np.ndarray, np.ndarray]:
    """Les rendements de demi-heure d'une cellule, et la barre qui ouvre chacun.

    Rend deux tableaux alignés : la position, dans la série de la cellule, de la
    barre qui ouvre chaque intervalle, et le rendement de cet intervalle sur
    trente barres. Un intervalle dont les trente barres sortent de la séance rend
    NaN -- c'est exactement ce que le harnais jette de son côté.
    """
    values = close.to_numpy(dtype=float)
    session_key = sessions.to_numpy()
    slot = (window_minutes.to_numpy() // INTERVAL_BARS).astype(np.int64)

    # La barre qui OUVRE chaque intervalle : la première de chaque couple
    # (séance, numéro d'intervalle). Les couples se suivent dans l'ordre du
    # temps, donc un changement de l'un ou de l'autre ouvre un intervalle.
    changed = np.empty(len(values), dtype=bool)
    changed[0] = True
    changed[1:] = (slot[1:] != slot[:-1]) | (session_key[1:] != session_key[:-1])
    anchors = np.flatnonzero(changed)

    ends = anchors + INTERVAL_BARS
    inside = ends < len(values)
    returns = np.full(len(anchors), np.nan, dtype=float)
    if inside.any():
        usable = anchors[inside]
        end_positions = ends[inside]
        # La barre d'arrivée doit appartenir à la MÊME séance : sans ce contrôle,
        # un intervalle de fin de fenêtre emprunterait son rendement à la séance
        # suivante, ce que le harnais ne fait jamais pour sa cible.
        same = session_key[end_positions] == session_key[usable]
        start_values = values[usable]
        end_values = values[end_positions]
        positive = start_values > 0
        ok = same & positive
        computed = np.full(len(usable), np.nan, dtype=float)
        computed[ok] = end_values[ok] / start_values[ok] - 1.0
        returns[inside] = computed
    return anchors, returns


def scores(
    panel: Panel,
    cells=None,
    horizon_bars: int = INTERVAL_BARS,
    *,
    lag_sessions: int | None = 1,
    lag_intervals: int | None = None,
) -> dict[tuple[str, str], pd.Series]:
    """Le rendement du même intervalle, `k` intervalles plus tôt.

    `lag_intervals` l'emporte quand il est donné : il fixe le décalage en
    intervalles, identique dans toutes les fenêtres, ce que demandent les creux
    de H03. Sinon le décalage vaut `lag_sessions` séances, donc un nombre
    d'intervalles qui DÉPEND de la fenêtre.
    """
    if horizon_bars != INTERVAL_BARS:
        raise ValueError(
            f"horizon_bars vaut {horizon_bars} : ce signal est défini sur des "
            f"intervalles de {INTERVAL_BARS} barres, et son décalage se compte "
            f"dans la même unité (H03)."
        )
    if lag_intervals is None and lag_sessions is None:
        raise ValueError("il faut un décalage : lag_sessions ou lag_intervals")

    wanted = tuple(cells) if cells is not None else panel.cells()
    out: dict[tuple[str, str], pd.Series] = {}

    for root in sorted({r for r, _ in wanted}):
        for window in sorted({w for r, w in wanted if r == root}):
            close, sessions = _common.cell_bars(panel, root, window)
            if close.empty:
                continue
            lag = (
                int(lag_intervals)
                if lag_intervals is not None
                else int(lag_sessions) * intervals_per_session(panel, window)
            )
            if lag < 1:
                raise ValueError(f"décalage {lag} : il doit valoir au moins 1 intervalle")

            window_minutes = minutes_from_open(close.index, panel, window)
            anchors, returns = _interval_returns(close, sessions, window_minutes)
            if len(anchors) <= lag:
                continue

            # Le score de l'intervalle n est le rendement de l'intervalle n - lag.
            scored_positions = anchors[lag:]
            scored_values = returns[:-lag]
            finite = np.isfinite(scored_values)
            if not finite.any():
                continue

            series = pd.Series(
                scored_values[finite],
                index=close.index[scored_positions[finite]],
                dtype=float,
            )
            if not series.empty:
                out[(root, window)] = series
    return out
