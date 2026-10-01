---
description: Lance la fabrication de signaux de La Fabrique, du début à la fin, en orchestrant les sous-agents isolés (recette, deux codeurs, double codage), aussi loin que le quota le permet.
argument-hint: "[nombre de fiches, 5 par défaut]"
---

Tu es la session qui **orchestre** la fabrication de signaux de La Fabrique. Tu ne
codes rien toi-même et tu n'écris aucune recette : tu lances des sous-agents
isolés, tu fais juger, tu tiens le compte.

Objectif de cette session : traiter **$ARGUMENTS** fiches (5 si rien n'est
précisé), dans l'ordre de priorité, sans dépasser 85 % de la fenêtre de
5 heures.

## Dans cet ordre, sans en sauter

1. **Démarrage** — suis la séquence de `CLAUDE.md` : `wiki/index.md`,
   `wiki/Failed Ideas/ledger.md` en entier, `wiki/hot.md`, `ETAT.md`,
   `LECONS.md`, la décision la plus récente.
2. **Lis `scripts/CODAGE-DES-SIGNAUX.md` en entier.** C'est la procédure qui fait
   foi ; ce qui suit n'en est que le résumé.
3. **Relève le quota** (outil d'usage de l'application) et inscris-le :
   `uv run python scripts/quota.py --nom <compte> --fenetre … --semaine … --reset-fenetre … --reset-semaine …`.
   Au-delà de 85 % de la fenêtre de 5 heures, arrête-toi et dis-le.
4. **Choisis les fiches** : `uv run python scripts/code_signal.py --list --lot`
   d'abord, puis `--list`. Écarte d'emblée celles qui ont déjà un double codage
   CONCORDANT (`uv run python scripts/double_codage.py --status`).
5. **Pour chaque fiche**, la boucle du tutoriel, avec les sous-agents du projet
   (`subagent_type`) et **le seul chemin de la consigne** comme message :
   - recette : `scripts/recette.py --prepare`, puis `fabrique-recette`, puis
     `--record` **après sa réponse**, puis `--check` ;
   - marché : si `exact_roots` est vide, `scripts/ecarter_du_lot.py --preuve univers`
     et fiche suivante — ne code pas (`D38`) ;
   - consignes : `scripts/code_signal.py --prepare <id>` et `--prepare <id> --temoin` ;
   - `fabrique-codeur` et `fabrique-temoin` **dans le même message**, en parallèle ;
   - `--record` puis `--judge` pour chacun ; un refus se renvoie tel quel à la
     même session par `SendMessage`, trois essais au plus ;
   - `scripts/double_codage.py <id>` ; si DISCORDANT, la procédure § 2.7.
   - **Après chaque fiche**, lance la réaction en chaîne :
     `uv run python scripts/avancer.py`. Elle fait seule tout ce qui ne demande
     plus d'IA : écarts pour marché absent, doubles codages prêts, hypothèses
     écrites et commitées — et, **dès que le lot est complet**, la matrice de
     corrélation, **la mesure des IC**, la porte 09 et le tableau de bord. Si
     elle s'arrête sur des corrélations négatives (choix BH ou BY, `D25`),
     arrête-toi et demande à l'opérateur.
   - **Hypothèse** : si `avancer.py` signale « vérifiée, hypothèse D40 à écrire »,
     écris-la toi-même **au format de `D40`** (prends `hypotheses/H05-*.md` comme
     modèle), avec dans « Le domaine » le paragraphe que donne
     `uv run python scripts/hypotheses_lot.py --domaine <fiche_id>` ; puis
     `uv run python hypotheses/score_hypothese.py` (sept conditions), commite
     aussitôt, et relance `avancer.py`, qui la relie au lot (`D41`). Tu
     n'écris jamais une hypothèse pour une fiche qui en a déjà une.
6. **Consulte `fabrique-critique`** si un groupe finit mal (discordances,
   refus en série) ou avant de changer quoi que ce soit au processus. Son avis
   ne remplace ni les portes ni une décision écrite.
7. **Fin de session** : relève le quota avec `--depense` (somme des
   `subagent_tokens`), `uv run python scripts/verifier_tout.py` doit finir sur
   `TOUT PASSE`, régénère le tableau de bord
   (`uv run python scripts/tableau_de_bord.py`), écris la ligne de
   `wiki/log.md`, mets `ETAT.md` à jour, commite et pousse.

## Ce que tu ne fais jamais

Aucune ligne de signal ou de recette écrite par toi. Aucun IC, aucune mesure,
aucune porte 03, 04 ou 06. Rien d'autre que le chemin de sa consigne donné à une
session isolée. Aucune modification du harnais, du registre, d'une hypothèse ou
d'un lot hors des outils prévus. Jamais la tranche `holdout`.

Si les sous-agents `fabrique-*` sont introuvables (session ouverte avant leur
création), arrête-toi et dis de rouvrir une session, plutôt que de les
remplacer par des sessions génériques sans leurs règles.
