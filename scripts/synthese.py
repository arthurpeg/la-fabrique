"""Les hypothèses de synthèse — une fiche tirée de PLUSIEURS papiers (`D39`).

Une grappe (`scripts/grappes.py`) réunit des papiers qui décrivent le même
mécanisme. Une session isolée (`fabrique-synthese`) lit leurs fiches — et rien
d'autre, **jamais un résultat de nos données** — et écrit UNE fiche de synthèse :
le mécanisme commun, ce sur quoi les papiers s'accordent et divergent, et UNE
version de l'hypothèse, choisie **avant toute mesure** selon des critères écrits
dans l'ordre (`CRITERES`). La fiche suit le schéma de `D14` ; elle entre ensuite
dans la chaîne ordinaire : recette, deux codeurs, double codage, lot.

**Le validateur est mécanique**, comme pour une fiche d'un seul papier : chaque
citation se retrouve à la lettre dans le texte d'**au moins un** papier source
(`score_extraction.check_f2`, sur l'union de leurs textes), chaque valeur dans
sa citation (`validate_fiches.check_fiche`), chaque source appartient à la
grappe, et la version retenue dit de quels papiers elle vient.

    python scripts/synthese.py --prepare G-a9d7ec
    python scripts/synthese.py --record corpus/fiches_synthese/synthese-g-a9d7ec.json
    python scripts/synthese.py --check corpus/fiches_synthese/synthese-g-a9d7ec.json
    python scripts/synthese.py --status
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "corpus"))
sys.path.insert(0, str(REPO / "catalogue"))

from codage_verifie import empreinte16, maintenant  # noqa: E402

DOSSIER = REPO / "corpus" / "fiches_synthese"
PRODUCED = REPO / "corpus" / "PRODUCED_synthese.json"
WORK = REPO / "corpus" / "consignes-synthese"
GRAPPES = REPO / "scripts" / "out" / "grappes.json"
SCHEMA = REPO / "corpus" / "SCHEMA.md"

# D39 : l'ordre dans lequel la synthèse choisit sa version. Écrit avant toute
# synthèse, appliqué dans cet ordre, jamais d'après un résultat.
CRITERES = (
    "l'accord : la construction que le plus de papiers de la grappe décrivent ou soutiennent",
    "la transposabilité : celle qui se calcule le mieux sur nos neuf futures intraday en OHLCV",
    "la parcimonie : à égalité, celle qui a le moins de paramètres",
    "la traçabilité : chaque paramètre retenu est cité dans au moins un papier",
)


def sid_de(gid: str) -> str:
    return f"synthese-{gid.lower()}"


def grappe(gid: str) -> dict:
    d = json.loads(GRAPPES.read_text(encoding="utf-8"))
    for g in d["groups"]:
        if g["id"] == gid:
            return g
    raise SystemExit(f"grappe inconnue : {gid} — `python scripts/grappes.py --status`")


def fiches_sources() -> dict[str, Path]:
    from code_signal import fiche_files  # noqa: PLC0415

    return {k: v for k, v in fiche_files().items() if not k.startswith("synthese-")}


def textes_des_sources(sources: list[str]) -> dict[str, str]:
    """L'union des extractions (D18) de chaque papier source."""
    from score_extraction import texts_of  # noqa: PLC0415

    ff = fiches_sources()
    out = {}
    for s in sources:
        for mode, t in texts_of(json.loads(ff[s].read_text(encoding="utf-8"))).items():
            out[f"{s}.{mode}"] = t
    return out


