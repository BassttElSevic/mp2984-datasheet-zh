param([string]$CacheDir = '')
$ErrorActionPreference = 'Stop'
Push-Location -LiteralPath $PSScriptRoot
try {
    if ($CacheDir) { $env:TECTONIC_CACHE_DIR = $CacheDir }
    elseif (Test-Path -LiteralPath '..\tmp\tex-cache') {
        $env:TECTONIC_CACHE_DIR = (Resolve-Path '..\tmp\tex-cache').Path
    }
    New-Item -ItemType Directory -Force -Path 'output\pdf' | Out-Null
    tectonic --keep-logs --keep-intermediates --outdir 'output\pdf' main.tex
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX compilation failed.' }
    tectonic --keep-logs --keep-intermediates --outdir 'output\pdf' main.tex
    if ($LASTEXITCODE -ne 0) { throw 'Final LaTeX compilation failed.' }
    Copy-Item -LiteralPath 'output\pdf\main.pdf' -Destination 'output\pdf\mp2984-zh.pdf' -Force
} finally { Pop-Location }
