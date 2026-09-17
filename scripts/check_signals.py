"""Contrôles sur les deux signaux de référence — et pas une corrélation.

Ce script vérifie que les étalons de `D06` sont *utilisables* : qu'ils produisent
des scores, en quantité suffisante, variés, et qu'ils ne regardent pas devant eux.
Il ne mesure **aucun IC**, et c'est délibéré (`D06` § Pourquoi) : implémenter et
mesurer sont deux gestes, seul le premier a lieu tant que les contrôles
automatiques de la phase 06 n'existent pas.

La comparaison entre les deux signaux se fait par **accord de signe**, pas par
corrélation : une matrice de corrélation entre signaux, c'est la taxonomie, et
elle se construit en phase 11 avec un stock de signaux, pas avec deux.

    python scripts/check_signals.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from panel import Panel  # noqa: E402
from signals import REFERENCE  # noqa: E402

ASOF = "2018-06-15 20:00"
EARLIER = "2017-06-15 20:00"
HORIZON_BARS = 30
MIN_OBSERVATIONS = 30  # le seuil sous lequel le harnais refuse de mesurer une cellule


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    panel = Panel.open(asof=ASOF, slice="pool")
    print(f"panel ouvert au {panel.asof}, tranche {panel.slice.name}, "
          f"{len(panel.cells())} cellules\n")

    produced: dict[str, dict[tuple[str, str], pd.Series]] = {}

    for signal_id, module in REFERENCE.items():
        print(f"--- {signal_id}  ({module.HYPOTHESIS}, signe attendu "
              f"{'+' if module.EXPECTED_SIGN > 0 else '-'}) ---")
        scores = module.scores(panel, horizon_bars=HORIZON_BARS)
        produced[signal_id] = scores

        check(len(scores) == len(panel.cells()),
              f"{signal_id} : {len(scores)} cellules scorées sur {len(panel.cells())}")

        total = 0
        thin = []
        flat = []
        for (root, window), series in sorted(scores.items()):
            values = series.to_numpy(dtype=float)
            total += len(values)
            check(np.isfinite(values).all(), f"{signal_id} {root}x{window} : score non fini")
            if len(values) < MIN_OBSERVATIONS:
                thin.append(f"{root}x{window} ({len(values)})")
            if len(np.unique(values)) < 2:
                flat.append(f"{root}x{window}")
            # aucun score après l'as-of du panel : la garantie du Panel, revérifiée ici
            check(series.index.max() <= panel.asof,
                  f"{signal_id} {root}x{window} : un score est daté après l'as-of")

        check(not thin, f"{signal_id} : cellules sous {MIN_OBSERVATIONS} observations — {thin}")
        check(not flat, f"{signal_id} : cellules à score constant — {flat}")

        spread = np.concatenate([s.to_numpy(dtype=float) for s in scores.values()])
        print(f"   {len(scores)} cellules, {total} scores, "
              f"médiane des observations par cellule "
              f"{int(np.median([len(s) for s in scores.values()]))}")
        print(f"   dispersion : écart-type {spread.std():.5f}, "
              f"min {spread.min():+.4f}, max {spread.max():+.4f}, "
              f"part de zéros exacts {np.mean(spread == 0):.2%}")

    # -- la causalité, en avance sur la porte 05 -----------------------------
    print("\n--- causalité : un panel qui en sait moins rend les mêmes scores ---")
    earlier = panel.truncate(end=EARLIER)
    for signal_id, module in REFERENCE.items():
        before = module.scores(earlier, horizon_bars=HORIZON_BARS)
        full = produced[signal_id]
        compared = 0
        for cell, series in before.items():
            check(cell in full, f"{signal_id} {cell} : la cellule disparaît du panel complet")
            if cell not in full:
                continue
            shared = series.index.intersection(full[cell].index)
            check(len(shared) == len(series),
                  f"{signal_id} {cell} : {len(series) - len(shared)} scores du panel tronqué "
                  "sont absents du panel complet")
            same = np.allclose(series.reindex(shared), full[cell].reindex(shared), equal_nan=True)
            check(same, f"{signal_id} {cell} : les scores changent quand le panel en sait plus")
            compared += len(shared)
        print(f"   {signal_id} : {compared} scores identiques des deux côtés")

    # -- les deux étalons ne sont pas le même ------------------------------
    print("\n--- les deux étalons diffèrent (accord de signe, pas corrélation) ---")
    gao, baltussen = produced.values()
    agree = disagree = 0
    for cell in sorted(set(gao) & set(baltussen)):
        shared = gao[cell].index.intersection(baltussen[cell].index)
        left = np.sign(gao[cell].reindex(shared).to_numpy(dtype=float))
        right = np.sign(baltussen[cell].reindex(shared).to_numpy(dtype=float))
        agree += int((left == right).sum())
        disagree += int((left != right).sum())
    share = agree / max(agree + disagree, 1)
    check(0.5 < share < 0.95,
          f"accord de signe à {share:.1%} : hors de [50 %, 95 %], les deux étalons sont "
          "soit indépendants soit le même signal")
    print(f"   {agree + disagree} paires, accord de signe {share:.1%} — corrélés, pas identiques")

    print(f"\n{checks} vérifications")
    if failures:
        print("CONTRÔLES : ÉCHOUÉS")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("CONTRÔLES : PASSÉS — les deux étalons sont utilisables, aucun IC calculé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
