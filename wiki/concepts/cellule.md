---
type: concept
updated: 2026-09-16
status: stable
sources: [decisions/DECISION-01-univers-et-donnees.md, scripts/out/a8_session_grid.json]
---

# Cellule

**Un couple (instrument, fenêtre de séance). L'unité d'évaluation du projet.**

## Ce que ça veut dire ici

9 instruments × 3 fenêtres = 27 couples, dont **25 retenus**.

Les trois fenêtres sont **disjointes par construction** et ancrées à l'horloge
locale de la place, `America/New_York` :

| Fenêtre | Heure locale (New York) | Ce qu'elle couvre |
|---|---|---|
| `ASIA` | 19:00 → 03:00 | réouverture Globex, matinée de Tokyo |
| `EUROPE` | 03:00 → 09:30 | Francfort et Londres, avant New York |
| `US` | 09:30 → 16:00 | la séance de cotation américaine |

16:00 → 19:00 n'appartient à aucune fenêtre : règlement, arrêt quotidien, l'heure
la plus mince. Conséquence directe : **au plus une stratégie vivante par actif à
un instant donné**, par construction.

**Deux cellules écartées** sous une règle de rétention posée *avant* lecture des
chiffres (volume médian ≥ 10 contrats/min, barres minces ≤ 25 %, aller-retour
estimé ≤ ⅓ du mouvement médian de 15 min) : `6B × ASIA` et `YM × ASIA`
([[Failed Ideas/ledger]] F10).

## Ce que ça ne veut pas dire

- **Une cellule n'est pas un test.** Un signal évalué sur la grille produit **UN**
  test au registre : la statistique poolée. La ventilation par cellule est un
  **diagnostic**. Compter 25 tests par famille ferait exploser le seuil de FDR
  pour une raison purement mécanique ([[concepts/comptage-des-tests]]).
- **Sélectionner après coup la cellule qui marche le mieux est interdit.** Si une
  cellule seule est retenue plutôt que la grille, c'est une **hypothèse distincte,
  pré-enregistrée avant de voir les résultats**, et elle compte comme un test
  supplémentaire (`D01` §4).
- **L'ancrage n'est pas UTC.** Ancrer à UTC ferait dériver les fenêtres d'une
  heure deux fois par an ([[Failed Ideas/ledger]] F12).
- **L'homogénéité de l'horloge n'est pas une propriété générale** : elle tient
  parce que les neuf instruments retenus sont tous sur CME Globex. La définition
  de séance sera **déclarée par instrument au catalogue** (`D01` §8).

## L'intuition qui s'est trompée

`NQ × ASIA` était annoncé comme un cas d'exclusion évident. Mesure : 41
contrats/minute, 11,6 % de barres minces, coût à **7 %** du mouvement médian — la
**meilleure** cellule asiatique de la grille. Retenue.
Voir [[Failed Ideas/ledger]] F11.

## Où c'est fixé

`D01` §3 · `scripts/out/a8_session_grid.json`

## Voir aussi

[[concepts/largeur-effective]] · [[concepts/cout-aller-retour]] ·
[[concepts/comptage-des-tests]]
