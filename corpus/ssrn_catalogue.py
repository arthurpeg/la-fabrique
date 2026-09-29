"""Le catalogue SSRN par actif — `D32`.

Verse dans la base les depots SSRN sur le petrole, l'or, les crypto-actifs et
les devises, avec leur seul RESUME (`text_source = 'abstract'`, `D31`), jusqu'a
un budget de taille ecrit dans `D32`. Il ne touche jamais a ssrn.com (`D30`) :
tout vient de Crossref, ou SSRN depose lui-meme ses notices.

**Ce n'est pas le moissonneur.** Un travail de `harvest.json` est destine a etre
sonde pour son PDF, trie, fiche. Ces papiers-ci ne le sont pas : ils servent la
RECHERCHE dans la base. Pour ficher l'un d'eux, il faut l'amener au moissonneur
par un axe (`D21`).

**Les requetes et le perimetre sont ecrits ici, avant d'etre lances** (`D32`).
Les changer apres un passage est une decision ecrite.

    python corpus/ssrn_catalogue.py --collect   # interroge Crossref, AUCUNE ecriture en base
    python corpus/ssrn_catalogue.py --ingest    # collecte PUIS verse, jusqu'au budget
    python corpus/ssrn_catalogue.py --status    # la base et le manifeste, sans Crossref
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "corpus" / "ssrn_catalogue.jsonl"
sys.path.insert(0, str(REPO / "corpus"))
sys.path.insert(0, str(REPO / "vectordb"))

from harvest import MAILTO, SSRN_PREFIX, UA, clean_abstract  # noqa: E402

CROSSREF = "https://api.crossref.org/works"

# Les requetes de `D32`, par actif. Un mot ou deux : une requete de plusieurs
# mots rend N'IMPORTE LEQUEL d'entre eux chez Crossref (`D31` § Journal).
QUERIES: list[tuple[str, str]] = [
    ("crypto", "bitcoin"),
    ("crypto", "cryptocurrency"),
    ("crypto", "blockchain"),
    ("crypto", "ethereum"),
    ("crypto", "stablecoin"),
    ("oil", "crude oil"),
    ("oil", "oil price"),
    ("oil", "oil"),
    ("oil", "petroleum"),
    ("gold", "gold"),
    ("gold", "precious metals"),
    ("fx", "exchange rate"),
    ("fx", "foreign exchange"),
    ("fx", "currency"),
    ("fx", "carry trade"),
]

# Le perimetre de `D32` : un mot de l'actif dans le titre ou le resume. Il
# DEFINIT la population demandee ; il ne juge pas l'implementabilite (`F50`).
SCOPE: dict[str, str] = {
    "oil": r"\boil\b|crude|petrol|brent|\bwti\b",
    "gold": r"\bgold\b|precious metal",
    "crypto": r"bitcoin|crypto|blockchain|ethereum|stablecoin|\bdefi\b",
    "fx": r"exchange rate|currenc|forex|foreign exchange|\bfx\b",
}

PAGE_ROWS = 1000
# 10 au premier passage ; 25 depuis le § Journal de `D32` (2026-09-28) : deux
# requetes de devises avaient ete coupees par ce plafond et non par le perimetre.
MAX_PAGES = 25
MIN_SCOPE_SHARE = 0.10  # une page sous 10 % dans le perimetre arrete la requete
PAUSE = 2.0

# `D32` : 80 % du plan Supabase — 500 Mo gratuits jusqu'au 2026-09-28, 8 Go depuis
# le 2026-09-29 (§ Journal). Meme budget que `vectordb/ingest.py`.
BUDGET_BYTES = 6_400_000_000
BYTES_PER_PAPER = 13_000  # mesure du 2026-09-28, vecteur et index compris


def get_json(url: str, tries: int = 8) -> dict:
    """Crossref, avec reprise sur `429`/`5xx` — attendre n'est pas contourner."""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == tries - 1:
                raise
            wait = float(e.headers.get("Retry-After") or 0) or min(120, 5 * 2**attempt)
            print(f"    Crossref {e.code}, pause {wait:.0f} s", flush=True)
            time.sleep(wait)
        except (urllib.error.URLError, TimeoutError):
            if attempt == tries - 1:
                raise
            time.sleep(min(120, 5 * 2**attempt))
    raise RuntimeError("inatteignable")


def assets_of(title: str, abstract: str) -> list[str]:
    text = f"{title} {abstract}"
    return [a for a, rx in SCOPE.items() if re.search(rx, text, re.I)]


def load_manifest() -> dict[str, dict]:
    if not MANIFEST.is_file():
        return {}
    out = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["doi"]] = row
    return out


