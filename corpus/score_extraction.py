"""Le juge de l'extraction. Il confronte une fiche produite au TEXTE de son papier.

Écrit **avant** l'extracteur, et vérifié contre des fiches fabriquées — l'ordre
de construction de `CLAUDE.md` appliqué à l'intérieur de la phase 07, comme
`score_triage.py` l'a fait pour le trieur.

Ce qu'il juge n'est pas la ressemblance à une fiche de référence — il n'y en a
que trois, et `D16` dit pourquoi un seuil sur trois items ne veut rien dire —
mais la **fidélité à la source** : chaque `quoted` doit se retrouver mot pour mot
dans le papier. `D14` vérifiait déjà qu'une `value` se retrouve dans sa
`quoted` ; il manquait que la `quoted` existe. Un extracteur qui fabrique la
citation *et* le chiffre passait `D14` sans une faute.

Les cinq conditions de `D16`, toutes à tolérance ZÉRO, valent ENSEMBLE :

    F1  la fiche passe validate_fiches.py (le schéma de D14)
    F2  chaque citation est mot pour mot dans le texte du papier — `quoted`,
        ou `quoted_source` quand une réparation est déclarée et nommée
    F3  chaque `value` numérique est dans la citation QUI FAIT FOI (sauf
        derived/spelled_out)
    F4  `source.pdf` désigne un fichier présent, `source_url` est une URL
    F5  aucune CONTRADICTION factuelle avec la fiche de référence, s'il en existe

Et ce qui est imprimé sans rien conditionner — les résultats de la référence que
la fiche produite a laissés de côté, les champs de prose côte à côte, le compte
des `null`. `L06` : un compte juste n'est pas un compte de choses justes.

    python corpus/score_extraction.py --check
    python corpus/score_extraction.py <fiche.json> <texte.txt> [--ref <reference.json>]

Code de sortie 1 si la porte n'est pas franchie, ou si l'entrée est malformée.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Les champs FACTUELS de F5, limitativement. D16 § Les cinq conditions :
# tout le reste est de la prose, imprimée côte à côte et jamais comptée.
FACTUAL = ("source.year", "source.amorce_entry", "source.peer_reviewed", "horizon.value")

# Les champs de prose, imprimés par le diagnostic et conditionnant RIEN.
PROSE = ("claim", "universe", "signal_construction", "what_is_missing")

NUMBER = re.compile(r"-?\d+(?:[.,]\d+)?")


class InputError(RuntimeError):
    """L'entrée est malformée. On ne note pas."""


# --------------------------------------------------------------------------
# La normalisation de F2, écrite dans D16 parce qu'elle décide de ce qui passe.
# Espaces repliés, tirets et guillemets ramenés à leur forme simple, casse
# ignorée. Elle ne va PAS plus loin : une citation dont les mots diffèrent est
# introuvable, et c'est voulu — une paraphrase n'est pas une citation.
# --------------------------------------------------------------------------

_DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")
_QUOTES = dict.fromkeys(map(ord, "‘’‚‛′"), "'")
_DQUOTES = dict.fromkeys(map(ord, "“”„‟″«»"), '"')


def normalize(text: str) -> str:
    """Replie une chaîne à la forme sur laquelle F2 compare."""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_DASHES).translate(_QUOTES).translate(_DQUOTES)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def value_in_quote(value: float | int, quoted: str) -> bool:
    """Le nombre se retrouve-t-il dans la citation, séparateurs ôtés ?

    Comparaison NUMÉRIQUE et non par sous-chaîne : `scripts/check_provenance.py`
    a pris ce garde en défaut sur `12500` contre « 12,500,000 » (`D09`).
    """
    for raw in NUMBER.findall(quoted.replace(",", "").replace(" ", "").replace(" ", "")):
        try:
            if abs(float(raw.replace(",", ".")) - float(value)) < 1e-9:
                return True
        except ValueError:
            continue
    return False


def dotted(fiche: dict, path: str):
    """Lit `a.b` dans un dict imbriqué. Renvoie None si le chemin n'existe pas."""
    node = fiche
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


# --------------------------------------------------------------------------
# Les cinq conditions
# --------------------------------------------------------------------------


