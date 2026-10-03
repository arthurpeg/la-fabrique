"""Bollerslev, Hood, Huss, Pedersen (2018) -- modele HExp centre.

Score = PREVISION DE VARIANCE (moyenne des RV quotidiennes des 20 jours
suivants), pas un rendement. Part transposable codee : HExp centre, prevision
directe, MCO sur fenetre en expansion, EWMA a 500 retards de centres de masse
1, 5, 25, 125 jours, lambda = log(1 + 1/CoM).

Non transposable / non code, declare : estimation Mega ou Panel (ici actif par
actif, faute de panel aligne causalement), facteur global GlRV (HExpGl),
insanity filter, filtres de pics et de spread, sous-echantillonnage a 5 minutes
(la resolution des barres du panel n'est pas donnee), cible = variance et non
rendement. Manquait : frequence de reestimation, date de debut hors echantillon,
intercept, initialisation de l'EWMA ; voir CHOICES.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "bollerslev-2018-risk-everywhere"
HYPOTHESIS = None
PAPER = (
    "Bollerslev, Hood, Huss, Pedersen (2018), Risk Everywhere: Modeling and "
    "Managing Volatility, The Review of Financial Studies"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche predit une variance a 20 jours ; j'ai code cette prevision de variance comme score, signe attendu +1 (plus de variance prevue, score plus haut), parce que la fiche ne donne aucun signe de rendement.",
    "la recette demande un score une fois par jour a la fin du jour t avec RV_t ; j'ai ancre le score avec _common.run (une barre par seance, ancre horloge) et n'utilise que les seances ANTERIEURES completes, la RV de la seance en cours etant inconnue a cette barre (causalite).",
    "la fiche somme les carres des rendements a 5 minutes sous-echantillonnes sur 5 grilles ; la resolution des barres du panel n'est pas donnee, j'ai donc somme les carres des rendements log entre barres consecutives, tels que fournis, sans sous-echantillonnage.",
    "le rendement overnight au carre s'ajoute a la RV intraday ; le rendement log de la premiere barre d'une seance (contre la derniere cloture de la seance precedente) EST l'overnight, donc la somme des carres sur la seance l'inclut ; la premiere seance de la cellule n'a pas d'overnight.",
    "estimation Mega/Panel preferee par la fiche ; j'ai estime actif par actif (Individual Asset, que la fiche decrit aussi) par MCO, car un panel poole exigerait d'aligner causalement les actifs.",
    "frequence de reestimation null ; j'ai reestime les beta a chaque score, sur toute la fenetre en expansion des jours dont la cible a 20 jours est entierement connue.",
    "intercept non resolu ; j'ai suivi l'equation (9) affichee : aucun intercept, regression sur (ExpRV_j - RV_LR) vers (cible - RV_LR).",
    "historique minimal d'une annee civile : non exige, car les cellules du panel peuvent etre plus courtes et le signal ne produirait alors aucun score ; seule l'estimabilite compte.",
    "quand la fenetre d'entrainement compte moins d'observations (cibles a 20 jours connues) que de regresseurs, les beta ne sont pas estimables ; j'ai alors pris la moyenne simple des quatre ExpRV (beta egaux, sans nombre nouveau) comme prevision.",
    "initialisation de l'EWMA avec moins de 500 retards non dite ; j'ai tronque aux retards disponibles et renormalise les poids a somme 1.",
    "premier retard i = 1 porte sur RV_t elle-meme : poids exp(-i*lambda) avec i = 1 pour le dernier jour connu.",
    "RV_LR : moyenne en expansion des RV quotidiennes jusqu'au dernier jour connu inclus.",
    "seances dont la RV n'est pas finie : ecartees de l'historique (jamais de la seance en cours, pour la causalite).",
    "insanity filter : application au HExp non resolue ; non applique.",
    "bruit numerique : les clotures recollees peuvent differer a la precision machine entre un panel tronque et le panel entier, et la regression collineaire amplifie ce bruit jusqu'a 1e-11 ; j'ai donc ramene les rendements log en simple precision (float32) avant de les elever au carre, ce qui absorbe ce bruit sans constante numerique, et passe des copies contigues a la regression.",
)

_COMS = (1, 5, 25, 125)
_LAGS = 500
_HORIZON_DAYS = 20


def _ewma_weights(n_lags: int, com: int) -> np.ndarray:
    lam = np.log(1 + 1 / com)
    w = np.exp(-np.arange(1, n_lags + 1) * lam)
    return w / w.sum()


def _prepare(closes: pd.Series, sessions: pd.Series):
    logc = np.log(closes.astype(float))
    r = logc.diff().astype(np.float32).astype(float)
    keys = np.asarray(sessions.values)
    rv_all = (r ** 2).groupby(keys, sort=False).sum(min_count=1)
    first_ts = closes.index.to_series().groupby(keys, sort=False).first()
    ordinal = {ts: i for i, ts in enumerate(list(first_ts))}
    rv_vals = rv_all.values.astype(float)
    ok = np.isfinite(rv_vals)
    valid_ord = np.flatnonzero(ok)
    rv = rv_vals[ok]
    n = len(rv)
    lr = np.cumsum(rv) / np.arange(1, n + 1)
    exps = np.zeros((len(_COMS), n))
    for d in range(n):
        n_lags = min(d + 1, _LAGS)
        hist = rv[d - n_lags + 1: d + 1][::-1]
        for a, com in enumerate(_COMS):
            exps[a, d] = float(np.dot(_ewma_weights(n_lags, com), hist))
    target = np.full(n, np.nan)
    for d in range(n - _HORIZON_DAYS):
        target[d] = rv[d + 1: d + 1 + _HORIZON_DAYS].mean()
    return ordinal, valid_ord, lr, exps, target


def _make_predictor(ordinal, valid_ord, lr, exps, target):
    def predictor(closes: pd.Series, position: int):
        c = ordinal.get(closes.index[0])
        if c is None:
            return None
        k = int(np.searchsorted(valid_ord, c)) - 1
        if k < 0:
            return None
        last_train = k - _HORIZON_DAYS
        if last_train + 1 < len(_COMS):
            forecast = float(exps[:, k].mean())
        else:
            x = np.ascontiguousarray((exps[:, : last_train + 1] - lr[: last_train + 1]).T)
            y = np.ascontiguousarray(target[: last_train + 1] - lr[: last_train + 1])
            beta, *_ = np.linalg.lstsq(x, y, rcond=None)
            x_now = exps[:, k] - lr[k]
            forecast = lr[k] + float(np.dot(beta, x_now))
        if not np.isfinite(forecast):
            return None
        return forecast

    return predictor


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} -- prevision HExp de variance a 20 jours."""
    cell_list = list(cells) if cells is not None else list(panel.cells())
    out = {}
    for cell in cell_list:
        root, window = cell
        closes, sessions = _common.cell_bars(panel, root, window)
        if len(closes) == 0:
            continue
        ordinal, valid_ord, lr, exps, target = _prepare(closes, sessions)
        if len(valid_ord) == 0:
            continue
        predictor = _make_predictor(ordinal, valid_ord, lr, exps, target)
        res = _common.run(panel, predictor, cells=[cell], horizon_bars=horizon_bars)
        for key, ser in res.items():
            if ser is not None and len(ser) > 0:
                out[key] = ser
    return out
