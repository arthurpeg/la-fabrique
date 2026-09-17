# Le registre des tests

`registry/tests.jsonl` — une ligne JSON par IC calculé. JSONL, **append-only**,
versionné avec git.

Depuis la phase 04, ce fichier n'est plus une intention : **les types et les
valeurs permises ci-dessous sont appliqués à l'écriture** par
`harness/registry.py` (`validate_record`, appelé par `append`). Une ligne qui ne
les respecte pas n'est pas écrite du tout. La porte 04
(`scripts/gate_04_registry.py`) vérifie en retour que ce document et le code
disent la même chose.

## Pourquoi il existe

Le registre compte combien de fois on a regardé les données. Ce compte rend
calculables les seuils de correction pour tests multiples : sans lui, on ne sait
pas si un IC de 0,04 est un résultat ou le meilleur de deux cents tirages. Il
rend également honnête le Sharpe dégonflé calculé à la phase 15.

Ajouté après coup, le compte est perdu — on ne reconstitue pas a posteriori le
nombre de choses qu'on a essayées — et tout l'appareil statistique s'effondre
rétroactivement. C'est pour cette raison que le registre est construit en phase
04, avant le premier signal.

## Schéma d'une ligne

Onze champs obligatoires, trois facultatifs. **Aucun autre** : un champ que
personne n'a décidé est un champ que personne ne lit, et son écriture est
refusée.

| Champ | Type | Valeurs permises |
|---|---|---|
| `test_id` | chaîne | `T-AAAAMMJJTHHMMSS-xxxxxx`, six caractères hexadécimaux ; jamais réutilisé |
| `timestamp` | chaîne | instant ISO 8601 **en UTC**, à la seconde |
| `signal_id` | chaîne | non vide |
| `hypothesis_ref` | chaîne ou `null` | l'hypothèse écrite *avant* le test (invariant IV) ; `null` **uniquement** pour une calibration |
| `stage` | chaîne | `03-calibration`, `04-audit`, `04-rapport-ic`, `05-regimes`, `06-controles`, `07-combinaisons`, `09-passage`, `15-holdout` |
| `data_slice` | chaîne | `pool` ou `holdout` — **deux, pas trois** (`D01` §5) |
| `horizon` | chaîne | `<n>min` ou `<n>h` |
| `ic` | nombre ou `null` | dans `[-1, 1]` ; un IC non calculable s'écrit `null`, **jamais `NaN`** |
| `t_stat` | nombre ou `null` | le `t` **final**, déflaté deux fois (`D04`) ; `null` si non calculable |
| `requested_by` | chaîne | `agent`, `script` ou `humain` |
| `code_hash` | chaîne | 16 caractères hexadécimaux — empreinte de `harness/*.py` au moment du calcul |

Facultatifs, écrits par le harnais quand ils ont un sens :

| Champ | Type | Contenu |
|---|---|---|
| `asof` | chaîne | l'instant d'ouverture du Panel |
| `cells` | entier ≥ 0 | le nombre de cellules qui ont produit un IC |
| `observations` | entier ≥ 0 | le nombre total d'observations poolées |
| `note` | chaîne non vide | une phrase sur les circonstances du calcul — pourquoi cette ligne existe, quand ce n'est pas évident. Jamais un résultat, jamais une justification après coup |

## Comment une ligne naît

Un IC n'est pas calculé puis enregistré : **les deux gestes n'en font qu'un**
(`D05`).

```python
ticket = registry.open_test(signal_id=..., hypothesis_ref=..., stage=...,
                            data_slice=..., horizon=...)   # rien n'est écrit
...                                                        # le calcul
metric.record_pooled(cells, ticket, ...)                   # écrit, PUIS rend
```

Le jeton est pris **avant** que le premier nombre soit touché : ce que le test
cherche doit être nommable avant que le résultat existe, sans quoi ce n'est pas
une hypothèse. Un jeton s'use une fois — un jeton, une ligne, un IC.

`harness.metric` ne publie plus aucune fonction rendant un IC poolé :
`_pool` et `_deflated_t` sont privées.

## Ce que ça ne prétend pas

Python n'a pas d'encapsulation réelle. Qui écrit `from harness.metric import
_pool` obtient encore un nombre. Le dispositif fabrique **l'impossibilité de le
faire sans un geste délibéré et visible** — un nom privé — et la porte 04 analyse
la syntaxe de chaque module du dépôt pour vérifier qu'aucun ne le fait.
Prétendre à davantage serait faux.

## Le registre du descellage

`registry/unseal.jsonl` — même régime, un fichier à part, vide jusqu'à la phase
15. Chaque ligne : `granted_at`, `reason`, `by`. **S'il contient un jour deux
lignes, l'invariant V est rompu** et tout ce qui suit est de la validation, pas
du holdout.

## Règles

- Le fichier ne se modifie qu'en **ajoutant** une ligne à la fin. Aucune
  suppression, aucune réécriture, aucun tri, aucun reformatage en masse. La
  porte 04 le vérifie contre la version commitée.
- Aucun chemin de code ne calcule un IC sans écrire ici (invariant III).
- Une ligne écrite par erreur reste. On ajoute une ligne qui la corrige.
- Une ligne dont le `code_hash` diffère du harnais courant est **périmée** : elle
  a été produite par un autre juge. Elle reste, et elle ne se compare pas.
