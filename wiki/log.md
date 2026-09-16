---
type: hub
updated: 2026-09-16
status: actif
sources: [wiki/SCHEMA.md]
---

# LOG — le journal du wiki

> **Append-only.** On ajoute à la fin. On ne corrige pas une ligne, on en ajoute
> une qui la corrige — même règle que `registry/tests.jsonl` et `LECONS.md`.
>
> Format, fixe pour rester greppable (voir `wiki/SCHEMA.md` § 2.6) :
> `## [AAAA-MM-JJ] <type> | <ce qui s'est passé> | <résultat>`
>
> ```
> grep "^## \[" wiki/log.md | tail -5
> ```
>
> Ce fichier alimente [[hot]], qui est régénéré à partir de lui. Ne pas éditer
> `hot.md` : éditer ici.

---

## [2026-09-16] setup | Création du wiki : squelette wiki/, SCHEMA, ledger des idées abandonnées, générateur de hot.md, crochets .claude, groupes de graphe Obsidian ; DECISION-02 écrite d'abord, CLAUDE.md complété d'une section « Wiki » | wiki opérationnel, 12 idées abandonnées recensées rétrospectivement depuis D01 et LECONS.md
