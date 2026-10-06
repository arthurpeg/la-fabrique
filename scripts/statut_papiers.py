"""Où en est chaque papier, et s'il peut encore servir.

La question de l'opérateur (2026-09-30) : un papier devient-il inutile, ou peut-il
toujours servir ? Ce script répond papier par papier, en lisant **seulement**
ce que la chaîne a déjà écrit — il ne décide rien, ne calcule aucun IC, et ne
lit pas la base (qui demande le réseau).

Chaque papier est placé à l'étape la plus avancée qu'il a atteinte, dans
l'ordre de la chaîne, et reçoit un **sort** :

- `fini` — doublon, écarté par le tri, écarté du lot, ou mesuré. Il ne sert
  plus pour un signal seul ; un papier mesuré reste lisible pour les régimes
  et les combinaisons (phases 05, 07).
- `bloqué` — inatteignable : péage, refus des robots, pas de source libre. Il
  servira si une source libre apparaît, ou s'il est déposé à la main (`D30`).
- `en cours` — toute autre étape : il attend la suivante, que la colonne
  « prochaine étape » nomme.

Le retrait de la base de recherche (`D33`, `corpus/base_retraits.jsonl`) est
signalé à part : il ne sort pas le papier de la chaîne, `D33` laisse intactes
la population du moissonneur, du tri et du lot.

    python scripts/statut_papiers.py                    # le bilan par étape
    python scripts/statut_papiers.py --etape "à trier"  # la liste d'une étape
    python scripts/statut_papiers.py --cherche momentum # un papier par son titre
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from codage_verifie import RECETTES, principal_de, verifie  # noqa: E402

CORPUS = REPO / "corpus"
OUT = REPO / "scripts" / "out" / "statut_papiers.json"

# Les étapes, dans l'ordre de la chaîne : (étape, sort, prochaine étape).
ETAPES = [
    ("doublon", "fini", "—"),
    ("inatteignable", "bloqué", "une source libre, ou un dépôt à la main (D30)"),
    ("non sondé", "en cours", "sonder (harvest.py --probe)"),
    ("à télécharger", "en cours", "télécharger (harvest.py --fetch)"),
    ("à trier", "en cours", "trier (corpus/triage_harvest.py)"),
    ("écarté par le tri", "fini", "—"),
    ("à promouvoir", "en cours", "promouvoir (corpus/promote_harvest.py)"),
    ("à ficher", "en cours", "ficher (extract_fiche_harvest.py)"),
    ("à mettre en recette", "en cours", "recette (scripts/recette.py)"),
    ("à coder", "en cours", "un codage (CODAGE-DES-SIGNAUX.md)"),
    ("codage refusé", "en cours", "renvoyer au codeur le verdict du juge (D23)"),
    ("vérifié, hors lot", "en cours", "entrer dans un lot"),
    ("vérifié, en lot", "en cours", "hypothèse, matrice, mesure (étapes 8-10)"),
    ("écarté du lot", "fini", "—"),
    ("mesuré", "fini", "—"),
]
SORT = {e: s for e, s, _ in ETAPES}
SUITE = {e: n for e, _, n in ETAPES}


def norm(titre: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (titre or "").lower()).strip()


def charger(nom: str, defaut):
    p = CORPUS / nom
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else defaut


def aval_de_la_fiche(fiche_id: str, lot: dict, mesures: set[str]) -> str:
    """L'étape d'un papier qui a sa fiche."""
    dans_lot = {e["fiche_id"] for e in lot.get("fiches", [])}
    ecartees = {e["fiche_id"] for e in lot.get("ecartees_codage", [])}
    if fiche_id in mesures:
        return "mesuré"
    if fiche_id in ecartees:
        return "écarté du lot"
    if verifie(fiche_id)[0]:
        return "vérifié, en lot" if fiche_id in dans_lot else "vérifié, hors lot"
    if not (RECETTES / f"{fiche_id}.json").is_file():
        return "à mettre en recette"
    if principal_de(fiche_id).is_file():
        return "codage refusé"
    return "à coder"


def bilan() -> list[dict]:
    works = charger("harvest.json", {}).get("works", [])
    tri = {norm(v["title"]): v["verdict"] for v in charger("triage_harvest_verdicts.json", [])}
    promus = {p["openalex_id"] for p in charger("harvest_promoted.json", [])}
    lot_path = REPO / "hypotheses" / "LOT-09.json"
    lot = json.loads(lot_path.read_text(encoding="utf-8")) if lot_path.is_file() else {}
    registre = [json.loads(x) for x in
                (REPO / "registry" / "tests.jsonl").read_text(encoding="utf-8").splitlines()
                if x.strip()]
    mesures = {r["signal_id"] for r in registre if r.get("stage") == "09-passage"}
    retraits = set()
    rp = CORPUS / "base_retraits.jsonl"
    if rp.is_file():
        for x in rp.read_text(encoding="utf-8").splitlines():
            if x.strip():
                retraits.add(norm(json.loads(x).get("title", "")))

    fiches_h = {}
    for f in (CORPUS / "fiches_harvest").glob("*.json"):
        m = re.search(r"-(W\d+)$", f.stem)
        if m:
            fiches_h[m.group(1)] = f.stem

    rows: list[dict] = []
    for w in works:
        oid, titre = w["openalex_id"], w["title"]
        if w.get("duplicate_of"):
            etape = "doublon"
        elif oid in fiches_h:
            etape = aval_de_la_fiche(fiches_h[oid], lot, mesures)
        elif oid in promus:
            etape = "à ficher"
        elif w["status"] == "inatteignable":
            etape = "inatteignable"
        elif w["status"] is None:
            etape = "non sondé"
        elif not w.get("pdf"):
            etape = "à télécharger"
        else:
            v = tri.get(norm(titre))
            etape = ("à trier" if v is None else
                     "écarté par le tri" if v == "non" else "à promouvoir")
        rows.append({"id": oid, "title": titre, "year": w.get("year"), "origin": "moisson",
                     "stage": etape, "fate": SORT[etape], "next": SUITE[etape],
                     "reason": w.get("reason") if etape == "inatteignable" else None,
                     "fiche_id": fiches_h.get(oid),
                     "out_of_search_base": norm(titre) in retraits})

    for e in charger("acquisition.json", []):
        fiche = next((f.stem for f in (CORPUS / "fiches").glob("*.json")
                      if json.loads(f.read_text(encoding="utf-8"))["source"]
                      .get("amorce_entry") == e["entry"]), None)
        if fiche:
            etape = aval_de_la_fiche(fiche, lot, mesures)
        elif e["status"] == "inatteignable":
            etape = "inatteignable"
        else:
            etape = "à ficher"
        rows.append({"id": f"AMORCE-{e['entry']}", "title": e["citation"], "year": None,
                     "origin": "AMORCE", "stage": etape, "fate": SORT[etape],
                     "next": SUITE[etape],
                     "reason": e.get("reason") if etape == "inatteignable" else None,
                     "fiche_id": fiche, "out_of_search_base": False})
    return rows


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le statut de chaque papier")
    ap.add_argument("--etape", help="lister les papiers d'une étape")
    ap.add_argument("--cherche", help="chercher un papier par son titre")
    a = ap.parse_args(argv)
    rows = bilan()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    if a.etape or a.cherche:
        choix = [r for r in rows if (a.etape and r["stage"] == a.etape)
                 or (a.cherche and a.cherche.lower() in (r["title"] or "").lower())]
        for r in choix:
            print(f"  {r['stage']:<22} {r['id']:<14} {(r['title'] or '')[:80]}")
        print(f"\n{len(choix)} papier(s)")
        return 0

    parts = Counter(r["stage"] for r in rows)
    sorts = Counter(r["fate"] for r in rows)
    print(f"{'étape':<24}{'papiers':>8}  {'sort':<9} prochaine étape")
    for etape, sort, suite in ETAPES:
        if parts.get(etape):
            print(f"{etape:<24}{parts[etape]:>8}  {sort:<9} {suite}")
    print(f"\n{len(rows)} papiers : " + ", ".join(f"{n} {s}" for s, n in sorts.most_common()))
    bloques = Counter(r["reason"] for r in rows if r["stage"] == "inatteignable")
    if bloques:
        print("bloqués : " + ", ".join(f"{n} {m}" for m, n in bloques.most_common()))
    hors = sum(r["out_of_search_base"] for r in rows)
    print(f"hors de la base de recherche (D33), sans sortir de la chaîne : {hors}")
    print(f"détail : {OUT.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
