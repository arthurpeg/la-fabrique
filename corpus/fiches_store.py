"""Les fiches vivent dans la base ; le dossier local n'en est que le miroir (D44).

**La base fait foi.** Chaque fiche est une ligne de la table `fiches` (migration
006) : son texte exact (`raw`), sa forme interrogeable (`content`), son
empreinte, son origine et le papier auquel elle se rattache. Les outils de la
chaîne lisent le **miroir** local (`corpus/fiches/`, `corpus/fiches_harvest/`,
`corpus/fiches_synthese/`), régénéré depuis la base **octet pour octet** — les
empreintes inscrites par les registres de production restent donc valides, et
rien de ce qui contrôle l'intégrité d'une fiche n'a à changer.

Le miroir reste versionné dans git : c'est la sauvegarde, comme le registre.

**Le sens des écritures.** Une fiche neuve (écrite par un sous-agent isolé,
qui n'a pas le réseau) arrive d'abord comme fichier du miroir ; `--pousser`
l'envoie à la base, après son inscription et son jugement. `--tirer` fait
l'inverse. **Un conflit ne s'écrase jamais** : une fiche qui diffère entre la
base et le miroir est signalée, pas remplacée.

Tout passe par l'API REST (HTTPS) et la clé secrète de `.env` : le port 5432
n'est pas nécessaire.

    python corpus/fiches_store.py --etat      # base et miroir sont-ils d'accord ?
    python corpus/fiches_store.py --pousser   # miroir -> base (fiches absentes de la base)
    python corpus/fiches_store.py --tirer     # base -> miroir (fiches absentes du miroir)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "vectordb"))

DOSSIERS = {
    "amorce": REPO / "corpus" / "fiches",
    "harvest": REPO / "corpus" / "fiches_harvest",
    "synthese": REPO / "corpus" / "fiches_synthese",
}


def api():
    from embed_api import Api  # noqa: PLC0415

    return Api()


def empreinte(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm_titre(titre: str) -> str:
    """L'expression de `papers.title_norm` (migration 001)."""
    return re.sub(r"[^a-zA-Z0-9]+", " ", titre or "").lower().strip()


def miroir() -> dict[str, tuple[str, Path]]:
    """fiche_id -> (origine, chemin) pour chaque fiche du miroir local."""
    out = {}
    for origine, d in DOSSIERS.items():
        for p in sorted(d.glob("*.json")):
            if p.stem in out:
                raise SystemExit(f"fiche en double dans le miroir : {p.stem}")
            out[p.stem] = (origine, p)
    return out


def base(a) -> dict[str, dict]:
    lignes, debut = [], 0
    while True:
        lot = a.appel("GET", "/rest/v1/fiches?select=fiche_id,origin,sha256,paper_id"
                             f"&order=fiche_id&limit=1000&offset={debut}") or []
        lignes += lot
        if len(lot) < 1000:
            return {r["fiche_id"]: r for r in lignes}
        debut += 1000


def papier_de(a, fiche: dict) -> str | None:
    titre = (fiche.get("source") or {}).get("title")
    if not titre:
        return None
    q = urllib.parse.quote(norm_titre(titre))
    r = a.appel("GET", f"/rest/v1/papers?select=id&title_norm=eq.{q}&limit=1") or []
    return r[0]["id"] if r else None


def do_etat() -> int:
    a = api()
    m, b = miroir(), base(a)
    seulement_miroir = sorted(set(m) - set(b))
    seulement_base = sorted(set(b) - set(m))
    conflits = sorted(f for f in set(m) & set(b)
                      if empreinte(m[f][1].read_bytes()) != b[f]["sha256"])
    print(f"base : {len(b)} fiche(s) ; miroir : {len(m)} ; d'accord : "
          f"{len(set(m) & set(b)) - len(conflits)}")
    for titre, liste in (("à pousser (miroir seul)", seulement_miroir),
                         ("à tirer (base seule)", seulement_base),
                         ("EN CONFLIT (diffèrent)", conflits)):
        if liste:
            print(f"  {titre} : {len(liste)}")
            for f in liste[:10]:
                print(f"      {f}")
    return 1 if conflits else 0


def do_pousser() -> int:
    a = api()
    m, b = miroir(), base(a)
    envoyees = 0
    for fid, (origine, p) in sorted(m.items()):
        raw = p.read_bytes()
        if fid in b:
            if b[fid]["sha256"] != empreinte(raw):
                print(f"  CONFLIT {fid} : la base porte une autre version — rien n'est écrasé")
            continue
        fiche = json.loads(raw.decode("utf-8"))
        a.appel("POST", "/rest/v1/fiches", {
            "fiche_id": fid, "origin": origine, "paper_id": papier_de(a, fiche),
            "raw": raw.decode("utf-8"), "content": fiche, "sha256": empreinte(raw)})
        envoyees += 1
        print(f"  poussée : {fid}", flush=True)
    print(f"{envoyees} fiche(s) poussée(s) dans la base")
    return 0


def do_tirer() -> int:
    a = api()
    m, b = miroir(), base(a)
    tirees = 0
    for fid in sorted(set(b) - set(m)):
        r = a.appel("GET", f"/rest/v1/fiches?select=origin,raw,sha256&fiche_id=eq.{fid}") or []
        if not r:
            continue
        raw = r[0]["raw"].encode("utf-8")
        if empreinte(raw) != r[0]["sha256"]:
            print(f"  REFUS {fid} : le texte de la base ne correspond pas à son empreinte")
            continue
        (DOSSIERS[r[0]["origin"]] / f"{fid}.json").write_bytes(raw)
        tirees += 1
        print(f"  tirée : {fid}")
    print(f"{tirees} fiche(s) tirée(s) de la base dans le miroir")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Les fiches dans la base — D44")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--etat", action="store_true")
    g.add_argument("--pousser", action="store_true")
    g.add_argument("--tirer", action="store_true")
    a = ap.parse_args(argv)
    if a.pousser:
        return do_pousser()
    if a.tirer:
        return do_tirer()
    return do_etat()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
