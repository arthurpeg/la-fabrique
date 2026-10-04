"""Le juge des hypothèses du lot 09 — `D40`, écrit AVANT la première hypothèse.

Ce que `gate_09.py` vérifie aujourd'hui d'une hypothèse : **qu'un fichier du bon
nom existe**. C'est tout, et c'est trop peu pour quarante et une. Ce script pose
les conditions de `D40` et les compte.

Sept conditions, à tolérance zéro comme `D16` et `D23` :

- `A1` — l'en-tête porte les sept champs de `D40`, et le nom du fichier donne une
  `ref` `H<NN>` unique ;
- `A2` — la fiche nommée **existe sur disque**, et `signal` = `fiche` (la
  convention que `D40` fixe) ;
- `A3` — le signe attendu est `+1` ou `−1`, jamais autre chose (`D25` `C1`) ;
- `A4` — la tranche est `pool` à l'`asof` **exact** de `D29` — une date choisie
  par hypothèse serait un bouton ;
- `A5` — les six sections de `D40` sont présentes, dans l'ordre, et non vides ;
- `A6` — chaque chiffre du papier invoqué **se retrouve dans `reported_results`
  de la fiche**, au même nom et à la même valeur (`F2` et `S5` transposés) ;
- `A7` — « Ce qui la contredirait » porte **au moins deux clauses et au moins un
  nombre**.

Plus deux conditions qui portent sur l'ensemble, pas sur un fichier :

- `B1` — **bijection avec le lot** : chaque fiche de `hypotheses/LOT-09.json` a
  exactement une hypothèse, et réciproquement ;
- `B2` — **le signe concorde avec le signal**, dès que le module existe.
  `gate_09` lit `module.EXPECTED_SIGN`, pas l'hypothèse, et rien ne vérifiait
  que les deux disent la même chose.

`B2` est le seul trou de protocole que `D40` ferme plutôt que documente : un
codeur qui oriente son score à l'envers ferait calculer un `p` unilatéral sur un
signe que personne n'avait pré-enregistré.

**Ce que ce juge ne sait pas faire**, et `D40` le dit : dire qu'une hypothèse est
*creuse*. Une affirmation fidèle à sa fiche, signée, falsifiable sur le papier et
sans le moindre intérêt passe les sept conditions. Même limite que `D16` pour les
fiches.

**AUCUN IC N'EST CALCULÉ ICI**, et le registre n'est jamais lu.

    python hypotheses/score_hypothese.py           # juge les hypothèses du lot
    python hypotheses/score_hypothese.py --check    # auto-test sur des fichiers
                                                    # FABRIQUÉS, ne juge rien de réel
    python hypotheses/score_hypothese.py --lier     # inscrit `ref` et `signal_id`
                                                    # dans LOT-09.json, dérivés des
                                                    # fichiers d'hypothèse (F54)
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

HYPOTHESES_DIR = REPO / "hypotheses"
LOT_FILE = HYPOTHESES_DIR / "LOT-09.json"
FICHES_DIRS = (REPO / "corpus" / "fiches", REPO / "corpus" / "fiches_harvest")
SIGNALS_DIR = REPO / "signals"

# `D29`, recopié de `scripts/gate_09.py` : la tranche entière, à un instant fixé
# d'avance. L'hypothèse doit le porter en clair, faute de quoi rien n'empêche
# qu'une mesure raccourcisse l'échantillon jusqu'à ce qu'un signal passe.
TRANCHE_REQUISE = "pool"
ASOF_REQUIS = "2023-12-29 20:00 UTC"

CHAMPS_REQUIS = ("écrite le", "fiche", "signal", "signe attendu", "tranche", "écrite par", "statut")

SECTIONS_REQUISES = (
    "Ce qui est affirmé",
    "Le domaine",
    "Ce qui est attendu, en chiffres",
    "Ce que le papier annonce, et d'où ça vient",
    "Ce qui la contredirait",
    "Ce qui n'est pas affirmé ici",
)
SECTION_PAPIER = SECTIONS_REQUISES[3]
SECTION_CONTREDIT = SECTIONS_REQUISES[4]

RE_REF = re.compile(r"^(H\d{2})-[a-z0-9-]+\.md$")
# Les quatre hypothèses écrites AVANT `D40`, dans les phases 05 et 06 : elles ne
# portent pas son en-tête et ne se jugent pas sur elle. Toute autre hypothèse est
# dans le périmètre de `D40` et doit nommer une fiche du lot — sans quoi elle est
# refusée ici, plutôt que silencieusement ignorée pendant que `B1` annonce sa
# fiche comme non couverte.
REFS_AVANT_D33 = ("H01", "H02", "H03", "H04")
RE_CHAMP = re.compile(r"^\*\*(?P<label>[^:*]+?)\s*:\*\*\s*(?P<valeur>.*)$")
RE_BACKTICK = re.compile(r"`([^`]+)`")
RE_SECTION = re.compile(r"^##\s+(.*?)\s*$", re.MULTILINE)


def normaliser_nombre(brut: str) -> float | None:
    """Le nombre que porte une cellule de table, ou `None` si elle n'en porte pas.

    Le signe moins typographique `−` (U+2212) et les séparateurs de milliers
    sont les deux formes que l'extraction PDF a déjà imposées au corpus (`L28`,
    `F26`) : les ignorer ici ferait refuser une valeur correcte.
    """
    t = brut.strip().strip("`*").replace("−", "-").replace(",", "").replace(" ", "")
    t = t.replace(" ", "").rstrip("%")
    if t.lower() in ("", "null", "none", "aucun"):
        return None
    try:
        return float(t)
    except ValueError:
        return None


def lire_entete(texte: str) -> dict[str, str]:
    """Les champs `**Label :** valeur` de l'en-tête, avant la première section."""
    entete = texte.split("\n## ", 1)[0]
    champs: dict[str, str] = {}
    for ligne in entete.splitlines():
        m = RE_CHAMP.match(ligne.strip())
        if m:
            champs[m.group("label").strip().casefold()] = m.group("valeur").strip()
    return champs


