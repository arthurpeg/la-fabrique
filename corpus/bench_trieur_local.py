"""Le trieur en local — la moins chère des trois étapes qui demandent un LLM.

`D15` a écrit le seuil du triage **avant** que le trieur existe, et le juge
(`corpus/score_triage.py`, 10 vérifications) ainsi que l'étalon (les 20 verdicts
humains de la colonne « implémentable » d'`AMORCE.md`) existent depuis le
2026-09-19. La question « un modèle local sait-il trier ? » se mesure donc sans
rien construire de neuf : il suffit de faire passer le même examen.

**Pourquoi cette étape et pas l'extraction.** Le 2026-09-24 a montré que ce qui
tue un modèle local n'est pas le raisonnement mais le **contexte** : 39K tokens
de papier font un cache KV de ~6 Go, hors de portée de 4 Go de VRAM. Le triage
ne lit qu'une **ligne de tableau** — titre, ce que le papier prédit, fréquence,
univers, données exigées. Environ 1K tokens. La contrainte qui a tout fait
échouer n'existe pas ici.

**UN APPEL PAR ENTRÉE, et c'est le cœur du dispositif.** Envoyer les 20 d'un coup
recréerait exactement le problème de contexte qu'on cherche à éviter, et ferait
dépendre chaque verdict des 19 autres. Une entrée, une invite courte, un verdict.

**L'isolement est ici PARFAIT, et mieux que celui d'une session.** `D15` §
Complément et `F42` exigent que le trieur n'ait pas lu `AMORCE.md`, qui porte la
réponse. Une session doit le promettre ; un modèle appelé par l'API d'`ollama`
**n'a aucun accès au disque** — il ne voit que les octets qu'on lui envoie. La
contamination n'est pas improbable, elle est impossible.

**`L17` est respectée dans l'exemple de format.** `corpus/TRIAGE.md` illustrait
le sien avec deux entrées RÉELLES et leur vrai verdict, dont l'un des deux seuls
`non` — le document écrit pour empêcher la contamination en était le vecteur.
L'exemple ci-dessous porte un numéro d'entrée **qui n'existe pas** et un sujet
fabriqué.

    python corpus/bench_trieur_local.py --run [--model qwen3:4b]
    python corpus/bench_trieur_local.py --juger <verdicts.json>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "corpus"))

from bench_extractor import appel, appel_gemini, est_gemini  # noqa: E402

ENTREE = REPO / "corpus" / "triage_input.json"
BENCH = REPO / "corpus" / "bench"
JUGE = REPO / "corpus" / "score_triage.py"

DEFAULT_MODEL = "qwen3:4b"
NUM_CTX = 8192  # une ligne de tableau + la regle : ~1K tokens, 8192 est large

# La regle et les contraintes sont RECOPIEES DE `corpus/TRIAGE.md`, qui les tient
# d'`AMORCE.md` (phase 01) et de `D01`. Elles definissent les trois classes sans
# rien dire d'aucune entree — c'est ce qui les rend donnables au trieur.
CONSIGNE = """\
Tu tries UN papier academique. Tu reponds si ce papier est implementable comme
signal sur NOTRE univers, et sur rien d'autre.

## Les trois classes, telles que le projet les definit

- **oui** = calculable avec open/high/low/close/volume a la minute, sur nos neuf
  instruments, sans donnee exterieure.
