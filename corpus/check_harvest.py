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
from harvest import (  # noqa: E402
    FROM_DATE,
    PER_FAMILY,
    REASONS,
    SORT,
    SUBFIELDS,
    load_axes,
)

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
    # Le plafond etait compare a LUI-MEME — le JSON declarait son propre plafond
    # et `H9` verifiait qu'il le respectait, donc un `--per-family 500` passait
    # sans un mot. Trou trouve le 2026-09-22 en portant le plafond a 60.
    if q.get("per_family") != PER_FAMILY:
        out.append(f"H1 `per_family` {q.get('per_family')!r}, D20 dit {PER_FAMILY!r}")

    # H10 — LE refus qui porte `D21`. Ajouter un axe est libre ; en modifier un
    # QUI A DEJA SERVI ne l'est pas. `harvest.json` garde la chaine exacte du
    # passage ; si le YAML en dit une autre, un axe a ete reecrit APRES avoir vu
    # ce qu'il rendait — et tout ce qu'il a ramene change retroactivement de sens.
    try:
        declared = load_axes()
    except Exception as e:  # noqa: BLE001 — un YAML casse est une faute, pas un plantage
        declared = {}
        out.append(f"H10 `harvest_axes.yaml` illisible : {type(e).__name__}: {e}")

    fams = data.get("families") or {}
    for key, f in fams.items():
        if key not in declared:
            out.append(f"H10 axe {key} utilise mais absent de harvest_axes.yaml")
        elif f.get("search") != declared[key]["search"]:
            out.append(f"H10 axe {key} : la recherche a CHANGE depuis le passage "
                       f"qui l'a utilise")
        elif f.get("source", "openalex") != declared[key].get("source", "openalex"):
            out.append(f"H10 axe {key} : la SOURCE de decouverte a change depuis "
                       f"le passage qui l'a utilise")
    for w in data.get("works") or []:
        if not (w.get("axes") or []):
            out.append(f"H10 travail {w.get('openalex_id')} : AUCUN axe — il est "
                       "dans le corpus sans trace de ce qui l'y a fait entrer")
            continue
        for ax in w["axes"]:
            if ax not in fams:
                out.append(f"H10 travail {w.get('openalex_id')} : axe {ax} "
                           "inconnu du recensement des axes")
                break

    for key, f in fams.items():
        # H9 — coherence des comptes.
        if (f.get("oa_total") or 0) > (f.get("total") or 0):
            out.append(f"H9 famille {key} : {f.get('oa_total')} libres "
                       f"pour {f.get('total')} travaux")
        if (f.get("retrieved") or 0) > (q.get("per_family") or 0):
            out.append(f"H9 famille {key} : {f.get('retrieved')} retenus "
                       f"pour un plafond de {q.get('per_family')}")

    seen_ids = set()
    for w in data.get("works") or []:
        # L'identite est l'identifiant OpenAlex, ou LE DOI quand OpenAlex ne
        # connait pas le travail — cas normal d'un depot SSRN qu'aucun autre
        # depot ne reprend (`D21`, voie Crossref). Ce qui reste exige, c'est
        # qu'une identite existe et soit unique : le nom de fichier en depend.
        oid = w.get("openalex_id") or (f"doi:{w['doi']}" if w.get("doi") else None)
        label = oid or w.get("title", "?")[:40]

        if not oid:
            out.append(f"H8 « {label} » : ni identifiant OpenAlex ni DOI")
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
    first_axis = sorted(c["families"])[0]
    c["families"][first_axis]["search"] = '"intraday momentum" AND profitable'
    checks.append(case("H10 un axe a ete REECRIT apres avoir servi", c, False, "H10"))

    c = copy.deepcopy(real)
    c["families"]["anomaly:invente-apres-coup"] = dict(
        c["families"][first_axis], label="axe non declare")
    checks.append(case("H10 un axe utilise sans etre declare", c, False, "H10"))

    c = copy.deepcopy(real)
    if c["works"]:
        c["works"][0]["axes"] = ["asset:jamais-declare"]
        checks.append(case("H10 un travail portant un axe inconnu", c, False, "H10"))

    c = copy.deepcopy(real)
    c["query"]["oa_only"] = False
    checks.append(case("H1 la moisson n'est plus restreinte au libre", c, False, "H1"))

    c = copy.deepcopy(real)
    c["query"]["per_family"] = PER_FAMILY * 20
    checks.append(case("H1 le plafond a ete releve hors decision", c, False, "H1"))

    # Un axe ABSENT n'est plus une faute depuis `D21` : lancer un sous-ensemble
    # d'axes est legitime. Ce qui reste une faute, c'est un papier SANS AUCUN
    # axe — il serait dans le corpus sans trace de ce qui l'y a fait entrer.
    c = copy.deepcopy(real)
    if c["works"]:
        c["works"][0]["axes"] = []
        checks.append(case("H10 un travail sans aucun axe", c, False, "H10"))

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
    c["works"][0]["doi"] = None
    checks.append(case("H8 ni identifiant OpenAlex ni DOI", c, False, "H8"))

    # Un travail sans identifiant OpenAlex mais AVEC un DOI est legitime : c'est
    # le depot SSRN qu'aucun autre depot ne reprend. Il doit passer.
    c = copy.deepcopy(real)
    c["works"][0]["openalex_id"] = None
    c["works"][0]["doi"] = "10.2139/ssrn.9999999"
    checks.append(case("H8 un DOI seul suffit comme identite", c, True, ""))

    c = copy.deepcopy(real)
    c["families"][first_axis]["oa_total"] = c["families"][first_axis]["total"] + 1
    checks.append(case("H9 plus de libres que de travaux", c, False, "H9"))

    c = copy.deepcopy(real)
    c["families"][first_axis]["retrieved"] = c["query"]["per_family"] + 1
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
