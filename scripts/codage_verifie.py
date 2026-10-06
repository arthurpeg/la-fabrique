"""Le codage vérifié — ce que `D34` ajoute au codeur de `D23`, en un seul endroit.

`D23` juge UN codage contre sa fiche : il attrape le grossier (contrat, imports,
look-ahead, dégénérescence, constante inventée). `D34` y ajoute, avant toute
mesure :

1. **la recette** (`scripts/recette.py`) : la formule, les entrées, le timing
   et chaque paramètre du papier, cités mot pour mot, ou `null` avec raison ;
2. **les choix écrits** : chaque module produit déclare `CHOICES`, les
   interprétations que son codeur a dû faire.

**Le double codage (un second codeur, `fabrique-temoin`) est supprimé par
`D54`** : sur neuf fiches, deux concordances, sept fiches bloquées, et des
désaccords venus surtout d'ambiguïtés de recette, que la recette doit
trancher, pas un second code. Un signal entre dans un lot quand son module
principal passe le juge `D23` et porte des `CHOICES` bien formés, à son
empreinte actuelle (`verifie`).

Ce module porte les chemins et les vérifications partagées. **Aucun IC n'est
calculé ici.**
"""

from __future__ import annotations

import ast
import datetime as dt
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

VERIF = REPO / "verification"
JUGEMENTS = VERIF / "jugements.jsonl"
CONCORDANCE = VERIF / "concordance.jsonl"  # archive du double codage, close par D54
RECETTES = REPO / "corpus" / "recettes"


def maintenant() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def empreinte16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def ajouter(path: Path, ligne: dict) -> None:
    """Ajout en fin de journal. Ces journaux sont append-only, comme le registre."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def lire(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO).as_posix()


# ---------------------------------------------------------------------------
# Les choix écrits — `CHOICES`
# ---------------------------------------------------------------------------

def fautes_choix(source: str) -> list[str]:
    """`CHOICES` doit être un tuple (ou une liste) non vide de chaînes non vides.

    Lu dans l'arbre syntaxique, sans importer le module : une valeur calculée
    n'est pas une déclaration, et ce contrôle ne doit rien exécuter.
    """
    for noeud in ast.parse(source).body:
        cibles = []
        if isinstance(noeud, ast.Assign):
            cibles, valeur = noeud.targets, noeud.value
        elif isinstance(noeud, ast.AnnAssign) and noeud.value is not None:
            cibles, valeur = [noeud.target], noeud.value
        if not any(isinstance(c, ast.Name) and c.id == "CHOICES" for c in cibles):
            continue
        if not isinstance(valeur, (ast.Tuple, ast.List)):
            return ["CHOICES doit être un tuple littéral de chaînes"]
        if not valeur.elts:
            return ["CHOICES est vide : tout codage fait au moins un choix — le "
                    "nommer, ou écrire qu'aucun n'a été nécessaire et pourquoi"]
        mauvais = [e for e in valeur.elts
                   if not (isinstance(e, ast.Constant) and isinstance(e.value, str)
                           and e.value.strip())]
        if mauvais:
            return ["CHOICES ne doit contenir que des chaînes non vides"]
        return []
    return ["CHOICES absent : chaque interprétation de la fiche doit être écrite (D34)"]


def choix(source: str) -> list[str]:
    for noeud in ast.parse(source).body:
        if isinstance(noeud, (ast.Assign, ast.AnnAssign)):
            cibles = noeud.targets if isinstance(noeud, ast.Assign) else [noeud.target]
            if any(isinstance(c, ast.Name) and c.id == "CHOICES" for c in cibles):
                try:
                    return [str(x) for x in ast.literal_eval(noeud.value)]
                except ValueError:
                    return []
    return []


# ---------------------------------------------------------------------------
# Les jugements — qui a passé `D23`, à quelle empreinte
# ---------------------------------------------------------------------------

def inscrire_jugement(module_path: Path, fiche_id: str, rc: int, choix_ok: bool,
                      horizon_bars: int | None = None) -> None:
    ligne = {
        "at": maintenant(), "path": rel(module_path), "fiche_id": fiche_id,
        "sha256_16": empreinte16(module_path), "d23_passed": rc == 0,
        "choices_ok": choix_ok,
    }
    if horizon_bars is not None:
        ligne["horizon_bars"] = horizon_bars  # D49
    ajouter(JUGEMENTS, ligne)


def jugement_vert(module_path: Path) -> tuple[bool, str]:
    """Le module, À SON EMPREINTE ACTUELLE, a-t-il passé D23 et `CHOICES` ?"""
    if not module_path.is_file():
        return False, f"{rel(module_path) if module_path.exists() else module_path} absent"
    sha = empreinte16(module_path)
    lignes = [j for j in lire(JUGEMENTS) if j["path"] == rel(module_path)
              and j["sha256_16"] == sha]
    if not lignes:
        return False, f"{module_path.name} n'a jamais été jugé à son empreinte {sha}"
    j = lignes[-1]
    if not j["d23_passed"]:
        return False, f"{module_path.name} : dernier jugement D23 refusé"
    if not j["choices_ok"]:
        return False, f"{module_path.name} : CHOICES absent ou mal formé"
    return True, ""


# ---------------------------------------------------------------------------
# L'univers d'une hypothèse — D38
# ---------------------------------------------------------------------------

def univers_de(recette: dict) -> dict | None:
    """Les cellules de la mesure, tirées du marché que la recette déclare (`D38`).

    `exact` : nos instruments qui SONT le marché du papier ; `classe` : les autres
    instruments de la même `asset_class` du catalogue, ajoutés par ce code et non
    par la session de recette ; `fenetres` : celles que le papier couvre, ou les
    trois s'il ne le dit pas. `None` si la recette ne déclare pas de marché ;
    `exact` vide = marché absent de notre univers, la fiche s'écarte.
    """
    m = (recette or {}).get("market")
    if not isinstance(m, dict):
        return None
    import sys  # noqa: PLC0415

    sys.path.insert(0, str(REPO))
    from panel.catalogue import load_catalogue  # noqa: PLC0415

    cat = load_catalogue()
    exact = [r for r in m.get("exact_roots") or [] if r in cat.instruments]
    classes = {cat.instrument(r).asset_class for r in exact}
    classe = [r for r, i in cat.instruments.items()
              if i.in_universe and i.asset_class in classes and r not in exact]
    fenetres = m.get("sessions") or ["ASIA", "EUROPE", "US"]
    return {"exact": exact, "classe": classe, "fenetres": list(fenetres),
            "studied": m.get("studied"), "fenetres_du_papier": m.get("sessions") is not None}


def cellules_de(univers: dict) -> set[tuple[str, str]]:
    return {(r, w) for r in univers["exact"] + univers["classe"] for w in univers["fenetres"]}


def fautes_univers(lot: dict) -> list[str]:
    """`D38` : chaque entrée du lot porte l'univers déclaré avant la mesure."""
    fautes = []
    for e in lot.get("fiches") or lot.get("hypotheses") or []:
        u = e.get("universe")
        if not u:
            fautes.append(f"{e.get('fiche_id')} : pas d'univers déclaré (D38)")
        elif not u.get("exact"):
            fautes.append(f"{e.get('fiche_id')} : univers sans actif du papier — la fiche "
                          "devait être écartée (D38)")
    return fautes


