# Consigne de lecture unique — La Fabrique, `D55`

Tu lis **une seule fois** le texte d'un papier académique, en fin de consigne,
et tu écris **deux fichiers, dans cet ordre** :

1. **la fiche** du papier, selon la PARTIE 1 ;
2. **sa recette**, selon la PARTIE 2. La recette complète la fiche que tu viens
   d'écrire.

Chaque fichier a ses propres règles et son propre contrôle automatique. Les
deux exigent la même chose : chaque citation recopiée **à la lettre** du texte,
et `null` avec sa raison pour tout ce que le papier ne dit pas. **N'invente
jamais une valeur.**

Écris la fiche d'abord, en entier, avec l'outil Write. Écris ensuite la recette.
Réponds en une ligne : les deux chemins écrits, le nombre de résultats cités
dans la fiche et le nombre d'ambiguïtés relevées dans la recette.

---

# PARTIE 1 — LA FICHE

# Consigne d'extraction — phase 09 de La Fabrique

Tu produis **une fiche JSON** à partir du texte d'un papier académique, et de
rien d'autre. Tu n'as pas accès au reste du projet, et c'est voulu : une fiche
écrite de mémoire ou d'après un résumé serait sans valeur.

## Ce que tu rends

Un **seul objet JSON**, rien avant, rien après, écrit à `corpus/fiches_harvest/can-oil-prices-predict-japanese-yen-W3111589756.json`. Pas de bloc de code, pas de
commentaire. Il suit le schéma reproduit ci-dessous, section « SCHÉMA ».

## Les règles qui font rejeter une fiche

1. **Chaque citation (`quoted`) doit se retrouver MOT POUR MOT dans le texte
   fourni.** Copie-la, ne la reformule pas, ne corrige pas sa ponctuation, ne
   remplace pas « at least » par « >= ». Un seul caractère qui diffère et la
   fiche est refusée.
2. **Chaque `value` numérique doit figurer dans sa propre citation**, sauf si tu
   déclares `"derived": true` (nombre que TU as calculé, avec une `note` disant
   comment) ou `"spelled_out": "<le mot>"` (le papier écrit le nombre en toutes
   lettres).
3. **Si le texte fourni est visiblement abîmé** là où la page serait claire —
   scan corrompu, symbole mathématique perdu, tableau mis à plat — mets la chaîne
   ABÎMÉE, telle quelle, dans `quoted_source`, une version lisible dans `quoted`,
   et le motif dans `quoted_repair` parmi `ocr`, `math_notation`, `table`.
   N'invente pas d'autre motif.
4. **N'invente jamais une valeur.** Ce que le papier ne dit pas vaut `null`, avec
   une `reason`. Un `null` est bruyant, une valeur plausible est indétectable.
5. **`transposability.what_does_not_transfer` ne peut pas être vide.** Notre
   univers est de neuf futures intraday ; un papier dont tout transfère n'a pas
   été lu avec attention.

## Ce qu'on te demande vraiment

Pas un résumé. **Ce que le papier affirme, ce qu'il a mesuré, et ce qui en
survivrait chez nous.** Une fiche fidèle mais creuse passe les contrôles et ne
sert à rien : préfère trois résultats qui portent des chiffres à dix qui n'en
portent pas.

---

## SCHÉMA

# Le schéma de fiche

Ce que doit contenir un fichier de `corpus/fiches/`, et ce que
`corpus/validate_fiches.py` refuse. Établi par
`decisions/DECISION-14-schema-de-fiche.md`.

Une **fiche** est le JSON structuré extrait d'un papier. Sa définition n'est pas
inventée ici : elle est dans `CLAUDE.md` § Le vocabulaire, et ce fichier ne fait
que la rendre exécutable.

---

## Les huit champs

Six viennent de la constitution, deux de la pratique.

| Champ | Origine | Obligatoire |
|---|---|---|
| `claim` | constitution — *hypothèse* | oui |
| `universe` | constitution — *univers* | oui |
| `horizon` | constitution — *horizon* | oui, `null` accepté **avec raison** |
| `signal_construction` | constitution — *construction du signal* | oui, `null` accepté **avec raison** |
| `reported_results` | constitution — *résultats annoncés* | oui |
| `what_is_missing` | constitution — *ce qui manque* | oui |
| `source` | pratique — d'où ça vient | oui |
| `transposability` | pratique — ce qui en survit chez nous | oui |

Plus l'identité : `fiche_id`, `written`, `written_by`.

Des champs supplémentaires sont **autorisés**. Un papier peut porter des choses
qu'aucun schéma ne prévoit — un modèle de coûts, une structure de validation, un
critère d'acceptation propre à l'auteur. Le schéma fixe un plancher, pas un
plafond.

---

## `source` — la provenance, au sens de `D09`

```json
"source": {
  "authors": "…",
  "title": "…",
  "year": 1997,
  "source_url": "https://…",
  "pdf": "corpus/pdf/…",
  "retrieved": "AAAA-MM-JJ",
  "peer_reviewed": true,
  "amorce_entry": 11
}
```

