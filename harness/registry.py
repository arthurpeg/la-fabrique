"""The registry writer. The only place an IC is allowed to come into existence.

Invariant III: every IC computed is written to registry/tests.jsonl, append-only.
Phase 04 will make the bypass impossible by construction; that is a different
obligation from this one, which starts now. A count added afterwards is a count
lost -- there is no reconstructing how many things were tried.

WHAT IS COUNTED IS NOT WHAT IS WRITTEN. Every line is written. Only the lines
carrying a hypothesis count towards the FDR denominator and towards the deflated
Sharpe of phase 15; a calibration of the harness is recorded, and excluded
(D04 4). The distinction lives in the `stage` field and in `hypothesis_ref`,
never in someone's memory of which run was which.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "registry" / "tests.jsonl"
HARNESS = Path(__file__).resolve().parent


def code_hash() -> str:
    """A fingerprint of the harness as it stands, so a stale result can be spotted."""
    digest = hashlib.sha256()
    for path in sorted(HARNESS.glob("*.py")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def new_test_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"T-{stamp}-{uuid.uuid4().hex[:6]}"


def append(record: dict) -> str:
    """Write one line. Never rewrite, never sort, never reformat."""
    required = (
        "test_id", "timestamp", "signal_id", "hypothesis_ref", "stage",
        "data_slice", "horizon", "ic", "t_stat", "requested_by", "code_hash",
    )
    missing = [field for field in required if field not in record]
    if missing:
        raise ValueError(f"the registry line is missing {missing}; see registry/SCHEMA.md")

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with REGISTRY.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return record["test_id"]


def record_ic(
    *,
    ic: float,
    t_stat: float,
    horizon: str,
    data_slice: str,
    signal_id: str,
    hypothesis_ref: str | None,
    stage: str,
    extra: dict | None = None,
) -> str:
    """The one call that turns a computed IC into a registered one."""
    record = {
        "test_id": new_test_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "signal_id": signal_id,
        "hypothesis_ref": hypothesis_ref,
        "stage": stage,
        "data_slice": data_slice,
        "horizon": horizon,
        "ic": None if ic != ic else round(float(ic), 6),
        "t_stat": None if t_stat != t_stat else round(float(t_stat), 4),
        "requested_by": os.environ.get("RSL_REQUESTED_BY", "agent"),
        "code_hash": code_hash(),
    }
    if extra:
        record.update(extra)
    return append(record)


def counted_tests() -> int:
    """The FDR denominator: registered lines that are hypothesis tests, not calibrations."""
    if not REGISTRY.exists():
        return 0
    total = 0
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("hypothesis_ref"):
            total += 1
    return total
