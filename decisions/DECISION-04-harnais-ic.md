# D04 — Le harnais d'IC : ce qu'il calcule, ce qu'il refuse, ce qu'il inscrit

**Date :** 2026-09-17
**Phase :** 03
**État :** prise

---

## La question

`D01` §2 fixe la métrique — IC en série temporelle, poolé, statistique robuste à
la corrélation transversale, FDR dès le premier test. Il reste à trancher ce
qu'il a délibérément laissé ouvert : quelle corrélation, sur quels horizons,
poolée comment, avec quelle statistique exactement, et que fait le harnais des
coûts dont une composante est `null`.

## Les options

**Sur la corrélation.** Pearson, écartée : sur des rendements à la minute, les
queues dominent et un seul saut de roulement mal ajusté déplacerait l'IC entier.
**Spearman de rang**, retenue : insensible aux queues, c'est la convention de la
littérature d'IC, et elle survit à une transformation monotone du score — ce qui
compte quand l'agent de la phase 08 écrira des scores d'échelles arbitraires.

**Sur le chevauchement.** Échantillonner sans recouvrement (une observation tous
les `h` minutes) donne une statistique propre mais jette `h - 1` observations sur
`h`. Retenue : **garder le recouvrement et déflater la statistique de `sqrt(h)`**
— deux observations voisines partagent `h - 1` barres, le compte effectif est
d'environ `n / h`. C'est le traitement classique des observations chevauchantes,
et ce n'est **pas** un estimateur de Newey-West : le harnais ne prétend pas en
calculer un, il applique une déflation dont la forme est dite ici.

**Sur le pooling.** Un IC par cellule puis une moyenne simple donnerait le même
poids à `6B × EUROPE` et à `NQ × US`, qui n'ont ni le même nombre d'observations
ni le même sens économique. Retenue : **moyenne pondérée par le nombre
d'observations**, la ventilation par cellule restant un diagnostic
(`D01` §4) — jamais une série de tests.

**Sur les coûts, dont les frais sont `null`.** Trois voies :

| | traiter `null` comme 0 | refuser tout chiffre net | **rendre un plancher, étiqueté** |
|---|---|---|---|
| Ce que ça produit | un IC net **faux et flatteur** | rien d'exploitable en phase 03 | un IC net **minoré**, dit comme tel |
| Ce qu'un lecteur pressé en retient | « ça passe » | — | « ça passe *au moins* ce coût-là » |
| Réversible à l'arrivée du barème | non — le chiffre a circulé | oui | oui, et le champ dit ce qui manque |

La troisième est retenue. Un coût dont une composante est inconnue n'est pas un
coût inconnu : c'est un **plancher**, utile s'il est nommé comme tel.

## Le choix

