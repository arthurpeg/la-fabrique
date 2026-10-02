"""Le banc d'essai de la recherche des voisins (`D45`, `D48`).

La recherche des voisins se juge sur un étalon fixé **avant** de comparer les
méthodes : des paires de papiers qui décrivent le même mécanisme et doivent se
trouver l'un l'autre.

- **Les grappes de `D39`** : les fiches qu'une similarité fiche contre fiche
  réunit. Chaque membre doit retrouver les autres parmi ses voisins.
- **Les paires évidentes**, écrites à la main : deux papiers dont l'un est la
  réponse publiée à l'autre (Baltussen 2021 répond à Gao 2018).

L'étalon est biaisé : les grappes viennent de la même représentation des
fiches. Il dit si une méthode retrouve des parents connus, pas si elle trouve
les bons inconnus. La mesure se complète en lisant les dossiers.

Les candidats de chaque graine se tirent **une fois**, largement, de la base
(`vector_search`, deux requêtes : sans et avec le préfixe de requête de `bge`),
puis chaque méthode les classe hors ligne. Aucun rendement, aucun IC.

    python scripts/banc_voisins.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "vectordb"))

from code_signal import fiche_files  # noqa: E402
from grappes import representation, texte  # noqa: E402

GRAPPES = REPO / "scripts" / "out" / "grappes.json"
CACHE = REPO / "scripts" / "out" / "banc_voisins_candidats.json"
SORTIE = REPO / "scripts" / "out" / "banc_voisins.json"
LARGEUR = 600  # morceaux tirés par requête
K = 10  # le rang qui compte : un dossier montre dix voisins

# Les paires évidentes : (fiche graine, titre exact du papier attendu en base).
PAIRES = [
    ("baltussen-2021-hedging-demand-intraday-momentum", "Market intraday momentum"),
]


def etalon(api) -> dict[str, set[str]]:
    lien = {x["fiche_id"]: x["paper_id"] for x in
            api.appel("GET", "/rest/v1/fiches?select=fiche_id,paper_id&paper_id=not.is.null")}
    out: dict[str, set[str]] = {}
    for g in json.loads(GRAPPES.read_text(encoding="utf-8"))["groups"]:
        for m in g["members"]:
            out.setdefault(m, set()).update(lien[x] for x in g["members"] if x != m)
    for graine, titre in PAIRES:
        r = api.appel("GET", f"/rest/v1/papers?select=id&title=eq.{quote(titre)}")
        if r:
            out.setdefault(graine, set()).add(r[0]["id"])
    return out


def candidats(api, graines: list[str]) -> dict:
    """Pour chaque graine : ses requêtes et les morceaux tirés, mis en cache."""
    if CACHE.is_file():
        c = json.loads(CACHE.read_text(encoding="utf-8"))
        if set(graines) <= set(c):
            return c
    from embed import embed_query, load_model  # noqa: PLC0415
    from vector_db import to_pgvector  # noqa: PLC0415

    model = load_model()
    ff = fiche_files()
    out = {}
    for g in graines:
        fiche = json.loads(ff[g].read_text(encoding="utf-8"))
        req = {
            "fiche": representation(fiche),
            "mecanisme": " \n".join(x for x in ((fiche.get("source") or {}).get("title") or "",
                                                texte(fiche.get("claim"))) if x),
            "construction": texte(fiche.get("signal_construction")) or representation(fiche),
        }
        tirages = {}
        for nom, q in req.items():
            # Seules les variantes comparées : la fiche sans et avec préfixe,
            # le mécanisme et la construction avec.
            for prefixe in ((False, True) if nom == "fiche" else (True,)):
                v = (embed_query(model, q) if prefixe
                     else next(iter(model.embed([q]))).tolist())
                lot = api.appel("POST", "/rest/v1/rpc/vector_search",
                                {"query_embedding": to_pgvector(v, len(v)),
                                 "match_count": LARGEUR}) or []
                tirages[f"{nom}{'+prefixe' if prefixe else ''}"] = [
                    {"paper_id": m["paper_id"], "title": m["title"], "section": m["section"],
                     "s": round(m["similarity"], 5), "content": m["content"]} for m in lot]
        out[g] = {"title": (fiche.get("source") or {}).get("title"), "queries": req,
                  "draws": tirages}
        print(f"  tiré : {g}", flush=True)
    CACHE.write_text(json.dumps(out, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def classer(morceaux: list[dict], exclus: str, agreg: str) -> list[tuple[str, float]]:
    par: dict[str, list[float]] = {}
    for m in morceaux:
        if m["title"] == exclus:
            continue
        par.setdefault(m["paper_id"], []).append(m["s"])
    def note(xs):
        xs = sorted(xs, reverse=True)
        if agreg == "max":
            return xs[0]
        k = 5 if agreg == "top5" else 3
        top = xs[:k] + [0.0] * (k - len(xs[:k]))
        return sum(top) / k
    return sorted(((p, note(xs)) for p, xs in par.items()), key=lambda x: -x[1])


def fusion(classements: list[list[tuple[str, float]]]) -> list[tuple[str, float]]:
    """Fusion par rangs réciproques : un papier haut dans les deux requêtes gagne."""
    sc: dict[str, float] = {}
    for cl in classements:
        for rang, (p, _) in enumerate(cl):
            sc[p] = sc.get(p, 0.0) + 1.0 / (60 + rang)
    return sorted(sc.items(), key=lambda x: -x[1])


def rerang(reranker, requete: str, morceaux: list[dict], ordre: list[str],
           n: int = 40) -> list[tuple[str, float]]:
    """Le cross-encodeur relit (requête, passage) pour les n premiers papiers."""
    meilleurs: dict[str, list[dict]] = {}
    for m in sorted(morceaux, key=lambda m: -m["s"]):
        if m["paper_id"] in ordre[:n] and len(meilleurs.setdefault(m["paper_id"], [])) < 3:
            meilleurs[m["paper_id"]].append(m)
    paires = [(p, m["content"]) for p, ms in meilleurs.items() for m in ms]
    notes = list(reranker.rerank(requete, [c for _, c in paires]))
    par: dict[str, float] = {}
    for (p, _), s in zip(paires, notes, strict=True):
        par[p] = max(par.get(p, -1e9), float(s))
    return sorted(par.items(), key=lambda x: -x[1]) + [(p, -1e9) for p in ordre[n:]]


def par_centroides(graines_papiers: dict[str, str],
                   n: int = 300) -> dict[str, list[tuple[str, float]]]:
    """Le papier ENTIER de la graine contre chaque papier : centroïde contre
    centroïde, comme les arêtes de l'Atlas (`vectordb/graph.py`)."""
    from vector_db import VectorDB  # noqa: PLC0415

    out = {}
    with VectorDB.from_env() as db, db.conn.cursor() as c:
        c.execute("set statement_timeout = '15min'")
        c.execute("""create temp table cent as
                     select paper_id, avg(embedding)::vector(768) v from chunks
                     where embedding is not null group by paper_id""")
        for g, pid in graines_papiers.items():
            c.execute("""select b.paper_id, 1 - (a.v <=> b.v) s from cent a, cent b
                         where a.paper_id = %s and b.paper_id <> a.paper_id
                         order by a.v <=> b.v limit %s""", (pid, n))
            out[g] = [(str(r["paper_id"]), float(r["s"])) for r in c.fetchall()]
    return out


