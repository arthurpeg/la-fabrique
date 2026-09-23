"""La calibration du codeur — `D23` § Le choix, et surtout § Pourquoi.

`D06` désignait deux étalons pour la porte 08 : Gao (entrée 1) et Baltussen
(entrée 2), implémentés **à la main**. L'idée était de comparer le signal produit
par un agent à l'implémentation humaine du même papier. `D23` a dû y renoncer
comme **seuil** — l'entrée 1 est inatteignable (`L20`), l'entrée 2 n'était pas
fichée, et `F43` a tranché qu'un seuil sur trois items ne distingue pas un
automate correct d'un automate chanceux ; sur un item, la question ne se pose
plus.

Mais `D23` a gardé la mesure comme **calibration** : *« Quand l'entrée 2 sera
fichée, on fera coder Baltussen et on inscrira la corrélation obtenue au
§ Journal. Elle NE CONDITIONNE RIEN. »* L'entrée 2 a été fichée le 2026-09-23 ;
ce script produit ce chiffre.

**CE N'EST PAS UN IC, ET LA DISTINCTION N'EST PAS COSMÉTIQUE.** Un IC est la
corrélation d'un signal avec les **rendements futurs** ; il se calcule dans la
seule fonction d'évaluation officielle et il écrit au registre (invariant III).
Ce qui est mesuré ici est la corrélation de **deux signaux entre eux** — aucun
rendement n'entre dans le calcul, aucune ligne n'est écrite, et le dénominateur
de la phase 15 ne bouge pas. Le script le vérifie et casse si le compte a bougé.

**Ce que ce chiffre dit, et ce qu'il ne dit pas.** Il dit à quel point le codeur
retrouve une lecture humaine du même papier sur un sujet connu. Il ne dit pas que
le codeur a raison : l'implémentation humaine n'est pas la vérité, c'est une
lecture. Une corrélation basse peut signifier que le codeur a dévié — ou que
l'humain avait simplifié.

    python scripts/calibrate_coder.py <module_produit> <module_humain>
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from harness import registry  # noqa: E402
from panel import Panel  # noqa: E402

ASOF = "2018-06-15 20:00"
HORIZON_BARS = 30
MIN_PAIRES = 30  # sous ce nombre, une corrélation ne dit rien


def importer(cible: str):
    if cible.endswith(".py") or "/" in cible or "\\" in cible:
        chemin = Path(cible).resolve()
        if not chemin.is_file():
            raise SystemExit(f"module introuvable : {cible}")
        cible = ".".join(chemin.relative_to(REPO).with_suffix("").parts)
    return importlib.import_module(cible)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La calibration du codeur — D23")
    ap.add_argument("produit", help="le module rendu par le codeur")
    ap.add_argument("humain", help="l'implémentation écrite à la main")
    a = ap.parse_args(argv)

    compte_avant = registry.counted_tests()
    lignes_avant = len(registry.read_all())

    mp, mh = importer(a.produit), importer(a.humain)
    panel = Panel.open(ASOF, slice="pool")
    sp = mp.scores(panel, horizon_bars=HORIZON_BARS)
    sh = mh.scores(panel, horizon_bars=HORIZON_BARS)

    print(f"produit : {mp.SIGNAL_ID}   signe attendu {mp.EXPECTED_SIGN:+d}")
    print(f"humain  : {mh.SIGNAL_ID}   signe attendu {mh.EXPECTED_SIGN:+d}")
    print(f"cellules : {len(sp)} contre {len(sh)}\n")

    communes = sorted(set(sp) & set(sh))
    if not communes:
        raise SystemExit("aucune cellule commune — les deux signaux ne parlent pas du même objet")

    print(f"{'cellule':<14}{'paires':>9}{'corrélation':>14}")
    tous_p, tous_h = [], []
    for cle in communes:
        a_, b_ = sp[cle].align(sh[cle], join="inner")
        ok = np.isfinite(a_) & np.isfinite(b_)
        a_, b_ = a_[ok], b_[ok]
        if len(a_) < MIN_PAIRES:
            print(f"{str(cle):<14}{len(a_):>9}{'  trop peu':>14}")
            continue
        r = float(pd.Series(a_.to_numpy()).corr(pd.Series(b_.to_numpy())))
        print(f"{str(cle):<14}{len(a_):>9}{r:>14.4f}")
        tous_p.append(a_.to_numpy())
        tous_h.append(b_.to_numpy())

    manquantes = sorted(set(sp) ^ set(sh))
    if manquantes:
        print(f"\ncellules notées par UN SEUL des deux : {len(manquantes)}")
        for cle in manquantes[:6]:
            lequel = "produit seul" if cle in sp else "humain seul"
            print(f"   {cle} — {lequel}")

    if not tous_p:
        raise SystemExit("aucune cellule n'a assez de paires pour une corrélation")

    p = np.concatenate(tous_p)
    h = np.concatenate(tous_h)
    globale = float(pd.Series(p).corr(pd.Series(h)))
    print(f"\nCORRÉLATION POOLÉE : {globale:.4f} sur {len(p)} paires, "
          f"{len(tous_p)} cellule(s)")

    compte = registry.counted_tests()
    if compte != compte_avant or len(registry.read_all()) != lignes_avant:
        raise SystemExit(
            f"CETTE CALIBRATION A TOUCHÉ AU REGISTRE : {lignes_avant} -> "
            f"{len(registry.read_all())} lignes, {compte_avant} -> {compte} tests. "
            "Elle ne doit rien écrire : ce n'est pas un IC."
        )
    print(f"  registre inchangé : {lignes_avant} lignes, {compte} test(s) compté(s)")
    print("\n  CE N'EST PAS UN IC — aucun rendement n'entre dans ce calcul.")
    print("  Cette mesure NE CONDITIONNE RIEN (D23). À recopier au § Journal de D23.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
