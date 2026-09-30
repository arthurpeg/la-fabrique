"""Le tableau de bord — il RASSEMBLE ce que la chaîne a écrit, et ne calcule rien.

Deux mosaïques, pour l'opérateur :

1. **les hypothèses**, dans l'ordre où elles ont été écrites : chacune avec son
   papier, les passages du papier qu'elle cite (fiche et recette, mot pour mot),
   les morceaux de la base de recherche qui contiennent ces passages (avec
   `--base`), le pourquoi, les actifs et les fenêtres horaires, la
   construction, les choix du codeur, le double codage, et qui s'en sert ;
2. **les IC**, tels que le registre les porte, avec le rapport entier quand la
   mesure l'a gardé (`scripts/out/rapports/`), et le code du signal **tel qu'il
   était au moment de la mesure** (git).

**AUCUN IC N'EST CALCULÉ ICI.** Tout chiffre affiché est recopié d'une ligne du
registre ou d'un rapport officiel, avec son `test_id` (invariant III). Le script
ne lit jamais la tranche `holdout`.

    python scripts/tableau_de_bord.py                 # écrit la page
    python scripts/tableau_de_bord.py --base          # + les morceaux de la base
    python scripts/tableau_de_bord.py --sortie X.html
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from codage_verifie import (  # noqa: E402
    CONCORDANCE,
    JUGEMENTS,
    RECETTES,
    choix,
    lire,
    univers_de,
)

HYP = REPO / "hypotheses"
LOT = HYP / "LOT-09.json"
REGISTRE = REPO / "registry" / "tests.jsonl"
RAPPORTS = REPO / "scripts" / "out" / "rapports"
TEMPLATE = REPO / "scripts" / "tableau_de_bord.html"
SORTIE = REPO / "scripts" / "out" / "tableau_de_bord.html"
FICHES = [REPO / "corpus" / "fiches", REPO / "corpus" / "fiches_harvest"]


def propre(x):
    """NaN et infinis -> None : JSON.parse les refuse."""
    if isinstance(x, float):
        return x if math.isfinite(x) else None
    if isinstance(x, dict):
        return {k: propre(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [propre(v) for v in x]
    return x


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def lire_json(p: Path, defaut=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else defaut


def fiche_de(fiche_id: str | None) -> tuple[dict | None, str | None]:
    if not fiche_id:
        return None, None
    for d in FICHES:
        p = d / f"{fiche_id}.json"
        if p.is_file():
            return lire_json(p), p.relative_to(REPO).as_posix()
    return None, None


def texte(v) -> str:
    if isinstance(v, dict):
        return str(v.get("value") or v.get("reason") or "")
    if isinstance(v, list):
        return " ; ".join(texte(x) for x in v)
    return "" if v is None else str(v)


# ---------------------------------------------------------------------------
# Les signaux : quel module porte quel SIGNAL_ID, et son code à une date
# ---------------------------------------------------------------------------

def modules() -> dict[str, Path]:
    out = {}
    for p in sorted((REPO / "signals").glob("*.py")):
        m = re.search(r'^SIGNAL_ID\s*=\s*["\']([^"\']+)', p.read_text(encoding="utf-8"), re.M)
        if m:
            out[m.group(1)] = p
    return out


def module_de(signal_id: str, mods: dict[str, Path]) -> Path | None:
    """Le module qui déclare ce SIGNAL_ID, ou dont il est une variante (Heston)."""
    if signal_id in mods:
        return mods[signal_id]
    prefixes = [s for s in mods if signal_id.startswith(s + "-")]
    return mods[max(prefixes, key=len)] if prefixes else None


def code_a_la_date(path: Path, instant: str | None) -> tuple[str, str]:
    """Le fichier tel qu'il était à `instant` (git), sinon tel qu'il est."""
    rel = path.relative_to(REPO).as_posix()
    if instant:
        sha = git("log", "-1", f"--before={instant}", "--format=%H", "--", rel).strip()
        if sha:
            src = git("show", f"{sha}:{rel}")
            if src:
                return src, f"version du commit {sha[:8]}, la dernière avant la mesure"
    return path.read_text(encoding="utf-8"), "version actuelle du dépôt"


# ---------------------------------------------------------------------------
# La base de recherche : quels morceaux contiennent une citation
# ---------------------------------------------------------------------------

class Base:
    def __init__(self, active: bool):
        self.db = None
        self.erreur = None
        if not active:
            return
        try:
            sys.path.insert(0, str(REPO / "vectordb"))
            from vector_db import VectorDB  # noqa: PLC0415

            self.db = VectorDB.from_env()
            self.db.__enter__()
        except Exception as e:  # noqa: BLE001 — la page se fait sans la base
            self.erreur = f"{type(e).__name__}: {str(e)[:120]}"
            self.db = None

    def morceaux(self, titre: str, citations: list[str]) -> list[dict]:
        if not self.db or not citations:
            return []
        out = []
        with self.db.conn.cursor() as c:
            for q in citations:
                frag = " ".join(q.split())[:70]
                if len(frag) < 20:
                    continue
                c.execute("""
                    select p.title, p.text_source, ch.ordinal, ch.section, ch.content
                    from chunks ch join papers p on p.id = ch.paper_id
                    where p.title_norm = trim(lower(regexp_replace(%s, '[^a-zA-Z0-9]+', ' ', 'g')))
                      and ch.content ilike %s
                    order by ch.ordinal limit 2
                """, (titre, f"%{frag}%"))
                for r in c.fetchall():
                    out.append({"quote": q[:160], "ordinal": r["ordinal"],
                                "section": r["section"], "source": r["text_source"],
                                "content": r["content"][:1200]})
        return out


# ---------------------------------------------------------------------------
# Les hypothèses
# ---------------------------------------------------------------------------

def entete(md: str, cle: str) -> str | None:
    m = re.search(rf"^\*\*{cle}\s*:\*\*\s*(.+)$", md, re.M)
    return m.group(1).strip() if m else None


def citations_de(fiche: dict | None, recette: dict | None) -> list[dict]:
    out = []
    for r in (fiche or {}).get("reported_results") or []:
        if r.get("quoted"):
            out.append({"from": "fiche · résultat", "name": r.get("name"),
                        "value": r.get("value"), "unit": r.get("unit"), "quoted": r["quoted"]})
    rec = recette or {}
    for cle in ("formula", "timing"):
        b = rec.get(cle) or {}
        if b.get("quoted"):
            out.append({"from": f"recette · {cle}", "name": b.get("statement"),
                        "value": None, "unit": None, "quoted": b["quoted"]})
    for p in rec.get("parameters") or []:
        if p.get("quoted"):
            out.append({"from": "recette · paramètre", "name": p.get("name"),
                        "value": p.get("value"), "unit": p.get("unit"), "quoted": p["quoted"]})
    return out


def hypotheses(registre: list[dict], lot: dict, mods: dict, base: Base) -> list[dict]:
    lot_par_ref = {e["ref"]: e for e in lot.get("fiches", []) if e.get("ref")}
    concord = {}
    for c in lire(CONCORDANCE):
        concord[c["fiche_id"]] = c
    out = []
    fichiers = sorted(HYP.glob("H*.md"), key=lambda p: int(re.match(r"H(\d+)", p.name).group(1)))
    for p in fichiers:
        md = p.read_text(encoding="utf-8")
        ref = re.match(r"(H\d+)", p.name).group(1)
        titre = md.splitlines()[0].lstrip("# ").split("—", 1)[-1].strip()
        entree = lot_par_ref.get(ref)
        lignes = [r for r in registre if r.get("hypothesis_ref") == ref]
        signaux = sorted({r["signal_id"] for r in lignes})
        m_sig = re.search(r"`([a-z0-9-]+)`", entete(md, "Signal") or "")
        if m_sig and m_sig.group(1) not in signaux:
            signaux.insert(0, m_sig.group(1))
        if entree and entree.get("signal_id") and entree["signal_id"] not in signaux:
            signaux.insert(0, entree["signal_id"])
        fiche_id = (entree or {}).get("fiche_id")
        if not fiche_id:
            m_f = re.search(r"corpus/fiches(?:_harvest)?/([a-z0-9-]+[A-Za-z0-9-]*)\.json", md)
            fiche_id = m_f.group(1) if m_f else None
        if not fiche_id:
            # Les hypothèses d'avant le lot nomment leur papier par son entrée
            # d'AMORCE.md ; la fiche porte le même numéro (`source.amorce_entry`).
            m_e = re.search(r"AMORCE\.md`?,?\s*entrée\s*(\d+)", md)
            if m_e:
                for f in sorted((REPO / "corpus" / "fiches").glob("*.json")):
                    entree_f = (lire_json(f) or {}).get("source", {}).get("amorce_entry")
                    if entree_f == int(m_e.group(1)):
                        fiche_id = f.stem
                        break
        fiche, fiche_path = fiche_de(fiche_id)
        recette = lire_json(RECETTES / f"{fiche_id}.json") if fiche_id else None
        mod = module_de(signaux[0], mods) if signaux else None
        src = mod.read_text(encoding="utf-8") if mod else None
        concordance = concord.get(fiche_id) if fiche_id else None
        cites = citations_de(fiche, recette)
        source = (fiche or {}).get("source") or {}
        out.append({
            "ref": ref, "title": titre, "file": p.relative_to(REPO).as_posix(),
            "written": (entete(md, "Écrite le") or "").split(",")[0],
            "status": entete(md, "Statut"),
            "origin": entete(md, "Origine"),
            "markdown": md,
            "signals": signaux,
            "module": mod.relative_to(REPO).as_posix() if mod else None,
            "code": src,
            "expected_sign": (re.search(r"^EXPECTED_SIGN\s*=\s*([+-]?\d)", src or "", re.M)
                              or [None, None])[1],
            "choices": choix(src) if src else [],
            "fiche_id": fiche_id, "fiche_file": fiche_path,
            "paper": {"title": source.get("title"), "authors": source.get("authors"),
                      "year": source.get("year"), "url": source.get("source_url"),
                      "venue": source.get("venue") or source.get("journal")},
            "claim": texte((fiche or {}).get("claim")),
            "universe": texte((fiche or {}).get("universe")),
            "horizon": texte((fiche or {}).get("horizon")),
            "construction": texte((fiche or {}).get("signal_construction")),
            "transfers": texte(((fiche or {}).get("transposability") or {}).get("what_transfers")),
            "does_not_transfer": texte(((fiche or {}).get("transposability") or {})
                                       .get("what_does_not_transfer")),
            "missing": texte((fiche or {}).get("what_is_missing")),
            "recipe": recette,
            "quotes": cites,
            "chunks": base.morceaux(source.get("title") or "", [c["quoted"] for c in cites]),
            "measured_universe": (entree or {}).get("universe") or univers_de(recette or {}),
            "concordance": ({k: concordance.get(k) for k in
                             ("verdict", "rho", "coverage", "round", "at")}
                            if concordance else None),
            "used_by": {"lot": "LOT-09 (D36)" if entree else None,
                        "tests": [r["test_id"] for r in lignes]},
        })
    return out


# ---------------------------------------------------------------------------
# Les IC
# ---------------------------------------------------------------------------

def ics(registre: list[dict], mods: dict, hash_courant: str) -> tuple[list[dict], dict]:
    codes: dict[str, dict] = {}
    out = []
    for r in registre:
        if r.get("hypothesis_ref") is None:
            continue
        mod = module_de(r["signal_id"], mods)
        cle = None
        if mod:
            src, quand = code_a_la_date(mod, r.get("timestamp"))
            cle = f"{mod.name}@{hash(src) & 0xFFFFFFFF:08x}"
            codes.setdefault(cle, {"path": mod.relative_to(REPO).as_posix(),
                                   "when": quand, "source": src})
        rapport = lire_json(RAPPORTS / f"{r['test_id']}.json")
        out.append({**{k: r.get(k) for k in (
            "test_id", "timestamp", "signal_id", "hypothesis_ref", "stage", "data_slice",
            "horizon", "asof", "ic", "t_stat", "observations", "cells", "code_hash",
            "ic_by_year")},
            "stale": r.get("code_hash") != hash_courant,
            "code_key": cle, "report": rapport})
    return out, codes


def ecartes(lot: dict, liste_ic: list[dict], hc: str) -> list[dict]:
    """Ce qui ne sera pas mesuré, ou plus lu : chaque entrée avec sa raison écrite."""
    out = []
    for e in lot.get("ecartees") or []:
        out.append({"kind": "écarté à la constitution du lot", "id": e.get("fiche_id"),
                    "why": e.get("motif"), "detail": {"verdict du tri": e.get("verdict"),
                                                      "décision": lot.get("decision")}})
    for e in lot.get("ecartees_codage") or []:
        out.append({"kind": f"écarté avant mesure ({e.get('preuve')})", "id": e.get("fiche_id"),
                    "why": e.get("motif_ecart"), "detail": {"le": e.get("at"),
                                                            "preuve": e.get("preuve")}})
    ecartees = {e.get("fiche_id") for e in lot.get("ecartees_codage") or []}
    for e in lot.get("fiches") or []:
        r = lire_json(RECETTES / f"{e['fiche_id']}.json")
        u = univers_de(r or {})
        if u is not None and not u["exact"] and e["fiche_id"] not in ecartees:
            out.append({"kind": "à écarter : marché absent de notre univers", "id": e["fiche_id"],
                        "why": f"Le papier étudie « {u['studied']} » ; aucun de nos neuf "
                               "instruments n'est ce marché (D38).",
                        "detail": {"prochaine étape": "ecarter_du_lot.py --preuve univers"}})
    perimes: dict[tuple, list] = {}
    for r in liste_ic:
        if r["stale"]:
            perimes.setdefault((r["hypothesis_ref"], r["code_hash"]), []).append(r["test_id"])
    for (ref, h), tests in perimes.items():
        out.append({"kind": "IC périmé", "id": f"{ref} · {len(tests)} mesure(s)",
                    "why": f"Mesuré(s) sous le harnais {h} ; le harnais courant est {hc}. Toute "
                           "modification du harnais périme les résultats antérieurs (D05) : ils "
                           "restent au registre et au décompte, mais rien ne s'appuie plus dessus.",
                    "detail": {"tests": ", ".join(tests[:6]) + (" …" if len(tests) > 6 else "")}})
    for r in liste_ic:
        rep_ = r.get("report") or {}
        for v in rep_.get("refused_cells") or []:
            cell = v.get("cell") if isinstance(v, dict) else None
            out.append({"kind": "données insuffisantes", "id": f"{r['test_id']} · {cell}",
                        "why": (v.get("reason") if isinstance(v, dict) else str(v)),
                        "detail": {"signal": r["signal_id"]}})
    return out


def entonnoir(lot: dict, reg: list[dict]) -> list[dict]:
    """Combien de papiers à chaque étape, de la moisson au test. Des comptes, pas des IC."""
    from statut_papiers import bilan  # noqa: PLC0415

    rows = bilan()
    works = [r for r in rows if r["origin"] == "moisson"]
    tri = lire_json(REPO / "corpus" / "triage_harvest_verdicts.json", [])
    fiches = sum(len(list(d.glob("*.json"))) for d in FICHES)
    entrees = lot.get("fiches", [])
    ids = {e["fiche_id"] for e in entrees}
    concord = {c["fiche_id"]: c["verdict"] for c in lire(CONCORDANCE)}
    mesures = {r["signal_id"] for r in reg if r.get("stage") == "09-passage"}
    etapes = [
        ("papiers moissonnés", len(works), "corpus/harvest.json, doublons compris"),
        ("atteignables, non doublons", sum(1 for r in works if r["stage"] not in
                                           ("doublon", "inatteignable", "non sondé")),
         "une source libre a été trouvée"),
        ("PDF sur ce poste", sum(1 for r in works if r["stage"] not in
                                 ("doublon", "inatteignable", "non sondé", "à télécharger")), ""),
        ("triés", len(tri), "corpus/triage_harvest_verdicts.json"),
        ("retenus par le tri", sum(1 for v in tri if v["verdict"] in ("oui", "partiel")),
         "oui + partiel"),
        ("fiches (AMORCE + moisson)", fiches, "corpus/fiches, corpus/fiches_harvest"),
        ("dans le lot 09", len(entrees), "hypotheses/LOT-09.json"),
        ("recette valide", sum(1 for i in ids if (RECETTES / f"{i}.json").is_file()), "D34"),
        ("signal codé", sum(1 for i in ids
                            if (REPO / "signals" / (i.replace("-", "_") + ".py")).is_file()), ""),
        ("codage vérifié", sum(1 for i in ids if concord.get(i) == "CONCORDANT"),
         "double codage concordant, D34"),
        ("hypothèse écrite", sum(1 for e in entrees if e.get("ref")), "étape 8"),
        ("mesurée", sum(1 for e in entrees if e.get("signal_id") in mesures), "étape 10"),
    ]
    return [{"label": a, "n": n, "note": c, "warn": False} for a, n, c in etapes]


def compteur(reg: list[dict], lot: dict, hc: str, counted: int) -> dict:
    from statistics import NormalDist  # noqa: PLC0415

    par: dict[str, dict] = {}
    for r in reg:
        d = par.setdefault(r.get("stage") or "?", {"counted": 0, "calibrations": 0, "stale": 0})
        if r.get("hypothesis_ref") is None:
            d["calibrations"] += 1
        else:
            d["counted"] += 1
        if r.get("code_hash") != hc:
            d["stale"] += 1
    n, q = lot.get("n") or 0, lot.get("q") or 0.10
    bh = {}
    if n:
        z = NormalDist()
        bh = {"n": n, "q": q, "p_first": f"{q / n:.4f}", "t_first": f"{z.inv_cdf(1 - q / n):.2f}",
              "t_last": f"{z.inv_cdf(1 - q):.2f}"}
    return {"counted": counted,
            "calibrations": sum(1 for r in reg if r.get("hypothesis_ref") is None),
            "stale": sum(1 for r in reg if r.get("code_hash") != hc),
            "by_stage": par, "bh": bh}


def fenetres() -> dict:
    import yaml  # noqa: PLC0415

    cat = yaml.safe_load((REPO / "catalogue" / "catalogue.yaml").read_text(encoding="utf-8"))
    grille = cat.get("grid") or cat
    w = grille.get("windows") or {}
    return {k: f"{v['start']}–{v['end']}" for k, v in w.items()}


def rassembler(avec_base: bool, quota: Path | None = None) -> dict:
    from harness import registry  # noqa: PLC0415

    reg = [json.loads(x) for x in REGISTRE.read_text(encoding="utf-8").splitlines() if x.strip()]
    lot = lire_json(LOT, {})
    mods = modules()
    base = Base(avec_base)
    hc = registry.code_hash()
    liste_ic, codes = ics(reg, mods, hc)
    liste_ecartes = ecartes(lot, liste_ic, hc)
    return propre({
        "generated": datetime.now(UTC).isoformat(timespec="minutes"),
        "harness": hc,
        "counted_tests": registry.counted_tests(),
        "registry_lines": len(reg),
        "windows": fenetres(),
        "clock": "America/New_York",
        "lot": {"n": lot.get("n"), "declared_at": lot.get("declared_at"),
                "decision": lot.get("decision"),
                "with_hypothesis": sum(1 for e in lot.get("fiches", []) if e.get("ref"))},
        "verified": sum(1 for c in {c["fiche_id"]: c for c in lire(CONCORDANCE)}.values()
                        if c["verdict"] == "CONCORDANT"),
        "judgements": len(lire(JUGEMENTS)),
        "base": {"asked": avec_base, "error": base.erreur},
        "hypotheses": hypotheses(reg, lot, mods, base),
        "ics": liste_ic,
        "excluded": liste_ecartes,
        "funnel": entonnoir(lot, reg),
        "counter": compteur(reg, lot, hc, registry.counted_tests()),
        "quota": lire_json(quota) if quota else None,
        "codes": codes,
    })


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le tableau de bord — rassemble, ne calcule rien")
    ap.add_argument("--base", action="store_true", help="relier les citations aux morceaux")
    ap.add_argument("--sortie", type=Path, default=SORTIE)
    ap.add_argument("--quota", type=Path, help="le relevé du quota (JSON), si on l'a")
    a = ap.parse_args(argv)
    data = rassembler(a.base, a.quota)
    page = TEMPLATE.read_text(encoding="utf-8").replace(
        "/*__DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    a.sortie.parent.mkdir(parents=True, exist_ok=True)
    a.sortie.write_text(page, encoding="utf-8")
    etat_base = ("reliée" if a.base and not data["base"]["error"]
                 else data["base"]["error"] or "non demandée")
    print(f"{len(data['hypotheses'])} hypothèse(s), {len(data['ics'])} IC, "
          f"{len(data['codes'])} version(s) de code ; base : {etat_base}")
    print(f"écrit : {a.sortie}  ({a.sortie.stat().st_size / 1e6:.2f} Mo)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
