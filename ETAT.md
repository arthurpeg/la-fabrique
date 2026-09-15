# ÉTAT

**Phase courante :** 01 — la décision données (pas encore commencée)
**Date de dernière mise à jour :** 2026-09-15
**Dernière porte franchie :** aucune. Le projet vient d'être amorcé.
**Décision la plus récente :** `decisions/DECISION-00-moteur-externe.md` — le
moteur de backtest est un composant tiers, pas encore en main ; rien n'en dépend
avant la phase 10.

> Ce fichier est lu en premier par chaque session et mis à jour en dernier.
> Les phases ci-dessous suivent **l'ordre de construction** (le juge avant
> l'accusé), pas l'ordre d'exécution de la chaîne. Voir `CLAUDE.md`, « Les deux
> ordres ».

---

## Acte I — Le socle

| # | Phase | Porte | État |
|---|---|---|---|
| 01 | La décision données | Un fichier dans `decisions/` fixe fournisseur, univers, période, granularité, et chiffre l'adéquation aux besoins du projet. Rien ne la bloque : elle se prend sur nos besoins, pas sur le format d'un moteur tiers (D00). | à faire |
| 02 | Le Panel point-in-time | Un panel se charge, est reproductible, et aucune ligne n'est visible avant son `close_stamp` + `publication_lag_minutes`. | à faire |
| 03 | Le harnais d'IC calibré à la main | Le harnais reproduit à la main, sur un cas connu, un IC vérifié indépendamment. Figé et versionné à partir de là. | à faire |
| 04 | Le registre et le verrou du holdout | Aucun chemin de code ne produit un IC sans écrire au registre ; la tranche `holdout` est inaccessible par construction. | à faire |

## Acte II — Automatiser le jugement

| # | Phase | Porte | État |
|---|---|---|---|
| 05 | API de signal, sandbox, test de causalité | Un signal qui tente de lire le futur échoue au test de causalité, automatiquement. | à faire |
| 06 | Contrôles automatiques et réplication | Le harnais réplique un résultat publié connu, contrôles compris, sans intervention. | à faire |
| 07 | Triage et extraction sur 20 papiers connus | 20 fiches produites ; le triage écarte ce qu'il doit écarter, sur un verdict humain de référence. | à faire |
| 08 | Le codeur de signal | Une fiche produit un signal exécutable qui passe la sandbox, sans retouche manuelle. | à faire |

## Acte III — Fermer la boucle une fois

| # | Phase | Porte | État |
|---|---|---|---|
| 09 | Premier passage complet sur 30 à 50 papiers | La chaîne tourne de bout en bout ; le registre compte tous les tests ; un rapport d'IC existe pour chaque signal. | à faire |
| 10 | Une stratégie, un backtest | Un signal survivant devient une stratégie backtestée. Une décision écrite fixe l'attache du moteur tiers — ou, s'il n'est pas arrivé, requalifie la phase en « construire un moteur ». | à faire |

## Acte IV — Étendre par risque croissant

| # | Phase | Porte | État |
|---|---|---|---|
| 11 | Taxonomie data-driven | Les familles de signaux sont déduites des données, pas postulées. | à faire |
| 12 | Combinaisons | Toute combinaison testée a une hypothèse écrite et horodatée avant son résultat. | à faire |
| 13 | Régimes | Idem pour les hybrides. Le nombre de régimes est justifié, pas ajusté après coup. | à faire |
| 14 | Générateur d'hypothèses | Le générateur s'alimente de `LECONS.md` et du registre ; ses propositions passent les mêmes portes. | à faire |
| 15 | Le holdout | Ouvert une fois. Sharpe dégonflé du nombre de tests du registre. Fin. | à faire |

---

## Prochaine action

**Phase 01 — la décision données.** Rien d'autre ne commence avant qu'elle soit
écrite dans `decisions/`.