def check_f1(fiche_path: Path) -> list[str]:
    """F1 — la fiche passe le schéma de D14.

    `validate_fiches.py` est importé plutôt que réécrit : deux implémentations
    d'un même schéma divergent, et c'est lui qui fait foi.
    """
    sys.path.insert(0, str(REPO / "corpus"))
    try:
        import validate_fiches  # type: ignore
    finally:
        sys.path.pop(0)
    fiche = json.loads(fiche_path.read_text(encoding="utf-8"))
    return validate_fiches.check_fiche(fiche_path.stem, fiche)


# Les raisons pour lesquelles le texte EXTRAIT peut différer du papier LU, et
# qui autorisent un `quoted_source`. Liste CLOSE — `D09` a la même discipline
# pour les valeurs externes : une échappatoire nommée, jamais une échappatoire
# générique. Aucune de ces raisons n'autorise une PARAPHRASE.
REPAIRS = {
    "ocr": "le PDF est un scan et son texte est corrompu",
    "math_notation": "le papier écrit un symbole que l'extraction ne rend pas",
    "table": "la citation vient d'un tableau, lu en cellules par l'extraction",
}


def anchor(res: dict) -> str:
    """La chaîne que F2 cherche dans le texte : `quoted_source` s'il existe.

    Quand le texte extrait ne dit pas ce que le papier dit — scan corrompu,
    notation mathématique perdue, tableau mis à plat — la fiche porte DEUX
    chaînes : `quoted`, lisible, et `quoted_source`, mot pour mot dans le texte.
    La seconde est celle que F2 vérifie, et `quoted_repair` nomme pourquoi les
    deux diffèrent. C'est le geste de `D14` avec `spelled_out` : on NOMME la
    réparation humaine au lieu de la cacher.
    """
    return res.get("quoted_source") or res.get("quoted") or ""


def check_f2(fiche: dict, source_text: str) -> list[str]:
    """F2 — chaque citation est mot pour mot dans le texte du papier.

    Une réparation déclarée déplace ce qui est cherché, jamais ce qui est exigé :
    il faut toujours UNE chaîne présente à la lettre dans le texte. Une
    paraphrase n'en fournit aucune, et c'est précisément ce que F2 attrape.
    """
    haystack = normalize(source_text)
    faults = []
    for i, res in enumerate(fiche.get("reported_results") or []):
        name = res.get("name", f"#{i}")
        needle = anchor(res)
        if not isinstance(needle, str) or not needle.strip():
            faults.append(f"`{name}` : `quoted` absente ou vide")
            continue

        repair = res.get("quoted_repair")
        if res.get("quoted_source"):
            if repair not in REPAIRS:
                faults.append(
                    f"`{name}` : `quoted_source` sans `quoted_repair` valide "
                    f"— attendu l'un de {sorted(REPAIRS)}, reçu {repair!r}"
                )
                continue
        elif repair:
            faults.append(f"`{name}` : `quoted_repair` déclaré sans `quoted_source`")
            continue

        # Une citation coupée par « … » se vérifie morceau par morceau : chaque
        # fragment doit être dans le texte, et dans l'ordre. C'est la forme
        # qu'emploient les trois fiches de référence.
        fragments = [f for f in re.split(r"\s*(?:\.\.\.|…)\s*", needle) if f.strip()]
        cursor = 0
        for frag in fragments:
            pos = haystack.find(normalize(frag), cursor)
            if pos < 0:
                short = frag.strip()[:70]
                faults.append(f"`{name}` : citation INTROUVABLE dans le papier — « {short}… »")
                break
            cursor = pos + len(normalize(frag))
    return faults


def check_f3(fiche: dict) -> list[str]:
    """F3 — chaque `value` numérique est dans sa `quoted`.

    Rejoué ici bien que `validate_fiches` le porte : F1 et F3 sont deux
    conditions distinctes de `D16`, et une porte qui délègue toutes ses clauses
    à une seule ne dit plus laquelle a cassé.
    """
    faults = []
    for i, res in enumerate(fiche.get("reported_results") or []):
        name = res.get("name", f"#{i}")
        # La chaîne qui fait foi est celle que F2 a trouvée dans le papier. Sans
        # cela, une réparation déclarée deviendrait un endroit où loger un
        # chiffre que le papier ne porte pas.
        value, quoted = res.get("value"), anchor(res)
        if res.get("derived"):
            continue
        if spelled := res.get("spelled_out"):
            if normalize(str(spelled)) not in normalize(quoted):
                faults.append(f"`{name}` : `spelled_out` « {spelled} » absent de la citation")
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        if not value_in_quote(value, quoted):
            faults.append(f"`{name}` : la valeur {value} ne se retrouve PAS dans sa citation")
    return faults


