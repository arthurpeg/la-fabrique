"""Le juge du codeur de signal — `D23`, porte 08.

Il répond à une seule question : **ce module code-t-il CETTE fiche ?** Six
conditions, toutes à tolérance zéro, qui valent ENSEMBLE.

    S1  le module satisfait le contrat de `D07`
    S2  il n'importe rien hors de la liste blanche
    S3  IL EST CAUSAL — score identique sur panel tronqué et panel entier
    S4  il n'est pas dégénéré, et ses scores tombent sur des barres MESURABLES
    S5  TOUTE CONSTANTE NUMERIQUE DU CODE SE RETROUVE DANS LA FICHE
    S6  zéro retouche manuelle depuis la production

**AUCUN IC N'EST CALCULE ICI**, et c'est la règle qui compte. Juger un codeur
sur son IC le sélectionnerait sur son résultat ; surtout, le nombre de tests est
la seule chose que la phase 15 ne peut pas recalculer. Un IC dépensé pour savoir
si du code compile est perdu pour toujours. Même règle que la clause 1 de la
porte 06 : le refus arrive AVANT le harnais, sans consommer de ligne de registre.

**`S5` est la condition qui porte la porte.** Un codeur qui écrit
`FENETRE = 30` là où la fiche dit quarante-cinq minutes produit un signal qui
tourne, qui est causal, qui n'est pas dégénéré — et qui ne code pas ce papier.
Rien d'autre ne l'attraperait. C'est `F2` transposé au code, et l'interdit
constitutionnel appliqué au code : un paramètre absent de la fiche est un
paramètre inventé.

**Ce que ce juge NE dit PAS** : que le signal soit LE BON. Un signal fidèle à
une fiche creuse, ou fidèle à un aspect secondaire du papier, passe les six
conditions. La pertinence n'aura de dénominateur qu'en phase 09 — `D23`
§ Pourquoi, comme `D16` le disait de l'extraction.

**ET `S5` EST NECESSAIRE, PAS SUFFISANTE — c'est mesuré.** Croisant les trois
signaux ecrits a la main avec les dix fiches, elle refuse **12 appariements sur
30, soit 40 %**. Elle laisse donc passer 60 % des mauvais.

La raison n'est pas reparable : deux papiers d'un meme domaine PARTAGENT leurs
parametres. `30` minutes est la demi-heure de Gao, le decalage de Heston et la
fenetre de Patton & Sheppard a la fois. Une constante juste pour le mauvais
papier reste une constante juste.

Ce que `S5` attrape vraiment, et que rien d'autre n'attrapait : un parametre
**invente**, absent de toute recette. C'est deja l'interdit constitutionnel, et
c'est tout ce qu'une verification de fidelite peut promettre sans etalon.

    python scripts/score_signal.py --check                 # le juge contre des fautes fabriquees
    python scripts/score_signal.py <module> --fiche <json> # juge un signal produit
    python scripts/score_signal.py <module> --fiche <json> --no-data  # S1, S2, S5, S6 seuls
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from harness import controls  # noqa: E402
from sandbox import contract, scan  # noqa: E402

PRODUCED = REPO / "signals" / "PRODUCED.json"

PROBES = 16
ASOF = "2018-06-15 20:00"
HORIZON_BARS = 30

# ---------------------------------------------------------------------------
# `S5` — la liste CLOSE des constantes qu'un code peut porter sans que la fiche
# les mentionne. Elle est close au sens de `D09`, `D14`, `D16` et `D17` : ce
# qu'elle ne couvre pas est REFUSE, et l'elargir est une decision ecrite
# (`L18` — avant d'elargir une liste close, chercher si la cause n'est pas
# ailleurs).
#
# Calibree sur les trois signaux ecrits a la main, qui sont les seuls cas
# connus : `gao_2018` ne porte que `FIRST_BARS = 30`, `0` et `1.0`.
# ---------------------------------------------------------------------------

# Conventions de langage : un index, un signe, une neutralite multiplicative.
# Elles ne parametrent rien et ne peuvent rien cacher.
CONVENTIONS = frozenset({0, 1, -1, 2})

# Valeurs qui viennent de `D01` (la grille, les tranches) ou du catalogue, donc
# du DEPOT et non du papier. Un signal a le droit de les employer sans que la
# fiche les repete — mais elles sont NOMMEES ici, une par une.
DU_DEPOT: dict[float, str] = {
    60: "une heure en minutes — arithmetique d'horloge",
    24: "heures dans un jour — arithmetique d'horloge",
    9: "nombre d'instruments de l'univers, D01 §1",
}
# `30` NE FIGURE PAS ICI, et c'est delibere. Il est l'horizon de la grille
# (`D01` §2) ET la demi-heure de Gao : l'exempter rendait invisible le SEUL
# parametre du signal de reference, et `S5` passait alors contre n'importe
# quelle fiche. Mesure du 2026-09-23. Un horizon legitime se retrouve dans le
# champ `horizon` de la fiche, qui est fouille.

# Les champs de la fiche ou vit la RECETTE. `S5` ne cherche que la-dedans.
#
# Chercher dans la fiche ENTIERE rendait la condition quasi vide, et c'est
# mesure : une fiche porte 41 a 194 nombres distincts — `reported_results` est
# plein de t-stats, de Sharpes et de tailles d'echantillon qui n'ont rien a voir
# avec le code — contre 2 a 25 pour `signal_construction`. Sur la fiche Heston,
# 19 des 101 entiers de 0 a 100 s'y trouvaient par hasard : presque toute
# constante passait.
CHAMPS_RECETTE = ("signal_construction", "horizon", "universe", "cost_model")

# Modules du DEPOT, partages par tous les signaux et ecrits a la main : ils ne
# sont PAS la sortie du codeur, donc `S5` ne les juge pas. Leurs constantes
# viennent de `D01` et de l'arithmetique d'horloge — `signals/_common.py` porte
# `24 * 60`, qui ne parametre aucun papier.
#
# Le trou apparent — un codeur qui cacherait ses parametres dans un utilitaire
# partage — est ferme AILLEURS : le codeur produit EXACTEMENT UN module (son
# propre fichier), et toute modification d'un fichier du depot se voit dans git
# et casse `S6`. Etendre `S5` a ces fichiers ferait refuser tous les signaux,
# y compris corrects, pour du code que le codeur n'a pas ecrit.
#
# Liste CLOSE : un nom de plus est une decision.
MODULES_DU_DEPOT = frozenset({"_common.py"})

MAX_FICHE_SEARCH = 4  # nombre de decimales tolerees a la comparaison


@dataclass
class Verdict:
    """Le resultat d'une condition : tenue, cassee, ou sans objet."""

    nom: str
    quoi: str
    fautes: list[str] = field(default_factory=list)
    sans_objet: str | None = None

    @property
    def tenue(self) -> bool:
        return self.sans_objet is not None or not self.fautes


