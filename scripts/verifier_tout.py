"""Toutes les vérifications du projet, en une commande, et un tableau.

Chaque session finissait par relancer à la main une vingtaine de gardes, dans
un ordre retenu de mémoire. Ce script les lance toutes, dit pour chacune si
elle passe, et rend un code de sortie : 0 si tout ce qui doit passer passe.

**Trois familles, et elles ne se jugent pas pareil :**

- **les gardes** — elles doivent passer, toujours. Un échec est une panne ;
- **les états** — `lot_correlations --check`, `measure_lot --check` : ils
  refusent tant que le lot n'est pas prêt, et c'est leur travail. Leur refus
  est rapporté comme un ÉTAT, avec sa première raison, jamais comme une panne ;
- **le réseau** — `vectordb/embed.py --dry-run` a besoin de la base : lancé
  seulement avec `--base`, et son échec dit « réseau ».

**Lecture seule par défaut.** Les portes 03, 04 et 06 écrivent des lignes de
calibration au registre (`L25`) : elles ne tournent qu'avec `--calibrations`.
Le script vérifie à la fin que, sans cette option, le registre n'a pas bougé.

    python scripts/verifier_tout.py                  # lecture seule
    python scripts/verifier_tout.py --calibrations   # + portes 03, 04, 06
    python scripts/verifier_tout.py --base           # + la base de recherche
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRE = REPO / "registry" / "tests.jsonl"

# (nom, commande, famille). L'ordre est celui des phases.
GARDES = [
    ("porte 01 — point-in-time", "scripts/gate_01_pit.py"),
    ("porte 02 — panel", "scripts/gate_02_panel.py"),
    ("porte 05 — API de signal", "scripts/gate_05_signal_api.py"),
    ("porte 07 — fiches", "scripts/gate_07.py"),
    ("porte 08 — codeur", "scripts/gate_08.py"),
    ("porte 09 — calcul BH", "scripts/gate_09.py --check"),
    ("catalogue", "catalogue/validate.py"),
    ("provenance des valeurs", "scripts/check_provenance.py"),
    ("contrôles des signaux", "scripts/check_signals.py"),
    ("juge du codeur (D23)", "scripts/score_signal.py --check"),
    ("validateur de recette (D34)", "scripts/recette.py --self-check"),
    ("juge du triage", "corpus/score_triage.py --check"),
    ("tri en masse", "corpus/tri_en_masse.py --self-check"),
    ("juge de l'extraction", "corpus/score_extraction.py --check"),
    ("garde des fiches", "corpus/check_fiches_guard.py"),
    ("schéma des fiches", "corpus/validate_fiches.py"),
    ("acquisition", "corpus/check_acquisition.py"),
    ("moissonneur", "corpus/check_harvest.py"),
    ("texte des papiers", "corpus/extract_text.py --check"),
    ("wiki", "wiki/update_hot.py --lint"),
]
CALIBRATIONS = [
    ("porte 03 — harnais", "scripts/gate_03_harness.py"),
    ("porte 04 — registre", "scripts/gate_04_registry.py"),
    ("porte 06 — contrôles", "scripts/gate_06_controls.py"),
]
ETATS = [
    ("lot : matrice de corrélation", "scripts/lot_correlations.py --check"),
    ("lot : mesure", "scripts/measure_lot.py --check"),
    ("lot : hypothèses", "scripts/hypotheses_lot.py --status"),
    ("double codage", "scripts/double_codage.py --status"),
]
RESEAU = [("base de recherche", "vectordb/embed.py --dry-run")]


def lignes_registre() -> int:
    return len(REGISTRE.read_text(encoding="utf-8").splitlines())


def lancer(cmd: str) -> tuple[int, str, float]:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    t0 = time.time()
    r = subprocess.run([sys.executable, *cmd.split()], cwd=REPO, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env)
    sortie = [x for x in (r.stdout + r.stderr).splitlines()
              if x.strip() and "warning" not in x.lower()]
    return r.returncode, "\n".join(sortie), time.time() - t0


def resume(sortie: str, rc: int) -> str:
    """La ligne qui dit le verdict, ou la première raison d'un refus."""
    import re  # noqa: PLC0415

    lignes = sortie.splitlines()
    for motif in (r"PORTE \d\d", r"GATE \d\d", r"VALIDE", r"PASSÉS", r"conforme",
                  r"vérifications", r"verifications", r"RECETTE", r"VALIDATEUR", r"TRI EN MASSE"):
        for x in reversed(lignes):
            if re.search(motif, x):
                return x.strip()
    if rc:
        for x in lignes:
            if x.strip().startswith("- "):
                return x.strip()
    return (lignes[-1].strip() if lignes else "(rien)")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Toutes les vérifications du projet")
    ap.add_argument("--calibrations", action="store_true",
                    help="ajoute les portes 03, 04, 06, qui écrivent des calibrations")
    ap.add_argument("--base", action="store_true", help="ajoute la base de recherche")
    a = ap.parse_args(argv)

    plan = [(n, c, "garde") for n, c in GARDES]
    if a.calibrations:
        plan += [(n, c, "garde") for n, c in CALIBRATIONS]
    plan += [(n, c, "état") for n, c in ETATS]
    if a.base:
        plan += [(n, c, "réseau") for n, c in RESEAU]

    avant = lignes_registre()
    pannes = 0
    print(f"{'':2}{'vérification':<32}{'durée':>7}  verdict")
    for nom, cmd, famille in plan:
        rc, sortie, duree = lancer(cmd)
        if famille == "garde":
            marque = "ok" if rc == 0 else "XX"
            pannes += rc != 0
        elif famille == "état":
            marque = "··"
        else:
            marque = "ok" if rc == 0 else "~~"
        print(f"{marque:2} {nom:<31}{duree:>6.0f}s  {resume(sortie, rc)[:110]}", flush=True)

    apres = lignes_registre()
    print(f"\nregistre : {avant} -> {apres} lignes")
    if not a.calibrations and apres != avant:
        print("PANNE : une vérification en lecture seule a écrit au registre")
        pannes += 1
    print("ok = passe · XX = PANNE · ·· = état (refuse tant que ce n'est pas prêt) · "
          "~~ = réseau")
    print("TOUT PASSE" if not pannes else f"{pannes} PANNE(S)")
    return 1 if pannes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
