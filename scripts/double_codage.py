"""Le double codage — le point 5 de `D34`.

Deux codeurs isolés, de deux modèles différents (`MODELE_PRINCIPAL`,
`MODELE_TEMOIN`), ont codé la même fiche avec sa recette : le principal dans
`signals/`, le témoin dans `verification/temoins/`. Ce script compare leurs
**scores** sur le `pool`, à l'instant du juge `D23`, et rend un verdict :

- **CONCORDANT** : même signe attendu, corrélation de rang pondérée par cellule
  d'au moins `SEUIL_RHO`, et au moins `SEUIL_COUVERTURE` des (cellule, instant)
  notés par les deux. Deux lectures indépendantes retrouvent le même signal :
  l'erreur de codage n'est plus l'explication d'un IC mort.
- **DISCORDANT** : au moins un codeur s'est trompé, ou la recette laisse une
  ambiguïté. Les `CHOICES` des deux sont affichés côte à côte : c'est là que
  se lit le désaccord. La suite est dans `scripts/CODAGE-DES-SIGNAUX.md`.

**CE N'EST PAS UN IC.** Aucun rendement n'entre dans le calcul, rien n'est écrit
au registre, et le script casse si le registre a bougé. Le verdict s'inscrit
dans `verification/concordance.jsonl`, append-only : c'est lui que lisent
`hypotheses_lot.py`, `measure_lot.py` et la porte 09.

**Deux codeurs d'accord peuvent se tromper ensemble** — ils lisent la même
fiche. La concordance prouve que la LECTURE de la fiche est stable, pas que la
fiche est fidèle au papier ; ce maillon-là est tenu par `D16` et par la recette.

    python scripts/double_codage.py <fiche_id>          # juge et inscrit
    python scripts/double_codage.py --status            # le verdict de chaque fiche
    python scripts/double_codage.py --compare A.py B.py # calibration, rien d'inscrit
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from codage_verifie import (  # noqa: E402
    ASOF_CONCORDANCE,
    CONCORDANCE,
    MIN_PAIRES,
    MODELE_PRINCIPAL,
    MODELE_TEMOIN,
    SEUIL_COUVERTURE,
    SEUIL_RHO,
    TOURS_MAX,
    ajouter,
    choix,
    empreinte16,
    jugement_vert,
    lire,
    maintenant,
    rel,
    temoin_path,
)
from code_signal import fiche_files, module_path  # noqa: E402

from harness import registry  # noqa: E402

HORIZON_BARS = 30


def importer(path: Path):
    nom = ".".join(path.resolve().relative_to(REPO).with_suffix("").parts)
    return importlib.import_module(nom)


def comparer(sa: dict, sb: dict) -> dict:
    """Corrélation de rang par cellule, pondérée par le nombre de paires."""
    cellules, poids, rhos = [], [], []
    union = communs = 0
    for cle in sorted(set(sa) | set(sb)):
        a = sa.get(cle, pd.Series(dtype=float)).dropna()
        b = sb.get(cle, pd.Series(dtype=float)).dropna()
        a_, b_ = a.align(b, join="inner")
        ok = np.isfinite(a_.to_numpy(dtype=float)) & np.isfinite(b_.to_numpy(dtype=float))
        a_, b_ = a_[ok], b_[ok]
        union += len(a.index.union(b.index))
        communs += len(a_)
        if len(a_) < MIN_PAIRES:
            rho = None
        elif a_.nunique() < 2 or b_.nunique() < 2:
            rho = 1.0 if a_.nunique() == b_.nunique() == 1 else 0.0
        else:
            rho = float(a_.corr(b_, method="spearman"))
        cellules.append({"cell": list(cle), "n": int(len(a_)), "rho": rho})
        if rho is not None:
            poids.append(len(a_))
            rhos.append(rho)
    rho = float(np.average(rhos, weights=poids)) if poids else None
    return {"rho": rho, "coverage": communs / union if union else 0.0,
            "pairs": int(communs), "cells": cellules}


def verdict(res: dict, signe_a: int, signe_b: int) -> tuple[str, list[str]]:
    motifs = []
    if signe_a != signe_b:
        motifs.append(f"signes attendus opposés : {signe_a:+d} contre {signe_b:+d}")
    if res["rho"] is None:
        motifs.append("aucune cellule n'a assez de paires pour une corrélation")
    elif res["rho"] < SEUIL_RHO:
        motifs.append(f"corrélation {res['rho']:.3f} < {SEUIL_RHO}")
    if res["coverage"] < SEUIL_COUVERTURE:
        motifs.append(f"couverture {res['coverage']:.3f} < {SEUIL_COUVERTURE} : les deux "
                      "codeurs ne notent pas les mêmes instants")
    return ("CONCORDANT" if not motifs else "DISCORDANT"), motifs


def scores_de(module, panel) -> dict:
    return module.scores(panel, horizon_bars=HORIZON_BARS)


def afficher(res: dict, v: str, motifs: list[str]) -> None:
    print(f"{'cellule':<16}{'paires':>8}{'rho':>9}")
    for c in res["cells"]:
        r = "  trop peu" if c["rho"] is None else f"{c['rho']:>9.3f}"
        print(f"{str(tuple(c['cell'])):<16}{c['n']:>8}{r}")
    rho = "—" if res["rho"] is None else f"{res['rho']:.3f}"
    print(f"\nrho pondéré {rho}  ·  couverture {res['coverage']:.3f}  ·  {res['pairs']} paires")
    print(f"VERDICT : {v}")
    for m in motifs:
        print(f"  - {m}")


def garder_le_registre():
    avant = (len(registry.read_all()), registry.counted_tests())

    def verifier() -> None:
        apres = (len(registry.read_all()), registry.counted_tests())
        if apres != avant:
            raise SystemExit(f"LE DOUBLE CODAGE A TOUCHÉ AU REGISTRE : {avant} -> {apres}. "
                             "Il ne doit rien écrire : ce n'est pas un IC.")
        print(f"registre inchangé : {avant[0]} lignes, {avant[1]} test(s) compté(s)")
    return verifier


def do_fiche(fiche_id: str) -> int:
    if fiche_id not in fiche_files():
        raise SystemExit(f"fiche inconnue : {fiche_id}")
    principal = module_path(fiche_id)
    temoin = temoin_path(principal)
    fautes = []
    for p in (principal, temoin):
        ok, pourquoi = jugement_vert(p)
        if not ok:
            fautes.append(pourquoi)
    tours = [c for c in lire(CONCORDANCE) if c["fiche_id"] == fiche_id]
    if len(tours) >= TOURS_MAX and tours[-1]["verdict"] != "CONCORDANT":
        fautes.append(f"{len(tours)} tours déjà faits, tous discordants : TOURS_MAX = "
                      f"{TOURS_MAX}. La fiche s'écarte (scripts/ecarter_du_lot.py), "
                      "elle ne se recode pas indéfiniment")
    if fautes:
        print("DOUBLE CODAGE REFUSÉ :")
        for f in fautes:
            print(f"  - {f}")
        return 1

    from panel import Panel

    verifier = garder_le_registre()
    ma, mb = importer(principal), importer(temoin)
    if ma.SIGNAL_ID != mb.SIGNAL_ID:
        raise SystemExit(f"SIGNAL_ID différents : {ma.SIGNAL_ID} contre {mb.SIGNAL_ID}")
    panel = Panel.open(ASOF_CONCORDANCE, slice="pool")
    res = comparer(scores_de(ma, panel), scores_de(mb, panel))
    v, motifs = verdict(res, ma.EXPECTED_SIGN, mb.EXPECTED_SIGN)
    afficher(res, v, motifs)

    ca = choix(principal.read_text(encoding="utf-8"))
    cb = choix(temoin.read_text(encoding="utf-8"))
    if v == "DISCORDANT":
        print(f"\nCHOICES du principal ({MODELE_PRINCIPAL}) :")
        for c in ca:
            print(f"  - {c}")
        print(f"CHOICES du témoin ({MODELE_TEMOIN}) :")
        for c in cb:
            print(f"  - {c}")
        print("\nLe désaccord se lit là. Voir CODAGE-DES-SIGNAUX.md § 2.7.")
    ajouter(CONCORDANCE, {
        "at": maintenant(), "fiche_id": fiche_id, "round": len(tours) + 1,
        "asof": ASOF_CONCORDANCE, "slice": "pool", "method": "spearman, pondéré par cellule",
        "thresholds": {"rho": SEUIL_RHO, "coverage": SEUIL_COUVERTURE},
        "principal": {"path": rel(principal), "sha256_16": empreinte16(principal),
                      "model": MODELE_PRINCIPAL, "expected_sign": ma.EXPECTED_SIGN,
                      "choices": ca},
        "temoin": {"path": rel(temoin), "sha256_16": empreinte16(temoin),
                   "model": MODELE_TEMOIN, "expected_sign": mb.EXPECTED_SIGN,
                   "choices": cb},
        "rho": res["rho"], "coverage": res["coverage"], "pairs": res["pairs"],
        "cells": res["cells"], "verdict": v, "reasons": motifs,
    })
    print(f"inscrit : {CONCORDANCE.relative_to(REPO).as_posix()} (tour {len(tours) + 1})")
    verifier()
    print("CE N'EST PAS UN IC — aucun rendement n'entre dans ce calcul.")
    return 0 if v == "CONCORDANT" else 1


def do_compare(a: str, b: str) -> int:
    """Calibration : deux modules quelconques, rien d'inscrit (comme calibrate_coder)."""
    from panel import Panel

    verifier = garder_le_registre()
    ma, mb = importer(Path(a)), importer(Path(b))
    panel = Panel.open(ASOF_CONCORDANCE, slice="pool")
    res = comparer(scores_de(ma, panel), scores_de(mb, panel))
    v, motifs = verdict(res, ma.EXPECTED_SIGN, mb.EXPECTED_SIGN)
    afficher(res, v, motifs)
    print("--compare : rien n'a été inscrit ; ce verdict n'ouvre aucun lot.")
    verifier()
    return 0


def do_status() -> int:
    derniers: dict[str, dict] = {}
    for c in lire(CONCORDANCE):
        derniers[c["fiche_id"]] = c
    if not derniers:
        print("aucun double codage inscrit")
    for fid, c in sorted(derniers.items()):
        rho = "—" if c["rho"] is None else f"{c['rho']:.3f}"
        print(f"  {c['verdict']:<11} tour {c['round']}  rho {rho}  couv {c['coverage']:.2f}  {fid}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le double codage — D34")
    ap.add_argument("fiche_id", nargs="?")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--compare", nargs=2, metavar=("A.py", "B.py"))
    a = ap.parse_args(argv)
    if a.status:
        return do_status()
    if a.compare:
        return do_compare(*a.compare)
    if a.fiche_id:
        return do_fiche(a.fiche_id)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
