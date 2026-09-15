"""Shared helpers for the phase-01 measurement scripts.

No hard-coded absolute paths: the data root comes from RSL_DATA_DIR, read from
the process environment or from the repository's .env file.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "scripts" / "out"

# Session convention used by every phase-01 measurement.
# CME Globex opens at 18:00 America/New_York and the whole overnight belongs to
# the NEXT trading date; shifting the New York wall clock by +6h therefore maps
# a session onto a single calendar date. This is a MEASUREMENT convention, not a
# project decision: the authoritative calendar is phase 02's business.
SESSION_TZ = "America/New_York"
SESSION_SHIFT_HOURS = 6


def data_dir() -> Path:
    value = os.environ.get("RSL_DATA_DIR")
    if not value:
        env_file = REPO / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("RSL_DATA_DIR="):
                    value = line.split("=", 1)[1].strip()
                    break
    if not value:
        raise SystemExit("RSL_DATA_DIR is not set (environment or .env).")
    path = Path(value)
    if not path.is_dir():
        raise SystemExit(f"RSL_DATA_DIR does not exist: {path}")
    return path


def manifest() -> dict:
    with (data_dir() / "manifeste.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def series_index() -> list[dict]:
    """The declared series, as the third party describes them. Claims, not facts."""
    return manifest()["series"]


def load(entry: dict, columns: list[str] | None = None) -> pd.DataFrame:
    frame = pd.read_parquet(data_dir() / entry["fichier"], columns=columns)
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise SystemExit(f"{entry['racine']}: index is not a DatetimeIndex")
    return frame


def session_date(index: pd.DatetimeIndex) -> pd.Series:
    local = index.tz_convert(SESSION_TZ) + pd.Timedelta(hours=SESSION_SHIFT_HOURS)
    return pd.Series(local.date, index=index, name="session_date")


def write_json(name: str, payload) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=1, default=str)
    return path
