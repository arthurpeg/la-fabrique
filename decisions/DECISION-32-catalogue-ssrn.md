# D32 — Le catalogue SSRN : remplir la base de résumés, jusqu'à un budget écrit

**Date :** 2026-09-28
**Phase :** 09
**État :** prise — complète `D31`

## La question

L'opérateur demande de verser dans la base **tous** les papiers SSRN sur le
pétrole, l'or, le bitcoin et les devises, jusqu'à ce qu'elle soit pleine et
**encore utilisable**. Combien en tient-elle, combien en existe-t-il, et par
quel chemin — le moissonneur plafonne à 60 par axe (`D20`) ?

## Ce qui est mesuré, le 2026-09-28

- **La base** pèse **163 Mo** pour 12 422 morceaux (745 papiers). Un papier
  « résumé seul » (`D31`) y coûte **~13 Ko** tout compris — morceau, vecteur
  768 dimensions, index HNSW, index plein texte.
- **Le plafond** : le plan gratuit de Supabase limite la base à **500 Mo**,
  au-delà desquels elle passe en lecture seule. Le budget du projet est de
  0 € (`D01`), donc c'est ce plan.
- **L'offre** : une requête d'un seul mot est précise — « bitcoin » rend
  **1 311** dépôts SSRN, **100 %** dans le périmètre sur les deux pages lues,
  45 à 71 % avec résumé. Une requête de plusieurs mots rend n'importe quel mot
  (`D31` § Journal) : le périmètre doit donc être vérifié, pas supposé.
- **Crossref** bride les requêtes lourdes (`429` sur des pages de 1 000) : il
  faut des pauses et des reprises.

## Les options

1. **Un catalogue séparé du moissonneur**, versé directement dans la base.
   Retenue.
2. **Des centaines d'axes de 60 dans `harvest.json`.** Écartée : ce serait
   contourner le plafond de `D20` par le nombre, et `harvest.json` —
   versionné, réécrit à chaque passage — enflerait de dizaines de mégaoctets
   dans git. Surtout, un travail de `harvest.json` est destiné à être SONDÉ pour
   son PDF ; 18 000 sondes n'ont aucun sens pour des résumés.
3. **Relever le plafond de `D20`.** Écartée : il protège le lot de la phase 09,
   qui vit dans `harvest.json`, et n'a pas de raison de bouger pour une base de
   recherche.

## Le choix

`corpus/ssrn_catalogue.py` interroge Crossref (préfixe SSRN `10.2139`) sur une
liste de requêtes **écrite dans le script avant d'être lancée**, pagine par
curseur, et verse chaque dépôt **dans le périmètre** et **pourvu d'un résumé**
dans la base, `text_source = 'abstract'`, jusqu'au budget.

**Le budget : 400 Mo**, soit 80 % du plafond. Les 100 Mo restants sont la
marge d'une base « utilisable » : reconstruction d'index, écritures futures des
fiches et stratégies, nettoyage (`VACUUM`), sans frôler la bascule en lecture
seule. Le script calcule avant d'insérer combien de papiers le budget permet
(~13 Ko chacun, vecteur compris) et s'arrête là.

**Le périmètre est une règle mécanique, écrite ici** : le titre ou le résumé
contient un mot de l'actif (pétrole : `oil`, `crude`, `petrol`, `brent`,
`wti` ; or : `gold`, `precious metal` ; crypto : `bitcoin`, `crypto`,
`blockchain`, `ethereum`, `stablecoin`, `defi` ; devises : `exchange rate`,
`currenc`, `forex`, `foreign exchange`, `fx`). Une requête s'arrête quand une
page de 1 000 n'a plus que **10 %** de dépôts dans le périmètre, ou après 10
pages.

## Pourquoi

**Ce n'est pas le filtre que `F50` interdit.** `F50` refuse au moissonneur de
juger ce qui est **implémentable** — la moitié de la porte 07, qui a son juge et
son étalon. Ici la règle ne juge rien de tel : elle **définit le périmètre**
que l'opérateur a demandé (« sur ces actifs »), par des mots écrits d'avance,
vérifiables par quiconque. Un papier sur le pétrole inimplémentable y entre ;
c'est le trieur qui l'écartera. Sans cette règle, une requête de plusieurs mots
verse des papiers d'actions — mesuré, 79 % au premier passage de `D31`.

**Ce qui est sacrifié.**

- **Ces papiers n'ont pas de PDF et ne sont pas dans `harvest.json`** : ni
  sonde, ni dépôt manuel (`D30`), ni fiche ne s'y appliquent directement. Pour
  ficher l'un d'eux, il faut d'abord l'amener dans le moissonneur par un axe.
