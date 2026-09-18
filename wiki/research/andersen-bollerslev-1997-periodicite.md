---
type: research
updated: 2026-09-18
status: lu
ref: Andersen & Bollerslev (1997)
amorce_entry: 11
fiche: corpus/fiches/andersen-bollerslev-1997-periodicity.json
implementable: oui
sources: [corpus/AMORCE.md, decisions/DECISION-13-ce-que-la-clause-2-peut-etre.md, hypotheses/H04-andersen-bollerslev-1997-periodicite.md]
---

# Andersen & Bollerslev (1997) — Périodicité intra-journalière et persistance de la volatilité

*Intraday periodicity and volatility persistence in financial markets*,
*J. Empirical Finance* 4(2-3):115-158. **Lu et fiché le 2026-09-18.** C'est la
cible qui a franchi la clause 2 de la porte 06.

## Ce que le papier affirme

La volatilité varie systématiquement au cours de la séance, selon un motif si
fort qu'il **domine la dynamique des rendements haute fréquence** : toute
dynamique intraday estimée sans l'en purger est faussée.

Deux faits chiffrés ont servi, et un seul est transposable comme valeur :

- **La forme en U**, sur les futures S&P 500, 1986-1989, barres de cinq minutes :
  `|r|` moyen de **0,095 %** le matin, **0,055 %** vers midi, **0,105 %** en fin
  de séance. Soit un **rapport sommet/creux de 1,91**.
- **Le corrélogramme déformé** : l'autocorrélation de `|r|` dessine un U lent qui
  occupe « exactement 80 intervalles, correspondant à la fréquence journalière ».

L'ordre de grandeur de l'effet, sur le change : `Q(10) = 36 680`. Ce n'est pas un
signal marginal, c'est la structure dominante des données.

## Pourquoi c'est la bonne cible pour la porte 06

Deux cibles étaient tombées. Mesfin sur sa **métrique** — un `t` sur des
rendements nets par trade, quand nous mesurons un IC. Heston sur son **résultat**
— le peigne n'est pas dans nos données.

Celle-ci mesure une propriété des **données**, pas un pouvoir prédictif. Trois
conséquences :

1. elle ne produit **aucun IC**, donc elle n'a coûté **aucun test compté** ;
2. son échec serait à peine concevable — ce qu'on demande à une épreuve
   d'instrument, comme on vérifie une balance avec un poids étalon et non avec un
   objet inconnu ;
3. sa figure porte sur les **futures S&P 500 pendant la séance américaine**,
   c'est-à-dire notre cellule `ES × US`. Même contrat, même fenêtre.

Voir `D13`, écrite **avant** la mesure.

## Ce que nos données rendent

Mesuré par `scripts/measure_h04.py`, tranche `pool`, ~790 000 barres par
instrument. Recopié de `scripts/out/h04_periodicity.json`.

| | rapport sommet/creux |
|---|---|
| `NQ × US` | **2,05** |
| `ES × US` | **1,74** |
| `YM × US` | **1,89** |
| *Andersen & Bollerslev, S&P 500, 1986-1989* | *1,91* |

Creux au milieu de séance sur les trois, sommets aux deux extrémités, rapports
tous dans la fourchette `[1,4 ; 3,0]` écrite avant de mesurer.

## Ce que ça valide, et ce que ça ne valide pas

**Validé :** la chaîne de données et la discipline de mesure — définition des
séances, horloge de la place, ajustement des roulements, filtrage des barres.

**Non validé :** le harnais d'IC, qui reste garanti par sa seule calibration à la
main (porte 03). `D13` § Pourquoi le dit sans détour, et
[[phases/phase-06-controles-et-replication]] le répète en tête.

## Ce qui reste à en tirer

Le **modèle périodique explicite** de leur section 5 — la procédure qui *purge*
la périodicité — n'a pas été testé. Il servira en phase 09 si la normalisation
des scores en a besoin : leur thèse centrale est justement qu'une dynamique
intraday estimée sans purge est fausse.

## Voir aussi

[[phases/phase-06-controles-et-replication]] · [[phases/phase-07-triage-et-extraction]] ·
[[research/bollerslev-2018-risk-everywhere]] · [[lessons|L16]]
