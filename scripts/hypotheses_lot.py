"""Relier les hypothèses du lot à leur lot — étape 8 de la phase 09 (`D40`, `D41`).

**Ce script n'écrit aucune hypothèse.** Leur format, leur rédaction et leur juge
sont ceux de `D40` (`hypotheses/score_hypothese.py`, sept conditions et la
bijection avec le lot). Jusqu'au 2026-10-01, ce script en écrivait une version
mécanique ; deux lignes de travail produisaient alors deux hypothèses pour une
même fiche. `D41` tranche : le format de `D40` fait foi, ce script relie.

Ce qu'il fait, pour chaque fiche du lot dont l'hypothèse passe le juge de `D40` :

- il inscrit dans le lot sa `ref` et son `signal_id` (le reflet que
  `score_hypothese.py --lier` reconstruit aussi : mêmes valeurs) ;
- il inscrit l'**univers de la mesure** (`D38`) :
  - une hypothèse **écrite avant `D38`** (avant le 2026-09-30) ou qui déclare
    « les 25 cellules » garde ce qu'elle a pré-enregistré : **la grille entière**.
    Une hypothèse ne se réécrit pas (invariant IV) ;
  - une hypothèse **écrite depuis** est mesurée sur l'actif du papier et sa
    classe, tirés de la recette — et sa section « Le domaine » doit nommer
    chaque actif du papier, sans quoi elle n'est pas reliée.

    python scripts/hypotheses_lot.py --status
    python scripts/hypotheses_lot.py --lier            # relie ce qui est prêt
    python scripts/hypotheses_lot.py --domaine <fiche> # le paragraphe d'univers D38 à écrire
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "hypotheses"))

from codage_verifie import RECETTES, concordance, principal_de, univers_de  # noqa: E402
from gate_09 import LOT_FILE  # noqa: E402

HYP_DIR = REPO / "hypotheses"
DATE_D38 = "2026-09-30"
FENETRES = ["ASIA", "EUROPE", "US"]


def juge() -> tuple[dict[str, str], list[str]]:
    """(fiche_id -> ref, fautes), par le juge de `D40`, sur les fiches du lot."""
    import score_hypothese as sh  # noqa: PLC0415

    return sh.juger_ensemble(HYP_DIR, sh.fiche_ids_du_lot())


def fichier_de(ref: str) -> Path | None:
    return next(iter(sorted(HYP_DIR.glob(f"{ref}-*.md"))), None)


def section(texte: str, titre: str) -> str:
    m = re.search(rf"^##\s+{re.escape(titre)}\s*$(.*?)(?=^##\s|\Z)", texte, re.M | re.S)
    return m.group(1) if m else ""


def ecrite_le(texte: str) -> str:
    m = re.search(r"^\*\*Écrite le\s*:\*\*\s*(\d{4}-\d{2}-\d{2})", texte, re.M | re.I)
    return m.group(1) if m else ""


def grille() -> dict:
    from panel.catalogue import load_catalogue  # noqa: PLC0415

    roots = [r for r, i in load_catalogue().instruments.items() if i.in_universe]
    return {"exact": roots, "classe": [], "fenetres": FENETRES, "grille": True,
            "studied": "la grille entière, pré-enregistrée avant D38"}


def horizon_de(texte: str) -> str | None:
    """L'horizon intraday que l'hypothèse a déclaré (`D42`) : « 15min », « 2h »,
    « cloture » (jusqu'à la clôture de la fenêtre), ou None s'il n'est pas lisible."""
    m = re.search(r"\*\*Horizon\s*:\*\*\s*(.+?)(?:\n\s*\n|\n- \*\*|\Z)",
                  section(texte, "Le domaine"), re.S | re.I)
    if not m:
        return None
    ligne = " ".join(m.group(1).split()).lower()
    # « de la fin de la première demi-heure à la clôture » : l'horizon est la
    # clôture, la demi-heure n'est que le point de départ. La clôture d'abord.
    if re.search(r"(?:à|jusqu.?à)\s+la\s+\**cl[ôo]ture", ligne):
        return "cloture"
    if "demi-heure" in ligne:
        return "30min"
    n = re.search(r"(\d+)\s*(minutes?|min\b)", ligne)
    if n:
        return f"{int(n.group(1))}min"
    n = re.search(r"(\d+)\s*(heures?|h\b)", ligne)
    if n:
        return f"{int(n.group(1))}h"
    if "clôture" in ligne or "cloture" in ligne:
        return "cloture"
    return None


def univers_pour(fid: str, ref: str) -> tuple[dict | None, str]:
    """L'univers que l'hypothèse a pré-enregistré, ou pourquoi on ne peut pas encore le dire."""
    texte = fichier_de(ref).read_text(encoding="utf-8")
    domaine = section(texte, "Le domaine")
    if ecrite_le(texte) < DATE_D38 or "25 cellules" in domaine:
        return grille(), ""
    rp = RECETTES / f"{fid}.json"
    u = univers_de(json.loads(rp.read_text(encoding="utf-8")) if rp.is_file() else {})
    if u is None:
        return None, "la recette ne déclare pas encore le marché (D38)"
    if not u["exact"]:
        return None, "marché absent de notre univers : la fiche s'écarte (D38)"
    absents = [r for r in u["exact"] if not re.search(rf"\b{re.escape(r)}\b", domaine)]
    if absents:
        return None, (f"« Le domaine » ne nomme pas l'actif du papier {absents} : l'univers "
                      "mesuré doit être celui que l'hypothèse a écrit")
    return {k: u[k] for k in ("exact", "classe", "fenetres", "studied")}, ""


def do_status() -> int:
    liens, fautes = juge()
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    for e in lot["fiches"]:
        fid = e["fiche_id"]
        ref = liens.get(fid)
        verif = "vérifiée" if concordance(fid, principal_de(fid))[0] else "non vérifiée"
        if not ref:
            etat = "hypothèse D40 à écrire"
        elif e.get("ref") == ref and e.get("universe"):
            etat = f"reliée {ref}" + (" (grille)" if e["universe"].get("grille") else "")
        else:
            etat = f"{ref} écrite, à relier"
        print(f"  {etat:<30} {verif:<13} {fid}")
    print(f"\n{len(liens)}/{len(lot['fiches'])} hypothèses au format D40 ; "
          f"{len(fautes)} faute(s) du juge (score_hypothese.py)")
    return 0


def do_lier() -> int:
    liens, fautes = juge()
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    reliees, attente = 0, []
    for e in lot["fiches"]:
        fid = e["fiche_id"]
        ref = liens.get(fid)
        if not ref:
            continue
        fichier = fichier_de(ref)
        if any(fichier.name in f for f in fautes):
            attente.append((fid, f"{ref} refusée par le juge de D40"))
            continue
        u, pourquoi = univers_pour(fid, ref)
        if u is None:
            attente.append((fid, pourquoi))
            continue
        h = horizon_de(fichier.read_text(encoding="utf-8"))
        if h is None:
            attente.append((fid, f"{ref} : horizon illisible dans « Le domaine » (D42)"))
            continue
        if e.get("ref") != ref or e.get("universe") != u or e.get("horizon") != h:
            e["ref"], e["signal_id"], e["universe"], e["horizon"] = ref, fid, u, h
            reliees += 1
    LOT_FILE.write_text(json.dumps(lot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{reliees} entrée(s) reliée(s) ; {len(liens)} hypothèse(s) D40 au total")
    for fid, pourquoi in attente:
        print(f"  ATTENTE {fid} : {pourquoi}")
    if reliees:
        print("Commiter le lot aussitôt : la date du commit prouve que l'univers "
              "précède la mesure.")
    return 0


def do_domaine(fid: str) -> int:
    rp = RECETTES / f"{fid}.json"
    u = univers_de(json.loads(rp.read_text(encoding="utf-8")) if rp.is_file() else {})
    if u is None:
        raise SystemExit("la recette ne déclare pas de marché : la refaire (D38)")
    if not u["exact"]:
        raise SystemExit("marché absent : la fiche s'écarte, pas d'hypothèse à écrire (D38)")
    print("À recopier dans la section « Le domaine » de l'hypothèse (D38, D41) :\n")
    print(f"- **Marché du papier :** {u['studied']}.")
    print(f"- **Actif du papier :** {', '.join(u['exact'])} — lu à part dans les résultats.")
    print(f"- **Même classe :** {', '.join(u['classe']) or 'aucun autre instrument'} — lue à part.")
    print(f"- **Fenêtres :** {', '.join(u['fenetres'])} (heure de New York).")
    print("- **Un seul test** : l'IC poolé sur ces cellules, et sur elles seules (D01 §4, D38).")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Relier les hypothèses D40 au lot — D41")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--lier", action="store_true")
    ap.add_argument("--domaine", metavar="FICHE_ID")
    ap.add_argument("--write", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.write:
        raise SystemExit("--write n'existe plus (D41) : les hypothèses s'écrivent au format D40 "
                         "et se jugent par hypotheses/score_hypothese.py ; ce script les relie.")
    if a.lier:
        return do_lier()
    if a.domaine:
        return do_domaine(a.domaine)
    return do_status()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
