"""Les hypothèses pré-enregistrées du lot — étape 8 de la phase 09.

Pour chaque fiche du lot (`hypotheses/LOT-09.json`) dont le signal est **codé**,
écrit `hypotheses/Hnn-<fiche>.md` et inscrit dans le lot sa `ref` et son
`signal_id` — ce que `scripts/gate_09.py` attend (« chaque entrée gagnera son
`ref` d'hypothèse et son `signal_id` »).

**Écrite avant toute mesure, et par construction** : l'hypothèse ne peut pas
dépendre d'un résultat, parce qu'il n'en existe aucun. Le script refuse
d'écrire l'hypothèse d'un signal qui a déjà une ligne au registre (`D28`).

**Rédigée mécaniquement, sans jugement** : le signe attendu est celui que le
signal déclare (`EXPECTED_SIGN`, choisi par le codeur depuis la fiche) ;
l'affirmation, le mécanisme et ce qui ne transpose pas sont **recopiés** de la
fiche ; les seuils qui la contrediraient sont ceux de `D25` et de `D01`. Aucune
magnitude n'est inventée. Une hypothèse plus riche — un mécanisme discuté, une
comparaison entre signaux — reste possible à la main, mais **avant** la mesure.

**Jamais réécrite** (`hypotheses/README.md`) : un fichier existant n'est pas
touché, et une entrée qui a déjà sa `ref` est laissée telle quelle.

    python scripts/hypotheses_lot.py --status   # quelle fiche en est où
    python scripts/hypotheses_lot.py --write    # écrit celles dont le signal est codé
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from codage_verifie import concordance, principal_de  # noqa: E402
from code_signal import fiche_files, signaux_existants  # noqa: E402
from gate_09 import LOT_FILE, importer_par_signal_id  # noqa: E402

from harness import registry  # noqa: E402

HYP_DIR = REPO / "hypotheses"
HORIZON = "30min"  # l'horizon de la grille et des signaux (`horizon_bars=30`)


def prochain_numero() -> int:
    nums = [int(m.group(1)) for p in HYP_DIR.glob("H*.md")
            if (m := re.match(r"H(\d+)-", p.name))]
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    for e in lot.get("fiches") or lot.get("hypotheses") or []:
        if (m := re.match(r"H(\d+)$", e.get("ref") or "")):
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def texte(v) -> str:
    """Le texte d'un champ de fiche, qu'il soit une chaîne ou `{value: ...}`."""
    if isinstance(v, dict):
        return str(v.get("value") or v.get("reason") or "")
    if isinstance(v, list):
        return " ; ".join(texte(x) for x in v)
    return str(v or "")


def rediger(ref: str, fiche: dict, module, fiche_path: Path) -> str:
    signe = "positif" if module.EXPECTED_SIGN > 0 else "négatif"
    contraire = "négatif" if module.EXPECTED_SIGN > 0 else "positif"
    src = fiche.get("source") or {}
    tr = fiche.get("transposability") or {}
    mod = Path(module.__file__).relative_to(REPO).as_posix()
    return f"""# {ref} — {src.get("title") or fiche["fiche_id"]}

**Écrite le :** {date.today().isoformat()}, avant toute mesure sur nos données
**Signal :** `{module.SIGNAL_ID}` (`{mod}`)
**Fiche :** `{fiche_path.relative_to(REPO).as_posix()}`
**Origine :** {module.PAPER}
**Lot :** `hypotheses/LOT-09.json` (`D36`) — mesurée une fois, à l'étape 10.
**Rédaction :** mécanique (`scripts/hypotheses_lot.py`) : signe tiré du signal,
affirmation et mécanisme recopiés de la fiche, seuils de `D25`. Rien n'a été vu.

## Ce qui est affirmé

Le score du signal `{module.SIGNAL_ID}` prédit le rendement des
**30 minutes** suivantes, avec un signe **{signe}**.

L'affirmation du papier, telle que la fiche la rapporte :

> {texte(fiche.get("claim"))}

## Le mécanisme, et ce qui ne transpose pas

