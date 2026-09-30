"""Le quota de chaque Claude, et ce qu'il reste à faire avec, en papiers.

Plusieurs Claude peuvent travailler en même temps. Les sessions d'un même compte
partagent un quota ; deux comptes ont chacun le leur. Chaque Claude inscrit donc
**son** relevé, sous son nom, dans `scripts/out/quota/<nom>.json` ; le tableau de
bord en fait une ligne par Claude.

**La conversion en papiers se MESURE, elle ne se suppose pas.** Le rapport entre
tokens et pourcentage de quota n'est publié nulle part. Chaque relevé peut dire
combien de tokens ont été dépensés depuis le précédent (`--depense`, la somme des
`subagent_tokens` que rapportent les sessions lancées, plus l'orchestrateur) : la
hausse du pourcentage divisée par ces tokens donne le coût d'un million de
tokens, et donc combien de fiches, de recettes ou de papiers triés tiennent dans
ce qui reste. Sans mesure, le tableau dit « à calibrer » — jamais un chiffre
inventé.

    python scripts/quota.py --nom principal --fenetre 30 --semaine 68 \\
        --reset-fenetre 2026-09-30T17:20 --reset-semaine 2026-10-02T08:00
    python scripts/quota.py --nom principal --fenetre 41 --semaine 71 ... --depense 330000
    python scripts/quota.py --status
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOSSIER = REPO / "scripts" / "out" / "quota"

# Coût mesuré de chaque activité, en tokens (journal de D34, 2026-09-30).
# Une mesure de plus les corrige dans ce dictionnaire, jamais ailleurs.
COUTS = {
    "fiche codée (recette + deux codeurs)": 330_000,
    "fiche extraite": 170_000,
    "papier trié": 1_400,
}


def lire(nom: str) -> dict:
    p = DOSSIER / f"{nom}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"name": nom,
                                                                          "releves": []}


def calibrer(releves: list[dict]) -> dict | None:
    """% de quota par million de tokens, sur la semaine et sur la fenêtre de 5 h.

    Seuls comptent les couples de relevés consécutifs avec une dépense déclarée
    et sans remise à zéro entre les deux (le pourcentage n'a pas baissé).
    """
    pts = {"semaine": [0.0, 0], "fenetre": [0.0, 0]}
    for a, b in zip(releves, releves[1:], strict=False):
        dep = b.get("depense") or 0
        if dep <= 0:
            continue
        for cle in pts:
            d = b[cle] - a[cle]
            if d >= 0 and b.get(f"reset_{cle}") == a.get(f"reset_{cle}"):
                pts[cle][0] += d
                pts[cle][1] += dep
    out = {f"{k}_pct_par_million": (v[0] / v[1] * 1e6) for k, v in pts.items() if v[1]}
    return out or None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le quota de chaque Claude")
    ap.add_argument("--nom", help="le nom de ce Claude (un par compte)")
    ap.add_argument("--fenetre", type=float, help="%% utilisés de la fenêtre de 5 heures")
    ap.add_argument("--semaine", type=float, help="%% utilisés de la semaine")
    ap.add_argument("--reset-fenetre")
    ap.add_argument("--reset-semaine")
    ap.add_argument("--depense", type=int, default=0,
                    help="tokens dépensés depuis le relevé précédent de ce Claude")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)

    if a.status or not a.nom:
        for p in sorted(DOSSIER.glob("*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            r = d["releves"][-1] if d["releves"] else {}
            print(f"{d['name']:<14} fenêtre {r.get('fenetre')} % · semaine {r.get('semaine')} % · "
                  f"relevé {r.get('at')} · calibration {d.get('calibration') or 'à faire'}")
        return 0
    if a.fenetre is None or a.semaine is None:
        raise SystemExit("--fenetre et --semaine sont exigés")
    d = lire(a.nom)
    d["releves"].append({"at": datetime.now(UTC).isoformat(timespec="minutes"),
                         "fenetre": a.fenetre, "semaine": a.semaine,
                         "reset_fenetre": a.reset_fenetre, "reset_semaine": a.reset_semaine,
                         "depense": a.depense})
    d["calibration"] = calibrer(d["releves"])
    d["couts"] = COUTS
    DOSSIER.mkdir(parents=True, exist_ok=True)
    (DOSSIER / f"{a.nom}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8")
    print(f"relevé inscrit pour {a.nom} ; calibration : {d['calibration'] or 'à faire'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
