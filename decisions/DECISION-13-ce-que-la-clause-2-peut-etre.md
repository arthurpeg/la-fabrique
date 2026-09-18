# D13 — Ce que la clause 2 peut être, quand trois cibles ont échoué

**Date :** 2026-09-18
**Phase :** 06
**État :** prise

## La question

La clause 2 exige que « le harnais réplique un résultat publié connu ». Trois
cibles ont été examinées le même jour. Mesfin (2026) est écartée : sa métrique
est un rendement net par trade, la nôtre un IC (`D12`). Heston et al. (2010) est
mesurée et **le motif n'est pas là** (`H03`). Reste à savoir si la clause peut
être satisfaite, et par quoi.

## Les options

1. **Chercher une quatrième cible exprimée en IC.** Écartée comme stratégie.
   Trois hypothèses ont maintenant été mesurées — `H01`, `H02`, `H03` — et les
   trois sont sans résultat ; Mesfin, dont le verdict est transportable (`L14`),
   annonce que rien ne survit. L'hypothèse qu'**aucun résultat publié en IC ne
   survive sur neuf futures intraday** est désormais la plus probable. Une porte
   qui exige l'impossible n'est pas une exigence, c'est un blocage.

2. **Assouplir la clause après avoir vu échouer `H03`.** Refusée, et nommément :
   `H03` § « Si le motif n'est pas là » l'interdit d'avance. Un échec ne s'achète
   pas en redéfinissant la porte.

3. **Redéfinir la clause, mais avant de savoir si la nouvelle cible passe.**
   Retenue. C'est la condition que `H03` posait elle-même, et elle est tenable
   ici : la décision est écrite **avant** la première mesure de `H04`.

## Le choix

La clause 2 est satisfaite quand **la chaîne reproduit un fait publié sur nos
données**, et non quand le seul harnais d'IC reproduit un IC publié. La cible est
**Andersen & Bollerslev (1997)** — la périodicité intra-journalière de la
volatilité — et l'hypothèse `H04` est pré-enregistrée avant toute mesure.

## Pourquoi

**Ce qu'on perd, et il faut le dire en premier.** La clause validait, dans son
intention d'origine, **le harnais d'IC** contre une vérité extérieure. Elle ne le
fera plus. Le harnais reste validé par sa **calibration à la main** (porte 03,
IC reproduit à 1e-12 sur un cas connu) — c'est une garantie plus faible, et c'est
désormais la seule. Écrit ici pour qu'aucune session ne croie le contraire.

**Ce qu'on garde, et qui n'est pas rien.** La couche de données, la grille, la
définition des séances, l'ajustement des roulements et la discipline de mesure
seront confrontées à un fait externe fort. Si notre `ES × US` ne montre pas la
forme en U que les futures S&P 500 montrent depuis quarante ans, quelque chose
est cassé en amont de tout signal — et nous ne le saurions par aucun autre moyen.

**La cible est choisie pour être difficile à rater, et c'est un argument, pas un
aveu.** Une épreuve d'instrument doit porter sur un fait dont l'absence
signalerait une panne, pas sur un fait dont la présence serait une découverte. La
périodicité intra-journalière de la volatilité est l'un des faits stylisés les
mieux établis de la discipline : `Q(10) = 36 680` chez les auteurs. Un balance de
précision se vérifie avec un poids étalon, pas avec un objet inconnu.

**Elle ne coûte aucun test compté.** Elle mesure une propriété des **données**,
pas un pouvoir prédictif : aucun IC n'est produit, donc l'invariant III ne
s'applique pas et le dénominateur ne bouge pas. Après les 52 lignes de `H03`,
ce n'est pas un détail.

**Et elle tombe sur le même contrat.** Leur figure porte sur les futures S&P 500
pendant la séance américaine ; notre cellule `ES × US` est ce contrat, sur cette
fenêtre.

## Ce que ça verrouille

**Où vit l'instrument : `scripts/`, pas `harness/`.** Il mesure les données, il
ne juge pas un signal. Deux raisons, et la seconde décide :

- l'invariant III porte sur les IC, et il n'en produit aucun ;
- `registry.code_hash()` n'empreinte que `harness/*.py`. Y ajouter un fichier
  **périmerait les 56 lignes comptées**, dont trois hypothèses mesurées. Ce prix
  était nul le matin même ; il ne l'est plus.

C'est la contrepartie de [[Failed Ideas/ledger#F22]], qui plaçait les contrôles
*dans* le harnais parce qu'ils jugent un signal. Le critère reste le même : ce
qui juge un signal entre dans l'empreinte, ce qui mesure les données n'y entre
pas.

**La clause 2 reste binaire.** `H04` dit ce qui la franchirait et ce qui ne la
franchirait pas, avant la mesure. Si le motif est absent, la porte reste fermée
et c'est le **dépôt** qu'il faudra soupçonner, pas le papier.

## Ce qui reste ouvert

| Point | Échéance |
|---|---|
| Le harnais d'IC n'aura **jamais** été confronté à une vérité extérieure. Si une cible en IC apparaît un jour — univers élargi, autre classe d'actifs — la question se rouvre | à l'occasion, et pas avant |
| Le **modèle périodique explicite** de leur section 5, qui purge la périodicité : utile en phase 09 pour normaliser les scores, hors sujet ici | phase 09 |
| **Bollerslev et al. (2018)**, 50+ futures, justification de notre *pooling* : demanderait le même genre d'instrument | phase 09 ou plus tard |
