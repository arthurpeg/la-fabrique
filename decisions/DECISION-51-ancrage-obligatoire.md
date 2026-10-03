# D51 — Tout score se pose à l'ancre de `_common.run`

**Date :** 2026-10-03
**Phase :** 09
**État :** prise — demande de l'opérateur (« rends l'ancrage par _common.run
obligatoire dans la consigne ») ; modifie l'outillage de `D23`/`D34`, ne
touche ni au harnais ni au registre

## La question

La consigne de codage disait de `_common.run` : « Tu n'es pas obligé de t'en
servir. » Le 2026-10-03, deux codages d'une même fiche ont concordé à
ρ ≈ 1,000 sur leurs instants communs, et ont été déclarés DISCORDANTS parce
que l'un notait une barre par séance et l'autre chaque minute (andersen-1997,
couverture 0,002). Faut-il imposer l'instant où un score se pose ?

## Les options

1. **Laisser libre.** Le désaccord sur l'instant continue de faire échouer
   des codages qui lisent le papier de la même façon.
2. **Baisser le seuil de couverture de `D34`.** C'est changer la règle après
   avoir vu les échecs (`L28`). Écartée.
3. **Imposer l'ancrage dans la consigne, et le vérifier sur les données.**
   Chaque score rendu doit tomber à une ancre de `_common.run` : une barre
   par séance et par cellule, à `horizon_bars` de la clôture de la fenêtre.

## Le choix

L'option 3. La consigne rend l'ancrage obligatoire.
`code_signal.py --judge` passe `--ancrage` au juge, et tout score posé
ailleurs casse `S1` (le contrat).

## Pourquoi

C'est l'instant que la mesure utilise : `measure_lot.py` appelle le signal à
l'horizon de son hypothèse, et le harnais mesure le rendement à venir depuis
l'instant du score. Un score posé à une autre barre est soit jeté, soit
mesuré à un horizon que personne n'a déclaré. L'ancre se lit sur l'horloge
du catalogue : c'est aussi ce qui rend le signal exécutable en séance
(`F21`).

La vérification se fait sur les données, pas sur la relecture du code
(`F19`). Le juge calcule les ancres avec `_common.run` et un prédicteur
trivial, et exige que l'index de chaque série en soit un sous-ensemble. Un
signal peut donc refuser des séances, mais il ne peut pas poser son score
ailleurs.

**Mesuré avant d'imposer** : 11 des 12 modules produits respectent déjà
l'ancrage. Le seul qui ne le respecte pas est le témoin d'andersen-1997, avec
6 328 721 scores hors ancre sur 6 344 365.

**Ce que ça ne règle pas, et il faut le dire.** Les autres échecs de
couverture de la journée ne viennent pas de l'instant :
- bitcoin-is-not-the-new-gold : un codeur se limite à ES, GC et CL, l'autre
  note toutes les cellules ;
- bollerslev-2018 : un codeur attend un an d'historique avant son premier
  score, l'autre non.

C'est un désaccord sur les **cellules** et les **séances**. `D51` ne
l'impose pas : c'est le papier, via la recette, qui doit trancher.

**Ce qui est sacrifié.** Un papier qui décide à heure fixe, par exemple
Boyarchenko à 16:15 ET, ne pose plus son score à cette heure : son
prédicteur la **lit** dans les clôtures de la séance, et le score tombe à
l'ancre. Un signal à l'ancre unique ne peut pas non plus produire plusieurs
décisions par séance. Si un papier l'exige un jour, il faudra une décision
qui élargit l'ancre, pas une exception silencieuse.

## Ce que ça verrouille

- `scripts/score_signal.py` : `hors_ancrage`, option `--ancrage`, dans `S1` ;
- `scripts/code_signal.py` : texte de la consigne, et `--judge` qui passe
  `--ancrage`.

**Signaux déjà produits.** Leurs jugements inscrits restent valides, et `S6`
interdit de les retoucher. La porte 08 ne passe pas `--ancrage` : elle juge
chaque signal selon la règle de son époque. Un rejugement par
`code_signal.py --judge` leur appliquerait `D51`.

## Ce qui reste ouvert

- Le désaccord sur les cellules et les séances (voir plus haut).
- L'option (a), (b) ou (c) pour les fiches sans signal de rendement
  (`F62`).

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-03 | décision prise et appliquée | `score_signal --check` 27/27 ; jugé sans inscription avec `--ancrage` : témoin andersen refusé `S1` (25 cellules, 277 223 scores sur 277 855 hors ancre en 6A×ASIA), principal andersen et baltussen verts ; registre 187 → 187 |
