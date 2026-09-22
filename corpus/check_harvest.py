"""Le garde du moissonnage — `D20`.

Meme office que `check_acquisition.py` pour le recensement : il ne sonde pas le
reseau, il juge le fichier ecrit. Une regle qui n'a rien qui la verifie n'est
pas une regle.

Ce qu'il refuse, et pourquoi chaque refus compte :

    H1  la requete inscrite dans `harvest.json` ne correspond plus a celle que
        `D20` a figee — c'est LE refus qui compte : une requete qu'on ajuste
        apres avoir vu ce qu'elle rend est un bouton, et tout le reste s'ecroule
    H2  un statut hors de {atteignable, inatteignable, non sonde}
    H3  un inatteignable sans raison, ou avec une raison hors de la liste CLOSE
        de `D17` — « inatteignable » sans motif est l'endroit ou l'on range ce
        qu'on n'a pas essaye
    H4  un atteignable sans URL source, ou sans dire d'OU vient cette URL (`D09`)
    H5  un atteignable sans preuve, ou dont la preuve ne dit pas `is_pdf`
        — c'est la faute qui laisserait passer une page de resume pour un texte
    H6  un atteignable portant quand meme une raison d'inatteignabilite
    H7  une entree sondee sans date de constat (`D17` : le constat est date)
    H8  un identifiant OpenAlex absent ou duplique — l'unicite du nom de
        fichier repose entierement dessus (`D20`)
    H9  le compte d'une famille est incoherent : plus de travaux libres que de
        travaux, ou plus de retenus que le plafond

Puis il se montre refusant chacune de ces fautes sur une moisson fabriquee, et
acceptant la moisson reelle. `L06` : un compte juste n'est pas un compte de
choses justes.

    python corpus/check_harvest.py

Code de sortie 1 si la moisson est fautive, ou si le garde laisse passer une
faute qu'il devait refuser.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARVEST = REPO / "corpus" / "harvest.json"

sys.path.insert(0, str(REPO / "corpus"))
from harvest import FAMILIES, FROM_DATE, REASONS, SORT, SUBFIELDS  # noqa: E402

STATUSES = ("atteignable", "inatteignable", None)


def faults(data: dict) -> list[str]:
    """Tout ce qui cloche, nomme. Liste vide = moisson conforme."""
    out = []

    # H1 — la requete. Comparee a `harvest.FAMILIES`, qui est la copie de
    # travail de ce que `D20` a ecrit. Un ecart ici ne se repare pas dans le
    # JSON : soit le code a derive, soit une decision manque.
    q = data.get("query") or {}
    if q.get("from_date") != FROM_DATE:
        out.append(f"H1 `from_date` {q.get('from_date')!r}, D20 dit {FROM_DATE!r}")
    if q.get("subfields") != SUBFIELDS:
        out.append(f"H1 `subfields` {q.get('subfields')!r}, D20 dit {SUBFIELDS!r}")
    if q.get("sort") != SORT:
        out.append(f"H1 `sort` {q.get('sort')!r}, D20 dit {SORT!r}")
    if not q.get("oa_only"):
        out.append("H1 la moisson n'est pas restreinte au libre (`oa_only`)")

    fams = data.get("families") or {}
    if sorted(fams) != sorted(FAMILIES):
        out.append(f"H1 familles {sorted(fams)}, D20 en fige {sorted(FAMILIES)}")
    for key, f in fams.items():
        if key in FAMILIES and f.get("search") != FAMILIES[key]:
            out.append(f"H1 famille {key} : la recherche a change depuis D20")
        # H9 — coherence des comptes.
        if (f.get("oa_total") or 0) > (f.get("total") or 0):
            out.append(f"H9 famille {key} : {f.get('oa_total')} libres "
                       f"pour {f.get('total')} travaux")
        if (f.get("retrieved") or 0) > (q.get("per_family") or 0):
            out.append(f"H9 famille {key} : {f.get('retrieved')} retenus "
                       f"pour un plafond de {q.get('per_family')}")

    seen_ids = set()
    for w in data.get("works") or []:
        oid = w.get("openalex_id")
        label = oid or w.get("title", "?")[:40]

        if not oid:
            out.append(f"H8 « {label} » : sans identifiant OpenAlex")
        elif oid in seen_ids:
            out.append(f"H8 {oid} : identifiant duplique")
        else:
            seen_ids.add(oid)

        status = w.get("status")
        if status not in STATUSES:
            out.append(f"H2 {label} : statut {status!r} hors de {STATUSES}")
            continue

        if status is None:
            continue

        if status == "inatteignable":
            if w.get("reason") not in REASONS:
                out.append(f"H3 {label} : raison {w.get('reason')!r} "
                           "absente de la liste close")
        else:
            if not w.get("source_url"):
                out.append(f"H4 {label} : atteignable sans `source_url`")
            if not w.get("source_via"):
                out.append(f"H4 {label} : atteignable sans provenance (`source_via`)")
            ev = w.get("evidence") or {}
            if not ev:
                out.append(f"H5 {label} : atteignable sans preuve")
            elif not ev.get("is_pdf"):
                out.append(f"H5 {label} : preuve ne disant pas `is_pdf`")
            if w.get("reason"):
                out.append(f"H6 {label} : atteignable ET raison {w['reason']!r}")

        if not w.get("checked"):
            out.append(f"H7 {label} : sonde sans date de constat")

    return out


def case(label: str, data: dict, expect_clean: bool, tag: str) -> bool:
    got = faults(data)
    ok = (not got) if expect_clean else any(f.startswith(tag) for f in got)
    print(f"  [{'ok ' if ok else 'RATE'}] {label}")
    if not ok:
        print(f"         attendu {tag}, obtenu : {got[:3] or 'aucune faute'}")
    return ok


def first(works: list[dict], status: str) -> dict | None:
    return next((w for w in works if w.get("status") == status), None)


def main() -> int:
    if not HARVEST.is_file():
        print(f"moisson absente : {HARVEST.relative_to(REPO)}")
        print("la produire avec : python corpus/harvest.py --search")
        return 1

    real = json.loads(HARVEST.read_text(encoding="utf-8"))
    checks = []

    print("La moisson reelle")
    checks.append(case("moisson conforme, acceptee", real, True, ""))

    print("\nLes fautes, chacune refusee pour la raison prevue")

    c = copy.deepcopy(real)
    c["query"]["sort"] = "publication_date:desc"
    checks.append(case("H1 le tri a change depuis D20", c, False, "H1"))

    c = copy.deepcopy(real)
    c["families"]["A"]["search"] = '"intraday momentum" AND profitable'
    checks.append(case("H1 la recherche d'une famille a change", c, False, "H1"))

    c = copy.deepcopy(real)
    c["query"]["oa_only"] = False
    checks.append(case("H1 la moisson n'est plus restreinte au libre", c, False, "H1"))

    c = copy.deepcopy(real)
    c["families"].pop("F", None)
    checks.append(case("H1 une famille manquante", c, False, "H1"))

    c = copy.deepcopy(real)
    c["works"][0]["status"] = "peut-etre"
    checks.append(case("H2 statut inconnu", c, False, "H2"))

    c = copy.deepcopy(real)
    if (bad := first(c["works"], "inatteignable")):
        bad["reason"] = "pas_eu_le_temps"
        checks.append(case("H3 raison hors de la liste close", c, False, "H3"))

    c = copy.deepcopy(real)
    if (bad := first(c["works"], "atteignable")):
        bad["source_url"] = None
        checks.append(case("H4 atteignable sans URL", c, False, "H4"))

    c = copy.deepcopy(real)
    if (bad := first(c["works"], "atteignable")):
        bad["source_via"] = ""
        checks.append(case("H4 atteignable sans provenance", c, False, "H4"))

    c = copy.deepcopy(real)
    if (bad := first(c["works"], "atteignable")):
        bad["evidence"] = dict(bad["evidence"], is_pdf=False)
        checks.append(case("H5 PDF annonce, preuve muette", c, False, "H5"))

    c = copy.deepcopy(real)
    if (bad := first(c["works"], "atteignable")):
        bad["reason"] = "peage"
        checks.append(case("H6 atteignable portant une raison", c, False, "H6"))

    c = copy.deepcopy(real)
    if (bad := first(c["works"], "atteignable")):
        bad["checked"] = None
        checks.append(case("H7 constat sans date", c, False, "H7"))

    c = copy.deepcopy(real)
    c["works"].append(copy.deepcopy(c["works"][0]))
    checks.append(case("H8 identifiant OpenAlex duplique", c, False, "H8"))

    c = copy.deepcopy(real)
    c["works"][0]["openalex_id"] = None
    checks.append(case("H8 identifiant absent", c, False, "H8"))

    c = copy.deepcopy(real)
    c["families"]["A"]["oa_total"] = c["families"]["A"]["total"] + 1
    checks.append(case("H9 plus de libres que de travaux", c, False, "H9"))

    c = copy.deepcopy(real)
    c["families"]["A"]["retrieved"] = c["query"]["per_family"] + 1
    checks.append(case("H9 plafond depasse", c, False, "H9"))

    works = real.get("works") or []
    ok = [w for w in works if w.get("status") == "atteignable"]
    sonde = [w for w in works if w.get("status")]
    print(f"\nEtat de la moisson au {real.get('checked')}")
    print(f"  candidats      : {len(works)}")
    print(f"  sondes         : {len(sonde)}")
    print(f"  atteignables   : {len(ok)}")
    print(f"  doublons       : {sum(1 for w in works if w.get('duplicate_of'))}")

    print(f"\ncheck_harvest : {sum(checks)} / {len(checks)} verifications")
    print("Rappel D20 : ce fichier n'entre PAS dans G1-G4. La porte 07 se juge")
    print("sur les 19 atteignables d'AMORCE.md et sur rien d'autre (F47).")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
