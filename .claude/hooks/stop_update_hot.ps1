# Stop, 1/2 — regenere wiki/hot.md.
#
# Doit tourner AVANT stop_commit.ps1, pour que hot.md regenere parte dans le
# meme commit. C'est stop.ps1 qui garantit cet ordre.

$ErrorActionPreference = 'SilentlyContinue'
$ProgressPreference = 'SilentlyContinue'

try {
    $root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    $script = Join-Path $root 'wiki\update_hot.py'

    if (-not (Test-Path $script)) { exit 0 }

    $python = $null
    foreach ($candidate in @('python', 'py', 'python3')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            $python = $candidate
            break
        }
    }
    if (-not $python) {
        Write-Output 'stop : python introuvable, hot.md laisse en l''etat.'
        exit 0
    }

    & $python $script 2>&1 | ForEach-Object { Write-Output $_ }
}
catch {
    # Un crochet ne casse jamais une session.
}

exit 0
