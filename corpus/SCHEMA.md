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
qu'aucun schéma ne prévoit — `friction`, `walk_forward`, `acceptance_criteria`
existent dans la fiche Mesfin parce que ce papier les impose. Le schéma fixe un
plancher, pas un plafond.

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
comité de lecture, et la distinction a déjà servi (Mesfin).

---

## `reported_results` — une liste, et chaque entrée porte sa citation

C'est ici que `D09` s'étend aux fiches. **Un résultat recopié d'un papier est une
valeur externe** : rien dans le dépôt ne peut la contredire.

```json
"reported_results": [
  {
    "name": "u_shape_peak_over_trough",
    "value": 1.91,
    "unit": "rapport",
    "quoted": "starting out at 0.095% in the morning … 0.055% around noon … 0.105% towards the end",
    "note": "0,105 / 0,055. Calculé par nous à partir des trois niveaux cités."
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

Un nombre **dérivé** par nous — comme le rapport 1,91, que les auteurs ne
donnent pas tel quel — n'a pas à figurer dans la citation : il porte
`"derived": true`, et le contrôle numérique est alors levé. Le `note` doit dire
comment il a été obtenu.

**Et un nombre écrit en toutes lettres.** Mesfin écrit « *Eleven signal families
fail* » : il n'y a aucun chiffre à retrouver. L'entrée porte alors
`"spelled_out": "Eleven"`, et le validateur vérifie que **le mot** est dans la
citation. Ce qu'il ne vérifie pas — que « Eleven » vaut 11 — reste un geste
humain, et le champ existe pour le **nommer** plutôt que pour le cacher derrière
`derived`, qui signifierait à tort qu'un calcul a eu lieu.

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

**Pourquoi c'est obligatoire.** C'est ce champ qui a écarté Mesfin de la porte 06
— sa métrique est un rendement net par trade, la nôtre un IC — et qui a cadré
Heston, dont seul le motif transférait. Une fiche sans lui dit ce qu'un papier
affirme, pas ce qu'il vaut ici.

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
