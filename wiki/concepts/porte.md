---
type: concept
updated: 2026-09-16
status: stable
sources: [CLAUDE.md, ETAT.md]
---

# Porte

**La condition explicite de passage d'une phase à la suivante. Binaire.**

## Ce que ça veut dire ici

Chaque phase de l'ordre de construction (01 → 15, `ETAT.md`) a une porte écrite
d'avance. Elle est **vraie ou fausse**, pas « à peu près franchie ».

> **Ne jamais franchir une porte « provisoirement, on y reviendra ».**
> Une porte à moitié franchie est une porte non franchie.
> — `CLAUDE.md` § Les interdits

## Ce que ça ne veut pas dire

- **Ce n'est pas une étape de la chaîne.** Les *phases* (ordre de construction)
  vont à l'inverse des *étapes* (ordre d'exécution 00 → 10). L'étape 04 de
  l'exécution — le rapport d'IC — se construit en **phase 03**, bien avant
  l'étape 02, le codage du signal, qui se construit en **phase 08**. Confondre
  les deux est l'erreur la plus fréquente d'une session froide. Voir
  [[concepts/les-deux-ordres]].
- **Une porte bloquée par un intrant externe reste fermée.** La phase 02 attend
  les dates de roulement de l'auteur des données. On peut préparer, on ne franchit
  pas.

## L'ordre de construction, en une ligne

**Le juge avant l'accusé.** On n'automatise jamais la production de quelque chose
qu'on ne sait pas encore juger. D'où l'interdit : *ne jamais écrire de code de
stratégie ou de backtest avant que le harnais d'IC existe et soit calibré* —
porte 03.

## Où c'est fixé

`ETAT.md` (le tableau des 15 phases, qui fait foi) · `CLAUDE.md` § Les deux ordres

## Voir aussi

[[concepts/les-deux-ordres]] · [[phases/phase-02-panel-pit]] ·
[[phases/phase-03-harnais-ic]] · [[hot]]
