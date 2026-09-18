---
type: concept
updated: 2026-09-17
status: stable
sources: [CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md, registry/SCHEMA.md]
---

# IC — coefficient d'information

**La corrélation entre le score d'un signal et le rendement futur. Ici : en série
temporelle, poolée, et produite par le seul harnais.**

## Ce que ça veut dire ici

**IC en série temporelle, poolé entre instruments et entre cellules** — jamais
transversal. Assorti de :

- une statistique de test **robuste à la corrélation contemporaine** entre
  instruments : les résidus sont corrélés en coupe, un t de Student naïf serait
  surévalué d'un facteur proche de `sqrt(9 / 4,2) ≈ 1,46` ;
- le *pooling* justifié par [[research/bollerslev-2018-risk-everywhere]] ;
- un seuil de **FDR appliqué dès le premier test**, jamais un t-stat à 2 ;
  calibrage : [[research/harvey-2016-cross-section]], `t > 3,0`.

**La cible.** IC requis pour un IR de 1 : **0,018** si les trois fenêtres sont
indépendantes (~3 100 paris/an), **0,031** sinon (~1 060). Le rapport d'IC doit
afficher **les deux bornes, jamais la plus flatteuse seule**.

## Ce que ça ne veut pas dire

- **L'IC transversal n'a aucun sens ici.** On ne classe pas neuf actifs en
  déciles quand ils portent ~4 paris ([[Failed Ideas/ledger]] F03).
- **Un IC par cellule n'est pas un IC.** C'est un diagnostic. Un signal sur la
  grille = un IC, un test ([[concepts/comptage-des-tests]]).
- **Un IC moyen ne dit rien de la queue.** La largeur réalisée tombe sous 3 paris
  dans 17 % des séances ([[concepts/largeur-effective]]).
- **Un IC brut n'est pas un IC net.** Le modèle de coût est de première classe dès
  la phase 03 ([[concepts/cout-aller-retour]]).

## La règle dure

> **Il ne doit exister aucun chemin de code qui produise un IC sans écrire au
> registre.** Pas de corrélation calculée à la main dans un notebook, pas de
> « juste pour voir ». — `CLAUDE.md` § Les interdits, invariant III

Le **rapport d'IC** est la sortie officielle du harnais et la **seule source d'IC
du projet**. Le wiki n'en est jamais une : voir `wiki/SCHEMA.md` § 0.

## Comment on en obtient un

```python
from harness import evaluate
report = evaluate(scores, panel, "30min", signal_id="...", hypothesis_ref="...")
```

`harness/`, **figé depuis le 2026-09-17** (`D04`). Spearman par cellule, poolé
par nombre d'observations, `t` déflaté deux fois :

| correction | facteur à 30 min | pourquoi |
|---|---|---|
| recouvrement | **mesuré** (`D11`) | ÷ √30 si le score est produit à chaque barre ; **÷ 1** s'il y en a un par séance, les observations étant alors espacées de ~415 barres pour un horizon de 30 |
| transversale | ÷ 1,46 = √(9 / 4,224) | neuf instruments, ~4,2 paris |

Soit un `t` divisé par 8 pour un signal scoré à chaque barre, et **par 1,46
seulement** pour un signal à une observation par séance. Le rapport porte toujours
les deux cibles, l'écart d'échantillonnage mesuré, et un coût **minoré** disant ce
qui lui manque.

## État actuel

`registry/tests.jsonl` porte **56 lignes comptées pour 3 hypothèses** — `H01` et
`H02` (deux lignes chacune : mesure puis reprise sous `D11`) et `H03` (52 lignes,
un décalage par ligne, **un seul motif prédit**). Les trois sont sans résultat. Toutes les autres lignes sont des calibrations
et des audits, sans hypothèse, hors dénominateur ; leur nombre monte à chaque
porte rejouée et ne veut rien dire. Le compte qui compte est celui de
`registry.counted_tests()`.

La déflation a mordu pour la première fois ce jour-là — et s'est révélée trop
mordante : le `t` naïf de `H01` valait −2,27, le `t` final **−0,28**, dont un
facteur 5,48 de recouvrement inexistant. Corrigé le jour même (`D11`), le `t`
final de référence est **−1,56**. Voir [[lessons|L13]].

## Où c'est fixé

`CLAUDE.md` invariant III · `D01` §2 · `registry/SCHEMA.md`

## Voir aussi

[[concepts/registre]] · [[concepts/largeur-effective]] ·
[[concepts/comptage-des-tests]] · [[reference/metrique-et-comptage]]