def check_f4(fiche: dict, repo: Path = REPO) -> list[str]:
    """F4 — le PDF désigné existe, et `source_url` est une adresse."""
    faults = []
    source = fiche.get("source") or {}
    pdf = source.get("pdf")
    if not pdf:
        faults.append("`source.pdf` absent — la fiche ne dit pas de quel fichier elle vient")
    elif not (repo / pdf).is_file():
        faults.append(f"`source.pdf` désigne un fichier ABSENT : {pdf}")
    url = source.get("source_url") or ""
    if not re.match(r"^https?://\S+$", str(url)):
        faults.append(f"`source.source_url` n'est pas une URL : {url!r}")
    return faults


def check_f5(fiche: dict, ref: dict | None) -> list[str]:
    """F5 — aucune CONTRADICTION factuelle avec la référence.

    L'absence n'est pas une contradiction (`D16`) : une fiche muette là où la
    référence parle est plus pauvre, ce que le diagnostic dira. F5 n'attrape que
    deux valeurs PRÉSENTES et incompatibles.
    """
    if ref is None:
        return []
    faults = []
    for path in FACTUAL:
        mine, theirs = dotted(fiche, path), dotted(ref, path)
        if mine is None or theirs is None:
            continue
        if mine != theirs:
            faults.append(f"`{path}` : {mine!r} contre {theirs!r} dans la référence")
    return faults


# --------------------------------------------------------------------------
# Le diagnostic — imprimé, jamais compté
# --------------------------------------------------------------------------


def diagnose(fiche: dict, ref: dict | None) -> dict:
    """Ce que L06 exige de voir, et que les cinq conditions ne portent pas."""
    names = {r.get("name") for r in (fiche.get("reported_results") or [])}
    out: dict = {
        "n_results": len(fiche.get("reported_results") or []),
        "repairs": [
            (r.get("name"), r.get("quoted_repair"))
            for r in (fiche.get("reported_results") or [])
            if r.get("quoted_source")
        ],
        "n_null": sum(
            1
            for f in ("horizon", "signal_construction")
            if isinstance(fiche.get(f), dict) and fiche[f].get("value") is None
        ),
        "missed": [],
        "extra": [],
        "prose": [],
    }
    if ref is not None:
        ref_names = {r.get("name") for r in (ref.get("reported_results") or [])}
        out["missed"] = sorted(n for n in ref_names - names if n)
        out["extra"] = sorted(n for n in names - ref_names if n)
        for field in PROSE:
            out["prose"].append((field, fiche.get(field), ref.get(field)))
    return out


def score(fiche_path: Path, source_text: str, ref: dict | None) -> dict:
    fiche = json.loads(fiche_path.read_text(encoding="utf-8"))
    conditions = {
        "F1": check_f1(fiche_path),
        "F2": check_f2(fiche, source_text),
        "F3": check_f3(fiche),
        "F4": check_f4(fiche),
        "F5": check_f5(fiche, ref),
    }
    return {
        "conditions": conditions,
        "passed": all(not v for v in conditions.values()),
        "diagnostic": diagnose(fiche, ref),
        "has_reference": ref is not None,
    }


LABELS = {
    "F1": "la fiche passe le schéma de D14",
    "F2": "chaque `quoted` est mot pour mot dans le papier",
    "F3": "chaque `value` numérique est dans sa citation",
    "F4": "le PDF désigné existe, `source_url` est une URL",
    "F5": "aucune contradiction factuelle avec la référence",
}


