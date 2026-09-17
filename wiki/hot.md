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
| **Phase courante** | 02 — le Panel point-in-time (commencée ; porte fermée) |
| **Dernière porte franchie** | **01**, le 2026-09-15 — `scripts/gate_01_pit.py` passe, empreintes de préfixe déposées dans `scripts/out/pit_fingerprints.json`. Rejouée le 2026-09-17 sur la machine courante : empreintes identiques. |
| **Décision la plus récente** | `decisions/DECISION-03-panel-et-catalogue.md` — le paquet `panel/`, la coupe poussée dans le lecteur Parquet, le catalogue et son validateur. Ouvre la phase 02 sans franchir sa porte. |
| **Tests au registre** | 0 |
| **Idées abandonnées recensées** | 14 |
| **Entrées au journal** | 5 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Dates de roulement autoritatives, et confirmation « brutes ou ajustées » | auteur des données — une requête `symbology.resolve` chez Databento suffit, voir la page de phase 02 | **phase 02** |
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | barèmes publics, à dépouiller | calibration du harnais, phase 03 |

## Prochaine action — reflet de `ETAT.md`

**Phase 02, ce qui est fait** (2026-09-17, `DECISION-03`) : le catalogue
(`catalogue/catalogue.yaml`, 9 instruments dans l'univers, 25 cellules, 3 `todos`
ouverts) et son validateur ; le paquet `panel/` — un Panel s'ouvre à une date, la
coupe est poussée dans le lecteur Parquet, `truncate` ne va que vers le passé, le
holdout et la tranche sont verrouillés ; `scripts/gate_02_panel.py`, qui exécute
les trois clauses de la porte.

L'**algorithme d'ajustement** est écrit et prouvé sur un cas synthétique
(`panel/rolls.py`, porte 02 clause 3a) : multiplicatif, sauts artificiels retirés,
rendements préservés, série construite en `t` égale à celle construite plus tard
à un facteur d'échelle près. Le mouvement réel de la minute de raccord, que
l'estimation ne sait pas séparer de l'artefact, est **injecté et mesuré** plutôt
qu'espéré : 5,0 bp pour 5,0 bp.

**Ce qui reste, et qui n'est pas de notre ressort :** la clause 3b — la série
ajustée des **instruments réels** — est **non vérifiable** tant que les dates de
roulement autoritatives ne sont pas au catalogue. `panel.adjusted()` lève
`RollDatesMissing` en les nommant. `gate_02_panel.py` sort en 1. **Ce qui manque
est de la donnée, pas du code** : le jour où les dates arrivent, la phase se
ferme en remplissant un champ du catalogue et en rejouant la porte.

**À la réception des dates :** comparer avant d'adopter — l'écart avec la
détection empirique mesure la méthode et fera une entrée dans `LECONS.md`
(`D01` §6).

## Les 5 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-17 | `mesure` | Deux vérifications : le raccord à 00:00 UTC tombe dans la fenêtre ASIA (19:00 NY en hiver, 20:00 en été) — pas dans la plage morte ; et les dates de roulement sont récupérables chez Databento par Historical.symbology.resolve (intervalles d0/d1/s, continuous -> raw_symbol), pas depuis nos fichiers | contrainte inscrite pour la phase 03 ; la demande à l'auteur des données devient précise |
| 2026-09-17 | `setup` | Emplacement des données fixé sur le poste de travail : RSL_DATA_DIR = C:\Users\Mathis\Desktop\Cotations (hors OneDrive) ; porte 01 rejouée sur les deux copies présentes | empreintes identiques à la ligne de base des deux côtés, catalogue valide, porte 02 inchangée (30/31) |
| 2026-09-17 | `phase` | Phase 02 complétée côté code : panel/rolls.py, l'ajustement multiplicatif à rebours (D01 §6), prouvé sur un cas synthétique — sauts retirés, rendements préservés, facteur d'échelle entre deux dates de construction, mouvement de la minute de raccord injecté et mesuré ; truncate() refuse aussi de sortir de la tranche par le bas | 30 vérifications sur 31 ; porte 02 toujours NON franchie — ce qui manque est de la donnée, pas du code |
| 2026-09-17 | `phase` | Phase 02 ouverte : D03 écrite, catalogue.yaml et son validateur, paquet panel/ (coupe poussée dans le lecteur Parquet, truncate vers le passé seul, holdout et tranche verrouillés), gate_02_panel.py ; porte 01 rejouée, empreintes identiques | 2 clauses sur 3 passent ; porte 02 NON franchie, bloquée sur les dates de roulement |
| 2026-09-16 | `setup` | Création du wiki : squelette wiki/, SCHEMA, ledger des idées abandonnées, générateur de hot.md, crochets .claude, groupes de graphe Obsidian ; DECISION-02 écrite d'abord, CLAUDE.md complété d'une section « Wiki » | wiki opérationnel, 12 idées abandonnées recensées rétrospectivement depuis D01 et LECONS.md |

Journal complet : [[log]]

## Le wiki en chiffres

| Dossier | Pages |
|---|---|
| `(racine)` | 5 |
| `Failed Ideas` | 1 |
| `concepts` | 12 |
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