CONSIGNE = """\
# Consigne de synthèse — La Fabrique, `D39`

Tu écris **une fiche de synthèse** à partir des fiches de {n} papiers qui
décrivent, d'après leur texte, le même mécanisme (grappe `{gid}`, cosinus moyen
{cos}). Tu n'as accès qu'à ces fiches. **Tu ne connais aucun résultat obtenu sur
nos données, et tu ne dois pas en chercher** : la version que tu retiens se
choisit sur ce que disent les papiers, jamais sur ce qui « marcherait ».

## Ce que tu rends

Un **seul fichier JSON**, écrit à `{chemin}`. C'est une fiche au schéma
ci-dessous (section SCHÉMA), avec ces règles propres à une synthèse :

- `fiche_id` : `{sid}` ; `written` : `{today}` ; `written_by` : ton nom.
- `source` : `authors` = « Synthèse de : » suivi des auteurs de chaque papier ;
  `title` = « Synthèse — » suivi du mécanisme ; `year` = l'année la plus récente
  des sources ; `source_url` = celle du papier dont vient la construction
  retenue ; `retrieved` = `{today}` ; `peer_reviewed` = `false`. Pas de `pdf`.
- `claim` : l'affirmation commune, telle que les papiers la soutiennent.
- `reported_results` : des résultats **recopiés des fiches sources, citation
  comprise, à la lettre** — chacun avec un champ `from_fiche` qui nomme sa
  fiche. N'écris aucune citation qui ne figure pas déjà dans une fiche source.
- `signal_construction` : **la version retenue**, une seule.
- un bloc `synthesis` :

```json
"synthesis": {{
  "group": "{gid}",
  "sources": ["<fiche_id>", "..."],
  "mechanism": "<le mécanisme commun, en tes mots>",
  "agreements": ["<ce sur quoi les papiers s'accordent>"],
  "disagreements": ["<ce sur quoi ils divergent : fenêtre, marché, signe, horizon…>"],
  "criteria_applied": ["<chaque critère ci-dessous, et ce qu'il a tranché>"],
  "chosen_from": ["<fiche_id dont vient la construction retenue>"],
  "why": "<pourquoi cette version, en une ou deux phrases>"
}}
```

## Comment choisir la version — dans cet ordre, et rien d'autre

{criteres}

Si les papiers se contredisent sur le **signe** de l'effet, ne tranche pas par
préférence : écris-le dans `disagreements`, et retiens la version du critère 1.

## Ce que tu ne fais pas

Tu n'inventes aucun paramètre, aucune valeur, aucune citation. Tu n'additionnes
pas les idées pour fabriquer un signal plus compliqué que ceux des papiers : une
synthèse retient la version la mieux étayée, elle n'empile pas.

---

## SCHÉMA

{schema}

---

## LES FICHES DE LA GRAPPE

{fiches}
"""


def do_prepare(gid: str) -> int:
    g = grappe(gid)
    ff = fiches_sources()
    manquantes = [m for m in g["members"] if m not in ff]
    if manquantes:
        raise SystemExit(f"fiches introuvables : {manquantes}")
    sid = sid_de(gid)
    # D52 : une fiche déjà graine ou source d'une autre synthèse n'en refait pas une.
    for f in sorted(DOSSIER.glob("synthese-*.json")):
        if f.stem == sid:
            continue
        syn = json.loads(f.read_text(encoding="utf-8")).get("synthesis") or {}
        pris = set(g["members"]) & {syn.get("dossier"), *(syn.get("sources") or [])}
        if pris:
            raise SystemExit(f"{sorted(pris)} déjà dans {f.stem} : une seconde synthèse "
                             "referait la même hypothèse (D52)")
    blocs = []
    for m in g["members"]:
        blocs.append(f"### `{m}`\n\n```json\n{ff[m].read_text(encoding='utf-8')}\n```\n")
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{sid}.md"
    out.write_text(CONSIGNE.format(
        n=len(g["members"]), gid=gid, cos=g["mean_cosine"], sid=sid, today=date.today().isoformat(),
        chemin=(DOSSIER / f"{sid}.json").relative_to(REPO).as_posix(),
        criteres="\n".join(f"{i}. {c}" for i, c in enumerate(CRITERES, 1)),
        schema=SCHEMA.read_text(encoding="utf-8"), fiches="\n".join(blocs)), encoding="utf-8")
    taille = out.stat().st_size / 1000
    print(f"consigne écrite : {out.relative_to(REPO).as_posix()}  ({taille:.0f} ko)")
    print(f"fiche attendue  : {(DOSSIER / f'{sid}.json').relative_to(REPO).as_posix()}")
    return 0


