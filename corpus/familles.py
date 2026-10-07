"""Les familles d'idées parmi les papiers retenus par le tri — et leur promesse.

Pour fusionner des papiers « cohérents et prometteurs » (demande de l'opérateur,
2026-10-06), il faut d'abord savoir quels papiers retenus (`oui`, `partiel`)
défendent **le même mécanisme**, et lesquels **annoncent un effet**. Le graphe de
similarité ne le dit pas : il relie des thèmes de proche en proche (une
composante de 194 papiers sur 308).

1. `--preparer` : des consignes de 30 papiers (titre, début du texte). Un agent
   isolé rend, pour chacun, son **mécanisme en une phrase** (la cause, et l'effet
   sur le prix) et **l'effet annoncé** dans une liste fermée, avec la citation
   du chiffre s'il y en a un.
2. `--verser` : contrôle mécanique (chaque papier une fois, valeurs dans la liste
   fermée) puis ajout à `corpus/familles_lectures.json`.
3. `--classer` : le code vectorise les mécanismes (le modèle de la base), forme
   des familles dont **chaque paire** dépasse `SEUIL` (lien complet), et classe les familles par promesse :
   nombre de papiers à effet positif chiffré, puis nombre de `oui`, puis taille.
   Sortie : `scripts/out/familles.json`.

Aucun rendement, aucun IC : seulement ce que les papiers disent d'eux-mêmes.

    python corpus/familles.py --preparer
    python corpus/familles.py --verser
    python corpus/familles.py --classer
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "corpus"))

import tri_en_masse as tri  # noqa: E402

WORK = REPO / "corpus" / "consignes-familles"
LECTURES = REPO / "corpus" / "familles_lectures.json"
SORTIE = REPO / "scripts" / "out" / "familles.json"
TAILLE = 30
EFFETS = ("positif_chiffre", "positif_qualitatif", "nul_ou_negatif", "non_dit")
SEUIL = 0.85  # cosinus entre deux phrases de mécanisme, fixé avant le premier classement

CONSIGNE = """\
# Consigne — le mécanisme et l'effet annoncé de {n} papiers (lot {lot} sur {total})

Tu es un lecteur isolé. Ta seule source est ce fichier : ne lis aucun autre
fichier, aucune commande, aucun accès web.

Pour **chaque** papier ci-dessous (titre, résumé et conclusion), rends :

- `mecanisme` : **une phrase de 15 mots au plus**, en français, qui dit **la
  cause et l'effet sur le prix** — par exemple « le rendement de la première
  demi-heure prédit celui de la dernière, dans le même sens », ou « un
  mouvement journalier extrême est suivi d'un retour partiel le lendemain ».
  Écris la cause **générale**, sans nom de pays ni de marché, pour que deux
  papiers sur le même mécanisme reçoivent des phrases proches. Si le papier ne
  propose aucun mécanisme de prix (méthode, mesure de volatilité), dis-le
  ainsi : « pas de mécanisme de prix : <ce qu'il mesure> ».
- `effet` : ce que le papier **annonce** pour ce mécanisme, un seul mot parmi
  `positif_chiffre` (un effet trouvé, avec un chiffre : rendement, Sharpe, t,
  R²), `positif_qualitatif` (un effet trouvé, sans chiffre visible ici),
  `nul_ou_negatif` (pas d'effet, ou l'effet inverse), `non_dit` (le début du
  texte ne le dit pas).
- `chiffre` : pour `positif_chiffre`, la phrase du texte qui porte le chiffre,
  **recopiée à la lettre** ; sinon `null`.

Juge sur le texte, rien d'autre. Ne devine pas un chiffre absent.

## Ce que tu rends

Écris avec l'outil Write, à `{chemin}`, un tableau JSON et rien d'autre :

```json
[{{"id": "<l'id donné>", "mecanisme": "...", "effet": "...", "chiffre": null}}, ...]
```

Un objet par papier, dans l'ordre, aucun omis. Réponds en une ligne : le chemin
écrit et le compte par `effet`.

## Les papiers

