"""Ce que le trieur voit, fabriqué déterministiquement depuis `corpus/AMORCE.md`.

`D15` fixe l'entrée du trieur : **la ligne d'`AMORCE.md` privée de sa colonne
verdict** — référence, ce qu'il prédit, fréquence et univers, données exigées,
accès. Ni plus, ni moins. Ce script la fabrique, et il vérifie qu'elle ne fuite
pas la réponse.

**Les titres de section ne sont pas repris, et c'est délibéré.** Le titre E dit
« Carry et structure de terme — *la famille que mes données ferment* » : c'est le
verdict lui-même, écrit par la même main au même moment. Le donner au trieur
rendrait la condition B (aucun `non` promu `oui`) satisfaite d'avance. Le trieur
décide ligne par ligne, sans le regroupement que l'auteur avait déjà conclu.

Ce qui reste dans la ligne suffit, et c'est ce que l'humain avait : pour les
entrées 18 et 19, la colonne « données exigées » dit « au moins la deuxième
échéance », et c'est un fait sur le papier, pas un jugement sur nos données.

    python corpus/make_triage_input.py            # écrit corpus/triage_input.json
    python corpus/make_triage_input.py --check    # vérifie sans écrire

Code de sortie 1 si l'entrée fuite, ou si `AMORCE.md` n'a plus la forme attendue.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AMORCE = REPO / "corpus" / "AMORCE.md"
OUTPUT = REPO / "corpus" / "triage_input.json"

VERDICT_COLUMN = "Implémentable"
EXPECTED_ENTRIES = 20

HEADER = re.compile(r"^\|\s*#\s*\|(.+)\|\s*$")
ROW = re.compile(r"^\|\s*(\d+)\s*\|(.+)\|\s*$")

# Ce qui trahirait la réponse dans une cellule conservée. La colonne verdict
# porte ses valeurs en gras ; si l'une de ces formes survit au découpage, c'est
# que le découpage est faux.
LEAKS = ("**oui**", "**partiel**", "**non**")


class LeakError(RuntimeError):
    """L'entrée du trieur contient la réponse. On n'écrit rien."""


def cells(body: str) -> list[str]:
    return [c.strip() for c in body.split("|")]


def build(path: Path = AMORCE) -> list[dict]:
    """Les 20 lignes notées, chacune privée de sa colonne verdict."""
    rows: list[dict] = []
    headers: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        header = HEADER.match(line)
        if header:
            headers = cells(header.group(1))
            continue
        row = ROW.match(line)
        if not row or not headers:
            continue
        if headers[-1] != VERDICT_COLUMN:
            continue  # section G (méthode) : pas de colonne verdict, hors étalon
        values = cells(row.group(2))
        if len(values) != len(headers):
            raise LeakError(
                f"entrée {row.group(1)} : {len(values)} cellules pour "
                f"{len(headers)} colonnes — le découpage ne tient pas"
            )
        rows.append(
            {
                "entry": int(row.group(1)),
                "fields": dict(zip(headers[:-1], values[:-1], strict=True)),
            }
        )
    return rows


def audit(rows: list[dict]) -> list[str]:
    """Tout ce qui empêche de servir cette entrée à un trieur. Vide veut dire propre."""
    bad: list[str] = []
    if len(rows) != EXPECTED_ENTRIES:
        bad.append(f"{len(rows)} entrées produites, {EXPECTED_ENTRIES} attendues")
    if sorted(r["entry"] for r in rows) != list(range(1, EXPECTED_ENTRIES + 1)):
        bad.append(f"les entrées ne sont pas 1..{EXPECTED_ENTRIES}")

    for row in rows:
        if VERDICT_COLUMN in row["fields"]:
            bad.append(f"entrée {row['entry']} : la colonne verdict est encore là")
        blob = " ".join(row["fields"].values()).lower()
        for leak in LEAKS:
            if leak in blob:
                bad.append(f"entrée {row['entry']} : une cellule porte `{leak}`")
    return bad


def main(argv: list[str]) -> int:
    check_only = argv == ["--check"]
    if argv and not check_only:
        print(__doc__)
        return 1

    try:
        rows = build()
    except LeakError as error:
        print(f"REFUSÉ : {error}")
        return 1

    problems = audit(rows)
    for row in rows:
        names = ", ".join(row["fields"])
        print(f"  entrée {row['entry']:2d} · {len(row['fields'])} champs : {names}")

    print(f"\n{len(rows)} entrées, colonne verdict retirée, titres de section non repris")
    if problems:
        print("ENTRÉE DU TRIEUR : REFUSÉE")
        for line in problems:
            print(f"  - {line}")
        return 1

    if check_only:
        print("ENTRÉE DU TRIEUR : propre — rien n'a été écrit (--check)")
        return 0

    OUTPUT.write_text(
        json.dumps({"source": AMORCE.name, "entries": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"ENTRÉE DU TRIEUR : propre — écrite dans {OUTPUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
