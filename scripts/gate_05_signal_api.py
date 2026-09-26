"""PORTE 05 — le contrat de signal, la sandbox, et le test de causalité.

La porte, telle que `ETAT.md` la pose : on injecte volontairement un look-ahead
dans un signal, et **le test l'attrape**. C'est la seule clause qui compte ici.
Les trois autres sections préparent le terrain ; celle-là décide.

    python scripts/gate_05_signal_api.py

Quatre tricheurs sont soumis au test (`sandbox/tainted.py`), et chacun doit être
attrapé pour une raison qu'on écrit d'avance : le premier et le quatrième parce
que leurs scores disparaissent quand on leur retire le futur, les deux autres
parce qu'ils changent de valeur. Le quatrième ne lit qu'UNE barre de trop, et il
doit tomber à CHAQUE sonde : c'est lui qui mesure la résolution du test (`D27`),
et un trou de cotation ne doit pas pouvoir faire le travail à sa place.
Un tricheur attrapé « pour une autre raison que prévu » est un test qu'on ne
comprend pas, donc une porte non franchie.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from panel import Panel  # noqa: E402
from sandbox import causality, contract, scan, signature  # noqa: E402
from sandbox.tainted import TAINTED  # noqa: E402
from signals import REFERENCE  # noqa: E402

ASOF = "2018-06-15 20:00"
PROBES = 16

# Écrit AVANT de lancer le test : pourquoi chaque tricheur doit tomber.
EXPECTED_CATCH = {
    "tainted-forward-return": "disparu",
    "tainted-full-sample-zscore": "valeur",
    "tainted-window-close": "valeur",
    "tainted-next-bar": "disparu",
}

# Ceux-là doivent tomber à CHAQUE sonde, pas seulement à une (D27). Avant D27,
# `tainted-next-bar` tombait à 2 sondes sur 16, par accident de cotation.
CAUGHT_AT_EVERY_PROBE = {"tainted-next-bar"}

REFUSED_SOURCES = {
    "le réseau": "import requests\n",
    "le système de fichiers": "def scores(p):\n    open('/etc/passwd')\n",
    "un décalage négatif": "import pandas as pd\n\n\ndef scores(p):\n    return p.shift(-30)\n",
    "l'évasion par dunder": "def scores(p):\n    return scores.__globals__\n",
    "le code depuis une chaîne": "def scores(p):\n    return eval('1 + 1')\n",
}


class NotASignal:
    """Ce qu'un module de signal ne doit pas pouvoir être."""

    SIGNAL_ID = ""
    EXPECTED_SIGN = 0


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    panel = Panel.open(asof=ASOF, slice="pool")
    print(f"panel au {panel.asof}, tranche {panel.slice.name}, "
          f"{len(panel.cells())} cellules\n")

    # -- 1. le contrat -------------------------------------------------------
    print("1. le contrat : ce qu'un signal doit exposer, et ce qu'il doit rendre")
    produced = {}
    for signal_id, module in REFERENCE.items():
        bad = contract.validate_module(module)
        check(not bad, f"{signal_id} ne satisfait pas le contrat : {bad}")
        scores = module.scores(panel)
        produced[signal_id] = scores
        bad = contract.validate_scores(scores, panel)
        check(not bad, f"{signal_id} : sortie hors contrat : {bad[:3]}")

    refused = contract.validate_module(NotASignal)
    check(len(refused) >= 3,
          f"un module sans PAPER, au SIGNAL_ID vide et au signe 0 n'est refusé que "
          f"pour {len(refused)} raison(s) : {refused}")
    bad_shapes = contract.validate_scores({("ZZ", "US"): pd.Series([1.0])}, panel)
    check(bad_shapes, "une cellule inexistante avec un index entier passe le contrat")
    print(f"   {len(REFERENCE)} étalons conformes ; un faux module refusé pour "
          f"{len(refused)} raisons, une sortie malformée pour {len(bad_shapes)}")

    # -- 2. la liste blanche -------------------------------------------------
    print("2. la liste blanche : ce qu'un signal a le droit d'importer et d'appeler")
    for signal_id, module in REFERENCE.items():
        bad = scan.scan_module(module)
        check(not bad, f"{signal_id} est refusé par son propre scan : {bad}")
    for what, source in REFUSED_SOURCES.items():
        bad = scan.scan_source(source, f"<{what}>")
        check(bool(bad), f"la sandbox laisse passer {what}")
    print(f"   {len(REFERENCE)} étalons acceptés, {len(REFUSED_SOURCES)} sources refusées : "
          f"{', '.join(REFUSED_SOURCES)}")

    # -- 3. l'empreinte du signal -------------------------------------------
    print("3. l'empreinte du signal, distincte de celle du harnais")
    hashes = {}
    for signal_id, module in REFERENCE.items():
        first = signature.signal_hash(module)
        check(first == signature.signal_hash(module), f"{signal_id} : empreinte instable")
        check(len(first) == 16, f"{signal_id} : empreinte de {len(first)} caractères")
        sources = scan.sources_of(module)
        check(any(path.name == "_common.py" for path in sources),
              f"{signal_id} : l'empreinte ignore signals/_common.py, qui décide de l'ancre")
        hashes[signal_id] = first
    check(len(set(hashes.values())) == len(hashes),
          f"deux signaux partagent une empreinte : {hashes}")
    from harness import registry  # noqa: PLC0415 -- lu ici, jamais appelé pour mesurer
    check(registry.code_hash() not in set(hashes.values()),
          "l'empreinte d'un signal est celle du harnais")
    print(f"   {len(hashes)} empreintes distinctes, helpers compris ; "
          f"harnais {registry.code_hash()}")

    # -- 4. LA PORTE : le test attrape ce qu'on lui a caché -------------------
    print("4. le test de causalité — les honnêtes passent, les tricheurs tombent")
    for signal_id, module in REFERENCE.items():
        divergences = causality.check(module, panel, probes=PROBES, full=produced[signal_id])
        check(not divergences,
              f"{signal_id} est honnête mais le test le condamne : "
              f"{[str(d) for d in divergences[:2]]}")
        print(f"   {signal_id:34s} {PROBES} sondes, 0 divergence")

    for tainted in TAINTED:
        divergences = causality.check(tainted, panel, probes=PROBES)
        check(bool(divergences),
              f"{tainted.SIGNAL_ID} lit le futur et le test NE L'ATTRAPE PAS")
        kinds = {d.kind for d in divergences}
        expected = EXPECTED_CATCH[tainted.SIGNAL_ID]
        check(expected in kinds,
              f"{tainted.SIGNAL_ID} est attrapé sur {kinds} et non sur {expected!r} — "
              "le test fonctionne pour une raison qu'on n'a pas prévue")
        if tainted.SIGNAL_ID in CAUGHT_AT_EVERY_PROBE:
            probes = causality.probe_instants(tainted.scores(panel), PROBES)
            caught = {d.probe for d in divergences}
            check(len(caught) == len(probes),
                  f"{tainted.SIGNAL_ID} n'est attrapé qu'à {len(caught)} sonde(s) sur "
                  f"{len(probes)} — la résolution du test ne tient pas à une barre (D27)")
            print(f"   {tainted.SIGNAL_ID:34s} attrapé à {len(caught)} sonde(s) sur {len(probes)}")
        first = divergences[0] if divergences else None
        print(f"   {tainted.SIGNAL_ID:34s} ATTRAPÉ — {len(divergences)} divergence(s), "
              f"{sorted(kinds)}")
        if first is not None:
            print(f"      {first}")

    print(f"\n{checks} vérifications")
    if failures:
        print("PORTE 05 : NON FRANCHIE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("PORTE 05 : FRANCHIE — un look-ahead injecté est attrapé, "
          "et le test dit lequel et où")
    return 0


if __name__ == "__main__":
    sys.exit(main())
