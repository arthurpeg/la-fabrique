"""D26 — l'encadrement des frais par contrat, rendu en points de base.

Les montants ci-dessous sont RECOPIÉS de trois tiers, le 2026-09-24, et chacun
porte sa source dans `decisions/DECISION-26-encadrement-des-frais.md`. Ce script
ne les dépose pas au catalogue (D26 § Ce que ça verrouille dit pourquoi) : il les
rapporte au prix médian de la tranche `pool` pour dire ce que pèse chaque borne,
en plein format et en micro, à côté du plancher d'écart mesuré.

    borne basse = barème Lucid seul                     (compte simulé : tout compris)
    borne haute = barème Lucid + frais CME non-membre + NFA   (rien n'est compris)

Aucun IC n'est calculé ; seule la tranche `pool` est lue, par le Panel.

    python scripts/fee_bracket.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from panel.catalogue import load_catalogue  # noqa: E402
from panel.panel import Panel  # noqa: E402

# USD par contrat et PAR SIDE. Lucid : support.lucidtrading.com, article 11508978.
# CME : Non-Member Fee Finder, « Estimated fee per side », Globex, barème antérieur
# au 2026-10-01 (SER-9799R). NFA : Bylaw 1301 (b)(i)(A), $.04 le round-turn après
# le 2027-06-30, soit 0,02 par side -- le taux le plus haut en vigueur sur
# l'horizon, retenu parce que la borne haute est pessimiste.
NFA_PER_SIDE = 0.02

# racine évaluée -> (micro, lucid plein, cme plein, lucid micro, cme micro, rapport de taille)
# Le rapport de taille est celui des unités de contrat CME (fiches contrat) : un
# micro vaut 1/10 du plein pour les indices, l'or et le pétrole. Les devises n'ont
# pas de micro au barème Lucid : None.
FEES = {
    "NQ": ("MNQ", 1.75, 1.38, 0.50, 0.35, 10),
    "ES": ("MES", 1.75, 1.38, 0.50, 0.35, 10),
    "YM": ("MYM", 1.75, 1.38, 0.50, 0.35, 10),
    "GC": ("MGC", 2.30, 1.65, 0.80, 0.70, 10),
    "CL": ("MCL", 2.00, 1.50, 0.50, 0.50, 10),
    "6E": (None, 2.40, 1.60, None, None, None),
    "6B": (None, 2.40, 1.60, None, None, None),
    "6J": (None, 2.40, 1.60, None, None, None),
    "6A": (None, 2.40, 1.60, None, None, None),
}

POOL_LAST_BAR = "2023-12-29 20:59:00+00:00"


def round_trip_bp(per_side_usd: float, multiplier: float, price: float) -> float:
    """D01 §7 : F / (P x M) x 10 000, deux sides pour un aller-retour."""
    return 2.0 * per_side_usd / (multiplier * price) * 1e4


def main() -> int:
    catalogue = load_catalogue()
    panel = Panel.open(POOL_LAST_BAR, slice="pool", catalogue=catalogue)

    rows = []
    for root, (micro, lucid, cme, lucid_m, cme_m, ratio) in FEES.items():
        instrument = catalogue.instrument(root)
        multiplier = instrument.multiplier
        if multiplier is None:
            print(f"{root} : multiplicateur null -- rien à rapporter")
            return 1
        close = panel.close(root)
        price = float(close.median())
        price_last = float(close[close.index >= pd.Timestamp("2023-01-01", tz="UTC")].median())
        floor = min(float(cell.spread_floor_bp) for cell in instrument.cells.values())

        low, high = lucid, lucid + cme + NFA_PER_SIDE
        row = {
            "root": root,
            "median_price": price,
            "floor_bp": floor,
            "low_usd": low,
            "high_usd": high,
            "low_bp": round_trip_bp(low, multiplier, price),
            "high_bp": round_trip_bp(high, multiplier, price),
            "high_bp_2023": round_trip_bp(high, multiplier, price_last),
        }
        if micro:
            m_mult = multiplier / ratio
            m_low, m_high = lucid_m, lucid_m + cme_m + NFA_PER_SIDE
            row |= {
                "micro": micro,
                "micro_low_bp": round_trip_bp(m_low, m_mult, price),
                "micro_high_bp": round_trip_bp(m_high, m_mult, price),
            }
        rows.append(row)

    print("Aller-retour, en bp du notionnel au prix médian de la tranche pool.")
    print("Plancher = écart d'un tick, mesuré (catalogue, meilleure cellule).\n")
    header = (
        f"{'':4s} {'prix méd.':>10s} {'plancher':>8s} | {'basse $':>7s} {'haute $':>7s} "
        f"| {'basse bp':>8s} {'haute bp':>8s} {'h. 2023':>8s} | {'micro':5s} "
        f"{'basse bp':>8s} {'haute bp':>8s}"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        micro = (
            f"{r['micro']:5s} {r['micro_low_bp']:8.2f} {r['micro_high_bp']:8.2f}"
            if "micro" in r
            else f"{'--':5s} {'--':>8s} {'--':>8s}"
        )
        print(
            f"{r['root']:4s} {r['median_price']:10.5g} {r['floor_bp']:8.2f} | "
            f"{r['low_usd']:7.2f} {r['high_usd']:7.2f} | {r['low_bp']:8.2f} "
            f"{r['high_bp']:8.2f} {r['high_bp_2023']:8.2f} | {micro}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
