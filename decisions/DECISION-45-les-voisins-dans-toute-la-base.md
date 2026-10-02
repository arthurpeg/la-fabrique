# D45 — Les voisins d'un papier se cherchent dans toute la base

**Date :** 2026-10-01
**Phase :** 09
**État :** prise — étend `D39` (les grappes) ; ne touche ni au harnais, ni au registre, ni aux fiches

## La question

L'opérateur veut ce chemin : un agent prend un papier intéressant, cherche par
le sens les papiers qui vont avec dans **toute** la base, et les additionne pour
écrire des hypothèses complètes et variées. Les grappes de `D39` ne relient que
des papiers déjà fichés (52 sur environ 2 100). Où chercher les voisins, et sous
quelle forme les donner à l'agent ?

## Les options

1. **Les grappes de `D39` seules** (fiche contre fiche). Écartée comme unique
   source : un papier sans fiche n'y figure pas, alors que la base en contient
   des centaines, déjà découpés et vectorisés.
2. **Une recherche par le sens dans tous les morceaux de la base**, à partir de
   la représentation de la fiche graine. Retenue.
3. **Donner à l'agent un accès direct à la base.** Écartée : l'agent qui écrit
   une hypothèse reste isolé et sans réseau (`D23`, `D34`). Il ne lit que ce
   qu'on lui remet.

## Le choix

`scripts/voisins.py <fiche_id>` :

1. vectorise la fiche graine localement, avec le modèle de la base
   (`bge-base-en-v1.5`) et la même représentation que `grappes.py` ;
2. interroge `vector_search` (migration 001) par l'API, sur **tous** les
   morceaux. Aucune origine n'est privilégiée : amorces, moissonnés et résumés
   se valent (choix de l'opérateur, « les amorces ne valent pas mieux que les
   PDF moissonnés ») ;
3. regroupe les morceaux par papier, écarte le papier graine et garde pour
   chaque voisin sa similarité, ses meilleurs passages mot pour mot, et sa
   fiche s'il en a une ;
4. écrit le **dossier** `corpus/dossiers/<fiche_id>.json` et `.md`. Il est
   régénérable et n'est pas versionné : c'est une entrée, pas un résultat.

Le dossier ne contient **aucun rendement ni aucun IC** : seulement des textes
de papiers.

## Pourquoi

C'est la seule façon de faire servir les papiers qui n'ont pas encore de fiche.
Un voisin pertinent sans fiche devient un candidat à ficher : la recherche dit
aussi **quoi ficher ensuite**, ce que l'ordre de `D33` ne savait faire que par
mots-clés.

**Ce qui est sacrifié.** Une dépendance au réseau et à l'index de similarité. Sans index,
la recherche reste exacte mais lente. Et la similarité d'un morceau ne prouve
pas que deux papiers disent la même chose : le dossier propose, il ne relie pas.

## Ce que ça verrouille

`scripts/voisins.py`, l'index `chunks_embedding_ivfflat` (`vectordb/index_morceaux.py`, `D46`),
la fonction `vector_search`. Le choix d'un autre modèle d'embedding
invaliderait les dossiers, pas les fiches.

## Ce qui reste ouvert

- **La synthèse à partir d'un dossier.** Le validateur de `D39` vérifie chaque
  citation dans le texte extrait (`D18`) d'un papier source. Un voisin sans
  fiche n'a parfois que son texte en base. Il faudra trancher, avant d'en
  écrire une, si une citation peut être vérifiée contre les morceaux de la base,
  ou si le voisin doit d'abord être fiché.
- **Le seuil de similarité** au-delà duquel un voisin compte. Aujourd'hui on
  prend les `n` plus proches, sans seuil.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-01 | outil écrit | essai en attente de la reconstruction de l'index HNSW |
