"""The one deliberate gesture that opens the holdout. It exists so that it cannot be casual.

Invariant V: the holdout is opened once, at the very end. Until phase 04 the
Panel simply refused the sealed slice, which is a refusal anybody could remove by
passing a different argument. What is built here is not secrecy -- the phrase
below is in plain sight -- but the impossibility of opening the seal ABSENTLY:

  1. the caller must set RSL_UNSEAL in the environment to an exact sentence that
     nobody types by accident;
  2. the caller must write down WHY, in prose, at the call site;
  3. the gesture is appended to registry/unseal.jsonl before the token exists.

So the holdout cannot be opened without leaving, in a versioned file, the date
and the stated reason. If that file ever holds two entries, invariant V has been
broken and every number that follows is a validation figure, not a holdout one.

Nothing in this repository calls `unseal_holdout`. Gate 04 checks that by parsing
every module, and will keep checking it until phase 15.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

LEDGER = Path(__file__).resolve().parents[1] / "registry" / "unseal.jsonl"
PHRASE = "PHASE 15 -- J'OUVRE LE HOLDOUT UNE SEULE FOIS"
ENV = "RSL_UNSEAL"


class SealRefused(Exception):
    """The holdout was asked for without the deliberate gesture."""


@dataclass(frozen=True)
class UnsealToken:
    """Proof that the gesture was made. Held by value, never forged from a string."""

    reason: str
    granted_at: str


def unseal_holdout(*, reason: str) -> UnsealToken:
    """Open the seal, on purpose, in writing, once."""
    if not isinstance(reason, str) or len(reason.strip()) < 20:
        raise SealRefused(
            "unseal_holdout(reason=...) wants a written reason, in prose, of at least "
            "twenty characters. A seal opened without a stated reason is a seal opened "
            "by habit."
        )
    if os.environ.get(ENV) != PHRASE:
        raise SealRefused(
            f"{ENV} is not set to the exact sentence that opens the holdout. This is not "
            "a password -- it is in panel/unseal.py, in plain sight. It is there so that "
            "the holdout cannot be opened by an argument someone passed without thinking "
            "(invariant V)."
        )
    entry = {
        "granted_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "reason": reason.strip(),
        "by": os.environ.get("RSL_REQUESTED_BY", "agent"),
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    return UnsealToken(reason=entry["reason"], granted_at=entry["granted_at"])


def times_opened() -> int:
    """How many times the seal has been broken. Anything but 0 or 1 is a broken invariant."""
    if not LEDGER.exists():
        return 0
    return sum(1 for line in LEDGER.read_text(encoding="utf-8").splitlines() if line.strip())
