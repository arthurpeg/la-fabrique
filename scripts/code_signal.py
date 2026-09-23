"""Le harnais du codeur de signal — phase 08, `D23`.

Il ne contient **aucune intelligence de codage**. Il prépare ce que le codeur
voit, fige ce qu'il a produit, puis fait juger. Le codage lui-même est fait par
une **session séparée**, et c'est le protocole, pas un détail d'implémentation.
Même forme que `corpus/extract_fiche.py` pour la phase 07, et pour la même
raison.

## Qui peut être le codeur — `D23` § Ce que ça verrouille

**Une session qui a lu `signals/` ne peut pas être le codeur.** Elle y
trouverait `gao_2018_intraday_momentum.py`, `baltussen_2021_intraday_momentum.py`
et `heston_2010_periodicity.py` — trois implémentations écrites à la main, dont
deux sont les étalons désignés par `D06`. Elle ne coderait pas la fiche, elle
recopierait un voisin, et les six conditions passeraient pour la pire des
raisons. Même piège que le trieur (`F42`) et l'extracteur (`D16`), même parade.

Elle ne doit pas non plus avoir lu `hypotheses/` : un codeur qui connaît
l'hypothèse pré-enregistrée d'un papier connaît la réponse attendue, et
l'invariant IV veut que l'hypothèse précède le résultat, pas qu'elle le guide.

## Ce que le codeur voit, limitativement

1. **la fiche** — et elle seule, comme source sur le papier ;
2. **le contrat de `D07`** — ce qu'un module de signal doit exposer ;
3. **la liste blanche des imports** de `sandbox/scan.py` ;
4. **l'interface de `signals/_common.py`** — ses signatures, pas son fichier ;
5. **la règle de `S5`**, qui est celle qui fera échouer la plupart des essais.

**Et rien d'autre.** Ni `signals/`, ni `hypotheses/`, ni `decisions/`, ni les
fiches des autres papiers.

**Le point 4 mérite d'être défendu.** `_common.py` vit dans `signals/`, que le
codeur ne doit pas lire. Mais ce module est de l'**outillage partagé** — il dit
comment obtenir les barres d'une cellule et à quelle barre un score se pose — et
non une réponse : `score_signal.py` l'exempte d'ailleurs de `S5` par
`MODULES_DU_DEPOT`. Priver le codeur de son interface l'obligerait à réécrire
cette mécanique, donc à porter des constantes d'horloge que `S5` refuserait
ensuite à bon droit. La consigne en donne donc un **résumé écrit à la main**, et
non le fichier : le docstring de `_common.py` mentionne ce dont parlent les
hypothèses de référence, et le recopier serait une fuite.

## Ce que le codeur ne peut pas faire, et qu'il faut lui dire

`HYPOTHESIS` doit valoir `None`. Le contrat de `D07` l'accepte — *« None pour un
signal qui n'affirme encore rien »* — et c'est la seule valeur honnête : le
codeur ne voit pas `hypotheses/`, donc tout identifiant qu'il écrirait serait
inventé. Rattacher le signal à une hypothèse pré-enregistrée est un geste
humain, postérieur, et `D23` ne le lui délègue pas.

    python scripts/code_signal.py --list
    python scripts/code_signal.py --prepare <fiche_id>
    python scripts/code_signal.py --record <module.py>          # fige S6
    python scripts/code_signal.py --judge <module.py> --fiche <fiche.json>
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from sandbox import contract, scan  # noqa: E402

FICHES = REPO / "corpus" / "fiches"
SIGNALS = REPO / "signals"
WORK = REPO / "corpus" / "consignes-signaux"
PRODUCED = SIGNALS / "PRODUCED.json"
JUGE = REPO / "scripts" / "score_signal.py"

# Les champs de la fiche que `S5` fouille. Ils sont ici pour que la consigne les
# NOMME au codeur : une condition à tolérance zéro qu'on ne lui annonce pas est
# un piège, pas un seuil. La liste fait foi dans `scripts/score_signal.py` ;
# celle-ci est lue depuis là, jamais recopiée.
from score_signal import CHAMPS_RECETTE, CONVENTIONS, DU_DEPOT  # noqa: E402

CONSIGNE = """\
# Consigne de codage — phase 08 de La Fabrique

