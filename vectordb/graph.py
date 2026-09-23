"""Extrait le graphe de similarité du corpus, pour une page partageable.

Un nœud par papier, une arête entre deux papiers dont les textes se
ressemblent. La similarité est celle des **centroïdes** — la moyenne des
vecteurs de chaque papier — ce qui donne une mesure stable et calculable en
une requête, là où comparer 11 813 morceaux deux à deux serait absurde.

**Ce qui sort d'ici est destiné à être PARTAGÉ.** Donc : titres, années,
auteurs, liens, et des extraits **courts**. Jamais le texte intégral des
morceaux, qui est celui de papiers sous droits. La base privée les garde ;
la page qu'on envoie à quelqu'un n'en montre que de quoi se repérer.

**Les arêtes sont choisies par RANG, pas par seuil.** Les similarités de
centroïdes sont toutes comprises entre ~0,90 et ~0,97 : la moyenne écrase les
écarts, et un seuil absolu relierait tout ou rien. On garde donc les `k` plus
proches voisins de chaque papier, ce qui produit un graphe lisible quelle que
soit l'échelle réelle des similarités.

    python vectordb/graph.py            # ecrit vectordb/graph_data.json
    python vectordb/graph.py --top 6    # plus d'aretes par papier
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vector_db import VectorDB  # noqa: E402

OUT = Path(__file__).resolve().parent / "graph_data.json"

TOP_EDGES = 4
EXCERPTS_PER_PAPER = 3
EXCERPT_CHARS = 320


def fetch(db: VectorDB, top: int) -> dict:
    with db.conn.cursor() as cur:
        cur.execute("""
            select p.id, p.title, p.year, p.authors, p.pdf_url, p.text_source,
                   count(ch.id)                                        as chunks,
                   count(ch.id) filter (where ch.embedding is not null) as vectorises
            from papers p
            left join chunks ch on ch.paper_id = p.id
            group by p.id
            order by p.title
        """)
        papers = cur.fetchall()

        # Un centroide par papier, puis toutes les paires. 136 papiers font
        # 9 180 paires : trivial pour Postgres, impensable sur les morceaux.
        cur.execute("""
            with cent as (
                select paper_id, avg(embedding)::vector(768) as v
                from chunks where embedding is not null
                group by paper_id
            )
            select a.paper_id, b.paper_id, 1 - (a.v <=> b.v) as sim
            from cent a join cent b on a.paper_id < b.paper_id
        """)
        paires = cur.fetchall()

        # Quelques extraits par papier, répartis sur les sections plutôt que
        # tous pris au début — le début d'un PDF est une page de garde.
        cur.execute("""
            select paper_id, page, section, left(content, %s) as excerpt
            from (
                select paper_id, page, section, content,
                       row_number() over (partition by paper_id, section
                                          order by ordinal) as rang
                from chunks
            ) t
            where rang = 2
            order by paper_id, page
        """, (EXCERPT_CHARS,))
        extraits = cur.fetchall()

    # Voisinage par RANG : les `top` plus proches de chaque papier, dans les
    # deux sens, puis dédoublonné. Une arête gardée par l'un des deux suffit.
    voisins: dict[str, list[tuple[str, float]]] = {}
    for row in paires:
        a, b, s = str(row["paper_id"]), str(row["b_paper_id"] if "b_paper_id" in row
                                            else list(row.values())[1]), row["sim"]
        voisins.setdefault(a, []).append((b, s))
        voisins.setdefault(b, []).append((a, s))

    gardees: set[tuple[str, str]] = set()
    poids: dict[tuple[str, str], float] = {}
    for a, liste in voisins.items():
        for b, s in sorted(liste, key=lambda x: -x[1])[:top]:
            cle = (a, b) if a < b else (b, a)
            gardees.add(cle)
            poids[cle] = s

    par_papier: dict[str, list[dict]] = {}
    for e in extraits:
        pid = str(e["paper_id"])
        if len(par_papier.setdefault(pid, [])) < EXCERPTS_PER_PAPER:
            par_papier[pid].append({
                "page": e["page"], "section": e["section"],
                "excerpt": (e["excerpt"] or "").strip(),
            })

    return {
        "papers": [{
            "id": str(p["id"]),
            "title": p["title"],
            "year": p["year"],
            "authors": (p["authors"] or [])[:4],
            "url": p["pdf_url"],
            "source": p["text_source"],
            "chunks": p["chunks"],
            "embedded": p["vectorises"],
            "excerpts": par_papier.get(str(p["id"]), []),
        } for p in papers],
        "edges": [{"a": a, "b": b, "w": round(poids[(a, b)], 4)}
                  for a, b in sorted(gardees)],
        "top": top,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Graphe de similarité du corpus")
    ap.add_argument("--top", type=int, default=TOP_EDGES,
                    help="arêtes gardées par papier (par rang, pas par seuil)")
    a = ap.parse_args(argv)

    with VectorDB.from_env() as db:
        data = fetch(db, a.top)

    sans_vecteur = [p for p in data["papers"] if p["embedded"] == 0]
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    print(f"  {len(data['papers'])} papiers, {len(data['edges'])} arêtes "
          f"(top {a.top} par papier)")
    par_source = {}
    for p in data["papers"]:
        par_source[p["source"]] = par_source.get(p["source"], 0) + 1
    print(f"  par origine : {par_source}")
    if sans_vecteur:
        print(f"  {len(sans_vecteur)} papier(s) SANS aucun vecteur — isolés dans "
              "le graphe, les embeddings ne sont pas finis")
    poids = [e["w"] for e in data["edges"]]
    if poids:
        print(f"  similarité des arêtes : {min(poids):.3f} à {max(poids):.3f}")
    print(f"  écrit : {OUT.name} ({OUT.stat().st_size / 1024:.0f} ko)")
    print("\n  Ce fichier est DESTINÉ AU PARTAGE : extraits courts seulement,")
    print("  jamais le texte intégral des morceaux.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
