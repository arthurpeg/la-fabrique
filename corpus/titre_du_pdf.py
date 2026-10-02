"""Un PDF moissonné porte-t-il le titre du papier qu'on lui attribue ?

Le 2026-10-02, le graphe du corpus a montré deux paires de papiers aux vecteurs
identiques : la moisson avait pris, sur une page PubMed Central, un lien de la
bibliographie (le livre blanc de Bitcoin) pour le PDF de deux papiers, et
OpenAlex attribuait un même dépôt arXiv à deux papiers de Kristoufek. Le texte
d'un autre papier était entré en base sous leur nom, sans qu'aucune garde ne
le voie.

Le contrôle : les mots du titre (quatre lettres au moins) doivent se retrouver
dans les deux premières pages du PDF. Un PDF qui n'en porte pas la plupart
n'est pas le bon papier — ou n'est pas lisible, ce qui revient au même pour
l'ingestion.

    python corpus/titre_du_pdf.py                 # tous les PDF moissonnés
    python corpus/titre_du_pdf.py --pdf <chemin> --titre "<titre>"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARVEST = REPO / "corpus" / "harvest.json"
SORTIE = REPO / "corpus" / "titres_des_pdf.json"

PAGES = 2
SEUIL = 0.6  # part des mots du titre retrouvés, fixée avant le premier passage


def norm(texte: str) -> str:
    t = unicodedata.normalize("NFKD", texte or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", t.lower())


def mots(titre: str) -> list[str]:
    return sorted({m for m in norm(titre).split() if len(m) >= 4})


def premieres_pages(pdf: Path) -> str | None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from pypdf import PdfReader  # noqa: PLC0415

        try:
            pages = PdfReader(str(pdf)).pages
            return " ".join((pages[i].extract_text() or "") for i in range(min(PAGES, len(pages))))
        except Exception:  # noqa: BLE001 — un PDF illisible est un verdict, pas une panne
            return None


def titre_principal(titre: str) -> str:
    """Le titre avant son sous-titre : une version de travail n'a souvent que lui
    (« Short-Selling Bans around the World », sans « Evidence from the 2007–09 Crisis »)."""
    return re.split(r"[:?—–]|\s-\s", titre or "")[0]


def part(texte: str, titre: str) -> float:
    attendus = mots(titre)
    if not attendus:
        return 1.0
    # Sans espaces aussi : pypdf colle souvent les mots d'un titre en capitales.
    lu, colle = f" {norm(texte)} ", norm(texte).replace(" ", "")
    return sum(1 for m in attendus if f" {m} " in lu or m in colle) / len(attendus)


def score(pdf: Path, titre: str) -> float | None:
    """La part des mots du titre présents au début du PDF ; None si illisible.

    Le meilleur du titre entier et du titre principal, celui-ci seulement s'il
    garde trois mots au moins : deux mots courants se retrouvent partout."""
    texte = premieres_pages(pdf)
    if texte is None:
        return None
    s = part(texte, titre)
    principal = titre_principal(titre)
    if principal != titre and len(mots(principal)) >= 3:
        s = max(s, part(texte, principal))
    return s


def porte_son_titre(pdf: Path, titre: str) -> bool:
    s = score(pdf, titre)
    return s is not None and s >= SEUIL


def balayer() -> list[dict]:
    works = json.loads(HARVEST.read_text(encoding="utf-8"))["works"]
    out = []
    avec_pdf = [w for w in works if w.get("pdf") and (REPO / w["pdf"]).is_file()]
    for rang, w in enumerate(avec_pdf, 1):
        if rang % 100 == 0:
            print(f"  {rang}/{len(avec_pdf)}", flush=True)
        s = score(REPO / w["pdf"], w.get("title") or "")
        out.append({"openalex_id": w["openalex_id"], "pdf": w["pdf"], "title": w.get("title"),
                    "source_url": w.get("source_url"), "duplicate_of": w.get("duplicate_of"),
                    "score": None if s is None else round(s, 3)})
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le PDF porte-t-il le titre du papier ?")
    ap.add_argument("--pdf", type=Path)
    ap.add_argument("--titre")
    a = ap.parse_args(argv)
    if a.pdf:
        s = score(a.pdf, a.titre or "")
        print(f"{'illisible' if s is None else f'{s:.2f}'} "
              f"{'OK' if s is not None and s >= SEUIL else 'REFUS'}")
        return 0 if s is not None and s >= SEUIL else 1
    res = balayer()
    SORTIE.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    refus = [r for r in res if r["score"] is None or r["score"] < SEUIL]
    print(f"{len(res)} PDF lus, {len(refus)} sous le seuil de {SEUIL} "
          f"(dont {sum(1 for r in refus if r['score'] is None)} illisibles)")
    for r in sorted(refus, key=lambda r: r["score"] or 0)[:40]:
        print(f"  {r['score']}  {(r['title'] or '')[:70]}  <- {(r['source_url'] or '')[:60]}")
    print(f"écrit : {SORTIE.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
