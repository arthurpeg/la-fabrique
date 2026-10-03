# D49 — Un signal se juge et se compare à son horizon, pas à 30 barres

**Date :** 2026-10-03
**Phase :** 09
**État :** prise — demande de l'opérateur (« ce n'est pas normal que ce soit
obligatoirement 30 horizon bars, ça devrait être comme la fiche le décide ») ;
modifie l'outillage de `D23` et `D34`, ne touche ni au harnais ni au registre

## La question

Le chiffre 30 intervenait à trois endroits :
- la consigne imposait aux codeurs `scores(panel, cells=None, horizon_bars: int = 30)` ;
- le juge (`score_signal.py`) appelait tous les signaux à 30 barres ;
- le double codage (`double_codage.py`) faisait de même.

La mesure (`measure_lot.py`), elle, prend l'horizon de l'hypothèse. À quel
horizon un signal doit-il donc être jugé et comparé, et faut-il garder la
valeur par défaut ?

## Les options

1. **Laisser 30 partout.** Rien à changer. Mais un double codage concordant à
   30 barres ne dit rien d'un signal mesuré à 15 minutes, et le défaut
   imposé fait refuser `S5` au hasard. Sur la session du 2026-10-03, quatre
   codages sur dix ont été refusés sur ce seul nombre, puis sont passés par un
   contournement (`L34`).
2. **Ne retirer que le défaut de la signature.** Cela supprime le faux refus,
   mais le juge et le double codage restent à un horizon qui n'est pas celui
   de la mesure.
3. **Retirer le défaut, et juger et comparer à l'horizon du signal**, lu
   dans l'hypothèse quand elle existe, sinon dans la fiche, sinon à
   l'ancrage par défaut. Le double codage inscrit l'horizon auquel il a été
   fait, et un double codage fait à un autre horizon que celui de
   l'hypothèse ne vaut plus pour le lot.
4. **Exiger l'hypothèse avant le codage**, pour toujours avoir l'horizon
   déclaré. Cela retourne l'ordre de `D41`, où l'hypothèse s'écrit une fois
   la fiche vérifiée, et coûte une hypothèse pour chaque fiche qui sera
   ensuite écartée.

## Le choix

L'option 3.

## Pourquoi

C'est la seule qui aligne les trois appels (juge, double codage, mesure) sur
**un même horizon**, celui sur lequel la mesure portera. L'ordre de
`D41` est conservé, puisque la fiche suffit tant que l'hypothèse n'existe pas.

L'horizon se lit dans `scripts/horizon_signal.py`, dans cet ordre :
1. l'horizon que le lot a recopié de l'hypothèse (`D42`) ;
2. le champ `horizon` de la fiche, s'il dit un horizon intraday lisible
   (minutes, heures, demi-heure, jusqu'à la clôture) ;
3. sinon 30 barres, l'ancrage par défaut de `signals/_common.run`.

« Jusqu'à la clôture » se pose à l'ancrage par défaut, comme `measure_lot.py`
le fait déjà (`D43`). La source de l'horizon est toujours imprimée avec le
nombre de barres.

La signature devient `scores(panel, cells=None, *, horizon_bars: int)`. Ce
paramètre est obligatoire et ne s'appelle que par mot-clé, et tous les
appelants du dépôt passent déjà `horizon_bars=` (vérifié). `D07` n'a jamais
exigé de valeur par défaut. Le `30` disparaît des modules produits, donc le
faux refus `S5` de `L34` aussi.

**Ce qui est sacrifié.** Le champ `horizon` d'une fiche est du texte libre,
lu par des expressions régulières : il peut être mal lu (par exemple « à 15
minutes avant l'annonce »). Le garde-fou est double : la source est imprimée,
et `codage_verifie.concordance` refuse un double codage fait à un autre
horizon que celui de l'hypothèse. Une mauvaise lecture coûte donc un double
codage à refaire, jamais une mesure fausse. Le cas inverse a aussi un coût :
une fiche sans horizon intraday reste jugée à 30 barres, sans plus de raison
qu'avant.

## Ce que ça verrouille

- `scripts/horizon_signal.py` (nouveau) ;
- `scripts/score_signal.py` (`--horizon-bars`, `juger`, `check_s3`) ;
- `scripts/code_signal.py` (signature de la consigne, `--judge` qui transmet
  l'horizon) ;
- `scripts/codage_verifie.py` (`inscrire_jugement` inscrit `horizon_bars`,
  `concordance` compare l'horizon du tour à celui du signal) ;
- `scripts/double_codage.py` (compare à l'horizon et inscrit `horizon_bars`
  et `horizon_source`).

**Les tours antérieurs** n'ont pas de champ `horizon_bars` et sont lus comme
faits à 30 barres, ce qu'ils étaient. Baltussen (`H05`, « 30min »,
30 barres) reste CONCORDANT, ce qui a été vérifié. Les signaux déjà produits,
écrits avec `= 30` par défaut, restent valides : `S6` interdit de les
retoucher, et les appelants passent l'horizon explicitement. Les seuils de
`D34` et la liste close de `S5` sont inchangés.

`check_signals.py`, `calibrate_coder.py` et les mesures `H01` à `H03` gardent
leur 30 : ils portent sur les étalons écrits à la main (`D06`), qui ont leurs
propres hypothèses.

## Ce qui reste ouvert

- **La porte 08** (`gate_08.py`) rejuge `signals/` contre la fiche seule, à
  30 barres, et ignore `fiches_harvest/` : elle est en panne depuis le
  2026-10-03 (`ETAT.md`). L'aligner sur `D34` et `D49` est une décision à
  part.
- **Une fiche dont l'hypothèse fixe un autre horizon** que celui jugé au
  codage devra refaire son double codage avant la mesure. Les outils le
  refusent, mais `avancer.py` ne le relance pas encore tout seul.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-03 | décision prise et appliquée | `score_signal --check` 27/27 ; Baltussen jugé à 30 barres (source `H05`), six conditions tenues, rien d'inscrit ; concordance de Baltussen toujours valide ; registre 187 → 187 |
