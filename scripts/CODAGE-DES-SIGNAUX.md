# La création de signaux par l'IA — le tutoriel de la session qui orchestre

**À qui s'adresse ce fichier.** À toute session Claude Code lancée pour
**produire des signaux**, aujourd'hui comme dans six mois. Il dit comment
passer d'une fiche, seule ou combinée à ses voisins, à un signal **vérifié**
puis mesuré, sans jamais tricher.

**Le rôle de la session qui lit ce fichier : orchestrer.** Elle choisit les
fiches, prépare les consignes, lance des **sous-agents isolés**, les fait
juger par le code, et tient le compte. **Elle n'écrit jamais elle-même une
recette, une synthèse ou un signal.** Elle écrit seulement les hypothèses
(`D40`), que le code juge ensuite.

Les règles viennent de `D07` (le contrat de signal), `D23` (le juge du codeur),
`D34` révisée par `D54` (le codage vérifié, **un seul codeur**), `D38`
(l'univers), `D40`–`D42` (les hypothèses), `D45`–`D53` (les voisins et la
synthèse), `D25`–`D29` (les lots et leur mesure), et de l'invariant I de
`CLAUDE.md` : **l'IA propose, le code déterministe tranche.**

---

## 0. Avant de commencer

1. Suis la séquence de démarrage de `CLAUDE.md` (wiki, `ETAT.md`, `LECONS.md`).
2. **Données** : `RSL_DATA_DIR` doit être renseigné dans `.env`. Sans elles, le
   juge ne peut vérifier ni la causalité (`S3`) ni la dégénérescence (`S4`).
   **Un verdict partiel ne vaut pas un signal réussi.**
3. **Quota.** Ordres de grandeur mesurés :

   | Étape | Tokens |
   |---|---|
   | recette (lit le papier entier) | ~165 000 |
   | codage | ~80 000 |
   | tri des voisins (facultatif) | ~90 000 |
   | synthèse d'un dossier (facultative) | 60 000 à 120 000 |

   Une fiche seule coûte donc ~245 000 tokens. Ne lance jamais un groupe qui
   ferait dépasser **85 %** de la fenêtre de 5 heures. **Inscris le quota avant
   et après chaque groupe** (`scripts/quota.py --nom <compte> …`, puis
   `--depense <somme des subagent_tokens>`).
4. **Où on en est** :

       uv run python scripts/avancer.py --etat
       uv run python scripts/code_signal.py --list --lot
       uv run python scripts/recette.py --status

## 1. La chaîne, en une vue

| | Étape | Qui | Outil | Ce qui la juge |
|---|---|---|---|---|
| A | choisir la graine | toi | `code_signal.py --list --lot` | l'ordre de priorité, § 2 |
| B | combiner avec ses voisins (facultatif) | `fabrique-voisins` puis `fabrique-synthese` | `synthese_dossier.py` | le validateur de synthèse (`D52`) |
| C | recette | `fabrique-recette` | `recette.py` | `--check` (citations à la lettre) |
| D | marché du papier | toi | la recette | `D38` |
| E | codage | `fabrique-codeur` | `code_signal.py` | le juge `D23` (S1–S6) et `CHOICES` |
| F | ambiguïtés restantes | toi | `CHOICES` du module | § 3.4 |
| G | hypothèse | toi | `hypotheses/score_hypothese.py` | les sept conditions de `D40` |
| H | lot, corrélations, mesure, porte 09 | le code | `avancer.py` | `gate_09.py` |

Travaille par **groupes de 5 fiches**, sous-agents lancés **en parallèle**, et
enchaîne les groupes tant que le quota le permet. Après **chaque** fiche, lance
`uv run python scripts/avancer.py` (§ 6).

## 2. Les sous-agents du projet

Définis dans `.claude/agents/`, chargés au démarrage d'une session ouverte sur
le dépôt. Lance-les avec **le seul chemin de la consigne** comme message, rien
d'autre. Ils n'ont que Read et Write : ils ne peuvent pas fouiller le dépôt.

