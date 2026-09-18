"""La prémisse de la clause 2 : la friction de Mesfin (2026), dans NOS unités.

`ETAT.md` § Prochaine action proposait un raccourci : montrer que notre plancher
de coût mesuré est « un ordre de grandeur sous les 8 à 15 bp » que vaut la
friction supposée de Mesfin sur nos données. Ce script fait le calcul au lieu de
le citer.

Il ne calcule **aucun IC** et ne dépense **aucun test** : il convertit une
hypothèse de coût exprimée en points d'indice en points de base, au niveau de
prix que nos propres données mesurent, et la compare aux planchers du catalogue.

Fenêtre. Mesfin mesure sur 2021-2025. La tranche `holdout` commence au
2024-01-01 et reste scellée (invariant V), donc la comparaison porte sur
**2021-01-01 → 2023-12-31** — trois des quatre années et demie du papier. C'est
dit, ce n'est pas caché, et ça ne change pas un ordre de grandeur.

    python scripts/check_mesfin_premise.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402

from panel import Panel  # noqa: E402
from panel.sessions import window_labels  # noqa: E402

ASOF = "2023-12-29 20:00"
START = "2021-01-01"

# Ce que le papier suppose, tel que `wiki/research/mesfin-2026-falsification`
# le rapporte de `corpus/AMORCE.md` entrée 7.
FRICTION_POINTS = 2.0
GROSS_POINTS = (0.07, 1.50)


def main() -> int:
    panel = Panel.open(asof=ASOF, slice="pool")
    close = panel.adjusted("NQ", columns=["close"])["close"]
    close = close[close.index >= f"{START} 00:00:00+00:00"]
    if close.empty:
        print("aucune barre NQ sur la fenêtre")
        return 1

    labels = window_labels(close.index, panel.catalogue)
    levels = close.to_numpy(dtype=float)

    low, high = float(np.quantile(levels, 0.01)), float(np.quantile(levels, 0.99))
    median = float(np.median(levels))

    print(f"NQ, tranche pool, {START} → 2023-12-31 — {len(levels):,} barres"
          .replace(",", " "))
    print(f"  niveau : centile 1 {low:,.0f} · médiane {median:,.0f} · "
          f"centile 99 {high:,.0f}".replace(",", " "))
    print()

    def to_bp(points: float, level: float) -> float:
        return points / level * 1e4

    print(f"La friction supposée par Mesfin — {FRICTION_POINTS:.0f} points d'indice "
          f"d'aller-retour — vaut, à ces niveaux :")
    for name, level in (("au plus haut (c99)", high), ("à la médiane", median),
                        ("au plus bas (c1)", low)):
        print(f"  {name:20s} {level:>8,.0f} → {to_bp(FRICTION_POINTS, level):.2f} bp"
              .replace(",", " "))
    print()

    print("Le rendement brut par trade qu'il rapporte, dans les mêmes unités :")
    for points in GROSS_POINTS:
        print(f"  {points:.2f} point → {to_bp(points, median):.2f} bp à la médiane")
    print()

    floors = {}
    windows = {w for w in labels.unique() if isinstance(w, str) and w}
    for window in sorted(windows):
        cell = panel.catalogue.instrument("NQ").cells.get(window)
        if cell is not None:
            floors[window] = float(cell.spread_floor_bp)
    worst = max(
        float(c.spread_floor_bp)
        for inst in panel.catalogue.instruments.values()
        for c in inst.cells.values()
        if c.retained
    )

    print("Notre plancher mesuré (écart seul — frais et glissement encore null) :")
    for window, floor in floors.items():
        print(f"  NQ × {window:7s} {floor:.2f} bp")
    print(f"  pire cellule de la grille   {worst:.2f} bp")
    print()

    friction_bp = to_bp(FRICTION_POINTS, median)
    ratio_us = friction_bp / floors["US"]
    ratio_worst = friction_bp / worst

    print("=" * 70)
    print("LE VERDICT SUR LA PRÉMISSE")
    print(f"  friction de Mesfin, à la médiane NQ : {friction_bp:.2f} bp")
    print(f"  notre plancher NQ × US              : {floors['US']:.2f} bp  "
          f"→ elle vaut {ratio_us:.1f}× le nôtre")
    print(f"  notre pire cellule                  : {worst:.2f} bp  "
          f"→ elle vaut {ratio_worst:.1f}× le nôtre")
    print()
    if ratio_us < 3:
        print("  La prémisse écrite dans ETAT.md NE TIENT PAS. Elle annonçait une")
        print("  friction de 8 à 15 bp, « un ordre de grandeur » au-dessus de notre")
        print("  plancher. Le calcul donne le MÊME ORDRE DE GRANDEUR.")
        print()
        print("  Et la comparaison est même flatteuse pour nous : notre plancher est")
        print("  un ÉCART SEUL, frais et glissement encore `null`, tandis que les")
        print("  2 points de Mesfin sont une friction TOUT COMPRIS. Une fois nos")
        print("  frais connus, l'écart restant se refermera encore.")
        print()
        print("  Conséquence : son verdict ne peut pas être écarté au motif d'une")
        print("  hypothèse de coût déraisonnable. Il est transportable.")
    else:
        print("  La prémisse tient : sa friction est bien d'un autre ordre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
