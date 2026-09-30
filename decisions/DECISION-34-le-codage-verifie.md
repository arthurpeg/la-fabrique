# D34 — Le codage vérifié : recette, choix écrits, double codage

**Date :** 2026-09-30
**Phase :** 09
**État :** prise — complète `D23` ; resserre l'entrée dans un lot (`D25`, `D27`, `D28`) ; ne touche pas au harnais

## La question

Un IC mort ne dit pas **pourquoi** il est mort : l'idée du papier ne marche pas
chez nous, ou le codeur a codé autre chose que le papier. `D23` juge un codage
contre sa fiche et attrape le grossier ; il laisse passer, et il le mesure
lui-même (§ Pourquoi), un signal fidèle à une lecture fausse ou partielle de la
fiche. Comment séparer les deux causes **avant** la mesure, sans calculer un
seul IC ?

## Les options

1. **Déboguer le codage d'après l'IC.** Écartée : c'est choisir son code d'après
   le résultat, et `D28` interdit la seconde mesure qu'il faudrait.
2. **Un relecteur séparé** qui compare fiche et code sans rien modifier.
   Écartée comme condition : un relecteur se laisse convaincre par un code qui
   a l'air propre, et son verdict n'est pas mécanique. Reste permise, sans
   effet sur la porte.
3. **Un mini-panel synthétique** dont la réponse se calcule à la main.
   Écartée par l'opérateur le 2026-09-30.
4. **Trois gestes mécaniques avant la mesure : la recette, les choix écrits, le
   double codage.** Retenue.

## Le choix

Aucun signal n'entre dans un lot — hypothèse écrite, matrice de corrélation,
mesure — sans ces trois gestes, tous tenus par du code déterministe :

**1. La recette** (`scripts/recette.py`). Avant le codage, une session isolée
relit le texte du papier et complète la fiche par sa formule, ses entrées et
l'instant où chacune est connue, le timing du score, chaque paramètre et les
ambiguïtés. **Tout est cité mot pour mot**, ou `null` avec sa raison. Le
validateur vérifie chaque citation dans le texte (`D18`), chaque valeur dans sa
citation (`value_in_quote`, `D09`), chaque `null` a sa raison, chaque résolution
d'ambiguïté a sa citation. Réparations admises : celles de `D16` (`ocr`,
`math_notation`, `table`). `code_signal.py --prepare` refuse une fiche sans
recette valide ; le codeur et le juge reçoivent la fiche augmentée de sa
recette, sous la clé `recipe`.

**`S5` s'étend à la recette, par ses valeurs et ses citations seulement**
(`score_signal.texte_de_la_recette`), jamais par sa prose : une phrase écrite
par la session de recette n'est pas le papier, et un nombre qu'elle y écrirait
serait un paramètre inventé que `S5` blanchirait.

**2. Les choix écrits.** Chaque module produit déclare `CHOICES`, un tuple
littéral de chaînes : chaque interprétation que la fiche ou sa recette laissait
ouverte, ce qui a été choisi, pourquoi. `code_signal.py --judge` refuse un
module qui n'en déclare pas. Le contrat de `D07` n'est pas modifié : `CHOICES`
est exigé par `D34`, pas par le harnais.

**3. Le double codage** (`scripts/double_codage.py`). Deux sessions isolées, de
**deux modèles différents** — principal `opus`, témoin `sonnet` — codent la même
fiche avec la même recette, sans se voir. Le principal écrit dans `signals/`, le
témoin dans `verification/temoins/` (même nom, même `SIGNAL_ID`, registre de
production propre). Chacun passe `D23` et `CHOICES`. Puis leurs **scores** sont
comparés sur le `pool` à l'instant du juge `D23` (`2018-06-15 20:00`) :

| Condition | Seuil |
|---|---|
| même `EXPECTED_SIGN` | exigé |
| Spearman par cellule, moyenne pondérée par le nombre de paires | **≥ 0,70** |
| part des (cellule, instant) notés par les deux | **≥ 0,80** |

**CONCORDANT** ouvre le lot. **DISCORDANT** renvoie à la recette : l'ambiguïté se
lit dans les `CHOICES` des deux codeurs, la recette est refaite en la nommant
(`--precisions`), et les deux codages sont refaits par des sessions neuves. Au
bout de **deux tours** discordants, la fiche est **écartée du lot**
(`scripts/ecarter_du_lot.py`), comme après trois refus de `D23` ou une recette
impossible.

**Écarter n'est permis qu'avant la première mesure du lot.** L'entrée passe de
`fiches` à `ecartees_codage`, avec sa preuve, son motif et sa date, et `n`
diminue d'autant. La porte 09 revérifie la concordance de chaque entrée et
l'antériorité de chaque écart (`codage_verifie.fautes_d34_du_lot`).

## Pourquoi

