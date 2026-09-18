"""La mesure de `H01` et `H02` — les deux premiers tests comptés du projet.

Ce script fait passer les deux étalons de `D06` par `evaluate()`, la seule porte
qui produit un IC, avec leur `hypothesis_ref`. Chaque appel **écrit une ligne au
registre** et fait monter `counted_tests()` : c'est irréversible, et c'est le
but. Les deux hypothèses sont pré-enregistrées depuis le 2026-09-17, avant toute
mesure (invariant IV).

**Elles ne sont jamais comptées comme deux tests indépendants.** Même cible —
la dernière demi-heure de la fenêtre —, prédicteurs différents ; `H02` le dit
explicitement. Le registre porte deux lignes parce que deux IC ont été calculés ;
toute correction de tests multiples devra traiter la paire comme corrélée.

L'as-of est la **fin de la tranche `pool`** : les hypothèses disent « tranche
pool », et le pool entier est leur domaine. Les portes, elles, se calibrent à un
point fixe au milieu (2018-06-15) — ce n'est pas la même question.

Le coût reste un **plancher étiqueté** tant que `fee_bp` et `slippage_bp` sont
`null` : tout IC net lu ici serait un MAJORANT de performance. L'IC brut, lui,
ne dépend pas des frais.

Il a tourné deux fois le 2026-09-18 : d'abord sous le harnais `e9ef2087`
(`T-20260918T064151-bc4048`, `T-20260918T064409-acc2e3`, **périmés**), puis sous
`9ac3e45e` après la correction de `D11` — `T-20260918T065822-2b3e5d` et
`T-20260918T070041-18cf25`, qui font référence. **Le relancer dépenserait deux tests comptés de
plus**, sur les mêmes hypothèses et les mêmes données, ce qui gonflerait le
dénominateur sans rien apprendre. D'où le garde ci-dessous : il refuse de partir
si `counted_tests()` n'est pas nul, sauf ordre explicite.

    python scripts/measure_h01_h02.py            # refuse si des tests sont déjà comptés
    python scripts/measure_h01_h02.py --force    # dépense deux tests de plus
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from harness import evaluate, registry  # noqa: E402
from panel import Panel  # noqa: E402
from signals import REFERENCE  # noqa: E402

ASOF = "2023-12-29 20:00"  # la dernière séance de la tranche pool (fin 2023-12-31)
HORIZON = "30min"

ORDER = [
    ("gao-2018-intraday-momentum", "H01"),
    ("baltussen-2021-intraday-momentum", "H02"),
]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    before = registry.counted_tests()

    # Le registre est append-only : une seconde mesure ne remplace pas la
    # première, elle s'ajoute. Deux lignes de plus sur les mêmes hypothèses et
    # les mêmes données gonflent le dénominateur sans rien apprendre.
    if before and "--force" not in argv:
        print(f"REFUSÉ — {before} test(s) déjà compté(s) au registre.")
        print("  H01 et H02 ont été mesurées le 2026-09-18 ; voir hypotheses/README.md.")
        print("  Relancer dépenserait deux tests de plus. Si c'est voulu : --force.")
        return 1

    print(f"tests comptés avant : {before}")
    print(f"harnais : {registry.code_hash()}\n")

    panel = Panel.open(asof=ASOF, slice="pool")
    print(f"panel ouvert au {panel.asof}, tranche {panel.slice.name}, "
          f"{len(panel.cells())} cellules retenues\n")

    reports = []
    for signal_id, hypothesis in ORDER:
        module = REFERENCE[signal_id]
        assert module.HYPOTHESIS == hypothesis, (
            f"{signal_id} porte {module.HYPOTHESIS}, pas {hypothesis}"
        )
        scores = module.scores(panel, horizon_bars=30)
        report = evaluate(
            scores,
            panel,
            HORIZON,
            signal_id=signal_id,
            hypothesis_ref=hypothesis,
        )
        reports.append((hypothesis, module, report))
        print("=" * 78)
        print(report.render())
        print()

    print("=" * 78)
    print("LE SIGNE, QUI EST L'AFFIRMATION PRINCIPALE DES DEUX HYPOTHÈSES")
    for hypothesis, module, report in reports:
        expected = "+" if module.EXPECTED_SIGN > 0 else "-"
        observed = "+" if report.ic > 0 else "-"
        verdict = "CONFORME" if expected == observed else "CONTREDIT"
        print(f"  {hypothesis}  attendu {expected}, observé {observed}  "
              f"IC {report.ic:+.5f}  t final {report.t['final']:+.2f}   {verdict}")

    after = registry.counted_tests()
    print(f"\ntests comptés après : {after}  (+{after - before})")
    print("  H01 et H02 portent sur la MÊME cible : jamais deux tests indépendants.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
