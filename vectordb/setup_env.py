"""Écrit `DATABASE_URL` dans `.env`, sans que le mot de passe transite ailleurs.

Existe parce que l'écrire à la main a échoué quatre fois, et jamais pour la
même raison : le `>>` de PowerShell encode en UTF-16, un collage tronque la
chaîne, l'adresse du tableau de bord se confond avec la chaîne de connexion,
et remplacer un mot dans un éditeur duplique la clé. Aucune de ces fautes
n'est évitable par un rappel : elles se préviennent par un outil.

Le mot de passe est saisi au clavier (`getpass`, donc non affiché), assemblé
ici, et écrit directement dans `.env`. Il ne passe ni par une transcription,
ni par un presse-papiers, ni par un historique de terminal.

    python vectordb/setup_env.py
"""

from __future__ import annotations

import getpass
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

REPO = Path(__file__).resolve().parents[1]
ENV = REPO / ".env"

PROJECT_REF = "ztyohbvjsrujtjdpekvo"
PORT = 5432
DATABASE = "postgres"
USER = f"postgres.{PROJECT_REF}"

# LA REGION N'EST PAS CONNUE, et l'avoir crue connue a coute cinq tentatives.
# Elle avait ete « lue » dans un collage de l'utilisateur — qui etait en fait
# mon propre exemple recopie. Un gabarit relu comme une mesure : c'est `L20`
# sous une autre forme, le nom du bon papier apparaissant dans le mauvais.
#
# Donc on ne devine plus : on essaie les regions une par une et on garde celle
# qui repond. Le pooler refuse un projet qu'il n'heberge pas (« Tenant or user
# not found »), ce qui distingue nettement une mauvaise REGION d'un mauvais
# MOT DE PASSE (« password authentication failed »).
# Le PREFIXE compte autant que la region : Supabase a deux generations de
# pooler, `aws-0-` et `aws-1-`. Ce projet vit sur `aws-1-eu-west-1`, trouve le
# 2026-09-22 en sondant les deux familles AVEC UN MOT DE PASSE VOLONTAIREMENT
# FAUX — « projet inconnu » (ENOTFOUND) et « mot de passe refuse » etant deux
# erreurs distinctes, l'hote se trouve sans jamais employer le vrai secret.
REGIONS = [
    "eu-west-1", "eu-west-3", "eu-central-1", "eu-west-2", "eu-central-2",
    "eu-north-1", "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "ca-central-1", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
    "ap-northeast-2", "ap-south-1", "sa-east-1",
]
PREFIXES = ["aws-1", "aws-0"]

# L'hote connu de CE projet, essaye en premier. Le balayage reste derriere :
# si Supabase deplace le projet, le script le retrouvera au lieu d'echouer.
HOSTS = ["aws-1-eu-west-1.pooler.supabase.com"] + [
    f"{p}-{r}.pooler.supabase.com" for r in REGIONS for p in PREFIXES
]

PLACEHOLDERS = ("motdepasse", "your-password", "your_password", "colle", "xxx",
                "password", "mot-de-passe")


def read_other_lines() -> list[str]:
    """Les lignes de `.env` qui ne sont PAS `DATABASE_URL`, telles quelles.

    Lues en UTF-8 tolérant : le fichier a déjà été corrompu en UTF-16 deux
    fois, et refuser de le lire pour autant ne rendrait service à personne.
    """
    if not ENV.is_file():
        return []
    text = ENV.read_bytes().decode("utf-8", errors="replace")
    return [line for line in text.splitlines()
            if not line.strip().startswith("DATABASE_URL")]


def masque(secret: str) -> str:
    """De quoi RECONNAÎTRE un mot de passe sans le révéler.

    Deux caractères à chaque bout suffisent à voir qu'on s'est trompé de
    chaîne, ou qu'un collage a été tronqué — ce qui est arrivé cinq fois.
    """
    if len(secret) <= 4:
        return "*" * len(secret)
    return f"{secret[:2]}{'*' * (len(secret) - 4)}{secret[-2:]}"


