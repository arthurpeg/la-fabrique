# H08 — Le rendement d'un quart d'heure se retourne au suivant

**Écrite le :** 2026-09-29, avant toute mesure sur nos données
**fiche :** `high-frequency-return-and-risk-patterns-in-u-s-s-W4301430573` (`corpus/fiches_harvest/high-frequency-return-and-risk-patterns-in-u-s-s-W4301430573.json`)
**signal :** `high-frequency-return-and-risk-patterns-in-u-s-s-W4301430573` — *non encore codé*
**signe attendu :** −1
**tranche :** `pool` uniquement, `asof` 2023-12-29 20:00 UTC (`D29`)
**écrite par :** session 2026-09-29, sous `D40`. Contamination déclarée : elle a lu `ETAT.md`, le wiki et les fiches. Aucun IC ne porte sur ce signal au registre (`D28` vérifié).
**Statut :** pré-enregistrée, non mesurée

## Ce qui est affirmé

À l'intérieur d'une fenêtre de séance, le rendement des **quinze dernières
minutes** prédit **négativement** le rendement des **quinze minutes suivantes**,
sur le même instrument.

Le signe est **négatif**, et c'est la seule des onze hypothèses de ce lot dont il
l'est. Le score pré-enregistré est le **rendement du quart d'heure écoulé**,
tel quel, non retourné : l'affirmation porte le signe, pas la construction. Un
signal qui renverserait le score pour afficher un signe positif dirait la même
chose en rendant le pré-enregistrement invérifiable.

## Le domaine

- **Univers :** les 25 cellules retenues (`D01` §3), chacune jugée pour elle-même.
- **Horizon :** 15 minutes, à l'intérieur de la fenêtre de séance, avec clôture
  forcée à la fin de la fenêtre.
- **Tranche :** `pool` uniquement. Le `holdout` reste scellé (invariant V).
- **Plusieurs observations par séance et par cellule** — une par quart d'heure
  dont l'horizon tient dans la fenêtre. C'est la **seule** de ces onze hypothèses
  qui produise plus d'une observation par séance, donc celle où la **déflation de
  recouvrement** de `D11` a une chance de mordre pour de bon : les observations
  sont adjacentes, pas espacées de 415 barres.
- **Données :** OHLCV à la minute, agrégé en quarts d'heure.

## Ce qui est attendu, en chiffres

| | |
|---|---|
| Signe de l'IC | **négatif** |
| Magnitude plausible | **−0,04 à 0** en IC de Spearman |
| Cible `D01` §2 | 0,018 et 0,031 **en valeur absolue** |

**Ce que le recouvrement va coûter, et il faut l'écrire avant.** `F30` a mesuré
qu'un facteur de déflation de 5,48 transforme un `t` naïf de 4 en 0,5. Ici les
observations se touchent : le facteur sera mesuré par le harnais (`D11`), pas
supposé, et il peut être grand. Un IC de −0,03 avec un `t` naïf confortable peut
finir sous 2 après déflation, et ce ne sera pas une anomalie.

## Ce que le papier annonce, et d'où ça vient

| Résultat | Valeur |
|---|---|
| `ar1_return_coef_consumer_staples` | -21.52 |
| `ar1_return_all_negative_significant` | — |
| `decision_tree_score_all_days_min_energy` | 0.671 |
| `decision_tree_score_all_days_max_communication` | 0.727 |
| `session_correlation_min` | 0.51 |

**Ce qui fonde le signe est la deuxième ligne, et elle est qualitative** : le
coefficient AR(1) des rendements à 15 minutes est **négatif et significatif pour
les onze secteurs**, sans exception. C'est un constat de signe uniforme, et c'est
ce qui autorise à pré-enregistrer −1 plutôt que de tirer au sort.

**Ce qui ne fonde rien : les deux scores d'arbre de décision.** La fiche écrit
que le « score » de 0,671 à 0,727 **n'est pas défini** — ni métrique, ni découpage
apprentissage/test, ni hyperparamètres, ni variables d'entrée. Un chiffre dont on
ne sait pas ce qu'il mesure ne prédit rien, et il est cité ici pour être écarté
explicitement, pas pour appuyer l'hypothèse.

## Ce qui la contredirait

- Un IC poolé **positif** avec un `t` final au-delà de **2** : la continuation au
  lieu du retournement, et l'hypothèse est fausse telle qu'écrite.
- Un `t` final sous **2** en valeur absolue : rien à distinguer du bruit.
- Un IC négatif qui **disparaît après la déflation de recouvrement** de `D11` :
  ce n'est pas un signal, c'est le même mouvement compté plusieurs fois. C'est
  l'issue la plus probable au vu de `F30`, et elle est écrite avant la mesure.
- Un IC négatif porté par **une ou deux cellules sur 25** : accident
  d'instrument, quand le papier annonce le signe sur **11** secteurs sur 11.
- Un IC net négatif au coût **borne haute** de `D26` — et ici la question est plus
  dure qu'ailleurs, un signal à horizon de 15 minutes tournant bien plus vite
  qu'un signal à une observation par séance.

## Ce qui n'est pas affirmé ici

Le **motif en U** — premiers et derniers quarts d'heure les plus volatils,
rendements convergeant vers zéro au milieu — n'est pas une hypothèse de rendement
mais une forme de volatilité : c'est ce que `H04` a déjà répliqué sur nos données
sous `D13`, **sans produire aucun IC**, et cela reste hors du harnais.

Le **rendement overnight négatif** et l'**arbre de décision** ne sont pas
affirmés non plus : le premier suppose un gap d'ouverture que nos contrats à
session quasi continue n'ont pas sous la même forme, le second n'est pas
reproductible faute de spécification.

Le conditionnement par **jour de la semaine**, que le papier explore, produirait
un score à cinq valeurs au plus : le contrôle de dégénérescence du harnais le
rejetterait avant tout IC. C'est un régime, phase 13.
