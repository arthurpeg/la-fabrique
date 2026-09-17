"""Where things live. No absolute path is hard-coded outside this module.

The measurement scripts of phase 01 resolve the data root their own way, on
purpose: they are frozen. This is the phase-02 copy, and the only one the
Panel uses.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOGUE = REPO / "catalogue" / "catalogue.yaml"


def data_dir() -> Path:
    """The data root, from RSL_DATA_DIR in the environment or in .env."""
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
