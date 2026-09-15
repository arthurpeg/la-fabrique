# La Fabrique

Transforme un corpus de papiers académiques en une poignée de signaux dont les
chiffres tiennent : une IA lit, extrait et implémente ; du code déterministe
juge et compte les tests.

Projet personnel, dépôt privé.

- **`CLAUDE.md`** — la constitution. À lire avant tout le reste.
- **`ETAT.md`** — où en est le projet, et quelle est la prochaine action.
- **`LECONS.md`** — les erreurs déjà payées.

Python 3.13, géré par [`uv`](https://docs.astral.sh/uv/). Les données vivent hors
du dépôt, à l'emplacement `RSL_DATA_DIR` défini dans `.env` (voir `.env.example`).

```bash
uv sync
```
