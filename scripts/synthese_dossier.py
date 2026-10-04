"""La synthèse d'un dossier — un papier et ses voisins dans toute la base (`D47`).

`scripts/voisins.py` trouve, par le sens, les papiers proches d'une fiche dans
toute la base, fichés ou non (`D45`). Ce script en fait une **consigne de
synthèse** : la fiche graine, et pour chaque voisin ses meilleurs passages (et
sa fiche s'il en a une). Une session isolée (`fabrique-synthese`) lit cette
consigne — **aucun résultat de nos données** — et écrit UNE fiche de synthèse :
l'hypothèse du papier graine, **complétée** par ce que les voisins apportent,
une seule version, choisie avant toute mesure selon `synthese.CRITERES`.

**Ce qui fait foi pour une citation d'un voisin sans fiche** : son texte en base,
**figé** au moment de la préparation dans `corpus/text/base-<id>.default.txt`,
versionné comme les extractions de `D18`. Le validateur y cherche chaque
citation à la lettre, et la recette (`recette.texte_du_papier`) le relit sans
changement. Un voisin fiché garde ses propres extractions.

La fiche rendue entre ensuite dans la chaîne ordinaire : recette, deux codeurs,
double codage, hypothèse, lot.

    python scripts/synthese_dossier.py --prepare <fiche_graine> [--voisins 8]
    python scripts/synthese_dossier.py --record <fiche de synthèse>
    python scripts/synthese_dossier.py --check  <fiche de synthèse>
    python scripts/synthese_dossier.py --status
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
sys.path.insert(0, str(REPO / "vectordb"))

from codage_verifie import empreinte16  # noqa: E402
from synthese import CRITERES, DOSSIER, PRODUCED, SCHEMA, WORK, do_record  # noqa: E402

DOSSIERS = REPO / "corpus" / "dossiers"
TEXT = REPO / "corpus" / "text"
PASSAGES = 4  # passages par voisin montrés à la synthèse


def sid_de(graine: str) -> str:
    return f"synthese-dossier-{graine}"


def base_id(paper_id: str) -> str:
    """L'identifiant d'un voisin sans fiche : le début de son identifiant en base."""
    return f"base-{paper_id[:8]}"


def fiches() -> dict[str, Path]:
    from code_signal import fiche_files  # noqa: PLC0415

    return {k: v for k, v in fiche_files().items() if not k.startswith("synthese-")}


def figer_texte(api, paper_id: str, ident: str) -> Path:
    """Le texte entier du papier en base, morceau après morceau, figé une fois."""
    out = TEXT / f"{ident}.default.txt"
    if out.is_file():
        return out
    morceaux, debut = [], 0
    while True:
        lot = api.appel("GET", f"/rest/v1/chunks?select=ordinal,content&paper_id=eq.{paper_id}"
                               f"&order=ordinal&offset={debut}&limit=1000") or []
        morceaux += lot
        if len(lot) < 1000:
            break
        debut += 1000
    if not morceaux:
        raise SystemExit(f"aucun morceau en base pour {paper_id}")
    out.write_text("\n\n".join(m["content"] for m in morceaux) + "\n", encoding="utf-8")
    return out


def sources_du_dossier(d: dict) -> dict[str, dict]:
    """Chaque source possible de la synthèse : la graine, puis chaque voisin."""
    out = {d["seed"]["fiche_id"]: {"kind": "graine", "title": d["seed"]["title"]}}
    for v in d["neighbors"]:
        ident = v["fiche_id"] or base_id(v["paper_id"])
        out[ident] = {"kind": "voisin fiché" if v["fiche_id"] else "voisin sans fiche",
                      "title": v["title"], "paper_id": v["paper_id"],
                      "similarity": v["similarity"]}
    return out


CONSIGNE = """\
# Consigne de synthèse d'un dossier — La Fabrique, `D47`

Tu écris **une fiche de synthèse** à partir d'un **papier graine** et de {n}
papiers **voisins**, trouvés par le sens dans toute notre base de papiers
(cosinus de leurs passages au mécanisme de la graine). Tu n'as accès qu'à ce
fichier. **Tu ne connais aucun résultat obtenu sur nos données, et tu ne dois
pas en chercher** : la version que tu retiens se choisit sur ce que disent les
papiers, jamais sur ce qui « marcherait ».

## Ce que tu cherches

L'hypothèse **du papier graine**, rendue **plus complète** par ses voisins :
un voisin peut confirmer le mécanisme, en préciser la construction, donner un
paramètre que la graine ne donne pas, dire sur quel marché ou à quel horizon il
tient, ou le contredire. Tu retiens **une seule version**, d'une **seule
famille de signal** — celle de la graine, ou celle d'un voisin si les
critères ci-dessous l'imposent.

Tu **n'empiles pas** des signaux distincts, et tu **ne conditionnes pas** le
signal à un régime (« seulement les jours de forte volatilité ») : les régimes
et les combinaisons sont des étapes à part, plus tard dans la chaîne. Un
voisin sans rapport réel avec la graine — la similarité du texte ne prouve pas
qu'il dit la même chose — **s'ignore**, et tu le dis dans `ignored`.

