---
description: Access the SupAgentic AI toolkit — 43 tools for agents, security, RAG, training, media, automation, simulation, and more. List, search, run, setup, and orchestrate tools via the CLI.
---

# SupAgentic Toolkit — Unified AI Tool Management

Use this workflow to interact with the SupAgentic collection of 43 open-source AI tools.

## Toolkit Location
- **Root**: `C:\Users\OMEN\Documents\SupAgentic`
- **Tools**: `C:\Users\OMEN\Documents\SupAgentic\tools\` (43 subdirectories)
- **CLI**: `C:\Users\OMEN\Documents\SupAgentic\supagentic.py`
- **Prompts**: `C:\Users\OMEN\Documents\SupAgentic\prompts\` (7 prompt files)
- **Dashboard**: https://alawalmuazu.github.io/SupAgentic

## Available Tools (43) — 13 Categories

### Agent Frameworks
- CrewAI, AutoGen, LangGraph, Dify, Langflow, MetaGPT, AutoGPT, LangChain, The Agency

### LLM Security
- Promptfoo (red-teaming, evaluation)

### AI Coding
- Aider, Open Interpreter, Fabric, Tabby, Claude Engineer, Gemini CLI, Claude Code, Impeccable

### RAG & Retrieval
- LlamaIndex, RAGFlow, Anything-LLM

### Swarm Intelligence
- MiroFish, OASIS, Swarms

### Simulation
- Generative Agents, AgentVerse, TwinMarket

### Local LLM
- Ollama, Open WebUI, DeepSeek-V3

### Training & Fine-Tuning
- Unsloth, NanoChat, LLaMA-Factory

### Media
- ComfyUI, Kokoro TTS, Fish Speech

### Automation & Browser
- OpenClaw, Browser-Use, n8n

### Model Serving
- vLLM

### Other
- OpenViking (memory), Heretic (modding), AI Engineering Hub (tutorials)

## CLI Commands (12)

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

6. Run a tool:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py run <tool-name>
```

7. Install dependencies:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py setup <tool-name>
```

8. Show dependency map:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py deps [tool-name]
```

9. View orchestration pipelines:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py pipeline [name]
```

10. MCP manifest:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py mcp --json
```

11. Start dashboard:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py serve
```

12. Open tool directory:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py open <tool-name>
```

## Orchestration Pipelines
- `scrape-predict-narrate`: Browser-Use → MiroFish → Fish Speech
- `train-serve-deploy`: Unsloth → vLLM → Langflow
- `research-simulate-report`: RAGFlow → AgentVerse → MiroFish

## Docker Stack
```powershell
docker compose -f C:\Users\OMEN\Documents\SupAgentic\docker-compose.local-stack.yml up -d
```
