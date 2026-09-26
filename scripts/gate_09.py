"""PORTE 09 — le premier passage : Benjamini–Hochberg sur un lot clos.

`ETAT.md` pose la porte ainsi : *« La chaîne tourne de bout en bout ; le
registre compte tous les tests ; un rapport d'IC existe pour chaque signal. »*
Rien n'y exige qu'un signal survive — le corpus implémentable est *attendu
mort* (`wiki/hot.md`), et zéro hypothèse retenue est un résultat valide de la
procédure, pas un échec de la porte. Ce qui est jugé ici, c'est que le
protocole de `D25` a été **suivi**, pas que la pêche a été bonne.

**Écrit avant que le lot existe**, comme `score_triage.py` l'a été avant le
trieur et `score_signal.py` avant le codeur — le juge avant l'accusé. Au
moment où ce fichier est écrit, `hypotheses/LOT-09.json` n'existe pas : le
corpus porte 17 fiches, il en faut 50 (`D25` C2). Lancer ce script maintenant
doit répondre NON FRANCHIE pour cette seule raison, et c'est la bonne réponse.

**Deux artefacts que cette porte est la première à exiger, et dont le format
est fixé ICI faute d'exister ailleurs :**

`hypotheses/LOT-09.json` — le lot clos AVANT la première mesure (`D25` C2) :

    {
      "declared_at": "2026-MM-JJ",
      "q": 0.10,
      "hypotheses": [
        {"ref": "H05", "signal_id": "...", "fiche_id": "..."},
        ...  (exactement 50)
      ]
    }

`scripts/out/lot_09_correlations.json` — la matrice de corrélation des
signaux du lot, mesurée et inscrite AVANT que `BH` soit appliqué (`D25`
§ Pourquoi, dernier paragraphe : « sans elle, le contrôle BH est une
hypothèse non vérifiée ») :

    {
      "measured_at": "2026-MM-JJ...",   (>= declared_at du lot)
      "signal_ids": ["...", ...],        (exactement les signal_id distincts du lot)
      "pairs": [{"a": "...", "b": "...", "correlation": ..., "n": ...}, ...]
    }

**Ce que la porte vérifie, dans l'ordre, et refuse un verdict dès la
première faute (D25 § Ce que ça verrouille) :**

1. le lot est bien formé — 50 entrées, `q` = 0,10, dates, pas de doublon ;
2. chaque hypothèse du lot est **écrite** dans `hypotheses/` (invariant IV) ;
3. la matrice de corrélation existe, couvre exactement les signaux du lot, et
   est datée après la clôture du lot ;
4. chaque hypothèse a **exactement une** mesure au registre, `stage` =
   `09-passage`, `code_hash` = celui du harnais **courant** (une ligne
   périmée « ne se compare pas », `registry/SCHEMA.md`) — une hypothèse
   absente ou dupliquée refuse le verdict, elle ne se devine pas.
   Elle porte en outre sur toute la tranche `pool`, à l'instant fixé par
   `D29` (`asof` = 2023-12-29 20:00 UTC) : une date choisie par hypothèse
   serait un bouton.
5. **aucune autre ligne du registre ne touche le lot** (`D28`) — ni une
   calibration (`hypothesis_ref` nul) portant le `signal_id` d'un signal du
   lot, ni une mesure d'une `ref` du lot sous un autre `stage` ou un autre
   harnais, qu'elle soit antérieure ou postérieure à la clôture. Une
   calibration n'entre pas dans `counted_tests()` : mesurer un signal « pour
   calibrer » avant sa mesure officielle serait un regard gratuit sur le
   résultat, invisible au dénominateur. Un signal déjà mesuré ne peut donc pas
   entrer dans un lot — il n'y serait plus à l'aveugle.

Alors seulement : `p` unilatéral au signe pré-enregistré (`EXPECTED_SIGN`,
`D07`), `BH` à `q` = 0,10 sur les `m` `p`-values du lot.

**AUCUN IC N'EST CALCULÉ ICI.** Les IC ont déjà été écrits par le harnais,
par `evaluate()`, ailleurs. Ce script ne fait que lire le registre et
juger — c'est la distinction que `registry/SCHEMA.md` fait entre calculer un
nombre et statuer dessus.

    python scripts/gate_09.py           # juge le lot réel
    python scripts/gate_09.py --check   # auto-test du calcul BH sur des cas
                                         # fabriqués, contre le tableau de D25 —
                                         # NE JUGE RIEN DE RÉEL, ne lit ni le
                                         # registre ni hypotheses/LOT-09.json
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scipy import stats  # noqa: E402

from harness import registry  # noqa: E402

LOT_FILE = REPO / "hypotheses" / "LOT-09.json"
CORR_FILE = REPO / "scripts" / "out" / "lot_09_correlations.json"
HYPOTHESES_DIR = REPO / "hypotheses"
SIGNALS_DIR = REPO / "signals"
STAGE = "09-passage"
# D29 : une mesure du lot porte sur la tranche `pool` ENTIÈRE, à un instant
# unique et fixé d'avance — celui des 56 tests comptés avant elle. Une date
# d'évaluation choisie par hypothèse serait un bouton : raccourcir l'échantillon
# jusqu'à ce qu'un signal passe.
SLICE_REQUIRED = "pool"
ASOF_REQUIRED = "2023-12-29 20:00:00+00:00"
Q_REQUIRED = 0.10  # D25 C3
N_REQUIRED = 50  # D25 C2


def one_sided_p(t_stat: float, expected_sign: int) -> float:
    """`p` pour un test unilatéral au signe pré-enregistré (`D25` C1).

    `p = 1 - Phi(signe * t)` : ne rejette que dans le sens annoncé avant la
    mesure. Un `t` du bon ordre de grandeur mais du mauvais signe rend un `p`
    proche de 1, jamais une découverte — c'est une réfutation, pas un signal
    manqué de peu. Approximation normale, pas Student : c'est celle que `D25`
    a elle-même utilisée pour construire son tableau de seuils, et `--check`
    le vérifie en le relisant à l'envers.
    """
    if t_stat is None or t_stat != t_stat:  # NaN : pas comparable à 0 ni à 1
        return float("nan")
    if expected_sign not in (1, -1):
        raise ValueError(f"expected_sign doit être +1 ou -1, reçu {expected_sign!r}")
    return float(1.0 - stats.norm.cdf(expected_sign * t_stat))


def benjamini_hochberg(pvalues: dict[str, float], q: float) -> list[str]:
    """Le pas de BH : le plus grand rang `i` tel que `p_(i) <= (i/m) * q`.

    Rend les clés retenues, dans l'ordre des `p`. Un `p` `NaN` — un test non
    calculable — est exclu du dénominateur `m` et jamais retenu : il n'a rien
    échoué, il n'existe pas pour la procédure.
    """
    items = [(k, p) for k, p in pvalues.items() if p == p]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    if m == 0:
        return []
    seuil_max = 0
    for i, (_, p) in enumerate(items, start=1):
        if p <= (i / m) * q:
            seuil_max = i
    return [k for k, _ in items[:seuil_max]]


def est_officielle(r: dict, entry: dict, hash_courant: str) -> bool:
    """La ligne est-elle LA mesure prévue de cette hypothèse du lot ?"""
    return (
        r.get("hypothesis_ref") == entry.get("ref")
        and r.get("signal_id") == entry.get("signal_id")
        and r.get("stage") == STAGE
        and r.get("code_hash") == hash_courant
        and r.get("data_slice") == SLICE_REQUIRED
        and r.get("asof") == ASOF_REQUIRED
    )


def lignes_hors_protocole(
    entries: list[dict], registre: list[dict], hash_courant: str
) -> list[dict]:
    """Les lignes du registre qui touchent le lot sans en être la mesure officielle (`D28`).

    Une ligne TOUCHE le lot si elle porte le `signal_id` d'un de ses signaux ou
    la `ref` d'une de ses hypothèses — calibrations comprises, puisque c'est
    précisément par elles qu'un regard échapperait à `counted_tests()`. Elle est
    officielle si elle est la mesure `09-passage`, sous le harnais courant, d'une
    entrée du lot, `ref` et `signal_id` concordants. Tout le reste est rendu :
    une liste vide est la seule réponse acceptable.

    Ce que ça ne voit pas : une ligne dont `signal_id` ET `hypothesis_ref`
    auraient été écrasés par l'argument `extra` de `registry.settle()`. Ce trou
    est dans le harnais figé ; `D28` § Ce qui reste ouvert.
    """
    signal_ids = {e.get("signal_id") for e in entries}
    refs = {e.get("ref") for e in entries}
    hors = []
    for r in registre:
        touche = r.get("signal_id") in signal_ids or (
            r.get("hypothesis_ref") is not None and r.get("hypothesis_ref") in refs
        )
        if touche and not any(est_officielle(r, e, hash_courant) for e in entries):
            hors.append(r)
    return hors


def importer_par_signal_id(signal_id: str):
    for chemin in sorted(SIGNALS_DIR.glob("*.py")):
        if chemin.name in ("_common.py", "__init__.py"):
            continue
        nom = ".".join(chemin.relative_to(REPO).with_suffix("").parts)
        module = importlib.import_module(nom)
        if getattr(module, "SIGNAL_ID", None) == signal_id:
            return module
    raise LookupError(
        f"aucun module de signals/ ne porte SIGNAL_ID={signal_id!r} — "
        "une hypothèse ne se juge pas sans le signe que son signal déclare"
    )


def run_check() -> int:
    verifs: list[tuple[str, bool]] = []

    def verifier(nom: str, condition: bool) -> None:
        verifs.append((nom, bool(condition)))

    # Le format le plus fort disponible : relire D25 à l'envers. Ces quatre
    # couples (t, p) sont recopiés de son tableau, pas recalculés ici.
    for t, p_attendu in ((2.88, 0.0020), (2.65, 0.0040), (2.51, 0.0060), (2.33, 0.0100)):
        p = one_sided_p(t, +1)
        verifier(f"D25 : t={t} donne p<={p_attendu} (mesuré {p:.4f})", p <= p_attendu + 5e-4)

    verifier(
        "signe correct : p petit pour un t fort dans le sens attendu", one_sided_p(4.0, +1) < 0.001
    )
    verifier(
        "signe inversé : p proche de 1, jamais une découverte déguisée",
        one_sided_p(4.0, -1) > 0.999,
    )
    nan_p = one_sided_p(float("nan"), +1)
    verifier("t NaN -> p NaN, jamais 0 ni 1", nan_p != nan_p)
    try:
        one_sided_p(1.0, 0)
        verifier("expected_sign=0 refusé", False)
    except ValueError:
        verifier("expected_sign=0 refusé", True)

    # BH lui-même : 5 hypothèses pile à leur seuil de rang (N=50, q=0.10),
    # 45 loin au-dessus — elles ne doivent jamais entrer dans la sélection.
    seuils = {f"H{i:02d}": (i / 50) * Q_REQUIRED for i in range(1, 6)}
    reste = {f"X{i:02d}": 0.5 for i in range(45)}
    retenues = set(benjamini_hochberg({**seuils, **reste}, Q_REQUIRED))
    verifier(
        "BH retient exactement les 5 premiers rangs à leur seuil exact", retenues == set(seuils)
    )

    # Un cran au-dessus de son seuil de rang fait tomber CE rang, sans faire
    # tomber ceux qui sont sous lui — BH est un pas, pas un seuil plat par test.
    pvals2 = dict(seuils, **reste)
    pvals2["H05"] = seuils["H05"] * 1.2
    retenues2 = set(benjamini_hochberg(pvals2, Q_REQUIRED))
    verifier(
        "un p qui dépasse son seuil de rang tombe sans entraîner les rangs sous lui",
        retenues2 == {"H01", "H02", "H03", "H04"},
    )

    # Un p NaN est exclu du dénominateur, jamais traité comme 0 ni comme 1.
    retenues3 = set(benjamini_hochberg({"A": 0.001, "B": float("nan"), "C": 0.5}, 0.10))
    verifier("un p NaN est exclu de BH plutôt que traité comme 0 ou comme 1", retenues3 == {"A"})

    verifier(
        "lot de p-values vide -> aucune découverte, pas d'exception",
        benjamini_hochberg({}, 0.10) == [],
    )

    # D28 : aucune ligne ne touche le lot hors de sa mesure officielle. Registre
    # fabriqué, jamais le vrai.
    h = "0123456789abcdef"
    lot = [{"ref": "H05", "signal_id": "sig-a"}, {"ref": "H06", "signal_id": "sig-b"}]

    def ligne(signal_id, ref, stage=STAGE, code_hash=h, asof=ASOF_REQUIRED):
        return {"signal_id": signal_id, "hypothesis_ref": ref, "stage": stage,
                "code_hash": code_hash, "data_slice": SLICE_REQUIRED, "asof": asof}

    propre = [ligne("sig-a", "H05"), ligne("sig-b", "H06"),
              ligne("calibration-bruit", None), ligne("autre", "H01")]
    verifier("D28 : un registre où le lot n'a que ses mesures officielles passe",
             lignes_hors_protocole(lot, propre, h) == [])
    cas = {
        "une calibration (ref nulle) d'un signal du lot": ligne("sig-a", None, "04-rapport-ic"),
        "une mesure antérieure d'une ref du lot, autre stage":
            ligne("sig-a", "H05", "04-rapport-ic"),
        "une mesure d'une ref du lot sous un harnais périmé":
            ligne("sig-b", "H06", code_hash="f" * 16),
        "une ref du lot mesurée sous un autre signal_id": ligne("sig-z", "H05"),
        "un signal du lot mesuré sous une ref hors lot": ligne("sig-b", "H99"),
        "une mesure du lot sur un échantillon raccourci (D29)":
            ligne("sig-a", "H05", asof="2019-12-31 20:00:00+00:00"),
    }
    for nom, intrus in cas.items():
        verifier(f"D28 : refuse {nom}",
                 lignes_hors_protocole(lot, propre + [intrus], h) == [intrus])
    # Une mesure officielle en double n'est pas « hors protocole » : elle est
    # officielle deux fois, et c'est la vérification 4 qui la refuse.
    # D29 : l'asof exigé tombe dans la tranche `pool`, sur sa DERNIÈRE séance
    # ouvrée — la tranche entière, pas un échantillon raccourci. Relu dans le
    # catalogue, pas recopié.
    import pandas as pd  # noqa: PLC0415

    from panel.catalogue import load_catalogue  # noqa: PLC0415

    tranche = load_catalogue().slices[SLICE_REQUIRED]
    asof = pd.Timestamp(ASOF_REQUIRED)
    fin = pd.Timestamp(tranche.end)
    ouvres_apres = pd.bdate_range(asof.date() + pd.Timedelta(days=1), fin)
    verifier(
        f"D29 : l'asof exigé ({ASOF_REQUIRED}) est dans la tranche {SLICE_REQUIRED!r} "
        f"et sur sa dernière séance ouvrée (fin {tranche.end})",
        pd.Timestamp(tranche.start) <= asof.tz_localize(None) <= fin + pd.Timedelta(days=1)
        and len(ouvres_apres) == 0,
    )
    verifier("D28 : un doublon officiel est laissé à la vérification 4",
             lignes_hors_protocole(lot, propre + [ligne("sig-a", "H05")], h) == [])

    for nom, ok in verifs:
        print(f"  {'OK' if ok else 'ECHEC'}  {nom}")
    echoues = [nom for nom, ok in verifs if not ok]
    print(f"\n{len(verifs)} vérifications, {len(echoues)} échec(s)")
    print(
        "\nCeci n'a jugé aucune hypothèse réelle : ni le registre ni "
        "hypotheses/LOT-09.json n'ont été lus."
    )
    return 1 if echoues else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La porte 09 — D25")
    ap.add_argument(
        "--check",
        action="store_true",
        help="auto-test du calcul BH sur des cas fabriqués, NE JUGE RIEN de réel",
    )
    a = ap.parse_args(argv)

    if a.check:
        return run_check()

    if not LOT_FILE.is_file():
        print("PORTE 09 : NON FRANCHIE")
        print(f"  {LOT_FILE.relative_to(REPO)} n'existe pas : aucun lot n'est déclaré.")
        print("  D25 C2 exige un lot clos AVANT la première mesure. Tant qu'il n'existe")
        print("  pas, il n'y a rien à juger — ce n'est pas une anomalie, c'est l'état")
        print("  attendu avant que la phase 09 ait produit ses 33 fiches et signaux")
        print("  manquants. Voir `python scripts/gate_09.py --check` pour vérifier le")
        print("  calcul lui-même sans attendre le lot.")
        return 1

    lot = json.loads(LOT_FILE.read_text(encoding="utf-8"))
    entries = lot.get("hypotheses") or []
    q = lot.get("q")
    declared_at = lot.get("declared_at")

    fautes: list[str] = []
    if q != Q_REQUIRED:
        fautes.append(f"q déclaré = {q!r} ; D25 C3 exige {Q_REQUIRED} sauf amendement écrit à D25")
    if len(entries) != N_REQUIRED:
        fautes.append(
            f"{len(entries)} hypothèse(s) déclarée(s) ; D25 C2 exige {N_REQUIRED} "
            "sauf amendement écrit à D25"
        )
    refs = [e.get("ref") for e in entries]
    if len(set(refs)) != len(refs):
        fautes.append("des `ref` sont dupliqués dans le lot")
    if not declared_at:
        fautes.append(
            "`declared_at` manque : un lot sans date ne prouve pas sa clôture avant mesure"
        )

    if fautes:
        print("PORTE 09 : NON FRANCHIE — le lot lui-même est mal formé.")
        for f in fautes:
            print(f"  - {f}")
        return 1

    for e in entries:
        ref = e.get("ref", "")
        if not list(HYPOTHESES_DIR.glob(f"{ref}-*.md")):
            fautes.append(
                f"{ref} : aucun fichier hypotheses/{ref}-*.md — une hypothèse non "
                "écrite n'est pas une hypothèse (invariant IV)"
            )

    if not CORR_FILE.is_file():
        fautes.append(
            f"{CORR_FILE.relative_to(REPO)} n'existe pas : D25 exige la matrice de "
            "corrélation du lot AVANT BH — sans elle, le contrôle BH est une "
            "hypothèse non vérifiée"
        )
    else:
        corr = json.loads(CORR_FILE.read_text(encoding="utf-8"))
        attendus = sorted({e.get("signal_id") for e in entries})
        obtenus = sorted(corr.get("signal_ids") or [])
        if obtenus != attendus:
            fautes.append(
                "la matrice de corrélation ne couvre pas exactement les signaux du "
                f"lot : {len(obtenus)} déclaré(s) contre {len(attendus)} attendu(s)"
            )
        mesuree_le = corr.get("measured_at") or ""
        if not mesuree_le or mesuree_le < declared_at:
            fautes.append("la matrice de corrélation n'est pas datée après la clôture du lot")

    if fautes:
        print("PORTE 09 : NON FRANCHIE")
        for f in fautes:
            print(f"  - {f}")
        return 1

    registre = registry.read_all()
    hash_courant = registry.code_hash()
    pvalues: dict[str, float] = {}
    diagnostics: list[tuple[str, str, float, int, float]] = []

    for e in entries:
        ref, signal_id = e["ref"], e["signal_id"]
        lignes = [r for r in registre if est_officielle(r, e, hash_courant)]
        if not lignes:
            fautes.append(
                f"{ref} : aucune mesure au registre (stage={STAGE!r}, harnais "
                f"courant, tranche {SLICE_REQUIRED!r}, asof {ASOF_REQUIRED}) — une "
                "hypothèse manque, D25 refuse le verdict"
            )
            continue
        if len(lignes) > 1:
            fautes.append(
                f"{ref} : {len(lignes)} mesures au registre — ambigu, une seule "
                "est attendue par hypothèse dans un lot clos (D25 C2)"
            )
            continue
        t = lignes[0].get("t_stat")
        try:
            module = importer_par_signal_id(signal_id)
        except LookupError as exc:
            fautes.append(f"{ref} : {exc}")
            continue
        signe = module.EXPECTED_SIGN
        p = one_sided_p(t, signe)
        pvalues[ref] = p
        diagnostics.append((ref, signal_id, t, signe, p))

    for r in lignes_hors_protocole(entries, registre, hash_courant):
        fautes.append(
            f"{r.get('test_id', '?')} : ligne hors protocole sur le lot — signal "
            f"{r.get('signal_id')!r}, ref {r.get('hypothesis_ref')!r}, stage "
            f"{r.get('stage')!r}, harnais {r.get('code_hash')!r}, tranche "
            f"{r.get('data_slice')!r}, asof {r.get('asof')!r}. Un signal du lot ne se "
            f"mesure qu'une fois, sous sa ref, au stage {STAGE}, sur toute la tranche "
            f"{SLICE_REQUIRED} à {ASOF_REQUIRED} (D28, D29)"
        )

    if fautes:
        print("PORTE 09 : NON FRANCHIE")
        for f in fautes:
            print(f"  - {f}")
        return 1

    retenues = set(benjamini_hochberg(pvalues, Q_REQUIRED))

    print(f"lot : {len(entries)} hypothèses, clos le {declared_at}, q = {Q_REQUIRED}\n")
    for ref, signal_id, t, signe, p in sorted(diagnostics, key=lambda d: d[4]):
        marque = "RETENU" if ref in retenues else "  —   "
        t_txt = f"{t:+7.3f}" if isinstance(t, (int, float)) and t == t else "   n/a "
        print(f"  {marque}  {ref:5s} {signal_id:45s} t={t_txt} signe attendu {signe:+d}  p={p:.4f}")

    print(
        f"\nPORTE 09 : FRANCHIE — {len(retenues)} hypothèse(s) retenue(s) sur {len(entries)}, "
        f"BH q={Q_REQUIRED}"
    )
    if retenues:
        print(
            "  Sur les hypothèses retenues, une sur dix sera fausse EN MOYENNE (D25 C3) : "
            "ce n'est pas rassurant, c'est le prix payé pour ne pas jeter les vraies. La phase "
            "10 (backtest) et la phase 15 (holdout) restent les vraies vérifications."
        )
    else:
        print(
            "  Zéro retenue est un résultat VALIDE de la procédure, pas un échec de la "
            "porte : la porte juge que le protocole a été suivi, pas que la pêche a été "
            "bonne (wiki/hot.md : « le corpus implémentable est attendu mort »)."
        )
    print(
        f"\n  registre : {len(registre)} lignes, {registry.counted_tests()} test(s) compté(s) "
        f"(hors calibrations), harnais {hash_courant}"
    )
    print("  AUCUN IC N'EST CALCULÉ ICI — ce script juge des lignes déjà écrites par le harnais.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
