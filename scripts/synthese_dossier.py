"""La synthèse d'un dossier — un papier et ses voisins dans toute la base (`D47`).

`scripts/voisins.py` trouve, par le sens, les papiers proches d'une fiche dans
toute la base, fichés ou non (`D45`). Ce script en fait une **consigne de
synthèse** : la fiche graine, et pour chaque voisin ses meilleurs passages (et
sa fiche s'il en a une). Une session isolée (`fabrique-synthese`) lit cette
consigne — **aucun résultat de nos données** — et écrit UNE fiche de synthèse :
l'hypothèse du papier graine, **complétée** par ce que les voisins apportent,
une seule version, choisie avant toute mesure selon `synthese.CRITERES`.

**Ce qui fait foi pour une citation d'un voisin sans fiche** : son texte en base,
**figé** au moment de la préparation dans `corpus/text/base-<id>.default.txt`,
versionné comme les extractions de `D18`. Le validateur y cherche chaque
citation à la lettre, et la recette (`recette.texte_du_papier`) le relit sans
changement. Un voisin fiché garde ses propres extractions.

La fiche rendue entre ensuite dans la chaîne ordinaire : recette, deux codeurs,
double codage, hypothèse, lot.

    python scripts/synthese_dossier.py --candidats <fiche_graine> [--n 30]   # puis fabrique-voisins
    python scripts/synthese_dossier.py --prepare <fiche_graine>   # puis fabrique-synthese
    python scripts/synthese_dossier.py --record <fiche de synthèse>
    python scripts/synthese_dossier.py --check  <fiche de synthèse>
    python scripts/synthese_dossier.py --status
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "corpus"))
sys.path.insert(0, str(REPO / "vectordb"))

from codage_verifie import empreinte16  # noqa: E402
from synthese import CRITERES, DOSSIER, PRODUCED, SCHEMA, WORK, do_record  # noqa: E402

DOSSIERS = REPO / "corpus" / "dossiers"
TEXT = REPO / "corpus" / "text"
PASSAGES = 4  # passages par voisin montrés à la synthèse

# D52 : ce que la synthèse dit de CHAQUE voisin, dans une liste fermée. C'est la
# logique imposée à l'agent : il ne retient pas un voisin parce qu'il est proche,
# il dit ce qu'il apporte, ou pourquoi il ne sert pas.
ROLES = {
    "complete": "apporte à la graine ce qu'elle n'a pas : un paramètre, un marché, un horizon,"
                " une étape de construction — cité",
    "confirme": "décrit le même mécanisme, sans rien ajouter à la construction",
    "contredit": "trouve l'effet inverse, ou son absence, sur un marché ou un horizon",
    "deja_teste": "a déjà sa propre hypothèse, et la synthèse ne ferait que la refaire",
    "hors_sujet": "proche par les mots, pas par le mécanisme",
}
GARDES = ("complete", "confirme", "contredit")  # les rôles qui font une source


def sid_de(graine: str) -> str:
    return f"synthese-dossier-{graine}"


def base_id(paper_id: str) -> str:
    """L'identifiant d'un voisin sans fiche : le début de son identifiant en base."""
    return f"base-{paper_id[:8]}"


def fiches() -> dict[str, Path]:
    from code_signal import fiche_files  # noqa: PLC0415

    return {k: v for k, v in fiche_files().items() if not k.startswith("synthese-")}


def figer_texte(api, paper_id: str, ident: str) -> Path:
    """Le texte entier du papier en base, morceau après morceau, figé une fois."""
    out = TEXT / f"{ident}.default.txt"
    if out.is_file():
        return out
    morceaux, debut = [], 0
    while True:
        lot = api.appel("GET", f"/rest/v1/chunks?select=ordinal,content&paper_id=eq.{paper_id}"
                               f"&order=ordinal&offset={debut}&limit=1000") or []
        morceaux += lot
        if len(lot) < 1000:
            break
        debut += 1000
    if not morceaux:
        raise SystemExit(f"aucun morceau en base pour {paper_id}")
    out.write_text("\n\n".join(m["content"] for m in morceaux) + "\n", encoding="utf-8")
    return out


def liens() -> dict[str, str]:
    """`fiche_id` -> identifiant du papier en base (table `fiches`, D44)."""
    from embed_api import Api  # noqa: PLC0415

    return {x["fiche_id"]: x["paper_id"] for x in Api().appel(
        "GET", "/rest/v1/fiches?select=fiche_id,paper_id&paper_id=not.is.null") or []}


def compte(f: Path) -> bool:
    """Une synthèse ne retient ses papiers que si elle peut devenir un test :
    valide, et, pour un dossier, avec un apport `nouveau` (D52, défaut 6). Une
    synthèse refusée ou sans apport ne sera jamais codée ; elle ne bloque rien."""
    if f.stem.startswith("synthese-dossier-"):
        syn = json.loads(f.read_text(encoding="utf-8")).get("synthesis") or {}
        return syn.get("apport") == "nouveau" and not valider(f)
    from synthese import valider as valider_grappe  # noqa: PLC0415

    return not valider_grappe(f)


def deja_utilises(lien: dict[str, str] | None = None) -> dict[str, str]:
    """Chaque papier déjà graine ou source d'une synthèse qui compte, et laquelle.

    Deux clés par papier : son identifiant dans la synthèse (`fiche_id` ou
    `base-…`), et `paper:<id en base>`. La seconde survit au jour où un voisin
    `base-…` reçoit sa fiche et change d'identifiant (D52, défaut 7)."""
    lien = lien if lien is not None else liens()
    out: dict[str, str] = {}
    for f in sorted(DOSSIER.glob("synthese-*.json")):
        if not compte(f):
            continue
        syn = json.loads(f.read_text(encoding="utf-8")).get("synthesis") or {}
        papier = dict(lien)
        fige = DOSSIERS / f"{f.stem}.json"
        if fige.is_file():
            for v in json.loads(fige.read_text(encoding="utf-8"))["neighbors"]:
                papier[v["fiche_id"] or base_id(v["paper_id"])] = v["paper_id"]
        for ident in [syn.get("dossier"), *(syn.get("sources") or [])]:
            if not ident:
                continue
            out.setdefault(ident, f.stem)
            if papier.get(ident):
                out.setdefault(f"paper:{papier[ident]}", f.stem)
    return out


