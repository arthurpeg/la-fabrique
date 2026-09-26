# D09 — La provenance des valeurs externes : ce qu'une valeur copiée doit porter avec elle

**Date :** 2026-09-18
**Phase :** 06
**État :** prise

## La question

`CLAUDE.md` interdit d'inventer une valeur de données : l'inconnu vaut `null` et
ouvre un `todo`. L'interdit dit quoi faire de ce qu'on ne sait pas ; il ne dit
rien de ce qu'on **apprend d'un tiers**. Un multiplicateur relevé sur une fiche
contrat n'est ni mesuré ni décidé : il est recopié. Rien dans le dépôt ne peut le
contredire, et une fois déposé il devient indiscernable d'une valeur inventée.

## Les options

1. **S'en remettre à l'interdit existant.** Écartée. Il ne distingue pas une
   valeur recopiée d'une valeur plausible : les deux sont des nombres non nuls
   dans un champ YAML. L'interdit protège la case vide, pas la case remplie.

2. **Exiger un commentaire YAML à côté de la valeur.** Écartée, et c'est l'état
   actuel : le `todo fees` porte URL, date et montants en prose, `roll_dates.json`
   porte un bloc structuré aux noms de champs différents. Deux formes, aucune
   imposée, et un commentaire ne se vérifie pas.

3. **Un registre `provenance` au catalogue, imposé par `catalogue/validate.py`.**
   Retenue. Une valeur externe non couverte fait échouer le validateur, comme un
   `null` sans `todo` le fait déjà depuis la phase 02.

