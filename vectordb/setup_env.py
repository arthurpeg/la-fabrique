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
REGION = "eu-west-3"
HOST = f"aws-0-{REGION}.pooler.supabase.com"
PORT = 5432
DATABASE = "postgres"
USER = f"postgres.{PROJECT_REF}"

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


def main() -> int:
    print(f"Projet   : {PROJECT_REF}")
    print(f"Région   : {REGION}")
    print(f"Hôte     : {HOST}:{PORT}  (session pooler)")
    print(f"Fichier  : {ENV}\n")
    print("Le mot de passe ne s'affichera pas pendant la saisie.")
    print("C'est celui de la BASE, pas celui de ton compte Google.\n")

    print("Colle SOIT le mot de passe seul, SOIT la chaîne `postgresql://…`")
    print("entière telle que Supabase l'affiche — les deux marchent.\n")
    saisie = getpass.getpass("Mot de passe ou chaîne de connexion : ").strip()

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
        if hote_donne != HOST:
            print(f"\n  hôte remplacé : {hote_donne}")
            print(f"                -> {HOST}  (session pooler, IPv4)")
    else:
        password = saisie

    low = password.lower()
    if any(p in low for p in PLACEHOLDERS):
        print(f"\nCe texte ressemble à un gabarit ({password[:4]}…), pas à un mot "
              "de passe. Rien n'a été écrit.")
        return 1

    # Un mot de passe peut contenir @ : / ? # — qui sont la syntaxe même de
    # l'URI. Sans encodage, un seul de ces caractères coupe la chaîne en deux.
    dsn = (f"postgresql://{USER}:{quote(password, safe='')}"
           f"@{HOST}:{PORT}/{DATABASE}")

    print("\nTest de la connexion…", flush=True)
    try:
        import psycopg
    except ImportError:
        print("  psycopg absent : pip install -r vectordb/requirements.txt")
        return 1
    try:
        with psycopg.connect(dsn, connect_timeout=20) as conn, conn.cursor() as cur:
            cur.execute("select current_database(), current_user, version()")
            db, user, version = cur.fetchone()
            print(f"  connecté : {db} / {user}")
            print(f"  {version.split(',')[0]}")
    except Exception as e:
        # Le message de psycopg peut contenir le DSN, donc le mot de passe.
        message = re.sub(r"://[^@]*@", "://<masque>@", str(e))
        print(f"  ÉCHEC : {type(e).__name__}: {message.strip()[:200]}")
        print("\nRien n'a été écrit. Si le mot de passe est en cause, la page")
        print("Settings > Database a un bouton « Reset database password ».")
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
    sys.exit(main())
