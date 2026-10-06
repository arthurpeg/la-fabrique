# D55 — Une seule lecture du papier pour la fiche et la recette ; le tri couvre la base

**Date :** 2026-10-06
**Phase :** 09
**État :** prise. Choix de l'opérateur : « oui, une seule lecture », et trier « les 1 874 de la base ». Révise `D16` (qui écrit la fiche) et `D34` (qui écrit la recette d'un nouveau papier) ; ne touche à aucun validateur.

## La question

L'opérateur a relevé que la chaîne se nourrissait mal : 55 fiches pour 1 925
papiers en texte intégral dans la base, et 119 papiers triés sur 3 117 PDF.
Comment faire entrer plus de papiers sans multiplier le coût ?

## Le constat

Coûts mesurés, par papier :
- **trier** (`fabrique-trieur`) : environ 1 000 tokens, sur passages ;
- **ficher** (`fabrique-extracteur`) : environ 170 000 tokens, papier entier ;
- **la recette** : environ 165 000 tokens, **en relisant le même papier entier**.

Le tri est donc le filtre bon marché qui manquait, et la double lecture est un
doublon.

## Le choix

1. **`fabrique-lecteur`** remplace `fabrique-extracteur` : il lit le papier une
   fois et écrit la fiche, puis sa recette. La consigne
   (`corpus/lecture_unique.py --prepare`) assemble les deux consignes
   existantes **sans en changer une règle**. Le texte n'y figure qu'une fois.
   Chaque fichier garde son validateur : `extract_fiche_harvest.py --judge`
   pour la fiche, `recette.py --check` pour la recette.
2. **`fabrique-recette` reste** pour la recette d'une fiche existante (les fiches
   du lot) et pour une recette refaite sur une ambiguïté (`--precisions`, `D54`).
3. **Le tri porte sur les papiers de la base** : `tri_en_masse.py --preparer --base`
   ne garde que les papiers moissonnés en texte intégral dans la base, dans
   l'ordre de similarité aux fiches (`D33`, `D39`). Il y en a 1 817 à trier.

## Pourquoi

Une graine coûte désormais ~170 000 tokens au lieu de ~335 000 : deux fois
plus de graines pour le même quota. Le tri, à environ 1 000 tokens par papier,
évite de lire en entier les papiers sans signal possible : au premier passage,
118 sur 150 ont été jugés `non`.

**Ce qui est sacrifié.** La recette n'est plus écrite par une session qui n'a pas
rédigé la fiche. Les deux validateurs restent mécaniques et indépendants, et
chaque citation de la recette est encore vérifiée à la lettre dans le texte.

## Ce que ça verrouille

`corpus/lecture_unique.py`, `.claude/agents/fabrique-lecteur.md`,
`corpus/tri_en_masse.py` (`--base`), `corpus/TRI-ET-FICHES.md` § 4,
`scripts/CODAGE-DES-SIGNAUX.md` § 2.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-06 | passage 02 du tri, 150 papiers de la base | 2 `oui`, 30 `partiel`, 118 `non` ; 148 317 tokens ; 5 trieurs de sévérité égale |
| 2026-10-06 | tri de la base terminé, passages 02-14 | 1 874 papiers en texte intégral de la base, tous triés : 15 oui, 259 partiel, 1 600 non. Aucun papier retiré de la base (consigne de l'opérateur : le tri juge, il ne supprime ni ne met à l'écart). Rendement décroissant avec l'ordre sémantique : 2 oui au passage 02, 0 à partir du 09 sauf 11 et 12 (1 chacun). Défaut corrigé : un travail sans identifiant OpenAlex (noté None) bloquait le versement (clé comparée en texte, DOI ou titre en repli) |