def lire_sections(texte: str) -> list[tuple[str, str]]:
    """Les sections `## Titre` dans l'ordre du fichier, avec leur corps."""
    bornes = [(m.group(1), m.start(), m.end()) for m in RE_SECTION.finditer(texte)]
    out: list[tuple[str, str]] = []
    for i, (titre, _, fin) in enumerate(bornes):
        suivant = bornes[i + 1][1] if i + 1 < len(bornes) else len(texte)
        out.append((titre, texte[fin:suivant].strip()))
    return out


def premier_backtick(valeur: str) -> str | None:
    m = RE_BACKTICK.search(valeur)
    return m.group(1).strip() if m else None


def charger_fiches() -> dict[str, dict]:
    """`fiche_id` -> la fiche, quelle que soit la population qui la porte."""
    fiches: dict[str, dict] = {}
    for dossier in FICHES_DIRS:
        for chemin in sorted(dossier.glob("*.json")):
            data = json.loads(chemin.read_text(encoding="utf-8"))
            fiches[data.get("fiche_id", chemin.stem)] = data
    return fiches


def signe_du_signal(signal_id: str) -> int | None:
    """`EXPECTED_SIGN` du module qui porte ce `SIGNAL_ID`, ou `None` s'il n'existe pas.

    Le module est **importé**, jamais lu au grep : c'est la valeur qu'exécutera
    `gate_09` qui compte, pas celle qu'on lit dans le texte.
    """
    for chemin in sorted(SIGNALS_DIR.glob("*.py")):
        if chemin.name in ("_common.py", "__init__.py"):
            continue
        nom = ".".join(chemin.relative_to(REPO).with_suffix("").parts)
        module = importlib.import_module(nom)
        if getattr(module, "SIGNAL_ID", None) == signal_id:
            return int(module.EXPECTED_SIGN)
    return None


def resultats_de_la_fiche(fiche: dict) -> dict[str, object]:
    return {r.get("name"): r.get("value") for r in fiche.get("reported_results", [])}


