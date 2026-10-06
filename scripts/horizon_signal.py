"""L'horizon auquel un signal se juge et se compare — `D49`.

Avant `D49`, le juge (`score_signal.py`) et le double codage (supprimé depuis
par `D54`) appelaient tous les signaux à `horizon_bars = 30`, quelle
que soit la fiche, pendant que la mesure (`measure_lot.py`) les appelle à
l'horizon de leur hypothèse. Un signal concordant à 30 barres ne l'est pas
forcément à 15 minutes ou à la clôture.

L'horizon se lit, dans cet ordre :

1. **l'hypothèse** : l'horizon que le lot a recopié de sa section « Le
   domaine » (`D42`) — c'est celui de la mesure, il fait foi ;
2. **la fiche** : son champ `horizon`, s'il dit un horizon intraday lisible
   (minutes, heures, demi-heure, jusqu'à la clôture) ;
3. **l'ancrage par défaut** de `signals/_common.run`, 30 barres, quand ni l'une
   ni l'autre ne disent un horizon intraday.

« Jusqu'à la clôture » n'est pas un nombre de barres : le signal se pose alors
à l'ancrage par défaut, exactement comme `measure_lot.py` le fait (`D43`).

La source est toujours rendue avec le nombre : un horizon mal lu dans le texte
libre d'une fiche se voit.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from harness import horizon_to_bars  # noqa: E402

LOT = REPO / "hypotheses" / "LOT-09.json"
DOSSIERS_FICHES = (REPO / "corpus" / "fiches", REPO / "corpus" / "fiches_harvest",
                   REPO / "corpus" / "fiches_synthese")

# L'ancrage par défaut de `signals/_common.run` et de `measure_lot.py`.
ANCRAGE_PAR_DEFAUT = 30


def horizon_du_lot(fiche_id: str) -> tuple[str | None, str | None]:
    """L'horizon (« 15min », « 2h », « cloture ») et la `ref` de l'hypothèse, si le lot
    les porte."""
    if not LOT.is_file():
        return None, None
    lot = json.loads(LOT.read_text(encoding="utf-8"))
    for e in lot.get("fiches") or []:
        if fiche_id in (e.get("fiche_id"), e.get("signal_id")) and e.get("horizon"):
            return str(e["horizon"]), e.get("ref")
    return None, None


def lire_horizon_intraday(valeur, unite: str | None = None) -> str | None:
    """Un horizon intraday lisible dans le champ `horizon` d'une fiche, ou None."""
    if valeur is None:
        return None
    unite = (unite or "").lower()
    if isinstance(valeur, (int, float)) and not isinstance(valeur, bool):
        if "minute" in unite:
            return f"{int(valeur)}min"
        if "heure" in unite:
            return f"{int(valeur)}h"
        return None
    texte = " ".join(str(valeur).split()).lower()
    # La PREMIÈRE mention fait foi : « Une heure. [...] mesuré sur 15:15-16:15 [...]
    # 10 heures » est un horizon d'une heure (vu sur boyarchenko-2023, lu 10 h
    # quand les motifs étaient essayés l'un après l'autre).
    candidats: list[tuple[int, str]] = []
    m = re.search(r"(?:à|a|jusqu.?à|jusqu.?a)\s+la\s+cl[ôo]ture", texte)
    if m:
        candidats.append((m.start(), "cloture"))
    m = re.search(r"demi-heure", texte)
    if m:
        candidats.append((m.start(), "30min"))
    m = re.search(r"(\d+)\s*(?:minutes?|min\b)", texte)
    if m:
        candidats.append((m.start(), f"{int(m.group(1))}min"))
    m = re.search(r"(\d+)\s*(?:heures?|h\b)", texte)
    if m:
        candidats.append((m.start(), f"{int(m.group(1))}h"))
    m = re.search(r"\bune heure\b", texte)
    if m:
        candidats.append((m.start(), "1h"))
    return min(candidats)[1] if candidats else None


def fiche_de(fiche_id: str) -> dict | None:
    for d in DOSSIERS_FICHES:
        f = d / f"{fiche_id}.json"
        if f.is_file():
            return json.loads(f.read_text(encoding="utf-8"))
    return None


def horizon_du_signal(fiche_id: str) -> tuple[int, str]:
    """Le nombre de barres à passer à `scores(..., horizon_bars=...)`, et d'où il vient."""
    h, ref = horizon_du_lot(fiche_id)
    if h:
        return (horizon_to_bars(h) or ANCRAGE_PAR_DEFAUT,
                f"hypothèse {ref or '?'} : « {h} »")
    fiche = fiche_de(fiche_id) or {}
    champ = fiche.get("horizon")
    if isinstance(champ, dict):
        h = lire_horizon_intraday(champ.get("value"), champ.get("unit"))
    else:
        h = lire_horizon_intraday(champ)
    if h:
        return (horizon_to_bars(h) or ANCRAGE_PAR_DEFAUT, f"fiche : « {h} »")
    return (ANCRAGE_PAR_DEFAUT,
            "ancrage par défaut : ni hypothèse ni horizon intraday lisible dans la fiche")


if __name__ == "__main__":
    for fid in sys.argv[1:]:
        barres, source = horizon_du_signal(fid)
        print(f"{fid} : {barres} barres ({source})")
