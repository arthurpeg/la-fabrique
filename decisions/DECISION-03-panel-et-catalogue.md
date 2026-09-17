# D03 — Le Panel, le catalogue, et la forme que prend l'invariant II

**Date :** 2026-09-17
**Phase :** 02
**État :** prise

---

## La question

Où vit la couche de données, quel contrat expose-t-elle, et par quel mécanisme
exact le look-ahead devient-il impossible plutôt que déconseillé ? Et puisque la
définition de séance doit être déclarée par instrument (`D01` §8), sous quelle
forme existe enfin le catalogue, resté vide depuis la phase 01 ?

## Les options

**Sur l'emplacement.**

- **Dans `harness/`.** Écartée : le harnais est figé à partir de la phase 03 et
  n'évalue que des signaux. Y loger la couche de données ferait geler avec lui du
  code qui doit encore changer — la série ajustée à rebours n'est pas écrite.
- **Dans `scripts/`.** Écartée : `scripts/` contient des outils ponctuels qui
  produisent un JSON et se rejouent ; le Panel est une bibliothèque importée.
- **Un paquet `panel/` à la racine.** Retenue. Il coûte une ligne à l'arbre de
  `CLAUDE.md`, que cette décision autorise.

**Sur le mécanisme de troncature — c'est le vrai choix.**

| | **A — lire tout, trancher en mémoire** | **B — pousser la coupe dans le lecteur** |
|---|---|---|
| Ce que le processus détient | l'historique entier, futur compris | rien après l'`asof` |
| Ce qui empêche la fuite | l'API : tant que personne ne touche au cache | la physique : la donnée n'a pas été lue |
| Coût mesuré (NQ, 1,88 M barres) | 0,08 s | **0,09 s** |
| Ce qu'un bug d'API coûte | le futur, silencieusement | rien à lire |

**Sur la série ajustée à rebours, en l'absence des dates de roulement.**

- **Utiliser la détection empirique** comme liste provisoire. Écartée : ses trous
  sont systématiques et corrélés au régime (`L05`, ledger F09), et une liste
  incomplète donne le sentiment que le problème est traité.
- **Ne rien exposer.** Écartée : une méthode absente se réinvente ailleurs, au
  niveau du signal, ce que `D01` §6 interdit explicitement.
- **Exposer une méthode qui refuse.** Retenue : `panel.adjusted()` existe, et
  lève `RollDatesMissing` en nommant l'intrant manquant et qui le doit.

## Le choix

La couche de données est le paquet `panel/` ; un Panel s'ouvre **à une date**,
ne lit jamais du disque une barre postérieure à cette date, et refuse bruyamment
— plutôt qu'il n'approxime — les quatre choses qu'il ne sait pas faire
honnêtement. Le catalogue est `catalogue/catalogue.yaml`, gardé par
`catalogue/validate.py`.

## Pourquoi

Parce que l'invariant II dit *par construction, jamais par vigilance*, et que
« lire tout puis n'exposer que le passé » est de la vigilance déguisée en
architecture : il suffit d'un attribut oublié, d'un `_cache` lu par curiosité,
d'une méthode ajoutée un soir de fatigue. Pousser la coupe dans le lecteur
Parquet supprime la question : à `asof` donné, le futur n'est jamais entré dans
le processus. La mesure dit que ça ne coûte rien (0,09 s contre 0,08 s sur
1,88 million de barres) — le choix aurait été le même à coût modéré, mais il n'a
même pas fallu arbitrer.

Quatre refus, et chacun a son nom, parce qu'un `ValueError` générique ne dit pas
ce qui vient d'être tenté :

| Refus | Ce qui l'a déclenché |
|---|---|
| `LookaheadRefused` | demander à un panel un instant postérieur au sien |
| `SliceExceeded` | une date hors de la tranche travaillée |
| `HoldoutLocked` | la tranche scellée, qui s'ouvre une fois, en phase 15 |
| `RollDatesMissing` | la série ajustée, tant que les dates manquent |

Ce qui est sacrifié : un répertoire de plus, une duplication assumée de la
résolution de `RSL_DATA_DIR` entre `scripts/_common.py` et `panel/paths.py` — le
code de mesure de la phase 01 reste figé, on ne le refactorise pas pour
économiser douze lignes — et la relecture d'un fichier à chaque `asof` distinct,
qui deviendra visible le jour où le harnais balaiera des milliers de dates. Ce
jour-là, la réponse sera un cache d'objets Panel, jamais un cache de séries
entières.

## Ce que ça verrouille

### 1. Le contrat du Panel

