"""The registry. An IC comes into existence HERE, or it does not come into existence.

Invariant III: every IC computed is written to registry/tests.jsonl, append-only.

Phase 03 satisfied that by having a single entry point that happened to write.
Phase 04 removes the "happened to": a pooled IC cannot be computed without a
`Ticket`, a Ticket is only issued here, and the line is written by the same call
that produces the number (D05). There is no state of the world in which the
number exists and the line does not -- not because we are careful, but because
the code that would produce it refuses to run.

WHAT IS COUNTED IS NOT WHAT IS WRITTEN. Every line is written. Only the lines
carrying a hypothesis count towards the FDR denominator and towards the deflated
Sharpe of phase 15; a calibration of the harness is recorded, and excluded
(D04 4). The distinction lives in `stage` and `hypothesis_ref`, never in
someone's memory of which run was which.

WHAT THIS DOES NOT CLAIM. Python has no real encapsulation: whoever writes
`from harness.metric import _pool` still gets a number. What is fabricated here
is the impossibility of doing it WITHOUT a deliberate, visible reach for a
private name -- which gate 04 then looks for, by parsing every module of this
repository. D05 says so in those words rather than pretending otherwise.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "registry" / "tests.jsonl"
HARNESS = Path(__file__).resolve().parent

# The schema, applied at the write. registry/SCHEMA.md documents it in prose and
# is the file a human reads; this is the copy the code enforces. Gate 04 checks
# the two against each other.
REQUIRED = (
    "test_id", "timestamp", "signal_id", "hypothesis_ref", "stage",
    "data_slice", "horizon", "ic", "t_stat", "requested_by", "code_hash",
)
OPTIONAL = ("asof", "cells", "observations", "note")

# The two slices D01 5 left. Not three: the contiguous `validation` block was
# abandoned, and a line naming it would be a line about a world that does not
# exist.
SLICES = ("pool", "holdout")

# Where a test came from. A stage absent from this tuple is a stage nobody
# decided on, so the write is refused rather than silently accepted.
STAGES = (
    "03-calibration",   # the harness measuring itself, gate 03
    "04-audit",         # deliberate bypass attempts, gate 04
    "04-rapport-ic",    # the chain's step 04: the IC report
    "05-regimes",
    "06-controles",
    "07-combinaisons",
    "09-passage",       # the first end-to-end run, phase 09
    "15-holdout",       # the seal, opened once
)
REQUESTED_BY = ("agent", "script", "humain")

TEST_ID = re.compile(r"^T-\d{8}T\d{6}-[0-9a-f]{6}$")
HORIZON = re.compile(r"^\d+(min|h)$")
CODE_HASH = re.compile(r"^[0-9a-f]{16}$")


class RegistryBypass(RuntimeError):
    """Raised when a number was asked for outside the one path that records it."""


def code_hash() -> str:
    """A fingerprint of the harness as it stands, so a stale result can be spotted.

    On CONTENT, not on raw bytes: line endings are folded to \n before hashing.
    Hashing the bytes read off the disk looked equivalent and was not. git
    rewrites line endings on checkout, and a file rewritten by a tool comes back
    with LF, so the mixture drifts file by file: the SAME harness wore four
    different fingerprints across two machines while no line of code changed,
    and gate 04 announced 53 stale registry lines that were not stale.

    That is the dangerous direction. An alarm that rings for a non-reason gets
    learned as noise, and then it no longer warns on the day the harness really
    does change. The repo pins eol=lf in .gitattributes as well; this fold is
    what makes the invariant hold even where that file is not honoured.

    See LECONS.md L12 and decisions/DECISION-10.
    """
    digest = hashlib.sha256()
    for path in sorted(HARNESS.glob("*.py")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()[:16]


def new_test_id() -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    return f"T-{stamp}-{uuid.uuid4().hex[:6]}"


@dataclass
class Ticket:
    """The right to compute ONE pooled IC, and the obligation to record it.

    Issued by `open_test`, spent by `settle`. It carries what the line will say
    about WHY the test happened -- which is why every field is demanded up front,
    before the number is known. An hypothesis named after seeing the result is
    not an hypothesis (invariant IV).
    """

    signal_id: str
    hypothesis_ref: str | None
    stage: str
    data_slice: str
    horizon: str
    _spent: bool = field(default=False, repr=False)

    @property
    def spent(self) -> bool:
        return self._spent

    def claim(self) -> None:
        if self._spent:
            raise RegistryBypass(
                "this ticket is spent. One ticket, one line, one IC -- reusing it "
                "would produce a second number under the first one's line (D05)."
            )
        self._spent = True


def open_test(
    *,
    signal_id: str,
    hypothesis_ref: str | None,
    stage: str,
    data_slice: str,
    horizon: str,
) -> Ticket:
    """Issue the right to compute one IC. Nothing is written yet: nothing exists yet."""
    if not isinstance(signal_id, str) or not signal_id.strip():
        raise ValueError("signal_id is required and must be a non-empty string")
    if hypothesis_ref is not None and (
        not isinstance(hypothesis_ref, str) or not hypothesis_ref.strip()
    ):
        raise ValueError("hypothesis_ref is either None (calibration) or a non-empty string")
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}; registry/SCHEMA.md allows {list(STAGES)}")
    if data_slice not in SLICES:
        raise ValueError(f"unknown slice {data_slice!r}; D01 5 left {list(SLICES)}")
    if not HORIZON.match(str(horizon)):
        raise ValueError(f"unreadable horizon {horizon!r}: expected '30min' or '2h'")
    return Ticket(
        signal_id=signal_id,
        hypothesis_ref=hypothesis_ref,
        stage=stage,
        data_slice=data_slice,
        horizon=str(horizon),
    )


def settle(ticket: Ticket, *, ic: float, t_stat: float, extra: dict | None = None) -> str:
    """Spend the ticket: write the line, then hand the number back. In that order."""
    if not isinstance(ticket, Ticket):
        raise RegistryBypass(
            "a pooled IC needs a Ticket from registry.open_test(). There is no other "
            "way to obtain one, and that is the point (invariant III, D05)."
        )
    ticket.claim()
    record = {
        "test_id": new_test_id(),
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
        "signal_id": ticket.signal_id,
        "hypothesis_ref": ticket.hypothesis_ref,
        "stage": ticket.stage,
        "data_slice": ticket.data_slice,
        "horizon": ticket.horizon,
        "ic": None if ic != ic else round(float(ic), 6),
        "t_stat": None if t_stat != t_stat else round(float(t_stat), 4),
        "requested_by": os.environ.get("RSL_REQUESTED_BY", "agent"),
        "code_hash": code_hash(),
    }
    if extra:
        record.update(extra)
    return append(record)


def _is_utc_iso(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == UTC.utcoffset(None)


def validate_record(record: dict) -> list[str]:
    """Every rule registry/SCHEMA.md states, applied. Returns the failures, named."""
    bad: list[str] = []
    missing = [f for f in REQUIRED if f not in record]
    if missing:
        bad.append(f"missing fields {missing}")
    unknown = [k for k in record if k not in REQUIRED + OPTIONAL]
    if unknown:
        bad.append(f"unknown fields {unknown}: a field nobody decided on is a field nobody reads")

    def typed(name, types, extra_check=None, message=""):
        if name not in record:
            return
        value = record[name]
        if not isinstance(value, types) or isinstance(value, bool):
            bad.append(f"{name}: {value!r} is {type(value).__name__}, expected {types}")
        elif extra_check is not None and not extra_check(value):
            bad.append(f"{name}: {value!r} {message}")

    typed("test_id", str, lambda v: bool(TEST_ID.match(v)), "is not T-<stamp>-<6 hex>")
    typed("timestamp", str, _is_utc_iso, "is not an ISO 8601 UTC instant")
    typed("signal_id", str, lambda v: bool(v.strip()), "is empty")
    typed("stage", str, lambda v: v in STAGES, f"is not one of {list(STAGES)}")
    typed("data_slice", str, lambda v: v in SLICES, f"is not one of {list(SLICES)}")
    typed("horizon", str, lambda v: bool(HORIZON.match(v)), "is not '<n>min' or '<n>h'")
    typed("requested_by", str, lambda v: v in REQUESTED_BY, f"is not one of {list(REQUESTED_BY)}")
    typed("code_hash", str, lambda v: bool(CODE_HASH.match(v)), "is not 16 hex characters")
    typed("cells", int, lambda v: v >= 0, "is negative")
    typed("observations", int, lambda v: v >= 0, "is negative")
    typed("asof", str, lambda v: bool(v.strip()), "is empty")
    typed("note", str, lambda v: bool(v.strip()), "is empty")

    if "hypothesis_ref" in record:
        value = record["hypothesis_ref"]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            bad.append(f"hypothesis_ref: {value!r} is neither null nor a non-empty string")
    for name, bound in (("ic", 1.0), ("t_stat", None)):
        if name not in record:
            continue
        value = record[name]
        if value is None:
            continue
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            bad.append(f"{name}: {value!r} is not a number nor null")
        elif value != value:
            bad.append(f"{name}: NaN is written as null, never as NaN")
        elif bound is not None and abs(value) > bound:
            bad.append(f"{name}: {value} is outside [-{bound}, {bound}]")
    return bad


def append(record: dict) -> str:
    """Write one line. Never rewrite, never sort, never reformat."""
    bad = validate_record(record)
    if bad:
        raise ValueError(
            "this line does not satisfy registry/SCHEMA.md and will not be written: "
            + "; ".join(bad)
        )
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with REGISTRY.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return record["test_id"]


def read_all() -> list[dict]:
    if not REGISTRY.exists():
        return []
    return [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def counted_tests() -> int:
    """The FDR denominator: registered lines that are hypothesis tests, not calibrations."""
    return sum(1 for record in read_all() if record.get("hypothesis_ref"))
