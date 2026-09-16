# SessionStart — synchronise le depot, au mieux, sans jamais bloquer.
#
# Le wiki vit dans le depot : si la machine precedente a pousse, on veut
# demarrer a jour. Si quoi que ce soit resiste — pas de reseau, pas d'upstream,
# arbre sale, avance divergente — on ne fait rien et on sort en 0.
#
# Jamais de merge, jamais de rebase, jamais de stash : --ff-only uniquement.

$ErrorActionPreference = 'SilentlyContinue'
$ProgressPreference = 'SilentlyContinue'

try {
    $root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

    if (-not (Test-Path (Join-Path $root '.git'))) { exit 0 }
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { exit 0 }

    # Pas de remote : rien a tirer.
    $remotes = & git -C $root remote 2>$null
    if (-not $remotes) { exit 0 }

    # Pas d'upstream sur la branche courante : un pull ferait un bruit inutile.
    & git -C $root rev-parse --abbrev-ref '--symbolic-full-name' '@{u}' 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Output 'session_start : pas d''upstream, pull ignore.'
        exit 0
    }

    # Arbre sale : un ff-only echouerait de toute facon, autant ne pas y toucher.
    $dirty = & git -C $root status --porcelain 2>$null
    if ($dirty) {
        Write-Output 'session_start : arbre sale, pull ignore.'
        exit 0
    }

    & git -C $root pull --ff-only --quiet 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Output 'session_start : depot a jour.'
    } else {
        Write-Output 'session_start : pull impossible, ignore.'
    }
}
catch {
    # Un crochet ne casse jamais une session.
}

exit 0
