---
type: phase
updated: 2026-09-16
status: a-faire
phase: 04
gate: aucun chemin de code ne produit un IC sans écrire au registre ; la tranche holdout est inaccessible par construction
blocked_by: phase 03
sources: [ETAT.md, registry/SCHEMA.md, CLAUDE.md]
---

# Phase 04 — Le registre et le verrou du holdout

## La porte

Aucun chemin de code ne produit un IC sans écrire au registre ; la tranche
`holdout` (2024-01-01 → 2026-08-28) est **inaccessible par construction**.

## Pourquoi cette phase existe

Les invariants III et V ne sont pas des consignes : ce sont des propriétés à
fabriquer. Un registre qu'on alimente « avec discipline » n'est pas un registre —
il l'est le jour où il n'existe plus de chemin pour l'éviter.

Et le compte ne se rattrape pas : **ajouté après coup, il est perdu**, on ne
reconstitue pas a posteriori le nombre de choses qu'on a essayées. Tout
l'appareil statistique s'effondrerait rétroactivement. D'où la construction
**avant le premier signal**.

## Ce qui est acquis

- L'intention du schéma : `registry/SCHEMA.md`, onze champs, une ligne par IC.
- Les règles de comptage, arrêtées en phase 01 (`D01` §4) —
  [[concepts/comptage-des-tests]].
- Les bornes du `holdout` et son **typage écrit d'avance** (`D01` §5) —
  [[concepts/tranche]].

## Ce qui manque

- Les types exacts, les valeurs permises et la validation, à fixer **en même temps
  que la fonction d'écriture** (`registry/SCHEMA.md`, dernier § du schéma).
- Le mécanisme d'inaccessibilité du `holdout`. À décider : refus au chargement du
  Panel, ou absence physique de la tranche dans l'objet remis au harnais. La
  seconde est plus forte.
- Le `code_hash` : sur quoi exactement porte l'empreinte (signal + harnais), et
  comment elle est calculée.

## Pièges connus

- **Le fichier ne se modifie qu'en ajoutant.** Aucune suppression, réécriture,
  tri, ni reformatage en masse. Une ligne écrite par erreur **reste** ; on ajoute
  une ligne qui la corrige.
- **Perdre le registre coûte la validité statistique de tout ce qui précède**, pas
  du temps (`CLAUDE.md` § Conventions, Git).
- Le holdout n'est pas « protégé par convention ». S'il est rouvert, il n'est plus
  un holdout — invariant V, sans exception.

## Voir aussi

[[phases/phase-03-harnais-ic]] · [[concepts/registre]] · [[concepts/tranche]] ·
[[concepts/comptage-des-tests]]
