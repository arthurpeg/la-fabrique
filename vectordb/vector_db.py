"""Le client de la base vectorielle des papiers de recherche.

Il fait UNE chose : parler à PostgreSQL. Il n'extrait aucun PDF, n'appelle
aucun modèle d'embedding, ne découpe aucun texte. Les vecteurs lui arrivent
tout faits ; il les range et les retrouve.

**Les embeddings sont passés en chaîne `'[0.1,0.2,...]'`**, forme que pgvector
lit nativement. C'est un choix : le paquet `pgvector` pour Python ferait la
même chose en ajoutant une dépendance, et cette sérialisation-là est stable
quelle que soit la version du pilote.

**Un vecteur voyage toujours avec le nom de son modèle.** La base le refuse
autrement (`chunks_embedding_provenance`), parce qu'une colonne qui mélange
deux modèles ne le dit jamais d'elle-même.

    from vector_db import VectorDB

    with VectorDB.from_env() as db:
        paper_id = db.insert_paper(Paper(title="...", year=2018))
        db.insert_chunks(paper_id, chunks)
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Literal
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

Section = Literal["intro", "methodology", "results", "conclusion", "other"]
StrategyType = Literal["momentum", "carry", "mean_reversion", "other"]

DEFAULT_DIM = 1536


class VectorDBError(RuntimeError):
    """Toute faute venant de cette couche, nommée plutôt que propagée nue."""


class DuplicatePaper(VectorDBError):
    """Le papier est déjà en base. Porte l'`id` de celui qui existe."""

    def __init__(self, paper_id: str, reason: str) -> None:
        super().__init__(f"papier déjà présent ({reason}) : {paper_id}")
        self.paper_id = paper_id
        self.reason = reason


# ---------------------------------------------------------------------------
# Les charges utiles. Des dataclasses plutôt que des dicts : un champ mal
# orthographié devient une erreur à l'appel, pas une colonne silencieusement
# absente à l'insertion.
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class Paper:
    title: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    doi: str | None = None
    pdf_url: str | None = None
    abstract: str | None = None


@dataclass(slots=True)
class Chunk:
    content: str
    ordinal: int
    section: Section = "other"
    page: int | None = None
    embedding: Sequence[float] | None = None
    embedding_model: str | None = None


@dataclass(slots=True)
class Strategy:
    asset: str
    strategy_type: StrategyType = "other"
    signals: str | None = None
    period_start: date | None = None
    period_end: date | None = None
    sharpe_ratio: float | None = None
    limitations: str | None = None
    embedding: Sequence[float] | None = None
    embedding_model: str | None = None


