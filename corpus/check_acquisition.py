"""Le garde du recensement — `G4` de `D17`.

`G4` exige **zéro papier inatteignable non recensé, avec la raison**. Une
condition en effectif ne vaut que si quelque chose la vérifie : ce fichier est
ce quelque chose. Il ne sonde pas le réseau — il juge le recensement écrit.

Ce qu'il refuse, et pourquoi chaque refus compte :

    A1  le recensement ne couvre pas exactement les 20 entrées d'AMORCE.md
        — un papier omis est un papier choisi après coup, ce que G1 interdit
    A2  un statut hors de {atteignable, inatteignable}
    A3  un inatteignable sans raison, ou avec une raison hors de la liste CLOSE
        — « inatteignable » sans motif est l'endroit où l'on range ce qu'on n'a
        pas essayé
    A4  un atteignable sans URL source, ou sans dire d'OÙ vient cette URL
        — D09 : une valeur qui vient du dehors porte sa provenance
    A5  un atteignable sans preuve d'avoir obtenu le texte (`evidence`)
    A6  un atteignable qui porte quand même une raison d'inatteignabilité
    A7  une entrée sans date de constat — D17 : « le constat est daté »
    A8  un atteignable en PDF dont la preuve ne dit pas `is_pdf`
        — c'est la faute qui laisserait passer une page de résumé pour un texte

Puis il se montre refusant chacune de ces fautes sur un recensement fabriqué,
et acceptant le recensement réel. `L06` : un compte juste n'est pas un compte
de choses justes.

    python corpus/check_acquisition.py

Code de sortie 1 si le recensement est incomplet, ou si le garde laisse passer
une faute qu'il devait refuser.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CENSUS = REPO / "corpus" / "acquisition.json"

sys.path.insert(0, str(REPO / "corpus"))
from probe_acquisition import EXPECTED_ENTRIES, REASONS  # noqa: E402

STATUSES = ("atteignable", "inatteignable")


def faults(census: list[dict]) -> list[str]:
    """Tout ce qui cloche, nommé. Liste vide = recensement complet."""
    out = []

    seen = sorted(r.get("entry") for r in census)
    if seen != list(range(1, EXPECTED_ENTRIES + 1)):
        out.append(f"A1 le recensement couvre {seen}, attendu 1..{EXPECTED_ENTRIES}")

    for r in census:
        n = r.get("entry")
        status = r.get("status")
        if status not in STATUSES:
            out.append(f"A2 entree {n} : statut {status!r} hors de {STATUSES}")
            continue

        if status == "inatteignable":
            reason = r.get("reason")
            if reason not in REASONS:
                out.append(f"A3 entree {n} : raison {reason!r} absente de la liste close")
        else:
            if not r.get("source_url"):
                out.append(f"A4 entree {n} : atteignable sans `source_url`")
            if not r.get("source_via"):
                out.append(f"A4 entree {n} : atteignable sans provenance (`source_via`)")
            if not r.get("evidence"):
                out.append(f"A5 entree {n} : atteignable sans preuve")
            if r.get("reason"):
                out.append(f"A6 entree {n} : atteignable ET raison {r['reason']!r}")
            if r.get("text_format") == "pdf" and not (r.get("evidence") or {}).get("is_pdf"):
                out.append(f"A8 entree {n} : annonce un PDF, la preuve ne le dit pas")

        if not r.get("checked"):
            out.append(f"A7 entree {n} : constat sans date")

    return out


def case(label: str, census: list[dict], expect_clean: bool, tag: str) -> bool:
    got = faults(census)
    ok = (not got) if expect_clean else any(f.startswith(tag) for f in got)
    print(f"  [{'ok ' if ok else 'RATE'}] {label}")
    if not ok:
        print(f"         attendu {tag}, obtenu : {got[:3] or 'aucune faute'}")
    return ok


def main() -> int:
    if not CENSUS.is_file():
        print(f"recensement absent : {CENSUS.relative_to(REPO)}")
        print("le produire avec : python corpus/probe_acquisition.py --write")
        return 1

    real = json.loads(CENSUS.read_text(encoding="utf-8"))
    checks = []

    print("Le recensement reel")
    checks.append(case("recensement complet, accepte", real, True, ""))

    print("\nLes fautes, chacune refusee pour la raison prevue")

    c = copy.deepcopy(real)
    c.pop()
    checks.append(case("A1 une entree manquante", c, False, "A1"))

    c = copy.deepcopy(real)
    c[0]["status"] = "peut-etre"
    checks.append(case("A2 statut inconnu", c, False, "A2"))

    c = copy.deepcopy(real)
    bad = next(r for r in c if r["status"] == "inatteignable")
    bad["reason"] = None
    checks.append(case("A3 inatteignable sans raison", c, False, "A3"))

    c = copy.deepcopy(real)
    bad = next(r for r in c if r["status"] == "inatteignable")
    bad["reason"] = "pas_eu_le_temps"
    checks.append(case("A3 raison hors de la liste close", c, False, "A3"))

    c = copy.deepcopy(real)
    next(r for r in c if r["status"] == "atteignable")["source_url"] = None
    checks.append(case("A4 atteignable sans URL", c, False, "A4"))

    c = copy.deepcopy(real)
    next(r for r in c if r["status"] == "atteignable")["source_via"] = ""
    checks.append(case("A4 atteignable sans provenance", c, False, "A4"))

    c = copy.deepcopy(real)
    next(r for r in c if r["status"] == "atteignable")["evidence"] = {}
    checks.append(case("A5 atteignable sans preuve", c, False, "A5"))

    c = copy.deepcopy(real)
    next(r for r in c if r["status"] == "atteignable")["reason"] = "peage"
    checks.append(case("A6 atteignable portant une raison", c, False, "A6"))

    c = copy.deepcopy(real)
    c[0]["checked"] = None
    checks.append(case("A7 constat sans date", c, False, "A7"))

    c = copy.deepcopy(real)
    bad = next(r for r in c if r.get("text_format") == "pdf")
    bad["evidence"] = dict(bad["evidence"], is_pdf=False)
    checks.append(case("A8 PDF annonce, preuve muette", c, False, "A8"))

    ok = [r for r in real if r["status"] == "atteignable"]
    ko = [r for r in real if r["status"] == "inatteignable"]
    print(f"\nEtat du recensement au {real[0]['checked']}")
    print(f"  atteignables   : {len(ok)} / {EXPECTED_ENTRIES}"
          f"  (dont {sum(1 for r in ok if r['text_format'] == 'pdf')} en PDF)")
    print(f"  inatteignables : {len(ko)}")
    for r in ko:
        print(f"    entree {r['entry']:>2} — {r['reason']} : {REASONS[r['reason']]}")
    alertes = [r for r in real if r.get("alerte")]
    if alertes:
        print(f"  alertes        : {len(alertes)} — entrees "
              f"{', '.join(str(r['entry']) for r in alertes)}")

    print(f"\ncheck_acquisition : {sum(checks)} / {len(checks)} verifications")
    if len(ok) < 5:
        print("SEUIL DE D17 FRANCHI VERS LE BAS : moins de 5 atteignables,")
        print("l'option 2 (elargir le corpus) doit etre rouverte.")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
