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
