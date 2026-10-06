"""Le tri en masse des papiers moissonnés — par passages successifs, hors ligne.

`corpus/triage_harvest.py` a fait **un** passage (119 papiers, 2026-09-23) : il
lit la base, donc demande le réseau, et il repartirait de zéro — il retrierait
les 119. Ce script fait les passages **suivants** :

- la population est **ce qui n'a jamais été trié** : un papier moissonné, non
  doublon, dont le PDF est sur ce poste, et dont le titre n'est pas déjà dans
  `corpus/triage_harvest_verdicts.json` ni dans un passage ouvert ;
- l'entrée du trieur est tirée **du PDF local** (ses deux premières pages, qui
  portent le résumé), ou du résumé de `harvest.json` si le PDF ne rend rien :
  aucun réseau ;
- l'**ordre** met en tête les papiers que la règle de pertinence de `D33` garde,
  puis les plus cités. Ordonner n'est pas filtrer : `D33` laisse intacte la
  population du tri, et **tous** les papiers passeront, les autres ensuite ;
- la consigne et l'échelle sont celles de `triage_harvest.py` (`D15`),
  importées, jamais recopiées.

**Le compte est refusé s'il ne se reconstitue pas** (`L21`, comme
`merge_triage.py`) : chaque passage déclare ses `id` d'avance
(`corpus/triage_passages/passage-NN.json`) ; `--verser` exige qu'ils soient
tous triés, une fois chacun, sur l'échelle de `D15`, avant d'ajouter une seule
ligne à `corpus/triage_harvest_verdicts.json`. Ajouter, jamais réécrire.

    python corpus/tri_en_masse.py --status
    python corpus/tri_en_masse.py --preparer --lots 5        # 5 lots de 30
    python corpus/tri_en_masse.py --verser 02                # après les trieurs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "corpus"
sys.path.insert(0, str(CORPUS))

from triage_harvest import CONSIGNE, RESUME_CHARS  # noqa: E402

HARVEST = CORPUS / "harvest.json"
VERDICTS = CORPUS / "triage_harvest_verdicts.json"
RETRAITS = CORPUS / "base_retraits.jsonl"
PASSAGES = CORPUS / "triage_passages"
WORK = CORPUS / "consignes-triage"
ECHELLE = ("oui", "partiel", "non")
TAILLE_LOT = 30


def norm(titre: str) -> str:
    """L'expression de `title_norm` (vectordb, migration 001), celle de promote_harvest."""
    return re.sub(r"[^a-zA-Z0-9]+", " ", titre or "").lower().strip()


def lire_json(path: Path, defaut):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else defaut


def passages() -> list[dict]:
    return [lire_json(p, {}) for p in sorted(PASSAGES.glob("passage-??.json"))]


def deja_tries() -> set[str]:
    titres = {norm(v["title"]) for v in lire_json(VERDICTS, [])}
    for p in passages():
        if not p.get("verse"):
            titres |= {norm(x["title"]) for x in p["papiers"]}
    return titres


def titres_en_base() -> set[str]:
    """Les titres des papiers moissonnés en texte intégral dans la base (`D44`), par l'API."""
    sys.path.insert(0, str(REPO / "vectordb"))
    from embed_api import Api  # noqa: PLC0415

    api, out, debut = Api(), set(), 0
    while True:
        lot = api.appel("GET", "/rest/v1/papers?select=title&text_source=eq.harvest"
                               f"&order=id&offset={debut}&limit=1000") or []
        out |= {norm(x["title"]) for x in lot}
        if len(lot) < 1000:
            return out
        debut += 1000


def population(semantique: bool = False, seulement: set[str] | None = None) -> list[dict]:
    works = lire_json(HARVEST, {}).get("works", [])
    faits = deja_tries()
    retires = set()
    if RETRAITS.is_file():
        for x in RETRAITS.read_text(encoding="utf-8").splitlines():
            if x.strip():
                retires.add(norm(json.loads(x).get("title", "")))
    vus: set[str] = set()
    out = []
    for w in works:
        t = norm(w["title"])
        if (w.get("duplicate_of") or not w.get("pdf") or t in faits or t in vus
                or not (REPO / w["pdf"]).is_file()
                or (seulement is not None and t not in seulement)):
            continue
        vus.add(t)
        out.append({**w, "_pertinent": t not in retires, "_priorite": None})
    if semantique and out:
        prioriser(out)
        out.sort(key=lambda w: (-w["_priorite"], w["title"]))
    else:
        out.sort(key=lambda w: (not w["_pertinent"], -(w.get("cited_by_count") or 0), w["title"]))
    return out


