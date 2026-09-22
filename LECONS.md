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

---

## L12 — Une empreinte d'octets n'identifie pas un fichier, elle identifie une copie de travail

**Ce qu'on croyait.** `registry.code_hash()` empreinte le harnais. Si le nombre
change, le harnais a changé, et `D05` l'énonce sans réserve : tous les résultats
antérieurs sont périmés. C'est l'instrument de l'interdit « ne jamais modifier le
harnais » — le seul.

**Ce qui était vrai.** Il empreinte **les octets de ce disque-là**, fins de ligne
comprises. Avec `core.autocrlf=true` et aucun `.gitattributes`, git réécrit les
fins de ligne à chaque extraction, tandis qu'un fichier réécrit par un outil
ressort en LF : le mélange dérive, fichier par fichier, sans qu'une ligne de code
bouge. Les **trois** empreintes du projet — `8c1b6512`, `5d6ce982`, `12f9b2c1` —
se reproduisent **toutes les trois** à partir des mêmes blobs git, en ne faisant
varier que quelles fins de ligne portent quels fichiers. Le même harnais vaut
`842a6ade` sur le poste d'aujourd'hui. Contenu identique, quatre numéros.

**Comment on s'en est aperçu.** L'empreinte ne correspondait à aucune des 53
lignes du registre alors que `git status` sur `harness/` était vide. Le symptôme
à reconnaître : **une empreinte qui bouge sans diff**. Le test qui tranche est
court et se refait — recalculer l'empreinte depuis les blobs git en essayant les
mélanges de fins de ligne ; si l'un retombe sur la valeur attendue, le contenu
n'a pas bougé.

Et la vraie leçon est dans la conséquence. `gate_04_registry.py` annonce alors
« 53 lignes périmées », c'est faux, et **il ne bloque pas**. Un signal d'alarme
qui se déclenche pour une non-raison **s'apprend comme du bruit** : le jour où le
harnais changera vraiment, ce nombre-là ne préviendra plus personne. Un garde qui
crie à tort est pire qu'un garde absent. Corollaire général : **ce qu'on empreinte
doit être le contenu, jamais son encodage** — c'est `L09` déplacée d'un cran,
de la lecture vers l'empreinte.

---

## L13 — Une correction statistique écrite pour une forme de signal en punit une autre, et dans le sens qui ne se voit pas

**Ce qu'on croyait.** La déflation de recouvrement de `D04` — diviser le `t` par
`√h` — est une correction prudente et universelle. Prudente, donc sans risque :
au pire elle est trop sévère, et trop sévère ne fait jamais de mal.

**Ce qui était vrai.** Elle suppose un signal **scoré à chaque barre**, et `D04`
le dit en toutes lettres : « deux observations voisines partagent `h−1` barres ».
`H01` et `H02` scorent **une fois par séance** : leurs observations sont espacées
de 415 barres pour un horizon de 30, et ne partagent rien. Le harnais leur a
retiré un facteur **5,48** sans raison — `t` final −0,28 au lieu de −1,56. La
conclusion tenait par chance, les deux étant dans le bruit de toute façon ; un
signal à `t` naïf de 4 aurait affiché **0,5** et aurait été écarté.

**Comment on s'en est aperçu.** Par une question sur *autre chose* — « une
anomalie sur un seul actif reste une anomalie » — qui obligeait à calculer un `t`
par cellule, donc à se demander ce que valait le `t` tout court. Jamais par une
exception, jamais par une porte : **toutes les portes passaient**, parce
qu'aucune ne testait la déflation contre un signal d'une autre forme que celui de
sa calibration.

Deux réflexes en sortent. **« Trop sévère » n'est pas un côté sûr** : une
correction trop sévère rejette des signaux réels, et un rejet ne se plaint pas.
Il n'y a pas de direction gratuite. Et : **une correction dont l'hypothèse est
écrite doit être testée contre un cas qui viole cette hypothèse**, sans quoi elle
est calibrée sur le seul cas où elle a raison — c'est `L11` sous un autre
visage, et la deuxième fois que le harnais se fait prendre à n'avoir qu'un
client en tête.

---

## L14 — Un ordre de grandeur recopié n'est pas un ordre de grandeur calculé

**Ce qu'on croyait.** La friction supposée par Mesfin (2026) — 2 points d'indice
d'aller-retour — valait **8 à 15 bp** sur nos données, soit une quinzaine de fois
l'écart d'un tick sur NQ. Une hypothèse de coût aussi lourde tuant n'importe quel
signal intraday, son résultat négatif mesurait peut-être davantage son hypothèse
que les signaux, et n'était donc pas transportable. C'était écrit dans
`wiki/research/mesfin-2026-falsification` depuis le 2026-09-16, et `ETAT.md` en
avait tiré un « raccourci honnête » pour franchir la clause 2 de la porte 06.

