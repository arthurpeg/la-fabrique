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
LARGEUR = 60  # morceaux demandés par voisin voulu : de quoi en regrouper assez
PLANCHER = 600  # au moins autant de morceaux tirés, comme le banc d'essai (D48)
TOP = 3  # un papier vaut la moyenne de ses trois meilleurs morceaux (D48)


def norm_titre(t: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", " ", t or "").lower().strip()


def meme_papier(a: str, b: str) -> bool:
    """Deux titres du même papier : une version de travail, une coquille, une
    ponctuation. Jaccard des mots d'au moins trois lettres, au-delà de 0,85 :
    « Intraday time-series momentum: Evidence from China » et « Intraday time
    series momentum: Global evidence » restent DEUX papiers (D52)."""
    ma = {m for m in norm_titre(a).split() if len(m) >= 3}
    mb = {m for m in norm_titre(b).split() if len(m) >= 3}
    return bool(ma and mb) and len(ma & mb) / len(ma | mb) >= 0.85


def hypotheses_par_fiche() -> dict[str, str]:
    """Les fiches qui ont déjà leur hypothèse : le lot figé, puis chaque H*.md par
    la fiche qu'il DÉCLARE (`**fiche :** `<id>``, `D40`) ou dont il cite le
    chemin (`corpus/fiches…/<id>.json`, avant `D40`). Jamais par une recherche de
    nom dans le texte : `lucca-moench-2015-…` est contenu dans
    `synthese-dossier-lucca-moench-2015-…` (D52, défaut 8)."""
    out = {}
    lot = REPO / "hypotheses" / "LOT-09.json"
    if lot.is_file():
        for e in json.loads(lot.read_text(encoding="utf-8"))["fiches"]:
            if e.get("ref"):
                out[e["fiche_id"]] = e["ref"]
    declaree = re.compile(r"\*\*fiche :\*\*\s*`([A-Za-z0-9-]+)`")
    chemin = re.compile(r"corpus/fiches(?:_harvest|_synthese)?/([A-Za-z0-9-]+)\.json")
    for h in sorted((REPO / "hypotheses").glob("H*.md")):
        texte = h.read_text(encoding="utf-8")
        for fid in declaree.findall(texte) + chemin.findall(texte):
            out.setdefault(fid, h.name.split("-")[0])
    return out


def vecteur(texte: str) -> str:
    from fastembed import TextEmbedding  # noqa: PLC0415
    from vector_db import to_pgvector  # noqa: PLC0415

    v = next(iter(TextEmbedding(model_name=MODELE).embed([texte])))
    return to_pgvector([float(x) for x in v], len(v))


def imposer(api, paper_id: str, q: str, n_passages: int) -> dict | None:
    """Un papier donné, noté comme un voisin trouvé : moyenne de ses TOP meilleurs
    morceaux contre la graine, ses meilleurs passages."""
    import numpy as np  # noqa: PLC0415

    rows = api.appel("GET", f"/rest/v1/chunks?select=content,section,page,embedding"
                            f"&paper_id=eq.{paper_id}") or []
    meta = api.appel("GET", f"/rest/v1/papers?select=title&id=eq.{paper_id}") or []
    if not rows or not meta:
        return None
    g = np.array(json.loads(q))
    g = g / np.linalg.norm(g)
    notes = []
    for r in rows:
        e = np.array(json.loads(r["embedding"]))
        notes.append((float(e @ g / np.linalg.norm(e)), r))
    notes.sort(key=lambda x: -x[0])
    return {"paper_id": paper_id, "title": meta[0]["title"], "imposed": True,
            "similarity": round(sum(s for s, _ in notes[:TOP]) / TOP, 4),
            "passages": [{"section": r["section"], "page": r["page"], "similarity": round(s, 4),
                          "content": r["content"]} for s, r in notes[:n_passages]]}


def chercher(fiche_id: str, n_voisins: int, n_passages: int,
             avec: list[str] | None = None) -> dict:
    """`avec` : identifiants en base de papiers à joindre aux candidats même si la
    recherche ne les tire pas (les autres membres d'une famille). Ils passent par
    le même trieur que les autres : être imposé n'est pas être gardé."""
    from embed_api import Api  # noqa: PLC0415

    ff = fiche_files()
    if fiche_id not in ff:
        raise SystemExit(f"fiche inconnue : {fiche_id}")
    fiche = json.loads(ff[fiche_id].read_text(encoding="utf-8"))
    titre_graine = (fiche.get("source") or {}).get("title") or ""
    api = Api()
    q = vecteur(representation(fiche))
    morceaux = api.appel("POST", "/rest/v1/rpc/vector_search", {
        "query_embedding": q,
        "match_count": max(PLANCHER, n_voisins * LARGEUR)}) or []

    fiches_par_papier = {}
    lignes = api.appel("GET", "/rest/v1/fiches?select=fiche_id,paper_id&paper_id=not.is.null")
    for r in lignes or []:
        fiches_par_papier[r["paper_id"]] = r["fiche_id"]
    papier_graine = {p for p, f in fiches_par_papier.items() if f == fiche_id}
    testees = hypotheses_par_fiche()

    voisins: dict[str, dict] = {}
    for m in sorted(morceaux, key=lambda m: -m["similarity"]):
        # Le papier graine lui-même, par son identifiant ou sous un autre titre.
        if m["paper_id"] in papier_graine or meme_papier(m["title"], titre_graine):
            continue
        fid = fiches_par_papier.get(m["paper_id"])
        v = voisins.setdefault(m["paper_id"], {
            "paper_id": m["paper_id"], "title": m["title"], "fiche_id": fid,
            "hypothesis": testees.get(fid), "passages": [], "_s": []})
        v["_s"].append(m["similarity"])
        if len(v["passages"]) < n_passages:
            v["passages"].append({"section": m["section"], "page": m["page"],
                                  "similarity": round(m["similarity"], 4),
                                  "content": m["content"]})
    # D48 : la moyenne des trois meilleurs morceaux, un manquant comptant zéro.
    # Un papier qui ne ressemble à la graine que par une phrase recule ; le
    # banc d'essai (scripts/banc_voisins.py) fait passer le rappel à 10 de
    # 0,29 (meilleur morceau seul) à 0,37.
    for v in voisins.values():
        v["similarity"] = round(sum(v.pop("_s")[:TOP]) / TOP, 4)
    # Les papiers imposés (une famille de `corpus/familles.py`) que la recherche
    # n'a pas tirés : leurs morceaux sont lus en base et notés de la même façon.
    for pid in avec or []:
        if pid in voisins or pid in papier_graine:
            continue
        v = imposer(api, pid, q, n_passages)
        if v:
            v["fiche_id"] = fiches_par_papier.get(pid)
            v["hypothesis"] = testees.get(v["fiche_id"])
            voisins[pid] = v
    # Deux copies d'un même papier parmi les voisins : on garde la mieux notée.
    classes: list[dict] = []
    imposes = set(avec or [])
    for v in sorted(voisins.values(), key=lambda v: (v["paper_id"] not in imposes,
                                                     -v["similarity"])):
        if not any(meme_papier(v["title"], w["title"]) for w in classes):
            classes.append(v)
        if len(classes) == n_voisins + len(imposes):
            break
    classes.sort(key=lambda v: -v["similarity"])
    # L'année et les auteurs de chaque voisin, lus en base : sans eux, une synthèse
    # devrait les deviner (D53, essai du 2026-10-05).
    if classes:
        ids = ",".join(v["paper_id"] for v in classes)
        meta = {r["id"]: r for r in api.appel(
            "GET", f"/rest/v1/papers?select=id,year,authors&id=in.({ids})") or []}
        for v in classes:
            m = meta.get(v["paper_id"]) or {}
            v["year"], v["authors"] = m.get("year"), (m.get("authors") or [])[:6]
    return {"generated": datetime.now(UTC).isoformat(timespec="minutes"),
            "seed": {"fiche_id": fiche_id, "title": titre_graine,
                     "hypothesis": testees.get(fiche_id),
                     "representation": representation(fiche)},
            "model": MODELE, "neighbors": classes}


def ecrire(d: dict, nom: str | None = None) -> Path:
    DOSSIERS.mkdir(parents=True, exist_ok=True)
    fid = d["seed"]["fiche_id"]
    nom = nom or fid
    (DOSSIERS / f"{nom}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8")
    lignes = [f"# Dossier — {d['seed']['title']}", "",
              f"Papier graine : `{fid}`. Voisins trouvés par le sens dans toute la base "
              f"({d['model']}), le {d['generated']}.", ""]
    for i, v in enumerate(d["neighbors"], 1):
        etat = f"fiche `{v['fiche_id']}`" if v["fiche_id"] else "pas encore de fiche"
        if v.get("hypothesis"):
            etat += f", **déjà testée ({v['hypothesis']})**"
        lignes += [f"## {i}. {v['title']}", "", f"Similarité {v['similarity']:.3f} · {etat}", ""]
        for p in v["passages"]:
            lignes += [f"> *{p['section']}, similarité {p['similarity']:.3f}* — "
                       + " ".join(p["content"].split())[:1500], ""]
    chemin = DOSSIERS / f"{nom}.md"
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
        etat = (f"testé {v['hypothesis']}" if v.get("hypothesis")
                else "fiché" if v["fiche_id"] else "")
        etat = f"{etat:<9}"
        print(f"  {v['similarity']:.3f} {etat} {v['title'][:85]}")
    print(f"dossier : {chemin.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
