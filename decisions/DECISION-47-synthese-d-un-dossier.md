# D47 — Une hypothèse tirée d'un papier et de ses voisins dans toute la base

**Date :** 2026-10-02
**Phase :** 09
**État :** prise — demande de l'opérateur (« fais le 1 » : l'étape qui combine un papier et ses voisins) ; étend `D39` et `D45`, ne touche ni au harnais, ni au registre

## La question

`D45` trouve les voisins d'une fiche dans toute la base, fichés ou non. Il
manquait l'étape qui les lit et en tire **une** hypothèse. Il fallait d'abord
trancher une question laissée ouverte par `D45` : contre quoi vérifier une
citation tirée d'un voisin **sans fiche** ?

## Les options

1. **Ficher d'abord chaque voisin retenu**, puis faire une synthèse `D39`
   ordinaire. Écartée : une fiche coûte environ 170 000 tokens, et la plupart
   des voisins ne servent qu'à confirmer ou préciser un point.
2. **Vérifier la citation contre le texte du voisin en base**, figé dans le
   dépôt au moment de la préparation. Retenue.

## Le choix

`scripts/synthese_dossier.py` :

1. `--prepare <fiche graine>` lance la recherche de `D45` et écrit le dossier
   (`corpus/dossiers/<graine>.json`, désormais **versionné** : c'est la liste
   des voisins contre laquelle on juge). Pour chaque voisin sans fiche, il fige
   son texte en base dans `corpus/text/base-<id>.default.txt`, à côté des
   extractions de `D18`. La consigne contient la fiche graine, puis, pour
   chaque voisin, sa fiche s'il en a une et ses quatre passages les plus proches.
2. `fabrique-synthese` écrit **une** fiche de synthèse (schéma `D14` plus le bloc
   `synthesis` de `D39`, augmenté de `dossier`, `ignored` et `contributions`).
   Il complète l'hypothèse de la graine, mais n'empile pas plusieurs signaux et
   ne conditionne pas à un régime : ces deux opérations sont des étapes à part.
   La version se choisit par les `CRITERES` de `D39`, dans l'ordre.
3. **Le validateur** est mécanique et tient à la lettre :
   - la graine et au moins un voisin figurent dans les sources ;
   - toute source appartient au dossier ;
   - chaque citation se retrouve mot pour mot dans le texte de sa source
     (`check_f2` : extractions `D18` pour un voisin fiché, texte figé sinon) ;
   - l'empreinte est inscrite.
4. La fiche vit dans `corpus/fiches_synthese/` et suit la chaîne ordinaire.
   `recette.texte_du_papier` lit le texte figé sans changement.

## Pourquoi

C'est le chemin que l'opérateur a demandé : partir d'un papier, chercher dans
toute la base ce qui va avec, et en faire une hypothèse plus complète. Et cela
sans payer une fiche par voisin. Le texte figé rend la vérification
reproductible hors réseau, comme pour une fiche.

**Ce qui est sacrifié.** Le texte en base d'un papier moissonné n'a pas la
double extraction de `D18`. C'est le texte lu à l'ingestion, désormais filtré
par le contrôle de titre (`L33`). Une citation y est trouvée ou non, mais rien
ne garantit que ce texte soit complet.

## Ce que ça verrouille

`scripts/synthese_dossier.py`, `.claude/agents/fabrique-synthese.md`,
`corpus/dossiers/`, `corpus/text/base-*`.

## Ce qui reste ouvert

- **Une synthèse qui n'apporte rien n'entre pas dans un lot.** Si la version
  retenue vient de la seule graine et qu'aucun voisin n'ajoute de paramètre,
  de marché ou d'horizon, la synthèse refait l'hypothèse de la graine : un test
  de plus, corrélé, pour rien. C'est le cas du premier essai (Baltussen 2021 :
  7 voisins sur 8 écartés, le huitième confirme sans rien changer). La règle est
  écrite dans `/fabriquer-signaux` ; elle n'est pas encore vérifiée par le code.
- **La graine doit avoir une fiche.** Partir d'un papier sans fiche demanderait
  de vectoriser sa représentation autrement.
- **La qualité des voisins** dépend de la recherche approchée (`D46`) et de la
  représentation de la fiche (`grappes.representation`). Le premier essai donne
  des voisins thématiquement proches mais rarement porteurs du même mécanisme.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-02 | premier dossier : `baltussen-2021-hedging-demand-intraday-momentum`, 8 voisins (7 sans fiche) | synthèse valide au premier essai (57 889 tokens) ; 1 voisin retenu, 7 écartés avec leur raison, 4 désaccords ; version retenue = celle de la graine, donc **pas mise au lot** (doublon de H02) ; la recette se prépare sur les textes des deux sources |
