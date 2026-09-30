"""Le codage vérifié — ce que `D34` ajoute au codeur de `D23`, en un seul endroit.

`D23` juge UN codage contre sa fiche : il attrape le grossier (contrat, imports,
look-ahead, dégénérescence, constante inventée) et laisse passer le subtil — un
signal fidèle à une lecture fausse ou partielle de la fiche. `D34` ferme ce
trou par trois gestes, avant toute mesure :

1. **la recette** (`scripts/recette.py`) : la formule, les entrées, le timing
   et chaque paramètre du papier, cités mot pour mot, ou `null` avec raison ;
2. **les choix écrits** : chaque module produit déclare `CHOICES`, les
   interprétations que son codeur a dû faire ;
3. **le double codage** (`scripts/double_codage.py`) : deux codeurs isolés, de
   deux modèles différents, codent la même fiche ; leurs SCORES doivent
   concorder.

Ce module porte les seuils, les chemins et les vérifications partagées. **Aucun
IC n'est calculé ici, ni nulle part dans `D34`** : on compare des scores entre
eux, jamais un score à un rendement futur.
"""

from __future__ import annotations

import ast
import datetime as dt
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Les seuils de `D34`, fixés AVANT toute mesure du lot. Les changer est une
# décision écrite, et ne peut se faire qu'avant la première mesure (`D28`).
SEUIL_RHO = 0.70          # concordance des scores, Spearman pondéré par cellule
SEUIL_COUVERTURE = 0.80   # part des (cellule, instant) notés par les deux codeurs
MIN_PAIRES = 30           # sous ce nombre, une cellule ne dit rien
ASOF_CONCORDANCE = "2018-06-15 20:00"  # l'instant du juge D23, pas celui de la mesure
MODELE_PRINCIPAL = "opus"
MODELE_TEMOIN = "sonnet"
TOURS_MAX = 2             # tours de concordance avant d'écarter la fiche

VERIF = REPO / "verification"
TEMOINS = VERIF / "temoins"
JUGEMENTS = VERIF / "jugements.jsonl"
CONCORDANCE = VERIF / "concordance.jsonl"
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


def temoin_path(module_path: Path) -> Path:
    """Le témoin d'un module de `signals/` porte le même nom, dans `verification/`."""
    return TEMOINS / module_path.name


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

def inscrire_jugement(module_path: Path, fiche_id: str, rc: int, choix_ok: bool) -> None:
    ajouter(JUGEMENTS, {
        "at": maintenant(), "path": rel(module_path), "fiche_id": fiche_id,
        "sha256_16": empreinte16(module_path), "d23_passed": rc == 0,
        "choices_ok": choix_ok,
    })


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
# La concordance — le verdict qui ouvre le lot
# ---------------------------------------------------------------------------

def principal_de(fiche_id: str) -> Path:
    """Le module principal d'une fiche — la règle de `code_signal.module_path`."""
    return REPO / "signals" / (fiche_id.replace("-", "_") + ".py")


def fautes_d34_du_lot(lot: dict, registre: list[dict], stage: str) -> list[str]:
    """Ce que `D34` exige d'un lot, pour la porte 09 et la mesure.

    1. chaque entrée a un double codage CONCORDANT, à l'empreinte actuelle de
       son module principal ;
    2. chaque fiche écartée l'a été AVANT la première mesure du lot — écarter
       après avoir vu un IC serait choisir le lot sur son résultat (`D28`).
    """
    fautes: list[str] = []
    entries = lot.get("fiches") or lot.get("hypotheses") or []
    for e in entries:
        fid = e.get("fiche_id") or e.get("signal_id")
        ok, pourquoi = concordance(fid, principal_de(fid))
        if not ok:
            fautes.append(f"{pourquoi} (D34)")
    ids = ({e.get("signal_id") for e in entries} | {e.get("fiche_id") for e in entries}
           | {x.get("fiche_id") for x in lot.get("ecartees_codage") or []}) - {None}
    mesures = sorted(r["timestamp"] for r in registre
                     if r.get("stage") == stage and r.get("signal_id") in ids)
    for x in lot.get("ecartees_codage") or []:
        if mesures and (x.get("at") or "9") >= mesures[0]:
            fautes.append(f"{x.get('fiche_id')} écartée le {x.get('at')}, APRÈS la première "
                          f"mesure du lot ({mesures[0]}) — D34 l'interdit")
    return fautes


def concordance(fiche_id: str, module_path: Path) -> tuple[bool, str]:
    """Le module principal a-t-il un verdict CONCORDANT, à son empreinte actuelle ?"""
    if not module_path.is_file():
        return False, f"{fiche_id} : module {module_path.name} absent"
    sha = empreinte16(module_path)
    lignes = [c for c in lire(CONCORDANCE) if c["fiche_id"] == fiche_id]
    if not lignes:
        return False, f"{fiche_id} : aucun double codage (D34)"
    c = lignes[-1]
    if c["principal"]["sha256_16"] != sha:
        return False, (f"{fiche_id} : le dernier double codage portait sur "
                       f"{c['principal']['sha256_16']}, le module est à {sha}")
    if c["verdict"] != "CONCORDANT":
        return False, f"{fiche_id} : double codage {c['verdict']} (rho {c.get('rho')})"
    return True, ""
