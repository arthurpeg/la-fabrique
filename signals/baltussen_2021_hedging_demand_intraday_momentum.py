"""r_ROD — le rendement du reste de la journee, predicteur de la derniere demi-heure.

Ce module code la recette de la fiche `baltussen-2021-hedging-demand-intraday-momentum`,
et elle seule.

Ce que dit la fiche (`signal_construction`)
-------------------------------------------
La journee de negociation va de la cloture du jour t-1 a la cloture du jour t. Elle
est decoupee en cinq intervalles : ON, FH, M, SLH, LH. Le signal retenu est le
rendement du *reste de la journee* :

    r_ROD,t = P(c-30, t) / P(c, t-1) - 1

c'est-a-dire le rendement d'un achat a la cloture de la veille et d'une vente trente
minutes avant la cloture du jour t. Il se lit a c-30, n'utilise que des prix
anterieurs a cet instant, et predit le rendement des trente dernieres minutes
(r_LH). Aucun parametre n'est ajuste.

Le signe attendu
----------------
`EXPECTED_SIGN = +1`. Le `claim` de la fiche est explicite : r_LH est *positivement*
predit par r_ROD (momentum intrajournalier). La regression Eq. (7),
r_LH = a + b_ROD * r_ROD + e, a un b_ROD positif et fortement significatif
(t = 7.29 sur les actions poolees), et la regle de negociation est « longue si le
predicteur est positif, courte sinon ». On rend donc le rendement r_ROD lui-meme,
pas son signe : la regle binaire de la fiche est une transformation monotone de ce
nombre, et la garder continue evite de fabriquer des ex aequo massifs.

Mecanique, et pourquoi elle est causale
---------------------------------------
L'ancrage de la barre notee est delegue a `_common.run` : une barre par seance et
par cellule, la premiere dont la distance a la cloture declaree de la fenetre est au
plus `horizon_bars`. Cet ancrage se lit sur l'horloge, jamais sur les donnees ; avec
`horizon_bars = 30` et des barres d'une minute, il tombe exactement sur le c-30 de
la fiche.

Le predicteur ne reçoit que les clotures d'UNE seance, alors que r_ROD a besoin de
la cloture de la veille. On la fournit par une table construite en amont depuis
`_common.cell_bars` : la derniere clotures de chaque seance, *decalee d'une seance*.
La valeur lue a la seance t est donc celle de la seance t-1, entierement passee — et
elle est identique sur un panel tronque, puisque tronquer ne change pas une seance
deja close (et si la troncature coupe la seance t-1, la seance t n'existe plus et
n'est pas notee). Dans le predicteur, seuls `closes.index[position]` et
`closes.iloc[position]` sont lus : rien au-dela de la position.

Les prix sont ceux de `cell_bars`, recolles, ce qui importe ici plus qu'ailleurs :
r_ROD franchit une frontiere de seance, donc un raccord de contrat non recolle
produirait un faux rendement de nuit.

Ce que la fiche ne donne pas, et qui n'a donc pas ete invente
------------------------------------------------------------
- **Les heures de seance.** Tout le decoupage ON/FH/M/SLH/LH depend des heures
  « communes » du sous-jacent, que les auteurs ne publient pas (`what_is_missing`,
  « available upon request »). Aucune heure n'est ecrite ici : la frontiere est la
  cloture declaree de la fenetre du panel, quelle qu'elle soit.
- **La granularite des barres.** La fiche travaille sur des barres d'une minute
  construites depuis du tick-by-tick. Si le panel est plus grossier, `c-30` n'est pas
  reconstituable a l'identique ; `horizon_bars` reste le seul reglage, et il est
  laisse au harnais plutot que redefini ici.
- **Les couts.** Aucun cout, tick, multiplicateur ni frais de roll n'existe dans le
  papier (`no_transaction_costs_in_results`) : le module n'en porte aucun, alors
  meme que la recette impose un aller-retour quotidien.
- **Le lag de publication et le fuseau de reference** ne sont pas specifies.

Ce qui ne se transpose pas a neuf futures intraday
--------------------------------------------------
- **Le regime de gamma negatif.** C'est pourtant la condition sous laquelle l'effet
  existe (Table 7 : rien de significatif quand NGE(t-1) >= 0, soit environ la moitie
  des jours). Il demande le NGE d'OptionMetrics / SqueezeMetrics et des NAV de LETF,
  donnees que nous n'avons pas. Le signal code ici est donc l'effet
  *inconditionnel*, c'est-a-dire une version diluee de ce que le papier decrit.
- **Les Sharpe de 0.87 a 1.73.** Ils viennent de portefeuilles 1/N de 8 a 21 contrats
  par classe d'actifs. A neuf futures, cette diversification transversale n'existe
  pas ; les chiffres par contrat (Tables B1-B4) sont bien plus faibles. Aucun de ces
  nombres n'est donc une cible, et aucun n'apparait dans ce code.
- **La metrique.** Le papier mesure des R2 poolees, un R2 hors echantillon a fenetre
  extensible (minimum 500 observations) et un Sharpe de strategie binaire. Rien de
  cela n'est un IC ; la validation hors echantillon recursive n'est pas transposee,
  elle appartiendrait au harnais et non au signal.
- **Les predicteurs concurrents** r_ONFH, r_M et r_SLH sont dans la fiche mais sont
  d'autres signaux : un module, un signal. Seul r_ROD est code ici.
- **Le controle de reversion** a un a trois jours et l'arret de la predictabilite a
  la cloture du cash (Table 12) sont des controles, pas des scores : ils ne sont pas
  implementes.
"""

