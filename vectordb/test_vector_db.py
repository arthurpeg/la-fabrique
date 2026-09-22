"""Le test de bout en bout de la base vectorielle.

Il insère deux faux papiers, vérifie les trois fonctions de recherche, puis
**nettoie ce qu'il a écrit**, y compris si une vérification échoue. Un test
qui laisse ses données derrière lui rend le suivant ininterprétable.

Ce qu'il ne prétend PAS faire : juger la qualité des résultats. Des vecteurs
aléatoires n'ont aucune structure sémantique, donc l'ordre rendu ne veut rien
dire. Ce qui est vérifié, c'est que la plomberie répond, filtre et compte
juste — pas qu'elle trouve le bon papier.

    python vectordb/test_vector_db.py
"""

from __future__ import annotations

import random
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vector_db import (  # noqa: E402
    Chunk,
    DuplicatePaper,
    Paper,
    Strategy,
    VectorDB,
    VectorDBError,
)

SEED = 20260922  # fixe : deux exécutions doivent rendre les mêmes vecteurs


def fake_embedding(rng: random.Random, dim: int) -> list[float]:
    """Un vecteur unitaire aléatoire. Unitaire parce que la distance cosinus
    l'est aussi, et qu'un vecteur nul la rend indéfinie."""
    v = [rng.gauss(0.0, 1.0) for _ in range(dim)]
    norm = sum(x * x for x in v) ** 0.5 or 1.0
    return [x / norm for x in v]


class Checks:
    """Un compteur qui nomme ce qui a raté, plutôt qu'un `assert` qui arrête
    au premier — on veut la liste complète en une exécution."""

    def __init__(self) -> None:
        self.passed = 0
        self.failed: list[str] = []

    def that(self, label: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"  [ok ] {label}")
        else:
            self.failed.append(label)
            print(f"  [RATE] {label}{f' — {detail}' if detail else ''}")


def a_moi(rows: list[dict], *paper_ids: str) -> list[dict]:
    """Ne garde que les lignes des papiers de CE test.

    Le test ne possède pas la base. Il l'a cru, et s'est cassé dès qu'elle a
    contenu le vrai corpus : « backwardated commodity futures » touchait des
    morceaux réels par le plein texte, et un compte global ne valait plus rien.
    Les recherches vectorielles tenaient encore, mais par accident — les
    morceaux réels ont `embedding IS NULL` et en sont exclus.
    """
    connus = set(paper_ids)
    return [r for r in rows if r.get("paper_id") in connus]


