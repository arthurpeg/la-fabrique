# D06 — Les signaux de référence, et le banc d'essai des portes 05, 06 et 08

**Date :** 2026-09-17
**Phase :** 05 (préalable)
**État :** prise

## La question

Les portes 05, 06 et 08 se démontrent toutes les trois **contre des signaux dont
on connaît déjà la réponse** : la 05 en y injectant un look-ahead qu'il faut
attraper, la 06 en les dégradant volontairement, la 08 en demandant à un agent de
les reproduire à mieux que 0,9 de corrélation. Ce banc d'essai n'existe pas :
`signals/` est vide. Sans lui, ces trois portes n'ont pas de sujet.

## Les options

1. **Aucun banc d'essai ; redéfinir les portes 05, 06 et 08 autrement.** Écartée.
   On peut tester un test de causalité sur un signal jetable, mais la porte 08 —
   « l'agent reproduit ton implémentation » — n'a alors plus de référent du tout.
   Elle deviendrait « l'agent produit du code qui tourne », ce qui ne mesure rien.

2. **Les cinq signaux du plan de montage** — momentum 12-1, book-to-price,
   low-vol, reversal, taille. Écartée : ils sont transversaux, mensuels, sur
   actions. Notre univers est de neuf futures en intraday portant 4,22 paris
   (`D01` §2, ledger F03). Les transposer n'aurait pas de sens ; les tester tels
   quels, encore moins.

3. **Deux signaux intraday tirés du corpus, codés à la main.** Retenue. Deux, pas
   cinq : ce qui est cherché est un **référent**, pas une bibliothèque, et chaque
   signal supplémentaire est une implémentation de plus à maintenir juste pour que
   trois portes aient un sujet.

## Le choix

Deux signaux de référence, écrits à la main, tirés de `corpus/AMORCE.md` — Gao et
al. (2018), entrée 1, et Baltussen et al. (2021), entrée 2 — implémentés dans
`signals/`, **avec leur hypothèse pré-enregistrée dans `hypotheses/` avant toute
mesure**, et sans qu'aucun IC ne soit calculé à ce stade.

## Pourquoi

**Ces deux-là, et pas d'autres.** Baltussen et al. portent sur **60+ futures**,
c'est-à-dire exactement notre univers et exactement notre granularité : c'est la
référence la plus proche de notre situation dans tout le corpus. Gao et al. sont
la tête de la famille — celle dont `AMORCE.md` dit qu'elle « porte presque tout ».
Les deux prédisent la **dernière demi-heure** de la séance, mais par des
prédicteurs différents : la première demi-heure pour Gao, tout le reste de la
journée pour Baltussen. Deux implémentations distinctes d'une même famille, ce
qui est précisément ce qu'il faut pour que la porte 08 mesure quelque chose.

**Écrire un signal à la main maintenant n'est pas confondre les deux ordres.**
L'étape 02 de la chaîne — le *codage automatique* d'un signal par un agent — se
construit en phase 08 et reste interdite d'ici là. Ce qui est fait ici est son
**banc d'essai**, que le plan de montage situe en amont, et sans lequel la phase
08 n'est pas jugeable. La distinction est celle-ci : ces deux signaux ne sont pas
des candidats à la production, ce sont des étalons.

**Aucun IC n'est calculé.** Les implémenter et les mesurer sont deux gestes
séparés, et seul le premier a lieu maintenant. Mesurer coûterait deux tests au
dénominateur du registre avant que les contrôles automatiques (phase 06) existent
pour les accompagner. Le banc d'essai n'en a pas besoin : la porte 05 compare des
**scores** à des scores, la porte 08 aussi.

**Ce que ça sacrifie.** Le plan de montage voulait cinq signaux et la vérification
que le harnais retrouve les faits stylisés connus. Avec deux signaux et aucune
mesure, cette vérification-là reste non faite — la porte 03 a été franchie
autrement, par calibration de construction (`D04`, complément du 2026-09-17), et
elle le reste. C'est un trou assumé, pas un trou ignoré : il se refermera à la
première mesure, en phase 06 ou 09, quand ces deux hypothèses seront testées avec
leurs contrôles.

## Ce que ça verrouille

- `signals/` : un module par signal, exposant `SIGNAL_ID`, `HYPOTHESIS`, et
  `scores(panel, cells)` rendant `{(root, window): Series}` — la forme
  qu'`evaluate()` accepte déjà. **Cette interface est provisoire** : la phase 05
  la formalise, et c'est elle qui décidera du `code_hash` propre au signal
  (`D05` § Ce qui reste ouvert).
- `hypotheses/` : un fichier par hypothèse, numéroté `H01`, `H02`, daté, écrit
  **avant** la mesure. Le champ `hypothesis_ref` du registre pointe dessus. Une
  hypothèse ajoutée ou modifiée après un résultat est une hypothèse morte
  (invariant IV).
- Les portes 05, 06 et 08 prennent ces deux signaux pour sujet.
- En changer plus tard : bon marché tant qu'aucune mesure n'a été faite sur eux,
  coûteux après — une hypothèse pré-enregistrée qu'on réécrit ne vaut plus rien.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| Le contrat définitif de la fonction de signal, et son empreinte propre | phase 05 |
| Faut-il un troisième étalon, hors famille du momentum intraday (volatilité réalisée, entrée 12) | phase 06, si les contrôles montrent que deux signaux d'une même famille ne les exercent pas assez |
| La mesure de `H01` et `H02` — les deux premiers tests comptés du projet | phase 06 ou 09, jamais avant que les contrôles automatiques existent |
