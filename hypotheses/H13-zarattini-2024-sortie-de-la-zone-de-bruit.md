# H13 — Sortir de la zone de bruit prédit la fin de la séance

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `zarattini-2024-beat-the-market-spy` (`corpus/fiches/zarattini-2024-beat-the-market-spy.json`)
**signal :** `zarattini-2024-beat-the-market-spy` — *non encore codé*
**signe attendu :** +1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D33`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches. Aucun IC ne porte sur ce signal au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

L'**écart du prix à sa zone de bruit** — la bande construite, heure par heure, à
partir du mouvement absolu moyen depuis l'ouverture de la fenêtre sur les
**quatorze** séances précédentes — prédit **positivement** le rendement de la
fenêtre courante jusqu'à sa clôture forcée, sur le même instrument.

Le signe est **positif** : au-dessus de la bande haute, le mouvement continue ; en
dessous de la bande basse, il continue à la baisse.

**Ce qui distingue cette hypothèse des cinq autres du lot qui portent sur le
momentum intraday.** Toutes les autres prennent pour score un **rendement passé
brut**. Celle-ci prend un **rendement normalisé par sa propre dispersion
récente** : le même mouvement de 0,3 % est un signal fort sur un instrument calme
et un bruit sur un instrument agité. C'est la seule du lot dont le score soit
**sans dimension**, donc la seule dont on puisse attendre qu'elle se comporte de
la même façon sur les neuf contrats — et c'est précisément l'argument que le
papier donne pour préférer une bande à un seuil absolu.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** de la barre scorée à la **clôture forcée de la fenêtre**, donc
  variable, et entièrement intra-fenêtre — ce que `harness/metric.py` est seul à
  savoir mesurer.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Une observation par séance et par cellule**, à la grille de décision
  semi-horaire du papier.
- **Données :** OHLCV à la minute, et rien d'autre : la zone de bruit ne demande
  que l'ouverture de la fenêtre courante, les clôtures des quatorze fenêtres
  précédentes et le VWAP cumulé depuis l'ouverture. La fiche le dit —
  *« aucune donnée externe, aucun réseau »*.
- **Le VWAP cumulé** est calculable ici : nos barres portent un volume. C'est le
  seul endroit de ces dix hypothèses où le volume entre dans le score.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **positif** |
| Magnitude plausible | **0 à 0,04** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 |

**Ce que la fiche interdit d'espérer, et il faut l'écrire.** Le Sharpe de 1,33 du
papier vient, *de son propre aveu rapporté par la fiche*, **du stop suiveur et du
dimensionnement plutôt que du signal lui-même**. Notre harnais ne mesure **que le
signal** : pas de stop, pas de dimensionnement, pas de plafond de levier. L'IC que
nous mesurerons porte donc sur la **partie du papier qui n'explique pas son
résultat**, et c'est une raison sérieuse d'attendre peu.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `sharpe_final_model` | 1.33 |
| `unconditional_daily_pnl_tstat` | 5.34 |
| `futures_markets_tested` | 33 |
| `futures_average_sharpe` | 0.6 |
| `sp500_future_sharpe` | 1.32 |
| `optimal_volatility_multiplier` | 1.5 |

**La ligne à lire est la quatrième.** Appliqué à **33 marchés de futures** — donc à
des instruments de notre nature, pas à un ETF d'actions — le Sharpe moyen tombe à
**0,6**, contre **1,32** sur le seul future S&P 500 et **1,33** sur SPY. Le motif
survit à la transposition aux futures, mais **divisé par deux**, et c'est le
chiffre le plus prédictif du lot pour nous.

Deux manques que la fiche nomme et qui pèsent autant : **aucune séparation hors
échantillon** — tout est calculé sur 2007-2024, y compris les sensibilités au
lookback et au multiplicateur — et **aucun compte des configurations testées**
(8 lookbacks, une grille de multiplicateurs, 8 motifs quotidiens, 5 jours de la
semaine, plusieurs seuils de VIX, 3 moyennes mobiles, 33 futures) sans aucune
correction de tests multiples. Le `t` de 5,34 n'est donc pas comparable au `t` que
`BH` nous demandera.

## Ce qui la contredirait

- Un IC poolé **négatif** avec un `t` final au-delà de **2** : sortir de la bande
  annonce le retour, pas la continuation. Ce serait un résultat intéressant et
  l'hypothèse serait fausse telle qu'écrite.
- Un `t` final sous **2** : rien à distinguer du bruit. Au vu du **0,6** de Sharpe
  moyen sur 33 futures et du fait que le gain du papier vient de la gestion de
  position, c'est l'issue la plus probable.
- Un IC positif porté par **une ou deux cellules sur 25** : accident
  d'instrument. La suspicion doit porter sur `ES` en fenêtre US, le seul couple
  proche de l'objet du papier.
- Un IC net négatif au coût **borne haute** de `D26`. Le modèle de coût du papier
  — 0,0035 $ de commission et 0,001 $ de glissement **par action** — n'a aucun
  sens sur un contrat à terme, et la fiche le dit : le passage exige le
  multiplicateur et le tick, donc `D26`.

## Ce qui n'est pas affirmé ici

Rien de la **chaîne d'exécution** n'est affirmé : ni le stop suiveur sur la bande
courante ou le VWAP, ni le dimensionnement à 2 % de volatilité quotidienne, ni le
plafond de levier de 4×. Ce sont des règles de stratégie, et elles appartiennent à
la phase 10 — pas à un score.

Les **régimes** du papier ne sont pas affirmés non plus : le Sharpe de 3,5 quand
le VIX dépasse 40, la pente de −3,25 bp par point de RSI, les motifs quotidiens
(NR4 à 22 bp/jour, triangle à 14, jour de tendance à −2) et le mercredi à
18 bp/jour. Huit motifs, cinq jours de semaine et plusieurs seuils de VIX
constituent, ensemble, exactement le genre de recherche que `D25` compte et que
le papier ne compte pas. Chacun devra être pré-enregistré à part, en phase 13.