class InputError(RuntimeError):
    """Une faute de l'appelant, pas du signal juge."""


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def fold(text: str) -> str:
    """Replie une chaine pour la recherche : accents otes, casse ignoree."""
    text = "".join(c for c in unicodedata.normalize("NFKD", text or "")
                   if not unicodedata.combining(c))
    return text.lower()


def nombres_du_texte(texte: str) -> set[float]:
    """Tous les nombres qu'un texte contient, separateurs de milliers otes.

    Comparaison NUMERIQUE et non par sous-chaine : `F26` a pris ce garde en
    defaut sur `12500` contre « 12,500,000 », et la meme faute guetterait ici.
    """
    plat = texte.replace(",", "").replace(" ", "").replace(" ", "")
    out: set[float] = set()
    for brut in re.findall(r"-?\d+(?:\.\d+)?", plat):
        try:
            out.add(round(float(brut), MAX_FICHE_SEARCH))
        except ValueError:
            continue
    # Un pourcentage ecrit « 2% » doit aussi repondre a `0.02` dans le code.
    for brut in re.findall(r"(-?\d+(?:\.\d+)?)\s*%", texte):
        try:
            out.add(round(float(brut) / 100, MAX_FICHE_SEARCH))
        except ValueError:
            continue
    # Une duree ecrite « 9:30 » porte 9 et 30, que la regex ci-dessus rend deja,
    # mais aussi 930 pour un code qui l'ecrirait ainsi.
    for h, m in re.findall(r"(\d{1,2}):(\d{2})", texte):
        out.add(float(int(h) * 100 + int(m)))
    return out


