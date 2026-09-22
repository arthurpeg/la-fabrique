"""Le recensement des atteignables — `G4` de `D17`.

`D17` : *un papier est **atteignable** quand son texte est obtenu sans péage ni
démarche auprès d'un tiers. Le constat est daté et inscrit.* Ce script fait le
constat et l'inscrit dans `corpus/acquisition.json`.

**Le critère porte sur le PAPIER, pas sur le lien qu'`AMORCE.md` porte.** Le
recensement du 2026-09-21 l'a appris en marchant : l'entrée 3 (Heston) n'a qu'un
lien SSRN, et son PDF est sur le disque depuis le 2026-09-20 — obtenu d'arXiv.
S'en tenir aux liens d'`AMORCE.md` rendait 5 atteignables sur 20 ; chercher le
papier en rend 19. Le premier chiffre aurait été faux, et `G1` l'aurait rendu
invisible en ne fichant que ce que le lien rendait.

**Ce script ne décide pas qu'un papier est atteignable parce qu'une URL répond
`200`.** Une page de résumé répond `200` derrière un péage. Il n'est atteignable
que si le texte arrive : un corps `application/pdf` d'une taille plausible, dont
les cinq premiers octets sont `%PDF-`.

**Il ne contourne rien.** SSRN sert un contrôle anti-robot ; c'est inscrit
`refus_robot` et rien n'a été tenté pour passer outre. Un corpus obtenu en
forçant une porte est un corpus que la session suivante ne sait pas reproduire.

Les liens d'`AMORCE.md` sont extraits par la même mécanique que
`make_triage_input.py`. Les sources ALTERNATIVES sont déclarées dans `ALTERNATES`
ci-dessous, avec **comment elles ont été trouvées et quand** — `D09` appliqué à
une URL : une valeur qui vient du dehors porte sa provenance.

    python corpus/probe_acquisition.py --dry-run   # extrait et montre, sans réseau
    python corpus/probe_acquisition.py --probe     # sonde, n'ÉCRIT AUCUN FICHIER
    python corpus/probe_acquisition.py --write     # sonde et écrit acquisition.json

Code de sortie 1 si `AMORCE.md` n'a plus la forme attendue.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AMORCE = REPO / "corpus" / "AMORCE.md"
OUTPUT = REPO / "corpus" / "acquisition.json"

EXPECTED_ENTRIES = 20
ROW = re.compile(r"^\|\s*(\d+)\s*\|(.+)\|\s*$")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")

MIN_PDF_BYTES = 20_000
UA = "Mozilla/5.0 (compatible; la-fabrique/recensement; usage academique)"

# La liste CLOSE des raisons d'inatteignabilite. Une raison hors de cette liste
# est un trou dans le recensement, et `check_acquisition.py` la refuse.
REASONS = {
    "peage": "le texte est derriere un peage",
    "refus_robot": "le site sert un controle anti-robot, non contourne",
    "sans_source_libre": "aucune version libre trouvee au recensement",
}

# Les sources trouvees HORS d'AMORCE.md, avec leur provenance. Une URL ajoutee
# ici sans dire d'ou elle vient est une valeur inventee au sens de CLAUDE.md.
FOUND = "recherche web du 2026-09-21"
ALTERNATES: dict[int, list[dict]] = {
    # L'URL Monash retiree le 2026-09-22 : elle sert un AUTRE PAPIER (voir
    # ALERTES[1] et `L20`). Reste la prepublication SSRN, sondee pour que le
    # refus soit inscrit comme preuve plutot que suppose — meme forme que 6.
    1: [{"url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866",
         "via": "lien d'AMORCE.md",
         "note": "prepublication SSRN — refus robot"}],
    3: [{"url": "https://arxiv.org/pdf/1005.3535",
         "via": "deja sur disque depuis le 2026-09-20 (D17)",
         "note": "arXiv, non liste par AMORCE"}],
    4: [{"url": "https://alexandria.unisg.ch/bitstreams/a99aba00-f967-49b3-aceb-f544dc386e0b/download",
         "via": FOUND + ", via l'API DSpace d'Alexandria (HSG)",
         "note": "copie du SSRN 4824172 deposee par l'universite"}],
    5: [{"url": "https://alexandria.unisg.ch/bitstreams/3c2989c4-688d-4d78-8a71-f02690990d51/download",
         "via": FOUND, "note": "copie du SSRN 4729284 deposee par l'universite"}],
    6: [{"url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3553682",
         "via": FOUND, "note": "prepublication SSRN — refus robot"}],
    8: [{"url": "https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf",
         "via": FOUND, "note": "Staff Report 917, version de travail du papier RFS"}],
    9: [{"url": "https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/",
         "via": "lien d'AMORCE.md", "note": "billet de blog — HTML, pas de PDF"}],
    10: [{"url": "https://personal.lse.ac.uk/polk/research/TugOfWar.pdf",
          "via": FOUND, "note": "page personnelle d'un auteur (LSE)"}],
    14: [{"url": "https://statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/Corsi2009JFinEtrics_LMmodelRealizedVola.pdf",
          "via": FOUND, "note": "copie de cours (WU Vienne)"}],
    15: [{"url": "https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf",
          "via": FOUND, "note": "Staff Report 512, version de travail du papier JF"}],
    16: [{"url": "https://www.skidmore.edu/economics/documents/KurovWolfeGilbert-TheDisappearingPre-FOMC-Announce-Drift-200914.pdf",
          "via": FOUND,
          "note": "ATTENTION : auteurs Kurov, Wolfe & Gilbert — voir le champ `alerte`"}],
    17: [{"url": "https://public.econ.duke.edu/~boller/Published_Papers/aer_03.pdf",
          "via": FOUND, "note": "page personnelle d'un auteur (Duke)"}],
    18: [{"url": "https://www.nber.org/system/files/working_papers/w19325/w19325.pdf",
          "via": FOUND, "note": "NBER WP 19325, version de travail du papier JFE"}],
    19: [{"url": "https://www.nber.org/system/files/working_papers/w13249/w13249.pdf",
          "via": FOUND, "note": "NBER WP 13249, version de travail du papier RoF"}],
    20: [{"url": "https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf",
          "via": FOUND, "note": "page personnelle d'un auteur (NYU Stern)"}],
}

# Ce que le recensement a constate et qui n'est pas de son ressort.
ALERTES: dict[int, str] = {
    1: ("REPARE LE 2026-09-22, voir `L20`. Le recensement du 2026-09-21 declarait "
        "cette entree atteignable sur une URL du depot Monash "
        "(researchmgt.monash.edu/ws/files/519509174/494419119_oa.pdf). Cette URL "
        "sert un AUTRE PAPIER : Limkriangkrai, Chai & Zheng (2023), « Market "
        "intraday momentum: APAC evidence », Pacific-Basin Finance Journal "
        "80:102086 — 13 pages, autre revue, autres auteurs. Trouve par COLLISION "
        "D'EMPREINTE sha256 au passage 1 du moissonneur (D20), le meme fichier "
        "etant servi pour le travail OpenAlex « APAC evidence ». Les deux "
        "verifications automatiques evidentes echouent : le titre attendu est une "
        "SOUS-CHAINE du titre reel, et le papier APAC CITE Gao et al. (2018) des "
        "son resume. Aucune copie libre du vrai Gao 2018 n'a ete trouvee : "
        "OpenAlex oa_status=closed avec 0 emplacement libre, Semantic Scholar "
        "openAccessPdf=CLOSED, SSRN 403, ScienceDirect peage, et la seule copie "
        "libre indexee rend AccessDenied y compris dans un navigateur."),
    16: ("AMORCE.md cite « Kurov, Sancetta, Strasser & Wolfe (2021) » mais le papier "
         "de Finance Research Letters 40 (2021) que son lien ScienceDirect designe "
         "(S1544612320315956) est de Kurov, Wolfe & Gilbert. Le PDF obtenu est la "
         "version de travail de CE papier-la. La liste d'auteurs d'AMORCE parait "
         "melangee avec un autre papier de Kurov. NON CORRIGE ici : AMORCE.md est "
         "l'etalon du triage (D15), on ne le retouche pas en passant."),
    9: ("Texte libre mais en HTML, pas en PDF. D17 le rend atteignable a la lettre "
        "(ni peage ni demarche), mais F4 de D16 exige un `source.pdf` qui existe. "
        "Ce cas n'est pas tranche : il demande une decision ecrite avant fichage."),
}


def entries(path: Path = AMORCE) -> list[dict]:
    """Les 20 entrees notees, avec leurs liens. Section G (methode) exclue."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        n = int(m.group(1))
        if not (1 <= n <= EXPECTED_ENTRIES):
            continue
        body = m.group(2)
        rows.append({
            "entry": n,
            "citation": body.split("|")[0].strip(),
            "amorce_links": [{"label": a, "url": u} for a, u in LINK.findall(body)],
        })
    seen = [r["entry"] for r in rows]
    if seen != list(range(1, EXPECTED_ENTRIES + 1)):
        raise SystemExit(f"AMORCE.md : entrees {seen}, attendu 1..{EXPECTED_ENTRIES}")
    return rows


