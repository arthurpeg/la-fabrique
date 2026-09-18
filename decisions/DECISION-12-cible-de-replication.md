# D12 — La cible de la clause 2 : un résultat que notre instrument sait lire

**Date :** 2026-09-18
**Phase :** 06
**État :** prise

## La question

La clause 2 de la porte 06 demande que « le harnais réplique un résultat publié
connu, contrôles compris, sans intervention ». La cible nommée depuis la phase 01
est Mesfin (2026). Le papier a été lu le 2026-09-18, et il ne convient pas : son
critère est un `t` sur des **rendements nets par trade**, le nôtre est un **IC de
Spearman**. Une porte dont l'instrument ne sait pas lire la réponse de sa cible
ne prouve rien.

## Les options

1. **Garder Mesfin et tester ses 14 familles en IC.** Écartée. Onze de ses
   quatorze familles échouent parce que leur rendement brut (0,07 à 1,50 point)
   est **sous la friction** — une insuffisance d'amplitude, pas une absence de
   prédiction. Un IC ne la voit pas : un IC non nul est compatible avec son
   échec, un IC nul ne le confirme pas. On ne répliquerait rien, dans aucun sens.

2. **Attendre le moteur de backtest.** Écartée. Une réplication fidèle demande un
   évaluateur au niveau du trade, c'est-à-dire la phase 10. La porte 06
   attendrait la 10, ce qui inverse l'ordre de construction — le juge après
   l'accusé.

3. **Changer de cible pour un résultat exprimé en corrélation.** Retenue.

## Le choix

La clause 2 vise désormais **Heston, Korajczyk & Sadka (2010)**, *Intraday
Patterns in the Cross-section of Stock Returns*, `JF` 65(4) — corpus entrée 3,
fiche `corpus/fiches/heston-2010-intraday-periodicity.json`. Mesfin reste au
programme comme **calibrage d'attente**, lu et fiché, mais cesse d'être la cible
d'une porte.

## Pourquoi

**Sa réponse est une corrélation.** Continuation du rendement aux lags multiples
exacts d'une journée, retournement aux premiers lags, et **rien de positif entre
les multiples**. C'est l'objet même que le harnais produit.

**C'est un motif, pas une valeur — et c'est ce qui le rend transposable.** Nos
neuf futures ne sont pas leurs actions américaines, et aucune magnitude du papier
n'est reprise comme attendue. Ce qui se réplique est la **forme** : le signe aux
multiples, le signe entre les multiples, l'ordre des deux. Une forme survit à un
changement d'univers là où un point de base n'y survit pas.

**Le témoin négatif est dans la cible.** Un peigne se falsifie tout seul : si les
lags non-multiples rendaient autant que les multiples, il n'y aurait pas de
périodicité, seulement un biais. C'est exactement ce qu'une porte doit exiger, et
ce qu'un IC positif isolé ne fournit jamais.

**La période est connue d'avance et diffère par fenêtre.** Leur journée fait 13
demi-heures (09:30-16:00) ; nos fenêtres `US` et `EUROPE` font 6,5 h donc 13 elles
aussi, `ASIA` en fait 16. Trois motifs distincts à retrouver, dont les périodes
sont dictées par le catalogue et non par le résultat. Un ajustement après coup se
verrait.

**Ce qu'on sacrifie.** La cible la plus proche de notre situation. Mesfin mesure
notre instrument, notre granularité, notre pauvreté de données — et son verdict
est transportable depuis `L14`. On perd cela comme épreuve de porte, on le garde
comme attente : **le corpus implémentable doit être tenu pour attendu mort**, et
`H01` et `H02` vont déjà dans ce sens.

## Ce que ça verrouille

**Le comptage, comme `D11` l'a posé.** La réplication est **une** hypothèse —
`H03`, une conjonction sur la forme du motif — même si elle produit autant de
lignes au registre qu'il y a de lags mesurés. Ce n'est pas une recherche du
meilleur lag : c'est la vérification d'un motif prédit en entier, à l'avance.
Garde-fou écrit ici : **aucun lag ne peut être retenu comme signal** sur la foi
de cette mesure ; il faudrait une hypothèse neuve, pré-enregistrée et comptée.

**Ce que « répliquer » veut dire ici, et ne veut pas dire.** Nos données ne sont
pas les leurs et ne le seront jamais ; toute réplication de ce projet est une
**transposition**. La porte 06 demande que le harnais retrouve un motif publié
sur *nos* données, pas qu'il reproduise des nombres publiés. C'est écrit
maintenant pour qu'une session future ne croie pas la porte franchie à moitié.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Que faire si le motif n'est pas là.** Un peigne absent sur nos futures serait un résultat, pas un échec de porte — mais la porte, elle, ne serait pas franchie pour autant. Le cas est à trancher **avant** de regarder | dans `H03`, qui doit le dire |
| **Bollerslev et al. (2018)**, 50+ futures, justification directe de notre *pooling* : sa réponse porte sur la volatilité réalisée et demanderait un second instrument | phase 09 ou plus tard |
| Mesfin comme **réplication au niveau du trade**, quand le moteur existera | phase 10 |
