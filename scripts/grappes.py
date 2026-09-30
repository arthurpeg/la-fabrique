"""Les grappes de fiches : quels papiers parlent du même mécanisme — `D39`.

Une hypothèse de synthèse se construit à partir de **plusieurs** papiers qui
décrivent le même phénomène. Les choisir au hasard mélangerait des idées sans
rapport ; les choisir d'après nos résultats serait du surajustement. On les
choisit par **ce qu'ils disent** : chaque fiche est vectorisée (le même modèle
que la base de recherche, `bge-base-en-v1.5`, en local) sur son affirmation, sa
construction, son univers et son horizon, et deux fiches sont liées quand leur
similarité cosinus dépasse `SEUIL`.

**AUCUN RENDEMENT, AUCUN IC N'ENTRE ICI.** Seul le texte des fiches est lu.

Sortie : `scripts/out/grappes.json` — pour chaque fiche ses voisins les plus
proches (la mémoire sémantique du critique), et les grappes (composantes
connexes au-dessus du seuil, au plus `TAILLE_MAX` fiches), chacune avec un
identifiant stable tiré de ses membres.

    python scripts/grappes.py            # calcule et écrit
    python scripts/grappes.py --status   # les grappes, sans recalcul
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from code_signal import fiche_files  # noqa: E402

MODELE = "BAAI/bge-base-en-v1.5"  # celui de vectordb/embed.py : un seul espace de sens
SEUIL = 0.80        # D39 : fixé avant de lire les grappes, sur le texte seul
TAILLE_MAX = 6      # une synthèse lit ses fiches entières : au-delà, elle ne les lit plus
VOISINS = 5
SORTIE = REPO / "scripts" / "out" / "grappes.json"


def texte(v) -> str:
    if isinstance(v, dict):
        return str(v.get("value") or v.get("reason") or "")
    if isinstance(v, list):
        return " ; ".join(texte(x) for x in v)
    return "" if v is None else str(v)


def representation(fiche: dict) -> str:
    """Ce qui dit le MÉCANISME d'un papier, pas ses chiffres."""
    src = fiche.get("source") or {}
    return " \n".join(x for x in (
        src.get("title") or "",
        texte(fiche.get("claim")),
        texte(fiche.get("signal_construction")),
        texte(fiche.get("universe")),
        texte(fiche.get("horizon")),
    ) if x)


def composantes(ids: list[str], sim, seuil: float) -> list[list[str]]:
    parent = {i: i for i in ids}

    def racine(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            if sim[a][b] >= seuil:
                parent[racine(ids[a])] = racine(ids[b])
    groupes: dict[str, list[str]] = {}
    for i in ids:
        groupes.setdefault(racine(i), []).append(i)
    return [sorted(g) for g in groupes.values()]


def grappes(ids: list[str], sim) -> list[list[str]]:
    """Composantes au-dessus du seuil ; une composante trop grande se recoupe à
    un seuil plus haut, jusqu'à ne plus dépasser TAILLE_MAX."""
    index = {i: k for k, i in enumerate(ids)}
    out, file = [], [(ids, SEUIL)]
    while file:
        membres, s = file.pop()
        for g in composantes(membres, [[sim[index[a]][index[b]] for b in membres]
                                       for a in membres], s):
            if len(g) > TAILLE_MAX and s < 0.99:
                file.append((g, round(s + 0.02, 2)))
            elif len(g) >= 2:
                out.append(g)
    return sorted(out, key=lambda g: (-len(g), g))


def do_calcul() -> int:
    import numpy as np  # noqa: PLC0415
    from fastembed import TextEmbedding  # noqa: PLC0415

    ff = fiche_files()
    ids = sorted(i for i in ff if not i.startswith("synthese-"))  # D39 : les papiers seuls
    fiches = {i: json.loads(ff[i].read_text(encoding="utf-8")) for i in ids}
    modele = TextEmbedding(model_name=MODELE)
    vecs = np.array(list(modele.embed([representation(fiches[i]) for i in ids])))
    vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    sim = (vecs @ vecs.T).tolist()

    voisins = {}
    for k, i in enumerate(ids):
        ordre = sorted(((sim[k][j], ids[j]) for j in range(len(ids)) if j != k), reverse=True)
        voisins[i] = [{"fiche_id": f, "cosine": round(c, 4)} for c, f in ordre[:VOISINS]]

    groupes = []
    for g in grappes(ids, sim):
        gid = "G-" + hashlib.sha1("|".join(g).encode()).hexdigest()[:6]
        paires = [sim[ids.index(a)][ids.index(b)] for x, a in enumerate(g) for b in g[x + 1:]]
        groupes.append({"id": gid, "members": g, "mean_cosine": round(sum(paires) / len(paires), 4),
                        "titles": {m: (fiches[m].get("source") or {}).get("title") for m in g}})

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps({
        "generated": datetime.now(UTC).isoformat(timespec="minutes"),
        "model": MODELE, "threshold": SEUIL, "max_size": TAILLE_MAX,
        "fiches": {i: {"title": (fiches[i].get("source") or {}).get("title"),
                       "neighbors": voisins[i]} for i in ids},
        "groups": groupes,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tous = sorted(sim[a][b] for a in range(len(ids)) for b in range(a + 1, len(ids)))
    q = lambda p: tous[int(p * (len(tous) - 1))]  # noqa: E731
    print(f"{len(ids)} fiches ; cosinus entre paires : médiane {q(.5):.3f}, "
          f"90e centile {q(.9):.3f}, max {tous[-1]:.3f}")
    return do_status()


def do_status() -> int:
    if not SORTIE.is_file():
        raise SystemExit("pas encore de grappes : python scripts/grappes.py")
    d = json.loads(SORTIE.read_text(encoding="utf-8"))
    print(f"{len(d['groups'])} grappe(s) au seuil {d['threshold']} ({d['model']}) :")
    for g in d["groups"]:
        print(f"\n  {g['id']}  {len(g['members'])} fiches, cosinus moyen {g['mean_cosine']:.3f}")
        for m in g["members"]:
            print(f"    - {m}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Les grappes de fiches — D39")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)
    return do_status() if a.status else do_calcul()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
