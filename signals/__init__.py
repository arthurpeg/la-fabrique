"""The signals. Two of them today, and both are etalons rather than candidates.

D06: gates 05, 06 and 08 each demonstrate themselves against a signal whose
answer is already known -- a look-ahead to inject and catch, a signal to degrade,
an implementation for an agent to reproduce. These two exist for that.

They are HAND-WRITTEN, which is not the same thing as the chain's step 02. The
automatic coding of a signal by an agent is built in phase 08 and stays forbidden
until then; what is built here is its bench (CLAUDE.md, "Les deux ordres").

    from signals import REFERENCE
    module = REFERENCE["gao-2018-intraday-momentum"]
    scores = module.scores(panel)

Their hypotheses are pre-registered in hypotheses/H01 and H02, written before any
measurement (invariant IV), and both were MEASURED on 2026-09-18 -- the first two
counted tests of the project. Both landed in the noise; see hypotheses/README.md.
"""

from signals import baltussen_2021_intraday_momentum as baltussen_2021
from signals import gao_2018_intraday_momentum as gao_2018
from signals import heston_2010_periodicity as heston_2010

# Les DEUX étalons de D06, et eux seuls. Les portes 05, 06 et 08 itèrent sur ce
# dictionnaire : ce qu'on y ajoute devient un sujet d'épreuve pour elles.
REFERENCE = {
    gao_2018.SIGNAL_ID: gao_2018,
    baltussen_2021.SIGNAL_ID: baltussen_2021,
}

# heston_2010 n'est PAS un étalon : c'est la cible de réplication de la clause 2
# de la porte 06 (D12), et son hypothèse H03 porte un motif, pas un signe isolé.
# Il est tenu hors de REFERENCE pour que les portes gardent le sujet que D06 leur
# a donné ; ses propres contrôles vivent dans scripts/check_heston.py.
REPLICATION = {
    heston_2010.SIGNAL_ID: heston_2010,
}

__all__ = [
    "REFERENCE",
    "REPLICATION",
    "baltussen_2021",
    "gao_2018",
    "heston_2010",
]