`authors`, `title`, `year`, `source_url` et `retrieved` sont exigés.
`peer_reviewed` est un booléen : un préprint non arbitré n'est pas une revue à
comité de lecture, et la distinction a déjà servi.

---

## `reported_results` — une liste, et chaque entrée porte sa citation

C'est ici que `D09` s'étend aux fiches. **Un résultat recopié d'un papier est une
valeur externe** : rien dans le dépôt ne peut la contredire.

> [!warning] **Les exemples de ce document sont FABRIQUÉS.** Ils citent un papier
> qui n'existe pas. C'est `L17` : un gabarit rempli avec des cas réels distribue
> les réponses qu'il prétend cacher, et ce document est lu par l'extracteur.
> Corrigé le 2026-09-21 ; les exemples portaient jusque-là le contenu réel d'une
> fiche de référence.

```json
"reported_results": [
  {
    "name": "afternoon_spread_bp",
    "value": 3.4,
    "unit": "bp",
    "quoted": "the average effective spread widens to 3.4 basis points after 14:00",
    "note": "Sur leur échantillon d'actions, pas sur des futures."
  }
]
```

`name` et `quoted` sont exigés pour chaque entrée. `value` peut être `null` quand
le résultat est qualitatif.

**Le contrôle qui mord.** Quand `value` est un nombre, le validateur vérifie
qu'il **se retrouve dans `quoted`**, séparateurs ôtés — la même fonction
`value_in_quote` que le catalogue, celle que `scripts/check_provenance.py` a
prise en défaut sur `12500` contre `12,500,000`. Ce qui est attrapé n'est pas la
source absente, qui se voit, mais la **faute de recopie**, qui ne se voit pas.

Un nombre **dérivé** par nous — un rapport entre deux niveaux que les auteurs
citent séparément, par exemple — n'a pas à figurer dans la citation : il porte
`"derived": true`, et le contrôle numérique est alors levé. Le `note` doit dire
comment il a été obtenu.

**Et un nombre écrit en toutes lettres.** Un papier peut écrire « *Seven of the
strategies fail* » : il n'y a aucun chiffre à retrouver. L'entrée porte alors
`"spelled_out": "Seven"`, et le validateur vérifie que **le mot** est dans la
citation. Ce qu'il ne vérifie pas — que « Seven » vaut 7 — reste un geste
humain, et le champ existe pour le **nommer** plutôt que pour le cacher derrière
`derived`, qui signifierait à tort qu'un calcul a eu lieu.

**Et quand le TEXTE EXTRAIT ne dit pas ce que le papier dit.** Un PDF scanné, une
notation mathématique perdue, un tableau mis à plat : le texte où `quoted` est
cherchée peut être abîmé là où la page est claire. L'entrée porte alors **deux**
chaînes :

```json
{
  "name": "afternoon_spread_bp",
  "value": 3.4,
  "quoted": "the average effective spread widens to 3.4 basis points after 14:00",
  "quoted_source": "the average effective spread widens to 3.4 basis p0ints after 14:00",
  "quoted_repair": "ocr"
}
```

`quoted` reste ce que le papier dit ; `quoted_source` est ce que le **texte**
porte, mot pour mot, et c'est elle qui est cherchée et qui fait foi pour le
contrôle numérique. `quoted_repair` dit **pourquoi** les deux diffèrent, dans une
liste **close** :

| Motif | Quand |
|---|---|
| `ocr` | le PDF est un scan et son texte est corrompu |
| `math_notation` | le papier écrit un symbole que l'extraction ne rend pas |
| `table` | la citation vient d'un tableau, lu en cellules par l'extraction |

**Ce que cela n'autorise pas, et c'est l'essentiel.** Il faut toujours **une
chaîne présente à la lettre** dans le texte. Une réparation déplace ce qui est
cherché, jamais ce qui est exigé. **Une paraphrase ne fournit aucune chaîne et
reste une faute** : si la phrase du papier ne dit pas exactement ce qu'on
voudrait lui faire dire, on cite ce qu'elle dit, ou on ne cite pas.

Un motif hors de la liste, un `quoted_source` sans motif, un motif sans
`quoted_source` : le validateur refuse les trois.

**Et quand l'extraction disloque LE NOMBRE LUI-MÊME.** Le cas ci-dessus suppose
un texte abîmé *autour* d'un chiffre intact. Il arrive que le chiffre soit la
victime : `pypdf` rend `−3.02` par `−3 . 02` quand le papier l'écrit en
italique, et `T = 496,512` par `T51,724z2885496,512` quand il colle une égalité
entière. Aucune comparaison numérique ne peut plus aboutir, alors même que
`quoted_source` est bien présente à la lettre.

L'entrée porte alors, **en plus** de la réparation, un `spelled_out` qui donne
le nombre **tel que la citation l'écrit** :

```json
{
  "name": "overnight_sorted_hedge_intraday_3f_alpha_monthly_pct",
  "value": -3.02,
  "quoted": "alpha of −3.02% per month with a t-statistic of −9.74)",
  "quoted_source": "alpha of −3 . 02% per month with a t -statistic of −9 . 74 )",
  "quoted_repair": "math_notation",
  "spelled_out": "−3 . 02"
}
```

