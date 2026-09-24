"""D09 — le garde de provenance, montré en train de refuser.

`catalogue/validate.py` §8 exige qu'une valeur externe entre accompagnée de sa
source. Le catalogue honnête le satisfait, et un catalogue qui satisfait un
garde ne prouve rien : ce qu'il faut voir, c'est le refus. Ce script fabrique
donc des catalogues délibérément fautifs — à partir du vrai, en mémoire, jamais
sur disque — et vérifie que chacun est refusé **pour la raison écrite d'avance**,
comme `sandbox/tainted.py` le fait des look-ahead pour la porte 05.

Le cas qui compte est le cinquième : un multiplicateur recopié `12500` sous une
citation qui dit « 12,500,000 Japanese yen ». La source est là, l'URL est bonne,
la date est bonne — et le nombre est faux d'un facteur mille. C'est la faute que
`source_url` seul ne voit pas (`D09` § Pourquoi).

    python scripts/check_provenance.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import yaml  # noqa: E402

sys.path.insert(0, str(REPO / "catalogue"))
from validate import provenance_failures, value_in_quote  # noqa: E402

CATALOGUE = REPO / "catalogue" / "catalogue.yaml"
ROLLS = REPO / "catalogue" / "roll_dates.json"

# La citation du CME pour le yen, dans ses mots et ses unités. Elle sert de
# décor : ce script ne dépose aucune valeur au catalogue.
YEN_QUOTE = "12,500,000 Japanese yen"
NQ_QUOTE = "$20 x Nasdaq-100 Index"


def entry(**overrides) -> dict:
    """Une entrée de provenance complète, que chaque cas abîme d'une façon."""
    base = {
        "id": "essai",
        "source": "CME Group -- fiche contrat",
        "source_url": "https://www.cmegroup.com/markets/fx/g10/japanese-yen.html",
        "retrieved": "2026-09-18",
        "quoted": YEN_QUOTE,
        "applies_to": ["instruments.6J.multiplier"],
    }
    base.update(overrides)
    return base


def blank(raw: dict) -> dict:
    """Le catalogue réel, vidé de ses valeurs externes et de leurs provenances.

    Chaque cas abîme UNE chose. Depuis que les multiplicateurs sont déposés
    (2026-09-24), abîmer le catalogue réel tel quel mêlerait la faute voulue aux
    valeurs légitimes qu'elle découvre : un cas qui remplace `provenance` laisse
    huit multiplicateurs sans source, et le refus ne dit plus rien du cas. On
    part donc d'un catalogue sans valeur externe — l'état où ce script a été
    écrit — pour que le refus observé soit celui de la faute, et d'elle seule.
    """
    for spec in raw["instruments"]:
        for field in ("multiplier", "fee_per_contract_usd"):
            spec[field] = None
    raw["provenance"] = []
    return raw


def fill(raw: dict, root: str, field: str, value) -> None:
    for spec in raw["instruments"]:
        if spec["root"] == root:
            spec[field] = value
            return
    raise KeyError(root)


# -- les cas, et la raison attendue de chaque refus --------------------------
# (nom, ce qu'on abîme, ce que le refus doit dire)

def case_valeur_sans_source(raw):
    fill(raw, "6J", "multiplier", 12500000.0)


def case_sans_url(raw):
    fill(raw, "6J", "multiplier", 12500000.0)
    raw["provenance"] = [entry(source_url="relevé à la main")]


def case_sans_citation(raw):
    fill(raw, "6J", "multiplier", 12500000.0)
    raw["provenance"] = [entry(quoted="   ")]


def case_date_floue(raw):
    fill(raw, "6J", "multiplier", 12500000.0)
    raw["provenance"] = [entry(retrieved="septembre 2026")]


def case_faute_de_recopie(raw):
    fill(raw, "6J", "multiplier", 12500.0)  # trois zéros perdus
    raw["provenance"] = [entry()]


def case_recopie_juste(raw):
    fill(raw, "6J", "multiplier", 12500000.0)
    raw["provenance"] = [entry()]


def case_unites_en_mots(raw):
    fill(raw, "NQ", "multiplier", 20.0)
    raw["provenance"] = [
        entry(
            id="cme-nq",
            quoted=NQ_QUOTE,
            applies_to=["instruments.NQ.multiplier"],
        )
    ]


def case_provenance_morte(raw):
    raw["provenance"] = [entry()]  # 6J.multiplier est resté null


def case_champ_non_externe(raw):
    raw["provenance"] = [entry(applies_to=["instruments.6J.tick"])]


