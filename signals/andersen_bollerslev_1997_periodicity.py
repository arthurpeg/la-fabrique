"""Andersen & Bollerslev (1997) -- profil intra-journalier de |R|, transpose au passe.

Le papier ne propose AUCUN score predictif (signal_construction = null, horizon
= null). Il decrit le profil intra-journalier de volatilite : pour chaque
intervalle de 5 minutes n de la seance, la moyenne sur les jours de
l'echantillon du rendement absolu |R_t,n|. Ce profil est un objet de VARIANCE,
pas de direction : sa transposition en score face a des rendements signes est
une diminution declaree, pas une pretention.

Part transposee : au score de la barre notee, la moyenne de |R| sur 5 minutes,
a la meme distance (en minutes entieres) du debut de seance, sur TOUTES les
seances strictement anterieures de la cellule (expansion jusqu'a t, faute de
fenetre dans le papier, qui moyenne sur tout l'echantillon futur compris).

Ce qui manquait, et ce qui a ete fait a la place : voir CHOICES. Non transposes :
la forme de Fourier (J = 1, P = 2), les indicatrices des intervalles 78-80, le
facteur journalier sigma_t (MA(1)-GARCH(1,1)), l'exclusion du krach de 1987,
le nombre d'intervalles (80) et de jours (991) propres a leur echantillon.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "andersen-bollerslev-1997-periodicity"
HYPOTHESIS = None
PAPER = (
    "Torben G. Andersen, Tim Bollerslev (1997), Intraday periodicity and "
    "volatility persistence in financial markets, Journal of Empirical Finance "
    "4(2-3):115-158"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche ne pose aucun score (signal_construction et horizon null) ; j'ai "
    "transpose l'objet mesure -- le profil moyen de |R| par position horaire -- "
    "en score, parce que c'est la seule grandeur que le papier construit.",
    "ambiguite 'amplitude recente ou profil moyen a la meme position' non "
    "resolue par le papier ; j'ai choisi le profil moyen a la meme position "
    "horaire, parce que c'est ce que le papier mesure (Fig. 2a), l'amplitude "
    "recente n'y etant pas un objet.",
    "le papier moyenne sur tout l'echantillon, jours futurs inclus "
    "(profile_estimation_window null) ; j'ai estime le profil en expansion sur "
    "les seules seances strictement anterieures a la seance notee, sans "
    "longueur de fenetre, parce qu'aucune n'est donnee et que tout autre "
    "choix demanderait un nombre invente.",
    "EXPECTED_SIGN : le papier predit une amplitude, pas une direction ; j'ai "
    "pris +1, d'apres claim.direction = positive de la fiche, en sachant que "
    "rien dans le papier ne lie le profil de |R| au signe du rendement futur.",
    "score_anchor_time null ; j'ai pose le score a l'ancre de _common.run (une "
    "barre par seance, a horizon_bars de la cloture declaree de la fenetre), "
    "parce que c'est la mecanique la plus simple qui tombe sur une barre "
    "mesurable, sans constante nouvelle.",
    "position horaire : le papier indexe les intervalles n = 1..80 depuis "
    "8h35 ; j'ai pris la distance en minutes entieres entre la barre et la "
    "premiere barre de sa seance, ce qui suit l'horloge de la fenetre et "
    "evite la question heure d'ete / heure standard (ambiguite 'central "
    "standard time' non resolue). Une seance dont la premiere barre manque "
    "decale cette distance ; je ne la corrige pas.",
    "rendement de 5 minutes (bar_minutes = 5) : nos barres sont a 1 minute ; "
    "j'ai pris |log c_t - log c_(t-5 min)| avec les deux barres dans la meme "
    "seance, glissant (non aligne sur une grille de 5 minutes), parce que "
    "l'ancre de run n'est pas forcement sur une telle grille.",
    "premier rendement de seance supprime par le papier (il contient la "
    "nuit) : aucun rendement n'enjambe deux seances, donc les 5 premieres "
    "minutes de chaque seance n'ont pas de |R| ; c'est l'equivalent de leur "
    "suppression.",
    "barre a 5 minutes plus tot absente (trou de donnees) : le rendement n'est "
    "pas calcule ; le papier interpole lineairement les prix, je n'interpole "
    "pas, ce qui est le choix le plus simple sans parametre.",
    "rendements absolus et non carres, sans retrait de la moyenne, comme le "
    "papier le fait pour le filtrage ('the mean return is practically zero').",
    "univers : la fiche etudie ES x US ; j'ai applique le signal a toutes les "
    "cellules que le panel ou l'appelant fournit, la forme etant le motif "
    "transposable selon la fiche ; le harnais choisit les cellules.",
    "pas d'exclusion du krach de 1987 (hors de nos dates), pas de correction "
    "jour-de-la-semaine ni jours feries (le papier n'en fait pas), pas de "
    "modele de Fourier ni de sigma_t (non releves de facon exploitable).",
    "les trois rendements apres la cloture du NYSE : la question du "
    "debordement de 15 minutes de leur seance sur notre fenetre US est non "
    "resolue ; je n'ajoute ni ne retire aucune barre, la fenetre est celle "
    "du panel.",
    "aucune valeur n'est rendue tant qu'aucune seance anterieure n'a de |R| a "
    "la meme position (premiere seance de la cellule) : le predicteur rend "
    "None plutot qu'une valeur de remplissage.",
)


def _cell_predictor(panel, root, window):
    """Construit le predicteur d'une cellule, qui ne lit que les seances
    strictement anterieures a celle qu'il note."""
    closes_all, sessions = _common.cell_bars(panel, root, window)
    if len(closes_all) == 0:
        return None
    idx = closes_all.index
    logc = pd.Series(np.log(closes_all.to_numpy(dtype=float)), index=idx)
    sess = pd.Series(sessions.to_numpy(), index=idx)

    stamps = pd.Series(idx, index=idx)
    first = stamps.groupby(sess.to_numpy()).transform("min")
    offset = ((stamps - first).dt.total_seconds() // 60).astype(int)

    lag_idx = idx - pd.Timedelta(minutes=5)
    prev = logc.reindex(lag_idx).to_numpy()
    prev_sess = sess.reindex(lag_idx).to_numpy()
    same = prev_sess == sess.to_numpy()
    r5 = np.abs(logc.to_numpy() - prev)
    ok = same & np.isfinite(r5)

    table = pd.DataFrame(
        {"offset": offset.to_numpy()[ok], "r": r5[ok]},
        index=idx[ok],
    )
    groups = {}
    for m, g in table.groupby("offset"):
        g = g.sort_index()
        groups[int(m)] = (g.index, np.cumsum(g["r"].to_numpy()))

    def predictor(closes, position):
        t0 = closes.index[0]
        tp = closes.index[position]
        m = int((tp - t0).total_seconds() // 60)
        entry = groups.get(m)
        if entry is None:
            return None
        times, csum = entry
        n = int(times.searchsorted(t0, side="left"))
        if n == 0:
            return None
        return float(csum[n - 1] / n)

    return predictor


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series}."""
    chosen = list(panel.cells()) if cells is None else list(cells)
    out = {}
    for root, window in chosen:
        predictor = _cell_predictor(panel, root, window)
        if predictor is None:
            continue
        res = _common.run(
            panel, predictor, cells=[(root, window)], horizon_bars=horizon_bars
        )
        for key, series in res.items():
            if series is not None and len(series) > 0:
                out[key] = series
    return out
