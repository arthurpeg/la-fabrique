"""La matrice de corrélation du lot — étape 9 de la phase 09.

`D25` exige de mesurer la dépendance **réelle** entre les signaux du lot
**avant** d'appliquer Benjamini–Hochberg : la procédure n'est valide que sous
dépendance positive (ou nulle). Si des paires sont franchement négatives, ou
la structure erratique, `D25` prévoit de passer à Benjamini–Yekutieli, plus
sévère — et cette décision se prend sur ce fichier, pas après avoir vu les IC.

**AUCUN IC N'EST CALCULÉ ICI.** On corrèle les **scores** des signaux entre eux,
jamais un score avec un rendement futur — c'est la mesure de
`scripts/calibrate_coder.py` à la porte 08, étendue au lot. Rien n'est écrit au
registre, et rien ne fait sortir un signal du lot (`D28` ne vise que le registre).

**Comment.** Chaque signal est calculé sur le `pool` entier, au même instant que
sa mesure future (`D29`). Pour chaque paire, on apparie les scores par
(cellule, instant) communs et on prend la corrélation **de rang** (Spearman),
comme le harnais pour l'IC. Une paire sans assez d'instants communs est
inscrite avec `correlation: null` : on ne devine pas.

Le format est celui qu'attend `scripts/gate_09.py` :
`scripts/out/lot_09_correlations.json`.

    python scripts/lot_correlations.py --check   # le lot est-il prêt ? sans calcul
    python scripts/lot_correlations.py           # calcule et écrit la matrice
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import pandas as pd  # noqa: E402
from codage_verifie import cellules_de  # noqa: E402
from gate_09 import (  # noqa: E402
    ASOF_REQUIRED,
    CORR_FILE,
    LOT_FILE,
    SLICE_REQUIRED,
    importer_par_signal_id,
)

MIN_PAIRES = 30  # sous ce nombre d'instants communs, une corrélation ne dit rien


def entrees() -> list[dict]:
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    return lot.get("fiches") or lot.get("hypotheses") or []


def verifier() -> list[str]:
    fautes = []
    for e in entrees():
        if not e.get("signal_id"):
            fautes.append(f"{e.get('fiche_id')} : pas de signal_id — signal non codé ou "
                          "hypothèse non écrite (étapes 7 et 8)")
    return fautes


def serie_plate(scores: dict) -> pd.Series:
    """{(root, window): Series} -> une Series indexée par (root, window, instant)."""
    parts = []
    for (root, window), s in scores.items():
        s = s.dropna()
        if len(s):
            s.index = pd.MultiIndex.from_arrays(
                [[root] * len(s), [window] * len(s), s.index])
            parts.append(s)
    return pd.concat(parts) if parts else pd.Series(dtype=float)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Matrice de corrélation du lot — D25")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    fautes = verifier()
    if fautes:
        print("LOT PAS PRÊT pour la matrice :")
        for f in fautes:
            print(f"  - {f}")
        return 1
    ids = sorted({e["signal_id"] for e in entrees()})
    univers = {e["signal_id"]: e.get("universe") for e in entrees()}
    print(f"lot prêt : {len(ids)} signaux")
    if a.check:
        print("--check : rien n'a été calculé.")
        return 0

    from panel import Panel

    panel = Panel.open(asof=ASOF_REQUIRED.replace("+00:00", ""), slice=SLICE_REQUIRED)
    plates: dict[str, pd.Series] = {}
    for i, sid in enumerate(ids, 1):
        module = importer_par_signal_id(sid)
        scores = module.scores(panel, horizon_bars=30)
        if univers.get(sid):  # D38 : les cellules que la mesure lira, pas les autres
            garder = cellules_de(univers[sid])
            scores = {c: s for c, s in scores.items() if c in garder}
        plates[sid] = serie_plate(scores)
        print(f"  scores {i}/{len(ids)} : {sid} ({len(plates[sid])} valeurs)", flush=True)

    pairs = []
    for a_id, b_id in itertools.combinations(ids, 2):
        joint = pd.concat([plates[a_id].rename("a"), plates[b_id].rename("b")],
                          axis=1, join="inner").dropna()
        n = int(len(joint))
        corr = (float(joint["a"].corr(joint["b"], method="spearman"))
                if n >= MIN_PAIRES else None)
        pairs.append({"a": a_id, "b": b_id, "correlation": corr, "n": n})

    out = {
        "measured_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "asof": ASOF_REQUIRED, "slice": SLICE_REQUIRED, "method": "spearman",
        "min_pairs": MIN_PAIRES, "signal_ids": ids, "pairs": pairs,
    }
    CORR_FILE.parent.mkdir(parents=True, exist_ok=True)
    CORR_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")

    vals = [p["correlation"] for p in pairs if p["correlation"] is not None]
    neg = [v for v in vals if v < -0.1]
    print(f"\n{len(pairs)} paires, {len(vals)} mesurables ; "
          f"{len(neg)} franchement négatives (< -0,1)")
    print("Si les paires négatives sont nombreuses ou fortes, D25 prévoit")
    print("Benjamini–Yekutieli au lieu de BH : à décider MAINTENANT, avant la mesure.")
    print(f"écrit : {CORR_FILE.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
