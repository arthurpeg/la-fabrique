"""La précision des voisins : combien décrivent le même mécanisme que la graine (`D53`).

`banc_voisins.py` (`D48`) mesure si des parents connus sont retrouvés. Il ne dit
pas combien des voisins proposés sont **hors sujet**, ce que l'opérateur veut
réduire. Ce banc le mesure.

1. `--tirer` : pour chaque graine, chaque variante de recherche classe ses
   candidats ; on réunit les dix premiers de chaque variante (la « mise en
   commun » des bancs de recherche d'information). Chaque candidat garde son
   titre et ses deux passages les plus proches.
2. `--consignes` : une consigne par graine, pour un juge isolé. Le juge lit
   le mécanisme de la graine et chaque candidat **mélangé, sans savoir quelle
   variante l'a proposé**, et répond `meme` ou `autre`, avec sa raison.
3. `--mesurer` : la précision à 10 de chaque variante, c'est-à-dire la part de
   ses dix premiers voisins jugés `meme`.

Les variantes et les graines sont fixées ici, avant le premier jugement. Aucun
rendement, aucun IC.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "vectordb"))

from code_signal import fiche_files  # noqa: E402
from grappes import representation, texte  # noqa: E402
from voisins import meme_papier  # noqa: E402

OUT = REPO / "scripts" / "out" / "banc_precision"
TIRAGE = OUT / "tirage.json"
K = 10
LARGEUR = 2000  # sans filtre SQL : un filtre de section fait abandonner l'index
GRAINES = [
    "lucca-moench-2015-pre-fomc-drift",
    "cryptocurrencies-and-momentum-W2930793690",
    "corsi-2009-har-realized-volatility",
    "baltussen-2021-hedging-demand-intraday-momentum",
    "gorton-2013-fundamentals-commodity-futures",
    "andersen-2003-micro-effects-macro-announcements",
]
VARIANTES = {
    "A": "actuelle : la fiche, toutes sections, moyenne des 3 meilleurs morceaux",
    "B": "la fiche, introductions et conclusions seulement",
    "C": "le mécanisme seul (titre, affirmation, construction), toutes sections",
    "D": "le mécanisme seul, introductions et conclusions seulement",
    "E": "A, puis les 30 premiers reclassés par cross-encodeur contre l'affirmation",
}


def mecanisme(fiche: dict) -> str:
    return " \n".join(x for x in ((fiche.get("source") or {}).get("title") or "",
                                  texte(fiche.get("claim")),
                                  texte(fiche.get("signal_construction"))) if x)


def tirer_requete(api, model, q: str) -> list[dict]:
    from vector_db import to_pgvector  # noqa: PLC0415

    v = next(iter(model.embed([q]))).tolist()
    return api.appel("POST", "/rest/v1/rpc/vector_search",
                     {"query_embedding": to_pgvector(v, len(v)), "match_count": LARGEUR}) or []


def sections(morceaux: list[dict], gardees: tuple[str, ...]) -> list[dict]:
    return [m for m in morceaux if m["section"] in gardees]


def classer(morceaux: list[dict], titre: str, exclus: set[str]) -> list[dict]:
    par: dict[str, dict] = {}
    for m in sorted(morceaux, key=lambda m: -m["similarity"]):
        if m["paper_id"] in exclus or meme_papier(m["title"], titre):
            continue
        p = par.setdefault(m["paper_id"], {"paper_id": m["paper_id"], "title": m["title"],
                                           "s": [], "passages": []})
        p["s"].append(m["similarity"])
        if len(p["passages"]) < 2:
            p["passages"].append({"section": m["section"], "content": m["content"]})
    for p in par.values():
        p["score"] = sum(p.pop("s")[:3]) / 3
    return sorted(par.values(), key=lambda p: -p["score"])


def do_tirer() -> int:
    from embed import load_model  # noqa: PLC0415
    from embed_api import Api  # noqa: PLC0415
    from fastembed.rerank.cross_encoder import TextCrossEncoder  # noqa: PLC0415

    api, model = Api(), load_model()
    rr = TextCrossEncoder(model_name="BAAI/bge-reranker-base")
    lien = {x["fiche_id"]: x["paper_id"] for x in
            api.appel("GET", "/rest/v1/fiches?select=fiche_id,paper_id&paper_id=not.is.null")}
    ff = fiche_files()
    tirage = {}
    for g in GRAINES:
        fiche = json.loads(ff[g].read_text(encoding="utf-8"))
        titre = (fiche.get("source") or {}).get("title") or ""
        exclus = {lien[g]} if g in lien else set()
        ic = ("intro", "conclusion")
        tf = tirer_requete(api, model, representation(fiche))
        tm = tirer_requete(api, model, mecanisme(fiche))
        cl = {
            "A": classer(tf, titre, exclus),
            "B": classer(sections(tf, ic), titre, exclus),
            "C": classer(tm, titre, exclus),
            "D": classer(sections(tm, ic), titre, exclus),
        }
        tete = cl["A"][:30]
        claim = texte(fiche.get("claim")) or mecanisme(fiche)
        notes = list(rr.rerank(claim, [" ".join(p["passages"][0]["content"].split())
                                       for p in tete]))
        cl["E"] = [p for _, p in sorted(zip(notes, tete, strict=True), key=lambda x: -x[0])]
        tops = {v: [p["paper_id"] for p in c[:K]] for v, c in cl.items()}
        candidats = {p["paper_id"]: p for c in cl.values() for p in c[:K]}
        tirage[g] = {"title": titre, "mechanism": mecanisme(fiche), "tops": tops,
                     "candidates": candidats}
        print(f"  {g} : {len(candidats)} candidats mis en commun", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    TIRAGE.write_text(json.dumps(tirage, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


CONSIGNE = """\
# Consigne de jugement — même mécanisme ou non (banc `D53`)

