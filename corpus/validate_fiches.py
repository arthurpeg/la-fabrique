"""Le garde des fiches. Il refuse ce que `corpus/SCHEMA.md` interdit.

Une fiche est le JSON structuré extrait d'un papier, et sa définition vient de
`CLAUDE.md` § Le vocabulaire : hypothèse, univers, horizon, construction du
signal, résultats annoncés, ce qui manque. `D14` y ajoute la source et la
transposabilité, et rend le tout exécutable.

Le contrôle qui mord est le quatrième : **un résultat recopié d'un papier est une
valeur externe** au sens de `D09`, donc il porte sa citation, et la valeur doit
s'y retrouver. La fonction employée est `value_in_quote`, celle du catalogue —
la même que `scripts/check_provenance.py` a prise en défaut sur `12500` contre
`12,500,000` (ledger F26). Ce qui est attrapé n'est pas la source absente, qui se
voit, mais la faute de recopie, qui ne se voit pas.

    python corpus/validate_fiches.py

Code de sortie 1 et chaque refus nommé.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "catalogue"))

from validate import value_in_quote  # noqa: E402 -- le garde de D09, réutilisé tel quel

FICHES = REPO / "corpus" / "fiches"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED = (
    "fiche_id",
    "written",
    "written_by",
    "source",
    "claim",
    "universe",
    "horizon",
    "signal_construction",
    "reported_results",
    "transposability",
    "what_is_missing",
)
SOURCE_REQUIRED = ("authors", "title", "year", "source_url", "retrieved")
NULLABLE_WITH_REASON = ("horizon", "signal_construction")
TRANSPOSABILITY_REQUIRED = (
    "what_transfers",
    "what_does_not_transfer",
    "what_aligns_well",
)


def check_fiche(name: str, fiche: dict) -> list[str]:
    """Tout ce que cette fiche mérite comme refus. Vide veut dire qu'elle passe."""
    bad: list[str] = []

    # 1. les champs obligatoires
    for field in REQUIRED:
        if field not in fiche:
            bad.append(f"{name} : champ obligatoire {field!r} absent")

    if fiche.get("fiche_id") != name:
        bad.append(f"{name} : fiche_id vaut {fiche.get('fiche_id')!r}, pas le nom du fichier")
    if not DATE.match(str(fiche.get("written", ""))):
        bad.append(f"{name} : written vaut {fiche.get('written')!r}, attendu AAAA-MM-JJ")

    # 2. la source
    source = fiche.get("source")
    if not isinstance(source, dict):
        bad.append(f"{name} : source n'est pas un objet")
    else:
        for field in SOURCE_REQUIRED:
            value = source.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                bad.append(f"{name} : source.{field} est vide")
        if not str(source.get("source_url", "")).startswith("http"):
            bad.append(f"{name} : source.source_url n'est pas une URL")
        if not DATE.match(str(source.get("retrieved", ""))):
            bad.append(
                f"{name} : source.retrieved vaut {source.get('retrieved')!r}, "
                f"attendu AAAA-MM-JJ"
            )
        if not isinstance(source.get("peer_reviewed"), bool):
            bad.append(
                f"{name} : source.peer_reviewed doit être un booléen — un préprint "
                f"n'est pas une revue à comité de lecture, et la distinction sert"
            )

    # 3. un null se justifie
    for field in NULLABLE_WITH_REASON:
        block = fiche.get(field)
        if not isinstance(block, dict):
            bad.append(f"{name} : {field} doit être un objet, même pour dire null")
            continue
        if "value" not in block:
            bad.append(f"{name} : {field}.value absent")
        elif block["value"] is None and not str(block.get("reason", "")).strip():
            bad.append(
                f"{name} : {field} vaut null sans raison — l'inconnu s'écrit, "
                f"il ne se tait pas"
            )

    # 4. les résultats annoncés, et leur citation
    results = fiche.get("reported_results")
    if not isinstance(results, list):
        bad.append(f"{name} : reported_results doit être une liste")
    elif not results:
        bad.append(f"{name} : reported_results est vide — un papier annonce quelque chose")
    else:
        seen: set[str] = set()
        for position, entry in enumerate(results):
            label = entry.get("name") if isinstance(entry, dict) else None
            where = f"{name} : reported_results[{label or position}]"
            if not isinstance(entry, dict):
                bad.append(f"{where} n'est pas un objet")
                continue
            if not str(entry.get("name", "")).strip():
                bad.append(f"{where} : name est vide")
            elif entry["name"] in seen:
                bad.append(f"{where} : name en double")
            else:
                seen.add(entry["name"])
            quoted = str(entry.get("quoted", ""))
            if not quoted.strip():
                bad.append(f"{where} : quoted est vide — un résultat recopié porte sa citation")
                continue

            # La RÉPARATION DÉCLARÉE de `D16` § Complément. `REPAIRS` est importée
            # de `score_extraction` plutôt que recopiée ici : `D16` en est
            # propriétaire, et deux définitions d'une même liste close divergent.
            # L'import est tardif parce que `score_extraction` importe ce module
            # pour `F1` — chacun a besoin de l'autre, aucun au chargement.
            from score_extraction import REPAIRS  # noqa: PLC0415

            source = entry.get("quoted_source")
            repair = entry.get("quoted_repair")
            if source is not None:
                if not str(source).strip():
                    bad.append(f"{where} : quoted_source est vide")
                    continue
                if repair not in REPAIRS:
                    bad.append(
                        f"{where} : quoted_source sans quoted_repair valide — "
                        f"attendu l'un de {sorted(REPAIRS)}, reçu {repair!r} (D16)"
                    )
                    continue
            elif repair is not None:
                bad.append(f"{where} : quoted_repair déclaré sans quoted_source (D16)")
                continue

            # LA CHAÎNE QUI FAIT FOI est celle que `F2` cherche dans le papier.
            # Sans cela, `F1` serait plus laxiste que `F3` sur une entrée réparée :
            # un chiffre logé dans la version lisible et absent de la source
            # passerait le schéma et casserait le juge. `D16` § Ce que ce
            # complément a découvert l'avait nommé ; c'est corrigé ici.
            quoted = str(source) if source else quoted

            value = entry.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            if entry.get("derived") is True:
                # Un nombre que NOUS avons calculé à partir de la citation n'a pas
                # à s'y retrouver ; il doit dire comment il a été obtenu.
                if not str(entry.get("note", "")).strip():
                    bad.append(f"{where} : derived sans note expliquant le calcul")
                continue
            spelled = entry.get("spelled_out")
            if spelled is not None:
                # Le papier écrit le nombre EN TOUTES LETTRES -- « Eleven signal
                # families fail ». Le contrôle numérique ne peut rien y faire, et
                # le contourner par `derived` serait un abus : rien n'a été
                # calculé. Le garde vérifie alors que le MOT est bien dans la
                # citation. Ce qu'il ne vérifie pas -- que le mot vaut ce nombre --
                # reste un geste humain, et il est nommé comme tel (D14).
                if not str(spelled).strip():
                    bad.append(f"{where} : spelled_out est vide")
                elif str(spelled).lower() not in quoted.lower():
                    bad.append(
                        f"{where} : spelled_out {spelled!r} est introuvable dans la citation"
                    )
                continue
            if not value_in_quote(value, quoted):
                bad.append(
                    f"{where} : la valeur {value!r} est introuvable dans sa citation "
                    f"{quoted[:60]!r} (D09, D14)"
                )

    # 5. la transposabilité
    transpo = fiche.get("transposability")
    if not isinstance(transpo, dict):
        bad.append(f"{name} : transposability n'est pas un objet")
    else:
        for field in TRANSPOSABILITY_REQUIRED:
            if field not in transpo:
                bad.append(f"{name} : transposability.{field} absent")
        does_not = transpo.get("what_does_not_transfer")
        if not isinstance(does_not, list) or not does_not:
            bad.append(
                f"{name} : transposability.what_does_not_transfer est vide — un papier "
                f"dont tout transfère n'a pas été lu avec assez d'attention"
            )

    # 6. ce qui manque
    missing = fiche.get("what_is_missing")
    if not isinstance(missing, list):
        bad.append(f"{name} : what_is_missing doit être une liste")

    return bad


def main() -> int:
    files = sorted(FICHES.glob("*.json"))
    if not files:
        print("aucune fiche dans corpus/fiches/")
        return 1

    failures: list[str] = []
    for path in files:
        try:
            fiche = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(f"{path.name} ne se parse pas : {error}")
            continue
        refusals = check_fiche(path.stem, fiche)
        failures.extend(refusals)
        results = fiche.get("reported_results") or []
        state = "REFUSÉE" if refusals else "valide"
        print(f"  {path.stem:42s} {len(results):2d} résultats · {state}")

    print(f"\n{len(files)} fiches")
    if failures:
        print("FICHES : INVALIDES")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("FICHES : VALIDES — chaque résultat recopié porte sa citation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
