#!/usr/bin/env python3
"""Regenere wiki/hot.md a partir de wiki/log.md, ETAT.md et du registre.

Stdlib uniquement. Concu pour ne JAMAIS faire echouer une session : toute
erreur est avalee, le script sort en 0, et hot.md garde sa version precedente
plutot que d'etre ecrase par du vide.

    python wiki/update_hot.py            regenere wiki/hot.md
    python wiki/update_hot.py --lint     controles mecaniques du SCHEMA, sec 3.1

Le bloc entre les marqueurs NEXT-ACTIONS est editable a la main : il est relu
et reinjecte tel quel a chaque regeneration.
"""

from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

LOG = WIKI / "log.md"
HOT = WIKI / "hot.md"
INDEX = WIKI / "index.md"
LEDGER = WIKI / "Failed Ideas" / "ledger.md"
ETAT = ROOT / "ETAT.md"
REGISTRY = ROOT / "registry" / "tests.jsonl"

N_LOG_ENTRIES = 8

START = "<!-- NEXT-ACTIONS:START -->"
END = "<!-- NEXT-ACTIONS:END -->"

DEFAULT_NEXT_ACTIONS = """\
> Bloc **éditable à la main**. Le générateur le relit et le réinjecte tel quel.
> Tout ce qui est en dehors des marqueurs est écrasé à chaque régénération.

- _(rien d'inscrit — voir « Prochaine action » ci-dessus, qui vient de `ETAT.md`)_
"""

LOG_RE = re.compile(r"^##\s*\[(\d{4}-\d{2}-\d{2})\]\s*([\w-]+)\s*\|(.*)$")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

VALID_TYPES = {"hub", "phase", "signal", "concept", "research", "router"}
REQUIRED_KEYS = ("type", "updated", "status", "sources")

FENCE_RE = re.compile(r"^\s*(```|~~~)")


# --------------------------------------------------------------------------
# lecture tolerante


def out(msg: str = "") -> None:
    """print qui ne meurt pas sur une console cp1252."""
    try:
        print(msg)
    except Exception:
        try:
            enc = sys.stdout.encoding or "ascii"
            sys.stdout.write(msg.encode(enc, "replace").decode(enc) + "\n")
        except Exception:
            pass


