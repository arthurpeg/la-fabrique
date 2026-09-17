"""PORTE 04 — le registre incontournable et le verrou du holdout.

Ce script ne vérifie pas que le registre fonctionne : il vérifie qu'on **ne peut
pas s'en passer**. La différence est toute la phase 04. Un dispositif qu'on n'a
jamais essayé de contourner n'est pas un dispositif, c'est une intention.

Ce qui est exigé (ETAT.md, phase 04) :

  1. aucun chemin de code ne produit un IC sans écrire au registre ;
  2. la tranche `holdout` est inaccessible par construction ;
  3. registry/SCHEMA.md fixe les types, les valeurs permises et la validation.

Le point 1 n'est pas démontrable de façon absolue en Python, et `D05` le dit :
`from harness.metric import _pool` rend encore un nombre. Ce qui est démontré ici
est plus étroit et plus vrai — **aucun chemin public** n'y mène, et **aucun module
de ce dépôt** ne prend le chemin privé. La section 6 le vérifie en analysant la
syntaxe de chaque fichier.

    python scripts/gate_04_registry.py
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from harness import metric, registry  # noqa: E402
from panel import Panel, unseal  # noqa: E402
from panel.panel import HoldoutLocked, SliceExceeded  # noqa: E402

SCHEMA_MD = REPO / "registry" / "SCHEMA.md"

# Une seule exception, écrite et motivée : la porte 03 exige une SECONDE
# implémentation de l'IC, écrite différemment, pour calibrer la première. C'est
# le contraire d'un contournement -- c'est la vérification. Toute autre
# occurrence de `spearmanr` hors de harness/ est un IC clandestin.
SPEARMAN_ALLOWED = {"scripts/gate_03_harness.py"}

PRIVATE_NAMES = {"_pool", "_deflated_t"}


def repo_modules() -> list[Path]:
    """Tout le code de ce dépôt, sans l'environnement ni les caches."""
    skip = {".venv", "__pycache__", ".git", ".ruff_cache"}
    return [
        path
        for path in sorted(REPO.rglob("*.py"))
        if not any(part in skip for part in path.parts)
    ]


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    def refuses(expected, call, what: str) -> None:
        """La seule forme de vérification qui compte ici : ça doit LEVER."""
        nonlocal checks
        checks += 1
        try:
            call()
        except expected:
            return
        except Exception as error:  # noqa: BLE001
            failures.append(
                f"{what} : a levé {type(error).__name__} au lieu de {expected.__name__}"
            )
            return
        failures.append(f"{what} : N'A PAS LEVÉ — le contournement fonctionne")

    # -- 1. le schéma du code et celui du document disent la même chose ------
    print("1. le schéma est appliqué, et le document le décrit fidèlement")
    schema_text = SCHEMA_MD.read_text(encoding="utf-8")
    for field in registry.REQUIRED + registry.OPTIONAL:
        check(f"`{field}`" in schema_text, f"le champ {field!r} n'est pas décrit dans SCHEMA.md")
    for value in registry.STAGES + registry.SLICES + registry.REQUESTED_BY:
        check(f"`{value}`" in schema_text, f"la valeur permise {value!r} est absente de SCHEMA.md")
    check(
        "append-only" in schema_text.lower(),
        "SCHEMA.md ne dit plus que le fichier est append-only",
    )
    print(f"   {len(registry.REQUIRED)} champs obligatoires, {len(registry.OPTIONAL)} facultatifs, "
          f"{len(registry.STAGES)} stages, {len(registry.SLICES)} tranches — tous documentés")

    # -- 2. le registre existant satisfait son propre schéma ----------------
    print("2. chaque ligne déjà écrite satisfait le schéma")
    lines = registry.read_all()
    for index, record in enumerate(lines, start=1):
        bad = registry.validate_record(record)
        check(not bad, f"ligne {index} du registre : {'; '.join(bad)}")
    stale = [r for r in lines if r.get("code_hash") != registry.code_hash()]
    print(f"   {len(lines)} lignes valides, {registry.counted_tests()} test(s) compté(s), "
          f"{len(stale)} produite(s) par un harnais antérieur (périmées, D05)")

    # -- 3. append-only, vérifié contre git ---------------------------------
    print("3. rien n'a été retiré ni réécrit depuis le dernier commit")
    try:
        committed = subprocess.run(
            ["git", "show", "HEAD:registry/tests.jsonl"],
            # encoding explicite : sans lui, Windows décode la sortie de git en
            # cp1252 et toute ligne accentuée paraît réécrite. Le faux positif
            # était réel -- il accusait la ligne 13, qui n'avait pas bougé.
            cwd=REPO, capture_output=True, encoding="utf-8", check=True,
        ).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        committed = None
    if committed is None:
        check(False, "impossible de lire la version commitée du registre (git absent ?)")
    else:
        current = registry.REGISTRY.read_text(encoding="utf-8").splitlines()
        check(
            len(current) >= len(committed),
            f"le registre a PERDU des lignes : {len(current)} aujourd'hui, "
            f"{len(committed)} au dernier commit",
        )
        rewritten = [
            i + 1
            for i, (was, now) in enumerate(zip(committed, current, strict=False))
            if was != now
        ]
        check(not rewritten, f"lignes réécrites depuis le commit : {rewritten[:5]}")
        print(f"   {len(committed)} lignes commitées, toutes intactes, "
              f"{len(current) - len(committed)} ajoutée(s) depuis")

    # -- 4. on essaie de produire un IC hors registre ------------------------
    print("4. on essaie délibérément de calculer un IC sans écrire — et on échoue")
    check(
        not hasattr(metric, "pool"),
        "harness.metric.pool existe encore : le chemin public vers un IC non écrit est ouvert",
    )
    check(
        not hasattr(metric, "deflated_t"),
        "harness.metric.deflated_t existe encore : un t se calcule sans ligne",
    )
    check(
        "pool" not in getattr(__import__("harness"), "__all__", []),
        "harness exporte encore `pool`",
    )

    empty = pd.Series(dtype=float)
    index = pd.DatetimeIndex([], tz="UTC")
    refuses(
        registry.RegistryBypass,
        lambda: metric.cell_ic(empty, empty, index, "NQ", "US", 30, None),
        "cell_ic sans jeton",
    )
    refuses(
        registry.RegistryBypass,
        lambda: metric.record_pooled([], None, horizon_bars=30, instruments=9,
                                     effective_breadth=4.224),
        "record_pooled sans jeton",
    )
    refuses(
        registry.RegistryBypass,
        lambda: registry.settle("un jeton que j'ai inventé", ic=0.9, t_stat=9.9),
        "settle avec un faux jeton",
    )
    refuses(
        ValueError,
        lambda: registry.open_test(signal_id="x", hypothesis_ref=None,
                                   stage="je-fais-ce-que-je-veux",
                                   data_slice="pool", horizon="30min"),
        "open_test avec un stage inventé",
    )
    refuses(
        ValueError,
        lambda: registry.open_test(signal_id="x", hypothesis_ref=None, stage="04-audit",
                                   data_slice="validation", horizon="30min"),
        "open_test sur la tranche `validation`, qui n'existe plus (D01 5)",
    )
    before = len(registry.read_all())
    refuses(
        ValueError,
        lambda: registry.append({"test_id": "pas-un-id", "ic": 4.0}),
        "append d'une ligne qui ne respecte pas le schéma",
    )
    check(
        len(registry.read_all()) == before,
        "une ligne refusée a quand même été écrite",
    )

    # le chemin légitime, lui, écrit exactement une ligne -- et le jeton s'use
    ticket = registry.open_test(
        signal_id="porte-04-chemin-legitime",
        hypothesis_ref=None,
        stage="04-audit",
        data_slice="pool",
        horizon="30min",
    )
    cells = [
        metric.CellIC("NQ", "US", 0.01, 1000, 30.0, 30.0),
        metric.CellIC("ES", "US", -0.01, 1000, 30.0, 30.0),
    ]
    settled = metric.record_pooled(
        cells, ticket, horizon_bars=30, instruments=9, effective_breadth=4.224
    )
    after = registry.read_all()
    check(
        len(after) == before + 1,
        f"le chemin légitime a écrit {len(after) - before} lignes, pas 1",
    )
    check(
        after[-1]["test_id"] == settled["test_id"],
        "la ligne écrite n'est pas celle qui est rendue",
    )
    check(after[-1]["observations"] == 2000, "la ligne n'a pas retenu le compte d'observations")
    refuses(
        registry.RegistryBypass,
        lambda: metric.record_pooled(cells, ticket, horizon_bars=30, instruments=9,
                                     effective_breadth=4.224),
        "réutilisation d'un jeton déjà dépensé",
    )
    refuses(
        registry.RegistryBypass,
        lambda: metric.cell_ic(empty, empty, index, "NQ", "US", 30, ticket),
        "cell_ic avec un jeton dépensé",
    )
    print(f"   6 contournements refusés ; le chemin légitime a écrit 1 ligne "
          f"({settled['test_id']}) et brûlé son jeton")

    # -- 5. le holdout -------------------------------------------------------
    print("5. le holdout, essayé par toutes les portes")
    in_holdout = "2024-06-03 20:00"
    refuses(
        HoldoutLocked,
        lambda: Panel.open(asof=in_holdout, slice="holdout"),
        "Panel.open sur le holdout",
    )
    refuses(
        HoldoutLocked,
        lambda: Panel.open(asof=in_holdout, slice="holdout", unseal=True),
        "Panel.open sur le holdout avec un jeton bidon (True)",
    )
    refuses(
        HoldoutLocked,
        lambda: Panel.open(asof=in_holdout, slice="holdout", unseal="PHASE 15"),
        "Panel.open sur le holdout avec la phrase en guise de jeton",
    )
    refuses(
        SliceExceeded,
        lambda: Panel.open(asof=in_holdout, slice="pool"),
        "Panel.open sur une date de holdout via la tranche pool",
    )
    refuses(
        unseal.SealRefused,
        lambda: unseal.unseal_holdout(reason="ouverture de la phase 15, comme prévu"),
        "unseal_holdout sans la phrase dans l'environnement",
    )
    os.environ[unseal.ENV] = unseal.PHRASE
    try:
        refuses(
            unseal.SealRefused,
            lambda: unseal.unseal_holdout(reason="vite"),
            "unseal_holdout avec la phrase mais sans raison écrite",
        )
    finally:
        del os.environ[unseal.ENV]
    check(
        unseal.times_opened() == 0,
        f"le holdout a été descellé {unseal.times_opened()} fois — invariant V rompu",
    )
    check(
        os.environ.get(unseal.ENV) is None,
        "la phrase de descellage traîne dans l'environnement après le test",
    )
    print("   5 refus, le registre de descellage est vide, la phrase n'est pas dans l'env")

    # -- 6. personne, dans ce dépôt, ne prend le chemin privé ----------------
    print("6. analyse syntaxique : aucun module ne contourne")
    scanned = 0
    for path in repo_modules():
        relative = path.relative_to(REPO).as_posix()
        in_harness = relative.startswith("harness/")
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except SyntaxError as error:
            check(False, f"{relative} ne se parse pas : {error}")
            continue
        scanned += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and not in_harness:
                names = {alias.name for alias in node.names}
                private = names & PRIVATE_NAMES
                check(not private, f"{relative} importe {sorted(private)} de {node.module}")
            if isinstance(node, ast.Attribute) and not in_harness:
                check(
                    node.attr not in PRIVATE_NAMES,
                    f"{relative} atteint {node.attr} — le chemin privé vers un IC non écrit",
                )
            if isinstance(node, ast.Call):
                called = node.func
                name = getattr(called, "attr", None) or getattr(called, "id", None)
                if name == "spearmanr" and not in_harness:
                    check(
                        relative in SPEARMAN_ALLOWED,
                        f"{relative} calcule une corrélation de rang hors du harnais",
                    )
                if name == "unseal_holdout" and relative != "panel/unseal.py":
                    check(
                        relative == Path(__file__).relative_to(REPO).as_posix(),
                        f"{relative} appelle unseal_holdout — la phase 15 n'est pas ouverte",
                    )
    print(f"   {scanned} modules analysés ; le seul appel à spearmanr hors harnais est "
          f"la seconde implémentation de la porte 03, écrite et motivée")

    # -- verdict -------------------------------------------------------------
    print(f"\n{checks} vérifications")
    if failures:
        print("PORTE 04 : NON FRANCHIE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("PORTE 04 : FRANCHIE — le registre est incontournable, le holdout est scellé")
    print(f"  registre : {len(registry.read_all())} lignes, "
          f"{registry.counted_tests()} test compté ; harnais {registry.code_hash()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
