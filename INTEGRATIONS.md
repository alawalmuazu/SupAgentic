# SupAgentic — Integration Guides

> Recipes for combining tools from this collection into powerful AI pipelines.

---

## 🏠 Fully Local Agent Pipeline
**CrewAI + Ollama + RAGFlow**

Build a multi-agent system that runs 100% locally — no API keys, no cloud, no data leaves your machine.

### Architecture
```
[Your Documents] → RAGFlow (index & retrieve) → Ollama (local LLM) → CrewAI (agent team)
```

### Setup
```bash
# 1. Start Ollama and pull a model
ollama pull llama3.1

# 2. Start RAGFlow (Docker required)
cd tools/ragflow
docker compose up -d

# 3. Configure CrewAI to use Ollama
export OPENAI_API_BASE=http://localhost:11434/v1
export OPENAI_API_KEY=ollama  # any string works
export OPENAI_MODEL_NAME=llama3.1
```

### Example: Research Agent Team
```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Research Analyst",
    goal="Find and summarize information from local documents",
    backstory="You have access to a RAGFlow knowledge base via API",
)

writer = Agent(
    role="Technical Writer",
    goal="Turn research into clear, structured reports",
    backstory="You specialize in making complex topics accessible",
)

research_task = Task(
    description="Search the knowledge base for information about {topic}",
    agent=researcher,
)

write_task = Task(
    description="Write a comprehensive report based on the research findings",
    agent=writer,
)

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff(inputs={"topic": "AI agent architectures"})
```

---

## 🛡️ LLM Security Testing Pipeline
**Promptfoo + Aider + Open Interpreter**

Automatically red-team your LLM applications before deploying.

### Setup
```bash
# Install Promptfoo globally
npm install -g promptfoo

# Create a test config
promptfoo init
```

### Workflow
1. **Build** your LLM app using Aider for pair programming
2. **Test** with Promptfoo's red-team suite:
   ```bash
   promptfoo redteam generate    # auto-generate attack prompts
   promptfoo redteam eval        # run the attacks
   promptfoo redteam report      # view results
   ```
3. **Fix** vulnerabilities found by the red-team using Aider
4. **Verify** fixes with Open Interpreter running the test suite locally

---

## 🎨 AI Content Factory
**ComfyUI + Kokoro TTS + Dify**

Build an automated content pipeline: text → images → voiceover → distribution.

### Architecture
```
[Dify Workflow] → ComfyUI (generate images) → Kokoro TTS (generate audio) → [Output]
```

### Setup
```bash
# 1. Start Dify
cd tools/dify/docker
docker compose up -d
# Access at http://localhost/install

# 2. Start ComfyUI
cd tools/comfyui
pip install -r requirements.txt
python main.py
# Access at http://localhost:8188

# 3. Install Kokoro TTS
pip install kokoro
```

### Use Case: Automated Podcast Generator
1. Dify workflow takes a topic and generates a script
2. ComfyUI generates episode artwork and scene illustrations
3. Kokoro TTS reads the script with natural-sounding voices
4. Output: complete podcast episode with art + audio

---

## 🔧 Fine-Tune & Deploy Pipeline
**Unsloth + NanoChat + Heretic + Ollama**

Train a custom model, optionally uncensor it, and deploy locally.

### Workflow
```
[Training Data] → Unsloth (fine-tune) → Heretic (optional abliteration) → Ollama (serve)
```

### Steps
```bash
# 1. Fine-tune with Unsloth (2-5x faster, 70% less VRAM)
cd tools/unsloth
# Use their Colab notebook or local script

# 2. (Optional) Remove safety alignment with Heretic
cd tools/heretic
python heretic.py --model ./my-fine-tuned-model

# 3. Convert to GGUF and serve with Ollama
ollama create my-model -f Modelfile
ollama run my-model
```

---

## 📚 Learn-by-Doing Pipeline
**AI Engineering Hub + LlamaIndex + LangGraph**

Use the tutorials collection as a learning path, building real projects.

### Suggested Learning Path
1. **Week 1: RAG Fundamentals** — `ai-engineering-hub/agentic_rag/` + LlamaIndex
2. **Week 2: Multi-Agent Systems** — `ai-engineering-hub/Multi-Agent-deep-researcher/` + LangGraph
3. **Week 3: Fine-Tuning** — `ai-engineering-hub/DeepSeek-finetuning/` + Unsloth
4. **Week 4: Full Pipeline** — Combine everything into your own project

---

*More integration recipes? Open an issue or PR on the [SupAgentic repo](https://github.com/alawalmuazu/SupAgentic).*
