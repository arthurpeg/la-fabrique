---
type: phase
updated: 2026-09-17
status: franchie
phase: 04
gate: aucun chemin de code ne produit un IC sans écrire au registre ; la tranche holdout est inaccessible par construction
sources: [ETAT.md, registry/SCHEMA.md, decisions/DECISION-05-registre-incontournable.md]
---

# Phase 04 — Le registre et le verrou du holdout

**Franchie le 2026-09-17**, `scripts/gate_04_registry.py`, 1 484 vérifications.
Fin de l'Acte I.

## La porte

Aucun chemin de code ne produit un IC sans écrire au registre ; la tranche
`holdout` (2024-01-01 → 2026-08-28) est **inaccessible par construction**.

## Pourquoi cette phase existe

Les invariants III et V ne sont pas des consignes : ce sont des propriétés à
fabriquer. Un registre qu'on alimente « avec discipline » n'est pas un registre —
il l'est le jour où il n'existe plus de chemin pour l'éviter.

Et le compte ne se rattrape pas : **ajouté après coup, il est perdu**. D'où la
construction **avant le premier signal**.

## Ce qui a été construit

**Le nombre n'existe pas avant sa ligne** (`decisions/DECISION-05-registre-incontournable.md`).
Avant, l'invariant
III tenait parce que `evaluate()` était le seul point d'entrée *et* qu'il écrivait
— deux gestes, donc un état du monde où le premier a eu lieu sans le second.
Depuis, c'est un seul geste :

1. `registry.open_test(...)` délivre un **jeton**, qui exige de nommer le signal,
   l'hypothèse, le stage, la tranche et l'horizon — *avant* que le résultat
   existe. Une hypothèse nommée après coup n'est pas une hypothèse (invariant IV).
2. `metric.cell_ic` et `metric.record_pooled` **réclament ce jeton**.
3. `record_pooled` **écrit la ligne, puis rend la valeur**. Dans cet ordre.
4. Le jeton s'use : un jeton, une ligne, un IC.
5. `_pool` et `_deflated_t` sont privées — `harness.metric` ne publie plus rien
   qui rende un IC.

**Le holdout** ne s'ouvre qu'avec un `UnsealToken`, produit par
`panel.unseal.unseal_holdout(reason=...)`, qui exige une phrase exacte dans
l'environnement **et** une raison écrite en prose, et qui **inscrit le geste dans
`registry/unseal.jsonl` avant de rendre le jeton**. Une valeur vraie d'un autre
type n'est pas une clé. Voir [[concepts/tranche]].

**Le schéma est appliqué à l'écriture** : `registry/SCHEMA.md` fixe onze champs
obligatoires, quatre facultatifs, huit stages, deux tranches — et
`registry.validate_record` les impose. Une ligne non conforme n'est pas écrite.

## Ce que ça ne prétend pas

Python n'a pas d'encapsulation réelle : `from harness.metric import _pool` rend
encore un nombre. La porte démontre un périmètre plus étroit et plus vrai —
**aucun chemin public**, et **aucun module de ce dépôt** ne prend le chemin privé,
vérifié par analyse syntaxique des 27 modules. Voir
[[Failed Ideas/ledger#F16]].

## Le prix payé

Le harnais était **figé** depuis la porte 03 ; cette phase l'a modifié. Le
`code_hash` passe de `8c1b6512…` à `5d6ce982…`, donc tous les résultats antérieurs
sont **périmés** — la règle s'applique. Coût réel : **nul**. Les 25 lignes
concernées étaient toutes des calibrations, `counted_tests()` valait 0. Le même
changement après le premier lot de signaux aurait coûté le lot.
La porte 03 a été **rejouée** sous le nouveau harnais : mêmes chiffres,
IC `+0,00108`, `t` final `+0,06`.

## Pièges connus

- **Le fichier ne se modifie qu'en ajoutant.** La porte le vérifie contre la
  version commitée — et attention à l'encodage de cette comparaison
  ([[lessons|L09]]).
- **Perdre le registre coûte la validité statistique de tout ce qui précède.**
- Si `registry/unseal.jsonl` contient un jour **deux** lignes, l'invariant V est
  rompu et tout ce qui suit est de la validation, pas du holdout.

## Voir aussi

[[phases/phase-03-harnais-ic]] · [[concepts/registre]] · [[concepts/tranche]] ·
[[concepts/comptage-des-tests]] · [[Failed Ideas/ledger#F15]]