def read(path: Path) -> str:
    """Contenu du fichier, ou '' s'il manque ou resiste."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""


def pages() -> list[Path]:
    try:
        return sorted(p for p in WIKI.rglob("*.md") if p.is_file())
    except Exception:
        return []


def without_code(text: str) -> str:
    """Le texte prive de son code : les liens d'exemple n'y comptent pas.

    Retire les blocs clotures (``` ou ~~~) puis les spans en accents graves.
    """
    keep, fenced = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            keep.append(line)
    return re.sub(r"`[^`\n]*`", "", "\n".join(keep))


def frontmatter(text: str) -> dict[str, str]:
    """Parse plat du frontmatter YAML. Pas de YAML imbrique ici, exprès."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


# --------------------------------------------------------------------------
# extraction


def log_entries() -> list[tuple[str, str, str]]:
    """[(date, type, reste), ...] dans l'ordre du fichier."""
    entries = []
    for line in read(LOG).splitlines():
        m = LOG_RE.match(line.strip())
        if m:
            entries.append((m.group(1), m.group(2), m.group(3).strip()))
    return entries


def etat_field(label: str) -> str:
    """Valeur d'un champ '**Label :** valeur' de ETAT.md, sur une ou deux lignes."""
    text = read(ETAT)
    if not text:
        return ""
    lines = text.splitlines()
    needle = f"**{label} :**"
    for i, line in enumerate(lines):
        if needle in line:
            val = line.split(needle, 1)[1].strip()
            # le champ peut deborder sur les lignes suivantes
            for nxt in lines[i + 1 : i + 3]:
                s = nxt.strip()
                if not s or s.startswith(("**", "#", ">", "|", "---")):
                    break
                val += " " + s
            return re.sub(r"\s+", " ", val).strip()
    return ""


def etat_next_action() -> str:
    """Le corps de la section '## Prochaine action' de ETAT.md."""
    text = read(ETAT)
    if not text:
        return ""
    m = re.search(r"^##\s*Prochaine action\s*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^##\s", rest, re.M)
    body = rest[: nxt.start()] if nxt else rest
    return body.strip()


def etat_blockers() -> list[str]:
    """Lignes du tableau 'Ce qui bloque' de ETAT.md."""
    text = read(ETAT)
    if not text:
        return []
    m = re.search(r"^##\s*Ce qui bloque.*$", text, re.M)
    if not m:
        return []
    rest = text[m.end() :]
    nxt = re.search(r"^##\s", rest, re.M)
    body = rest[: nxt.start()] if nxt else rest
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("|") and not re.fullmatch(r"\|[\s|:-]+\|", s):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and cells[0].lower() not in ("attendu", ""):
                rows.append(s)
    return rows


def registry_count() -> int | None:
    """Lignes non vides du registre, ou None s'il est illisible."""
    try:
        if not REGISTRY.exists():
            return None
        return sum(1 for ln in read(REGISTRY).splitlines() if ln.strip())
    except Exception:
        return None


def ledger_count() -> int | None:
    try:
        if not LEDGER.exists():
            return None
        return sum(
            1 for ln in read(LEDGER).splitlines() if re.match(r"^\|\s*F\d+\s*\|", ln)
        )
    except Exception:
        return None


def page_census() -> list[tuple[str, int]]:
    census: dict[str, int] = {}
    for p in pages():
        try:
            rel = p.relative_to(WIKI)
        except Exception:
            continue
        folder = rel.parts[0] if len(rel.parts) > 1 else "(racine)"
        census[folder] = census.get(folder, 0) + 1
    return sorted(census.items())


def preserved_next_actions() -> str:
    """Le bloc editable a la main, tel quel."""
    text = read(HOT)
    if START in text and END in text:
        block = text.split(START, 1)[1].split(END, 1)[0]
        if block.strip():
            return block.strip("\n")
    return DEFAULT_NEXT_ACTIONS.rstrip("\n")


# --------------------------------------------------------------------------
# rendu


def render() -> str:
    today = _dt.date.today().isoformat()
    entries = log_entries()
    phase = etat_field("Phase courante") or "_inconnue — `ETAT.md` illisible_"
    gate = etat_field("Dernière porte franchie") or "_inconnue_"
    decision = etat_field("Décision la plus récente") or "_inconnue_"
    nextact = etat_next_action()
    blockers = etat_blockers()
    nreg = registry_count()
    nled = ledger_count()

    L: list[str] = []
    a = L.append

    a("---")
    a("type: hub")
    a(f"updated: {today}")
    a("status: genere")
    a("sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]")
    a("---")
    a("")
    a("# HOT — l'état courant")
    a("")
    a("> [!warning] Page **générée**. Ne pas l'éditer à la main.")
    a("> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.")
    a("> Toute modification hors du bloc « Prochaines actions » sera perdue.")
    a("> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.")
    a("")
    a(f"*Régénérée le {today}.*")
    a("")
    a("---")
    a("")
    a("## État courant")
    a("")
    a("| | |")
    a("|---|---|")
    a(f"| **Phase courante** | {phase} |")
    a(f"| **Dernière porte franchie** | {gate} |")
    a(f"| **Décision la plus récente** | {decision} |")
    if nreg is None:
        a("| **Tests au registre** | _registre introuvable_ |")
    else:
        a(f"| **Tests au registre** | {nreg} |")
    if nled is not None:
        a(f"| **Idées abandonnées recensées** | {nled} |")
    a(f"| **Entrées au journal** | {len(entries)} |")
    a("")

    if blockers:
        a("## Ce qui bloque")
        a("")
        a("| Attendu | De qui | Bloque |")
        a("|---|---|---|")
        for row in blockers:
            a(row)
        a("")

    if nextact:
        a("## Prochaine action — reflet de `ETAT.md`")
        a("")
        for line in nextact.splitlines():
            a(line)
        a("")

    shown = min(N_LOG_ENTRIES, len(entries))
    a("## " + ("La dernière entrée du journal" if shown == 1
              else f"Les {shown} dernières entrées du journal"))
    a("")
    if entries:
        a("| Date | Type | Ce qui s'est passé | Résultat |")
        a("|---|---|---|---|")
        for date, kind, rest in reversed(entries[-N_LOG_ENTRIES:]):
            what, _, outcome = rest.partition("|")
            what = what.strip().replace("|", r"\|")
            outcome = outcome.strip().replace("|", r"\|") or "—"
            a(f"| {date} | `{kind}` | {what} | {outcome} |")
    else:
        a("_Aucune entrée lisible dans `wiki/log.md`._")
    a("")
    a("Journal complet : [[log]]")
    a("")

    census = page_census()
    if census:
        a("## Le wiki en chiffres")
        a("")
        a("| Dossier | Pages |")
        a("|---|---|")
        for folder, n in census:
            a(f"| `{folder}` | {n} |")
        a("")

    a("## Prochaines actions")
    a("")
    a(START)
    a(preserved_next_actions())
    a(END)
    a("")
    a("---")
    a("")
    a("À lire au démarrage : [[index]] puis [[Failed Ideas/ledger]] — "
      "règles permanentes de `CLAUDE.md` § Wiki.")
    a("")
    return "\n".join(L)


# --------------------------------------------------------------------------
# lint mecanique — SCHEMA sec. 3.1


def lint() -> int:
    problems: list[str] = []
    all_pages = pages()

    stems: set[str] = set()
    for p in all_pages:
        try:
            rel = p.relative_to(WIKI).with_suffix("")
        except Exception:
            continue
        stems.add(rel.as_posix())
        stems.add(rel.name)

    index_text = read(INDEX)
    linked: set[str] = set()

    for p in all_pages:
        text = read(p)
        try:
            rel = p.relative_to(WIKI).with_suffix("").as_posix()
        except Exception:
            continue

        fm = frontmatter(text)
        if not fm:
            problems.append(f"frontmatter absent      : {rel}")
        else:
            for key in REQUIRED_KEYS:
                if key not in fm:
                    problems.append(f"frontmatter, '{key}' manquant : {rel}")
            t = fm.get("type", "")
            if t and t not in VALID_TYPES:
                problems.append(f"type '{t}' hors valeurs permises : {rel}")
            u = fm.get("updated", "")
            if u and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", u):
                problems.append(f"updated '{u}' non ISO : {rel}")

        for raw in WIKILINK_RE.findall(without_code(text)):
            target = raw.split("|")[0].split("#")[0].strip()
            if not target:
                continue
            linked.add(target)
            linked.add(target.split("/")[-1])
            if target not in stems:
                problems.append(f"lien mort [[{target}]] dans : {rel}")

    for p in all_pages:
        try:
            rel = p.relative_to(WIKI).with_suffix("").as_posix()
        except Exception:
            continue
        if rel in ("index", "hot"):
            continue
        in_index = rel in index_text or p.name in index_text
        if not in_index and rel not in linked and p.stem not in linked:
            problems.append(f"orpheline (ni index ni lien) : {rel}")

    for i, line in enumerate(read(LOG).splitlines(), 1):
        s = line.strip()
        if s.startswith("## ") and not LOG_RE.match(s):
            problems.append(f"log.md:{i} ligne hors format : {s[:70]}")

    if problems:
        out(f"lint : {len(problems)} point(s)")
        for pb in sorted(set(problems)):
            out(f"  - {pb}")
    else:
        out("lint : rien à signaler (contrôles mécaniques seuls).")
    out("")
    out("Les contrôles de jugement — contradictions, supersession, concepts")
    out("manquants, autorité usurpée — demandent une lecture. Voir")
    out("wiki/SCHEMA.md section 3.2.")
    return 0


# --------------------------------------------------------------------------


def main() -> int:
    try:
        if "--lint" in sys.argv:
            return lint()

        if not WIKI.is_dir():
            out("update_hot : wiki/ introuvable, rien à faire.")
            return 0

        content = render()
        if not content.strip():
            out("update_hot : rendu vide, hot.md laissé intact.")
            return 0

        HOT.write_text(content, encoding="utf-8", newline="\n")
        out(f"update_hot : {HOT.relative_to(ROOT).as_posix()} régénéré.")
        return 0
    except Exception as exc:  # jamais fatal
        out(f"update_hot : ignoré ({type(exc).__name__}: {exc})")
        return 0


if __name__ == "__main__":
    sys.exit(main())