Tu produis **un module Python de signal** à partir d'une fiche de papier
académique, et de rien d'autre. Tu n'as pas accès au reste du projet, et c'est
voulu : il contient trois signaux déjà écrits à la main, et un codeur qui les
lirait recopierait un voisin au lieu de coder cette fiche.

## Ce que tu rends

Un **seul fichier Python**, écrit à `{chemin}`. Rien d'autre : pas de test, pas
de notebook, pas de modification d'un fichier existant.

## Le contrat — `D07`

Le module expose exactement ceci :

```python
SIGNAL_ID = "{signal_id}"      # cette chaîne, à la lettre
HYPOTHESIS = None              # None, et rien d'autre — voir plus bas
PAPER = "<auteurs (année), titre, revue>"
EXPECTED_SIGN = +1             # ou -1. JAMAIS 0, jamais None

def scores(panel, cells=None, horizon_bars: int = 30):
    \"\"\"Rend {{(root, window): pd.Series}}.\"\"\"
```

- `EXPECTED_SIGN` dit dans quel sens le papier prétend que le signal prédit.
  Un signal dont on n'attend aucun signe est un signal dont on n'attend rien.
- `HYPOTHESIS` vaut **`None`**. Les hypothèses pré-enregistrées du projet ne te
  sont pas montrées ; tout identifiant que tu écrirais serait inventé.
- `scores()` rend un dictionnaire dont les clés sont des paires
  `(root, window)` présentes dans `panel.cells()`, et les valeurs des
  `pd.Series` indexées par un `DatetimeIndex` **avec fuseau**. Une cellule sans
  score **s'omet** : elle ne se déclare pas avec une série vide.

## Les six conditions, toutes à tolérance zéro

| | |
|---|---|
| `S1` | le contrat ci-dessus est respecté |
| `S2` | aucun import hors de la liste blanche |
| `S3` | **causalité** : les scores sont identiques sur un panel tronqué et sur le panel entier |
| `S4` | les scores ne sont pas dégénérés, et tombent sur des barres mesurables |
| `S5` | **toute constante numérique du code se retrouve dans la fiche** |
| `S6` | zéro retouche manuelle après production |

### `S2` — la liste blanche des imports

Seuls ces modules racines sont autorisés :

{imports}

Sont refusés, entre autres : tout accès réseau, `open()`, `eval`, `exec`,
`compile`, `globals`, `locals`, et les attributs `__globals__`, `__class__`,
`__subclasses__`, `__dict__`, `__mro__`.

### `S3` — la causalité, qui est la vraie difficulté

Le panel refuse déjà de te montrer le futur. Mais **tu peux encore regarder en
avant à l'intérieur de ce qu'il te montre**, en lisant une barre postérieure à
celle que tu notes. La règle tient en une ligne :

> un prédicteur reçoit les clôtures de sa séance et la **position** de la barre
> notée, et ne lit **rien au-delà de cette position**.

En particulier : `close.shift(-n)` est du look-ahead écrit en toutes lettres, et
« la barre qui est à trente barres de la fin du groupe » en est aussi — savoir où
le groupe finit demande de connaître l'avenir. Un ancrage se lit **sur l'horloge**
(la distance à la clôture déclarée de la fenêtre), jamais sur les données.

Un test automatique compare tes scores sur un panel tronqué et sur le panel
entier. S'ils diffèrent d'un seul point, le signal est refusé.

### `S5` — celle qui fera échouer la plupart des essais

**Chaque nombre écrit en dur dans ton code doit se retrouver dans la fiche**,
dans l'un de ces champs, et seulement ceux-là :

{champs}

Si la fiche dit « quarante-cinq minutes » et que tu écris `FENETRE = 30`, le
signal tournera, sera causal, ne sera pas dégénéré — et ne codera pas ce papier.
C'est exactement ce que cette condition attrape.