| Rôle | `subagent_type` | Modèle | Ce qu'il écrit |
|---|---|---|---|
| trier les voisins | `fabrique-voisins` | sonnet | les étiquettes `meme` / `autre` |
| synthèse | `fabrique-synthese` | opus | une fiche de synthèse |
| recette | `fabrique-recette` | opus | la recette citée |
| codage | `fabrique-codeur` | opus | le module de signal |
| (corpus) tri des PDF | `fabrique-trieur` | sonnet | verdicts `oui` / `partiel` / `non` |
| (corpus) extraction | `fabrique-extracteur` | opus | une fiche |

Et, **hors de la boucle isolée**, `fabrique-critique` (opus, lecture seule, avec
la mémoire du projet). Consulte-le avant de changer quoi que ce soit au
processus, et quand un groupe finit mal (refus en série). Il rend ACCEPTE,
REFUSE ou À AMENDER, avec ses sources. Son avis ne remplace ni une porte ni une
décision écrite.

Si une session ne voit pas un sous-agent (ouverte avant sa création), arrête-toi
et dis de rouvrir une session plutôt que de le remplacer par une session
générique : ses règles d'isolement ne seraient plus garanties.

## 3. La boucle, fiche par fiche

### 3.1 Choisir la graine (A)

1. **Les fiches d'un lot figé**, dans l'ordre de `code_signal.py --list --lot`.
   Un lot attend tous ses signaux pour être mesuré : c'est ce qui débloque la
   suite.
2. **Les autres fiches sans signal**, dans l'ordre de `--list`. `--list` ne
   propose une synthèse de dossier que si elle est valide et apporte du
   nouveau (`D52`).
3. **Plus rien à coder** : le goulot devient les fiches. C'est un autre travail
   (`corpus/TRI-ET-FICHES.md`) ; dis-le dans le compte rendu.

### 3.2 Combiner avec ses voisins (B, facultatif)

Quand une fiche mérite d'être complétée par ce que d'autres papiers en disent :

    uv run python scripts/synthese_dossier.py --candidats <fiche>

La recherche (`D48`) propose 30 candidats dans toute la base. Lance
`fabrique-voisins` sur `corpus/consignes-synthese/tri-<fiche>.md` : il garde les
papiers du **même mécanisme**, en lisant le début de chaque papier et ses
passages proches (`D53`). Puis :

    uv run python scripts/synthese_dossier.py --prepare <fiche>

Seuls les candidats `meme` entrent au dossier, avec leur texte figé en base.
**S'il n'en reste aucun, il n'y a pas de synthèse** : la base n'a pas de voisin
pour cette graine. Note-le et passe. Sinon, lance `fabrique-synthese` sur la
consigne, puis, **après sa réponse** :

    uv run python scripts/synthese_dossier.py --record corpus/fiches_synthese/synthese-dossier-<fiche>.json
    uv run python scripts/synthese_dossier.py --check  corpus/fiches_synthese/synthese-dossier-<fiche>.json

Le validateur exige :
- un rôle pour chaque voisin : `complete`, `confirme`, `contredit`,
  `deja_teste` ou `hors_sujet` ;
- des sources qui en découlent ;
- une citation à la lettre pour chaque voisin `complete`.

Un refus se renvoie tel quel à la même session, trois essais au plus. La
synthèse devient une fiche `synthese-dossier-<fiche>` qui suit la suite de la
boucle, **si `--list` la propose**. Une synthèse d'apport `aucun` ne se code
pas : elle referait l'hypothèse de sa graine.

Les grappes de `D39` (`scripts/synthese.py --prepare <G-…>`) suivent les mêmes
règles. Une graine déjà graine ou source d'une synthèse qui compte est refusée
dans les deux cas.

### 3.3 La recette (C) et le marché (D)

    uv run python scripts/recette.py --prepare <fiche_id>