def utilise_par(utilises: dict[str, str], ident: str, paper_id: str | None) -> str | None:
    return utilises.get(ident) or (utilises.get(f"paper:{paper_id}") if paper_id else None)


def sources_du_dossier(d: dict) -> dict[str, dict]:
    """Chaque source possible de la synthèse : la graine, puis chaque voisin."""
    out = {d["seed"]["fiche_id"]: {"kind": "graine", "title": d["seed"]["title"]}}
    for v in d["neighbors"]:
        ident = v["fiche_id"] or base_id(v["paper_id"])
        out[ident] = {"kind": "voisin fiché" if v["fiche_id"] else "voisin sans fiche",
                      "title": v["title"], "paper_id": v["paper_id"],
                      "similarity": v["similarity"]}
    return out


CONSIGNE = """\
# Consigne de synthèse d'un dossier — La Fabrique, `D47`

Tu écris **une fiche de synthèse** à partir d'un **papier graine** et de {n}
papiers **voisins**, trouvés par le sens dans toute notre base de papiers,
puis retenus par un trieur isolé comme décrivant **le même mécanisme** (`D53`).
Le trieur peut se tromper : le rôle `hors_sujet` reste possible. Tu n'as accès qu'à ce
fichier. **Tu ne connais aucun résultat obtenu sur nos données, et tu ne dois
pas en chercher** : la version que tu retiens se choisit sur ce que disent les
papiers, jamais sur ce qui « marcherait ».

## Ce que tu cherches

L'hypothèse **du papier graine**, rendue **plus complète** par ses voisins :
un voisin peut confirmer le mécanisme, en préciser la construction, donner un
paramètre que la graine ne donne pas, dire sur quel marché ou à quel horizon il
tient, ou le contredire. Tu retiens **une seule version**, d'une **seule
famille de signal** — celle de la graine, ou celle d'un voisin si les
critères ci-dessous l'imposent.

Tu **n'empiles pas** des signaux distincts, et tu **ne conditionnes pas** le
signal à un régime (« seulement les jours de forte volatilité ») : les régimes
et les combinaisons sont des étapes à part, plus tard dans la chaîne.

## La logique, voisin par voisin — obligatoire

Pour **chaque** voisin, sans en sauter un, tu donnes **un rôle et un seul**,
dans cette liste fermée, avec sa raison :

{roles}

Dans cet ordre de questions : décrit-il le **même mécanisme** que la graine
(sinon `hors_sujet` — la similarité d'un texte ne prouve rien) ? A-t-il **déjà
son hypothèse** (marqué « déjà testé » ci-dessous) et la synthèse ne ferait-elle
que la refaire (`deja_teste`) ? Trouve-t-il l'effet **inverse ou absent**
(`contredit`) ? Apporte-t-il **un élément cité que la graine n'a pas**
(`complete`) ? Sinon, il `confirme`.

Puis tu déclares l'**apport** de la synthèse : `nouveau` si au moins un voisin
`complete` la graine, `aucun` sinon. **Une synthèse sans apport n'est pas un
échec** : c'est le constat que la graine se suffit, et elle ne sera pas codée.
Ne force jamais un rôle `complete` pour avoir un apport.
{graine_testee}

## Ce que tu rends

Un **seul fichier JSON**, écrit à `{chemin}`. C'est une fiche au schéma
ci-dessous (section SCHÉMA), avec ces règles propres à une synthèse :

- `fiche_id` : `{sid}` ; `written` : `{today}` ; `written_by` : ton nom.
- `source` : `authors` = « Synthèse de : » suivi des auteurs des papiers
  retenus ; `title` = « Synthèse — » suivi du mécanisme ; `year` = l'année la
  plus récente des sources ; `source_url` = celle du papier dont vient la
  construction retenue ; `retrieved` = `{today}` ; `peer_reviewed` = `false`.
  Pas de `pdf`.
- `claim` : l'affirmation, telle que les papiers retenus la soutiennent.
- `reported_results` : des résultats **recopiés à la lettre** de la fiche
  graine, d'une fiche voisine, ou **d'un passage cité ci-dessous** — chacun
  avec un champ `from_fiche` qui nomme sa source par son **identifiant**
  (`{graine}`, ou l'identifiant d'un voisin entre crochets ci-dessous). Une
  citation qui ne figure pas mot pour mot dans ta source sera refusée.
- `signal_construction` : **la version retenue**, une seule.
- un bloc `synthesis` :

```json
"synthesis": {{
  "dossier": "{graine}",
  "roles": {{"<identifiant de CHAQUE voisin>": {{"role": "<rôle>", "why": "<raison>"}}}},
  "apport": "nouveau | aucun",
  "sources": ["{graine}", "<chaque voisin complete, confirme ou contredit>"],
  "ignored": ["<chaque voisin hors_sujet ou deja_teste> : <pourquoi>"],
  "mechanism": "<le mécanisme commun, en tes mots>",
  "agreements": ["<ce sur quoi les papiers s'accordent>"],
  "disagreements": ["<ce sur quoi ils divergent : fenêtre, marché, signe, horizon…>"],
  "contributions": ["<identifiant> : <ce que ce voisin ajoute à la graine>"],
  "criteria_applied": ["<chaque critère ci-dessous, et ce qu'il a tranché>"],
  "chosen_from": ["<identifiant dont vient la construction retenue>"],
  "why": "<pourquoi cette version, en une ou deux phrases>"
}}
```

`sources` contient la graine et **exactement** les voisins `complete`,
`confirme` ou `contredit`. Chaque voisin `complete` a au moins un résultat cité
dans `reported_results` (son `from_fiche`) : ce qu'il apporte se lit dans son
texte.

## Comment choisir la version — dans cet ordre, et rien d'autre

{criteres}

Si les papiers se contredisent sur le **signe** de l'effet, ne tranche pas par
préférence : écris-le dans `disagreements`, et retiens la version du critère 1.

## Ce que tu ne fais pas

Tu n'inventes aucun paramètre, aucune valeur, aucune citation. Ce qu'aucun
papier ne dit reste `null`, avec sa raison.

---

## SCHÉMA

{schema}

---

## LE PAPIER GRAINE — `{graine}`

```json
{fiche_graine}
```

---

## LES VOISINS

{voisins}
"""



