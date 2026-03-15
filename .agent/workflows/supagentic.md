---
description: Access the SupAgentic AI toolkit — 25 tools for agents, security, RAG, training, media. List, search, health-check, and update tools via the CLI.
---

# SupAgentic Toolkit — Unified AI Tool Management

Use this workflow to interact with the SupAgentic collection of 25 open-source AI tools.

## Toolkit Location
- **Root**: `C:\Users\OMEN\Documents\SupAgentic`
- **Tools**: `C:\Users\OMEN\Documents\SupAgentic\tools\` (25 subdirectories)
- **CLI**: `C:\Users\OMEN\Documents\SupAgentic\supagentic.py`
- **Prompts**: `C:\Users\OMEN\Documents\SupAgentic\prompts\` (7 prompt files)
- **Dashboard**: `C:\Users\OMEN\Documents\SupAgentic\index.html`

## Available Tools (25)

### Agent Frameworks
- CrewAI, AutoGen, LangGraph, Dify, The Agency

### LLM Security
- Promptfoo (red-teaming, evaluation)

### AI Coding
- Aider, Open Interpreter, Fabric, Tabby, Claude Engineer, Impeccable

### RAG & Retrieval
- LlamaIndex, RAGFlow, Anything-LLM

### Training & Fine-Tuning
- Unsloth, NanoChat, LLaMA-Factory

### Model Modification
- Heretic (abliteration)

### Media Generation
- ComfyUI (image/video), Kokoro TTS (text-to-speech)

### Other
- Ollama (local LLM), OpenViking (memory), MiroFish (swarm), AI Engineering Hub (tutorials)

## CLI Commands

// turbo-all

1. List all tools:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py list
```

2. Search tools:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py search <query>
```

3. Get tool info:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py info <tool-name>
```

4. Check health:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py health
```

5. Update tools:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py update [tool-name]
```

6. Start dashboard:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py serve
```

## Integration Pipelines
See INTEGRATIONS.md for 5 recipes:
1. Fully Local Agent Pipeline (CrewAI + Ollama + RAGFlow)
2. LLM Security Testing (Promptfoo + Aider + Open Interpreter)
3. AI Content Factory (ComfyUI + Kokoro TTS + Dify)
4. Fine-Tune & Deploy (Unsloth + Heretic + Ollama)
5. Learn-by-Doing (AI Engineering Hub + LlamaIndex + LangGraph)
