#!/usr/bin/env pwsh
# Clone 5 new SupAgentic tools
$ErrorActionPreference = "Continue"

$tools = @(
    @{ name = "gstack";       repo = "https://github.com/garrytan/gstack.git" },
    @{ name = "hermes-agent"; repo = "https://github.com/NousResearch/hermes-agent.git" },
    @{ name = "superpowers";  repo = "https://github.com/obra/superpowers.git" },
    @{ name = "paperclip";    repo = "https://github.com/paperclipai/paperclip.git" },
    @{ name = "agent-skills"; repo = "https://github.com/anthropics/skills.git" },
    @{ name = "opencode";     repo = "https://github.com/opencode-ai/opencode.git" },
    @{ name = "aletheia";     repo = "https://github.com/google-deepmind/superhuman.git" },
    @{ name = "claude-mem";   repo = "https://github.com/thedotmack/claude-mem.git" },
    @{ name = "awesome-claude-code"; repo = "https://github.com/hesreallyhim/awesome-claude-code.git" },
    @{ name = "ui-ux-pro-max-skill"; repo = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git" },
    @{ name = "turboquant";  repo = "https://github.com/0xSero/turboquant.git" }
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

Write-Host ""
Write-Host "Done! Run 'python supagentic.py list' to verify." -ForegroundColor Green