def juger_fichier(
    chemin: Path,
    fiches: dict[str, dict],
    signes_signaux: dict[str, int | None],
) -> tuple[str | None, str | None, list[str]]:
    """Juge une hypothèse. Rend `(ref, fiche_id, fautes)`.

    `ref` et `fiche_id` sont rendus même en cas de faute quand ils sont lisibles :
    la couverture du lot (`B1`) doit pouvoir se prononcer sur un fichier fautif
    plutôt que de le traiter comme absent.
    """
    fautes: list[str] = []
    m = RE_REF.match(chemin.name)
    ref = m.group(1) if m else None
    if not ref:
        fautes.append(f"A1 {chemin.name} : le nom doit être `H<NN>-<slug>.md`")

    texte = chemin.read_text(encoding="utf-8")
    champs = lire_entete(texte)
    for c in CHAMPS_REQUIS:
        if c not in champs:
            fautes.append(f"A1 {chemin.name} : champ d'en-tête `{c}` absent")

    fiche_id = premier_backtick(champs.get("fiche", "")) if "fiche" in champs else None
    signal_id = premier_backtick(champs.get("signal", "")) if "signal" in champs else None
    if fiche_id is None:
        fautes.append(f"A2 {chemin.name} : `fiche` ne nomme aucun `fiche_id` entre accents graves")
    elif fiche_id not in fiches:
        fautes.append(
            f"A2 {chemin.name} : la fiche `{fiche_id}` n'existe sur aucun disque de "
            "`corpus/fiches/` ni `corpus/fiches_harvest/` — une hypothèse sans fiche "
            "n'a pas de source"
        )
    if signal_id is None:
        fautes.append(f"A2 {chemin.name} : `signal` ne nomme aucun `signal_id`")
    elif fiche_id is not None and signal_id != fiche_id:
        fautes.append(
            f"A2 {chemin.name} : `signal` = `{signal_id}` mais `fiche` = `{fiche_id}` — "
            "`D40` fixe la convention `signal_id` = `fiche_id`, et `gate_09` apparie "
            "les lignes du registre sur `signal_id`"
        )

    signe = None
    brut_signe = champs.get("signe attendu", "")
    n = normaliser_nombre(brut_signe)
    if n in (1.0, -1.0):
        signe = int(n)
    else:
        fautes.append(
            f"A3 {chemin.name} : `signe attendu` = {brut_signe!r} ; `D25` `C1` n'admet "
            "que `+1` ou `−1`"
        )

    tranche = champs.get("tranche", "")
    if TRANCHE_REQUISE not in tranche or ASOF_REQUIS not in tranche:
        fautes.append(
            f"A4 {chemin.name} : `tranche` doit porter `{TRANCHE_REQUISE}` et "
            f"l'as-of exact de `D29` ({ASOF_REQUIS}) ; lu {tranche!r}"
        )

    sections = lire_sections(texte)
    titres = [t for t, _ in sections]
    presentes = [t for t in titres if t in SECTIONS_REQUISES]
    if presentes != list(SECTIONS_REQUISES):
        manquantes = [s for s in SECTIONS_REQUISES if s not in titres]
        if manquantes:
            fautes.append(f"A5 {chemin.name} : section(s) absente(s) : {manquantes}")
        else:
            fautes.append(
                f"A5 {chemin.name} : les six sections de `D40` ne sont pas dans "
                f"l'ordre — lu {presentes}"
            )
    corps = dict(sections)
    for titre in SECTIONS_REQUISES:
        if titre in corps and not corps[titre].strip():
            fautes.append(f"A5 {chemin.name} : section « {titre} » vide")

    # A6 — les chiffres du papier se rattachent à la fiche, ou n'existent pas.
    table = corps.get(SECTION_PAPIER, "")
    if fiche_id in fiches:
        attendus = resultats_de_la_fiche(fiches[fiche_id])
        lignes = [
            ligne.strip()
            for ligne in table.splitlines()
            if ligne.strip().startswith("|") and ligne.strip().count("|") >= 3
        ]
        nomme_aucun = re.search(r"\baucun\b", table, re.IGNORECASE) is not None
        rattachements = 0
        for ligne in lignes:
            cells = [c.strip() for c in ligne.strip("|").split("|")]
            nom = premier_backtick(cells[0]) or cells[0]
            if (
                not nom
                or set(nom) <= set("-—: ")
                or nom.casefold() in ("résultat", "resultat", "aucun")
            ):
                continue  # en-tête, filet de la table, ou le `aucun` explicite
            rattachements += 1
            if nom not in attendus:
                fautes.append(
                    f"A6 {chemin.name} : `{nom}` n'est pas une entrée de "
                    f"`reported_results` de la fiche `{fiche_id}` — un chiffre du "
                    "papier absent de la fiche est un chiffre inventé"
                )
                continue
            if len(cells) < 2:
                continue
            attendu, lu = attendus[nom], normaliser_nombre(cells[1])
            if attendu is None:
                if lu is not None:
                    fautes.append(
                        f"A6 {chemin.name} : `{nom}` vaut `null` dans la fiche et {lu} ici"
                    )
            elif lu is None or abs(float(attendu) - lu) > 1e-9 * max(1.0, abs(float(attendu))):
                fautes.append(
                    f"A6 {chemin.name} : `{nom}` vaut {attendu} dans la fiche et "
                    f"{cells[1]!r} ici"
                )
        if rattachements == 0 and not nomme_aucun:
            fautes.append(
                f"A6 {chemin.name} : « {SECTION_PAPIER} » ne rattache aucun chiffre et "
                "n'écrit pas `aucun` — un silence ne passe pas pour une absence (`L05`)"
            )

    # A7 — la falsifiabilité est comptée, pas promise.
    contre = corps.get(SECTION_CONTREDIT, "")
    clauses = [ligne for ligne in contre.splitlines() if ligne.strip().startswith(("- ", "* "))]
    if len(clauses) < 2:
        fautes.append(
            f"A7 {chemin.name} : « {SECTION_CONTREDIT} » porte {len(clauses)} clause(s) ; "
            "`D40` en exige au moins deux"
        )
    if not re.search(r"\d", contre):
        fautes.append(
            f"A7 {chemin.name} : « {SECTION_CONTREDIT} » ne porte aucun nombre — une "
            "hypothèse qu'aucun chiffre ne peut contredire ne mérite pas un test"
        )

    # B2 — le signe concorde avec le signal, dès que celui-ci existe.
    if signal_id is not None and signe is not None:
        signe_module = signes_signaux.get(signal_id)
        if signe_module is not None and signe_module != signe:
            fautes.append(
                f"B2 {chemin.name} : l'hypothèse pré-enregistre {signe:+d} et "
                f"`signals/` déclare EXPECTED_SIGN = {signe_module:+d} — `gate_09` "
                "lirait le second, donc le `p` unilatéral porterait sur un signe "
                "que personne n'a pré-enregistré"
            )

    return ref, fiche_id, fautes


