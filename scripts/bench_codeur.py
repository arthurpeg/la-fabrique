"""Le banc d'essai du CODEUR de signal — `D23` passé à un modèle de rechange.

L'extraction a occupé le 2026-09-25 et la question s'est deplacee : le corpus
porte desormais **51 fiches, toutes vertes**, produites par des sessions de
frontiere isolees. Ce qui manque maintenant, ce sont les **signaux** — et
`D23` a ecrit leur seuil avant que le codeur existe, avec son juge
(`scripts/score_signal.py`, six conditions a tolerance zero).

La question se mesure donc sans rien construire : faire passer le meme examen.

**Trois differences avec le banc d'extraction, et elles comptent.**

1. **La sortie est du PYTHON, pas du JSON.** Le forcage `response_format` est
   donc desactive — l'imposer rendrait du code enveloppe dans une chaine.
2. **Le module va dans `corpus/bench/signaux_<modele>/`**, jamais dans
   `signals/`. Une sortie d'essai dans la population reelle la polluerait, et
   `gate_08` juge `S6` sur TOUT `signals/PRODUCED.json` sans filtrer — meme
   piege que celui evite entre `corpus/fiches/` et `corpus/fiches_harvest/`.
3. **Aucun IC n'est calcule.** `D23` l'ecrit : la porte 08 se franchit sans
   depenser une ligne de registre, et ce banc non plus.

**Budget.** Les consignes de codage vont de 3 240 a 9 345 tokens selon la
fiche ; le palier gratuit de Groq plafonne a 8 000 par minute et **rejette**
au-dela (413, mesure du 2026-09-25). `--list` dit lesquelles passent.

    python scripts/bench_codeur.py --list
    python scripts/bench_codeur.py --run <fiche_id> --model groq/openai/gpt-oss-120b
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "corpus"))

from bench_extractor import appel_avec_attente, nom_de_fichier  # noqa: E402

CONSIGNES = REPO / "corpus" / "consignes-signaux"
FICHES = REPO / "corpus" / "fiches"
BENCH = REPO / "corpus" / "bench"
JUGE = REPO / "scripts" / "score_signal.py"
PREPARE = REPO / "scripts" / "code_signal.py"

PLAFOND_GROQ = 8000
MAX_ESSAIS = 3

REPRISE = """\
Ton module precedent a ete refuse par un controle mecanique. Voici son verdict,
mot pour mot :

{verdict}

Corrige UNIQUEMENT ce qui est reproche. Rends de nouveau le module Python
COMPLET, rien d'autre.
"""


def extraire_python(texte: str) -> tuple[str | None, str]:
    """Le module, sorti de son enrobage eventuel. La forme est NOTEE, pas tue.

    La consigne demande un module et rien d'autre ; qu'un modele l'entoure de
    prose ou d'une cloture Markdown est une faute de consigne, reparee ici mais
    comptee — c'est ce que le banc d'extraction fait pour le JSON.
    """
    bloc = re.search(r"```(?:python)?\s*(.+?)```", texte, re.S)
    if bloc:
        return bloc.group(1).strip(), "enrobe dans un bloc de code"
    nu = texte.strip()
    if nu.startswith(("\"\"\"", "'''", "#", "from ", "import ")):
        return nu, "module nu"
    return None, "aucun module Python reconnaissable"


def do_list() -> int:
    if not CONSIGNES.is_dir():
        raise SystemExit("aucune consigne — `python scripts/code_signal.py --prepare <fiche_id>`")
    print(f"consignes de codage disponibles (plafond Groq : {PLAFOND_GROQ} tokens)\n")
    for f in sorted(CONSIGNES.glob("*.md"), key=lambda p: p.stat().st_size):
        tok = f.stat().st_size // 4
        verdict = "PASSE " if tok < PLAFOND_GROQ - 600 else "trop gros"
        print(f"  {tok:>6} tokens  {verdict}  {f.stem}")
    return 0


def do_run(fiche_id: str, model: str) -> int:
    consigne = CONSIGNES / f"{fiche_id}.md"
    if not consigne.is_file():
        raise SystemExit(
            f"consigne absente — `python scripts/code_signal.py --prepare {fiche_id}`"
        )
    fiche = FICHES / f"{fiche_id}.json"
    if not fiche.is_file():
        raise SystemExit(f"fiche absente : {fiche}")

    sortie_dir = BENCH / f"signaux_{nom_de_fichier(model)}"
    sortie_dir.mkdir(parents=True, exist_ok=True)
    cible = sortie_dir / f"{fiche_id.replace('-', '_')}.py"

    texte = consigne.read_text(encoding="utf-8")
    messages = [{"role": "user", "content": texte}]
    print(f"=== {fiche_id}\n    {model}, consigne {len(texte) // 4} tokens")

    for essai in range(1, MAX_ESSAIS + 1):
        print(f"    essai {essai} — appel en cours…", flush=True)
        try:
            # `json_force=False` : le codeur rend du Python.
            rep = appel_avec_attente(model, messages, 8192, json_force=False)
        except Exception as e:
            print(f"    ECHEC — {type(e).__name__}: {str(e)[:90]}")
            return 1

        contenu = (rep.get("message") or {}).get("content", "")
        module, note = extraire_python(contenu)
        print(f"    {rep['_wall_s']}s, invite {rep.get('prompt_eval_count')} tok, "
              f"sortie {rep.get('eval_count')} tok, {note}")
        if module is None:
            messages += [
                {"role": "assistant", "content": contenu[:1500]},
                {"role": "user", "content": REPRISE.format(verdict=note)},
            ]
            continue

        cible.write_text(module + "\n", encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(JUGE), str(cible), "--fiche", str(fiche)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        verdict = (r.stdout or r.stderr or "").strip()
        # Le juge ecrit « CASSÉE », avec l'accent. Un motif sans accent ne
        # matche rien et le banc affiche « voir verdict » — il rejette alors
        # sans dire QUOI, ce qui est exactement l'ecueil de `L24`.
        cassees = re.findall(r"\b(S[1-6]) : CASS", verdict)
        if r.returncode == 0:
            print(f"    VERT a l'essai {essai} — les six conditions de D23 tiennent")
            print(f"    module : {cible.relative_to(REPO)}")
            return 0
        print(f"    refuse : {', '.join(cassees) or 'voir verdict'}")
        messages += [
            {"role": "assistant", "content": module[:1500]},
            {"role": "user", "content": REPRISE.format(verdict=verdict[:2500])},
        ]

    print(f"    EPUISE apres {MAX_ESSAIS} essais")
    return 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Banc d'essai du codeur — D23")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--run", metavar="FICHE_ID")
    ap.add_argument("--model", default="groq/openai/gpt-oss-120b")
    a = ap.parse_args(argv)

    if a.list:
        return do_list()
    if a.run:
        return do_run(a.run, a.model)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