## Ce que tu rends

Un **seul fichier JSON**, écrit à `{chemin}`. C'est une fiche au schéma
ci-dessous (section SCHÉMA), avec ces règles propres à une synthèse :

- `fiche_id` : `{sid}` ; `written` : `{today}` ; `written_by` : ton nom.
- `source` : `authors` = « Synthèse de : » suivi des auteurs des papiers
  retenus ; `title` = « Synthèse — » suivi du mécanisme ; `year` = l'année la
  plus récente des sources ; `source_url` = celle du papier dont vient la
  construction retenue ; `retrieved` = `{today}` ; `peer_reviewed` = `false`.
  Pas de `pdf`.
- `claim` : l'affirmation, telle que les papiers retenus la soutiennent.
- `reported_results` : des résultats **recopiés à la lettre** de la fiche
  graine, d'une fiche voisine, ou **d'un passage cité ci-dessous** — chacun
  avec un champ `from_fiche` qui nomme sa source par son **identifiant**
  (`{graine}`, ou l'identifiant d'un voisin entre crochets ci-dessous). Une
  citation qui ne figure pas mot pour mot dans ta source sera refusée.
- `signal_construction` : **la version retenue**, une seule.
- un bloc `synthesis` :

```json
"synthesis": {{
  "dossier": "{graine}",
  "sources": ["{graine}", "<identifiant d'un voisin retenu>", "..."],
  "ignored": ["<identifiant d'un voisin écarté> : <pourquoi>"],
  "mechanism": "<le mécanisme commun, en tes mots>",
  "agreements": ["<ce sur quoi les papiers s'accordent>"],
  "disagreements": ["<ce sur quoi ils divergent : fenêtre, marché, signe, horizon…>"],
  "contributions": ["<identifiant> : <ce que ce voisin ajoute à la graine>"],
  "criteria_applied": ["<chaque critère ci-dessous, et ce qu'il a tranché>"],
  "chosen_from": ["<identifiant dont vient la construction retenue>"],
  "why": "<pourquoi cette version, en une ou deux phrases>"
}}
```

`sources` contient toujours la graine et au moins un voisin.

## Comment choisir la version — dans cet ordre, et rien d'autre

{criteres}

Si les papiers se contredisent sur le **signe** de l'effet, ne tranche pas par
préférence : écris-le dans `disagreements`, et retiens la version du critère 1.

## Ce que tu ne fais pas

Tu n'inventes aucun paramètre, aucune valeur, aucune citation. Ce qu'aucun
papier ne dit reste `null`, avec sa raison.

---

## SCHÉMA

{schema}

---

## LE PAPIER GRAINE — `{graine}`

```json
{fiche_graine}
```

---

## LES VOISINS

