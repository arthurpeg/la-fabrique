"""Produit le texte qui fait foi — `D18`.

`F2` exige qu'une citation se retrouve mot pour mot dans « le texte du papier ».
Ce texte n'existe pas : il y a des **extractions**, qui diffèrent. `D18` tranche
que le texte qui fait foi est l'**union de deux extractions fixées d'avance et
identiques pour tous les papiers** — `pypdf` par défaut et `pypdf` en mode
`layout` — et ce script les produit.

**Rien ici n'est réglable par papier**, et c'est le cœur de `D18`. Un mode choisi
au cas par cas serait un bouton : l'extracteur échoue sur un papier, on change
son mode, il passe. C'est « modifier le harnais pour faire passer un signal »,
transposé au corpus.

**Le texte est versionné** (`corpus/text/`) parce que `F2` doit être rejouable
sans les PDF, qui restent hors dépôt. C'est un résultat, comme les fiches.

**La version de `pypdf` est inscrite** dans `corpus/text/MANIFEST.json`, hors du
texte lui-même pour ne pas polluer ce que `F2` fouille. Une montée de version qui
changerait le texte périmerait les `quoted_source` ; `--check` le rend bruyant.

    python corpus/extract_text.py            # (re)produit ce qui manque
    python corpus/extract_text.py --force    # reproduit tout
    python corpus/extract_text.py --check    # ne produit rien, dit ce qui a bouge

Code de sortie 1 si `--check` trouve une divergence, ou si une extraction echoue.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PDFDIR = REPO / "corpus" / "pdf"
TEXTDIR = REPO / "corpus" / "text"
MANIFEST = TEXTDIR / "MANIFEST.json"

# Les deux extractions de D18. Liste CLOSE : en ajouter une est une decision
# ecrite, pas un geste. L'ordre est fixe pour que le manifeste soit stable.
MODES: dict[str, dict] = {
    "default": {},
    "layout": {"extraction_mode": "layout"},
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def extract(pdf: Path, mode: str) -> str:
    """Une extraction, deterministe, sans repli silencieux.

    `pypdf` avertit sur le texte pivote ; l'avertissement est tu ICI et
    seulement ici, parce qu'il se repete des centaines de fois et noie la sortie.
    Ce qu'il signale est inscrit dans le manifeste : `rotated_text_warning`.
    """
    from pypdf import PdfReader

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        reader = PdfReader(str(pdf))
        pages = [(page.extract_text(**MODES[mode]) or "") for page in reader.pages]
        rotated = any("rotated" in str(w.message).lower() for w in caught)
    return "\n".join(pages), len(reader.pages), rotated


def targets() -> list[Path]:
    return sorted(PDFDIR.glob("*.pdf"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    import pypdf

    TEXTDIR.mkdir(parents=True, exist_ok=True)
    old = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else {}
    old_files = {e["path"]: e for e in old.get("files", [])}

    pdfs = targets()
    if not pdfs:
        print(f"aucun PDF dans {PDFDIR.relative_to(REPO)} — rien a extraire")
        print("les recuperer avec : python corpus/fetch_pdfs.py")
        return 1

    entries, changed, written = [], [], 0
    for pdf in pdfs:
        for mode in MODES:
            rel = f"corpus/text/{pdf.stem}.{mode}.txt"
            dest = REPO / rel
            try:
                text, pages, rotated = extract(pdf, mode)
            except Exception as e:
                print(f"ECHEC {pdf.name} [{mode}] : {type(e).__name__}: {e}")
                return 1

            h = digest(text)
            entries.append({"path": rel, "pdf": f"corpus/pdf/{pdf.name}", "mode": mode,
                            "pages": pages, "chars": len(text), "sha256_16": h,
                            "rotated_text_warning": rotated})

            was = old_files.get(rel, {}).get("sha256_16")
            if was and was != h:
                changed.append((rel, was, h))

            if args.check:
                continue
            if dest.is_file() and not args.force and was == h:
                continue
            dest.write_text(text, encoding="utf-8")
            written += 1

    manifest = {"decision": "D18", "pypdf": pypdf.__version__,
                "modes": sorted(MODES), "files": entries}

    if args.check:
        missing = [e["path"] for e in entries if not (REPO / e["path"]).is_file()]
        if changed:
            print("LE TEXTE A CHANGE — les `quoted_source` reposent dessus (D18) :")
            for rel, was, now in changed:
                print(f"  {rel}  {was} -> {now}")
        if missing:
            print(f"{len(missing)} fichier(s) texte absent(s), dont {missing[0]}")
        if old.get("pypdf") and old["pypdf"] != pypdf.__version__:
            print(f"pypdf {old['pypdf']} -> {pypdf.__version__} : montee de version")
        if not changed and not missing and old.get("pypdf") == pypdf.__version__:
            print(f"texte conforme au manifeste — {len(entries)} fichiers, "
                  f"pypdf {pypdf.__version__}")
            return 0
        return 1

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    total = sum(e["chars"] for e in entries)
    print(f"{len(pdfs)} PDF x {len(MODES)} modes = {len(entries)} fichiers, "
          f"{written} ecrit(s), {total/1e6:.2f} Mo, pypdf {pypdf.__version__}")
    if changed:
        print("ATTENTION — le texte de ces fichiers a CHANGE depuis le manifeste :")
        for rel, was, now in changed:
            print(f"  {rel}  {was} -> {now}")
        print("Les `quoted_source` ecrites contre l'ancien texte sont a reverifier (D18).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