def candidates(row: dict) -> list[dict]:
    """Toutes les URL ou le texte pourrait vivre, d'AMORCE puis d'ALTERNATES."""
    out = []
    for lk in row["amorce_links"]:
        u = lk["url"]
        if u.lower().endswith(".pdf"):
            out.append({"url": u, "via": "lien d'AMORCE.md", "note": ""})
        m = re.match(r"https?://arxiv\.org/abs/(.+)$", u)
        if m:
            out.append({"url": f"https://arxiv.org/pdf/{m.group(1)}",
                        "via": "lien d'AMORCE.md (abs -> pdf)", "note": ""})
    out.extend(ALTERNATES.get(row["entry"], []))
    seen, uniq = set(), []
    for c in out:
        if c["url"] not in seen:
            seen.add(c["url"])
            uniq.append(c)
    return uniq


def fetch(url: str, timeout: int = 30) -> dict:
    """Une tentative, et ce qu'elle a REELLEMENT rendu."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(400_000)
            length = r.headers.get("Content-Length")
            return {
                "url": url,
                "http": r.status,
                "content_type": (r.headers.get("Content-Type") or "").split(";")[0].strip(),
                "bytes": int(length) if length else len(body),
                "is_pdf": body[:5] == b"%PDF-",
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "http": e.code, "error": f"HTTPError {e.code}"}
    except Exception as e:
        return {"url": url, "http": None, "error": f"{type(e).__name__}: {e}"}


def verdict(row: dict, attempts: list[dict]) -> dict:
    """Le statut, SA RAISON et la preuve — tires de ce qui a ete observe."""
    got = next((a for a in attempts
                if a.get("is_pdf") and a.get("bytes", 0) >= MIN_PDF_BYTES), None)
    if got:
        src = next(c for c in candidates(row) if c["url"] == got["url"])
        return {"status": "atteignable", "text_format": "pdf", "reason": None,
                "source_url": got["url"], "source_via": src["via"],
                "source_note": src["note"], "evidence": got}

    html = next((a for a in attempts if a.get("content_type") == "text/html"
                 and a.get("http") == 200), None)
    if html and row["entry"] == 9:
        src = next(c for c in candidates(row) if c["url"] == html["url"])
        return {"status": "atteignable", "text_format": "html", "reason": None,
                "source_url": html["url"], "source_via": src["via"],
                "source_note": src["note"], "evidence": html}

    if any(a.get("http") == 403 and "ssrn" in a["url"] for a in attempts):
        reason = "refus_robot"
    elif any("sciencedirect" in a["url"] or "aeaweb" in a["url"] for a in attempts):
        reason = "peage"
    else:
        reason = "sans_source_libre"
    return {"status": "inatteignable", "text_format": None, "reason": reason,
            "source_url": None, "source_via": None, "source_note": "",
            "evidence": {"attempts": attempts}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    rows = entries()
    if args.dry_run:
        for r in rows:
            print(f"{r['entry']:>2} | candidats={len(candidates(r))} | {r['citation'][:56]}")
        return 0
    if not (args.probe or args.write):
        ap.error("choisir --dry-run, --probe ou --write")

    out = []
    for r in rows:
        attempts = [fetch(c["url"]) for c in candidates(r)]
        v = verdict(r, attempts)
        rec = {**r, **v, "attempts": attempts, "checked": date.today().isoformat()}
        if r["entry"] in ALERTES:
            rec["alerte"] = ALERTES[r["entry"]]
        # Le nom du fichier local, SEUL consommateur `extract_fiche.py`. Il vient
        # de la table DECLAREE de `fetch_pdfs.py`, jamais d'un nom devine. Import
        # differe : `fetch_pdfs` importe ce module, et le faire en tete serait
        # circulaire. Le champ manquait a la sortie du recensement alors que le
        # fichier le portait — donc un `--write` le detruisait en silence et
        # cassait `extract_fiche --list`. Trouve le 2026-09-22 en reparant L20.
        if v["status"] == "atteignable" and v.get("text_format") == "pdf":
            from fetch_pdfs import NAMES
            if r["entry"] not in NAMES:
                raise SystemExit(f"entree {r['entry']} atteignable en PDF mais absente "
                                 "de fetch_pdfs.NAMES — nom a declarer")
            rec["pdf"] = f"corpus/pdf/{NAMES[r['entry']]}"
        out.append(rec)
        tag = v["status"] if v["status"] == "inatteignable" else f"atteignable/{v['text_format']}"
        print(f"{r['entry']:>2} | {tag:<18} | {(v['reason'] or v['source_url'] or '')[:74]}")

    ok = [r for r in out if r["status"] == "atteignable"]
    print(f"\natteignables : {len(ok)} / {EXPECTED_ENTRIES}"
          f"  (dont {sum(1 for r in ok if r['text_format'] == 'pdf')} en PDF)")
    for reason in REASONS:
        n = sum(1 for r in out if r["reason"] == reason)
        if n:
            print(f"  {reason:<18} : {n}  — {REASONS[reason]}")

    if args.write:
        OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
        print(f"ecrit : {OUTPUT.relative_to(REPO)}")
    else:
        print("(--probe : aucun fichier ecrit)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
