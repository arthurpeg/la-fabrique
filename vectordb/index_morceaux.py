"""Retirer puis reconstruire l'index de similarité des morceaux — sans toucher aux données.

L'index est un IVFFlat (`chunks_embedding_ivfflat`, migration 007, `D46`) : le
HNSW de la migration 001 ne se construisait pas sur la petite instance. Un
IVFFlat ne s'adapte pas aux vecteurs ajoutés après lui : après une grosse
ingestion, le reconstruire.

Historique : le HNSW se mettait à jour à chaque
embedding écrit. Le 2026-09-30, avec ~90 000 vecteurs déjà indexés, la petite
instance Supabase n'a plus suivi : un lot de 64 morceaux toutes les ~20 minutes,
des délais dépassés, des connexions fermées. La pratique pour un remplissage en
masse : retirer l'index, écrire les vecteurs, le reconstruire en une fois.

**Aucune donnée n'est touchée.** L'index est une structure de recherche
calculée à partir des embeddings stockés ; le retirer laisse intacts papiers,
morceaux et vecteurs. Sans lui, une recherche par similarité reste exacte, mais
lente (parcours complet). La reconstruction reprend **la définition de la
migration 007**, lue dans le fichier, jamais recopiée.

    python vectordb/index_morceaux.py --etat
    python vectordb/index_morceaux.py --retirer
    python vectordb/index_morceaux.py --reconstruire
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from vector_db import VectorDB  # noqa: E402

NOM = "chunks_embedding_ivfflat"
MIGRATION = HERE / "migrations" / "007_index_ivfflat.sql"


def definition() -> str:
    """Le `create index` de la migration 007, tel qu'il y est écrit."""
    sql = MIGRATION.read_text(encoding="utf-8")
    m = re.search(rf"create index if not exists {NOM} on chunks\s+using \w+[^;]+;", sql)
    if not m:
        raise SystemExit(f"définition de {NOM} introuvable dans {MIGRATION.name}")
    return m.group(0)


def existe(db: VectorDB) -> bool:
    with db.conn.cursor() as cur:
        cur.execute("select 1 from pg_indexes where indexname = %s", (NOM,))
        return cur.fetchone() is not None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Index de similarité des morceaux")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--etat", action="store_true")
    g.add_argument("--retirer", action="store_true")
    g.add_argument("--reconstruire", action="store_true")
    a = ap.parse_args(argv)

    db = VectorDB.from_env()
    try:
        with db.conn.cursor() as cur:
            cur.execute("set statement_timeout = '180min'")
        if a.etat:
            print(f"{NOM} : {'présent' if existe(db) else 'ABSENT'}")
            print(f"définition (migration 007) : {definition()}")
            return 0
        if a.retirer:
            if not existe(db):
                print(f"{NOM} est déjà absent")
                return 0
            with db.conn.cursor() as cur:
                cur.execute(f"drop index {NOM}")
            db.conn.commit()
            print(f"{NOM} retiré. Les données sont intactes ; les recherches par similarité "
                  "seront lentes jusqu'à la reconstruction.")
            return 0
        if existe(db):
            # Une construction interrompue (le 2026-10-01, l'éditeur SQL du tableau
            # de bord a coupé la requête) peut laisser un index INVALIDE : il porte
            # le bon nom, ne sert à rien, et `if not exists` le sauterait.
            with db.conn.cursor() as cur:
                cur.execute("select i.indisvalid from pg_index i join pg_class c "
                            "on c.oid = i.indexrelid where c.relname = %s", (NOM,))
                ligne = cur.fetchone()
            if ligne and ligne["indisvalid"]:
                print(f"{NOM} est déjà présent et valide : rien à reconstruire")
                return 0
            print(f"{NOM} existe mais est INVALIDE (construction interrompue) : on le retire")
            with db.conn.cursor() as cur:
                cur.execute(f"drop index {NOM}")
            db.conn.commit()
        sql = definition()
        print(f"reconstruction : {sql}")
        t0 = time.time()
        with db.conn.cursor() as cur:
            # La petite instance n'a pas la mémoire partagée de 512 Mo, ni d'un
            # travail en parallèle (« No space left on device », 2026-10-01) :
            # 128 Mo, un seul processus. Plus lent, mais ça tient.
            cur.execute("set maintenance_work_mem = '128MB'")
            cur.execute("set max_parallel_maintenance_workers = 0")
            cur.execute(sql)
        db.conn.commit()
        print(f"{NOM} reconstruit en {(time.time() - t0) / 60:.1f} min")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
