"""La mesure du lot — étape 10 de la phase 09. LE SEUL SCRIPT QUI DÉPENSE DES TESTS.

Pour chaque hypothèse du lot : **une** mesure, par le harnais (`evaluate`), au
stage `09-passage`, sur toute la tranche `pool` à l'instant fixé (`D29`). Chaque
IC s'écrit au registre dans le même geste (invariant III) et compte au
dénominateur de la phase 15. Ensuite, `scripts/gate_09.py` juge.

**Il refuse de mesurer tant que le harnais du lot n'est pas désigné.** Des
modifications du harnais sont annoncées et doivent être faites AVANT : frais et
`slippage_bp` (`D26`), trou d'`extra` dans `registry.settle()` (`D28`),
diagnostic par année (`D29`). Toute modification change l'empreinte et PÉRIME
les mesures faites avant — et un lot périmé ne peut pas être remesuré : une
seconde mesure est une ligne hors protocole (`D28`). Mesurer trop tôt, c'est
brûler le lot. `HARNAIS_DU_LOT` doit donc être renseigné **par une décision
écrite**, à l'empreinte du harnais final.

**Il vérifie tout ce que la porte 09 vérifiera, AVANT la première mesure** :
le lot, chaque hypothèse écrite, la matrice de corrélation datée après la
clôture, et **aucune ligne du registre qui touche déjà le lot**. Un défaut
découvert après avoir mesuré ne se répare plus.

**Il reprend sans jamais mesurer deux fois** : une hypothèse qui a déjà sa
mesure officielle est sautée ; une coupure au milieu du lot se relance.

    python scripts/measure_lot.py --check             # préalables, AUCUN calcul
    python scripts/measure_lot.py --run --je-mesure   # mesure, écrit au registre
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from codage_verifie import cellules_de, fautes_d34_du_lot, fautes_univers  # noqa: E402
from gate_09 import (  # noqa: E402
    ASOF_REQUIRED,
    CORR_FILE,
    HYPOTHESES_DIR,
    LOT_FILE,
    SLICE_REQUIRED,
    STAGE,
    est_officielle,
    importer_par_signal_id,
    lignes_hors_protocole,
)

from harness import registry  # noqa: E402

# D42 : chaque hypothèse est mesurée à SON horizon intraday, déclaré avant la
# mesure (`horizon` de l'entrée du lot, lu dans « Le domaine » par
# hypotheses_lot.py). « cloture » — jusqu'à la clôture de la fenêtre — demande au
# harnais un horizon variable qu'il n'a pas encore : refusé, jamais remplacé.
HORIZON_CLOTURE = "cloture"
# L'empreinte du harnais avec lequel le lot sera mesuré. None tant que la
# décision de harnais groupée (`D26`, `D28`, `D29`) n'est pas prise : elle
# renseigne cette valeur, et nulle part ailleurs.
HARNAIS_DU_LOT: str | None = "94b495fa7525d3b8"  # D35, D37


RAPPORTS = REPO / "scripts" / "out" / "rapports"


def garder_rapport(rapport, univers: dict | None = None) -> Path:
    """Le rapport d'IC ENTIER, recopié tel que le harnais l'a rendu.

    Le registre ne porte que l'IC poolé ; la ventilation par cellule, la
    décomposition du t, les coûts et les avertissements n'existaient qu'à
    l'écran. Ils sont gardés ici, nommés par le `test_id` de la ligne que le
    harnais a écrite : c'est une copie de SA sortie, jamais un calcul de plus
    (invariant III). Le tableau de bord les lit (`scripts/tableau_de_bord.py`).
    """
    import dataclasses  # noqa: PLC0415

    RAPPORTS.mkdir(parents=True, exist_ok=True)
    chemin = RAPPORTS / f"{rapport.test_id}.json"
    donnees = dataclasses.asdict(rapport)
    donnees["render"] = rapport.render()
    # Pour lire à part l'actif du papier et sa classe (D38) : l'univers déclaré.
    donnees["universe"] = univers
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=1, default=str) + "\n",
                      encoding="utf-8")
    return chemin


def charger() -> tuple[dict, list[dict]]:
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    return lot, lot.get("fiches") or lot.get("hypotheses") or []


def prealables() -> tuple[list[str], list[dict]]:
    """Les fautes qui interdisent de mesurer, et les entrées encore à mesurer."""
    fautes: list[str] = []
    lot, entries = charger()
    courant = registry.code_hash()
    if HARNAIS_DU_LOT is None:
        fautes.append("HARNAIS_DU_LOT n'est pas désigné : la décision de harnais groupée "
                      "(frais D26, extra D28, diagnostic D29) doit précéder la mesure")
    elif HARNAIS_DU_LOT != courant:
        fautes.append(f"le harnais a changé : {courant} au lieu de {HARNAIS_DU_LOT}")
    for e in entries:
        ref, sid = e.get("ref"), e.get("signal_id")
        if not ref or not sid:
            fautes.append(f"{e.get('fiche_id')} : pas de ref ou de signal_id (étapes 7 et 8)")
        elif not list(HYPOTHESES_DIR.glob(f"{ref}-*.md")):
            fautes.append(f"{ref} : fichier d'hypothèse absent")
    if not CORR_FILE.is_file():
        fautes.append("matrice de corrélation absente (étape 9)")
    else:
        corr = json.loads(CORR_FILE.read_text(encoding="utf-8"))
        attendus = sorted({e.get("signal_id") for e in entries})
        if sorted(corr.get("signal_ids") or []) != attendus:
            fautes.append("la matrice de corrélation ne couvre pas exactement le lot")
        if (corr.get("measured_at") or "") < (lot.get("declared_at") or "9"):
            fautes.append("la matrice de corrélation n'est pas datée après la clôture du lot")
    registre = registry.read_all()
    fautes += fautes_d34_du_lot(lot, registre, STAGE)
    fautes += fautes_univers(lot)
    # D40, D41 : chaque hypothèse passe son juge, et la bijection avec le lot tient.
    sys.path.insert(0, str(REPO / "hypotheses"))
    import score_hypothese as sh  # noqa: PLC0415

    _, fautes_d40 = sh.juger_ensemble(sh.HYPOTHESES_DIR, sh.fiche_ids_du_lot())
    fautes += [f"D40 : {f}" for f in fautes_d40]
    for r in lignes_hors_protocole(entries, registre, courant):
        fautes.append(f"{r.get('test_id')} touche déjà le lot hors protocole (D28)")
    for e in entries:
        h = e.get("horizon")
        if not h:
            fautes.append(f"{e.get('fiche_id')} : pas d'horizon déclaré (D42)")
        elif h == HORIZON_CLOTURE:
            fautes.append(f"{e.get('ref')} : horizon « jusqu'à la clôture de la fenêtre » — "
                          "le harnais ne sait pas encore le mesurer (D42)")
    a_faire = [e for e in entries
               if not any(est_officielle(r, e, courant) for r in registre)]
    return fautes, a_faire


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Mesure du lot — phase 09")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--je-mesure", action="store_true",
                    help="confirmation explicite : chaque mesure dépense un test")
    a = ap.parse_args(argv)

    fautes, a_faire = prealables()
    if fautes:
        print("MESURE REFUSÉE — préalables non tenus :")
        for f in fautes:
            print(f"  - {f}")
        return 1
    print(f"préalables tenus : {len(a_faire)} hypothèse(s) à mesurer")
    if a.check or not a.run:
        print("--check : AUCUN IC n'a été calculé.")
        return 0
    if not a.je_mesure:
        print("--run exige --je-mesure : chaque mesure dépense un test, et elle est définitive.")
        return 1

    from harness import evaluate, horizon_to_bars
    from panel import Panel

    panel = Panel.open(asof=ASOF_REQUIRED.replace("+00:00", ""), slice=SLICE_REQUIRED)
    avant = registry.counted_tests()
    for i, e in enumerate(a_faire, 1):
        module = importer_par_signal_id(e["signal_id"])
        # D38 : la mesure porte sur les cellules que l'hypothèse a déclarées,
        # et sur elles seules. Le signal note toute la grille ; on ne garde que
        # l'univers écrit AVANT, jamais une cellule choisie après.
        garder = cellules_de(e["universe"]) & set(panel.cells())
        horizon = e["horizon"]
        barres = horizon_to_bars(horizon)
        scores = {c: s for c, s in module.scores(panel, horizon_bars=barres).items()
                  if c in garder}
        rapport = evaluate(scores, panel, horizon,
                           signal_id=e["signal_id"], hypothesis_ref=e["ref"], stage=STAGE)
        print(f"  {i}/{len(a_faire)} {e['ref']} {e['signal_id']:<48} "
              f"IC {rapport.ic:+.5f}  t {rapport.t['final']:+.2f}", flush=True)
        garder_rapport(rapport, e["universe"])
    print(f"\ntests comptés : {avant} -> {registry.counted_tests()}")
    print("Étape suivante : python scripts/gate_09.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
