"""Enregistre les PDF atteignables dans `corpus/pdf/`.

Geste **distinct du recensement**, et postérieur à lui : `probe_acquisition.py`
constate qu'un texte est obtenable, celui-ci l'écrit sur le disque. Le second
n'a aucune autorité sur le premier — il ne lit que `corpus/acquisition.json` et
ne télécharge que ce qui y est déjà inscrit `atteignable` en PDF.

**Les noms de fichiers sont déclarés, pas devinés.** Un nom fabriqué par
expression régulière depuis une citation se casse en silence sur la première
citation mal formée, et produit un fichier qu'aucune fiche ne retrouvera. La
table `NAMES` est explicite ; une entrée atteignable absente de la table est une
erreur bruyante, pas un nom approximatif.

**Ce que ce script ne fait PAS, et c'est la leçon du 2026-09-21** : il n'inscrit
nulle part que les fichiers « sont sur le disque ». `corpus/pdf/` est dans
`.gitignore` — son état est vrai d'un poste et d'une heure, jamais du dépôt. Le
seul énoncé qui ne se périme pas est celui du juge : `F4` de
`corpus/score_extraction.py`, lancé à l'instant où on en a besoin.

    python corpus/fetch_pdfs.py --dry-run   # dit ce qu'il ferait
    python corpus/fetch_pdfs.py             # telecharge ce qui manque
    python corpus/fetch_pdfs.py --verify    # ne telecharge rien, verifie l'existant

Code de sortie 1 si un telechargement echoue, ou si un fichier ecrit n'est pas
un PDF.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CENSUS = REPO / "corpus" / "acquisition.json"
PDFDIR = REPO / "corpus" / "pdf"

sys.path.insert(0, str(REPO / "corpus"))
from probe_acquisition import MIN_PDF_BYTES, UA  # noqa: E402

# Le nom de fichier par entree. Les trois premiers existaient deja et gardent
# le nom que leur fiche designe — le changer casserait `F4` sur ces fiches.
NAMES: dict[int, str] = {
    # L'entree 1 est INATTEIGNABLE depuis le 2026-09-22 (`L20`), donc absente de
    # `targets()`. Le nom reste ici parce qu'il est JUSTE : c'est l'URL qui etait
    # fausse, pas lui. Ne PAS retelecharger sous ce nom sans avoir verifie la
    # premiere page du PDF — c'est exactement la faute qui a ete reparee.
    1: "gao-2018-market-intraday-momentum.pdf",
    2: "baltussen-2021-hedging-demand-intraday-momentum.pdf",
    3: "heston-2010-1005.3535.pdf",
    4: "zarattini-2024-beat-the-market-spy.pdf",
    5: "zarattini-2024-profitable-day-trading-us-equity.pdf",
    7: "mesfin-2026-2605.04004.pdf",
    8: "boyarchenko-2023-overnight-drift.pdf",
    10: "lou-2019-tug-of-war.pdf",
    11: "andersen-bollerslev-1997-periodicity.pdf",
    12: "bollerslev-2018-risk-everywhere.pdf",
    13: "patton-sheppard-2015-good-volatility-bad-volatility.pdf",
    14: "corsi-2009-har-realized-volatility.pdf",
    15: "lucca-moench-2015-pre-fomc-drift.pdf",
    16: "kurov-2021-disappearing-pre-fomc-drift.pdf",
    17: "andersen-2003-micro-effects-macro-announcements.pdf",
    18: "koijen-2018-carry.pdf",
    19: "gorton-2013-fundamentals-commodity-futures.pdf",
    20: "moskowitz-2012-time-series-momentum.pdf",
}

# Ce qu'il faut savoir sur un fichier pour ne pas se tromper de papier plus tard.
NOTES: dict[int, str] = {
    5: ("L'entree 5 cite DEUX papiers (Zarattini & Aziz 2023, ORB 5 min sur QQQ ; "
        "Zarattini, Barbon & Aziz 2024). Le lien d'AMORCE designe le SECOND "
        "(SSRN 4729284), et c'est lui qui est enregistre."),
    8: "Version de travail (NY Fed Staff Report 917), non la version RFS.",
    15: "Version de travail (NY Fed Staff Report 512), non la version JF.",
    16: ("Version de travail. ATTENTION : auteurs Kurov, Wolfe & Gilbert — "
         "AMORCE.md cite une autre liste d'auteurs, voir le champ `alerte` du "
         "recensement."),
    18: "Version de travail (NBER WP 19325), non la version JFE.",
    19: "Version de travail (NBER WP 13249), non la version Review of Finance.",
}


def targets() -> list[dict]:
    """Les entrees a enregistrer, tirees du recensement et de lui seul."""
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    out = []
    for r in census:
        if r["status"] != "atteignable" or r["text_format"] != "pdf":
            continue
        n = r["entry"]
        if n not in NAMES:
            raise SystemExit(f"entree {n} atteignable mais absente de NAMES — nom a declarer")
        out.append({"entry": n, "url": r["source_url"], "name": NAMES[n],
                    "expected": r["evidence"].get("bytes", 0)})
    return out


def verify(path: Path) -> str | None:
    """None si le fichier est un PDF plausible, sinon ce qui cloche."""
    if not path.is_file():
        return "absent"
    size = path.stat().st_size
    if size < MIN_PDF_BYTES:
        return f"trop petit ({size} octets)"
    with path.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            return "n'est pas un PDF"
    return None


def download(url: str, dest: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(body)
    tmp.replace(dest)
    return len(body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    PDFDIR.mkdir(parents=True, exist_ok=True)
    rows = targets()
    failed, fetched, present = [], 0, 0

    for t in rows:
        dest = PDFDIR / t["name"]
        problem = verify(dest)

        if problem is None:
            present += 1
            print(f"{t['entry']:>2} | deja la   | {dest.stat().st_size:>8} o | {t['name']}")
            continue
        if args.verify:
            failed.append((t["entry"], problem))
            print(f"{t['entry']:>2} | MANQUE    | {problem:<22} | {t['name']}")
            continue
        if args.dry_run:
            print(f"{t['entry']:>2} | a prendre | ~{t['expected']:>7} o | {t['name']}")
            continue

        try:
            size = download(t["url"], dest)
        except Exception as e:
            failed.append((t["entry"], f"{type(e).__name__}: {e}"))
            print(f"{t['entry']:>2} | ECHEC     | {type(e).__name__}       | {t['name']}")
            continue

        problem = verify(dest)
        if problem:
            dest.unlink(missing_ok=True)
            failed.append((t["entry"], problem))
            print(f"{t['entry']:>2} | REFUSE    | {problem:<22} | {t['name']}")
            continue
        fetched += 1
        print(f"{t['entry']:>2} | pris      | {size:>8} o | {t['name']}")

    print(f"\n{present} deja la, {fetched} pris, {len(failed)} en echec, "
          f"{len(rows)} attendus")
    for n, why in failed:
        print(f"  entree {n:>2} : {why}")
    if NOTES and not args.dry_run:
        print("\nCe qu'il faut savoir sur certains fichiers :")
        for n in sorted(NOTES):
            print(f"  entree {n:>2} — {NOTES[n]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