- **Construction** (fiche) : {texte(fiche.get("signal_construction"))}
- **Ce qui se transpose** (fiche) : {texte(tr.get("what_transfers"))}
- **Ce qui ne se transpose pas** (fiche) : {texte(tr.get("what_does_not_transfer"))}

## Le domaine

- **Univers :** les cellules retenues de la grille (`D01` §3).
- **Horizon :** 30 minutes, à l'intérieur de la fenêtre et de la séance.
- **Tranche :** `pool` entière, `asof` 2023-12-29 20:00 UTC (`D29`).
- **Une seule mesure**, par le harnais, au stage `09-passage` (`D28`).

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **{signe}** |
| Seuil de rétention | `BH` à `q` = 0,10 sur le lot, test **unilatéral** au signe (`D25`) |
| Cible économique | IC de 0,018 à 0,031 pour un IR de 1 (`D01` §2) |

## Ce qui la contredirait

- Un IC poolé **{contraire}** : le signe affirmé est faux.
- Une `p`-valeur unilatérale qui ne passe pas le seuil de `BH` à son rang :
  indistinguable du bruit sur cet univers, au nombre de tests près.
- Un IC du bon signe mais sous **0,018** : statistiquement présent peut-être,
  économiquement sans intérêt (`D01` §2).
"""


def charger_lot() -> dict:
    return json.loads(LOT_FILE.read_text(encoding="utf-8"))


def do_status() -> int:
    lot = charger_lot()
    codes = signaux_existants()
    for e in lot["fiches"]:
        fid = e["fiche_id"]
        if e.get("ref"):
            etat = "hypothèse " + e["ref"]
        elif fid not in codes:
            etat = "signal à coder"
        elif not concordance(fid, principal_de(fid))[0]:
            etat = "codé, double codage à faire (D34)"
        else:
            etat = "vérifié, hypothèse à écrire"
        print(f"  {etat:<34} {fid}")
    faits = sum(1 for e in lot["fiches"] if e.get("ref"))
    print(f"\n{faits}/{len(lot['fiches'])} hypothèses écrites")
    return 0


def do_write() -> int:
    lot = charger_lot()
    codes, fiches = signaux_existants(), fiche_files()
    touches = {r.get("signal_id") for r in registry.read_all()}
    ecrites = 0
    for e in lot["fiches"]:
        fid = e["fiche_id"]
        if e.get("ref") or fid not in codes:
            continue
        if fid in touches:
            print(f"  REFUS {fid} : son signal a déjà une ligne au registre — il n'est "
                  "plus à l'aveugle et ne peut pas entrer dans le lot (D28)")
            continue
        ok, pourquoi = concordance(fid, principal_de(fid))
        if not ok:
            print(f"  ATTENTE {pourquoi} — l'hypothèse s'écrira quand le codage "
                  "sera vérifié (D34)")
            continue
        module = importer_par_signal_id(fid)
        if module.EXPECTED_SIGN not in (1, -1):
            print(f"  REFUS {fid} : EXPECTED_SIGN = {module.EXPECTED_SIGN!r}")
            continue
        ref = f"H{prochain_numero():02d}"
        path = HYP_DIR / f"{ref}-{fid}.md"
        path.write_text(rediger(ref, json.loads(fiches[fid].read_text(encoding="utf-8")),
                                module, fiches[fid]), encoding="utf-8")
        e["ref"], e["signal_id"] = ref, module.SIGNAL_ID
        # Le lot est réécrit APRÈS chaque hypothèse : une coupure ne laisse
        # jamais une hypothèse écrite sans sa ref dans le lot.
        LOT_FILE.write_text(json.dumps(lot, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")
        print(f"  {ref} écrite — {fid}")
        ecrites += 1
    print(f"\n{ecrites} hypothèse(s) écrite(s). Les commiter AVANT toute mesure : "
          "la date du commit est la preuve qu'elles précèdent le résultat.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Hypothèses pré-enregistrées du lot")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    if a.write:
        return do_write()
    if a.status:
        return do_status()
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
