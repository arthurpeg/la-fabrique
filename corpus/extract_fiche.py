"""Le harnais de l'extracteur — phase 07, moitié extraction.

Il ne contient **aucune intelligence d'extraction**. Il prépare ce que
l'extracteur voit, puis juge ce qu'il rend. L'extraction elle-même est faite par
une session séparée, et c'est le cœur du protocole, pas un détail
d'implémentation.

## Qui peut être l'extracteur — `D16` § Qui peut être l'extracteur

**Une session qui a lu la fiche de référence d'un papier ne peut pas être
l'extracteur de ce papier.** Elle ne lirait pas le texte, elle recopierait la
fiche, et `F2` passerait triomphalement pour la pire des raisons. Même piège que
le trieur (`D15` § Complément, `F42`), même parade : l'extracteur est une session
séparée qui reçoit la **consigne** produite ici, et rien d'autre du corpus.

## Ce que l'extracteur voit, limitativement

1. `corpus/SCHEMA.md` — le schéma de fiche (`D14`) ;
2. **le texte du papier**, extraction `default` de `D18` ;
3. la consigne de sortie ci-dessous.

**Et rien d'autre.** Pas `AMORCE.md`, qui porte le verdict de triage. Pas
`corpus/fiches/`, qui porte les réponses. Pas les décisions, qui racontent ce que
les papiers ont donné. `corpus/SCHEMA.md` a été purgé de son contenu réel le
2026-09-21 pour cette raison (`L17`).

**Pourquoi l'extraction `default` et une seule.** `F2` cherche dans l'union des
deux (`D18`), mais donner les deux doublerait l'entrée sans rien apprendre à
l'extracteur : il cite ce qu'il lit. Le choix est **fixe pour tous les papiers** —
un texte choisi par papier serait le bouton que `D18` refuse.

    python corpus/extract_fiche.py --prepare <entree>   # ecrit la consigne
    python corpus/extract_fiche.py --judge <fiche.json> # juge une sortie
    python corpus/extract_fiche.py --list               # ce qui reste a ficher

Code de sortie 1 si l'entree est inconnue, ou si la fiche jugee ne passe pas.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CENSUS = REPO / "corpus" / "acquisition.json"
SCHEMA = REPO / "corpus" / "SCHEMA.md"
FICHES = REPO / "corpus" / "fiches"
WORK = REPO / "corpus" / "consignes"

MODE = "default"  # D18, fixe pour tous les papiers

CONSIGNE = """\
# Consigne d'extraction — phase 07 de La Fabrique

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
- `source.amorce_entry` : `{entry}`
- `written_by` : le nom de la session qui extrait
- `written` : `{today}`

---

## TEXTE DU PAPIER

{text}
"""


def census() -> list[dict]:
    if not CENSUS.is_file():
        raise SystemExit("recensement absent — `python corpus/probe_acquisition.py --write`")
    return json.loads(CENSUS.read_text(encoding="utf-8"))


def entry_of(n: int) -> dict:
    for row in census():
        if row["entry"] == n:
            return row
    raise SystemExit(f"entree {n} absente du recensement")


def fiche_id_for(row: dict) -> str:
    return Path(row["pdf"]).stem


def already_fichees() -> set[str]:
    """Les PDF deja fiches, apparies par `source.pdf` et NON par nom de fichier.

    Une fiche porte le nom de son SUJET (`mesfin-2026-ohlcv-falsification`), le
    PDF celui de sa provenance (`mesfin-2026-2605.04004`). Apparier les deux par
    le nom de fichier faisait compter trois papiers fiches comme non fiches, et
    `G1` — zero atteignable non fiche — aurait ete declare rouge a tort.
    """
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
    todo, blocked = [], []
    for row in census():
        if row["status"] != "atteignable":
            blocked.append((row["entry"], row["reason"]))
        elif row["text_format"] != "pdf":
            blocked.append((row["entry"],
                            f"texte en {row['text_format']} — D18 ne traite que les PDF"))
        elif fiche_id_for(row) not in done:
            todo.append(row["entry"])
    print(f"fichees      : {len(done)}")
    print(f"a ficher     : {len(todo)} -> {todo}")
    print(f"hors d'atteinte du fichage : {len(blocked)}")
    for n, why in blocked:
        print(f"  entree {n:>2} : {why}")
    print("\n`G1` de D17 exige ZERO papier atteignable non fiche.")
    return 0


def do_prepare(n: int) -> int:
    from datetime import date

    row = entry_of(n)
    if row["status"] != "atteignable" or row["text_format"] != "pdf":
        raise SystemExit(f"entree {n} : {row['status']}/{row['text_format']} — rien a preparer")

    stem = Path(row["pdf"]).stem
    text_path = REPO / "corpus" / "text" / f"{stem}.{MODE}.txt"
    if not text_path.is_file():
        raise SystemExit(f"texte absent : {text_path} — `python corpus/extract_text.py`")

    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"entree-{n:02d}-{stem}.md"
    out.write_text(
        CONSIGNE.format(
            schema=SCHEMA.read_text(encoding="utf-8"),
            fiche_id=stem,
            pdf=row["pdf"],
            url=row["source_url"],
            retrieved=row["checked"],
            entry=n,
            today=date.today().isoformat(),
            text=text_path.read_text(encoding="utf-8", errors="replace"),
        ),
        encoding="utf-8",
    )
    print(f"consigne ecrite : {out.relative_to(REPO)}  ({out.stat().st_size/1000:.0f} ko)")
    print(f"fiche attendue  : corpus/fiches/{stem}.json")
    print("\nELLE NE DOIT PAS ETRE DONNEE A UNE SESSION QUI A LU corpus/fiches/ (D16).")
    return 0


def do_judge(path: Path) -> int:
    if not path.is_file():
        raise SystemExit(f"fiche introuvable : {path}")
    r = subprocess.run(
        [sys.executable, str(REPO / "corpus" / "score_extraction.py"), str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    print(r.stdout or r.stderr)
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare", type=int, metavar="ENTREE")
    ap.add_argument("--judge", type=Path, metavar="FICHE")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        return do_list()
    if args.prepare is not None:
        return do_prepare(args.prepare)
    if args.judge is not None:
        return do_judge(args.judge)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