{voisins}
"""


def do_prepare(graine: str, n_voisins: int) -> int:
    from embed_api import Api  # noqa: PLC0415
    from voisins import chercher, ecrire  # noqa: PLC0415

    ff = fiches()
    if graine not in ff:
        raise SystemExit(f"fiche graine inconnue : {graine}")
    sid = sid_de(graine)
    if (DOSSIER / f"{sid}.json").is_file():
        raise SystemExit(f"{sid} existe déjà : son dossier est figé. Une synthèse se refait "
                         "par une décision écrite, pas en réécrivant ce contre quoi on la juge.")
    d = chercher(graine, n_voisins, PASSAGES)
    # Le dossier d'une synthèse est figé sous le nom de la synthèse : `voisins.py`
    # peut réécrire le dossier d'exploration, jamais celui contre lequel on juge.
    d["seed"]["dossier_of"] = sid_de(graine)
    ecrire(d, nom=sid_de(graine))
    api = Api()
    blocs = []
    for v in d["neighbors"]:
        if v["fiche_id"] and v["fiche_id"] in ff:
            ident = v["fiche_id"]
            texte = ff[ident].read_text(encoding="utf-8")
            corps = f"Ce voisin a sa fiche :\n\n```json\n{texte}\n```\n"
        else:
            ident = base_id(v["paper_id"])
            figer_texte(api, v["paper_id"], ident)
            corps = ""
        passages = "\n\n".join(
            f"> *{p['section']}, page {p['page']}, similarité {p['similarity']:.3f}*\n>\n> "
            + " ".join(p["content"].split()) for p in v["passages"])
        blocs.append(f"### [{ident}] {v['title']}\n\nSimilarité {v['similarity']:.3f}.\n\n"
                     f"{corps}Ses passages les plus proches de la graine :\n\n{passages}\n")
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{sid}.md"
    out.write_text(CONSIGNE.format(
        n=len(d["neighbors"]), graine=graine, sid=sid, today=date.today().isoformat(),
        chemin=(DOSSIER / f"{sid}.json").relative_to(REPO).as_posix(),
        criteres="\n".join(f"{i}. {c}" for i, c in enumerate(CRITERES, 1)),
        schema=SCHEMA.read_text(encoding="utf-8"),
        fiche_graine=ff[graine].read_text(encoding="utf-8"), voisins="\n".join(blocs)),
        encoding="utf-8")
    print(f"dossier         : {(DOSSIERS / f'{sid}.json').relative_to(REPO).as_posix()} "
          f"({len(d['neighbors'])} voisins)")
    ko = out.stat().st_size / 1000
    print(f"consigne écrite : {out.relative_to(REPO).as_posix()}  ({ko:.0f} ko)")
    print(f"fiche attendue  : {(DOSSIER / f'{sid}.json').relative_to(REPO).as_posix()}")
    return 0


def textes(ident: str, ff: dict[str, Path]) -> dict[str, str]:
    """Le texte qui fait foi pour une source : ses extractions D18, ou son texte figé."""
    from score_extraction import texts_of  # noqa: PLC0415

    if ident in ff:
        return {f"{ident}.{m}": t for m, t in
                texts_of(json.loads(ff[ident].read_text(encoding="utf-8"))).items()}
    p = TEXT / f"{ident}.default.txt"
    return {ident: p.read_text(encoding="utf-8")} if p.is_file() else {}


def valider(path: Path) -> list[str]:
    from score_extraction import check_f2  # noqa: PLC0415
    from validate_fiches import check_fiche  # noqa: PLC0415

    fiche = json.loads(path.read_text(encoding="utf-8"))
    syn = fiche.get("synthesis")
    if not isinstance(syn, dict):
        return ["bloc `synthesis` absent"]
    graine = syn.get("dossier")
    f_dossier = DOSSIERS / f"{sid_de(graine)}.json"
    if not graine or not f_dossier.is_file():
        return [f"dossier introuvable : {f_dossier.relative_to(REPO).as_posix()}"]
    possibles = sources_du_dossier(json.loads(f_dossier.read_text(encoding="utf-8")))
    fautes = []
    if fiche.get("fiche_id") != sid_de(graine) or path.stem != sid_de(graine):
        fautes.append(f"fiche_id et nom de fichier doivent valoir {sid_de(graine)}")
    sources = syn.get("sources") or []
    if graine not in sources or len(sources) < 2:
        fautes.append("`sources` contient la graine et au moins un voisin")
    hors = [s for s in sources if s not in possibles]
    if hors:
        fautes.append(f"sources hors du dossier : {hors}")
    choisies = syn.get("chosen_from") or []
    if not choisies or any(c not in sources for c in choisies):
        fautes.append("`chosen_from` doit nommer au moins une source de la synthèse")
    for cle in ("mechanism", "why"):
        if not str(syn.get(cle) or "").strip():
            fautes.append(f"synthesis.{cle} vide")
    for cle in ("agreements", "disagreements", "criteria_applied", "contributions"):
        if not isinstance(syn.get(cle), list) or not syn.get(cle):
            fautes.append(f"synthesis.{cle} doit être une liste non vide")
    for i, r in enumerate(fiche.get("reported_results") or []):
        if isinstance(r, dict) and r.get("from_fiche") not in sources:
            fautes.append(f"reported_results[{i}] : `from_fiche` doit nommer une source")
    fautes += check_fiche(path.stem, fiche)
    if not fautes:
        ff = fiches()
        tous = {}
        for s in sources:
            t = textes(s, ff)
            if not t:
                fautes.append(f"texte de {s} introuvable — relancer `--prepare`")
            tous.update(t)
        if not fautes:
            fautes += check_f2(fiche, tous)
    reg = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = reg.get(path.stem)
    if ligne is None:
        fautes.append("fiche non inscrite : `--record` avant `--check`")
    elif ligne["sha256_16"] != empreinte16(path):
        fautes.append("fiche modifiée depuis sa production — une synthèse se refait, "
                      "elle ne se retouche pas")
    return fautes


def do_check(path: Path) -> int:
    fautes = valider(path)
    if fautes:
        print(f"SYNTHÈSE REFUSÉE — {path.stem} :")
        for f in fautes:
            print(f"  - {f}")
        return 1
    print(f"SYNTHÈSE VALIDE — {path.stem} : chaque citation est dans le texte d'une source, "
          "chaque source dans le dossier, la version retenue dit d'où elle vient")
    return 0


def do_status() -> int:
    for f in sorted(DOSSIERS.glob("synthese-dossier-*.json")):
        p = DOSSIER / f"{f.stem}.json"
        etat = ("valide" if not valider(p) else "REFUSÉE") if p.is_file() else "à synthétiser"
        print(f"  {etat:<14} {f.stem}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La synthèse d'un dossier de voisins — D47")
    ap.add_argument("--prepare", metavar="FICHE_GRAINE")
    ap.add_argument("--voisins", type=int, default=8)
    ap.add_argument("--record", type=Path)
    ap.add_argument("--check", type=Path)
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)
    if a.prepare:
        return do_prepare(a.prepare, a.voisins)
    if a.record:
        return do_record(a.record)
    if a.check:
        return do_check(a.check)
    return do_status()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
