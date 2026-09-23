"""Du texte qui fait foi vers la base vectorielle.

Il relie deux pièces qui existaient déjà et ne se parlaient pas : `corpus/text/`,
le texte versionné de `D18`, et `vectordb/`, la base. Entre les deux, il découpe,
situe et range. Il n'extrait aucun PDF de son propre chef et n'appelle aucun
modèle d'embedding.

**Le texte ingéré est celui qui fait foi, pas une nouvelle extraction.** Chaque
morceau vient de `corpus/text/<papier>.default.txt`, dont le manifeste porte
l'empreinte. Ré-extraire ici créerait une seconde source qui dériverait de la
première sans que rien ne le dise.

**Le mode `default` et non `layout`, et il faut le dire.** `D18` définit le texte
qui fait foi comme l'UNION des deux, et c'est ce que `F2` fouille pour vérifier
une citation. Mais une base vectorielle a besoin d'UN texte, pas de deux : le
mode `layout` aligne les colonnes avec des espaces de remplissage, qui gonflent
les morceaux sans rien porter de sémantique. Le choix est donc `default`, et il
ne change rien à `F2`, qui continue de chercher dans les deux.

**LES PAGES SONT RECONSTRUITES, PUIS VÉRIFIÉES.** `corpus/text/` recolle les
pages avec `\\n` : les frontières sont perdues, et `chunks.page` ne peut pas en
être déduit. On ré-extrait donc page par page sous le `pypdf` épinglé par `D19`,
et on exige que le RECOLLAGE redonne exactement le fichier qui fait foi. Si
l'égalité tient, la pagination est un raffinement du même texte ; sinon
l'ingestion s'arrête, parce qu'une pagination approximative est pire qu'aucune.

    python vectordb/ingest.py --dry-run    # ce qu'il ferait, sans reseau ni base
    python vectordb/ingest.py              # ingere
    python vectordb/ingest.py --paper gao  # un seul papier (sous-chaine du nom)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEXTDIR = REPO / "corpus" / "text"
PDFDIR = REPO / "corpus" / "pdf"
MANIFEST = TEXTDIR / "MANIFEST.json"
CENSUS = REPO / "corpus" / "acquisition.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vector_db import Chunk, DuplicatePaper, Paper, VectorDB, VectorDBError  # noqa: E402

MODE = "default"

# Le decoupage. 1 500 caracteres font environ 375 jetons : loin des 8 191 que
# `text-embedding-3-small` accepte, et assez court pour qu'un morceau porte une
# seule idee. Le recouvrement evite qu'une phrase coupee en deux disparaisse des
# deux cotes.
CHUNK_CHARS = 1500
OVERLAP_CHARS = 200
MIN_CHUNK_CHARS = 120

# Detection de section : des EN-TETES, pas du jugement. Un motif qui ne
# correspond a rien laisse la section a `other` — c'est la reponse honnete, et
# `other` qui gonfle est un signal a lire, pas un defaut a masquer.
# `\s*` et non `\s+` apres la numerotation : l'extraction ecrase parfois les
# espaces (`ByTORBENG.ANDERSEN`), et exiger un espace ferait rater `I.Data`.
_NUM = r"^\s*(?:[IVXivx]+|\d+)?\s*[.)]?\s*"
SECTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("intro", re.compile(_NUM + r"introduction\b", re.I)),
    ("methodology", re.compile(
        _NUM + r"(?:data\b|methodolog|the\s*model\b|empirical\s*"
        r"(?:design|strateg|method|framework)|estimation\b|research\s*design\b|"
        r"data\s*and\s*method)", re.I)),
    ("results", re.compile(
        _NUM + r"(?:empirical\s*)?(?:results|findings|main\s*results)\b", re.I)),
    ("conclusion", re.compile(
        _NUM + r"(?:conclusion|concluding\s*remarks|summary\s*and\s*conclusion)\b",
        re.I)),
]

# En deçà de ce nombre de sections DISTINCTES trouvées, la structure du papier
# n'a pas été reconnue et tous ses morceaux restent `other`.
#
# Étiqueter à moitié serait pire que ne pas étiqueter : au premier essai,
# `boyarchenko` ne rendait que DEUX en-têtes sur 98 pages, et les 67 pages
# d'annexes qui suivaient « VI. Conclusion » héritaient toutes de `conclusion`
# — 101 morceaux sur 171. Un champ faux à ce point ne se distingue pas d'un
# champ juste une fois en base.
MIN_SECTIONS_DETECTED = 2

# Compteur des octets NUL retirés. Une liste plutôt qu'un entier : il est lu et
# incrémenté depuis `split_pages`, et un compte qui n'est pas affiché est un
# nettoyage silencieux.
NUL_COUNT = [0]

CITATION = re.compile(r"\*\*(?P<authors>[^*]+?)\s*\((?P<year>\d{4})\)\*\*"
                      r"(?:.*?[«]\s*(?P<title>.+?)\s*[»])?", re.S)


HARVEST = REPO / "corpus" / "harvest.json"
HARVEST_PDFDIR = REPO / "corpus" / "pdf" / "harvest"


@dataclass(slots=True)
class Source:
    """Un papier prêt à être ingéré : ses métadonnées et son texte paginé."""

    stem: str
    title: str
    authors: list[str]
    year: int | None
    pdf_url: str | None
    pages: list[str]
    # `D22` : `authoritative` si le texte vient de `corpus/text/`, `harvest`
    # s'il est lu du PDF à l'ingestion. Les deux cherchent ; seul le premier
    # peut servir à `F2`.
    text_source: str = "authoritative"


# ---------------------------------------------------------------------------
# Métadonnées — tirées du recensement, seule source qui couvre les 17
# ---------------------------------------------------------------------------

def census_by_stem() -> dict[str, dict]:
    """Le recensement, indexé par le nom de fichier du PDF."""
    out = {}
    for row in json.loads(CENSUS.read_text(encoding="utf-8")):
        if row.get("pdf"):
            out[Path(row["pdf"]).stem] = row
    return out


def parse_citation(citation: str) -> tuple[str, list[str], int | None]:
    """Titre, auteurs et année, depuis la citation Markdown d'`AMORCE.md`.

    Format observé : `**Gao, Han, Li & Zhou (2018)**, « Titre », *Revue* …`.
    Une citation qui ne s'y plie pas ne fait PAS échouer l'ingestion : elle rend
    un titre vide, que l'appelant remplace par le nom du fichier. Le recensement
    est un étalon qu'on ne retouche pas pour arranger un analyseur.
    """
    m = CITATION.search(citation or "")
    if not m:
        return "", [], None
    authors = [a.strip() for a in re.split(r",|&| et ", m.group("authors")) if a.strip()]
    year = int(m.group("year"))
    return (m.group("title") or "").strip(), authors, year


# ---------------------------------------------------------------------------
# Pagination — reconstruite, puis vérifiée contre ce qui fait foi
# ---------------------------------------------------------------------------

def paginate(stem: str) -> list[str]:
    """Les pages du papier, garanties recoller sur le texte qui fait foi.

    L'égalité est exigée caractère pour caractère. Elle n'est pas une
    précaution de principe : `pypdf` sous une autre version rend un autre texte
    (`D19`, `L19`), et une pagination calculée sur une extraction différente
    placerait les citations sur les mauvaises pages — une faute silencieuse, du
    genre que `L20` décrit.
    """
    authoritative = (TEXTDIR / f"{stem}.{MODE}.txt").read_text(encoding="utf-8")
    pdf = PDFDIR / f"{stem}.pdf"
    if not pdf.is_file():
        raise VectorDBError(
            f"PDF absent : {pdf.relative_to(REPO)} — le récupérer avec "
            "`python corpus/fetch_pdfs.py`. Le texte seul ne donne pas les pages."
        )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from pypdf import PdfReader

        pages = [(p.extract_text() or "") for p in PdfReader(str(pdf)).pages]

    if "\n".join(pages) != authoritative:
        raise VectorDBError(
            f"{stem} : le recollage des pages NE REDONNE PAS le texte qui fait "
            "foi. La pagination serait fausse, donc l'ingestion s'arrête. "
            "Vérifier `python corpus/extract_text.py --check` et la version de "
            "pypdf (D19 l'épingle à 6.14.2)."
        )
    return pages


# ---------------------------------------------------------------------------
# Découpage
# ---------------------------------------------------------------------------

def detect_section(line: str) -> str | None:
    """La section qu'annonce une ligne d'en-tête, ou `None`."""
    if len(line.strip()) > 90:  # une phrase, pas un titre
        return None
    for name, pattern in SECTION_PATTERNS:
        if pattern.match(line):
            return name
    return None


def split_pages(pages: list[str]) -> list[tuple[str, int, str]]:
    """Découpe en (contenu, page, section).

    La page retenue est celle où le morceau COMMENCE. Un morceau à cheval est
    inévitable ; le faire porter par sa page d'ouverture est arbitraire mais
    constant, ce qui suffit pour retrouver un passage.
    """
    out: list[tuple[str, int, str]] = []
    section = "other"
    vues: set[str] = set()
    apres_conclusion = False

    for page_no, raw in enumerate(pages, start=1):
        for line in raw.splitlines():
            if (found := detect_section(line)):
                section = found
                vues.add(found)
                apres_conclusion = False
        # Ce qui suit la conclusion est annexe, tableaux, references — pas la
        # conclusion. Sans cette bascule, un papier de 98 pages voyait ses
        # 67 dernieres etiquetees `conclusion`.
        if section == "conclusion" and apres_conclusion:
            section = "other"
        if section == "conclusion":
            apres_conclusion = True

        # PostgreSQL refuse l'octet NUL dans un champ texte, et `pypdf` en
        # produit : 10 sur les 17 papiers. Les retirer écarte le texte ingéré
        # de celui qui fait foi — écart assumé et compté, jamais silencieux.
        # `F2` continue de vérifier les citations contre `corpus/text/`, qui
        # n'est pas touché ; c'est la COPIE de recherche qui est nettoyée.
        nuls = raw.count("\x00")
        if nuls:
            NUL_COUNT[0] += nuls
            raw = raw.replace("\x00", "")

        text = re.sub(r"[ \t]+", " ", raw)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if len(text) < MIN_CHUNK_CHARS:
            continue

        start = 0
        while start < len(text):
            end = min(start + CHUNK_CHARS, len(text))
            if end < len(text):
                # Couper sur une frontiere de phrase ou de paragraphe plutot
                # qu'au milieu d'un mot : un morceau tronque brouille autant
                # l'embedding que la lecture humaine.
                window = text[start:end]
                cut = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"))
                if cut > CHUNK_CHARS // 2:
                    end = start + cut + 1
            piece = text[start:end].strip()
            if len(piece) >= MIN_CHUNK_CHARS:
                out.append((piece, page_no, section))
            if end >= len(text):
                break
            start = max(end - OVERLAP_CHARS, start + 1)

    if len(vues) < MIN_SECTIONS_DETECTED:
        # Structure non reconnue : on ne devine pas, on le dit par `other`.
        return [(c, p, "other") for c, p, _ in out]
    return out


# ---------------------------------------------------------------------------
# Assemblage
# ---------------------------------------------------------------------------

def sources(filtre: str | None = None) -> list[Source]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    stems = sorted({Path(e["path"]).name.rsplit(".", 2)[0] for e in manifest["files"]})
    census = census_by_stem()

    out = []
    for stem in stems:
        if filtre and filtre.lower() not in stem.lower():
            continue
        row = census.get(stem, {})
        title, authors, year = parse_citation(row.get("citation", ""))
        out.append(Source(
            stem=stem,
            title=title or stem.replace("-", " "),
            authors=authors,
            year=year,
            pdf_url=row.get("source_url"),
            pages=paginate(stem),
        ))
    return out


def harvest_sources(filtre: str | None = None) -> list[Source]:
    """Les papiers moissonnés — texte lu du PDF, `text_source = harvest`.

    Aucune vérification de recollage ici, et c'est le point : il n'y a AUCUN
    texte versionné contre quoi vérifier. C'est exactement ce que `D22`
    inscrit dans la colonne plutôt que de le laisser à la prose — un morceau
    `harvest` est indiscernable d'un morceau `D18` une fois en base.
    """
    if not HARVEST.is_file():
        raise VectorDBError("corpus/harvest.json absent — lancer le moissonneur")
    works = json.loads(HARVEST.read_text(encoding="utf-8"))["works"]
    par_pdf = {Path(w["pdf"]).name: w for w in works if w.get("pdf")}

    out = []
    for pdf in sorted(HARVEST_PDFDIR.glob("*.pdf")):
        if filtre and filtre.lower() not in pdf.stem.lower():
            continue
        w = par_pdf.get(pdf.name)
        if w is None:
            # Un PDF sur le disque que la moisson ne connaît pas : on ne devine
            # pas ses métadonnées, on le saute en le disant.
            print(f"  ignoré, absent de harvest.json : {pdf.name}")
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from pypdf import PdfReader

            try:
                pages = [(p.extract_text() or "") for p in PdfReader(str(pdf)).pages]
            except Exception as e:  # noqa: BLE001 — un PDF cassé n'arrête pas les 122 autres
                print(f"  ignoré, illisible ({type(e).__name__}) : {pdf.name}")
                continue
        out.append(Source(
            stem=pdf.stem,
            title=w.get("title") or pdf.stem.replace("-", " "),
            authors=list(w.get("authors") or []),
            year=w.get("year"),
            pdf_url=w.get("source_url"),
            pages=pages,
            text_source="harvest",
        ))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Ingestion du corpus — D18 vers vectordb")
    ap.add_argument("--dry-run", action="store_true",
                    help="montre ce qui serait inséré, sans base ni réseau")
    ap.add_argument("--paper", default=None, help="n'ingérer qu'un papier")
    ap.add_argument("--harvest", action="store_true",
                    help="les papiers moissonnés (texte NON versionné, D22) "
                         "au lieu des 17 d'AMORCE")
    a = ap.parse_args(argv)

    try:
        papers = harvest_sources(a.paper) if a.harvest else sources(a.paper)
    except VectorDBError as e:
        print(f"ARRÊT : {e}")
        return 1
    if not papers:
        print("aucun papier ne correspond")
        return 1

    if a.harvest:
        print(f"{len(papers)} papier(s) MOISSONNÉ(S) — texte lu du PDF à "
              "l'instant, `text_source = harvest` (D22).")
        print("Ce texte NE FAIT PAS FOI : aucune pagination n'est vérifiée, car")
        print("il n'existe aucun texte de référence contre quoi la vérifier.")
        print("`F2` ne doit pas s'en servir, et rien ici n'est reproductible")
        print("depuis le dépôt — `corpus/pdf/` est ignoré par git.\n")
    else:
        print(f"{len(papers)} papier(s), texte du mode `{MODE}`, "
              "pagination vérifiée\n")
    plan = [(s, split_pages(s.pages)) for s in papers]

    print(f"  {'papier':<46} {'pages':>5} {'morceaux':>9}  sections")
    for s, chunks in plan:
        sections = {}
        for _, _, sec in chunks:
            sections[sec] = sections.get(sec, 0) + 1
        resume = " ".join(f"{k}:{v}" for k, v in sorted(sections.items()))
        print(f"  {s.stem[:46]:<46} {len(s.pages):>5} {len(chunks):>9}  {resume}")

    total = sum(len(c) for _, c in plan)
    muets = [s.stem for s, c in plan if {sec for _, _, sec in c} == {"other"}]
    part_other = sum(1 for _, c in plan for _, _, sec in c if sec == "other") / max(total, 1)
    print(f"\n  {total} morceaux au total, embeddings laissés à NULL")
    print(f"  structure NON reconnue sur {len(muets)} papier(s) sur {len(plan)}"
          f" — tout y reste `other`")
    print(f"  part de `other` sur l'ensemble : {part_other:.0%}")
    if muets:
        print(f"    {', '.join(m[:34] for m in muets)}")
    print("  La section est une heuristique d'en-têtes, pas un jugement : elle se")
    print("  lit comme un indice, jamais comme un fait sur le papier.")
    if NUL_COUNT[0]:
        print(f"  {NUL_COUNT[0]} octet(s) NUL retiré(s) — PostgreSQL les refuse."
              " `corpus/text/` n'est pas touché.")

    if a.dry_run:
        print("\n--dry-run : rien n'a été écrit. Exemple du premier morceau :\n")
        contenu, page, sec = plan[0][1][0]
        print(f"  [{sec}] page {page}")
        print("  " + contenu[:300].replace("\n", "\n  "))
        return 0

    print("\nInsertion…", flush=True)
    inserted = skipped = 0
    with VectorDB.from_env() as db:
        for s, chunks in plan:
            try:
                paper_id = db.insert_paper(Paper(
                    title=s.title, authors=s.authors, year=s.year,
                    pdf_url=s.pdf_url, text_source=s.text_source,
                ))
            except DuplicatePaper as e:
                print(f"  {s.stem[:46]:<46} déjà en base ({e.paper_id[:8]}…)")
                skipped += 1
                continue
            n = db.insert_chunks(paper_id, [
                Chunk(content=c, ordinal=i, section=sec, page=page)
                for i, (c, page, sec) in enumerate(chunks)
            ])
            print(f"  {s.stem[:46]:<46} {n:>4} morceaux")
            inserted += n

    print(f"\n{inserted} morceaux insérés, {skipped} papier(s) déjà présent(s)")
    print("La recherche PLEIN TEXTE fonctionne dès maintenant (le tsvector est")
    print("généré). La vectorielle attend des embeddings.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