Tu es un juge isolé. Ta seule source est ce fichier. Ne lis aucun autre fichier,
aucune commande, aucun accès web.

## Le papier graine

**{titre}**

Son mécanisme, tel que sa fiche le décrit :

{mecanisme}

## Ta tâche

Pour **chaque** candidat ci-dessous, dans l'ordre, réponds :

- `meme` : il étudie **le même mécanisme économique** que la graine (la même
  cause qui produit le même type de mouvement de prix), même sur un autre
  marché, une autre période ou avec une autre méthode ;
- `autre` : il partage le thème, le marché ou la méthode, mais pas le
  mécanisme (« même sujet, autre effet »), ou il n'a pas de rapport.

Juge sur le titre et les passages, rien d'autre. En cas de doute réel, `autre`.

## Ce que tu rends

Écris avec l'outil Write, à `{chemin}`, un tableau JSON et rien d'autre :

```json
[{{"id": "c01", "label": "meme", "why": "<une phrase>"}}, ...]
```

Un objet par candidat, aucun omis. Réponds en une ligne : le chemin écrit et le
compte meme / autre.

## Les candidats

{candidats}
"""


def do_consignes() -> int:
    tirage = json.loads(TIRAGE.read_text(encoding="utf-8"))
    for g, t in tirage.items():
        ids = sorted(t["candidates"])
        random.Random(f"D53-{g}").shuffle(ids)  # l'ordre ne dit rien de la variante
        t["blind"] = {f"c{i:02d}": pid for i, pid in enumerate(ids, 1)}
        blocs = []
        for cid, pid in t["blind"].items():
            c = t["candidates"][pid]
            ps = "\n\n".join(f"> *{p['section']}* — " + " ".join(p["content"].split())[:900]
                             for p in c["passages"])
            blocs.append(f"### {cid} — {c['title']}\n\n{ps}\n")
        chemin = OUT / f"jugement-{g}.json"
        (OUT / f"consigne-{g}.md").write_text(CONSIGNE.format(
            titre=t["title"], mecanisme=t["mechanism"], chemin=chemin.as_posix(),
            candidats="\n".join(blocs)), encoding="utf-8")
        print(f"  {OUT.relative_to(REPO).as_posix()}/consigne-{g}.md  "
              f"({len(blocs)} candidats)")
    TIRAGE.write_text(json.dumps(tirage, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


def do_mesurer() -> int:
    tirage = json.loads(TIRAGE.read_text(encoding="utf-8"))
    par_var: dict[str, list[float]] = {v: [] for v in VARIANTES}
    print(f"  {'graine':<52}" + "".join(f"{v:>6}" for v in VARIANTES))
    for g, t in tirage.items():
        f = OUT / f"jugement-{g}.json"
        if not f.is_file():
            print(f"  {g:<52} pas encore jugé")
            continue
        lab = {t["blind"][x["id"]]: x["label"] for x in json.loads(f.read_text(encoding="utf-8"))}
        ligne = []
        for v in VARIANTES:
            top = t["tops"][v]
            p = sum(1 for pid in top if lab.get(pid) == "meme") / len(top)
            par_var[v].append(p)
            ligne.append(p)
        print(f"  {g[:52]:<52}" + "".join(f"{x:>6.1f}" for x in ligne))
    print(f"  {'MOYENNE (précision à 10)':<52}"
          + "".join(f"{sum(x) / len(x):>6.2f}" if x else "     —" for x in par_var.values()))
    for v, d in VARIANTES.items():
        print(f"    {v} : {d}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Précision des voisins (D53)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tirer", action="store_true")
    g.add_argument("--consignes", action="store_true")
    g.add_argument("--mesurer", action="store_true")
    a = ap.parse_args(argv)
    return do_tirer() if a.tirer else do_consignes() if a.consignes else do_mesurer()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