4. **Rendre la chose impossible plutôt que refusée** — un type qui n'accepte un
   nombre externe qu'accompagné de sa source. Écartée pour la raison de
   [[Failed Ideas/ledger#F16]] : le catalogue est un fichier YAML que n'importe
   qui édite à la main. Prétendre à l'impossibilité mentirait. C'est un **garde**,
   et il est nommé comme tel.

## Le choix

Toute valeur externe du catalogue est couverte par une entrée du registre
`provenance`, qui porte `source`, `source_url`, `retrieved`, `quoted` et
`applies_to` ; `catalogue/validate.py` refuse le catalogue si l'une manque, si la
valeur déposée est introuvable dans sa citation, ou si une entrée ne couvre plus
rien.

## Pourquoi

**Les trois natures d'une valeur.** Chaque nombre du catalogue est exactement
l'un des trois, et le savoir dit comment le vérifier :

| Nature | Qui la produit | Comment on la vérifie |
|---|---|---|
| **mesurée** | notre code, sur nos données | `validate.py` la recalcule — tick, historique, statistiques de cellule |
| **décidée** | nous, par écrit | un fichier de `decisions/` — fenêtres, tranches, règle de rétention |
| **externe** | un tiers | **rien dans le dépôt** — d'où ce registre |

**`quoted` est le cœur, pas `source_url`.** Une URL juste ne rend pas le nombre
juste : c'est `L06` sous une autre forme — un compte juste n'est pas un compte de
choses justes. La citation porte les mots et les **unités du tiers**, et le
validateur vérifie que la valeur déposée s'y retrouve, séparateurs ôtés. Ce qui
est attrapé là n'est pas la source absente — elle se voit — mais la **faute de
recopie**, qui ne se voit pas. Un `125000` devenu `12500` reste un nombre
plausible pour toujours.

**La sous-catégorie qui n'a pas besoin d'entrée, et pourquoi elle est nommée.**
Une valeur externe que l'une de nos mesures peut **contredire** est corroborée :
le cycle de roulement l'est par le taux observé — c'est ainsi que `L07` a pris
`D01` §6 en défaut sur l'or, mensuel déclaré et 5,07 roulements par an —, et les
champs venus du manifeste le sont par le manifeste lui-même (`validate.py` §7).
Elles restent externes ; elles ont déjà un juge. La liste en est **close
ci-dessous**, pour qu'aucune valeur ne s'y range d'elle-même.

**Ce qu'on sacrifie.** Déposer une valeur coûte désormais une citation à
recopier, et un relevé sans citation ne vaut rien — la valeur reste `null` et le
`todo` reste ouvert. C'est le coût voulu : il rend le dépôt d'une valeur plus
cher que son abstention, dans le seul sens qui nous protège.

## Ce que ça verrouille

**Le multiplicateur a une définition, pas seulement une valeur.** Le CME l'énonce
dans des mots différents selon la classe d'actif — « $20 × index », « 100 troy
ounces », « 1,000 barrels », « 125,000 euro ». Le catalogue tient **l'unité de
contrat telle que `notionnel_usd = multiplier × prix`**, ce qui vaut pour les
neuf sans exception. Une session qui recopierait `100` pour l'or sans cette
définition produirait un notionnel en onces.

**Le piège micro/mini reste ouvert et reste écrit.** Les séries évaluées sont
celles des minis ; les contrats effectivement tradés seront des micros. Le
multiplicateur déposé est celui de la **série évaluée**, et l'écart devra être
écrit avant la phase 10 — le `todo fees` le porte déjà.

**Fichiers.** `catalogue/catalogue.yaml` gagne un bloc `provenance` ;
`catalogue/validate.py` gagne son §8 ; `catalogue/roll_dates.json` gagne le
`source_url` qui lui manquait. `harness/` n'est pas touché : l'empreinte du
harnais ne bouge pas et **aucun résultat antérieur n'est périmé**.

**Ce que ça coûterait d'en changer.** Peu. Le registre est déclaratif et le garde
tient en une section du validateur. Ce qui coûterait cher est l'inverse : déposer
les neuf multiplicateurs **sans** la convention, puis vouloir retrouver un an
plus tard d'où ils venaient.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| Les **multiplicateurs** eux-mêmes. Relevés tentés le 2026-09-18, `cmegroup.com` injoignable depuis le poste (timeout puis ECONNRESET sur trois URLs) : `todo multipliers` reste ouvert, les neuf champs restent `null` | à la première session où le site répond |
| Le caractère **all-in** du barème Lucid, et micro ou mini selon ce qui sera tradé | réponse attendue du tiers ; bloque `todo fees` |
| `slippage_bp`, valeur **déclarée** et non externe — elle relèvera d'une décision écrite, pessimiste, comme `D04` l'exige, et non de ce registre | avant toute lecture nette |
| L'extension du registre aux **fiches de papier** (`corpus/fiches/`), qui recopieront des résultats annoncés par des tiers | phase 07, si la même forme convient |

## Journal

- **2026-09-26** — **`value_in_quote` ôtait TOUTES les virgules**, et pas
  seulement les séparateurs de milliers que § Le choix désigne. Une liste collée
  par l'extraction PDF — « `17.71,18.22` » — devenait `17.7118.22` et ne
  cautionnait plus aucun de ses deux nombres (faux refus, fiche moissonnée
  `cryptocurrencies-and-momentum`) ; « `{12,6,1}` » devenait `1261` et
  cautionnait un nombre que la citation ne contient pas (faux accord, jamais
  exploité : les 35 fiches et le catalogue passent avant comme après). Corrigé
  dans `catalogue/validate.py` (`THOUSANDS`) : un séparateur — virgule,
  apostrophe, espace insécable — n'est ôté que suivi d'exactement trois
  chiffres, derrière un entier. `scripts/check_provenance.py` porte les onze
  cas nouveaux, écrits et vus échouer **avant** la correction (7 faux sur 11),
  **44 vérifications**. Rejoué vert : catalogue, `validate_fiches`,
  `check_fiches_guard`, `score_extraction --check`, portes 07 et 08, 17 fiches
  `AMORCE` sur 17, 17 moissonnées sur 18 (la dix-huitième pour `F4`, sans
  rapport). La règle de § Le choix ne change pas ; son implémentation la
  rejoint.
