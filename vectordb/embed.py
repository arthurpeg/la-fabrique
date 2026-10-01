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

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vector_db import DEFAULT_DIM, VectorDB, VectorDBError, to_pgvector  # noqa: E402

MODEL = "BAAI/bge-base-en-v1.5"
MODEL_DIM = 768
BATCH = 64

# Au-dela, ce n'est plus une coupure passagere mais une panne : on s'arrete
# au lieu de marteler un service qui ne repond plus.
MAX_COUPURES = 40

# `bge` attend ce préfixe sur les textes INDEXÉS d'un corpus de recherche —
# c'est ainsi qu'il a été entraîné, et l'omettre dégrade la récupération sans
# rien casser de visible. Les REQUÊTES, elles, prennent un préfixe différent
# (voir `embed_query`), et confondre les deux est la faute classique.
PASSAGE_PREFIX = ""
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def load_model(gpu: bool = False):
    """Charge le modèle, en disant ce qu'il télécharge la première fois.

    **`gpu`** (2026-09-29) : le même modèle, exécuté par `onnxruntime-gpu` sur
    la carte graphique. Il vit dans un environnement À PART (`.venv-gpu`), parce
    que `fastembed` et `fastembed-gpu` ne cohabitent pas :

        uv venv --python 3.13 .venv-gpu
        uv pip install --python .venv-gpu/Scripts/python.exe fastembed-gpu==0.8.1 \\
            "onnxruntime-gpu[cuda,cudnn]" "psycopg[binary]>=3.2" "numpy>=2.0"
        .venv-gpu/Scripts/python.exe vectordb/embed.py --gpu

    **Les vecteurs sont les mêmes**, et c'est ce qui autorise à garder le même
    nom de modèle dans `embedding_model` : mesuré sur 300 morceaux de la base,
    cosinus GPU/CPU ≥ 0,999992, écart absolu maximal 6,6e-4. Vitesse mesurée
    sur une RTX 4050 Laptop : 49,6 morceaux/s, contre 1,5 sur le processeur.
    """
    from fastembed import TextEmbedding

    if gpu:
        import onnxruntime as ort

        # Charge les bibliothèques CUDA/cuDNN installées par pip (`[cuda,cudnn]`).
        ort.preload_dlls()
        if "CUDAExecutionProvider" not in ort.get_available_providers():
            raise VectorDBError("--gpu : CUDA indisponible — lancer depuis .venv-gpu")
    print(f"Modèle : {MODEL} ({MODEL_DIM} dimensions, local, {'GPU' if gpu else 'CPU'})")
    print("Premier lancement : ~0,21 Go téléchargés puis mis en cache.\n", flush=True)
    kw = {"providers": ["CUDAExecutionProvider"]} if gpu else {}
    return TextEmbedding(model_name=MODEL, **kw)


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


HERE = Path(__file__).resolve().parent
# Le délai de requête par défaut du pooler Supabase ne suffit plus à ~140 000
# morceaux : le comptage initial le dépassait (2026-09-30). On l'allonge pour la
# session, et l'index partiel de la migration 004 rend ce comptage immédiat.
DELAI_REQUETE = "10min"


def connecter() -> VectorDB:
    db = VectorDB.from_env()
    with db.conn.cursor() as cur:
        cur.execute(f"set statement_timeout = '{DELAI_REQUETE}'")
    db.conn.commit()
    return db


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Embeddings locaux — bge-base-en-v1.5")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--gpu", action="store_true",
                    help="sur la carte graphique, depuis .venv-gpu (voir load_model)")
    ap.add_argument("--migrer-004", action="store_true",
                    help="créer l'index partiel des morceaux à vectoriser, puis s'arrêter")
    a = ap.parse_args(argv)

    if DEFAULT_DIM != MODEL_DIM:
        print(f"ARRÊT : le client attend {DEFAULT_DIM} dimensions, le modèle en "
              f"rend {MODEL_DIM}. Aligner la migration et `DEFAULT_DIM`.")
        return 1

    db = connecter()
    if a.migrer_004:
        sql = (HERE / "migrations" / "004_chunks_a_vectoriser.sql").read_text(encoding="utf-8")
        with db.conn.cursor() as cur:
            cur.execute("set statement_timeout = '60min'")
            cur.execute(sql)
        db.conn.commit()
        print("migration 004 appliquée : index partiel chunks_sans_embedding_idx")
        db.close()
        return 0
    try:
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

        model = load_model(a.gpu)
        depart = time.time()
        traites = 0
        coupures = 0

        while traites < restants:
            # LA CONNEXION TOMBE SUR UN TRAVAIL LONG, et il faut le prévoir :
            # le pooler de Supabase a fermé la nôtre après ~20 min au premier
            # essai (« server closed the connection unexpectedly »), à 16 % des
            # 10 219 morceaux. Le calcul lui-même dure plus d'une heure, donc
            # la coupure n'est pas un incident : c'est le régime normal.
            #
            # Rien n'est perdu : chaque lot est écrit avant le suivant, et la
            # requête ne prend que les `embedding is null`. Se reconnecter et
            # continuer suffit ; abandonner obligerait à relancer à la main
            # toutes les vingt minutes.
            try:
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
                # UNE requête par lot, pas une par morceau : à travers une
                # connexion lente, chaque aller-retour coûte (skill Supabase,
                # « batch » ; 2026-10-01). Les vecteurs voyagent en texte et se
                # convertissent côté base.
                with db.conn.transaction(), db.conn.cursor() as cur:
                    cur.execute(
                        "update chunks as c set embedding = v.e::vector, embedding_model = %s "
                        "from unnest(%s::uuid[], %s::text[]) as v(id, e) where c.id = v.id",
                        (MODEL, [r["id"] for r in lot],
                         [to_pgvector(v, MODEL_DIM) for v in vecteurs]),
                    )
            except psycopg.OperationalError as e:
                coupures += 1
                if coupures > MAX_COUPURES:
                    print(f"\n{coupures} coupures : on s'arrête. {traites} "
                          "morceaux sont écrits, relancer reprend là.")
                    raise
                print(f"  connexion perdue ({str(e).splitlines()[0][:52]}) — "
                      f"reconnexion {coupures}/{MAX_COUPURES}", flush=True)
                time.sleep(3)
                db.close()
                db = connecter()
                continue

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
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
