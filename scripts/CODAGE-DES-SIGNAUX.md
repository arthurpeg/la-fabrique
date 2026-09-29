# Coder les signaux — guide de la session qui orchestre

**À qui s'adresse ce fichier.** À une session Claude Code lancée pour produire
des signaux à partir des fiches. Cette session **orchestre** : elle prépare les
consignes, lance des **sessions de codage séparées**, les juge, et tient le
compte. **Elle ne code jamais un signal elle-même.**

Lis ce fichier en entier avant de commencer. Il dit ce que tu fais, dans quel
ordre, et ce que tu n'as **pas le droit** de faire. Les règles viennent de
`D07` (le contrat de signal), `D23` (le juge du codeur), `D25`–`D29` (le lot
et sa mesure) et de l'invariant I de `CLAUDE.md` : **l'IA propose, le code
déterministe tranche.**

---

## 0. Avant de commencer

1. Suis la séquence de démarrage de `CLAUDE.md` (wiki, `ETAT.md`, `LECONS.md`).
2. Vérifie que les données sont là : `RSL_DATA_DIR` dans `.env`. Sans elles,
   le juge ne peut pas vérifier la causalité (`S3`) ni la dégénérescence
   (`S4`), et **un verdict partiel ne vaut pas un signal réussi**.
3. Vérifie le quota de l'abonnement (outil `get_usage` de l'application, ou
   la carte d'usage). Une session de codage consomme ~100 000 tokens. Ne
   lance pas un lot qui ferait dépasser **85 %** de la fenêtre de 5 heures :
   une session coupée en plein codage est un essai perdu.
4. Liste ce qui reste à faire :

       uv run python scripts/code_signal.py --list --lot

   La priorité est **le lot figé de la phase 09** (`hypotheses/LOT-09.json`,
   41 fiches). Hors lot : `--list` sans `--lot`.

---

## 1. La boucle, fiche par fiche

Travaille par **lots de 5 fiches**, sessions de codage lancées **en
parallèle**. Pour chaque fiche `<fiche_id>` :

### 1.1 Préparer la consigne

    uv run python scripts/code_signal.py --prepare <fiche_id>

Elle est écrite dans `corpus/consignes-signaux/<fiche_id>.md`. Elle contient
**tout** ce que le codeur a le droit de savoir : la fiche, le contrat `D07`,
la liste blanche des imports, l'interface de `signals/_common.py`, la règle
`S5`. Le module attendu est `signals/<fiche_id avec _ au lieu de ->.py`.

### 1.2 Lancer la session de codage — isolée

Outil `Agent` (type `general-purpose`), une par fiche, en parallèle, **au
premier plan** (`run_in_background: false`) pour que le lot se termine dans ton
tour. Consigne à donner, **mot pour mot**, en remplaçant les deux chemins :

