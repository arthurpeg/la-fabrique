"""Klein, Thu & Walther (2018) -- jours de detresse par VaR historique.

Le papier est descriptif : aucun signal, BEKK/GARCH estimes sur l'echantillon
entier, VaR sur l'echantillon entier, Savitzky-Golay bilateral. Rien de cela ne
se transpose tel quel. Part transposable codee : la VaR empirique q = 1 %, 5 %,
10 % (le ceil(T*q)-ieme plus petit rendement), rendue point-in-time par un
quantile en expansion ; le score est la profondeur du rendement courant sous
ces VaR (positive en detresse).

Ce qui manque et ce qui est fait a la place : pas de BEKK (parametres non
publies), pas de poids de variance minimale, pas de croisement actif/indice.
Le score est calcule sur la cellule elle-meme.
"""

from __future__ import annotations

import numpy as np

from signals import _common

SIGNAL_ID = "bitcoin-is-not-the-new-gold-a-comparison-of-vola-W2799918576"
HYPOTHESIS = None
PAPER = (
    "Klein, Thu & Walther (2018), Bitcoin is not the New Gold - A comparison of "
    "volatility, correlation, and portfolio performance, International Review "
    "of Financial Analysis"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche ne construit aucun signal ; j'ai code seulement la VaR historique des jours de detresse, le reste (BEKK, variance minimale, Savitzky-Golay) n'est ni transposable ni parametre",
    "la VaR est calculee sur tout l'echantillon dans le papier ; j'ai pris un quantile en expansion, au passe de la barre notee, pour la causalite",
    "l'historique du quantile est limite a la seance (le predicteur de _common.run ne voit que les clotures d'une seance) : rendements des barres de la seance avant la barre notee",
    "rendement log x 100 (return_scaling) entre barres successives ; VaR_q = le ceil(n*q/100)-ieme plus petit rendement passe, q = 1, 5, 10 (en %), ceil calcule en entiers",
    "score continu = somme sur q des ecarts (VaR_q - rendement courant) : positif quand le rendement est sous la VaR (detresse, inegalite stricte du papier), negatif sinon ; continu pour ne pas etre degenere, sans poids invente",
    "EXPECTED_SIGN = +1 : le papier ne predit rien ; choix par defaut, un score de detresse plus haut est lu comme un rebond plus fort, sans fondement dans la fiche",
    "cross-asset (or/WTI contre ES) non code : aucune formule de score dans la fiche ; chaque cellule est notee sur elle-meme",
    "horizon_bars vaut None par defaut : la fiche ne donne aucun horizon (null), on laisse l'ancrage par defaut de _common.run",
    "pas de lissage (fenetre et degre Savitzky-Golay null), pas de traitement des week-ends ni des jours feries",
)

_NIVEAUX = (1, 5, 10)
_ECHELLE = 100


def _predictor(closes, position):
    c = np.asarray(closes, dtype=float)[: position + 1]
    r = _ECHELLE * np.diff(np.log(c))
    if len(r) < 2:
        return None
    courant = r[-1]
    passe = np.sort(r[:-1])
    n = len(passe)
    if not np.isfinite(courant) or not np.all(np.isfinite(passe)):
        return None
    score = 0.0
    for q in _NIVEAUX:
        k = max(-((-n * q) // _ECHELLE), 1)
        score += passe[k - 1] - courant
    return float(score)


def scores(panel, cells=None, horizon_bars=None):
    """Rend {(root, window): pd.Series}."""
    if horizon_bars is None:
        return _common.run(panel, _predictor, cells=cells)
    return _common.run(panel, _predictor, cells=cells, horizon_bars=horizon_bars)
