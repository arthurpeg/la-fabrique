"""Promeut les papiers moissonnés retenus par le triage vers le texte qui fait foi — `D22`.

`D22` § Ce qui reste ouvert : « Verser tout ou partie des moissonnés dans
`corpus/text/` si la phase 09 en retient beaucoup — à la sélection de la phase
09. » Le triage du 2026-09-23 (`corpus/triage_harvest_verdicts.json`) a retenu
**39 papiers sur 119** (10 `oui`, 29 `partiel`) : c'est cette sélection.

**Ce que ce script ne fait pas.** Il ne trie pas — c'est fait, par une session
séparée, sur l'échelle de `D15`. Il ne fiche pas — ce sera fait ensuite, par une
session séparée par papier (`D16` § Qui peut être l'extracteur), et ce script
ne prépare même pas la consigne, qui appartient à un outil du même genre que
`extract_fiche.py`, pas à celui-ci. Il fait le pont MÉCANIQUE que `D22` exige
avant qu'un papier `harvest` devienne fichable :

1. télécharge le PDF de chaque papier retenu — chacun déjà sondé `atteignable`
   par `corpus/harvest.py`, qui connaît sa `source_url` — dans
   `corpus/pdf/harvest/`, en réutilisant les fonctions de `harvest.py`
   (`filename`, `sha256`, `known_hashes`, `load`/`save`) plutôt que de les
   réécrire ;
2. le copie dans `corpus/pdf/` — là où `corpus/extract_text.py` (`D18`) le
   trouvera : `PDFDIR.glob("*.pdf")` n'est pas récursif, et la sortie de la
   quarantaine `harvest/` vers le dépôt curé est le même geste que
   `text_source: harvest -> authoritative` ;
3. **n'écrit RIEN dans `corpus/acquisition.json`.** `D20`/`F47` : le produit du
   moissonneur n'entre jamais dans `G1`-`G4`, qui reste la population des 20
   entrées d'`AMORCE.md`, et seule elle. Ce script écrit son propre registre,
   `corpus/harvest_promoted.json`, une ligne par papier promu.

**La correspondance des identifiants n'est pas triviale, et c'est le premier
piège du script.** `triage_harvest_verdicts.json` porte l'`id` de la base
Postgres (uuid, `papers.id`) ; `harvest.json` porte l'`openalex_id`. Les deux
espaces ne se recoupent pas directement : la correspondance se fait par
**titre normalisé**, avec exactement l'expression de la colonne générée
`title_norm` du schéma (`vectordb/migrations/001_init_vector_db.sql`) —
`trim(lower(regexp_replace(title, '[^a-zA-Z0-9]+', ' ', 'g')))` — pour que le
script et la base soient d'accord sur ce qu'est « le même titre ».

**`--flip-text-source` est un geste séparé, délibérément.** Il touche la base
partagée ; il ne s'exécute jamais en même temps qu'un téléchargement, pour
qu'une erreur réseau au milieu du lot ne laisse pas la base dans un état que
rien ne peut relire.

    python corpus/promote_harvest.py --report            # etat, SANS reseau
    python corpus/promote_harvest.py --fetch              # telecharge + copie
    python corpus/promote_harvest.py --flip-text-source   # DB : harvest -> authoritative,
                                                            # pour les papiers dont le texte
                                                            # D18 existe deja

Code de sortie 1 si un telechargement echoue, ou si une correspondance de
titre est introuvable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "corpus"))
sys.path.insert(0, str(REPO / "vectordb"))

import harvest  # noqa: E402
from probe_acquisition import MIN_PDF_BYTES, UA  # noqa: E402

VERDICTS = REPO / "corpus" / "triage_harvest_verdicts.json"
PROMOTED = REPO / "corpus" / "harvest_promoted.json"
TEXTDIR = REPO / "corpus" / "text"
CURATED_PDFDIR = REPO / "corpus" / "pdf"


def title_norm(title: str) -> str:
    """Identique a la colonne generee `papers.title_norm` (001_init_vector_db.sql)."""
    return re.sub(r"[^a-zA-Z0-9]+", " ", title).strip().lower()


def retenus() -> list[dict]:
    verdicts = json.loads(VERDICTS.read_text(encoding="utf-8"))
    return [v for v in verdicts if v["verdict"] in ("oui", "partiel")]


def matcher(selection: list[dict], data: dict) -> tuple[list[dict], list[dict]]:
    """Associe chaque verdict retenu a son entree de `harvest.json`, par titre.

    Rend (apparies, manquants). Un manquant casse le script plutot que
    d'avancer avec une correspondance devinee.
    """
    par_titre = {title_norm(w["title"]): w for w in data["works"]}
    apparies, manquants = [], []
    for v in selection:
        w = par_titre.get(title_norm(v["title"]))
        if w is None:
            manquants.append(v)
        else:
            apparies.append({"verdict": v, "work": w})
    return apparies, manquants


def charge_promus() -> dict[str, dict]:
    if not PROMOTED.is_file():
        return {}
    return {p["paper_id"]: p for p in json.loads(PROMOTED.read_text(encoding="utf-8"))}


def ecrit_promus(promus: dict[str, dict]) -> None:
    lignes = sorted(promus.values(), key=lambda p: p["title"])
    PROMOTED.write_text(json.dumps(lignes, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def do_report() -> int:
    selection = retenus()
    data = harvest.load()
    apparies, manquants = matcher(selection, data)
    promus = charge_promus()

    print(f"triage : {len(selection)} papier(s) retenu(s) (oui + partiel)")
    print(f"apparies a harvest.json par titre : {len(apparies)}")
    if manquants:
        print(f"NON apparies : {len(manquants)}")
        for m in manquants:
            print(f"  - {m['title'][:90]}")

    non_atteignables = [a for a in apparies if a["work"]["status"] != "atteignable"]
    if non_atteignables:
        print(f"ATTEIGNABLES REQUIS mais absents : {len(non_atteignables)}")
        for a in non_atteignables:
            print(f"  - {a['work']['title'][:90]} : status={a['work']['status']!r}")

    deja_promus = sum(1 for a in apparies if a["verdict"]["id"] in promus)
    print(f"deja promus (PDF copie dans corpus/pdf/) : {deja_promus}")

    textes = sorted(TEXTDIR.glob("*.default.txt")) if TEXTDIR.is_dir() else []
    print(f"corpus/text/ : {len(textes)} texte(s) default present(s)")
    return 0


def do_fetch() -> int:
    selection = retenus()
    data = harvest.load()
    apparies, manquants = matcher(selection, data)
    if manquants:
        print(
            f"ARRET : {len(manquants)} papier(s) retenu(s) sans correspondance dans "
            "harvest.json par titre — corriger avant de continuer."
        )
        for m in manquants:
            print(f"  - {m['title'][:90]}")
        return 1

    non_atteignables = [a for a in apparies if a["work"]["status"] != "atteignable"]
    if non_atteignables:
        print(
            f"ARRET : {len(non_atteignables)} papier(s) retenu(s) non `atteignable` dans "
            "harvest.json — relancer `harvest.py --probe` d'abord."
        )
        for a in non_atteignables:
            print(f"  - {a['work']['title'][:90]} : {a['work']['status']!r}")
        return 1

    harvest.PDFDIR.mkdir(parents=True, exist_ok=True)
    hashes = harvest.known_hashes()
    promus = charge_promus()
    echecs: list[tuple[str, str]] = []

    for a in apparies:
        verdict, work = a["verdict"], a["work"]
        name = harvest.filename(work)
        quarantaine = harvest.PDFDIR / name
        curated = CURATED_PDFDIR / name

        if not (quarantaine.is_file() and quarantaine.stat().st_size >= MIN_PDF_BYTES):
            try:
                import urllib.request

                req = urllib.request.Request(work["source_url"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read()
                if body[:5] != b"%PDF-" or len(body) < MIN_PDF_BYTES:
                    echecs.append((name, f"pas un PDF plausible ({len(body)} o)"))
                    print(f"  ECHEC     | {name}")
                    continue
                tmp = quarantaine.with_suffix(".part")
                tmp.write_bytes(body)
                tmp.replace(quarantaine)
                time.sleep(harvest.PAUSE_PROBE)
            except Exception as e:
                echecs.append((name, f"{type(e).__name__}: {e}"))
                print(f"  ECHEC     | {name}")
                continue

        digest = harvest.sha256(quarantaine)
        work["sha256"] = digest
        work["pdf"] = str(quarantaine.relative_to(REPO)).replace("\\", "/")

        if digest in hashes and hashes[digest] != name:
            print(
                f"  DOUBLON   | {name}  =  {hashes[digest]} — deja dans corpus/pdf/, "
                "pas copie une seconde fois"
            )
            work["duplicate_of"] = {"rule": "empreinte sha256", "file": hashes[digest]}
        else:
            if not curated.is_file():
                curated.write_bytes(quarantaine.read_bytes())
            hashes[digest] = name
            print(f"  promu     | {curated.stat().st_size:>8} o | {name}")

        promus[verdict["id"]] = {
            "paper_id": verdict["id"],
            "title": verdict["title"],
            "verdict": verdict["verdict"],
            "openalex_id": work["openalex_id"],
            "pdf": str((curated if curated.is_file() else quarantaine).relative_to(REPO)).replace(
                "\\", "/"
            ),
            "sha256": digest,
        }

    harvest.save(data)
    ecrit_promus(promus)

    print(f"\n{len(apparies) - len(echecs)} promu(s) sur {len(apparies)}, {len(echecs)} echec(s)")
    for name, why in echecs:
        print(f"  {name} : {why}")
    return 1 if echecs else 0


def do_flip_text_source() -> int:
    """Bascule `papers.text_source` de `harvest` a `authoritative` — D22.

    Seulement pour les papiers dont le texte D18 (`corpus/text/<slug>.default.txt`
    ET `.layout.txt`) existe deja : basculer avant que le texte existe rendrait
    la colonne fausse, ce que D22 interdit nommement ("Sans defaut, deliberement").
    """
    sys.path.insert(0, str(REPO / "vectordb"))
    from vector_db import VectorDB

    promus = charge_promus()
    if not promus:
        print("aucun papier promu — lancer --fetch d'abord")
        return 1

    manifest_path = TEXTDIR / "MANIFEST.json"
    manifest = (
        json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    )
    pdfs_avec_texte: dict[str, set[str]] = {}
    for e in manifest.get("files", []):
        pdfs_avec_texte.setdefault(e["pdf"], set()).add(e["mode"])

    a_basculer = []
    for p in promus.values():
        pdf_rel = f"corpus/pdf/{Path(p['pdf']).name}"
        if pdfs_avec_texte.get(pdf_rel) == {"default", "layout"}:
            a_basculer.append(p)

    if not a_basculer:
        print(
            "aucun papier promu n'a encore de texte D18 dans corpus/text/ — "
            "lancer `python corpus/extract_text.py` d'abord"
        )
        return 1

    print(f"{len(a_basculer)} papier(s) a basculer harvest -> authoritative")
    with VectorDB.from_env() as db:
        with db.conn.cursor() as cur:
            for p in a_basculer:
                cur.execute(
                    "update papers set text_source = 'authoritative' "
                    "where id = %s and text_source = 'harvest'",
                    (p["paper_id"],),
                )
                touche = cur.rowcount
                statut = "bascule" if touche else "deja fait / id absent"
                print(f"  {statut:<22} | {p['title'][:80]}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Promotion des papiers moissonnes retenus — D22")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--flip-text-source", action="store_true")
    a = ap.parse_args(argv)

    if a.fetch:
        return do_fetch()
    if a.flip_text_source:
        return do_flip_text_source()
    return do_report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
