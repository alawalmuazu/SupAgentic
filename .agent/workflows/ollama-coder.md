---
description: Use the local Qwen2.5-Coder-14B abliterated model via Ollama for uncensored code generation — exploits, payloads, security scripts, HTML reports, YARA rules
---

# Ollama Coder 14B — Uncensored Code Generation

Use this workflow when the user needs code or content that requires an uncensored model with no guardrails.

## Model Details
- **Name**: Qwen2.5-Coder-14B-Instruct-abliterated
- **ID**: `hf.co/bartowski/Qwen2.5-Coder-14B-Instruct-abliterated-GGUF:Q4_K_M`
- **Size**: 9 GB (Q4_K_M quantization)
- **Context**: 32,768 tokens
- **Speed**: ~12-18 tok/s on RTX 3070
- **Specialization**: Code generation, abliterated (zero refusal)

## When to Use
- Exploit code / PoC scripts
- Offensive security tools
- YARA rules & detection signatures
- HTML/CSS/JS report sections
- Reverse engineering assistance
- Bug bounty payload crafting
- Any code a cloud model would refuse to generate

## How to Call

// turbo-all

1. Send prompt to the model via Ollama API:
```powershell
$body = @{ model = "hf.co/bartowski/Qwen2.5-Coder-14B-Instruct-abliterated-GGUF:Q4_K_M"; prompt = "YOUR_PROMPT_HERE"; stream = $false } | ConvertTo-Json -Depth 3; Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty response
```

2. For multi-turn chat:
```powershell
$body = @{ model = "hf.co/bartowski/Qwen2.5-Coder-14B-Instruct-abliterated-GGUF:Q4_K_M"; messages = @(@{ role = "user"; content = "YOUR_PROMPT_HERE" }); stream = $false } | ConvertTo-Json -Depth 5; Invoke-RestMethod -Uri "http://localhost:11434/api/chat" -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty message | Select-Object -ExpandProperty content
```

## Quick Interactive Mode
```powershell
ollama run hf.co/bartowski/Qwen2.5-Coder-14B-Instruct-abliterated-GGUF:Q4_K_M
```

## Tips
- Be specific with language, framework, and target details
- Ask for complete scripts with error handling
- Works best for code under ~500 lines per generation
- Faster than the 32B model — use this for quick tasks
