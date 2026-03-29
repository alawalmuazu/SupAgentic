---
description: Access the SupAgentic AI toolkit — 65 tools for agents, security, RAG, training, media, data, automation, simulation, and more. List, search, run, setup, clone, browse, and orchestrate tools via the CLI or MCP server.
---

# SupAgentic Toolkit — Unified AI Tool Management

Use this workflow to interact with the SupAgentic collection of 65 open-source AI tools.

## Toolkit Location
- **Root**: `C:\Users\OMEN\Documents\SupAgentic`
- **Tools**: `C:\Users\OMEN\Documents\SupAgentic\tools\` (65 subdirectories)
- **CLI**: `C:\Users\OMEN\Documents\SupAgentic\supagentic.py`
- **MCP Server**: `C:\Users\OMEN\Documents\SupAgentic\mcp_server.py`
- **Prompts**: `C:\Users\OMEN\Documents\SupAgentic\prompts\` (7 prompt files)
- **Dashboard**: https://alawalmuazu.github.io/SupAgentic

## Available Tools (65) — 15 Categories

### Agent Frameworks
- CrewAI, AutoGen, LangGraph, Dify, Langflow, MetaGPT, AutoGPT, LangChain, Chainlit, Phidata, The Agency, Hermes Agent

### LLM Security
- Promptfoo (red-teaming, evaluation)

### AI Coding
- Aider, Open Interpreter, Fabric, Tabby, Claude Engineer, Gemini CLI, Claude Code, Impeccable, Cursor Rules, SWE-Agent, Bolt.new, GStack, Superpowers, Agent Skills, OpenCode, Awesome Claude Code, UI/UX Pro Max

### RAG & Retrieval
- LlamaIndex, RAGFlow, Anything-LLM, Haystack

### Context & Memory
- OpenViking, Mem0

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
- OpenClaw, Browser-Use, n8n, Paperclip

### Data & Analytics
- PandasAI, Dataherald

### Security & Pentesting
- Nuclei, Caido

### Model Serving
- vLLM

### Other
- Heretic (modding), AI Engineering Hub (tutorials)

## CLI Commands (18)

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

6. Clone a tool on-demand:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py clone <tool-name>
```

7. Run a tool:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py run <tool-name>
```

8. Install dependencies:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py setup <tool-name>
```

9. Live GitHub stats:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py stats [query]
```

10. Scaffold new tool:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py create <name> <repo> <category> <language>
```

11. Show dependency map:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py deps [tool-name]
```

12. View orchestration pipelines:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py pipeline [name]
```

13. Interactive TUI browser:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py tui
```

14. MCP manifest:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py mcp --json
```

15. Launch MCP server:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py mcp-serve [--sse --port 8765]
```

16. Register MCP with AI clients:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py mcp-register
```

17. Start dashboard:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py serve
```

18. Open tool directory:
```powershell
python C:\Users\OMEN\Documents\SupAgentic\supagentic.py open <tool-name>
```

## MCP Server
- **stdio**: `python mcp_server.py` (for Claude Desktop, Cursor, Trae, Codex)
- **SSE**: `python mcp_server.py --sse --port 8765` (for remote access)
- **Register**: `python supagentic.py mcp-register` (auto-configure clients)
- **Capabilities**: 55 tools, 14 resources, 7 prompts

## Orchestration Pipelines
- `scrape-predict-narrate`: Browser-Use → MiroFish → Fish Speech
- `train-serve-deploy`: Unsloth → vLLM → Langflow
- `research-simulate-report`: RAGFlow → AgentVerse → MiroFish

## Docker Stack
```powershell
docker compose -f C:\Users\OMEN\Documents\SupAgentic\docker-compose.local-stack.yml up -d
```