```python
p = Panel.open(asof="2021-06-15 20:00", slice="pool")
p.universe()              # les instruments cotés à cette date, et eux seuls
p.bars("NQ", window="US") # prix bruts, jamais une barre postérieure
p.truncate(end=t)         # un panel qui en sait moins ; jamais davantage
p.adjusted("NQ")          # RollDatesMissing tant que les dates manquent
```

- `truncate` ne va que vers le passé. C'est l'accroche du test de causalité de la
  phase 05 : un signal qui tente d'avancer l'`asof` lève.
- `universe()` ne dépend que de l'`asof`. C'est la condition de passage de la
  phase 02 dans sa formulation d'origine : *le nombre d'actifs dans l'univers à
  une date passée ne change pas selon la date à laquelle on pose la question*.
- **Le prix brut reste la sortie normale de `bars()`** (`D01` §6). La série
  ajustée sera une méthode distincte, jamais un remplacement silencieux.

### 2. La date de séance, et la fenêtre qui n'appartient à personne

Une séance porte la date calendaire de sa fenêtre `US`. Décalée de +6 h sur
l'horloge de New York, une séance tombe donc sur une seule date. La frontière
entre deux séances tombe à 18:00 locales — **à l'intérieur de la plage
16:00 → 19:00, qui n'appartient à aucune fenêtre**. C'est ce qui rend la
convention sans conséquence : aucune barre négociable ne change de séance selon
l'arrondi. Cette convention, mesure de la phase 01 (`scripts/_common.py` la
déclarait explicitement provisoire), devient ici la convention du projet.

### 3. Le catalogue, et ce qu'il n'a pas le droit d'être

`catalogue/catalogue.yaml` déclare, par instrument : le fichier, la place,
l'horloge, l'appartenance à l'univers, l'historique mesuré, la règle et le cycle
de roulement, le tick **mesuré**, et par cellule les chiffres de la phase 01.

- **Un champ inconnu vaut `null` et ouvre une entrée `todos`.** Trois sont
  ouvertes : `roll-dates` (bloquant, phase 02), `multipliers` et `fees`
  (bloquants pour la calibration du harnais, phase 03).
- **Aucun nombre du catalogue n'est autoritatif par lui-même.**
  `catalogue/validate.py` re-dérive chacun depuis sa source — `a1_inventory.json`,
  `a8_session_grid.json`, le manifeste du fournisseur — et **réapplique la règle
  de rétention** aux chiffres mesurés au lieu de croire le drapeau `retained`.
  Une divergence est une erreur, pas un arbitrage.
- Un `null` sans `todo`, ou un `todo` dont plus rien n'est `null`, échoue.

### 4. La porte 02 reste fermée, et c'est désormais mécanique

`scripts/gate_02_panel.py` exécute les clauses de la porte : 31 vérifications,
30 passent. Seule échoue la clause 3b — la série ajustée des instruments réels —
faute des dates de roulement autoritatives. La porte n'est pas franchie, et le dépôt le dit
maintenant par un code de sortie, pas par une phrase dans un fichier.

### 5. `CLAUDE.md` gagne deux lignes d'arbre

`panel/` est ajouté à « Où trouver quoi », et la ligne `catalogue/` cesse de
décrire un dossier vide. C'est la seule modification de la constitution
qu'autorise cette décision.

### 6. Une dépendance de plus

`pyyaml`, pour lire le catalogue. Déclarée dans `pyproject.toml` ; **le verrou
`uv.lock` est à rejouer**, comme il l'est déjà depuis le commit `1a317d4`. La
machine courante n'a pas `uv` : les scripts ont été exécutés avec l'interpréteur
3.13 du système.

## Ce qui reste ouvert

| Point | Échéance | Statut |
|---|---|---|
| La série ajustée à rebours sur données réelles | **phase 02**, à réception des dates | l'algorithme est écrit et prouvé (complément ci-dessous) ; il refuse faute de dates. Comparer la liste reçue à la détection empirique avant d'adopter (`D01` §6) |
| Le cache d'objets Panel | ~~phase 03~~ → **phase 09**, au walk-forward | non dû : le harnais de la phase 03 évalue à une seule date, et sa porte tourne en 38 s. Ce sera un cache de panels, jamais de séries entières |
| Le calendrier de jours fériés par place | ~~phase 03~~ → **dès qu'une grandeur comptera des séances absentes** (phase 09 ou 10) | non dû : le harnais compte des observations, pas des séances. Les séances se déduisent des barres présentes |
| Multiplicateurs et frais | phase 03 | `null`, `todo`, sources nommées (`D01` §7) |
| `uv` sur cette machine | quand on y reviendra | absent ; `uv.lock` non rejoué |

## Condition de révision

1. **Les dates de roulement arrivent** — `adjusted()` s'écrit, la porte 02 se
   rejoue, et l'écart avec la détection empirique fait une entrée dans
   `LECONS.md`.