def main() -> int:
    rng = random.Random(SEED)
    checks = Checks()
    written: list[str] = []

    try:
        db = VectorDB.from_env()
    except VectorDBError as e:
        print(f"connexion impossible : {e}")
        return 1

    dim = db.dim
    print(f"base ouverte, dimension {dim}\n")

    try:
        # -- insertion ----------------------------------------------------
        print("Insertion")
        p1 = db.insert_paper(Paper(
            title="Market intraday momentum in index futures",
            authors=["Ada Lovelace", "Alan Turing"],
            year=2018,
            doi="10.9999/test.0001",
            pdf_url="https://example.invalid/p1.pdf",
            abstract="First half-hour return predicts the last half-hour return.",
        ))
        written.append(p1)
        checks.that("papier 1 inséré", bool(p1))

        p2 = db.insert_paper(Paper(
            title="Carry and term structure in commodity markets",
            authors=["Grace Hopper"],
            year=2013,
            doi="10.9999/test.0002",
            abstract="Roll yield explains the cross-section of commodity returns.",
        ))
        written.append(p2)
        checks.that("papier 2 inséré", bool(p2) and p2 != p1)

        # -- dédoublonnage ------------------------------------------------
        print("\nDédoublonnage")
        try:
            db.insert_paper(Paper(title="peu importe", doi="10.9999/test.0001"))
            checks.that("un DOI déjà présent est refusé", False, "aucune erreur levée")
        except DuplicatePaper as e:
            checks.that("un DOI déjà présent est refusé", e.paper_id == p1)

        try:
            db.insert_paper(Paper(title="MARKET  Intraday!! Momentum in Index Futures"))
            checks.that("un titre équivalent est refusé", False, "aucune erreur levée")
        except DuplicatePaper as e:
            checks.that("un titre équivalent est refusé (normalisation)",
                        e.paper_id == p1)

        same = db.insert_paper(Paper(title="peu importe", doi="10.9999/test.0001"),
                               on_duplicate="return_existing")
        checks.that("`return_existing` rend l'id existant", same == p1)

        # -- durabilité ---------------------------------------------------
        # LA vérification qui manquait. Relire sur la même connexion ne prouve
        # rien : une transaction non validée voit ses propres écritures. Il a
        # fallu une SECONDE connexion pour découvrir que tout était annulé au
        # `close()` — l'ingestion annonçait quatre papiers, la base en avait
        # zéro. Une écriture n'est écrite que lorsqu'un AUTRE la voit.
        print("\nDurabilité (seconde connexion)")
        with VectorDB.from_env() as autre:
            vu = autre.find_existing_paper(doi="10.9999/test.0001")
        checks.that("le papier 1 est visible d'une autre connexion",
                    vu == p1, f"vu={vu!r}")

        # -- morceaux -----------------------------------------------------
        print("\nMorceaux")
        chunks_1 = [
            Chunk(content="We document market intraday momentum in equity index "
                          "futures across nine markets.",
                  ordinal=0, section="intro", page=1,
                  embedding=fake_embedding(rng, dim), embedding_model="test-rand-v1"),
            Chunk(content="We regress the last half-hour return on the first "
                          "half-hour return using intraday data.",
                  ordinal=1, section="methodology", page=4,
                  embedding=fake_embedding(rng, dim), embedding_model="test-rand-v1"),
            Chunk(content="The predictive coefficient is positive and significant "
                          "with a t-statistic above three.",
                  ordinal=2, section="results", page=9,
                  embedding=fake_embedding(rng, dim), embedding_model="test-rand-v1"),
        ]
        n1 = db.insert_chunks(p1, chunks_1)
        checks.that("3 morceaux insérés pour le papier 1", n1 == 3, f"rendu {n1}")

        n2 = db.insert_chunks(p2, [
            Chunk(content="Carry predicts commodity futures returns in the "
                          "cross-section and in the time series.",
                  ordinal=0, section="results", page=2,
                  embedding=fake_embedding(rng, dim), embedding_model="test-rand-v1"),
        ])
        checks.that("1 morceau inséré pour le papier 2", n2 == 1)

        # -- garde de provenance -----------------------------------------
        print("\nGarde de provenance")
        try:
            db.insert_chunks(p2, [Chunk(content="vecteur sans modèle", ordinal=99,
                                        embedding=fake_embedding(rng, dim))])
            checks.that("un vecteur sans son modèle est refusé", False,
                        "aucune erreur levée")
        except Exception:
            checks.that("un vecteur sans son modèle est refusé", True)

        try:
            db.insert_chunks(p2, [Chunk(content="mauvaise taille", ordinal=98,
                                        embedding=[0.0] * (dim + 1),
                                        embedding_model="test-rand-v1")])
            checks.that("une dimension fausse est refusée", False,
                        "aucune erreur levée")
        except VectorDBError:
            checks.that("une dimension fausse est refusée, et NOMMÉE", True)

        # -- stratégies ---------------------------------------------------
        print("\nStratégies")
        s1 = db.insert_strategy(p1, Strategy(
            asset="S&P500", strategy_type="momentum",
            signals="Long if the first half-hour return is positive.",
            period_start=date(1999, 1, 1), period_end=date(2016, 12, 31),
            sharpe_ratio=0.87, limitations="Costs excluded.",
            embedding=fake_embedding(rng, dim), embedding_model="test-rand-v1"))
        checks.that("stratégie avec Sharpe insérée", bool(s1))

        s2 = db.insert_strategy(p2, Strategy(
            asset="oil", strategy_type="carry",
            signals="Long backwardated contracts.",
            sharpe_ratio=None,  # le papier ne le donne pas : NULL, pas 0.0
            embedding=fake_embedding(rng, dim), embedding_model="test-rand-v1"))
        checks.that("stratégie SANS Sharpe insérée (NULL assumé)", bool(s2))

        # -- recherche vectorielle ----------------------------------------
        print("\nRecherche vectorielle")
        q = fake_embedding(rng, dim)
        r = a_moi(db.vector_search(q, match_count=40), p1, p2)
        checks.that("rend les 4 morceaux", len(r) == 4, f"rendu {len(r)}")
        checks.that("chaque ligne porte le titre du papier",
                    all(row["title"] for row in r))
        checks.that("similarité dans [-1, 1]",
                    all(-1.000001 <= row["similarity"] <= 1.000001 for row in r))
        checks.that("ordre décroissant de similarité",
                    all(r[i]["similarity"] >= r[i + 1]["similarity"]
                        for i in range(len(r) - 1)))

        r = a_moi(db.vector_search(q, match_count=40, section="methodology"), p1, p2)
        checks.that("filtre `section` appliqué",
                    len(r) == 1 and r[0]["section"] == "methodology", f"rendu {len(r)}")

        r = a_moi(db.vector_search(q, match_count=40, year_min=2015), p1, p2)
        checks.that("filtre `year_min` appliqué", len(r) == 3, f"rendu {len(r)}")

        r = db.vector_search(q, match_count=2)
        checks.that("`match_count` respecté", len(r) == 2, f"rendu {len(r)}")

        # -- recherche hybride --------------------------------------------
        print("\nRecherche hybride (RRF)")
        r = a_moi(db.hybrid_search("intraday momentum futures", q, match_count=60), p1, p2)
        checks.that("rend des résultats", len(r) > 0, f"rendu {len(r)}")
        checks.that("chaque ligne porte contenu, score, titre et page",
                    all({"content", "score", "title", "page"} <= set(row) for row in r))
        checks.that("score strictement positif", all(row["score"] > 0 for row in r))
        checks.that("score borné par 2/(k+1)",
                    all(row["score"] <= 2.0 / 61 + 1e-9 for row in r))
        checks.that("ordre décroissant de score",
                    all(r[i]["score"] >= r[i + 1]["score"] for i in range(len(r) - 1)))

        hit = a_moi(db.hybrid_search("commodity futures carry", q, match_count=60), p1, p2)
        checks.that("le plein texte remonte le bon papier",
                    any(row["paper_id"] == p2 for row in hit))

        # `websearch_to_tsquery` combine les termes en ET. Un seul mot absent
        # du morceau, et le plein texte ne rend RIEN — le classement retombe
        # alors sur le seul vectoriel. Ce n'est pas un défaut, c'est le
        # comportement à connaître avant d'écrire une requête.
        #
        # Vérifié ici parce que la première rédaction de ce test l'ignorait :
        # elle cherchait « backwardated contracts carry » alors que
        # « backwardated » vit dans `strategies.signals`, qui n'est PAS indexé
        # par `chunks.tsv`. Le test échouait, le code avait raison.
        et = a_moi(db.hybrid_search("backwardated commodity futures", q, match_count=60), p1, p2)
        checks.that("un terme absent annule le plein texte (sémantique ET)",
                    len(et) == 4, f"rendu {len(et)}")

        none = a_moi(db.hybrid_search("zzzzqqqq inexistant", q, match_count=60), p1, p2)
        checks.that("un texte sans correspondance rend quand même le vectoriel",
                    len(none) == 4, f"rendu {len(none)}")

        # -- recherche de stratégies --------------------------------------
        print("\nRecherche de stratégies")
        r = a_moi(db.strategy_search(q, match_count=40), p1, p2)
        checks.that("rend les 2 stratégies", len(r) == 2, f"rendu {len(r)}")

        r = a_moi(db.strategy_search(q, match_count=40, asset="oil"), p1, p2)
        checks.that("filtre `asset` appliqué", len(r) == 1 and r[0]["asset"] == "oil")

        r = a_moi(db.strategy_search(q, match_count=40, strategy_type="momentum"), p1, p2)
        checks.that("filtre `strategy_type` appliqué", len(r) == 1)

        r = a_moi(db.strategy_search(q, match_count=40, sharpe_min=0.5), p1, p2)
        checks.that("`sharpe_min` garde celle qui dépasse", len(r) == 1)

        r = a_moi(db.strategy_search(q, match_count=40, sharpe_min=2.0), p1, p2)
        checks.that("`sharpe_min` EXCLUT la stratégie sans Sharpe",
                    len(r) == 0, f"rendu {len(r)}")

        # -- suppression en cascade ---------------------------------------
        print("\nSuppression en cascade")
        checks.that("le papier 2 est supprimé", db.delete_paper(p2))
        written.remove(p2)
        checks.that("supprimer deux fois rend False", not db.delete_paper(p2))
        r = a_moi(db.vector_search(q, match_count=40), p1, p2)
        checks.that("ses morceaux sont partis avec lui", len(r) == 3, f"rendu {len(r)}")
        r = a_moi(db.strategy_search(q, match_count=40), p1, p2)
        checks.that("ses stratégies aussi", len(r) == 1, f"rendu {len(r)}")

    finally:
        # Le nettoyage passe MÊME si une vérification a levé : sans lui, la
        # prochaine exécution butera sur les doublons qu'on vient d'écrire.
        for pid in written:
            try:
                db.delete_paper(pid)
            except Exception as e:  # noqa: BLE001
                print(f"  nettoyage incomplet pour {pid} : {e}")
        db.close()

    total = checks.passed + len(checks.failed)
    print(f"\n{checks.passed} / {total} vérifications")
    if checks.failed:
        print("ÉCHECS : " + ", ".join(checks.failed))
        return 1
    print("BASE VECTORIELLE : les trois recherches répondent, filtrent et comptent juste.")
    print("Ce test ne dit RIEN de la pertinence : les vecteurs sont aléatoires.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
