"""The signal sandbox. Phase 05.

    from sandbox import causality, contract, scan, signature

    bad = contract.validate_module(module) + scan.scan_module(module)
    divergences = causality.check(module, panel)

Three things live here, and only the third is a proof of anything:

  contract.py   what a signal must expose, and what its output must look like.
  scan.py       what it is allowed to import and call -- a white list.
  causality.py  the test: a signal that needed the future stops producing the
                same thing once the future is taken away.

`signature.py` gives a signal its own fingerprint, distinct from the harness's,
which D05 had left open.

The harness is not imported here and must not be: nothing in this package
computes an IC, and the sandbox has no business being able to.
"""

from sandbox import causality, contract, scan, signature

__all__ = ["causality", "contract", "scan", "signature"]
