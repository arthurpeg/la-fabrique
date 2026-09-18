# D10 — L'empreinte du harnais porte sur le contenu, pas sur les octets

**Date :** 2026-09-18
**Phase :** 06
**État :** prise

## La question

`registry.code_hash()` est le **seul** instrument de l'interdit « ne jamais
modifier le harnais » : si le nombre bouge, `D05` déclare périmés tous les
résultats antérieurs. Or il empreinte les octets lus sur le disque, fins de ligne
comprises — et ces octets changent d'un poste à l'autre sans qu'une ligne de code
bouge.

## Les options

1. **Ne rien faire, et le documenter.** Écartée. Ce n'est pas un désagrément
   cosmétique : `gate_04_registry.py` annonce « 53 lignes périmées », c'est faux,
   et il ne bloque pas. Une alarme qui sonne pour une non-raison **s'apprend
   comme du bruit**, et le jour où le harnais changera vraiment, plus personne ne
   la lira. Le coût d'attendre est en plus croissant : la réparation est gratuite
   tant que `counted_tests()` vaut 0, et jamais après.

2. **`.gitattributes` seul.** Écartée comme suffisante. Elle traite la cause au
   bon endroit, mais laisse l'invariant suspendu à un fichier de configuration :
   une extraction qui ne l'honore pas, un outil qui réécrit autrement, et
   l'empreinte redérive sans prévenir.

3. **L'empreinte normalisée seule.** Écartée comme suffisante aussi, pour la
   raison inverse : elle rend le nombre robuste mais laisse le dépôt produire des
   octets différents selon le poste, ce qui continuera de brouiller tout ce qui
   compare des fichiers — les diffs, les revues, et le contrôle d'append-only du
   registre.

4. **Les deux.** Retenue. Elles ne se recouvrent pas : l'une supprime la cause,
   l'autre rend l'invariant indépendant de la configuration.

## Le choix

`.gitattributes` fixe `* text=auto eol=lf` pour tous les postes, et
`registry.code_hash()` replie les fins de ligne sur `\n` avant d'empreinter.

## Pourquoi

**Le diagnostic est vérifié, pas supposé.** Les trois empreintes que porte
l'histoire du projet — `8c1b6512`, `5d6ce982`, `12f9b2c1` — se reproduisent
**toutes les trois** à partir des mêmes blobs git, en ne faisant varier que
quelles fins de ligne portent quels fichiers. Sur le poste du 2026-09-18 le même
harnais valait `842a6ade`, avec six fichiers en CRLF et `costs.py` en LF. Le
contenu n'a jamais bougé ; le mélange, si. Détail : le mélange **dérive à
l'intérieur d'un même poste** d'une session à l'autre, parce qu'un fichier
réécrit par un outil ressort en LF là où git le rendait en CRLF.

**Ce qu'on empreinte doit être le contenu, jamais son encodage.** C'est `L09`
déplacée d'un cran — de la lecture vers l'empreinte — et c'est la deuxième fois
que l'encodage accuse un fichier qui n'a pas bougé. La normalisation est vérifiée
dans les deux sens : l'empreinte vaut `e9ef2087` que les sept fichiers soient
tous en LF ou tous en CRLF.

**Ce qu'on sacrifie.** L'empreinte change une fois, délibérément :
`12f9b2c1` → `e9ef2087`. Les 53 lignes antérieures du registre sont **réputées
périmées**, comme `D05` l'exige de tout changement du harnais. Le coût réel est
**nul** — aucune n'est un test compté — et c'est la **dernière fois** qu'il l'est.

## Ce que ça verrouille

Les portes 03, 04, 05 et 06 ont été rejouées sous le nouveau harnais, vertes :
41, 2 002, 29 et 25 vérifications. Le registre passe de 53 à 58 lignes
(calibrations et audits), `counted_tests()` vaut toujours **0**.

`.gitattributes` porte aussi `registry/tests.jsonl -merge` : le registre est
irremplaçable et ne doit jamais être fusionné automatiquement.

L'arbre de travail a été réécrit en LF — 114 fichiers. Aucun contenu committé
n'en est changé : les blobs git étaient déjà en LF, c'est l'extraction qui les
convertissait, et `git diff` le confirme fichier par fichier.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| L'empreinte ne couvre toujours que `harness/*.py`. C'est délibéré (`D08`, [[Failed Ideas/ledger#F22]]) : élargir reviendrait à dire que d'autres fichiers sont le harnais | à la première pièce de jugement déterministe logée ailleurs |
| Le repli ne traite que `\r\n`. Un `\r` isolé — vieux macOS — passerait encore | rien ne l'exige ; à rouvrir seulement si un tel fichier apparaît |
| `gate_04_registry.py` **signale** les lignes périmées sans bloquer. Correct tant que la péremption est rare et écrite ; à revoir si elle devenait courante | phase 09 |
