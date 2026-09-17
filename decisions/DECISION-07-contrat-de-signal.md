# D07 — Le contrat de signal, la sandbox, et le test de causalité

**Date :** 2026-09-17
**Phase :** 05
**État :** prise

## La question

Le harnais reçoit des **scores** et ignore délibérément ce qu'est un signal
(`D04`). Il faut maintenant fixer ce qu'est un signal : ce qu'il reçoit, ce qu'il
rend, ce qu'il a le droit d'importer, et surtout **comment on prouve qu'il ne
regarde pas devant lui**. L'invariant II exige que le look-ahead soit empêché par
construction ; le Panel l'empêche de lire une barre postérieure à son as-of, mais
rien n'empêche encore un signal de lire, *à l'intérieur de ce que le Panel montre*,
une barre postérieure à celle qu'il score.

## Les options

**Pour le test de causalité :**

1. **Relire le code et se convaincre.** Écartée — c'est de la vigilance, et
   l'invariant II l'exclut nommément.

2. **Analyse syntaxique seule** : interdire `shift(-n)`, les tranches vers
   l'avant, etc. Écartée **comme test principal** : elle attrape les formes
   connues et passe à côté de tout le reste — une normalisation en plein
   échantillon ne contient aucun décalage négatif. Conservée comme **filtre
   d'importation** (ce qu'un signal a le droit d'appeler), pas comme preuve.

3. **Recalculer le signal sur un panel qui en sait moins, et exiger l'identité.**
   Retenue. Si un signal a besoin d'une donnée postérieure à la barre qu'il
   score, alors tronquer le panel juste après cette barre **change son résultat
   ou le fait disparaître**. C'est une propriété du signal, pas de sa syntaxe :
   elle attrape aussi les formes qu'on n'a pas prévues.

## Le choix

Un signal est un module exposant `SIGNAL_ID`, `HYPOTHESIS`, `PAPER`,
`EXPECTED_SIGN` et `scores(panel, cells, horizon_bars)` ; il est refusé s'il
importe hors d'une liste blanche ; et il n'est causal que si, pour chaque
timestamp scoré `t`, le score obtenu sur un panel tronqué juste après `t` est
**exactement** celui obtenu sur le panel entier — même index, mêmes valeurs.

## Pourquoi

**L'identité, et pas seulement l'égalité des valeurs communes.** Un signal qui
lit `close[t+30]` ne rend pas une valeur *fausse* sur un panel tronqué : il ne
rend **rien du tout** à cet endroit, puisque la barre n'existe pas. Comparer les
seules valeurs partagées le laisserait passer. Le test compare donc **les index
aussi** : un score que le panel entier produit et que le panel tronqué ne produit
pas est un score qui avait besoin du futur.

**Les instants de troncature ne sont pas choisis au hasard.** Ils sont pris
**sur les barres scorées elles-mêmes**, une minute après. C'est là, et
pratiquement nulle part ailleurs, qu'un signal qui triche se distingue d'un
signal honnête : loin du bord, le futur qu'il lit est disponible des deux côtés
et la fraude est invisible. Un test de causalité qui échantillonne au milieu ne
teste rien.

**La sandbox interdit plutôt qu'elle ne surveille.** Liste blanche
d'importations — `pandas`, `numpy`, `panel`, `signals._common`, et rien d'autre.
Pas de réseau (`CLAUDE.md` § Les interdits), pas de système de fichiers, pas
d'`eval`, pas d'accès aux attributs privés du Panel. Une liste blanche se relit ;
une liste noire se contourne.

**Ce que ça sacrifie.** Le test est empirique : il prouve que le signal n'a pas
regardé devant lui **sur les instants sondés**, pas sur tous. Un signal qui ne
tricherait qu'un jour sur mille passerait. C'est pourquoi les sondes sont
nombreuses (32 par signal, réparties sur les cellules et sur le temps) et
pourquoi l'analyse syntaxique est conservée en second rideau. Prétendre à une
preuve serait faux — voir [[Failed Ideas/ledger#F16]], c'est la même honnêteté.

## Ce que ça verrouille

- `sandbox/` : `contract.py` (la forme), `scan.py` (la liste blanche),
  `causality.py` (le test), `signature.py` (l'empreinte du signal, **distincte**
  de celle du harnais — `D05` § Ce qui reste ouvert la laissait ouverte, elle se
  ferme ici).
- `sandbox/tainted.py` : trois signaux **volontairement tricheurs**, qui existent
  pour que la porte 05 ait quelque chose à attraper. Un test qui n'a jamais rien
  attrapé n'est pas un test.
- `signals/_common.py` : l'ancre est lue **sur l'horloge** (le catalogue), plus
  sur la longueur du groupe de barres. La première version demandait où la
  fenêtre se terminait — ce qui, en séance, n'est pas encore connaissable.
  Coût mesuré : 153 observations perdues sur 15 822, soit **0,97 %**.
- Tout signal futur, écrit à la main ou produit par l'agent de la phase 08, passe
  par ce contrat.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| L'exécution réellement **isolée** (processus séparé, limites de mémoire et de temps) | phase 08, quand le code viendra d'un agent et non de nous |
| Le nombre de sondes et leur répartition, si un signal tricheur passait | à la première alerte |
| Les contrôles de dégénérescence — signal constant, 99 % de NaN, doublons | phase 06, c'est sa porte |