from __future__ import annotations

import pandas as pd

from signals import _common

SIGNAL_ID = "baltussen-2021-hedging-demand-intraday-momentum"
HYPOTHESIS = None
PAPER = (
    "Baltussen, Da, Lammers, Martens (2021), "
    "Hedging demand and market intraday momentum, "
    "Journal of Financial Economics"
)
EXPECTED_SIGN = +1


def _previous_session_close_by_bar(
    closes: pd.Series, sessions: pd.Series
) -> pd.Series:
    """Pour chaque barre, la cloture de la seance precedente — P(c, t-1).

    Construit par decalage d'une seance sur les clotures de seance : la valeur
    portee par les barres de la seance t est celle de la seance t-1, jamais celle
    de la seance t.
    """
    session_close = closes.groupby(sessions).last()
    previous = session_close.shift(1)
    mapped = sessions.map(previous)
    return mapped[~mapped.index.duplicated()]


def _make_predictor(previous_close_by_bar: pd.Series):
    """Le predicteur r_ROD pour une cellule, ferme sur sa table de clotures veille."""

    def predictor(closes: pd.Series, position: int) -> float | None:
        stamp = closes.index[position]
        base = previous_close_by_bar.get(stamp)
        if base is None or pd.isna(base) or base == 0:
            return None
        price = closes.iloc[position]
        if pd.isna(price) or price == 0:
            return None
        return float(price) / float(base) - 1

    return predictor


def scores(panel, cells=None, horizon_bars: int = 30) -> dict:
    """Rend {(root, window): pd.Series} — r_ROD lu a la barre ancree sur l'horloge.

    `horizon_bars` vaut trente par defaut : la fiche predit le rendement des trente
    dernieres minutes de la seance a partir de l'information disponible a c-30
    (`horizon.value` = « 30 minutes »).
    """
    selected = list(cells) if cells is not None else list(panel.cells())

    out: dict = {}
    for cell in selected:
        root, window = cell
        closes, sessions = _common.cell_bars(panel, root, window)
        if closes is None or len(closes) == 0:
            continue

        previous_close_by_bar = _previous_session_close_by_bar(closes, sessions)
        produced = _common.run(
            panel,
            _make_predictor(previous_close_by_bar),
            cells=[(root, window)],
            horizon_bars=horizon_bars,
        )

        for key, series in produced.items():
            if series is None:
                continue
            series = series.dropna()
            if len(series) == 0:
                continue
            out[key] = series

    return out
