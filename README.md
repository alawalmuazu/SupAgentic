# 🚀 SupAgentic

> A unified collection of **34 powerful open-source AI tools** + **7 curated prompts** — from agent orchestration to image generation to LLM training from scratch.

[![GitHub Pages](https://img.shields.io/badge/Dashboard-Live-6366f1?style=for-the-badge)](https://alawalmuazu.github.io/SupAgentic)
[![Tools](https://img.shields.io/badge/Tools-34-14b8a6?style=for-the-badge)](.)
[![Prompts](https://img.shields.io/badge/Prompts-7-ec4899?style=for-the-badge)](prompts/)

---

## 📦 Tools by Category

### 🤖 Agent Frameworks
| # | Tool | Directory | Stars | Description |
|---|------|-----------|-------|-------------|
| 1 | **The Agency** | `tools/agency-agents/` | — | Personality-driven AI agent collection |
| 2 | **CrewAI** | `tools/crewai/` | 44k ⭐ | Role-based multi-agent orchestration |
| 3 | **AutoGen** | `tools/autogen/` | 54k ⭐ | Microsoft's multi-agent conversation framework |
| 4 | **LangGraph** | `tools/langgraph/` | 24k ⭐ | Stateful agent workflows with graph execution |
| 5 | **Dify** | `tools/dify/` | 129k ⭐ | Visual AI app builder with built-in RAG |

### 🛡️ LLM Security
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 6 | **Promptfoo** | `tools/promptfoo/` | LLM evaluation & red-teaming CLI |

### 💻 AI Coding Assistants
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 7 | **Impeccable** | `tools/impeccable/` | Claude design skill to fight "AI slop" |
| 8 | **Aider** | `tools/aider/` | Terminal AI pair programmer with Git integration |
| 9 | **Open Interpreter** | `tools/open-interpreter/` | Let LLMs run code locally |
| 10 | **Fabric** | `tools/fabric/` | 100+ curated AI prompt patterns |
| 11 | **Tabby** | `tools/tabby/` | Self-hosted GitHub Copilot replacement |
| 12 | **Claude Engineer** | `tools/claude-engineer/` | Autonomous coding agent for Claude |

### 📚 RAG & Retrieval
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 13 | **LlamaIndex** | `tools/llama-index/` | Data framework for LLM applications |
| 14 | **RAGFlow** | `tools/ragflow/` | End-to-end production RAG engine |
| 15 | **Anything-LLM** | `tools/anything-llm/` | All-in-one RAG desktop app |

### 🧠 Context & Memory
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 16 | **OpenViking** | `tools/openviking/` | Context database with `viking://` protocol |

### 🐟 Swarm Intelligence
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 17 | **MiroFish** | `tools/mirofish/` | Prediction engine using knowledge graphs |

### 🏠 Local LLM Inference
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 18 | **Ollama** | `tools/ollama/` | Run LLMs locally with one command |

### 🔧 Fine-Tuning & Training
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 19 | **Unsloth** | `tools/unsloth/` | 2-5x faster fine-tuning, 70% less VRAM |
| 20 | **NanoChat** | `tools/nanochat/` | Karpathy's minimal LLM-from-scratch framework |
| 21 | **LLaMA-Factory** | `tools/llama-factory/` | All-in-one fine-tuning with web GUI |

### ⚡ Model Modification
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 22 | **Heretic** | `tools/heretic/` | Automated abliteration for local LLMs |

### 🎨 Image & Media Generation
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 23 | **ComfyUI** | `tools/comfyui/` | Node-based AI image/video/3D generation |
| 24 | **Kokoro TTS** | `tools/kokoro-tts/` | 82M param multilingual text-to-speech |

### 🧪 Tutorials
| # | Tool | Directory | Description |
|---|------|-----------|-------------|
| 25 | **AI Engineering Hub** | `tools/ai-engineering-hub/` | 100+ hands-on AI tutorials |
| 26 | **AI Project Gallery** | `tools/ai-project-gallery/` | ML, Deep Learning & GenAI projects |
| 27 | **500 AI/ML Projects** | `tools/500-ai-ml-projects/` | 500+ real-world projects with code |
| 28 | **E2E GenAI Projects** | `tools/end-to-end-genai-projects/` | Production GenAI with LLMs, RAG, agents |
| 29 | **GenAI Projects** | `tools/genai-projects/` | GenAI portfolio: images, code, text |
| 30 | **100 AI/ML Projects** | `tools/100-ai-ml-projects/` | 100 curated CNN/RNN/GAN/CV/NLP projects |
| 31 | **Awesome Deep Learning** | `tools/awesome-deep-learning/` | 23k⭐ DL tutorials, projects & books |
| 32 | **Awesome ML** | `tools/awesome-machine-learning/` | 66k⭐ Definitive ML frameworks list |
| 33 | **Awesome Project Ideas** | `tools/awesome-project-ideas/` | ML/NLP/CV project ideas for portfolios |
| 34 | **Awesome GenAI Guide** | `tools/awesome-genai-guide/` | Comprehensive GenAI resource hub |

---

## 💬 Prompt Library (7 Prompts)

| Prompt | File | Purpose |
|--------|------|---------|
| Claude Deck Builder | `prompts/Claude prompt.txt` | Auto-generate pitch decks via Gamma |
| System Prompt Extractor | `prompts/system-prompt-extractor.txt` | Educational prompt injection research |
| Full-Stack App Generator | `prompts/fullstack-app-generator.txt` | Scaffold complete apps in one shot |
| Code Review Expert | `prompts/code-review-expert.txt` | Structured security/perf/bug review |
| Chain-of-Thought | `prompts/chain-of-thought.txt` | Force structured reasoning |
| Data Analysis | `prompts/data-analysis.txt` | Comprehensive dataset analysis |
| Resume Generator | `prompts/resume-generator.txt` | ATS-optimized resume/CV builder |

---

## ⚡ Quick Start

```bash
# View the dashboard
python -m http.server 8899
# Open http://localhost:8899

# Use the CLI
python supagentic.py list       # List all tools
python supagentic.py search rag # Search by category
python supagentic.py health     # Check repo freshness
python supagentic.py serve      # Launch dashboard

# Install tool dependencies
.\setup.ps1                     # Interactive installer

# Spin up local AI stack (Docker)
docker compose -f docker-compose.local-stack.yml up -d
```

---

## 📚 More

- **[INTEGRATIONS.md](INTEGRATIONS.md)** — 5 recipes for combining tools
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to suggest & add tools
- **[setup.ps1](setup.ps1)** — Interactive dependency installer
- **[health.ps1](health.ps1)** — Repo freshness checker
- **[supagentic.py](supagentic.py)** — CLI tool

---

## 📄 License

Each tool retains its original license. See `tools/<name>/LICENSE`.
