# D08 — Les contrôles automatiques : où ils vivent, et pourquoi ils ne se sautent pas

**Date :** 2026-09-17
**Phase :** 06
**État :** prise

## La question

La porte 06 exige qu'un signal dégénéré — constant, ou presque vide — soit
**rejeté avant d'atteindre le harnais d'IC**. Reste à décider où ce refus habite.
Un contrôle qu'on appelle avant `evaluate()` est un contrôle qu'on oublie
d'appeler ; un contrôle dans un paquet à part n'entre pas dans l'empreinte du
harnais et change pourtant ce que le harnais juge.

## Les options

1. **Un script de contrôle qu'on lance avant de mesurer.** Écartée. C'est l'état
   de `scripts/check_signals.py`, utile pour travailler, inutile comme garantie :
   il se saute en ne le lançant pas. Même raison que
   [[Failed Ideas/ledger#F15]].

2. **Un paquet `controls/` appelé par `evaluate()`.** Écartée pour une raison
   précise et facile à manquer : `registry.code_hash()` n'empreinte que
   `harness/*.py`. Un seuil modifié dans `controls/` changerait les rejets sans
   changer l'empreinte, et deux résultats incomparables porteraient le même
   numéro de juge. Il faudrait alors élargir l'empreinte — c'est-à-dire admettre
   que ces fichiers font partie du harnais.

3. **`harness/controls.py`, dans le harnais, exécuté avant le jeton.** Retenue.
   Les contrôles *sont* du jugement déterministe : leur place est avec le juge,
   figée et empreintée avec lui. Et ils s'exécutent **avant `open_test`**, donc
   un signal rejeté ne consomme aucune ligne de registre — il n'a produit aucun
   IC, il n'y a rien à inscrire (invariant III).

## Le choix

Les contrôles de dégénérescence vivent dans `harness/controls.py`, sont
empreintés avec le reste du harnais, et s'exécutent dans `evaluate()` **avant**
que le jeton soit pris ; le détecteur de « trop beau pour être vrai » ne bloque
rien et voyage dans le rapport d'IC.

## Pourquoi

**Rejeter avant le jeton, et non après.** Un signal dégénéré n'a pas produit
d'IC ; l'inscrire au registre gonflerait le dénominateur avec des tests qui n'ont
jamais eu lieu, et un dénominateur faux est aussi nuisible qu'un dénominateur
absent. Le refus lève une exception, il n'écrit rien.

**Les seuils sont écrits avant d'avoir vu quoi que ce soit**, et ils portent sur
le **signal**, jamais sur son résultat. Un seuil ajusté après coup pour laisser
passer un signal qu'on aime est la forme la plus douce de la triche, et la plus
difficile à voir ensuite.

| Contrôle | Seuil | Effet |
|---|---|---|
| score constant sur une cellule | moins de 2 valeurs distinctes | cellule rejetée |
| score quasi constant | moins de 10 % de valeurs distinctes | cellule rejetée |
| trop peu d'observations | moins de 30 | cellule rejetée |
| signal exsangue | moins de 2 cellules survivantes | **signal rejeté**, rien n'est écrit |

**Une exception, et elle a été trouvée par la porte 03 qui tombait.** Le plancher
de deux cellules existe pour empêcher qu'un **diagnostic de cellule soit promu en
résultat** (`D01` §4). Une **calibration** ne promeut rien : la porte 03
reproduit à la main l'IC d'**une seule** cellule, à 1e-12, et c'est tout son
objet. Le plancher tombe donc à une cellule quand `hypothesis_ref` est `null`.
La dérogation n'achète rien à personne — une calibration ne porte pas
d'hypothèse et n'atteint jamais le dénominateur.

**« 99 % de NaN » ne se traduit pas par « 99 % de barres non scorées ».** Nos
étalons scorent **une barre par séance** sur environ 390 : 99,7 % des barres
n'ont pas de score, et c'est la forme même de l'hypothèse, pas une dégénérescence.
Ce qui compte est le nombre d'**observations** qui en résultent, pas la densité
des scores. Un contrôle écrit sans cette distinction rejetterait les deux seuls
signaux du projet (`L10` dit la même chose d'un autre angle).

**La suspicion ne bloque pas.** Un IC au-dessus de 0,10 sur cet univers est
invraisemblable — `D01` §2 fixe les cibles à 0,018 et 0,031 — mais le refuser
reviendrait à décider du résultat avant de le voir. Il est donc **calculé,
inscrit, et signalé dans le rapport**, avec la raison. Un chiffre gênant qu'on
empêche d'exister est un chiffre qu'on ne peut plus expliquer.

**Ce que ça sacrifie.** Le harnais change une deuxième fois, donc son empreinte
change et **tous les résultats antérieurs sont périmés**. Le coût est encore nul,
et c'est la dernière fois : `counted_tests()` vaut 0 aujourd'hui, et la phase 06
est précisément celle qui le fera passer à 2. Après la première mesure
d'hypothèse, ce même changement coûterait cette mesure.

## Ce que ça verrouille

- `harness/controls.py` : les seuils, et `Degenerate`, l'exception du refus.
- `harness/evaluate.py` : les contrôles avant `registry.open_test`.
- `harness/report.py` : le rapport porte ses avertissements et les imprime.
- `scripts/gate_06_controls.py` : la porte, qui soumet des signaux dégénérés
  fabriqués pour l'occasion.
- Tout signal futur, y compris ceux de l'agent de la phase 08, passe par là.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **La détection de doublons entre signaux** exige de garder les scores des signaux déjà testés. Le comparateur existe (`controls.duplicate_of`), le magasin non | phase 11, avec la taxonomie — c'est le même besoin |
| Le seuil de suspicion, 0,10, s'il se révèle trop lâche ou trop serré | à la première alerte |
| L'autocorrélation des scores comme motif de **rejet** et non d'avertissement | phase 09, quand plusieurs signaux auront été vus |
