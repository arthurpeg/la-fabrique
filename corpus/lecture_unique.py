"""Une seule lecture du papier pour la fiche ET la recette — `D55`.

Avant `D55`, un papier moissonné était lu en entier deux fois, par deux
sessions Opus :
- l'extracteur, qui écrit la fiche (`D14`, `D16`, environ 170 000 tokens) ;
- puis la recette, qui relit tout pour la formule, le timing et les
  paramètres (`D34`, environ 165 000 tokens).

`fabrique-lecteur` lit le texte une fois et écrit les deux fichiers, dans cet
ordre. Chacun garde son propre validateur, inchangé :
- la fiche : `extract_fiche_harvest.py --record` puis `--judge` ;
- la recette : `recette.py --record` puis `--check`.

Les citations de l'une et de l'autre se cherchent dans le même texte (`D18`).

Cette consigne assemble les deux consignes existantes, sans en changer une règle.
Le texte du papier n'y figure qu'une fois.

    python corpus/lecture_unique.py --prepare <fiche_id>
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "corpus"))
sys.path.insert(0, str(REPO / "scripts"))

WORK = REPO / "corpus" / "consignes-lecture"
REPERE = "@@TEXTE@@"

ENTETE = """\
# Consigne de lecture unique — La Fabrique, `D55`

Tu lis **une seule fois** le texte d'un papier académique, en fin de consigne,
et tu écris **deux fichiers, dans cet ordre** :

1. **la fiche** du papier, selon la PARTIE 1 ;
2. **sa recette**, selon la PARTIE 2. La recette complète la fiche que tu viens
   d'écrire.

Chaque fichier a ses propres règles et son propre contrôle automatique. Les
deux exigent la même chose : chaque citation recopiée **à la lettre** du texte,
et `null` avec sa raison pour tout ce que le papier ne dit pas. **N'invente
jamais une valeur.**

Écris la fiche d'abord, en entier, avec l'outil Write. Écris ensuite la recette.
Réponds en une ligne : les deux chemins écrits, le nombre de résultats cités
dans la fiche et le nombre d'ambiguïtés relevées dans la recette.
"""


def section_sans(texte: str, titre: str) -> str:
    """La consigne jusqu'à la section `titre` exclue : le texte n'y est pas répété."""
    i = texte.find(titre)
    if i < 0:
        raise SystemExit(f"section « {titre} » introuvable : une consigne source a changé")
    return texte[:i].rstrip().rstrip("-").rstrip()


def do_prepare(fiche_id: str) -> int:
    import extract_fiche_harvest as ext  # noqa: PLC0415
    import recette as rec  # noqa: PLC0415

    if (ext.FICHES / f"{fiche_id}.json").is_file():
        raise SystemExit(f"{fiche_id} a déjà sa fiche : pour sa recette seule, "
                         f"`python scripts/recette.py --prepare {fiche_id}`")
    row = ext.entry_of(fiche_id)
    texte = REPO / "corpus" / "text" / f"{fiche_id}.{ext.MODE}.txt"
    if not texte.is_file():
        raise SystemExit(f"texte absent : {texte} — `python corpus/extract_text.py`")
    url, checked = ext.source_url_and_checked(row)
    partie1 = section_sans(ext.CONSIGNE.format(
        schema=ext.SCHEMA.read_text(encoding="utf-8"), fiche_id=fiche_id, pdf=row["pdf"],
        url=url, retrieved=checked, today=date.today().isoformat(), text=REPERE),
        "## TEXTE DU PAPIER")
    partie1 = partie1.replace(
        "Un **seul objet JSON**, rien avant, rien après.",
        f"Un **seul objet JSON**, rien avant, rien après, écrit à "
        f"`corpus/fiches_harvest/{fiche_id}.json`.")
    partie2 = section_sans(rec.CONSIGNE.format(
        chemin=rec.recette_path(fiche_id).relative_to(REPO).as_posix(), fiche_id=fiche_id,
        repairs=", ".join(f"`{r}`" for r in sorted(rec.REPAIRS)), precisions="",
        instruments=chr(10).join(f"    - `{r}` : {d}" for r, d in rec.INSTRUMENTS.items()),
        fiche=REPERE, text=REPERE), "## LA FICHE")
    corps = (ENTETE + "\n---\n\n# PARTIE 1 — LA FICHE\n\n" + partie1
             + "\n\n---\n\n# PARTIE 2 — LA RECETTE\n\n"
             + "La fiche que tu complètes est celle que tu viens d'écrire en PARTIE 1.\n\n"
             + partie2 + "\n\n---\n\n## LE TEXTE DU PAPIER (pour les deux parties)\n\n"
             + texte.read_text(encoding="utf-8", errors="replace"))
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{fiche_id}.md"
    out.write_text(corps, encoding="utf-8")
    ko = out.stat().st_size / 1000
    print(f"consigne écrite : {out.relative_to(REPO).as_posix()}  ({ko:.0f} ko)")
    print(f"fiche attendue  : corpus/fiches_harvest/{fiche_id}.json")
    print(f"recette attendue: {rec.recette_path(fiche_id).relative_to(REPO).as_posix()}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Une seule lecture : fiche et recette — D55")
    ap.add_argument("--prepare", metavar="FICHE_ID", required=True)
    return do_prepare(ap.parse_args(argv).prepare)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
