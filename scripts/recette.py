"""La recette d'une fiche — le point 1 de `D34`.

Un codeur se trompe surtout quand il doit **deviner** : quelle fenêtre, à quelle
barre une entrée est connue, quelle normalisation. La fiche (`D14`) résume le
papier ; elle ne garantit pas que chaque paramètre du calcul y soit. La recette
est un complément écrit AVANT le codage par une session isolée qui relit le
texte du papier, et qui rend, **cités mot pour mot** :

- la **formule** du signal ;
- les **entrées**, et l'instant où chacune est connue ;
- le **timing** : à quel instant le score se pose ;
- chaque **paramètre** numérique ;
- les **ambiguïtés** : ce que le papier ne tranche pas.

**Tout ce que le papier ne dit pas est `null`, avec sa raison.** Un paramètre
deviné par la recette serait un paramètre inventé que `S5` laisserait ensuite
passer : c'est pourquoi `S5` ne lit dans la recette QUE les valeurs et les
citations, jamais la prose (`scripts/score_signal.py`, `texte_de_la_recette`).

Le validateur est mécanique, comme celui des fiches : chaque citation se
retrouve à la lettre dans le texte du papier (`D18`, extraction `default`),
chaque valeur numérique se retrouve dans sa citation (`value_in_quote`, `D09`),
chaque `null` porte sa raison. Il n'y a aucun IC ici.

    python scripts/recette.py --prepare <fiche_id>      # la consigne de la session
    python scripts/recette.py --record corpus/recettes/<fiche_id>.json
    python scripts/recette.py --check corpus/recettes/<fiche_id>.json
    python scripts/recette.py --self-check              # juger le validateur
    python scripts/recette.py --status                  # quelles fiches ont la leur
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "catalogue"))
sys.path.insert(0, str(REPO / "corpus"))

from codage_verifie import RECETTES, empreinte16, maintenant  # noqa: E402
from score_extraction import REPAIRS, normalize  # noqa: E402
from validate import value_in_quote  # noqa: E402

TEXT = REPO / "corpus" / "text"
WORK = REPO / "corpus" / "consignes-recettes"
PRODUCED = RECETTES / "PRODUCED.json"
MODE = "default"  # D18, identique aux extracteurs de fiches

ELISION = re.compile(r"\s*(?:\.\.\.|…|\[\.\.\.\]|\[…\])\s*")

CONSIGNE = """\
# Consigne de recette — La Fabrique, `D34`

Tu complètes **une fiche** de papier académique par sa **recette** : la formule,
les entrées, le timing, les paramètres et les ambiguïtés du signal, **cités mot
pour mot** dans le texte du papier. Un codeur lira ta recette et rien d'autre du
papier : ce que tu n'écris pas, il devra le deviner ; ce que tu inventes, il le
codera.

## Ce que tu rends

Un **seul fichier JSON**, écrit à `{chemin}`. Rien d'autre.

## Le format

Exemple **fabriqué** — il cite un papier qui n'existe pas (`L17`) :

```json
{{
  "fiche_id": "{fiche_id}",
  "written": "AAAA-MM-JJ",
  "written_by": "<modèle>",
  "formula": {{
    "statement": "score = rendement de l'ouverture à la barre notée, divisé par sa volatilité",
    "quoted": "we scale the return since the open by its trailing volatility",
    "reason": null
  }},
  "inputs": [
    {{"name": "open_return", "description": "rendement depuis l'ouverture de la séance",
      "known_at": "à la clôture de la barre notée", "quoted": "the return since the open"}}
  ],
  "timing": {{
    "statement": "le score se pose 45 minutes avant la clôture",
    "quoted": "the signal is formed 45 minutes before the close",
    "reason": null
  }},
  "parameters": [
    {{"name": "formation_minutes", "value": 45, "unit": "minutes",
      "quoted": "the signal is formed 45 minutes before the close"}},
    {{"name": "volatility_window_days", "value": null, "unit": "days",
      "quoted": null, "reason": "le papier dit « trailing » sans donner la longueur"}}
  ],
  "ambiguities": [
    {{"question": "la volatilité est-elle calculée sur les rendements journaliers ou intraday ?",
      "resolution": null, "quoted": null}}
  ]
}}
```

## Les règles, vérifiées par une machine

- **`quoted`** est une phrase du papier, **à la lettre**, ou un extrait coupé
  par `...`. Une paraphrase est refusée. Le contrôle cherche la chaîne dans le
  texte ci-dessous, casse et espaces repliés.
- **Si le texte extrait abîme la phrase** (formule mathématique mal rendue,
  tableau mis à plat, scan) : écris la phrase telle que le papier la dit dans
  `quoted`, telle que le texte la porte dans `quoted_source`, et le motif dans
  `quoted_repair`, parmi {repairs}. C'est `quoted_source` qui est cherchée.
