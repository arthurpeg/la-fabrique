"""Le banc d'essai de l'extracteur LOCAL — la question posée le 2026-09-24.

Le projet fait tourner **un seul modèle en local** : `BAAI/bge-base-en-v1.5`
via `fastembed`, pour les embeddings (`vectordb/embed.py`). Les trois étapes de
raisonnement — trieur (`D15`), extracteur (`D16`), codeur (`D23`) — ont toujours
été des sessions d'un modèle de frontière, et personne ne l'avait écrit ni
chiffré. Ce banc chiffre ce qu'un modèle **local et gratuit** ferait à la place
de l'extracteur.

**Ce qui rend la question légitime, et ce n'est pas l'économie.** L'invariant I
dit « le LLM propose, le code déterministe tranche » — il ne dit pas *lequel*.
Et l'extraction est l'étape la mieux placée pour un modèle faible, parce que
`corpus/score_extraction.py` la juge à **tolérance zéro** : un extracteur faible
échoue bruyamment et recommence, il ne se trompe pas en silence. C'est
l'architecture qui rend l'essai possible, pas l'espoir.

**L'expérience est contrôlée, et c'est tout son intérêt.** Le modèle local
reçoit **exactement la même consigne**, octet pour octet, que celle donnée aux
sessions de frontière — le fichier produit par `extract_fiche_harvest.py
--prepare`, sans un mot ajouté. Il est jugé par **le même juge**. Il a droit à la
**même boucle de reprise** (verdict du juge renvoyé, nouvel essai). Seul le
modèle change, donc seul le modèle explique l'écart.

**Référence à battre, mesurée et non recopiée** (`corpus/PRODUCED_harvest.json`,
le 2026-09-24) : **1,33 essai par fiche** sur 6 fiches produites par un modèle de
frontière — 8 essais, 6 fiches, 6 vertes. En phase 07, sur une autre population :
1,29.

**Le banc n'écrit JAMAIS dans `corpus/fiches_harvest/`.** Ses sorties vont dans
`corpus/bench_local/<modele>/`. Une fiche d'essai dans la population réelle la
polluerait, et c'est la même faute que celle évitée entre `corpus/fiches/` et
`corpus/fiches_harvest/` : la séparation vit dans le stockage, pas dans la prose.

**Le contexte est fixé explicitement, et c'est la précaution qui compte.**
`ollama` tronque SILENCIEUSEMENT une invite plus longue que `num_ctx`. Un modèle
qui n'aurait vu que la moitié du papier échouerait `F2` pour une raison qui n'est
pas la sienne, et on conclurait faux. Le banc fixe `num_ctx`, mesure
`prompt_eval_count`, et **refuse de juger une sortie dont l'invite a été
tronquée** — le cas est inscrit `contexte_depasse`, jamais confondu avec un échec
de fidélité.

    python corpus/bench_local_extractor.py --machine   # CETTE machine vs la reference
    python corpus/bench_local_extractor.py --list
    python corpus/bench_local_extractor.py --run <fiche_id> [--model qwen3:8b]
    python corpus/bench_local_extractor.py --report

Code de sortie 1 si `ollama` ne répond pas, ou si aucun essai n'aboutit.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONSIGNES = REPO / "corpus" / "consignes_harvest"
BENCH = REPO / "corpus" / "bench_local"
RESULTS = BENCH / "results.json"
JUGE = REPO / "corpus" / "score_extraction.py"

OLLAMA = "http://localhost:11434"
# Qwen3-8B a ete essaye et RETIRE le 2026-09-24 : 5,2 Go de poids pour 4 Go de
# VRAM, donc inference entierement sur processeur, a une vitesse deja
# redhibitoire chez le 4B. Le meilleur modele que CE poste peut tenir est un 4B.
DEFAULT_MODEL = "qwen3:4b"

# Le contexte doit tenir la consigne ENTIERE, et PAS PLUS. Un `num_ctx` plat a
# 40960 a ete essaye le 2026-09-24 : le cache KV de Qwen3-4B pese ~144 ko par
# token, soit ~5,9 Go a 40960 — au-dela des 4 Go de VRAM ET de ce que 16 Go de
# RAM absorbent sans que Windows gonfle son fichier d'echange. Mesure : le
# disque est passe de 12 Go a 1,4 Go libres, et un seul appel sur le PLUS PETIT
# papier n'avait pas rendu la main apres 25 minutes.
#
# Le contexte est donc calcule PAR PAPIER. Trop grand coute de la memoire pour
# rien ; trop petit TRONQUE EN SILENCE, ce qui ferait echouer `F2` pour une
# raison qui n'est pas celle du modele. Le garde de troncature reste la parade.
NUM_CTX_MAX = 40960
NUM_CTX_MIN = 8192
CHARS_PAR_TOKEN = 3.5  # mesure basse, donc prudente : elle surestime le besoin
MARGE_SORTIE = 6144  # la fiche elle-meme, ecrite dans le meme contexte
MAX_ESSAIS = 3

# Mesure du 2026-09-24 : un essai a tenu 2301 s (38 min) sur ce poste, et quatre
# papiers ont expire a 3600 s sans rien rendre. Un plafond d'une heure par appel
# fait donc perdre une heure par papier pour apprendre la meme chose. 2700 s
# laisse passer l'essai le plus long observe, avec de la marge, et coupe plus tot
# ce qui ne finira pas.
TIMEOUT_APPEL_S = 2700


def contexte_pour(chars: int) -> int:
    """Le `num_ctx` juste suffisant pour cette consigne, arrondi au multiple de 2048."""
    besoin = int(chars / CHARS_PAR_TOKEN) + MARGE_SORTIE
    arrondi = ((besoin + 2047) // 2048) * 2048
    return max(NUM_CTX_MIN, min(NUM_CTX_MAX, arrondi))


# La reprise donne au modele le verdict du juge, exactement comme une session de
# frontiere le recoit. Rien de plus : ni la bonne reponse, ni un exemple.
REPRISE = """\
Ta sortie precedente a ete refusee par un controle mecanique. Voici son verdict,
mot pour mot :