def case_double_couverture(raw):
    fill(raw, "6J", "multiplier", 12500000.0)
    raw["provenance"] = [entry(), entry(id="essai-bis")]


def case_registre_absent(raw):
    fill(raw, "6J", "multiplier", 12500000.0)
    del raw["provenance"]


CASES = [
    ("une valeur déposée sans aucune source", case_valeur_sans_source,
     "no provenance vouches for it", True),
    ("une source sans URL", case_sans_url, "source_url is not a URL", True),
    ("une source sans citation", case_sans_citation, "quoted is empty", True),
    ("une date de relevé non datée", case_date_floue, "expected AAAA-MM-JJ", True),
    ("un multiplicateur recopié à un facteur mille près", case_faute_de_recopie,
     "nowhere in the quoted source", True),
    ("la même valeur, recopiée juste", case_recopie_juste, None, False),
    ("des unités dans les mots du tiers", case_unites_en_mots, None, False),
    ("une provenance qui atteste un trou", case_provenance_morte,
     "is null -- close the entry", True),
    ("une provenance sur un champ mesuré", case_champ_non_externe,
     "is not an external field", True),
    ("deux sources pour la même valeur", case_double_couverture,
     "already covered by", True),
    ("le registre lui-même retiré", case_registre_absent,
     "missing top-level key", True),
]


def main() -> int:
    raw = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))
    rolls = json.loads(ROLLS.read_text(encoding="utf-8"))

    failures: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    # -- 1. le catalogue réel passe -----------------------------------------
    print("1. le catalogue tel qu'il est")
    verdict = provenance_failures(copy.deepcopy(raw), rolls)
    check(not verdict, f"le catalogue réel est refusé : {verdict}")
    print(f"   {len(verdict)} refus — attendu 0")

    # -- 2. onze catalogues abîmés ------------------------------------------
    print("\n2. les catalogues fautifs, un par forme de faute")
    for name, damage, expected, must_fail in CASES:
        broken = blank(copy.deepcopy(raw))
        damage(broken)
        verdict = provenance_failures(broken, rolls)
        if must_fail:
            check(bool(verdict), f"{name} : ACCEPTÉ, alors qu'il devait être refusé")
            named = any(expected in line for line in verdict)
            check(named, f"{name} : refusé, mais pour une autre raison — {verdict}")
            mark = "refusé" if verdict and named else "MANQUÉ"
        else:
            check(not verdict, f"{name} : refusé à tort — {verdict}")
            mark = "accepté" if not verdict else "REFUSÉ À TORT"
        print(f"   {mark:8s} {name}")

    # -- 3. la citation, séparateurs ôtés -----------------------------------
    print("\n3. la valeur retrouvée dans les mots du tiers")
    for value, quoted, expected in (
        (12500000.0, YEN_QUOTE, True),
        (12500.0, YEN_QUOTE, False),
        (20.0, NQ_QUOTE, True),
        (100.0, "100 troy ounces", True),
        (1000.0, "1,000 barrels", True),
        (125000.0, "125,000 euro", True),
        (5.0, "$5 x Dow Jones Industrial Average Index", True),
        (0.5, "$0.50 per side", True),
    ):
        got = value_in_quote(value, quoted)
        check(got == expected, f"{value} dans {quoted!r} : {got}, attendu {expected}")
        print(f"   {str(got):5s} {value:>12g}  dans  {quoted!r}")

    # -- 4. le fichier tiers porte sa propre provenance ---------------------
    print("\n4. roll_dates.json, fichier reçu du fournisseur")
    for field in ("source", "source_url", "retrieved"):
        check(str(rolls.get(field, "")).strip() != "", f"roll_dates.json : {field} est vide")
    amputated = {k: v for k, v in rolls.items() if k != "source_url"}
    verdict = provenance_failures(copy.deepcopy(raw), amputated)
    check(
        any("roll_dates.json: source_url is empty" in line for line in verdict),
        f"roll_dates.json amputé de son URL n'est pas refusé : {verdict}",
    )
    print(f"   {rolls['source']} — {rolls['source_url']}, relevé {rolls['retrieved']}")
    print("   amputé de son source_url : refusé")

    print(f"\n{checks} vérifications")
    if failures:
        print("PROVENANCE : LE GARDE NE TIENT PAS")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("PROVENANCE : le garde refuse chacune des 9 fautes, pour la raison prévue")
    external = sum(
        spec.get(field) is not None
        for spec in raw["instruments"]
        for field in ("multiplier", "fee_per_contract_usd")
    )
    print(f"  (D09 ; le catalogue réel porte {external} valeur(s) externe(s), "
          f"toutes couvertes — les cas fautifs partent d'un catalogue vidé)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
