$ErrorActionPreference = "Continue"

$repos = @(
    # OSINT Tools
    "https://github.com/sherlock-project/sherlock.git",
    "https://github.com/megadose/holehe.git",
    "https://github.com/smicallef/spiderfoot.git",
    
    # LLM Developer Tools
    "https://github.com/567-labs/instructor.git",
    "https://github.com/BerriAI/litellm.git",
    "https://github.com/dottxt-ai/outlines.git",
    "https://github.com/unclecode/crawl4ai.git",
    "https://github.com/stanfordnlp/dspy.git",
    "https://github.com/ollama/ollama.git",
    "https://github.com/qdrant/qdrant.git",
    "https://github.com/langfuse/langfuse.git",
    "https://github.com/VikParuchuri/marker.git",
    "https://github.com/chonkie-inc/chonkie.git",
    
    # Assorted Tools Batch 1
    "https://github.com/simplex-chat/simplex-chat.git",
    "https://github.com/kunchenguid/no-mistakes.git",
    "https://github.com/mauriceboe/TREK.git",
    "https://github.com/aws/agent-toolkit-for-aws.git",
    "https://github.com/apple/container.git",
    "https://github.com/phuryn/pm-skills.git",
    "https://github.com/openai/plugins.git",
    "https://github.com/athasdev/athas.git",
    "https://github.com/bholmesdev/hubble.md.git",
    "https://github.com/joelbqz/writer-computer.git",
    "https://github.com/junhoyeo/tokscale.git",
    "https://github.com/facebook/astryx.git",
    "https://github.com/temporalio/omes.git",
    "https://github.com/edwardsanchez/Tinkerble.git",
    "https://github.com/yorgai/ORG2.git",
    "https://github.com/Forsy-AI/agent-apprenticeship.git",
    "https://github.com/StarTrail-org/PixelRAG.git",
    "https://github.com/vercel/eve.git",
    "https://github.com/zai-org/SCAIL-2.git",
    "https://github.com/samwillis/multithreaded-postgres.git",
    
    # Assorted Tools Batch 2
    "https://github.com/calesthio/OpenMontage.git",
    "https://github.com/bytedance/deer-flow.git",
    "https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git",
    "https://github.com/heygen-com/hyperframes.git",
    "https://github.com/DeusData/codebase-memory-mcp.git",
    "https://github.com/mattpocock/skills.git",
    "https://github.com/garrytan/gstack.git",
    "https://github.com/baidu/Unlimited-OCR.git",
    "https://github.com/nvidia/skillspector.git",
    "https://github.com/palmier-io/palmier-pro.git",
    "https://github.com/NousResearch/hermes-agent.git"
)

$toolsDir = Join-Path $PSScriptRoot "tools"
if (!(Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Path $toolsDir | Out-Null
}

Set-Location $toolsDir

foreach ($repo in $repos) {
    # Extract default folder name
    $folder = ($repo -split '/')[-1] -replace '\.git$'
    
    # Handle naming collisions
    if ($folder -eq "skills" -and $repo -match "mattpocock") {
        $folder = "mattpocock-skills"
    }

    if (Test-Path $folder) {
        # Check if it's a valid git repo or just a broken folder from a timeout
        if (Test-Path "$folder\.git") {
            Write-Host "Skipping $folder - already exists and appears valid." -ForegroundColor Green
        } else {
            Write-Host "Folder $folder exists but is not a valid git repo (likely a failed partial download). Removing and retrying..." -ForegroundColor Yellow
            Remove-Item -Recurse -Force $folder
            git clone --depth 1 $repo $folder
        }
    } else {
        Write-Host "Cloning $folder..." -ForegroundColor Cyan
        git clone --depth 1 $repo $folder
    }
}

Write-Host "`nAll clone checks complete! Check for any red errors above if connections dropped again." -ForegroundColor Green
