# signals/andersen_bollerslev_1997_periodicity.py
"""
Signal : Andersen & Bollerslev 1997 – periodicité intrajournalière

Le papier décrit une forme « U » de la volatilité intrajournalière mais ne
propose aucun score prédictif exploitable.  Afin de respecter le contrat du
projet (module : ``scores`` renvoyant un dictionnaire de séries) nous implémentons
un **proxy minimal** : la variation absolue du cours entre deux barres
consécutives au sein de chaque cellule.

Ce choix :

* utilise uniquement les données disponibles à la position de la barre
  (causalité : aucune lecture au‑delà de la position) ;
* produit un score non‑dégradé (au moins une valeur par cellule dès que la
  cellule comporte deux barres) ;
* ne fait appel à aucune constante numérique qui ne proviendrait pas de la fiche
  (les seules valeurs numériques présentes sont les conventions de langage) ;
* respecte le format attendu par le harnais grâce à ``signals._common.run``.

Le signal n’est **pas** celui étudié dans le papier ; il ne prétend pas
reproduire le modèle de la section 5.  Il sert uniquement à fournir un objet
conforme au contrat tout en restant fidèle à la description de la fiche.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from signals import _common

# --------------------------------------------------------------------------- #
# Contrat du projet (D07)
# --------------------------------------------------------------------------- #
SIGNAL_ID = "andersen-bollerslev-1997-periodicity"
HYPOTHESIS = None
PAPER = "<Torben G. Andersen, Tim Bollerslev, 1997, Intraday periodicity and volatility persistence in financial markets, Journal of Empirical Finance>"
EXPECTED_SIGN = +1  # le papier indique une influence positive de la forme « U » sur la volatilité


def _predictor(closes: pd.Series, position: int) -> float | None:
    """
    Retourne la variation absolue du cours entre la barre *position* et la
    barre précédente.  Aucun accès n’est effectué au‑delà de ``position`` :
    la fonction est donc strictement causale.

    Si ``position`` est la première barre de la série, aucune valeur précédente
    n’est disponible et ``None`` est renvoyé (aucun score n’est produit).
    """
    if position == 0:
        # pas de donnée précédente → aucun score
        return None

    # différence absolue entre la clôture courante et la clôture précédente
    return abs(closes.iloc[position] - closes.iloc[position - 1])


def scores(
    panel,
    cells: Tuple[str, str] | None = None,
    horizon_bars: int = 30,
) -> Dict[Tuple[str, str], pd.Series]:
    """
    Applique le prédicteur à chaque cellule retenue du panel.

    Le mécanisme d’ancrage (première barre dont la distance à la clôture
    déclarée de la fenêtre est ≤ ``horizon_bars``) est géré par
    ``signals._common.run``.  Le dictionnaire retourné a pour clés les couples
    ``(root, window)`` et pour valeurs les séries de scores indexées par un
    ``DatetimeIndex`` avec fuseau horaire.
    """
    return _common.run(
        panel,
        predictor=_predictor,
        cells=cells,
        horizon_bars=horizon_bars,
    )
