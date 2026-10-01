# D42 — Une hypothèse pour chaque fiche, à son propre horizon intraday

**Date :** 2026-10-01
**Phase :** 09
**État :** prise — choix de l'opérateur ; complète `D40` et `D41`

## La question

`hypotheses/NON-ECRITES-09.md` laissait 31 fiches du lot sans hypothèse
(aucune prédiction de rendement, horizon hors fenêtre, donnée manquante), et la
chaîne mesurait toutes les hypothèses à 30 minutes. L'opérateur, le
2026-10-01 : on n'écarte pas ces fiches ; l'IA écrit pour chacune une
hypothèse — monte ou baisse, à quel horizon — et le harnais en mesure l'IC ;
et l'horizon n'est pas « 30 minutes », il est **intraday**.

## Le choix

1. **Aucune fiche ne s'écarte pour un écran de contenu.** Chaque fiche du lot
   reçoit son hypothèse au format de `D40`, écrite par l'IA avant toute mesure.
   Pour un papier qui ne prédit pas de rendement à notre échelle, l'hypothèse
   **transpose** son idée en une prédiction de rendement intraday sur nos
   contrats, et le dit dans « Ce qui n'est pas affirmé ici ». C'est une
   hypothèse de l'IA inspirée du papier, pas une affirmation du papier ; le
   harnais la juge comme les autres. Restent les écarts mécaniques déjà
   décidés : codage discordant ou refusé (`D34`), marché absent pour une
   hypothèse écrite depuis `D38`.
2. **Chaque hypothèse déclare son horizon intraday** dans « Le domaine »
   (`**Horizon :**` — « 15 minutes », « 2 heures », ou « jusqu'à la clôture de la
   fenêtre »), à l'intérieur de la fenêtre de séance. `hypotheses_lot.py` le lit
   et l'inscrit dans le lot (`horizon`) ; `measure_lot.py` et
   `lot_correlations.py` mesurent **à cet horizon**, et à lui seul.
3. **« Jusqu'à la clôture de la fenêtre »** (`H07`, `H11`, `H13`, `H14`) est un
   horizon variable que le harnais ne sait pas encore mesurer : la mesure le
   **refuse** plutôt que de le remplacer par un horizon fixe. L'ajouter au
   harnais est une modification à décider et à appliquer, avant la mesure.

## Pourquoi

**Mesurer une hypothèse à un autre horizon que celui qu'elle a écrit, c'est
mesurer une autre hypothèse** (invariant IV). Et écarter une fiche sur le
jugement de la session qui la lit revient à trier le lot sur une conclusion
qu'aucun test n'a produite : l'opérateur préfère que le harnais tranche.

**Ce qui est sacrifié.** Le lot garde ses 41 tests, donc un seuil de
Benjamini–Hochberg plus sévère (t ≈ 2,81 pour la meilleure) que s'il n'en
gardait que 10. Et des hypothèses transposées de papiers sur la volatilité ont
peu de chances de prédire un rendement : c'est le harnais qui le dira.

## Ce que ça verrouille

`scripts/hypotheses_lot.py` (`horizon_de`), `scripts/measure_lot.py`,
`scripts/lot_correlations.py`, `.claude/commands/fabriquer-signaux.md`.

## Ce qui reste ouvert

- **L'horizon « jusqu'à la clôture »** dans le harnais (`harness/metric.py`,
  `forward_returns`), avec sa déflation de recouvrement : une décision, une
  nouvelle empreinte, la porte 03 relancée.
- **`NON-ECRITES-09.md`** reste comme constat ; ses 31 fiches recevront leur
  hypothèse par `/fabriquer-signaux`.
