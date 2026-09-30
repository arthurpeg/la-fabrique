# D35 — Le harnais du lot : frais en deux bornes, glissement en grille, IC par année, `extra` fermé

**Date :** 2026-09-30
**Phase :** 09
**État :** proposée — prise quand l'opérateur applique le patch (voir § Comment l'appliquer). Tranche ce que `D26`, `D28` et `D29` renvoyaient à **une seule** modification du harnais.

## La question

Trois décisions ont chacune reconnu un changement nécessaire du harnais figé, et
chacune l'a renvoyé à une décision commune pour ne périmer le registre **qu'une
fois** :

- `D26` : le harnais ne sait pas ajouter les frais au coût, et `slippage_bp` est
  toujours « inconnu » ;
- `D28` : `registry.settle()` applique `extra` après les champs du ticket, et un
  appelant pourrait écraser `hypothesis_ref` ;
- `D29` : le rapport d'IC ne dit pas si un signal tient sur toute la période ou
  sur une seule.

Tout doit être fait **avant** la première mesure du lot `LOT-09` : une mesure
faite avant serait périmée par la modification, et `D28` interdit de la refaire.

## Les options

**Frais.**
1. Une valeur unique déposée au catalogue. Écartée par `D26` : la somme n'est la
   citation d'aucun tiers, et ce serait une borne présentée comme la valeur.