**Ce qui était vrai.** 2 points sur un indice à 14 688 valent **1,36 bp**, pas
13,6. L'erreur est un facteur 10, et elle renverse la conclusion : sa friction
vaut **1,7×** notre plancher `NQ × US` et **0,9×** notre pire cellule — elle est
plus légère que ce que nous mesurons nous-mêmes sur CL. Et notre plancher est un
**écart seul**, frais et glissement encore `null`, quand ses 2 points sont une
friction tout compris. Son verdict est transportable ; le raccourci qui devait
l'écarter n'existe pas.

**Comment on s'en est aperçu.** En faisant le calcul au lieu de le citer, au
moment de s'en servir — `scripts/check_mesfin_premise.py`. Deux symptômes
étaient visibles depuis le début, et personne ne les a lus. D'abord **aucun
script ne produisait ce nombre** : il n'apparaissait que dans une page dérivée, et
le wiki interdit nommément ce genre de chose — mais seulement pour les **IC**
(`CLAUDE.md` § Wiki). La garde couvrait le nombre qui inquiétait, pas celui qui
était faux. Ensuite la plage de niveaux citée, « 13 000 à 25 000 », ne
correspondait pas à la tranche `pool`, dont le centile 99 est à 17 556 : le
chiffre venait d'ailleurs tout en étant présenté comme mesuré chez nous.

Le réflexe : **un nombre qui sert à décider se recalcule au moment de décider**,
et une page qui affirme « nos propres données mesurent » doit nommer le script
qui les a mesurées. C'est `D09` — la provenance des valeurs externes — dont on
découvre ici qu'elle manque au wiki autant qu'au catalogue.

---

## L15 — Deux seaux qui se recouvrent laissent une hypothèse être validée par le mauvais phénomène

