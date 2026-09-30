"""Baltussen, Da, Lammers, Martens (2021) -- r_ROD, le rendement du reste de la journee.

Score : r_ROD,t = P(c-30,t) / P(c,t-1) - 1 (Eq. 2), rendement simple d'un achat a
la cloture de la seance precedente et d'une vente 30 minutes avant la cloture de
la seance t. Il predit positivement r_LH,t, le rendement des 30 dernieres minutes.

Mecanique : `_common.run` place le score a UNE barre par seance, la premiere dont
la distance a la cloture declaree de la fenetre est au plus `horizon_bars`
(30 par defaut, soit c-30 sur des barres d'une minute). Cet ancrage se lit sur
l'horloge, pas sur les donnees.

P(c,t-1) est la derniere cloture de la seance precedente de la meme cellule, lue
dans `_common.cell_bars` ; elle est entierement anterieure a la seance notee, donc
causale.

Ce qui manque et ce qui a ete fait a la place :
- les heures d'ouverture/cloture retenues par le papier par marche ne sont pas
  publiees : on prend la seance et la cloture declaree de la fenetre du panel ;
- l'etiquetage de la barre d'une minute n'est pas precise : on prend la cloture
  de la barre notee par `run` ;
- le canal NGE (gamma net des teneurs de marche) exige des donnees absentes ;
  seul le signal non conditionne est code ;
- les Sharpe du papier viennent de portefeuilles 1/N de 8 a 21 contrats par
  classe ; avec neuf futures, cette diversification ne se transpose pas.
"""

from __future__ import annotations

import math

import pandas as pd

from signals import _common

SIGNAL_ID = "baltussen-2021-hedging-demand-intraday-momentum"
HYPOTHESIS = None
PAPER = (
    "Baltussen, Da, Lammers, Martens (2021), Hedging demand and market intraday "
    "momentum, Journal of Financial Economics 142, 377-403"
)
EXPECTED_SIGN = +1
CHOICES = (
    "la fiche dit que r_ROD predit positivement r_LH (Eq. 7, strategie longue si "
    "r_ROD > 0) ; j'ai choisi EXPECTED_SIGN = +1, parce que c'est le sens annonce "
    "du momentum intrajournalier",
    "la fiche donne r_ROD continu (regressions) et son signe (strategie de timing) ; "
    "j'ai rendu r_ROD continu, parce que c'est la variable de l'Eq. 7 et que le "
    "harnais mesure un IC sur un score, le signe en etant une version appauvrie",
    "la fiche dit P(c-30,t), 30 minutes avant la cloture retenue ; j'ai pris la "
    "cloture de la barre ancree par _common.run avec horizon_bars (30 par defaut, "
    "soit 30 barres d'une minute), parce que cet ancrage se lit sur l'horloge de la "
    "cloture declaree de la fenetre, comme c-30 dans le papier",
    "la fiche dit P(c,t-1), prix a la cloture retenue de la veille, sans preciser "
    "le traitement des week-ends, jours feries ou jours retires ; j'ai pris la "
    "derniere cloture disponible de la seance precedente de la meme cellule "
    "(root, window) dans les clotures recollees de _common.cell_bars, parce que "
    "c'est la derniere cloture de reference connue et qu'elle est anterieure a la "
    "seance notee",
    "la fiche laisse ouverte la question du roll le jour de bascule (P(c,t-1) sur "
    "l'ancien ou le nouveau contrat) ; j'ai utilise les clotures recollees de "
    "_common.cell_bars, parce qu'un rendement brut a travers un raccord est un "
    "artefact",
    "les heures de seance par marche ne sont pas publiees (available upon request) ; "
    "j'ai pris la seance et la cloture declaree de la fenetre du panel, parce que "
    "c'est la seule definition disponible, ce qui deplace les frontieres du "
    "decoupage ON/FH/M/SLH/LH par rapport au papier",
    "la fiche ne dit pas quoi faire si le prix a c-30 ou c(t-1) manque ; je n'ecris "
    "aucun score (None) si la seance precedente est absente de la cellule ou si un "
    "prix est manquant, non fini ou non positif, parce que le papier retire les prix "
    "non positifs et qu'inventer un prix de reference serait inventer une donnee",
    "la fiche mentionne un filtre de volume (jours < 100 contrats retires) et le "
    "retrait des jours de cloture anticipee ; je ne les applique pas, parce que le "
    "predicteur ne recoit que des clotures et que le calendrier des clotures "
    "anticipees n'est pas dans la fiche",
    "la fiche conditionne l'effet au signe du NGE ; je ne l'implemente pas, parce "
    "que les donnees NGE (OptionMetrics, SqueezeMetrics) sont absentes",
    "rendement simple et non logarithmique, parce que l'Eq. 2 ecrit un rapport de "
    "prix moins un",
)


def _previous_close_map(closes: pd.Series, sessions: pd.Series):
    """Pour chaque barre, la derniere cloture de la seance precedente.

    La seance precedente est terminee avant la premiere barre de la seance
    courante : aucune lecture posterieure a la barre notee."""
    frame = pd.DataFrame({"close": closes, "session": sessions}).dropna(
        subset=["session"]
    )
    last_by_session = frame.groupby("session", sort=False)["close"].last()
    first_ts = frame.reset_index().groupby("session", sort=False).first()
    order = sorted(
        last_by_session.index,
        key=lambda s: first_ts.loc[s].iloc[0],
    )
    prev = {}
    for i in range(1, len(order)):
        prev[order[i]] = last_by_session.loc[order[i - 1]]
    session_of_bar = frame["session"]
    return session_of_bar, prev


def _make_predictor(session_of_bar: pd.Series, prev: dict):
    def predictor(closes: pd.Series, position: int):
        if position < 0 or position >= len(closes):
            return None
        ts = closes.index[0]
        if ts not in session_of_bar.index:
            return None
        sess = session_of_bar.loc[ts]
        if isinstance(sess, pd.Series):
            sess = sess.iloc[0]
        p_prev = prev.get(sess)
        if p_prev is None:
            return None
        p_prev = float(p_prev)
        p_now = float(closes.iloc[position])
        if not (math.isfinite(p_prev) and math.isfinite(p_now)):
            return None
        if p_prev <= 0 or p_now <= 0:
            return None
        return p_now / p_prev - 1

    return predictor


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} : r_ROD a c-30, une valeur par seance."""
    selected = list(panel.cells()) if cells is None else list(cells)
    out = {}
    for cell in selected:
        root, window = cell
        closes, sessions = _common.cell_bars(panel, root, window)
        if closes is None or len(closes) == 0:
            continue
        session_of_bar, prev = _previous_close_map(closes, sessions)
        if not prev:
            continue
        predictor = _make_predictor(session_of_bar, prev)
        result = _common.run(
            panel, predictor, cells=[(root, window)], horizon_bars=horizon_bars
        )
        for key, series in result.items():
            if series is not None and len(series) > 0:
                out[key] = series
    return out