- **Chaque `value` numérique se retrouve dans sa citation.** Un nombre que tu as
  calculé toi-même porte `"derived": true` et un `note` qui dit comment.
- **Tout ce que le papier ne dit pas est `null`**, avec `reason` non vide.
  **N'invente jamais une valeur plausible** : c'est un interdit constitutionnel
  du projet. Un `null` est bruyant, une valeur inventée est invisible.
- `formula`, `timing` et au moins une entrée sont exigés. `quoted` peut y être
  `null`, avec sa raison.
- **Les ambiguïtés sont le cœur du travail.** Chaque question dont la réponse
  change le calcul — une fenêtre, une normalisation, un traitement des jours
  fériés, un signe — s'écrit ici, avec la réponse du papier si elle existe
  (`resolution` et `quoted`), ou `null` s'il n'en donne pas.
{precisions}
## Ce que tu ne fais pas

Tu ne codes rien, tu ne mesures rien, tu ne juges pas si l'idée est bonne. Tu
dis **ce que le papier dit**, et où il se tait.

---

## LA FICHE

```json
{fiche}
```

---

## LE TEXTE DU PAPIER

{text}
"""


# ---------------------------------------------------------------------------
# Où sont les choses
# ---------------------------------------------------------------------------

def fiche_files() -> dict[str, Path]:
    from code_signal import fiche_files as ff  # noqa: PLC0415

    return ff()


def recette_path(fiche_id: str) -> Path:
    return RECETTES / f"{fiche_id}.json"


def texte_du_papier(fiche_id: str) -> str:
    p = TEXT / f"{fiche_id}.{MODE}.txt"
    if not p.is_file():
        raise SystemExit(f"texte absent : {p.relative_to(REPO)} — `python corpus/extract_text.py`")
    return p.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Le validateur
# ---------------------------------------------------------------------------

def trouvee(citation: str, texte_normalise: str) -> bool:
    """La citation, ou chacun de ses morceaux coupés par `...`, dans l'ordre."""
    curseur = 0
    for frag in (f for f in ELISION.split(citation) if f.strip()):
        pos = texte_normalise.find(normalize(frag), curseur)
        if pos < 0:
            return False
        curseur = pos + len(normalize(frag))
    return curseur > 0


def fautes_citation(where: str, bloc: dict, texte_n: str, exige_raison_si_null=True) -> list[str]:
    fautes: list[str] = []
    q = bloc.get("quoted")
    qs, motif = bloc.get("quoted_source"), bloc.get("quoted_repair")
    if (qs is None) != (motif is None):
        fautes.append(f"{where} : `quoted_source` et `quoted_repair` vont ensemble")
    if motif is not None and motif not in REPAIRS:
        fautes.append(f"{where} : motif de réparation {motif!r} hors de la liste {sorted(REPAIRS)}")
    if q is None:
        if exige_raison_si_null and not str(bloc.get("reason") or "").strip():
            fautes.append(f"{where} : `quoted` vaut null sans `reason`")
        return fautes
    if not isinstance(q, str) or not q.strip():
        return fautes + [f"{where} : `quoted` doit être une chaîne non vide, ou null"]
    cherchee = qs if qs is not None else q
    if not trouvee(cherchee, texte_n):
        fautes.append(f"{where} : citation introuvable dans le texte du papier : "
                      f"« {cherchee[:90]} »")
    return fautes


