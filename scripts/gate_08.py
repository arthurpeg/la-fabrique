"""PORTE 08 — un signal produit par le codeur passe les six conditions de `D23`.

La porte, telle que `ETAT.md` la pose : *« Une fiche produit un signal exécutable
qui passe la sandbox, sans retouche manuelle. »* `D23` en a fait six conditions à
tolérance zéro, et `scripts/score_signal.py` les vérifie **sur un module**. Ce
fichier-ci fait ce que le juge ne fait pas : il regarde **tout ce que le codeur a
produit**, et répond oui ou non pour la porte.

**Pourquoi il existe séparément du juge.** La porte 07 a passé trois jours sans
compteur, et son chiffre a vécu dans la prose de `ETAT.md`, où il a été faux
trois fois (`L21`). Les portes 01 à 07 ont chacune leur script ; celle-ci aussi.
Un effectif sans script est un effectif qu'on recopie.

**Ce que la porte exige, et qui est plus étroit qu'il n'y paraît :**

1. **au moins un signal produit par le codeur** passe les **six** conditions — un
   verdict partiel (`--no-data`) ne compte pas, `D23` les voulant ENSEMBLE ;
2. **aucun signal produit n'a été retouché à la main**, même ceux qui échouent.
   Un codeur dont on répare une sortie sur dix n'est pas un codeur ; c'est `G3`
   de `D17` transposé, et c'est la clause qui porte vraiment la porte.

**Les trois signaux écrits à la main ne comptent pas.** `gao_2018`,
`baltussen_2021_intraday_momentum` et `heston_2010_periodicity` sont les étalons
de `D06`, antérieurs aux fiches. Ils ne figurent pas dans
`signals/PRODUCED.json`, et c'est ce registre — non le contenu de `signals/` —
qui dit ce que le codeur a produit. Les compter gonflerait son bilan d'un travail
humain.

**AUCUN IC N'EST CALCULÉ ICI**, et le script casse si le registre a bougé.

    python scripts/gate_08.py
    python scripts/gate_08.py --no-data   # inspection rapide, NE FRANCHIT RIEN
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from harness import registry  # noqa: E402

FICHES = REPO / "corpus" / "fiches"
PRODUCED = REPO / "signals" / "PRODUCED.json"
JUGE = REPO / "scripts" / "score_signal.py"


def juger(module: Path, fiche: Path, sans_donnees: bool) -> tuple[bool, list[str]]:
    argv = [sys.executable, str(JUGE), str(module), "--fiche", str(fiche)]
    if sans_donnees:
        argv.append("--no-data")
    r = subprocess.run(argv, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    sortie = (r.stdout or "") + (r.stderr or "")
    lignes = [x.strip() for x in sortie.splitlines()
              if x.strip().startswith("S") and " : " in x]
    partiel = "n'ont pas été jugées" in sortie
    return (r.returncode == 0 and not partiel), lignes


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La porte 08 — D23")
    ap.add_argument("--no-data", action="store_true",
                    help="S1, S2, S5, S6 seuls — inspection, ne franchit rien")
    a = ap.parse_args(argv)

    compte_avant = registry.counted_tests()
    lignes_avant = len(registry.read_all())

    if not PRODUCED.is_file():
        print("PORTE 08 : NON FRANCHIE")
        print("  `signals/PRODUCED.json` n'existe pas — le codeur n'a rien produit,")
        print("  et `S6` serait SANS OBJET sur tout module. Voir `L22` : une")
        print("  condition qu'on ne peut pas mesurer n'est pas tenue, elle est absente.")
        return 1

    registre = json.loads(PRODUCED.read_text(encoding="utf-8"))
    if not registre:
        print("PORTE 08 : NON FRANCHIE — registre de production vide.")
        return 1

    print(f"signaux produits par le codeur : {len(registre)}")
    total_essais = sum(len(d.get("attempts") or [1]) for d in registre.values())
    print(f"essais du codeur : {total_essais} pour {len(registre)} signal(aux) "
          f"— {total_essais / len(registre):.2f} par signal\n")

    passants, fautes = [], []
    for signal_id, d in sorted(registre.items()):
        module = REPO / d["path"]
        fiche = FICHES / f"{signal_id}.json"
        if not module.is_file():
            fautes.append(f"{signal_id} : module ABSENT ({d['path']}) — un signal "
                          "produit puis supprimé est une retouche, la plus radicale")
            continue
        if not fiche.is_file():
            fautes.append(f"{signal_id} : aucune fiche de ce nom — un signal se juge "
                          "CONTRE la fiche qu'il prétend coder")
            continue
        ok, verdicts = juger(module, fiche, a.no_data)
        n = len(d.get("attempts") or [1])
        print(f"  {'PASSE' if ok else 'REFUSÉ'}  {signal_id}  (essai {n})")
        for v in verdicts:
            print(f"      {v}")
        if ok:
            passants.append(signal_id)

    # CLAUSE 2 — elle vaut pour TOUS les produits, pas seulement les passants.
    # Un codeur dont on répare une sortie sur dix n'est pas un codeur.
    retouchees = [
        signal_id for signal_id, d in registre.items()
        if (REPO / d["path"]).is_file()
        and hashlib.sha256((REPO / d["path"]).read_bytes()).hexdigest()[:16]
        != d["sha256_16"]
    ]
    if retouchees:
        fautes.append(
            f"{len(retouchees)} signal(aux) MODIFIÉ(S) depuis leur production : "
            f"{', '.join(retouchees)}. `S6` de `D23` exige zéro retouche, et la "
            "clause vaut pour tout ce que le codeur a produit, pas seulement pour "
            "ce qui passe."
        )

    compte = registry.counted_tests()
    if compte != compte_avant or len(registry.read_all()) != lignes_avant:
        fautes.append(f"cette porte a touché au registre : {lignes_avant} -> "
                      f"{len(registry.read_all())} lignes, {compte_avant} -> {compte} "
                      "tests. Elle ne doit rien dépenser (D23)")

    print()
    if a.no_data:
        print("PORTE 08 : NON JUGÉE — `--no-data` ne vérifie que S1, S2, S5, S6.")
        print("  Les six conditions valent ENSEMBLE (D23) : un verdict partiel ne")
        print("  franchit rien. Relancer sans `--no-data`.")
        return 1
    if fautes:
        print("PORTE 08 : NON FRANCHIE")
        for f in fautes:
            print(f"  - {f}")
    elif not passants:
        print("PORTE 08 : NON FRANCHIE — aucun signal produit ne tient les six conditions.")
    else:
        print(f"PORTE 08 : FRANCHIE — {len(passants)} signal(aux) sur {len(registre)} "
              "tiennent les six conditions,")
        print("  et aucun signal produit n'a été retouché à la main.")
        for s in passants:
            print(f"      {s}")
        print("\n  CE QUE CETTE PORTE NE DIT PAS : que le signal soit LE BON. Un signal")
        print("  fidèle à une fiche creuse passe les six conditions — `D23` § Pourquoi.")
        print("  La pertinence n'aura de dénominateur qu'en phase 09.")

    print(f"  registre : {len(registry.read_all())} lignes, {compte} test(s) compté(s), "
          f"inchangé par cette porte ; harnais {registry.code_hash()}")
    print("  AUCUN IC N'EST CALCULÉ ICI.")
    return 1 if (fautes or not passants) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
