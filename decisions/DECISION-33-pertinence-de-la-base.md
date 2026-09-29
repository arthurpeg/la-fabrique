# D33 — La base de recherche ne garde que les papiers pertinents

**Date :** 2026-09-29
**Phase :** 09
**État :** prise — complète `D22`, `D31`, `D32` ; ne touche pas `D15`, `D20`

## La question

L'opérateur demande que la base ne contienne que des papiers **pertinents**
pour nous, et que les autres en soient **retirés**. Le moissonneur, lui, ne
juge pas (`F50`). Comment trier la base sans rouvrir ce que `F50` a fermé ?

## Les options

1. **Une règle mécanique écrite d'avance, appliquée à la base seule.**
   Retenue.
2. **Filtrer dans le moissonneur.** Écartée : c'est `F50` — un filtre non jugé
   écarterait des papiers du TRI sans que rien ne mesure ce qu'il écarte à
   tort. La population de `harvest.json`, du triage et du lot reste intacte.
3. **Faire juger chaque papier par un modèle.** Écartée pour la base : non
   déterministe, non rejouable, et c'est le rôle du trieur, qui a son étalon.

## Le choix

`corpus/relevance.py` : un papier est pertinent s'il nomme un **marché** de
notre univers (futures, indices et leurs contrats, or, pétrole, matières
premières, devises, crypto, taux, VIX) **et** un **signal** (rendements,
volatilité, trading, stratégie, anomalie, momentum, retournement,
prévisibilité, prévision, arbitrage, avance-retard, transmission, causalité,
intraday, haute fréquence, découverte des prix, mauvaise évaluation). Compté
sur le titre et le début du texte : **1 marché et 1 signal** dans un résumé ;
**2 marchés et 3 signaux** dans les 5 000 premiers caractères d'un texte
intégral, qui nomme en passant bien des choses.

- **À l'entrée** : `ingest.py --harvest` ne verse que les papiers pertinents.
- **Dans la base** : `relevance.py --prune` retire les papiers `harvest` et
  `abstract` non pertinents. **`authoritative` n'est jamais touché** : c'est le
  corpus fiché.

## Pourquoi

Une base de recherche où un tiers des papiers parle de retraites, de scolarité
ou de politique européenne rend des résultats hors sujet à chaque requête. La
règle est grossière, et elle le dit : elle écarte sur des **mots**, pas sur le
fond. Elle est écrite, comptée, et rejouable.

**Ce qui est sacrifié.** Des papiers utiles au vocabulaire inhabituel seront
écartés (un papier de microstructure qui ne dit ni « returns » ni « futures »
au début). Ils ne sont pas perdus : le PDF reste sur le disque, le travail
reste dans `harvest.json`, et le retrait est inscrit.

## Ce que ça verrouille

- `corpus/relevance.py` : les deux listes de mots et les seuils. Les changer
  après une purge est une décision écrite.
- `corpus/base_retraits.jsonl` : tout papier retiré, avec ses comptes et la
  date — en ajout seul. Un retrait se reverse en réingérant.

## Ce qui reste ouvert

- **La purge elle-même** attend que la base réponde (le 2026-09-29, la
  connexion à Supabase expire, probablement pendant le changement d'offre).
  Elle sera lancée à blanc d'abord, puis pour de bon.

## Journal

- **2026-09-29** — décision prise ; règle branchée dans `ingest.py --harvest`.
