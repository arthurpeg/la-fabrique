---
type: hub
updated: 2026-09-17
status: actif
sources: [decisions/DECISION-01-univers-et-donnees.md, decisions/DECISION-03-panel-et-catalogue.md, LECONS.md, corpus/AMORCE.md]
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
| F13 | Charger la **série entière en mémoire** puis n'exposer que le passé, plutôt que pousser la coupe dans le lecteur Parquet | 2026-09-17 | 02 | Le futur resterait dans le processus, et seule l'API l'en tiendrait éloigné — de la vigilance déguisée en architecture, là où l'invariant II exige une impossibilité. Et ça ne coûte rien : **0,09 s contre 0,08 s** pour lire NQ (1,88 M barres) avec la coupe poussée dans le lecteur. | `D03` § Les options, `panel/panel.py` | La disparition du filtrage à la lecture (changement de format ou de bibliothèque) — auquel cas il faut **remplacer** le mécanisme, pas revenir à celui-ci. |
| F14 | Ajuster les séries de roulement **par différence** (soustraire l'écart) plutôt que par ratio | 2026-09-17 | 02 | `D01` §6 exige que la série construite en `t` ne diffère de celle construite en `t+1` que par un **facteur d'échelle uniforme** — c'est la définition du multiplicatif. L'additif décale les niveaux d'une constante et **ne préserve pas les rendements** : tout IC calculé dessus serait faux d'une quantité qui dépend du niveau de prix. | `D03` § Complément 2026-09-17, `panel/rolls.py` | Rien pour des prix strictement positifs. La question se reposerait sur un sous-jacent pouvant passer sous zéro — un spread, ou le pétrole d'avril 2020 s'il était dans l'univers. |
| F15 | Rendre l'invariant III incontournable par un **garde extérieur à `harness/`** — crochet d'import, `sitecustomize`, lint refusant `from harness.metric import ...` | 2026-09-17 | 04 | Même raison que [[Failed Ideas/ledger#F13]], et c'est la deuxième fois qu'elle sert : le nombre resterait **calculable dans le processus**, et seule une couche extérieure l'en tiendrait éloigné. De la vigilance déguisée en architecture. Remplacé par la fusion des deux gestes — le jeton est pris avant le calcul, la ligne est écrite par la fonction qui produit le nombre. | `D05` § Les options, `harness/metric.py`, `harness/registry.py` | Rien. Si le mécanisme du jeton devait tomber, il faudrait le **remplacer** par plus fort, pas revenir à un garde extérieur. |
| F16 | Prétendre que le contournement est **impossible** plutôt que « impossible sans un geste délibéré et visible » | 2026-09-17 | 04 | Python n'a pas d'encapsulation réelle : `from harness.metric import _pool` rend encore un nombre, et aucune écriture de ce dépôt n'y changera rien. Une porte qui affirmerait l'impossibilité absolue mentirait, et un jour quelqu'un s'y fierait. La porte 04 démontre donc le vrai périmètre : aucun chemin **public**, et aucun module **de ce dépôt** ne prend le chemin privé — vérifié par analyse syntaxique des 27 modules. | `D05` § Pourquoi, `registry/SCHEMA.md` § Ce que ça ne prétend pas, `scripts/gate_04_registry.py` §6 | Un langage ou un mécanisme d'exécution offrant une vraie encapsulation. Pas d'ici là. |
| F17 | Prendre pour banc d'essai **les cinq signaux du plan de montage** — momentum 12-1, book-to-price, low-vol, reversal à un mois, taille | 2026-09-17 | 05 | Ils sont **transversaux, mensuels, sur actions**. Notre univers est de neuf futures en intraday portant **4,22 paris indépendants** : on ne classe pas neuf actifs en déciles ([[Failed Ideas/ledger#F03]]), et book-to-price n'existe pas sur un contrat à terme. Les transposer n'aurait pas de sens ; les tester tels quels, encore moins. | `D06` § Les options, `D01` §2 | Un changement de classe d'actifs — c'est-à-dire un autre projet. |
| F18 | **Se passer de banc d'essai** et redéfinir les portes 05, 06 et 08 sans vérité terrain | 2026-09-17 | 05 | La porte 05 s'accommoderait d'un signal jetable, mais la porte 08 — « l'agent reproduit ton implémentation à mieux que 0,9 de corrélation » — perdrait **tout référent** : elle deviendrait « l'agent produit du code qui tourne », ce qui ne mesure rien. Une porte sans sujet est une porte franchie d'avance. | `D06` § Les options, `ETAT.md` phases 05-08 | Rien. Remplacé par deux étalons écrits à la main (`H01`, `H02`). |
| F19 | Établir la causalité d'un signal en **relisant son code** | 2026-09-17 | 05 | C'est de la vigilance, et l'invariant II l'exclut nommément. Une relecture ne dit rien d'une normalisation en plein échantillon, qui ne contient aucun décalage vers l'avant et lit pourtant tout le futur. | `D07` § Les options, `CLAUDE.md` invariant II | Rien. |
| F20 | Établir la causalité par **analyse syntaxique seule** — interdire `shift(-n)`, les tranches vers l'avant | 2026-09-17 | 05 | Elle attrape les formes connues et **rien d'autre** : sur les trois tricheurs de `sandbox/tainted.py`, elle n'en voit qu'un. Le z-score en plein échantillon et la lecture de la clôture de fenêtre passent sans une ligne suspecte. Conservée comme **liste blanche d'importations**, jamais comme preuve. | `D07` § Les options, `sandbox/scan.py`, `sandbox/tainted.py` | Rien. Le test de propriété (`sandbox/causality.py`) est le premier rideau, celui-ci le second. |
| F21 | Ancrer un signal **sur la longueur du groupe de barres** — « trente barres avant la dernière » | 2026-09-17 | 05 | Demande où la fenêtre **se termine**, ce qui en séance n'est pas encore connaissable : irréprochable en backtest, faux en production, et invisible sans un test qui le cherche. Remplacé par une ancre lue sur l'horloge du catalogue, propriété que chaque barre porte seule. Coût mesuré : **153 observations sur 15 822**, soit 0,97 %. | `D07` § Ce que ça verrouille, `signals/_common.py` | Rien. Un signal qui ne pourrait pas tourner en séance ne sert à rien à un opérateur qui l'exécutera lui-même. |
| F22 | Loger les contrôles automatiques dans un paquet `controls/` **à côté** du harnais | 2026-09-17 | 06 | `registry.code_hash()` n'empreinte que `harness/*.py`. Un seuil modifié une ligne plus loin changerait les rejets **sans changer l'empreinte**, et deux résultats incomparables porteraient le même numéro de juge. Les contrôles sont du jugement déterministe : leur place est dans `harness/`, figée et empreintée avec le reste. | `D08` § Les options, `harness/controls.py` | Rien, tant que l'empreinte se calcule sur `harness/*.py`. L'élargir reviendrait à admettre que ces fichiers sont le harnais. |
| F23 | Traduire « 99 % de NaN » par **99 % de barres non scorées** | 2026-09-17 | 06 | Aurait rejeté **les deux seuls signaux du projet**. Les étalons scorent une barre par séance sur environ 390 : 99,7 % des barres n'ont pas de score, et c'est **la forme de l'hypothèse**, pas une dégénérescence. Ce qui compte est le nombre d'**observations** qui en résultent. | `D08` § Pourquoi, `harness/controls.py`, `LECONS.md` L10 | Rien. Le contrôle porte sur les observations, et c'est la bonne grandeur. |
| F24 | Appliquer le plancher de deux cellules **à tout appel du harnais**, calibrations comprises | 2026-09-17 | 06 | A cassé la **porte 03** immédiatement : sa calibration reproduit à la main l'IC d'une seule cellule, à 1e-12, et c'est tout son objet. Le harnais sert deux sortes de clients — des tests et des calibrations de lui-même — et une règle écrite pour les premiers interdisait les secondes. Remplacé par une dérogation écrite, vérifiée étroite par la porte 06. | `D08` § Pourquoi, `LECONS.md` L11, `harness/controls.py` | Rien. La dérogation n'achète rien : une calibration ne porte pas d'hypothèse et n'atteint jamais le dénominateur. |

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
