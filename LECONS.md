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
