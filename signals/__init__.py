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

No IC has been computed on either of them. Their hypotheses are pre-registered in
hypotheses/H01 and H02, written before any measurement (invariant IV).
"""

from signals import baltussen_2021_intraday_momentum as baltussen_2021
from signals import gao_2018_intraday_momentum as gao_2018

REFERENCE = {
    gao_2018.SIGNAL_ID: gao_2018,
    baltussen_2021.SIGNAL_ID: baltussen_2021,
}

__all__ = ["REFERENCE", "baltussen_2021", "gao_2018"]
