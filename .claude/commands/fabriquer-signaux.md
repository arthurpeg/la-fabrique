---
description: Lance la création de signaux de La Fabrique, du papier à l'IC, en orchestrant les sous-agents isolés (voisins, synthèse, recette, codeur) aussi loin que le quota le permet.
argument-hint: "[nombre de fiches, 5 par défaut]"
---

Tu es la session qui **orchestre** la création de signaux de La Fabrique. Tu
n'écris ni recette, ni synthèse, ni signal : tu lances des sous-agents isolés,
le code les juge, tu tiens le compte. Tu écris seulement les hypothèses
(`D40`), que le code juge aussi.

Objectif de cette session : traiter **$ARGUMENTS** fiches (5 si rien n'est
précisé), dans l'ordre de priorité, sans dépasser 85 % de la fenêtre de
5 heures.

## Dans cet ordre, sans en sauter

1. **Démarrage** : suis la séquence de `CLAUDE.md` (`wiki/index.md`,
   `wiki/Failed Ideas/ledger.md` en entier, `wiki/hot.md`, `ETAT.md`,
   `LECONS.md`, la décision la plus récente).
2. **Lis `scripts/CODAGE-DES-SIGNAUX.md` en entier.** C'est la procédure qui
   fait foi ; ce qui suit n'en est que le résumé.
3. **Relève le quota** et inscris-le avec `scripts/quota.py`. Au-delà de 85 % de
   la fenêtre de 5 heures, arrête-toi et dis-le.
4. **Choisis les fiches** : `uv run python scripts/code_signal.py --list --lot`
   d'abord, puis `--list`. `uv run python scripts/avancer.py --etat` dit ce qui
   bloque le lot.
5. **Pour chaque fiche**, avec les sous-agents du projet et **le seul chemin de
   la consigne** comme message :
   - **voisins (facultatif, `D53`)** : `synthese_dossier.py --candidats <id>`,
     puis `fabrique-voisins`, puis `--prepare <id>`. S'il ne reste aucun voisin
     du même mécanisme, pas de synthèse. Sinon, `fabrique-synthese`, puis
     `--record` et `--check`. La synthèse ne se code que si `--list` la propose
     (apport `nouveau`, `D52`) ;
   - **recette** : `recette.py --prepare`, puis `fabrique-recette`, puis
     `--record` **après sa réponse**, puis `--check`. Si `exact_roots` est vide,
     `ecarter_du_lot.py --preuve univers` et fiche suivante (`D38`) ;
   - **codage** : `code_signal.py --prepare`, puis `fabrique-codeur`, puis
     `--record` et `--judge`. Un refus se renvoie tel quel au même codeur, trois
     essais au plus. **Un seul codeur (`D54`)** : un module vert est vérifié ;
   - **ambiguïtés** : lis les `CHOICES` du module vert. Un choix qui tranche une
     ambiguïté que la recette laissait ouverte fait refaire la recette **une
     fois**, avec `--precisions "<question neutre>"`, par une session neuve ;
     recode si elle tranche autrement ;
   - **hypothèse** : quand `avancer.py` dit « vérifiée, hypothèse D40 à écrire »,
     écris-la au format de `D40` (modèle `hypotheses/H05-*.md`), avec le
     paragraphe de `hypotheses_lot.py --domaine <id>`, **le signe** et **un
     horizon intraday** (`D42`). Puis `hypotheses/score_hypothese.py`, commite
     aussitôt. Chaque fiche a son hypothèse, transposée si le papier ne prédit
     pas de rendement ;
   - **après chaque fiche** : `uv run python scripts/avancer.py`. Il écarte,
     relie, verse les fiches dans la base, et, **dès que le lot est complet**,
     lance les corrélations, **la mesure des IC**, la porte 09 et le tableau de
     bord. S'il s'arrête sur des corrélations négatives (BH ou BY, `D25`),
     arrête-toi et demande à l'opérateur.
6. **Consulte `fabrique-critique`** si un groupe finit mal, ou avant de changer
   quoi que ce soit au processus. Son avis ne remplace ni les portes ni une
   décision écrite.
7. **Fin de session** :
   - relève le quota avec `--depense` ;
   - `scripts/verifier_tout.py` doit finir sur `TOUT PASSE` ;
   - régénère le tableau de bord (`scripts/tableau_de_bord.py --base`) ;
   - écris la ligne de `wiki/log.md` et mets `ETAT.md` à jour ;
   - commite et pousse.

## Ce que tu ne fais jamais

Aucune ligne de signal, de recette ou de synthèse écrite par toi. Aucun IC à la
main, aucune porte 03, 04 ou 06. Rien d'autre que le chemin de sa consigne
donné à un sous-agent. Aucune modification du harnais, du registre, d'une
hypothèse existante ou d'un lot hors des outils prévus. Jamais la tranche
`holdout`.

Si un sous-agent `fabrique-*` est introuvable (session ouverte avant sa
création), arrête-toi et dis de rouvrir une session, plutôt que de le remplacer
par une session générique sans ses règles.
