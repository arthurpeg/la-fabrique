"""PORTE 06, clause 1 — un signal dégénéré est rejeté AVANT le harnais d'IC.

La clause, telle que le plan de montage la pose : « un signal volontairement
dégénéré — constant, ou 99 % de NaN — est rejeté avant d'atteindre le harnais
d'IC ». Rejeté, et **sans consommer de ligne de registre** : il n'a produit aucun
IC, il n'y a rien à inscrire, et un dénominateur gonflé de tests qui n'ont jamais
eu lieu est aussi faux qu'un dénominateur absent (`D08`).

La clause 2 de la porte — **la réplication d'un résultat publié** — n'est pas
ici : elle vit dans `scripts/measure_h04.py`, et elle a été **franchie le
2026-09-18** (`H04`, Andersen & Bollerslev 1997). Les deux clauses sont donc
tenues par deux scripts distincts, parce qu'elles mesurent deux choses
différentes — un signal dégénéré d'un côté, une propriété des données de
l'autre (`D13`).

Les scores de cette porte sont **synthétiques**. Aucun n'est celui de `H01` ou de
`H02` : voir un résultat sur une hypothèse pré-enregistrée avant sa mesure
officielle, fût-ce sous l'étiquette « calibration », serait exactement le coup
d'œil que le registre existe pour empêcher.

    python scripts/gate_06_controls.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from harness import controls, evaluate, registry  # noqa: E402
from panel import Panel  # noqa: E402
from signals import _common  # noqa: E402

ASOF = "2018-06-15 20:00"
HORIZON = "30min"
HONEST_CELLS = [("NQ", "US"), ("ES", "US")]
DEAD_CELL = ("YM", "US")


def noise_scores(panel: Panel, cell: tuple[str, str], seed: int) -> pd.Series:
    """Un score déterministe et indépendant du futur, sur de vraies barres.

    Déterministe pour que la porte soit reproductible ; indépendant des
    rendements pour qu'il ne dise rien — ce qui est testé ici est le chemin, pas
    un résultat.
    """
    close, _ = _common.cell_bars(panel, *cell)
    index = close.index[::391]  # une barre par séance environ, comme un vrai signal
    generator = np.random.default_rng(seed)
    return pd.Series(generator.standard_normal(len(index)), index=index, dtype=float)


def main() -> int:
    failures: list[str] = []
    checks = 0
    # Ce que cette porte doit prouver : ELLE ne dépense aucun test. Elle a
    # longtemps écrit `== 0`, ce qui était vrai tant qu'aucune hypothèse n'avait
    # été testée et faux depuis H01 et H02 (2026-09-18). Un compteur global
    # n'est pas une propriété de cette porte.
    counted_before = registry.counted_tests()

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    def refuses(call, what: str) -> None:
        """Le refus doit lever, et ne rien écrire."""
        nonlocal checks
        checks += 1
        before = len(registry.read_all())
        try:
            call()
        except controls.Degenerate:
            after = len(registry.read_all())
            checks += 1
            if after != before:
                failures.append(
                    f"{what} : rejeté, mais {after - before} ligne(s) écrite(s) au registre"
                )
            return
        except Exception as error:  # noqa: BLE001
            failures.append(f"{what} : a levé {type(error).__name__}, pas Degenerate")
            return
        failures.append(f"{what} : N'A PAS ÉTÉ REJETÉ")

    panel = Panel.open(asof=ASOF, slice="pool")
    print(f"panel au {panel.asof}, {len(panel.cells())} cellules, "
          f"registre à {len(registry.read_all())} lignes\n")

    honest = {cell: noise_scores(panel, cell, seed) for seed, cell in enumerate(HONEST_CELLS)}
    reference_index = honest[HONEST_CELLS[0]].index

    # -- 1. les dégénérés, un par motif -------------------------------------
    print("1. quatre signaux dégénérés, un par motif")
    constant = {
        cell: pd.Series(0.42, index=series.index, dtype=float)
        for cell, series in honest.items()
    }
    refuses(
        lambda: evaluate(constant, panel, HORIZON, signal_id="degenere-constant",
                         stage="06-controles"),
        "un score constant sur toutes ses cellules",
    )

    quasi = {
        cell: pd.Series(np.resize([0.0, 1.0, 2.0], len(series)), index=series.index,
                        dtype=float)
        for cell, series in honest.items()
    }
    refuses(
        lambda: evaluate(quasi, panel, HORIZON, signal_id="degenere-quasi-constant",
                         stage="06-controles"),
        "trois valeurs distinctes sur six cents séances",
    )

    thin = {cell: series.iloc[:10] for cell, series in honest.items()}
    refuses(
        lambda: evaluate(thin, panel, HORIZON, signal_id="degenere-exsangue",
                         stage="06-controles"),
        "dix scores par cellule, sous le plancher de trente",
    )

    # Celui-ci porte une `hypothesis_ref` : le plancher de deux cellules ne vaut
    # que pour un TEST. Une calibration a le droit de n'en mesurer qu'une — c'est
    # la porte 03 qui a imposé cette dérogation, en tombant (D08).
    lonely = {HONEST_CELLS[0]: honest[HONEST_CELLS[0]]}
    refuses(
        lambda: evaluate(lonely, panel, HORIZON, signal_id="degenere-une-cellule",
                         hypothesis_ref="porte-06-cellule-unique", stage="06-controles"),
        "une seule cellule survivante, pour un test",
    )
    kept, _ = controls.screen(lonely, is_test=False)
    check(len(kept) == 1, "la dérogation de calibration ne laisse pas passer une cellule")
    try:
        controls.screen(lonely, is_test=True)
        check(False, "la dérogation s'applique aussi aux tests : elle n'est pas étroite")
    except controls.Degenerate:
        check(True, "")
    print("   4 rejets, 0 ligne de registre consommée ; dérogation de calibration "
          "vérifiée étroite")

    # -- 2. le rejet est partiel quand il doit l'être ------------------------
    print("2. une cellule morte au milieu de cellules vivantes")
    mixed = dict(honest)
    mixed[DEAD_CELL] = pd.Series(1.0, index=reference_index, dtype=float)
    before = len(registry.read_all())
    report = evaluate(mixed, panel, HORIZON, signal_id="porte-06-cellule-morte",
                      stage="06-controles")
    after = len(registry.read_all())

    check(after == before + 1, f"{after - before} lignes écrites au lieu d'une")
    check(len(report.refused_cells) == 1,
          f"{len(report.refused_cells)} cellule(s) refusée(s) au lieu d'une")
    check(all(v.cell != DEAD_CELL for v in report.cells if hasattr(v, "cell")),
          "la cellule morte figure quand même dans la ventilation")
    measured = {(c.root, c.window) for c in report.cells}
    check(DEAD_CELL not in measured, f"{DEAD_CELL} a été mesurée alors qu'elle est constante")
    check(measured <= set(HONEST_CELLS), f"cellules mesurées inattendues : {measured}")
    rendered = report.render()
    check("cellules refusées" in rendered,
          "le rapport ne dit pas que des cellules ont été refusées")
    check(f"{DEAD_CELL[0]}" in rendered.split("cellules refusées")[1][:200],
          "le rapport ne nomme pas la cellule refusée")
    print(f"   {len(measured)} cellules mesurées, 1 refusée et nommée dans le rapport, "
          f"1 ligne au registre ({report.test_id})")

    # -- 3. le détecteur de « trop beau pour être vrai » ---------------------
    print("3. la suspicion signale, et ne bloque pas")
    loud = controls.warnings_for(0.35, honest)
    check(any("0,10" in w or "0.10" in w for w in loud),
          f"un IC de 0,35 ne déclenche aucune suspicion : {loud}")
    quiet = controls.warnings_for(0.02, honest)
    check(not any("au-delà" in w for w in quiet),
          f"un IC de 0,02 déclenche une suspicion : {quiet}")
    check(report.warnings == controls.warnings_for(report.ic, {
        cell: series for cell, series in mixed.items() if cell != DEAD_CELL
    }), "le rapport ne porte pas les avertissements de son propre IC")
    persistent = {
        cell: pd.Series(np.arange(len(series), dtype=float), index=series.index)
        for cell, series in honest.items()
    }
    check(any("persistants" in w for w in controls.warnings_for(0.01, persistent)),
          "un score monotone ne déclenche pas l'avertissement de persistance")
    print(f"   IC 0,35 : {len(loud)} avertissement(s) ; IC 0,02 : aucun ; "
          f"scores monotones signalés")

    # -- 4. le comparateur de doublons --------------------------------------
    print("4. deux signaux trop proches ne sont pas deux tests")
    itself = controls.duplicate_of(honest, honest)
    check(abs(itself - 1.0) < 1e-9, f"un signal comparé à lui-même rend {itself}")
    shifted = {cell: series + 0.001 for cell, series in honest.items()}
    check(controls.duplicate_of(honest, shifted) > controls.DUPLICATE_RHO,
          "une translation constante n'est pas vue comme un doublon")
    other = {cell: noise_scores(panel, cell, 100 + i) for i, cell in enumerate(HONEST_CELLS)}
    rho = controls.duplicate_of(honest, other)
    check(abs(rho) < 0.2, f"deux bruits indépendants sont corrélés à {rho:+.3f}")
    print(f"   lui-même {itself:+.3f} · translaté "
          f"{controls.duplicate_of(honest, shifted):+.3f} · bruit indépendant {rho:+.3f}")

    # -- verdict -------------------------------------------------------------
    counted = registry.counted_tests()
    check(
        counted == counted_before,
        f"cette porte a fait passer counted_tests de {counted_before} à {counted} ; "
        f"elle ne doit rien dépenser",
    )

    print(f"\n{checks} vérifications")
    if failures:
        print("PORTE 06, CLAUSE 1 : NON FRANCHIE")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("PORTE 06, CLAUSE 1 : FRANCHIE — un signal dégénéré n'atteint pas le harnais")
    print(f"  registre : {len(registry.read_all())} lignes, {counted} test(s) compté(s), "
          f"inchangé par cette porte ; "
          f"harnais {registry.code_hash()}")
    print("  CLAUSE 2 (réplication) : franchie le 2026-09-18 par "
          "scripts/measure_h04.py — la porte 06 est entière.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