**Parce que la concordance est la seule mesure de l'erreur de codage qui ne
regarde aucun rendement.** Deux lectures indépendantes qui retrouvent le même
score disent que l'erreur de codage n'explique pas un IC mort ; deux lectures
qui divergent disent qu'on ne saurait pas lequel mesurer. Rien de tout cela
n'est un IC : aucun rendement n'entre dans le calcul, rien n'est écrit au
registre, et les deux outils cassent si le registre bouge.

**Le seuil de 0,70 est fixé avant toute mesure, et il est sévère à dessein.**
La seule mesure connue, la calibration de `D23` sur Baltussen (2026-09-23),
donne 0,53 entre le codeur et une implémentation humaine : 0,76 à 0,80 sur les
indices américains en séance US, 0,28 à 0,41 ailleurs. Sous `D34`, ce couple
serait DISCORDANT, et c'est ce qu'on veut : les deux lectures partagent l'idée
mais divergent hors de la séance US, et un IC mesuré là ne dirait pas laquelle
il juge. Un seuil plus bas laisserait entrer exactement ce cas.

**Deux modèles plutôt qu'un.** Deux sessions du même modèle ont les mêmes
réflexes et font les mêmes erreurs ; leur accord prouve moins.

**Ce qui est sacrifié.** Le coût double : deux sessions de codage et une de
recette par fiche au lieu d'une, donc environ deux fois moins de signaux par
jour d'abonnement. Et le lot peut rétrécir, puisque des fiches en sortiront
sans avoir été mesurées. On préfère un lot plus petit dont chaque IC juge
l'idée à un lot plus grand où l'on ne sait pas ce qu'il juge — c'est le but du
projet (`CLAUDE.md`, « trois signaux dont il connaît la fragilité »).

**Ce que `D34` ne prouve pas.** Deux codeurs d'accord peuvent se tromper
ensemble : ils lisent la même fiche et la même recette. La concordance prouve
que la **lecture** est stable, pas qu'elle est fidèle au papier ; ce maillon est
tenu par `D16` et par les citations de la recette, pas par `D34`.

## Ce que ça verrouille

- `scripts/codage_verifie.py` (seuils, chemins, journaux), `scripts/recette.py`,
  `scripts/double_codage.py`, `scripts/ecarter_du_lot.py` ;
- `scripts/code_signal.py` (`--temoin`, recette, `CHOICES`, jugements inscrits) ;
- `scripts/score_signal.py` (`S5` lit la recette ; `S6` lit le registre du
  dossier du module) ;
- `scripts/hypotheses_lot.py`, `scripts/measure_lot.py`, `scripts/gate_09.py`
  exigent la concordance ;
- `verification/jugements.jsonl` et `verification/concordance.jsonl` sont
  **append-only**, comme le registre ;
- `scripts/CODAGE-DES-SIGNAUX.md` décrit la boucle.

Changer un seuil après la première mesure d'un lot est interdit : ce serait
choisir le lot sur son résultat. Avant, c'est une décision écrite.

**Le signal déjà codé du lot** (`baltussen-2021-hedging-demand-intraday-momentum`,
porte 08) ne déclare pas `CHOICES` et n'a ni recette ni témoin : il repasse par
la boucle comme les autres. Son module actuel reste l'essai 1 de
`signals/PRODUCED.json`.

## Ce qui reste ouvert

- **Le seuil lui-même** n'est calibré que sur un cas. Le journal ci-dessous
  recevra la distribution des ρ des premiers tours ; si elle montre un seuil
  mal placé, il se révise **avant** la première mesure du lot, par écrit.
- **La recette n'est pas jugée contre un étalon** : son validateur prouve
  qu'elle cite, pas qu'elle cite ce qui compte. Comme la fiche creuse de `D16`.
- **L'instant de concordance** est celui du juge (`2018-06-15`), pas celui de la
  mesure (`2023-12-29`), pour tenir le coût : un désaccord qui n'apparaîtrait
  qu'après 2018 échapperait. Ouvert si un cas le montre.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-09-30 | décision prise | — |
| 2026-09-30 | calibration de l'outil, `double_codage.py --compare` (rien d'inscrit) | un signal contre lui-même : ρ 1,000, couverture 1,000, CONCORDANT. Baltussen main contre codeur : ρ **0,506** (Spearman ; 0,53 en Pearson dans `D23`), couverture 0,998, **DISCORDANT** — NQ/US 0,80, YM/US 0,75, YM/EUROPE 0,30. Registre inchangé : 169 lignes, 56 tests |
| 2026-09-30 | premier passage réel : `baltussen-2021-hedging-demand-intraday-momentum` | recette valide au 2ᵉ essai (un paramètre non numérique refusé), 18 ambiguïtés ; principal `opus` et témoin `sonnet` verts au 1ᵉʳ essai ; **ρ 1,000, couverture 1,000, CONCORDANT** sur 25 cellules. Coût mesuré : recette ~165 000 tokens (le texte du papier entier), codages ~80 000 chacun. Deux bugs d'outil trouvés par ce passage et corrigés (`L30`) |
