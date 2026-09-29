"""La pertinence d'un papier pour la BASE DE RECHERCHE — `D33`.

Une regle MECANIQUE, ecrite avant d'etre appliquee : un papier est pertinent
s'il parle d'un MARCHE de notre univers (futures, indices, or, petrole,
devises, crypto, taux) ET d'un SIGNAL (rendements, volatilite, strategie,
anomalie, previsibilite, causalite, intraday...). Sur le titre et le debut du
texte — le resume, ou les premiers 5 000 caracteres d'un texte integral.

**Ce qu'elle n'est pas** : le trieur. `F50` interdit au moissonneur de juger
l'IMPLEMENTABILITE, qui a son juge (`D15`) et son etalon. Cette regle ne touche
ni `harvest.json`, ni le lot de la phase 09 : elle decide seulement ce que la
base de recherche garde. Un papier ecarte ici reste moissonne, et reste
triable.

    python corpus/relevance.py --dry-run   # ce que la purge retirerait, sans rien ecrire
    python corpus/relevance.py --prune     # retire de la base les non pertinents (D33)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REMOVED = REPO / "corpus" / "base_retraits.jsonl"

MARKET = re.compile(
    r"\bfutures?\b|\bstock (?:market|index|indices|returns?|prices?)\b|\bequity (?:index|market)"
    r"|\bs&p\b|\bs&p 500\b|\bnasdaq\b|\bdow jones\b|\be-mini\b|\bgold\b|\bcrude\b"
    r"|\boil (?:price|prices|market|futures)\b|\bcommodit|\bexchange rates?\b|\bcurrenc"
    r"|\bforex\b|\bforeign exchange\b|\bbitcoin\b|\bcrypto|\btreasury (?:bond|futures|yield)"
    r"|\bbond market|\bvix\b|\bindex returns\b|\bstock returns\b",
    re.I,
)
SIGNAL = re.compile(
    r"\breturns?\b|\bvolatil|\btrading\b|\bstrateg|\banomal|\bmomentum\b|\brevers"
    r"|\bpredictab|\bforecast|\barbitrage\b|\blead[- ]lag\b|\bspillover|\bcausalit"
    r"|\bintraday\b|\bhigh[- ]frequency\b|\bprice discovery\b|\bmispricing\b",
    re.I,
)

HEAD_CHARS = 5000
# Un resume est court : un marche et un signal suffisent. Un texte integral
# nomme en passant bien des choses : il en faut davantage, sur son debut.
THRESHOLDS = {"abstract": (1, 1), "full": (2, 3)}


def is_relevant(title: str, text: str, kind: str) -> tuple[bool, int, int]:
    """(pertinent ?, occurrences de marche, occurrences de signal)."""
    head = f"{title}\n{(text or '')[:HEAD_CHARS]}"
    m, s = len(MARKET.findall(head)), len(SIGNAL.findall(head))
    need_m, need_s = THRESHOLDS[kind]
    return (m >= need_m and s >= need_s), m, s


def scan(db) -> list[dict]:
    """Juge chaque papier `harvest` et `abstract` de la base. `authoritative`
    n'est jamais touche : c'est le corpus fiche."""
    out = []
    with db.conn.cursor() as cur:
        cur.execute("""
            select p.id, p.title, p.doi, p.text_source,
                   string_agg(c.content, ' ' order by c.ordinal)
                       filter (where c.ordinal < 5) as head
            from papers p left join chunks c on c.paper_id = p.id
            where p.text_source in ('harvest', 'abstract')
            group by p.id""")
        for r in cur.fetchall():
            kind = "abstract" if r["text_source"] == "abstract" else "full"
            ok, m, s = is_relevant(r["title"], r["head"] or "", kind)
            out.append({"id": str(r["id"]), "title": r["title"], "doi": r["doi"],
                        "text_source": r["text_source"], "relevant": ok,
                        "market_hits": m, "signal_hits": s})
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Pertinence pour la base de recherche — D33")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--prune", action="store_true")
    ap.add_argument("--show", type=int, default=15, help="titres ecartes a montrer")
    a = ap.parse_args(argv)
    if not (a.dry_run or a.prune):
        ap.print_help()
        return 1

    sys.path.insert(0, str(REPO / "vectordb"))
    from vector_db import VectorDB

    with VectorDB.from_env() as db:
        rows = scan(db)
        out = [r for r in rows if not r["relevant"]]
        for src in ("harvest", "abstract"):
            n = sum(1 for r in rows if r["text_source"] == src)
            k = sum(1 for r in out if r["text_source"] == src)
            print(f"  {src:9s} {n:>6} en base, {k:>6} non pertinents ({k / max(n, 1):.0%})")
        print("\nexemples ecartes :")
        for r in out[: a.show]:
            print(f"  [{r['text_source'][:4]}] m={r['market_hits']} s={r['signal_hits']}  "
                  f"{(r['title'] or '')[:80]}")
        if a.dry_run:
            print("\n--dry-run : rien n'a ete retire.")
            return 0

        # Le manifeste d'abord : ce qui est retire doit pouvoir etre reverse
        # (le PDF reste sur le disque, le resume se rend par son DOI).
        today = str(date.today())
        with REMOVED.open("a", encoding="utf-8") as fh:
            for r in out:
                fh.write(json.dumps({**{k: r[k] for k in ("doi", "title", "text_source",
                                                         "market_hits", "signal_hits")},
                                     "removed": today, "rule": "D33"},
                                    ensure_ascii=False) + "\n")
        ids = [r["id"] for r in out]
        with db.conn.transaction(), db.conn.cursor() as cur:
            for i in range(0, len(ids), 500):
                cur.execute("delete from papers where id = any(%s::uuid[])", (ids[i:i + 500],))
        print(f"\n{len(ids)} papier(s) retire(s) de la base (morceaux en cascade) ; "
              f"liste dans {REMOVED.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
