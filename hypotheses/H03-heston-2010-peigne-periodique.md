# H03 — Le peigne : continuation aux multiples exacts d'une séance

**Écrite le :** 2026-09-18, **avant toute mesure sur nos données**
**Signal :** `heston-2010-periodicity` — à implémenter, `signals/` ne le porte pas
encore
**Origine :** Heston, Korajczyk & Sadka (2010), « Intraday Patterns in the
Cross-section of Stock Returns », *JF* 65(4):1369-1407 — `corpus/AMORCE.md`
entrée 3, fiche `corpus/fiches/heston-2010-intraday-periodicity.json`
**Rôle :** cible de la **clause 2 de la porte 06** (`D12`)
**Statut :** **testée le 2026-09-18** — voir « Le résultat » en fin de fichier.
L'affirmation ci-dessous n'a pas été touchée d'un mot depuis sa rédaction.

## Ce qui est affirmé

Sur une cellule donnée, le rendement d'un intervalle de demi-heure est
**positivement** lié à son propre rendement **`m` séances plus tôt, au même
intervalle de la fenêtre** — et il ne l'est **pas** aux décalages qui ne tombent
pas sur un multiple de séance.

C'est un **motif de signes**, et c'est ce motif qui est affirmé, en trois clauses
qui valent ensemble :

| | Clause | Prédiction |
|---|---|---|
| **A — les dents** | IC aux décalages de `m` séances, même intervalle, `m = 1…40` | **positif** |
| **B — les creux** | IC aux décalages de `j` intervalles à l'intérieur d'une séance, `j = 1…P−1` | **négatif ou nul**, et dans tous les cas **inférieur** aux dents |
| **C — le retournement court** | IC aux décalages `j = 1, 2, 3` | **négatif** |

`P` est le nombre de demi-heures de la fenêtre, **dicté par le catalogue et non
par le résultat** : `US` 09:30→16:00 et `EUROPE` 03:00→09:30 font 6,5 h, donc
**P = 13** ; `ASIA` 19:00→03:00 fait 8 h, donc **P = 16**. Le peigne a donc
**deux périodes différentes** selon la fenêtre, et c'est une contrainte, pas une
liberté : un ajustement de `P` après coup se verrait immédiatement.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3).

  > **Précision du 2026-09-18, écrite à l'implémentation et avant le lancement de
  > la mesure.** La première rédaction prévoyait de mesurer séparément les
  > fenêtres de période 13 et celle de période 16, pour que le *pooling* ne
  > mélange pas une dent et un creux. Le signal est finalement paramétré **en
  > séances** (`lag_sessions`) et non en intervalles : le décalage en intervalles
  > est alors calculé par fenêtre depuis le catalogue, de sorte qu'une dent est
  > une dent dans les trois fenêtres à la fois. La séparation devient inutile, et
  > les 25 cellules se poolent sans mélange. Les creux, eux, se comptent en
  > intervalles (`j = 1…12`), valeurs qui ne sont multiples ni de 13 ni de 16.
  > Aucun résultat n'avait été vu quand ceci a été écrit.
- **Grandeur :** rendement de demi-heure, à l'intérieur de la fenêtre et de la
  séance.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Décalages mesurés :** `m = 1…40` séances (clause A) et `j = 1…P−1`
  intervalles (clauses B et C).

## Ce qui est attendu, en chiffres

**Aucune magnitude n'est prédite, et c'est délibéré.** Le papier mesure une
réponse **transversale** en points de base, dont l'effet de marché est retiré ; il
écrit lui-même que « using cross-sectional regression in this way is different
from measuring the autocorrelation of stock returns ». Nous mesurons une
corrélation de rang **en série temporelle par cellule**, sur neuf futures et non
sur des milliers d'actions. Reprendre son `t` minimal de 9,62 comme attente
serait une faute de transposition.

Ce qui est prédit est donc l'**ordre**, pas la valeur :

```
IC(dents)  >  IC(creux)        et      IC(dents) > 0      et      IC(j=1,2,3) < 0
```

## Ce qui la contredirait

- **Pas de séparation.** `IC(dents) ≤ IC(creux)` : il n'y a pas de périodicité, et
  la clause A ne dit rien de plus que la clause B.
- **Des dents négatives.** `IC(dents) < 0` avec un `t` final au-delà de 2 : le
  motif existe à l'envers.
- **Un peigne à la mauvaise période.** Un motif présent mais dont les pics ne
  tombent pas sur `P` : ce ne serait pas le résultat de Heston et al., ce serait
  autre chose — à ne pas rebaptiser.
- **Un peigne porté par une seule cellule** sur les 25 : accident d'instrument,
  pas périodicité (même clause que `H01`, et voir
  `wiki/concepts/comptage-des-tests` sur le coût de la sélection).
- **Aucun retournement court** : la clause C tombe et, avec elle, la moitié du
  motif que le papier décrit.

## Si le motif n'est pas là — écrit avant de regarder

`D12` § Ce qui reste ouvert l'exige, et la réponse est écrite ici pour qu'elle ne
soit pas arrangée après coup.

L'absence du peigne sur nos futures serait **un résultat valide sur notre
univers** — et une information utile, puisque le motif est réputé robuste. Mais
**la clause 2 ne serait pas franchie pour autant** : elle demande que le harnais
retrouve un résultat publié connu, et un instrument qui ne retrouve pas ce qu'il
devrait retrouver n'est pas validé contre une vérité extérieure. Il faudrait
alors une **nouvelle cible**, par décision écrite — pas un assouplissement de
celle-ci.

Dit autrement : cette hypothèse peut échouer **sans que personne ait mal
travaillé**, et son échec ne s'achète pas en redéfinissant la porte.

## Comptage

