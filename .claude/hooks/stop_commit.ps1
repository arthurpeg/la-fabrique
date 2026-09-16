# Stop, 2/2 — commit horodate et poussee, au mieux.
#
# Raison d'etre : registry/tests.jsonl et LECONS.md sont append-only et
# irremplacables ; le depot distant est la sauvegarde. Perdre le code coute du
# temps, perdre le registre coute la validite statistique de tout ce qui
# precede (CLAUDE.md, Conventions, Git).
#
# ATTENTION : ce crochet commite `git add -A`, donc TOUT l'arbre, travail en
# cours compris. C'est assume — point ouvert de DECISION-02. Pour le
# restreindre, remplacer le `add -A` ci-dessous par une liste de chemins.
#
# Il ne touche jamais a l'historique : pas d'amend, pas de rebase, pas de
# force-push.

$ErrorActionPreference = 'SilentlyContinue'
$ProgressPreference = 'SilentlyContinue'

try {
    $root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

    if (-not (Test-Path (Join-Path $root '.git'))) { exit 0 }
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { exit 0 }

    $dirty = & git -C $root status --porcelain 2>$null
    if (-not $dirty) {
        Write-Output 'stop : rien a commiter.'
        exit 0
    }

    & git -C $root add -A 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) { exit 0 }

    # Rien n'est reellement stage (tout etait ignore) : on s'arrete la.
    & git -C $root diff --cached --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Output 'stop : rien de stage, commit ignore.'
        exit 0
    }

    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $count = (& git -C $root diff --cached --name-only 2>$null | Measure-Object -Line).Lines
    $message = @"
session $stamp ($count fichier(s))

Commit automatique du crochet Stop (.claude/hooks/stop_commit.ps1).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
"@

    & git -C $root commit -m $message 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Output 'stop : commit refuse (hook git ?), ignore.'
        exit 0
    }
    Write-Output "stop : commit ($count fichier(s))."

    $remotes = & git -C $root remote 2>$null
    if (-not $remotes) { exit 0 }

    & git -C $root push --quiet 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        # Premiere poussee de la branche : pas encore d'upstream.
        & git -C $root push --quiet --set-upstream origin HEAD 2>$null | Out-Null
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Output 'stop : pousse.'
    } else {
        Write-Output 'stop : poussee impossible, commit conserve en local.'
    }
}
catch {
    # Un crochet ne casse jamais une session.
}

exit 0
