#!/usr/bin/env pwsh
# Clone 10 GitHub hot repos from May 21, 2026 report
$ErrorActionPreference = "Continue"

$tools = @(
    @{ name = "openhuman";               repo = "https://github.com/tinyhumansai/openhuman.git" },
    @{ name = "codegraph";               repo = "https://github.com/colbymchenry/codegraph.git" },
    @{ name = "academic-research-skills"; repo = "https://github.com/Imbad0202/academic-research-skills.git" },
    @{ name = "supertonic";              repo = "https://github.com/supertone-inc/supertonic.git" },
    @{ name = "agentmemory";             repo = "https://github.com/rohitg00/agentmemory.git" },
    @{ name = "CloakBrowser";            repo = "https://github.com/CloakHQ/CloakBrowser.git" },
    @{ name = "RuView";                  repo = "https://github.com/ruvnet/RuView.git" },
    @{ name = "bun";                     repo = "https://github.com/oven-sh/bun.git" },
    @{ name = "12-factor-agents";        repo = "https://github.com/humanlayer/12-factor-agents.git" },
    @{ name = "easy-vibe";               repo = "https://github.com/datawhalechina/easy-vibe.git" }
)

$toolsDir = Join-Path $PSScriptRoot "tools"
if (!(Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
}

foreach ($t in $tools) {
    $dest = Join-Path $toolsDir $t.name
    if (Test-Path $dest) {
        Write-Host "[SKIP] $($t.name) already exists" -ForegroundColor Yellow
    } else {
        Write-Host "[CLONE] $($t.name) ..." -ForegroundColor Cyan
        git clone --depth 1 $t.repo $dest
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] $($t.name) cloned" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] $($t.name)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Done cloning GitHub Hot Repositories!" -ForegroundColor Green