**`H03` est UNE hypothèse**, quelle que soit le nombre de lignes qu'elle écrit au
registre — environ une centaine, une par décalage mesuré et par groupe de
période. Ce n'est pas une recherche du meilleur décalage : c'est la vérification
d'un motif **prédit en entier avant d'être vu**. `D11` § Ce que ça verrouille et
`D12` § Ce que ça verrouille posent la règle que la phase 15 devra suivre :
**on compte des hypothèses éprouvées, pas des lignes écrites**.

**Garde-fou, écrit d'avance.** Aucun décalage ne peut être retenu comme signal
sur la foi de cette mesure, même s'il ressort nettement. Le retenir exigerait une
hypothèse neuve, pré-enregistrée, et comptée en plus.

## Ce qui n'est pas affirmé ici

Le papier propose aussi des variations **conditionnelles** — heure de la journée,
taille, volume, écart. Elles appartiennent aux régimes (phase 13) et devront être
pré-enregistrées séparément. Les tester en même temps que celle-ci et retenir la
meilleure serait exactement ce que le registre existe pour rendre visible.

---

## Le résultat

**Mesuré le 2026-09-18**, 52 décalages, tranche `pool`, as-of 2023-12-29, 25
cellules, ~630 000 à 657 000 observations par décalage, harnais `9ac3e45e`.
Recopié des rapports d'IC officiels ; le registre fait foi. `counted_tests()`
passe de 4 à **56**, pour **une** hypothèse.

### Ce que les trois clauses rendent

| Clause | Médiane | Détail |
|---|---|---|
| **A** — dents `m = 1…40` | **+0,00065** | 28/40 positifs |
| **B** — creux `j = 1…12` | **−0,00112** | 7/12 négatifs |
| **C** — court `j = 1, 2, 3` | **−0,00815** | 3/3 négatifs |

### Clause C — confirmée, et c'est le seul effet net de la mesure

| | IC | `t` final |
|---|---|---|
| `j = 1` | **−0,01150** | **−6,14** |
| `j = 2` | −0,00815 | −4,35 |
| `j = 3` | −0,00248 | −1,33 |
| `j = 4` | −0,00811 | −4,33 |

Le retournement de court terme existe sur nos futures, et fortement. C'est ce que
le papier décrit avant le peigne — rebond entre bid et ask, dislocations
temporaires de liquidité.

### Clauses A et B — non établies, et le seau B était mal construit

**La faute est dans cette hypothèse, pas dans la mesure.** `H03` définit les
creux comme `j = 1…12` et le retournement court comme `j = 1…3` : le second est
un **sous-ensemble** du premier. La séparation « dents > creux » pouvait donc
être produite par le retournement court seul, sans aucune périodicité. Elle l'a
été :

| | médiane des dents | médiane des creux | séparation | Mann-Whitney |
|---|---|---|---|---|
| creux tels qu'écrits, `j = 1…12` | +0,00065 | −0,00112 | +0,00177 | p = 0,030 |
| creux **sans** le court, `j = 4…12` | +0,00065 | **+0,00056** | **+0,00009** | **p = 0,247** |

Retirer du seau B ce qui appartenait au seau C fait disparaître la séparation.

**Et aucune dent ne ressort de la sélection.** Le plus grand `t` des 40 vaut
**+3,01** (`m = 5`) ; le maximum de `|t|` sur 40 tirages de bruit pur a une
médiane de **2,38** et un 95ᵉ centile de **3,22**. La meilleure dent est donc
*en dessous* de ce que la sélection produit seule. Le 28/40 de dents positives
donne un binomial unilatéral de 0,0083, mais les 40 dents partagent les mêmes
barres : le compte effectif est très inférieur à 40, et ce `p` est un plancher
optimiste, pas un résultat.

**Enfin, la moitié négative de la claim tombe aussi.** Le papier dit qu'entre les
multiples la réponse reste « largement négative ». Chez nous, `j = 4…12` donne
**5 valeurs positives sur 9**.

### Le verdict, selon ce qui était écrit avant

**Le peigne n'est pas là.** Ce qui est là est un retournement de court terme,
c'est-à-dire la préface du motif et non le motif.

`H03` § « Si le motif n'est pas là » l'avait prévu et la réponse ne se négocie
pas : c'est **un résultat valide sur notre univers**, et **la clause 2 de la
porte 06 n'est PAS franchie**. Un instrument qui ne retrouve pas ce qu'il devrait
retrouver n'est pas validé contre une vérité extérieure. Il faut une **nouvelle
cible, par décision écrite** — pas un assouplissement de celle-ci, et surtout pas
une relecture indulgente de la clause B.

### Ce que cette mesure n'a PAS vérifié

`H03` § Ce qui la contredirait prévoyait aussi : « un peigne porté par une seule
cellule sur les 25 : accident d'instrument ». **Cette clause n'a pas pu être
vérifiée.** `scripts/measure_h03.py` n'a inscrit que l'IC poolé par décalage ;
la ventilation par cellule, produite par le harnais, n'a pas été conservée. C'est
un défaut du script, pas du harnais.

La vérifier coûterait **52 lignes comptées de plus**, et elle ne pourrait que
rendre le motif **plus faible** — jamais plus fort. Le verdict ne changerait donc
pas. Le défaut est noté ici plutôt que payé.

### Garde-fou, rappelé

Aucun décalage n'est retenu comme signal. `j = 1` et `j = 2` sont des
retournements nets, et ce ne sont **pas** des signaux tant qu'une hypothèse neuve
ne les a pas pré-enregistrés, avec un coût d'aller-retour en face : notre
plancher est de 0,21 à 1,55 bp, et `|IC| = 0,0115` sur une demi-heure ne dit rien
d'un rendement net.
