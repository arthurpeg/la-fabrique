"""Andersen & Bollerslev (1997) : periodicite intraday de la volatilite.

La fiche ne propose AUCUN signal predictif (signal_construction = null) : la
grandeur du papier est descriptive, la moyenne sur les jours de |R_t,n| par
intervalle intraday n (motif en U). La part transposable codee ici est ce
profil : le score d'une barre est la moyenne, sur les SEANCES PASSEES, du
rendement logarithmique absolu de la meme barre de la journee (meme minute
d'horloge). Le score est donc la volatilite saisonniere attendue de la barre.

Ne se transpose pas et n'est pas code : le modele de Fourier de la section 5 /
annexe B (non releve par la fiche), le facteur journalier sigma_t du
MA(1)-GARCH(1,1) (disponibilite et fenetre non donnees), les niveaux en %
(barres de 5 minutes chez les auteurs, autres chez nous), le correlogramme.
Manquait : le rang des intervalles du U, la regle de roll, le fuseau ; rien
n'a ete invente a la place (voir CHOICES).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "andersen-bollerslev-1997-periodicity"
HYPOTHESIS = None
PAPER = (
    "Andersen & Bollerslev (1997), Intraday periodicity and volatility "
    "persistence in financial markets, Journal of Empirical Finance 4(2-3)"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche ne propose aucun score (signal_construction null) ; j'ai compris que la part transposable est le profil moyen de |R| par intervalle intraday, et je score chaque barre par ce profil estime au passe, parce que c'est la seule grandeur du papier qui se lit comme une prevision (volatilite saisonniere attendue).",
    "la moyenne du papier est faite en une passe sur tout l'echantillon ; j'ai pris une moyenne en expansion sur les seances strictement anterieures a la seance notee, parce que toute statistique de la serie entiere fuit l'avenir.",
    "le rendement de la barre notee n'entre pas dans son propre score ; seules les seances precedentes servent, parce qu'une barre est horodatee a son ouverture et que son rendement n'est connu qu'a sa fin.",
    "l'intervalle n du papier est repere par la minute d'horloge de la barre (heure*60+minute, entiers, dans le fuseau de l'index), parce que les rangs 1 a 80 supposent des barres de 5 minutes que nos donnees n'ont pas ; aucune taille de barre ni nombre d'intervalles n'est code.",
    "rendement = difference des logarithmes des clotures recollees de _common.cell_bars, au sein d'une seance : le premier rendement de la seance (nuit) n'existe donc pas et rien ne traverse la nuit, comme le papier supprime le premier rendement et les rendements overnight.",
    "valeur absolue |R| plutot que carre, comme le papier le prefere ; pas de centrage, le papier dit que c'est sans importance (moyenne pratiquement nulle).",
    "pas de standardisation par sigma_t ni de filtre de Fourier (J=1, P=2 non utilises) : la fiche ne donne ni disponibilite ni fenetre du GARCH, et le modele n'est pas releve.",
    "le krach 1987, les jours de semaine, les jours feries ne sont pas traites : sans objet pour nos donnees, et le papier ne corrige pas les jours de semaine.",
    "le score est pose sur toutes les barres ayant au moins une seance passee pour leur minute d'horloge, sans ancrage sur la fin de fenetre, parce que le papier ne pose aucune decision a une date donnee ; horizon_bars est accepte mais ignore, et son defaut est None (et non un nombre) car la fiche ne donne aucun horizon (horizon null) et S5 interdit une constante absente de la fiche.",
    "EXPECTED_SIGN = +1 : le papier affirme une relation positive (claim.direction positive), un profil de volatilite plus haut annonce des mouvements absolus plus grands ; le signe vaut pour l'amplitude, la fiche n'en donne aucun pour la direction du rendement.",
    "le score est le niveau brut de la moyenne, sans normalisation entre cellules ni division par la moyenne du profil, parce que la fiche n'en donne pas.",
)


def _cell_score(closes: pd.Series, session: pd.Series) -> pd.Series | None:
    sess = pd.Series(np.asarray(session), index=closes.index)
    logc = np.log(closes.astype(float))
    ret = logc.groupby(sess.values).diff().abs()

    idx = closes.index
    slot = pd.Series(idx.hour * 60 + idx.minute, index=idx)

    frame = pd.DataFrame(
        {"session": sess.values, "slot": slot.values, "r": ret.values},
        index=idx,
    )
    valid = frame["r"].notna() & frame["session"].notna()
    if not valid.any():
        return None

    order = pd.unique(frame["session"].dropna())
    table = frame[valid].pivot_table(
        index="session", columns="slot", values="r", aggfunc="mean"
    )
    table = table.reindex(order)
    past = table.expanding().mean().shift(1)

    long = past.stack()
    keys = pd.MultiIndex.from_arrays([frame["session"].values, frame["slot"].values])
    values = long.reindex(keys).to_numpy()
    out = pd.Series(values, index=idx, dtype=float).dropna()
    if out.empty:
        return None
    return out


def scores(panel, cells=None, horizon_bars=None):
    """Rend {(root, window): pd.Series} : profil intraday passe de |R|."""
    if cells is None:
        cells = panel.cells()
    result = {}
    for cell in cells:
        root, window = cell[0], cell[1]
        closes, session = _common.cell_bars(panel, root, window)
        series = _cell_score(closes, session)
        if series is not None:
            result[(root, window)] = series
    return result