C'est la règle 4 appliquée telle qu'elle est écrite — *« une `value` numérique
introuvable dans sa `quoted`, sauf `derived: true` ou `spelled_out` »* — et non
une exception nouvelle. Le champ avait été décrit pour les nombres **en
toutes lettres** ; sa fonction est plus générale, et c'est celle-ci : **nommer
le geste humain qui relie une `value` à une citation où aucune machine ne la
reconnaît.**

**Ce que cela n'affaiblit pas.** `spelled_out` doit toujours se retrouver à la
lettre dans la citation, laquelle doit toujours se retrouver à la lettre dans le
texte. Un extracteur qui voudrait loger un chiffre inventé devrait donc
fabriquer une chaîne réellement présente dans le PDF — ce qui est exactement ce
que `F2` interdit.

**Ce que cela ne vérifie pas**, et qui reste un geste humain nommé : que
`−3 . 02` *vaille* `-3.02`. Comme pour « Seven » et 7, le champ existe pour
**montrer** cette lecture, pas pour la garantir. Quand le décodage n'est pas
évident, la `note` le rend vérifiable : pour Andersen (2003), l'extraction rend
`=` par `5` et `'` par `9`, ce que confirment quatre occurrences indépendantes
du même papier — `K541`, `P53`, `p(J9)50`, `J9512`.

---

## `horizon` et `signal_construction` — `null` se justifie

```json
"horizon": {"value": null, "reason": "le papier ne prédit rien ; il décrit une propriété des données"}
```

Un `null` nu est refusé. C'est la règle du catalogue (`CLAUDE.md` § Les
interdits) appliquée ici : l'inconnu s'écrit, il ne se tait pas.

---

## `signal_construction` — la forme attendue quand il n'est pas `null`

C'est un **objet**, comme `universe` et `horizon` : une `value` en prose, et
ses `quoted`.

```json
"signal_construction": {
  "value": "Score = (clôture de la première demi-heure − ouverture de séance) / ouverture, calculé à l'ouverture + 30 min, appliqué dans le même sens à la dernière demi-heure.",
  "quoted": ["we define the first half-hour return as", "predicts the last half-hour return"]
}
```

**C'est la faute la plus fréquente du corpus, et de loin.** Au moins **sept
extracteurs indépendants**, appartenant à **trois familles de modèles
différentes**, ont écrit à la place un objet structuré de leur invention —
`{"sampling": …, "components": […], "model": …}` — **sans la clé `value`**, que
le schéma exige et que le validateur refuse.

Aucun de ces extracteurs n'avait vu les fautes des autres. Sept fois la même
erreur n'est pas sept inattentions : **c'est cette section qui manquait.** Le
schéma ne montrait que le cas `null` ci-dessus, jamais la forme normale.

Des sous-clés supplémentaires restent **autorisées** si elles éclairent la
construction. `value` doit être là.

---

## `what_is_missing` — une liste

```json
"what_is_missing": [
  "aucun multiplicateur de contrat, aucun frais",
  "la fenêtre horaire est donnée en heure locale, sans fuseau nommé",
  "le critère de sélection des jours n'est pas chiffré"
]
```

Une **liste de chaînes**, comme `transposability.what_does_not_transfer`. Ce
qui manque au papier s'énumère ; une prose continue se lit moins bien et se
compte mal.

---

## `transposability` — ce qui en survit chez nous

Trois sous-champs, tous exigés :

- `what_transfers` — ce qui vaut sur neuf futures intraday ;
- `what_does_not_transfer` — une **liste**, non vide ; un papier dont *tout*
  transfère n'a pas été lu avec assez d'attention ;
- `what_aligns_well` — ce qui, au contraire, tombe juste.

**Pourquoi c'est obligatoire.** C'est ce champ qui a déjà fait écarter une cible
de réplication — sa métrique était un rendement net par trade, la nôtre un IC —
et qui en a cadré une autre, dont seul le motif transférait. Une fiche sans lui
dit ce qu'un papier affirme, pas ce qu'il vaut ici. Les cas sont dans
`decisions/`, pas ici : ce document est lu par l'extracteur.

---

## Ce que le validateur refuse

    python corpus/validate_fiches.py

1. un champ obligatoire absent ;
2. `horizon` ou `signal_construction` à `null` **sans** `reason` ;
3. une entrée de `reported_results` sans `name` ou sans `quoted` ;
4. une `value` numérique **introuvable** dans sa `quoted`, sauf `derived: true`
   ou `spelled_out` — et `spelled_out` doit alors se retrouver dans la citation ;
5. `what_does_not_transfer` vide ;
6. un `source` incomplet, un `source_url` qui n'est pas une URL, un `retrieved`
   mal daté ;
7. un `fiche_id` qui ne correspond pas au nom du fichier.

`corpus/check_fiches_guard.py` le montre en train de refuser, sur des fiches
délibérément fautives — même discipline que `scripts/check_provenance.py`. **Un
garde qui n'a jamais rien refusé est un garde que personne n'a testé.**

---

## Ce que ce schéma ne dit pas

