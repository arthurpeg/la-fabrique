"""Le harnais de l'extracteur pour les papiers moissonnés — phase 09.

Sœur d'`extract_fiche.py`, pour une **population différente**. `extract_fiche.py`
sert les 20 entrées d'`AMORCE.md`, dont dépendent `G1`-`G4` (porte 07, franchie
le 2026-09-23). Ce script sert les papiers promus par `corpus/promote_harvest.py`
depuis le triage du moissonneur (`corpus/harvest_promoted.json`) — et `D20`/`F47`
sont explicites : **leur produit n'entre jamais dans `G1`-`G4`**.

## Pourquoi ce n'est pas la même fonction avec un autre fichier de recensement

`scripts/gate_07.py` ne filtre PAS ses conditions `G2` et `G3` par population :
`G2` juge **toutes** les fiches de `corpus/fiches/*.json`, `G3` compare **toutes**
les entrées de `corpus/PRODUCED.json` à leur empreinte de production. Une fiche
de ce script écrite dans `corpus/fiches/`, ou une production inscrite dans
`corpus/PRODUCED.json`, entrerait dans le calcul de `G2`/`G3` **sans que rien ne
l'ait voulu** — et une seule fiche de cette population qui casserait `D16`
repasserait la porte 07 à NON FRANCHIE, alors qu'elle est franchie et qu'aucune
décision n'a demandé de la rouvrir. C'est exactement la faute que `D24` a
nommée pour `G1` (« deux populations mélangées ») transposée à `G2`/`G3` : la
parade est la même, une séparation dans le STOCKAGE, pas dans la prose.

**Storage séparé, donc :**

| | AMORCE (porte 07) | Moissonné (phase 09) |
|---|---|---|
| Recensement | `corpus/acquisition.json` | `corpus/harvest_promoted.json` |
| Fiches | `corpus/fiches/` | `corpus/fiches_harvest/` |
| Registre `G3`/`S6` | `corpus/PRODUCED.json` | `corpus/PRODUCED_harvest.json` |
| Consignes | `corpus/consignes/` | `corpus/consignes_harvest/` |

Le **juge** est le même — `corpus/score_extraction.py`, les cinq conditions de
`D16` — parce qu'il juge une fiche seule, jamais un répertoire : deux
implémentations du même juge divergeraient tôt ou tard (même raison que
`value_in_quote` unifiée le 2026-09-22).

## Qui peut être l'extracteur — `D16` § Qui peut être l'extracteur, inchangé

**Une session qui a lu la fiche de référence d'un papier ne peut pas être
l'extracteur de ce papier**, ni avoir lu `corpus/fiches_harvest/` en général.
L'extracteur reçoit la consigne produite ici, et rien d'autre du corpus.

## Ce que l'extracteur voit, limitativement

1. `corpus/SCHEMA.md` — le schéma de fiche (`D14`), identique à l'AMORCE ;
2. **le texte du papier**, extraction `default` de `D18` ;
3. la consigne de sortie ci-dessous.

    python corpus/extract_fiche_harvest.py --prepare <fiche_id>
    python corpus/extract_fiche_harvest.py --record <fiche.json>
    python corpus/extract_fiche_harvest.py --judge <fiche.json>
    python corpus/extract_fiche_harvest.py --list

Code de sortie 1 si le papier est inconnu, ou si la fiche jugée ne passe pas.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CENSUS = REPO / "corpus" / "harvest_promoted.json"
HARVEST = REPO / "corpus" / "harvest.json"
SCHEMA = REPO / "corpus" / "SCHEMA.md"
FICHES = REPO / "corpus" / "fiches_harvest"
WORK = REPO / "corpus" / "consignes_harvest"
PRODUCED = REPO / "corpus" / "PRODUCED_harvest.json"

MODE = "default"  # D18, fixe pour tous les papiers — identique à extract_fiche.py

CONSIGNE = """\
# Consigne d'extraction — phase 09 de La Fabrique