{verdict}

Corrige UNIQUEMENT ce qui est reproche. Le reste de la fiche doit rester
identique. Rends de nouveau UN SEUL OBJET JSON, rien avant, rien apres.
"""


def ollama_disponible() -> bool:
    try:
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def appel(model: str, messages: list[dict], num_ctx: int = NUM_CTX_MIN) -> dict:
    """Un appel a ollama. `think: false` — le raisonnement visible brulerait le
    contexte sans rien ajouter a une tache de recopie fidele."""
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "stream": False,
            "think": False,
            "options": {"num_ctx": num_ctx, "temperature": 0},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    debut = time.time()
    with urllib.request.urlopen(req, timeout=TIMEOUT_APPEL_S) as r:
        payload = json.loads(r.read().decode("utf-8"))
    payload["_wall_s"] = round(time.time() - debut, 1)
    return payload


def extraire_json(texte: str) -> tuple[dict | None, str]:
    """Rend (objet, note). La consigne demande UN OBJET JSON ET RIEN D'AUTRE.

    Qu'un modele enrobe sa sortie d'un bloc de code ou d'une phrase est une
    FAUTE DE CONSIGNE, pas un detail d'analyse — elle est donc reparee ici mais
    NOTEE, pour que le rapport dise combien de fois elle s'est produite.
    """
    brut = texte.strip()
    if brut.startswith("{") and brut.endswith("}"):
        try:
            return json.loads(brut), "json nu"
        except json.JSONDecodeError as e:
            return None, f"json nu invalide : {e}"

    bloc = re.search(r"```(?:json)?\s*(\{.*\})\s*```", brut, re.S)
    if bloc:
        try:
            return json.loads(bloc.group(1)), "enrobe dans un bloc de code"
        except json.JSONDecodeError as e:
            return None, f"bloc de code invalide : {e}"

    debut, fin = brut.find("{"), brut.rfind("}")
    if debut >= 0 and fin > debut:
        try:
            return json.loads(brut[debut : fin + 1]), "accolades extraites de la prose"
        except json.JSONDecodeError as e:
            return None, f"prose, accolades illisibles : {e}"
    return None, "aucun objet JSON trouve"


def juger(path: Path) -> tuple[bool, str]:
    r = subprocess.run(
        [sys.executable, str(JUGE), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode == 0, (r.stdout or r.stderr or "").strip()


def conditions_cassees(verdict: str) -> list[str]:
    return re.findall(r"\b(F[1-5]) : CASSEE", verdict)


def charger_resultats() -> dict:
    if RESULTS.is_file():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {}


def ecrire_resultats(res: dict) -> None:
    BENCH.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(
        json.dumps(res, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


# Le poste sur lequel la question a ete posee, MESURE le 2026-09-24. C'est un
# fait D'UN POSTE, pas un fait du depot — le depot s'est deja trompe trois fois
# en ecrivant l'un pour l'autre (les PDF de `corpus/pdf/`, `L20`, `L21`). Il est
# donc date, nomme, et il ne sert qu'a etre COMPARE, jamais a etre cru.
REFERENCE = {
    "poste": "arthur (2026-09-24)",
    "gpu": "NVIDIA GeForce GTX 1650",
    "vram_go": 4.0,
    "ram_go": 15.9,
    "cpu": "Intel i5-10400F",
    "constat": "4 Go de VRAM : Qwen3-8B (5,2 Go) n'y tient meme pas SANS cache KV. "
    "Tout deborde en RAM, Windows gonfle son fichier d'echange, et un seul essai "
    "sur le plus petit papier depasse 25 minutes.",
}

# Qwen3-8B en Q4 : 5,2 Go de poids, et un cache KV de ~144 ko par token.
POIDS_8B_GO = 5.2
KV_KO_PAR_TOKEN = 144
VRAM_TOUT_LE_CORPUS = 12.0  # couvre num_ctx 40960 : 5,2 + 5,6 = 10,8, plus la marge
VRAM_PETITS_PAPIERS = 8.0  # couvre num_ctx ~18432 : 5,2 + 2,5 = 7,7


def _go(valeur: float) -> str:
    return f"{valeur:.1f} Go" if valeur else "inconnu"


def sonder_machine() -> dict:
    """Ce que CETTE machine peut faire. Ce qu'on ne sait pas vaut `None`, jamais
    une valeur plausible — l'interdit constitutionnel vaut ici comme ailleurs."""
    import shutil

    profil = {"gpu": None, "vram_go": None, "ram_go": None, "disque_libre_go": None}

    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=20,
        )
        if r.returncode == 0 and r.stdout.strip():
            nom, mib = (x.strip() for x in r.stdout.strip().splitlines()[0].split(","))
            profil["gpu"] = nom
            profil["vram_go"] = round(int(mib) / 1024, 1)
    except Exception:
        pass

    try:
        meminfo = Path("/proc/meminfo")
        if meminfo.is_file():
            for ligne in meminfo.read_text().splitlines():
                if ligne.startswith("MemTotal:"):
                    profil["ram_go"] = round(int(ligne.split()[1]) / 1024 / 1024, 1)
                    break
        else:
            r = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode == 0 and r.stdout.strip().isdigit():
                profil["ram_go"] = round(int(r.stdout.strip()) / 1024**3, 1)
    except Exception:
        pass

    try:
        profil["disque_libre_go"] = round(shutil.disk_usage(REPO).free / 1024**3, 1)
    except Exception:
        pass

    return profil


