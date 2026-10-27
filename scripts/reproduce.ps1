param([string]$Python = "$PSScriptRoot/../.venv/Scripts/python.exe")
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path "$PSScriptRoot/..").Path
$projectPython = (Resolve-Path $Python).Path
Push-Location $projectRoot
try {
    $env:QUARTO_PYTHON = $projectPython
    & $projectPython scripts/check.py
    if ($LASTEXITCODE) { throw 'Python checks failed' }
    & $projectPython scripts/export_reference.py
    if ($LASTEXITCODE) { throw 'Reference export failed' }
    node scripts/check_browser_math.cjs
    if ($LASTEXITCODE) { throw 'Browser mathematics failed' }
    & $projectPython scripts/run_study.py
    if ($LASTEXITCODE) { throw 'Study failed' }
    & $projectPython scripts/make_figures.py
    if ($LASTEXITCODE) { throw 'Figure generation failed' }
    quarto render index.qmd
    if ($LASTEXITCODE) { throw 'Quarto render failed' }
} finally {
    Pop-Location
}