Le harnais est le paquet `harness/`. Il calcule un **IC de Spearman en série
temporelle par cellule**, poolé par pondération des observations, assorti d'un
`t` corrigé **deux fois** — du recouvrement et de la corrélation
transversale (la largeur effective, pas le nombre d'instruments). Il rend un
**rapport d'IC** qui porte les deux cibles de `D01` §2, un coût d'aller-retour
**minoré et étiqueté**, et il **écrit au registre à chaque IC produit**.

## Pourquoi

Parce que les trois façons de se mentir sur un IC sont connues d'avance, et que
chacune reçoit ici une contre-mesure mécanique plutôt qu'une consigne :

1. **Le `t` gonflé.** Neuf instruments ne portent que ~4,2 paris. Un `t` de
   Student naïf est surévalué d'un facteur proche de `sqrt(9 / 4,2) ≈ 1,46`
   (`D01` §2). Le harnais applique ce facteur ; il n'est pas laissé à la
   vigilance de qui lit le rapport.
2. **Le coût oublié.** Un IC brut qui passe le seuil et un IC net qui ne le passe
   pas sont le résultat le plus fréquent d'un projet intraday — c'est le verdict
   de Mesfin (2026), la référence la plus proche de notre situation. Le rapport
   affiche les deux, toujours, et le net porte la mention de ce qui manque.
3. **La cible flatteuse.** `D01` §2 donne deux cibles selon que les trois
   fenêtres sont indépendantes ou non : 0,018 et 0,031. Le rapport porte les
   deux ; il n'y a aucun chemin pour n'en afficher qu'une.

Ce qui est sacrifié : de la puissance statistique. Les deux corrections se
multiplient, et un signal réel mais faible sera déclaré non significatif. C'est
le sens du projet — `D01` §9, « aucune voie rapide pour une idée manifestement
bonne » — et l'erreur symétrique, un faux positif engagé en capital réel, coûte
beaucoup plus cher qu'un vrai signal manqué.

## Ce que ça verrouille

### 1. Le contrat, et ce que le harnais ignore volontairement

```python
from harness import evaluate

report = evaluate(
    scores,            # {(root, window): Series de scores indexée par horodatage}
    panel,             # un Panel ouvert à une date (phase 02)
    horizon="30min",
    hypothesis_ref="HYP-2026-09-17-a",   # écrite AVANT (invariant IV)
    stage="03-calibration",
)
```

**Le harnais ne sait pas ce qu'est un signal.** Il reçoit des scores déjà
calculés. C'est la phase 05 qui dira comment un signal les produit sans toucher
au futur ; en attendant, rien ici ne préjuge de cette interface.

### 2. Ce que le rapport contient, et qu'on ne peut pas en retirer

- l'IC poolé, son `t` corrigé, le nombre d'observations, le nombre de cellules ;
- **les deux cibles**, 0,018 et 0,031, et la distance à chacune ;
- le coût d'aller-retour par cellule, **minoré**, avec la liste explicite des
  composantes inconnues (`fee_bp` est `null` tant que le barème n'est pas
  dépouillé) ;
- la ventilation par cellule, **marquée diagnostic**, jamais un test ;
- l'empreinte du code du harnais au moment du calcul.

### 3. Les deux corrections du `t`, appliquées dans cet ordre

```
t_naïf          = IC * sqrt(n - 2) / sqrt(1 - IC²)
t_recouvrement  = t_naïf / sqrt(h)                        h = horizon en barres
t_final         = t_recouvrement / sqrt(instruments / largeur_effective)
```

À 30 minutes sur cet univers : ÷ 5,48 puis ÷ 1,46, soit **un `t` divisé par 8**
avant tout jugement.

La largeur effective vient de la mesure de la phase 01 —
`scripts/out/a5_breadth_intraday.json`, ratio de participation à 15 minutes,
**4,224** — lue dans le fichier à chaque rapport, jamais recopiée en dur.

### 4. L'invariant III prend effet maintenant, pas en phase 04

**Chaque IC calculé écrit une ligne au registre, dès aujourd'hui.** La phase 04
ne crée pas cette obligation : elle rend son contournement *impossible* et
verrouille le holdout. Distinguer les deux évite le piège que
`registry/SCHEMA.md` décrit — un compte ajouté après coup est un compte perdu.

**Conséquence sur le comptage :** toute ligne porte un `stage`. Les lignes de
`stage` commençant par `03-calibration` sont des **calibrations du harnais**, pas
des tests d'hypothèse : elles sont inscrites, et **exclues du dénominateur** de
FDR et du Sharpe dégonflé. Un test d'hypothèse porte un `hypothesis_ref`
non vide. La règle reste celle de `D01` §4 : un signal sur la grille = un test.

### 5. Ce qui est figé

À partir du franchissement de la porte 03, `harness/` est **figé et versionné**.
Il ne se modifie que par une décision écrite, et **tous les résultats antérieurs
sont alors réputés périmés** (`CLAUDE.md`). Le `code_hash` de chaque ligne du
registre est là pour rendre ce périmètre visible.

## Ce qui reste ouvert

| Point | Échéance | Statut |
|---|---|---|
| Les frais et multiplicateurs | dès leur obtention | `null` ; le coût est un plancher étiqueté jusque-là |
| Le glissement (`slippage_bp`) | avant le premier signal réel, phase 08 | hypothèse déclarée et pessimiste, à écrire |
| Le nombre et les frontières des plis du walk-forward | phase 09 | non tranché ; la calibration de la phase 03 n'en a pas besoin |
| Le seuil de FDR opérationnel | phase 09, au premier lot | la référence reste `t > 3,0` (Harvey, Liu & Zhu) |
| Les horizons retenus pour la production | phase 08 | le harnais les accepte tous ; la calibration en utilise un, 30 minutes, sur les 25 cellules |

## Condition de révision

1. **La largeur effective change** — un instrument entre ou sort de l'univers, et
   le facteur de correction transversale doit être recalculé.
2. **Les frais arrivent** — le coût cesse d'être un plancher, et les rapports
   antérieurs deviennent des minorants connus, pas des résultats.
3. **La calibration échoue à retrouver un IC vérifié indépendamment** — le
   harnais est faux, et c'est ici qu'on s'arrête, pas quatre mois plus tard.

---

## Complément du 2026-09-17 — porte franchie, et ce que la calibration a corrigé

**Porte 03 franchie**, `scripts/gate_03_harness.py`, 41 vérifications. Un score
qui **est** le rendement futur rend un IC de `1.000000000` sur les **25 cellules
retenues** (5 958 995 observations) ; une seconde implémentation des rendements
et de l'IC, écrite différemment — position par position, sans `groupby` — les
reproduit à 1e-12 ; un score indépendant du futur rend `+0,00108` et un `t` final
de `+0,06`. Le harnais est **figé** à partir d'ici : il ne change que par une
décision écrite, et tous les résultats antérieurs seraient alors périmés.

**Un chiffre trompeur a été corrigé avant le gel.** Le rapport annonçait un
« horizon réalisé p99 » de 3 960 minutes pour un horizon de 30 : il était calculé
sur tout l'index de la cellule, sauts entre séances compris — c'est-à-dire
précisément sur les paires que `forward_returns` écarte. Il est désormais mesuré
sur les seules paires qui produisent une observation, et vaut 30. Un diagnostic
calculé sur un autre support que la mesure qu'il accompagne alarme sans informer.

**Trois lignes de calibration figurent au registre** (`stage: 03-calibration`,
`hypothesis_ref: null`). Elles sont inscrites, comme l'exige l'invariant III, et
exclues du dénominateur : `counted_tests()` rend 0.