Tu produis **une fiche JSON** à partir du texte d'un papier académique, et de
rien d'autre. Tu n'as pas accès au reste du projet, et c'est voulu : une fiche
écrite de mémoire ou d'après un résumé serait sans valeur.

## Ce que tu rends

Un **seul objet JSON**, rien avant, rien après. Pas de bloc de code, pas de
commentaire. Il suit le schéma reproduit ci-dessous, section « SCHÉMA ».

## Les règles qui font rejeter une fiche

1. **Chaque citation (`quoted`) doit se retrouver MOT POUR MOT dans le texte
   fourni.** Copie-la, ne la reformule pas, ne corrige pas sa ponctuation, ne
   remplace pas « at least » par « >= ». Un seul caractère qui diffère et la
   fiche est refusée.
2. **Chaque `value` numérique doit figurer dans sa propre citation**, sauf si tu
   déclares `"derived": true` (nombre que TU as calculé, avec une `note` disant
   comment) ou `"spelled_out": "<le mot>"` (le papier écrit le nombre en toutes
   lettres).
3. **Si le texte fourni est visiblement abîmé** là où la page serait claire —
   scan corrompu, symbole mathématique perdu, tableau mis à plat — mets la chaîne
   ABÎMÉE, telle quelle, dans `quoted_source`, une version lisible dans `quoted`,
   et le motif dans `quoted_repair` parmi `ocr`, `math_notation`, `table`.
   N'invente pas d'autre motif.
4. **N'invente jamais une valeur.** Ce que le papier ne dit pas vaut `null`, avec
   une `reason`. Un `null` est bruyant, une valeur plausible est indétectable.
5. **`transposability.what_does_not_transfer` ne peut pas être vide.** Notre
   univers est de neuf futures intraday ; un papier dont tout transfère n'a pas
   été lu avec attention.

## Ce qu'on te demande vraiment

Pas un résumé. **Ce que le papier affirme, ce qu'il a mesuré, et ce qui en
survivrait chez nous.** Une fiche fidèle mais creuse passe les contrôles et ne
sert à rien : préfère trois résultats qui portent des chiffres à dix qui n'en
portent pas.

---

## SCHÉMA

{schema}

---

## IDENTITÉ DE LA FICHE

- `fiche_id` : `{fiche_id}`
- `source.pdf` : `{pdf}`
- `source.source_url` : `{url}`
- `source.retrieved` : `{retrieved}`
- `written_by` : le nom de la session qui extrait
- `written` : `{today}`

---

## TEXTE DU PAPIER

