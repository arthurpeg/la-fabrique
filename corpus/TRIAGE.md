# Le protocole du triage

Ce que le trieur reçoit, ce qu'il rend, et à quelles conditions son passage
compte. Établi par `decisions/DECISION-15-seuil-du-triage.md`.

Le juge est `corpus/score_triage.py`. Il a été écrit et vérifié **avant** ce
fichier, et avant que le trieur existe.

---

## La règle qui passe avant les autres : qui peut être le trieur

**Une session qui a lu la colonne « implémentable » d'`AMORCE.md` ne peut pas
être le trieur.** Elle ne trierait pas, elle réciterait.

C'est la contrainte la plus facile à enfreindre sans s'en apercevoir, parce que
la séquence de démarrage de `CLAUDE.md` conduit une session à lire `ETAT.md`, le
wiki et le corpus — donc, tôt ou tard, l'étalon. Le trieur doit donc être
**une session ou un agent qui n'a vu ni la colonne, ni le § Verdict d'`AMORCE.md`,
ni `D15` § Sur l'étalon, ni ce paragraphe-ci en contexte d'un fichier qui les
contient.**

Ce qu'il reçoit, il le reçoit par `corpus/triage_input.json` — jamais en lisant
`AMORCE.md`, qui porte la réponse deux fois : dans la colonne, et dans son
§ Verdict.

> C'est de la **vigilance**, et le dépôt le sait : `F13`, `F15`, `F16` et `F25`
> ont toutes écarté un garde extérieur au motif qu'il déguisait la vigilance en
> architecture. Ici l'impossibilité par construction n'est pas atteignable — on
> ne peut pas empêcher un lecteur de lire — donc la règle est écrite, et le
> § Journal de `D15` note pour chaque passage **qui** a trié et **ce qu'il avait
> vu**. Ce qui n'est pas empêchable est au moins déclaré.

## Ce que le trieur reçoit

**`corpus/triage_input.json`, et rien d'autre du corpus.** Fabriqué
déterministiquement par `corpus/make_triage_input.py` : les 20 lignes notées
d'`AMORCE.md`, chacune privée de sa colonne verdict, et **sans les titres de
section** — le titre E dit « la famille que mes données ferment », ce qui est le
verdict lui-même.

Les lignes n'ont pas toutes les mêmes champs : les entrées 1 à 7 et 18 à 19
portent « données exigées », les autres non. C'est la forme du document, et
c'est ce que l'auteur humain avait sous les yeux.

**La règle de classement, telle qu'`AMORCE.md` l'énonce depuis la phase 01** —
elle définit les trois classes sans rien dire d'aucune entrée :

> **oui** = calculable avec `open/high/low/close/volume` à la minute, sur mes
> neuf instruments, sans donnée extérieure · **partiel** = exige une donnée que
> je n'ai pas mais qui est gratuite et obtenable (calendrier d'annonces), ou un
> univers différent dont la méthode se transpose · **non** = exige une donnée que
> je n'ai pas et qui coûte.

**Nos contraintes de données**, qui viennent de `D01` et du catalogue, jamais de
l'étalon :

- neuf futures CME Globex, barres **1 minute**, OHLCV seul ;
- grille **actif × séance** (`ASIA`, `EUROPE`, `US`), 25 cellules retenues sur 27 ;
- détention **intraday**, clôture forcée en fin de fenêtre ;
- **une seule échéance** par contrat — pas de structure de terme, pas de base ;
- **aucun calendrier** d'annonces macro dans les fichiers ;
- **aucun carnet d'ordres**, aucune donnée d'options, aucun consensus d'analystes ;
- largeur effective mesurée à **4,22 paris** pour neuf instruments — un test
  transversal en déciles n'a pas de sens ici (`F03`).

## Ce que le trieur rend

Un JSON, exactement 20 entrées, et **un motif par entrée** — le juge refuse une
entrée sans motif, parce que `D15` demande que chaque désaccord soit examiné et
non compté (`L06`).

**Gabarit — aucune entrée réelle, aucun verdict réel.** Les chevrons sont des
trous à remplir ; le bloc n'est pas du JSON valide tel quel, et c'est voulu.

```
{
  "trieur": "<qui a trié, et ce qu'il avait vu>",
  "date": "AAAA-MM-JJ",
  "entries": [
    {"entry": <numéro 1 à 20>, "verdict": "<oui|partiel|non>", "reason": "<une phrase : ce qui rend le signal calculable, ou la donnée qui manque>"},
    ...  (vingt en tout, une par numéro)
  ]
}
```

`verdict` vaut `oui`, `partiel` ou `non`. Les clés `trieur` et `date` ne sont pas
lues par le juge ; elles sont là pour le § Journal de `D15`.

> [!warning] **Pourquoi ce gabarit est vide, et doit le rester.**
> Jusqu'au 2026-09-20, cette section illustrait le format avec **deux entrées
> réelles et leur verdict juste** — l'entrée 1 en `oui`, l'entrée 18 en `non`.
> L'entrée 18 est l'un des **deux seuls `non`** de l'étalon, donc **la moitié de
> la condition B** : donner ce fichier au trieur, c'était lui donner deux
> réponses sur vingt, dans le document même qui interdit de lire les réponses.
>
> Le passage 1 ne l'a pas reçu et a classé l'entrée 18 `non` sans l'indice ; le
> défaut n'a donc rien coûté cette fois. Corrigé le 2026-09-20, **après** le
> passage et jamais pendant. Voir `L17` et `D15` § Journal.
>
> **Un exemple appartient au même périmètre que les données qu'il illustre.** Il
> se remplit de valeurs fabriquées, jamais de cas réels.

## Comment on le note

```
python corpus/make_triage_input.py          # (re)fabrique l'entrée, et l'audite
python corpus/score_triage.py verdicts.json # le juge, et les quatre conditions
```

Le juge imprime la **matrice entière**, chaque désaccord avec le motif que le
trieur a donné, puis les quatre conditions de `D15` :

| | Condition | Effectif |
|---|---|---|
| A | `oui` de l'étalon classés autrement | ≤ 1 sur 13 |
| B | `non` de l'étalon classés `oui` | 0 sur 2 |
| C | `partiel` de l'étalon en désaccord | ≤ 2 sur 5 |
| D | désaccords de deux crans (`oui` ↔ `non`) | 0 |

Les quatre valent ensemble. Trois sur quatre ne franchissent rien.

## Le premier passage fait foi

Un trieur retouché après lecture de sa matrice est un trieur **ajusté à son
étalon**, et rien ne le signalerait ensuite. Tout passage ultérieur s'inscrit au
§ Journal de `D15` avec ce qui a changé entre les deux, et le verdict final cite
le nombre de passages — comme la phase 15 citera `counted_tests()`.

**Un échec ne s'achète pas en redéfinissant le seuil** (`D13`, option 2). Il
s'écrit, et il se comprend : un désaccord peut désigner le trieur **ou** l'étalon,
et le § Journal doit dire lequel — sans jamais corriger l'étalon après coup.
