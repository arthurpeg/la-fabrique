"""Le superviseur de la moisson : il enchaine, mesure, et relance seul.

Chaine : rechercher les axes -> sonder les PDF -> telecharger -> verser dans la
base (pertinents seulement, `D33`, sous le budget de `D32`). PAS d'embeddings :
ils viennent apres, a part (`python vectordb/embed.py`).

**Chaque etape reprend la ou elle s'est arretee** — c'est ce qui rend la
relance sans danger : la recherche dedoublonne, la sonde ne reprend que les non
sondes, le telechargement saute les PDF presents, le versement saute les
papiers deja en base. Une etape FINIE n'est pas refaite (`state.json`).

**Ce qu'il appelle un plantage** : un code de sortie inattendu, une exception,
ou AUCUNE ligne produite pendant `STALL_SECONDS` (processus bloque). Il relance
alors l'etape, avec une attente croissante, jusqu'a `MAX_ATTEMPTS` fois.

**Le temps restant** est tire de la sortie meme des etapes : toute ligne
portant `i/N` donne l'avancement, d'ou une vitesse et une estimation.

    python scripts/pipeline_runner.py --run      # lance ou reprend la chaine
    python scripts/pipeline_runner.py --status   # ou en est-on, et pour combien de temps
    python scripts/pipeline_runner.py --reset    # oublie les etapes finies
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORK = REPO / ".pipeline"
STATE = WORK / "state.json"
STATUS = WORK / "status.json"
PY = [sys.executable]

MAX_ATTEMPTS = 12
STALL_SECONDS = 20 * 60
BACKOFF = [60, 120, 300, 600, 900, 1800, 1800, 1800, 1800, 1800, 1800, 1800]

# (nom, commande, codes de sortie acceptes). `--fetch` rend 1 quand un fichier
# annonce n'etait pas un PDF : c'est un refus juste, pas un plantage.
STAGES: list[tuple[str, list[str], set[int]]] = [
    # Passage 6 (`D20` § Journal) : les 79 axes OpenAlex, plafond 200. Pas les
    # axes `ssrn:*`, dont Crossref ne rend que des notices (`D30`, `D31`).
    #
    # L'ORDRE, revu le 2026-09-30 : OpenAlex facture desormais ses requetes
    # (`cost_usd` dans chaque reponse) et refuse l'anonyme une fois son credit
    # du jour epuise — la recherche intraday a ete refusee plus de trois heures.
    # La sonde, elle, ne l'interroge pas (liens deja inscrits, NBER, CORE,
    # pages de depot). On sonde donc ce qui est deja trouve AVANT de relancer
    # les recherches restantes : un refus d'OpenAlex ne bloque plus le reste.
    *[(f"recherche {g}", [*PY, "corpus/harvest.py", "--search", "--axis", g], {0})
      for g in ("family", "asset", "method", "anomaly", "strategy", "hypothesis")],
    ("sonde", [*PY, "corpus/harvest.py", "--probe", "--sans-ssrn"], {0}),
    ("telechargement", [*PY, "corpus/harvest.py", "--fetch"], {0, 1}),
    ("versement", [*PY, "vectordb/ingest.py", "--harvest"], {0}),
    *[(f"recherche {g}", [*PY, "corpus/harvest.py", "--search", "--axis", g], {0})
      for g in ("intraday", "instrument", "causality", "mechanism")],
    ("sonde (2)", [*PY, "corpus/harvest.py", "--probe", "--sans-ssrn"], {0}),
    ("telechargement (2)", [*PY, "corpus/harvest.py", "--fetch"], {0, 1}),
    ("versement (2)", [*PY, "vectordb/ingest.py", "--harvest"], {0}),
]

PROGRESS = re.compile(r"(\d+)\s*/\s*(\d+)")


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save(path: Path, data) -> None:
    WORK.mkdir(exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def fmt(seconds: float | None) -> str:
    if seconds is None:
        return "inconnu"
    h, rem = divmod(int(seconds), 3600)
    return f"{h} h {rem // 60:02d} min" if h else f"{rem // 60} min {rem % 60:02d} s"


def run_stage(name: str, cmd: list[str], ok: set[int], attempt: int, status: dict) -> int:
    """Lance une etape, lit sa sortie, tient le statut a jour. Rend le code de sortie."""
    log = WORK / f"{re.sub(r'[^a-z0-9]+', '-', name)}.log"
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    proc = subprocess.Popen(cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", env=env)
    started = time.time()
    last_out = [time.time()]
    first_seen: dict[str, float] = {}

    def watchdog() -> None:
        while proc.poll() is None:
            if time.time() - last_out[0] > STALL_SECONDS:
                status["events"].append(f"{now()} {name} : aucune sortie depuis "
                                        f"{STALL_SECONDS // 60} min — arrete, sera relance")
                proc.kill()
                return
            time.sleep(15)

    threading.Thread(target=watchdog, daemon=True).start()
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"\n===== {now()} tentative {attempt} : {' '.join(cmd)}\n")
        for line in proc.stdout:
            fh.write(line)
            fh.flush()
            last_out[0] = time.time()
            # « pause 10 s (1/5) » est un compteur de reprises, pas un avancement.
            m = None if "pause" in line else PROGRESS.search(line)
            cur = status["current"]
            cur["last_line"] = line.strip()[:160]
            if m and int(m.group(2)) >= int(m.group(1)) and int(m.group(2)) > 0:
                i, n = int(m.group(1)), int(m.group(2))
                key = str(n)
                first_seen.setdefault(key, time.time() - 1)
                rate = i / max(time.time() - first_seen[key], 1)
                cur.update({"done": i, "total": n, "rate_per_min": round(rate * 60, 1),
                            "eta_seconds": round((n - i) / rate) if rate > 0 else None})
            cur["elapsed_seconds"] = round(time.time() - started)
            cur["updated"] = now()
            save(STATUS, status)
    code = proc.wait()
    return code


def run() -> int:
    # Le PC en veille tuait le superviseur (code 4) : il le garde éveillé tant
    # qu'il travaille, et rend la veille au système en sortant.
    sys.path.insert(0, str(REPO / "scripts"))
    from anti_veille import eveille  # noqa: PLC0415

    with eveille():
        return _run()


def _run() -> int:
    state = load(STATE, {"done": []})
    status = {"started": now(), "pid": os.getpid(), "events": [], "current": {},
              "stages": [s[0] for s in STAGES], "done": state["done"]}
    save(STATUS, status)
    for name, cmd, ok in STAGES:
        if name in state["done"]:
            continue
        for attempt in range(1, MAX_ATTEMPTS + 1):
            status["current"] = {"stage": name, "attempt": attempt, "started": now()}
            save(STATUS, status)
            try:
                code = run_stage(name, cmd, ok, attempt, status)
            except Exception as e:  # noqa: BLE001 — le superviseur ne doit pas tomber
                code = -1
                status["events"].append(f"{now()} {name} : exception {type(e).__name__}: {e}")
            if code in ok:
                state["done"].append(name)
                save(STATE, state)
                status["done"] = state["done"]
                status["events"].append(f"{now()} {name} : terminee (code {code})")
                save(STATUS, status)
                break
            wait = BACKOFF[min(attempt - 1, len(BACKOFF) - 1)]
            status["events"].append(f"{now()} {name} : ECHEC code {code}, tentative "
                                    f"{attempt}/{MAX_ATTEMPTS}, relance dans {wait} s")
            save(STATUS, status)
            if attempt == MAX_ATTEMPTS:
                status["events"].append(f"{now()} {name} : ABANDON apres {MAX_ATTEMPTS} "
                                        "tentatives — intervention requise")
                status["current"]["failed"] = True
                save(STATUS, status)
                return 1
            time.sleep(wait)
    status["finished"] = now()
    status["current"] = {}
    save(STATUS, status)
    return 0


def show() -> int:
    st = load(STATUS, None)
    if not st:
        print("aucune execution enregistree")
        return 1
    cur = st.get("current") or {}
    age = None
    if cur.get("updated"):
        age = (datetime.now(UTC) - datetime.fromisoformat(cur["updated"])).total_seconds()
    print(f"lance le {st['started']} (pid {st['pid']})")
    print(f"etapes finies : {len(st.get('done', []))}/{len(st['stages'])} — "
          f"{', '.join(st.get('done', [])) or 'aucune'}")
    if st.get("finished"):
        print(f"TERMINE le {st['finished']}")
    elif cur:
        print(f"en cours : {cur.get('stage')} (tentative {cur.get('attempt')})")
        if cur.get("total"):
            print(f"  avancement {cur['done']}/{cur['total']}, {cur.get('rate_per_min')} /min, "
                  f"reste ~{fmt(cur.get('eta_seconds'))} pour cette etape")
        print(f"  derniere ligne : {cur.get('last_line', '')}")
        if age is not None and age > STALL_SECONDS:
            print(f"  ATTENTION : aucune nouvelle depuis {fmt(age)} — le superviseur "
                  "est peut-etre arrete")
    for ev in st.get("events", [])[-8:]:
        print(f"  · {ev}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Superviseur de la moisson")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--reset", action="store_true")
    a = ap.parse_args(argv)
    if a.reset:
        save(STATE, {"done": []})
        print("etapes oubliees")
        return 0
    if a.status:
        return show()
    if a.run:
        return run()
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
