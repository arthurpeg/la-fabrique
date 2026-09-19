"""Le juge du triage. Il apparie un verdict de trieur à l'étalon, entrée par entrée.

Écrit **avant** le trieur, et vérifié contre des sorties fabriquées — l'ordre de
construction de `CLAUDE.md` appliqué à l'intérieur de la phase 07, comme `D06`
l'a fait pour les signaux.

L'étalon est la colonne « implémentable » de `corpus/AMORCE.md`, lue ici **dans
le fichier** plutôt que recopiée : une copie dérive, et `L14` a montré ce qu'un
nombre recopié coûte. Sections A à F, entrées 1 à 20, attendues en
13 `oui` / 5 `partiel` / 2 `non` (`D15`). Si le fichier ne rend plus exactement
cette forme, le script **refuse de noter quoi que ce soit** : l'étalon est gelé,
et un étalon qui bouge sous le juge n'est plus un étalon.

Ce qui est vérifié n'est pas un score mais un **appariement** — `L06` mot pour
mot : un compte juste n'est pas un compte de choses justes. La matrice entière
est imprimée, et chaque désaccord est nommé avec le motif que le trieur a donné.

    python corpus/score_triage.py --check              # le juge se teste lui-même
    python corpus/score_triage.py verdicts.json        # le juge note un trieur

Code de sortie 1 si la porte n'est pas franchie, ou si l'entrée est malformée.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AMORCE = REPO / "corpus" / "AMORCE.md"

CLASSES = ("oui", "partiel", "non")
RANK = {"non": 0, "partiel": 1, "oui": 2}

# L'étalon, tel que D15 le fixe. Ce n'est pas la source — AMORCE.md l'est — mais
# la forme attendue : le script refuse de noter si le fichier ne la rend plus.
EXPECTED_ENTRIES = 20
EXPECTED_COUNTS = {"oui": 13, "partiel": 5, "non": 2}

# Les quatre conditions de D15 § Le choix. Elles valent ENSEMBLE.
MAX_OUI_MISSED = 1  # A
MAX_NON_PROMOTED = 0  # B
MAX_PARTIEL_DISAGREED = 2  # C
MAX_TWO_RUNG = 0  # D

ROW = re.compile(r"^\|\s*(\d+)\s*\|(.+)\|\s*$")
VERDICT = re.compile(r"^\**(oui|partiel|non)\**(?:\s|$|—|-)")


class EtalonError(RuntimeError):
    """L'étalon ne rend plus la forme que D15 a gelée. On ne note pas."""


def read_etalon(path: Path = AMORCE) -> dict[int, str]:
    """La colonne « implémentable », lue dans AMORCE.md. Entrées 1 à 20.

    Les quatre entrées de la section G (méthode) n'ont pas cette colonne : leur
    dernière cellule est une phrase, pas un verdict, et le filtre les écarte
    parce qu'elles ne commencent par aucun des trois mots.
    """
    etalon: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        entry = int(match.group(1))
        last = match.group(2).split("|")[-1].strip()
        verdict = VERDICT.match(last)
        if verdict is None:
            continue  # section G : pas de colonne verdict
        if entry in etalon:
            raise EtalonError(f"l'entrée {entry} apparaît deux fois dans {path.name}")
        etalon[entry] = verdict.group(1)

    counts = {c: sum(1 for v in etalon.values() if v == c) for c in CLASSES}
    if len(etalon) != EXPECTED_ENTRIES or counts != EXPECTED_COUNTS:
        raise EtalonError(
            f"{path.name} rend {len(etalon)} verdicts {counts}, "
            f"quand D15 a gelé {EXPECTED_ENTRIES} verdicts {EXPECTED_COUNTS}. "
            "L'étalon est gelé : une correction s'inscrit en note datée, jamais "
            "par réécriture de la colonne."
        )
    if set(etalon) != set(range(1, EXPECTED_ENTRIES + 1)):
        raise EtalonError(f"les entrées notées ne sont pas 1..{EXPECTED_ENTRIES}")
    return etalon


