-- 005 — Écrire les embeddings par l'API REST (HTTPS), quand le port 5432 est fermé.
--
-- Le réseau de l'université bloque le port 5432 ; l'API de Supabase passe par
-- HTTPS. Elle ne sait pas mettre à jour un lot de vecteurs d'un coup : cette
-- fonction le fait, en une requête par lot (`vectordb/embed.py --api`).
--
-- SÉCURITÉ : la fonction n'est exécutable que par `service_role`, c'est-à-dire
-- avec la clé SECRÈTE du projet. Ni la clé publique (`anon`, `publishable`) ni un
-- utilisateur connecté ne peuvent l'appeler : sans cette restriction, n'importe
-- qui ayant la clé publique pourrait réécrire les vecteurs.
--
-- À coller dans l'éditeur SQL du tableau de bord Supabase.

create or replace function public.enregistrer_embeddings(
    ids uuid[], vecteurs text[], modele text
) returns integer
language sql
set search_path = public
as $$
    with v as (select unnest(ids) as id, unnest(vecteurs) as e),
         u as (
             update chunks as c
                set embedding = v.e::vector,
                    embedding_model = modele
               from v
              where c.id = v.id
          returning 1
         )
    select count(*)::integer from u;
$$;

revoke execute on function public.enregistrer_embeddings(uuid[], text[], text)
    from public, anon, authenticated;
grant execute on function public.enregistrer_embeddings(uuid[], text[], text)
    to service_role;