def do_machine() -> int:
    """Compare CETTE machine au poste de reference, par la mesure.

    Ce mode existe pour une raison precise : la question « ta machine est-elle
    meilleure que la mienne ? » se repond par un chiffre releve, pas par une
    memoire de specifications. `L21` — relancer plutot que recopier.
    """
    p = sonder_machine()
    print("CETTE MACHINE\n")
    print(f"  GPU            {p['gpu'] or 'aucun GPU NVIDIA detecte'}")
    print(f"  VRAM           {_go(p['vram_go'])}")
    print(f"  RAM            {_go(p['ram_go'])}")
    print(f"  disque libre   {_go(p['disque_libre_go'])}")

    print(f"\nPOSTE DE REFERENCE — {REFERENCE['poste']}\n")
    print(f"  GPU            {REFERENCE['gpu']}")
    print(f"  VRAM           {_go(REFERENCE['vram_go'])}")
    print(f"  RAM            {_go(REFERENCE['ram_go'])}")
    print(f"\n  {REFERENCE['constat']}")

    vram = p["vram_go"]
    print("\nVERDICT\n")
    if vram is None:
        print("  VRAM INCONNUE — sans GPU NVIDIA detecte, `nvidia-smi` ne repond pas.")
        print("  Un 8B tournerait sur processeur, donc plus lentement encore que la")
        print("  reference. Ne pas lancer le corpus entier sans avoir mesure UN papier.")
        return 1

    ecart = vram / REFERENCE["vram_go"]
    print(f"  VRAM : {_go(vram)} contre {_go(REFERENCE['vram_go'])} — "
          f"{ecart:.1f}x la reference")
    if vram >= VRAM_TOUT_LE_CORPUS:
        print(f"  AU-DESSUS DU SEUIL ({_go(VRAM_TOUT_LE_CORPUS)}) : Qwen3-8B tient en VRAM")
        print("  pour TOUS les papiers du lot, y compris les 40 960 tokens de contexte.")
    elif vram >= VRAM_PETITS_PAPIERS:
        print(f"  SEUIL PARTIEL ({_go(VRAM_PETITS_PAPIERS)}) : Qwen3-8B tient pour les")
        print("  PETITS papiers seulement. Les gros deborderont — le banc les inscrira")
        print("  `contexte_depasse` plutot que de rendre un verdict faux.")
    else:
        print(f"  SOUS LE SEUIL : {_go(vram)} ne tient pas les 5,2 Go de poids du 8B.")
        print("  Meme situation que la reference. Un 4B est le maximum realiste.")

    if p["disque_libre_go"] is not None and p["disque_libre_go"] < 15:
        print(f"\n  ATTENTION DISQUE : {_go(p['disque_libre_go'])} libres. Il faut ~6 Go")
        print("  pour le modele, ET de la marge : sous pression memoire Windows gonfle")
        print("  son fichier d'echange. Sur la reference, 12 Go libres sont tombes a 1,4.")

    print("\n  CE QUE CE VERDICT NE DIT PAS : que la fiche PASSE. La VRAM decide si le")
    print("  modele tourne, jamais s'il sait citer mot pour mot. Cela se mesure avec")
    print("  `--run`, sur un papier, et se lit dans `--report`.")
    return 0