def main(visible: bool = False, region_forcee: str | None = None) -> int:
    print(f"Projet   : {PROJECT_REF}")
    print(f"Fichier  : {ENV}\n")
    if not visible:
        print("La saisie ne s'affichera pas. Pour la voir : --visible")
    print("C'est le mot de passe de la BASE, pas celui de ton compte Google.\n")

    print("Colle SOIT le mot de passe seul, SOIT la chaîne `postgresql://…`")
    print("entière telle que Supabase l'affiche — les deux marchent.\n")

    if visible:
        print("MODE VISIBLE : ce que tu tapes s'affiche, et reste dans l'historique")
        print("du terminal. À utiliser pour vérifier un collage, puis réinitialiser")
        print("le mot de passe si tu préfères.\n")
        saisie = input("Mot de passe ou chaîne de connexion : ").strip()
    else:
        saisie = getpass.getpass("Mot de passe ou chaîne de connexion : ").strip()
        print(f"  ({len(saisie)} caractères reçus)")

    if not saisie:
        print("\nRien saisi. Rien n'a été écrit.")
        return 1

    if saisie.startswith(("http://", "https://")):
        print("\nC'est l'adresse d'une page web, pas une chaîne de connexion.")
        print("Celle qu'il faut commence par `postgresql://`. Rien n'a été écrit.")
        return 1

    if saisie.startswith("postgresql://"):
        # La chaîne entière a été collée. On n'en garde QUE le mot de passe et
        # on reconstruit l'hôte : Supabase propose aussi la connexion DIRECTE
        # (`db.<ref>.supabase.co`), qui n'est joignable qu'en IPv6 — donc pas
        # depuis un poste qui n'en a pas. Le pooler, lui, répond en IPv4.
        m = re.match(r"postgresql://([^:]+):([^@]+)@([^:/]+):(\d+)/", saisie)
        if not m:
            print("\nChaîne incomplète ou tronquée — un collage coupé, sans doute.")
            print("Rien n'a été écrit.")
            return 1
        _, brut, hote_donne, _ = m.groups()
        password = unquote(brut)
        if (m2 := re.match(r"aws-0-(.+)\.pooler\.supabase\.com$", hote_donne)):
            # La chaîne collée vient du bon onglet : elle PORTE la région.
            region_forcee = region_forcee or m2.group(1)
            print(f"\n  région lue dans la chaîne : {region_forcee}")
        else:
            print(f"\n  hôte ignoré : {hote_donne}")
            print("              (connexion directe, joignable en IPv6 seulement —")
            print("               on passera par le pooler, cherché ci-dessous)")
    else:
        password = saisie

    low = password.lower()
    if any(p in low for p in PLACEHOLDERS):
        print(f"\nCe texte ressemble à un gabarit ({password[:4]}…), pas à un mot "
              "de passe. Rien n'a été écrit.")
        return 1

    # Un mot de passe peut contenir @ : / ? # — qui sont la syntaxe même de
    # l'URI. Sans encodage, un seul de ces caractères coupe la chaîne en deux.
    print("\n--- ce que je vais chercher ---")
    print(f"  utilisateur  : {USER}")
    print(f"  mot de passe : {masque(password)}  ({len(password)} caractères)")
    print(f"  base         : {DATABASE}")
    print(f"  hôtes        : {len(HOSTS)} candidats, à commencer par le connu")

    try:
        import psycopg
    except ImportError:
        print("\npsycopg absent : pip install -r vectordb/requirements.txt")
        return 1

    if region_forcee:
        candidates = ([h for h in HOSTS if region_forcee in h]
                      or [f"aws-1-{region_forcee}.pooler.supabase.com"])
    else:
        # Dédoublonne en gardant l'ordre : l'hôte connu reste en tête.
        candidates = list(dict.fromkeys(HOSTS))

    print(f"\nRecherche de l'hôte ({len(candidates)} candidats)…", flush=True)
    dsn = None
    mauvais_mdp = False
    for host in candidates:
        essai = (f"postgresql://{USER}:{quote(password, safe='')}"
                 f"@{host}:{PORT}/{DATABASE}")
        try:
            with psycopg.connect(essai, connect_timeout=12) as conn, conn.cursor() as cur:
                cur.execute("select current_database(), current_user, version()")
                db, user, version = cur.fetchone()
            print(f"  {host:<44} TROUVÉ")
            print(f"\n  connecté : {db} / {user}")
            print(f"  {version.split(',')[0]}")
            dsn = essai
            break
        except Exception as e:
            # Le message peut contenir le DSN, donc le mot de passe.
            brut = re.sub(r"://[^@]*@", "://<masque>@", str(e)).strip()
            court = brut.splitlines()[0][:70] if brut else type(e).__name__
            if "password authentication failed" in brut.lower():
                # Le pooler a RECONNU le projet et refusé le mot de passe :
                # l'hôte est le bon, et continuer serait absurde.
                print(f"  {host:<44} hôte correct, MOT DE PASSE REFUSÉ")
                mauvais_mdp = True
                break
            motif = ("projet inconnu ici"
                     if ("ENOTFOUND" in brut or "Tenant or user not found" in brut)
                     else court)
            print(f"  {host:<44} non — {motif}")

    if dsn is None:
        print("\nRien n'a été écrit.")
        if mauvais_mdp:
            print("La région est bonne, c'est le mot de passe qui ne passe pas.")
            print("Settings > Database > « Reset database password », puis relance.")
        else:
            print("Aucun hôte n'a reconnu ce projet. Vérifie sur le tableau de")
            print("bord (Settings > Database > Connection string > Session pooler)")
            print("et relance avec :  --region <ce-qu-affiche-la-page>")
        return 1

    lines = read_other_lines()
    while lines and not lines[-1].strip():
        lines.pop()
    lines += ["", "# Ecrit par vectordb/setup_env.py — ne pas editer a la main.",
              f"DATABASE_URL={dsn}"]
    ENV.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))

    print(f"\nÉcrit dans {ENV.name}, en UTF-8. La connexion répond.")
    print("Tu peux revenir me dire « c'est fait ».")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    forcee = None
    if "--region" in argv:
        forcee = argv[argv.index("--region") + 1]
    sys.exit(main(visible="--visible" in argv, region_forcee=forcee))
