"""Bollerslev, Hood, Huss, Pedersen (2018) -- modele HExp centre, prevision de variance a 20 jours.

Ce que code ce module : la part transposable de la fiche. Le papier ne predit
AUCUN rendement : il predit la variance realisee moyenne des 20 seances
suivantes. Le score rendu est cette prevision de variance (HExp centre),
calculee cellule par cellule ((root, window)), une fois par seance, a l'ancre
d'horloge de `_common.run`.

    prevision_t = RV_LR_t + sum_j beta_j (ExpRV^j_t - RV_LR_t),  j in {1, 5, 25, 125}

- RV quotidienne : somme des carres des rendements log a 5 barres, moyennee sur
  5 grilles decalees d'une barre, plus le rendement "overnight" au carre
  (derniere cloture de la seance precedente -> premiere cloture de la seance).
- RV_LR : moyenne en expansion des RV quotidiennes jusqu'a t inclus.
- ExpRV^CoM : EWMA tronquee a 500 retards, poids exp(-i * lambda) normalises,
  lambda = log(1 + 1/CoM).
- betas : MCO sans intercept, en expansion, sur les observations quotidiennes
  chevauchantes dont la cible a 20 seances est entierement close avant la
  seance notee. Resolution directe par moindres carres sur la matrice des
  regresseurs (pas d'equations normales), pour ne pas elever au carre le
  conditionnement de facteurs EWMA tres colineaires.

Ce qui manquait ou ne se transpose pas : pas de facteur global (HExpGl), pas
d'estimation "Mega" (estimation cellule par cellule), pas d'insanity filter, pas
de filtres de pics / spreads / heures liquides, frequence de reestimation et
date de premiere prevision non donnees. Voir CHOICES.
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
    "Managing Volatility, The Review of Financial Studies 31(7), 2729-2773"
)
EXPECTED_SIGN = +1
CHOICES = (
    "La fiche dit que le papier predit une VARIANCE realisee a 20 jours et aucun rendement ; "
    "j'ai code la prevision de variance HExp centree comme score, en le declarant : c'est la seule "
    "part de la fiche qui produit un nombre par date et par instrument.",
    "EXPECTED_SIGN = +1 : le papier SUPPOSE un Sharpe conditionnel constant (SR = 0.4), donc un "
    "rendement espere proportionnel a la volatilite ; une variance prevue plus forte implique un "
    "rendement espere plus fort. Ce signe est une deduction de cette hypothese, pas un resultat "
    "mesure du papier.",
    "Le score est la variance prevue elle-meme, pas sa racine : la fiche dit que le modele porte sur "
    "la variance ; la racine serait une transformation monotone sans effet sur un classement.",
    "Estimation : la fiche prefere le panel Mega ; j'ai estime cellule par cellule ((root, window)), "
    "schema 'Individual Asset' du papier, parce qu'un pooling causal entre cellules aux horaires "
    "differents exigerait une regle de cloture des cibles des autres cellules que la fiche ne donne pas.",
    "Regression centree sans intercept : l'equation (9) n'affiche aucun intercept (ambiguite non "
    "resolue dans la recette) ; j'ai pris la forme ecrite.",
    "MCO resolu par moindres carres directs sur la matrice des regresseurs (SVD de numpy), et non par "
    "les equations normales : les quatre EWMA sont tres colineaires et les equations normales "
    "amplifiaient l'arrondi flottant des clotures recollees au point de rendre le score sensible "
    "au futur (verdict S3 precedent, ecarts de l'ordre de 1e-11).",
    "Frequence de reestimation (null dans la recette) : betas reestimes a chaque seance sur tout le "
    "passe disponible, choix le plus simple pour 'up to that point in time'.",
    "Observations d'estimation : donnees quotidiennes chevauchantes (resolu par la recette) ; pour "
    "la seance notee k, seules entrent les seances s dont la cible (seances s+1 a s+20) est close "
    "avant la seance k, soit s <= k-21.",
    "Historique minimal : une observation n'entre dans l'estimation que si sa date est au moins 1 an "
    "apres la premiere seance de la cellule ; j'ai lu '1 full calendar year of RV' comme un an "
    "d'historique, sans aligner sur le 1er janvier.",
    "Date de premiere prevision (oos_start_date null dans la recette) : aucun score tant que les "
    "observations d'estimation ne couvrent pas elles-memes 1 an (seance notee au moins 1 an apres "
    "la premiere observation eligible). J'ai reutilise la seule duree que donne la fiche, une annee, "
    "comme fenetre initiale d'estimation, plutot que d'emettre des previsions sur une poignee "
    "d'observations colineaires. Il faut aussi au moins autant d'observations que de regresseurs (4).",
    "Une 'journee' du papier est ici une seance de la cellule (une fenetre ASIA/EUROPE/US d'un jour) "
    "telle que la donne _common.cell_bars ; l'overnight est le rendement log au carre entre la "
    "derniere cloture de la seance precedente de la cellule et la premiere de la seance courante.",
    "Echantillonnage a 5 minutes lu en positions de barres (une barre sur 5), en supposant des barres "
    "d'une minute ; les 5 grilles demarrent aux 5 premieres barres de la seance. Une barre manquante "
    "decale donc la grille, au lieu d'une grille d'horloge.",
    "Rendements logarithmiques calcules comme log du rapport de clotures consecutives sur les clotures "
    "recollees de cell_bars ; un prix non positif ou manquant donne un rendement NaN, ignore dans la somme.",
    "Premiere seance de la cellule : pas d'overnight calculable, sa RV est la seule partie intraday.",
    "Instant du score : ancre de _common.run (premiere barre a au plus horizon_bars de la cloture "
    "declaree). La RV du jour t y est PARTIELLE (barres jusqu'a la barre notee incluse, plus "
    "l'overnight) et traitee comme RV_t, alors que les RV des jours passes sont completes ; la "
    "recette dit 'avec les RV jusqu'a RV_t incluse'.",
    "EWMA a moins de 500 seances d'historique : poids tronques au nombre de seances disponibles et "
    "renormalises a somme 1 (ambiguite ouverte dans la recette).",
    "Premier retard i = 1 porte sur RV_t elle-meme, poids exp(-i * lambda), conformement a la recette.",
    "Facteur global GlRV / HExpGl non code : la fiche dit qu'il perd son sens sur neuf instruments, et "
    "la ponderation (simple ou ponderee) est contradictoire dans la recette.",
    "Insanity filter non applique : la recette ne dit pas s'il vaut pour HExp.",
    "Filtres de pics (mediane centree = look-ahead), de spread et d'heures liquides non appliques : "
    "les donnees du panel sont prises telles quelles.",
    "Univers : toutes les cellules du panel, pas seulement les racines exact_roots de la recette ; la "
    "methode du papier se veut commune a toutes les classes d'actifs.",
)

FORECAST_HORIZON_DAYS = 20
RV_SAMPLING_BARS = 5
SUBSAMPLE_GRIDS = 5
EWMA_COMS = (1, 5, 25, 125)
EWMA_TRUNCATION_LAGS = 500
MIN_HISTORY_YEARS = 1

_LAGS = np.arange(1, EWMA_TRUNCATION_LAGS + 1, dtype=float)
_WEIGHTS = tuple(np.exp(-_LAGS * math.log(1 + 1 / com)) for com in EWMA_COMS)


def _intraday_rv(prices: np.ndarray) -> float:
    """RV sous-echantillonnee d'une suite de clotures (rien au-dela de sa fin)."""
    n = len(prices)
    grids = [g for g in range(SUBSAMPLE_GRIDS) if g < n]
    if not grids:
        return float("nan")
    vals = []
    for g in grids:
        p = prices[g::RV_SAMPLING_BARS]
        with np.errstate(all="ignore"):
            r = np.log(p[1:] / p[:-1])
        r = r[np.isfinite(r)]
        vals.append(float(np.sum(r * r)))
    return float(np.mean(vals))