- **Le résumé n'est pas versionné** : il vit dans la base. Le dépôt garde le
  **manifeste** (`corpus/ssrn_catalogue.jsonl` : DOI, titre, année, actifs,
  requête, date), qui suffit à le retrouver chez Crossref. Versionner 18 000
  résumés alourdirait git pour une donnée qu'un DOI rend.
- **Un dépôt sans résumé chez Crossref** n'entre pas : il n'a aucun texte.

## Ce que ça verrouille

- `corpus/ssrn_catalogue.py` : requêtes, règle de périmètre, budget, arrêt.
  Modifier une requête ou la règle après un passage est une décision écrite.
- `corpus/ssrn_catalogue.jsonl` : le manifeste, en ajout seul.
- La base : `text_source = 'abstract'` pour ces papiers (`D31`, migration
  `003`).

## Ce qui reste ouvert

- **Le plan Supabase.** Si la base passe à un plan payant, le budget se
  réécrit ici, pas dans le script seul.
- **La qualité de la recherche** avec des milliers de résumés à côté de 136
  textes intégraux : une requête plein texte ou vectorielle ramènera surtout
  des résumés. Filtrer par `text_source` dans les requêtes de recherche est à
  décider quand on s'en servira.

## Journal

- **2026-09-28** — décision prise. Résultats du passage ci-dessous.
- **2026-09-28, premier passage** (`--ingest`, 10 pages au plus par requête) :
  **12 618 dépôts** nouveaux dans le périmètre et pourvus d'un résumé — devises
  6 014, pétrole 4 247, crypto 3 102, or 1 275 (un dépôt peut compter pour deux
  actifs). **11 929 versés** ; les autres étaient déjà en base (DOI ou titre).
  Base : 163 → 220 Mo avant embeddings. Aucun `429` : les pauses ont suffi.
  **Le budget n'a pas tranché, l'offre si** : `bitcoin`, `cryptocurrency`,
  `blockchain`, `ethereum`, `stablecoin`, `crude oil` (9 897 notices, toutes
  lues), `petroleum`, `gold`, `currency` épuisées ; `oil` n'ajoute rien à
  `crude oil`, qui l'englobe ; `precious metals` et `carry trade` arrêtées par
  la règle des 10 %. **Deux requêtes ont été coupées par le plafond de 10
  pages et non par le périmètre** : `exchange rate` (13 % à la page 10) et
  `foreign exchange` (23 %), ainsi que `oil price` (52 %, mais tout dépôt
  pétrole y est déjà couvert par `crude oil`).
- **2026-09-28, amendement déclaré AVANT le second passage** : `MAX_PAGES`
  passe de 10 à **25**. Seule la règle des 10 % et le budget arrêtent désormais
  une requête. Les requêtes et le périmètre ne changent pas.
- **2026-09-28, second passage** (25 pages au plus) : **731 papiers de plus**
  versés ; base 230 → 235 Mo avant embeddings. **Toutes les requêtes sont
  désormais épuisées** — lues jusqu'à leur dernière page (`exchange rate` 17,
  `foreign exchange` 15, `oil price` 23), ou arrêtées par la règle des 10 %
  (`precious metals`, `carry trade`). Le passage annonçait 1 472 « nouveaux » :
  la différence est faite de dépôts SSRN **au même titre** qu'un papier déjà
  en base (SSRN attribue un numéro par version), écartés par
  `papers_title_norm_key` et absents du manifeste, d'où leur retour.
- **Bilan** : **13 269 papiers `abstract`** en base (609 de `D31`, 12 660 de
  ce catalogue), manifeste de 12 660 lignes. **Le budget n'a jamais tranché :
  c'est l'offre SSRN de ces requêtes qui est épuisée.** Taille finale après
  embeddings : ci-dessous.
- **2026-09-28, taille finale après embeddings** : **335 Mo** sur un budget de
  400 Mo (67 % des 500 Mo du plan gratuit) ; 25 082 morceaux, **tous
  vectorisés** (`bge-base-en-v1.5`) ; table `chunks` 284 Mo dont index HNSW
  98 Mo. Coût réel mesuré : ~13,5 Ko par papier `abstract`, conforme à
  l'estimation. **Marge restante : ~65 Mo sous le budget, ~165 Mo sous le
  plafond** — de quoi verser environ 4 800 résumés de plus avant le budget, si
  des requêtes nouvelles sont décidées par écrit.