def render(result: dict) -> str:
    lines = ["", "Les cinq conditions de D16 — toutes a tolerance ZERO, elles valent ENSEMBLE", ""]
    for key in ("F1", "F2", "F3", "F4", "F5"):
        faults = result["conditions"][key]
        if key == "F5" and not result["has_reference"]:
            lines.append(f"  {key} : sans objet — aucune fiche de reference fournie")
            continue
        mark = "tenue" if not faults else f"CASSEE ({len(faults)})"
        lines.append(f"  {key} : {mark} — {LABELS[key]}")
        lines.extend(f"         - {f}" for f in faults)

    diag = result["diagnostic"]
    lines += ["", "Diagnostic — imprime, ne conditionne RIEN (D16, L06)", ""]
    lines.append(f"  resultats rapportes : {diag['n_results']}")
    lines.append(f"  champs a null justifie : {diag['n_null']} sur 2")
    if diag["repairs"]:
        lines.append(f"  citations REPAREES, et pourquoi : {diag['repairs']}")
    if result["has_reference"]:
        lines.append(f"  resultats de la reference LAISSES DE COTE : {diag['missed'] or 'aucun'}")
        lines.append(f"  resultats absents de la reference : {diag['extra'] or 'aucun'}")
        lines.append("")
        lines.append("  Les champs de prose, cote a cote — a lire, jamais a compter :")
        for field, mine, theirs in diag["prose"]:
            lines.append(f"    [{field}]")
            lines.append(f"      produite  : {str(mine)[:150]}")
            lines.append(f"      reference : {str(theirs)[:150]}")

    lines += [""]
    if result["passed"]:
        lines.append("EXTRACTION : les cinq conditions de D16 tiennent.")
        lines.append("Le verdict de la porte cite le NUMERO DU PASSAGE (D16 § Journal).")
        lines.append("Ce que ce juge NE dit PAS : que la fiche retienne ce qui compte.")
    else:
        broken = [k for k, v in result["conditions"].items() if v]
        lines.append(f"EXTRACTION : NON FRANCHIE — {', '.join(broken)}.")
        lines.append("Un echec ne s'achete pas en redefinissant le seuil (D13, option 2).")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Le juge se teste lui-même, sur des fiches FABRIQUÉES.
# Aucune n'est tirée d'une fiche de référence : L17, et D16 § Qui peut être
# l'extracteur. Le papier fictif ci-dessous n'existe pas.
# --------------------------------------------------------------------------

PAPER = """
    Section 4. Results.
    We document a pronounced U-shaped pattern, with realized variance
    starting out at 0.095% in the morning, falling to 0.041% around noon,
    and rising to 0.102% towards the end of the trading day.
    Seven of the strategies fail to survive transaction costs.
    The effect is strongest on announcement days.
    We note a tendency for the fight part of the pattern to rise.
"""
# La dernière ligne porte une faute d'OCR délibérée — « fight » pour « right ».
# Elle vient du cas réel : le scan d'Andersen & Bollerslev (1997) la produit
# telle quelle, et la fiche écrite à la main citait le mot correct.


def _fiche(**over) -> dict:
    base = {
        "fiche_id": "fictif-2099-banc-d-essai",
        "written": "2026-09-20",
        "written_by": "score_extraction.py --check",
        "claim": "La variance realisee suit une forme en U au cours de la seance.",
        "universe": "un contrat fictif, 2099",
        "horizon": {"value": "30 minutes"},
        "signal_construction": {"value": "variance realisee par demi-heure"},
        "what_is_missing": ["tout : ce papier n'existe pas"],
        "reported_results": [
            {
                "name": "morning_rv",
                "value": 0.095,
                "unit": "%",
                "quoted": "starting out at 0.095% in the morning",
            },
            {
                "name": "n_failing",
                "spelled_out": "Seven",
                "value": None,
                "quoted": "Seven of the strategies fail to survive transaction costs",
            },
            {
                "name": "peak_over_trough",
                "value": 2.49,
                "derived": True,
                "quoted": "0.102% towards the end",
                "note": "0,102 / 0,041, calcule par nous",
            },
        ],
        "source": {
            "authors": "Personne",
            "title": "Un papier qui n'existe pas",
            "year": 2099,
            "source_url": "https://example.invalid/fictif.pdf",
            "pdf": "corpus/pdf/.gitkeep",
            "retrieved": "2026-09-20",
            "peer_reviewed": False,
            "amorce_entry": 99,
        },
        "transposability": {
            "what_transfers": "rien, le papier est fictif",
            "what_does_not_transfer": ["tout"],
            "what_aligns_well": "rien",
        },
    }
    base.update(over)
    return base


