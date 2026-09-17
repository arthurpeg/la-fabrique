"""The signal's own fingerprint, distinct from the harness's.

`D05` left this open: `registry.code_hash()` fingerprints `harness/*.py`, so it
tells you which JUDGE produced a line and says nothing about which ACCUSED. Two
different signals, or two versions of one, land in the registry under the same
harness hash and become indistinguishable the day someone asks whether a result
still holds.

So a signal carries its own hash, computed over its source AND over every helper
of `signals/` it imports -- `signals/_common.py` decides where the anchor falls,
and a change there is a change of signal even if the named file is untouched.
"""

from __future__ import annotations

import hashlib

from sandbox.scan import sources_of


def signal_hash(module) -> str:
    """Sixteen hex characters over the signal's sources, helpers included."""
    digest = hashlib.sha256()
    for path in sources_of(module):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]