Le **triage** — décider qu'un papier est implémentable — n'est pas ici. C'est
l'autre moitié de la porte 07, et elle exige un seuil chiffré écrit avant mesure
(`L06` : *un compte juste n'est pas un compte de choses justes*).


---

## IDENTITÉ DE LA FICHE

- `fiche_id` : `can-oil-prices-predict-japanese-yen-W3111589756`
- `source.pdf` : `corpus/pdf/can-oil-prices-predict-japanese-yen-W3111589756.pdf`
- `source.source_url` : `https://a-e-l.scholasticahq.com/article/17964.pdf`
- `source.retrieved` : `2026-09-30`
- `written_by` : le nom de la session qui extrait
- `written` : `2026-10-06`

---

# PARTIE 2 — LA RECETTE

La fiche que tu complètes est celle que tu viens d'écrire en PARTIE 1.

# Consigne de recette — La Fabrique, `D34`

Tu complètes **une fiche** de papier académique par sa **recette** : la formule,
les entrées, le timing, les paramètres et les ambiguïtés du signal, **cités mot
pour mot** dans le texte du papier. Un codeur lira ta recette et rien d'autre du
papier : ce que tu n'écris pas, il devra le deviner ; ce que tu inventes, il le
codera.

## Ce que tu rends

Un **seul fichier JSON**, écrit à `corpus/recettes/can-oil-prices-predict-japanese-yen-W3111589756.json`. Rien d'autre.

## Le format

Exemple **fabriqué** — il cite un papier qui n'existe pas (`L17`) :

```json
{
  "fiche_id": "can-oil-prices-predict-japanese-yen-W3111589756",
  "written": "AAAA-MM-JJ",
  "written_by": "<modèle>",
  "formula": {
    "statement": "score = rendement de l'ouverture à la barre notée, divisé par sa volatilité",
    "quoted": "we scale the return since the open by its trailing volatility",
    "reason": null
  },
  "inputs": [
    {"name": "open_return", "description": "rendement depuis l'ouverture de la séance",
      "known_at": "à la clôture de la barre notée", "quoted": "the return since the open"}
  ],
  "timing": {
    "statement": "le score se pose 45 minutes avant la clôture",
    "quoted": "the signal is formed 45 minutes before the close",
    "reason": null
  },
  "parameters": [
    {"name": "formation_minutes", "value": 45, "unit": "minutes",
      "quoted": "the signal is formed 45 minutes before the close"},
    {"name": "volatility_window_days", "value": null, "unit": "days",
      "quoted": null, "reason": "le papier dit « trailing » sans donner la longueur"}
  ],
  "ambiguities": [
    {"question": "la volatilité est-elle calculée sur les rendements journaliers ou intraday ?",
      "resolution": null, "quoted": null}
  ],
  "market": {
    "studied": "le contrat à terme sur l'indice S&P 500, séance régulière",
    "quoted": "we use one-minute prices of the S&P 500 index futures",
    "exact_roots": ["ES"],
    "sessions": ["US"],
    "sessions_quoted": "from the 9:30 open to the 16:00 close",
    "sessions_reason": null
  }
}
```

## Les règles, vérifiées par une machine

- **`quoted`** est une phrase du papier, **à la lettre**, ou un extrait coupé
  par `...`. Une paraphrase est refusée. Le contrôle cherche la chaîne dans le
  texte ci-dessous, casse et espaces repliés.
- **Si le texte extrait abîme la phrase** (formule mathématique mal rendue,
  tableau mis à plat, scan) : écris la phrase telle que le papier la dit dans
  `quoted`, telle que le texte la porte dans `quoted_source`, et le motif dans
  `quoted_repair`, parmi `math_notation`, `ocr`, `table`. C'est `quoted_source` qui est cherchée.
- **Chaque `value` numérique se retrouve dans sa citation.** Un nombre que tu as
  calculé toi-même porte `"derived": true` et un `note` qui dit comment.
- **Tout ce que le papier ne dit pas est `null`**, avec `reason` non vide.
  **N'invente jamais une valeur plausible** : c'est un interdit constitutionnel
  du projet. Un `null` est bruyant, une valeur inventée est invisible.
- `formula`, `timing` et au moins une entrée sont exigés. `quoted` peut y être
  `null`, avec sa raison.
- **Les ambiguïtés sont le cœur du travail.** Chaque question dont la réponse
  change le calcul — une fenêtre, une normalisation, un traitement des jours
  fériés, un signe — s'écrit ici, avec la réponse du papier si elle existe
  (`resolution` et `quoted`), ou `null` s'il n'en donne pas.
- **`market` dit sur quel marché le papier mesure** (`D38`) — c'est lui qui
  fixe les cellules de la mesure, avant tout résultat :
  - `studied` : le marché, en tes mots ; `quoted` : la phrase du papier qui le
    nomme, à la lettre ;
  - `exact_roots` : parmi **nos** instruments, ceux qui sont **ce marché même**
    ou son équivalent direct — et eux seuls :
    - `ES` : E-mini S&P 500 (l'indice S&P 500, ses contrats, le SPY)
    - `NQ` : E-mini Nasdaq-100 (l'indice Nasdaq-100, ses contrats, le QQQ)
    - `YM` : E-mini Dow (le Dow Jones Industrial Average, ses contrats, le DIA)
    - `GC` : l'or (contrat COMEX, or au comptant)
    - `CL` : le pétrole brut WTI (contrat NYMEX)
    - `6E` : l'euro contre dollar (EUR/USD)
    - `6B` : la livre contre dollar (GBP/USD)
    - `6J` : le yen contre dollar (USD/JPY, JPY/USD)
    - `6A` : le dollar australien contre dollar (AUD/USD)
    Des actions individuelles, un indice étranger (Chine, Moyen-Orient…), le
    bitcoin, des obligations : **aucun** de nos instruments n'est ce marché,
    `exact_roots` vaut `[]`, et c'est une réponse valable. Ne rapproche pas
    « par ressemblance » : la classe est ajoutée par le code, pas par toi ;
  - `sessions` : nos fenêtres (heure de New York) que les données du papier
    couvrent — `ASIA` 19:00–03:00, `EUROPE` 03:00–09:30, `US` 09:30–16:00 —
    avec `sessions_quoted` ; ou `null` avec `sessions_reason` si le papier ne
    le dit pas.

## Ce que tu ne fais pas

Tu ne codes rien, tu ne mesures rien, tu ne juges pas si l'idée est bonne. Tu
dis **ce que le papier dit**, et où il se tait.

---

## LE TEXTE DU PAPIER (pour les deux parties)

Peer-reviewed research 
Can Oil Prices Predict Japanese Yen? Can Oil Prices Predict Japanese Yen? 
Neluka Devpura 1 a 
1 Department of Statistics, Faculty of Applied Sciences, University of Sri Jayewardenepura, Sri Lanka 
Keywords: exchange rate, predictability, time-varying, japanese yen, oil price 
10.46557/001c.17964 
Asian Economics Letters 
In this paper, we examine the relationship between Japanese Yen (vis-à-vis the US dollar) 
and the crude oil futures price. The novelty is that we use high frequency (intraday 
hourly) data to examine time-varying predictability. We find limited evidence that oil 
prices predict the Yen. There is no time-varying predictability relationship. 
I. Introduction I. Introduction 
The literature has shown the relevance of exchange rates 
for asset prices, particularly during the COVID-19 period. P. 
K. Narayan et al. (2020), for instance, show that the Yen ex-
change rate predic ts Japanese stock returns. P. K. Narayan 
(2020a) show that the Y en has bec ome more resilient to 
shocks during the C OVID-19 period. P. K. Narayan (2020b) 
shows that bubble ac tivity in the Y en e xchange rate has 
intensified in the C OVID-19 period, rendering the mark et 
more inefficient. Moreo ver, Iyke (2020)  shows that 
COVID-19 virus cases predic t e xchange rates. Ov er the 
COVID-19 period, oil pric es have become over 900% more 
volatile (see Devpura & Narayan, 2020) . Given this litera -
ture, we argue that oil price is also a shock to exchange rates 
given that oil prices have been shown to influence exchange 
rates and there are multiple theories that support such a re-
lationship, such as the terms of trade channel (see Amano 
& Van Norden, 1998) and the wealth channel (see Krugman, 
1983); f or a sur vey of rele vant theories, see Beckmann et 
al. (2020). For empirical studies on oil pric e shocks and ex-
change rates, see, inter alia, Jiang et al. (2020), Nusair & Ol-
son (2019), and Jung et al. (2020).1 
In this paper , w e e xamine whether the W est Texas In -
termediate (WTI) 1-month oil futures pric e predicts Japan-
ese Yen. Our hypo thesis is that the predic tability relation-
ship –that is, the abilit y of oil pric es to predic t exchange 
rates would have become stronger in the C OVID-19 period 
because the Y en has bec ome: (a) more resilient to shocks 
as demonstrated in the w ork of P. K. Narayan (2020a) ; and 
(b) has seen bubble activity intensify (P. K. Narayan, 2020b). 
For this reason, given the evolving literature on the Japan -
ese market, in this study w e focus on Japan. For the Japan -
ese Yen, we choose the U.S. (United States) dollar as a basis 
because the WTI oil futures pric e is e xpressed in U.S. dol -
lars. Our choice of WTI 1-month oil futures pric e is mainly 
because futures are used as a derivativ e contract to hedge 
against any risk or uncertainty. 
Our approach to testing the proposed hypo thesis is to 
employ a time-var ying predic tability model. That our 
dataset is high frequency aids our approach and hypo thesis 
test. Hourly data span 17 hours per day and cover the period 
01/07/2019 to 04/09/2020. Our in-sample predictability set-
up is based on using the first 50% of the sample as the 
first estimation windo w and c ontinue recursive estimation 
by e xpanding the windo w b y an hour thereaf ter until the 
sample is e xhausted. In order to depic t any predic tability 
relationship emanating from COVID-19, we divide the main 
sample into two sub-samples, namely, a pre-COVID-19 pe-
riod (01/07/2019 to 30/12/2019) and a C OVID-19 sub-sam-
ple (from 31/12/2019 to 04/09/2020).2 
The main findings are; first, the oil pric e has predic tive 
ability for Japanese Yen but the evidence is limited. Our re-
sults indicate that, for the full sample, the oil price predicts 
Yen only about 6% of the time. Henc e, we do no t find e vi-
dence that Yen predictability is time-var ying. Second, with 
regards to the direction of the relationship, we discover the 
negative relationship is dominant o verall, particularly dur-
ing the COVID-19 sample. We evaluate the sensitivity of our 
results to the in-sample window choice by setting it to 25% 
of the data. W e obtain consistent results regarding the di -
rection of the negative relationship. 
This paper c ontributes to the literature in the f ollowing 
way. P ost-COVID-19, the Japanese Y en has rec eived most 
attention from an e xchange rate e volution and behavior 
points of view, as reviewed earlier. We add to these studies 
by showing that the e volution of the Y en in the C OVID-19 
period has lit tle to do with the oil pric e, which has tradi -
tionally been regarded as a predictor of exchange rates. 
The research paper is organized as follows. Section II ex-
plains our data and methodology . Section III presents and 
discusses results. Finally, we present concluding remarks in 
Section IV. 
II. Data and Methodology II. Data and Methodology 
We have Japanese Y en against the US dollar as the e x-
change rate variable ( ) and the WTI 1-month oil 
Corresponding author: Department of Statistics, Faculty of Applied Sciences, University of Sri Jayewardenepura, Sri Lanka. Email: nde-
vpura@sci.sjp.ac.lk 
For oil price and exchange rate relationship, see Basher et al. (2012, 2016); for U.S. dollar and oil relationship, see F. Wen et al. (2018) and 
D. Wen et al. (2020); for oil price and Indonesia’s exchange rate, see S. Narayan et al. (2019); and for oil price and Fiji’s exchange rate, see 
P. K. Narayan et al. (2008). Moreover, Liu et al. (2020) examine whether oil price predicts exchange rates. 
For Japanese currency and stock market relationship, see P. K. Narayan et al. (2020) study using daily data with the COVID-19 period to 
pre-COVID-19 period. 
a 
1 
2 
Devpura, N. (2020). Can Oil Prices Predict Japanese Yen? Asian Economics Letters.
Table 1: Descriptive Statistics Table 1: Descriptive Statistics 
Panel A: Panel A: 
Full Sample Full Sample 
Panel B: Panel B: 
Pre-COVID-19 Sub-sample Pre-COVID-19 Sub-sample 
Panel C: Panel C: 
COVID-19 Sub-sample COVID-19 Sub-sample 
JPY oil JPY oil JPY oil 
Mean 107.84 46.35 108.00 56.69 107.72 38.77 
Median 107.81 52.44 108.26 56.51 107.50 40.33 
Maximum 112.15 64.57 109.78 62.71 112.15 64.57 
Minimum 102.06 -7.65 105.12 50.60 102.06 -7.65 
Std. Dev. 1.42 13.13 1.10 2.33 1.61 12.61 
Skewness -0.13 -0.91 -0.67 0.21 0.12 -0.23 
Jarque-Bera 32.83 725.73 191.16 38.42 8.64 36.23 
Probability 0.00 0.00 0.00 0.00 0.01 0.00 
Observations 5270 5270 2227 2227 3043 3043 
Panel D: Japanese Yen Log Percentage Return Panel D: Japanese Yen Log Percentage Return 
Pre-COVID COVID 
Mean 0.000 -0.001 
Median 0.000 0.000 
Maximum 1.266 1.090 
Minimum -0.672 -3.111 
Std. Dev. 0.085 0.135 
Skewness 1.005 -4.054 
Jarque-Bera 86666 1249034 
Probability 0.00 0.00 
Observations 2226 3042 
This table reports descriptive statistics of the Japanese Yen (against the U.S. dollar) and the WTI 1-month oil futures price. Panel A shows the results for the full sample period from 
01/07/2019 to 04/09/2020, Panel B indicates the pre-COVID-19 sub-sample from 1/07/2019 to 30/12/2019 and Panel C shows the COVID-19 sub-sample from 31/12/2019 to 04/09/
2020. The Panel D presents descriptive statistics for the Japanese Yen log percentage returns for both the pre-COVID-19 and the COVID-19 sub-samples. 
futures pric e as a pro xy f or oil pric e ( oil). The data are 
17-hour per day, from 01:00am to 17:00pm. The time frame 
is from 01/07/2019 to 04/09/2020. The data include the 
COVID-19 period: we divide the main sample into tw o sub-
samples, namely the pre-C OVID-19 period (01/07/2019 to 
30/12/2019) and the C OVID-19 sub-sample period (31/12/
2019 to 04/09/2020). 
We calculate the natural log perc entage returns of the 
Yen as: 
We emplo y the W esterlund and Narayan (2012, 2015) 
predictive regression model that examines the null hypoth-
esis of no predictability, , as follows: 
In this regression, we include  in order to control 
for persistency and endogeneity of the oil variable, and  is 
the disturbance term. In order to c ontrol for heteroskedas-
ticity, we divide each variable by its corresponding standard 
deviation. Finally, the c oefficients are estimated using the 
Ordinary Least Squares method. 
III. Discussion of Results III. Discussion of Results 
In this section, we elaborate on the descriptive statistics 
followed by the time-varying results from Equation (2). 
Table 1 (Panel A) shows the descriptive statistics for the 
full sample of data while P anels B and C sho w statistics for 
the pre-COVID-19 and the COVID-19 sub-samples, respec-
tively. The average of Japanese Yen is roughly the same f or 
the full sample and the two sub-samples. When we consider 
the standard deviation, we see the lowest is reported for the 
pre-COVID-19 sample (JPY 1.10). The sk ewness measure is 
negative in bo th the full sample and the pre-C OVID sam-
ple; however, in the C OVID-19 sample it is positiv e, indi -
cating possible asymmetry. The Jarque-Bera test rejects the 
null hypothesis of normalit y for all samples in the case of 
the Yen. Regarding evidence from oil pric e data, the av er-
age is lo west in the C OVID-19 sample. The standard de vi-
ation is highest in the full sample. Ho wever, when we split 
the data into sub-samples, the standard de viation is high -
er in the C OVID-19 sample. This indicates that the high -
er volatility in the full sample is mainly c oming from the 
COVID-19 period. For oil pric e, the null of normalit y is re -
jected for all samples. Finally , Panel D reports the descrip -
tive measures for the log percentage returns of the Yen. The 
average is negative and volatility is higher in the COVID-19 
sample compared to the pre-COVID-19 period. 
Our objec tive is to e xamine the time-var ying relation -
ship between the Yen and the oil pric e. Figure 1 illustrates 
the results from Equation (2). The recursiv e coefficients of 
the oil pric e variable are presented in P anel A. W e hav e 
a horizontal line across 0 to diff erentiate the positiv e and 
negative values. W e no tice that the direc tion of the rela -
tionship is unstable. Ho wever, from mid-March 2020 the 
sign is negative throughout. The c orresponding -statistics 
of the oil price coefficients are plotted in Panel B. The hor-
izontal line at  indicates the standard normal distribu-
Can Oil Prices Predict Japanese Yen?
Asian Economics Letters 2
Figure 1: Time-Varying Oil Coefficients -Full sample (01/07/2019 to 04/09/2020) Figure 1: Time-Varying Oil Coefficients -Full sample (01/07/2019 to 04/09/2020) 
This figure illustrates the regression results from the model,  Here,  is the Japanese Yen in natural log percentage return 
form,  is the WTI 1-month oil futures price, and  is the disturbance term. We use a recursive window to estimate time-varying  coefficients. The first 50% of the data are 
used as an in-sample period and the model is estimated. We then increase the sample by one observation (by one-hour) and generate the second estimated . We use this 
process until the last observation of the data is completed. Panel A indicates  estimated from the model against time and Panel B shows the corresponding -statistics against 
time. The horizontal line at  1.96 is to identify the significance of the  at 5% significance level. 
tion values at the 5% level of significance. If the coefficients 
lie beyond these limits, then the relationship can be consid-
ered as statistically significant. W e notice that only in the 
month of March 2020 oil prices predict Yen. 
In Figure 2, for the pre-COVID-19 period (Panel A), the 
-statistics range from 0 to 1.2 and sho w a positive relation-
ship throughout the pre-C OVID-19 period. Ho wever, the 
-statistics for the COVID-19 sample (Panel B) are dominat-
ed by negative values. Overall, we do not find evidence that 
oil prices predict the Yen when using a 50% recursive time-
varying approach. 
For robustness, w e re-estimated Equation (2) b y using 
25% of the initial data as in-sample and the proc ess is con-
tinued until all the data are used. The results are not shown 
here due to spac e c onstraints but are available upon re -
quest. We find that the results are consistent with those ob-
tained when using a 50% in-sample window. Again, the only 
period when oil prices predict the Yen is in March 2020. 
IV. Conclusion IV. Conclusion 
We examine the relationship betw een the Japanese Y en 
(vis-à-vis the US dollar) and the WTI 1-month oil futures 
price using hourly data (01/07/2019 to 04/09/2020). Our 
main c ontribution is that w e test the predic tability rela -
tionship using a time-varying model. Based on 50% of data 
in-sample, w e find that in only about 6% of the sample 
oil prices predic t the Y en. This relationship only e xists in 
March 2020. P ost-March 2020, there is no e vidence of any 
predictability. Our main c onclusion, theref ore, is that oil 
prices and the Yen do not share a time-varying predictabili-
ty relationship. 
Submitted: October 30, 2020 AEDT, Accepted: November 13, 
2020 AEDT 
Can Oil Prices Predict Japanese Yen?
Asian Economics Letters 3
Figure 2: Time-varying t-statistics for sub-sample Figure 2: Time-varying t-statistics for sub-sample 
This figure illustrates the regression results from the model, . Here,  is the Japanese Yen in natural log percentage return 
form,  is the WTI 1-month oil futures price, and  is the disturbance term. We use a recursive window to estimate time-varying  coefficients. The first 50% of the data are 
used as an in-sample period and the model is estimated. We then increase the sample by one observation (by one-hour) and generate the second estimated . We use this 
process until the last observation of the data is used. Panel A indicates -statistics against time for the pre-COVID-19 sample (01/07/2019 to 30/12/2019) and Panel B shows 
the -statistics against time for the COVID-19 sample (31/12/2019 to 04/09/2020) respectively. 
This is an open-access article distributed under the terms of the Creative Commons Attribution 4.0 International License (CC-
BY-SA-4.0). View this license’s legal deed at https://creativecommons.org/licenses/by-sa/4.0 and legal code at https://cre-
ativecommons.org/licenses/by-sa/4.0/legalcode for more information. 
Can Oil Prices Predict Japanese Yen?
Asian Economics Letters 4
REFERENCES 
Amano, R. A., & Van Norden, S. (1998). Exchange 
rates and oil prices. Review of International 
Economics, 6(4), 683–694. https://doi.org/10.1111/14
67-9396.00136 
Basher, S. A., Haug, A. A., & Sadorsky, P. (2012). Oil 
prices, exchange rates and emerging stock markets. 
Energy Economics, 34(1), 227–240. https://doi.org/1
0.1016/j.eneco.2011.10.005 
Basher, S. A., Haug, A. A., & Sadorsky, P. (2016). The 
impact of oil shocks on exchange rates: A Markov-
switching approach. Energy Economics, 54, 11–23. ht
tps://doi.org/10.1016/j.eneco.2015.12.004 
Beckmann, J., Czudaj, R. L., & Arora, V. (2020). The 
relationship between oil prices and exchange rates: 
Revisiting theory and evidence. Energy Economics, 
88, 104772. https://doi.org/10.1016/j.eneco.2020.1047
72 
Devpura, N., & Narayan, P. K. (2020). Hourly oil price 
volatility: The role of COVID-19. Energy Research 
Letters, 1(2). https://doi.org/10.46557/001c.13683 
Iyke, B. N. (2020). The Disease Outbreak Channel of 
Exchange Rate Return Predictability: Evidence from 
COVID-19. Emerging Markets Finance and Trade, 
56(10), 2277–2297. https://doi.org/10.1080/1540496
x.2020.1784718 
Jiang, Y., Feng, Q., Mo, B., & Nie, H. (2020). Visiting 
the effects of oil price shocks on exchange rates: 
Quantile-on-quantile and causality-in-quantiles 
approaches. The North American Journal of 
Economics and Finance, 52, 101161. https://doi.org/1
0.1016/j.najef.2020.101161 
Jung, Y. C., Dam, A., & McFarlane, A. (2020). The 
asymmetric relationship between the oil price and the 
US-Canada exchange rate. The Quarterly Review of 
Economics and Finance, 76, 198–206. https://doi.org/
10.1016/j.qref.2019.06.003 
Krugman, P. (1983). .Oil Shocks and Exchange Rate 
Dynamics. , Exchange Rates and International 
Macroeconomics, National Bureau of Economic 
Research, Inc, 259–284. https://EconPapers.repec.or
g/RePEc:nbr:nberch:11382 
Liu, L., Tan, S., & Wang, Y. (2020). Can commodity 
prices forecast exchange rates? Energy Economics, 87, 
104719. https://doi.org/10.1016/j.eneco.2020.104719 
Narayan, P. K. (2020a). Has COVID-19 Changed 
Exchange Rate Resistance to Shocks? Asian 
Economics Letters, 1(1). https://doi.org/10.46557/001
c.17389 
Narayan, P. K. (2020b). Did Bubble Activity Intensify 
During COVID-19? Asian Economics Letters, 1–5. htt
ps://doi.org/10.46557/001c.17654 
Narayan, P. K., Devpura, N., & Wang, H. (2020). 
Japanese currency and stock market-What happened 
during the COVID-19 pandemic? Economic Analysis 
and Policy, 68, 191–198. https://doi.org/10.1016/j.ea
p.2020.09.014 
Narayan, P. K., Narayan, S., & Prasad, A. (2008). 
Understanding the oil price-exchange rate nexus for 
the Fiji islands. Energy Economics, 30(5), 2686–2696. 
https://doi.org/10.1016/j.eneco.2008.03.003 
Narayan, S., Falianty, T., & Tobing, L. (2019). The 
influence if oil prices in Indonesia’s exchange rate. 
Bulletin of Monetary Economics and Banking, 21(3), 
303–322. https://doi.org/10.21098/bemp.v21i3.1007 
Nusair, S. A., & Olson, D. (2019). The effects of oil 
price shocks on Asian exchange rates: Evidence from 
quantile regression analysis. Energy Economics, 
Elsevier, 78, 44–63. 
Wen, D., Liu, L., Ma, C., & Wang, Y. (2020). Extreme 
Risk Spillovers Between Crude Oil Prices and the U.S. 
Exchange Rate Evidence from Oil-exporting and Oil-
importing countries. Energy, 212, 1–16. 
Wen, F., Xiao, J., Huang, C., & Xia, X. (2018). 
Interaction between oil and US dollar exchange rate: 
Nonlinear causality, time-varying influence and 
structural breaks in volatility. Applied Economics, 
50(3), 319–334. https://doi.org/10.1080/00036846.201
7.1321838 
Can Oil Prices Predict Japanese Yen?
Asian Economics Letters 5