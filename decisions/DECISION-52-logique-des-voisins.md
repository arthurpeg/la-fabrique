# D52 — La synthèse dit le rôle de chaque voisin, et ne refait jamais un test

**Date :** 2026-10-05
**Phase :** 09
**État :** prise. Demande de l'opérateur : « vérifie qu'il prend bien les voisins cohérents et adjacents, il ne doit pas prendre les mêmes, le sous-agent doit avoir une logique ». Complète `D45`, `D47` et `D48`.

## La question

Un audit de la recherche des voisins et de la synthèse (`D47`) a trouvé quatre
défauts :

1. **Des voisins déjà testés.** Sur la graine « momentum intraday mondial », 5
   voisins sur 10 avaient déjà leur hypothèse (H04, H05, H10, H11, H13), et rien
   ne le disait à l'agent. Une synthèse pouvait refaire l'un de ces tests. C'est
   arrivé avec Baltussen, qui refaisait H02/H05.
2. **Le même papier sous un autre titre.** La graine n'était écartée que par son
   titre exact.
3. **Des synthèses qui se recoupent.** A avec B, puis B avec A, ou une grappe
   `D39` qui refait une synthèse de dossier.
4. **Un agent sans logique imposée.** Il « pouvait » ignorer un voisin, et la
   règle « pas d'apport, pas de code » n'était qu'une phrase dans la commande.

## Le choix

- **`voisins.py`** :
  - la graine s'écarte par son identifiant en base, ou par un titre presque
    identique (Jaccard des mots ≥ 0,85) ;
  - deux copies d'un même papier parmi les voisins ne comptent qu'une fois ;
  - chaque voisin porte `hypothesis`, la référence de son hypothèse s'il en a
    une (lot figé et `H*.md`).
- **`synthese_dossier.py --prepare`** :
  - il refuse une graine déjà graine ou source d'une autre synthèse ;
  - la consigne marque chaque voisin « déjà testé » ou « déjà source » ;
  - elle dit si la graine a déjà son hypothèse.
- **La logique de l'agent, imposée par le validateur.** Chaque voisin reçoit
  **un** rôle d'une liste fermée, avec sa raison :
  - `complete` : il apporte un élément cité absent de la graine ;
  - `confirme` ;
  - `contredit` : l'effet inverse ou absent ;
  - `deja_teste` ;
  - `hors_sujet`.

  Les questions se posent dans cet ordre : même mécanisme ? déjà testé ?
  contredit ? complète ? Le validateur vérifie que :
  - tous les voisins ont un rôle ;
  - `sources` = la graine + les voisins `complete`, `confirme` et `contredit` ;
  - `apport` vaut `nouveau` si et seulement si un voisin est `complete` ;
  - chaque voisin `complete` a au moins un résultat cité de son texte.
- **`code_signal.py --list`** ne propose au codage une synthèse de dossier que
  si elle est valide et que son apport est `nouveau`.
- **`synthese.py --prepare`** (`D39`) refuse une grappe dont un membre est
  déjà dans une synthèse.

## Pourquoi

Le danger n'est pas qu'une synthèse soit mauvaise : le validateur et la mesure
le diraient. Le danger est qu'elle **refasse un test déjà fait**. Ce serait un
test corrélé de plus au registre, et donc un seuil plus sévère pour tous, sans
idée nouvelle. La logique par rôles rend chaque décision de l'agent lisible et
vérifiable.

**Ce qui est sacrifié.** La synthèse Baltussen du 2026-10-02 ne porte pas de
rôles : elle est désormais refusée, donc non codable. C'était déjà la
conclusion de `D47`.

## Ce que ça verrouille

`scripts/voisins.py`, `scripts/synthese_dossier.py` (`ROLES`), `scripts/synthese.py`,
`scripts/code_signal.py`, `.claude/commands/fabriquer-signaux.md`.

## Ce qui reste ouvert

- **La cohérence de la recherche reste moyenne.** Sur Lucca-Moench, 7 voisins
  sur 10 sont `hors_sujet`, à juste titre et pour des raisons précises
  (« Price Drift Before U.S. Macroeconomic News » suit le sens de la surprise,
  un autre mécanisme). L'agent filtre bien ; la recherche, elle, propose
  encore trop de papiers du même thème mais d'un autre mécanisme.
- Le seuil de Jaccard (0,85) n'a pas d'étalon. Il est choisi pour qu'« Evidence
  from China » et « Global evidence » restent deux papiers.

## Journal

| Date | Quoi | Résultat |
|---|---|---|
| 2026-10-05 | garde de recoupement | `--prepare` sur le momentum intraday mondial refusé (déjà source de `synthese-g-a9d7ec`) ; `synthese.py --prepare G-e6c338` refusé (Kurov et Lucca déjà dans la synthèse ci-dessous) |
| 2026-10-05 | synthèse Lucca-Moench 2015, 10 voisins | valide au premier essai (118 539 tokens) : 1 `complete` (devises, « Exchange Rates and Monetary Policy Uncertainty »), 2 `contredit` (Kurov 2021, Hu et al. : effet disparu sur la période récente, qui couvre notre pool), 7 `hors_sujet` ; apport `nouveau`, donc codable |
| 2026-10-05 | trois défauts corrigés après audit | **(6)** seule une synthèse qui peut devenir un test retient ses papiers (valide, et apport `nouveau` pour un dossier) : 15 papiers bloqués → 7 (Baltussen, crypto momentum et leurs voisins libérés) ; **(7)** chaque papier utilisé est aussi suivi par son identifiant en base (`paper:<id>`), un voisin `base-…` fiché plus tard reste reconnu ; **(8)** « déjà testé » se lit dans la fiche que chaque `H*.md` déclare (`**fiche :**`) ou dont il cite le chemin, plus par une recherche de nom dans le texte (`lucca-moench-…` est contenu dans `synthese-dossier-lucca-moench-…`). La garde de `synthese.py` (`D39`) suit la même règle |
