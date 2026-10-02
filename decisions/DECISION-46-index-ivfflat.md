# D46 — L'index de similarité des morceaux est un IVFFlat

**Date :** 2026-10-02
**Phase :** 09
**État :** prise — choix de l'opérateur (« fait ça : index IVFFlat ») ; remplace l'index `chunks_embedding_hnsw` de la migration 001

## La question

La recherche par le sens dans toute la base (`D45`) demande un index sur les
145 356 vecteurs des morceaux. Le HNSW de la migration 001 ne se construit pas
sur la petite instance Supabase. Quel index, et à quel prix ?

## Les options

1. **Attendre le HNSW.** Écartée : le 2026-10-01, avec les 32 Mo de mémoire de
   maintenance par défaut, la construction est tombée à ~5 blocs par minute
   (environ deux jours restants), a saturé la base (connexions refusées), puis
   s'est arrêtée sans rien laisser. À 512 Mo, « No space left on device ».
2. **Agrandir l'instance le temps de construire le HNSW.** Écartée par
   l'opérateur : payant, et à refaire à chaque reconstruction.
3. **Un index IVFFlat.** Retenue.

## Le choix

Migration `007_index_ivfflat.sql` : `chunks_embedding_hnsw` est retiré,
`chunks_embedding_ivfflat` le remplace (`lists = 150`), et `vector_search` lit
12 listes (`ivfflat.probes = 12`, posé sur la fonction). Les deux réglages
suivent les recommandations de pgvector (`lists` ≈ lignes / 1000 sous le
million de lignes, `probes` ≈ √`lists`) et sont fixés **avant** tout essai de
recherche.

## Pourquoi

IVFFlat se construit en une passe de k-moyennes, avec peu de mémoire, en
quelques minutes sur l'instance actuelle, gratuitement.

**Ce qui est sacrifié.** La recherche est approchée plus grossièrement qu'avec
HNSW : un morceau proche rangé dans une liste non lue est manqué. Pour un
dossier de voisins (`D45`), qui ne mesure rien et ne fait que proposer des
papiers à lire, la perte est acceptable. Et l'index ne s'adapte pas : ses
centres sont ceux des vecteurs présents à sa construction. Après une grosse
ingestion, il faut le reconstruire.

## Ce que ça verrouille

`vectordb/migrations/007_index_ivfflat.sql`, `vector_search`,
`scripts/voisins.py`. Aucun IC, aucune fiche, aucune hypothèse n'en dépend :
changer d'index plus tard ne périme rien.

## Ce qui reste ouvert

- Le **rappel** réel (la part des vrais plus proches voisins retrouvée) n'est pas
  mesuré. On peut le comparer à une recherche exacte sur quelques fiches, si
  les dossiers semblent manquer des papiers évidents.
- `strategies_embedding_hnsw` reste un HNSW : la table est minuscule.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-02 | construction lancée par l'outil Supabase (HTTPS ; le port 5432 est bloqué sur ce réseau) | en cours |