Trois échappatoires, **nommées et closes** :

- les conventions de langage : {conventions} ;
- les valeurs du dépôt, qui ne viennent pas du papier : {du_depot} ;
- un nombre en commentaire ou en docstring **ne justifie rien** : le contrôle
  lit l'arbre syntaxique, pas le texte.

**Si un paramètre te manque, ne l'invente pas.** C'est un interdit
constitutionnel du projet, pas une préférence de style. Écris le module avec ce
que la fiche donne, et dis dans le docstring ce qui manquait et ce que tu as fait
à la place.

## L'outillage partagé — `signals/_common.py`

Tu peux l'importer (`from signals import _common`). Ses constantes ne te sont
pas comptées. Voici son interface, et c'est tout ce que tu en sauras :

```python
def cell_bars(panel, root: str, window: str) -> tuple[pd.Series, pd.Series]:
    \"\"\"Les clôtures recollées d'une cellule, et la séance de chaque barre.

    Recollées, comme les rendements contre lesquels le harnais mesure : un
    mouvement brut à travers un raccord de contrat est un artefact.\"\"\"

def run(panel, predictor, cells=None, horizon_bars: int = 30) -> dict:
    \"\"\"Applique un prédicteur à chaque cellule retenue du panel.

    `predictor(closes: pd.Series, position: int) -> float | None` reçoit les
    clôtures d'UNE séance et la position de la barre notée, et ne doit rien
    lire au-delà de cette position. Rendre None n'écrit aucun score.

    Un score est produit à UNE barre par séance et par cellule : la première
    dont la distance à la clôture déclarée de la fenêtre est au plus
    `horizon_bars`. Cet ancrage se lit sur l'horloge, ce qui est précisément
    ce qui rend le signal exécutable en direct.\"\"\"
```

**Tu n'es pas obligé de t'en servir.** Si la recette de la fiche ne se pose pas
à la fin d'une fenêtre, écris ta propre mécanique — mais alors chaque constante
qu'elle porte t'est comptée par `S5`.

## Ce qu'on te demande vraiment

Pas un signal qui marche : **un signal qui code CETTE fiche**. Le harnais ne
mesurera aucun IC pour juger ton travail, et c'est délibéré — te noter sur ton
résultat te sélectionnerait sur ton résultat. Ce qui est jugé est la fidélité.

Si la fiche décrit quelque chose qui **ne se transpose pas** à neuf futures
intraday en OHLCV — un tri en déciles sur des milliers d'actions, un modèle qui
prédit une variance et non un rendement — **dis-le dans le docstring** et code la
part transposable en le déclarant. Un signal honnêtement diminué vaut mieux
qu'un signal qui prétend.

---

## LA FICHE