def valider(recette: dict, fiche_id: str, texte: str) -> list[str]:
    """Les fautes d'une recette. Vide = recette valide."""
    fautes: list[str] = []
    texte_n = normalize(texte)
    if recette.get("fiche_id") != fiche_id:
        fautes.append(f"fiche_id = {recette.get('fiche_id')!r}, attendu {fiche_id!r}")
    for cle in ("written", "written_by"):
        if not str(recette.get(cle) or "").strip():
            fautes.append(f"`{cle}` manque")

    for cle in ("formula", "timing"):
        bloc = recette.get(cle)
        if not isinstance(bloc, dict):
            fautes.append(f"`{cle}` manque ou n'est pas un objet")
            continue
        if not str(bloc.get("statement") or "").strip():
            fautes.append(f"{cle} : `statement` vide")
        fautes += fautes_citation(cle, bloc, texte_n)

    inputs = recette.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        fautes.append("`inputs` : au moins une entrée est exigée")
        inputs = []
    for i, e in enumerate(inputs):
        where = f"inputs[{i}] {e.get('name', '?')}"
        for cle in ("name", "description", "known_at"):
            if not str(e.get(cle) or "").strip():
                fautes.append(f"{where} : `{cle}` vide")
        fautes += fautes_citation(where, e, texte_n)

    params = recette.get("parameters")
    if not isinstance(params, list):
        fautes.append("`parameters` doit être une liste (vide si le papier n'en a aucun)")
        params = []
    noms = [p.get("name") for p in params]
    if len(set(noms)) != len(noms):
        fautes.append("`parameters` : des noms en double")
    for i, p in enumerate(params):
        where = f"parameters[{i}] {p.get('name', '?')}"
        if not str(p.get("name") or "").strip():
            fautes.append(f"{where} : `name` vide")
        v = p.get("value")
        if v is None:
            if not str(p.get("reason") or "").strip():
                fautes.append(f"{where} : `value` vaut null sans `reason`")
            fautes += fautes_citation(where, p, texte_n, exige_raison_si_null=False)
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            fautes.append(f"{where} : `value` doit être un nombre, ou null")
            continue
        if p.get("derived") is True:
            if not str(p.get("note") or "").strip():
                fautes.append(f"{where} : `derived` sans `note` qui dit le calcul")
            fautes += fautes_citation(where, p, texte_n, exige_raison_si_null=False)
            continue
        if p.get("quoted") is None:
            fautes.append(f"{where} : une valeur numérique sans citation est une valeur inventée")
            continue
        fautes += fautes_citation(where, p, texte_n)
        cherchee = p.get("quoted_source") or p.get("quoted")
        if isinstance(cherchee, str) and not value_in_quote(v, cherchee):
            fautes.append(f"{where} : la valeur {v:g} ne se retrouve pas dans sa citation")

    amb = recette.get("ambiguities")
    if not isinstance(amb, list):
        fautes.append("`ambiguities` doit être une liste (vide s'il n'y en a aucune)")
        amb = []
    for i, a in enumerate(amb):
        where = f"ambiguities[{i}]"
        if not str(a.get("question") or "").strip():
            fautes.append(f"{where} : `question` vide")
        if a.get("resolution") is not None and a.get("quoted") is None:
            fautes.append(f"{where} : une résolution sans citation est une réponse devinée")
        fautes += fautes_citation(where, a, texte_n, exige_raison_si_null=False)
    return fautes


def fautes_s6(path: Path) -> list[str]:
    """La recette est-elle celle qui a été produite, sans retouche ?"""
    reg = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = reg.get(path.stem)
    if ligne is None:
        return [f"{path.name} n'est pas inscrite : `--record` avant `--check`"]
    if ligne["sha256_16"] != empreinte16(path):
        return [f"{path.name} a changé depuis sa production — une recette se refait, "
                "elle ne se retouche pas"]
    return []


def recette_valide(fiche_id: str) -> tuple[bool, list[str]]:
    """Pour `code_signal.py` : la recette existe, est inscrite, et passe."""
    p = recette_path(fiche_id)
    if not p.is_file():
        return False, [f"pas de recette : {p.relative_to(REPO).as_posix()}"]
    recette = json.loads(p.read_text(encoding="utf-8"))
    fautes = fautes_s6(p) + valider(recette, fiche_id, texte_du_papier(fiche_id))
    return not fautes, fautes


# ---------------------------------------------------------------------------
# Les commandes
# ---------------------------------------------------------------------------

def do_prepare(fiche_id: str, precisions: str | None) -> int:
    fiches = fiche_files()
    if fiche_id not in fiches:
        raise SystemExit(f"fiche inconnue : {fiche_id}")
    WORK.mkdir(parents=True, exist_ok=True)
    bloc = ""
    if precisions:
        bloc = ("\n## Ce qu'un double codage a laissé ouvert\n\n"
                "Deux codeurs indépendants ont lu la recette précédente autrement "
                "sur ce point. Cherche ce que le papier en dit ; s'il se tait, "
                f"écris-le comme ambiguïté non résolue.\n\n> {precisions}\n")
    out = WORK / f"{fiche_id}.md"
    out.write_text(CONSIGNE.format(
        chemin=recette_path(fiche_id).relative_to(REPO).as_posix(),
        fiche_id=fiche_id,
        repairs=", ".join(f"`{r}`" for r in sorted(REPAIRS)),
        precisions=bloc,
        fiche=fiches[fiche_id].read_text(encoding="utf-8"),
        text=texte_du_papier(fiche_id),
    ), encoding="utf-8")
    taille = out.stat().st_size / 1000
    print(f"consigne écrite : {out.relative_to(REPO).as_posix()}  ({taille:.0f} ko)")
    print(f"recette attendue : {recette_path(fiche_id).relative_to(REPO).as_posix()}")
    return 0


