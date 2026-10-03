"""Boyarchenko, Larsen et Whelan (2022), « The Overnight Drift ».

Ce que dit la fiche : RSV_close = (contrats a l'achat - contrats a la vente) /
(contrats a l'achat + contrats a la vente), mesure sur la derniere heure avant
la pause (15:15-16:15 ET), borne dans [-1, 1], predit NEGATIVEMENT le
rendement de la fenetre ou arrive la vague de liquidite suivante (02:00-03:00
ET pour l'ES). RSV negatif (desequilibre vendeur, teneurs de marche longs)
predit un rendement positif.

Ce qui ne se transpose pas, et ce qui a ete fait a la place :

- RSV exige des trades classes acheteur/vendeur par comparaison au sommet du
  carnet. Le panel ne porte que des barres, et ce module n'en lit que les
  clotures recollees (`_common.cell_bars` / `_common.run`). RSV n'est donc pas
  calculable. Substitut declare : une regle de tick a l'echelle de la barre.
  Chaque barre dont la cloture monte par rapport a la precedente compte comme
  une unite « a l'achat », chaque barre dont la cloture baisse comme une unite
  « a la vente », les barres inchangees sont ecartees (cas ambigus). Le score
  est (hausses - baisses) / (hausses + baisses), borne dans [-1, 1] comme RSV.
  Ce n'est PAS le signal du papier : c'est un desequilibre directionnel sans
  volume ni carnet.
- La fenetre de mesure est « la derniere heure » : ici, l'heure (60 minutes
  d'horloge) qui se termine a la cloture de la barre notee, ancree par
  `_common.run` a la fin declaree de la fenetre de seance.
- L'heure cible 02:00-03:00 ET et la fenetre OD+ ne sont pas codees : c'est le
  harnais qui choisit le rendement mesure apres la barre notee. La fiche dit
  elle-meme que coder « 02:00-03:00 » en dur recopierait un resultat, pas un
  mecanisme.
- La variante buy-the-dip (seuil RSV < 0), le conditionnement par le VIX de
  cloture et le double tri en terciles ne sont pas codes : le VIX n'est pas
  dans le panel, et la variante BtD est une strategie, pas un score continu.
"""

from __future__ import annotations

import pandas as pd

from signals import _common

SIGNAL_ID = "boyarchenko-2023-overnight-drift"
HYPOTHESIS = None
PAPER = (
    "Nina Boyarchenko, Lars C. Larsen and Paul Whelan (2022), "
    "The Overnight Drift, Federal Reserve Bank of New York Staff Reports no. 917"
)
EXPECTED_SIGN = -1

CHOICES = (
    "La fiche definit RSV a partir de trades classes au bid/ask ; le panel n'a "
    "que des barres et je ne lis que les clotures recollees : j'ai remplace la "
    "classification par une regle de tick a l'echelle de la barre (cloture en "
    "hausse = une unite a l'achat, en baisse = une unite a la vente), parce que "
    "c'est la seule direction de transaction lisible sans carnet ni volume. "
    "Ce substitut n'est pas le signal du papier.",
    "Chaque barre pese une unite, et non un nombre de contrats : le volume "
    "n'est pas expose par l'interface de _common que je connais ; aucun poids "
    "invente.",
    "Les barres a cloture inchangee sont ecartees du numerateur et du "
    "denominateur : la fiche laisse null le traitement des trades ambigus "
    "(ni au bid ni au ask) ; les ecarter est le choix le plus simple.",
    "« La derniere heure » (15:15-16:15 ET) : j'ai pris les variations de "
    "cloture des barres ouvertes dans les 60 minutes d'horloge qui precedent "
    "et incluent la barre notee, soit une heure qui se termine a la cloture de "
    "la barre notee ; la base de la premiere variation est la cloture de la "
    "barre precedente, deja connue.",
    "L'ancrage a la fin de la fenetre est celui de _common.run (premiere barre "
    "a au plus horizon_bars de la cloture declaree de la fenetre), et non "
    "16:15 ET en dur : la fiche ancre la mesure sur « la derniere heure avant "
    "la pause », que _common.run lit sur l'horloge de la fenetre.",
    "Instruments et seances : la fiche etudie le seul ES et mesure a la "
    "cloture US ; sa section transposabilite dit que le motif (desequilibre de "
    "fin de seance, renversement a l'arrivee de la liquidite suivante) vaut par "
    "instrument et que RSV, borne, se compare entre instruments. J'applique "
    "donc le score a toutes les cellules retenues (cells=None : toutes), sans "
    "filtre de racine ni de seance.",
    "Signe : le score est le RSV proxy brut, et EXPECTED_SIGN = -1, parce que "
    "le papier dit qu'un RSV_close negatif predit un rendement positif "
    "(beta = -17.49 bp par unite de RSV).",
    "Aucune normalisation temporelle (z-score, fenetre glissante) : la recette "
    "dit que RSV est utilise brut, la division par le total tenant lieu de "
    "normalisation.",
    "Si l'heure ne contient aucune barre en hausse ni en baisse (ou s'il n'y a "
    "pas de barre precedente dans la seance), aucun score n'est ecrit (None) "
    "plutot qu'un zero invente.",
    "Non codes : la variante buy-the-dip (RSV < 0), le conditionnement par le "
    "VIX de 16:15 (absent du panel), les fenetres cibles 02:00-03:00 et "
    "01:30-03:30 ET (la cible est choisie par le harnais), l'exclusion des "
    "jours ou l'ecart Londres-New York differe de cinq heures.",
)


def _rsv_proxy(closes: pd.Series, position: int) -> float | None:
    """Desequilibre de tick sur l'heure qui se termine a la barre notee.

    Ne lit rien au-dela de `position`."""
    if position < 1:
        return None
    seen = closes.iloc[: position + 1]
    t_end = seen.index[-1]
    start = t_end - pd.Timedelta(minutes=60)
    moves = seen.diff()
    in_hour = moves[seen.index > start].dropna()
    ups = int((in_hour > 0).sum())
    downs = int((in_hour < 0).sum())
    total = ups + downs
    if total == 0:
        return None
    return (ups - downs) / total


def scores(panel, cells=None, horizon_bars: int = 30):
    """Rend {(root, window): pd.Series} du RSV proxy de fin de fenetre."""
    return _common.run(panel, _rsv_proxy, cells=cells, horizon_bars=horizon_bars)
