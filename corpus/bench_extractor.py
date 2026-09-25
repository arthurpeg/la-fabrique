"""Le banc d'essai des extracteurs de rechange — la question posée le 2026-09-24.

Le projet fait tourner **un seul modèle en local** : `BAAI/bge-base-en-v1.5`
via `fastembed`, pour les embeddings (`vectordb/embed.py`). Les trois étapes de
raisonnement — trieur (`D15`), extracteur (`D16`), codeur (`D23`) — ont toujours
été des sessions d'un modèle de frontière, et personne ne l'avait écrit ni
chiffré. Ce banc chiffre ce qu'un **autre** extracteur ferait à leur place.

**Deux backends, une seule boucle.** `ollama` en local, et l'API Gemini. Le
choix se lit dans le nom du modèle (`gemini-…` bascule l'un, tout le reste
l'autre) ; la boucle de reprise, le juge et le registre sont **identiques**.
Deux implémentations d'une même règle divergent toujours — c'est ce qui est
arrivé à `value_in_quote`, tenue en double jusqu'au 2026-09-22.

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
`corpus/bench/<modele>/`. Une fiche d'essai dans la population réelle la
polluerait, et c'est la même faute que celle évitée entre `corpus/fiches/` et
`corpus/fiches_harvest/` : la séparation vit dans le stockage, pas dans la prose.

**Le contexte est fixé explicitement, et c'est la précaution qui compte.**
`ollama` tronque SILENCIEUSEMENT une invite plus longue que `num_ctx`. Un modèle
qui n'aurait vu que la moitié du papier échouerait `F2` pour une raison qui n'est
pas la sienne, et on conclurait faux. Le banc fixe `num_ctx`, mesure
`prompt_eval_count`, et **refuse de juger une sortie dont l'invite a été
tronquée** — le cas est inscrit `contexte_depasse`, jamais confondu avec un échec
de fidélité.

    python corpus/bench_extractor.py --machine   # CETTE machine vs la reference
    python corpus/bench_extractor.py --modeles   # les modeles Gemini de ta cle
    python corpus/bench_extractor.py --list
    python corpus/bench_extractor.py --run <fiche_id> [--model gemini-2.5-flash]
    python corpus/bench_extractor.py --report

Code de sortie 1 si `ollama` ne répond pas, ou si aucun essai n'aboutit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONSIGNES = REPO / "corpus" / "consignes_harvest"
BENCH = REPO / "corpus" / "bench"
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

# LE CONFONDANT DU PASSAGE DU 2026-09-24, ET IL EST INSCRIT PLUTOT QUE TU.
# Qwen3-4B a ete declare en echec « sur la FORME » : aucun de ses trois essais
# n'a rendu un objet JSON lisible. Mais il n'avait PAS recu `format: "json"`,
# que `ollama` offre et qui contraint la sortie — alors que le backend Gemini
# recoit `responseMimeType: application/json`. Comparer les deux ainsi
# mesurerait la PILE autant que le modele.
#
# La capacite est donc ajoutee ici, et le drapeau est inscrit dans chaque trace.
# Tant que le passage `ollama` n'a pas ete rejoue avec, la conclusion de `F56`
# tient sur ce poste — le modele n'a jamais fini un papier sur cinq — mais son
# ATTRIBUTION a la forme reste a verifier. C'est `L18` : chercher si la cause
# n'est pas ailleurs avant de nommer le coupable.
FORMAT_JSON_OLLAMA = True


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


# ---------------------------------------------------------------------------
# VARIANTE « lignes » — changer la TACHE plutot que le modele.
#
# Constat du 2026-09-24 : `gemini-2.5-flash` rend du JSON parfait mais echoue
# `F2` sur 4 papiers sur 5. `F2` exige de RECOPIER mot pour mot depuis 20 000
# tokens, et c'est exactement ce qu'un modele faible fait le plus mal : il
# paraphrase. Le seuil n'est pas negociable ; l'INTERFACE, si.
#
# Ici le texte est numerote et le modele ne recopie rien : il designe un
# INTERVALLE DE LIGNES, que le harnais resout lui-meme.
#
# CE QUE CELA CHANGE, ET IL FAUT LE LIRE AVANT DE COMPARER LES CHIFFRES.
# `F2` devient VRAI PAR CONSTRUCTION — la citation est extraite du fichier, elle
# ne peut plus etre fabriquee. Ce n'est pas un affaiblissement : c'est le geste
# de l'invariant II, « empeche par construction, jamais par vigilance ». Mais un
# « vert » sous cette variante ne se compare PAS a un « vert » sous le contrat
# courant, et le banc l'inscrit dans chaque trace.
#
# LE RISQUE SE DEPLACE, IL NE DISPARAIT PAS : le modele peut pointer les
# MAUVAISES lignes. C'est `F3` qui l'attrape — la valeur annoncee doit se
# retrouver dans les lignes resolues — et `F3` devient donc la condition
# porteuse de la variante. Elle, elle peut echouer.
VARIANTES = ("citation", "lignes")

REGLE_LIGNES = """\
1. **Tu ne recopies AUCUNE citation.** Le texte du papier t'est donné avec un
   NUMÉRO DE LIGNE en tête de chaque ligne. Pour chaque citation, tu donnes
   `"quoted_lines"` à la place de `"quoted"` : l'intervalle de lignes qui
   contient ce que tu cites, bornes incluses.
   - dans `reported_results`, un seul intervalle : `"quoted_lines": [1234, 1236]`
   - dans `claim`, `universe`, `horizon`, `signal_construction`, une LISTE
     d'intervalles : `"quoted_lines": [[12, 14], [98, 98]]`
   Le harnais ira chercher le texte lui-même, à l'octet près. Ne mets jamais de
   champ `quoted` : il sera écrasé.
