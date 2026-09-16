---
type: hub
updated: 2026-09-16
status: actif
sources: [decisions/DECISION-01-univers-et-donnees.md, LECONS.md, corpus/AMORCE.md]
---

# Registre des idées abandonnées

> **À lire en entier avant de commencer quoi que ce soit.** C'est la règle
> permanente n° 1 de `CLAUDE.md` § Wiki, et c'est le fichier le plus important du
> wiki.
>
> Sa seule fonction : t'empêcher de repayer un cul-de-sac que quelqu'un — toi,
> dans une session que tu ne te rappelles pas — a déjà payé. Une session qui
> arrive froide n'a aucun moyen de savoir qu'une idée évidente a déjà été
> essayée. Ici, elle l'a.
>
> **Une ligne ne se supprime jamais.** Une idée qui redevient valide reçoit une
> ligne dans la colonne « ce qui la rouvrirait », et une nouvelle ligne au
> [[log]] — la ligne d'origine reste, parce qu'elle raconte pourquoi on avait eu
> raison de l'écarter *à l'époque*.

## Comment ajouter une ligne

Une idée abandonnée, une ligne. Obligatoirement :

- **la raison**, chiffrée ou liée à une mesure. « Ça ne marchait pas » ne dissuade
  personne — c'est une ligne inutile ;
- **l'autorité** : la décision, la leçon ou le fichier de mesure qui l'a tuée ;
- **ce qui la rouvrirait**, ou `rien` si elle est close définitivement. Beaucoup
  d'idées ne sont pas fausses : elles sont fausses *étant donné* une contrainte
  qui peut tomber.

Si l'abandon a coûté quelque chose — du temps, un résultat faux, un test gaspillé
— il relève **aussi** de `LECONS.md`, qui fait foi. Le ledger le référence alors,
il ne le réécrit pas.

---

## Le registre

