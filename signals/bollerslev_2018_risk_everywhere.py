"""Bollerslev, Hood, Huss, Pedersen (2018), Risk Everywhere — modèle HExp centré, en « Mega » panel.

Ce que la fiche décrit : une prévision directe de la variance réalisée moyenne des
20 jours suivants, RV_LR_t + somme_j beta_j (ExpRV^j_t - RV_LR_t), avec quatre EWMA
des RV quotidiennes (centres de masse 1, 5, 25, 125 jours, tronquées à 500 retards,
lambda = log(1 + 1/CoM)), RV_LR la moyenne en expansion, et des beta estimés par MCO
sur fenêtre en expansion, de préférence en panel commun à tous les actifs (« Mega »).

Ce qui ne se transpose pas, et qui est déclaré : le papier prédit une VARIANCE, jamais
un rendement, et ne donne aucune direction de trade. Le score rendu ici est la variance
prédite elle-même ; le signe attendu vient de la seule hypothèse du papier qui relie
risque et rendement (Sharpe conditionnel supposé constant, donc espérance de rendement
proportionnelle à la volatilité). Le facteur global (HExpGl), le filtre d'aberrations,
l'« insanity filter » et les règles de roulement ne sont pas codés : voir CHOICES.

Ce qui manquait et ce qui a été fait à la place est listé dans CHOICES.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "bollerslev-2018-risk-everywhere"
HYPOTHESIS = None
PAPER = (
    "Tim Bollerslev, Benjamin Hood, John Huss, Lasse Heje Pedersen (2018), "
    "Risk Everywhere: Modeling and Managing Volatility, "
    "The Review of Financial Studies, v. 31 n. 7, 2729-2773"
)
EXPECTED_SIGN = +1
CHOICES = (
    "La fiche prédit une variance réalisée, pas un rendement, et ne donne aucune direction "
    "de trade ; j'ai pris pour score la variance prédite elle-même (modèle HExp centré) et "
    "EXPECTED_SIGN = +1, parce que la seule liaison risque-rendement du papier est son "
    "hypothèse d'un Sharpe conditionnel constant (SR = 0.4), qui rend l'espérance de "
    "rendement croissante avec la volatilité prédite.",
    "Score en variance et non en volatilité : la fiche dit que les résultats principaux "
    "portent sur la variance ; la racine carrée ne changerait de toute façon pas l'ordre.",
    "« Jour » du papier : j'ai pris une séance de la cellule (root, window) telle que la "
    "rend _common.cell_bars ; les jours sans séance sont simplement absents de la suite "
    "(les 20 jours de l'horizon sont les 20 séances présentes suivantes).",
    "RV d'une séance : pour chacune des cinq grilles de 5 minutes, définies sur l'horloge "
    "par la minute entière du jour modulo 5, somme des carrés des rendements log entre "
    "barres consécutives de la grille ; moyenne sur les grilles qui ont au moins un "
    "rendement. J'ai supposé des barres horodatées à la minute ; aucun filtre "
    "d'aberrations (1 % autour de la médiane de trois rendements) n'est appliqué, la "
    "fiche laissant ambigu le caractère passé ou centré de la médiane.",
    "Rendement « overnight » : log de la première clôture de la séance sur la dernière "
    "clôture de la séance précédente de la même cellule, au carré, attribué à la séance "
    "qui ouvre ; absent pour la première séance. Une séance dont la RV n'est pas finie "
    "(prix non positifs, une seule barre sans overnight) est écartée de la suite.",
    "Timing : la fiche forme la prévision à la fin du jour t ; le score d'une séance est "
    "posé par _common.run à la barre d'ancrage de la séance et n'utilise que les séances "
    "ANTÉRIEURES complètes (origine t = séance précédente). La séance en cours n'entre pas "
    "dans la RV, car elle n'est pas finie.",
    "EWMA : poids e^(-i*lambda), i = 1..500, sur RV_t, RV_(t-1), ... ; quand l'historique "
    "est plus court que 500 séances (ambiguïté laissée null), les poids sont renormalisés "
    "sur les retards disponibles.",
    "RV_LR : moyenne en expansion de toutes les RV de la cellule jusqu'à l'origine incluse.",
    "Schéma d'estimation : « Mega », comme le préfère la fiche — un seul jeu de beta commun "
    "à toutes les cellules (root, window) du panel, chaque cellule comptant comme un actif. "
    "Équation (9) sans intercept ni effets fixes (ambiguïté laissée null ; j'ai suivi la "
    "lettre de l'équation).",
    "Observations de l'estimation (ambiguïté laissée null) : seules les paires dont la cible "
    "(moyenne des RV des 20 séances suivantes) est entièrement réalisée — dernière barre de "
    "la séance t+20 strictement antérieure au début de la séance notée — entrent dans la "
    "régression ; aucun look-ahead.",
    "Fréquence de réestimation (non donnée) : à chaque séance notée, sur toutes les paires "
    "réalisées jusque-là (fenêtre en expansion, sommes cumulées de X'X et X'y). Si X'X n'est "
    "pas de rang plein, aucun score.",
    "Historique minimal « 1 full calendar year » : interprété comme une paire admise "
    "seulement si son origine est au moins un an (pd.DateOffset(years=1)) après la première "
    "barre de la cellule, plutôt qu'une année civile complète au sens strict.",
    "Univers : les exact_roots de la fiche (ES, CL, GC, 6E, 6B, 6J, 6A) ne filtrent pas les "
    "cellules ; la thèse du papier est la communauté du risque entre tous les actifs, et le "
    "modèle est appliqué à toutes les cellules du panel.",
    "Non codés, et déclarés : HExpGl (le facteur global GlRV perd son sens sur neuf futures, "
    "dit la fiche), l'« insanity filter » (ambiguïté laissée null pour le HExp), la règle "
    "d'omission des 5 dernières minutes pour le roulement (le recollage est celui de "
    "_common.cell_bars).",
)

_HORIZON_DAYS = 20
_CENTERS_OF_MASS = (1, 5, 25, 125)
_TRUNCATION_LAGS = 500
_SAMPLING_MINUTES = 5
_SUBSAMPLE_GRIDS = 5
_MIN_HISTORY_YEARS = 1


def _session_table(closes: pd.Series, sessions: pd.Series):
    """Séances complètes ordonnées : (débuts ns, fins ns, RV)."""
    closes = closes.sort_index()
    sessions = sessions.reindex(closes.index)
    groups = []
    for _, idx in closes.groupby(sessions.values, sort=False).groups.items():
        sub = closes.loc[idx].sort_index()
        if len(sub) == 0:
            continue
        groups.append(sub)
    groups.sort(key=lambda s: s.index[0])

    starts, ends, rvs = [], [], []
    prev_last = None
    for sub in groups:
        values = sub.to_numpy(dtype=float)
        with np.errstate(divide="ignore", invalid="ignore"):
            logc = np.where(values > 0, np.log(np.where(values > 0, values, 1.0)), np.nan)
        minutes = (sub.index.hour * 60 + sub.index.minute).to_numpy()
        grid_rvs = []
        for g in range(_SUBSAMPLE_GRIDS):
            lc = logc[minutes % _SAMPLING_MINUTES == g]
            if len(lc) < 2:
                continue
            r = np.diff(lc)
            r = r[np.isfinite(r)]
            if len(r) == 0:
                continue
            grid_rvs.append(float(np.sum(r * r)))
        intraday = float(np.mean(grid_rvs)) if grid_rvs else math.nan

        overnight_sq = math.nan
        if prev_last is not None and values[0] > 0 and prev_last > 0:
            on = math.log(values[0] / prev_last)
            overnight_sq = on * on
        prev_last = values[-1]

        if math.isfinite(intraday) and math.isfinite(overnight_sq):
            rv = intraday + overnight_sq
        elif math.isfinite(intraday):
            rv = intraday
        elif math.isfinite(overnight_sq):
            rv = overnight_sq
        else:
            continue
        starts.append(sub.index[0].value)
        ends.append(sub.index[-1].value)
        rvs.append(rv)
    return (
        np.asarray(starts, dtype=np.int64),
        np.asarray(ends, dtype=np.int64),
        np.asarray(rvs, dtype=float),
    )


def _features(rv: np.ndarray):
    """Pour chaque origine t : RV_LR_t et les quatre ExpRV^CoM_t (RV jusqu'à t incluse)."""
    n = len(rv)
    lr = np.cumsum(rv) / np.arange(1, n + 1)
    exp = np.full((n, len(_CENTERS_OF_MASS)), np.nan)
    lags = np.arange(1, _TRUNCATION_LAGS + 1)
    for j, com in enumerate(_CENTERS_OF_MASS):
        lam = math.log(1 + 1 / com)
        w_full = np.exp(-lam * lags)
        for t in range(n):
            lo = max(0, t + 1 - _TRUNCATION_LAGS)
            seg = rv[lo : t + 1][::-1]
            w = w_full[: len(seg)]
            exp[t, j] = float(np.dot(w, seg) / np.sum(w))
    return lr, exp


def _cell_model(panel, root, window):
    closes, sessions = _common.cell_bars(panel, root, window)
    if closes is None or len(closes) == 0:
        return None
    starts, ends, rv = _session_table(closes, sessions)
    if len(rv) == 0:
        return None
    lr, exp = _features(rv)
    first_ts = pd.Timestamp(closes.sort_index().index[0])
    min_origin = (first_ts + pd.DateOffset(years=_MIN_HISTORY_YEARS)).value

    xs, ys, times = [], [], []
    for t in range(len(rv) - _HORIZON_DAYS):
        if ends[t] < min_origin:
            continue
        x = exp[t] - lr[t]
        y = float(np.mean(rv[t + 1 : t + 1 + _HORIZON_DAYS])) - lr[t]
        if not (np.all(np.isfinite(x)) and math.isfinite(y)):
            continue
        xs.append(x)
        ys.append(y)
        times.append(ends[t + _HORIZON_DAYS])
    return {
        "starts": starts,
        "ends": ends,
        "lr": lr,
        "exp": exp,
        "xs": xs,
        "ys": ys,
        "times": times,
    }


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} — variance prédite à 20 séances, HExp « Mega »."""
    all_cells = list(panel.cells())
    wanted = all_cells if cells is None else [c for c in cells if c in set(all_cells)]

    models = {}
    for root, window in all_cells:
        m = _cell_model(panel, root, window)
        if m is not None:
            models[(root, window)] = m

    k = len(_CENTERS_OF_MASS)
    xs, ys, times = [], [], []
    for cell in all_cells:
        m = models.get(cell)
        if m is None:
            continue
        xs.extend(m["xs"])
        ys.extend(m["ys"])
        times.extend(m["times"])
    if not xs:
        return {}
    X = np.asarray(xs, dtype=float).reshape(-1, k)
    Y = np.asarray(ys, dtype=float)
    T = np.asarray(times, dtype=np.int64)
    order = np.argsort(T, kind="stable")
    X, Y, T = X[order], Y[order], T[order]
    cum_xtx = np.cumsum(np.einsum("ni,nj->nij", X, X), axis=0)
    cum_xty = np.cumsum(X * Y[:, None], axis=0)

    out = {}
    for cell in wanted:
        m = models.get(cell)
        if m is None:
            continue

        def predictor(closes, position, m=m):
            start = closes.index[0].value
            n_prior = int(np.sum(m["ends"] < start))
            if n_prior == 0:
                return None
            origin = n_prior - 1
            c = int(np.searchsorted(T, start, side="left"))
            if c == 0:
                return None
            A = cum_xtx[c - 1]
            b = cum_xty[c - 1]
            if np.linalg.matrix_rank(A) < k:
                return None
            beta = np.linalg.solve(A, b)
            x = m["exp"][origin] - m["lr"][origin]
            forecast = float(m["lr"][origin] + np.dot(beta, x))
            if not math.isfinite(forecast):
                return None
            return forecast

        res = _common.run(panel, predictor, cells=[cell], horizon_bars=horizon_bars)
        for key, series in res.items():
            if series is not None and len(series) > 0:
                out[key] = series
    return out
