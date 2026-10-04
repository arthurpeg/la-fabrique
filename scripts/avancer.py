"""La réaction en chaîne : tout ce qui ne demande plus d'IA se fait tout seul.

Après chaque passage d'un sous-agent (recette, codeurs), l'orchestrateur lance
ce script. Il fait, dans l'ordre, **chaque étape déterministe qui est prête**,
et dit ce qui bloque le reste :

1. une fiche dont la recette déclare un marché absent de notre univers
   s'écarte du lot (`D38`, preuve `univers`) — tant que la mesure n'a pas
   commencé ;
2. une fiche dont les deux codages sont verts et sans verdict de concordance à
   leur empreinte passe au double codage (`D34`) ;
3. les hypothèses des fiches vérifiées s'écrivent (étape 8) **et se commitent
   aussitôt** : la date du commit prouve qu'elles précèdent le résultat ;
4. **quand le lot est complet** — chaque entrée a son hypothèse, ou a été
   écartée — : la matrice de corrélation (étape 9), puis **la mesure des IC**
   (étape 10), la porte 09, le tableau de bord, et un commit.

**Pourquoi la mesure attend le lot entier, et pas chaque fiche.** BH se calcule
sur le lot clos (`D25`) ; aucune fiche ne s'écarte plus après la première mesure
(`D28`, `D34`) — mesurer tôt figerait le lot avec des entrées impossibles à
finir ; et la matrice de corrélation doit couvrir tout le lot avant BH.

**Un seul arrêt volontaire** : si la matrice montre des paires franchement
négatives, `D25` impose de choisir BH ou BY **avant** de mesurer. C'est une
décision de l'opérateur ; le script s'arrête et le dit.

    python scripts/avancer.py              # fait tout ce qui est prêt
    python scripts/avancer.py --sans-mesure
    python scripts/avancer.py --etat       # dit seulement ce qui bloque
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from codage_verifie import (  # noqa: E402
    CONCORDANCE,
    RECETTES,
    TOURS_MAX,
    concordance,
    jugement_vert,
    lire,
    principal_de,
    temoin_path,
    univers_de,
)
from gate_09 import CORR_FILE, LOT_FILE, STAGE  # noqa: E402

from harness import registry  # noqa: E402

SEUIL_NEGATIF = -0.1  # D25 : une paire sous ce seuil demande de choisir BH ou BY


def lancer(*args: str) -> tuple[int, str]:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, *args], cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


def commit(message: str, *chemins: str) -> None:
    subprocess.run(["git", "add", *chemins], cwd=REPO, capture_output=True)
    r = subprocess.run(["git", "commit", "-q", "-m", message], cwd=REPO,
                       capture_output=True, text=True)
    if r.returncode == 0:
        subprocess.run(["git", "push", "-q"], cwd=REPO, capture_output=True)
        print(f"  commit : {message.splitlines()[0]}")


def mesure_commencee(entries: list[dict]) -> bool:
    ids = {e.get("signal_id") for e in entries} | {e["fiche_id"] for e in entries}
    return any(r.get("stage") == STAGE and r.get("signal_id") in ids
               for r in registry.read_all())


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La réaction en chaîne")
    ap.add_argument("--sans-mesure", action="store_true", help="s'arrêter avant l'étape 9")
    ap.add_argument("--etat", action="store_true", help="ne rien faire, dire ce qui bloque")
    a = ap.parse_args(argv)
    faire = not a.etat

    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    entries = lot["fiches"]
    commencee = mesure_commencee(entries)
    tours = {}
    dernier = {}  # D49 : un tour CONCORDANT à un autre horizon se refait, il ne s'écarte pas
    for c in lire(CONCORDANCE):
        tours[c["fiche_id"]] = tours.get(c["fiche_id"], 0) + 1
        dernier[c["fiche_id"]] = c["verdict"]

    # 0 — D44 : la base fait foi pour les fiches. On tire celles qu'une autre
    # session a versées, puis on pousse les nouvelles d'ici. Sans réseau, on
    # continue sur le miroir, et on le dit.
    if faire:
        for sens in ("--tirer", "--pousser"):
            rc, out = lancer("corpus/fiches_store.py", sens)
            print("  fiches " + (out.splitlines()[-1] if out and rc == 0
                                 else f"{sens} impossible (réseau ?) : on continue sur le miroir"))

    # 1 et 2 — fiche par fiche
    bloque: dict[str, list[str]] = {}
    for e in list(entries):
        fid = e["fiche_id"]
        # D41 : une hypothèse D40 peut précéder le codage ; la fiche passe quand
        # même par toutes les étapes de codage. Seule une hypothèse qui a
        # pré-enregistré la grille entière ne s'écarte pas pour son marché.
        grille = (e.get("universe") or {}).get("grille", False)
        rp = RECETTES / f"{fid}.json"
        u = univers_de(json.loads(rp.read_text(encoding="utf-8"))) if rp.is_file() else None
        if u is not None and not u["exact"] and not grille:
            if commencee:
                bloque.setdefault("marché absent, mais la mesure a commencé", []).append(fid)
            elif faire:
                rc, out = lancer("scripts/ecarter_du_lot.py", fid, "--preuve", "univers",
                                 "--motif", f"marché du papier absent : {u['studied']}")
                print(f"  écartée (D38) : {fid}" if rc == 0 else f"  écart refusé : {fid} — {out}")
            continue
        p = principal_de(fid)
        if concordance(fid, p)[0]:
            if u is None and not grille:
                bloque.setdefault("vérifiée, recette sans marché (D38) : refaire la recette",
                                  []).append(fid)
            continue
        vert_p, vert_t = jugement_vert(p)[0], jugement_vert(temoin_path(p))[0]
        if not (rp.is_file()):
            bloque.setdefault("recette à faire", []).append(fid)
        elif not (vert_p and vert_t):
            bloque.setdefault("deux codages verts à obtenir", []).append(fid)
        elif tours.get(fid, 0) >= TOURS_MAX and dernier.get(fid) != "CONCORDANT":
            bloque.setdefault("discordante au dernier tour : à écarter", []).append(fid)
        elif faire:
            rc, out = lancer("scripts/double_codage.py", fid)
            verdict = "CONCORDANT" if rc == 0 else "DISCORDANT ou refusé"
            print(f"  double codage : {fid} — {verdict}")
            if rc != 0:
                bloque.setdefault("discordante : § 2.7 du tutoriel", []).append(fid)

    # 3 — relier les hypothèses D40 au lot, et dire celles qui restent à écrire
    # (D41). Ce script n'écrit aucune hypothèse : elles s'écrivent au format de D40
    # et se jugent par hypotheses/score_hypothese.py.
    if faire:
        rc, out = lancer("scripts/hypotheses_lot.py", "--lier")
        print("  " + (out.splitlines()[0] if out else ""))
        if "reliée(s)" in out and not out.startswith("0 "):
            commit("Lot : hypotheses D40 reliees, avec leur univers, avant toute mesure\n\n"
                   "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
                   "hypotheses/LOT-09.json")
    for e in entries:
        if not e.get("ref") and concordance(e["fiche_id"], principal_de(e["fiche_id"]))[0]:
            bloque.setdefault("vérifiée, hypothèse D40 à écrire", []).append(e["fiche_id"])

    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    entries = lot["fiches"]
    manquent = [e["fiche_id"] for e in entries if not e.get("ref")]
    faites = len(entries) - len(manquent)
    print(f"\nlot {LOT_FILE.stem} : {faites}/{len(entries)} hypothèses écrites, "
          f"{len(lot.get('ecartees_codage') or [])} écartée(s) avant mesure")
    for raison, fids in bloque.items():
        print(f"  bloque — {raison} : {len(fids)}")
        for f in fids[:8]:
            print(f"      {f}")
    if manquent:
        print("La mesure attend que chaque entrée ait son hypothèse, ou soit écartée.")
        return 0
    if a.sans_mesure or not faire:
        print("Lot complet : la mesure est prête (relancer sans --sans-mesure / --etat).")
        return 0

    # 4 — le lot est complet : matrice, mesure, porte, tableau de bord
    if not CORR_FILE.is_file() or json.loads(CORR_FILE.read_text(encoding="utf-8")).get(
            "signal_ids") != sorted({e["signal_id"] for e in entries}):
        rc, out = lancer("scripts/lot_correlations.py")
        print(out.splitlines()[-1] if out else "")
        if rc:
            print("ARRÊT : la matrice de corrélation n'a pas pu s'écrire.")
            return 1
        commit("Matrice de correlation du lot, avant la mesure (D25)\n\n"
               "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", str(CORR_FILE))
    corr = json.loads(CORR_FILE.read_text(encoding="utf-8"))
    negatives = [p for p in corr["pairs"] if (p["correlation"] or 0) < SEUIL_NEGATIF]
    if negatives:
        print(f"ARRÊT VOLONTAIRE : {len(negatives)} paire(s) sous {SEUIL_NEGATIF}. D25 impose de "
              "choisir BH ou BY AVANT la mesure : c'est une décision de l'opérateur.")
        return 2
    rc, out = lancer("scripts/measure_lot.py", "--run", "--je-mesure")
    print(out)
    if rc:
        print("ARRÊT : la mesure a refusé ; ses préalables sont nommés ci-dessus.")
        return 1
    commit("Mesure du lot : IC inscrits au registre (etape 10)\n\n"
           "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
           "registry/tests.jsonl", "scripts/out/rapports")
    rc, out = lancer("scripts/gate_09.py")
    print(out)
    lancer("scripts/tableau_de_bord.py")
    print("Tableau de bord régénéré : scripts/out/tableau_de_bord.html")
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