CANDIDATS = 30  # candidats montrés au trieur (D53)
DEBUT = 1500  # caractères du début de chaque candidat (titre, résumé) montrés au trieur

CONSIGNE_TRI = """\
# Consigne de tri des voisins — La Fabrique, `D53`

Tu es un trieur isolé. Ta seule source est ce fichier. Ne lis aucun autre
fichier, aucune commande, aucun accès web.

## Le papier graine

**{titre}**

Son mécanisme, tel que sa fiche le décrit :

{mecanisme}

## Ta tâche

Pour **chaque** candidat ci-dessous, dans l'ordre, réponds :

- `meme` : il étudie **le même mécanisme économique** que la graine (la même
  cause qui produit le même type de mouvement de prix), même sur un autre
  marché, une autre période ou avec une autre méthode — y compris s'il
  conclut que l'effet n'existe pas ou s'inverse ;
- `autre` : il partage le thème, le marché ou la méthode, mais pas le
  mécanisme (« même sujet, autre effet »), ou il n'a pas de rapport.

Juge sur le titre, le début du papier (son résumé) et les passages, rien
d'autre. **Le résumé dit ce que le papier étudie ; un passage peut tromper.**
Une **revue de littérature** n'est `meme` que si elle est consacrée au mécanisme
de la graine, pas si celui-ci n'est qu'un de ses sujets. En cas de doute réel,
`autre`.

## Ce que tu rends

Écris avec l'outil Write, à `{chemin}`, un tableau JSON et rien d'autre :

```json
[{{"id": "c01", "label": "meme", "why": "<une phrase>"}}, ...]
```

Un objet par candidat, aucun omis. Réponds en une ligne : le chemin écrit et le
compte meme / autre.

## Les candidats

{candidats}
"""