Lance `fabrique-recette` sur `corpus/consignes-recettes/<fiche_id>.md`. Puis,
**après sa réponse**, et toujours dans cet ordre :

    uv run python scripts/recette.py --record corpus/recettes/<fiche_id>.json
    uv run python scripts/recette.py --check  corpus/recettes/<fiche_id>.json

Un refus se renvoie tel quel à la même session ; **trois essais au plus**.

La recette déclare `market.exact_roots`, les instruments qui **sont** le marché
du papier (`D38`). Vide : **ne code pas**, écarte la fiche (§ 3.6). Le marché
est absent de notre univers, et coder coûterait ~80 000 tokens pour rien.

### 3.4 Le codage (E) et les ambiguïtés restantes (F)

    uv run python scripts/code_signal.py --prepare <fiche_id>

Lance `fabrique-codeur` sur `corpus/consignes-signaux/<fiche_id>.md`. Note son
identifiant : c'est à lui, et à lui seul, que tu renverras un refus. Puis,
**après sa réponse**, toujours dans cet ordre :

    uv run python scripts/code_signal.py --record signals/<module>.py
    uv run python scripts/code_signal.py --judge  signals/<module>.py

Le juge applique six conditions à tolérance zéro (`D23`) :

| | Condition |
|---|---|
| `S1` | le contrat du module est respecté |
| `S2` | les imports sont dans la liste blanche |
| `S3` | causalité : aucun regard vers le futur |
| `S4` | les scores ne sont pas dégénérés |
| `S5` | chaque constante vient de la fiche ou des valeurs de sa recette |
| `S6` | zéro retouche depuis la production |

Il exige aussi `CHOICES`, les choix écrits du codeur (`D34`). Le verdict est
inscrit dans `verification/jugements.jsonl`. **Un module vert à son empreinte
actuelle est un signal vérifié** (`D54`) : il peut entrer dans un lot.

Un refus se renvoie **tel quel**, par `SendMessage`, au codeur : « Corrige en
réécrivant le fichier entier, à partir de la seule consigne. » **Trois essais
au plus.** Regarde **comment** un module devient vert (`L28`). Il doit l'être
parce que la faute est corrigée. Un contournement du juge, au contraire, se
signale.

**Les ambiguïtés restantes — ce que le double codage attrapait.** Quand le
module est vert, lis ses `CHOICES`. Un choix qui tranche un point que la
recette avait relevé comme **ambigu sans résolution** change peut-être le
signal : une fenêtre, une normalisation, un signe, une séance, le prix de
référence d'un rendement. Dans ce cas, et **une seule fois** par fiche :

1. écris la question en une phrase neutre, sans réponse ;
2. refais la recette par une **session neuve** :
   `recette.py --prepare <fiche_id> --precisions "<la question>"`, puis
   `--record` et `--check` ;
3. si la recette tranche autrement que le codeur, recode par une **session
   neuve** (le module précédent sera remplacé et rejugé).

Si le papier ne tranche pas, le choix du codeur reste, écrit dans `CHOICES` :
c'est un résultat, pas une panne.

### 3.5 L'hypothèse (G)

Quand `avancer.py` signale « vérifiée, hypothèse D40 à écrire », écris-la
**toi-même** au format de `D40` (modèle : `hypotheses/H05-*.md`) :
- dans « Le domaine », le paragraphe que donne
  `uv run python scripts/hypotheses_lot.py --domaine <fiche_id>` ;
- le **signe** (monte, baisse) et un **horizon intraday** lisible (`D42`).

Pour un papier sans prédiction de rendement, transpose son idée et dis-le dans
« Ce qui n'est pas affirmé ici ». Puis
`uv run python hypotheses/score_hypothese.py` (sept conditions), **commite
aussitôt**, et relance `avancer.py`, qui relie l'hypothèse au lot (`D41`). Tu
n'écris jamais une seconde hypothèse pour une fiche qui en a déjà une.

