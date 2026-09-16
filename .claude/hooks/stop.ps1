# Stop — lance les deux crochets d'arret DANS L'ORDRE.
#
# L'ordre compte : hot.md doit etre regenere avant le commit, sinon il part
# avec un tour de retard. Deux entrees de crochet dans settings.json ne
# garantissent pas cet ordre ; ce lanceur, si.

$ErrorActionPreference = 'SilentlyContinue'
$ProgressPreference = 'SilentlyContinue'

foreach ($step in @('stop_update_hot.ps1', 'stop_commit.ps1')) {
    try {
        $path = Join-Path $PSScriptRoot $step
        if (Test-Path $path) { & $path }
    }
    catch {
        # Une etape qui echoue n'empeche pas la suivante, et rien ne casse
        # la session.
    }
}

exit 0
