# LEÇONS

Les erreurs apprises, et ce qu'elles ont coûté.

## Mode d'emploi

- Une leçon par entrée, numérotée `L01`, `L02`, `L03`… dans l'ordre où elles sont
  apprises.
- **Jamais renumérotée. Jamais supprimée. Jamais réécrite.** Une leçon qui se
  révèle fausse donne lieu à une nouvelle entrée qui corrige la précédente en la
  citant — pas à une rature.
- Chaque entrée dit trois choses, dans cet ordre :
  1. **Ce qu'on croyait.**
  2. **Ce qui était vrai.**
  3. **Comment on s'en est aperçu** — le symptôme exact, parce que c'est lui qui
     permettra de le reconnaître la prochaine fois.
- Une leçon vaut d'être écrite si elle a coûté quelque chose : du temps, un
  résultat faux, un test gaspillé. Pas les broutilles.

Ce fichier est lu en entier au démarrage de chaque session. Il alimentera plus
tard le générateur d'hypothèses (phase 14) : les erreurs passées y deviennent des
contraintes sur les propositions futures. Garde-le donc précis et court.

---

## L01 — Une convention de roulement décide de l'existence des données

**Ce qu'on croyait.** Le choix entre roulement calendaire (`.c.0`) et roulement
au basculement du volume (`.v.0`) est un détail de construction de série
continue, qui déplace quelques barres autour des échéances.

**Ce qui était vrai.** Il décide de la quantité d'historique qui existe. En
calendaire, l'or rendait **136 702 barres au lieu de 3 717 717** — vingt-sept
fois moins — et les futures de devises perdaient plus de la moitié de leur
historique. Le roulement au volume a été retenu pour cette raison.

**Comment on s'en est aperçu.** Par un comptage de barres, pas par une erreur :
**aucune exception n'est levée**. Une série tronquée de 96 % se charge, se
calcule, et produit des chiffres d'apparence normale. Le symptôme à reconnaître
est un volume de données inférieur à ce que la période impliquerait — d'où le
réflexe : toujours confronter `barres ≈ années × séances × barres par séance`.

---

## L02 — Un instrument sept fois plus court n'est pas « un peu plus court »

**Ce qu'on croyait.** FDAX est un instrument comme les autres, simplement moins
profond ; on l'inclut et on verra.

**Ce qui était vrai.** Databento n'a intégré EUREX qu'en mars 2025 : FDAX
plafonne à **1,46 an** contre 10,65 pour les neuf autres, et le contrat ne se
traite nulle part ailleurs. Aucun budget ne comble cet écart chez ce
fournisseur. Un tel instrument rend **hétérogène tout calcul qui l'inclut** :
une corrélation, une normalisation transversale, une tranche de découpage
n'ont plus le même sens selon qu'on est avant ou après mars 2025, et il est
absent de la totalité de la tranche `research`.

**Comment on s'en est aperçu.** Par la colonne « années » du manifeste,
c'est-à-dire avant tout calcul — le seul moment où cette découverte est gratuite.
Le symptôme à reconnaître : un instrument dont la période ne recouvre pas celle
des autres doit être traité comme un univers séparé, ou exclu, jamais fondu dans
le lot.

---

## L03 — La largeur ne vient pas de la fréquence, elle vient du calendrier

**Ce qu'on croyait.** Les corrélations baissent quand la fréquence
d'échantillonnage monte ; mesurée sur barres 15 minutes, la largeur effective de
l'univers serait donc nettement supérieure aux 4,03 du journalier.

**Ce qui était vrai.** Elle vaut **4,22**. À 30 minutes, 4,19 ; à 60 minutes,
4,17 ; en journalier, 4,03. La corrélation absolue moyenne ne bouge pas non plus
(0,295 à 15 min contre 0,313 en journalier). **Changer de fréquence ne crée
aucune largeur.** Ce qui en crée, c'est la grille actif × séance : 4,43 en
Asie, 4,10 en Europe, 3,87 aux États-Unis, soit 12,40 en sommant des fenêtres
disjointes. Et le gain ne vient pas du nombre d'instruments mais de la
**structure de blocs**, qui change d'une séance à l'autre : le bloc devises, soudé
en Europe et aux États-Unis, **se dissout en séance asiatique** — 6E, 6J et 6A y
deviennent trois paris séparés.

