# reference/

Documents externes, en **lecture seule**, chacun daté de son snapshot. Rien ici
n'est modifié par le projet : ce sont des photographies de sources dont
l'original vit ailleurs.

---

## `rsl-squelette-v1.json`

**Ce que c'est :** la référence de conception d'un **moteur tiers que nous ne
possédons pas**. Le format se déclare `rsl-squelette@1` ; le document décrit les
nœuds, primitives, compositions, contraintes et sections de spécification de ce
moteur.

**Ce que ce n'est pas :** l'auto-description de notre moteur. Nous n'avons pas de
moteur. Celui-ci a été produit par un tiers, avec son code et sur ses données, et
nous est attendu sous quelques jours. Voir
[`decisions/DECISION-00-moteur-externe.md`](../decisions/DECISION-00-moteur-externe.md).

**Provenance.**

| | |
|---|---|
| Source | `Test.json`, transmis par un tiers |
| Snapshot | 2026-09-15 (mtime du fichier source : 2026-09-15 19:57 +0200) |
| Taille | 113 717 octets |
| SHA-256 | `68a4c3eebadd8877980eba6b2c8db3f8f68ee24fc05aff25dff0a8041a6b4707` |
| Format déclaré | `rsl-squelette@1` |
| Fichier | en lecture seule. Ne pas éditer ; en cas de nouvelle version, ajouter `-v2` à côté. |

### Avertissement — les chiffres qu'il contient ne sont pas des faits acquis

Le document est truffé de mesures et de seuils : « mesuré à 90 séances sur 2 748
sur NQ », des seuils de garde, des comptages, des références à des leçons
numérotées (`L29`…) qui appartiennent au corpus du tiers, pas au nôtre.

**Ce sont les constats d'un tiers, sur ses données, avec son moteur.** Ils
indiquent *quoi vérifier* — les pièges qu'il a rencontrés sont probablement les
nôtres : demi-séances sans barre de clôture, exécution décalée d'une barre,
fenêtres en séances plutôt qu'en barres, séries exogènes qui cessent d'être
alimentées. Ils ne valent **jamais** comme mesures de ce projet. Aucun chiffre
lu ici n'est recopié dans le catalogue, une fiche ou un rapport sans avoir été
remesuré sur nos propres données.

### Comment s'en servir

Comme d'un catalogue de pièges et d'un inventaire de ce qu'un moteur de ce genre
doit savoir faire. Utile pour anticiper la phase 10 et pour reconnaître, en phase
01 et 02, les questions que les données devront pouvoir trancher (horodatage de
clôture, granularité, latence de publication, calendriers de séance).

**Le vocabulaire de ce document ne s'impose pas au nôtre.** Nous n'avons pas de
contrainte d'interopérabilité avec un moteur que nous n'avons pas : le catalogue
et les schémas de ce projet emploient des clés anglaises propres, choisies pour
elles-mêmes. Voir `CLAUDE.md`, « Conventions ».
