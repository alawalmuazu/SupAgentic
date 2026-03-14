# ═══════════════════════════════════════════════════════════════
# SupAgentic — Unified Setup Script
# Detects which tools you want and installs their dependencies
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "Continue"
$ToolsDir = Join-Path $PSScriptRoot "tools"

# All available tools with their install commands
$Tools = @(
    @{ Name = "The Agency";       Dir = "agency-agents";       Type = "prompts";  Deps = $null }
    @{ Name = "CrewAI";           Dir = "crewai";              Type = "python";   Deps = "pip install crewai" }
    @{ Name = "AutoGen";          Dir = "autogen";             Type = "python";   Deps = "pip install autogen-agentchat" }
    @{ Name = "LangGraph";        Dir = "langgraph";           Type = "python";   Deps = "pip install langgraph" }
    @{ Name = "Dify";             Dir = "dify";                Type = "docker";   Deps = "docker compose up -d" }
    @{ Name = "Promptfoo";        Dir = "promptfoo";           Type = "node";     Deps = "npm install -g promptfoo" }
    @{ Name = "Impeccable";       Dir = "impeccable";          Type = "prompts";  Deps = $null }
    @{ Name = "Aider";            Dir = "aider";               Type = "python";   Deps = "pip install aider-chat" }
    @{ Name = "Open Interpreter"; Dir = "open-interpreter";    Type = "python";   Deps = "pip install open-interpreter" }
    @{ Name = "LlamaIndex";       Dir = "llama-index";         Type = "python";   Deps = "pip install llama-index" }
    @{ Name = "RAGFlow";          Dir = "ragflow";             Type = "docker";   Deps = "docker compose up -d" }
    @{ Name = "OpenViking";       Dir = "openviking";          Type = "python";   Deps = "pip install -r requirements.txt" }
    @{ Name = "MiroFish";         Dir = "mirofish";            Type = "python";   Deps = "pip install -r requirements.txt" }
    @{ Name = "Ollama";           Dir = "ollama";              Type = "binary";   Deps = "winget install Ollama.Ollama" }
    @{ Name = "Unsloth";          Dir = "unsloth";             Type = "python";   Deps = "pip install unsloth" }
    @{ Name = "NanoChat";         Dir = "nanochat";            Type = "python";   Deps = "pip install -r requirements.txt" }
    @{ Name = "Heretic";          Dir = "heretic";             Type = "python";   Deps = "pip install -r requirements.txt" }
    @{ Name = "ComfyUI";          Dir = "comfyui";             Type = "python";   Deps = "pip install -r requirements.txt" }
    @{ Name = "Kokoro TTS";       Dir = "kokoro-tts";          Type = "python";   Deps = "pip install kokoro" }
    @{ Name = "AI Engineering Hub"; Dir = "ai-engineering-hub"; Type = "tutorials"; Deps = $null }
)

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║     SupAgentic — Setup Installer      ║" -ForegroundColor Cyan
Write-Host "  ╚═══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "[CHECK] Prerequisites:" -ForegroundColor Yellow
$prereqs = @{
    "Python"  = { python --version 2>&1 }
    "pip"     = { pip --version 2>&1 }
    "Node.js" = { node --version 2>&1 }
    "npm"     = { npm --version 2>&1 }
    "Git"     = { git --version 2>&1 }
    "Docker"  = { docker --version 2>&1 }
}

foreach ($tool in $prereqs.Keys) {
    try {
        $ver = & $prereqs[$tool] 2>&1
        if ($LASTEXITCODE -eq 0 -or $ver -match '\d+\.\d+') {
            Write-Host "  ✅ $tool — $($ver.ToString().Trim())" -ForegroundColor Green
        } else { throw }
    } catch {
        Write-Host "  ⚠️  $tool — not found (some tools may not install)" -ForegroundColor DarkYellow
    }
}

Write-Host ""
Write-Host "Available tools:" -ForegroundColor Yellow
for ($i = 0; $i -lt $Tools.Count; $i++) {
    $t = $Tools[$i]
    $status = if (Test-Path (Join-Path $ToolsDir $t.Dir)) { "✅" } else { "❌" }
    $depInfo = if ($t.Deps) { "[$($t.Type)]" } else { "[no deps]" }
    Write-Host ("  {0,2}. {1} {2,-22} {3}" -f ($i+1), $status, $t.Name, $depInfo)
}

Write-Host ""
Write-Host "Options:" -ForegroundColor Yellow
Write-Host "  [A] Install ALL tools with dependencies"
Write-Host "  [S] Select specific tools (comma-separated numbers)"
Write-Host "  [Q] Quit"
Write-Host ""
$choice = Read-Host "Your choice"

if ($choice -eq 'Q' -or $choice -eq 'q') { exit }

$selected = @()
if ($choice -eq 'A' -or $choice -eq 'a') {
    $selected = 0..($Tools.Count - 1)
} elseif ($choice -eq 'S' -or $choice -eq 's') {
    $nums = Read-Host "Enter tool numbers (e.g., 1,2,5,14)"
    $selected = $nums -split ',' | ForEach-Object { [int]$_.Trim() - 1 } | Where-Object { $_ -ge 0 -and $_ -lt $Tools.Count }
}

Write-Host ""
foreach ($idx in $selected) {
    $t = $Tools[$idx]
    $toolPath = Join-Path $ToolsDir $t.Dir

    if (-not (Test-Path $toolPath)) {
        Write-Host "  ⚠️  $($t.Name) — directory not found, skipping" -ForegroundColor DarkYellow
        continue
    }

    if (-not $t.Deps) {
        Write-Host "  ✅ $($t.Name) — no dependencies needed" -ForegroundColor Green
        continue
    }

    Write-Host "  🔧 Installing $($t.Name)..." -ForegroundColor Cyan
    try {
        Push-Location $toolPath
        Invoke-Expression $t.Deps
        Pop-Location
        Write-Host "  ✅ $($t.Name) — installed" -ForegroundColor Green
    } catch {
        Pop-Location
        Write-Host "  ❌ $($t.Name) — failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "  Setup complete! Run 'python -m http.server 8899' to view the dashboard." -ForegroundColor Cyan
Write-Host ""