**Comment on s'en est aperçu.** En mesurant les deux au lieu d'en supposer une.
Corollaire à retenir, qu'aucune moyenne ne montre : la largeur **réalisée séance
par séance** a une médiane de 3,74 mais un centile 5 à **2,38**, et **17 % des
séances tombent sous 3 paris**, 1,7 % sous 2. Les pires — 2022-09-13,
2022-11-10, 2022-12-13, 2023-02-14 — sont des jours de chiffre macro, où un seul
PC explique jusqu'à **84 %** de la variance transversale. Ces jours-là, neuf
instruments font un pari. Ça ne se voit jamais dans un IC moyen ; ça se voit dans
la queue d'un PnL.

## L04 — Un estimateur qui rend zéro ne mesure pas un marché gratuit

**Ce qu'on croyait.** L'estimateur d'écart de cotation de Corwin & Schultz (2012),
construit sur les extrêmes haut/bas, donnerait une estimation utilisable du coût
de transaction par cellule, puisqu'on n'a pas de carnet.

**Ce qui était vrai.** Sur barres 1 minute, sa médiane est **exactement zéro** pour
6A, 6B, 6J et pour toutes les cellules asiatiques. L'estimateur a été conçu pour
des barres journalières ; à la minute, la plupart des fenêtres de deux barres
donnent un alpha négatif, ramené à zéro par construction, et la médiane s'effondre.
Un critère de rétention bâti là-dessus déclarait **27 cellules sur 27 négociables**,
y compris celles où 42 % des barres portent moins de dix contrats.

**Comment on s'en est aperçu.** Par une colonne entière de `0.00` dans une table
de coûts — le genre de chiffre qu'on lit comme une bonne nouvelle. Le remède n'a
pas été de deviner un écart, mais d'en **mesurer le plancher** : la plus petite
variation de prix non nulle sur onze ans donne le tick de chaque contrat
(NQ 0,25 · CL 0,01 · 6J 0,0000005 …), et un marché ne peut pas être plus serré
qu'un tick. Le tick est une *mesure*, pas une valeur déclarée : il ne tombe pas
sous l'interdit sur les valeurs inventées. Les frais, eux, restent `null`.

## L05 — Un détecteur calibré sur les cas bruyants est muet sur les cas discrets, et son silence ressemble à une absence

**Ce qu'on croyait.** La détection empirique des recollements, une fois la minute
de raccord identifiée (00:00 UTC) et le seuil d'isolement réglé, donnerait la
liste des roulements.

**Ce qui était vrai.** Elle en donne **3,4 à 3,6 par an** pour les indices là où
il y en a 4, et **8,5** pour CL là où il y en a 12. Les manquants sont les
roulements des années à taux proches de zéro, dont l'écart de calendrier était
trop petit pour émerger du bruit local. Pour 6A l'écart de taux AUD/USD est si
faible que la méthode ne tranche pas du tout, et pour FDAX 373 séances ne
suffisent pas à estimer un centile 99,9.

**Comment on s'en est aperçu.** En comparant le compte annuel détecté au compte
attendu par le cycle d'échéances — jamais par une erreur. Le symptôme à
reconnaître : un détecteur dont le rendement **dépend de l'amplitude du phénomène**
produit une liste dont les trous sont systématiques et corrélés au régime, pas
aléatoires. Une liste incomplète de dates de roulement est plus dangereuse
qu'aucune liste, parce qu'elle donne le sentiment que le problème est traité.

## L06 — Un détecteur jugé sur son compte, et non sur ses correspondances, paraît bien meilleur qu'il n'est

**Ce qu'on croyait.** D'après `L05`, la détection empirique des recollements
manquait « quelques » roulements, ceux des années à taux proches de zéro. Les
comptes annuels — 3,4 à 3,6 par an pour les indices là où il y en a 4 —
suggéraient un rendement de l'ordre de 90 %.