def main() -> int:
    from embed_api import Api  # noqa: PLC0415

    api = Api()
    gold = etalon(api)
    cand = candidats(api, sorted(gold))
    from fastembed.rerank.cross_encoder import TextCrossEncoder  # noqa: PLC0415

    reranker = TextCrossEncoder(model_name="BAAI/bge-reranker-base")
    lien = {x["fiche_id"]: x["paper_id"] for x in
            api.appel("GET", "/rest/v1/fiches?select=fiche_id,paper_id&paper_id=not.is.null")}
    cents = par_centroides({g: lien[g] for g in cand if g in lien})
    methodes = {}
    for g, c in cand.items():
        d, t = c["draws"], c["title"]
        base = classer(d["fiche"], t, "max")
        top3 = classer(d["fiche"], t, "top3")
        pref = classer(d["fiche+prefixe"], t, "top3")
        multi = fusion([classer(d["mecanisme+prefixe"], t, "top3"),
                        classer(d["construction+prefixe"], t, "top3")])
        pool = d["mecanisme+prefixe"] + d["construction+prefixe"]
        rr = rerang(reranker, c["queries"]["fiche"], pool, [p for p, _ in multi])
        rr1 = rerang(reranker, c["queries"]["fiche"], d["fiche"], [p for p, _ in top3])
        rrm = rerang(reranker, c["queries"]["mecanisme"], d["fiche"], [p for p, _ in top3])
        top5 = classer(d["fiche"], t, "top5")
        cen = cents.get(g, [])
        for nom, cl in (("0 actuelle (fiche, max)", base), ("1 fiche, top-3", top3),
                        ("2 fiche + préfixe, top-3", pref), ("3 mécanisme + construction", multi),
                        ("4 = 3 + reclassement", rr), ("5 fiche, top-5", top5),
                        ("6 = 1 + reclassement (fiche)", rr1),
                        ("7 = 1 + reclassement (mécanisme)", rrm),
                        ("8 centroïde du papier graine", cen),
                        ("9 fusion 1 + 8", fusion([top3, cen]) if cen else top3)):
            ordre = [p for p, _ in cl]
            rangs = [ordre.index(x) + 1 if x in ordre else None for x in gold[g]]
            methodes.setdefault(nom, []).append({"seed": g, "ranks": rangs})
    attendus = sum(len(v) for v in gold.values())
    print(f"\nÉtalon : {len(gold)} graines, {attendus} parents attendus\n")
    print(f"  {'méthode':<30} {'rappel@' + str(K):>9} {'rang médian':>12} {'jamais vus':>11}")
    resume = {}
    for nom, lignes in methodes.items():
        rangs = [r for x in lignes for r in x["ranks"]]
        trouves = [r for r in rangs if r is not None]
        rappel = sum(1 for r in trouves if r <= K) / len(rangs)
        med = sorted(trouves)[len(trouves) // 2] if trouves else None
        print(f"  {nom:<30} {rappel:>9.2f} {med if med else '—':>12} {rangs.count(None):>11}")
        resume[nom] = {"recall_at_k": round(rappel, 3), "median_rank": med,
                       "never_seen": rangs.count(None), "per_seed": lignes}
    SORTIE.write_text(json.dumps({"k": K, "methods": resume}, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    print(f"\nécrit : {SORTIE.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
