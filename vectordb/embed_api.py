"""Les embeddings par l'API REST de Supabase (HTTPS), quand le port 5432 est fermé.

Même modèle, mêmes vecteurs que `vectordb/embed.py` — seul le chemin change :
la lecture des morceaux à faire et l'écriture des vecteurs passent par l'API
(port 443), que le réseau de l'université laisse passer. L'écriture appelle la
fonction `enregistrer_embeddings` (migration 005), une requête par lot.

**La clé secrète** (`SUPABASE_SECRET_KEY`) et l'adresse (`SUPABASE_URL`) se
lisent dans `.env`, que l'opérateur remplit lui-même ; elles ne s'écrivent nulle
part ailleurs et ne s'affichent jamais. La clé publique ne suffit pas, et c'est
voulu : la fonction n'est exécutable que par `service_role`.

    .venv-gpu/Scripts/python.exe vectordb/embed_api.py --gpu
    .venv-gpu/Scripts/python.exe vectordb/embed_api.py --essai   # un lot, pour vérifier
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from embed import BATCH, MODEL, MODEL_DIM, embed_texts, load_model  # noqa: E402
from vector_db import load_env_file, to_pgvector  # noqa: E402

PAUSES = (5, 15, 30, 60, 120)  # reprises sur erreur réseau, croissantes


class Api:
    def __init__(self) -> None:
        load_env_file()
        self.url = os.environ.get("SUPABASE_URL", "").rstrip("/")
        self.cle = os.environ.get("SUPABASE_SECRET_KEY", "").strip()
        if not self.url or not self.cle:
            raise SystemExit("SUPABASE_URL ou SUPABASE_SECRET_KEY absent de .env — à remplir "
                             "par l'opérateur (clé SECRÈTE, jamais la clé publique)")

    def appel(self, methode: str, chemin: str, corps=None) -> object:
        donnees = json.dumps(corps).encode() if corps is not None else None
        req = urllib.request.Request(f"{self.url}{chemin}", data=donnees, method=methode, headers={
            "apikey": self.cle, "Authorization": f"Bearer {self.cle}",
            "Content-Type": "application/json", "Accept": "application/json"})
        for i, pause in enumerate((0, *PAUSES)):
            time.sleep(pause)
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    texte = r.read().decode()
                    return json.loads(texte) if texte else None
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")[:300]
                if e.code < 500 or i == len(PAUSES):
                    raise SystemExit(f"API {e.code} sur {chemin} : {detail}") from None
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if i == len(PAUSES):
                    raise SystemExit(f"API injoignable : {e}") from None
                print(f"  coupure réseau ({type(e).__name__}) — reprise {i + 1}/{len(PAUSES)}",
                      flush=True)
        return None

    def a_faire(self, n: int) -> list[dict]:
        return self.appel("GET", "/rest/v1/chunks?select=id,content&embedding=is.null"
                                 f"&order=paper_id,ordinal&limit={n}") or []

    def ecrire(self, ids: list[str], vecteurs: list[str]) -> int:
        return int(self.appel("POST", "/rest/v1/rpc/enregistrer_embeddings",
                              {"ids": ids, "vecteurs": vecteurs, "modele": MODEL}) or 0)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Embeddings par l'API REST de Supabase")
    ap.add_argument("--gpu", action="store_true")
    ap.add_argument("--essai", action="store_true", help="un seul lot, pour vérifier le chemin")
    a = ap.parse_args(argv)

    api = Api()
    model = load_model(a.gpu)
    faits, depart = 0, time.time()
    while True:
        lot = api.a_faire(BATCH)
        if not lot:
            break
        vecteurs = embed_texts(model, [r["content"] for r in lot])
        ecrits = api.ecrire([r["id"] for r in lot],
                            [to_pgvector(v, MODEL_DIM) for v in vecteurs])
        if ecrits != len(lot):
            raise SystemExit(f"{ecrits} vecteur(s) écrit(s) pour un lot de {len(lot)} : arrêt")
        faits += ecrits
        print(f"  {faits:>6} écrits  {faits / (time.time() - depart):5.1f} morceaux/s", flush=True)
        if a.essai:
            print("--essai : un lot écrit, le chemin fonctionne.")
            return 0
    print(f"\n{faits} morceaux vectorisés par l'API en {(time.time() - depart) / 60:.1f} min ; "
          "plus aucun morceau sans embedding.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