{text}
"""


def census() -> list[dict]:
    if not CENSUS.is_file():
        raise SystemExit("recensement absent — `python corpus/promote_harvest.py --fetch`")
    return json.loads(CENSUS.read_text(encoding="utf-8"))


def fiche_id_for(row: dict) -> str:
    return Path(row["pdf"]).stem


def entry_of(fiche_id: str) -> dict:
    for row in census():
        if fiche_id_for(row) == fiche_id:
            return row
    raise SystemExit(f"{fiche_id!r} absent de corpus/harvest_promoted.json")


def source_url_and_checked(row: dict) -> tuple[str, str]:
    """Retrouve `source_url`/`checked` dans `harvest.json`, par `openalex_id`.

    `harvest_promoted.json` ne les porte pas lui-même : il n'a pas à dupliquer
    ce que `harvest.json` sait déjà, et une seule source évite qu'elles divergent
    (même raison que `value_in_quote` unifiée le 2026-09-22).
    """
    data = json.loads(HARVEST.read_text(encoding="utf-8"))
    for w in data["works"]:
        if w["openalex_id"] == row["openalex_id"]:
            return w.get("source_url") or "", w.get("checked") or ""
    raise SystemExit(f"openalex_id {row['openalex_id']!r} absent de harvest.json")


def already_fichees() -> set[str]:
    out = set()
    for path in FICHES.glob("*.json"):
        try:
            fiche = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        pdf = (fiche.get("source") or {}).get("pdf")
        if pdf:
            out.add(Path(pdf).stem)
    return out


def do_list() -> int:
    done = already_fichees()
    rows = census()
    todo = [fiche_id_for(r) for r in rows if fiche_id_for(r) not in done]
    print(f"population (moissonnee, promue D18) : {len(rows)}")
    print(f"fichees      : {len(done)}")
    print(f"a ficher     : {len(todo)}")
    for fid in todo:
        print(f"  - {fid}")
    print("\nCette population N'ENTRE PAS dans G1-G4 de la porte 07 (D20, F47).")
    print("Elle alimente le lot de la phase 09 (D25).")
    return 0


def do_prepare(fiche_id: str) -> int:
    from datetime import date

    row = entry_of(fiche_id)
    text_path = REPO / "corpus" / "text" / f"{fiche_id}.{MODE}.txt"
    if not text_path.is_file():
        raise SystemExit(f"texte absent : {text_path} — `python corpus/extract_text.py`")

    url, checked = source_url_and_checked(row)
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{fiche_id}.md"
    out.write_text(
        CONSIGNE.format(
            schema=SCHEMA.read_text(encoding="utf-8"),
            fiche_id=fiche_id,
            pdf=row["pdf"],
            url=url,
            retrieved=checked,
            today=date.today().isoformat(),
            text=text_path.read_text(encoding="utf-8", errors="replace"),
        ),
        encoding="utf-8",
    )
    print(f"consigne ecrite : {out.relative_to(REPO)}  ({out.stat().st_size / 1000:.0f} ko)")
    print(f"fiche attendue  : corpus/fiches_harvest/{fiche_id}.json")
    print("\nELLE NE DOIT PAS ETRE DONNEE A UNE SESSION QUI A LU corpus/fiches_harvest/ (D16).")
    return 0


def empreinte(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enregistrer_production(path: Path) -> dict:
    registre = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    nom = path.stem
    ligne = registre.get(nom) or {"attempts": []}
    ligne.setdefault("attempts", []).append(
        {
            "produced": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            "sha256": empreinte(path),
        }
    )
    ligne["sha256"] = ligne["attempts"][-1]["sha256"]
    ligne["produced"] = ligne["attempts"][-1]["produced"]
    registre[nom] = ligne
    PRODUCED.write_text(
        json.dumps(dict(sorted(registre.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return registre[nom]


def do_record(path: Path) -> int:
    if not path.is_file():
        raise SystemExit(f"fiche introuvable : {path}")
    ligne = enregistrer_production(path)
    n = len(ligne["attempts"])
    print(f"inscrite : {path.stem}  (essai {n})")
    print(f"  sha256   {ligne['sha256'][:16]}…")
    print(f"  produite {ligne['produced']}")
    if n > 1:
        print(f"  L'EXTRACTEUR A REPASSÉ {n} FOIS sur cette fiche.")
    print("\nTOUTE MODIFICATION À LA MAIN DE CE FICHIER CASSERAIT une future porte")
    print("qui s'appuierait sur ce registre — même discipline que G3 (D17).")
    return 0


def do_judge(path: Path) -> int:
    if not path.is_file():
        raise SystemExit(f"fiche introuvable : {path}")
    r = subprocess.run(
        [sys.executable, str(REPO / "corpus" / "score_extraction.py"), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(r.stdout or r.stderr)

    if PRODUCED.is_file():
        registre = json.loads(PRODUCED.read_text(encoding="utf-8"))
        ligne = registre.get(path.stem)
        if ligne and ligne["sha256"] != empreinte(path):
            print(f"\n  RETOUCHE DÉTECTÉE — {path.stem} a été MODIFIÉE depuis sa production "
                  f"du {ligne['produced']}.")
            return 1
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare", metavar="FICHE_ID")
    ap.add_argument("--judge", type=Path, metavar="FICHE")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--record", type=Path, metavar="FICHE")
    args = ap.parse_args()

    if args.list:
        return do_list()
    if args.prepare is not None:
        return do_prepare(args.prepare)
    if args.record is not None:
        return do_record(args.record)
    if args.judge is not None:
        return do_judge(args.judge)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
