"""`D14` — le garde des fiches, montré en train de refuser.

`corpus/validate_fiches.py` accepte les trois fiches écrites à la main, et une
fiche qui satisfait un garde ne prouve rien : ce qu'il faut voir, c'est le refus.
Ce script fabrique donc des fiches délibérément fautives — à partir d'une vraie,
en mémoire, jamais sur disque — et vérifie que chacune est refusée **pour la
raison écrite d'avance**.

Même discipline que `scripts/check_provenance.py` pour le catalogue et
`sandbox/tainted.py` pour les look-ahead. **Un garde qui n'a jamais rien refusé
est un garde que personne n'a testé** — et celui du catalogue s'est fait prendre
ainsi, sur `12500` contre `12,500,000` (ledger F26).

    python corpus/check_fiches_guard.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "corpus"))

from validate_fiches import check_fiche  # noqa: E402

REFERENCE = REPO / "corpus" / "fiches" / "andersen-bollerslev-1997-periodicity.json"
NAME = REFERENCE.stem


def first_numeric(fiche: dict) -> dict:
    """La première entrée de résultat qui porte un nombre vérifiable."""
    for entry in fiche["reported_results"]:
        if isinstance(entry.get("value"), (int, float)) and not entry.get("derived"):
            if "spelled_out" not in entry:
                return entry
    raise LookupError("la fiche de référence ne porte aucun nombre vérifiable")


# -- les cas, et la raison attendue de chaque refus --------------------------

def case_champ_absent(f):
    del f["transposability"]


def case_horizon_null_nu(f):
    f["horizon"] = {"value": None}


def case_resultat_sans_citation(f):
    first_numeric(f)["quoted"] = "   "


def case_faute_de_recopie(f):
    entry = first_numeric(f)
    entry["value"] = float(entry["value"]) * 10


def case_derive_sans_note(f):
    entry = first_numeric(f)
    entry["derived"] = True
    entry.pop("note", None)


def case_mot_absent(f):
    entry = first_numeric(f)
    entry["spelled_out"] = "Seventeen"


def case_tout_transfere(f):
    f["transposability"]["what_does_not_transfer"] = []


def case_source_sans_url(f):
    f["source"]["source_url"] = "relevé à la main"


def case_preprint_non_declare(f):
    f["source"]["peer_reviewed"] = "oui"


def case_nom_incoherent(f):
    f["fiche_id"] = "une-autre-fiche"


def case_resultats_vides(f):
    f["reported_results"] = []


def case_reparation_sans_motif(f):
    """Une réparation déclarée sans dire POURQUOI : l'échappatoire générique."""
    entry = first_numeric(f)
    entry["quoted_source"] = entry["quoted"]


def case_motif_hors_liste(f):
    """Un motif de réparation inventé : la liste de `D16` est CLOSE."""
    entry = first_numeric(f)
    entry["quoted_source"] = entry["quoted"]
    entry["quoted_repair"] = "extraction_bizarre"


def case_motif_sans_reparation(f):
    """Un motif sans chaine source : rien n'est réparé, le champ ment."""
    first_numeric(f)["quoted_repair"] = "ocr"


def case_chiffre_loge_dans_la_lisible(f):
    """LA FAUTE QUE `D16` AVAIT NOMMÉE SANS LA FERMER.

    Le nombre est dans `quoted`, lisible, et ABSENT de `quoted_source`, qui fait
    foi. Avant le 2026-09-21, `F1` l'acceptait et `F3` la refusait : le schéma
    était plus laxiste que le juge, et la réparation déclarée devenait l'endroit
    où loger un chiffre que le papier ne porte pas.
    """
    entry = first_numeric(f)
    entry["quoted_source"] = "une phrase du papier sans le moindre nombre dedans"
    entry["quoted_repair"] = "ocr"


def case_intact(f):
    return None


CASES = [
    ("un champ obligatoire retiré", case_champ_absent, "transposability", True),
    ("un horizon null sans raison", case_horizon_null_nu, "sans raison", True),
    ("un résultat sans citation", case_resultat_sans_citation, "quoted est vide", True),
    ("une valeur recopiée à un facteur dix près", case_faute_de_recopie,
     "introuvable dans sa citation", True),
    ("un nombre dérivé sans dire comment", case_derive_sans_note, "derived sans note", True),
    ("un nombre en toutes lettres, mais le mauvais mot", case_mot_absent,
     "introuvable dans la citation", True),
    ("un papier dont TOUT transfère", case_tout_transfere, "what_does_not_transfer", True),
    ("une source sans URL", case_source_sans_url, "source_url n'est pas une URL", True),
    ("un arbitrage par les pairs non booléen", case_preprint_non_declare,
     "peer_reviewed", True),
    ("un fiche_id qui ment sur le nom du fichier", case_nom_incoherent, "fiche_id", True),
    ("un papier qui n'annonce rien", case_resultats_vides, "reported_results est vide", True),
    ("une réparation déclarée sans motif", case_reparation_sans_motif,
     "quoted_repair valide", True),
    ("un motif de réparation hors de la liste close", case_motif_hors_liste,
     "quoted_repair valide", True),
    ("un motif sans chaine source", case_motif_sans_reparation,
     "sans quoted_source", True),
    ("un chiffre logé dans la version lisible, absent de la source",
     case_chiffre_loge_dans_la_lisible, "introuvable dans sa citation", True),
    ("la fiche intacte", case_intact, None, False),
]


def main() -> int:
    reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    print(f"fiche de référence : {NAME}\n")
    for label, damage, expected, must_fail in CASES:
        broken = copy.deepcopy(reference)
        damage(broken)
        refusals = check_fiche(NAME, broken)
        if must_fail:
            check(bool(refusals), f"{label} : ACCEPTÉE, alors qu'elle devait être refusée")
            named = any(expected in line for line in refusals)
            check(named, f"{label} : refusée, mais pour une autre raison — {refusals}")
            mark = "refusée" if refusals and named else "MANQUÉE"
        else:
            check(not refusals, f"{label} : refusée à tort — {refusals}")
            mark = "acceptée" if not refusals else "REFUSÉE À TORT"
        print(f"   {mark:8s} {label}")

    refused = sum(1 for _, _, _, must_fail in CASES if must_fail)
    print(f"\n{checks} vérifications")
    if failures:
        print("GARDE DES FICHES : IL NE TIENT PAS")
        for line in failures:
            print(f"  - {line}")
        return 1
    print(f"GARDE DES FICHES : il refuse chacune des {refused} fautes, "
          f"pour la raison prévue (D14)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
