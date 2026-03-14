# SupAgentic — Tool Comparison Matrix

> Side-by-side comparison of all 25 tools across key dimensions.

---

## 🤖 Agent Frameworks Compared

| Feature | The Agency | CrewAI | AutoGen | LangGraph | Dify |
|---------|-----------|--------|---------|-----------|------|
| **Stars** | ~500 | 44k | 54k | 24k | 129k |
| **Language** | Prompts | Python | Python | Python | Python/TS |
| **Multi-agent** | ✅ Role-based | ✅ Crew/Role | ✅ Conversation | ✅ Graph-based | ✅ Visual |
| **Visual UI** | ❌ | ❌ | ❌ | ❌ | ✅ Built-in |
| **Built-in RAG** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Docker Ready** | ❌ | ❌ | ✅ Sandbox | ❌ | ✅ |
| **Production Use** | Prototyping | Fortune 500 | Enterprise | Production | Production |
| **Learning Curve** | 🟢 Easy | 🟢 Easy | 🟡 Medium | 🟡 Medium | 🟢 Easy |
| **Best For** | Quick teams | Role teams | Conversations | Complex flows | No-code apps |

---

## 💻 Coding Assistants Compared

| Feature | Impeccable | Aider | Open Interpreter | Fabric | Tabby | Claude Engineer |
|---------|-----------|-------|-----------------|--------|-------|----------------|
| **Type** | Prompt Skill | CLI Tool | CLI Tool | Framework | IDE Extension | CLI Agent |
| **Language** | — | Python | Python | Go | Rust | Python |
| **Git Integration** | ❌ | ✅ Auto-commit | ❌ | ❌ | ❌ | ✅ |
| **Code Execution** | ❌ | ❌ | ✅ Local | ❌ | ❌ | ✅ |
| **Multi-model** | Claude only | ✅ Any LLM | ✅ Any LLM | ✅ Any LLM | ✅ Local | Claude only |
| **Offline** | ❌ | ❌ | ✅ w/ Ollama | ✅ w/ Ollama | ✅ Self-hosted | ❌ |
| **Best For** | UI design | Pair coding | Automation | Patterns | Copilot alt | Complex tasks |

---

## 📚 RAG & Retrieval Compared

| Feature | LlamaIndex | RAGFlow | Anything-LLM |
|---------|-----------|---------|---------------|
| **Stars** | 125k | Growing | Growing |
| **Type** | Framework | Engine | Desktop App |
| **Language** | Python | Python/TS | JavaScript |
| **Document Types** | PDF, DB, API | PDF, Images, Tables | PDF, Web, Files |
| **Built-in UI** | ❌ | ✅ Web UI | ✅ Desktop + Web |
| **Multi-user** | ❌ | ✅ | ✅ |
| **Embedding Models** | Any | Built-in | Any |
| **Local/Private** | ✅ | ✅ | ✅ |
| **Best For** | Custom pipelines | Enterprise docs | Quick setup |

---

## 🔧 Fine-Tuning Tools Compared

| Feature | Unsloth | NanoChat | LLaMA-Factory |
|---------|---------|---------|---------------|
| **Stars** | Growing | New | 42k |
| **Speed** | 2-5x faster | Standard | Standard |
| **VRAM Saving** | 70-80% | Standard | Moderate |
| **GUI** | ❌ | ❌ | ✅ Web UI |
| **Methods** | LoRA, QLoRA | Full training | LoRA, QLoRA, RLHF, DPO |
| **Models** | Llama, Mistral, DeepSeek | GPT-2 class | 100+ models |
| **CUDA Kernels** | ✅ Custom | ❌ | ❌ |
| **Best For** | Speed + efficiency | Learning | Flexibility |

---

## 🎨 Media Generation Compared

| Feature | ComfyUI | Kokoro TTS |
|---------|---------|-----------|
| **Type** | Visual workflow | TTS model |
| **Output** | Image, Video, 3D, Audio | Speech audio |
| **Interface** | Node graph | Python API |
| **Models** | Flux, SDXL, custom | 82M param custom |
| **Languages** | N/A | EN, FR, KR, JP, ZH |
| **License** | GPL-3.0 | Apache 2.0 |

---

## 📊 Quick Decision Guide

| I want to... | Use |
|--------------|-----|
| Build an AI app without coding | **Dify** |
| Create an AI dev team | **CrewAI** |
| Run models locally | **Ollama** |
| Fine-tune a model fast | **Unsloth** |
| Fine-tune with a GUI | **LLaMA-Factory** |
| Chat with my documents | **Anything-LLM** |
| Build custom RAG pipelines | **LlamaIndex** |
| Red-team my LLM app | **Promptfoo** |
| AI pair programming | **Aider** |
| Replace GitHub Copilot | **Tabby** |
| Generate images | **ComfyUI** |
| Generate speech | **Kokoro TTS** |
| Learn AI engineering | **AI Engineering Hub** |
| Extract AI prompt patterns | **Fabric** |