- **partiel** = exige une donnee que nous n'avons pas mais qui est gratuite et
  obtenable (par exemple un calendrier d'annonces), OU un univers different dont
  la methode se transpose.
- **non** = exige une donnee que nous n'avons pas et qui coute.

## Nos contraintes de donnees

- neuf futures CME Globex, barres **1 minute**, OHLCV seul ;
- grille actif x seance (ASIA, EUROPE, US), 25 cellules retenues sur 27 ;
- detention **intraday**, cloture forcee en fin de fenetre ;
- **une seule echeance** par contrat — pas de structure de terme, pas de base ;
- **aucun calendrier** d'annonces macro dans les fichiers ;
- **aucun carnet d'ordres**, aucune donnee d'options, aucun consensus d'analystes ;
- largeur effective mesuree a **4,22 paris** pour neuf instruments — un test
  transversal en deciles n'a pas de sens ici.

## Ce que tu rends

Un seul objet JSON, rien avant, rien apres :

{{"verdict": "oui|partiel|non", "reason": "une phrase courte qui dit CE QUI
manque ou CE QUI transpose"}}

Exemple de FORME uniquement (ce papier n'existe pas) :

{{"verdict": "non", "reason": "Exige le flux de revisions d'analystes, donnee
payante que nous n'avons pas."}}

## Le papier a trier

{papier}
"""


# VARIANTE « b » — MEME REGLE, MEME CONTRAINTES, AUTRE MISE EN FORME.
#
# Le passage « a » du 2026-09-25 a rendu 16 `partiel` sur 20, presque tous avec
# la meme phrase — « exige un calendrier d'annonces macro » — y compris pour des
# papiers qui n'en demandent aucun. Ce n'est pas un jugement nuance qui se
# trompe, c'est une reponse DEGENEREE : le modele s'est accroche a une
# contrainte de la liste et l'a appliquee partout.
#
# Avant de conclure que le modele ne sait pas trier, il faut separer les deux
# causes (`L18`). Cette variante ne change NI la regle NI les contraintes — elle
# demande seulement de NOMMER D'ABORD la donnee exigee par le papier, puis de
# classer. Un petit modele qui doit repondre avant de raisonner attrape le
# motif le plus saillant ; celui-la doit d'abord lire.
#
# CE QU'ELLE NE FAIT PAS : souffler la distribution de l'etalon. Dire « la
# plupart des papiers n'exigent rien de plus » serait donner la reponse, et
# c'est exactement ce que `F42` et `L17` interdisent.
CONSIGNE_B = CONSIGNE.replace(
    """## Ce que tu rends

Un seul objet JSON, rien avant, rien apres :

{{"verdict": "oui|partiel|non", "reason": "une phrase courte qui dit CE QUI
manque ou CE QUI transpose"}}""",
    """## Comment tu procedes, dans cet ordre

1. **Dis d'abord quelle donnee le papier exige REELLEMENT** pour etre calcule.
   Beaucoup de signaux ne demandent que des prix et des volumes : ne suppose pas
   qu'une donnee exterieure est necessaire si le papier n'en nomme aucune.
2. **Puis compare** cette donnee a ce que nous avons.
3. **Puis classe.**

## Ce que tu rends

Un seul objet JSON, rien avant, rien apres :

{{"donnee_exigee": "ce que le papier demande, en trois mots",
  "verdict": "oui|partiel|non", "reason": "une phrase courte qui dit CE QUI
manque ou CE QUI transpose"}}""",
)


def rendre_papier(entree: dict) -> str:
    return "\n".join(f"- **{cle}** : {valeur}" for cle, valeur in entree["fields"].items())


def extraire_json(texte: str) -> dict | None:
    brut = texte.strip()
    debut, fin = brut.find("{"), brut.rfind("}")
    if debut < 0 or fin <= debut:
        return None
    try:
        return json.loads(brut[debut : fin + 1])
    except json.JSONDecodeError:
        return None


def do_run(model: str, consigne_id: str = "a") -> int:
    payload = json.loads(ENTREE.read_text(encoding="utf-8"))
    entrees = payload["entries"]
    fonction = appel_gemini if est_gemini(model) else appel

    verdicts, illisibles, secondes = [], [], 0.0
    print(f"trieur local — {model}, {len(entrees)} entrees, un appel chacune\n")

    for e in entrees:
        gabarit = CONSIGNE if consigne_id == "a" else CONSIGNE_B
        invite = gabarit.format(papier=rendre_papier(e))
        debut = time.time()
        try:
            rep = fonction(model, [{"role": "user", "content": invite}], NUM_CTX)
        except Exception as exc:
            print(f"  entree {e['entry']:>2} : ECHEC {type(exc).__name__}")
            illisibles.append(e["entry"])
            continue
        secondes += rep["_wall_s"]

        objet = extraire_json((rep.get("message") or {}).get("content", ""))
        if not objet or objet.get("verdict") not in ("oui", "partiel", "non"):
            print(f"  entree {e['entry']:>2} : SORTIE ILLISIBLE")
            illisibles.append(e["entry"])
            continue

        verdicts.append({
            "entry": e["entry"],
            "verdict": objet["verdict"],
            "reason": str(objet.get("reason", ""))[:400],
        })
        print(f"  entree {e['entry']:>2} : {objet['verdict']:<8} {rep['_wall_s']:>6.1f}s"
              f"   {str(objet.get('reason',''))[:60]}")
        _ = time.time() - debut

    BENCH.mkdir(parents=True, exist_ok=True)
    suffixe = "" if consigne_id == "a" else f"+{consigne_id}"
    sortie = BENCH / f"trieur_{model.replace(':', '_')}{suffixe}.json"
    # LA FORME QUE LE JUGE ATTEND — lue dans `read_verdicts`, pas devinee : un
    # objet portant `entries`, jamais une liste nue. Verifie AVANT de relancer
    # vingt appels, ce qui n'a pas ete fait la premiere fois.
    sortie.write_text(
        json.dumps({"source": model, "entries": verdicts}, ensure_ascii=False, indent=1)
        + "\n",
        encoding="utf-8",
    )

    print(f"\n{len(verdicts)} verdict(s) sur {len(entrees)}, "
          f"{len(illisibles)} illisible(s), {secondes / 60:.1f} min au total")
    if illisibles:
        # UNE ENTREE MANQUANTE N'EST PAS UNE ENTREE NEUTRE : le juge compte sur
        # les 20, et un trieur qui se tait sur les cas durs se noterait tout
        # seul. `L21` — un compte qui perd un element le perd du bon cote.
        print(f"  entrees sans verdict : {illisibles}")
        print("  Le juge va les compter comme des desaccords, et c'est voulu.")
    print(f"\necrit : {sortie.relative_to(REPO)}")
    return do_juger(sortie)


def do_juger(chemin: Path) -> int:
    print(f"\n{'=' * 60}\nLE JUGE — `D15`, quatre conditions en effectifs\n")
    r = subprocess.run(
        [sys.executable, str(JUGE), str(chemin)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    print(r.stdout or r.stderr)
    return r.returncode


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le trieur en local — D15")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--juger", type=Path, metavar="VERDICTS")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--consigne", default="a", choices=("a", "b"))
    a = ap.parse_args(argv)

    if a.juger:
        return do_juger(a.juger)
    if a.run:
        return do_run(a.model, a.consigne)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