def tri_de(graine: str) -> tuple[Path, Path, Path]:
    """Les candidats, la consigne du trieur, ses étiquettes."""
    return (DOSSIERS / f"tri-{graine}.json", WORK / f"tri-{graine}.md",
            DOSSIERS / f"tri-{graine}.labels.json")


def gardes_de_graine(graine: str, ff: dict[str, Path]) -> None:
    if graine not in ff:
        raise SystemExit(f"fiche graine inconnue : {graine}")
    sid = sid_de(graine)
    if (DOSSIER / f"{sid}.json").is_file():
        raise SystemExit(f"{sid} existe déjà : son dossier est figé. Une synthèse se refait "
                         "par une décision écrite, pas en réécrivant ce contre quoi on la juge.")
    lien = liens()
    deja = utilise_par(deja_utilises(lien), graine, lien.get(graine))
    if deja:
        raise SystemExit(f"{graine} est déjà graine ou source de {deja} : une seconde "
                         "synthèse referait la même hypothèse (D52)")


def do_candidats(graine: str, n: int, avec: list[str] | None = None) -> int:
    """Étape 1 (D53) : les candidats de la recherche, et la consigne du trieur."""
    from grappes import texte  # noqa: PLC0415
    from voisins import chercher  # noqa: PLC0415

    ff = fiches()
    gardes_de_graine(graine, ff)
    d = chercher(graine, n, PASSAGES, avec)
    for i, v in enumerate(d["neighbors"], 1):
        v["cid"] = f"c{i:02d}"
    f_tri, f_consigne, f_labels = tri_de(graine)
    DOSSIERS.mkdir(parents=True, exist_ok=True)
    f_tri.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    fiche = json.loads(ff[graine].read_text(encoding="utf-8"))
    mecanisme = "\n\n".join(x for x in (texte(fiche.get("claim")),
                                         texte(fiche.get("signal_construction"))) if x)
    from embed_api import Api  # noqa: PLC0415

    api = Api()
    blocs = []
    for v in d["neighbors"]:
        # Le début du papier (titre, résumé) en plus des deux passages : deux passages
        # seuls ont trompé le trieur (« Cryptoasset factor models », revue du 2026-10-05).
        debut = api.appel("GET", f"/rest/v1/chunks?select=content&paper_id=eq.{v['paper_id']}"
                                 "&order=ordinal&limit=3") or []
        debut = " ".join(" ".join(c["content"].split()) for c in debut)[:DEBUT]
        ps = "\n\n".join(f"> *{p['section']}* — " + " ".join(p["content"].split())[:900]
                         for p in v["passages"][:2])
        blocs.append(f"### {v['cid']} — {v['title']}\n\n**Début du papier :** {debut}\n\n"
                     f"**Passages les plus proches de la graine :**\n\n{ps}\n")
    WORK.mkdir(parents=True, exist_ok=True)
    f_consigne.write_text(CONSIGNE_TRI.format(
        titre=d["seed"]["title"], mecanisme=mecanisme, chemin=f_labels.as_posix(),
        candidats="\n".join(blocs)), encoding="utf-8")
    print(f"candidats       : {f_tri.relative_to(REPO).as_posix()} ({len(d['neighbors'])})")
    print(f"consigne de tri : {f_consigne.relative_to(REPO).as_posix()}")
    print(f"étiquettes      : {f_labels.relative_to(REPO).as_posix()}  (fabrique-voisins)")
    return 0