def _stringify_ids(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ramène tout identifiant à une chaîne.

    Sans cela l'API parle DEUX langues : `insert_paper` rend un `str`, les
    recherches rendaient un `uuid.UUID`, et `row["paper_id"] == paper_id`
    valait `False` **en silence**. Trouvé en exécutant le test contre une vraie
    base — aucune analyse statique ne l'aurait vu.
    """
    for row in rows:
        for key, value in row.items():
            if isinstance(value, UUID):
                row[key] = str(value)
    return rows


def to_pgvector(values: Sequence[float] | None, dim: int = DEFAULT_DIM) -> str | None:
    """Sérialise un vecteur pour pgvector, en vérifiant sa dimension ICI.

    Sans ce contrôle, un vecteur de mauvaise taille est refusé par Postgres
    avec un message qui ne dit pas lequel des mille de l'insertion par lot est
    fautif. Le vérifier au bord rend l'erreur lisible.
    """
    if values is None:
        return None
    if len(values) != dim:
        raise VectorDBError(
            f"dimension {len(values)}, attendu {dim} — la colonne est figée par "
            "le DDL, voir l'en-tête de la migration"
        )
    return "[" + ",".join(repr(float(v)) for v in values) + "]"


# ---------------------------------------------------------------------------
# Le client
# ---------------------------------------------------------------------------

class VectorDB:
    """Une connexion et les gestes qu'on lui demande.

    L'objet ne valide rien que la base puisse valider elle-même : les
    contraintes vivent dans le schéma, où elles s'appliquent à TOUS les
    clients, et non dans celui-ci, où elles ne protégeraient que lui.
    """

    def __init__(self, conn: psycopg.Connection, dim: int = DEFAULT_DIM) -> None:
        self.conn = conn
        self.dim = dim

    # -- cycle de vie ------------------------------------------------------

    @classmethod
    def from_env(cls, dim: int | None = None) -> VectorDB:
        """Ouvre une connexion depuis l'environnement.

        `DATABASE_URL` d'abord — c'est ce que Supabase donne. À défaut, les
        variables séparées. Aucune valeur par défaut pour le mot de passe :
        un identifiant deviné est un identifiant qui finit dans un dépôt.
        """
        dsn = os.environ.get("DATABASE_URL", "").strip()
        if not dsn:
            missing = [k for k in ("PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD")
                       if not os.environ.get(k)]
            if missing:
                raise VectorDBError(
                    "connexion impossible : ni DATABASE_URL ni "
                    f"{', '.join(missing)} — voir vectordb/README.md"
                )
            dsn = (f"host={os.environ['PGHOST']} port={os.environ.get('PGPORT', 5432)} "
                   f"dbname={os.environ['PGDATABASE']} user={os.environ['PGUSER']} "
                   f"password={os.environ['PGPASSWORD']}")
        env_dim = os.environ.get("EMBEDDING_DIM")
        resolved = dim or (int(env_dim) if env_dim else DEFAULT_DIM)
        return cls(psycopg.connect(dsn, row_factory=dict_row), resolved)

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> VectorDB:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @contextmanager
    def _tx(self):
        """Une transaction, un curseur. Tout ou rien.

        Une insertion par lot à moitié écrite est pire qu'une insertion
        refusée : elle laisse un papier avec la moitié de ses morceaux, et
        rien ne dit lesquels manquent.
        """
        with self.conn.transaction(), self.conn.cursor() as cur:
            yield cur

    # -- lecture -----------------------------------------------------------

    def find_existing_paper(self, doi: str | None = None,
                            title: str | None = None) -> str | None:
        """L'id d'un papier déjà en base, par DOI puis par titre normalisé.

        La normalisation du titre est celle de la colonne GÉNÉRÉE : on
        interroge `title_norm` avec la même expression, pour que le client et
        la contrainte d'unicité ne puissent pas diverger.
        """
        with self.conn.cursor() as cur:
            if doi:
                cur.execute("select id from papers where doi = %s", (doi,))
                if (row := cur.fetchone()):
                    return str(row["id"])
            if title:
                cur.execute(
                    "select id from papers where title_norm = "
                    "trim(lower(regexp_replace(%s, '[^a-zA-Z0-9]+', ' ', 'g')))",
                    (title,),
                )
                if (row := cur.fetchone()):
                    return str(row["id"])
        return None

    # -- écriture ----------------------------------------------------------

    def insert_paper(self, paper: Paper, *, on_duplicate: str = "raise") -> str:
        """Insère un papier et rend son id.

        `on_duplicate` vaut `raise` (défaut) ou `return_existing`. Il n'y a
        PAS de mode « écraser » : remplacer un papier supprimerait ses
        morceaux en cascade, ce qui ne doit jamais arriver par inadvertance.
        """
        if on_duplicate not in ("raise", "return_existing"):
            raise VectorDBError(f"on_duplicate inconnu : {on_duplicate!r}")

        existing = self.find_existing_paper(paper.doi, paper.title)
        if existing:
            if on_duplicate == "return_existing":
                return existing
            raise DuplicatePaper(existing, "DOI" if paper.doi else "titre")

        with self._tx() as cur:
            cur.execute(
                """
                insert into papers (title, authors, year, doi, pdf_url, abstract)
                values (%s, %s, %s, %s, %s, %s)
                returning id
                """,
                (paper.title, list(paper.authors), paper.year, paper.doi,
                 paper.pdf_url, paper.abstract),
            )
            return str(cur.fetchone()["id"])

    def insert_chunks(self, paper_id: str, chunks: Sequence[Chunk]) -> int:
        """Insère les morceaux d'un papier, EN UNE transaction.

        `executemany` est envoyé en pipeline par psycopg 3 : un aller-retour
        pour le lot, pas un par ligne.
        """
        if not chunks:
            return 0
        rows = [
            (paper_id, c.content, c.section, c.page, c.ordinal,
             to_pgvector(c.embedding, self.dim), c.embedding_model)
            for c in chunks
        ]
        with self._tx() as cur:
            cur.executemany(
                """
                insert into chunks
                    (paper_id, content, section, page, ordinal,
                     embedding, embedding_model)
                values (%s, %s, %s, %s, %s, %s::vector, %s)
                """,
                rows,
            )
        return len(rows)

    def insert_strategy(self, paper_id: str, strategy: Strategy) -> str:
        """Insère une stratégie extraite d'un papier et rend son id."""
        with self._tx() as cur:
            cur.execute(
                """
                insert into strategies
                    (paper_id, asset, strategy_type, signals, period_start,
                     period_end, sharpe_ratio, limitations, embedding,
                     embedding_model)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s::vector, %s)
                returning id
                """,
                (paper_id, strategy.asset, strategy.strategy_type,
                 strategy.signals, strategy.period_start, strategy.period_end,
                 strategy.sharpe_ratio, strategy.limitations,
                 to_pgvector(strategy.embedding, self.dim),
                 strategy.embedding_model),
            )
            return str(cur.fetchone()["id"])

    def delete_paper(self, paper_id: str) -> bool:
        """Supprime un papier ET, en cascade, ses morceaux et stratégies.

        Rend `False` si rien n'a été supprimé — un appelant qui croit avoir
        nettoyé et ne l'a pas fait est un bogue silencieux.
        """
        with self._tx() as cur:
            cur.execute("delete from papers where id = %s", (paper_id,))
            return cur.rowcount > 0

    # -- recherche ---------------------------------------------------------

    def vector_search(
        self,
        query_embedding: Sequence[float],
        match_count: int = 10,
        year_min: int | None = None,
        year_max: int | None = None,
        section: Section | None = None,
    ) -> list[dict[str, Any]]:
        """Recherche par similarité cosinus seule."""
        with self.conn.cursor() as cur:
            cur.execute(
                "select * from vector_search(%s::vector, %s, %s, %s, %s::section_type)",
                (to_pgvector(query_embedding, self.dim), match_count,
                 year_min, year_max, section),
            )
            return _stringify_ids(cur.fetchall())

    def hybrid_search(
        self,
        query_text: str,
        query_embedding: Sequence[float],
        match_count: int = 10,
        year_min: int | None = None,
        year_max: int | None = None,
        section: Section | None = None,
        rrf_k: int = 60,
    ) -> list[dict[str, Any]]:
        """Plein texte et vectoriel, fusionnés par Reciprocal Rank Fusion.

        Le `score` rendu n'est PAS une similarité et ne se compare pas d'une
        requête à l'autre : c'est une somme d'inverses de rangs, bornée par
        `2/(k+1)`. Il ordonne, il ne mesure pas.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "select * from hybrid_search(%s, %s::vector, %s, %s, %s, "
                "%s::section_type, %s)",
                (query_text, to_pgvector(query_embedding, self.dim), match_count,
                 year_min, year_max, section, rrf_k),
            )
            return _stringify_ids(cur.fetchall())

    def strategy_search(
        self,
        query_embedding: Sequence[float],
        match_count: int = 10,
        asset: str | None = None,
        strategy_type: StrategyType | None = None,
        sharpe_min: float | None = None,
    ) -> list[dict[str, Any]]:
        """Recherche de stratégies.

        `sharpe_min` non nul EXCLUT les stratégies sans Sharpe : un nombre
        absent ne se compare pas, et les garder traiterait « inconnu » comme
        « au-dessus du seuil ».
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "select * from strategy_search(%s::vector, %s, %s, "
                "%s::strategy_type, %s)",
                (to_pgvector(query_embedding, self.dim), match_count,
                 asset, strategy_type, sharpe_min),
            )
            return _stringify_ids(cur.fetchall())