def do_list() -> int:
    consignes = sorted(CONSIGNES.glob("*.md"))
    print(f"{len(consignes)} consigne(s) disponibles :\n")
    for c in consignes:
        ko = c.stat().st_size / 1000
        print(
            f"  {ko:>6.0f} ko  ~{ko / 4:>3.0f}K tokens  "
            f"num_ctx {contexte_pour(c.stat().st_size):>6}  {c.stem}"
        )
    return 0


def do_run(fiche_id: str, model: str) -> int:
    consigne = CONSIGNES / f"{fiche_id}.md"
    if not consigne.is_file():
        raise SystemExit(f"consigne absente : {consigne}")
    if not ollama_disponible():
        raise SystemExit("ollama ne repond pas sur localhost:11434")

    sortie_dir = BENCH / model.replace(":", "_")
    sortie_dir.mkdir(parents=True, exist_ok=True)
    cible = sortie_dir / f"{fiche_id}.json"

    texte_consigne = consigne.read_text(encoding="utf-8")
    num_ctx = contexte_pour(len(texte_consigne))
    messages = [{"role": "user", "content": texte_consigne}]

    resultats = charger_resultats()
    trace = {
        "model": model,
        "num_ctx": num_ctx,
        "consigne_chars": len(texte_consigne),
        "essais": [],
        "verdict": None,
    }

    print(f"=== {fiche_id}")
    print(f"    modele {model}, consigne {len(texte_consigne) / 1000:.0f} ko, num_ctx {num_ctx}")

    for essai in range(1, MAX_ESSAIS + 1):
        print(f"    essai {essai} — appel en cours…", flush=True)
        # `TimeoutError` N'EST PAS un `URLError`, et ne l'attraper que par ce
        # dernier a coute quatre heures de preuve le 2026-09-24 : les quatre
        # premiers papiers ont expire a une heure chacun, et l'exception est
        # remontee en traceback au lieu d'etre INSCRITE. Un echec non enregistre
        # est un echec qui n'a pas eu lieu, et c'est `L23` — un chemin de code
        # qu'aucun essai n'emprunte n'est pas un chemin verifie.
        try:
            rep = appel(model, messages, num_ctx)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ligne = {
                "essai": essai,
                "issue": "expire" if isinstance(e, TimeoutError) else "reseau",
                "detail": f"{type(e).__name__}: {e}",
                "timeout_s": TIMEOUT_APPEL_S,
            }
            trace["essais"].append(ligne)
            trace["verdict"] = ligne["issue"]
            print(f"    {ligne['issue'].upper()} — {type(e).__name__} apres "
                  f"{TIMEOUT_APPEL_S}s. INSCRIT, pas perdu.")
            break

        contenu = (rep.get("message") or {}).get("content", "")
        prompt_tokens = rep.get("prompt_eval_count", 0)
        out_tokens = rep.get("eval_count", 0)
        ligne = {
            "essai": essai,
            "wall_s": rep["_wall_s"],
            "prompt_tokens": prompt_tokens,
            "output_tokens": out_tokens,
        }

        # LA TRONCATURE SILENCIEUSE, avant tout jugement. Une invite rabotee
        # ferait echouer F2 pour une raison qui n'est pas celle du modele.
        if prompt_tokens >= num_ctx - 64:
            ligne["issue"] = "contexte_depasse"
            trace["essais"].append(ligne)
            trace["verdict"] = "contexte_depasse"
            print(
                f"    CONTEXTE DEPASSE — {prompt_tokens} tokens d'invite pour "
                f"num_ctx={num_ctx}. Non juge : l'invite a ete tronquee."
            )
            break

        objet, note = extraire_json(contenu)
        ligne["forme_sortie"] = note
        print(f"    {rep['_wall_s']}s, invite {prompt_tokens} tok, sortie {out_tokens} tok, {note}")

        if objet is None:
            ligne["issue"] = "json_illisible"
            trace["essais"].append(ligne)
            messages += [
                {"role": "assistant", "content": contenu[:2000]},
                {
                    "role": "user",
                    "content": REPRISE.format(
                        verdict=f"Ta sortie n'est pas un objet JSON lisible : {note}"
                    ),
                },
            ]
            continue

        cible.write_text(json.dumps(objet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        vert, verdict = juger(cible)
        ligne["conditions_cassees"] = conditions_cassees(verdict)
        ligne["vert"] = vert
        trace["essais"].append(ligne)

        if vert:
            trace["verdict"] = "vert"
            print(f"    VERT a l'essai {essai} — les cinq conditions de D16 tiennent")
            break

        print(f"    refuse : {', '.join(ligne['conditions_cassees']) or 'voir verdict'}")
        messages += [
            {"role": "assistant", "content": contenu[:2000]},
            {"role": "user", "content": REPRISE.format(verdict=verdict[:3000])},
        ]
    else:
        trace["verdict"] = "epuise"
        print(f"    EPUISE apres {MAX_ESSAIS} essais")

    resultats.setdefault(model, {})[fiche_id] = trace
    ecrire_resultats(resultats)
    return 0 if trace["verdict"] == "vert" else 1


def do_report() -> int:
    res = charger_resultats()
    if not res:
        raise SystemExit("aucun resultat — lancer `--run` d'abord")

    print("BANC D'ESSAI DE L'EXTRACTEUR LOCAL\n")
    print("Reference mesuree (modele de frontiere, corpus/PRODUCED_harvest.json) :")
    print("  6 fiches, 8 essais, 1,33 essai par fiche, 6 vertes sur 6\n")

    for model, fiches in sorted(res.items()):
        verts = [f for f, t in fiches.items() if t["verdict"] == "vert"]
        essais_verts = sum(len(fiches[f]["essais"]) for f in verts)
        secondes = sum(e["wall_s"] for t in fiches.values() for e in t["essais"])
        print(f"=== {model}")
        print(f"  {len(verts)} verte(s) sur {len(fiches)} papier(s) tentes")
        if verts:
            print(f"  {essais_verts / len(verts):.2f} essai par fiche VERTE (reference : 1,33)")
        print(
            f"  {secondes / 60:.1f} minutes de calcul au total, "
            f"{secondes / max(1, len(fiches)) / 60:.1f} min par papier\n"
        )
        for fiche_id, t in sorted(fiches.items()):
            marque = {"vert": "VERT  ", "epuise": "EPUISE", "contexte_depasse": "CTX   "}.get(
                t["verdict"], "?     "
            )
            casses = sorted({c for e in t["essais"] for c in e.get("conditions_cassees", [])})
            detail = f"  cassees : {', '.join(casses)}" if casses else ""
            print(
                f"  {marque} {len(t['essais'])} essai(s)  "
                f"{t['consigne_chars'] / 1000:>4.0f} ko  {fiche_id[:44]}{detail}"
            )
        print()

    print("CE QUE CE BANC NE DIT PAS : que la fiche soit BONNE. Il dit qu'elle")
    print("passe les cinq conditions de D16 — la pertinence n'a toujours pas de")
    print("denominateur (D16 § Pourquoi).")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Banc d'essai — extracteur local")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--machine", action="store_true")
    ap.add_argument("--run", metavar="FICHE_ID")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    a = ap.parse_args(argv)

    if a.machine:
        return do_machine()
    if a.list:
        return do_list()
    if a.run:
        return do_run(a.run, a.model)
    if a.report:
        return do_report()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
