#!/usr/bin/env pwsh
$ErrorActionPreference = "Continue"

$tools = @(
    @{ name = "moneyprinterturbo"; repo = "https://github.com/harry0703/MoneyPrinterTurbo.git" },
    @{ name = "headroom"; repo = "https://github.com/chopratejas/headroom.git" },
    @{ name = "markitdown"; repo = "https://github.com/microsoft/markitdown.git" },
    @{ name = "odysseus"; repo = "https://github.com/pewdiepie-archdaemon/odysseus.git" },
    @{ name = "gbrain"; repo = "https://github.com/garrytan/gbrain.git" },
    @{ name = "webwright"; repo = "https://github.com/microsoft/webwright.git" },
    @{ name = "liteparse"; repo = "https://github.com/run-llama/liteparse.git" },
    @{ name = "compound-engineering-plugin"; repo = "https://github.com/EveryInc/compound-engineering-plugin.git" },
    @{ name = "stop-slop"; repo = "https://github.com/hardikpandya/stop-slop.git" },
    @{ name = "supermemory"; repo = "https://github.com/supermemoryai/supermemory.git" },
    @{ name = "ecc"; repo = "https://github.com/affaan-m/ECC.git" },
    @{ name = "taste-skill"; repo = "https://github.com/Leonxlnx/taste-skill.git" },
    @{ name = "understand-anything"; repo = "https://github.com/Lum1104/Understand-Anything.git" },
    @{ name = "voxcpm"; repo = "https://github.com/OpenBMB/VoxCPM.git" },
    @{ name = "AutoHedge"; repo = "https://github.com/The-Swarm-Corporation/AutoHedge.git" },
    @{ name = "Vibe-Trading"; repo = "https://github.com/HKUDS/Vibe-Trading.git" },
    @{ name = "FinceptTerminal"; repo = "https://github.com/Fincept-Corporation/FinceptTerminal.git" },
    @{ name = "LibreChat"; repo = "https://github.com/danny-avila/LibreChat.git" },
    @{ name = "Open-Generative-AI"; repo = "https://github.com/Anil-matcha/Open-Generative-AI.git" },
    @{ name = "Open-LLM-VTuber"; repo = "https://github.com/Open-LLM-VTuber/Open-LLM-VTuber.git" },
    @{ name = "claude-ads"; repo = "https://github.com/AgriciDaniel/claude-ads.git" },
    @{ name = "agentic-inbox"; repo = "https://github.com/cloudflare/agentic-inbox.git" },
    @{ name = "camofox-browser"; repo = "https://github.com/jo-inc/camofox-browser.git" },
    @{ name = "hyperframes"; repo = "https://github.com/heygen-com/hyperframes.git" },
    @{ name = "last30days-skill"; repo = "https://github.com/mvanhorn/last30days-skill.git" },
    @{ name = "open-notebook"; repo = "https://github.com/lfnovo/open-notebook.git" },
    @{ name = "ian-xiaohei-illustrations"; repo = "https://github.com/helloianneo/ian-xiaohei-illustrations.git" },
    @{ name = "tolaria"; repo = "https://github.com/refactoringhq/tolaria.git" },
    @{ name = "rilable"; repo = "https://github.com/rbrown101010/rilable.git" },
    @{ name = "pm-skills"; repo = "https://github.com/phuryn/pm-skills.git" },
    @{ name = "openai-plugins"; repo = "https://github.com/openai/plugins.git" },
    @{ name = "Agent-Reach"; repo = "https://github.com/Panniantong/Agent-Reach.git" },
    @{ name = "cosmos"; repo = "https://github.com/NVIDIA/cosmos.git" },
    @{ name = "container"; repo = "https://github.com/apple/container.git" }
)

$toolsDir = Join-Path $PSScriptRoot "tools"

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

Write-Host "Done cloning new repositories!" -ForegroundColor Green
