# Coder des signaux — le tutoriel de la session qui orchestre

**À qui s'adresse ce fichier.** À toute session Claude Code lancée pour
**produire des signaux**, aujourd'hui comme dans six mois. Il ne vise aucun lot
ni aucun papier en particulier : il dit comment transformer **le plus grand
nombre possible de fiches** en signaux jugés, sans jamais tricher.

**Le rôle de la session qui lit ce fichier : orchestrer.** Elle choisit les
fiches, prépare les consignes, lance des **sessions de codage séparées**, les
fait juger, et tient le compte. **Elle ne code jamais un signal elle-même.**

Les règles viennent de `D07` (le contrat de signal), `D23` (le juge du
codeur), `D25`–`D29` (les lots et leur mesure) et de l'invariant I de
`CLAUDE.md` : **l'IA propose, le code déterministe tranche.**

---

## 0. Avant de commencer

1. Suis la séquence de démarrage de `CLAUDE.md` (wiki, `ETAT.md`, `LECONS.md`).
2. **Données** : `RSL_DATA_DIR` doit être renseigné dans `.env`. Sans les
   données, le juge ne peut vérifier ni la causalité (`S3`) ni la
   dégénérescence (`S4`), et **un verdict partiel ne vaut pas un signal
   réussi**.
3. **Quota** : regarde l'usage de l'abonnement (outil `get_usage` de
   l'application, ou la carte d'usage). Une session de codage consomme
   ~100 000 tokens. Ne lance jamais un groupe qui ferait dépasser **85 %** de
   la fenêtre de 5 heures : une session coupée en plein codage est un essai
   perdu.
4. **Ce qui reste à coder** :

       uv run python scripts/code_signal.py --list

   Toutes les fiches sans signal, qu'elles viennent d'`AMORCE.md`
   (`corpus/fiches/`) ou du moissonneur (`corpus/fiches_harvest/`).

## 1. L'ordre de priorité

Code dans cet ordre, et **aussi loin que le quota le permet** :

1. **Les fiches d'un lot figé**, s'il en existe un (`hypotheses/LOT-*.json`) :

       uv run python scripts/code_signal.py --list --lot

   Un lot attend ses signaux pour être mesuré ; c'est ce qui débloque la suite.
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

Travaille par **groupes de 5 fiches**, sessions de codage lancées **en
parallèle**, et enchaîne les groupes tant que le quota le permet. Pour chaque
fiche `<fiche_id>` :

### 2.1 Préparer la consigne

    uv run python scripts/code_signal.py --prepare <fiche_id>

Elle est écrite dans `corpus/consignes-signaux/<fiche_id>.md` et contient
**tout** ce que le codeur a le droit de savoir : la fiche, le contrat `D07`, la
liste blanche des imports, l'interface de `signals/_common.py`, la règle `S5`.
Le module attendu est `signals/<fiche_id, les - remplacés par des _>.py`.

### 2.2 Lancer la session de codage — isolée

Outil `Agent` (type `general-purpose`), une par fiche, en parallèle, **au
premier plan** (`run_in_background: false`). Consigne à donner **mot pour
mot**, en remplaçant les deux chemins :

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

### 2.3 Figer ce qu'elle a produit — AVANT de juger

    uv run python scripts/code_signal.py --record signals/<module>.py

C'est ce qui rend « zéro retouche » (`S6`) mesurable (`L22`). **Toujours
`--record` avant `--judge`**, à chaque essai.

### 2.4 Juger

    uv run python scripts/code_signal.py --judge signals/<module>.py --fiche $(uv run python scripts/code_signal.py --fiche-path <fiche_id>)

Six conditions à tolérance zéro (`D23`) : `S1` contrat, `S2` liste blanche,
`S3` causalité, `S4` non-dégénérescence, `S5` fidélité à la fiche, `S6` zéro
retouche. **Aucun IC n'est calculé.**

### 2.5 Si le juge refuse