def _overnight(prev_last: float, first: float) -> float:
    with np.errstate(all="ignore"):
        r = math.log(first / prev_last) if (prev_last > 0 and first > 0) else float("nan")
    if not np.isfinite(r):
        return 0.0
    return float(r * r)


def _exp_factors(history: np.ndarray) -> np.ndarray | None:
    """EWMA des RV, la plus recente en dernier ; rien au-dela de la fin de `history`."""
    recent = history[::-1][:EWMA_TRUNCATION_LAGS]
    mask = np.isfinite(recent)
    if not mask.any():
        return None
    out = []
    for w in _WEIGHTS:
        ww = w[: len(recent)][mask]
        out.append(float(np.dot(ww, recent[mask]) / ww.sum()))
    return np.asarray(out)


def _cell_scores(panel, root, window, horizon_bars):
    closes, sessions = _common.cell_bars(panel, root, window)
    if closes is None or len(closes) == 0:
        return None

    labels = sessions.tolist()
    order = list(dict.fromkeys(labels))
    groups = {lab: [] for lab in order}
    for pos, lab in enumerate(labels):
        groups[lab].append(pos)

    prices_all = np.asarray(closes.to_numpy(), dtype=float)
    n_sess = len(order)
    first_ts = {}
    first_px = np.empty(n_sess)
    last_px = np.empty(n_sess)
    rv = np.empty(n_sess)
    dates = []
    for k, lab in enumerate(order):
        idx = groups[lab]
        px = prices_all[idx]
        first_ts[closes.index[idx[0]]] = k
        dates.append(closes.index[idx[0]])
        first_px[k] = px[0]
        last_px[k] = px[-1]
        on = _overnight(last_px[k - 1], first_px[k]) if k > 0 else 0.0
        rv[k] = _intraday_rv(px) + on

    # Moyenne longue en expansion et facteurs EWMA, chacun ne lisant que rv[:s+1].
    n_reg = len(EWMA_COMS)
    xs = np.full((n_sess, n_reg), np.nan)
    lr = np.full(n_sess, np.nan)
    for s in range(n_sess):
        hist = rv[: s + 1]
        hist = hist[np.isfinite(hist)]
        if len(hist) == 0:
            continue
        lr[s] = float(hist.mean())
        f = _exp_factors(rv[: s + 1])
        if f is not None:
            xs[s] = f - lr[s]

    # Cible a 20 seances : n'est lue que pour s <= k-21 a la seance k.
    ys = np.full(n_sess, np.nan)
    for s in range(n_sess - FORECAST_HORIZON_DAYS):
        fut = rv[s + 1 : s + 1 + FORECAST_HORIZON_DAYS]
        if np.isfinite(fut).all() and np.isfinite(lr[s]):
            ys[s] = float(fut.mean()) - lr[s]

    start = dates[0] + pd.DateOffset(years=MIN_HISTORY_YEARS)
    eligible = np.array([d >= start for d in dates]) & np.isfinite(ys) & np.isfinite(xs).all(axis=1)
    elig_idx = np.flatnonzero(eligible)

    def predictor(sess_closes: pd.Series, position: int):
        if len(sess_closes) == 0:
            return None
        k = first_ts.get(sess_closes.index[0])
        if k is None:
            return None
        last_obs = k - FORECAST_HORIZON_DAYS - 1
        if last_obs < 0:
            return None
        rows = elig_idx[elig_idx <= last_obs]
        if len(rows) < n_reg:
            return None
        if dates[k] < dates[rows[0]] + pd.DateOffset(years=MIN_HISTORY_YEARS):
            return None
        beta = np.linalg.lstsq(xs[rows], ys[rows], rcond=None)[0]

        px = np.asarray(sess_closes.to_numpy(), dtype=float)[: position + 1]
        if len(px) == 0:
            return None
        rv_today = _intraday_rv(px)
        if k > 0:
            rv_today += _overnight(last_px[k - 1], px[0])
        history = np.concatenate([rv[:k], [rv_today]])
        hist_f = history[np.isfinite(history)]
        if len(hist_f) == 0:
            return None
        lr_t = float(hist_f.mean())
        f = _exp_factors(history)
        if f is None:
            return None
        forecast = lr_t + float(np.dot(beta, f - lr_t))
        if not np.isfinite(forecast):
            return None
        return forecast

    return _common.run(panel, predictor, cells=[(root, window)], horizon_bars=horizon_bars)


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} : la prevision HExp de la variance a 20 seances."""
    selected = list(panel.cells()) if cells is None else list(cells)
    out = {}
    for root, window in selected:
        res = _cell_scores(panel, root, window, horizon_bars)
        if not res:
            continue
        for key, series in res.items():
            if series is not None and len(series) > 0:
                out[key] = series
    return out