2. **Choisis l'intervalle le plus COURT qui porte ce que tu cites**, et pour un
   résultat chiffré, **l'intervalle DOIT contenir le nombre**. Un contrôle
   mécanique vérifie que la valeur annoncée se trouve dans les lignes que tu as
   désignées : pointer à côté fait rejeter la fiche."""


def numeroter(texte: str) -> str:
    return "\n".join(f"{i:>5}| {ligne}" for i, ligne in enumerate(texte.splitlines(), 1))


def consigne_lignes(fiche_id: str) -> str:
    """Bâtit la consigne de la variante depuis les MEMES sources que l'originale.

    Le schéma et le texte sont ceux de `extract_fiche_harvest.py --prepare` ;
    seules les deux premières règles changent. Rien n'est recopié à la main.
    """
    originale = (CONSIGNES / f"{fiche_id}.md").read_text(encoding="utf-8")
    tete, _, texte = originale.partition("## TEXTE DU PAPIER\n")
    if not texte:
        raise SystemExit(f"consigne illisible : {fiche_id}")

    # Les deux premieres regles de la consigne d'origine sont remplacees ; le
    # reste — schema, interdits, identite de la fiche — est conserve tel quel.
    debut = tete.find("1. **Chaque citation")
    fin = tete.find("3. **Si le texte fourni est visiblement abîmé**")
    if debut < 0 or fin < 0:
        raise SystemExit("les regles 1 et 2 n'ont pas ete retrouvees dans la consigne")
    tete = tete[:debut] + REGLE_LIGNES + "\n" + tete[fin:]
    return tete + "## TEXTE DU PAPIER (numéroté)\n\n" + numeroter(texte.lstrip("\n"))


def _resoudre(paires, lignes: list[str]):
    """Un intervalle (ou une liste d'intervalles) -> le texte exact du fichier."""
    def une(paire):
        a, b = int(paire[0]), int(paire[1])
        if a < 1 or b < a or b > len(lignes):
            raise ValueError(f"intervalle hors texte : [{a}, {b}] pour {len(lignes)} lignes")
        return "\n".join(lignes[a - 1 : b])

    if not isinstance(paires, list) or not paires:
        raise ValueError(f"quoted_lines illisible : {paires!r}")
    if isinstance(paires[0], (int, float, str)):
        return une(paires)
    return [une(p) for p in paires]


def resoudre_lignes(objet: dict, fiche_id: str) -> list[str]:
    """Remplace tout `quoted_lines` par le `quoted` qu'il designe. Rend les fautes.

    Les fautes ne sont PAS corrigees en silence : un intervalle hors texte laisse
    le champ sans `quoted`, et le juge le refusera — ce qui est le comportement
    voulu. Un resolveur indulgent masquerait precisement ce qu'on mesure.
    """
    texte = (REPO / "corpus" / "text" / f"{fiche_id}.default.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    lignes = texte.splitlines()
    fautes: list[str] = []

    def traiter(noeud, ou: str):
        if isinstance(noeud, dict):
            if "quoted_lines" in noeud:
                try:
                    resolu = _resoudre(noeud.pop("quoted_lines"), lignes)
                    # LA FORME DU CHAMP SUIT LE CONTRAT EXISTANT, pas l'inverse.
                    # `reported_results[].quoted` est une CHAINE dans toutes les
                    # fiches du corpus, et `check_f3` l'appelle `.replace()` :
                    # une liste y fait PLANTER le juge — constate le 2026-09-25,
                    # `AttributeError: 'list' object has no attribute 'replace'`.
                    # La variante change l'interface d'ENTREE du modele ; elle ne
                    # touche pas au schema de sortie, et surtout pas au juge.
                    if "reported_results" in ou and isinstance(resolu, list):
                        resolu = "\n".join(resolu)
                    noeud["quoted"] = resolu
                except ValueError as e:
                    fautes.append(f"{ou} : {e}")
            for cle, valeur in noeud.items():
                traiter(valeur, f"{ou}.{cle}")
        elif isinstance(noeud, list):
            for i, element in enumerate(noeud):
                traiter(element, f"{ou}[{i}]")

    traiter(objet, "fiche")
    return fautes


def charger_env() -> None:
    """Lit `.env` sans ecraser ce que l'environnement porte deja.

    Ecrit ici plutot qu'importe de `vectordb/vector_db.py` : ce module tire
    `psycopg` a l'import, et ce banc n'a aucune raison d'exiger une base.
    """
    fichier = REPO / ".env"
    if not fichier.is_file():
        return
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, _, valeur = ligne.partition("=")
        os.environ.setdefault(cle.strip(), valeur.strip())


def cle_gemini() -> str | None:
    charger_env()
    for nom in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(nom, "").strip():
            return os.environ[nom].strip()
    return None


def appel_gemini(model: str, messages: list[dict], num_ctx: int) -> dict:
    """Un appel a l'API Gemini, normalise dans la forme que rend `appel()`.

    **La cle voyage dans un EN-TETE, jamais dans l'URL.** Une cle en parametre
    de requete se retrouve dans les journaux de serveur, les historiques et les
    traces d'erreur ; c'est une fuite gratuite.

    `num_ctx` est ignore — l'API n'en prend pas — mais il reste dans la trace
    pour que les deux backends se lisent dans la meme colonne.
    """
    cle = cle_gemini()
    if cle is None:
        raise SystemExit(
            "GEMINI_API_KEY absente. La deposer dans `.env` (jamais dans le code, "
            "jamais dans une URL) : voir `.env.example`."
        )

    contents = [
        {"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
        for m in messages
    ]
    body = json.dumps(
        {
            "contents": contents,
            "generationConfig": {
                "temperature": 0,
                # Le JSON force est la configuration SAINE en production. Elle
                # introduit en revanche un CONFONDANT avec le passage `ollama` du
                # 2026-09-24, qui ne l'avait pas : voir `FORMAT_JSON_OLLAMA`.
                "responseMimeType": "application/json",
            },
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=body,
        headers={"Content-Type": "application/json", "x-goog-api-key": cle},
    )
    debut = time.time()
    with urllib.request.urlopen(req, timeout=TIMEOUT_APPEL_S) as r:
        payload = json.loads(r.read().decode("utf-8"))

    candidats = payload.get("candidates") or []
    parts = candidats[0].get("content", {}).get("parts", []) if candidats else []
    texte = "".join(p.get("text", "") for p in parts)
    usage = payload.get("usageMetadata") or {}
    return {
        "message": {"content": texte},
        "prompt_eval_count": usage.get("promptTokenCount", 0),
        "eval_count": usage.get("candidatesTokenCount", 0),
        "_wall_s": round(time.time() - debut, 1),
        "_finish_reason": candidats[0].get("finishReason") if candidats else None,
    }


def est_gemini(model: str) -> bool:
    return model.startswith("gemini")


def do_modeles() -> int:
    """Liste les modeles que CETTE cle peut reellement appeler.

    Ecrit parce qu'un nom de modele se DEMANDE a l'API, il ne se devine pas :
    les identifiants du palier gratuit changent et se deprecient sur calendrier.
    Un nom recopie de memoire est un nom qui sera faux un jour.
    """
    cle = cle_gemini()
    if cle is None:
        print("GEMINI_API_KEY absente — ajouter la ligne suivante dans `.env` :")
        print("\n    GEMINI_API_KEY=AIza...\n")
        print("Sans guillemets, sans espace autour du `=`. Voir `.env.example`.")
        return 1

    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models",
        headers={"x-goog-api-key": cle},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"l'API refuse : HTTP {e.code} — {e.read().decode('utf-8', 'replace')[:300]}")
        return 1

    modeles = [
        m
        for m in payload.get("models", [])
        if "generateContent" in (m.get("supportedGenerationMethods") or [])
    ]
    print(f"{len(modeles)} modele(s) appelables par cette cle :\n")
    for m in sorted(modeles, key=lambda x: x["name"]):
        nom = m["name"].removeprefix("models/")
        entree = m.get("inputTokenLimit", 0)
        marque = "  <-- tient nos consignes" if entree >= 45000 else ""
        print(f"  {nom:<44} entree {entree:>9,} tok{marque}".replace(",", " "))
    print("\nLa plus grosse consigne du lot fait ~39K tokens : tout modele au-dessus")
    print("de 45 000 la tient sans troncature.")
    return 0


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
            "format": "json" if FORMAT_JSON_OLLAMA else None,
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
            capture_output=True,
            text=True,
            timeout=20,
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
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
                ],
                capture_output=True,
                text=True,
                timeout=30,
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
    print(f"  VRAM : {_go(vram)} contre {_go(REFERENCE['vram_go'])} — {ecart:.1f}x la reference")
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


def do_run(fiche_id: str, model: str, variante: str = "citation") -> int:
    consigne = CONSIGNES / f"{fiche_id}.md"
    if not consigne.is_file():
        raise SystemExit(f"consigne absente : {consigne}")
    if est_gemini(model):
        if cle_gemini() is None:
            raise SystemExit(
                "GEMINI_API_KEY absente de l'environnement et de `.env` — voir `.env.example`."
            )
    elif not ollama_disponible():
        raise SystemExit("ollama ne repond pas sur localhost:11434")

    etiquette = model.replace(":", "_") + ("" if variante == "citation" else f"+{variante}")
    sortie_dir = BENCH / etiquette
    sortie_dir.mkdir(parents=True, exist_ok=True)
    cible = sortie_dir / f"{fiche_id}.json"

    texte_consigne = (
        consigne.read_text(encoding="utf-8") if variante == "citation"
        else consigne_lignes(fiche_id)
    )
    num_ctx = contexte_pour(len(texte_consigne))
    messages = [{"role": "user", "content": texte_consigne}]

    resultats = charger_resultats()
    trace = {
        "model": model,
        "backend": "gemini" if est_gemini(model) else "ollama",
        "format_json_force": True if est_gemini(model) else FORMAT_JSON_OLLAMA,
        "variante": variante,
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
            rep = (appel_gemini if est_gemini(model) else appel)(model, messages, num_ctx)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ligne = {
                "essai": essai,
                "issue": "expire" if isinstance(e, TimeoutError) else "reseau",
                "detail": f"{type(e).__name__}: {e}",
                "timeout_s": TIMEOUT_APPEL_S,
            }
            trace["essais"].append(ligne)
            trace["verdict"] = ligne["issue"]
            # NE PAS annoncer le plafond quand ce n'est PAS lui qui a coupe : un
            # `404` affiche « apres 2700s » laisserait croire a une lenteur la
            # ou il y a un refus immediat, et on chercherait au mauvais endroit.
            quand = f" apres {TIMEOUT_APPEL_S}s" if isinstance(e, TimeoutError) else ""
            print(f"    {ligne['issue'].upper()} — {type(e).__name__}{quand}. INSCRIT, pas perdu.")
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
        #
        # ELLE N'A PAS LE MEME VISAGE SELON LE BACKEND, et les confondre fait
        # crier le garde pour une non-raison — ce qui est pire qu'un garde
        # absent (`L12`). Mesure du 2026-09-24 : applique a Gemini, ce test a
        # refuse de juger une reponse JAMAIS tronquee, `num_ctx` n'etant qu'une
        # notion d'`ollama` quand l'API porte un contexte d'un million.
        #
        #   ollama : l'invite au-dela de `num_ctx` est rabotee EN SILENCE ;
        #   Gemini : l'invite passe, mais la SORTIE peut etre coupee, et l'API
        #            le dit — `finishReason == "MAX_TOKENS"`.
        if est_gemini(model):
            tronque = rep.get("_finish_reason") == "MAX_TOKENS"
            motif = "la sortie a ete coupee (finishReason=MAX_TOKENS)"
        else:
            tronque = prompt_tokens >= num_ctx - 64
            motif = f"l'invite a ete tronquee a num_ctx={num_ctx}"
        if tronque:
            ligne["issue"] = "contexte_depasse"
            trace["essais"].append(ligne)
            trace["verdict"] = "contexte_depasse"
            print(f"    CONTEXTE DEPASSE — {prompt_tokens} tokens d'invite. Non juge : {motif}.")
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

        if variante == "lignes":
            fautes = resoudre_lignes(objet, fiche_id)
            ligne["intervalles_fautifs"] = fautes
            ligne["quoted_lines_restants"] = json.dumps(objet).count("quoted_lines")
            if fautes:
                print(f"    {len(fautes)} intervalle(s) hors texte — champ laisse SANS")
                print("      citation, le juge le refusera. Non corrige en silence.")
            if ligne["quoted_lines_restants"]:
                print(f"    {ligne['quoted_lines_restants']} `quoted_lines` NON RESOLUS "
                      "— le resolveur ne les a pas vus.")

        cible.write_text(json.dumps(objet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        vert, verdict = juger(cible)
        ligne["conditions_cassees"] = conditions_cassees(verdict)
        ligne["vert"] = vert
        # UN JUGE QUI PLANTE N'EST PAS UN JUGE QUI REFUSE, et les confondre
        # ecrit « aucune condition cassee » sous un rejet. Constate le
        # 2026-09-25 : `check_f3` leve `AttributeError` sur un `quoted` de type
        # liste, donc `conditions_cassees` rend [] alors que rien n'est vert.
        if not vert and not ligne["conditions_cassees"]:
            ligne["juge_plante"] = verdict.strip().splitlines()[-1][:200] if verdict else "?"
            print(f"    LE JUGE A PLANTE — {ligne['juge_plante']}")
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

    resultats.setdefault(etiquette, {})[fiche_id] = trace
    ecrire_resultats(resultats)
    return 0 if trace["verdict"] == "vert" else 1


def do_report() -> int:
    res = charger_resultats()
    if not res:
        raise SystemExit("aucun resultat — lancer `--run` d'abord")

    print("BANC D'ESSAI DES EXTRACTEURS DE RECHANGE\n")
    print("Reference mesuree (modele de frontiere, corpus/PRODUCED_harvest.json) :")
    print("  6 fiches, 8 essais, 1,33 essai par fiche, 6 vertes sur 6\n")

    for model, fiches in sorted(res.items()):
        verts = [f for f, t in fiches.items() if t["verdict"] == "vert"]
        essais_verts = sum(len(fiches[f]["essais"]) for f in verts)
        secondes = sum(e.get("wall_s", 0) for t in fiches.values() for e in t["essais"])
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
    ap.add_argument(
        "--modeles", action="store_true", help="les modeles Gemini appelables par la cle de .env"
    )
    ap.add_argument("--run", metavar="FICHE_ID")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--variante", default="citation", choices=VARIANTES,
                    help="`lignes` : le modele designe des numeros de ligne au lieu de recopier")
    a = ap.parse_args(argv)

    if a.modeles:
        return do_modeles()
    if a.machine:
        return do_machine()
    if a.list:
        return do_list()
    if a.run:
        return do_run(a.run, a.model, a.variante)
    if a.report:
        return do_report()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
