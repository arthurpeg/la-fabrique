"""Andersen & Bollerslev (1997) : profil intra-journalier de |rendement|.

Le papier ne propose aucun score. Il mesure le profil moyen de |R| par position
horaire de la seance. Part transposable codee ici : pour chaque barre, la
moyenne, sur les seances STRICTEMENT anterieures, de |rendement de 5 barres|
a la meme position dans la seance. Le score est ce profil estime au passe.

Ne se transpose pas / manquait : modele de Fourier (section 5), facteur
sigma_t (MA(1)-GARCH), fenetre d'estimation, ancre de pose : tous non donnes
ou non transposables, donc non codes (voir CHOICES).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "andersen-bollerslev-1997-periodicity"
HYPOTHESIS = None
PAPER = (
    "Andersen & Bollerslev (1997), Intraday periodicity and volatility "
    "persistence in financial markets, Journal of Empirical Finance"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche ne pose aucun score ; j'ai compris que la part transposable est le profil moyen de |R| par position horaire, et le score est ce profil, parce que c'est la grandeur que le papier mesure",
    "le profil du papier est moyenne sur tout l'echantillon (futur inclus) ; j'estime au passe : moyenne expansive sur les seances strictement anterieures a la seance de la barre notee, pour la causalite",
    "la fenetre d'estimation est null dans la recette ; j'ai pris l'expansion complete depuis le debut de l'historique, sans nombre nouveau",
    "le rendement est celui de 5 barres (bar_minutes = 5) en log-prix des clotures recollees, a l'interieur d'une seance ; je suppose des barres d'une minute comme dit dans la fiche (leurs rendements sont a 5 minutes, les notres a 1 minute)",
    "la position horaire est le rang de la barre dans sa seance (comptage depuis l'ouverture, causal) ; les 5 premieres barres sans rendement de 5 barres n'ont pas de score, analogue du premier rendement supprime (nuit)",
    "score_anchor_time est null : je pose un score a chaque barre ayant un profil passe, au lieu d'une ancre par seance, sans _common.run car le profil exige l'historique inter-seances",
    "signe attendu +1 : un profil de |R| eleve annonce une amplitude de mouvement plus forte (claim direction positive) ; la valeur absolue ne donne pas de direction",
    "modele de Fourier, sigma_t GARCH, dummies 78-80, traitement des suspensions et du krach de 1987, heure standard ou d'ete : non codes, car non transposables ou null dans la fiche",
    "|R| plutot que R^2, sans retrait de moyenne, comme la fiche le dit",
    "toutes les cellules demandees (ou panel.cells()) sont traitees ; la fenetre US 09:30-16:00 est celle du panel, sans les trois dernieres barres post-cloture (resolution null)",
)


def _cell_scores(panel, root, window):
    closes, sessions = _common.cell_bars(panel, root, window)
    if len(closes) == 0:
        return None
    lag = 5  # bar_minutes
    logc = np.log(closes.astype(float))
    sess_code, _ = pd.factorize(sessions.to_numpy())  # ordre d'apparition
    sess_code = pd.Series(sess_code, index=closes.index)
    pos = sess_code.groupby(sess_code).cumcount()
    ret = logc.groupby(sess_code).diff(lag).abs()

    df = pd.DataFrame(
        {"s": sess_code.to_numpy(), "p": pos.to_numpy(), "a": ret.to_numpy()}
    )
    # unstack garde les colonnes toutes NaN (pivot_table les supprimait, et
    # get_indexer rendait -1, qui lisait la derniere colonne : fuite).
    piv = df.set_index(["s", "p"])["a"].unstack("p").sort_index()
    prof = piv.shift(1).expanding(min_periods=1).mean()
    row = prof.index.get_indexer(df["s"])
    col = prof.columns.get_indexer(df["p"])
    vals = prof.to_numpy()[row, col]
    vals = np.where((row < 0) | (col < 0), np.nan, vals)
    out = pd.Series(vals, index=closes.index).dropna()
    if len(out) == 0:
        return None
    return out


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} : profil passe de |R| a 5 barres."""
    wanted = list(cells) if cells is not None else list(panel.cells())
    available = set(panel.cells())
    result = {}
    for root, window in wanted:
        if (root, window) not in available:
            continue
        s = _cell_scores(panel, root, window)
        if s is not None:
            result[(root, window)] = s
    return result
