---
type: concept
updated: 2026-09-16
status: stable
sources: [CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md, registry/SCHEMA.md]
---

# IC — coefficient d'information

**La corrélation entre le score d'un signal et le rendement futur. Ici : en série
temporelle, poolée, et produite par le seul harnais.**

## Ce que ça veut dire ici

**IC en série temporelle, poolé entre instruments et entre cellules** — jamais
transversal. Assorti de :

- une statistique de test **robuste à la corrélation contemporaine** entre
  instruments : les résidus sont corrélés en coupe, un t de Student naïf serait
  surévalué d'un facteur proche de `sqrt(9 / 4,2) ≈ 1,46` ;
- le *pooling* justifié par [[research/bollerslev-2018-risk-everywhere]] ;
- un seuil de **FDR appliqué dès le premier test**, jamais un t-stat à 2 ;
  calibrage : [[research/harvey-2016-cross-section]], `t > 3,0`.

**La cible.** IC requis pour un IR de 1 : **0,018** si les trois fenêtres sont
indépendantes (~3 100 paris/an), **0,031** sinon (~1 060). Le rapport d'IC doit
afficher **les deux bornes, jamais la plus flatteuse seule**.

## Ce que ça ne veut pas dire

- **L'IC transversal n'a aucun sens ici.** On ne classe pas neuf actifs en
  déciles quand ils portent ~4 paris ([[Failed Ideas/ledger]] F03).
- **Un IC par cellule n'est pas un IC.** C'est un diagnostic. Un signal sur la
  grille = un IC, un test ([[concepts/comptage-des-tests]]).
- **Un IC moyen ne dit rien de la queue.** La largeur réalisée tombe sous 3 paris
  dans 17 % des séances ([[concepts/largeur-effective]]).
- **Un IC brut n'est pas un IC net.** Le modèle de coût est de première classe dès
  la phase 03 ([[concepts/cout-aller-retour]]).

## La règle dure

> **Il ne doit exister aucun chemin de code qui produise un IC sans écrire au
> registre.** Pas de corrélation calculée à la main dans un notebook, pas de
> « juste pour voir ». — `CLAUDE.md` § Les interdits, invariant III

Le **rapport d'IC** est la sortie officielle du harnais et la **seule source d'IC
du projet**. Le wiki n'en est jamais une : voir `wiki/SCHEMA.md` § 0.

## État actuel

`registry/tests.jsonl` : **0 ligne**. Le harnais n'existe pas encore — il se
construit en [[phases/phase-03-harnais-ic]].

## Où c'est fixé

`CLAUDE.md` invariant III · `D01` §2 · `registry/SCHEMA.md`

## Voir aussi

[[concepts/registre]] · [[concepts/largeur-effective]] ·
[[concepts/comptage-des-tests]] · [[reference/metrique-et-comptage]]
