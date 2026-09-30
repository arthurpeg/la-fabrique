# Coder des signaux — le tutoriel de la session qui orchestre

**À qui s'adresse ce fichier.** À toute session Claude Code lancée pour
**produire des signaux**, aujourd'hui comme dans six mois. Il ne vise aucun lot
ni aucun papier en particulier : il dit comment transformer **le plus grand
nombre possible de fiches** en signaux **vérifiés**, sans jamais tricher.

**Le rôle de la session qui lit ce fichier : orchestrer.** Elle choisit les
fiches, prépare les consignes, lance des **sessions séparées** (recette, codeur
principal, codeur témoin), les fait juger, compare les deux codages, et tient
le compte. **Elle n'écrit jamais elle-même ni une recette ni un signal.**

Les règles viennent de `D07` (le contrat de signal), `D23` (le juge du
codeur), `D34` (le codage vérifié), `D25`–`D29` (les lots et leur mesure) et de
l'invariant I de `CLAUDE.md` : **l'IA propose, le code déterministe tranche.**

---

## 0. Avant de commencer

1. Suis la séquence de démarrage de `CLAUDE.md` (wiki, `ETAT.md`, `LECONS.md`).
2. **Données** : `RSL_DATA_DIR` doit être renseigné dans `.env`. Sans les
   données, le juge ne peut vérifier ni la causalité (`S3`) ni la
   dégénérescence (`S4`), et le double codage ne peut rien comparer. **Un
   verdict partiel ne vaut pas un signal réussi.**
3. **Quota** : regarde l'usage de l'abonnement (outil `get_usage` de
   l'application, ou la carte d'usage). Une fiche coûte **trois sessions** :
   une recette (~165 000 tokens mesurés : elle lit le papier entier) et deux
   codages (~80 000 chacun), soit ~325 000 tokens par fiche. Ne lance
   jamais un groupe qui ferait dépasser **85 %** de la fenêtre de 5 heures :
   une session coupée en plein travail est un essai perdu.
4. **Ce qui reste à coder** :

       uv run python scripts/code_signal.py --list
       uv run python scripts/recette.py --status
       uv run python scripts/double_codage.py --status

## 1. L'ordre de priorité

Traite les fiches dans cet ordre, et **aussi loin que le quota le permet** :

1. **Les fiches d'un lot figé**, s'il en existe un (`hypotheses/LOT-*.json`) :

       uv run python scripts/code_signal.py --list --lot

   Un lot attend ses signaux vérifiés pour être mesuré ; c'est ce qui débloque
   la suite.
2. **Toutes les autres fiches sans signal**, dans l'ordre de `--list`.
3. **Quand il ne reste plus aucune fiche à coder**, le goulot n'est plus le
   codage mais les fiches : dis-le dans le compte rendu (§ 4) — il faut alors
   ficher de nouveaux papiers, ce qui est un autre travail
   (`corpus/extract_fiche_harvest.py`), avec ses propres règles (`D16`).

