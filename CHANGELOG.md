# Changelog

All notable changes to SupAgentic are documented here.

## [1.5.0] — 2026-03-19

### New Commands
- `clone <tool>` — install any tool on-demand from GitHub
- `stats [query]` — live GitHub stars/forks/issues via API
- `create <name> <repo> <cat> <lang>` — scaffold new tool entries
- `tui` / `browse` — interactive tool browser using rich tables
- `mcp-serve` — real MCP server with stdio JSON-RPC protocol

### Infrastructure
- `pyproject.toml` — PyPI-ready packaging (`pip install supagentic`)
- CLI now has **17 commands** (up from 12)
- Tutorials pruned from tool count display and stats

---

## [1.4.0] — 2026-03-19 🎯 **50-TOOL MILESTONE**

### Added
- **Cursor Rules** — community-curated .cursorrules library (10k ⭐)
- **Haystack** — Deepset's RAG & NLP pipeline framework (42k ⭐)
- **Chainlit** — build production-ready chat UIs for AI (8k ⭐)
- **Mem0** — self-improving memory layer for agents (25k ⭐)
- **Phidata** — multi-modal agent toolkit with function calling (20k ⭐)
- **SWE-Agent** — Princeton's autonomous software engineer (18k ⭐)
- **Bolt.new** — AI full-stack web app builder by StackBlitz (28k ⭐)
- Toolkit now at **50 tools** across **13 categories** 🎉

---

## [1.3.0] — 2026-03-19

### Added
- **n8n** — workflow automation with AI (160k ⭐)
- **MetaGPT** — multi-agent software company (62k ⭐)
- **AutoGPT** — the OG autonomous agent platform (175k ⭐)
- **LangChain** — foundational LLM framework (123k ⭐)
- Toolkit now at **43 tools** across **13 categories**

---

## [1.2.0] — 2026-03-19

### Added
- **Open WebUI** — self-hosted ChatGPT UI for Ollama (80k ⭐)
- **DeepSeek-V3** — GPT-4-class open MoE model (100k ⭐)
- **Gemini CLI** — Google's agentic coding terminal (87k ⭐)
- **Claude Code** — Anthropic's on-device coding assistant (46k ⭐)
- `setup` command — auto-install tool dependencies
- Social preview image (`assets/social-preview.png`)

---

## [1.1.0] — 2026-03-18

### Added
- **OpenClaw** — personal AI assistant, 250k ⭐
- **Browser-Use** — browser automation for AI agents
- **Langflow** — visual agent builder, 140k ⭐
- **Fish Speech** — voice cloning TTS, 26k ⭐
- **vLLM** — high-throughput model serving engine

### New Features
- `run <tool>` — auto-start any tool
- `deps [tool]` — dependency map with ports
- `pipeline [name]` — 3 orchestration pipelines
- `mcp [--json]` — MCP manifest export
- `docker-compose.local-stack.yml` — 7-service Docker stack
- 5 new dashboard filter buttons (Swarm, Simulation, Automation, Browser, Serving)

---

## [1.0.0] — 2026-03-17

### Added
- **MiroFish** — prediction engine with swarm intelligence
- **OASIS** — social simulation engine (CAMEL-AI)
- **Generative Agents** — Stanford Smallville (18k ⭐)
- **AgentVerse** — multi-agent simulation platform
- **TwinMarket** — financial market simulation (NeurIPS 2025)
- **Swarms** — enterprise multi-agent orchestration
- Windows UTF-8 encoding fix for CLI

### Initial Release (25 tools)
- Agent frameworks: The Agency, CrewAI, AutoGen, LangGraph, Dify
- Security: Promptfoo
- Coding: Impeccable, Aider, Open Interpreter, Fabric, Tabby, Claude Engineer
- RAG: LlamaIndex, RAGFlow, Anything-LLM
- Memory: OpenViking
- Local LLM: Ollama
- Training: Unsloth, NanoChat, LLaMA-Factory
- Modding: Heretic
- Media: ComfyUI, Kokoro TTS
- Tutorials: AI Engineering Hub
- 7 curated prompts
- CLI with list, search, info, health, update, serve, open
- Dashboard with search, filters, and dark/light theme
- GitHub Pages deployment