def voisins_tries(graine: str) -> dict:
    """Étape 2 (D53) : les seuls candidats que le trieur a jugés du même mécanisme."""
    f_tri, _, f_labels = tri_de(graine)
    if not f_tri.is_file() or not f_labels.is_file():
        raise SystemExit(f"tri absent pour {graine} : `--candidats {graine}`, puis le trieur "
                         "`fabrique-voisins`, avant `--prepare`")
    d = json.loads(f_tri.read_text(encoding="utf-8"))
    labels = json.loads(f_labels.read_text(encoding="utf-8"))
    par_id = {x.get("id"): x for x in labels if isinstance(x, dict)}
    cids = [v["cid"] for v in d["neighbors"]]
    fautes = [c for c in cids if c not in par_id
              or par_id[c].get("label") not in ("meme", "autre")
              or not str(par_id[c].get("why") or "").strip()]
    if fautes or set(par_id) != set(cids):
        ecart = fautes or sorted(set(par_id) ^ set(cids))
        raise SystemExit(f"étiquettes incomplètes ou hors liste : {ecart} — renvoyer la "
                         "consigne au trieur")
    gardes = [v for v in d["neighbors"] if par_id[v["cid"]]["label"] == "meme"]
    d["triage"] = {"candidates": len(cids), "kept": len(gardes),
                   "labels": f_labels.relative_to(REPO).as_posix()}
    d["neighbors"] = gardes
    return d


