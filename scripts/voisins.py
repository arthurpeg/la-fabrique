"""Les voisins d'un papier dans toute la base — le dossier d'une hypothèse (D45).

On part d'une fiche (le « papier graine »). Son mécanisme — titre, affirmation,
construction, univers, horizon, la même représentation que `grappes.py` — est
vectorisé localement (`bge-base-en-v1.5`, le modèle de la base), puis cherché
dans **toute** la base par la fonction `vector_search` (migration 001), à
travers l'API : papiers fichés ou non, quelle que soit leur origine. Les
morceaux trouvés sont regroupés par papier ; chaque voisin garde ses meilleurs
passages, mot pour mot, et sa similarité.

Le dossier (`corpus/dossiers/<fiche_id>.json` et `.md`) est ce que lira l'agent
qui écrit l'hypothèse : le papier graine et ce que les autres papiers en disent.
**Aucun rendement, aucun IC n'entre ici** ; seuls des textes de papiers.

    python scripts/voisins.py <fiche_id>                # 10 voisins, 2 passages chacun
    python scripts/voisins.py <fiche_id> --voisins 15 --passages 3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "vectordb"))

from code_signal import fiche_files  # noqa: E402
from grappes import MODELE, representation  # noqa: E402

DOSSIERS = REPO / "corpus" / "dossiers"
LARGEUR = 40  # morceaux demandés par voisin voulu : de quoi en regrouper assez


def norm_titre(t: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", " ", t or "").lower().strip()


def vecteur(texte: str) -> str:
    from fastembed import TextEmbedding  # noqa: PLC0415
    from vector_db import to_pgvector  # noqa: PLC0415

    v = next(iter(TextEmbedding(model_name=MODELE).embed([texte])))
    return to_pgvector([float(x) for x in v], len(v))


def chercher(fiche_id: str, n_voisins: int, n_passages: int) -> dict:
    from embed_api import Api  # noqa: PLC0415

    ff = fiche_files()
    if fiche_id not in ff:
        raise SystemExit(f"fiche inconnue : {fiche_id}")
    fiche = json.loads(ff[fiche_id].read_text(encoding="utf-8"))
    titre_graine = (fiche.get("source") or {}).get("title") or ""
    api = Api()
    morceaux = api.appel("POST", "/rest/v1/rpc/vector_search", {
        "query_embedding": vecteur(representation(fiche)),
        "match_count": n_voisins * LARGEUR}) or []

    fiches_par_papier = {}
    lignes = api.appel("GET", "/rest/v1/fiches?select=fiche_id,paper_id&paper_id=not.is.null")
    for r in lignes or []:
        fiches_par_papier[r["paper_id"]] = r["fiche_id"]

    voisins: dict[str, dict] = {}
    for m in morceaux:
        if norm_titre(m["title"]) == norm_titre(titre_graine):
            continue  # le papier graine lui-même
        v = voisins.setdefault(m["paper_id"], {
            "paper_id": m["paper_id"], "title": m["title"], "similarity": m["similarity"],
            "fiche_id": fiches_par_papier.get(m["paper_id"]), "passages": []})
        if len(v["passages"]) < n_passages:
            v["passages"].append({"section": m["section"], "page": m["page"],
                                  "similarity": round(m["similarity"], 4),
                                  "content": m["content"]})
    classes = sorted(voisins.values(), key=lambda v: -v["similarity"])[:n_voisins]
    for v in classes:
        v["similarity"] = round(v["similarity"], 4)
    return {"generated": datetime.now(UTC).isoformat(timespec="minutes"),
            "seed": {"fiche_id": fiche_id, "title": titre_graine,
                     "representation": representation(fiche)},
            "model": MODELE, "neighbors": classes}


def ecrire(d: dict) -> Path:
    DOSSIERS.mkdir(parents=True, exist_ok=True)
    fid = d["seed"]["fiche_id"]
    (DOSSIERS / f"{fid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8")
    lignes = [f"# Dossier — {d['seed']['title']}", "",
              f"Papier graine : `{fid}`. Voisins trouvés par le sens dans toute la base "
              f"({d['model']}), le {d['generated']}.", ""]
    for i, v in enumerate(d["neighbors"], 1):
        etat = f"fiche `{v['fiche_id']}`" if v["fiche_id"] else "pas encore de fiche"
        lignes += [f"## {i}. {v['title']}", "", f"Similarité {v['similarity']:.3f} · {etat}", ""]
        for p in v["passages"]:
            lignes += [f"> *{p['section']}, similarité {p['similarity']:.3f}* — "
                       + " ".join(p["content"].split())[:1500], ""]
    chemin = DOSSIERS / f"{fid}.md"
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    return chemin


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Les voisins d'un papier dans toute la base")
    ap.add_argument("fiche_id")
    ap.add_argument("--voisins", type=int, default=10)
    ap.add_argument("--passages", type=int, default=2)
    a = ap.parse_args(argv)
    d = chercher(a.fiche_id, a.voisins, a.passages)
    chemin = ecrire(d)
    print(f"{len(d['neighbors'])} voisin(s) pour {a.fiche_id} :")
    for v in d["neighbors"]:
        etat = "fiché" if v["fiche_id"] else "      "
        print(f"  {v['similarity']:.3f} {etat} {v['title'][:85]}")
    print(f"dossier : {chemin.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
