# D54 — Un seul codeur : le double codage est supprimé

**Date :** 2026-10-06
**Phase :** 09
**État :** prise. Demande de l'opérateur : « enlève le deuxième codeur et les agents qui n'ont pas de sens, calcule lesquels sont les plus inutiles et supprime-les, réécris la technique de création par IA ». Révise `D34` (le codage vérifié) ; ne touche ni au harnais, ni au registre, ni au juge `D23`.

## La question

Chaque agent rapporte-t-il plus qu'il ne coûte ? Lesquels supprimer, et que
mettre à la place de ce qu'ils faisaient ?

## Les options

Le bilan mesuré de chaque agent, tiré des registres de production, des
journaux de `verification/` et du wiki (2026-10-06) :

| Agent | Utilisation | Résultat | Verdict |
|---|---|---|---|
| `fabrique-temoin` (second codeur) | 8 fiches, 24 essais (jusqu'à 6) | **2 concordances sur 9 fiches** (14 tours). 7 bloquées, 5 écartées du lot sans mesure. Désaccords surtout d'ambiguïtés de recette et d'outillage (`L34`, `L35`), aucune erreur de code avérée. Une session : 1,28 M tokens pour 2 fiches | **supprimé** |
| `fabrique-trieur` (PDF moissonnés) | 119 papiers | 10 `oui` (8 %), inactif depuis le 2026-09-30 | gardé : seule porte d'entrée des 3 225 PDF |
| `fabrique-synthese` | 4 synthèses | 1 codable | gardé : l'étape voulue par l'opérateur |
| `fabrique-critique` | 2 avis | 2 erreurs évitées (conflit `D42`/`D34`, seuil BH abaissé à tort) | gardé, coût minime |
| `fabrique-recette` | 8 fiches, 27 essais | empêche toute constante inventée (`S5`) | gardé |
| `fabrique-extracteur` | 41 fiches, 48 essais | 1,2 essai par fiche | gardé |
| `fabrique-codeur` | 8 fiches, 20 essais | produit les signaux | gardé |
| `fabrique-voisins` | 1 tri | 77 % d'accord avec un contrôle Opus à l'aveugle (`D53`) | gardé |

## Le choix

1. **Supprimés** : `fabrique-temoin`, `scripts/double_codage.py`,
   `verification/temoins/` (modules et registre), l'option `--temoin` de
   `code_signal.py`, les constantes et la preuve d'écart « concordance ».
   `verification/concordance.jsonl` reste, comme **archive** close.
2. **La règle d'un lot** (`codage_verifie.verifie`, `fautes_d34_du_lot`) : une
   entrée est vérifiée quand son module principal passe le juge `D23` (S1–S6)
   et porte des `CHOICES` bien formés, à son empreinte actuelle.
3. **Ce que le double codage attrapait vraiment, gardé pour moins cher** : les
   ambiguïtés laissées ouvertes par la recette. L'orchestrateur lit les
   `CHOICES` du module vert. Un choix qui tranche une ambiguïté non résolue
   fait refaire la recette **une fois**, avec `--precisions` et une question
   neutre ; on recode si elle tranche autrement
   (`scripts/CODAGE-DES-SIGNAUX.md` § 3.4).
4. **Les cinq fiches écartées du lot pour le seul double codage y reviennent**
   (`ecarts_annules` du lot, avec date et motif). Leur module principal est
   jugé vert, et aucune mesure du lot n'a eu lieu (`D28` respecté) :
   - andersen-bollerslev-1997 ;
   - bitcoin-is-not-the-new-gold ;
   - bitcoin-intraday ;
   - boyarchenko-2023 ;
   - bollerslev-2018.

   Le lot `LOT-09` repasse de n = 36 à **n = 41**, ce qui rend le seuil BH plus
   sévère. Leurs motifs d'écart nomment de vraies ambiguïtés (« le papier ne
   dit pas quel prédicteur transposer »). Elles passent par le § 3.4 avant leur
   hypothèse.
5. **La technique de création par IA est réécrite**, en une seule chaîne :
   graine → voisins et synthèse (facultatif) → recette → marché → codage →
   ambiguïtés → hypothèse → lot et mesure. Fichiers :
   `scripts/CODAGE-DES-SIGNAUX.md`, `.claude/commands/fabriquer-signaux.md`.

## Pourquoi

Un contrôle qui bloque 7 fiches sur 9 sans trouver d'erreur de code mesure
l'ambiguïté des papiers, pas la qualité du codeur. Cette ambiguïté se traite là
où elle naît, dans la recette, par une question ciblée, au lieu de doubler
chaque codage. Le juge mécanique `D23` reste la garde contre le grossier : le
regard vers le futur, les constantes inventées, la dégénérescence.

**Ce qui est sacrifié.** Une erreur d'interprétation **subtile**, que le juge ne
voit pas et que le codeur ne déclare pas dans `CHOICES`, n'est plus attrapée.
C'est la seule chose que le double codage aurait pu voir de plus. Les
registres n'en montrent aucun cas, mais ce n'est pas une preuve qu'elle
n'arrive jamais.

## Ce que ça verrouille

- `scripts/codage_verifie.py` (`verifie`), `scripts/avancer.py`,
  `scripts/ecarter_du_lot.py`, `scripts/hypotheses_lot.py` ;
- `scripts/statut_papiers.py`, `scripts/tableau_de_bord.py` et `.html`,
  `scripts/code_signal.py`, `scripts/verifier_tout.py` ;
- `hypotheses/LOT-09.json`, `.claude/agents/`, `scripts/CODAGE-DES-SIGNAUX.md`,
  `.claude/commands/fabriquer-signaux.md`.

## Ce qui reste ouvert

- Si une erreur subtile de codage apparaît un jour (un signal mesuré qui ne
  fait pas ce que la fiche dit), cette décision se rouvre.
- `fabrique-trieur` : à remplacer ou à relancer quand il faudra de nouvelles
  graines.