def do_prepare(graine: str) -> int:
    """Étape 3 : le dossier des voisins retenus par le tri, et la consigne de synthèse."""
    from embed_api import Api  # noqa: PLC0415
    from voisins import ecrire  # noqa: PLC0415

    ff = fiches()
    gardes_de_graine(graine, ff)
    sid = sid_de(graine)
    utilises = deja_utilises()
    d = voisins_tries(graine)
    if not d["neighbors"]:
        print(f"{graine} : aucun des {d['triage']['candidates']} candidats ne décrit le même "
              "mécanisme. La base n'a pas de voisin pour cette graine : pas de synthèse (D53).")
        return 1
    # Le dossier d'une synthèse est figé sous le nom de la synthèse : `voisins.py`
    # peut réécrire le dossier d'exploration, jamais celui contre lequel on juge.
    d["seed"]["dossier_of"] = sid_de(graine)
    ecrire(d, nom=sid_de(graine))
    api = Api()
    blocs = []
    for v in d["neighbors"]:
        if v["fiche_id"] and v["fiche_id"] in ff:
            ident = v["fiche_id"]
            texte = ff[ident].read_text(encoding="utf-8")
            corps = f"Ce voisin a sa fiche :\n\n```json\n{texte}\n```\n"
        else:
            ident = base_id(v["paper_id"])
            figer_texte(api, v["paper_id"], ident)
            corps = ""
        marques = []
        if v.get("hypothesis"):
            marques.append(f"**déjà testé** : ce papier a sa propre hypothèse, {v['hypothesis']}")
        deja = utilise_par(utilises, ident, v["paper_id"])
        if deja:
            marques.append(f"**déjà source** de la synthèse `{deja}`")
        marque = "".join(f"> {m}\n" for m in marques) + ("\n" if marques else "")
        passages = "\n\n".join(
            f"> *{p['section']}, page {p['page']}, similarité {p['similarity']:.3f}*\n>\n> "
            + " ".join(p["content"].split()) for p in v["passages"])
        auteurs = ", ".join(v.get("authors") or []) or "auteurs non renseignés en base"
        annee = v.get("year") or "année non renseignée en base"
        blocs.append(f"### [{ident}] {v['title']}\n\n{auteurs} ({annee}). "
                     f"Similarité {v['similarity']:.3f}.\n\n"
                     f"{marque}{corps}Ses passages les plus proches de la graine :\n\n"
                     f"{passages}\n")
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{sid}.md"
    out.write_text(CONSIGNE.format(
        n=len(d["neighbors"]), graine=graine, sid=sid, today=date.today().isoformat(),
        chemin=(DOSSIER / f"{sid}.json").relative_to(REPO).as_posix(),
        criteres="\n".join(f"{i}. {c}" for i, c in enumerate(CRITERES, 1)),
        roles="\n".join(f"- `{k}` : {v}" for k, v in ROLES.items()),
        graine_testee=(f"\n**La graine a déjà son hypothèse, {d['seed']['hypothesis']}.** Une "
                       "synthèse dont la version est celle de la graine, sans voisin `complete`, "
                       "la referait : son apport est alors `aucun`.\n"
                       if d["seed"].get("hypothesis") else ""),
        schema=SCHEMA.read_text(encoding="utf-8"),
        fiche_graine=ff[graine].read_text(encoding="utf-8"), voisins="\n".join(blocs)),
        encoding="utf-8")
    print(f"dossier         : {(DOSSIERS / f'{sid}.json').relative_to(REPO).as_posix()} "
          f"({len(d['neighbors'])} voisins)")
    ko = out.stat().st_size / 1000
    print(f"consigne écrite : {out.relative_to(REPO).as_posix()}  ({ko:.0f} ko)")
    print(f"fiche attendue  : {(DOSSIER / f'{sid}.json').relative_to(REPO).as_posix()}")
    return 0


def textes(ident: str, ff: dict[str, Path]) -> dict[str, str]:
    """Le texte qui fait foi pour une source : ses extractions D18, ou son texte figé."""
    from score_extraction import texts_of  # noqa: PLC0415

    if ident in ff:
        return {f"{ident}.{m}": t for m, t in
                texts_of(json.loads(ff[ident].read_text(encoding="utf-8"))).items()}
    p = TEXT / f"{ident}.default.txt"
    return {ident: p.read_text(encoding="utf-8")} if p.is_file() else {}


