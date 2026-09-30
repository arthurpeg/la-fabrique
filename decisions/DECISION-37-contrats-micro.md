# D37 — On exécute en micro, sauf les devises

**Date :** 2026-09-30
**Phase :** 09
**État :** prise le 2026-09-30 — patch appliqué par un agent **sur instruction explicite de l'opérateur** (« oui, applique-la »), qui lève pour ce seul geste la règle de l'invariant I. Tranche la taille de contrat que `D35` § Ce qui reste ouvert laissait ouverte.

## La question

`D35` calcule les frais en bp sur les contrats **pleins**, ceux de nos données.
Mais les frais d'un aller-retour dépendent du contrat **exécuté** : un micro vaut
un dixième du plein (`D26`, vérifié sur les fiches CME), et ses frais par
contrat ne sont pas dix fois plus petits. Quel contrat l'opérateur exécute-t-il,
et comment le harnais le sait-il ?

## Les options

1. **Plein format partout.** Écartée : ce n'est pas ce que l'opérateur fera.
2. **Micro partout.** Impossible : le barème Lucid n'a **pas de micro devises**
   (`D26`, relevé du 2026-09-24) — 6E, 6B, 6J, 6A ne se traitent qu'en plein
   format.
3. **Micro partout où Lucid en propose, plein format pour les devises.**
   Retenue (choix de l'opérateur, 2026-09-30).
4. **Retirer les devises de l'univers exécutable**, ou **supposer les micros
   devises du CME**. Écartées par l'opérateur.

## Le choix

| Instrument | Contrat exécuté |
|---|---|
| NQ, ES, YM | MNQ, MES, MYM |
| GC, CL | MGC, MCL |
| 6E, 6B, 6J, 6A | plein format (pas de micro chez Lucid) |

Le catalogue porte, par instrument, `execution_contract` (une valeur **décidée**
ici) et `execution_multiplier` (une valeur **externe**, `D09`). Les trois
composantes de frais de `D35` sont celles **du contrat exécuté**. Le harnais
convertit les frais en bp au multiplicateur de ce contrat
(`Instrument.fee_multiplier`) : celui du micro s'il y en a un, celui de
l'instrument pour un contrat plein format.

**Les multiplicateurs des micros restent `null`** (todo `micro-multipliers`).
`D26` a lu les fiches CME et constaté le rapport d'un dixième, mais sans en
recopier les citations mot pour mot ; ils seront relevés avec leur provenance,
comme les frais, puis déposés. Tant qu'ils manquent, le rapport d'IC nomme
`execution_multiplier` parmi les composantes manquantes, jamais comme un zéro.
**Les déposer ne change pas l'empreinte du harnais.**

**Ce qui ne change pas** : le plancher d'écart et le glissement se comptent en
ticks de prix, et le tick d'un micro est celui du plein (MNQ 0,25 comme NQ). Seuls
les frais en bp dépendent de la taille.

## Pourquoi

**Parce que c'est ce qui sera exécuté**, et qu'un coût calculé sur un autre
contrat serait faux dans le sens flatteur. À titre d'ordre de grandeur, avec le
barème Lucid seul : 0,50 $ par side sur MNQ (notionnel 2 $ × l'indice) contre
1,75 $ sur NQ (20 $ × l'indice), soit des frais environ **2,9 fois plus lourds
en bp** sur le micro (`scripts/fee_bracket.py`).

**Ce qui est sacrifié.** Une modification de plus du harnais, faite **avant** la
mesure du lot, donc sans rien périmer du lot ; seules les lignes de calibration
écrites sous `4806666dc55c46c9` (portes 03 et 04 du 2026-09-30) passent
périmées. Et le coût reste un plancher tant que frais et multiplicateurs micro
ne sont pas relevés.

## Ce que ça verrouille

- `harness/costs.py` — empreinte `4806666dc55c46c9` → `94b495fa7525d3b8` ;
- `panel/catalogue.py` (`execution_contract`, `execution_multiplier`,
  `fee_multiplier`, todo `micro-multipliers`), `catalogue/catalogue.yaml`,
  `catalogue/validate.py`, `scripts/check_provenance.py` ;
- `scripts/gate_03_harness.py` — les frais d'une devise se rapportent au
  multiplicateur de l'instrument ; un multiplicateur micro manquant est nommé ;
- `scripts/measure_lot.py` — `HARNAIS_DU_LOT = "94b495fa7525d3b8"`.

Patch : `decisions/DECISION-37-contrats-micro.patch`.

## Ce qui reste ouvert

- **Relever** les frais de Lucid (micros et devises), du CME (après le
  2026-10-01) et de la NFA, et les multiplicateurs des cinq micros, avec leurs
  citations — puis les déposer. Aucune empreinte ne change.
- **Si Lucid ajoute des micros devises**, `execution_contract` des devises se
  révise par une décision, sans toucher au harnais.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-09-30 | patch préparé dans une copie isolée, puis appliqué au dépôt | empreinte `94b495fa7525d3b8` ; porte 03 FRANCHIE (52), 04 FRANCHIE (6 640), 06 FRANCHIE (25) ; catalogue et provenance valides ; todo `micro-multipliers` ouvert sur NQ, ES, YM, GC, CL ; registre 176 → 181 (calibrations seulement), 56 tests comptés |
