# Trier et ficher les papiers moissonnés — le tutoriel de la session qui orchestre

**À qui s'adresse ce fichier.** À toute session Claude Code lancée pour faire
passer les papiers moissonnés **du PDF à la fiche**, aujourd'hui comme dans six
mois. Il est générique : il ne vise aucun papier en particulier. Il dit comment
trier et ficher **le plus grand nombre possible** de papiers sans jamais
tricher. La suite — de la fiche au signal vérifié — est
`scripts/CODAGE-DES-SIGNAUX.md`.

**Le rôle de la session qui lit ce fichier : orchestrer.** Elle prépare les
consignes, lance des **sessions séparées** (trieurs, extracteurs), fait juger,
et tient le compte. **Elle ne rend jamais elle-même un verdict de tri, et
n'écrit jamais une fiche.**

Les règles viennent de `D15` (l'échelle du tri), `D16` (le juge de
l'extraction), `D18` (le texte qui fait foi), `D20`/`F47` (le moissonné
n'entre jamais dans `G1`-`G4`), `D22` (la promotion), `D33` (la pertinence) et
de l'invariant I : **l'IA propose, le code déterministe tranche.**

---

## 0. Avant de commencer

1. Suis la séquence de démarrage de `CLAUDE.md` (wiki, `ETAT.md`, `LECONS.md`).
2. **Où on en est** :

       uv run python scripts/statut_papiers.py
       uv run python corpus/tri_en_masse.py --status
       uv run python corpus/extract_fiche_harvest.py --list

3. **Quota** : regarde l'usage (outil `get_usage`, ou la carte d'usage). Ordres
   de grandeur : un lot de tri de 30 papiers ≈ 40 000 tokens ; une fiche ≈
   170 000 (elle lit le papier entier). Ne lance jamais un groupe qui ferait
   dépasser **85 %** de la fenêtre de 5 heures. **Inscris le quota avant et
   après chaque groupe** (`scripts/quota.py --nom <compte> …`, avec
   `--depense <tokens>` après) : c'est ce qui calibre la conversion en papiers
   du tableau de bord.
4. **Aucun réseau n'est nécessaire** pour trier ni pour ficher : le tri lit les
   PDF locaux, l'extraction lit `corpus/text/`. Seule la promotion télécharge.

## 0 bis. Les sous-agents du projet — à utiliser en priorité

`fabrique-trieur` (sonnet) et `fabrique-extracteur` (opus), définis dans
`.claude/agents/`, portent leurs règles d'isolement et n'ont que Read et Write.
Lance-les avec **le seul chemin de la consigne** comme message. Une session
ouverte avant leur création ne les voit pas : emploie alors `general-purpose`
avec la consigne mot pour mot ci-dessous.

## 1. L'ordre de priorité

Chaque étape nourrit la suivante. Quand il faut choisir, fais **d'abord ce qui
est le plus près du signal** :

1. **ficher** les papiers promus qui n'ont pas de fiche (`--list`) ;
2. **promouvoir** les papiers retenus par le tri (`oui`, `partiel`) ;
3. **trier** les papiers jamais triés, par passages successifs.

Une fiche est ce qui manque au codage ; un tri est ce qui manque à la fiche.

---

## 2. Le tri, par passages

Le tri est un **passage** de quelques lots de 30 papiers. Les papiers que la
règle de pertinence de `D33` garde passent **en tête** ; les autres suivent :
ordonner n'est pas filtrer, tous seront triés.

### 2.1 Préparer un passage

    uv run python corpus/tri_en_masse.py --preparer --lots 5

Il écrit `corpus/consignes-triage/passage-NN/lot-MM.md` et déclare d'avance,
dans `corpus/triage_passages/passage-NN.json`, **chaque papier** du passage.
Un passage ouvert doit être versé avant le suivant.

### 2.2 Lancer les trieurs — isolés, en parallèle

Une session `Agent` par lot (type `general-purpose`, `model: "sonnet"`, au
premier plan), **toutes dans le même message**, avec cette consigne **mot pour
mot** :

