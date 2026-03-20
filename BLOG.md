# I Built a CLI That Manages 67 AI Tools — Here's How

> One command to rule them all: agents, RAG, coding assistants, math olympiad solvers, robotics, voice cloning, and more.

---

## The Problem

If you're building with AI, you know the pain. Every week there's a new framework: CrewAI for agents, Langflow for RAG, Aider for coding, vLLM for inference, Whisper for speech... Each one has its own installation, its own docs, its own quirks.

I had 20+ AI tool repos scattered across my machine. Finding one meant `cd`-ing through nested directories. Running one meant remembering which used `npm`, `python`, or `docker`. Updating them meant doing `git pull` one. by. one.

**I needed a single CLI to manage all of them.**

## The Solution: SupAgentic

[SupAgentic](https://github.com/alawalmuazu/SupAgentic) is a unified toolkit for managing 67+ open-source AI tools from one CLI:

```bash
pip install supagentic

supagentic list          # See all 67 tools by category
supagentic search rag    # Find RAG tools instantly
supagentic clone mirofish  # Install any tool on-demand
supagentic setup langflow  # Auto-install dependencies
supagentic run langflow    # Start it (auto-detects npm/python/docker)
supagentic stats          # Live GitHub stars/forks
supagentic tui            # Interactive browser
```

### 18 Commands, Zero Friction

| Command | What it does |
|---------|-------------|
| `list` | All tools by category |
| `search` | Find by name/category/language |
| `clone` | Install a tool from GitHub |
| `run` | Start a tool (auto-detect runtime) |
| `setup` | Auto-install dependencies |
| `stats` | Live GitHub stars & forks |
| `update` | Git pull one or all tools |
| `tui` | Interactive terminal browser |
| `mcp-serve` | Launch MCP server for AI agents |
| `mcp-register` | Auto-configure Claude Desktop, Cursor, etc. |

## The Full MCP Server

This is the killer feature. SupAgentic includes a full [Model Context Protocol](https://modelcontextprotocol.io/) server — any AI assistant can discover and use your tools:

```bash
# Claude Desktop, Cursor, Trae — just register:
supagentic mcp-register

# Remote access via SSE:
python mcp_server.py --sse --port 8765
```

Once connected, you can tell Claude: *"What RAG tools do you have?"* and it searches your toolkit. Say *"Clone and set up Langflow"* and it actually runs the commands.

**55 callable tools × 14 resources × 7 prompt templates** — all accessible to any MCP-compatible AI.

## 16 Categories

| Category | Tools | Highlights |
|----------|-------|-----------|
| 🤖 Agent Frameworks | 11 | CrewAI, AutoGen, LangGraph, Dify, MetaGPT |
| 💻 AI Coding | 12 | Aider, Cursor Rules, SWE-Agent, Claude Code, Gemini CLI |
| 📚 RAG & Retrieval | 4 | LlamaIndex, RAGFlow, Haystack |
| 🧮 Math/Reasoning | 6 | NuminaMath, IMO25, Lean4 |
| 🤖 Robotics | 3 | LeRobot, Isaac Lab, OpenVLA |
| 🎙️ Voice/Audio | 5 | Whisper, Bark, Piper, Kokoro, Fish Speech |
| 🐟 Swarm Intelligence | 3 | MiroFish, OASIS, Swarms |
| 🏠 Local LLM | 3 | Ollama, Open WebUI, DeepSeek |
| 🔒 Security | 2 | Nuclei, Caido |
| + 7 more... | | Training, Simulation, Automation, Data, Media, Serving, Tutorials |

## Orchestration Pipelines

Chain tools together:

```
scrape-predict-narrate:
  Browser-Use → MiroFish → Fish Speech

train-serve-deploy:
  Unsloth → vLLM → Langflow

research-simulate-report:
  RAGFlow → AgentVerse → MiroFish
```

## The Dashboard

A live, searchable dashboard at [alawalmuazu.github.io/SupAgentic](https://alawalmuazu.github.io/SupAgentic) with:
- Search & filter by category
- Direct GitHub links
- MCP server documentation
- Prompt library

## Try It

```bash
git clone https://github.com/alawalmuazu/SupAgentic.git
cd SupAgentic
python supagentic.py list
```

Or install globally:
```bash
pip install supagentic
supagentic tui
```

---

**Star the repo**: [github.com/alawalmuazu/SupAgentic](https://github.com/alawalmuazu/SupAgentic)

*Built with love and way too many git clones.*

---

**Tags**: #ai #opensource #python #cli #mcp #agents #rag #machinelearning #devtools