def do_record(path: Path) -> int:
    path = path.resolve()
    json.loads(path.read_text(encoding="utf-8"))  # un JSON illisible n'est pas inscrit
    reg = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = reg.get(path.stem) or {"attempts": []}
    ligne["attempts"].append({"produced": maintenant(), "sha256_16": empreinte16(path)})
    ligne["sha256_16"] = ligne["attempts"][-1]["sha256_16"]
    reg[path.stem] = ligne
    PRODUCED.parent.mkdir(parents=True, exist_ok=True)
    PRODUCED.write_text(json.dumps(dict(sorted(reg.items())), ensure_ascii=False, indent=2)
                        + "\n", encoding="utf-8")
    print(f"inscrite : {path.stem}  (essai {len(ligne['attempts'])}, {ligne['sha256_16']})")
    return 0


def do_check(path: Path) -> int:
    ok, fautes = recette_valide(path.stem)
    if ok:
        print(f"RECETTE VALIDE — {path.stem} : chaque citation est dans le texte, "
              "chaque valeur dans sa citation, chaque null a sa raison")
        return 0
    print(f"RECETTE REFUSÉE — {path.stem} :")
    for f in fautes:
        print(f"  - {f}")
    return 1


def do_status() -> int:
    ids = sorted(fiche_files())
    faites = [f for f in ids if recette_path(f).is_file()]
    for f in faites:
        ok, _ = recette_valide(f)
        print(f"  {'valide ' if ok else 'REFUSÉE'} {f}")
    print(f"\n{len(faites)}/{len(ids)} fiches ont une recette")
    return 0


def self_check() -> int:
    texte = ("We form the signal 45 minutes before the close. The return since the "
             "open is scaled by its trailing volatility. Volatility uses twenty days.")
    bonne = {
        "fiche_id": "x", "written": "2026-09-30", "written_by": "test",
        "formula": {"statement": "s", "quoted": "the return since the open is scaled"},
        "timing": {"statement": "t", "quoted": "We form the signal 45 minutes before the close"},
        "inputs": [{"name": "r", "description": "d", "known_at": "k",
                    "quoted": "return since the open"}],
        "parameters": [
            {"name": "m", "value": 45, "unit": "min", "quoted": "45 minutes before the close"},
            {"name": "w", "value": None, "unit": "d", "quoted": None,
             "reason": "écrit en toutes lettres"},
        ],
        "ambiguities": [{"question": "q", "resolution": None, "quoted": None}],
    }
    cas: list[tuple[str, dict, bool]] = [("recette fidèle", bonne, True)]

    def variante(label: str, fn, attendu=False) -> None:
        r = copy.deepcopy(bonne)
        fn(r)
        cas.append((label, r, attendu))

    variante("paraphrase refusée",
             lambda r: r["timing"].update(quoted="the signal is built 45 min before close"))
    variante("valeur absente de sa citation",
             lambda r: r["parameters"][0].update(value=30))
    variante("valeur inventée sans citation",
             lambda r: r["parameters"][1].update(value=20))
    variante("null sans raison", lambda r: r["parameters"][1].update(reason=""))
    variante("résolution devinée",
             lambda r: r["ambiguities"][0].update(resolution="journaliers"))
    variante("motif de réparation inconnu",
             lambda r: r["formula"].update(quoted_source="the return", quoted_repair="flou"))
    variante("citation coupée par ... acceptée",
             lambda r: r["formula"].update(quoted="We form the signal ... before the close"),
             attendu=True)
    variante("dérivée avec sa note acceptée",
             lambda r: r["parameters"].append({"name": "h", "value": 0.75, "unit": "h",
                                               "derived": True, "note": "45 / 60",
                                               "quoted": "45 minutes"}), attendu=True)
    variante("aucune entrée", lambda r: r.update(inputs=[]))

    ok = True
    for label, r, attendu in cas:
        f = valider(r, "x", texte)
        bon = (not f) == attendu
        ok &= bon
        print(f"  {'ok  ' if bon else 'FAUX'} {label:<38} {'acceptée' if not f else f[0][:60]}")
    print("\nVALIDATEUR DE RECETTE : " + ("il refuse chaque faute, pour sa raison" if ok
                                          else "EN DÉFAUT"))
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La recette d'une fiche — D34")
    ap.add_argument("--prepare", metavar="FICHE_ID")
    ap.add_argument("--precisions", metavar="TEXTE",
                    help="avec --prepare : le point qu'un double codage a laissé ouvert")
    ap.add_argument("--record", type=Path, metavar="RECETTE.json")
    ap.add_argument("--check", type=Path, metavar="RECETTE.json")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--self-check", action="store_true")
    a = ap.parse_args(argv)
    if a.self_check:
        return self_check()
    if a.prepare:
        return do_prepare(a.prepare, a.precisions)
    if a.record:
        return do_record(a.record)
    if a.check:
        return do_check(a.check)
    if a.status:
        return do_status()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