> Tu es un trieur isolé. Ta seule source est ce fichier :
>
> `C:\Users\Mathis\Documents\la-fabrique\corpus\consignes-triage\passage-NN\lot-MM.md`
>
> Lis-le EN ENTIER (par morceaux avec l'outil Read). Ne lis AUCUN autre fichier
> du dépôt, aucune commande shell, aucune recherche, aucun accès web. Rends un
> verdict par papier, dans l'ordre, aucun omis, sur l'échelle `oui` / `partiel`
> / `non`, avec une raison d'une phrase. Écris le tableau JSON (et rien
> d'autre) avec l'outil Write à l'emplacement que la consigne indique. Réponds
> en une ligne : le chemin écrit et le compte oui / partiel / non.

### 2.3 Verser le passage

**Seulement quand tous les trieurs ont répondu** :

    uv run python corpus/tri_en_masse.py --verser NN

Il refuse — **sans rien verser** — tant qu'un papier manque, qu'un `id` est
recopié de travers, qu'un verdict sort de l'échelle ou n'a pas de raison.
Un lot refusé se renvoie **tel quel**, par `SendMessage`, au trieur qui l'a
écrit : « Corrige en réécrivant le fichier entier, mêmes règles. » Il ajoute
ses verdicts à `corpus/triage_harvest_verdicts.json`, et n'y réécrit rien.

**Lis la répartition par lot** qu'il affiche : un trieur bien plus sévère ou
bien plus indulgent que les autres est un signal à écrire dans le compte rendu.

---

## 3. La promotion et le texte

Quand un passage est versé :

    uv run python corpus/promote_harvest.py --fetch
    uv run python corpus/extract_text.py

La promotion copie le PDF de chaque papier retenu dans `corpus/pdf/` (`D22`) ;
l'extraction produit son texte `default` (`D18`), celui qui fait foi. Un échec
en mode `layout` seul n'empêche pas de ficher.

---

## 4. L'extraction des fiches

### 4.1 Préparer

    uv run python corpus/extract_fiche_harvest.py --prepare <fiche_id>

La consigne est écrite dans `corpus/consignes_harvest/<fiche_id>.md` : le schéma
de fiche (`D14`), l'identité de la fiche et le texte entier du papier.

### 4.2 Lancer l'extracteur — isolé

Une session `Agent` par papier (type `general-purpose`, `model: "opus"`, au
premier plan), par groupes de 5 en parallèle, avec **mot pour mot** :

> Tu es un extracteur de fiche isolé. Ta seule source est ce fichier :
>
> `C:\Users\Mathis\Documents\la-fabrique\corpus\consignes_harvest\<fiche_id>.md`
>
> Lis-le EN ENTIER (par morceaux avec l'outil Read). Ne lis AUCUN autre fichier
> du dépôt — jamais `corpus/fiches/`, `corpus/fiches_harvest/`, `signals/`,
> `hypotheses/`, `decisions/` — aucune commande shell, aucune recherche, aucun
> accès web. Chaque citation est recopiée À LA LETTRE du texte ; ce que le
> papier ne dit pas est null avec sa raison — n'invente jamais une valeur.
> Écris la fiche JSON (et rien d'autre) avec l'outil Write dans :
> `C:\Users\Mathis\Documents\la-fabrique\corpus\fiches_harvest\<fiche_id>.json`
> Réponds en une ligne : le chemin écrit et le nombre de résultats cités.

### 4.3 Figer, puis juger — dans cet ordre

**Seulement après la réponse de la session** (figer un fichier qu'elle écrit
encore inscrit un état intermédiaire) :

    uv run python corpus/extract_fiche_harvest.py --record corpus/fiches_harvest/<fiche_id>.json
    uv run python corpus/extract_fiche_harvest.py --judge corpus/fiches_harvest/<fiche_id>.json

Cinq conditions (`D16`, `F1`–`F5`), à tolérance zéro. Un refus se renvoie **tel
quel**, par `SendMessage`, à la même session : « Corrige en réécrivant le
fichier entier, à partir de la seule consigne, mêmes règles. » Puis `--record`
et `--judge` à nouveau. **Trois essais au plus** ; au troisième refus, le
papier est en échec, avec le dernier verdict, dans le compte rendu.

Une fiche verte passe ensuite à `scripts/CODAGE-DES-SIGNAUX.md` : recette,
deux codages, double codage (`D34`).

---

## 5. Ce que tu n'as PAS le droit de faire

Ce ne sont pas des recommandations.

- **Ne jamais rendre toi-même un verdict de tri, ni écrire ou corriger une
  fiche.** Pas une ligne. Une fiche retouchée casse le registre de production ;
  un verdict écrit par l'orchestrateur n'a pas été rendu par un trieur isolé.
- **Ne jamais montrer à une session autre chose que sa consigne** : ni une
  fiche voisine, ni le verdict d'un autre trieur, ni ce que « l'on cherche ».
- **Ne jamais filtrer la population du tri** par la pertinence de `D33` ou par
  un autre critère : l'ordre, oui ; l'exclusion, non. Un papier écarté sans
  verdict est un papier perdu sans trace (`L21`).
- **Ne jamais réécrire** `corpus/triage_harvest_verdicts.json`, un passage
  versé, ni `corpus/PRODUCED_harvest.json` à la main.
- **Ne jamais écrire une fiche moissonnée dans `corpus/fiches/`**, ni une
  production dans `corpus/PRODUCED.json` : cette population n'entre jamais dans
  `G1`-`G4` de la porte 07 (`D20`, `F47`).
- **Ne jamais calculer un IC** ni lancer une mesure : trier et ficher ne
  regardent aucun rendement.

---

## 6. En fin de session

1. Relance toutes les gardes, en lecture seule — elles doivent finir sur
   `TOUT PASSE` :

       uv run python scripts/verifier_tout.py

2. Écris le compte rendu dans `wiki/log.md` (une ligne datée, en ajout) :
   passages versés et leur répartition, papiers promus, fiches vertes, essais,
   **chaque échec avec sa raison**, et ce qui reste (`statut_papiers.py`).
3. Mets à jour `ETAT.md`, commite et pousse.

## 7. Reprendre après une coupure

- un passage ouvert se reprend : relance les trieurs des lots non rendus, puis
  `--verser` ;
- `extract_fiche_harvest.py --list` ne montre que les papiers promus **sans**
  fiche ;
- une fiche écrite mais non inscrite par une session coupée se **supprime**, et
  le papier repart de 4.1 avec une session neuve.
