"""Bollerslev, Hood, Huss, Pedersen (2018) - modele HExp centre, version transposee.

Ce que le papier fait : prevoir la VARIANCE realisee moyenne des 20 prochains
jours, RV_LR + somme_j beta_j (ExpRV^j - RV_LR), j de centre de masse 1, 5, 25,
125 jours, EWMA tronquees a 500 retards, lambda = log(1 + 1/CoM), MCO sur
fenetre en expansion.

Ce qui ne se transpose pas et que je declare :
- la cible est une variance, pas un rendement : le score est une variance
  predite, le papier ne donne aucune direction de trade ;
- RV a 5 minutes sous-echantillonnee, filtre d'aberrations, roulement : non
  reproduits, les barres du panel sont prises telles quelles ;
- HExpGl (facteur global), estimation Panel/Mega : non codes, voir CHOICES.
Aucun parametre invente : tous les nombres viennent de la recette.

Le papier exige au moins 1 annee civile complete de RV avant d'estimer : c'est
code, et cela evite aussi les regressions sur quelques paires, tres mal
conditionnees, dont le resultat bougeait avec le moindre ecart des clotures
recollees.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "bollerslev-2018-risk-everywhere"
HYPOTHESIS = None
PAPER = (
    "Bollerslev, Hood, Huss, Pedersen (2018), Risk Everywhere: Modeling and "
    "Managing Volatility, The Review of Financial Studies 31(7)"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche ne donne aucune direction de trade (cible = variance) ; j'ai pris EXPECTED_SIGN = +1 (variance predite elevee = score eleve), parce qu'il faut un signe non nul et que c'est le plus simple, sans que le papier l'affirme",
    "la fiche propose individuel, Panel ou Mega ; j'ai estime les beta par MCO actif par actif (une cellule a la fois), parce que le Mega demande de melanger des cellules de seances differentes sans regle de calendrier donnee ; c'est une diminution declaree",
    "HExpGl (facteur global, decalage d'un jour) non code : il exige des horaires par actif que la fiche ne donne pas ; seul HExp est code",
    "la RV quotidienne est la somme des carres des rendements log entre barres consecutives de la cellule, regroupes par seance, premier rendement de la seance (raccord avec la cloture precedente) inclus comme rendement overnight au carre ; pas d'echantillonnage a 5 minutes ni de sous-echantillonnage, parce que la frequence des barres du panel est donnee et que la fiche ne permet pas de la changer",
    "pas de filtre d'aberrations ni de regle de roulement propre : les clotures recollees de cell_bars sont prises telles quelles",
    "intercept : equation (9) sans intercept, donc MCO sans constante sur les variables centrees, sans effets fixes",
    "observations d'estimation au score de la seance k : seules les paires (s, cible RV moyenne des jours s+1..s+20) dont la cible est entierement realisee avant la fin de la seance k-1 (s + 20 <= k-1) ; la fiche ne le dit pas, c'est le choix sans look-ahead",
    "reestimation des coefficients a chaque seance (fenetre en expansion), la frequence n'etant pas donnee ; c'est le choix le plus simple",
    "EWMA tronquee a 500 retards : quand l'historique est plus court, poids renormalises sur les retards disponibles plutot que d'attendre 500 jours",
    "minimum d'une annee civile complete de RV (fiche : 1 full calendar year) : lu comme 'aucun score avant l'annee civile qui suit la premiere annee civile complete de la cellule', soit annee de la derniere seance connue >= annee de la premiere barre + 2 ; la premiere annee, souvent partielle, n'est pas comptee comme complete",
    "insanity filter non applique (la fiche ne dit pas s'il vise HExp)",
    "ancrage : une barre par seance et par cellule, celle que _common.run choisit sur l'horloge ; le score y est la prevision formee avec les seances completes precedentes (RV de la seance courante non utilisee)",
    "variance et non volatilite : score en variance, comme les resultats principaux",
    "MCO resolu par equations normales et elimination de Gauss a pivot partiel avec sommes fsum, pour un calcul deterministe ; systeme singulier : pas de score",
)

_COMS = (1, 5, 25, 125)
_TRUNC = 500
_H = 20
_MIN_YEARS = 1


def _ewma(rv: np.ndarray, s: int, lam: float) -> float:
    lo = max(0, s + 1 - _TRUNC)
    window = rv[lo : s + 1][::-1]
    lags = np.arange(1, len(window) + 1)
    w = np.exp(-lags * lam)
    return math.fsum((w * window).tolist()) / math.fsum(w.tolist())


def _solve(x: np.ndarray, t: np.ndarray):
    """MCO sans constante par equations normales, Gauss a pivot partiel."""
    k = x.shape[1]
    a = [
        [math.fsum((x[:, i] * x[:, j]).tolist()) for j in range(k)]
        + [math.fsum((x[:, i] * t).tolist())]
        for i in range(k)
    ]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(a[r][c]))
        if a[p][c] == 0 or not math.isfinite(a[p][c]):
            return None
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, k):
            f = a[r][c] / a[c][c]
            for m in range(c, k + 1):
                a[r][m] -= f * a[c][m]
    beta = [0.0] * k
    for i in range(k - 1, -1, -1):
        beta[i] = (a[i][k] - math.fsum(a[i][j] * beta[j] for j in range(i + 1, k))) / a[i][i]
    return beta


def _forecasts(rv: np.ndarray, years: np.ndarray) -> np.ndarray:
    """Prevision formee en fin de seance s (indice), NaN si absente."""
    n = len(rv)
    lams = [math.log(1 + 1 / c) for c in _COMS]
    lr = np.array([math.fsum(rv[: s + 1].tolist()) / (s + 1) for s in range(n)])
    feats = np.empty((n, len(_COMS)))
    for s in range(n):
        for j, lam in enumerate(lams):
            feats[s, j] = _ewma(rv, s, lam) - lr[s]
    # cible centree, definie seulement quand realisee (s + H < n)
    y = np.full(n, np.nan)
    for s in range(n - _H):
        y[s] = math.fsum(rv[s + 1 : s + _H + 1].tolist()) / _H - lr[s]
    out = np.full(n, np.nan)
    for s in range(n):
        if years[s] < years[0] + _MIN_YEARS + 1:
            continue  # pas encore une annee civile complete de RV
        last = s - _H  # derniere paire dont la cible est realisee a la fin de s
        if last + 1 <= len(_COMS):
            continue
        beta = _solve(feats[: last + 1], y[: last + 1])
        if beta is None:
            continue
        out[s] = lr[s] + math.fsum(float(feats[s, j]) * beta[j] for j in range(len(_COMS)))
    return out


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series}."""
    anchors = _common.run(panel, lambda closes, position: 1.0, cells, horizon_bars)
    result = {}
    for key, anchor in anchors.items():
        if anchor is None or len(anchor) == 0:
            continue
        root, window = key
        closes, sessions = _common.cell_bars(panel, root, window)
        logc = np.log(closes.astype(float))
        r2 = logc.diff() ** 2
        rv = r2.groupby(sessions.values, sort=False).sum()
        first_ts = pd.Series(closes.index, index=closes.index).groupby(
            sessions.values, sort=False
        ).first()
        years = np.array([t.year for t in first_ts.loc[rv.index]])
        order = pd.Index(rv.index)
        fc = _forecasts(rv.to_numpy(dtype=float), years)
        sess_at = sessions.reindex(anchor.index)
        pos = order.get_indexer(sess_at.values)
        vals = []
        idx = []
        for ts, k in zip(anchor.index, pos):
            if k < 1:
                continue
            v = fc[k - 1]
            if np.isnan(v):
                continue
            vals.append(v)
            idx.append(ts)
        if not vals:
            continue
        result[key] = pd.Series(vals, index=pd.DatetimeIndex(idx), dtype=float)
    return result
