# D27 — On tronque le panel à la barre scorée, pas une minute après

**Date :** 2026-09-26
**Phase :** 09
**État :** prise — révise `D07` § Pourquoi sur un point : l'instant de troncature

## La question

`D07` fait tronquer le panel « sur les barres scorées elles-mêmes, une minute
après ». Or une barre est horodatée à son **ouverture** : le panel tronqué à
`t + 1 min` contient encore la barre `t+1`. Un signal qui lit une barre de trop
passe-t-il le test de causalité ?

## Le fait, mesuré

**L'horodatage.** Les fichiers portent `ts_event` (Databento, `ohlcv-1m`), qui
désigne le **début** de la minute agrégée. Vérifié sur `CL`, le 2026-06-15,
autour de l'arrêt quotidien du CME (17:00–18:00 à New York) : dernière barre
**16:59**, première barre **18:00**. Horodatées à la clôture, elles auraient été
17:00 et 18:01. La barre `ts_event = t` n'est donc complète qu'à `t + 1 min`.

**Le trou.** `Panel.truncate(end=e)` garde toute barre `ts_event <= e`.
Tronquer à `t + 1 min` garde la barre `t+1`, dont la clôture n'est connue qu'à
`t + 2 min`. Un signal qui lit `close[t+1]` pour scorer `t` rend donc le **même**
score sur les deux panels.

**La démonstration.** Un tricheur qui lit la clôture de la barre suivante,
soumis au test de la porte 05 (même `ASOF`, 16 sondes) : **2 divergences sur
16 sondes**. Les deux sont sur `6A × US` et `6B × US`, là où la barre `t+1`
**manquait** dans les données — le tricheur n'est attrapé que par accident, par
un trou de cotation. Sur une cellule dense (`NQ × US`, `ES × US`), il passerait
la porte 05 et la condition `S3` de `D23`.

**Pourquoi c'est grave et pas cosmétique.** Sur un horizon de 30 barres, la
minute lue d'avance est un trentième du rendement à prédire : sa corrélation avec
lui est de l'ordre de √(1/30) ≈ **0,18**, quand la cible économique de `D01` est
un IC de **0,018 à 0,031**. Un décalage d'une barre dans un signal écrit par un
codeur automatique ne produirait pas un signal un peu optimiste : il produirait
une découverte, et `BH` la retiendrait.

## Les options

1. **Tronquer à `t`.** Retenue. Le panel tronqué contient la barre scorée `t`
   (`ts_event <= t`) et rien de ce qui la suit. Un signal honnête, qui lit au plus
   `closes.iloc[:position + 1]` (contrat de `signals/_common.py`), rend
   l'identique ; un signal qui lit une barre de plus perd son score (`disparu`).
2. **Changer la convention du Panel** — décaler `ts_event` d'une minute pour
   horodater à la clôture. Écartée : elle touche la couche de données de la
   porte 02, les fenêtres de séance, le recollement à `splice_minute_utc` et le
   harnais qui lit le même Panel. Beaucoup de surface pour fermer un trou qui
   se ferme en une ligne là où il est.
3. **Rendre le test plus dense** — plus de sondes, en espérant tomber sur des
   trous de cotation. Écartée : c'est exactement la détection par accident que
   la mesure ci-dessus a montrée. Invariant II : par construction, pas par
   chance.

## Le choix

`sandbox/causality.py` tronque à `instant`, la barre scorée elle-même. La porte
05 reçoit un **quatrième tricheur** (`tainted-next-bar`, une barre de futur) et
l'exige attrapé à **chaque** sonde, pas seulement à une.

## Pourquoi

Le test de `D07` était juste dans son principe et faux d'une barre dans son
réglage. L'écart ne se voyait pas parce que les trois tricheurs de la porte 05
lisaient tous **loin** dans le futur (30 barres, la clôture de fenêtre, toute la
cellule) : un test calibré uniquement sur des fraudes grossières ne dit rien de
sa résolution. Le quatrième tricheur est là pour que la résolution soit
**mesurée** à chaque passage de la porte, et l'exigence « à chaque sonde » pour
qu'un trou de cotation ne puisse plus faire le travail à sa place.

**Ce qui est sacrifié.** Rien de mesuré : aucun IC n'a été calculé sur un signal
qui ne serait causal qu'à une minute près. Les deux étalons et le signal produit
de la porte 08 ont été rejugés sous la nouvelle troncature.

## Ce que ça verrouille

- `sandbox/causality.py` — **hors de `harness/`** : l'empreinte du harnais
  (`registry.code_hash()`) ne change pas, et **aucune ligne du registre n'est
  périmée**.
- La porte 05 et la condition `S3` de `D23` (porte 08) utilisent ce test : elles
  sont rejouées sous cette décision (§ Journal).
- `D07` § Pourquoi (« une minute après ») se lit désormais « à la barre scorée ».
  `D07` n'est pas réécrite.
- Le contrat de `signals/_common.py` — un prédicteur lit au plus
  `closes.iloc[:position + 1]` — devient **vérifié** à la barre près, et plus
  seulement déclaré.

## Ce qui reste ouvert

- **La sémantique du Panel pour les signaux à horaire d'événement.** Un Panel
  ouvert « à `t` » contient la barre qui s'ouvre à `t` et se ferme à `t + 1 min`.
  Pour un signal qui se cale sur l'heure d'une annonce (FOMC à 14:00, chiffres
  macro à 8:30), la barre de 14:00 **contient déjà** la réaction. Cohérent pour le
  harnais (score et rendement partent tous deux de la clôture de la barre
  scorée), mais un codeur qui écrirait « avant l'annonce » en scorant la barre de
  14:00 se tromperait. À écrire dans la consigne du codeur avant le premier
  signal à horaire d'événement de la phase 09.

## Journal

- **2026-09-26** — décision prise et appliquée le même jour. Rejoué : porte 05,
  porte 08, `scripts/check_signals.py`. Résultats dans `ETAT.md`.
