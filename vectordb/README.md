# `vectordb` — la base vectorielle des papiers

PostgreSQL sur Supabase, `pgvector`, recherche hybride par *Reciprocal Rank
Fusion*.

Cette couche fait **une** chose : ranger et retrouver. Elle n'extrait aucun
PDF, n'appelle aucun modèle d'embedding, ne découpe aucun texte, ne backteste
rien. Les vecteurs lui arrivent tout faits.

```
vectordb/
  migrations/001_init_vector_db.sql   le schéma, les index, les 3 fonctions
  vector_db.py                        le client Python
  test_vector_db.py                   le test de bout en bout
  requirements.txt
```

---

## 1. Installer

```bash
python -m pip install -r vectordb/requirements.txt
```

**Volontairement hors de `pyproject.toml`.** Le verrou du dépôt vient d'être
épinglé par `D19` (`pypdf==6.14.2`) ; y ajouter une dépendance sans rapport le
ferait rejouer. À intégrer plus tard, par une décision.

## 2. Choisir la dimension

`pgvector` fige la taille dans le DDL — il n'existe aucune façon de la rendre
dynamique. Par défaut **1536** (`text-embedding-3-small`). Pour une autre :

```bash
sed -i 's/vector(1536)/vector(3072)/g' vectordb/migrations/001_init_vector_db.sql
```

Après chargement des données, en changer impose une migration de table
complète. C'est le moment de décider.

## 3. Migrer

**Par le tableau de bord** — *SQL Editor*, coller le contenu de
`001_init_vector_db.sql`, exécuter. L'extension `vector` est disponible sur
toutes les offres Supabase, y compris gratuite.

**Par la ligne de commande** :

```bash
psql "$DATABASE_URL" -f vectordb/migrations/001_init_vector_db.sql
```

La migration n'est **pas idempotente** : `create type` échoue si le type
existe. Pour rejouer à blanc :

```sql
-- L'ORDRE COMPTE : les fonctions dépendent des types, et `drop type` échoue
-- tant qu'elles existent. Vérifié en rejouant la migration à blanc.
drop function if exists vector_search, hybrid_search, strategy_search;
drop table    if exists chunks, strategies, papers cascade;
drop type     if exists section_type, strategy_type;
```

## 4. Connexion

Dans `.env`, à la racine :

```bash
# Supabase : Project Settings > Database > Connection string > URI
DATABASE_URL=postgresql://postgres.<ref>:<mot-de-passe>@<host>:5432/postgres

# Facultatif, si la dimension n'est pas 1536
EMBEDDING_DIM=1536
```

À défaut de `DATABASE_URL`, les variables `PGHOST`, `PGPORT`, `PGDATABASE`,
`PGUSER`, `PGPASSWORD` sont lues. Aucune valeur par défaut pour le mot de
passe : un identifiant deviné est un identifiant qui finit dans un dépôt.

`.env` est déjà dans `.gitignore`.

## 5. Tester

```bash
python vectordb/test_vector_db.py
```

Il insère deux faux papiers, exerce les trois recherches et les filtres, puis
**nettoie ce qu'il a écrit — même si une vérification échoue**.

Ce qu'il ne prétend pas faire : juger la pertinence. Les vecteurs sont
aléatoires, donc l'ordre rendu ne veut rien dire. Ce qui est vérifié, c'est que
la plomberie répond, filtre et compte juste.

---

## Ce qu'il faut savoir avant de s'en servir

**RLS est activé, sans aucune politique.** Donc : refus par défaut pour `anon`
et `authenticated`, passage libre pour `service_role` et pour une connexion
`psycopg` directe. Une clé publique qui fuiterait ne lirait rien. Ouvrir la
lecture à un rôle demande une politique explicite — à traiter comme une
décision, pas comme un réglage.

**Un vecteur ne s'insère jamais sans le nom de son modèle.** La contrainte
`*_embedding_provenance` refuse l'un sans l'autre. Sans elle, changer de modèle
un jour mélangerait des vecteurs incomparables dans la même colonne **sans que
rien ne le dise**. C'est `D09` — une valeur venue du dehors porte sa
provenance — appliqué aux embeddings.

