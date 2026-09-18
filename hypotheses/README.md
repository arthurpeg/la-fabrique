# Les hypothèses pré-enregistrées

Un fichier par hypothèse, numéroté `H01`, `H02`, … **écrit et daté avant** que le
moindre résultat soit vu (invariant IV). Le champ `hypothesis_ref` de
`registry/tests.jsonl` porte ce numéro ; une ligne du registre dont
`hypothesis_ref` est `null` est une calibration, hors dénominateur (`D04` §4).

## Les règles

- **Écrite avant.** Une hypothèse rédigée, complétée ou précisée après avoir vu
  un chiffre n'est plus une hypothèse. Elle est morte, et le test qu'elle
  accompagnait compte quand même.
- **Falsifiable avant d'être testée.** Chaque fichier dit ce qui la
  *contredirait*, en chiffres, avant de savoir. Une hypothèse qu'aucun résultat
  ne peut contredire ne mérite pas un test.
- **Le signe d'abord.** Sur neuf futures portant 4,22 paris indépendants, se
  tromper de signe est l'erreur qui coûte le plus. Le signe attendu est écrit
  avant la magnitude.
- **Jamais réécrite.** Une hypothèse qui se révèle mal posée donne lieu à une
  **nouvelle** hypothèse qui cite la précédente, comme dans `LECONS.md`.
- **Une hypothèse n'est pas un signal.** Le signal est une implémentation dans
  `signals/` ; l'hypothèse est ce qu'on affirme de lui avant de regarder. Un même
  signal peut porter plusieurs hypothèses, à des horizons différents.

## Les cibles, fixées en phase 01

`D01` §2, et les deux valent ensemble, jamais l'une seule :

| Régime de fenêtres | Paris par an | IC requis pour un IR de 1 |
|---|---|---|
| indépendantes | ~3 100 | **0,018** |
| dépendantes | ~1 060 | **0,031** |

Une hypothèse qui prédit un IC très au-dessus de ces cibles doit dire pourquoi
elle croit battre la littérature, et pas seulement l'espérer. Un IC au-dessus de
**0,10** déclenchera un rapport de suspicion automatique en phase 06.

## L'état

| # | Signal | Statut | Testée le | Résultat |
|---|---|---|---|---|
| [H01](H01-gao-2018-premiere-demi-heure.md) | `gao-2018-intraday-momentum` | **testée** | 2026-09-18 | IC −0,01061, `t` final **−1,56** — non confirmée, dans le bruit (`T-20260918T065822-2b3e5d`) |
| [H02](H02-baltussen-2021-reste-de-la-journee.md) | `baltussen-2021-intraday-momentum` | **testée** | 2026-09-18 | IC −0,00432, `t` final **−0,63** — non confirmée, dans le bruit (`T-20260918T070041-18cf25`) |

**`counted_tests()` vaut 4 pour DEUX hypothèses.** Chacune porte deux lignes : la
première mesure et sa reprise sous `D11`, qui a corrigé la déflation de
recouvrement. La correction de tests multiples de la phase 15 compte des
**hypothèses éprouvées, pas des lignes écrites** — une reprise après changement
du harnais n'est pas une recherche supplémentaire (`D11` § Ce que ça verrouille).
Et `H01` et `H02` portant sur la même cible, elles ne valent de toute façon
**jamais deux tests indépendants**.
