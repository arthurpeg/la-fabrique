"""Écarter une fiche du lot avant sa mesure — `D34` § Quand le codage échoue.

Une fiche dont le codage ne se vérifie pas — double codage discordant après
`TOURS_MAX` tours, juge `D23` refusé trois fois, ou recette impossible — ne peut
pas être mesurée : un IC mort n'y distinguerait pas l'idée du codeur. Elle sort
du lot, **avant toute mesure**, et la sortie est écrite dans le lot même :

- l'entrée passe de `fiches` à `ecartees_codage`, avec son motif, sa preuve et
  sa date ;
- `n` diminue d'autant, pour que la porte 09 retrouve son compte (`L21`).

**Refusé dès que la mesure du lot a commencé.** Écarter après avoir vu un IC,
c'est choisir le lot sur son résultat (`D28`). La porte 09 le revérifie par les
dates (`codage_verifie.fautes_d34_du_lot`).

    python scripts/ecarter_du_lot.py <fiche_id> --preuve concordance --motif "…"
    python scripts/ecarter_du_lot.py <fiche_id> --preuve juge --motif "…"
    python scripts/ecarter_du_lot.py <fiche_id> --preuve recette --motif "…"
    python scripts/ecarter_du_lot.py <fiche_id> --preuve univers --motif "…"   # D38
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from codage_verifie import (  # noqa: E402
    CONCORDANCE,
    RECETTES,
    TOURS_MAX,
    lire,
    maintenant,
    univers_de,
)
from gate_09 import LOT_FILE, STAGE  # noqa: E402

from harness import registry  # noqa: E402

PREUVES = ("concordance", "juge", "recette", "univers")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Écarter une fiche du lot — D34")
    ap.add_argument("fiche_id")
    ap.add_argument("--preuve", choices=PREUVES, required=True)
    ap.add_argument("--motif", required=True)
    a = ap.parse_args(argv)

    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    entries = lot["fiches"]
    cible = next((e for e in entries if e["fiche_id"] == a.fiche_id), None)
    if cible is None:
        raise SystemExit(f"{a.fiche_id} n'est pas dans le lot")
    if cible.get("ref"):
        raise SystemExit(f"{a.fiche_id} a déjà son hypothèse {cible['ref']} : elle a passé "
                         "le double codage, elle ne s'écarte plus")
    ids = {e.get("signal_id") for e in entries} | {e["fiche_id"] for e in entries}
    mesures = [r for r in registry.read_all()
               if r.get("stage") == STAGE and r.get("signal_id") in ids]
    if mesures:
        raise SystemExit(f"la mesure du lot a commencé ({len(mesures)} ligne(s) au stage "
                         f"{STAGE}) : plus aucune fiche ne s'écarte (D28, D34)")
    if a.preuve == "concordance":
        tours = [c for c in lire(CONCORDANCE) if c["fiche_id"] == a.fiche_id]
        if len(tours) < TOURS_MAX or any(c["verdict"] == "CONCORDANT" for c in tours[-1:]):
            raise SystemExit(f"preuve insuffisante : {len(tours)} tour(s) inscrit(s), il en "
                             f"faut {TOURS_MAX} discordants")
    if a.preuve == "univers":
        # D38 : le marché du papier n'est aucun de nos instruments, et c'est la
        # recette — citée, validée — qui le dit, pas l'orchestrateur.
        rp = RECETTES / f"{a.fiche_id}.json"
        u = univers_de(json.loads(rp.read_text(encoding="utf-8")) if rp.is_file() else {})
        if u is None:
            raise SystemExit("preuve insuffisante : la recette ne déclare pas de marché (D38)")
        if u["exact"]:
            raise SystemExit(f"preuve contraire : la recette désigne {u['exact']} comme le "
                             "marché du papier — la fiche ne s'écarte pas pour son univers")
    if not a.motif.strip():
        raise SystemExit("--motif vide")

    lot["fiches"] = [e for e in entries if e is not cible]
    lot.setdefault("ecartees_codage", []).append(
        {**cible, "preuve": a.preuve, "motif_ecart": a.motif, "at": maintenant()})
    lot["n"] = len(lot["fiches"])
    LOT_FILE.write_text(json.dumps(lot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{a.fiche_id} écartée ({a.preuve}) — le lot passe à n = {lot['n']}")
    print("Commiter aussitôt : la date du commit prouve que l'écart précède la mesure.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
