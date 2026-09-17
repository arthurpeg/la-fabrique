---
type: phase
updated: 2026-09-17
status: franchie
phase: 05
gate: un signal qui tente de lire le futur échoue au test de causalité, automatiquement
sources: [ETAT.md, decisions/DECISION-07-contrat-de-signal.md, sandbox/, LECONS.md]
---

# Phase 05 — API de signal, sandbox, test de causalité

**Franchie le 2026-09-17**, `scripts/gate_05_signal_api.py`, 29 vérifications.
Première phase de l'Acte II.

## La porte

Un signal qui tente de lire le futur **échoue au test de causalité,
automatiquement**. Un test qui n'a jamais rien attrapé n'est pas un test : la
porte n'est franchie que parce que trois look-ahead injectés exprès
(`sandbox/tainted.py`) tombent, **chacun pour la raison écrite d'avance**.

## Ce qui a été construit

`sandbox/`, et le harnais n'y est pas importé — rien ici ne calcule d'IC.

| Module | Ce qu'il fait |
|---|---|
| `contract.py` | ce qu'un signal doit exposer, et à quoi sa sortie doit ressembler |
| `scan.py` | la **liste blanche** d'importations et d'appels |
| `causality.py` | **le test** |
| `signature.py` | l'empreinte propre du signal, que `D05` avait laissée ouverte |
| `tainted.py` | trois signaux qui trichent, pour que le test ait quelque chose à attraper |

## Le test, en une phrase

Prendre une barre que le signal a scorée à l'instant `t`, tronquer le panel **une
minute après `t`**, et redemander. Un signal honnête rend le score identique :
tout ce qu'il a utilisé était à `t` ou avant. Un tricheur rend autre chose, ou ne
rend rien.

Deux détails font tout, et sont dans `D07` :

- **les sondes sont posées sur les barres scorées**, pas au hasard. Au milieu du
  panel, le futur qu'un tricheur lit est disponible des deux côtés et la fraude
  est invisible. Le bord discrimine, donc il faut le mettre là où le signal
  travaille ;
- **l'index est comparé, pas seulement les valeurs.** Un signal qui lit
  `close[t+30]` ne rend pas un nombre faux sans son futur — il ne rend **rien**.
  Comparer les seules valeurs partagées le laisserait passer.

## Ce que la porte a coûté, et trouvé

Elle a échoué deux fois avant de passer, et les deux échecs valaient le détour.

**Le premier** : `tainted-forward-return`, le tricheur le plus grossier, n'était
pas attrapé — parce qu'il ne produisait **aucun score**, même sur le panel
complet. En remontant : l'ancre des étalons tombait exactement trente barres
avant la clôture, donc le rendement à trente barres sortait de la fenêtre.

**Le second, et c'est lui qui compte** : la même cause faisait que `NQ × US`, la
cellule la **plus dense** de la grille, produisait 615 scores et **zéro
observation mesurable**. Le coupable était une comparaison d'horloge en
flottants — 15:29 face à une clôture à 16:00 rend `31,000000000000004`, donc
`<= 31` est faux. Voir [[lessons|L10]]. En minutes entières : 88,6 % des scores
deviennent des observations.

Le contrôle qui a trouvé ça n'existait pas avant, et il existe maintenant :
*combien des scores produits tombent sur une barre que le harnais sait mesurer*.
Il n'y a pas de meilleur résumé de la phase — un signal se juge sur ses
observations, pas sur ses scores.

## Ce que ça ne prétend pas

La preuve est **empirique** : le signal était causal **sur les instants sondés**,
seize par signal, répartis sur les cellules et sur le temps. Un tricheur qui ne
tricherait qu'un jour sur mille passerait. `scan.py` tient le second rideau, et
[[Failed Ideas/ledger#F20]] dit pourquoi il ne peut pas tenir le premier.

## Voir aussi

[[phases/phase-04-registre-et-holdout]] · [[signaux/README]] ·
[[concepts/point-in-time]] · [[Failed Ideas/ledger#F19]] ·
[[Failed Ideas/ledger#F21]]
