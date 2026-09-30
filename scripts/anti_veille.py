"""Empêcher la mise en veille du PC pendant un long travail.

Le superviseur de la moisson meurt quand le PC se met en veille (code de
sortie 4, vu le 2026-09-29) : il se relance ensuite, mais le temps perdu est
perdu. Windows offre `SetThreadExecutionState`, qui dit au système « ce
processus travaille, ne dors pas ». L'effet dure tant que le fil qui l'a
demandé vit, et cesse de lui-même à sa mort : rien ne reste bloqué si le
script tombe.

**Ce que ça empêche** : la veille automatique pour inactivité. **Ce que ça
n'empêche pas** : la veille demandée à la main, ni la fermeture du capot si
Windows est réglé pour dormir alors — ce réglage-là est à l'opérateur.
L'écran, lui, peut s'éteindre : seul le système reste éveillé.

    python scripts/anti_veille.py --pid 26380   # garde éveillé tant que ce processus vit
    python scripts/anti_veille.py --minutes 90  # garde éveillé 90 minutes

Dans le code : `with eveille(): ...` (c'est ce que fait `pipeline_runner.py`).
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import os
import sys
import time

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def _demander(flags: int) -> bool:
    if os.name != "nt":
        return False
    return bool(ctypes.windll.kernel32.SetThreadExecutionState(flags))


@contextlib.contextmanager
def eveille():
    """Le système reste éveillé dans ce bloc ; hors de Windows, ne fait rien."""
    actif = _demander(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    try:
        yield actif
    finally:
        if actif:
            _demander(ES_CONTINUOUS)


def vivant(pid: int) -> bool:
    if os.name == "nt":
        synchronize = 0x00100000
        h = ctypes.windll.kernel32.OpenProcess(synchronize, False, pid)
        if not h:
            return False
        try:
            # WAIT_TIMEOUT (0x102) : le processus tourne encore.
            return ctypes.windll.kernel32.WaitForSingleObject(h, 0) == 0x102
        finally:
            ctypes.windll.kernel32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Empêcher la veille du PC")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pid", type=int, help="tant que ce processus vit")
    g.add_argument("--minutes", type=float, help="pendant cette durée")
    a = ap.parse_args(argv)
    with eveille() as actif:
        if not actif:
            print("anti-veille indisponible (pas Windows, ou refus du système)")
            return 1
        if a.pid is not None:
            if not vivant(a.pid):
                print(f"le processus {a.pid} ne tourne pas")
                return 1
            print(f"PC gardé éveillé tant que le processus {a.pid} tourne", flush=True)
            while vivant(a.pid):
                time.sleep(30)
            print(f"le processus {a.pid} est fini : veille rendue au système")
        else:
            print(f"PC gardé éveillé pendant {a.minutes:g} minutes", flush=True)
            time.sleep(a.minutes * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