{papiers}
"""


def retenus() -> list[dict]:
    """Chaque papier retenu par le tri, avec son entrée de moisson (par titre)."""
    verdicts = tri.lire_json(tri.VERDICTS, [])
    works = {tri.norm(w["title"]): w for w in tri.lire_json(tri.HARVEST, {}).get("works", [])
             if w.get("pdf") and not w.get("duplicate_of")}
    out, vus = [], set()
    for v in verdicts:
        t = tri.norm(v["title"])
        if v["verdict"] not in ("oui", "partiel") or t in vus or t not in works:
            continue
        vus.add(t)
        out.append({"id": tri.ident(works[t]), "title": v["title"], "verdict": v["verdict"],
                    "work": works[t]})
    return out


RESUME = 1500  # caractères du résumé, puis de la conclusion, montrés au lecteur


def textes_en_base(titres: list[str]) -> dict[str, str]:
    """Le résumé et la conclusion de chaque papier, lus dans la base.

    Le 2026-10-06, la première lecture ne montrait que 1 100 caractères des deux
    premières pages du PDF (page de garde, remerciements) : 2 effets chiffrés
    sur 307. Le résultat d'un papier se lit dans son résumé et sa conclusion.
    """
    sys.path.insert(0, str(REPO / "vectordb"))
    from embed_api import Api  # noqa: PLC0415

    api, ids, debut = Api(), {}, 0
    while True:
        lot = api.appel("GET", "/rest/v1/papers?select=id,title&text_source=neq.abstract"
                               f"&order=id&offset={debut}&limit=1000") or []
        ids.update({tri.norm(x["title"]): x["id"] for x in lot})
        if len(lot) < 1000:
            break
        debut += 1000
    out = {}
    for t in titres:
        pid = ids.get(tri.norm(t))
        if not pid:
            continue
        tete = " ".join(" ".join(c["content"].split()) for c in api.appel(
            "GET", f"/rest/v1/chunks?select=content&paper_id=eq.{pid}&order=ordinal&limit=4")
            or [])
        i = tete.lower().find("abstract")
        resume = tete[i:] if i >= 0 else tete
        concl = api.appel("GET", f"/rest/v1/chunks?select=content&paper_id=eq.{pid}"
                                 "&section=eq.conclusion&order=ordinal&limit=2") or []
        if not concl:
            concl = list(reversed(api.appel(
                "GET", f"/rest/v1/chunks?select=content&paper_id=eq.{pid}"
                       "&order=ordinal.desc&limit=2") or []))
        fin = " ".join(" ".join(c["content"].split()) for c in concl)
        out[tri.norm(t)] = (f"**Résumé ou début :** {resume[:RESUME]}\n\n"
                            f"**Conclusion :** {fin[:RESUME]}")
    return out


def lots() -> list[Path]:
    return sorted(WORK.glob("lot-*.md"))


def do_preparer() -> int:
    deja = {x["id"] for x in tri.lire_json(LECTURES, [])}
    pop = [r for r in retenus() if r["id"] not in deja]
    if not pop:
        print("tous les papiers retenus sont lus")
        return 0
    WORK.mkdir(parents=True, exist_ok=True)
    for f in lots():
        f.unlink()
    groupes = [pop[i:i + TAILLE] for i in range(0, len(pop), TAILLE)]
    textes = textes_en_base([r["title"] for r in pop])
    for n, g in enumerate(groupes, 1):
        blocs = [f"### id `{r['id']}`\n\n**{r['title']}**\n\n"
                 + (textes.get(tri.norm(r["title"])) or "> " + (
                     tri.debut_du_papier(r["work"]) or "AUCUN TEXTE — juge sur le titre seul."))
                 + "\n" for r in g]
        chemin = WORK / f"lot-{n:02d}.json"
        (WORK / f"lot-{n:02d}.md").write_text(CONSIGNE.format(
            n=len(g), lot=n, total=len(groupes), chemin=chemin.as_posix(),
            papiers="\n".join(blocs)), encoding="utf-8")
    (WORK / "attendus.json").write_text(json.dumps(
        {r["id"]: {"title": r["title"], "verdict": r["verdict"]} for r in pop},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(pop)} papiers retenus en {len(groupes)} lot(s) : {WORK.relative_to(REPO)}")
    return 0


def do_verser() -> int:
    attendus = json.loads((WORK / "attendus.json").read_text(encoding="utf-8"))
    lus, fautes = {}, []
    for f in lots():
        rendu = f.with_suffix(".json")
        if not rendu.is_file():
            fautes.append(f"{rendu.name} non rendu")
            continue
        for x in json.loads(rendu.read_text(encoding="utf-8")):
            i = str(x.get("id"))
            if x.get("effet") not in EFFETS or not str(x.get("mecanisme") or "").strip():
                fautes.append(f"{i} : mecanisme vide ou effet hors liste")
            lus[i] = x
    manquants = set(attendus) - set(lus)
    intrus = set(lus) - set(attendus)
    if manquants or intrus:
        fautes.append(f"{len(manquants)} manquant(s), {len(intrus)} id inconnu(s) : "
                      f"{sorted(manquants | intrus)[:3]}")
    if fautes:
        print("REFUSÉ — rien n'est versé :")
        for f in fautes[:10]:
            print(f"  - {f}")
        return 1
    existants = tri.lire_json(LECTURES, [])
    existants += [{**lus[i], "id": i, **attendus[i]} for i in attendus]
    LECTURES.write_text(json.dumps(existants, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    from collections import Counter  # noqa: PLC0415

    print(f"{len(attendus)} lectures versées ; {Counter(lus[i]['effet'] for i in attendus)}")
    return 0


def do_classer() -> int:
    import numpy as np  # noqa: PLC0415
    from fastembed import TextEmbedding  # noqa: PLC0415

    lect = [x for x in tri.lire_json(LECTURES, [])
            if not x["mecanisme"].lower().startswith("pas de mécanisme")]
    m = np.array(list(TextEmbedding(model_name=tri.MODELE).embed([x["mecanisme"] for x in lect])))
    m = m / np.linalg.norm(m, axis=1, keepdims=True)
    # Lien complet : chaque paire d'une famille dépasse SEUIL. Le lien simple
    # (union-find, premier classement du 2026-10-07) enchaînait de proche en proche
    # et fondait 61 mécanismes sans rapport en une seule famille.
    from scipy.cluster.hierarchy import fcluster, linkage  # noqa: PLC0415
    from scipy.spatial.distance import squareform  # noqa: PLC0415

    dist = np.clip(1.0 - m @ m.T, 0.0, None)
    np.fill_diagonal(dist, 0.0)
    etiquettes = fcluster(linkage(squareform(dist, checks=False), method="complete"),
                          t=1.0 - SEUIL, criterion="distance")
    groupes: dict[int, list[dict]] = {}
    for e, x in zip(etiquettes, lect, strict=True):
        groupes.setdefault(int(e), []).append(x)
    familles = []
    for membres in groupes.values():
        if len(membres) < 2:
            continue
        familles.append({
            "papers": len(membres),
            "positif_chiffre": sum(x["effet"] == "positif_chiffre" for x in membres),
            "positif": sum(x["effet"].startswith("positif") for x in membres),
            "nul_ou_negatif": sum(x["effet"] == "nul_ou_negatif" for x in membres),
            "oui": sum(x["verdict"] == "oui" for x in membres),
            "members": [{k: x[k] for k in ("id", "title", "verdict", "mecanisme", "effet",
                                             "chiffre")} for x in membres],
        })
    familles.sort(key=lambda f: (-f["positif_chiffre"], -f["oui"], -f["papers"]))
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps({"seuil": SEUIL, "lectures": len(lect), "familles": familles},
                                 ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    seuls = len(lect) - sum(f["papers"] for f in familles)
    print(f"{len(lect)} mécanismes de prix, {len(familles)} familles (≥ 2 papiers), "
          f"{seuls} isolés ; seuil {SEUIL}")
    for k, f in enumerate(familles[:15], 1):
        print(f"\n{k:2d}. {f['papers']} papiers · {f['positif_chiffre']} effet chiffré · "
              f"{f['nul_ou_negatif']} nul/négatif · {f['oui']} oui")
        for x in f["members"][:4]:
            print(f"     - {x['mecanisme'][:90]}  [{x['effet']}]")
    print(f"\nécrit : {SORTIE.relative_to(REPO).as_posix()}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Familles d'idées parmi les papiers retenus")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--preparer", action="store_true")
    g.add_argument("--verser", action="store_true")
    g.add_argument("--classer", action="store_true")
    a = ap.parse_args(argv)
    return do_preparer() if a.preparer else do_verser() if a.verser else do_classer()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
