# Le registre des tests

`registry/tests.jsonl` — une ligne JSON par IC calculé. JSONL, **append-only**,
versionné avec git.

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

```
{ test_id, timestamp, signal_id, hypothesis_ref, stage,
  data_slice, horizon, ic, t_stat, requested_by, code_hash }
```

| Champ | Contenu |
|---|---|
| `test_id` | identifiant unique de ce test, jamais réutilisé |
| `timestamp` | date et heure du calcul, UTC, ISO 8601 |
| `signal_id` | le signal évalué |
| `hypothesis_ref` | l'hypothèse écrite *avant* le test (invariant IV) |
| `stage` | l'étape de la chaîne d'où vient la demande |
| `data_slice` | `research`, `validation` ou `holdout` |
| `horizon` | l'horizon de prédiction évalué |
| `ic` | la valeur calculée |
| `t_stat` | sa statistique de test |
| `requested_by` | qui a demandé ce test — agent, script, humain |
| `code_hash` | empreinte du code de signal et du harnais au moment du calcul |

Les types exacts, les valeurs permises et la validation seront fixés en phase 04,
en même temps que la fonction d'écriture. Ce fichier documente l'intention ; il
sera précisé, jamais contredit.

## Règles

- Le fichier ne se modifie qu'en **ajoutant** une ligne à la fin. Aucune
  suppression, aucune réécriture, aucun tri, aucun reformatage en masse.
- Aucun chemin de code ne calcule un IC sans écrire ici (invariant III).
- Une ligne écrite par erreur reste. On ajoute une ligne qui la corrige.
