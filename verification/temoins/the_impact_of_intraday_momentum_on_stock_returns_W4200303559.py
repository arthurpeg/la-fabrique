"""Hossain et al. (2021) : le rendement de la premiere demi-heure de la seance
comme prediteur du rendement de la derniere demi-heure de la meme seance.

Ce que le module code : le score d'une cellule, a l'ancre de `_common.run`, est
le rendement de la premiere demi-heure de la seance (IMreturn1), lu dans les
clotures de la seance jusqu'a la barre notee, et rien au-dela.

Ce qui ne se transpose pas, et que le module ne code donc pas :
- la regression OLS, les t-stats de Newey-West, les R2 : le harnais mesure un
  IC, pas une pente ;
- le gap overnight : le papier mesure la premiere demi-heure depuis la cloture
  de la veille a 16:00, ce que le prediteur (qui ne recoit que les clotures de
  la seance courante) ne voit pas ; la premiere demi-heure est ici mesuree a
  l'interieur de la seance ;
- les conditionnements (signe, terciles de volatilite et de volume, lundi) :
  seuils et mesure de volatilite non donnes par le papier, terciles calcules
  sur l'echantillon entier (look-ahead) ; ils relevent des regimes, pas de ce
  signal ;
- l'avant-dernier segment : le papier lui-meme le trouve sans pouvoir
  predictif sur le plein echantillon ;
- la grille du CSI300 (pause dejeuner) : sans analogue.

Parametre manquant : la convention de prix d'une demi-heure et la forme du
rendement (log ou arithmetique) ne sont pas donnees ; voir CHOICES.
"""

from __future__ import annotations

import pandas as pd

from signals import _common

SIGNAL_ID = "the-impact-of-intraday-momentum-on-stock-returns-W4200303559"
HYPOTHESIS = None
PAPER = (
    "Hossain, Gavurova, Yuan, Hasan, Olah (2021), The Impact of Intraday "
    "Momentum on Stock Returns: Evidence from S&P500 and CSI300, "
    "E&M Economics and Management 24(4)"
)
EXPECTED_SIGN = +1

CHOICES = (
    "la fiche dit que le predicteur est IMreturn1, rendement de la premiere "
    "demi-heure, positivement lie au rendement de la derniere demi-heure ; "
    "EXPECTED_SIGN = +1 : le score est le rendement de la premiere "
    "demi-heure lui-meme, sans inversion de signe, car le papier trouve un "
    "momentum positif (long si le premier segment est positif).",
    "la fiche donne une demi-heure de 30 minutes (parametre derive de 'half "
    "an hour') ; j'ai compris que la premiere demi-heure couvre les 30 "
    "premieres minutes de la seance de la cellule, de la cloture de sa "
    "premiere barre a la derniere cloture dont l'instant est au plus "
    "30 minutes plus tard, parce que cela s'ecrit sur l'horloge des barres "
    "et reste valable si une minute manque.",
    "la fiche mesure la premiere demi-heure du S&P500 depuis la cloture de "
    "la veille a 16:00 (gap overnight inclus) ; le predicteur ne recoit que "
    "les clotures de la seance courante, donc j'ai mesure le rendement a "
    "l'interieur de la seance, sans le gap overnight, et je le declare comme "
    "un ecart a la fiche (les futures cotent quasi en continu).",
    "la fiche ne dit pas si le rendement est logarithmique ou arithmetique "
    "(formules 1 et 2 non rendues) ; j'ai pris l'arithmetique, "
    "cloture_fin / cloture_debut - 1, le choix le plus simple, sans fonction "
    "ni constante en plus.",
    "la fiche ne dit pas quel prix represente une demi-heure ; j'ai pris la "
    "derniere cloture 1 minute de l'intervalle (dernier prix connu), parce "
    "que c'est le seul prix connu a la fin de l'intervalle sans regarder au-"
    "dela.",
    "la fiche donne un timing flou (aucune heure d'entree) ; j'ai suivi "
    "l'ancrage obligatoire de _common.run, une barre par seance et par "
    "cellule a horizon_bars de la cloture de la fenetre, avec horizon_bars "
    "transmis tel que recu ; si la barre notee est anterieure a la fin de la "
    "premiere demi-heure, le predicteur rend None (cellule-seance omise) "
    "plutot que d'inventer une valeur.",
    "la fiche decrit un signal de position (long si positif, sinon court ou "
    "sortie, deux versions contradictoires) ; j'ai garde la valeur continue "
    "du rendement comme score, et non son seul signe, parce que le "
    "harnais lit un score de rang/IC et que la formule donne le rendement "
    "comme variable explicative.",
    "la fiche restreint l'univers au S&P500 (racine ES) et au CSI300 ; je "
    "ne filtre pas les cellules par racine : j'applique le meme motif a "
    "toutes les cellules que l'appelant retient, le CSI300 etant "
    "intransposable.",
    "la fiche laisse le conditionnement (signe, terciles de volatilite et "
    "de volume, lundi) et l'avant-dernier segment non codes : seuils et "
    "mesure de volatilite null, terciles sur l'echantillon entier ; je ne les "
    "invente pas.",
    "la fiche ne dit rien des jours feries et seances ecourtees ; aucun "
    "traitement special, une seance trop courte pour atteindre la fin de la "
    "premiere demi-heure a la barre notee ne produit aucun score.",
)

HALF_HOUR_MINUTES = 30


def _first_half_hour_return(closes: pd.Series, position: int) -> float | None:
    """Rendement de la premiere demi-heure, lu jusqu'a `position` inclus."""
    seen = closes.iloc[: position + 1]
    if len(seen) < 2:
        return None
    start_time = seen.index[0]
    end_time = start_time + pd.Timedelta(minutes=HALF_HOUR_MINUTES)
    # La demi-heure doit etre achevee a la barre notee : rien au-dela.
    if seen.index[-1] < end_time:
        return None
    window = seen[seen.index <= end_time]
    first = window.iloc[0]
    last = window.iloc[-1]
    if pd.isna(first) or pd.isna(last) or first <= 0:
        return None
    return float(last / first - 1)


def scores(panel, cells=None, *, horizon_bars: int):
    """Rend {(root, window): pd.Series}."""
    return _common.run(
        panel,
        _first_half_hour_return,
        cells=cells,
        horizon_bars=horizon_bars,
    )
