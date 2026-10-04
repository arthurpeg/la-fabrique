"""Momentum intraday : le rendement du premier segment de séance comme
prédicteur du rendement du dernier segment de la MÊME séance.

Fiche : « The Impact of Intraday Momentum on Stock Returns: Evidence from
S&P500 and CSI300 » (Hossain, Gavurová, Yuan, Hasan, Oláh, 2021).

Ce que la fiche demande, et ce qui est codé ici
-----------------------------------------------
La recette (clé ``formula``) donne une régression prédictive intra-séance
``IMreturn_last,t = alpha + beta * IMreturn_1,t + eps`` : le rendement de la
première demi-heure prédit celui de la dernière demi-heure du même jour. Le
seul objet exploitable comme score est le membre de droite, c'est-à-dire le
rendement de la première demi-heure de la séance courante
(``inputs[0] = first_half_hour_return``, connu « à 10:00 Eastern Time du jour
t »). C'est exactement ce que ce module calcule.

Ne sont PAS codés, et pourquoi :

* la régression OLS elle-même, ses pentes (0.102, 0.219, 0.193 …) et ses R² :
  ce sont des résultats annoncés in-sample sur 2020-01-01 → 2020-09-11, pas
  une recette de score. Estimer beta ici demanderait la cible, donc la fin de
  la séance : du look-ahead. Le score est donc le prédicteur brut, dont le
  papier dit que la pente est positive (d'où ``EXPECTED_SIGN = +1``) ;
* l'avant-dernière demi-heure (``predictor_index_second_last_sp500 = 12``) :
  la fiche dit elle-même (``transposability.what_transfers``) que sur plein
  échantillon ce prédicteur ne porte rien ; la version conjointe exigerait
  deux coefficients que le papier ne donne qu'in-sample ;
* les conditionnements (signe, terciles de volatilité et de volume, lundi) :
  ``tercile_cutoffs`` et ``volatility_measure_window`` sont ``null`` dans la
  recette, et le papier trie « all trading days in our sample », donc avec de
  l'information postérieure à la date de décision. Rien de cela n'est
  reproductible sans inventer un paramètre ;
* les t-stats Newey-West (``newey_west_lags = null``) et les seuils de
  significativité : hors du chemin d'un score ;
* tout le Panel B / CSI300 : la fiche déclare sa grille horaire (pause
  déjeuner, 8 demi-heures) sans analogue dans notre univers.

Ce que la fiche ne donne pas, et ce qui a été fait à la place
------------------------------------------------------------
* La définition du rendement de demi-heure (log ou arithmétique) n'est pas
  vérifiable : rendement arithmétique simple, qui n'introduit aucune
  constante.
* Le « prix de la demi-heure » n'a aucune convention d'échantillonnage dans le
  papier : la clôture de barre, seule série que la couche de données recolle.
* Le point de départ de la première demi-heure du S&P500 est la clôture de la
  veille à 16:00 (le gap overnight est donc dedans). Ce point de départ est
  hors de la séance courante : un prédicteur ne reçoit que les clôtures de sa
  séance. Le segment est donc mesuré à l'intérieur de la séance, de sa
  première clôture disponible au prix trente minutes après son ouverture.
  C'est le seul écart de fond avec la fiche, et il est inévitable ici.

Aucun score n'est posé ailleurs qu'à l'ancre de ``_common.run`` : une barre
par séance et par cellule, à ``horizon_bars`` de la clôture déclarée de la
fenêtre. Le papier lit son prédicteur à 10:00 ; nous le lisons aussi, mais
nous posons le score à l'ancre, comme le harnais l'exige.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "the-impact-of-intraday-momentum-on-stock-returns-W4200303559"
HYPOTHESIS = None
PAPER = (
    "Hossain, Gavurova, Yuan, Hasan, Olah (2021), The Impact of Intraday "
    "Momentum on Stock Returns: Evidence from S&P500 and CSI300, "
    "E&M Economics and Management, 24(4), 124-141"
)
EXPECTED_SIGN = +1

CHOICES = (
    "La fiche decrit une regression OLS predictive intra-seance ; j'ai code le "
    "seul membre observable a la date de decision, le rendement de la premiere "
    "demi-heure de la seance courante (recipe.inputs 'first_half_hour_return', "
    "connu a 10:00 ET), parce qu'estimer la pente demanderait la cible, donc la "
    "fin de la seance.",
    "La fiche annonce des pentes positives pour ce predicteur (0.102 plein "
    "echantillon, 0.219 quand la premiere demi-heure est positive, 0.193 le "
    "lundi) ; EXPECTED_SIGN = +1, le score est le rendement du premier segment "
    "lui-meme, sans remise a l'echelle par une pente in-sample.",
    "La longueur du segment est 'half_hour_interval_minutes' = 30 minutes de la "
    "recette (seule constante numerique du code hors conventions de langage et "
    "arithmetique d'horloge) ; elle est mesuree en MINUTES ENTIERES depuis "
    "l'horodatage d'ouverture de la premiere barre de la seance, jamais en "
    "heures flottantes.",
    "La recette mesure la premiere demi-heure du S&P500 depuis la cloture de la "
    "veille a 16:00, donc gap overnight inclus ; un predicteur ne recoit que les "
    "clotures de SA seance, le point de depart est donc la premiere cloture "
    "disponible de la seance courante et non la cloture de la veille. Le segment "
    "code court de cette premiere cloture au prix trente minutes apres "
    "l'ouverture de la seance. Ecart assume, impossible a combler sans lire une "
    "autre seance.",
    "L'ambiguite 'rendement log ou arithmetique' est non resolue dans la fiche "
    "(formules 1 et 2 non rendues par l'extraction) : rendement arithmetique "
    "simple (prix final / prix initial - 1), qui n'introduit aucune constante "
    "nouvelle.",
    "L'ambiguite 'quel prix represente une demi-heure' est non resolue : j'ai "
    "pris la cloture de barre, la seule serie que la couche de donnees recolle "
    "a travers les raccords de contrat.",
    "Le prix de fin du premier segment est la cloture de la derniere barre dont "
    "l'ouverture est strictement anterieure a trente minutes apres l'ouverture "
    "de la seance : une barre horodatee a son ouverture cloture a la fin de son "
    "intervalle, donc cette barre cloture au plus tard a l'instant +30 minutes.",
    "Si la barre notee tombe avant la fin du premier segment, ou si la seance "
    "observee jusqu'a cette barre ne depasse pas trente minutes, le predicteur "
    "rend None : aucun score n'est ecrit plutot qu'un score lu sur un segment "
    "incomplet.",
    "Les conditionnements du papier (signe du premier segment, terciles de "
    "volatilite et de volume, lundi matin) ne sont pas codes : "
    "'tercile_cutoffs', 'volatility_measure_window' valent null dans la recette, "
    "et le tri du papier porte sur 'all trading days in our sample', donc sur de "
    "l'information posterieure a la date de decision. Les coder demanderait "
    "d'inventer un parametre.",
    "L'avant-derniere demi-heure (parametres 12 / 7) n'est pas codee : la fiche "
    "declare elle-meme qu'elle ne porte rien sur plein echantillon, et la "
    "variante conjointe exige deux pentes in-sample.",
    "recipe.market.exact_roots ne nomme que 'ES' et sessions 'US' ; je ne filtre "
    "pourtant aucune cellule, parce que 'transposability.what_transfers' declare "
    "le motif 'implementable sur nos neuf futures intraday' et que l'ancrage de "
    "run se lit sur la cloture declaree de chaque fenetre. Le score est donc "
    "calcule sur toutes les cellules que l'appelant retient.",
    "Le signe du score n'est pas binarise en long/short : la regle de trading du "
    "papier est contradictoire (sortie du marche d'un cote, position courte de "
    "l'autre, et une troisieme version inverse en Discussion). Le score reste la "
    "valeur continue du rendement du premier segment, dont le signe suffit a "
    "retrouver la regle.",
    "Jours feries, seances ecourtees et jours manquants ne sont pas traites par "
    "le papier : chaque seance est traitee independamment des autres, telle que "
    "la couche de donnees la decoupe ; une seance trop courte ou dont les "
    "clotures utiles sont absentes ne produit simplement pas de score.",
    "horizon_bars est transmis tel quel a _common.run, sans valeur par defaut "
    "dans scores() : la fiche n'exprime son horizon qu'en 'derniere demi-heure "
    "de la meme seance', ce n'est pas un nombre de barres.",
)

# recipe.parameters > half_hour_interval_minutes = 30 minutes
_HALF_HOUR_MINUTES = 30


def _first_segment_return(closes: pd.Series, position: int) -> float | None:
    """Rendement du premier segment de la seance, lu jusqu'a `position`.

    Ne lit aucune barre posterieure a `position`.
    """
    if position < 0 or position >= len(closes):
        return None

    seen = closes.iloc[: position + 1]
    if len(seen) < 2:
        return None

    index = pd.DatetimeIndex(seen.index)
    opened_at = index[0]
    # minutes entieres ecoulees depuis l'ouverture de la premiere barre vue
    elapsed = (index - opened_at) // pd.Timedelta(minutes=1)
    elapsed = np.asarray(elapsed, dtype="int64")

    # la seance vue doit depasser le premier segment, sinon il est incomplet
    if elapsed[-1] < _HALF_HOUR_MINUTES:
        return None

    inside = np.flatnonzero(elapsed < _HALF_HOUR_MINUTES)
    if inside.size < 1:
        return None
    end = int(inside[-1])
    if end < 1:
        return None

    values = np.asarray(seen.to_numpy(), dtype="float64")
    start_price = values[0]
    end_price = values[end]
    if not np.isfinite(start_price) or not np.isfinite(end_price):
        return None
    if start_price == 0:
        return None

    return float(end_price / start_price - 1)


def scores(panel, cells=None, *, horizon_bars: int):
    """Rend {(root, window): pd.Series} : le rendement du premier segment."""
    return _common.run(
        panel,
        _first_segment_return,
        cells,
        horizon_bars=horizon_bars,
    )
