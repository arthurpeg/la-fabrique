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

---

## `horizon` et `signal_construction` — `null` se justifie

```json
"horizon": {"value": null, "reason": "le papier ne prédit rien ; il décrit une propriété des données"}
```

Un `null` nu est refusé. C'est la règle du catalogue (`CLAUDE.md` § Les
interdits) appliquée ici : l'inconnu s'écrit, il ne se tait pas.

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
