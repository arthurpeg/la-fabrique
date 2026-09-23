"""L'entrée du trieur pour les papiers moissonnés — `D15` appliqué hors `AMORCE.md`.

`corpus/make_triage_input.py` fabrique l'entrée du trieur depuis `AMORCE.md` :
une ligne écrite à la main, privée de sa colonne verdict. Les 119 papiers
moissonnés n'ont pas de telle ligne — personne ne les a résumés. Ce script
fabrique l'équivalent **depuis le papier lui-même** : titre, année, auteurs, et
ses premiers morceaux de texte, qui portent le résumé.

**Il n'y a rien à faire fuiter ici, et c'est la différence avec `AMORCE.md`.**
Le risque que `make_triage_input.py` combat — donner au trieur le verdict que
l'humain avait déjà écrit — n'existe pas : aucun verdict n'existe pour ces
papiers. Le trieur travaille donc sur la matière brute, ce qui est plus dur et
plus honnête.

**Ce que ce script NE fait PAS : juger.** Il prépare. Le verdict est rendu par
une session séparée, sur l'échelle de `D15` — `oui`, `partiel`, `non` — et il
n'y a pas d'étalon humain pour le noter. La note du trieur a été prise au
passage 1 du 2026-09-20 sur les 20 d'`AMORCE.md` (A/B/C/D = 1/0/2/0) ; ici il
est **en production**, pas à l'examen.

    python corpus/triage_harvest.py            # ecrit les consignes par lots
    python corpus/triage_harvest.py --lot 30   # taille de lot
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "vectordb"))

WORK = REPO / "corpus" / "consignes-triage"
SORTIE = REPO / "corpus" / "triage_harvest.json"

RESUME_CHARS = 1100  # de quoi porter un resume, pas une page de garde entiere

CONSIGNE = """\
# Consigne de triage — papiers moissonnés

Tu rends **un verdict par papier** : ce papier est-il implémentable comme signal
sur **notre univers**, et sur rien d'autre ?

## Notre univers, qui est la seule chose qui compte ici

- **9 contrats à terme** : NQ, ES, YM (indices actions US), GC (or), CL (pétrole),
  6E, 6B, 6J, 6A (devises).
- **Barres d'une minute, OHLCV seulement** : ouverture, haut, bas, clôture,
  volume. **Rien d'autre.** Pas de carnet d'ordres, pas de données d'options,
  pas de fondamentaux, pas de positions de traders, pas de nouvelles.
- **Horizon intrajournalier**, jusqu'à quelques jours.
- Historique 2016 → 2023 pour la recherche.

## L'échelle, et elle a trois crans

| Verdict | Quand |
|---|---|
| `oui` | la recette du papier se calcule **entièrement** sur nos 9 contrats en OHLCV |
| `partiel` | l'idée transfère mais il manque quelque chose — un autre
univers, une donnée partiellement absente, un horizon à adapter |
| `non` | infaisable chez nous : donnée absente, univers incompatible
(actions individuelles, obligations, crypto), ou ce n'est pas un signal de prix |

**Sois franc sur `non`.** Un papier d'économie, de politique monétaire, de
comportement du consommateur, de régulation, de macro : c'est `non`, sans
hésiter. Le moissonneur ratisse large **exprès** et n'a jamais prétendu juger.

**Et sois franc sur `oui`.** Un `non` promu `oui` coûte un papier lu, une fiche
écrite et un signal codé pour rien. Un `oui` manqué coûte un papier de moins,
et ça se rattrape.

## Ce que tu rends

**Un seul tableau JSON**, rien avant, rien après :

```json
[
  {{"id": "<l'id donné>", "verdict": "oui|partiel|non", "raison": "<une phrase>"}},
  ...
]
```

Une ligne par papier, **dans l'ordre donné**, aucune omise. La `raison` dit ce
qui décide — la donnée manquante, l'univers incompatible, ou ce qui rend la
recette calculable chez nous.

---

## LES PAPIERS — lot {lot} sur {total}

{papiers}
"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Entrée du trieur pour le moissonnage")
    ap.add_argument("--lot", type=int, default=30, help="papiers par consigne")
    a = ap.parse_args(argv)

    from vector_db import VectorDB

    with VectorDB.from_env() as db, db.conn.cursor() as c:
        c.execute("""
            select p.id, p.title, p.year, p.authors,
                   string_agg(ch.content, ' ' order by ch.ordinal) as debut
            from papers p
            left join lateral (
                select content, ordinal from chunks
                where paper_id = p.id order by ordinal limit 3
            ) ch on true
            where p.text_source = 'harvest'
            group by p.id
            order by p.title
        """)
        papiers = c.fetchall()

    WORK.mkdir(parents=True, exist_ok=True)
    for f in WORK.glob("lot-*.md"):
        f.unlink()

    lots = [papiers[i:i + a.lot] for i in range(0, len(papiers), a.lot)]
    for n, lot in enumerate(lots, 1):
        blocs = []
        for p in lot:
            auteurs = ", ".join((p["authors"] or [])[:4]) or "auteurs inconnus"
            debut = " ".join((p["debut"] or "").split())[:RESUME_CHARS]
            if not debut:
                # `L21` : un papier sans texte ne DISPARAIT pas du lot. Il y
                # figure avec son manque, et le trieur tranche sur le titre.
                debut = ("AUCUN TEXTE EXTRAIT — l'extraction du PDF n'a rien "
                         "rendu. Juge sur le titre seul, et dis-le dans la raison.")
            blocs.append(
                f"### id `{p['id']}`\n\n"
                f"**{p['title']}** — {auteurs}, {p['year'] or 'année inconnue'}\n\n"
                f"> {debut}\n"
            )
        (WORK / f"lot-{n:02d}.md").write_text(
            CONSIGNE.format(lot=n, total=len(lots), papiers="\n".join(blocs)),
            encoding="utf-8",
        )

    SORTIE.write_text(json.dumps(
        [{"id": str(p["id"]), "title": p["title"]} for p in papiers],
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{len(papiers)} papiers moissonnés, {len(lots)} lot(s) de {a.lot}")
    for n in range(1, len(lots) + 1):
        f = WORK / f"lot-{n:02d}.md"
        print(f"  {f.relative_to(REPO)}  ({f.stat().st_size / 1000:.0f} ko)")
    print("\nLE TRIEUR EST ICI EN PRODUCTION, PAS A L'EXAMEN : aucun etalon")
    print("humain n'existe pour ces papiers, donc `score_triage.py` ne peut pas")
    print("les noter. Sa note a ete prise au passage 1 du 2026-09-20 sur les 20")
    print("d'AMORCE.md, et c'est elle qui fonde qu'on lui fasse confiance ici.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
