"""Rassemble les verdicts de triage des lots, et vérifie qu'il n'en manque aucun.

Quatre sessions ont trié 119 papiers par lots de 30. Ce script recolle leurs
sorties et **refuse de rendre un compte si la population n'est pas reconstituée**.

**C'est `L21` appliqué à l'endroit où elle mord.** Un papier absent d'un lot, ou
un `id` recopié de travers, disparaîtrait du compte sans aucune erreur — et du
côté qui arrange, puisqu'un papier perdu est un papier qu'on ne triera pas. Le
contrôle est donc frontal : l'ensemble des `id` triés doit être **exactement**
celui de `corpus/triage_harvest.json`, ni plus, ni moins.

    python corpus/merge_triage.py
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "corpus"
ATTENDUS = CORPUS / "triage_harvest.json"
SORTIE = CORPUS / "triage_harvest_verdicts.json"

VERDICTS = ("oui", "partiel", "non")


def main() -> int:
    if not ATTENDUS.is_file():
        raise SystemExit("corpus/triage_harvest.json absent — lancer triage_harvest.py")
    attendus = {p["id"]: p["title"] for p in json.loads(ATTENDUS.read_text(encoding="utf-8"))}

    lus: dict[str, dict] = {}
    doublons: list[str] = []
    fichiers = sorted(CORPUS.glob("triage_verdicts_lot-*.json"))
    if not fichiers:
        raise SystemExit("aucun fichier de verdicts — les trieurs n'ont rien rendu")
    for f in fichiers:
        for ligne in json.loads(f.read_text(encoding="utf-8")):
            i = str(ligne["id"])
            if i in lus:
                doublons.append(i)
            lus[i] = {**ligne, "lot": f.stem[-2:]}

    fautes: list[str] = []
    manquants = sorted(set(attendus) - set(lus))
    intrus = sorted(set(lus) - set(attendus))
    if manquants:
        fautes.append(f"{len(manquants)} papier(s) NON TRIÉ(S) — ils sortiraient du "
                      f"compte sans erreur (L21). Premier : {manquants[0]}")
    if intrus:
        fautes.append(f"{len(intrus)} id INCONNU(S) du recensement, donc recopié(s) "
                      f"de travers : {intrus[:3]}")
    if doublons:
        fautes.append(f"{len(doublons)} papier(s) trié(s) DEUX FOIS : {doublons[:3]}")
    mauvais = [i for i, v in lus.items() if v.get("verdict") not in VERDICTS]
    if mauvais:
        fautes.append(f"{len(mauvais)} verdict(s) hors de l'échelle de D15 "
                      f"{VERDICTS} : {mauvais[:3]}")

    print(f"attendus : {len(attendus)}   triés : {len(lus)}   "
          f"lots : {len(fichiers)}\n")
    compte = collections.Counter(v.get("verdict") for v in lus.values())
    for verdict in VERDICTS:
        n = compte[verdict]
        part = 100 * n / len(lus) if lus else 0
        print(f"  {verdict:<9}{n:>5}   ({part:>4.0f} %)")

    par_lot = collections.defaultdict(collections.Counter)
    for v in lus.values():
        par_lot[v["lot"]][v.get("verdict")] += 1
    print("\npar lot — un trieur bien plus sévère qu'un autre serait un signal :")
    for lot in sorted(par_lot):
        c = par_lot[lot]
        print(f"  lot {lot} : " + "  ".join(f"{k} {c[k]:>2}" for k in VERDICTS))

    retenus = [i for i, v in lus.items() if v.get("verdict") in ("oui", "partiel")]
    print(f"\nRETENUS (oui + partiel) : {len(retenus)} sur {len(lus)}")

    if fautes:
        print("\nCOMPTE REFUSÉ :")
        for f in fautes:
            print(f"  - {f}")
        return 1

    # `for i in lus` avec `v[k]` a l'interieur : `v` venait de la boucle
    # PRECEDENTE, et les 119 lignes ont ete ecrites avec le meme verdict.
    # Les comptes imprimes restaient justes — ils se calculent sur `lus` — donc
    # rien n'a cassé et le fichier était faux en silence. Nomme explicitement
    # la variable de boucle, et vérifie la sortie plutôt que de l'espérer.
    lignes = sorted(
        ({"id": i, "title": attendus[i],
          **{k: ligne[k] for k in ("verdict", "raison", "lot") if k in ligne}}
         for i, ligne in lus.items()),
        key=lambda x: (x["verdict"], x["title"]),
    )

    # LE GARDE QUI MANQUAIT : ce qu'on ECRIT doit recompter comme ce qu'on a LU.
    ecrit = collections.Counter(x["verdict"] for x in lignes)
    if ecrit != compte:
        raise SystemExit(
            f"le fichier écrit ne recompte pas comme les verdicts lus : "
            f"{dict(ecrit)} contre {dict(compte)}. Rien n'est écrit."
        )

    SORTIE.write_text(json.dumps(lignes, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"\nécrit : {SORTIE.relative_to(REPO)}  "
          f"(recompté : {dict(ecrit)})")
    print("\nCE TRIAGE N'EST PAS NOTÉ : aucun étalon humain n'existe pour ces")
    print("papiers. Ce qui fonde la confiance est le passage 1 du 2026-09-20 sur")
    print("les 20 d'AMORCE.md (A/B/C/D = 1/0/2/0), et rien d'autre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
