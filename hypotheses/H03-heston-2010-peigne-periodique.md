# H03 — Le peigne : continuation aux multiples exacts d'une séance

**Écrite le :** 2026-09-18, **avant toute mesure sur nos données**
**Signal :** `heston-2010-periodicity` — à implémenter, `signals/` ne le porte pas
encore
**Origine :** Heston, Korajczyk & Sadka (2010), « Intraday Patterns in the
Cross-section of Stock Returns », *JF* 65(4):1369-1407 — `corpus/AMORCE.md`
entrée 3, fiche `corpus/fiches/heston-2010-intraday-periodicity.json`
**Rôle :** cible de la **clause 2 de la porte 06** (`D12`)
**Statut :** pré-enregistrée, **non testée**

## Ce qui est affirmé

Sur une cellule donnée, le rendement d'un intervalle de demi-heure est
**positivement** lié à son propre rendement **`m` séances plus tôt, au même
intervalle de la fenêtre** — et il ne l'est **pas** aux décalages qui ne tombent
pas sur un multiple de séance.

C'est un **motif de signes**, et c'est ce motif qui est affirmé, en trois clauses
qui valent ensemble :

| | Clause | Prédiction |
|---|---|---|
| **A — les dents** | IC aux décalages de `m` séances, même intervalle, `m = 1…40` | **positif** |
| **B — les creux** | IC aux décalages de `j` intervalles à l'intérieur d'une séance, `j = 1…P−1` | **négatif ou nul**, et dans tous les cas **inférieur** aux dents |
| **C — le retournement court** | IC aux décalages `j = 1, 2, 3` | **négatif** |

`P` est le nombre de demi-heures de la fenêtre, **dicté par le catalogue et non
par le résultat** : `US` 09:30→16:00 et `EUROPE` 03:00→09:30 font 6,5 h, donc
**P = 13** ; `ASIA` 19:00→03:00 fait 8 h, donc **P = 16**. Le peigne a donc
**deux périodes différentes** selon la fenêtre, et c'est une contrainte, pas une
liberté : un ajustement de `P` après coup se verrait immédiatement.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), regroupées par période —
  `P = 13` (US et EUROPE) et `P = 16` (ASIA), mesurées séparément pour que le
  *pooling* ne mélange pas une dent et un creux.
- **Grandeur :** rendement de demi-heure, à l'intérieur de la fenêtre et de la
  séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Décalages mesurés :** `m = 1…40` séances (clause A) et `j = 1…P−1`
  intervalles (clauses B et C).

## Ce qui est attendu, en chiffres

**Aucune magnitude n'est prédite, et c'est délibéré.** Le papier mesure une
réponse **transversale** en points de base, dont l'effet de marché est retiré ; il
écrit lui-même que « using cross-sectional regression in this way is different
from measuring the autocorrelation of stock returns ». Nous mesurons une
corrélation de rang **en série temporelle par cellule**, sur neuf futures et non
sur des milliers d'actions. Reprendre son `t` minimal de 9,62 comme attente
serait une faute de transposition.

Ce qui est prédit est donc l'**ordre**, pas la valeur :

```
IC(dents)  >  IC(creux)        et      IC(dents) > 0      et      IC(j=1,2,3) < 0
```

## Ce qui la contredirait

- **Pas de séparation.** `IC(dents) ≤ IC(creux)` : il n'y a pas de périodicité, et
  la clause A ne dit rien de plus que la clause B.
- **Des dents négatives.** `IC(dents) < 0` avec un `t` final au-delà de 2 : le
  motif existe à l'envers.
- **Un peigne à la mauvaise période.** Un motif présent mais dont les pics ne
  tombent pas sur `P` : ce ne serait pas le résultat de Heston et al., ce serait
  autre chose — à ne pas rebaptiser.
- **Un peigne porté par une seule cellule** sur les 25 : accident d'instrument,
  pas périodicité (même clause que `H01`, et voir
  `wiki/concepts/comptage-des-tests` sur le coût de la sélection).
- **Aucun retournement court** : la clause C tombe et, avec elle, la moitié du
  motif que le papier décrit.

## Si le motif n'est pas là — écrit avant de regarder

`D12` § Ce qui reste ouvert l'exige, et la réponse est écrite ici pour qu'elle ne
soit pas arrangée après coup.

L'absence du peigne sur nos futures serait **un résultat valide sur notre
univers** — et une information utile, puisque le motif est réputé robuste. Mais
**la clause 2 ne serait pas franchie pour autant** : elle demande que le harnais
retrouve un résultat publié connu, et un instrument qui ne retrouve pas ce qu'il
devrait retrouver n'est pas validé contre une vérité extérieure. Il faudrait
alors une **nouvelle cible**, par décision écrite — pas un assouplissement de
celle-ci.

Dit autrement : cette hypothèse peut échouer **sans que personne ait mal
travaillé**, et son échec ne s'achète pas en redéfinissant la porte.

## Comptage

**`H03` est UNE hypothèse**, quelle que soit le nombre de lignes qu'elle écrit au
registre — environ une centaine, une par décalage mesuré et par groupe de
période. Ce n'est pas une recherche du meilleur décalage : c'est la vérification
d'un motif **prédit en entier avant d'être vu**. `D11` § Ce que ça verrouille et
`D12` § Ce que ça verrouille posent la règle que la phase 15 devra suivre :
**on compte des hypothèses éprouvées, pas des lignes écrites**.

**Garde-fou, écrit d'avance.** Aucun décalage ne peut être retenu comme signal
sur la foi de cette mesure, même s'il ressort nettement. Le retenir exigerait une
hypothèse neuve, pré-enregistrée, et comptée en plus.

## Ce qui n'est pas affirmé ici

Le papier propose aussi des variations **conditionnelles** — heure de la journée,
taille, volume, écart. Elles appartiennent aux régimes (phase 13) et devront être
pré-enregistrées séparément. Les tester en même temps que celle-ci et retenir la
meilleure serait exactement ce que le registre existe pour rendre visible.
