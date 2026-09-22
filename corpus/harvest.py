"""Le moissonneur de corpus — `D20`.

**Il ratisse et il ne juge pas.** Il interroge des catalogues publics sur la
requete ECRITE DANS `D20` avant d'etre lancee, sonde les PDF libres avec le
critere de preuve de `D17`, et les enregistre. Il ne classe pas, ne note pas,
n'ecarte rien pour sa pertinence.

**Ce qu'il ne fait pas, et c'est l'essentiel.** Il ne TRIE pas. Decider qu'un
papier est implementable sur neuf futures intraday est la moitie de la porte 07,
et cette moitie a deja son juge (`corpus/score_triage.py`) et son etalon
(`AMORCE.md`, 20 verdicts humains ecrits en phase 01). Un filtre de pertinence
loge ici ecarterait des papiers sans que rien ne mesure CE QU'IL ECARTE A TORT
— son silence ressemblerait a une absence, ce qui est `L05`.

**Il ne contient aucune intelligence artificielle**, et c'est voulu : chercher,
resoudre une URL, verifier qu'un octet est `%PDF-` ne demande aucun jugement, et
tout y gagne a etre deterministe, gratuit et rejouable. L'IA vient APRES — le
trieur, puis l'extracteur.

**Son produit n'entre pas dans `G1`-`G4`.** `corpus/harvest.json` n'a AUCUNE
autorite sur `corpus/acquisition.json` : la porte 07 se juge sur les
19 atteignables d'`AMORCE.md` et sur rien d'autre (`F47`). Le corpus moissonne
alimente la phase 09.

**Une annonce de PDF libre n'est pas un PDF libre.** OpenAlex rend
`oa_status=bronze` avec un `pdf_url` pointant vers ScienceDirect. Toute URL est
sondee ; aucune n'est crue. Les constantes du critere sont IMPORTEES de
`probe_acquisition.py`, jamais recopiees : deux seuils qui derivent l'un de
l'autre, c'est deux definitions de l'atteignable.

**Rien n'est contourne.** Un controle anti-robot est inscrit `refus_robot` et
reste la.

    python corpus/harvest.py --search      # interroge les catalogues, AUCUN PDF
    python corpus/harvest.py --probe       # sonde les PDF, N'ECRIT AUCUN fichier
    python corpus/harvest.py --fetch       # enregistre dans corpus/pdf/harvest/
    python corpus/harvest.py --report      # l'etat, SANS reseau

Code de sortie 1 si une etape echoue ou si l'etat attendu n'est pas la.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARVEST = REPO / "corpus" / "harvest.json"
CENSUS = REPO / "corpus" / "acquisition.json"
PDFDIR = REPO / "corpus" / "pdf" / "harvest"
AMORCE_PDFDIR = REPO / "corpus" / "pdf"

sys.path.insert(0, str(REPO / "corpus"))
from probe_acquisition import MIN_PDF_BYTES, REASONS, UA  # noqa: E402

# ---------------------------------------------------------------------------
# LA REQUETE. Figee par `D20`, ecrite AVANT d'etre lancee. En changer un seul
# element — un mot-cle, une famille, le domaine, le tri, le plafond — est une
# DECISION ECRITE, et tout comptage de corpus anterieur devient perime.
# ---------------------------------------------------------------------------

AXES_FILE = REPO / "corpus" / "harvest_axes.yaml"


def load_axes() -> dict[str, dict]:
    """Les axes declares, depuis `corpus/harvest_axes.yaml` — `D21`.

    Un axe est un PERIMETRE de recherche, pas un verdict. Ajouter un axe est
    libre ; en modifier un qui a deja servi ne l'est pas, et `check_harvest.py`
    (`H10`) refuse l'ecart en comparant a la chaine enregistree au passage.
    """
    import yaml

    doc = yaml.safe_load(AXES_FILE.read_text(encoding="utf-8"))
    out = {}
    for a in doc["axes"]:
        if a["id"] in out:
            raise SystemExit(f"axe duplique dans harvest_axes.yaml : {a['id']}")
        if a.get("retired"):
            continue
        out[a["id"]] = a
    return out


def select_axes(pattern: str) -> dict[str, dict]:
    """`all`, `family` (tout un axe), ou `anomaly:carry` (un seul)."""
    axes = load_axes()
    if pattern in ("all", "*"):
        return axes
    if ":" in pattern:
        chosen = {k: v for k, v in axes.items() if k == pattern}
    else:
        chosen = {k: v for k, v in axes.items() if k.split(":", 1)[0] == pattern}
    if not chosen:
        raise SystemExit(f"aucun axe ne correspond a {pattern!r} — "
                         f"connus : {', '.join(sorted(axes))}")
    return chosen

# 2002 Economics and Econometrics, 2003 Finance. Sans cette contrainte,
# « overnight » ramene la litterature medicale et « trend following » ramene
# tout : mesure le 2026-09-22, famille B passe de 999 a 14 833 travaux.
SUBFIELDS = "primary_topic.subfield.id:2002|2003"
FROM_DATE = "1995-01-01"
SORT = "cited_by_count:desc"

# Porte de 25 a 60 le 2026-09-22 par le § Journal de `D20`, passage 2. Le
# passage 1 a rendu 43 PDF, sous la cible de 50 a 100 de la phase 09.
#
# **Creuser plus profond n'est pas changer la requete**, et c'est ce qui rend
# cette revision licite : la recherche, le domaine et le tri ne bougent pas, donc
# les 25 premiers de chaque famille sont le PREFIXE EXACT des 60 premiers. Rien
# n'est re-selectionne en voyant ce que le passage 1 a rendu. Changer un
# mot-cle, une famille, le domaine ou le tri resterait une decision a part
# entiere — c'est cela que `D20` verrouille.
PER_FAMILY = 60

OPENALEX = "https://api.openalex.org/works"
UNPAYWALL = "https://api.unpaywall.org/v2"

# Crossref indexe TOUT DOI enregistre. SSRN attribue le prefixe 10.2139 a chacun
# de ses depots, donc `/prefixes/10.2139/works` est la liste des papiers SSRN —
# obtenue sans jamais toucher a ssrn.com, dont le controle anti-robot reste
# intouche. Crossref ne rend AUCUN texte : c'est OpenAlex qui resout ensuite.
#
# Note du 2026-09-22 : l'endpoint de RECHERCHE d'Unpaywall a ete retire le
# 18/09/2026 (`410 Gone`) et sa documentation designe OpenAlex comme son
# successeur, « meme equipe, memes donnees ». `unpaywall_urls` ne reste qu'un
# second avis par DOI, et n'apporte presque rien.
CROSSREF = "https://api.crossref.org/works"
SSRN_PREFIX = "10.2139"
CROSSREF_SORT = "is-referenced-by-count"

# Le « pool poli » d'OpenAlex et l'API d'Unpaywall demandent une adresse de
# courriel. Elle n'est PAS ecrite en dur : c'est une donnee personnelle, et
# l'envoyer a un tiers est un geste que l'utilisateur pose lui-meme, en
# renseignant `HARVEST_MAILTO` dans `.env`. Sans elle, OpenAlex repond quand
# meme (pool commun) et Unpaywall est saute, ce qui est dit a l'ecran.
MAILTO = os.environ.get("HARVEST_MAILTO", "").strip() or None

# Hotes d'editeurs : leur `pdf_url` est le plus souvent une page derriere
# peage. Sondes en DERNIER, jamais exclus — c'est la sonde qui tranche.
PUBLISHER_HOSTS = (
    "sciencedirect.com", "link.springer.com", "onlinelibrary.wiley.com",
    "tandfonline.com", "journals.sagepub.com", "academic.oup.com",
    "jstor.org", "aeaweb.org", "emerald.com", "degruyter.com",
)

# Sans `HARVEST_MAILTO`, OpenAlex nous met dans son pool COMMUN, qui limite plus
# tot : 0,25 s suffisait au plafond de 25, pas a celui de 60. Mesure le
# 2026-09-22, un `429` au passage 2.
PAUSE_API = 1.5
PAUSE_PROBE = 0.5


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def ascii_fold(text: str) -> str:
    """Retire les accents sans rien perdre d'autre."""
    return "".join(c for c in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(c))


