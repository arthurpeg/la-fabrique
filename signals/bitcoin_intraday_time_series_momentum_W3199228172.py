"""Shen, Urquhart & Wang (2022), Bitcoin intraday time-series momentum.

Signal principal de la fiche : r_ONFH,t = p(ouverture+30 min, t) / p(cloture, t-1) - 1,
qui predit positivement le rendement de la derniere demi-heure de la seance.

Transposition declaree (signal honnetement diminue) :

- le papier porte sur du BTC au comptant 24h/24 ; nos instruments sont des futures
  a seances. L'ouverture « au pic de volume » (regle de detection non chiffree,
  heures fixees ex post sur tout l'echantillon, Table 1) n'a pas d'equivalent :
  l'ouverture retenue est la premiere barre de la seance que le harnais fournit ;
- le predicteur ne recoit que les clotures d'UNE seance : la cloture de la veille
  (p(c, t-1)) n'est pas accessible. Le prix de reference est donc la cloture de la
  premiere barre de la seance, ce qui ne garde de r_ONFH que sa composante
  « premiere demi-heure » et perd la composante nocturne, celle que le papier
  donne pour dominante (t 5.28 contre 2.09) ;
- la cible (derniere demi-heure de la seance) est celle que `_common.run` mesure :
  le score est pose a la premiere barre a au plus `horizon_bars` de la cloture
  declaree de la fenetre, et la valeur par defaut de `horizon_bars` vaut 30,
  soit la demi-heure du papier sur des barres d'une minute ;
- ni le predicteur secondaire r_SLH, ni la version combinee, ni l'allocation
  moyenne-variance, ni le conditionnement par terciles (formes sur l'annee ou
  l'echantillon entiers, donc avec look-ahead) ne sont codes ici.
"""

from __future__ import annotations

import math

import pandas as pd

from signals import _common

SIGNAL_ID = "bitcoin-intraday-time-series-momentum-W3199228172"
HYPOTHESIS = None
PAPER = (
    "Shen, D., Urquhart, A., Wang, P. (2022), Bitcoin intraday time-series "
    "momentum, Financial Review 57 (2), pp. 319-344"
)
EXPECTED_SIGN = +1

# recipe.parameters.first_half_hour_minutes
FIRST_HALF_HOUR_MINUTES = 30

CHOICES = (
    "La fiche donne trois regles de timing (ONFH, SLH, combinee) ; j'ai code le "
    "predicteur principal r_ONFH seul, parce que la fiche le designe comme "
    "« Score principal » et que c'est lui que la transposabilite retient en premier.",
    "EXPECTED_SIGN = +1 : r_ONFH predit positivement la derniere demi-heure "
    "(beta_ONFH = 0.968, t 4.38 ; long si r_ONFH > 0).",
    "Le score est la valeur continue de r_ONFH et non sa regle de timing binaire "
    "(long si > 0, short si <= 0) : le signe du score porte la meme decision, et "
    "la valeur garde l'information que la regression du papier exploite.",
    "La cloture de la veille p(c, t-1) n'est pas lisible par un predicteur qui ne "
    "recoit qu'une seance ; je l'ai remplacee par la cloture de la premiere barre "
    "de la seance. Consequence : la composante nocturne de r_ONFH est perdue, il "
    "ne reste que la premiere demi-heure.",
    "L'ouverture au « pic de volume » (9:00 a 9:40 EST par plateforme, regle non "
    "chiffree, fixee ex post) n'a pas d'equivalent sur nos futures ; j'ai pris "
    "l'ouverture de la seance fournie par le harnais, sans recopier les heures "
    "crypto de la Table 1 (545, 540, 555, 580 minutes), qui ne concernent pas nos "
    "instruments.",
    "Le prix a ouverture+30 min est la cloture de la derniere barre horodatee au "
    "plus 30 minutes apres l'horodatage de la premiere barre de la seance ; "
    "comparaison faite sur des Timestamp et un Timedelta en minutes entieres, "
    "jamais en heures flottantes.",
    "Si la seance n'a pas encore atteint ouverture+30 min a la barre notee "
    "(derniere barre lue anterieure a cet instant), aucun score n'est produit "
    "(None) : la demi-heure d'ouverture n'est pas complete.",
    "Le score est pose par _common.run (une barre par seance et par cellule, la "
    "premiere a au plus horizon_bars de la cloture declaree), avec horizon_bars = "
    "30 par defaut : c'est la derniere demi-heure de la seance, transposition de "
    "la fenetre cible 16:30-17:00 EST ; la cloture a 17:00 EST (pause CME) n'est "
    "pas recopiee, la fenetre cible est celle de nos propres horaires.",
    "Heure d'ete, week-ends, definition du jour t : non traites par le papier ; "
    "sans objet ici puisque tout se lit a l'interieur d'une seance du harnais.",
    "Prix d'un instant non precise par le papier (dernier tick, VWAP) : j'ai pris "
    "les clotures recollees de barre que fournit le harnais.",
    "Prix nul, manquant ou non fini a l'une des deux bornes : aucun score (None), "
    "sans remplissage.",
)


def _onfh(closes: pd.Series, position: int) -> float | None:
    """r_ONFH transpose, lu uniquement jusqu'a `position` incluse."""
    if position < 0 or position >= len(closes):
        return None
    seen = closes.iloc[: position + 1]
    index = seen.index
    start = index[0]
    limit = start + pd.Timedelta(minutes=FIRST_HALF_HOUR_MINUTES)
    if index[-1] < limit:
        return None
    within = seen[index <= limit]
    if len(within) == 0:
        return None
    p_ref = float(seen.iloc[0])
    p_o30 = float(within.iloc[-1])
    if not (math.isfinite(p_ref) and math.isfinite(p_o30)) or p_ref == 0:
        return None
    value = p_o30 / p_ref - 1
    if not math.isfinite(value):
        return None
    return value


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} du r_ONFH transpose."""
    return _common.run(panel, _onfh, cells=cells, horizon_bars=horizon_bars)
