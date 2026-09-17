"""The white list. What a signal is allowed to import, and to call.

A white list, not a black list: a black list is a list of the tricks somebody
already thought of, and it is wrong the day somebody thinks of another one. This
is the second curtain anyway -- the real proof of causality is in `causality.py`,
which tests a PROPERTY rather than a syntax (D07).

What this refuses, and why:

  the network      CLAUDE.md forbids any network-touching dependency in the
                   computation path of a signal. A signal that phones out is not
                   reproducible, and its result is not attributable to the data.
  the filesystem   the only door to data is the Panel. A signal that opens a file
                   reads something nobody dated.
  eval and friends a string that becomes code is a scan that means nothing.
  dunder attributes `__globals__`, `__class__.__subclasses__` -- the classic way
                   out of any Python restriction.
  a negative shift `close.shift(-30)` is reading the future, written plainly. It
                   is the one syntactic form worth naming, and naming it is not
                   the same as catching every form.
"""

from __future__ import annotations

import ast
from pathlib import Path

ALLOWED_ROOTS = frozenset({
    "__future__",
    "collections",
    "dataclasses",
    "math",
    "numpy",
    "pandas",
    "panel",
    "signals",
    "typing",
})

FORBIDDEN_CALLS = frozenset({
    "compile", "eval", "exec", "globals", "input", "locals", "open", "vars",
    "__import__",
})

FORBIDDEN_ATTRS = frozenset({
    "__globals__", "__class__", "__subclasses__", "__bases__", "__code__",
    "__builtins__", "__dict__", "__mro__",
})


def scan_source(source: str, where: str) -> list[str]:
    """Every refusal this module deserves, named. Empty means it passes."""
    bad: list[str] = []
    try:
        tree = ast.parse(source, filename=where)
    except SyntaxError as error:
        return [f"{where} ne se parse pas : {error}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root not in ALLOWED_ROOTS:
                    bad.append(f"{where}:{node.lineno} importe {alias.name!r}, hors liste blanche")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if node.level:
                continue  # un import relatif reste dans le paquet du signal
            if root not in ALLOWED_ROOTS:
                bad.append(
                    f"{where}:{node.lineno} importe depuis {node.module!r}, hors liste blanche"
                )
        elif isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_ATTRS:
                bad.append(f"{where}:{node.lineno} atteint {node.attr}")
        elif isinstance(node, ast.Call):
            name = getattr(node.func, "id", None)
            if name in FORBIDDEN_CALLS:
                bad.append(f"{where}:{node.lineno} appelle {name}()")
            if getattr(node.func, "attr", None) == "shift":
                for argument in node.args:
                    if isinstance(argument, ast.UnaryOp) and isinstance(argument.op, ast.USub):
                        bad.append(
                            f"{where}:{node.lineno} appelle shift() avec un décalage négatif — "
                            "c'est lire le futur, écrit en toutes lettres"
                        )
    return bad


def scan_module(module) -> list[str]:
    """Scan a signal module and every module of `signals/` it leans on."""
    bad: list[str] = []
    for path in sources_of(module):
        bad.extend(scan_source(path.read_text(encoding="utf-8"), path.name))
    return bad


def sources_of(module) -> list[Path]:
    """The signal's own file, plus the helpers it imports from `signals/`.

    A signal is not only the module that carries its name: `signals/_common.py`
    decides where the anchor falls, and a change there changes the signal.
    """
    main = Path(module.__file__).resolve()
    found = [main]
    tree = ast.parse(main.read_text(encoding="utf-8"), filename=main.name)
    package = main.parent
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "signals":
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.Import):
            names = [
                alias.name.split(".")[-1]
                for alias in node.names
                if alias.name.startswith("signals.")
            ]
        for name in names:
            candidate = package / f"{name}.py"
            if candidate.exists() and candidate not in found:
                found.append(candidate)
    return sorted(found)