MODELE = "BAAI/bge-base-en-v1.5"  # celui de la base et des grappes (D39)


def cibles() -> list[str]:
    """Ce qui nous intéresse déjà : chaque fiche, et chaque papier retenu par le tri."""
    sys.path.insert(0, str(REPO / "scripts"))
    from code_signal import fiche_files  # noqa: PLC0415
    from grappes import representation  # noqa: PLC0415

    out = [representation(json.loads(p.read_text(encoding="utf-8")))
           for p in fiche_files().values()]
    out += [v["title"] for v in lire_json(VERDICTS, []) if v["verdict"] in ("oui", "partiel")]
    return out


def prioriser(papiers: list[dict]) -> None:
    """La priorité d'un papier : sa plus grande similarité (cosinus) avec une fiche
    ou un papier retenu. ORDONNER, jamais filtrer (D33) : chaque papier passera ;
    ceux qui ressemblent à ce que la chaîne sait déjà transformer passent d'abord,
    là où les grappes et les synthèses ont le plus de chances de naître (D39).
    Titre et résumé moissonné seuls : aucun rendement, aucun IC, aucun PDF lu ici.
    """
    import numpy as np  # noqa: PLC0415
    from fastembed import TextEmbedding  # noqa: PLC0415

    modele = TextEmbedding(model_name=MODELE)
    norme = lambda m: m / np.linalg.norm(m, axis=1, keepdims=True)  # noqa: E731
    c = norme(np.array(list(modele.embed(cibles()))))
    textes = [f"{w['title']}\n{w.get('abstract') or ''}"[:1500] for w in papiers]
    p = norme(np.array(list(modele.embed(textes))))
    sim = p @ c.T
    for w, s in zip(papiers, sim.max(axis=1), strict=True):
        w["_priorite"] = round(float(s), 4)


def debut_du_papier(w: dict) -> str:
    """Les deux premières pages du PDF local ; le résumé moissonné à défaut."""
    texte = ""
    try:
        from pypdf import PdfReader  # noqa: PLC0415

        lecteur = PdfReader(str(REPO / w["pdf"]))
        texte = " ".join((page.extract_text() or "") for page in lecteur.pages[:2])
    except Exception:  # noqa: BLE001 — un PDF illisible ne sort pas du lot (L21)
        texte = ""
    texte = " ".join(texte.split())
    if len(texte) < 200 and w.get("abstract"):
        texte = " ".join(str(w["abstract"]).split())
    return texte[:RESUME_CHARS]


def do_status() -> int:
    tries = lire_json(VERDICTS, [])
    c = Counter(v["verdict"] for v in tries)
    print(f"déjà triés : {len(tries)}  ({', '.join(f'{k} {c[k]}' for k in ECHELLE)})")
    for p in passages():
        rendus = sum(1 for f in PASSAGES.glob(f"passage-{p['passage']}-lot-*.json"))
        etat = "versé" if p.get("verse") else f"ouvert, {rendus}/{p['lots']} lot(s) rendus"
        print(f"  passage {p['passage']} : {len(p['papiers'])} papiers, {etat}")
    pop = population()
    pert = sum(w["_pertinent"] for w in pop)
    print(f"restent à trier : {len(pop)}  (dont {pert} gardés par D33, en tête de file)")
    return 0


