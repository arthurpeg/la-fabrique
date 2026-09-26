"""Récupérer les morceaux utiles d'un papier, au lieu de donner le papier entier.

**Le problème que ça résout, et il est chiffré.** Une consigne d'extraction pèse
11 000 à 39 000 tokens parce qu'elle porte le papier en entier. C'est ce qui a
fait échouer toutes les routes gratuites du 2026-09-25 : un cache KV de ~6 Go
hors de portée de 4 Go de VRAM en local, et un refus sec en HTTP 413 chez Groq,
dont le palier gratuit plafonne à **8 000 tokens par minute**.

Or une fiche ne s'appuie pas sur un papier entier : elle s'appuie sur une
dizaine de passages. La base vectorielle les a déjà découpés et vectorisés —
et elle ne servait pas à l'extraction.

**Les requêtes sont FIXES pour tous les papiers.** C'est la discipline de `D18` :
un texte choisi par papier serait un bouton qu'on tourne jusqu'à ce que la fiche
passe. Elles sont écrites ici, une fois, et ne se règlent pas au cas par cas.

**L'embedding est local et gratuit** — `BAAI/bge-base-en-v1.5` via `fastembed`,
le seul modèle que ce projet fait déjà tourner chez lui (`vectordb/embed.py`).
La récupération ne coûte donc rien.

**CE QUE CELA CHANGE POUR LA FICHE, et qui doit être dit dans la donnée.** Un
extracteur qui ne voit que des extraits **ne peut pas honnêtement remplir
`what_is_missing`** : il ignore ce que le papier ne dit pas, il ne connaît que
ce qui n'a pas été récupéré. Ce n'est pas un détail de formulation — c'est la
différence entre « le papier ne le dit pas » et « je ne l'ai pas lu ». La
consigne le dit au modèle, et une bascule en production demanderait une décision
écrite, du même genre que `D22` pour `papers.text_source`.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROMOTED = REPO / "corpus" / "harvest_promoted.json"

# LES CINQ REQUETES, une par famille de champs de la fiche (`D14`). Fixes pour
# tous les papiers, ecrites avant tout resultat. En changer une est une decision,
# pas un reglage — et elle perimerait les fiches produites avec les anciennes.
REQUETES = {
    "claim": "main hypothesis, central claim, what the paper predicts, key finding",
    "universe": "data sample, instruments, assets, period, frequency of observations",
    "horizon": "forecast horizon, holding period, prediction window, rebalancing",
    "construction": "how the signal or predictor is computed, formula, definition, method",
    "results": "empirical results, coefficients, t-statistics, Sharpe ratio, returns, table",
}


def paper_id_pour(fiche_id: str) -> str:
    """L'identifiant en base du papier, depuis le registre de promotion.

    `harvest_promoted.json` est le seul endroit qui relie un `fiche_id` (le nom
    du PDF) a l'uuid Postgres. Le deduire autrement — par titre normalise, par
    exemple — serait une SECONDE deduction de la meme chose, et deux deductions
    paralleles finissent toujours par diverger (`D24`, la cause de `G1`).
    """
    for ligne in json.loads(PROMOTED.read_text(encoding="utf-8")):
        if Path(ligne["pdf"]).stem == fiche_id:
            return ligne["paper_id"]
    raise SystemExit(f"{fiche_id!r} absent de corpus/harvest_promoted.json")


# LE PLAFOND EST UN COMPROMIS, PAS UN REGLAGE NEUTRE, et il faut le dire.
# Douze morceaux font une invite de ~7 700 tokens : elle ne tient sous les
# 8 000 par minute de Groq QUE si le seau est vide, et le moindre residu la
# fait refuser en 413 — constate le 2026-09-25 sur les cinq papiers. Huit
# morceaux laissent de la marge, au prix de ce que l'extracteur ne verra pas.
# Ce que ce chiffre achete est du DEBIT ; ce qu'il coute est de la COUVERTURE.
PLAFOND_MORCEAUX = 8


def morceaux_pour(
    fiche_id: str, par_requete: int = 3, plafond: int = PLAFOND_MORCEAUX
) -> list[dict]:
    """Les morceaux les plus proches des cinq requetes, dedoublonnes et REMIS EN ORDRE.

    L'ordre de lecture est retabli (`ordinal`) plutot que l'ordre de pertinence :
    un papier lu en desordre se cite mal, et les passages voisins s'eclairent.
    """
    import sys

    sys.path.insert(0, str(REPO / "vectordb"))
    from embed import embed_query, load_model  # type: ignore
    from vector_db import VectorDB, to_pgvector  # type: ignore

    pid = paper_id_pour(fiche_id)
    modele = load_model()
    trouves: dict[int, dict] = {}

    with VectorDB.from_env() as db:
        for nom, requete in REQUETES.items():
            vecteur = embed_query(modele, requete)
            with db.conn.cursor() as cur:
                cur.execute(
                    "select ordinal, content, page from chunks "
                    "where paper_id = %s and embedding is not null "
                    "order by embedding <=> %s::vector limit %s",
                    (pid, to_pgvector(vecteur, db.dim), par_requete),
                )
                for rang, row in enumerate(cur.fetchall()):
                    # Un morceau rendu par PLUSIEURS requetes est plus central :
                    # on garde son meilleur rang pour departager sous le plafond.
                    vu = trouves.get(row["ordinal"])
                    if vu is None or rang < vu["_rang"]:
                        trouves[row["ordinal"]] = {**row, "_rang": rang, "_requete": nom}

    retenus = sorted(trouves.values(), key=lambda m: (m["_rang"], m["ordinal"]))[:plafond]
    return sorted(retenus, key=lambda m: m["ordinal"])


def rendre(morceaux: list[dict]) -> str:
    """Les morceaux mis bout a bout, avec les TROUS MARQUES.

    Un extracteur qui ignore qu'il manque des passages croit lire un papier
    entier — et remplit `what_is_missing` comme s'il savait ce que le papier
    tait. La coupure est donc visible, numerotee, et nommee.
    """
    sorties: list[str] = []
    precedent: int | None = None
    for m in morceaux:
        if precedent is not None and m["ordinal"] != precedent + 1:
            manquants = m["ordinal"] - precedent - 1
            sorties.append(f"\n[… {manquants} passage(s) non récupéré(s) …]\n")
        sorties.append(m["content"])
        precedent = m["ordinal"]
    return "\n".join(sorties)