def valider(path: Path) -> list[str]:
    from score_extraction import check_f2  # noqa: PLC0415
    from validate_fiches import check_fiche  # noqa: PLC0415

    fiche = json.loads(path.read_text(encoding="utf-8"))
    syn = fiche.get("synthesis")
    if not isinstance(syn, dict):
        return ["bloc `synthesis` absent"]
    graine = syn.get("dossier")
    f_dossier = DOSSIERS / f"{sid_de(graine)}.json"
    if not graine or not f_dossier.is_file():
        return [f"dossier introuvable : {f_dossier.relative_to(REPO).as_posix()}"]
    possibles = sources_du_dossier(json.loads(f_dossier.read_text(encoding="utf-8")))
    fautes = []
    if fiche.get("fiche_id") != sid_de(graine) or path.stem != sid_de(graine):
        fautes.append(f"fiche_id et nom de fichier doivent valoir {sid_de(graine)}")
    sources = syn.get("sources") or []
    hors = [s for s in sources if s not in possibles]
    if hors:
        fautes.append(f"sources hors du dossier : {hors}")
    # D52 : chaque voisin a son rôle, et les sources s'en déduisent.
    roles = syn.get("roles")
    voisins = {k for k, v in possibles.items() if v["kind"] != "graine"}
    if not isinstance(roles, dict):
        fautes.append("synthesis.roles absent : chaque voisin reçoit un rôle (D52)")
        roles = {}
    if set(roles) != voisins:
        fautes.append(f"rôles manquants {sorted(voisins - set(roles))} ou en trop "
                      f"{sorted(set(roles) - voisins)}")
    for k, r in roles.items():
        if (not isinstance(r, dict) or r.get("role") not in ROLES
                or not str(r.get("why") or "").strip()):
            fautes.append(f"rôle de {k} : un de {sorted(ROLES)}, avec sa raison")
    def de_role(*noms: str) -> set[str]:
        return {k for k, r in roles.items() if isinstance(r, dict) and r.get("role") in noms}
    if roles and set(sources) != {graine} | de_role(*GARDES):
        fautes.append("`sources` = la graine + les voisins complete, confirme ou contredit")
    completes = de_role("complete")
    apport = syn.get("apport")
    if apport not in ("nouveau", "aucun"):
        fautes.append("synthesis.apport : `nouveau` ou `aucun`")
    elif (apport == "nouveau") != bool(completes):
        fautes.append("apport `nouveau` si et seulement si un voisin `complete` la graine")
    cites = {r.get("from_fiche") for r in fiche.get("reported_results") or []
             if isinstance(r, dict)}
    for k in sorted(completes - cites):
        fautes.append(f"{k} est `complete` sans aucun résultat cité de son texte")
    choisies = syn.get("chosen_from") or []
    if not choisies or any(c not in sources for c in choisies):
        fautes.append("`chosen_from` doit nommer au moins une source de la synthèse")
    for cle in ("mechanism", "why"):
        if not str(syn.get(cle) or "").strip():
            fautes.append(f"synthesis.{cle} vide")
    for cle in ("agreements", "disagreements", "criteria_applied"):
        if not isinstance(syn.get(cle), list) or not syn.get(cle):
            fautes.append(f"synthesis.{cle} doit être une liste non vide")
    for i, r in enumerate(fiche.get("reported_results") or []):
        if isinstance(r, dict) and r.get("from_fiche") not in sources:
            fautes.append(f"reported_results[{i}] : `from_fiche` doit nommer une source")
    fautes += check_fiche(path.stem, fiche)
    if not fautes:
        ff = fiches()
        tous = {}
        for s in sources:
            t = textes(s, ff)
            if not t:
                fautes.append(f"texte de {s} introuvable — relancer `--prepare`")
            tous.update(t)
        if not fautes:
            fautes += check_f2(fiche, tous)
    reg = json.loads(PRODUCED.read_text(encoding="utf-8")) if PRODUCED.is_file() else {}
    ligne = reg.get(path.stem)
    if ligne is None:
        fautes.append("fiche non inscrite : `--record` avant `--check`")
    elif ligne["sha256_16"] != empreinte16(path):
        fautes.append("fiche modifiée depuis sa production — une synthèse se refait, "
                      "elle ne se retouche pas")
    return fautes


def do_check(path: Path) -> int:
    fautes = valider(path)
    if fautes:
        print(f"SYNTHÈSE REFUSÉE — {path.stem} :")
        for f in fautes:
            print(f"  - {f}")
        return 1
    print(f"SYNTHÈSE VALIDE — {path.stem} : chaque citation est dans le texte d'une source, "
          "chaque source dans le dossier, la version retenue dit d'où elle vient")
    return 0


def do_status() -> int:
    for f in sorted(DOSSIERS.glob("synthese-dossier-*.json")):
        p = DOSSIER / f"{f.stem}.json"
        etat = ("valide" if not valider(p) else "REFUSÉE") if p.is_file() else "à synthétiser"
        print(f"  {etat:<14} {f.stem}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="La synthèse d'un dossier de voisins — D47")
    ap.add_argument("--candidats", metavar="FICHE_GRAINE")
    ap.add_argument("--n", type=int, default=CANDIDATS)
    ap.add_argument("--avec", nargs="*", default=[], metavar="PAPER_ID",
                    help="papiers en base joints aux candidats (une famille, corpus/familles.py)")
    ap.add_argument("--prepare", metavar="FICHE_GRAINE")
    ap.add_argument("--record", type=Path)
    ap.add_argument("--check", type=Path)
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)
    if a.candidats:
        return do_candidats(a.candidats, a.n, a.avec)
    if a.prepare:
        return do_prepare(a.prepare)
    if a.record:
        return do_record(a.record)
    if a.check:
        return do_check(a.check)
    return do_status()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
