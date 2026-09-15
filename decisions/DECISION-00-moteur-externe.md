# D00 — Le moteur de backtest est un composant tiers, non possédé

**Date :** 2026-09-15
**Phase :** 00 (amorçage)
**État :** prise

## La question

Le backtest de la phase 10 s'appuiera sur un moteur produit par un tiers, que
nous n'avons pas encore reçu. Faut-il attendre, en supposer la forme, ou
construire le nôtre — et que peut-on faire d'ici là ?

## Les options

- **Attendre le moteur et n'en rien présumer.** Le seul artefact en main est un
  document de conception ; aucune ligne de code de ce projet n'en dépend d'ici la
  phase 10.
- **Aligner dès maintenant nos schémas sur son vocabulaire.** Écartée : elle
  paie aujourd'hui, au prix de clés contraintes et parfois irrégulières, une
  interopérabilité avec un composant que nous n'avons pas, dont nous ne
  connaissons pas l'interface réelle, et qui peut ne jamais arriver.
- **Construire notre propre moteur tout de suite.** Écartée : c'est du travail de
  phase 10 fait en phase 00, avant même de savoir juger un signal.

## Le choix

Le moteur reste **externe et hors périmètre** jusqu'à la phase 10 ; son mode
d'attache — sous-module, dépendance installée, ou reprise du code — sera tranché
à ce moment-là dans une décision distincte.

## Pourquoi

Un composant qu'on ne possède pas ne contraint rien tant qu'on ne l'a pas vu.
Supposer son interface, c'est se lier à une hypothèse invérifiable dont le coût
se paierait partout — dans le catalogue, dans les fiches, dans les schémas — et
resterait à payer même si le moteur n'arrivait jamais. À l'inverse, ne rien en
présumer ne coûte qu'une chose : une conversion à écrire en phase 10, là où
l'interface sera enfin connue.

Ce qui est sacrifié : l'assurance que notre catalogue se branchera sans
adaptateur. C'est un coût borné, localisé, et payable une seule fois.

## Ce que ça verrouille

- **La contrainte d'alignement du vocabulaire tombe.** Le catalogue, les fiches
  et les schémas de ce projet emploient des clés anglaises propres, choisies pour
  elles-mêmes, sans imiter le vocabulaire du squelette RSL. `CLAUDE.md` est mis à
  jour en conséquence — la dérogation « les champs imposés par RSL gardent leur
  nom » est supprimée.
- **La phase 01 n'est plus bloquée.** L'interdit qui la subordonnait à l'arrivée
  du squelette reposait sur une prémisse fausse : le squelette décrivait notre
  moteur. Il décrit celui d'un tiers. La décision données se prend sur nos
  besoins, pas sur son format.
- `reference/rsl-squelette-v1.json` est une **référence de conception**, en
  lecture seule, datée. Les mesures qu'il contient sont les constats d'un tiers,
  sur ses données, avec son moteur : elles indiquent quoi vérifier, jamais ce qui
  est vrai ici. Voir `reference/README.md`.
- Aucun module de ce dépôt ne peut importer, appeler ou supposer le moteur avant
  la décision de phase 10.

## Ce qui reste ouvert

- **Le mode d'attache du moteur** — phase 10, décision distincte.
- **Condition de révision :** si le moteur n'arrive pas, la phase 10 change de
  nature. Elle devient « construire un moteur de backtest », et son estimation
  change en conséquence. Cette décision est alors rouverte et remplacée.