### 3.6 Une fiche en échec

Un échec se note dans le compte rendu avec sa raison. Si la fiche est dans un
lot dont la mesure n'a pas commencé :

    uv run python scripts/ecarter_du_lot.py <fiche_id> --preuve juge|recette|univers --motif "<raison>"

puis **commite aussitôt** : la date du commit prouve que l'écart précède la
mesure. Après la première mesure du lot, plus rien ne s'écarte (`D28`).

---

## 4. Ce que tu n'as PAS le droit de faire

Ce ne sont pas des recommandations.

- **N'écris ni ne corrige jamais une recette, une synthèse ou un signal
  toi-même.** Pas une ligne : une retouche casse `S6` et invalide le travail.
- **Ne donne jamais à un sous-agent autre chose que sa consigne** : ni un signal
  voisin, ni une hypothèse, ni un indice sur « ce qui marche », ni un
  résultat. Il recopierait au lieu de produire (`D23`, `F42`).
- **Ne tranche jamais une ambiguïté à la place du papier.** Tu poses la
  question (§ 3.4) ; c'est la recette, citations à l'appui, qui y répond.
- **Ne calcule jamais un IC, ne lance jamais une mesure à la main.** Tout IC
  s'écrit au registre et compte au dénominateur (invariant III). La mesure ne
  se fait que par `avancer.py`, quand le lot est complet.
- **Ne lance jamais les portes 03, 04 ou 06** : elles écrivent au registre
  (`L25`).
- **Ne touche jamais au lot** (`hypotheses/LOT-*.json`) autrement que par
  `ecarter_du_lot.py` et `hypotheses_lot.py`.
- **Ne touche jamais** au harnais (`harness/`), au registre, à la tranche
  `holdout`, aux fiches, ni aux registres de production et aux journaux
  append-only (`verification/jugements.jsonl`, `verification/concordance.jsonl`,
  archivé depuis `D54`).
- **Ne choisis ni ne refais jamais une synthèse ou une recette d'après un
  résultat de nos données.**

---

## 5. En fin de session

1. `uv run python scripts/verifier_tout.py` doit finir sur `TOUT PASSE`.
2. Relève le quota avec `--depense`.
3. Écris une ligne datée dans `wiki/log.md` :
   - fiches traitées, synthèses, recettes valides, signaux vérifiés ;
   - essais au total ;
   - **chaque échec avec sa raison** ;
   - chaque recette refaite pour une ambiguïté (§ 3.4) ;
   - ce qui reste (`avancer.py --etat`).
4. Mets à jour `ETAT.md`, régénère le tableau de bord
   (`uv run python scripts/tableau_de_bord.py --base`), commite et pousse.

## 6. La réaction en chaîne — `scripts/avancer.py`

Après **chaque** fiche, `uv run python scripts/avancer.py` fait seul, dans
l'ordre, tout ce qui ne demande plus d'IA :
- il tire et pousse les fiches de la base (`D44`) ;
- il écarte les fiches dont le marché est absent (`D38`) ;
- il relie au lot les hypothèses écrites ;
- **dès que chaque entrée du lot a son hypothèse ou a été écartée**, il lance
  la matrice de corrélation, **la mesure des IC**, la porte 09, le tableau de
  bord et un commit.

La mesure attend le lot entier : BH se calcule sur le lot clos (`D25`). Seul
arrêt volontaire : des corrélations franchement négatives, qui demandent à
l'opérateur de choisir BH ou BY. `--etat` dit ce qui bloque sans rien faire.

## 7. Reprendre après une coupure

Tout est reprenable : `avancer.py --etat`, `code_signal.py --list`,
`recette.py --status`, `synthese_dossier.py --status` disent où en est chaque
fiche, et les registres de production gardent chaque essai. Une session coupée
laisse soit rien, soit un fichier non inscrit : **supprime le fichier non
inscrit** et relance l'étape avec une session neuve.