def do_preparer(lots: int, taille: int, semantique: bool = True, base: bool = False) -> int:
    ouverts = [p for p in passages() if not p.get("verse")]
    if ouverts:
        raise SystemExit(f"le passage {ouverts[0]['passage']} est encore ouvert : "
                         f"`--verser {ouverts[0]['passage']}` d'abord")
    # 2026-10-06 : `--base` ne garde que les papiers déjà en texte intégral dans la
    # base, ceux que la recherche des voisins voit (choix de l'opérateur).
    pop = population(semantique=semantique,
                     seulement=titres_en_base() if base else None)[: lots * taille]
    if not pop:
        print("rien à trier")
        return 0
    numero = f"{len(passages()) + 2:02d}"  # le passage 01 est celui de triage_harvest.py
    dossier = WORK / f"passage-{numero}"
    dossier.mkdir(parents=True, exist_ok=True)
    groupes = [pop[i:i + taille] for i in range(0, len(pop), taille)]
    for n, groupe in enumerate(groupes, 1):
        blocs = []
        for w in groupe:
            auteurs = ", ".join((w.get("authors") or [])[:4]) or "auteurs inconnus"
            debut = debut_du_papier(w) or ("AUCUN TEXTE EXTRAIT — juge sur le titre seul, "
                                           "et dis-le dans la raison.")
            blocs.append(f"### id `{w['openalex_id']}`\n\n**{w['title']}** — {auteurs}, "
                         f"{w.get('year') or 'année inconnue'}\n\n> {debut}\n")
        texte = CONSIGNE.format(lot=n, total=len(groupes), papiers="\n".join(blocs))
        texte += (f"\n---\n\nÉcris ton tableau JSON avec l'outil Write dans "
                  f"`corpus/triage_passages/passage-{numero}-lot-{n:02d}.json`.\n")
        (dossier / f"lot-{n:02d}.md").write_text(texte, encoding="utf-8")
    PASSAGES.mkdir(parents=True, exist_ok=True)
    (PASSAGES / f"passage-{numero}.json").write_text(json.dumps({
        "passage": numero, "prepared": date.today().isoformat(), "lots": len(groupes),
        "taille": taille, "verse": False,
        "order": "similarité sémantique aux fiches et aux papiers retenus (D39)",
        "papiers": [{"id": w["openalex_id"], "title": w["title"], "lot": i // taille + 1,
                     "pertinent_d33": w["_pertinent"], "priority": w["_priorite"]}
                    for i, w in enumerate(pop)],
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"passage {numero} : {len(pop)} papiers en {len(groupes)} lot(s)")
    for n in range(1, len(groupes) + 1):
        f = dossier / f"lot-{n:02d}.md"
        print(f"  {f.as_posix()}  ({f.stat().st_size / 1000:.0f} ko)")
    return 0


def do_verser(numero: str) -> int:
    chemin = PASSAGES / f"passage-{numero}.json"
    p = lire_json(chemin, None)
    if p is None:
        raise SystemExit(f"passage {numero} inconnu")
    if p.get("verse"):
        raise SystemExit(f"le passage {numero} est déjà versé")
    attendus = {x["id"]: x for x in p["papiers"]}
    lus: dict[str, dict] = {}
    fautes: list[str] = []
    for n in range(1, p["lots"] + 1):
        f = PASSAGES / f"passage-{numero}-lot-{n:02d}.json"
        if not f.is_file():
            fautes.append(f"lot {n:02d} non rendu : {f.name}")
            continue
        for ligne in json.loads(f.read_text(encoding="utf-8")):
            i = str(ligne.get("id"))
            if i in lus:
                fautes.append(f"{i} trié deux fois")
            lus[i] = {**ligne, "lot": f"p{numero}-{n:02d}"}
    manquants = sorted(set(attendus) - set(lus))
    intrus = sorted(set(lus) - set(attendus))
    mauvais = [i for i, v in lus.items() if v.get("verdict") not in ECHELLE]
    sans_raison = [i for i, v in lus.items() if not str(v.get("raison") or "").strip()]
    if manquants:
        fautes.append(f"{len(manquants)} papier(s) non trié(s) (L21) : {manquants[:3]}")
    if intrus:
        fautes.append(f"{len(intrus)} id inconnu(s), recopié(s) de travers : {intrus[:3]}")
    if mauvais:
        fautes.append(f"{len(mauvais)} verdict(s) hors de l'échelle de D15 : {mauvais[:3]}")
    if sans_raison:
        fautes.append(f"{len(sans_raison)} verdict(s) sans raison : {sans_raison[:3]}")
    existants = lire_json(VERDICTS, [])
    deja = {norm(v["title"]) for v in existants}
    doubles = [i for i in attendus if norm(attendus[i]["title"]) in deja]
    if doubles:
        fautes.append(f"{len(doubles)} papier(s) déjà dans les verdicts : {doubles[:3]}")
    if fautes:
        print(f"PASSAGE {numero} REFUSÉ — rien n'est versé :")
        for f in fautes:
            print(f"  - {f}")
        return 1

    nouveaux = [{"id": i, "title": attendus[i]["title"], "verdict": lus[i]["verdict"],
                 "raison": lus[i]["raison"], "lot": lus[i]["lot"]} for i in attendus]
    VERDICTS.write_text(json.dumps(existants + nouveaux, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    p["verse"] = date.today().isoformat()
    chemin.write_text(json.dumps(p, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    c = Counter(v["verdict"] for v in nouveaux)
    print(f"passage {numero} versé : {len(nouveaux)} verdicts "
          f"({', '.join(f'{k} {c[k]}' for k in ECHELLE)})")
    par_lot: dict[str, Counter] = {}
    for v in nouveaux:
        par_lot.setdefault(v["lot"], Counter())[v["verdict"]] += 1
    print("par lot — un trieur bien plus sévère qu'un autre serait un signal :")
    for lot, cc in sorted(par_lot.items()):
        print(f"  {lot} : " + "  ".join(f"{k} {cc[k]:>2}" for k in ECHELLE))
    print("Étape suivante : python corpus/promote_harvest.py --fetch")
    return 0


def self_check() -> int:
    """Le mécanisme, sur une copie temporaire : aucun fichier réel n'est touché.

    Les verdicts de ce test sont fabriqués DANS la copie, pour éprouver le
    compte ; ils ne jugent aucun papier et disparaissent avec elle.
    """
    import shutil  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    global VERDICTS, PASSAGES, WORK, population  # noqa: PLW0603
    reels = (VERDICTS, PASSAGES, WORK)
    vraie_population = population
    tmp = Path(tempfile.mkdtemp())
    ok = True

    # La population du test est FABRIQUÉE, et ne dépend d'aucun PDF du poste :
    # les PDF ne sont pas dans git, et un poste qui n'a pas moissonné avait une
    # file vide — le test échouait alors sur « passage 02 inconnu » (L32).
    fabriques = [{"openalex_id": f"WTEST{i}", "title": f"Papier fabrique pour le test {i}",
                  "authors": ["Test"], "year": 2000, "abstract": "Texte fabrique.",
                  "pdf": None, "_pertinent": True, "_priorite": None} for i in range(5)]

    def population_de_test(semantique: bool = False, seulement=None) -> list[dict]:
        faits = deja_tries()
        return [w for w in fabriques if norm(w["title"]) not in faits]

    def cas(label: str, cond: bool) -> None:
        nonlocal ok
        ok &= cond
        print(f"  {'ok  ' if cond else 'FAUX'} {label}")

    try:
        if reels[0].is_file():
            shutil.copy(reels[0], tmp / "v.json")
        else:
            (tmp / "v.json").write_text("[]", encoding="utf-8")
        VERDICTS, PASSAGES, WORK = tmp / "v.json", tmp / "passages", tmp / "consignes"
        population = population_de_test
        avant = len(population())
        do_preparer(1, 3, semantique=False)
        p = lire_json(PASSAGES / "passage-02.json", {})
        ids = [x["id"] for x in p.get("papiers", [])]
        cas("un passage de 3 papiers est préparé", len(ids) == 3)
        cas("un lot non rendu est refusé", do_verser("02") == 1)
        lot = PASSAGES / "passage-02-lot-01.json"
        lot.write_text(json.dumps([{"id": i, "verdict": "non", "raison": "test"}
                                   for i in ids[:2]]), encoding="utf-8")
        cas("un papier manquant est refusé (L21)", do_verser("02") == 1)
        lot.write_text(json.dumps([{"id": i, "verdict": "peut-être", "raison": "test"}
                                   for i in ids]), encoding="utf-8")
        cas("un verdict hors de l'échelle est refusé", do_verser("02") == 1)
        lot.write_text(json.dumps([{"id": i, "verdict": "non", "raison": "test"}
                                   for i in ids]), encoding="utf-8")
        cas("un lot complet est versé", do_verser("02") == 0)
        try:
            do_verser("02")
            cas("un passage ne se verse pas deux fois", False)
        except SystemExit:
            cas("un passage ne se verse pas deux fois", True)
        cas("la file diminue d'autant", len(population()) == avant - 3)
    finally:
        VERDICTS, PASSAGES, WORK = reels
        population = vraie_population
        shutil.rmtree(tmp, ignore_errors=True)
    print("TRI EN MASSE : " + ("le compte tient" if ok else "EN DÉFAUT"))
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le tri en masse des papiers moissonnés")
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--preparer", action="store_true")
    ap.add_argument("--lots", type=int, default=5, help="avec --preparer : nombre de lots")
    ap.add_argument("--taille", type=int, default=TAILLE_LOT)
    ap.add_argument("--base", action="store_true",
                    help="avec --preparer : seulement les papiers en texte intégral dans la base")
    ap.add_argument("--verser", metavar="NN")
    a = ap.parse_args(argv)
    if a.self_check:
        return self_check()
    if a.preparer:
        return do_preparer(a.lots, a.taille, base=a.base)
    if a.verser:
        return do_verser(a.verser)
    return do_status()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