def self_check() -> int:
    """Le juge doit REFUSER ce qu'il est écrit pour refuser. Sinon il ne garde rien."""
    checks, failures = 0, []

    def case(label: str, fiche: dict, expect_pass: bool, expect_broken=None, ref=None):
        """Une faute, et les conditions qu'elle DOIT casser — pas une de plus.

        `expect_broken` peut nommer plusieurs conditions : F1 recouvre F3 par
        construction, `D16` l'assume, et une porte qui ne dit pas laquelle a
        casse ne dit plus rien.
        """
        nonlocal checks
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fictif-2099-banc-d-essai.json"
            path.write_text(json.dumps(fiche, ensure_ascii=False), encoding="utf-8")
            result = score(path, PAPER, ref)
        checks += 1
        if result["passed"] != expect_pass:
            failures.append(
                f"{label} : attendu {'passe' if expect_pass else 'refuse'}, obtenu l'inverse"
            )
            return
        if expect_broken:
            expected = [expect_broken] if isinstance(expect_broken, str) else list(expect_broken)
            broken = [k for k, v in result["conditions"].items() if v]
            checks += 1
            if broken != expected:
                failures.append(f"{label} : attendu {expected} cassee(s), obtenu {broken}")

    # La fiche intacte passe. Sans elle, tous les refus ci-dessous ne prouvent rien.
    case("fiche intacte", _fiche(), True)

    # F2 — le coeur de D16 : la citation fabriquee.
    bad = _fiche()
    bad["reported_results"] = [
        {"name": "invente", "value": 0.095, "quoted": "we find a 0.095% effect at the open"}
    ]
    case("F2 citation ABSENTE du papier", bad, False, "F2")

    # Une paraphrase n'est pas une citation, meme si elle dit vrai.
    bad = _fiche()
    bad["reported_results"] = [
        {"name": "paraphrase", "value": 0.095, "quoted": "the morning value is 0.095%"}
    ]
    case("F2 paraphrase fidele mais non citee", bad, False, "F2")

    # La normalisation doit laisser passer tirets, guillemets et espaces.
    ok = _fiche()
    ok["reported_results"] = [
        {"name": "typo", "value": 0.095, "quoted": "starting   out  at 0.095%  in the morning"}
    ]
    case("F2 espaces multiples tolerés", ok, True)

    # Une citation coupee se verifie fragment par fragment, DANS L'ORDRE.
    ok = _fiche()
    ok["reported_results"] = [
        {"name": "coupee", "value": 0.041, "quoted": "falling to 0.041% … towards the end"}
    ]
    case("F2 citation coupee, fragments dans l'ordre", ok, True)

    bad = _fiche()
    bad["reported_results"] = [
        {"name": "desordre", "value": 0.041, "quoted": "towards the end … falling to 0.041%"}
    ]
    case("F2 fragments DANS LE DESORDRE", bad, False, "F2")

    # F2, la réparation déclarée. Le texte extrait dit « fight », le papier dit
    # « right » : la fiche porte les deux, et NOMME pourquoi.
    ok = _fiche()
    ok["reported_results"] = [
        {
            "name": "ocr",
            "value": None,
            "quoted": "a tendency for the right part of the pattern to rise",
            "quoted_source": "a tendency for the fight part of the pattern to rise",
            "quoted_repair": "ocr",
        }
    ]
    case("F2 reparation OCR declaree", ok, True)

    # Une réparation ne dispense de rien : la chaîne déclarée doit exister.
    bad = _fiche()
    bad["reported_results"] = [
        {
            "name": "fausse-reparation",
            "value": None,
            "quoted": "a tendency for the right part of the pattern to rise",
            "quoted_source": "a tendency that this paper never states",
            "quoted_repair": "ocr",
        }
    ]
    case("F2 reparation dont la chaine est ABSENTE", bad, False, "F2")

    # Une réparation non nommée est une échappatoire générique : refusée.
    bad = _fiche()
    bad["reported_results"] = [
        {
            "name": "sans-raison",
            "value": None,
            "quoted": "a tendency for the right part of the pattern to rise",
            "quoted_source": "a tendency for the fight part of the pattern to rise",
        }
    ]
    case("F2 quoted_source SANS raison nommee", bad, False, "F2")

    bad = _fiche()
    bad["reported_results"] = [
        {
            "name": "raison-inconnue",
            "value": None,
            "quoted": "a tendency for the right part of the pattern to rise",
            "quoted_source": "a tendency for the fight part of the pattern to rise",
            "quoted_repair": "parce que",
        }
    ]
    case("F2 raison HORS de la liste close", bad, False, "F2")

    bad = _fiche()
    bad["reported_results"] = [
        {
            "name": "raison-seule",
            "value": None,
            "quoted": "starting out at 0.095% in the morning",
            "quoted_repair": "ocr",
        }
    ]
    case("F2 raison declaree sans quoted_source", bad, False, "F2")

    # Le chiffre est lu dans la chaîne QUI FAIT FOI, pas dans la version lisible :
    # sinon la réparation devient l'endroit où loger un nombre absent du papier.
    bad = _fiche()
    bad["reported_results"] = [
        {
            "name": "valeur-logee",
            "value": 7.77,
            "quoted": "an effect of 7.77% in the morning",
            "quoted_source": "starting out at 0.095% in the morning",
            "quoted_repair": "ocr",
        }
    ]
    # F1 ne l'attrape PAS : `validate_fiches` ignore `quoted_source` et regarde
    # `quoted`, où 7,77 figure bien. Sur une entrée réparée, F3 est donc plus
    # strict que le garde de D14 — noté dans D16 § Ce qui reste ouvert.
    case("F3 valeur presente dans `quoted` mais ABSENTE de la source", bad, False, "F3")

    # F3 — le chiffre qui ne figure pas dans sa propre citation.
    bad = _fiche()
    bad["reported_results"] = [
        {"name": "recopie", "value": 0.85, "quoted": "starting out at 0.095% in the morning"}
    ]
    # F1 l'attrape aussi — `D14` portait deja cette regle. Le recouvrement est
    # voulu et ecrit dans D16 : deux conditions distinctes, un meme symptome.
    case("F3 valeur absente de sa citation", bad, False, ["F1", "F3"])

    # `derived` leve le controle numerique, `spelled_out` verifie le MOT.
    bad = _fiche()
    bad["reported_results"] = [
        {
            "name": "lettres",
            "spelled_out": "Eleven",
            "quoted": "Seven of the strategies fail to survive transaction costs",
        }
    ]
    case("F3 spelled_out absent de la citation", bad, False, "F3")

    # F4 — le PDF qui n'est pas la.
    bad = _fiche()
    bad["source"] = {**_fiche()["source"], "pdf": "corpus/pdf/absent.pdf"}
    case("F4 PDF designe mais absent", bad, False, "F4")

    # F5 — contradiction factuelle, et l'absence qui n'en est PAS une.
    ref = _fiche()
    case("F5 fiche identique a sa reference", _fiche(), True, None, ref)

    contradicted = _fiche()
    contradicted["source"] = {**_fiche()["source"], "year": 2098}
    case("F5 annee CONTRADICTOIRE", contradicted, False, "F5", ref)

    silent = _fiche()
    silent["horizon"] = {"value": None, "reason": "le papier ne l'indique pas"}
    case("F5 silence n'est pas contradiction", silent, True, None, ref)

    # Le diagnostic voit la fiche creuse que les cinq conditions laissent passer.
    hollow = _fiche()
    hollow["reported_results"] = [
        {"name": "morning_rv", "value": 0.095, "quoted": "starting out at 0.095% in the morning"}
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fictif-2099-banc-d-essai.json"
        path.write_text(json.dumps(hollow, ensure_ascii=False), encoding="utf-8")
        result = score(path, PAPER, ref)
    checks += 1
    if not result["passed"]:
        failures.append("fiche creuse : attendue ACCEPTEE par les cinq conditions")
    checks += 1
    if sorted(result["diagnostic"]["missed"]) != ["n_failing", "peak_over_trough"]:
        failures.append(
            "fiche creuse : le diagnostic devait nommer 2 resultats laisses de cote, "
            f"il donne {result['diagnostic']['missed']}"
        )

    print(f"score_extraction --check : {checks} verifications")
    if failures:
        print("\nLE JUGE NE GARDE PAS CE QU'IL DOIT GARDER :")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("Le juge refuse chacune des fautes que D16 nomme, et accepte la fiche intacte.")
    print(
        "Il ACCEPTE une fiche creuse : c'est ecrit dans D16 § Pourquoi, et le diagnostic la montre."
    )
    return 0


def main(argv: list[str]) -> int:
    if len(argv) >= 1 and argv[0] == "--check":
        return self_check()
    if len(argv) < 2:
        print(__doc__)
        return 1
    fiche_path, text_path = Path(argv[0]), Path(argv[1])
    ref = None
    if "--ref" in argv:
        ref = json.loads(Path(argv[argv.index("--ref") + 1]).read_text(encoding="utf-8"))
    if not fiche_path.is_file():
        raise InputError(f"fiche introuvable : {fiche_path}")
    if not text_path.is_file():
        raise InputError(f"texte du papier introuvable : {text_path}")
    result = score(fiche_path, text_path.read_text(encoding="utf-8", errors="replace"), ref)
    print(render(result))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