def juger_ensemble(
    dossier: Path,
    fiche_ids_du_lot: list[str],
    fiches: dict[str, dict] | None = None,
    signes_signaux: dict[str, int | None] | None = None,
) -> tuple[dict[str, str], list[str]]:
    """Juge tous les fichiers `H<NN>-*.md` d'un dossier. Rend `(fiche_id -> ref, fautes)`."""
    fiches = charger_fiches() if fiches is None else fiches
    du_lot = set(fiche_ids_du_lot)
    if signes_signaux is None:
        signes_signaux = {f: signe_du_signal(f) for f in du_lot}

    fautes: list[str] = []
    par_ref: dict[str, Path] = {}
    liens: dict[str, str] = {}
    for chemin in sorted(dossier.glob("H*.md")):
        m = RE_REF.match(chemin.name)
        if m and m.group(1) in REFS_AVANT_D33:
            continue  # écrite avant `D40`, hors de son périmètre
        ref, fiche_id, f = juger_fichier(chemin, fiches, signes_signaux)
        if fiche_id is not None and fiche_id in ecartees_du_lot():
            continue  # D41 : écartée avant mesure, son hypothèse reste pour mémoire
        if fiche_id is not None and fiche_id not in du_lot:
            fautes.append(
                f"B1 {chemin.name} : la fiche `{fiche_id}` n'est pas au lot — une "
                "hypothèse de la phase 09 porte sur une fiche du lot clos (`D25` `C2`)"
            )
            continue
        fautes.extend(f)
        if ref is not None:
            if ref in par_ref:
                fautes.append(
                    f"A1 {chemin.name} : la `ref` {ref} est déjà portée par "
                    f"{par_ref[ref].name} — deux hypothèses ne partagent pas un numéro"
                )
            par_ref[ref] = chemin
        if fiche_id is not None and ref is not None:
            if fiche_id in liens:
                fautes.append(
                    f"B1 {chemin.name} : la fiche `{fiche_id}` a déjà l'hypothèse "
                    f"{liens[fiche_id]} — une fiche du lot porte exactement une hypothèse"
                )
            else:
                liens[fiche_id] = ref

    for fiche_id in fiche_ids_du_lot:
        if fiche_id not in liens:
            fautes.append(
                f"B1 : la fiche `{fiche_id}` est au lot et n'a aucune hypothèse écrite "
                "(invariant IV)"
            )
    return liens, fautes