def read_verdicts(path: Path) -> tuple[dict[int, str], dict[int, str]]:
    """Ce que le trieur a rendu : un verdict et un motif par entrée.

    Le motif est **exigé**. Un trieur qui ne dit pas pourquoi ne se relit pas, et
    `D15` demande que chaque désaccord soit examiné, pas compté.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("entries")
    if not isinstance(rows, list):
        raise ValueError(f"{path.name} : clé `entries` absente ou pas une liste")

    verdicts: dict[int, str] = {}
    reasons: dict[int, str] = {}
    for row in rows:
        entry = row.get("entry")
        verdict = row.get("verdict")
        reason = (row.get("reason") or "").strip()
        if not isinstance(entry, int):
            raise ValueError(f"{path.name} : `entry` absent ou pas un entier — {row}")
        if verdict not in CLASSES:
            raise ValueError(f"{path.name} : entrée {entry}, verdict `{verdict}` hors {CLASSES}")
        if not reason:
            raise ValueError(f"{path.name} : entrée {entry} sans motif — D15 l'exige")
        if entry in verdicts:
            raise ValueError(f"{path.name} : l'entrée {entry} est rendue deux fois")
        verdicts[entry] = verdict
        reasons[entry] = reason
    return verdicts, reasons


def score(etalon: dict[int, str], verdicts: dict[int, str]) -> dict:
    """Les quatre conditions de D15, et la matrice qui permet de les relire.

    `B` est un sous-ensemble de `D` — un `non` promu `oui` est aussi un désaccord
    de deux crans. Les deux sont gardées parce qu'elles nomment deux coûts
    distincts (B : un signal codé sur une donnée qu'on n'a pas ; D : une panne de
    lecture), et parce qu'une condition qui se déduit d'une autre ne coûte rien à
    vérifier. Ce n'est pas une redondance cachée : elle est écrite ici.
    """
    missing = sorted(set(etalon) - set(verdicts))
    extra = sorted(set(verdicts) - set(etalon))
    if missing or extra:
        raise ValueError(
            f"le trieur doit rendre exactement les entrées 1..{EXPECTED_ENTRIES} — "
            f"manquantes {missing}, en trop {extra}"
        )

    matrix = {t: {p: 0 for p in CLASSES} for t in CLASSES}
    disagreements: list[tuple[int, str, str]] = []
    for entry, truth in sorted(etalon.items()):
        pred = verdicts[entry]
        matrix[truth][pred] += 1
        if pred != truth:
            disagreements.append((entry, truth, pred))

    a = sum(1 for _, t, p in disagreements if t == "oui" and p != "oui")
    b = sum(1 for _, t, p in disagreements if t == "non" and p == "oui")
    c = sum(1 for _, t, p in disagreements if t == "partiel" and p != "partiel")
    d = sum(1 for _, t, p in disagreements if abs(RANK[t] - RANK[p]) == 2)

    conditions = {
        "A": (a, MAX_OUI_MISSED, "`oui` de l'étalon classés autrement"),
        "B": (b, MAX_NON_PROMOTED, "`non` de l'étalon classés `oui`"),
        "C": (c, MAX_PARTIEL_DISAGREED, "`partiel` de l'étalon en désaccord"),
        "D": (d, MAX_TWO_RUNG, "desaccords de deux crans (`oui` <-> `non`)"),
    }
    passed = all(value <= limit for value, limit, _ in conditions.values())
    return {
        "matrix": matrix,
        "disagreements": disagreements,
        "conditions": conditions,
        "passed": passed,
    }


def render(result: dict, reasons: dict[int, str] | None = None) -> str:
    lines = ["", "Matrice — lignes : l'étalon · colonnes : le trieur", ""]
    lines.append(f"  {'':10s}" + "".join(f"{p:>10s}" for p in CLASSES))
    for truth in CLASSES:
        row = "".join(f"{result['matrix'][truth][p]:>10d}" for p in CLASSES)
        lines.append(f"  {truth:10s}{row}")

    lines.append("")
    if result["disagreements"]:
        lines.append(f"Désaccords ({len(result['disagreements'])} sur {EXPECTED_ENTRIES}) :")
        for entry, truth, pred in result["disagreements"]:
            gravity = " — DEUX CRANS" if abs(RANK[truth] - RANK[pred]) == 2 else ""
            lines.append(f"  entrée {entry:2d} : étalon `{truth}`, trieur `{pred}`{gravity}")
            if reasons:
                lines.append(f"             motif du trieur : {reasons[entry]}")
    else:
        lines.append("Aucun désaccord.")

    lines.append("")
    for key, (value, limit, label) in result["conditions"].items():
        state = "tenue" if value <= limit else "ROMPUE"
        lines.append(f"  {key} : {value} (max {limit}) · {label} — {state}")

    lines.append("")
    if result["passed"]:
        lines.append("TRIAGE : les quatre conditions de D15 tiennent.")
        lines.append("Le verdict de la porte cite le NUMÉRO DU PASSAGE (D15 § Journal).")
    else:
        lines.append("TRIAGE : NON FRANCHI — au moins une condition de D15 est rompue.")
        lines.append("Un échec ne s'achète pas en redéfinissant le seuil (D13, option 2).")
    return "\n".join(lines)


def self_check() -> int:
    """Le juge se teste contre des sorties fabriquées, avant que le trieur existe.

    Chaque cas dit ce qu'il doit faire et pourquoi. Un juge qu'on n'a vu rendre
    qu'un seul verdict n'a pas été vu travailler.
    """
    etalon = read_etalon()
    checks: list[tuple[str, bool, bool]] = []

    def case(label: str, verdicts: dict[int, str], expected_pass: bool) -> None:
        result = score(etalon, verdicts)
        checks.append((label, result["passed"], expected_pass))

    perfect = dict(etalon)
    case("un trieur parfait passe", perfect, True)

    oui_entries = [e for e, v in etalon.items() if v == "oui"]
    partiel_entries = [e for e, v in etalon.items() if v == "partiel"]
    non_entries = [e for e, v in etalon.items() if v == "non"]

    one_oui_missed = dict(perfect)
    one_oui_missed[oui_entries[0]] = "partiel"
    case("un seul `oui` manqué d'un cran passe (A = 1)", one_oui_missed, True)

    two_oui_missed = dict(one_oui_missed)
    two_oui_missed[oui_entries[1]] = "partiel"
    case("deux `oui` manqués échouent (A = 2)", two_oui_missed, False)

    one_non_promoted = dict(perfect)
    one_non_promoted[non_entries[0]] = "oui"
    case("un seul `non` promu `oui` échoue (B = 1)", one_non_promoted, False)

    non_to_partiel = dict(perfect)
    non_to_partiel[non_entries[0]] = "partiel"
    case("un `non` glissé en `partiel` passe (un cran, B = 0)", non_to_partiel, True)

    two_partiel = dict(perfect)
    two_partiel[partiel_entries[0]] = "oui"
    two_partiel[partiel_entries[1]] = "non"
    case("deux `partiel` en désaccord passent (C = 2)", two_partiel, True)

    three_partiel = dict(two_partiel)
    three_partiel[partiel_entries[2]] = "oui"
    case("trois `partiel` en désaccord échouent (C = 3)", three_partiel, False)

    two_rung = dict(perfect)
    two_rung[oui_entries[0]] = "non"
    case("un seul `oui` classé `non` échoue (D = 1, deux crans)", two_rung, False)

    # Le garde de l'étalon. C'est ce qui rend « l'étalon est gelé » vérifiable
    # plutôt que promis : si AMORCE.md bouge, le juge refuse de noter.
    guard: list[tuple[str, bool]] = []

    def guard_case(label: str, text: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "AMORCE.md"
            fake.write_text(text, encoding="utf-8")
            try:
                read_etalon(fake)
            except EtalonError:
                guard.append((label, True))
            else:
                guard.append((label, False))

    source = AMORCE.read_text(encoding="utf-8")
    flipped = source.replace("| **partiel** — univers actions", "| **oui** — univers actions", 1)
    dropped = "\n".join(line for line in source.splitlines() if not line.startswith("| 12 |"))
    if flipped == source or dropped == source:
        print("REFUSÉ : les mutations de contrôle ne mordent plus sur AMORCE.md")
        return 1
    guard_case("un verdict retourné dans AMORCE.md est refusé", flipped)
    guard_case("une ligne retirée d'AMORCE.md est refusée", dropped)

    print("Le juge, testé contre des sorties fabriquées — avant que le trieur existe.\n")
    failures = 0
    for label, got, want in checks:
        ok = got == want
        failures += not ok
        verdict = "franchi" if got else "non franchi"
        print(f"  {'ok ' if ok else 'FAUX'}  {label:58s} -> {verdict}")

    for label, refused in guard:
        failures += not refused
        state = "refusé" if refused else "ACCEPTÉ — le garde ne mord pas"
        print(f"  {'ok ' if refused else 'FAUX'}  {label:58s} -> {state}")

    print(f"\n{len(checks) + len(guard)} vérifications")
    if failures:
        print(f"JUGE DU TRIAGE : {failures} cas ne se comportent pas comme D15 l'écrit")
        return 1
    print("JUGE DU TRIAGE : il rend ce que D15 écrit, sur chacun des cas fabriqués")
    print(f"Étalon lu dans {AMORCE.name} : {EXPECTED_ENTRIES} verdicts {EXPECTED_COUNTS}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 1
    if argv[0] == "--check":
        return self_check()

    try:
        etalon = read_etalon()
        verdicts, reasons = read_verdicts(Path(argv[0]))
        result = score(etalon, verdicts)
    except (EtalonError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSÉ : {error}")
        return 1

    print(render(result, reasons))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
