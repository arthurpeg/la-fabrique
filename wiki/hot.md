---
type: hub
updated: 2026-09-17
status: genere
sources: [wiki/log.md, ETAT.md, registry/tests.jsonl]
---

# HOT — l'état courant

> [!warning] Page **générée**. Ne pas l'éditer à la main.
> `wiki/update_hot.py` la réécrit entièrement à chaque arrêt de session.
> Toute modification hors du bloc « Prochaines actions » sera perdue.
> Pour changer ce qui s'affiche ici, édite `wiki/log.md` ou `ETAT.md`.

*Régénérée le 2026-09-17.*

---

## État courant

| | |
|---|---|
| **Phase courante** | 02 — le Panel point-in-time (pas encore commencée) |
| **Dernière porte franchie** | **01**, le 2026-09-15 — `scripts/gate_01_pit.py` passe, empreintes de préfixe déposées dans `scripts/out/pit_fingerprints.json`. |
| **Décision la plus récente** | `decisions/DECISION-02-wiki.md` — un wiki tenu par l'agent sous `wiki/`, dérivé et sans autorité. N'affecte aucune porte. |
| **Tests au registre** | 0 |
| **Idées abandonnées recensées** | 12 |
| **Entrées au journal** | 1 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Dates de roulement autoritatives, et confirmation « brutes ou ajustées » | auteur des données | **phase 02** |
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | barèmes publics, à dépouiller | calibration du harnais, phase 03 |

## Prochaine action — reflet de `ETAT.md`

**Phase 02 — le Panel point-in-time.** Elle peut être préparée sans les dates de
roulement (chargement, calendrier de séance par instrument, structure du panel),
mais **sa porte ne peut pas être franchie sans elles** : la série ajustée à
rebours en dépend. Ne pas franchir « provisoirement ».

## La dernière entrée du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-16 | `setup` | Création du wiki : squelette wiki/, SCHEMA, ledger des idées abandonnées, générateur de hot.md, crochets .claude, groupes de graphe Obsidian ; DECISION-02 écrite d'abord, CLAUDE.md complété d'une section « Wiki » | wiki opérationnel, 12 idées abandonnées recensées rétrospectivement depuis D01 et LECONS.md |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 11 |
| `phases` | 4 |
| `reference` | 3 |
| `research` | 6 |
| `signaux` | 1 |

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
> Bloc **editable a la main**. Le generateur le relit et le reinjecte tel quel.
> Tout ce qui est en dehors des marqueurs est ecrase a chaque regeneration.

- _(rien d'inscrit — voir « Prochaine action » ci-dessus, qui vient de `ETAT.md`)_
<!-- NEXT-ACTIONS:END -->

---

À lire au démarrage : [[index]] puis [[Failed Ideas/ledger]] — règles permanentes de `CLAUDE.md` § Wiki.
