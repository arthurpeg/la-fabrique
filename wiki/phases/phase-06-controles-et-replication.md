---
type: phase
updated: 2026-09-17
status: en-cours
phase: 06
gate: un signal dégénéré est rejeté avant le harnais ; le harnais réplique un résultat publié connu
sources: [ETAT.md, decisions/DECISION-08-controles-automatiques.md, harness/controls.py]
---

# Phase 06 — Contrôles automatiques et réplication

**Ouverte le 2026-09-17. NON FRANCHIE.** Sa clause 1 est franchie
(`scripts/gate_06_controls.py`, 25 vérifications) ; sa clause 2 ne l'est pas, et
une porte à moitié franchie est une porte non franchie.

## La porte, en deux clauses

1. **Un signal volontairement dégénéré — constant, ou presque vide — est rejeté
   avant d'atteindre le harnais d'IC.** Franchie.
2. **Le harnais réplique un résultat publié connu, contrôles compris, sans
   intervention.** Première cible : la falsification de Mesfin (2026). Non
   franchie, et bloquée — voir plus bas.

## Clause 1 — ce qui a été construit

`harness/controls.py`, **dans** le harnais et non à côté. La raison est facile à
manquer : `registry.code_hash()` n'empreinte que `harness/*.py`, donc un seuil
modifié une ligne plus loin changerait les rejets sans changer l'empreinte, et
deux résultats incomparables porteraient le même numéro de juge
([[Failed Ideas/ledger#F22]]).

Les contrôles tournent **avant que le jeton soit pris**. Un signal rejeté n'a
produit aucun IC : il ne consomme aucune ligne, et le dénominateur ne se remplit
pas de tests qui n'ont jamais eu lieu.

| Contrôle | Seuil | Effet |
|---|---|---|
| score constant | moins de 2 valeurs distinctes | cellule rejetée |
| quasi constant | moins de 10 % de valeurs distinctes | cellule rejetée |
| trop peu d'observations | moins de 30 | cellule rejetée |
| signal exsangue | moins de 2 cellules survivantes | **signal rejeté** |
| « trop beau pour être vrai » | IC au-delà de 0,10 | **signalé**, jamais bloqué |

Le détecteur de suspicion ne bloque pas, et c'est délibéré : refuser un résultat
parce qu'il est trop beau reviendrait à le décider avant de le voir. Il est
calculé, inscrit, et **imprimé dans le rapport**.

## Deux pièges écartés, et une porte qui est tombée

**« 99 % de NaN » ne veut pas dire « 99 % de barres non scorées ».** Les étalons
scorent une barre par séance sur environ 390 : 99,7 % des barres n'ont pas de
score, et c'est la forme de l'hypothèse. Un contrôle écrit sans cette distinction
aurait rejeté les deux seuls signaux du projet
([[Failed Ideas/ledger#F23]]).

**Le plancher de deux cellules a cassé la porte 03** dans la minute. Sa
calibration reproduit à la main l'IC d'**une seule** cellule, à 1e-12 — c'est tout
son objet. Le harnais sert deux sortes de clients, des tests et des calibrations
de lui-même, et une règle écrite pour les premiers interdisait les secondes.
Dérogation écrite, et vérifiée **étroite** par la porte 06 elle-même. Voir
[[lessons|L11]] et [[Failed Ideas/ledger#F24]].

## Clause 2 — tentée le 2026-09-18, NON franchie

Rejouer Mesfin (2026) « avec notre modèle de coût » suppose de connaître notre
coût. `harness/costs.py` ne rend qu'un **plancher** : `fee_bp` et `slippage_bp`
sont ouverts. Conséquence à ne pas contourner — on peut conclure « ne survit pas
même au plancher », jamais « survit sous nos coûts ».

Ce qu'il faut avant, dans l'ordre : une convention de provenance des valeurs
externes, les multiplicateurs CME, la réponse de Lucid sur le caractère all-in de
ses commissions, une déclaration écrite de `slippage_bp`. Voir `ETAT.md`
§ Prochaine action.

**Premier maillon posé le 2026-09-18.** `D09` fixe la convention de provenance :
toute valeur du catalogue est *mesurée*, *décidée* ou *externe*, et une valeur
externe n'entre qu'avec `source`, `source_url`, `retrieved`, `quoted` et
`applies_to`. `catalogue/validate.py` §8 refuse le catalogue sinon ;
`scripts/check_provenance.py` le montre en train de refuser neuf fautes, chacune
pour la raison écrite d'avance. Le registre `provenance:` est **vide** — les deux
seuls champs externes du catalogue, `multiplier` et `fee_per_contract_usd`, sont
encore `null` sur les dix instruments. La convention est écrite **avant** les
valeurs, et c'est l'ordre voulu.

**Deuxième maillon, non posé.** Les multiplicateurs CME ont été tentés le même
jour : `cmegroup.com` est injoignable depuis le poste (timeout puis ECONNRESET
sur trois URLs). Rien n'a été déposé — une valeur relevée dans un extrait de
moteur de recherche n'est pas une valeur citée, et `D09` la refuserait.

**Puis la cible a changé, et la tentative a échoué.** `L14` a montré que la
friction de Mesfin est du même ordre que notre plancher, donc son verdict est
transportable ; la lecture du papier a montré que sa **métrique** ne l'est pas
(un `t` sur des rendements nets par trade, quand nous mesurons un IC). `D12` a
donc visé **Heston, Korajczyk & Sadka (2010)**, dont le résultat est une
corrélation. `H03` a été pré-enregistrée puis mesurée le jour même : **le peigne
n'est pas là** — dents à +0,00065 contre creux à +0,00056 hors retournement
court, p = 0,25. Seul le **retournement de court terme** ressort, nettement
(`j=1` à IC −0,0115, `t` −6,14), et c'est la préface du motif, pas le motif.

La clause 2 reste **non franchie**, comme `H03` l'avait écrit d'avance. Voir
[[lessons|L15]] et [[Failed Ideas/ledger#F33]].

## Ce qui n'a pas encore été fait, et qui appartient à cette phase

**`H01` et `H02` sont mesurés** depuis le 2026-09-18 — les deux premiers tests
comptés du projet. Les deux sont **dans le bruit** (`t` final de référence −1,56
et −0,63), avec un signe négatif là où le signe attendu était
positif ; la clause de falsification qui s'applique est « rien à distinguer du
bruit », pas « le motif existe à l'envers ». Voir [[signaux/README]].

Ce qui s'est appris ce jour-là dépasse les deux chiffres, et dans les deux sens.
**La déflation mord** : le `t` naïf de `H01` valait −2,27 — un calcul sans
précaution aurait annoncé le premier résultat du projet. **Et elle mordait trop** :
un facteur 5,48 de recouvrement était appliqué à des observations espacées de 415
barres, qui n'en partagent aucune. Corrigé le jour même par `D11` ; le `t` final
de référence est −1,56. Voir [[lessons|L13]] et [[Failed Ideas/ledger#F30]].

**L'empreinte du harnais ne désignait pas le harnais** — découvert en marge le
2026-09-18, et **réparé le même jour** par `D10`. `registry.code_hash()`
empreintait les octets sur disque, fins de ligne comprises : les trois empreintes
du projet se reproduisent toutes des mêmes blobs git, et `gate_04` annonçait 53
lignes périmées qui ne l'étaient pas. Deux gestes — `.gitattributes` fixant
`eol=lf`, et le repli des fins de ligne dans l'empreinte — qui ne se recouvrent
pas ([[Failed Ideas/ledger#F28]]). L'empreinte passe de `12f9b2c1` à `e9ef2087`,
vérifiée invariante ; les portes 03 à 06 sont rejouées vertes et
`counted_tests()` vaut toujours 0. Voir [[lessons|L12]] et
[[Failed Ideas/ledger#F27]].

## Voir aussi

[[phases/phase-05-api-de-signal]] · [[signaux/README]] ·
[[concepts/comptage-des-tests]] · [[concepts/cout-aller-retour]]
