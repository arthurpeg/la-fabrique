# D14 — Le schéma de fiche, et la provenance de ce qu'une fiche recopie

**Date :** 2026-09-18
**Phase :** 07
**État :** prise

## La question

La phase 07 doit produire des fiches automatiquement. Trois existent, écrites à
la main pour la porte 06, et elles **divergent** : l'une porte
`signal_families`, une autre `method`, une troisième ni l'un ni l'autre ; aucune
n'a de champ `horizon`. Un extracteur construit sur cet exemple produirait vingt
fiches incomparables.

## Les options

1. **Généraliser les trois fiches manuelles.** Écartée. Elles ont été écrites
   pour trois besoins différents — écarter une cible, en évaluer une autre, en
   retenir une troisième — et leur forme suit ce besoin, pas l'objet. En faire
   un schéma reviendrait à graver trois accidents.

2. **Un schéma minimal — source, résultat, verdict.** Écartée. C'est ce qui
   suffit à un lecteur, pas à la chaîne : l'étape 02 devra **coder un signal**
   à partir d'une fiche, et elle aura besoin de l'horizon et de la construction.

3. **Le schéma que la constitution nomme déjà.** Retenue.

## Le choix

Une fiche porte les **six champs que `CLAUDE.md` § Le vocabulaire nomme** —
hypothèse, univers, horizon, construction du signal, résultats annoncés, ce qui
manque — plus deux que la pratique a rendus indispensables : la **source** et la
**transposabilité**. `corpus/SCHEMA.md` en donne la forme exacte,
`corpus/validate_fiches.py` la fait respecter.

## Pourquoi

**On n'invente pas le vocabulaire qu'on a déjà.** La constitution définit la
fiche depuis le premier jour ; mes trois fiches manuelles s'en sont écartées sans
le remarquer, chacune à sa façon. Le schéma n'ajoute rien : il rend obligatoire
ce qui était déjà écrit.

**La transposabilité est le champ qui a décidé de tout.** C'est lui qui a écarté
Mesfin — sa métrique est un rendement net par trade, la nôtre un IC — et lui qui
a cadré Heston, dont seul le *motif* transférait et non les magnitudes. Une fiche
qui dit ce qu'un papier affirme sans dire **ce qui en survit chez nous** est une
notice de lecture, pas un intrant de chaîne. Le rendre obligatoire coûte un
champ ; l'omettre a failli coûter une porte.

**L'horizon et la construction, parce que l'étape 02 en vivra.** Une fiche sert à
coder un signal. `andersen-bollerslev` n'en propose aucun : son
`signal_construction` vaut `null`, et le `null` porte sa raison, comme partout
ailleurs dans ce dépôt.

**`D09` s'étend ici, et c'est le même garde.** Un résultat recopié d'un papier est
une **valeur externe** au sens exact de `D09` : rien dans le dépôt ne peut la
contredire. Chaque résultat annoncé porte donc sa citation, et le validateur
vérifie que **la valeur se retrouve dans la citation** — en réutilisant
`value_in_quote`, la fonction même que `scripts/check_provenance.py` a prise en
défaut ([[Failed Ideas/ledger#F26]]). Ce qui est attrapé n'est pas la source
absente, qui se voit, mais la **faute de recopie**, qui ne se voit pas. `L14` a
montré ce qu'un chiffre recopié faux coûte quand personne ne le recalcule : une
réserve fausse pendant deux jours, et un plan bâti dessus.

**Ce qu'on sacrifie.** Les trois fiches manuelles doivent être **réécrites** au
schéma. C'est le test du schéma autant que des fiches : s'il ne sait pas exprimer
ce qu'elles disaient, c'est lui qui est faux.

## Ce que ça verrouille

`corpus/SCHEMA.md` devient pour les fiches ce que `registry/SCHEMA.md` est pour
le registre. Le validateur vit dans `corpus/`, à côté de son objet, et **hors de
`harness/`** — il ne juge aucun signal et l'empreinte du harnais ne doit pas
bouger (`D13` § Ce que ça verrouille).

**Les fiches restent versionnées.** Ce sont des résultats, pas des données :
`CLAUDE.md` § Où trouver quoi le dit déjà de `corpus/fiches/`.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Le triage** — décider qu'un papier est implémentable — n'est pas ici. C'est l'autre moitié de la porte 07, et elle exige un seuil chiffré écrit avant mesure (`L06`) | décision suivante, avant de coder le trieur |
| La **citation d'un résultat non numérique** (un signe, une direction) ne peut pas être vérifiée mécaniquement ; le validateur exige la citation, pas sa cohérence | rien ne le résout ; `L15` invite à s'en méfier |
| Le schéma ne dit rien des **figures**, dont les trois fiches manuelles n'ont rien tiré faute de les lire | phase 09, si un papier s'avère illisible sans ses figures |
