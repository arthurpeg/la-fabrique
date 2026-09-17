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

| # | Signal | Statut | Testée le |
|---|---|---|---|
| [H01](H01-gao-2018-premiere-demi-heure.md) | `gao-2018-intraday-momentum` | **pré-enregistrée, non testée** | — |
| [H02](H02-baltussen-2021-reste-de-la-journee.md) | `baltussen-2021-intraday-momentum` | **pré-enregistrée, non testée** | — |
