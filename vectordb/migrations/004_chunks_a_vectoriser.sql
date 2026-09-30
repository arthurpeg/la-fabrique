-- 004 — Trouver vite les morceaux qui n'ont pas encore d'embedding.
--
-- Le 2026-09-30, avec ~140 000 morceaux en base, `select count(*) from chunks
-- where embedding is null` parcourait toute la table — vecteurs compris — et
-- dépassait le délai de requête du pooler Supabase (`statement timeout`) :
-- `vectordb/embed.py` tombait avant même de commencer. Un index PARTIEL, sur les
-- seules lignes encore à vectoriser, rend ce comptage et la sélection des lots
-- quasi immédiats. Il se vide de lui-même à mesure que les embeddings s'écrivent.
--
-- Appliquée par `vectordb/embed.py --migrer-004` (délai de requête allongé), ou
-- à la main dans l'éditeur SQL de Supabase.

create index if not exists chunks_sans_embedding_idx
    on chunks (paper_id, ordinal)
    where embedding is null;