Renvoie le verdict **tel quel**, par `SendMessage`, **à la même session**
(son `agentId`), avec : « Corrige en réécrivant le fichier entier, à partir de
la seule consigne, mêmes règles d'isolement. » Puis reprends en 2.3.

- **Trois essais au plus par fiche.** Au troisième refus, arrête : la fiche
  est notée en échec, avec le dernier verdict, dans le compte rendu (§ 4), et
  tu passes à la suivante. Un échec est un résultat, pas une panne.
- Regarde **comment** un signal devient vert (`L28`) : par la faute corrigée,
  ou par un contournement. Un contournement se signale, il ne se garde pas en
  silence.

---

## 3. Ce que tu n'as PAS le droit de faire

Ce ne sont pas des recommandations.

- **Ne jamais écrire ni corriger un signal toi-même.** Pas une ligne. Une
  retouche à la main casse `S6` et invalide le signal. Un signal faux se
  refait par le codeur.
- **Ne jamais donner au codeur autre chose que sa consigne** : ni un signal
  voisin, ni une hypothèse, ni un indice sur « ce qui marche ». Il recopierait
  au lieu de coder (`D23`, `F42`).
- **Ne jamais calculer un IC, ni lancer une mesure.** Pas de `evaluate()`, pas
  de `scripts/measure_*.py`, pas de corrélation « pour voir ». Tout IC s'écrit
  au registre et compte au dénominateur (invariant III) ; un signal regardé
  avant sa mesure officielle ne peut plus entrer dans un lot (`D28`).
- **Ne jamais lancer les portes 03, 04 ou 06** : elles écrivent au registre
  (`L25`). Les portes 05, 07, 08 et `gate_09.py --check` sont en lecture seule.
- **Ne jamais écrire ni modifier une hypothèse** (`hypotheses/H*.md`), ni un
  lot (`hypotheses/LOT-*.json`) : ce sont des étapes à part, avant la mesure,
  qui ne sont pas celles du codeur. `HYPOTHESIS` vaut `None` dans chaque
  signal produit.
- **Ne jamais toucher** au harnais (`harness/`), au registre
  (`registry/tests.jsonl`), à la tranche `holdout`, ni aux fiches.
- **Ne jamais modifier `signals/PRODUCED.json` à la main** : il n'est écrit
  que par `--record`.

---

## 4. En fin de session

1. Relance le juge de la porte, en lecture seule :

       uv run python scripts/gate_08.py

2. Écris le compte rendu dans `wiki/log.md` (une ligne datée, en ajout) :
   fiches traitées, signaux verts, essais au total, **chaque échec avec sa
   raison**, et ce qui reste à coder (`--list`).
3. Mets à jour `ETAT.md` : signaux produits, signaux restant à coder, et si
   le goulot est devenu les fiches (§ 1, point 3).
4. Commite et pousse.

---

## 5. Reprendre après une coupure

Tout est reprenable : `--list` ne montre que les fiches **sans** signal, et
`signals/PRODUCED.json` garde chaque essai. Une session de codage coupée en
cours laisse soit rien, soit un fichier non inscrit : dans le second cas,
**supprime ce fichier non inscrit** et relance la fiche depuis 2.2, avec une
session neuve.

---

## 6. Ce qui vient après, et qui n'est PAS ce travail

Un signal codé n'est pas un signal testé. Pour qu'il soit mesuré, il faut, dans
cet ordre et **hors de la session de codage** : écrire son hypothèse
pré-enregistrée, le déclarer dans un lot clos, produire la matrice de
corrélation du lot, puis mesurer une fois chaque hypothèse (`D25`, `D28`,
`D29`).

| Étape | Outil |
|---|---|
| 8. Hypothèses | `scripts/hypotheses_lot.py --status` puis `--write`, **commiter aussitôt** |
| 9. Matrice de corrélation | `scripts/lot_correlations.py --check` puis sans option |
| 10. Mesure | `scripts/measure_lot.py --check` ; `--run --je-mesure` seulement après la décision de harnais groupée, qui renseigne `HARNAIS_DU_LOT` |
| Porte 09 | `scripts/gate_09.py` |
