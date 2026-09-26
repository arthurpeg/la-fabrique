# D28 — Aucune ligne du registre ne touche le lot hors de sa mesure officielle

**Date :** 2026-09-26
**Phase :** 09
**État :** prise — complète `D25` (le budget) et `scripts/gate_09.py` (son juge)

## La question

Une mesure faite avec `hypothesis_ref = None` est une calibration :
`counted_tests()` l'ignore, et `gate_09.py` ne cherche que les lignes portant la
`ref` d'une hypothèse du lot. Peut-on regarder le résultat d'un signal avant sa
mesure officielle sans que personne ne le compte ?

## Le fait

**Oui, et sans rien forcer.** `evaluate(scores, panel, horizon, signal_id=...)`
sans `hypothesis_ref` passe par le chemin officiel, écrit sa ligne au registre —
l'invariant III est tenu — et rend l'IC. Mais la ligne est une calibration :
elle n'entre pas dans le dénominateur de `D25`, et la porte 09 ne la voyait pas.
Mesurer ainsi les 50 signaux, garder ceux qui plaisent et ne déclarer qu'eux
dans `hypotheses/LOT-09.json` aurait franchi la porte avec un `BH` calculé sur
un lot qui n'était plus aveugle. L'invariant IV (hypothèse écrite **avant** le
résultat) aurait été contourné sans qu'aucune ligne ne mente.

**Un second chemin, dans le harnais.** `registry.settle()` applique l'argument
`extra` **après** les champs du ticket (`record.update(extra)`) : un appelant de
`record_pooled(..., extra={"hypothesis_ref": None})` écrase la `ref` que le
ticket avait fixée d'avance. Personne ne le fait dans ce dépôt — `evaluate` ne
passe que `asof` et `cells` — mais rien ne l'empêche.

## Les options

1. **Durcir la porte 09.** Retenue. Toute ligne du registre qui porte le
   `signal_id` d'un signal du lot, ou la `ref` d'une de ses hypothèses, doit
   être **la** mesure officielle d'une entrée du lot (`ref` et `signal_id`
   concordants, `stage` = `09-passage`, harnais courant). Sinon, la porte refuse
   le verdict et nomme la ligne. Dans `scripts/`, hors du harnais : **aucune
   empreinte ne change, aucune ligne n'est périmée**.
2. **Compter les calibrations dans le dénominateur.** Écartée : les calibrations
   de `gate_03`, `gate_04` et `gate_06` (113 lignes au 2026-09-26) ne portent
   aucune hypothèse, et les compter gonflerait le dénominateur de la phase 15
   pour rien. Le défaut n'est pas qu'on ignore les calibrations, c'est qu'on ne
   vérifiait pas qu'un signal du lot n'en était pas une.
3. **Interdire `hypothesis_ref = None` hors d'une liste de `signal_id` de
   calibration.** Écartée pour l'instant : c'est une modification du harnais
   (`harness/controls.py` et `registry.py`), donc une décision qui périme les
   56 tests comptés. Elle se groupe avec la suivante (§ Ce qui reste ouvert).

## Le choix

`scripts/gate_09.py` refuse tout lot dont un signal ou une hypothèse a, au
registre, une autre ligne que sa mesure officielle — calibration, autre `stage`,
harnais périmé, `ref` ou `signal_id` discordants, avant ou après la clôture.

## Pourquoi

Le lot de `D25` vaut par une seule propriété : il est **clos avant la première
mesure**. Une ligne antérieure sur un de ses signaux le rend non aveugle, quelle
que soit l'étiquette qu'elle porte. La porte vérifiait la forme du lot et le
nombre de mesures par hypothèse ; elle ne vérifiait pas qu'aucun regard n'avait
précédé. C'est `L22` : une condition qu'on ne peut pas mesurer n'est pas tenue,
elle est absente.

**Ce qui est sacrifié.** Un signal **déjà mesuré** ne peut plus entrer dans un
lot. C'est voulu. Les deux étalons `H01` et `H02` (`gao-2018-intraday-momentum`,
`baltussen-2021-intraday-momentum`) ont des lignes au registre : ils ne peuvent
pas être rejoués dans le lot de la phase 09. Le signal produit de la porte 08
(`baltussen-2021-hedging-demand-intraday-momentum`) n'en a aucune, et le peut.

## Ce que ça verrouille

- `scripts/gate_09.py` : cinquième vérification (`lignes_hors_protocole`),
  auto-testée par `--check` — six fraudes fabriquées refusées, un registre
  propre accepté. **19 vérifications** au lieu de 12.
- Toute mesure exploratoire d'un signal candidat au lot, même « pour voir », le
  **disqualifie** du lot. À dire au codeur et à toute session de la phase 09.

## Ce qui reste ouvert

- **Le trou de `settle()` n'est pas fermé.** Une ligne dont `signal_id` **et**
  `hypothesis_ref` auraient été écrasés par `extra` échappe à la porte 09 comme
  au décompte. La réparation est dans le harnais : appliquer `extra` **avant**
  les champs du ticket, ou refuser toute clé d'`extra` qui en recouvre un. Elle
  périme les tests comptés ; `D26` annonce déjà **une** décision qui touchera le
  harnais (lire les frais et `slippage_bp`) et périmera les 56 tests une seule
  fois. **Les deux réparations doivent passer dans cette même décision**, pour
  ne payer la péremption qu'une fois.
- **Le dénominateur de la phase 15** (`counted_tests()`) reste aveugle aux
  calibrations portant un vrai signal hors lot. La porte 09 protège le lot ; la
  phase 15 devra se poser la même question pour le registre entier.

## Journal

- **2026-09-26** — décision prise et appliquée. `gate_09.py --check` : 19
  vérifications, 0 échec. Branchement vérifié hors dépôt, sur un lot et un
  registre fabriqués en mémoire : registre propre → FRANCHIE ; même registre
  plus une calibration du signal du lot → NON FRANCHIE, ligne nommée. Registre
  réel 169 → 169.
