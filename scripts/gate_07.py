"""PORTE 07 — les quatre effectifs de `D17`, comptés et non recopiés.

`D17` a requalifié la porte : elle ne demande plus « 20 fiches » mais un
extracteur jugé sur **tout le corpus atteignable**, le reste étant recensé avec
sa raison. Quatre conditions en effectifs, toutes à **zéro**, qui valent
ENSEMBLE :

    G1  papiers atteignables NON FICHÉS
    G2  fiches produites ne passant pas les cinq conditions de `D16`
    G3  fiches ayant demandé une RETOUCHE MANUELLE après production
    G4  papiers inatteignables NON RECENSÉS, avec la raison

**Pourquoi ce script existe.** Jusqu'au 2026-09-23, `G1`–`G4` étaient les seuls
effectifs du projet sans compteur — les portes 01 à 06 en ont chacune un. Le
chiffre vivait donc dans la prose de `ETAT.md`, et il y a été faux trois fois :
« 19 atteignables » après que `L20` a fait tomber l'entrée 1, « 18 PDF » pour
17, et `G1 = 7` pour 8. `L21` en tire la règle ; ce fichier la rend inutile.

**`G1` se compte sur la POPULATION ENTIÈRE**, et c'est tout l'objet de `L21` :
l'entrée 9 sortait du compte sans bruit parce qu'elle est en HTML et n'a pas de
`pdf`, donc aucune clé pour se rapprocher des fiches. Ici, les deux moitiés
doivent reconstituer le recensement — `atteignables == fichés + non fichés` —
et l'écart est une faute, pas un silence.

    python scripts/gate_07.py            # les quatre effectifs
    python scripts/gate_07.py --detail   # et le détail de chaque manquant
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from harness import registry  # noqa: E402

ACQUISITION = REPO / "corpus" / "acquisition.json"
FICHES = REPO / "corpus" / "fiches"
JUGE = REPO / "corpus" / "score_extraction.py"

# `G3` — le registre des fiches produites par l'extracteur, qu'il écrirait au
# fur et à mesure. Tant qu'il n'existe pas, `G3` est SANS OBJET et le dit :
# aucune fiche n'a été produite par un automate, donc aucune n'a pu être
# retouchée. L'annoncer « tenu » serait le tenir pour zéro sans l'avoir mesuré.
PRODUITES = REPO / "corpus" / "PRODUCED.json"


def charger_recensement() -> list[dict]:
    if not ACQUISITION.is_file():
        raise SystemExit(
            f"recensement introuvable : {ACQUISITION.relative_to(REPO)} — "
            "`G4` ne peut pas être mesuré, donc aucun des quatre. "
            "Le produire avec corpus/probe_acquisition.py."
        )
    return json.loads(ACQUISITION.read_text(encoding="utf-8"))


def cle(entree: dict) -> str | None:
    """La clé par laquelle une entrée se rapproche d'une fiche.

    C'est le nom du PDF, et **une entrée peut ne pas en avoir** : l'entrée 9 est
    un billet HTML. Rendre `None` plutôt que de l'omettre est exactement ce que
    `L21` demande — l'élément sans clé doit rester DANS la population.
    """
    p = entree.get("pdf")
    return Path(p).name if p else None


def fiches_par_pdf() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for f in sorted(FICHES.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        p = (d.get("source") or {}).get("pdf")
        if p:
            out[Path(p).name] = f
    return out


def juger(fiche: Path) -> tuple[bool, list[str]]:
    """Lance `score_extraction.py` SANS lui imposer de texte.

    Le juge résout lui-même le texte qui fait foi depuis la fiche — l'UNION des
    deux extractions de `D18`. Lui passer un fichier le fait imprimer « hors
    D18, le verdict ne fait pas foi », et produit un rouge de plus : c'est
    arrivé le 2026-09-23 sur `heston`, dont le `F2` cassait pour cette seule
    raison.
    """
    r = subprocess.run(
        [sys.executable, str(JUGE), str(fiche)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if "ne fait pas foi" in (r.stdout or ""):
        raise SystemExit("le juge a été appelé hors D18 — ce verdict ne compte pas")
    fautes = [ligne.strip() for ligne in (r.stdout or "").splitlines() if "CASSEE" in ligne]
    return r.returncode == 0, fautes


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Les quatre effectifs de la porte 07 — D17")
    ap.add_argument("--detail", action="store_true", help="nommer chaque manquant")
    a = ap.parse_args(argv)

    compte_avant = registry.counted_tests()
    entrees = charger_recensement()
    par_pdf = fiches_par_pdf()

    atteignables = [e for e in entrees if e["status"] == "atteignable"]
    inatteignables = [e for e in entrees if e["status"] != "atteignable"]

    # -- G1 ------------------------------------------------------------------
    fichees, manquants = [], []
    for e in atteignables:
        k = cle(e)
        (fichees if k and k in par_pdf else manquants).append(e)

    # LE CONTRÔLE DE `L21` : les deux moitiés doivent reconstituer la
    # population. Sans lui, un élément sans clé sort du compte SANS ERREUR,
    # et du côté qui arrange.
    reconstitue = len(fichees) + len(manquants) == len(atteignables)

    # -- G2 ------------------------------------------------------------------
    rouges: list[tuple[Path, list[str]]] = []
    toutes = sorted(FICHES.glob("*.json"))
    for f in toutes:
        vert, fautes = juger(f)
        if not vert:
            rouges.append((f, fautes))

    # -- G3 ------------------------------------------------------------------
    g3_sans_objet = not PRODUITES.is_file()
    retouchees: list[str] = []
    if not g3_sans_objet:
        produites = json.loads(PRODUITES.read_text(encoding="utf-8"))
        retouchees = [n for n, d in produites.items() if d.get("retouchee")]

    # -- G4 ------------------------------------------------------------------
    sans_raison = [e for e in inatteignables if not e.get("reason")]

    # -- rendu ---------------------------------------------------------------
    pdf = sum(1 for e in atteignables if e.get("text_format") == "pdf")
    autre = len(atteignables) - pdf
    print(f"recensement : {len(entrees)} entrées — {len(atteignables)} atteignables "
          f"({pdf} PDF, {autre} autre), {len(inatteignables)} inatteignables")
    print(f"fiches produites : {len(toutes)}\n")

    # `G1` A DEUX LECTURES, ET CE SCRIPT NE TRANCHE PAS ENTRE ELLES.
    # `D17` compte les « atteignables non fichés », et l'entrée 9 est
    # `atteignable` : son texte s'obtient sans péage. Mais elle est en HTML, et
    # `F4` exige un `source.pdf` tandis que `D18` ne traite que les PDF — d'où
    # `corpus/extract_fiche.py --list`, qui la range « hors d'atteinte du
    # fichage » et annonce 7. Les deux lectures sont défendables ; les départager
    # demande une décision écrite, pas un choix de programmeur. Les deux sont
    # donc imprimées, et la plus exigeante fait le verdict.
    infichables = [e for e in manquants if (e.get("text_format") or "pdf") != "pdf"]

    g1, g2, g3, g4 = len(manquants), len(rouges), len(retouchees), len(sans_raison)
    g3_txt = "  —" if g3_sans_objet else f"{g3:>3}"
    g3_note = ("SANS OBJET — aucun extracteur n'a produit en série"
               if g3_sans_objet else "(exige 0)")
    print(f"  G1  atteignables non fichés                  {g1:>3}   (exige 0)")
    print(f"  G2  fiches cassant D16                       {g2:>3}   (exige 0)")
    print(f"  G3  fiches retouchées à la main              {g3_txt}   {g3_note}")
    print(f"  G4  inatteignables sans raison écrite        {g4:>3}   (exige 0)")

    if infichables:
        print("\n  ATTENTION — `G1` a DEUX lectures, et ce script ne tranche pas :")
        print(f"    {g1} en comptant tout atteignable non fiché (D17, lecture littérale)")
        print(f"    {g1 - len(infichables)} en écartant les {len(infichables)} atteignable(s) "
              f"NON FICHABLE(S) en l'état,")
        print("      dont le texte n'est pas un PDF — `F4` exige `source.pdf` et `D18` ne")
        print("      traite que les PDF. C'est le compte de corpus/extract_fiche.py --list.")
        print("    Le verdict ci-dessous retient la lecture LA PLUS EXIGEANTE. Les")
        print("    départager demande une décision écrite (D18 § Ce qui reste ouvert).")

    if a.detail:
        if manquants:
            print("\nG1 — atteignables non fichés :")
            for e in manquants:
                fmt = e.get("text_format") or "?"
                note = "" if cle(e) else ("   <- SANS PDF : invisible à tout "
                                          "rapprochement par nom (L21)")
                print(f"   entrée {e['entry']:>2} [{fmt:>4}] {e['citation'][:70]}{note}")
        if rouges:
            print("\nG2 — fiches cassant D16 :")
            for f, fautes in rouges:
                print(f"   {f.stem}")
                for x in fautes:
                    print(f"      {x}")
        if sans_raison:
            print("\nG4 — inatteignables sans raison :")
            for e in sans_raison:
                print(f"   entrée {e['entry']:>2} {e['citation'][:70]}")

    # -- verdict -------------------------------------------------------------
    fautes: list[str] = []
    if not reconstitue:
        fautes.append(
            f"les deux moitiés ne reconstituent pas la population : "
            f"{len(fichees)} + {len(manquants)} != {len(atteignables)} (L21)"
        )
    for nom, n in (("G1", g1), ("G2", g2), ("G4", g4)):
        if n:
            fautes.append(f"{nom} = {n}, exige 0")
    if not g3_sans_objet and g3:
        fautes.append(f"G3 = {g3}, exige 0")

    compte = registry.counted_tests()
    if compte != compte_avant:
        fautes.append(f"cette porte a fait passer counted_tests de {compte_avant} "
                      f"à {compte} ; elle ne doit rien dépenser")

    print()
    if fautes:
        print("PORTE 07 : NON FRANCHIE")
        for x in fautes:
            print(f"  - {x}")
    elif g3_sans_objet:
        print("PORTE 07 : NON FRANCHIE — G1, G2 et G4 sont tenus, mais G3 est SANS OBJET.")
        print("  Une porte à moitié franchie est une porte non franchie (CLAUDE.md).")
        print("  G3 demande un extracteur qui produise en série, et le registre de ce")
        print("  qu'il a produit : corpus/PRODUCED.json.")
    else:
        print("PORTE 07 : FRANCHIE — les quatre effectifs sont à zéro.")

    print(f"  registre : {len(registry.read_all())} lignes, {compte} test(s) compté(s), "
          f"inchangé par cette porte ; harnais {registry.code_hash()}")
    print("  AUCUN IC N'EST CALCULÉ ICI.")
    return 1 if (fautes or g3_sans_objet) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
