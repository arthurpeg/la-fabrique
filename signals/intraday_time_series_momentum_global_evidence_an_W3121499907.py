"""Momentum temporel intrajournalier (ITSM) — Li, Sakkas et Urquhart (2022).

La fiche décrit deux objets. (1) Un prédicteur statistique : le rendement de la
première demi-heure de la séance, rF_t = pfirst30,t / pclose,t-1 − 1, dont la
régression prédictive rL_t = alpha + betaF * rF_t + epsilon_t sur le rendement
de la dernière demi-heure de la MÊME séance donne une pente positive dans 12
marchés sur 16. (2) Une règle de trading qui n'en retient que le signe : long
sur la dernière demi-heure si rF_t > 0, court si rF_t <= 0, tout fermé à la
clôture.

Ce module code l'objet (1) : le score d'une séance est le rendement de sa
première demi-heure. La règle de signe est une transformation monotone de ce
score ; elle n'ajoute rien à une mesure d'association et perdrait le niveau.

Ce que la fiche donne et que ce module NE peut PAS reproduire, faute de données
ou parce que cela violerait la causalité :

- `pclose,t-1`, la clôture de la séance précédente, donc le gap overnight que
  les auteurs incluent explicitement dans rF_t. Le prédicteur ne voit que les
  clôtures de SA séance, et la fiche note elle-même (`what_does_not_transfer`)
  qu'un future qui cote presque en continu n'a pas de gap overnight au même
  sens. Le dénominateur retenu est donc la première clôture de la séance : le
  score est le rendement intra-séance des trente premières minutes, overnight
  exclu. C'est un signal honnêtement diminué, pas le rF_t du papier.
- Le prix exact pris comme `pfirst30,t` et les bornes de minute : la fiche
  laisse l'ambiguïté ouverte (« il ne dit pas lequel des champs disponibles
  (open, high, low, last) est pris »). Ce module n'a que les clôtures recollées
  de `_common.cell_bars`, et s'en sert.
- Le filtre de prix 1.2 / 0.8 : il se calcule sur le plus haut et le plus bas
  journaliers de TOUT l'échantillon. Appliqué ici, il lirait l'avenir. Non
  appliqué.
- Les coûts de transaction, la normalisation par volatilité et la taille de
  position : la recette les donne explicitement `null`. Aucun n'est inventé.
- Toute la moitié internationale du papier (prédictibilité croisée du rendement
  US, 18 portefeuilles globaux, facteur TVC, ACP régionales) et les trois tris
  de conditionnement (crise/récession, liquidité High-Low de Corwin et Schultz,
  information discreteness). Les premiers n'ont pas d'analogue sur neuf futures
  qui ne forment ni régions ni pays ; les seconds sont des régimes, hors du
  contrat de ce module.
- La conversion en dollars au taux de change à la minute : la fiche ne nomme ni
  la source ni les heures de cotation de ce taux.

Aucun IC n'est comparable à ce papier : son évidence est en pentes de
régression, R2 ajusté, R2 hors échantillon, alphas et Sharpe.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from signals import _common

SIGNAL_ID = "intraday-time-series-momentum-global-evidence-an-W3121499907"
HYPOTHESIS = None
PAPER = (
    "Zeming Li, Athanasios Sakkas, Andrew Urquhart (2022), "
    "Intraday time series momentum: global evidence and links to market "
    "characteristics, Journal of Financial Markets"
)
EXPECTED_SIGN = +1

# recipe.parameters.interval_minutes / holding_window_minutes : « we divide each
# trading day into 30-minute non-overlapping intervals. »
INTERVAL_MINUTES = 30

# recipe.market.sessions : la seule séance que le papier date dans un fuseau
# explicite (« the US market between 9:30AM and 4:00PM Eastern Standard Time »).
SESSIONS = ("US",)

CHOICES = (
    "La fiche décrit un prédicteur statistique (rF_t, régression) et une règle "
    "de trading (son signe). J'ai codé le prédicteur statistique : le score est "
    "rF_t lui-même, non +1/-1. Raison : la règle de signe est une "
    "transformation monotone du score et le harnais mesure une association, "
    "pas un rendement de stratégie. Conséquence assumée : le cas rF_t = 0, que "
    "l'équation (6) range du côté court, reste neutre dans un score continu.",
    "La fiche écrit rF_t = pfirst30,t / pclose,t-1 − 1, donc overnight inclus. "
    "Le prédicteur ne reçoit que les clôtures de SA séance : la clôture de la "
    "veille lui est structurellement inaccessible, et la fiche note elle-même "
    "qu'un future quasi continu n'a pas de gap overnight au même sens. J'ai "
    "donc pris comme dénominateur la PREMIÈRE clôture de la séance : le score "
    "est le rendement intra-séance des trente premières minutes. Signal "
    "diminué, déclaré comme tel.",
    "pfirst30,t est « the last price in the first 30 minutes after market "
    "open » et la fiche ne dit ni quel champ de prix ni comment les bornes de "
    "minute sont arrondies. J'ai pris la clôture de la dernière barre dont la "
    "distance à la première barre de la séance est STRICTEMENT inférieure à 30 "
    "minutes : la dernière barre entièrement contenue dans la première "
    "demi-heure, quelle que soit la largeur des barres. Les prix sont les "
    "clôtures recollées rendues par _common, les seules dont je dispose.",
    "L'horloge est lue en minutes entières, par différence d'horodatage avec la "
    "première barre de la séance (division entière par une minute), jamais en "
    "heures flottantes.",
    "Je ne lis jamais au-delà de la barre notée : la fenêtre du matin est "
    "cherchée dans les seules barres d'indice <= position. L'ancrage du score "
    "est celui de _common.run, obligatoire : une barre par séance et par "
    "cellule, à horizon_bars de la clôture déclarée de la fenêtre — c'est-à-"
    "dire exactement le début de la dernière demi-heure du papier quand "
    "l'appelant passe l'horizon de la fiche. horizon_bars est transmis tel que "
    "reçu, sans valeur par défaut.",
    "Aucun score n'est rendu quand la barre notée tombe à l'intérieur de la "
    "première demi-heure (la fenêtre de formation ne serait pas close, et le "
    "papier interdit tout chevauchement entre formation et fenêtre prédite), "
    "ni quand la première demi-heure ne contient qu'une seule barre "
    "(numérateur et dénominateur confondus : le rendement n'est pas "
    "observable). Rendre None n'écrit aucun score.",
    "Univers : la recette nomme ES comme seule correspondance exacte (le S&P "
    "500 du papier) mais le papier applique la MÊME régression par marché à "
    "chacun des marchés de son univers. J'ai donc gardé tous les roots du "
    "panel — nos futures sont notre analogue d'univers — en restreignant les "
    "fenêtres à la séance que la recette nomme, « US ». Si aucune cellule "
    "candidate ne porte ce nom de fenêtre, je retombe sur les cellules "
    "candidates telles qu'elles me sont données, pour ne pas rendre un "
    "dictionnaire vide sur une simple divergence de nommage.",
    "Je n'applique pas le filtre de prix 1.2 / 0.8 de la fiche : il se calcule "
    "sur le plus haut et le plus bas journaliers de tout l'échantillon, donc "
    "il lirait l'avenir de la barre notée.",
    "Aucun coût de transaction, aucune normalisation par volatilité, aucune "
    "taille de position : la recette donne ces trois paramètres à null, et un "
    "paramètre manquant ne s'invente pas. Le score est donc brut, comme tous "
    "les rendements du papier.",
    "Les jours sans donnée ne sont pas comblés : une séance sans barre "
    "exploitable n'écrit simplement pas de score, ce qui suit le traitement du "
    "papier (« the number of available trading days varies from country to "
    "country »). Une cellule sans aucun score est omise du dictionnaire.",
)


def _first_window_return(closes: pd.Series, position: int) -> float | None:
    """Rendement de la première demi-heure de la séance, lu jusqu'à `position`.

    Numérateur : clôture de la dernière barre strictement à moins de
    INTERVAL_MINUTES minutes de la première barre de la séance.
    Dénominateur : clôture de la première barre de la séance (la clôture de la
    veille, dénominateur du papier, est hors de portée du prédicteur).
    """
    total = len(closes)
    if total == 0 or position < 0 or position >= total:
        return None

    index = closes.index
    elapsed = np.asarray((index[: position + 1] - index[0]) // pd.Timedelta(minutes=1))
    inside = np.flatnonzero(elapsed < INTERVAL_MINUTES)
    if inside.size == 0:
        return None

    end = int(inside[-1])
    # end == position : la barre notée est encore dans la première demi-heure.
    # end == 0 : la première demi-heure ne tient qu'une barre, pas de rendement.
    if end == 0 or end == position:
        return None

    try:
        base = float(closes.iloc[0])
        last = float(closes.iloc[end])
    except (TypeError, ValueError):
        return None

    if not math.isfinite(base) or not math.isfinite(last) or base <= 0:
        return None

    return last / base - 1


def scores(panel, cells=None, *, horizon_bars: int):
    """Rend {(root, window): pd.Series} — un score par séance et par cellule."""
    candidates = list(panel.cells()) if cells is None else list(cells)

    selected = [cell for cell in candidates if cell[1] in SESSIONS]
    if not selected:
        selected = candidates
    if not selected:
        return {}

    raw = _common.run(
        panel,
        _first_window_return,
        cells=selected,
        horizon_bars=horizon_bars,
    )

    out = {}
    for key, series in raw.items():
        if series is None:
            continue
        cleaned = series.dropna()
        if len(cleaned) == 0:
            continue
        out[key] = cleaned
    return out