def slug(title: str, limit: int = 48) -> str:
    """Un nom de fichier lisible. Sa justesse n'est PAS ce qui garantit
    l'unicite — l'identifiant OpenAlex s'en charge. Voir `D20`."""
    s = re.sub(r"[^a-z0-9]+", "-", ascii_fold(title or "").lower()).strip("-")
    return s[:limit].rstrip("-") or "sans-titre"


def norm_title(title: str) -> str:
    """La forme sur laquelle deux titres se comparent."""
    return re.sub(r"[^a-z0-9]+", " ", ascii_fold(title or "").lower()).strip()


def get_json(url: str, timeout: int = 30, tries: int = 6) -> dict:
    """Une requete de catalogue, avec RECUL PROGRESSIF sur un `429`.

    Un `429` dit « trop vite » : la reponse juste est de ralentir, et c'est
    exactement le contraire d'un contournement. Sans `HARVEST_MAILTO` on
    interroge le pool COMMUN d'OpenAlex, qui limite plus tot — le passage 2 du
    2026-09-22 s'y est casse. L'attente double a chaque essai et le nombre
    d'essais est borne : au-dela, on s'arrete au lieu de marteler.
    """
    # 10, 20, 40, 80, 160 s. Porte de 5 a 10 le 2026-09-22 : au troisieme axe
    # lance dans la meme session, le pool commun refusait encore apres 75 s
    # cumulees. Plus on a demande, plus il faut attendre — c'est la regle, et on
    # l'applique au lieu de la contourner.
    delay = 10.0
    for attempt in range(1, tries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            # Nommer l'hote : « 429 » sans dire QUI limite ne permet pas de
            # savoir quel service ralentir. Defaut trouve le 2026-09-22.
            host = urllib.parse.urlparse(url).netloc
            if e.code != 429 or attempt == tries:
                raise urllib.error.HTTPError(
                    url, e.code, f"{e.reason} — {host}", e.headers, e.fp) from None
            print(f"    429 {host} — pause {delay:.0f} s ({attempt}/{tries - 1})",
                  flush=True)
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("inatteignable")  # pragma: no cover


def probe(url: str, timeout: int = 30) -> dict:
    """Une tentative, et ce qu'elle a REELLEMENT rendu. Meme forme de preuve
    que `probe_acquisition.fetch` : un `200` ne prouve rien, `%PDF-` si."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(400_000)
            length = r.headers.get("Content-Length")
            return {
                "url": url,
                "http": r.status,
                "content_type": (r.headers.get("Content-Type") or "").split(";")[0].strip(),
                "bytes": int(length) if length else len(body),
                "is_pdf": body[:5] == b"%PDF-",
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "http": e.code, "error": f"HTTPError {e.code}"}
    except Exception as e:
        return {"url": url, "http": None, "error": f"{type(e).__name__}: {e}"}


def load() -> dict:
    if not HARVEST.is_file():
        raise SystemExit("corpus/harvest.json absent — lancer d'abord `--search`")
    return json.loads(HARVEST.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    HARVEST.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n",
                       encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Chercher — metadonnees seules, aucun PDF, aucun jugement
# ---------------------------------------------------------------------------

def query_url(search: str, per_page: int, oa_only: bool, sort: str | None) -> str:
    params = {
        "search": search,
        "filter": f"from_publication_date:{FROM_DATE},type:article,{SUBFIELDS}"
                  + (",is_oa:true" if oa_only else ""),
        "per-page": per_page,
    }
    if sort:
        params["sort"] = sort
    if MAILTO:
        params["mailto"] = MAILTO
    return f"{OPENALEX}?{urllib.parse.urlencode(params)}"


def crossref_url(search: str, rows: int) -> str:
    """La liste des papiers SSRN correspondant a `search`, par prefixe de DOI."""
    params = {
        "filter": f"prefix:{SSRN_PREFIX},from-pub-date:{FROM_DATE}",
        "query.bibliographic": search,
        "rows": rows,
        "sort": CROSSREF_SORT,
        "order": "desc",
        "select": "DOI,title,author,issued,container-title,is-referenced-by-count",
    }
    if MAILTO:
        params["mailto"] = MAILTO
    return f"{CROSSREF}?{urllib.parse.urlencode(params)}"


def openalex_by_dois(dois: list[str]) -> dict[str, dict]:
    """Resout des DOI en travaux OpenAlex, PAR PAQUETS.

    OpenAlex accepte un OU sur `doi` avec `|`, jusqu'a 50 valeurs. Cinquante DOI
    en une requete au lieu de cinquante : c'est ce qui rend la voie Crossref
    tenable sans marteler un service qui nous limite deja.

    La resolution est TOLERANTE : si OpenAlex nous limite, on garde ce qui a ete
    resolu et on rend la main. La decouverte Crossref, elle, est acquise et ne
    doit pas etre perdue parce qu'un second service a dit non — les deux pas
    repondent a deux questions distinctes. Le reste se rattrape par `--resolve`.
    """
    out: dict[str, dict] = {}
    for i in range(0, len(dois), 50):
        lot = [d for d in dois[i:i + 50] if d]
        if not lot:
            continue
        params = {"filter": "doi:" + "|".join(lot), "per-page": 50}
        if MAILTO:
            params["mailto"] = MAILTO
        try:
            page = get_json(f"{OPENALEX}?{urllib.parse.urlencode(params)}")
        except urllib.error.HTTPError as e:
            print(f"    resolution interrompue ({e.code}) — {len(out)} resolus, "
                  f"le reste attend `--resolve`", flush=True)
            return out
        for w in page.get("results", []):
            doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            if doi:
                out[doi] = w
        time.sleep(PAUSE_API)
    return out


def amorce_index() -> dict[str, int]:
    """Les titres d'`AMORCE.md`, normalises, pour le dedoublonnage.

    Le titre vit entre guillemets francais dans la citation. Une citation qui
    ne s'y prete pas ne fait PAS echouer le moissonnage : elle prive seulement
    d'une regle de dedoublonnage, et l'empreinte du PDF reste la seconde.
    """
    if not CENSUS.is_file():
        return {}
    out = {}
    for row in json.loads(CENSUS.read_text(encoding="utf-8")):
        m = re.search(r"[««]\s*(.+?)\s*[»»]", row.get("citation") or "")
        if m:
            out[norm_title(m.group(1))] = row["entry"]
    return out


def work_row(work: dict, axis: str, seen_titles: dict[str, int]) -> dict:
    oid = (work.get("id") or "").rsplit("/", 1)[-1]
    title = work.get("title") or work.get("display_name") or ""
    doi = (work.get("doi") or "").replace("https://doi.org/", "") or None
    authors = [(a.get("author") or {}).get("display_name")
               for a in (work.get("authorships") or [])][:8]
    primary = work.get("primary_location") or {}
    dup = seen_titles.get(norm_title(title))
    return {
        "openalex_id": oid,
        # Un papier peut entrer par PLUSIEURS axes, et c'est enregistre : savoir
        # lequel l'a amene n'a pas d'interet, savoir qu'il est au croisement de
        # deux pistes en a (`D21`).
        "axes": [axis],
        "title": title,
        "authors": [a for a in authors if a],
        "year": work.get("publication_year"),
        "doi": doi,
        "venue": ((primary.get("source") or {}).get("display_name")),
        "cited_by_count": work.get("cited_by_count"),
        "oa_status": (work.get("open_access") or {}).get("oa_status"),
        "oa_locations": [
            {"host": ((loc.get("source") or {}).get("display_name")),
             "pdf_url": loc.get("pdf_url"),
             "landing_page_url": loc.get("landing_page_url")}
            for loc in (work.get("locations") or []) if loc.get("is_oa")
        ],
        "found_via": f"OpenAlex, axe {axis}, requete de D20/D21",
        "duplicate_of": ({"rule": "titre normalise, AMORCE.md", "entry": dup}
                         if dup else None),
        "status": None,
        "reason": None,
        "source_url": None,
        "source_via": None,
        "evidence": None,
        "refused_by": None,
        "attempts": [],
        "checked": None,
        "pdf": None,
        "sha256": None,
    }


def migrate(data: dict) -> tuple[dict, int]:
    """Traduit une moisson anterieure a `D21` vers le vocabulaire des axes.

    Les passages 1 et 2 nommaient les familles « A ».. « F ». `D21` les nomme
    `family:A`..`family:F`. La traduction porte sur DEUX endroits — les travaux
    et le recensement des familles — et oublier le second a rendu `H10` rouge
    sur six axes « absents du YAML ». Rien n'est efface : on renomme.
    """
    touched = 0
    for w in data.get("works") or []:
        if "axes" not in w:
            w["axes"] = [f"family:{w.get('family')}"] if w.get("family") else []
            touched += 1
    fams = {}
    for k, v in (data.get("families") or {}).items():
        key = f"family:{k}" if len(k) == 1 else k
        if key != k:
            touched += 1
        fams[key] = v
    data["families"] = fams
    return data, touched


def do_resolve() -> int:
    """Rattrape la resolution des travaux decouverts par Crossref.

    Un papier peut etre DECOUVERT sans etre RESOLU — Crossref dit qu'il existe,
    OpenAlex dit ou vit une copie libre, et le second peut nous limiter quand le
    premier a repondu. Ce geste reprend les non resolus, et lui seul.
    """
    data = load()
    todo = [w for w in data["works"]
            if not w.get("openalex_id") and w.get("doi") and w.get("status") is None]
    if not todo:
        print("rien a resoudre")
        return 0
    print(f"{len(todo)} travail/travaux a resoudre chez OpenAlex")
    resolved = openalex_by_dois([w["doi"] for w in todo])
    done = 0
    for w in todo:
        oa = resolved.get(w["doi"])
        if not oa:
            continue
        w["openalex_id"] = (oa.get("id") or "").rsplit("/", 1)[-1]
        w["oa_status"] = (oa.get("open_access") or {}).get("oa_status")
        w["oa_locations"] = [
            {"host": ((loc.get("source") or {}).get("display_name")),
             "pdf_url": loc.get("pdf_url"),
             "landing_page_url": loc.get("landing_page_url")}
            for loc in (oa.get("locations") or []) if loc.get("is_oa")
        ]
        done += 1
    save(data)
    print(f"{done} resolu(s), {len(todo) - done} toujours inconnus d'OpenAlex")
    return 0


def do_migrate() -> int:
    data, touched = migrate(load())
    save(data)
    print(f"{touched} element(s) traduit(s) vers le vocabulaire de D21, sans reseau")
    return 0


def row_from_crossref(rec: dict, axis: str, seen_titles: dict[str, int]) -> dict:
    """Un papier connu de Crossref mais INCONNU d'OpenAlex.

    Il n'a donc aucun emplacement libre repertorie. On l'inscrit quand meme,
    sonde a vide, et il sortira `sans_source_libre` : c'est la reponse juste
    pour un depot SSRN qu'aucun autre depot ne reprend. L'omettre ferait croire
    qu'on ne l'a pas cherche.
    """
    doi = (rec.get("DOI") or "").lower()
    title = (rec.get("title") or [""])[0]
    authors = [" ".join(filter(None, (a.get("given"), a.get("family"))))
               for a in (rec.get("author") or [])][:8]
    year = ((rec.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    dup = seen_titles.get(norm_title(title))
    return {
        "openalex_id": None,
        "doi": doi,
        "axes": [axis],
        "title": title,
        "authors": [a for a in authors if a],
        "year": year,
        "venue": (rec.get("container-title") or [None])[0],
        "cited_by_count": rec.get("is-referenced-by-count"),
        "oa_status": None,
        "oa_locations": [],
        "found_via": f"Crossref, prefixe {SSRN_PREFIX} (SSRN), axe {axis}, D21",
        "duplicate_of": ({"rule": "titre normalise, AMORCE.md", "entry": dup}
                         if dup else None),
        "status": None, "reason": None, "source_url": None, "source_via": None,
        "evidence": None, "refused_by": None, "attempts": [],
        "checked": None, "pdf": None, "sha256": None,
    }


def work_key(row: dict) -> str:
    """L'identite d'un travail. OpenAlex si connu, sinon son DOI.

    Un papier decouvert par Crossref et resolu par OpenAlex porte le MEME
    identifiant qu'un papier decouvert par OpenAlex : c'est ce qui fait que les
    deux voies se dedoublonnent au lieu de s'additionner.
    """
    return row.get("openalex_id") or f"doi:{(row.get('doi') or '').lower()}"


def do_search(per_family: int, pattern: str = "all") -> int:
    """Cherche, et AJOUTE a ce qui existe deja.

    Un passage ne remplace jamais le precedent : les travaux deja sondes gardent
    leur statut, leur preuve et leur date de constat. Sans quoi approfondir la
    moisson obligerait a resonder tout ce qui l'a deja ete — et effacerait le
    constat date du passage anterieur, qui est une piece du dossier.
    """
    if not MAILTO:
        print("note : HARVEST_MAILTO non renseigne — pool commun d'OpenAlex,\n"
              "       et Unpaywall sera saute au `--probe`. Voir .env.example.\n")
    today = str(date.today())
    seen_titles = amorce_index()
    print(f"dedoublonnage : {len(seen_titles)} titres lus dans AMORCE.md")

    previous = json.loads(HARVEST.read_text(encoding="utf-8")) if HARVEST.is_file() else {}
    previous, migres = migrate(previous)
    works = list(previous.get("works") or [])
    by_id = {work_key(w): w for w in works}
    if works:
        print(f"passage precedent : {len(works)} candidats conserves, "
              f"{sum(1 for w in works if w.get('status'))} deja sondes"
              + (f", {migres} migres vers D21" if migres else ""))

    axes = select_axes(pattern)
    print(f"axes lances : {len(axes)} — {', '.join(sorted(axes))}\n")

    # Meme migration que pour les travaux, et elle avait ete OUBLIEE ici : les
    # passages 1 et 2 ecrivaient les familles sous les cles « A »..« F ». Le
    # garde `H10` l'a trouve tout seul en refusant six axes « absents du YAML ».
    families = dict(previous.get("families") or {})
    for key in sorted(axes):
        spec = axes[key]
        search = spec["search"]
        source = spec.get("source", "openalex")

        if source == "crossref":
            # Decouverte chez Crossref, resolution chez OpenAlex. Les deux pas
            # sont distincts parce qu'ils repondent a deux questions : « ce
            # papier existe-t-il ? » et « ou vit une copie libre ? ».
            page = get_json(crossref_url(search, per_family))["message"]
            time.sleep(PAUSE_API)
            items = page.get("items", [])
            total = oa_total = page.get("total-results", 0)
            resolved = openalex_by_dois([(it.get("DOI") or "").lower() for it in items])
            rows = []
            for it in items:
                doi = (it.get("DOI") or "").lower()
                oa = resolved.get(doi)
                rows.append(work_row(oa, key, seen_titles) if oa
                            else row_from_crossref(it, key, seen_titles))
            oa_total = len(resolved)
        else:
            total = get_json(query_url(search, 1, False, None))["meta"]["count"]
            time.sleep(PAUSE_API)
            page = get_json(query_url(search, per_family, True, SORT))
            time.sleep(PAUSE_API)
            oa_total = page["meta"]["count"]
            rows = [work_row(w, key, seen_titles) for w in page["results"]]

        kept, crossed = 0, 0
        for row in rows:
            k = work_key(row)
            if k in ("", "doi:"):
                continue
            seen = by_id.get(k)
            if seen is not None:
                # Deja trouve par un autre axe : on note le croisement et on
                # garde son statut de sondage. On ne le re-sonde pas.
                if key not in seen.setdefault("axes", []):
                    seen["axes"].append(key)
                    crossed += 1
                continue
            by_id[k] = row
            works.append(row)
            kept += 1
        families[key] = {
            "label": spec["label"], "search": search, "added": str(spec.get("added")),
            "source": source, "total": total, "oa_total": oa_total,
            "retrieved": len(rows), "new": kept,
        }
        tag = "resolus" if source == "crossref" else "libres"
        print(f"  {key:34s} {total:>7,} travaux, {oa_total:>7,} {tag}"
              f" — {kept:>2} nouveaux, {crossed:>2} croises")

    dups = sum(1 for w in works if w["duplicate_of"])
    passages = list(previous.get("passages") or [])
    passages.append({"date": today, "per_family": per_family,
                     "axes": sorted(axes), "candidats_apres": len(works),
                     "mailto_set": bool(MAILTO)})
    data = {
        "decision": "D20+D21",
        "checked": today,
        "query": {"from_date": FROM_DATE, "subfields": SUBFIELDS, "sort": SORT,
                  "per_family": per_family, "oa_only": True,
                  "source": "OpenAlex", "mailto_set": bool(MAILTO)},
        "passages": passages,
        "families": families,
        "works": works,
    }
    save(data)
    print(f"\n{len(works)} candidats au total, dont {dups} deja dans AMORCE.md")
    print(f"a sonder : {sum(1 for w in works if w['status'] is None and not w['duplicate_of'])}")
    print(f"ecrit : {HARVEST.relative_to(REPO)} — AUCUN PDF n'a ete telecharge")
    return 0


# ---------------------------------------------------------------------------
# 2. Sonder — ou vit le PDF, et est-ce vraiment un PDF
# ---------------------------------------------------------------------------

def unpaywall_urls(doi: str) -> list[dict]:
    """Le second avis. Saute sans `HARVEST_MAILTO` : l'API l'exige."""
    if not MAILTO or not doi:
        return []
    try:
        d = get_json(f"{UNPAYWALL}/{urllib.parse.quote(doi)}?email={MAILTO}")
    except Exception:
        return []
    out = []
    for loc in ([d.get("best_oa_location")] + (d.get("oa_locations") or [])):
        if loc and loc.get("url_for_pdf"):
            out.append({"url": loc["url_for_pdf"], "via": "Unpaywall (DOI)"})
    return out


def pdf_candidates(work: dict) -> list[dict]:
    """Toutes les URL ou le PDF pourrait vivre, depots AVANT editeurs.

    L'ordre compte : un `pdf_url` d'editeur est le plus souvent une page
    derriere peage (mesure de `D20` — OpenAlex rend `bronze` sur ScienceDirect).
    Il est sonde quand meme, en dernier : c'est la sonde qui tranche, pas l'ordre.
    """
    repos, publishers = [], []
    for loc in work.get("oa_locations") or []:
        url = loc.get("pdf_url")
        if not url:
            continue
        via = f"OpenAlex, depot « {loc.get('host')} »"
        (publishers if any(h in url for h in PUBLISHER_HOSTS) else repos).append(
            {"url": url, "via": via})
    out = repos + unpaywall_urls(work.get("doi") or "") + publishers
    seen, uniq = set(), []
    for c in out:
        if c["url"] not in seen:
            seen.add(c["url"])
            uniq.append(c)
    return uniq


def verdict(cands: list[dict], attempts: list[dict]) -> dict:
    """Le statut, SA RAISON et la preuve — tires de ce qui a ete observe.

    La liste close de `D17` n'est PAS elargie : `peage`, `refus_robot`,
    `sans_source_libre` couvrent tout ce que le moissonnage rencontre (`L18`).

    **L'ORDRE DES TESTS EST LE FOND DU SUJET, et le premier passage l'a appris
    en se trompant.** Tester le code `403` AVANT l'hote faisait de tout refus un
    `refus_robot` : au passage 1 du 2026-09-22, 64 entrees sur 65 portaient cette
    raison, alors que 56 des 67 tentatives refusees venaient d'hotes d'EDITEURS
    — Wiley 27, ScienceDirect 14, OUP 8, AEA 4. Un editeur qui repond `403` sur
    son propre PDF ne « sert pas un controle anti-robot » : il garde son texte.
    L'hote decide donc en premier, et `refus_robot` est reserve a ce qu'il
    designe vraiment — un refus servi par un site qui n'est pas l'editeur.

    `refused_by` inscrit hote et code pour chaque tentative refusee : une raison
    de liste close doit etre VERIFIABLE, pas seulement plausible.
    """
    got = next((a for a in attempts
                if a.get("is_pdf") and a.get("bytes", 0) >= MIN_PDF_BYTES), None)
    if got:
        src = next(c for c in cands if c["url"] == got["url"])
        return {"status": "atteignable", "reason": None, "source_url": got["url"],
                "source_via": src["via"], "evidence": got, "refused_by": None}

    refused = [{"host": urllib.parse.urlparse(a["url"]).netloc, "http": a.get("http")}
               for a in attempts]
    publisher = [r for r in refused if any(h in r["host"] for h in PUBLISHER_HOSTS)]

    if refused and len(publisher) == len(refused):
        reason = "peage"
    elif any(r["http"] in (403, 429) for r in refused if r not in publisher):
        reason = "refus_robot"
    elif publisher:
        reason = "peage"
    else:
        reason = "sans_source_libre"
    return {"status": "inatteignable", "reason": reason, "source_url": None,
            "source_via": None, "evidence": None, "refused_by": refused or None}


def do_reverdict() -> int:
    """Recalcule les verdicts sur les tentatives DEJA enregistrees, sans reseau.

    Existe parce qu'une regle de verdict peut se reveler fausse APRES coup — ce
    qui est arrive au passage 1 — et qu'il serait absurde de resonder cent hotes
    pour corriger une erreur qui est entierement dans notre code. Les tentatives
    sont le fait observe ; le verdict n'en est que la lecture.
    """
    data = load()
    before = {w["openalex_id"]: w.get("reason") for w in data["works"]}
    touched = 0
    for w in data["works"]:
        if not w.get("attempts") and w.get("status") is None:
            continue
        cands = [{"url": a["url"], "via": w.get("source_via") or "inconnu"}
                 for a in w["attempts"]]
        w.update(verdict(cands, w["attempts"]))
        if before[w["openalex_id"]] != w.get("reason"):
            touched += 1
    save(data)
    after: dict[str, int] = {}
    for w in data["works"]:
        if w["status"] == "inatteignable":
            after[w["reason"]] = after.get(w["reason"], 0) + 1
    print(f"{touched} verdict(s) change(s), sans une seule requete reseau\n")
    for reason, n in sorted(after.items()):
        was = sum(1 for k, v in before.items() if v == reason)
        print(f"  {reason:<18} {was:>3} -> {n:>3}   {REASONS.get(reason, '')}")
    return 0


def do_probe(limit: int | None) -> int:
    data = load()
    today = str(date.today())
    todo = [w for w in data["works"] if w["status"] is None and not w["duplicate_of"]]
    if limit:
        todo = todo[:limit]
    print(f"{len(todo)} candidats a sonder "
          f"({sum(1 for w in data['works'] if w['duplicate_of'])} doublons sautes)\n")

    for i, w in enumerate(todo, 1):
        cands = pdf_candidates(w)
        attempts = []
        for c in cands:
            attempts.append(probe(c["url"]))
            time.sleep(PAUSE_PROBE)
            if attempts[-1].get("is_pdf") and attempts[-1].get("bytes", 0) >= MIN_PDF_BYTES:
                break
        w.update(verdict(cands, attempts))
        w["attempts"] = attempts
        w["checked"] = today
        mark = "PDF " if w["status"] == "atteignable" else f"{w['reason']:<18}"
        print(f"  {i:>3}/{len(todo)} {mark} {w['title'][:56]}")
        if i % 10 == 0:
            save(data)

    save(data)
    ok = sum(1 for w in data["works"] if w["status"] == "atteignable")
    print(f"\n{ok} atteignables sur {len(data['works'])} candidats")
    print("AUCUN fichier n'a ete ecrit — c'est `--fetch` qui enregistre")
    return 0


# ---------------------------------------------------------------------------
# 3. Enregistrer — et verifier APRES ecriture
# ---------------------------------------------------------------------------

def filename(work: dict) -> str:
    """`<titre-abrege>-<identifiant OpenAlex>.pdf`.

    L'identifiant garantit l'unicite PAR CONSTRUCTION ; le titre ne sert qu'a
    la lisibilite. C'est la parade de `fetch_pdfs.py` (« un nom fabrique par
    expression reguliere se casse en silence ») tenue autrement, sa table
    ecrite a la main ne passant pas a cent papiers. Voir `D20`.
    """
    ident = work.get("openalex_id") or slug(work.get("doi") or "", 32) or "sans-id"
    return f"{slug(work['title'])}-{ident}.pdf"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def known_hashes() -> dict[str, str]:
    """Les empreintes des PDF deja sur le disque — seconde regle de
    dedoublonnage, celle qui ne depend pas de la forme d'une citation."""
    out = {}
    for pdf in sorted(AMORCE_PDFDIR.glob("*.pdf")):
        out[sha256(pdf)] = pdf.name
    return out


