---
type: hub
updated: 2026-09-21
status: actif
sources: [LECONS.md, decisions/DECISION-01-univers-et-donnees.md]
---

# LEÇONS — la synthèse transversale

> **`LECONS.md`, à la racine, fait foi.** Il est numéroté, append-only, jamais
> réécrit, et lu en entier au démarrage de chaque session. Cette page ne le
> remplace pas et n'en recopie pas le contenu comme vérité : elle cherche ce que
> les leçons ont **en commun**, ce qu'aucune d'elles ne dit toute seule.
>
> Si cette page et `LECONS.md` divergent, `LECONS.md` gagne et cette page est
> corrigée.

État : **18 leçons** (L01 → L18) dans `LECONS.md`, qui fait foi.

> [!warning] **Cette synthèse ne couvre que L01 → L05**, acquises en phase 01.
> Constaté le 2026-09-21 : la page annonçait « 5 leçons » comme un état du projet
> alors que `LECONS.md` en porte 18. Le compte est corrigé ; **la synthèse ne
> l'est pas** — relire treize leçons pour en tirer les motifs communs est un
> travail en soi, et le bâcler produirait précisément le genre de résumé plausible
> que ce projet refuse. Les motifs ci-dessous restent vrais de L01 à L05 ; ils ne
> prétendent rien des suivantes. Voir `LECONS.md` pour L06 à L18.

---

## Le motif qui revient dans quatre leçons sur cinq

**Aucune de ces erreurs n'a levé d'exception.**

| Leçon | Le symptôme réel | Ce qu'un test unitaire aurait vu |
|---|---|---|
| L01 — roulement calendaire | une série amputée de 96 % se charge et calcule normalement | rien |
| L02 — FDAX sept fois plus court | une colonne « années » dans un manifeste | rien |
| L04 — Corwin & Schultz à zéro | une colonne entière de `0.00`, **lue comme une bonne nouvelle** | rien |
| L05 — détection des recollements | un compte annuel inférieur au cycle d'échéances | rien |

La conséquence pratique est une règle de travail, pas une morale : **un contrôle
qui ne compare pas à un attendu externe ne contrôle rien.** Chaque fois, ce qui a
sauvé la mise est un ordre de grandeur calculé *à part* — barres ≈ années ×
séances × barres par séance (L01), cycle d'échéances trimestriel ou mensuel
(L05), plancher du tick (L04), recouvrement des périodes (L02).

L03 est la seule qui n'ait rien cassé : elle a réfuté une intuition avant qu'elle
ne coûte. C'est le mode qu'on cherche à rendre habituel.

## Le second motif : le silence d'un estimateur ressemble à une mesure

L04 et L05 sont la même erreur à deux endroits. Un estimateur dont le **rendement
dépend de l'amplitude du phénomène** produit des trous *systématiques*, pas
aléatoires — et un trou systématique ressemble à une valeur.

- Corwin & Schultz rend `0` là où le marché est le plus mince, donc la table de
  coûts est la plus optimiste **exactement là où elle devrait alarmer**.
- La détection de recollements rate les roulements des années à taux zéro, donc
  la liste est la plus incomplète **exactement pour le régime qu'on veut étudier**.

Corollaire opérationnel : avant d'adopter un estimateur, se demander *dans quelle
direction il se trompe quand il se trompe*. S'il se trompe vers le résultat qui
arrange, il ne sert à rien sans une borne indépendante.

## Le troisième motif : l'intuition est fausse dans les deux sens

L03 a réfuté un espoir (« monter en fréquence crée de la largeur » — non : 4,22
contre 4,03). Le cas `NQ × ASIA` a réfuté une évidence négative (« exclusion
évidente » — non : la meilleure cellule asiatique de la grille, voir
[[Failed Ideas/ledger]] F11).

Les deux coûtent pareil. Il n'y a pas de côté de l'intuition qui soit
sûr.

## Ce que les leçons ont déjà verrouillé ailleurs

Une leçon utile change une règle, pas seulement un souvenir. Ce qui a été
verrouillé :

- roulement au volume, définitivement — L01 → [[Failed Ideas/ledger]] F01
- FDAX hors univers, fichier gardé comme témoin — L02 → F02
- la largeur vient de la grille actif × séance, pas de la fréquence — L03 → F06,
  et la métrique de la phase 03 (`D01` §2)
- le tick mesuré comme plancher de coût, les frais restant `null` — L04 → F08
- les dates de roulement de l'auteur des données comme intrant **bloquant** de la
  phase 02 — L05 → F09, et [[phases/phase-02-panel-pit]]

## Ce qu'on n'a pas encore appris et qu'on apprendra

Écrit d'avance, pour pouvoir le relire après :

- le harnais n'a jamais tourné ; aucune leçon ne porte encore sur l'évaluation ;
- le registre est **vide** (`registry/tests.jsonl`, 0 ligne) ; aucune leçon ne
  porte encore sur le comptage des tests ;
- aucun papier n'a été **lu** intégralement (`corpus/AMORCE.md`, dernière ligne) ;
  aucune leçon ne porte encore sur l'extraction.

Les trois premières leçons de ces domaines seront plus chères que les cinq
premières, parce qu'elles arriveront après du code.

## Voir aussi

- `LECONS.md` — l'original, qui fait foi
- [[Failed Ideas/ledger]] — les idées abandonnées, dont la moitié viennent d'ici
- [[concepts/largeur-effective]] · [[concepts/point-in-time]] · [[concepts/cout-aller-retour]]
