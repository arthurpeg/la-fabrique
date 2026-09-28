"""Le lot de la phase 09 — appliqué, jamais recopié. `D27`.

`D25` engageait **50 signaux**. Ce chiffre a été écrit le 2026-09-23, quand le
corpus portait 17 fiches : c'était une estimation, pas une mesure. Le corpus en
porte 51 aujourd'hui, le moissonné est épuisé, et **50 ne tient pas** — pas
sans y verser des papiers qui exigent une donnée que nous n'avons pas.

`D27` remplace donc le nombre par un **critère**, et ce fichier l'applique :

> Le lot est l'ensemble des fiches dont le papier a été trié **`oui`**, plus
> celles triées **`partiel` dont la raison est une transposition d'univers** —
> jamais celles dont le `partiel` tient à une **donnée manquante**.

**Pourquoi un critère et pas un nombre.** Un `N` fixe se justifierait après
coup ; un critère se vérifie. Et il s'appuie sur un triage **déjà jugé contre un
étalon humain** (`D15`, quatre conditions), pas sur le jugement de la session qui
compose le lot — laquelle a vu les fiches et ne peut donc plus les trier sans
biais (`F42`).

**Le compte se RELANCE.** `L21` : un effectif recopié se périme, et celui-ci
bougera si le corpus s'élargit. Aucune prose de ce dépôt ne doit porter ce
nombre sans l'avoir recalculé.

    python corpus/lot_phase09.py            # le lot, et ce qui en est ecarte
    python corpus/lot_phase09.py --ecrire   # fige le lot, DATE — D25 C2
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "corpus"))

FICHES_AMORCE = REPO / "corpus" / "fiches"
FICHES_HARVEST = REPO / "corpus" / "fiches_harvest"
PROMOTED = REPO / "corpus" / "harvest_promoted.json"
VERDICTS = REPO / "corpus" / "triage_harvest_verdicts.json"
ACQUISITION = REPO / "corpus" / "acquisition.json"
LOT = REPO / "hypotheses" / "LOT-09.json"

# Les mots qui, dans la RAISON du trieur, designent une DONNEE MANQUANTE. Un
# `partiel` de ce genre ne se code pas en OHLCV : c'est la difference que `D15`
# pose entre « il manque une donnee » et « la methode se transpose ».
#
# LISTE CLOSE, et elle est volontairement LARGE : dans le doute, la fiche sort
# du lot. Un faux exclu coute une hypothese ; un faux inclus coute un signal
# qu'on ne peut pas ecrire, decouvert au moment de le coder.
DONNEE_MANQUANTE = (
    "calendrier", "annonce", "macro", "fomc", "carnet", "order flow",
    "option", "analyste", "echeance", "échéance", "stock", "open interest",
    "intérêt ouvert", "volume de carnet", "tick par tick", "payant",
)


def verdicts_moissonnes() -> dict[str, dict]:
    """`fiche_id` -> le verdict de triage, via le registre de promotion.

    Le passage par `harvest_promoted.json` est le SEUL chemin qui relie un nom
    de fiche a l'uuid du papier en base. Le rededuire autrement serait une
    seconde deduction de la meme chose (`D24`).
    """
    prom = {Path(p["pdf"]).stem: p for p in json.loads(PROMOTED.read_text(encoding="utf-8"))}
    verd = {v["id"]: v for v in json.loads(VERDICTS.read_text(encoding="utf-8"))}
    out = {}
    for f in sorted(FICHES_HARVEST.glob("*.json")):
        p = prom.get(f.stem)
        if p and (v := verd.get(p["paper_id"])):
            out[f.stem] = v
    return out


def verdicts_amorce() -> dict[str, dict]:
    """`fiche_id` -> le verdict HUMAIN d'`AMORCE.md`, lu par son propre lecteur."""
    from score_triage import read_etalon  # type: ignore

    etalon = read_etalon()
    out = {}
    for a in json.loads(ACQUISITION.read_text(encoding="utf-8")):
        if not a.get("pdf"):
            continue
        stem = Path(a["pdf"]).stem
        if not (FICHES_AMORCE / f"{stem}.json").is_file():
            continue
        if v := etalon.get(a["entry"]):
            # L'etalon humain ne porte pas de raison ecrite : un `partiel` y est
            # donc INDECIDABLE au regard du critere, et il sort du lot. Le dire
            # plutot que de trancher a sa place.
            out[stem] = {"verdict": v, "raison": "", "source": "AMORCE (etalon humain)"}
    return out


def classer(verdict: str, raison: str) -> tuple[bool, str]:
    """Rend (dans_le_lot, motif). Le motif est ecrit, jamais sous-entendu."""
    if verdict == "oui":
        return True, "trié `oui` — calculable en OHLCV seul"
    if verdict != "partiel":
        return False, f"trié `{verdict}`"
    if not raison.strip():
        return False, "trié `partiel` sans raison écrite — indécidable, donc écarté"
    bas = raison.lower()
    for mot in DONNEE_MANQUANTE:
        if mot in bas:
            return False, f"trié `partiel`, donnée manquante (« {mot} »)"
    return True, "trié `partiel`, transposition d'univers"


def composer() -> tuple[list[dict], list[dict]]:
    tous = {**verdicts_amorce(), **verdicts_moissonnes()}
    dedans, dehors = [], []
    for fiche_id, v in sorted(tous.items()):
        ok, motif = classer(v["verdict"], v.get("raison") or "")
        ligne = {"fiche_id": fiche_id, "verdict": v["verdict"], "motif": motif}
        (dedans if ok else dehors).append(ligne)
    return dedans, dehors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le lot de la phase 09 — D27")
    ap.add_argument("--ecrire", action="store_true", help="fige le lot et le date (D25 C2)")
    a = ap.parse_args(argv)

    dedans, dehors = composer()
    print(f"LOT DE LA PHASE 09 — critère de `D27`, appliqué le {date.today()}\n")
    print(f"  DANS LE LOT : {len(dedans)}")
    for ligne in dedans:
        print(f"    {ligne['verdict']:8} {ligne['fiche_id'][:52]}")
    print(f"\n  ÉCARTÉES : {len(dehors)}")
    for ligne in dehors:
        print(f"    {ligne['motif'][:56]:58} {ligne['fiche_id'][:40]}")

    print(f"\n  N = {len(dedans)}")
    print("  Ce nombre se RELANCE, il ne se recopie pas (`L21`) : il bougera si")
    print("  le corpus s'élargit, et toute prose qui le porte se périme.")

    if a.ecrire:
        LOT.write_text(
            json.dumps(
                {
                    "decision": "D27",
                    "declared_at": date.today().isoformat(),
                    "q": 0.10,
                    "critere": "trié `oui`, ou `partiel` par transposition d'univers",
                    "n": len(dedans),
                    "fiches": dedans,
                    "ecartees": dehors,
                },
                ensure_ascii=False,
                indent=1,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\n  lot figé : {LOT.relative_to(REPO)} — {date.today()}")
        print("  `D25` C2 : il est CLOS. L'élargir après une mesure casse `BH`.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