**Ce qui était vrai.** Confrontée à la liste autoritative du fournisseur — 527
roulements sur 2016-2026 — elle en retrouve **331, soit 62,8 %**, et date en plus
**67 événements qui n'en sont pas**. Le rappel va de 97,6 % (6E, 41 sur 42) à
38 % (6B, 16 sur 42) et 0 % (FDAX, 0 sur 51). Le compte annuel était trompeur
parce que **manques et faux positifs se compensent** : NQ affichait 39 détections
pour 42 roulements, soit 93 % en apparence, mais **32 seulement étaient
réelles**. Et les manques ne sont pas concentrés sur les années à taux nul : pour
CL ils sont répartis sur les onze années, de 4 à 8 par an. Une tolérance de
±1 jour n'y change rien (62,8 % → 63,4 %) : ce sont de vrais manques, pas un
décalage systématique.

**Comment on s'en est aperçu.** En comparant **avant** d'adopter, comme `D01` §6
l'exigeait — `scripts/compare_rolls.py`. L'occasion était unique : une fois la
liste au catalogue, la question ne peut plus être posée. Le symptôme à
reconnaître dépasse les roulements : **un compte juste n'est pas un compte de
choses justes.** Tout détecteur évalué par « combien il en trouve » plutôt que
par « lesquels il trouve » doit être supposé faux jusqu'à appariement.

## L07 — Un cycle déclaré n'est pas un cycle observé

**Ce qu'on croyait.** `D01` §6 : cycle trimestriel pour les indices et les
devises, **mensuel pour GC et CL**.

**Ce qui était vrai.** Pour CL, oui : 12,02 roulements par an. Pour GC, non :
**5,07 par an**, répartis sur dix mois et **jamais en septembre ni en octobre**.
Les échéances actives de l'or ne sont pas mensuelles, et un roulement au volume
ne visite que celles-là. Le détecteur de la phase 01, configuré en « mensuel »
pour GC, plafonnait mécaniquement à un événement par mois. Pire pour FDAX : 51
bascules en 1,47 an, 52 intervalles pour **28 échéances distinctes**, dont **24
retours à une échéance déjà quittée**. Le symbole continu n'y roule pas, il
**oscille** — troisième motif d'exclusion, indépendant de la profondeur (`L02`)
et de la corrélation (ledger F02).

**Comment on s'en est aperçu.** En rapportant le compte de la liste autoritative
au cycle déclaré, instrument par instrument. C'est désormais un contrôle
mécanique de `catalogue/validate.py` : un taux hors de [3,5 ; 4,5] pour un cycle
trimestriel, ou hors de [11 ; 13] pour un mensuel, fait échouer le catalogue.

## L08 — Le raccord ne tombe pas toujours sur une barre, et alors il coûte cher

**Ce qu'on croyait.** Le raccord tombant à 00:00 UTC, l'ajustement mesure l'écart
sur **une minute** : il n'absorbe donc qu'une minute de mouvement réel avec
l'artefact (`D03`, complément).

**Ce qui était vrai.** Pour 292 des 333 roulements visibles à mi-2023, oui. Pour
les 41 autres — **31 % des roulements de CL, 29 % de ceux de GC**, aucun sur les
indices — le marché était fermé à cet instant, et la première barre suivante
arrive des heures plus tard, jusqu'à **70 heures**. L'écart mesuré enjambe alors
toute la fermeture : médiane **44,9 bp** contre 28,5 bp pour un recollement tombé
sur une barre, et jusqu'à **3 648 bp**. C'est ce que l'ajustement absorbe, en
silence, sur ces dates-là.

**Comment on s'en est aperçu.** Par un échec de la porte 02 : le contrôle
« l'ajustement ne touche aucun rendement hors recollement » a sauté sur GC et CL
et passé sur NQ, parce qu'il s'ancrait sur la date du roulement au lieu de la
barre où le saut atterrit réellement. Le symptôme à reconnaître : **un contrôle
qui passe sur l'instrument le plus liquide et échoue sur les autres** désigne une
hypothèse de calendrier, presque jamais une erreur de calcul.

---

## L09 — Un décodage implicite accuse un fichier qui n'a pas bougé

**Ce qu'on croyait.** Comparer le registre à sa version commitée est trivial :
`git show HEAD:registry/tests.jsonl`, on compare ligne à ligne, et toute
différence signale une réécriture — exactement ce que l'append-only interdit.