2. **Le lecteur Parquet cesse de pousser la coupe** (changement de format ou de
   bibliothèque) — le mécanisme central de cette décision tombe, et il faut le
   remplacer, pas le contourner.
3. **Le volume relu devient le goulot** en phase 03 — le cache d'objets Panel est
   tranché par écrit, et cette décision est complétée.

---

## Complément du 2026-09-17 — l'algorithme d'ajustement, écrit avant les dates

Cette décision annonçait que la série ajustée s'écrirait à réception des dates.
Elle s'écrit maintenant, et seules les **dates** manquent : le jour où elles
arrivent, la phase se ferme en remplissant un champ du catalogue et en rejouant
la porte, pas en écrivant du code sous pression. Rien de ce qui suit n'invente
une valeur de donnée.

**Multiplicatif, pas additif.** `D01` §6 dit que la série construite en `t` ne
diffère de celle construite en `t+1` que par un **facteur d'échelle uniforme**.
C'est la définition de la convention multiplicative : chaque segment antérieur à
un recollement est multiplié par les écarts qui le suivent. L'additive
décalerait les niveaux d'une constante et **ne préserverait pas les rendements**
— voir [[Failed Ideas/ledger]] F14.

**Ce que l'estimation de l'écart coûte, et qui est mesuré.** Avec une série déjà
recollée et rien d'autre, l'écart ne se lit qu'à un endroit : le rendement d'une
minute à la minute de raccord. Ce rendement contient l'écart entre contrats
**et** ce que le marché a réellement fait dans cette minute, et rien ici ne les
sépare. L'ajustement retire donc un peu de mouvement réel avec l'artefact. Ce
n'est pas une approximation cachée : la porte 02 l'injecte et le mesure — 5,0 bp
injectés à la minute de raccord, 5,0 bp absorbés, exactement. C'est la même
convention que le détecteur de la phase 01 (`scripts/roll_diagnostics.py`), et
c'est la seule chose calculable sans données par échéance.

**Ce que la porte vérifie désormais** (`scripts/gate_02_panel.py`, clause 3a, sur
un cas synthétique dont la réponse est connue) : les sauts artificiels
disparaissent ; les rendements ajustés égalent les vrais à 1e-12 ; la série
construite en `t` et celle construite plus tard ne diffèrent que par un facteur
uniforme ; un recollement postérieur à l'`asof` est invisible à l'ajustement.

**Ce que ça ne fait pas :** franchir la porte. La clause 3b — les instruments
réels — échoue toujours, et c'est de la donnée qui manque, pas du code.

**Corrigé au passage :** `truncate()` refusait d'avancer l'`asof` mais acceptait
de sortir de la tranche par le bas. Il lève désormais `SliceExceeded`, comme
`open()`.

---

## Complément du 2026-09-17 (soir) — les dates sont arrivées, la porte est franchie

Les dates de roulement ont été obtenues le jour même, par
`Historical.symbology.resolve` chez le fournisseur (`stype_in=continuous`,
`stype_out=instrument_id`, 2016-01-03 → 2026-08-29), **facturé 0,00 $** : la
symbologie n'est pas métrée. 527 roulements, déposés dans
`catalogue/roll_dates.json` avec la requête qui les a produits.

**Comparées avant d'être adoptées**, comme `D01` §6 l'exige — et le verdict est
sévère pour notre détection empirique : **62,8 % de rappel, 67 faux positifs**
(`scripts/compare_rolls.py`, `LECONS.md` L06). Deux corrections de fait en
découlent : le cycle de GC n'est pas mensuel mais irrégulier, 5,07 par an (`L07`),
et le symbole continu de FDAX **oscille** au lieu de rouler — 24 retours à une
échéance déjà quittée. Un contrôle mécanique a été ajouté au validateur : un taux
de roulement hors des bornes du cycle déclaré fait échouer le catalogue.

**Un coût s'est révélé plus large qu'annoncé.** Le complément précédent disait que
l'ajustement absorbe le mouvement réel d'**une minute**. C'est vrai pour 292 des
333 roulements visibles à mi-2023 ; pour les 41 autres — 31 % de CL, 29 % de GC —
le marché était fermé à l'instant du raccord et l'écart mesuré enjambe la
fermeture : médiane 44,9 bp contre 28,5, jusqu'à 3 648 bp (`L08`).

**Porte 02 franchie le 2026-09-17**, `scripts/gate_02_panel.py`, 103 vérifications
sur les neuf instruments de l'univers.
Les ticks ont été arrondis à la valeur que `D01` §7 déclare : la mesure brute
portait le bruit de la soustraction flottante (GC mesuré 0,0999999999994543), et
le validateur compare désormais avec une tolérance relative.