**Ce qu'on croyait.** `H03` était pré-enregistrée dans les règles : trois clauses
écrites avant la mesure, un motif prédit en entier, un témoin négatif intégré. Le
peigne de Heston et al. se vérifierait en comparant les **dents** (décalages
multiples d'une séance) aux **creux** (décalages non multiples), et la séparation
des deux serait le résultat.

**Ce qui était vrai.** Les deux seaux **se recouvraient**. Les creux étaient
définis comme `j = 1…12`, et le retournement de court terme — un phénomène
distinct, que le papier décrit séparément — comme `j = 1…3`, donc **à
l'intérieur** des creux. La mesure a rendu une séparation nette, `+0,00177` et
`p = 0,030` : elle venait **entièrement** du retournement court. Le seau retiré
de ce qui ne lui appartenait pas, `j = 4…12`, la séparation tombe à `+0,00009` et
`p = 0,247`. Le peigne n'existe pas ; un résumé automatique annonçait pourtant
« séparation : OUI ».

**Comment on s'en est aperçu.** En refusant le résumé et en redemandant *sur quoi*
la séparation reposait. Rien ne le signalait : les 52 lignes sont justes, le
harnais a bien travaillé, et l'hypothèse était bien pré-enregistrée. C'est la
**définition des seaux** qui portait la faute, et une pré-inscription ne protège
de rien si ce qu'elle inscrit est mal découpé.

Le réflexe : **deux catégories qu'on va comparer doivent être disjointes, et on
le vérifie en les écrivant**, pas après. Et le corollaire, plus dur : un test
pré-enregistré qui « passe » se relit aussi attentivement qu'un test qui échoue —
un résultat conforme est précisément celui que personne n'a envie d'examiner.

---

## L16 — Un témoin négatif a une position, et mal placé il mesure un plancher

**Ce qu'on croyait.** `H04` clause C comparait l'autocorrélation de `|r|` aux
décalages **multiples d'une séance** à celle des décalages **voisins non
multiples**. Le témoin était pris à 15 et 30 minutes du multiple : assez proche
pour être comparable, assez loin pour n'être pas le même décalage. Cela semblait
le bon réglage.

**Ce qui était vrai.** À 15 ou 30 minutes d'un multiple de séance, on est presque
à la **même phase du cycle intra-journalier** — c'est-à-dire là où l'effet
cherché est presque aussi fort. Le témoin mesurait donc l'effet contre lui-même.
L'écart obtenu valait **+0,0055 à +0,0104** ; placé à une demi-séance, en phase
opposée, il vaut **+0,0457 à +0,0684**, soit **cinq à sept fois plus**. La clause
tenait, mais elle rendait un **plancher** de l'effet, pas l'effet.

**Comment on s'en est aperçu.** Parce que le résultat paraissait *trop faible
pour un fait aussi réputé* — les auteurs rapportent un Ljung-Box de 36 680 — et
que cette gêne a suffi à faire vérifier où le témoin était posé. Aucun contrôle
ne l'aurait signalé : la clause passait.

Le réflexe, qui prolonge `L13` : **« trop sévère » n'est pas un côté sûr**, et un
témoin négatif mal placé est une sévérité involontaire. Quand un motif est
périodique, le témoin se place à la **phase opposée**, jamais au voisinage — sans
quoi on compare la crête à la crête. Et le corollaire : **un résultat qui passe
mais paraît trop faible pour ce qu'on savait mérite le même examen qu'un résultat
qui échoue.**


---

## L17 — Un protocole qui illustre son format avec des cas réels distribue les réponses qu'il prétend cacher

**Le 2026-09-20**, au moment de lancer le premier passage du trieur.

`corpus/TRIAGE.md` fait tout ce qu'il faut pour protéger l'étalon : il consacre sa
première section à *qui peut être le trieur*, nomme les fichiers interdits,
explique que `AMORCE.md` porte la réponse deux fois, et fabrique une entrée
expurgée pour que le trieur n'ait jamais à l'ouvrir. Puis, quatre sections plus
bas, il montre la forme du JSON attendu :

```json
{"entry": 1, "verdict": "oui", ...}
{"entry": 18, "verdict": "non", ...}
```

**Les deux verdicts sont justes**, et l'entrée 18 est l'un des **deux seuls `non`**
de l'étalon — c'est-à-dire la moitié de la condition B, celle qui vaut zéro sur
deux. Le document écrit pour empêcher la contamination en était le vecteur.

**Pourquoi ça ne se voit pas.** Un exemple de format n'est pas lu comme une
donnée : il est lu comme de la syntaxe. L'auteur le remplit avec ce qu'il a sous
la main — et ce qu'il a sous la main, parce qu'il vient de lire l'étalon, ce sont
des cas réels avec leur vraie réponse. Le geste est machinal, et c'est exactement
pour ça qu'il passe les relectures : personne ne relit un bloc de code
d'illustration en se demandant *ce qu'il révèle*.

**Ce que ça généralise.** Partout où un document sépare un juge d'un jugé — une
consigne d'annotation, un jeu de tests dont on cache les attendus, une
pré-inscription d'hypothèse — **les exemples appartiennent au même périmètre que
les données**. Un gabarit s'écrit avec des valeurs fabriquées, ou avec des
numéros qui n'existent pas dans le jeu réel.

Le réflexe : **relire ses propres exemples comme un adversaire les lirait**, et
se demander non pas « est-ce que c'est clair ? » mais « qu'est-ce que ça
donne ? ». Et le corollaire de méthode, qui a joué ici : quand on découvre le
défaut **au moment d'appliquer le protocole**, on contourne sans le corriger —
corriger le protocole dans le geste même qui l'applique est ce que « le premier
passage fait foi » interdit. On contourne, on déclare, on corrige après.

## L18 — Avant d'élargir une liste close, chercher si la cause n'est pas ailleurs

**Le 2026-09-21**, en réparant les trois fiches de référence.

Cinq citations de la fiche Heston étaient introuvables dans le texte du papier.
Le mécanisme prévu pour ce cas existait : la **réparation déclarée** de `D16` —
`quoted_source` mot pour mot dans le texte, `quoted_repair` nommant la raison
dans une liste **close** : `ocr`, `math_notation`, `table`.

La cause observée ne rentrait dans aucune des trois. Le texte extrait insérait
des espaces à l'intérieur des mots : « multiples **o f** 13 », « half-hour
**inte rvals** », « way is **d ifferent** ». La réponse qui vient d'elle-même est
d'ajouter une quatrième valeur à la liste — `extraction_spacing`, ou quelque nom
de ce genre — et de réparer les cinq citations.

**Elle aurait été fausse deux fois.**

D'abord parce que `ocr`, la valeur la plus proche, aurait été un **mensonge
vérifiable** : les métadonnées du PDF disent *LaTeX with hyperref* et *GPL
Ghostscript*. Le papier est **né numérique**. Une liste close ne vaut que si
chacun de ses noms est vrai ; y loger un cas « à peu près » la vide de son sens
plus sûrement que de l'élargir franchement.

Ensuite et surtout parce que **la cause n'était pas dans la fiche**. Un test à la
racine l'a montré en une minute : `pypdf` avec `extraction_mode="layout"` rend
les cinq citations trouvables **sans toucher une ligne de la fiche**, et ne casse
aucune des deux autres. Il n'y avait rien à réparer. La fiche avait raison depuis
le début ; c'est l'outil de lecture qui se trompait.

**Ce que la réparation aurait coûté.** Cinq `quoted_source` reproduisant
fidèlement les fautes d'un extracteur mal réglé, une valeur de liste close
inventée pour les couvrir, et une fiche de référence **dégradée pour ressembler à
un défaut d'outil**. Le tout aurait été vert. C'est la forme la plus coûteuse de
l'erreur : celle qui passe la porte.

**Ce que ça généralise.** Une liste close, une liste blanche, une liste
d'exceptions — c'est un aveu d'humilité écrit à l'avance : *voici les cas
irréguliers que nous acceptons, nommés un par un*. Quand un cas nouveau s'y
présente, la pression est de l'y ajouter, parce que le mécanisme est là, qu'il
fonctionne, et qu'ajouter une ligne coûte moins que remettre en cause l'outil qui
a produit le symptôme. **C'est précisément l'inverse qu'il faut faire** : une
liste d'exceptions qui s'allonge est le symptôme d'une cause non cherchée, pas
d'un monde irrégulier.

Le réflexe, dans l'ordre : **d'où vient le symptôme, avant de savoir comment le
nommer.** Et la question qui tranche : *si l'outil avait raison, la fiche
aurait-elle tort ?* Ici la réponse était non, et elle s'obtenait en changeant un
argument.

Le corollaire tient en une phrase, et il rejoint `L17` : **la décision
d'élargir la liste n'était pas la mienne à prendre en passant** — elle appartient
à `D16`. Chercher la cause était donc la seule chose que je pouvais faire sans
excéder mon mandat, et c'est celle qui a résolu le problème. La contrainte a
mieux travaillé que ne l'aurait fait la liberté.

---

## L19 — Un verrou de dépendances commité ne garantit pas l'environnement qui a tourné

**Le 2026-09-22**, en lançant `corpus/extract_text.py --check` pour la première
fois depuis la production du texte.

**Ce qu'on croyait.** Que `uv.lock` étant commité, le texte versionné dans
`corpus/text/` — celui qui *fait foi* pour `F2` depuis `D18` — était reproductible
par toute session qui synchronise le dépôt.

**Ce qui était vrai.** `uv.lock` portait `pypdf 6.19.0` depuis le commit du
**2026-09-20**. Le texte a été produit le **2026-09-21** avec **6.14.2**, par un
environnement **en retard sur le verrou commité**. Personne ne l'a vu, et rien
n'était fait pour le voir : le verrou décrit ce qu'un `uv sync` *installerait*,
jamais ce que l'interpréteur qui tourne *contient*.

**Comment on s'en est aperçu.** `extract_text.py --check` a rendu **31 fichiers
sur 36 divergents**, avec la mention `pypdf 6.14.2 -> 6.19.0`. Le symptôme est
donc excellent — `D18` l'avait voulu bruyant, et il l'a été. Ce qui manquait
n'était pas le garde, c'était qu'une version soit **fixée** plutôt que
seulement **inscrite**. Le manifeste notait fidèlement `"pypdf": "6.14.2"` :
**noter n'est pas contraindre.**

**Le piège de diagnostic, et il a failli fonctionner.** Les 15 PDF manquants
venaient d'être repris le matin même. Une divergence pouvait donc venir du
*fichier* autant que de la *version*, et attribuer d'emblée à `pypdf` aurait été
une conclusion non mesurée. Les deux causes ont été séparées dans un
environnement jetable : le même corpus ré-extrait sous 6.14.2 rend **36 sur 36
conformes**. La version était bien seule en cause — et, au passage, la preuve
est faite que **les PDF repris sont identiques à ceux du 21**, donc que
l'acquisition est reproductible.

**Ce que la mesure a retourné.** L'intuition disait « une version récente lit
mieux ». Mesuré sur les 18 papiers, 6.19.0 récupère **+0,05 %** de contenu en
mode `default` et **+0,66 %** en `layout`, mais **dégrade de 12 %** les lettres
orphelines en `layout` — le symptôme même de `L18`. Aucune des deux versions
n'est meilleure. Le choix s'est donc décidé sur le coût, pas sur la qualité, et
c'est `D19`.

**Ce que ça généralise.** Dès qu'une sortie d'outil est **versionnée comme un
résultat** — le texte de `D18`, demain un corpus moissonné — l'outil qui l'a
produite entre dans la définition de ce résultat, au même titre que le harnais
entre dans la définition d'un IC (`D10`). Il s'épingle, et en changer périme.
La question à se poser devant un artefact versionné : *quelle version de quoi
faudrait-il pour le reproduire, et qu'est-ce qui l'impose ?* Si la réponse est
« c'est écrit quelque part », ce n'est pas imposé.

---

## L20 — Vérifier qu'un PDF est arrivé ne vérifie pas que c'est le bon papier

**Le 2026-09-22**, au premier passage du moissonneur (`D20`).

**Ce qu'on croyait.** Que `corpus/acquisition.json` recensait 19 papiers
atteignables, chacun prouvé par un `application/pdf` d'au moins 20 000 octets
commençant par `%PDF-`. `ACQUISITION.md` § Comment le constat est fait est
explicite et fier de l'être : *« Une URL qui répond 200 ne prouve rien. Une page
de résumé répond 200 derrière un péage. »*

**Ce qui était vrai.** La preuve établit qu'**un** PDF est arrivé. Elle
n'établit nulle part que c'est **celui qu'on a demandé**. L'entrée 1 du
recensement — *Gao, Han, Li & Zhou (2018), « Market intraday momentum », JFE
129(2):394-414* — désigne une URL du dépôt Monash qui sert en réalité
**Limkriangkrai, Chai & Zheng (2023), « Market intraday momentum: APAC
evidence », *Pacific-Basin Finance Journal* 80:102086**. Treize pages, une autre
revue, d'autres auteurs, cinq ans d'écart.

**Comment on s'en est aperçu**, et c'est le cœur de la leçon : **par une
collision d'empreintes entre deux affirmations indépendantes sur les mêmes
octets**. Le moissonneur dédoublonne par `sha256` ; il a trouvé que le PDF servi
pour le travail OpenAlex « APAC evidence » était **le même fichier** que celui
enregistré sous le nom de Gao 2018. Deux sources, deux noms, un seul fichier :
au moins l'une des deux a tort.

**Les deux vérifications automatiques évidentes échouent toutes les deux**, et
il faut le savoir avant de les écrire :

| Test | Verdict sur l'entrée 1 | Pourquoi il se trompe |
|---|---|---|
| le titre d'`AMORCE.md` est dans la 1re page | **passe** | « Market intraday momentum » est une **sous-chaîne** de « Market intraday momentum: APAC evidence » |
| premier auteur **et** année dans les 2 premières pages | **passe** | le papier APAC **cite** Gao et al. (2018) dès son résumé |

Un papier ressemble à un autre papier, et **le nom du bon papier apparaît dans
le mauvais** — c'est même la règle en littérature académique, où l'on cite ce
qu'on prolonge. Aucune heuristique de métadonnée ne s'en sort seule.

**Ce que ça aurait coûté si le moissonneur n'avait pas existé.** L'entrée 1
n'est pas encore fichée. Si elle l'avait été, la fiche aurait porté le nom de
Gao 2018 et les chiffres de Limkriangkrai 2023 — et **`F2` et `F4` auraient
toutes deux été vertes** : les citations existent bien dans ce texte-là, et le
PDF désigné existe bien. Le garde le plus strict du projet aurait validé une
fiche sur le mauvais papier, sans une faute à signaler. C'est la forme la plus
coûteuse de l'erreur, celle qui passe la porte — comme `L18`.

**Et l'artefact versionné est déjà faux** : `corpus/text/gao-2018-*.txt`, le
texte qui *fait foi* au sens de `D18`, est le texte du papier APAC sous le nom
de Gao. Il est commité. Aucune fiche ne s'en sert à ce jour, donc rien en aval
n'est contaminé — mais le fait qu'il ait traversé `D17`, `D18`, `D19` et deux
gardes sans être vu mesure exactement ce que la chaîne ne regarde pas.

**Ce que ça généralise.** Une preuve répond toujours à **la question qu'elle
pose**, et jamais à celle qu'on croit poser. « Le texte est-il arrivé ? » et
« est-ce le bon texte ? » sont deux questions, et la première ne rend pas la
seconde. Devant un garde, la question à se poser n'est pas *« que vérifie-t-il
? »* mais *« qu'est-ce qui passerait quand même ? »*.

Le seul contrôle qui a marché est **redondant par construction** : deux sources
indépendantes qui nomment le même objet, et qu'on compare. C'est le même motif
que la porte 03 — une seconde implémentation écrite différemment — et que `L12`,
où l'empreinte d'un même harnais différait selon le poste. Quand un fait compte,
il se fait affirmer deux fois par deux chemins qui ne se parlent pas.