**Ce qui était vrai.** `subprocess.run(..., text=True)` décode la sortie avec
l'encodage **de la machine**, cp1252 sous Windows, quand le fichier est lu en
UTF-8. Toute ligne contenant un accent paraît alors réécrite. La porte 04 a
accusé la ligne 13 du registre d'avoir été modifiée : elle était intacte, et
c'était le mot « vérifier » à l'intérieur qui ne survivait pas au décodage.

**Comment on s'en est aperçu.** Parce que la porte désignait **une seule ligne**
sur vingt-cinq. Un vrai problème d'encodage aurait sali toutes les lignes ; un
vrai problème d'append-only en aurait sali une et toutes les suivantes. Une seule
ligne isolée, au milieu, ne correspond à aucune des deux — c'est cette forme-là
qui trahit un artefact de lecture. Le réflexe : devant une comparaison de
fichiers qui échoue, **vérifier d'abord comment les deux côtés ont été décodés**,
avant de croire ce qu'elle raconte. `encoding="utf-8"` explicite des deux côtés,
toujours, et jamais `text=True` seul sur une sortie susceptible de porter des
accents.

---

## L10 — Une comparaison d'horloge en flottants décale l'ancre d'une barre, et le signal produit des scores qui ne se mesurent jamais

**Ce qu'on croyait.** Placer l'ancre d'un signal « à trente minutes de la clôture
de la fenêtre » est une question d'horloge, sans piège : on calcule les minutes
restantes, on compare au seuil, on prend la première barre qui passe.

**Ce qui était vrai.** Calculées en heures fractionnaires, les minutes restantes
de la barre de 15:29 face à une clôture à 16:00 valent
**31,000000000000004** — donc `<= 31` est **faux**, l'ancre glisse d'une barre, et
le rendement à trente barres tombe **une barre au-delà** de la fenêtre. Le harnais
le jette. `NQ × US`, la cellule la plus dense de la grille, produisait **615
scores et zéro observation**. En minutes entières, la comparaison est exacte et la
même cellule rend 100 %.

**Comment on s'en est aperçu.** Pas par une exception — il n'y en a aucune — mais
par un contrôle ajouté pour une autre raison : *combien des scores produits
tombent sur une barre que le harnais sait mesurer*. Il répondait **0 %**. Et le
motif désignait le coupable : les cellules `ASIA` passaient, `EUROPE` et `US`
étaient à zéro, ce qui n'est pas une histoire de densité de données mais de
chemin de calcul. Deux réflexes en sortent. **Toute arithmétique d'horloge se
fait en unités entières**, jamais en heures flottantes comparées à un seuil. Et
**un signal se juge d'abord sur le nombre d'observations qu'il produit**, pas sur
le nombre de scores : les deux peuvent différer de tout, silencieusement.

---

## L11 — Le harnais a deux sortes de clients, et une règle écrite pour l'un casse l'autre

**Ce qu'on croyait.** Un plancher de deux cellules survivantes est une règle
simple et sans victime : un IC poolé sur une seule cellule n'est qu'un diagnostic
de cellule promu en résultat, et `D01` §4 l'interdit. On l'applique partout.

**Ce qui était vrai.** La **porte 03** est tombée dans la seconde qui a suivi. Sa
calibration reproduit à la main l'IC d'**une seule** cellule, à 1e-12 — c'est tout
son objet, et c'est ce qui prouve que le harnais mesure juste. La règle était
bonne, la calibration aussi, et elles s'excluaient : le harnais sert deux sortes
de clients — **des tests d'hypothèse et des calibrations de lui-même** — et une
contrainte écrite en pensant aux premiers interdit les secondes.

**Comment on s'en est aperçu.** En rejouant la porte 03 après avoir modifié le
harnais, ce que `D05` impose justement. Sans ce réflexe, la règle serait passée
en production et la prochaine session aurait trouvé une porte 03 cassée sans
comprendre pourquoi. Le réflexe à garder : **toute contrainte ajoutée au chemin
d'évaluation se teste contre une calibration autant que contre un test**, et si
elle doit distinguer les deux, elle doit le faire explicitement — ici,
`screen(..., is_test=hypothesis_ref is not None)`, dérogation écrite et vérifiée
étroite par la porte 06.
