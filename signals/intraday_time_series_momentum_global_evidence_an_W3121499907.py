"""Intraday time series momentum (ITSM) — Li, Sakkas, Urquhart (2022).

Ce que la fiche demande et ce que ce module code
------------------------------------------------
La fiche donne deux objets. Le premier est une regression predictive
(rL_t = alpha + beta_F * rF_t + eps_t) qui ne sert qu'a *mesurer* la
predictibilite. Le second, seul tradable, est une regle de signe sans aucun
parametre estime : score = rF_t, position longue sur la derniere demi-heure si
rF_t > 0, courte si rF_t <= 0, tout ferme a la cloture.

C'est ce second objet qui est code ici : le score d'une seance est le rendement
de la premiere demi-heure de cette seance, lu dans les clotures de la seance et
rien d'autre. La regression, l'evaluation hors echantillon en fenetre extensible
(cinq ans d'amorce), et toute la moitie internationale du papier (ACP par
region, prediction croisee par la premiere demi-heure US, dix-huit portefeuilles
globaux, facteur TVC de position nette) ne se transposent pas a neuf futures
intraday : elles supposent seize indices au comptant en devises differentes et
un investisseur en dollars. Elles ne sont pas codees, et la fiche le dit
elle-meme dans `transposability.what_does_not_transfer`.

La these du papier est que l'ITSM est un phenomene *general* : la meme regle,
sans parametre, appliquee marche par marche a tout son univers. Elle est donc
appliquee ici marche par marche a tout notre univers, chaque cellule mesuree
separement comme le papier mesure separement chacun de ses seize indices.

Ce qui manquait, et ce qui a ete fait a la place
------------------------------------------------
- `pclose,t-1` (cloture de la veille), denominateur exact de rF_t dans le
  papier, n'est pas accessible : un predicteur ne recoit que les clotures de SA
  seance. Le denominateur utilise est donc la premiere cloture disponible de la
  seance. Le gap overnight sort du rendement — ce que la fiche signale deja
  comme non capturable sur des futures qui cotent presque en continu.
- Les filtres de prix extremes (1.2 / 0.8 du plus haut / plus bas prix
  journalier « over the sample period ») exigent les extremes de tout
  l'echantillon : ce sont des statistiques sur la serie entiere, interdites par
  la causalite. Ils ne sont pas appliques.
- La conversion en dollars au taux de change a la minute n'a pas d'objet ici, et
  la fiche ne donne de toute facon ni source ni horaires pour ce taux.
- Aucun cout de transaction n'est deduit : le papier n'en donne aucun.
- Le papier *prend position* au debut de la derniere demi-heure. Ici le score est
  pose a l'ancre imposee par `_common.run` (une barre par seance, a
  `horizon_bars` de la cloture declaree de la fenetre). La premiere demi-heure
  est donc *lue* dans les clotures jusqu'a la barre notee, jamais posee ailleurs.
"""

from __future__ import annotations

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