def collect() -> list[dict]:
    """Interroge Crossref pour chaque requete de `D32`. Rend les depots NOUVEAUX,
    dans le perimetre et pourvus d'un resume, dedoublonnes par DOI."""
    known = load_manifest()
    seen: dict[str, dict] = {}
    today = str(date.today())
    # L'actif de la requete n'est qu'une etiquette de lecture : le perimetre
    # est juge sur TOUS les actifs, un papier « oil » trouve par « currency »
    # compte pour les deux.
    for _asset, query in QUERIES:
        cursor, kept_q = "*", 0
        for page in range(1, MAX_PAGES + 1):
            params = {"filter": f"prefix:{SSRN_PREFIX}", "query.bibliographic": query,
                      "rows": PAGE_ROWS, "cursor": cursor,
                      "select": "DOI,title,author,issued,abstract"}
            if MAILTO:
                params["mailto"] = MAILTO
            msg = get_json(f"{CROSSREF}?{urllib.parse.urlencode(params)}")["message"]
            items, cursor = msg.get("items") or [], msg.get("next-cursor")
            if not items:
                break
            in_scope = 0
            for it in items:
                doi = (it.get("DOI") or "").lower()
                title = (it.get("title") or [""])[0]
                abstract = clean_abstract(it.get("abstract")) or ""
                tags = assets_of(title, abstract)
                if not tags:
                    continue
                in_scope += 1
                if not abstract or not title.strip() or doi in known or doi in seen:
                    continue
                authors = [" ".join(filter(None, (a.get("given"), a.get("family"))))
                           for a in (it.get("author") or [])][:8]
                year = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
                seen[doi] = {"doi": doi, "title": title, "authors": [a for a in authors if a],
                             "year": year, "assets": tags, "query": query, "date": today,
                             "abstract": abstract}
                kept_q += 1
            share = in_scope / len(items)
            print(f"  {query:18s} page {page:>2} : {len(items):>4} notices, "
                  f"perimetre {share:4.0%}, {kept_q:>5} nouvelles retenues "
                  f"(total {msg.get('total-results')})", flush=True)
            time.sleep(PAUSE)
            if share < MIN_SCOPE_SHARE or len(items) < PAGE_ROWS or not cursor:
                break
    return list(seen.values())


def db_size(cur) -> int:
    cur.execute("select pg_database_size(current_database()) as b")
    return int(cur.fetchone()["b"])


def ingest(rows: list[dict]) -> int:
    from vector_db import VectorDB

    with VectorDB.from_env() as db:
        with db.conn.cursor() as cur:
            size = db_size(cur)
        cur_null = 0
        with db.conn.cursor() as cur:
            cur.execute("select count(*) as n from chunks where embedding is null")
            cur_null = int(cur.fetchone()["n"])
        # Les morceaux deja verses sans vecteur grossiront encore : on les compte.
        room = BUDGET_BYTES - size - cur_null * (BYTES_PER_PAPER // 2)
        allowed = max(0, room // BYTES_PER_PAPER)
        print(f"\nbase : {size / 1e6:.0f} Mo ; budget {BUDGET_BYTES / 1e6:.0f} Mo "
              f"(D32) ; place pour ~{allowed} papier(s)")
        if len(rows) > allowed:
            print(f"  {len(rows)} candidats, {allowed} verses : le budget tranche")
            rows = rows[:allowed]

        inserted, kept = 0, []
        for i in range(0, len(rows), 200):
            batch = rows[i:i + 200]
            with db.conn.transaction(), db.conn.cursor() as cur:
                ids = []
                for r in batch:
                    ident = r["doi"].rsplit(".", 1)[-1]
                    cur.execute(
                        "insert into papers (title, authors, year, doi, pdf_url, abstract, "
                        "text_source) values (%s, %s, %s, %s, %s, %s, 'abstract') "
                        "on conflict do nothing returning id",
                        (r["title"], r["authors"], r["year"], r["doi"],
                         f"https://papers.ssrn.com/sol3/papers.cfm?abstract_id={ident}",
                         r["abstract"]))
                    got = cur.fetchone()
                    if got:
                        ids.append((got["id"], r))
                cur.executemany(
                    "insert into chunks (paper_id, content, section, ordinal) "
                    "values (%s, %s, 'other', 0)",
                    [(pid, r["abstract"]) for pid, r in ids])
            inserted += len(ids)
            kept += [r for _, r in ids]
            print(f"  {min(i + 200, len(rows)):>6}/{len(rows)} examines, {inserted} verses",
                  flush=True)
            # Le manifeste s'ecrit APRES chaque lot valide : une reprise ne
            # reverse rien, et rien n'y figure qui ne soit en base.
            with MANIFEST.open("a", encoding="utf-8") as fh:
                for _, r in ids:
                    fh.write(json.dumps({k: v for k, v in r.items() if k != "abstract"},
                                        ensure_ascii=False) + "\n")
        with db.conn.cursor() as cur:
            print(f"\n{inserted} papier(s) verse(s) ; base {db_size(cur) / 1e6:.0f} Mo "
                  "avant embeddings")
    print("Embeddings a NULL : `python vectordb/embed.py` les calcule.")
    return inserted


def status() -> int:
    from vector_db import VectorDB

    man = load_manifest()
    by_asset: dict[str, int] = {}
    for r in man.values():
        for a in r["assets"]:
            by_asset[a] = by_asset.get(a, 0) + 1
    print(f"manifeste : {len(man)} depot(s) — {by_asset}")
    with VectorDB.from_env() as db, db.conn.cursor() as cur:
        size = db_size(cur)
        cur.execute("select text_source, count(*) as n from papers group by 1")
        print(f"base : {size / 1e6:.0f} Mo sur un budget de {BUDGET_BYTES / 1e6:.0f} Mo (D32)")
        for r in cur.fetchall():
            print(f"  {r['text_source']:14s} {r['n']:>6}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le catalogue SSRN par actif — D32")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--ingest", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)
    if a.status:
        return status()
    if a.collect or a.ingest:
        rows = collect()
        by: dict[str, int] = {}
        for r in rows:
            for t in r["assets"]:
                by[t] = by.get(t, 0) + 1
        print(f"\n{len(rows)} depot(s) nouveaux, dans le perimetre, avec resume — {by}")
        if a.ingest:
            ingest(rows)
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