```json
{fiche}
```
"""


def fiches() -> dict[str, dict]:
    return {
        f.stem: json.loads(f.read_text(encoding="utf-8"))
        for f in sorted(FICHES.glob("*.json"))
    }


def module_path(fiche_id: str) -> Path:
    """Le chemin du module attendu pour une fiche. Un tiret devient un blanc."""
    return SIGNALS / (fiche_id.replace("-", "_") + ".py")


def signaux_existants() -> dict[str, Path]:
    """Les `SIGNAL_ID` déclarés par les modules de `signals/`, sans les importer.

    **Le rapprochement se fait sur `SIGNAL_ID`, pas sur le nom de fichier**, et
    ce n'est pas un raffinement : les trois signaux écrits à la main précèdent
    les fiches et portent leurs propres noms. `heston_2010_periodicity.py`
    déclare `heston-2010-periodicity` là où la fiche s'appelle
    `heston-2010-intraday-periodicity`. Rapprocher par nom de fichier les
    déclarerait tous les trois absents — c'est ce que faisait la première
    version de ce script, qui annonçait « 0 déjà codées » en en voyant trois.
    Même famille de faute que `L21` : une clé de rapprochement qui ne désigne
    pas ce qu'on croit.
    """
    out: dict[str, Path] = {}
    for p in sorted(SIGNALS.glob("*.py")):
        if p.name.startswith("_"):
            continue
        for ligne in p.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("SIGNAL_ID"):
                out[ligne.split("=", 1)[1].strip().strip("\"'")] = p
                break
    return out


def empreinte16(path: Path) -> str:
    """Les seize premiers caractères du sha256 — le format qu'attend `S6`."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def do_list() -> int:
    toutes = fiches()
    existants = signaux_existants()
    produits = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}

    codees = [fid for fid in toutes if fid in existants]
    todo = [fid for fid in toutes if fid not in existants]
    # Un signal qui ne répond à aucune fiche : les trois étalons de `D06`,
    # écrits à la main avant que les fiches existent. Ils ne sont PAS la sortie
    # du codeur, et les compter comme telle gonflerait son bilan.
    orphelins = {sid: p for sid, p in existants.items() if sid not in toutes}

    print(f"fiches                 : {len(toutes)}")
    print(f"  avec un signal       : {len(codees)}")
    print(f"  a coder              : {len(todo)}")
    for fid in todo:
        print(f"      {fid}")
    if orphelins:
        print(f"\nsignaux SANS FICHE     : {len(orphelins)} — ecrits a la main, `D06`.")
        print("  Ce ne sont PAS des sorties du codeur, et ils ne comptent pas pour la porte.")
        for sid, p in sorted(orphelins.items()):
            marque = "produit par le codeur" if sid in produits else "ecrit a la main"
            print(f"      {sid:<40} {p.name}  ({marque})")
    print("\nLa porte 08 ne demande PAS de tout coder : elle demande qu'UNE fiche")
    print("produise un signal qui passe les six conditions, sans retouche (D23).")
    return 0


def do_prepare(fiche_id: str) -> int:
    toutes = fiches()
    if fiche_id not in toutes:
        raise SystemExit(
            f"fiche inconnue : {fiche_id}\n"
            f"connues : {', '.join(sorted(toutes))}"
        )
    fiche = toutes[fiche_id]
    chemin = module_path(fiche_id)

    WORK.mkdir(parents=True, exist_ok=True)
    texte = CONSIGNE.format(
        chemin=chemin.relative_to(REPO).as_posix(),
        signal_id=fiche_id,
        imports="\n".join(f"- `{r}`" for r in sorted(scan.ALLOWED_ROOTS)),
        champs="\n".join(f"- `{c}`" for c in CHAMPS_RECETTE),
        conventions=", ".join(f"`{c}`" for c in sorted(CONVENTIONS)),
        du_depot=", ".join(f"`{v:g}` ({r})" for v, r in sorted(DU_DEPOT.items())),
        fiche=json.dumps(fiche, ensure_ascii=False, indent=2),
    )
    out = WORK / f"{fiche_id}.md"
    out.write_text(texte, encoding="utf-8")

    print(f"consigne ecrite : {out.relative_to(REPO)}  ({out.stat().st_size / 1000:.0f} ko)")
    print(f"module attendu  : {chemin.relative_to(REPO).as_posix()}")
    print("\nELLE NE DOIT PAS ETRE DONNEE A UNE SESSION QUI A LU signals/ NI")
    print("hypotheses/ (D23). L'une contient trois implementations ecrites a la")
    print("main, l'autre les reponses attendues.")
    return 0