2. **Deux bornes, calculées par le harnais à partir de trois composantes
   citées.** Retenue (choix de l'opérateur, 2026-09-30).

**Glissement.**
1. Une valeur unique déclarée pessimiste (`D01` §7). Écartée : un seul chiffre
   cache la sensibilité du coût à cette hypothèse, qui n'est pas une mesure.
2. **Une grille de 1 à 5 ticks par side, toutes affichées.** Retenue (choix de
   l'opérateur, 2026-09-30) : on voit comment le coût bouge, et rien ne choisit
   un point de la grille à la place du lecteur.

**Diagnostic de stabilité.**
1. Des plis de walk-forward. Écartés par `D29` : rien n'est ajusté sur le `pool`.
2. **L'IC poolé par année civile**, en diagnostic. Retenu (choix de l'opérateur,
   2026-09-30).

**Trou d'`extra`.**
1. Appliquer `extra` avant les champs du ticket. Écartée : un écrasement
   silencieux reste un écrasement.
2. **Refuser toute clé d'`extra` qui recouvre un champ du ticket.** Retenue : la
   faute casse au lieu de passer.

## Le choix

**1. Les frais, en deux bornes** (`harness/costs.py`). Le catalogue porte, par
instrument, trois composantes externes en USD par contrat et **par side**, chacune
avec sa provenance (`D09`) : `fee_broker_usd` (le barème Lucid),
`fee_exchange_usd` (le CME, négociation et compensation) et `fee_regulatory_usd`
(la NFA). Elles remplacent `fee_per_contract_usd`.

| Borne | Composantes |
|---|---|
| basse | courtier seul — comme si le barème était tout compris |
| haute | courtier + bourse + régulateur — comme si rien n'était compris |

Le harnais fait la somme ; **le catalogue ne porte jamais la somme**. Une
composante `null` laisse sa borne non chiffrée, et le rapport la nomme
(`fee_bp` ou `fee_high_bp`), jamais comme un zéro.

**Les composantes restent `null` pour l'instant**, et `todo fees` reste ouvert.
Les frais CME changent le 2026-10-01 (`D26` § Ce qui reste ouvert) : ils seront
relevés après, avec leurs citations, et déposés au catalogue. **Déposer une valeur
ne change pas l'empreinte du harnais** : `code_hash` ne lit que `harness/*.py`.

**2. Le glissement, en grille** : `SLIPPAGE_TICKS = (1, 2, 3, 4, 5)` ticks **par
side**, en plus du plancher d'écart. Aller-retour :

    coût(k, borne) = plancher_d_écart + 2 × k × tick_bp + frais(borne)

Le rapport affiche les dix cases (5 glissements × 2 bornes), chacune en moyenne
pondérée par les observations (le pari moyen) et pour la pire cellule.

**3. Le prix de référence.** Frais et glissement sont convertis en bp au **prix
brut médian de la cellule sur l'échantillon évalué**. C'est la référence qu'a
employée `scripts/session_grid.py` pour le plancher, qui n'a pas changé.

**4. L'IC par année civile** (UTC) : même IC de Spearman, même pondération par les
observations, restreint à chaque année ; une cellule-année de moins de 30
observations est omise. Il est **écrit sur la ligne poolée du registre**
(`ic_by_year`, `registry/SCHEMA.md`), pour qu'aucun IC n'existe hors du registre
(invariant III), et affiché comme **diagnostic, jamais comme un test**.

**5. `extra` fermé** : `settle()` lève `RegistryBypass` si une clé d'`extra`
recouvre un champ du ticket, et n'écrit rien.

**6. `HARNAIS_DU_LOT = "4806666dc55c46c9"`** dans `scripts/measure_lot.py` :
l'empreinte du harnais ainsi modifié, avec laquelle le lot sera mesuré.

## Pourquoi

**Une seule péremption.** Chaque changement du harnais périme tout ce qui a été
mesuré avant (`D05`, `D10`). Grouper les quatre changements, c'est payer une fois.
Et les faire avant le lot, c'est ne rien perdre du lot.

**Aucun de ces changements ne modifie un IC.** L'IC est brut : les frais et le
glissement ne touchent que la section coût du rapport ; `ic_by_year` est un
découpage de ce qui était déjà calculé ; la garde d'`extra` n'agit que sur un
appel fautif, qu'aucun appelant du dépôt ne fait. La porte 03, relancée sur le
harnais modifié, le vérifie : IC du signal parfait à 1, du bruit à +0,001, les
deux déflations inchangées (§ Journal).

**Deux bornes et une grille plutôt que deux chiffres.** Le coût d'un aller-retour
est ce qui décidera si un signal est exploitable. Le présenter comme une plage,
dont on voit la sensibilité, est la direction d'erreur voulue par `D04` : un
lecteur qui ne voit qu'un chiffre le croit.

**Ce qui est sacrifié.** Les 56 tests comptés, les calibrations des portes 03, 04
et 06, et les deux mesures H01/H02 et H03 sont **périmés** : ils restent au
registre et au dénominateur de la phase 15, mais aucune conclusion ne peut plus
s'appuyer sur eux sans remesure. Tant que les frais sont `null`, le coût reste un
plancher, étiqueté comme tel ; la grille de glissement, elle, est complète dès
maintenant.

## Ce que ça verrouille

- `harness/costs.py`, `harness/metric.py`, `harness/evaluate.py`,
  `harness/report.py`, `harness/registry.py` — empreinte `9ac3e45ed8413e13` →
  `4806666dc55c46c9` ;
- `panel/catalogue.py`, `catalogue/catalogue.yaml`, `catalogue/validate.py`,
  `scripts/check_provenance.py` — les trois composantes de frais ;
- `registry/SCHEMA.md` — le champ `ic_by_year` ;
- `scripts/gate_03_harness.py` — les vérifications de la grille, de `ic_by_year`
  et du refus d'`extra` ;
- `scripts/measure_lot.py` — `HARNAIS_DU_LOT`.

**Toute modification ultérieure du harnais avant la mesure du lot** exigera une
nouvelle décision et une nouvelle valeur de `HARNAIS_DU_LOT`. Après la mesure,
elle périmerait le lot.

## Comment l'appliquer

Le harnais est protégé : **aucun agent n'y écrit** (invariant I). La modification a
été préparée et testée dans une copie isolée du dépôt, puis livrée en patch :
`decisions/DECISION-35-harnais.patch`. L'opérateur la relit, puis :

    git apply --check decisions/DECISION-35-harnais.patch
    git apply decisions/DECISION-35-harnais.patch
    uv run python scripts/gate_03_harness.py

La porte 03 doit rendre `FRANCHIE` avec l'empreinte `4806666dc55c46c9`. Puis
commiter, et passer l'état de cette décision à « prise ».

## Ce qui reste ouvert

- **Les valeurs des frais** : relever Lucid, CME (après le 2026-10-01) et NFA avec
  leurs citations, et les déposer au catalogue. Aucune empreinte ne change.
- **La taille de contrat** : les bornes sont calculées sur les contrats pleins
  (ceux de nos données). Les micros coûtent proportionnellement plus en bp
  (`scripts/fee_bracket.py`) ; à trancher avant la phase 10, quand la taille
  d'exécution sera connue.
- **La période d'échantillon des papiers**, que `D29` renvoie à avant la lecture
  des résultats du lot, n'est pas traitée ici.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-09-30 | patch préparé et testé dans une copie isolée | porte 03 FRANCHIE sur le harnais modifié, 50 vérifications, empreinte `4806666dc55c46c9` ; signal parfait IC 1,000000000 sur 25 cellules ; bruit IC +0,00108, t final +0,06 ; grille de coût NQ×US de 1,72 bp (1 tick) à 5,43 bp (5 ticks), frais manquants nommés |
| 2026-09-30 | toutes les portes relancées sur la copie modifiée | 01 PASSED, 02 FRANCHIE (103), 04 FRANCHIE (6 343 ; 169 lignes antérieures périmées, comme prévu), 05 FRANCHIE (32), 06 FRANCHIE (25), 08 FRANCHIE, 09 `--check` 21/21, `check_signals` 261, `score_signal --check` 27/27, catalogue et provenance valides. Porte 07 non franchie **dans la copie seulement** : `corpus/pdf/` n'y est pas (ignoré par git), donc F4 échoue sur 17 fiches ; franchie sur le dépôt. Patch appliqué sur une copie neuve : empreinte `4806666dc55c46c9`, identique |