def ecartees_du_lot() -> set[str]:
    """Les fiches sorties du lot AVANT mesure (`D34`, `D38`), écart daté et motivé.

    `D41` : une hypothèse au format de `D40` peut précéder le codage ; si la fiche
    s'écarte ensuite (codage discordant, marché absent), son hypothèse n'est ni
    supprimée ni réécrite — elle reste, et ne compte plus dans la bijection `B1`.
    """
    if not LOT_FILE.is_file():
        return set()
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    return {e["fiche_id"] for e in lot.get("ecartees_codage") or []}


def fiche_ids_du_lot() -> list[str]:
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    entrees = lot.get("fiches") or lot.get("hypotheses") or []
    return [e["fiche_id"] for e in entrees]


def lier(liens: dict[str, str]) -> int:
    """Inscrit `ref` et `signal_id` dans le lot, dérivés des fichiers d'hypothèse.

    `F54` impose ce sens : `corpus/lot_phase09.py --ecrire` ne connaît que
    `fiche_id`, `verdict` et `motif`, donc un `ref` écrit à la main dans le lot
    serait détruit en silence au prochain passage. La source de vérité est le
    fichier d'hypothèse ; cette fonction ne fait que reconstruire le reflet, et
    elle ne touche à **rien** d'autre.
    """
    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    entrees = lot.get("fiches") or []
    manquants = [e["fiche_id"] for e in entrees if e["fiche_id"] not in liens]
    if manquants:
        print(f"REFUS : {len(manquants)} fiche(s) du lot sans hypothèse — rien n'est écrit.")
        return 1
    for e in entrees:
        e["ref"] = liens[e["fiche_id"]]
        e["signal_id"] = e["fiche_id"]
    LOT_FILE.write_text(json.dumps(lot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  {len(entrees)} entrée(s) du lot portent désormais leur `ref` et leur `signal_id`.")
    print("  Le lot n'a ni gagné ni perdu une fiche : `D25` `C2` est intact.")
    return 0


GABARIT = """# {ref} — un titre

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `{fiche}` (`corpus/fiches/{fiche}.json`)
**signal :** `{fiche}` — *non encore codé*
**signe attendu :** {signe}
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** auto-test de `score_hypothese.py`
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

Quelque chose.

## Le domaine

Les 25 cellules.

## Ce qui est attendu, en chiffres

Un IC positif.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
{table}

## Ce qui la contredirait

{contredit}

## Ce qui n'est pas affirmé ici

Le reste.
"""


def run_check() -> int:
    """Auto-test sur des fichiers FABRIQUÉS. Ne lit ni le lot ni les vraies fiches."""
    verifs: list[tuple[str, bool]] = []

    def verifier(nom: str, condition: bool) -> None:
        verifs.append((nom, bool(condition)))

    fiche_fictive = {
        "fiche_id": "papier-fictif",
        "reported_results": [
            {"name": "alpha_mensuel_pct", "value": 1.4},
            {"name": "observations", "value": 454825},
            {"name": "remarque_qualitative", "value": None},
        ],
    }
    fiches = {"papier-fictif": fiche_fictive}
    contredit_ok = "- Un IC négatif au-delà de 2 en `t`.\n- Un `t` final sous 2."
    table_ok = "| `alpha_mensuel_pct` | 1.4 |"

    def ecrire(dossier: Path, nom: str, **kw) -> Path:
        base = {"ref": nom.split("-")[0], "fiche": "papier-fictif", "signe": "+1",
                "table": table_ok, "contredit": contredit_ok}
        base.update(kw)
        texte = GABARIT.format(**base)
        for vieux, neuf in kw.pop("remplacements", {}).items():
            texte = texte.replace(vieux, neuf)
        chemin = dossier / nom
        chemin.write_text(texte, encoding="utf-8")
        return chemin

    def fautes_de(nom: str, **kw) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            dossier = Path(tmp)
            remplacements = kw.pop("remplacements", {})
            chemin = ecrire(dossier, nom, **kw)
            if remplacements:
                texte = chemin.read_text(encoding="utf-8")
                for vieux, neuf in remplacements.items():
                    texte = texte.replace(vieux, neuf)
                chemin.write_text(texte, encoding="utf-8")
            _, _, f = juger_fichier(chemin, fiches, {"papier-fictif": None})
            return f

    verifier("une hypothèse bien formée passe les sept conditions", fautes_de("H99-bonne.md") == [])

    cas = {
        "A1 — nom de fichier hors gabarit": ("h99_bonne.md", {}),
        "A1 — un champ d'en-tête absent": (
            "H99-bonne.md", {"remplacements": {"**Statut :**": "**Etat :**"}}),
        "A2 — fiche inexistante": ("H99-bonne.md", {"fiche": "papier-absent"}),
        "A2 — signal different de la fiche": (
            "H99-bonne.md",
            {"remplacements": {"**signal :** `papier-fictif`": "**signal :** `autre-signal`"}}),
        "A3 — signe ni +1 ni −1": ("H99-bonne.md", {"signe": "+2"}),
        "A3 — signe absent": ("H99-bonne.md", {"signe": "à déterminer"}),
        "A4 — as-of autre que celui de D29": (
            "H99-bonne.md", {"remplacements": {"2023-12-29 20:00 UTC": "2019-12-31 20:00 UTC"}}),
        "A4 — tranche autre que `pool`": (
            "H99-bonne.md", {"remplacements": {"**tranche :** `pool`": "**tranche :** `holdout`"}}),
        "A5 — une section absente": (
            "H99-bonne.md", {"remplacements": {"## Le domaine": "## Le perimetre"}}),
        "A5 — une section vide": (
            "H99-bonne.md", {"remplacements": {"Les 25 cellules.": ""}}),
        "A6 — un chiffre du papier absent de la fiche": (
            "H99-bonne.md", {"table": "| `alpha_invente_pct` | 9.9 |"}),
        "A6 — un chiffre de la fiche recopié faux": (
            "H99-bonne.md", {"table": "| `alpha_mensuel_pct` | 1.5 |"}),
        "A6 — un `null` de la fiche chiffré ici": (
            "H99-bonne.md", {"table": "| `remarque_qualitative` | 3.0 |"}),
        "A6 — aucun rattachement et pas de `aucun`": (
            "H99-bonne.md", {"table": "| | |"}),
        "A7 — une seule clause de falsification": (
            "H99-bonne.md", {"contredit": "- Un `t` final sous 2."}),
        "A7 — aucune clause chiffrée": (
            "H99-bonne.md",
            {"contredit": "- Un IC négatif.\n- Un IC nul."}),
    }
    for nom, (fichier, kw) in cas.items():
        verifier(f"refuse {nom}", fautes_de(fichier, **kw) != [])

    # A6 — `aucun` écrit explicitement est la seule façon de ne rattacher aucun chiffre.
    verifier(
        "A6 — `aucun`, écrit en clair, est accepté",
        fautes_de("H99-bonne.md", table="| `aucun` — le papier ne donne aucun chiffre | — |") == [],
    )
    # Un séparateur de milliers ne doit pas faire refuser une valeur juste (`L28`).
    verifier(
        "A6 — `454,825` vaut 454825, pas un refus",
        fautes_de("H99-bonne.md", table="| `observations` | 454,825 |") == [],
    )
    # Le signe moins typographique est celui du corpus (`D09` § Journal).
    verifier(
        "A3 — le signe `−1` typographique est lu comme −1",
        fautes_de("H99-moins.md", signe="−1") == [],
    )

    # B2 — la concordance avec le signal, sans importer aucun module réel.
    with tempfile.TemporaryDirectory() as tmp:
        chemin = ecrire(Path(tmp), "H99-bonne.md")
        _, _, f_ok = juger_fichier(chemin, fiches, {"papier-fictif": +1})
        _, _, f_ko = juger_fichier(chemin, fiches, {"papier-fictif": -1})
    verifier("B2 — un signal du même signe passe", f_ok == [])
    verifier("B2 — refuse un signal dont EXPECTED_SIGN contredit l'hypothèse", f_ko != [])

    # B1 — la bijection avec le lot, sur un lot fabriqué.
    with tempfile.TemporaryDirectory() as tmp:
        dossier = Path(tmp)
        ecrire(dossier, "H99-bonne.md")
        liens, f = juger_ensemble(dossier, ["papier-fictif"], fiches, {"papier-fictif": None})
        verifier("B1 — un lot d'une fiche couverte par une hypothèse passe",
                 f == [] and liens == {"papier-fictif": "H99"})
        liens2, f2 = juger_ensemble(
            dossier, ["papier-fictif", "papier-sans-hypothese"], fiches,
            {"papier-fictif": None, "papier-sans-hypothese": None})
        verifier("B1 — refuse une fiche du lot sans hypothèse", f2 != [])
        ecrire(dossier, "H98-doublon.md")
        _, f3 = juger_ensemble(dossier, ["papier-fictif"], fiches, {"papier-fictif": None})
        verifier("B1 — refuse deux hypothèses sur la même fiche du lot", f3 != [])
    with tempfile.TemporaryDirectory() as tmp:
        dossier = Path(tmp)
        ecrire(dossier, "H99-bonne.md")
        ecrire(dossier, "H99-autre.md")
        _, f4 = juger_ensemble(dossier, ["papier-fictif"], fiches, {"papier-fictif": None})
        verifier("A1 — refuse deux fichiers portant la même `ref`", f4 != [])
    # `H01`-`H04` précèdent `D40` et ne se jugent pas sur elle ; toute autre
    # hypothèse doit nommer une fiche du lot, et être refusée sinon.
    with tempfile.TemporaryDirectory() as tmp:
        dossier = Path(tmp)
        ecrire(dossier, "H01-ancienne.md", signe="+2")  # fautive, mais antérieure à D40
        _, f5 = juger_ensemble(dossier, [], fiches, {})
        verifier("une hypothèse antérieure à `D40` est ignorée, pas refusée", f5 == [])
    with tempfile.TemporaryDirectory() as tmp:
        dossier = Path(tmp)
        ecrire(dossier, "H99-hors-lot.md")
        _, f6 = juger_ensemble(dossier, [], fiches, {})
        verifier("B1 — refuse une hypothèse dont la fiche n'est pas au lot", f6 != [])

    for nom, ok in verifs:
        print(f"  {'OK' if ok else 'ECHEC'}  {nom}")
    echoues = [nom for nom, ok in verifs if not ok]
    print(f"\n{len(verifs)} vérifications, {len(echoues)} échec(s)")
    print("\nCeci n'a jugé aucune hypothèse réelle : ni le lot ni les fiches du dépôt")
    print("n'ont été lus, et le registre n'est jamais ouvert.")
    return 1 if echoues else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le juge des hypothèses du lot 09 — D40")
    ap.add_argument("--check", action="store_true", help="auto-test, NE JUGE RIEN de réel")
    ap.add_argument("--lier", action="store_true", help="inscrit `ref`/`signal_id` dans le lot")
    a = ap.parse_args(argv)

    if a.check:
        return run_check()

    ids = fiche_ids_du_lot()
    liens, fautes = juger_ensemble(HYPOTHESES_DIR, ids)
    ecrites = len(liens)
    print(f"LOT 09 : {len(ids)} fiches, {ecrites} hypothèse(s) écrite(s)\n")
    if fautes:
        for f in fautes[:60]:
            print(f"  - {f}")
        if len(fautes) > 60:
            print(f"  … et {len(fautes) - 60} autre(s)")
        print(f"\n{len(fautes)} faute(s) — les sept conditions de `D40` sont à tolérance zéro.")
        return 1
    print("  les sept conditions de `D40` tiennent, et la bijection avec le lot est faite.")
    if a.lier:
        return lier(liens)
    print("  `--lier` inscrira `ref` et `signal_id` dans hypotheses/LOT-09.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