> Tu es un codeur de signal isolé. Ta seule source est ce fichier de consigne :
>
> `C:\Users\Mathis\Documents\la-fabrique\corpus\consignes-signaux\<fiche_id>.md`
>
> Règles d'isolement, strictes :
> - Lis ce fichier EN ENTIER (par morceaux avec l'outil Read si besoin).
> - Ne lis AUCUN autre fichier du dépôt : jamais `signals/`, `hypotheses/`,
>   `decisions/`, `corpus/fiches*/`, `registry/`, `harness/`, `ETAT.md`,
>   `wiki/`, ni l'historique git. Aucune commande shell, aucune recherche
>   (Grep/Glob), aucun accès web.
> - Suis la consigne à la lettre : le contrat exact, `HYPOTHESIS = None`,
>   uniquement les imports autorisés, et **aucune constante numérique absente
>   de la fiche**.
>
> Écris le module (et rien d'autre) avec l'outil Write dans :
> `C:\Users\Mathis\Documents\la-fabrique\signals\<module>.py`
>
> Réponds en une ligne : le chemin écrit et le signe attendu choisi. Il est
> possible que je te renvoie le verdict d'un juge automatique : tu corrigeras
> alors en réécrivant le fichier entier, toujours à partir de la seule
> consigne.

Note l'identifiant de chaque session (`agentId`) : c'est à elle, et à elle
seule, que tu renverras un refus.

### 1.3 Figer ce qu'elle a produit — AVANT de juger

    uv run python scripts/code_signal.py --record signals/<module>.py

C'est ce qui rend « zéro retouche » (`S6`) mesurable (`L22`). **Toujours
`--record` avant `--judge`**, à chaque essai.

### 1.4 Juger

    uv run python scripts/code_signal.py --judge signals/<module>.py --fiche $(uv run python scripts/code_signal.py --fiche-path <fiche_id>)

Six conditions à tolérance zéro (`D23`) : `S1` contrat, `S2` liste blanche,
`S3` causalité, `S4` non-dégénérescence, `S5` fidélité à la fiche, `S6` zéro
retouche. **Aucun IC n'est calculé.**

### 1.5 Si le juge refuse

Renvoie le verdict **tel quel**, par `SendMessage`, **à la même session**
(son `agentId`), avec : « Corrige en réécrivant le fichier entier, à partir de
la seule consigne, mêmes règles d'isolement. » Puis reprends en 1.3.

- **Trois essais au plus par fiche.** Au troisième refus, arrête : la fiche
  est notée en échec, avec le verdict, dans le compte rendu (§ 3).
- Regarde **comment** un signal devient vert (`L28`) : par la faute corrigée,
  ou par un contournement. Un contournement se signale, il ne se garde pas en
  silence.

---

## 2. Ce que tu n'as PAS le droit de faire

Ce ne sont pas des recommandations.

- **Ne jamais écrire ni corriger un signal toi-même.** Pas une ligne. Une
  retouche à la main casse `S6` et invalide le signal. Si un signal est faux,
  il se refait par le codeur.
- **Ne jamais donner au codeur autre chose que sa consigne** : ni un signal
  voisin, ni une hypothèse, ni un indice sur « ce qui marche ». Il
  recopierait au lieu de coder (`D23`, `F42`).
- **Ne jamais calculer un IC, ni lancer une mesure.** Pas de `evaluate()`,
  pas de `scripts/measure_*.py`, pas de corrélation « pour voir ». Tout IC
  s'écrit au registre et compte au dénominateur (invariant III) ; un signal
  regardé avant sa mesure officielle est exclu du lot (`D28`).
- **Ne jamais lancer les portes 03, 04 ou 06** : elles écrivent au registre
  (`L25`). Les portes 05, 07, 08 et 09 (`--check`) sont en lecture seule.
- **Ne jamais écrire ni modifier une hypothèse** (`hypotheses/H*.md`) : c'est
  une étape à part, qui se fait avant la mesure et qui n'est pas celle du
  codeur. `HYPOTHESIS` vaut `None` dans chaque signal produit.
- **Ne jamais modifier le lot** (`hypotheses/LOT-09.json`) : il est figé. L'élargir après une mesure casse `BH` (`D25` C2).
- **Ne jamais toucher** au harnais (`harness/`), au registre
  (`registry/tests.jsonl`), à la tranche `holdout`, ni aux fiches.
- **Ne jamais retoucher un fichier `signals/PRODUCED.json` à la main** : il
  n'est écrit que par `--record`.

---

## 3. En fin de session

1. Relance le juge de la porte en lecture seule :

       uv run python scripts/gate_08.py

2. Écris le compte rendu dans `wiki/log.md` (une ligne datée, en ajout) :
   combien de fiches traitées, combien de signaux verts, combien d'essais au
   total, et **chaque échec avec sa raison**.
3. Mets à jour `ETAT.md` : combien de signaux du lot restent à coder.
4. Commite (le hook de fin de session le fait, mais un message explicite vaut
   mieux) et pousse.

---

## 4. Reprendre après une coupure

Tout est reprenable : `--list --lot` ne montre que les fiches **sans** signal,
et `signals/PRODUCED.json` garde chaque essai. Une session de codage coupée en
cours laisse soit rien, soit un fichier non inscrit : dans le second cas,
**supprime ce fichier non inscrit** et relance la fiche depuis 1.2, avec une
session neuve.

---

## 5. Ce qui vient après, et qui n'est PAS ce travail

Une fois les 41 signaux du lot codés : écrire les 41 hypothèses
pré-enregistrées, produire la matrice de corrélation du lot, puis mesurer une
fois chaque hypothèse (`D25`, `D28`, `D29`). Ces étapes ont leurs propres
règles et **ne se font pas dans une session de codage**.
