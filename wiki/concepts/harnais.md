---
type: concept
updated: 2026-09-17
status: stable
sources: [decisions/DECISION-04-harnais-ic.md, CLAUDE.md, decisions/DECISION-01-univers-et-donnees.md]
---

# Harnais

**Le code déterministe qui juge un signal. Une seule porte d'entrée, `evaluate`,
et elle écrit au registre avant de rendre quoi que ce soit.**

**Figé depuis le 2026-09-17** (porte 03). Il ne change que par une décision
écrite — et alors **tous les résultats antérieurs sont réputés périmés**.

## Ce que ça veut dire ici

```python
from harness import evaluate

report = evaluate(
    scores,                          # {(root, window): Series de scores}
    panel,                           # un Panel ouvert à une date
    "30min",
    signal_id="S01",
    hypothesis_ref="HYP-...",        # écrite AVANT (invariant IV)
)
```

Il **ignore volontairement ce qu'est un signal** : il reçoit des scores déjà
calculés. Comment un signal les produit sans toucher au futur est l'affaire de la
phase 05 ; rien ici ne préjuge de cette interface.

## Les trois façons de se mentir, et leur contre-mesure mécanique

| Le piège | Ce que le harnais fait, sans qu'on ait à y penser |
|---|---|
| Le `t` gonflé | déflation ÷ √h (recouvrement) puis ÷ √(9 / 4,224) (transversale) — **÷ 8 à 30 minutes** |
| Le coût oublié | rend un **plancher** et nomme ce qui manque (`fee_bp`, `slippage_bp`) |
| La cible flatteuse | affiche **les deux** cibles de `D01` §2, 0,018 et 0,031, sans chemin pour n'en montrer qu'une |

## Ce que ça ne veut pas dire

- **Ce n'est pas le Panel.** Le [[concepts/panel]] lit ; le harnais juge. Le
  Panel n'est pas figé, le harnais l'est.
- **La ventilation par cellule n'est pas une série de tests.** C'est un
  diagnostic ; une évaluation sur 25 cellules écrit **une** ligne
  ([[concepts/comptage-des-tests]]).
- **Un IC net n'est pas disponible aujourd'hui.** Le coût est minoré tant que les
  frais sont `null` : ce qu'on peut en dire est « au moins ce coût-là », donc
  « au plus cette performance ». Voir [[concepts/cout-aller-retour]].
- **Écrire au registre n'est pas la porte 04.** L'invariant III s'applique depuis
  aujourd'hui ; la phase 04 rend son **contournement impossible** et verrouille
  le holdout. Voir [[phases/phase-04-registre-et-holdout]].

## Comment il a été calibré

Porte 03, `scripts/gate_03_harness.py`, 19 vérifications : un score qui **est**
le rendement futur rend `1.000000000` sur les trois cellules de calibration ; une
seconde implémentation, écrite différemment, reproduit rendements et IC à 1e-12 ;
un score indépendant du futur rend `+0,00108` et un `t` final de `+0,06`.

## Où c'est fixé

`D04` · `harness/` · `scripts/gate_03_harness.py` · `CLAUDE.md` invariants I et III

## Voir aussi

[[concepts/ic]] · [[concepts/registre]] · [[concepts/comptage-des-tests]] ·
[[concepts/panel]] · [[phases/phase-03-harnais-ic]]
