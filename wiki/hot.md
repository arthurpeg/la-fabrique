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
| **Phase courante** | 03 — le harnais d'IC calibré à la main (pas encore commencée) |
| **Dernière porte franchie** | **02**, le 2026-09-17 — `scripts/gate_02_panel.py` passe ses 43 vérifications. La porte 01 a été rejouée le même jour : empreintes identiques à la ligne de base du 2026-09-15. |
| **Décision la plus récente** | `decisions/DECISION-03-panel-et-catalogue.md` — le paquet `panel/`, la coupe poussée dans le lecteur Parquet, le catalogue et son validateur, l'ajustement des roulements. Deux compléments datés du 2026-09-17. |
| **Tests au registre** | 0 |
| **Idées abandonnées recensées** | 14 |
| **Entrées au journal** | 6 |

## Ce qui bloque

| Attendu | De qui | Bloque |
|---|---|---|
| Moteur de backtest | tiers | phase 10 |
| Frais CME / EUREX, multiplicateurs de contrat | barèmes publics, à dépouiller | calibration du harnais, phase 03 |

## Prochaine action — reflet de `ETAT.md`

**Phase 03 — le harnais d'IC, calibré à la main.** C'est le juge, et la porte la
plus importante du projet : à partir d'elle, le harnais est **figé et versionné**.

Ce qu'elle exige, et que `D01` impose déjà : IC en **série temporelle, poolé**
entre instruments et entre cellules (l'IC transversal est refusé, ledger F03) ;
une statistique robuste à la corrélation contemporaine — un t de Student naïf
serait surévalué d'un facteur proche de `sqrt(9 / 4,2) ≈ 1,46` ; un **FDR dès le
premier test**, jamais un t-stat à 2 (Harvey, Liu & Zhu : `t > 3,0`) ; les **deux
comptes de largeur** affichés, donc les deux cibles d'IC — 0,018 et 0,031 —
jamais la plus flatteuse seule ; et le **modèle de coûts par cellule** en
première classe (`D01` §7).

La porte se franchit en reproduisant **à la main**, sur un cas connu, un IC que
le harnais retrouve indépendamment.

**Ce qui manquera en route :** les frais CME/EUREX et les multiplicateurs de
contrat, `null` et `todo` au catalogue. Ils ne bloquent pas l'écriture du
harnais ; ils bloquent sa **calibration en coûts**. Ne pas les deviner.

## Les 6 dernières entrées du journal

| Date | Type | Ce qui s'est passé | Résultat |
|---|---|---|---|
| 2026-09-17 | `gate` | PORTE 02 FRANCHIE : dates de roulement obtenues du fournisseur par symbology.resolve (527, facturé 0,00 $), comparées AVANT adoption (compare_rolls.py) puis déposées au catalogue ; clause 3b réécrite sur les instruments réels ; L06, L07, L08 | gate_02_panel.py 43/43 ; détection empirique mesurée à 62,8 % de rappel et 67 faux positifs ; GC n'est pas mensuel (5,07/an) ; FDAX oscille ; phase courante = 03 |
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
