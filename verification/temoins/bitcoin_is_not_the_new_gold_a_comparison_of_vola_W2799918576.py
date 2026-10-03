"""Klein, Thu & Walther (2018) -- Bitcoin is not the New Gold.

Le papier est descriptif : il ne construit aucun score. Ce module code la seule
part transposable et causale : la profondeur de detresse de la seance, c'est-a-dire
le rendement log x100 de la cloture de la seance jusqu'a la barre notee
(r = 100 x log(P_t / P_ouverture)), l'analogue intraday du rendement journalier
de cloture a cloture dont l'indicateur de detresse 1{r_t < VaR_q} est fait.

Ce qui ne se transpose pas : le seuil VaR_q (quantile empirique plein echantillon,
ex post), les correlations BEKK (parametres non publies, fenetre inconnue),
les poids de variance minimale, le lissage de Savitzky-Golay (fenetre non donnee),
l'univers Bitcoin/argent/MSCI. Le seuil VaR n'est pas code : la fiche ne donne
aucune fenetre glissante, et en inventer une serait un parametre invente.
Le score est donc le rendement continu brut, sans seuil ni indicateur.
Ancrage et lecture de l'horloge : deleges a `_common.run`.
"""

from __future__ import annotations

import math

from signals import _common

SIGNAL_ID = "bitcoin-is-not-the-new-gold-a-comparison-of-vola-W2799918576"
HYPOTHESIS = None
PAPER = (
    "Klein, Thu & Walther (2018), Bitcoin is not the New Gold - A comparison of "
    "volatility, correlation, and portfolio performance, International Review of "
    "Financial Analysis 59, 105-116"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche ne construit aucun signal ; j'ai code la profondeur de detresse "
    "de la seance (100 x log(cloture a la barre / cloture d'ouverture de la seance)), "
    "parce que c'est le rendement r_t dont depend l'indicateur 1{r_t < VaR_q}.",
    "le seuil VaR_q (1 %, 5 %, 10 %) est plein echantillon dans le papier ; la recette "
    "ne donne aucune fenetre glissante, je ne l'ai donc pas code et le score reste "
    "continu, sans indicateur ni quantile.",
    "signe attendu +1 : dans le papier l'or monte en detresse (flight-to-quality) et "
    "la detresse est un rendement negatif ; je lis un score = rendement de seance, "
    "dont le signe positif signifie que le mouvement de seance se prolonge. Le papier "
    "n'annonce aucun sens de prediction ; ce choix est le plus simple.",
    "BEKK, poids de variance minimale, Savitzky-Golay, APARCH/FIAPARCH : non transposables "
    "(parametres ou fenetres absents, estimation plein echantillon), non codes.",
    "mise a l'echelle 100 reprise de la recette (return_scaling) ; ancrage, une barre par "
    "seance, delegues a _common.run avec horizon_bars=30 (la valeur par defaut du contrat, "
    "aussi la fenetre de 30 jours de la recette).",
    "la premiere barre de la seance (position 0) n'a pas de rendement : aucun score.",
)


def _predictor(closes, position):
    if position <= 0:
        return None
    p0 = float(closes.iloc[0])
    pt = float(closes.iloc[position])
    if not (p0 > 0 and pt > 0):
        return None
    return 100 * math.log(pt / p0)


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series}."""
    return _common.run(panel, _predictor, cells=cells, horizon_bars=horizon_bars)
