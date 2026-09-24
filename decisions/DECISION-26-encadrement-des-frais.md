# D26 — Les frais par contrat sont encadrés, pas devinés

**Date :** 2026-09-24
**Phase :** 09
**État :** prise

## La question

`fee_per_contract_usd` est `null` sur les dix instruments. Le barème de l'exécutant
prévu, Lucid Trading, est public, mais **ne dit pas s'il est tout compris** ou si les
frais CME et NFA s'y ajoutent, et l'opérateur n'a pas encore de compte dont un relevé
trancherait. Que faut-il retenir comme frais, et où les inscrire ?

## Ce qui a été relevé le 2026-09-24

Trois sources. Toutes les valeurs sont en USD **par contrat et par side**.

**Lucid Trading** — *Approved Products and Commissions*,
<https://support.lucidtrading.com/en/articles/11508978>, colonne « Commission (Per
Side) ». Relu à l'identique du relevé du 2026-09-17.

**CME Group** — *Non-Member Fee Finder*,
<https://www.cmegroup.com/company/clearing-fees/fee-finder.html>, ligne « Estimated
fee per side », Globex. La page parente dit : *« Exchange fees for clearing and
trading »* — le montant couvre compensation **et** négociation. Pour chaque produit,
le code Globex affiché a été vérifié égal à la racine. URL de chaque résultat :
`.../fee-finder/product-fees.html?uniqueId=<id>&venueTrans=globexTrade`, avec :

| Racine | `uniqueId` | Racine | `uniqueId` |
|---|---|---|---|
| NQ | `CME-NGTF6USLRZ7B-FUT` | MNQ | `CME-FAUQQNCNAZFH-FUT` |
| ES | `CME-VGQ4V6NVXLBW-FUT` | MES | `CME-HCRO7TMCTUOP-FUT` |
| YM | `CBT-XP43JNWQF4NW-FUT` | MYM | `CBT-YKBJ4WCZ75Z6-FUT` |
| GC | `CMX-DZVNALIUR5JI-FUT` | MGC | `CMX-OMWOQRKBA5HF-FUT` |
| CL | `NYX-J6RPLCCJNZSE-FUT` | MCL | `NYX-Y5C4WL55TA7F-FUT` |
| 6E | `CME-K756BOA4VAYC-FUT` | 6B | `CME-UQD2MJRM4A2U-FUT` |
| 6J | `CME-ICHN7TZSGFJO-FUT` | 6A | `CME-WVTWQUTQ25W3-FUT` |

**NFA** — Bylaw 1301 (b)(i)(A),
<https://www.nfa.futures.org/rulebooksql/rules.aspx?Section=3&RuleID=BYLAW+1301> :
*« $.02 for each commodity futures contract [...] on a round-turn basis during the
period of July 1, 2026, through June 30, 2027, after which time the assessment will
be equal to $.04 »*. Soit 0,01 par side aujourd'hui, **0,02 par side à partir du
2027-07-01**.

| Évalué | Lucid | CME | | Micro | Lucid | CME |
|---|---|---|---|---|---|---|
| NQ | 1,75 | 1,38 | | MNQ | 0,50 | 0,35 |
| ES | 1,75 | 1,38 | | MES | 0,50 | 0,35 |
| YM | 1,75 | 1,38 | | MYM | 0,50 | 0,35 |
| GC | 2,30 | 1,65 | | MGC | 0,80 | 0,70 |
| CL | 2,00 | 1,50 | | MCL | 0,50 | 0,50 |
| 6E, 6B, 6J, 6A | 2,40 | 1,60 | | — | pas de micro devise au barème Lucid | |

Le rapport micro / plein a été vérifié sur les fiches contrat CME, ligne « Contract
Unit » : $2 contre $20 × Nasdaq-100, $5 contre $50 × S&P 500, $0.50 contre $5 × DJIA,
10 contre 100 troy ounces, 100 contre 1,000 barrels. **Exactement un dixième**, ce
que `D01` §7 laissait « à vérifier ».

## Les options

1. **Attendre une réponse de Lucid.** Écartée *comme seule voie* : rien ne garantit
   qu'elle vienne, et elle ne serait qu'une citation de plus. Elle reste souhaitable
   et, si elle arrive, elle **choisit une borne** sans rien rouvrir.

2. **Déposer le barème Lucid dans `fee_per_contract_usd`.** Écartée, et c'est le
   piège de cette décision. `harness/costs.py` ne consulte ce champ que pour savoir
   s'il est `null` : rempli, il **retire `fee_bp` de la liste des composantes
   manquantes** sans pour autant l'ajouter au plancher, qui reste l'écart seul. Le
   rapport d'IC afficherait un coût moins incomplet qu'il ne l'est — le trou
   deviendrait silencieux, exactement ce que `D04` interdit. Et ce serait la borne
   **basse**, déposée comme si elle était *la* valeur.

3. **Déposer la somme Lucid + CME + NFA.** Écartée pour la même raison, et pour une
   seconde : cette somme n'est la citation d'aucun tiers, donc `catalogue/validate.py`
   §8 la refuserait à bon droit. C'est une valeur **décidée**, pas externe (`D09`,
   les trois natures).

