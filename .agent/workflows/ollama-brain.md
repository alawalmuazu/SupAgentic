---
description: Use the local QwQ-32B abliterated reasoning model via Ollama for deep uncensored analysis — vulnerability research, threat modeling, exploit chain reasoning, MITRE ATT&CK mapping
---

# Ollama Brain 32B — Uncensored Deep Analysis

Use this workflow when the user needs deep reasoning and analysis that requires an uncensored model with no guardrails.

## Model Details
- **Name**: QwQ-32B-abliterated (huihui-ai)
- **ID**: `hf.co/bartowski/huihui-ai_QwQ-32B-abliterated-GGUF:Q4_K_M`
- **Size**: 19 GB (Q4_K_M quantization)
- **Context**: 32,768 tokens
- **Speed**: ~5-10 tok/s on RTX 3070 + 64GB RAM
- **Specialization**: Reasoning, chain-of-thought, abliterated (zero refusal)

## When to Use
- Deep vulnerability analysis
- Threat modeling & kill chain design
- MITRE ATT&CK technique mapping
- Complex exploit chain reasoning
- Malware behavior analysis
- Security architecture review
- Strategic penetration test planning
- Any analysis a cloud model would refuse to perform

## How to Call

// turbo-all

1. Send prompt to the model via Ollama API:
```powershell
$body = @{ model = "hf.co/bartowski/huihui-ai_QwQ-32B-abliterated-GGUF:Q4_K_M"; prompt = "YOUR_PROMPT_HERE"; stream = $false } | ConvertTo-Json -Depth 3; Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty response
```

2. For multi-turn chat:
```powershell
$body = @{ model = "hf.co/bartowski/huihui-ai_QwQ-32B-abliterated-GGUF:Q4_K_M"; messages = @(@{ role = "user"; content = "YOUR_PROMPT_HERE" }); stream = $false } | ConvertTo-Json -Depth 5; Invoke-RestMethod -Uri "http://localhost:11434/api/chat" -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty message | Select-Object -ExpandProperty content
```

## Quick Interactive Mode
```powershell
ollama run hf.co/bartowski/huihui-ai_QwQ-32B-abliterated-GGUF:Q4_K_M
```

## Tips
- This model uses chain-of-thought reasoning — responses take longer but are much deeper
- Output includes <think> tags showing the reasoning process
- Best for complex multi-step analysis, NOT for quick code snippets
- Provide as much context as possible — paste code, configs, logs
- Ask for structured output: tables, MITRE mappings, severity ratings
- Slower than Coder 14B but significantly smarter
