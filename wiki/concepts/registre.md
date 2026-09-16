---
type: concept
updated: 2026-09-16
status: stable
sources: [CLAUDE.md, registry/SCHEMA.md, registry/tests.jsonl]
---

# Registre

**`registry/tests.jsonl` — une ligne JSON par IC calculé. Append-only. Le fichier
le plus irremplaçable du dépôt.**

## Ce que ça veut dire ici

Le registre **compte combien de fois on a regardé les données**. Ce compte rend
calculables les seuils de correction pour tests multiples : sans lui, on ne sait
pas si un IC de 0,04 est un résultat ou le meilleur de deux cents tirages. Il
rend aussi honnête le Sharpe dégonflé de la phase 15
([[research/bailey-2014-deflated-sharpe]]).

Schéma d'une ligne (`registry/SCHEMA.md` fait foi) :

```
{ test_id, timestamp, signal_id, hypothesis_ref, stage,
  data_slice, horizon, ic, t_stat, requested_by, code_hash }
```

## Ce que ça ne veut pas dire

- **Ce n'est pas un journal qu'on peut compléter après coup.** Ajouté après coup,
  le compte est perdu : on ne reconstitue pas a posteriori le nombre de choses
  qu'on a essayées, et **tout l'appareil statistique s'effondre rétroactivement**.
  C'est pour cela qu'il se construit en phase 04, avant le premier signal.
- **Ce n'est pas modifiable.** Aucune suppression, aucune réécriture, aucun tri,
  aucun reformatage en masse. Une ligne écrite par erreur **reste** ; on ajoute
  une ligne qui la corrige. Même règle que `LECONS.md`.
- **Ce n'est pas le wiki.** Aucune page de wiki ne tient de compte de tests. Les
  chiffres ne s'y écrivent que recopiés d'un rapport d'IC, avec leur `test_id`
  (`wiki/SCHEMA.md` § 0).

## La règle dure

> Aucun chemin de code ne calcule un IC sans écrire ici — invariant III.

Ce n'est pas une convention d'usage mais une propriété à **fabriquer** en
[[phases/phase-04-registre-et-holdout]] : l'écriture doit être sur le chemin, pas
à côté.

## Ce qui compte pour un test

Voir [[concepts/comptage-des-tests]]. En résumé : un signal sur la grille = 1 ;
les k plis d'un walk-forward = 1 ; une cellule choisie après coup = interdit, et
pré-enregistrée = +1.

## État actuel

**0 ligne.** Le registre est amorcé, vide, et le restera jusqu'à la phase 04.

## Où c'est fixé

`registry/SCHEMA.md` · `CLAUDE.md` invariant III et § Les interdits · `D01` §4

## Voir aussi

[[concepts/ic]] · [[concepts/comptage-des-tests]] · [[concepts/tranche]]