def do_fetch(dry_run: bool) -> int:
    data = load()
    PDFDIR.mkdir(parents=True, exist_ok=True)
    targets = [w for w in data["works"] if w["status"] == "atteignable"]
    if not targets:
        raise SystemExit("aucun atteignable — lancer `--probe` d'abord")

    hashes = known_hashes() if not dry_run else {}
    names: dict[str, str] = {}
    taken, present, failed, dups = 0, 0, [], 0

    for w in targets:
        name = filename(w)
        if name in names and names[name] != work_key(w):
            raise SystemExit(f"collision de nom : {name} — a corriger, pas a resoudre")
        names[name] = work_key(w)
        dest = PDFDIR / name

        if dry_run:
            print(f"  a prendre | ~{w['evidence'].get('bytes', 0):>8} o | {name}")
            continue

        if dest.is_file() and dest.stat().st_size >= MIN_PDF_BYTES:
            present += 1
        else:
            try:
                req = urllib.request.Request(w["source_url"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read()
                if body[:5] != b"%PDF-" or len(body) < MIN_PDF_BYTES:
                    failed.append((name, f"pas un PDF plausible ({len(body)} o)"))
                    print(f"  ECHEC     | {name}")
                    continue
                tmp = dest.with_suffix(".part")
                tmp.write_bytes(body)
                tmp.replace(dest)
                taken += 1
            except Exception as e:
                failed.append((name, f"{type(e).__name__}: {e}"))
                print(f"  ECHEC     | {name}")
                continue
            time.sleep(PAUSE_PROBE)

        digest = sha256(dest)
        w["sha256"] = digest
        w["pdf"] = str(dest.relative_to(REPO)).replace("\\", "/")
        if digest in hashes:
            dups += 1
            w["duplicate_of"] = {"rule": "empreinte sha256", "file": hashes[digest]}
            print(f"  DOUBLON   | {name}  =  {hashes[digest]}")
        else:
            hashes[digest] = name
            print(f"  {'deja la' if not taken else 'pris':<9} | {dest.stat().st_size:>8} o"
                  f" | {name}")

    if not dry_run:
        save(data)
        print(f"\n{taken} pris, {present} deja la, {len(failed)} en echec, "
              f"{dups} doublon(s) d'un PDF existant")
        for name, why in failed:
            print(f"  {name} : {why}")
    return 1 if failed else 0


# ---------------------------------------------------------------------------
# 4. L'etat, sans reseau
# ---------------------------------------------------------------------------

def do_report() -> int:
    data = load()
    works = data["works"]
    print(f"moisson du {data['checked']} — requete de {data['decision']}\n")
    print(f"  {'axe':32s} {'total':>7s} {'libres':>7s} {'pris':>5s} {'PDF':>5s}")
    for key, f in data["families"].items():
        # Compte sur les travaux eux-memes, et non sur le `new` du dernier
        # passage : apres un second passage, `new` ne dit plus que l'ajout.
        mine = [w for w in works if key in (w.get("axes") or [])]
        got = sum(1 for w in mine if w["status"] == "atteignable")
        print(f"  {key:32s} {f['total']:>7,} {f['oa_total']:>7,} "
              f"{len(mine):>5} {got:>5}")
    croises = sum(1 for w in works if len(w.get("axes") or []) > 1)
    print(f"  {'(au croisement de 2 axes ou plus)':32s} {'':>7s} {'':>7s} {croises:>5}")

    done = [w for w in works if w["status"]]
    ok = [w for w in works if w["status"] == "atteignable"]
    dup = [w for w in works if w["duplicate_of"]]
    on_disk = [w for w in ok if w["pdf"] and (REPO / w["pdf"]).is_file()]
    print(f"\n  candidats        {len(works):>4}")
    print(f"  sondes           {len(done):>4}")
    print(f"  atteignables     {len(ok):>4}")
    print(f"  doublons         {len(dup):>4}")
    print(f"  PDF sur CE poste {len(on_disk):>4}  <- se verifie, ne se lit pas (L19)")
    by_reason = {}
    for w in works:
        if w["status"] == "inatteignable":
            by_reason[w["reason"]] = by_reason.get(w["reason"], 0) + 1
    for reason, n in sorted(by_reason.items()):
        print(f"    {reason:<18} {n:>3}  {REASONS.get(reason, '')}")
    print("\nCe fichier n'entre PAS dans G1-G4 (D20, F47) : la porte 07 se juge")
    print("sur les 19 atteignables d'AMORCE.md et sur rien d'autre.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Le moissonneur de corpus — D20")
    ap.add_argument("--search", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--reverdict", action="store_true")
    ap.add_argument("--migrate", action="store_true")
    ap.add_argument("--resolve", action="store_true")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--per-family", type=int, default=PER_FAMILY)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--axis", default="all",
                    help="`all`, un axe entier (`anomaly`) ou un seul "
                         "(`anomaly:reversal`). Voir corpus/harvest_axes.yaml")
    ap.add_argument("--axes", action="store_true", help="liste les axes declares")
    a = ap.parse_args(argv)

    if a.axes:
        for k, v in sorted(load_axes().items()):
            print(f"  {k:34s} {v['label']:38s} (declare le {v.get('added')})")
        return 0
    if a.search:
        return do_search(a.per_family, a.axis)
    if a.probe:
        return do_probe(a.limit)
    if a.reverdict:
        return do_reverdict()
    if a.migrate:
        return do_migrate()
    if a.resolve:
        return do_resolve()
    if a.fetch:
        return do_fetch(a.dry_run)
    if a.report:
        return do_report()
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