Une fiche donne **un** signal (un module par fiche, nommé d'après elle). Une
fiche dont rien ne se transpose à nos neuf futures intraday peut ne donner
aucun signal valable : le juge le dira.

---

## 2. La boucle, fiche par fiche

Travaille par **groupes de 5 fiches**, sessions lancées **en parallèle**, et
enchaîne les groupes tant que le quota le permet. Pour chaque fiche
`<fiche_id>`, dans cet ordre :

| Étape | Qui | Outil |
|---|---|---|
| 2.1 Recette | une session isolée, `opus` | `scripts/recette.py` |
| 2.2 Consignes | toi | `code_signal.py --prepare` et `--prepare --temoin` |
| 2.3 Deux codages | deux sessions isolées, `opus` et `sonnet` | `Agent` |
| 2.4 Figer | toi | `code_signal.py --record` |
| 2.5 Juger | toi | `code_signal.py --judge` |
| 2.6 Comparer | toi | `scripts/double_codage.py` |
| 2.7 Si discordant | toi, puis des sessions neuves | retour en 2.1 |

### 2.1 La recette — avant tout codage

    uv run python scripts/recette.py --prepare <fiche_id>

La consigne est écrite dans `corpus/consignes-recettes/<fiche_id>.md` : la
fiche, le format de la recette et **le texte entier du papier**. Lance une
session `Agent` (type `general-purpose`, `model: "opus"`, au premier plan) avec
cette consigne **mot pour mot** :

> Tu es une session de recette isolée. Ta seule source est ce fichier :
>
> `C:\Users\Mathis\Documents\la-fabrique\corpus\consignes-recettes\<fiche_id>.md`
>
> Lis-le EN ENTIER (par morceaux avec l'outil Read). Ne lis AUCUN autre fichier
> du dépôt, aucune commande shell, aucune recherche, aucun accès web. Écris la
> recette JSON (et rien d'autre) avec l'outil Write à l'emplacement que la
> consigne indique. Chaque citation est recopiée À LA LETTRE du texte ; ce que
> le papier ne dit pas est null avec sa raison — n'invente jamais une valeur.
> Réponds en une ligne : le chemin écrit et le nombre d'ambiguïtés relevées.

Puis, **seulement après la réponse de la session** — figer un fichier qu'elle
écrit encore inscrit un état intermédiaire, et `--check` le refuse (vu le
2026-09-30) — et **toujours dans cet ordre** :

    uv run python scripts/recette.py --record corpus/recettes/<fiche_id>.json
    uv run python scripts/recette.py --check corpus/recettes/<fiche_id>.json

Un refus se renvoie **tel quel**, par `SendMessage`, à la même session :
« Corrige en réécrivant le fichier entier, mêmes règles. » Puis `--record` et
`--check` à nouveau. **Trois essais au plus** ; au troisième refus, la fiche
est en échec « recette » (§ 2.8).

### 2.1 bis Le marché du papier — avant de coder (`D38`)

La recette déclare `market` : sur quel marché le papier mesure, et lesquels de
nos instruments **sont** ce marché (`exact_roots`). Regarde-le **avant** de
lancer les codeurs :

    uv run python -c "import json,sys; print(json.load(open(sys.argv[1], encoding='utf-8')).get('market'))" corpus/recettes/<fiche_id>.json

- `exact_roots` non vide : continue en 2.2. La mesure portera sur ces
  instruments et leur classe, dans les fenêtres du papier.
- `exact_roots: []` : le marché du papier nous est absent. **Ne code pas** —
  écarte la fiche, c'est une économie de ~160 000 tokens :

      uv run python scripts/ecarter_du_lot.py <fiche_id> --preuve univers --motif "<le marché du papier>"

  et commite aussitôt.

### 2.2 Les deux consignes de codage

    uv run python scripts/code_signal.py --prepare <fiche_id>
    uv run python scripts/code_signal.py --prepare <fiche_id> --temoin

Elles sont écrites dans `corpus/consignes-signaux/<fiche_id>.md` et
`<fiche_id>.temoin.md`, et contiennent **tout** ce qu'un codeur a le droit de
savoir : la fiche **avec sa recette** (clé `recipe`), le contrat `D07` avec
`CHOICES`, la liste blanche des imports, l'interface de `signals/_common.py`, la
règle `S5`. Elles ne diffèrent que par le chemin du module :

| | Module écrit |
|---|---|
| principal | `signals/<fiche_id, les - remplacés par des _>.py` |
| témoin | `verification/temoins/<même nom>.py` |

`--prepare` refuse une fiche sans recette valide : reviens alors en 2.1.

### 2.3 Les deux codages — isolés, de deux modèles, en parallèle

Deux sessions `Agent` (type `general-purpose`, au premier plan), **lancées
dans le même message** :

- le **principal** avec `model: "opus"` et la consigne `<fiche_id>.md` ;
- le **témoin** avec `model: "sonnet"` et la consigne `<fiche_id>.temoin.md`.

À chacune, **mot pour mot**, en remplaçant les deux chemins :

> Tu es un codeur de signal isolé. Ta seule source est ce fichier de consigne :
>
> `C:\Users\Mathis\Documents\la-fabrique\corpus\consignes-signaux\<consigne>.md`
>
> Règles d'isolement, strictes :
> - Lis ce fichier EN ENTIER (par morceaux avec l'outil Read si besoin).
> - Ne lis AUCUN autre fichier du dépôt : jamais `signals/`, `verification/`,
>   `hypotheses/`, `decisions/`, `corpus/`, `registry/`, `harness/`,
>   `ETAT.md`, `wiki/`, ni l'historique git. Aucune commande shell, aucune
>   recherche (Grep/Glob), aucun accès web.
> - Suis la consigne à la lettre : le contrat exact, `HYPOTHESIS = None`,
>   `CHOICES` rempli de chacune de tes interprétations, uniquement les imports
>   autorisés, et **aucune constante numérique absente de la fiche ou des
>   valeurs de sa recette**.
>
> Écris le module (et rien d'autre) avec l'outil Write dans :
> `C:\Users\Mathis\Documents\la-fabrique\<chemin du module>`
>
> Réponds en une ligne : le chemin écrit et le signe attendu choisi. Il est
> possible que je te renvoie le verdict d'un juge automatique : tu corrigeras
> alors en réécrivant le fichier entier, toujours à partir de la seule
> consigne.

Note l'identifiant de chaque session (`agentId`) : c'est à elle, et à elle
seule, que tu renverras un refus. **Ne dis jamais à un codeur ce qu'a écrit
l'autre.**

### 2.4 Figer ce qu'elles ont produit — AVANT de juger

    uv run python scripts/code_signal.py --record signals/<module>.py
    uv run python scripts/code_signal.py --record verification/temoins/<module>.py

C'est ce qui rend « zéro retouche » (`S6`) mesurable (`L22`) ; chaque dossier
a son registre de production. **Toujours `--record` avant `--judge`**, à chaque
essai.

### 2.5 Juger chaque codage

    uv run python scripts/code_signal.py --judge signals/<module>.py
    uv run python scripts/code_signal.py --judge verification/temoins/<module>.py

Six conditions à tolérance zéro (`D23`) — `S1` contrat, `S2` liste blanche,
`S3` causalité, `S4` non-dégénérescence, `S5` fidélité à la fiche et aux
valeurs de sa recette, `S6` zéro retouche — **plus `CHOICES`** (`D34`). Le
verdict est inscrit dans `verification/jugements.jsonl`. **Aucun IC n'est
calculé.**

Un refus se renvoie **tel quel**, par `SendMessage`, **à la session qui a
écrit ce module**, avec : « Corrige en réécrivant le fichier entier, à partir
de la seule consigne, mêmes règles d'isolement. » Puis reprends en 2.4.
**Trois essais au plus par codeur** ; au troisième refus, la fiche est en échec
« juge » (§ 2.8). Regarde **comment** un signal devient vert (`L28`) : par la
faute corrigée, ou par un contournement. Un contournement se signale.

### 2.6 Comparer les deux codages

Quand les deux sont verts :

    uv run python scripts/double_codage.py <fiche_id>

Il compare leurs **scores** (jamais un rendement), et inscrit le verdict dans
`verification/concordance.jsonl` :

- **CONCORDANT** — même signe attendu, ρ ≥ 0,70, couverture ≥ 0,80 : la fiche
  est **vérifiée**. Elle peut entrer dans un lot. Fini pour elle.
- **DISCORDANT** — passe en 2.7.

### 2.7 Si les deux codages divergent

Le script affiche les `CHOICES` des deux codeurs côte à côte. **Le désaccord
se lit là** : une fenêtre, une normalisation, un signe, une séance que la
recette laissait ouverts.

1. Écris **la question** en une phrase neutre, sans donner de réponse ni dire
   quel codeur avait raison — par exemple : « la volatilité se calcule-t-elle
   sur les rendements journaliers ou intraday ? ».
2. Refais la recette en la nommant, par une **session neuve** :

       uv run python scripts/recette.py --prepare <fiche_id> --precisions "<la question>"

   puis 2.1 (`--record`, `--check`).
3. Refais **les deux codages** par des **sessions neuves** (2.2 à 2.6). Pas
   les anciennes : elles savent ce qu'elles ont écrit.

**Deux tours au plus.** Au second DISCORDANT, la fiche est en échec
« concordance » (§ 2.8). Il est possible que le papier ne tranche vraiment pas :
c'est un résultat, pas une panne.

### 2.8 Une fiche en échec

Un échec se note dans le compte rendu (§ 4) avec sa raison. **Si la fiche est
dans un lot** et que la mesure du lot n'a pas commencé :

    uv run python scripts/ecarter_du_lot.py <fiche_id> --preuve concordance|juge|recette --motif "<raison>"

puis **commite aussitôt** : la date du commit prouve que l'écart précède la
mesure. Après la première mesure, plus rien ne s'écarte (`D28`).

---

## 3. Ce que tu n'as PAS le droit de faire

Ce ne sont pas des recommandations.

- **Ne jamais écrire ni corriger une recette ou un signal toi-même.** Pas une
  ligne. Une retouche à la main casse `S6` et invalide le travail. Un signal
  faux se refait par le codeur ; une recette fausse, par une session de
  recette.
- **Ne jamais donner à un codeur autre chose que sa consigne** : ni un signal
  voisin, ni l'autre codage de la même fiche, ni une hypothèse, ni un indice
  sur « ce qui marche ». Il recopierait au lieu de coder (`D23`, `F42`), et le
  double codage ne mesurerait plus rien.
- **Ne jamais trancher une ambiguïté à la place du papier.** En 2.7, tu poses
  la question ; c'est la recette, citations à l'appui, qui y répond — ou qui
  dit que le papier se tait.
- **Ne jamais calculer un IC, ni lancer une mesure.** Pas de `evaluate()`, pas
  de `scripts/measure_*.py`, pas de corrélation avec un rendement « pour
  voir ». Tout IC s'écrit au registre et compte au dénominateur (invariant
  III) ; un signal regardé avant sa mesure officielle ne peut plus entrer dans
  un lot (`D28`). `double_codage.py` compare des scores entre eux : c'est
  permis, et c'est tout.
- **Ne jamais lancer les portes 03, 04 ou 06** : elles écrivent au registre
  (`L25`). Les portes 05, 07, 08 et `gate_09.py --check` sont en lecture seule.
- **Ne jamais écrire ni modifier une hypothèse** (`hypotheses/H*.md`), ni un
  lot (`hypotheses/LOT-*.json`) autrement que par `ecarter_du_lot.py` : ce
  sont des étapes à part, qui ne sont pas celles du codeur. `HYPOTHESIS` vaut
  `None` dans chaque signal produit.
- **Ne jamais toucher** au harnais (`harness/`), au registre
  (`registry/tests.jsonl`), à la tranche `holdout`, ni aux fiches.
- **Ne jamais modifier à la main** `signals/PRODUCED.json`,
  `verification/temoins/PRODUCED.json`, `corpus/recettes/PRODUCED.json`,
  `verification/jugements.jsonl` ni `verification/concordance.jsonl` : ils ne
  s'écrivent que par les outils, et les deux journaux sont append-only.
- **Ne jamais changer un seuil de `D34`** (`scripts/codage_verifie.py`) : c'est
  une décision écrite, et elle est interdite après la première mesure d'un lot.

---

## 4. En fin de session

1. Relance toutes les gardes, en lecture seule — elles doivent finir sur
   `TOUT PASSE` :

       uv run python scripts/verifier_tout.py

2. Écris le compte rendu dans `wiki/log.md` (une ligne datée, en ajout) :
   fiches traitées, recettes valides, signaux vérifiés (CONCORDANT), essais et
   tours au total, **chaque échec avec sa raison**, et ce qui reste à coder
   (`--list`, `double_codage.py --status`).
3. Recopie les ρ des tours de la session au § Journal de `D34` : le seuil
   n'est calibré que sur un cas, et ces chiffres diront s'il est bien placé.
4. Mets à jour `ETAT.md` : signaux vérifiés, restant à coder, fiches écartées,
   et si le goulot est devenu les fiches (§ 1, point 3).
5. Commite et pousse.

---

## 5. Reprendre après une coupure

Tout est reprenable :

- `code_signal.py --list` ne montre que les fiches **sans** signal principal ;
- `recette.py --status` et `double_codage.py --status` disent où en est chaque
  fiche ;
- les registres de production gardent chaque essai.

Une session coupée en cours laisse soit rien, soit un fichier non inscrit :
dans le second cas, **supprime ce fichier non inscrit** et relance l'étape
avec une session neuve. Une fiche dont le principal existe mais pas le témoin
reprend en 2.2 pour le témoin seul.

---

## 6. Ce qui vient après, et qui n'est PAS ce travail

Un signal vérifié n'est pas un signal testé. Pour qu'il soit mesuré, il faut,
dans cet ordre et **hors de la session de codage** : écrire son hypothèse
pré-enregistrée, le déclarer dans un lot clos, produire la matrice de
corrélation du lot, puis mesurer une fois chaque hypothèse (`D25`, `D28`,
`D29`). Chacun de ces outils refuse un signal sans double codage CONCORDANT
(`D34`).

| Étape | Outil |
|---|---|
| 8. Hypothèses | `scripts/hypotheses_lot.py --status` puis `--write`, **commiter aussitôt** |
| 9. Matrice de corrélation | `scripts/lot_correlations.py --check` puis sans option |
| 10. Mesure | `scripts/measure_lot.py --check` ; `--run --je-mesure` seulement après la décision de harnais groupée, qui renseigne `HARNAIS_DU_LOT` |
| Porte 09 | `scripts/gate_09.py` |