def principal_de(fiche_id: str) -> Path:
    """Le module principal d'une fiche — la règle de `code_signal.module_path`."""
    return REPO / "signals" / (fiche_id.replace("-", "_") + ".py")


def verifie(fiche_id: str) -> tuple[bool, str]:
    """Le module principal d'une fiche passe-t-il le juge `D23` et `CHOICES`, à son
    empreinte actuelle ? C'est la seule condition de codage d'un lot depuis `D54`."""
    ok, pourquoi = jugement_vert(principal_de(fiche_id))
    return ok, "" if ok else f"{fiche_id} : {pourquoi}"


def fautes_d34_du_lot(lot: dict, registre: list[dict], stage: str) -> list[str]:
    """Ce que `D34` (révisée par `D54`) exige d'un lot, pour la porte 09 et la mesure.

    1. chaque entrée a un module principal jugé vert, à son empreinte actuelle ;
    2. chaque fiche écartée l'a été AVANT la première mesure du lot — écarter
       après avoir vu un IC serait choisir le lot sur son résultat (`D28`).
    """
    fautes: list[str] = []
    entries = lot.get("fiches") or lot.get("hypotheses") or []
    for e in entries:
        fid = e.get("fiche_id") or e.get("signal_id")
        ok, pourquoi = verifie(fid)
        if not ok:
            fautes.append(f"{pourquoi} (D34, D54)")
    ids = ({e.get("signal_id") for e in entries} | {e.get("fiche_id") for e in entries}
           | {x.get("fiche_id") for x in lot.get("ecartees_codage") or []}) - {None}
    mesures = sorted(r["timestamp"] for r in registre
                     if r.get("stage") == stage and r.get("signal_id") in ids)
    for x in lot.get("ecartees_codage") or []:
        if mesures and (x.get("at") or "9") >= mesures[0]:
            fautes.append(f"{x.get('fiche_id')} écartée le {x.get('at')}, APRÈS la première "
                          f"mesure du lot ({mesures[0]}) — D34 l'interdit")
    return fautes
