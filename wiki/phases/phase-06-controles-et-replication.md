---
type: phase
updated: 2026-09-17
status: en-cours
phase: 06
gate: un signal dégénéré est rejeté avant le harnais ; le harnais réplique un résultat publié connu
sources: [ETAT.md, decisions/DECISION-08-controles-automatiques.md, harness/controls.py]
---

# Phase 06 — Contrôles automatiques et réplication

**Ouverte le 2026-09-17. NON FRANCHIE.** Sa clause 1 est franchie
(`scripts/gate_06_controls.py`, 25 vérifications) ; sa clause 2 ne l'est pas, et
une porte à moitié franchie est une porte non franchie.

## La porte, en deux clauses

1. **Un signal volontairement dégénéré — constant, ou presque vide — est rejeté
   avant d'atteindre le harnais d'IC.** Franchie.
2. **Le harnais réplique un résultat publié connu, contrôles compris, sans
   intervention.** Première cible : la falsification de Mesfin (2026). Non
   franchie, et bloquée — voir plus bas.

## Clause 1 — ce qui a été construit

`harness/controls.py`, **dans** le harnais et non à côté. La raison est facile à
manquer : `registry.code_hash()` n'empreinte que `harness/*.py`, donc un seuil
modifié une ligne plus loin changerait les rejets sans changer l'empreinte, et
deux résultats incomparables porteraient le même numéro de juge
([[Failed Ideas/ledger#F22]]).

Les contrôles tournent **avant que le jeton soit pris**. Un signal rejeté n'a
produit aucun IC : il ne consomme aucune ligne, et le dénominateur ne se remplit
pas de tests qui n'ont jamais eu lieu.

| Contrôle | Seuil | Effet |
|---|---|---|
| score constant | moins de 2 valeurs distinctes | cellule rejetée |
| quasi constant | moins de 10 % de valeurs distinctes | cellule rejetée |
| trop peu d'observations | moins de 30 | cellule rejetée |
| signal exsangue | moins de 2 cellules survivantes | **signal rejeté** |
| « trop beau pour être vrai » | IC au-delà de 0,10 | **signalé**, jamais bloqué |

Le détecteur de suspicion ne bloque pas, et c'est délibéré : refuser un résultat
parce qu'il est trop beau reviendrait à le décider avant de le voir. Il est
calculé, inscrit, et **imprimé dans le rapport**.

## Deux pièges écartés, et une porte qui est tombée

**« 99 % de NaN » ne veut pas dire « 99 % de barres non scorées ».** Les étalons
scorent une barre par séance sur environ 390 : 99,7 % des barres n'ont pas de
score, et c'est la forme de l'hypothèse. Un contrôle écrit sans cette distinction
aurait rejeté les deux seuls signaux du projet
([[Failed Ideas/ledger#F23]]).

**Le plancher de deux cellules a cassé la porte 03** dans la minute. Sa
calibration reproduit à la main l'IC d'**une seule** cellule, à 1e-12 — c'est tout
son objet. Le harnais sert deux sortes de clients, des tests et des calibrations
de lui-même, et une règle écrite pour les premiers interdisait les secondes.
Dérogation écrite, et vérifiée **étroite** par la porte 06 elle-même. Voir
[[lessons|L11]] et [[Failed Ideas/ledger#F24]].

## Clause 2 — pourquoi elle est bloquée

Rejouer Mesfin (2026) « avec notre modèle de coût » suppose de connaître notre
coût. `harness/costs.py` ne rend qu'un **plancher** : `fee_bp` et `slippage_bp`
sont ouverts. Conséquence à ne pas contourner — on peut conclure « ne survit pas
même au plancher », jamais « survit sous nos coûts ».

Ce qu'il faut avant, dans l'ordre : une convention de provenance des valeurs
externes, les multiplicateurs CME, la réponse de Lucid sur le caractère all-in de
ses commissions, une déclaration écrite de `slippage_bp`. Voir `ETAT.md`
§ Prochaine action.

## Ce qui n'a pas encore été fait, et qui appartient à cette phase

**`H01` et `H02` ne sont pas mesurés.** `counted_tests()` vaut **0**. Leur mesure
fera les deux premiers tests comptés du projet, et elle est irréversible.

## Voir aussi

[[phases/phase-05-api-de-signal]] · [[signaux/README]] ·
[[concepts/comptage-des-tests]] · [[concepts/cout-aller-retour]]