def valider(path: Path) -> list[str]:
    from score_extraction import check_f2  # noqa: PLC0415
    from validate_fiches import check_fiche  # noqa: PLC0415

    fiche = json.loads(path.read_text(encoding="utf-8"))
    fautes = []
    syn = fiche.get("synthesis")
    if not isinstance(syn, dict):
        return ["bloc `synthesis` absent"]
    gid = syn.get("group")
    try:
        g = grappe(gid)
    except SystemExit as e:
        return [str(e)]
    if fiche.get("fiche_id") != sid_de(gid) or path.stem != sid_de(gid):
        fautes.append(f"fiche_id et nom de fichier doivent valoir {sid_de(gid)}")
    sources = syn.get("sources") or []
    if len(sources) < 2:
        fautes.append("une synthèse a au moins deux sources")
    hors = [s for s in sources if s not in g["members"]]
    if hors:
        fautes.append(f"sources hors de la grappe {gid} : {hors}")
    choisies = syn.get("chosen_from") or []
    if not choisies or any(c not in sources for c in choisies):
        fautes.append("`chosen_from` doit nommer au moins une source de la synthèse")
    for cle in ("mechanism", "why"):
        if not str(syn.get(cle) or "").strip():
            fautes.append(f"synthesis.{cle} vide")
    for cle in ("agreements", "disagreements", "criteria_applied"):
        if not isinstance(syn.get(cle), list) or not syn.get(cle):
            fautes.append(f"synthesis.{cle} doit être une liste non vide")
    for i, r in enumerate(fiche.get("reported_results") or []):
        if isinstance(r, dict) and r.get("from_fiche") not in sources:
            fautes.append(f"reported_results[{i}] : `from_fiche` doit nommer une source")
    fautes += check_fiche(path.stem, fiche)
    if not fautes:
        fautes += check_f2(fiche, textes_des_sources(sources))
    reg = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = reg.get(path.stem)
    if ligne is None:
        fautes.append("fiche non inscrite : `--record` avant `--check`")
    elif ligne["sha256_16"] != empreinte16(path):
        fautes.append("fiche modifiée depuis sa production — une synthèse se refait, "
                      "elle ne se retouche pas")
    return fautes


def do_record(path: Path) -> int:
    path = path.resolve()
    json.loads(path.read_text(encoding="utf-8"))
    reg = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = reg.get(path.stem) or {"attempts": []}
    ligne["attempts"].append({"produced": maintenant(), "sha256_16": empreinte16(path)})
    ligne["sha256_16"] = ligne["attempts"][-1]["sha256_16"]
    reg[path.stem] = ligne
    PRODUCED.write_text(json.dumps(dict(sorted(reg.items())), ensure_ascii=False, indent=2)
                        + "\n", encoding="utf-8")
    print(f"inscrite : {path.stem} (essai {len(ligne['attempts'])})")
    return 0


def do_check(path: Path) -> int:
    fautes = valider(path)
    if fautes:
        print(f"SYNTHÈSE REFUSÉE — {path.stem} :")
        for f in fautes:
            print(f"  - {f}")
        return 1
    print(f"SYNTHÈSE VALIDE — {path.stem} : chaque citation est dans un papier source, "
          "chaque source dans la grappe, la version retenue dit d'où elle vient")
    return 0


def do_status() -> int:
    d = json.loads(GRAPPES.read_text(encoding="utf-8")) if GRAPPES.is_file() else {"groups": []}
    for g in d["groups"]:
        p = DOSSIER / f"{sid_de(g['id'])}.json"
        etat = ("valide" if not valider(p) else "REFUSÉE") if p.is_file() else "à synthétiser"
        print(f"  {g['id']}  {len(g['members'])} fiches  {etat:<14} {sid_de(g['id'])}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Les hypothèses de synthèse — D39")
    ap.add_argument("--prepare", metavar="GRAPPE")
    ap.add_argument("--record", type=Path)
    ap.add_argument("--check", type=Path)
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)
    if a.prepare:
        return do_prepare(a.prepare)
    if a.record:
        return do_record(a.record)
    if a.check:
        return do_check(a.check)
    return do_status()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