def enregistrer(path: Path) -> dict:
    """Fige l'etat du module AU MOMENT OU LE CODEUR VIENT DE L'ECRIRE.

    `S6` de `D23` ne se mesure que contre un etat d'origine. Sans ce registre,
    la condition est SANS OBJET — et `score_signal.py` le dit plutot que de la
    tenir pour zero, ce qui la viderait de son sens (`L22`).

    Comme pour les fiches, **une reproduction n'est pas une retouche** : quand
    le codeur repasse sur sa propre sortie apres un refus, rien n'a ete repare
    a la main. Chaque passage est donc inscrit, jamais ecrase, et le compte des
    essais est lui-meme un resultat.
    """
    # Un chemin relatif est la façon NORMALE de désigner un fichier depuis la
    # racine du dépôt, et c'est ce qu'on tape. `relative_to` le refusait.
    path = path.resolve()
    source = path.read_text(encoding="utf-8")
    fautes = scan.scan_source(source, path.name)
    if fautes:
        raise SystemExit(
            "le module ne passe pas la liste blanche, il n'est pas inscrit :\n  "
            + "\n  ".join(fautes)
        )
    signal_id = None
    for ligne in source.splitlines():
        if ligne.startswith("SIGNAL_ID"):
            signal_id = ligne.split("=", 1)[1].strip().strip("\"'")
            break
    if not signal_id:
        raise SystemExit(f"{path.name} ne declare pas de SIGNAL_ID — `S1` le refuserait")

    registre = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = registre.get(signal_id) or {"attempts": []}
    ligne.setdefault("attempts", []).append({
        "produced": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "sha256_16": empreinte16(path),
    })
    # `check_s6` lit `path` et `sha256_16` a la racine : ces deux cles font foi.
    ligne["path"] = path.relative_to(REPO).as_posix()
    ligne["sha256_16"] = ligne["attempts"][-1]["sha256_16"]
    ligne["produced"] = ligne["attempts"][-1]["produced"]
    registre[signal_id] = ligne

    PRODUCED.write_text(
        json.dumps(dict(sorted(registre.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return ligne


def do_record(path: Path) -> int:
    if not path.is_file():
        raise SystemExit(f"module introuvable : {path}")
    ligne = enregistrer(path)
    n = len(ligne["attempts"])
    print(f"inscrit : {path.stem}  (essai {n})")
    print(f"  sha256_16 {ligne['sha256_16']}")
    print(f"  produit   {ligne['produced']}")
    if n > 1:
        print(f"  LE CODEUR A REPASSE {n} FOIS. Ce n'est pas une retouche manuelle,")
        print("  et `S6` ne casse pas — mais le compte est garde.")
    print("\nTOUTE MODIFICATION A LA MAIN DE CE FICHIER CASSERA `S6`.")
    return 0


def do_judge(path: Path, fiche: Path, sans_donnees: bool) -> int:
    if not path.is_file():
        raise SystemExit(f"module introuvable : {path}")
    if not fiche.is_file():
        raise SystemExit(f"fiche introuvable : {fiche}")
    argv = [sys.executable, str(JUGE), str(path), "--fiche", str(fiche)]
    if sans_donnees:
        argv.append("--no-data")
    r = subprocess.run(argv, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(r.stdout or r.stderr)
    return r.returncode


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le harnais du codeur de signal — D23")
    ap.add_argument("--list", action="store_true", help="les fiches sans signal")
    ap.add_argument("--prepare", metavar="FICHE_ID", help="ecrire la consigne")
    ap.add_argument("--record", type=Path, metavar="MODULE", help="figer S6")
    ap.add_argument("--judge", type=Path, metavar="MODULE")
    ap.add_argument("--fiche", type=Path, metavar="FICHE.json")
    ap.add_argument("--no-data", action="store_true",
                    help="S1, S2, S5, S6 seuls — porte NON franchie sur un verdict partiel")
    a = ap.parse_args(argv)

    if a.list:
        return do_list()
    if a.prepare:
        return do_prepare(a.prepare)
    if a.record:
        return do_record(a.record)
    if a.judge:
        if not a.fiche:
            raise SystemExit("--judge demande --fiche : un signal se juge CONTRE une fiche")
        return do_judge(a.judge, a.fiche, a.no_data)
    print(__doc__)
    return 1


if __name__ == "__main__":
    # `contract` est importe pour que ce fichier casse tout de suite si le
    # contrat de `D07` bouge sans que cette consigne suive.
    assert contract.REQUIRED_ATTRS == ("SIGNAL_ID", "HYPOTHESIS", "PAPER", "EXPECTED_SIGN"), (
        "le contrat de D07 a change : la section « Le contrat » de la consigne "
        "ci-dessus ne le decrit plus, et un codeur la suivrait dans le vide."
    )
    sys.exit(main(sys.argv[1:]))
