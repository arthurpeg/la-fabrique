---
type: phase
updated: 2026-09-23
status: juge-ecrit-accuse-absent
phase: 08
gate: une fiche produit un signal executable qui passe la sandbox, sans retouche manuelle
sources: [ETAT.md, decisions/DECISION-23-seuil-du-codeur-de-signal.md, scripts/score_signal.py]
---

# Phase 08 — Le codeur de signal

**Pas encore ouverte** : la porte 07 la précède. Mais **son juge est déjà écrit**,
comme [[phase-07-triage-et-extraction|`D15` l'a été avant le trieur et `D16`
avant l'extracteur]]. C'est l'ordre de construction de `CLAUDE.md` — le juge
avant l'accusé.

## La porte

> Une fiche produit un signal exécutable qui passe la sandbox, sans retouche
> manuelle.

Six conditions à tolérance zéro, qui valent **ensemble**. Elles sont dans
`decisions/DECISION-23-seuil-du-codeur-de-signal.md`, et `scripts/score_signal.py`
les vérifie — **25 vérifications**, une faute fabriquée par condition.

| | Condition |
|---|---|
| `S1` | le contrat de `D07` |
| `S2` | rien hors de la liste blanche d'imports |
| `S3` | **causalité** — score identique sur panel tronqué et panel entier |
| `S4` | non-dégénérescence, scores sur des barres **mesurables** |
| `S5` | **toute constante du code se retrouve dans la fiche** |
| `S6` | **zéro retouche manuelle** depuis la production |

**Aucun IC n'est calculé pour franchir cette porte**, et c'est la règle qui
compte : le nombre de tests est la seule chose que la phase 15 ne peut pas
recalculer. Voir [[phase-04-registre-et-holdout]].

## `S5` : ce qu'elle vaut, mesuré

`S5` est `F2` transposé au code — un paramètre absent de la fiche est un
paramètre **inventé**, ce que l'interdit constitutionnel vise.

**Elle est nécessaire, pas suffisante, et le chiffre est là :** 3 signaux × 10
fiches, elle **refuse 12 appariements sur 30, soit 40 %**. Le signal Heston passe
`S5` contre la fiche Lou (2019), qui n'a rien à voir.

La raison n'est pas réparable : deux papiers d'un même domaine **partagent leurs
paramètres**. `30` minutes est la demi-heure de Gao, le décalage de Heston et la
fenêtre de Patton & Sheppard à la fois. Pousser `S5` plus loin en ferait une
vérification de **pertinence**, qui par `D23` n'a pas de juge automatique et
attend la phase 09.

## Ce qui a été calibré, et pourquoi pas autrement

Deux fois `S5` s'est révélée vide, et deux fois la cause était ailleurs que dans
la liste close — c'est `L18` appliqué. Le détail chiffré est au § Journal des
calibrations de `D23` : exemption de `_common.py` plutôt qu'un `24` de plus dans
`DU_DEPOT` ; recherche bornée à quatre champs de recette et **`30` retiré** des
valeurs du dépôt, parce qu'il est à la fois l'horizon de grille et le seul
paramètre du signal de référence.

## Ce qui manque

- **`code_signal.py`** — l'accusé. Il n'existe pas.
- **`G1` et `G2` de la porte 07** le précèdent : 8 papiers restent à ficher,
  3 fiches cassent `D16`. Un codeur sans fiches n'a rien à coder.
- **La calibration sur Baltussen** — impossible tant que l'entrée 2 n'est pas
  fichée. Les deux étalons de `D06` n'ont pas de fiche, et l'entrée 1 est
  inatteignable ([[lessons|`L20`]]).

## Voir aussi

- [[phase-07-triage-et-extraction]] — elle doit se fermer d'abord
- [[index]] · [[hot]] · [[lessons]]