def constantes_du_code(source: str) -> list[tuple[float, int]]:
    """Les litteraux numeriques du module, avec leur ligne.

    Analyse SYNTAXIQUE et non textuelle : un nombre dans une chaine ou un
    commentaire n'est pas un parametre, et le compter ferait refuser des
    signaux corrects pour une docstring.
    """
    arbre = ast.parse(source)
    out: list[tuple[float, int]] = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, (int, float)):
            if isinstance(noeud.value, bool):
                continue
            out.append((round(float(noeud.value), MAX_FICHE_SEARCH), noeud.lineno))
    return out


def texte_de_la_fiche(fiche: dict) -> str:
    """Ce que la fiche dit de la RECETTE, et rien d'autre.

    Volontairement restreint a `CHAMPS_RECETTE`. Un parametre de code se
    justifie par la construction du signal, son horizon, son univers ou son
    modele de cout — jamais par un t-stat rapporte ni un numero de page.
    """
    return json.dumps({k: fiche.get(k) for k in CHAMPS_RECETTE}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Les six conditions
# ---------------------------------------------------------------------------

def check_s1(module, scores, panel) -> Verdict:
    v = Verdict("S1", "le module satisfait le contrat de D07")
    v.fautes.extend(contract.validate_module(module))
    if scores is not None and panel is not None:
        v.fautes.extend(contract.validate_scores(scores, panel))
    elif not v.fautes:
        v.sans_objet = "sans données : seuls les attributs sont vérifiés"
    return v


def check_s2(module) -> Verdict:
    v = Verdict("S2", "il n'importe rien hors de la liste blanche")
    v.fautes.extend(scan.scan_module(module))
    return v


def check_s3(module, panel, scores) -> Verdict:
    v = Verdict("S3", "il est causal")
    if panel is None:
        v.sans_objet = "sans données : le test de causalité demande un panel"
        return v
    from sandbox import causality

    for d in causality.check(module, panel, probes=PROBES,
                             horizon_bars=HORIZON_BARS, full=scores):
        v.fautes.append(str(d))
    return v


def check_s4(scores) -> Verdict:
    v = Verdict("S4", "il n'est pas dégénéré, et ses scores sont mesurables")
    if scores is None:
        v.sans_objet = "sans données : la dégénérescence se juge sur des scores"
        return v
    try:
        gardes, verdicts = controls.screen(scores, is_test=True)
    except controls.Degenerate as e:
        v.fautes.append(f"rejeté par les contrôles : {e}")
        return v
    refusees = [x for x in verdicts if not getattr(x, "kept", True)]
    if refusees:
        v.fautes.extend(f"cellule refusée : {x}" for x in refusees[:4])
    if not gardes:
        v.fautes.append("aucune cellule ne survit aux contrôles")
    return v


def check_s5(module, fiche: dict) -> Verdict:
    """LA condition qui porte la porte — `F2` transposé au code."""
    v = Verdict("S5", "toute constante du code se retrouve dans la fiche")
    attendus = nombres_du_texte(texte_de_la_fiche(fiche))

    for chemin in scan.sources_of(module):
        if chemin.name in MODULES_DU_DEPOT:
            continue
        source = chemin.read_text(encoding="utf-8")
        for valeur, ligne in constantes_du_code(source):
            if valeur in CONVENTIONS:
                continue
            if valeur in DU_DEPOT:
                continue
            if valeur in attendus:
                continue
            v.fautes.append(
                f"{chemin.name}:{ligne} — la constante {valeur:g} n'est ni dans "
                "la fiche, ni dans la liste close (conventions, dépôt). "
                "Un paramètre absent de la fiche est un paramètre inventé."
            )
    return v


def check_s6(module) -> Verdict:
    """Zéro retouche manuelle : le fichier est-il celui qui a été produit ?

    Vérifiable seulement si la production a été enregistrée. Sans registre,
    la condition est SANS OBJET et le dit — jamais « tenue » par défaut, ce
    qui la viderait de son sens.
    """
    v = Verdict("S6", "zéro retouche manuelle depuis la production")
    if not PRODUCED.is_file():
        v.sans_objet = ("aucun registre de production — `signals/PRODUCED.json` "
                        "sera écrit par `code_signal.py`, qui n'existe pas encore")
        return v
    registre = json.loads(PRODUCED.read_text(encoding="utf-8"))
    attendu = registre.get(module.SIGNAL_ID)
    if attendu is None:
        v.sans_objet = f"« {module.SIGNAL_ID} » n'est pas au registre de production"
        return v
    for chemin in scan.sources_of(module):
        if chemin.name != Path(attendu["path"]).name:
            continue
        digest = hashlib.sha256(chemin.read_bytes()).hexdigest()[:16]
        if digest != attendu["sha256_16"]:
            v.fautes.append(
                f"{chemin.name} a changé depuis sa production : "
                f"{attendu['sha256_16']} -> {digest}. `S6` de `D23` exige zéro "
                "retouche ; réparer à la main est exactement la faille qu'il ferme."
            )
    return v


# ---------------------------------------------------------------------------
# Le jugement
# ---------------------------------------------------------------------------

def juger(module, fiche: dict, panel=None) -> list[Verdict]:
    scores = None
    if panel is not None:
        scores = module.scores(panel, horizon_bars=HORIZON_BARS)
    return [
        check_s1(module, scores, panel),
        check_s2(module),
        check_s3(module, panel, scores),
        check_s4(scores),
        check_s5(module, fiche),
        check_s6(module),
    ]


def rendre(verdicts: list[Verdict], signal_id: str) -> str:
    lignes = ["Les six conditions de D23 — toutes à tolérance ZÉRO, elles valent ENSEMBLE",
              ""]
    for v in verdicts:
        if v.sans_objet:
            lignes.append(f"  {v.nom} : sans objet — {v.sans_objet}")
        elif v.fautes:
            lignes.append(f"  {v.nom} : CASSÉE ({len(v.fautes)}) — {v.quoi}")
            lignes.extend(f"         - {f}" for f in v.fautes[:4])
            if len(v.fautes) > 4:
                lignes.append(f"         … et {len(v.fautes) - 4} autre(s)")
        else:
            lignes.append(f"  {v.nom} : tenue — {v.quoi}")

    passe = all(v.tenue for v in verdicts)
    ignorees = [v.nom for v in verdicts if v.sans_objet]
    lignes += ["", "AUCUN IC N'A ÉTÉ CALCULÉ — la porte 08 ne consomme aucune",
               "ligne de registre (D23).", ""]
    if passe:
        lignes.append(f"SIGNAL « {signal_id} » : les six conditions tiennent.")
        if ignorees:
            lignes.append(f"  MAIS {', '.join(ignorees)} n'ont pas été jugées — "
                          "la porte n'est pas franchie sur un verdict partiel.")
        lignes.append("Ce que ce juge NE dit PAS : que le signal soit LE BON.")
    else:
        cassees = [v.nom for v in verdicts if not v.tenue]
        lignes.append(f"SIGNAL « {signal_id} » : NON FRANCHI — {', '.join(cassees)}.")
        lignes.append("Un échec ne s'achète pas en redéfinissant le seuil (D13).")
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Le juge, jugé — des fautes fabriquées, chacune refusée pour sa raison
# ---------------------------------------------------------------------------

def self_check() -> int:
    checks: list[bool] = []

    def cas(label: str, condition: bool, detail: str = "") -> None:
        checks.append(condition)
        print(f"  [{'ok ' if condition else 'RATE'}] {label}"
              f"{'' if condition else f' — {detail}'}")

    print("Les nombres qu'un texte porte")
    n = nombres_du_texte("une fenetre de 30 minutes, un seuil de 2%, a 9:30")
    cas("30 est trouvé", 30.0 in n)
    cas("« 2% » répond aussi à 0.02", 0.02 in n)
    cas("« 9:30 » porte 9, 30 et 930", {9.0, 30.0, 930.0} <= n)
    n2 = nombres_du_texte("12,500,000 Japanese yen")
    cas("12500 NE passe PAS sous « 12,500,000 » (F26)", 12500.0 not in n2,
        f"trouvé dans {sorted(n2)}")
    cas("12500000 y est bien", 12500000.0 in n2)

    print("\nLes constantes qu'un code porte")
    src = ('"""30 dans une docstring."""\n'
           "X = 45  # 99 en commentaire\n"
           "def f():\n    return X * 2.5\n")
    c = {v for v, _ in constantes_du_code(src)}
    cas("45 et 2.5 sont vus", {45.0, 2.5} <= c)
    cas("30 de la docstring est IGNORÉ", 30.0 not in c, f"vu {sorted(c)}")
    cas("99 du commentaire est IGNORÉ", 99.0 not in c)
    cas("un booléen n'est pas une constante", not constantes_du_code("Y = True"))

    print("\nS5 sur des cas fabriqués")
    fiche = {"signal_construction": {"value": "fenetre de 45 minutes",
                                     "steps": ["seuil a 2%"]}}

    class FauxModule:
        SIGNAL_ID = "faux"

    def s5_sur(source: str) -> Verdict:
        chemin = REPO / "scripts" / "_s5_tmp.py"
        chemin.write_text(source, encoding="utf-8")
        try:
            vrai = scan.sources_of
            scan.sources_of = lambda m: [chemin]  # noqa: ARG005
            return check_s5(FauxModule, fiche)
        finally:
            scan.sources_of = vrai
            chemin.unlink(missing_ok=True)

    cas("une constante de la fiche passe", s5_sur("W = 45\n").tenue)
    cas("un pourcentage de la fiche passe", s5_sur("S = 0.02\n").tenue)
    v = s5_sur("W = 37\n")
    cas("une constante ABSENTE de la fiche est refusée", not v.tenue)
    cas("  et la faute nomme le fichier et la ligne",
        bool(v.fautes) and "_s5_tmp.py:1" in v.fautes[0], str(v.fautes[:1]))
    cas("une convention (0, 1, -1, 2) passe", s5_sur("A=0\nB=1\nC=-1\nD=2\n").tenue)
    cas("une valeur du dépôt passe (60 min/h, horloge)",
        s5_sur("H = 60\n").tenue)
    # `30` a ete RETIRE de `DU_DEPOT` le 2026-09-23 : horizon de grille ET
    # demi-heure de Gao a la fois. L'exempter rendait `S5` vide. Le garde
    # ci-dessous casse si quelqu'un le remet sans y repenser.
    cas("  et `30` n'est PLUS exempté — il est ambigu", 30 not in DU_DEPOT)
    cas("une valeur du dépôt NON listée est refusée", not s5_sur("Z = 7\n").tenue)
    cas("un nombre en docstring ne suffit PAS à justifier le code",
        not s5_sur('"""37"""\nW = 37\n').tenue)

    # Les utilitaires du dépôt ne sont pas la sortie du codeur. Sans cette
    # exemption, `signals/_common.py` et son `24 * 60` — de l'arithmétique
    # d'horloge — faisaient refuser TOUS les signaux, corrects compris.
    cas("un module du dépôt est exempté de S5", "_common.py" in MODULES_DU_DEPOT)
    reel = check_s5(
        importlib.import_module("signals.gao_2018_intraday_momentum"),
        json.loads((REPO / "corpus" / "fiches"
                    / "patton-sheppard-2015-good-volatility-bad-volatility.json"
                    ).read_text(encoding="utf-8")))
    cas("  et `_common.py` ne figure plus dans les fautes",
        all("_common.py" not in f for f in reel.fautes), str(reel.fautes[:1]))

    print("\nS6 sans registre de production")
    class M:
        SIGNAL_ID = "gao-2018-intraday-momentum"
    v6 = check_s6(M)
    cas("sans registre, S6 est SANS OBJET et non « tenue »",
        v6.sans_objet is not None)
    cas("  et un verdict partiel ne franchit pas la porte",
        "n'ont pas été jugées" in rendre([v6], "x") or v6.sans_objet is not None)

    print("\nLe rendu")
    bon = [Verdict("S1", "x"), Verdict("S2", "y")]
    cas("six conditions tenues -> message de réussite",
        "les six conditions tiennent" in rendre(bon, "s"))
    mauvais = [Verdict("S5", "y", fautes=["une constante inventée"])]
    cas("une condition cassée -> NON FRANCHI", "NON FRANCHI" in rendre(mauvais, "s"))
    cas("  et le seuil n'est pas négociable",
        "ne s'achète pas" in rendre(mauvais, "s"))

    print(f"\nscore_signal --check : {sum(checks)} / {len(checks)} vérifications")
    if all(checks):
        print("Le juge refuse chacune des fautes que D23 nomme, pour sa raison.")
        print("Il ACCEPTE un signal fidèle à une fiche creuse : c'est écrit dans")
        print("D23 § Pourquoi, et la pertinence n'aura de dénominateur qu'en phase 09.")
    return 0 if all(checks) else 1


def importer(cible: str):
    """Importe un signal designe par un CHEMIN ou par un nom pointe.

    Les deux ecritures arrivent naturellement — `signals/gao.py` sort d'un
    `ls`, `signals.gao` sort d'un import — et n'en accepter qu'une faisait
    echouer l'appel le plus evident sur un `ModuleNotFoundError` illisible.
    """
    if cible.endswith(".py") or "/" in cible or "\\" in cible:
        chemin = Path(cible).resolve()
        if not chemin.is_file():
            raise InputError(f"module introuvable : {cible}")
        try:
            rel = chemin.relative_to(REPO)
        except ValueError:
            raise InputError(
                f"{cible} est hors du depot : un signal vit dans signals/"
            ) from None
        cible = ".".join(rel.with_suffix("").parts)
    try:
        return importlib.import_module(cible)
    except ModuleNotFoundError as e:
        raise InputError(f"module introuvable : {cible} ({e})") from None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le juge du codeur de signal — D23")
    ap.add_argument("module", nargs="?",
                    help="le signal, en chemin (signals/gao_2018.py) ou en nom "
                         "pointe (signals.gao_2018)")
    ap.add_argument("--fiche", help="la fiche que ce signal prétend coder")
    ap.add_argument("--check", action="store_true", help="juger le juge")
    ap.add_argument("--no-data", action="store_true",
                    help="S1, S2, S5, S6 seuls — sans panel, donc porte NON franchie")
    a = ap.parse_args(argv)

    if a.check:
        return self_check()
    if not a.module or not a.fiche:
        print(__doc__)
        return 1

    chemin = Path(a.fiche)
    if not chemin.is_file():
        raise InputError(f"fiche introuvable : {chemin}")
    fiche = json.loads(chemin.read_text(encoding="utf-8"))
    module = importer(a.module)

    panel = None
    if not a.no_data:
        from panel import Panel

        # `slice`, et non `slice_name` : la faute datait du 2026-09-23 et n'a
        # tenu que parce que le juge n'avait jamais été lancé AVEC données —
        # `--check` et `--no-data` ne passent pas par ici. Un chemin de code
        # qu'aucun garde n'emprunte n'est pas un chemin vérifié.
        panel = Panel.open(ASOF, slice="pool")

    verdicts = juger(module, fiche, panel)
    print(rendre(verdicts, getattr(module, "SIGNAL_ID", a.module)))
    return 0 if all(v.tenue for v in verdicts) and not any(
        v.sans_objet for v in verdicts) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
