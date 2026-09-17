---
type: hub
updated: 2026-09-17
status: actif
sources: [wiki/SCHEMA.md, decisions/DECISION-02-wiki.md]
---

# INDEX — le catalogue du wiki

> **Ce fichier est lu en premier à chaque session**, avec
> [[Failed Ideas/ledger]]. C'est la règle permanente n° 1 de `CLAUDE.md` § Wiki.
>
> Il ne contient rien d'autre qu'un catalogue : une ligne par page, ce qu'elle
> dit, son statut. On y cherche, on descend dans la page, on ne lit pas tout.
>
> **Le wiki est dérivé et n'a aucune autorité.** Il pointe vers la source ; il ne
> la recopie pas. En cas de contradiction, la source gagne — `CLAUDE.md`,
> `ETAT.md`, `LECONS.md`, `decisions/`, `registry/`. Voir [[SCHEMA]] § 0.
>
> Il **ajoute** une lecture à la séquence de démarrage de `CLAUDE.md`, il n'en
> remplace aucune.

---

## Les cinq piliers

| Page | Ce que c'est |
|---|---|
| [[index]] | ce fichier — le catalogue, lu en premier |
| [[SCHEMA]] | le règlement : gabarits, enchaînements, lint |
| [[log]] | le journal, **append-only**, une ligne datée par événement |
| [[hot]] | l'état courant, **généré** — ne pas éditer |
| [[lessons]] | la synthèse transversale des leçons ; `LECONS.md` fait foi |
| [[Failed Ideas/ledger]] | **les idées abandonnées et pourquoi. À lire avant toute nouvelle piste.** |

## Phases — l'unité de travail courante

Une page par phase de l'**ordre de construction** (`ETAT.md`, phases 01→15).
`ETAT.md` fait foi ; ces pages le reflètent et l'étoffent.

- [[phases/phase-01-decision-donnees|Phase 01 — La décision données]] — univers, grille, métrique, tranches ; `franchie`
- [[phases/phase-02-panel-pit|Phase 02 — Le Panel point-in-time]] — l'impossibilité du look-ahead se fabrique ici ; `franchie` 2026-09-17
- [[phases/phase-03-harnais-ic|Phase 03 — Le harnais d'IC calibré]] — le juge, figé et versionné à partir de là ; **phase courante**, `a-faire`
- [[phases/phase-04-registre-et-holdout|Phase 04 — Le registre et le verrou du holdout]] — invariants III et V fabriqués, pas promis ; `a-faire`

> Les phases 05 à 15 n'ont pas encore de page. On les crée en s'en approchant,
> pas d'avance : une page de phase lointaine est une page qui vieillit sans être
> lue.

## Signaux — l'unité du produit fini

- [[signaux/README|Signaux — dossier vide, et c'est correct]] — pourquoi il n'y a rien ici avant la phase 08

## Concepts — pour qu'on entende la même chose

- [[concepts/cellule|Cellule]] — un couple (instrument, fenêtre de séance) ; 25 retenues sur 27. `stable`
- [[concepts/comptage-des-tests|Comptage des tests]] — un signal sur la grille = 1 test, pas 25. `stable`
- [[concepts/cout-aller-retour|Coût d'aller-retour]] — tick mesuré, frais `null`, glissement déclaré. `provisoire`
- [[concepts/ic|IC — coefficient d'information]] — en série temporelle, poolé, et produit par le seul harnais. `stable`
- [[concepts/largeur-effective|Largeur effective]] — ~4 paris pour 9 instruments ; la contrainte centrale. `stable`
- [[concepts/les-deux-ordres|Les deux ordres]] — construction contre exécution ; l'erreur la plus fréquente d'une session froide. `stable`
- [[concepts/panel|Panel]] — la couche de données : ouvert à une date, il ne peut pas lire le futur. `provisoire`
- [[concepts/point-in-time|Point-in-time]] — par construction, jamais par vigilance. `stable`
- [[concepts/porte|Porte]] — binaire ; jamais franchie « provisoirement ». `stable`
- [[concepts/registre|Registre]] — le compte des tests, irremplaçable et append-only. `stable`
- [[concepts/roulement|Roulement, recollement]] — une discontinuité de prix, pas un détail. `provisoire`
- [[concepts/tranche|Tranche]] — `pool` et `holdout` ; deux, pas trois. `stable`

## Research — les sources externes

Le corpus autoritatif est `corpus/AMORCE.md` (24 références) et, à partir de la
phase 07, `corpus/fiches/`. Ces pages commentent et relient ; elles ne remplacent
ni l'un ni l'autre.

**Aucune de ces sources n'a été lue intégralement** — statut `repere`, pas `lu`.

- [[research/bailey-2014-deflated-sharpe|Bailey & López de Prado (2014) — Deflated Sharpe ratio]] — la dernière opération du projet. `repere`
- [[research/baltussen-2021-hedging-demand|Baltussen et al. (2021) — Hedging demand and market intraday momentum]] — 60+ futures, un mécanisme explicite. `repere`
- [[research/bollerslev-2018-risk-everywhere|Bollerslev et al. (2018) — Risk everywhere]] — la justification du *pooling*. `repere`
- [[research/gao-2018-intraday-momentum|Gao et al. (2018) — Market intraday momentum]] — tête de la famille qui porte presque tout. `repere`
- [[research/harvey-2016-cross-section|Harvey, Liu & Zhu (2016)]] — `t > 3,0`, pas 2,0. `repere`
- [[research/mesfin-2026-falsification|Mesfin (2026) — Structural limits of OHLCV intraday signals]] — résultat négatif, le calibrage le plus proche. `repere`

## Reference — les routeurs

Pages qui ne contiennent **aucun fait** : seulement l'adresse du fait.
À ne pas confondre avec `reference/` **à la racine** du dépôt (documents tiers
datés, en lecture seule — voir `reference/README.md`).

- [[reference/metrique-et-comptage|Où trouver : la métrique et le comptage des tests]]
- [[reference/ou-trouver-les-couts|Où trouver : les coûts, les frais, les multiplicateurs]]
- [[reference/ou-trouver-les-donnees|Où trouver : les données]]

## Outillage

- `wiki/update_hot.py` — régénère [[hot]] ; `--lint` passe les contrôles mécaniques du [[SCHEMA]] § 3.1

---

## Les sources, qui font foi

Le wiki ne remplace aucune d'elles.

| Fichier | Ce qu'il tient |
|---|---|
| `CLAUDE.md` | la constitution : invariants, interdits, vocabulaire |
| `ETAT.md` | phase courante, portes, prochaine action |
| `LECONS.md` | les leçons numérotées, jamais réécrites |
| `decisions/` | une décision structurante par fichier |
| `registry/tests.jsonl` | **tout** IC calculé, append-only |
| `corpus/AMORCE.md`, `corpus/fiches/` | les papiers |
| `scripts/out/*.json` | les chiffres mesurés |
| `reference/` | les documents tiers, datés, en lecture seule |
