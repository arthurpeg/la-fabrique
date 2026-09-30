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

from codage_verifie import fautes_d34_du_lot  # noqa: E402
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

HORIZON = "30min"
# L'empreinte du harnais avec lequel le lot sera mesuré. None tant que la
# décision de harnais groupée (`D26`, `D28`, `D29`) n'est pas prise : elle
# renseigne cette valeur, et nulle part ailleurs.
HARNAIS_DU_LOT: str | None = "4806666dc55c46c9"  # D35


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
    for r in lignes_hors_protocole(entries, registre, courant):
        fautes.append(f"{r.get('test_id')} touche déjà le lot hors protocole (D28)")
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

    from harness import evaluate
    from panel import Panel

    panel = Panel.open(asof=ASOF_REQUIRED.replace("+00:00", ""), slice=SLICE_REQUIRED)
    avant = registry.counted_tests()
    for i, e in enumerate(a_faire, 1):
        module = importer_par_signal_id(e["signal_id"])
        rapport = evaluate(module.scores(panel, horizon_bars=30), panel, HORIZON,
                           signal_id=e["signal_id"], hypothesis_ref=e["ref"], stage=STAGE)
        print(f"  {i}/{len(a_faire)} {e['ref']} {e['signal_id']:<48} "
              f"IC {rapport.ic:+.5f}  t {rapport.t['final']:+.2f}", flush=True)
    print(f"\ntests comptés : {avant} -> {registry.counted_tests()}")
    print("Étape suivante : python scripts/gate_09.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
