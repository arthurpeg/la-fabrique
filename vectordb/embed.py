"""Remplit la colonne `embedding` des morceaux déjà en base.

**Localement et gratuitement.** `BAAI/bge-base-en-v1.5`, 768 dimensions, licence
MIT, 0,21 Go, exécuté par `fastembed` sur le processeur — pas de `torch`, pas de
clé, pas de réseau une fois le modèle téléchargé.

**Pourquoi 768 et non 1 536.** Aucun modèle libre ne produit 1 536 dimensions :
c'est un chiffre propre à OpenAI. Le choix était donc entre payer une clé et
migrer la colonne. La migration a été faite tant que la colonne était vide, ce
qui ne coûtait rien ; après coup elle aurait imposé de tout recalculer.

**Le nom du modèle voyage avec le vecteur.** La base refuse l'un sans l'autre
(`chunks_embedding_provenance`), et c'est ce qui rend un changement de modèle
BRUYANT au lieu d'être silencieux : deux modèles produisent des vecteurs
incomparables, et rien dans les nombres eux-mêmes ne le dirait.

**Il est reprenable.** Il ne traite que les morceaux dont l'`embedding` est
`NULL`, écrit par lots, et peut être relancé après une interruption sans
recalculer ce qui est déjà fait.

    python vectordb/embed.py --dry-run   # ce qu'il ferait, sans modele ni base
    python vectordb/embed.py             # calcule et ecrit
    python vectordb/embed.py --limit 50  # un echantillon
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vector_db import DEFAULT_DIM, VectorDB, VectorDBError, to_pgvector  # noqa: E402

MODEL = "BAAI/bge-base-en-v1.5"
MODEL_DIM = 768
BATCH = 64

# `bge` attend ce préfixe sur les textes INDEXÉS d'un corpus de recherche —
# c'est ainsi qu'il a été entraîné, et l'omettre dégrade la récupération sans
# rien casser de visible. Les REQUÊTES, elles, prennent un préfixe différent
# (voir `embed_query`), et confondre les deux est la faute classique.
PASSAGE_PREFIX = ""
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def load_model():
    """Charge le modèle, en disant ce qu'il télécharge la première fois."""
    from fastembed import TextEmbedding

    print(f"Modèle : {MODEL} ({MODEL_DIM} dimensions, local, CPU)")
    print("Premier lancement : ~0,21 Go téléchargés puis mis en cache.\n", flush=True)
    model = TextEmbedding(model_name=MODEL)
    return model


def embed_texts(model, textes: list[str]) -> list[list[float]]:
    vecteurs = [v.tolist() for v in model.embed([PASSAGE_PREFIX + t for t in textes])]
    for v in vecteurs:
        if len(v) != MODEL_DIM:
            raise VectorDBError(
                f"le modèle rend {len(v)} dimensions, la colonne en attend "
                f"{MODEL_DIM} — migration et modèle ont divergé"
            )
    return vecteurs


def embed_query(model, texte: str) -> list[float]:
    """Le vecteur d'une REQUÊTE. Préfixe différent de celui des passages."""
    return next(iter(model.embed([QUERY_PREFIX + texte]))).tolist()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Embeddings locaux — bge-base-en-v1.5")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args(argv)

    if DEFAULT_DIM != MODEL_DIM:
        print(f"ARRÊT : le client attend {DEFAULT_DIM} dimensions, le modèle en "
              f"rend {MODEL_DIM}. Aligner la migration et `DEFAULT_DIM`.")
        return 1

    with VectorDB.from_env() as db:
        with db.conn.cursor() as cur:
            cur.execute("select count(*) from chunks where embedding is null")
            restants = cur.fetchone()["count"]
            cur.execute("select count(*) from chunks where embedding is not null")
            faits = cur.fetchone()["count"]

        print(f"  {faits} morceau(x) déjà vectorisé(s), {restants} à faire")
        if a.limit:
            restants = min(restants, a.limit)
            print(f"  --limit : on s'arrête à {restants}")
        if not restants:
            print("\nRien à faire.")
            return 0
        if a.dry_run:
            print("\n--dry-run : ni modèle chargé, ni base écrite.")
            return 0

        model = load_model()
        depart = time.time()
        traites = 0

        while traites < restants:
            with db.conn.cursor() as cur:
                cur.execute(
                    "select id, content from chunks where embedding is null "
                    "order by paper_id, ordinal limit %s",
                    (min(BATCH, restants - traites),),
                )
                lot = cur.fetchall()
            if not lot:
                break

            vecteurs = embed_texts(model, [r["content"] for r in lot])
            with db.conn.transaction(), db.conn.cursor() as cur:
                cur.executemany(
                    "update chunks set embedding = %s::vector, embedding_model = %s "
                    "where id = %s",
                    [(to_pgvector(v, MODEL_DIM), MODEL, r["id"])
                     for v, r in zip(vecteurs, lot, strict=True)],
                )
            traites += len(lot)
            ecoule = time.time() - depart
            reste = (restants - traites) * ecoule / max(traites, 1)
            print(f"  {traites:>5}/{restants}  {traites / ecoule:>5.1f} morceaux/s"
                  f"  reste ~{reste / 60:.1f} min", flush=True)

        print(f"\n{traites} morceaux vectorisés en {(time.time() - depart) / 60:.1f} min")

        with db.conn.cursor() as cur:
            cur.execute("select embedding_model, count(*) from chunks "
                        "where embedding is not null group by 1")
            for row in cur.fetchall():
                print(f"  {row['count']} morceaux sous « {row['embedding_model']} »")
            cur.execute("select count(*) from chunks where embedding is null")
            manquants = cur.fetchone()["count"]
        if manquants:
            print(f"  {manquants} encore sans embedding — relancer reprend là.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
