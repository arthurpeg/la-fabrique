"""Baltussen, Da, Lammers, Martens (2021) : momentum intrajournalier.

Score : r_ROD,t = P(c-30,t) / P(c,t-1) - 1, rendement simple de la cloture de
la veille jusqu'a 30 minutes avant la cloture du jour t, lu a c-30 (l'ancrage
est donne par `_common.run` sur l'horloge, avec horizon_bars = 30). Le papier
predit r_LH (derniere demi-heure) positivement par r_ROD.

Ce qui ne se transpose pas ou manque : les heures de seance par contrat ne sont
pas publiees (on prend la seance et la cloture declarees du panel) ; la
regression, le R2 hors echantillon, le portefeuille 1/N et le conditionnement
NGE ne sont pas codes (aucune donnee NGE). Le score est r_ROD continu, pas son
signe.
"""

from __future__ import annotations

import pandas as pd

from signals import _common

SIGNAL_ID = "baltussen-2021-hedging-demand-intraday-momentum"
HYPOTHESIS = None
PAPER = (
    "Baltussen, Da, Lammers, Martens (2021), Hedging demand and market "
    "intraday momentum, Journal of Financial Economics 142"
)
EXPECTED_SIGN = +1
CHOICES = (
    "la fiche dit r_ROD = P(c-30)/P(c,t-1) - 1 ; j'ai compris le prix a c-30 "
    "comme la cloture de la barre ancree par _common.run (premiere barre a au "
    "plus horizon_bars=30 de la cloture declaree), parce que la recette donne "
    "30 minutes avant la cloture et que l'ancrage se lit sur l'horloge",
    "la fiche dit P(c,t-1) sans dire quelle barre ; j'ai pris la derniere "
    "cloture disponible de la seance precedente du panel, parce que les heures "
    "de seance par contrat ne sont pas publiees et que la seance du panel est "
    "la seule definition disponible",
    "la fiche laisse ouvert le traitement week-end/jour retire ; j'ai pris la "
    "seance precedente presente dans les donnees de la cellule comme veille",
    "la fiche laisse ouvert le roll ; j'ai pris les clotures recollees de "
    "_common.cell_bars, parce qu'un raccord de contrat brut serait un artefact",
    "la fiche donne le score continu (Eq. 7) et son signe (Eq. 12) ; j'ai "
    "choisi le r_ROD continu, parce que le harnais mesure un classement, et le "
    "signe s'en deduit",
    "la fiche dit rendement simple ; j'ai pris le rapport de prix moins un, "
    "pas le logarithme",
    "la fiche donne les heures 09:30-16:00 pour l'E-Mini seulement ; je n'ai "
    "code aucune heure, la cloture est celle declaree de la fenetre du panel",
    "la fiche exclut les jours de volume inferieur a 100 contrats ; non code, "
    "le panel n'expose pas ce filtre de facon utilisable ici",
    "EXPECTED_SIGN = +1 : le papier dit que r_LH est positivement predit par "
    "r_ROD",
)


def _price(closes: pd.Series, position: int):
    """Prix a la barre notee, sans rien lire au-dela de la position."""
    value = closes.iloc[position]
    if pd.isna(value):
        return None
    return float(value)


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} de r_ROD lu a c-30."""
    levels = _common.run(panel, _price, cells=cells, horizon_bars=horizon_bars)
    out = {}
    for key, level in levels.items():
        if level is None or len(level) == 0:
            continue
        root, window = key
        closes, sessions = _common.cell_bars(panel, root, window)
        last = closes.groupby(sessions).last()
        prev = last.shift(1)
        sess = sessions.reindex(level.index)
        denom = pd.Series(prev.reindex(sess.values).values, index=level.index)
        score = (level / denom - 1).replace([float("inf"), float("-inf")], float("nan"))
        score = score.dropna()
        if len(score) == 0:
            continue
        out[key] = score
    return out