4. **Encadrer.** Retenue. Deux bornes, chacune sourcée, inscrites ici ; le
   catalogue n'est pas touché tant que le harnais ne sait pas s'en servir.

## Le choix

Les frais par side sont encadrés entre une **borne basse** — le barème Lucid seul —
et une **borne haute** — barème Lucid + frais CME non-membre + NFA à 0,02 —, et
toute lecture nette qui conditionne une décision (phase 10, backtest) se fait **à la
borne haute**.

## Pourquoi

**Les deux bornes ont chacune un sens réel, pas seulement arithmétique.** Sur les
comptes d'évaluation et *sim-funded* de Lucid, aucun exchange ne facture rien : le
montant débité est celui que Lucid configure, donc la borne basse y est le coût
complet. Sur un compte live (LucidLive, Tradovate ou Rithmic), le barème n'est pas
publié ; la borne haute est ce qu'il coûterait si le barème ne couvrait **rien** des
frais d'exchange.

**Un indice, qui n'est pas une preuve.** Sur les quatorze contrats, le barème Lucid
est **supérieur ou égal** aux frais CME non-membre, et **égal** pour MCL (0,50 et
0,50). Un barème conçu comme une répercussion des frais d'exchange plus une marge
aurait exactement cette forme. Cela penche vers « tout compris » — sans le dire. Si
c'était dit, la borne haute serait trop pessimiste d'environ 40 % du total ; c'est
l'erreur qu'on choisit de faire.

**Pourquoi 0,02 et non 0,01 pour la NFA.** C'est le taux en vigueur à partir de
juillet 2027, à l'intérieur de l'horizon d'exécution d'une stratégie retenue en
phase 10. Sur un coût de 3 à 4 dollars, l'écart est négligeable ; le prendre haut
évite d'avoir à rouvrir.

**Ce que ça pèse** — `scripts/fee_bracket.py`, aller-retour en bp du notionnel au
prix médian de la tranche `pool`. *Relancer plutôt que recopier (`L21`)*, mais pour
fixer l'ordre de grandeur :

- en **plein format**, la borne haute vaut **0,37 bp (NQ) à 1,18 bp (CL)** — du même
  ordre que le plancher d'écart mesuré (0,21 à 1,55 bp) ; l'écart entre les deux
  bornes est de 0,15 à 0,5 bp ;
- en **micro**, elle vaut **1,03 bp (MNQ) à 3,43 bp (MCL)**. Le décuplement de `D01`
  §7 est vérifié : même contrat, même prix, dix fois moins de notionnel, des frais qui
  ne baissent que de 62 à 72 %.

**Ce qu'on sacrifie.** Une stratégie viable à la borne basse et non à la haute sera
écartée alors qu'elle était peut-être bonne. C'est la direction d'erreur voulue : un
coût flatteur qui a circulé ne se rappelle pas (`harness/costs.py`, en-tête).

## Ce que ça verrouille

**Le catalogue n'est pas touché.** `fee_per_contract_usd` reste `null` sur les dix
instruments et `todo fees` reste ouvert, désormais adossé à cette décision. Déposer
une valeur n'aura de sens que lorsque le harnais saura **l'ajouter** au coût — ce qui
est une modification du harnais, donc une décision écrite qui périme les tests
comptés (`D05`). Cette future décision devra aussi trancher `slippage_bp`, pour ne
périmer le registre **qu'une fois**, et dire la forme du champ : deux bornes, ou des
composantes, et pour quelle taille de contrat.

**Aucun IC n'est calculé, aucun fichier de `harness/` n'est touché**, l'empreinte ne
bouge pas, aucun résultat n'est périmé. `counted_tests` reste 56.

**Fichiers.** Cette décision ; `scripts/fee_bracket.py`, qui porte les montants et
les rapporte en bp ; `catalogue/catalogue.yaml`, dont `todo fees` pointe ici.

**Ce que ça coûterait d'en changer.** Rien tant que le harnais ne lit pas les
frais : ce ne sont que deux colonnes et un script. Après, un changement de borne
réécrit le coût de tout ce qui a été lu net.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| **Les frais CME changent le 2026-10-01** (SER-9799R, 2026-09-02). Le PDF de l'avis n'a pas pu être lu ; un résumé tiers parle d'une hausse des E-minis, non vérifiée. Les montants ci-dessus sont **antérieurs** : les relever de nouveau au Fee Finder | après le 2026-10-01, et avant toute lecture nette |
| Le caractère tout compris du barème Lucid — une réponse écrite de Lucid, ou un relevé d'exécution une fois le compte ouvert, choisit la borne | dès que disponible ; ne rouvre rien |
| Le barème des comptes **live**, non publié | avant la phase 10 |
| L'intégration des frais au coût du harnais, avec `slippage_bp` et la forme du champ au catalogue | une seule décision, avant toute lecture nette qui conditionne un choix |
| FDAX : frais EUREX et unité en EUR | seulement s'il entre dans l'univers |