| # | Idée abandonnée | Date | Phase | Pourquoi — la raison, chiffrée | Autorité | Ce qui la rouvrirait |
|---|---|---|---|---|---|---|
| F01 | Construire les séries continues au **roulement calendaire** (`.c.0`) plutôt qu'au basculement de volume (`.v.0`) | 2026-09-15 | 01 | Décide de la **quantité d'historique qui existe**, pas de quelques barres : l'or rendait 136 702 barres au lieu de 3 717 717 — 27 fois moins — et les devises perdaient plus de la moitié. Aucune exception n'est levée : la série tronquée se charge et produit des chiffres normaux. | `LECONS.md` L01 | Rien. Le `.v.0` est retenu. |
| F02 | Inclure **FDAX** dans l'univers de travail | 2026-09-15 | 01 | 1,46 an d'historique contre 10,65 pour les neuf autres (Databento n'a intégré EUREX qu'en mars 2025) : **absent de la totalité de la tranche `research`**. Corrélation 0,70–0,76 avec NQ/ES/YM sur sa propre fenêtre — zéro pari supplémentaire. Et une horloge d'échange distincte, qui imposerait une seconde définition de séance pour rien. | `D01` §1, `LECONS.md` L02 | Rien à ce fournisseur. Le fichier est conservé comme **témoin hors univers**. |
| F03 | Évaluer les signaux par un **IC transversal** (classement en déciles des 9 instruments) | 2026-09-15 | 01 | Neuf instruments ne portent que **4,03 paris indépendants** (4,22 à 15 min). On ne classe pas neuf actifs en déciles ; un rang transversal sur quatre blocs corrélés mesure surtout le bruit d'estimation de la matrice de corrélation. | `D01` §2, `scripts/out/a3_breadth.json` | Un élargissement substantiel de l'univers — donc [[Failed Ideas/ledger#F04]] d'abord. |
| F04 | **Acheter de la largeur** : deuxième échéance via Databento, pour ouvrir la famille carry (option B de D01) | 2026-09-15 | 01 | Deux motifs, et **le second est le vrai**. Budget : 2 388 à 54 000 $/an pour un budget de 0 €. Surtout : le **carry est un signal de plusieurs jours à plusieurs mois**, il ne se loge pas dans une grille intraday à clôture forcée. Même gratuite, la deuxième échéance n'apporterait rien à l'horizon retenu. | `D01` § Les options, § Condition de révision 1 et 4 | **Deux portes distinctes.** (a) Un accès Databento gratuit (licence de l'auteur des données) lève le motif budget — mais pas le motif horizon. (b) **Un changement d'horizon** hors de l'intraday lève les deux. Ne pas rouvrir sur le seul (a). |
| F05 | **Passer en journalier** (option C de D01) | 2026-09-15 | 01 | Divise par ~1 350 le nombre d'observations pour gagner **zéro pari** : 4,03 en journalier contre 4,22 à 15 minutes. L'IC requis pour un IR de 1 passerait de 0,018 à 0,031. | `D01` § Les options | Un changement d'horizon décidé par écrit. Voir F04 (b). |
| F06 | **Monter en fréquence** pour gagner de la largeur | 2026-09-15 | 01 | La largeur effective ne bouge pas : 4,22 à 15 min, 4,19 à 30 min, 4,17 à 60 min, 4,03 en journalier. **Changer de fréquence ne crée aucune largeur.** Ce qui en crée, c'est la grille actif × séance (12,40 en sommant trois fenêtres disjointes), et le gain vient de la **structure de blocs** — le bloc devises se dissout en séance asiatique — pas du nombre d'instruments. | `LECONS.md` L03, `scripts/out/a5_breadth_intraday.json` | Rien. La réponse est mesurée, pas supposée. |
| F07 | Découper les tranches en **trois blocs contigus** `research` / `validation` / `holdout` | 2026-09-15 | 01 | Deux ans de validation composés d'un unique régime baissier (2022-2023, NQ à +2,0 % de dérive contre +20,9 % en recherche) ne valident qu'une chose : ce régime-là. Remplacé par un `pool` 2016→2023 en **walk-forward purgé, plusieurs plis, embargo aux frontières**. | `D01` §5 | Rien. |
| F08 | Estimer le coût de transaction par **Corwin & Schultz (2012) seul** | 2026-09-15 | 01 | Sur barres 1 minute sa médiane est **exactement zéro** pour 6A, 6B, 6J et toutes les cellules asiatiques : l'estimateur est conçu pour des barres journalières. Un critère de rétention bâti là-dessus déclarait **27 cellules sur 27 négociables**, y compris celles où 42 % des barres portent moins de dix contrats. | `LECONS.md` L04, `D01` §7 | Il est **conservé comme borne haute** là où il dépasse le tick (CL et NQ en séance US). Le plancher, lui, est le tick mesuré. |
| F09 | Traiter la **détection empirique des recollements** comme la liste autoritative des roulements | 2026-09-15 | 01→02 | Elle rend 3,4–3,6 roulements par an pour les indices là où il y en a 4, et 8,5 pour CL là où il y en a 12. Les manquants sont ceux des années à taux proches de zéro — **trous systématiques et corrélés au régime**, pas aléatoires. 6A n'est pas tranché du tout. Une liste incomplète est plus dangereuse qu'aucune liste : elle donne le sentiment que le problème est traité. | `LECONS.md` L05, `D01` §6 | Rien — elle ne sera jamais autoritative. Elle reste utile comme **contrôle** : à la réception des dates de l'auteur des données, comparer avant d'adopter, l'écart mesure la méthode et fera l'objet d'une entrée dans `LECONS.md`. |
| F10 | Retenir les **27 cellules** actif × séance | 2026-09-15 | 01 | Deux tombent sous la règle de rétention posée **avant** lecture des chiffres (volume médian ≥ 10 contrats/min, barres minces ≤ 25 %, aller-retour ≤ ⅓ du mouvement médian de 15 min) : `6B × ASIA` (42,4 % de barres minces, coût à 35 % du mouvement) et `YM × ASIA` (34,6 %, 15 contrats/min). | `D01` §3, `scripts/out/a8_session_grid.json` | Rien pour ces deux-là aux seuils actuels. Un changement de seuil serait une décision écrite. |
| F11 | Exclure **`NQ × ASIA`**, « cas d'exclusion évident » | 2026-09-15 | 01 | **L'intuition était fausse et la mesure l'a retournée** : 41 contrats/minute, 11,6 % de barres minces, coût à **7 %** du mouvement médian — la meilleure cellule asiatique de la grille. Elle est retenue. Ligne gardée comme rappel : l'évidence non mesurée est un piège symétrique de l'espoir non mesuré. | `D01` §3 | Sans objet — c'est l'exclusion qui a été abandonnée, pas la cellule. |
| F12 | Ancrer les **fenêtres de séance à UTC** | 2026-09-15 | 01 | Ferait dériver les fenêtres d'une heure deux fois par an, à des dates que personne n'a choisies. La disjonction des fenêtres — l'objet même de l'exigence UTC — est préservée dans `America/New_York`, la seule horloge où elle peut l'être pour neuf instruments tous sur CME Globex. | `D01` §3, §8 | Un instrument hors CME Globex dans l'univers, qui exigerait une définition de séance par instrument (déjà prévue au catalogue). |

---

## Idées annoncées mortes par la littérature, à tester quand même

Ce ne sont **pas** des idées abandonnées, et elles n'ont pas de numéro `F`. Elles
sont ici parce que la confusion serait coûteuse dans les deux sens.

`corpus/AMORCE.md` recense deux familles que la littérature déclare éteintes : la
**dérive nocturne** (entrée 8, démentie par l'entrée 9) et la **dérive pré-FOMC**
(entrée 15, démentie par l'entrée 16). Ce n'est pas une raison de ne pas les
tester — c'en est une de les tester **en sachant, avant de regarder, que le
résultat attendu est nul**. C'est exactement ce que demande l'invariant IV.

Elles ne descendront ici que si *nos* mesures les tuent, avec *nos* chiffres.

## Voir aussi

- [[lessons]] — la synthèse transversale ; `LECONS.md` à la racine fait foi
- [[index]] · [[hot]] · [[SCHEMA]]
