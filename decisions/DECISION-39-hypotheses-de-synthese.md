# D39 — Des hypothèses tirées de plusieurs papiers, reliés par ce qu'ils disent

**Date :** 2026-09-30
**Phase :** 09
**État :** prise — étend la chaîne fiche → signal (`D14`, `D16`, `D23`, `D34`, `D38`) à une fiche tirée de plusieurs papiers ; ne touche pas au harnais

## La question

L'opérateur veut que des hypothèses naissent aussi de **plusieurs** papiers
combinés, pour en tirer la meilleure version — et que les papiers soient reliés
par leur contenu, pas au hasard. Comment relier les papiers, comment choisir
« la meilleure version » sans surajuster, et comment faire entrer le résultat
dans la chaîne existante ?

## Les options

**Relier les papiers.**
1. Au hasard, ou par mots-clés. Écartée : des idées sans rapport.
2. **Par les embeddings de leurs fiches** (même modèle que la base,
   `bge-base-en-v1.5`), liés au-delà d'un seuil de similarité. Retenue.

**Choisir la version.**
1. Mesurer plusieurs variantes et garder la meilleure. **Interdite** : c'est
   choisir sur le résultat (invariants III et IV, `D28`).
2. Déclarer plusieurs variantes, toutes mesurées et comptées. Écartée par
   l'opérateur : plus de tests, seuil plus sévère pour tout le lot.
3. **Une seule version, choisie avant toute mesure selon des critères écrits.**
   Retenue (choix de l'opérateur, 2026-09-30).

## Le choix

1. **Les grappes** (`scripts/grappes.py`) : chaque fiche est vectorisée sur son
   titre, son affirmation, sa construction, son univers et son horizon ; deux
   fiches sont liées au-delà d'un cosinus de **0,80** ; les grappes sont les
   composantes connexes, recoupées à un seuil plus haut au-delà de 6 fiches.
   Le seuil est fixé avant de lire les grappes, sur le texte seul ; il
   correspond au 88ᵉ centile des similarités entre paires (médiane 0,756). La
   même sortie donne à chaque fiche ses cinq voisines les plus proches : la
   mémoire sémantique du critique.
2. **La synthèse** (`scripts/synthese.py`, sous-agent `fabrique-synthese`) :
   une session isolée lit les fiches d'une grappe, **aucun résultat**, et écrit
   une fiche au schéma de `D14`, plus un bloc `synthesis` (sources, mécanisme,
   accords, désaccords, critères appliqués, version retenue et d'où elle vient).
   La version se choisit dans cet ordre : l'accord entre papiers, la
   transposabilité à nos neuf futures, la parcimonie, la traçabilité.
3. **Le validateur** : chaque citation est recopiée d'une fiche source et se
   retrouve à la lettre dans le texte d'**au moins un** papier source
   (`check_f2` sur l'union de leurs extractions `D18`) ; chaque valeur dans sa
   citation ; chaque source dans la grappe ; la version retenue nomme ses
   papiers. Une synthèse n'a pas de PDF : `F4` ne s'applique pas, chaque source
   a le sien.
4. **La suite est la chaîne ordinaire** : la fiche de synthèse vit dans
   `corpus/fiches_synthese/`, que `code_signal.py` lit ; la recette lit les
   textes de toutes ses sources, bout à bout (`recette.texte_du_papier`) ; puis
   le marché (`D38`), les deux codeurs, le double codage (`D34`), un lot.
5. **Une synthèse est un test de plus.** Si ses papiers sources ont aussi leur
   hypothèse, les deux sont corrélées : la matrice de corrélation du lot
   (`D25`) le mesure, et le critique le signale avant la déclaration du lot.

## Pourquoi

**Parce qu'une idée soutenue par plusieurs papiers indépendants est plus
solide qu'une idée soutenue par un seul**, et que le choix de sa construction
peut s'appuyer sur leur accord plutôt que sur un résultat. Relier les papiers
par leur texte garantit que la synthèse réunit ce qui parle de la même chose.

**Ce qui est sacrifié.** Une synthèse ajoute un test et, si ses sources sont
déjà dans un lot, de la redondance. Et la « meilleure version » n'est la
meilleure qu'au sens des papiers : on renonce à chercher celle qui marcherait le
mieux chez nous, parce que la chercher la rendrait fausse.

## Ce que ça verrouille

- `scripts/grappes.py` (`SEUIL = 0.80`, `TAILLE_MAX = 6`), `scripts/synthese.py`
  (`CRITERES`, validateur), `.claude/agents/fabrique-synthese.md` ;
- `scripts/code_signal.py` (`FICHES_SYNTHESE`), `scripts/recette.py`
  (`texte_du_papier` d'une synthèse) ;
- `corpus/fiches_synthese/`, `corpus/PRODUCED_synthese.json`.

Changer le seuil ou les critères est une décision, et ne vaut que pour les
synthèses écrites après elle.

## Ce qui reste ouvert

- **Le lot des synthèses.** `LOT-09` est fermé ; les synthèses entreront dans un
  lot suivant, et les outils du lot (`hypotheses_lot.py`, `measure_lot.py`,
  `lot_correlations.py`, `gate_09.py`) lisent encore `LOT-09.json` seul : à
  généraliser avant ce lot.
- **Les grappes avec les papiers de la base** (non fichés) : quand les
  embeddings de la base seront complets, les papiers proches d'une grappe
  diront lesquels ficher en priorité.
- **Le seuil** n'est calibré sur aucun étalon ; le journal ci-dessous recevra ce
  que les premières synthèses en montrent.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-09-30 | premières grappes | 51 fiches ; cosinus entre paires : médiane 0,756, 90ᵉ centile 0,810, max 0,940 ; **8 grappes** de 2 à 4 fiches (transmission de volatilité, momentum sur séries temporelles, momentum intraday actions, crypto, dérive pré-FOMC…) |
| 2026-09-30 | première synthèse, grappe `G-a9d7ec` (3 papiers de momentum sur séries temporelles) | valide au 1ᵉʳ essai (après correction d'un appel du validateur, qui passait le nom de fichier avec son extension). Version retenue : Li, Sakkas & Urquhart, les 30 premières minutes prédisent les 30 dernières ; 6 désaccords écrits, dont l'effondrement hors échantillon rapporté par Duan. ~94 000 tokens. La recette lit les textes des trois sources |