**`sharpe_ratio` reste `NULL` quand le papier ne le donne pas.** Jamais `0.0`,
jamais une estimation. L'interdit constitutionnel : *une valeur plausible
inventée devient indétectable en aval ; un `NULL` est bruyant.*

Conséquence directe : un `sharpe_min` non nul **exclut** les stratégies sans
Sharpe. On ne filtre pas sur un nombre absent, et les garder traiterait
« inconnu » comme « au-dessus du seuil ».

**`asset` est du texte libre, assumé.** « oil », « Oil » et « CL » seront trois
actifs distincts. Aucune jointure vers `catalogue/catalogue.yaml`. Normaliser
plus tard coûtera une migration de données.

**Le `score` de `hybrid_search` n'est pas une similarité.** C'est une somme
d'inverses de rangs, bornée par `2/(k+1)` ≈ 0,033 pour `k = 60`. Il **ordonne**
et ne **mesure** pas : il ne se compare pas d'une requête à l'autre.

RRF combine des *rangs* précisément parce qu'une distance cosinus et un
`ts_rank_cd` ne vivent pas sur la même échelle — les additionner donnerait un
nombre dont personne ne saurait dire ce qu'il mesure.

**Le plein texte combine les termes en ET**, `websearch_to_tsquery` étant ainsi
fait. Un seul mot absent du morceau et la moitié plein texte ne rend **rien** ;
le classement retombe alors sur le seul vectoriel — silencieusement, puisque
RRF n'a plus qu'une liste à fusionner.

```
'backwardated contracts carry'  ->  'backward' & 'contract' & 'carri'   aucune correspondance
'commodity futures carry'       ->  'commod' & 'futur' & 'carri'        correspond
```

Ça n'est pas un défaut, c'est le comportement à connaître avant d'écrire une
requête. Pour un OU explicite, `to_tsquery` avec `|` conviendrait mieux — c'est
un changement de fonction, donc une décision.

**Seul `chunks.content` est indexé en plein texte.** `strategies.signals` et
`papers.abstract` ne le sont pas : une recherche hybride ne les atteindra
jamais. C'est ce qui a fait échouer la première rédaction du test.

---

## Les trois fonctions

| Fonction SQL | Wrapper Python | Ce qu'elle fait |
|---|---|---|
| `vector_search` | `VectorDB.vector_search` | similarité cosinus seule ; filtres `year_min`, `year_max`, `section` |
| `hybrid_search` | `VectorDB.hybrid_search` | plein texte + vectoriel fusionnés par RRF ; rend contenu, score, titre, page |
| `strategy_search` | `VectorDB.strategy_search` | stratégies ; filtres `asset`, `strategy_type`, `sharpe_min` |

```python
from vector_db import VectorDB, Paper, Chunk

with VectorDB.from_env() as db:
    paper_id = db.insert_paper(Paper(title="…", year=2018, doi="10.…"))
    db.insert_chunks(paper_id, [
        Chunk(content="…", ordinal=0, section="results", page=9,
              embedding=[...], embedding_model="text-embedding-3-small"),
    ])
    for row in db.hybrid_search("intraday momentum", query_vec, match_count=5):
        print(row["score"], row["title"], row["page"])
```

## Notes de schéma

- **`ordinal`**, pas `position` : `position(x in y)` est une fonction SQL et
  `order` est réservé. `ordinal` ne l'est pas.
- **`title_norm`** est une colonne *générée* : c'est elle qui porte l'unicité
  quand le DOI manque. La calculer côté client laisserait deux appelants
  diverger sur la même chaîne, et le doublon passerait.
- **`section` et `strategy_type` sont des `enum`**, donc des listes closes.
  Ajouter une valeur est un `alter type` explicite. Une catégorie `other` qui
  gonfle est un signal à lire, pas un fourre-tout à élargir en passant.
- **La suppression est en cascade** depuis `papers`. Il n'existe volontairement
  aucun mode « écraser » à l'insertion : remplacer un papier emporterait ses
  morceaux, ce qui ne doit jamais arriver par inadvertance.