CHOICES = (
    "La fiche donne deux objets ; seul le signal de trading est code. "
    "`recipe.formula` ecrit « score = rF_t, et la position sur la derniere "
    "demi-heure est donnee par son signe » : je rends donc rF_t brut, et non "
    "la position +1/-1. La regle de signe est monotone en rF_t, donc le signe "
    "attendu est le meme ; et un score continu garde l'amplitude que le papier "
    "mesure par sa pente de regression.",
    "Consequence du choix precedent sur `signal_sign_threshold` = 0 : le seuil "
    "large (rF_t <= 0 -> court) ne s'applique qu'a la position discrete. Un "
    "score brut exactement nul reste nul et ne vote dans aucun sens ; je n'ai "
    "pas transforme le score pour forcer le zero du cote court, ce qui aurait "
    "demande un choix que la fiche ne fait pas pour un score continu.",
    "Univers : le papier mesure la MEME regle, sans parametre libre, "
    "separement sur chacun des seize marches de son univers, et sa these est "
    "precisement la generalite de l'effet (« 12 des 16 marches »). Je "
    "l'applique donc separement a chaque cellule que l'appelant soumet, sans "
    "selectionner d'instrument. `recipe.market.exact_roots` = [\"ES\"] et "
    "`recipe.market.sessions` = [\"US\"] nomment le plus proche analogue de "
    "l'indice americain, mais s'y restreindre coderait un resultat pays "
    "isole du papier, non sa these ; et aucune de nos neuf racines n'est un "
    "indice au comptant, donc aucune n'est l'objet du papier plus qu'une "
    "autre.",
    "`pclose,t-1` est hors d'atteinte d'un predicteur qui ne voit que sa propre "
    "seance : le denominateur de rF_t est la premiere cloture disponible de la "
    "seance, pas la cloture de la veille. Le rendement mesure donc la premiere "
    "demi-heure hors gap overnight. La fiche classe elle-meme le gap dans ce "
    "qui ne se transpose pas (« un future qui cote presque en continu n'a pas "
    "de gap overnight au meme sens »).",
    "Aucun prix d'ouverture n'est utilise : `_common.cell_bars` rend des "
    "clotures recollees. La fenetre du matin va donc de la premiere cloture de "
    "la seance au repere des 30 minutes, et non de l'ouverture a ce repere.",
    "« dernier prix des 30 premieres minutes » : je prends la cloture de la "
    "derniere barre dont l'ouverture est strictement anterieure au repere des "
    "30 minutes. Une barre est horodatee a son ouverture ; cette barre est donc "
    "la derniere a se terminer au plus tard au repere, quelle que soit la "
    "duree des barres du panel. Une inegalite large aurait inclus une barre qui "
    "s'ouvre au repere et deborde la demi-heure.",
    "Le repere des 30 minutes est compte depuis l'horodatage de la premiere "
    "barre de la seance, en minutes entieres (minute du jour, modulo la "
    "journee pour une seance qui franchit minuit), jamais en heures flottantes. "
    "C'est la lecture de l'ambiguite « les 30 minutes sont-elles comptees sur "
    "l'horaire officiel ou sur les observations presentes ? », que la fiche "
    "tranche en faveur des horodatages observes.",
    "Si aucune barre visible jusqu'a la barre notee n'atteint le repere des 30 "
    "minutes, la demi-heure n'est pas close : aucun score n'est rendu (None) "
    "plutot qu'un rendement tronque qui ne serait pas la grandeur du papier.",
    "Les scores sont poses a l'ancre de `_common.run`, une barre par seance et "
    "par cellule, parce que `D51` l'impose. Le papier prend position au debut "
    "de la derniere demi-heure : cet instant precis n'est pas reproductible "
    "sans poser le score ailleurs, ce qui est refuse. Le predicteur se contente "
    "donc de lire la premiere demi-heure dans les clotures jusqu'a la barre "
    "notee.",
    "La pause dejeuner et l'heterogeneite des horaires (Tokyo) sont signalees "
    "par la fiche sans consequence tranchee : je ne traite aucune pause a part. "
    "La premiere barre de la seance telle que la donne le panel sert de debut "
    "de seance, conformement a la resolution « premier enregistrement du jour "
    "comme ouverture ».",
    "Les filtres de prix 1.2 / 0.8, l'amorce de cinq ans, le tri en trois "
    "groupes a 30 %, le spread High-Low sur cinq minutes, le facteur 100 "
    "d'echelle des pentes, les 2000 replications bootstrap et les valeurs "
    "critiques ENC-NEW appartiennent a la partie mesure ou conditionnement du "
    "papier, pas au signal : aucun de ces nombres n'entre dans le code.",
    "Aucun parametre absent n'a ete invente : `volatility_scaling` et "
    "`transaction_costs` sont null dans la recette parce que le papier n'en "
    "applique aucun — le score n'est donc ni normalise par une volatilite ni "
    "ampute d'un cout. `returns_annualization` est null et ne concerne que les "
    "rendements rapportes, pas le score.",
    "Jours manquants : une seance sans barre atteignant le repere des 30 "
    "minutes, ou dont la premiere cloture est nulle ou non finie, est omise "
    "sans interpolation ni report de la veille, la fiche ne disant rien d'un "
    "jour manquant.",
)

# `recipe.parameters.interval_minutes` = 30 minutes
# (« we divide each trading day into 30-minute non-overlapping intervals »).
INTERVAL_MINUTES = 30

# Arithmetique d'horloge, valeurs du depot et non du papier.
MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR


def _first_half_hour_return(closes: pd.Series, position: int) -> float | None:
    """rF_t lu dans les clotures de la seance, jusqu'a `position` incluse.

    Rend `None` si la premiere demi-heure n'est pas close dans ce qui est
    visible, ou si son prix de reference est inutilisable.
    """
    if position < 0 or position >= len(closes):
        return None

    visible = closes.iloc[: position + 1]
    index = visible.index

    minute_of_day = (
        np.asarray(index.hour, dtype=np.int64) * MINUTES_PER_HOUR
        + np.asarray(index.minute, dtype=np.int64)
    )
    elapsed = (minute_of_day - minute_of_day[0]) % MINUTES_PER_DAY

    in_window = elapsed < INTERVAL_MINUTES
    if bool(in_window.all()):
        # La demi-heure n'est pas encore refermee : rien a rendre.
        return None

    values = np.asarray(visible.to_numpy(), dtype=float)
    base = values[0]
    last = values[in_window][-1]
    if not np.isfinite(base) or not np.isfinite(last) or base == 0:
        return None

    return float(last / base - 1)


def scores(panel, cells=None, *, horizon_bars: int):
    """Rend {(root, window): pd.Series} — un score de rF_t par seance."""
    return _common.run(
        panel,
        _first_half_hour_return,
        cells,
        horizon_bars=horizon_bars,
    )
