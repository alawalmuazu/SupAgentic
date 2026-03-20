#!/usr/bin/env python3
"""
SupAgentic CLI — Unified interface for managing your AI toolkit.

Usage:
    python supagentic.py list              # List all tools
    python supagentic.py search <query>    # Search tools
    python supagentic.py info <tool>       # Show tool details
    python supagentic.py health            # Check repo health
    python supagentic.py update [tool]     # Git pull tool(s)
    python supagentic.py serve             # Start dashboard server
    python supagentic.py open <tool>       # Open tool directory
"""

import os
import sys
import json
import subprocess
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console encoding: force UTF-8 so emoji & box-drawing chars work
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR / "tools"

# ═══ Tool Registry ═══
TOOLS = [
    {"name": "The Agency",       "dir": "agency-agents",     "cat": "Agents",      "repo": "msitarzewski/agency-agents",         "lang": "Prompts"},
    {"name": "CrewAI",           "dir": "crewai",            "cat": "Agents",      "repo": "crewAIInc/crewAI",                   "lang": "Python"},
    {"name": "AutoGen",          "dir": "autogen",           "cat": "Agents",      "repo": "microsoft/autogen",                  "lang": "Python"},
    {"name": "LangGraph",        "dir": "langgraph",         "cat": "Agents",      "repo": "langchain-ai/langgraph",             "lang": "Python"},
    {"name": "Dify",             "dir": "dify",              "cat": "Agents",      "repo": "langgenius/dify",                    "lang": "Python/TS"},
    {"name": "Promptfoo",        "dir": "promptfoo",         "cat": "Security",    "repo": "promptfoo/promptfoo",                "lang": "TypeScript"},
    {"name": "Impeccable",       "dir": "impeccable",        "cat": "Coding",      "repo": "pbakaus/impeccable",                 "lang": "Prompts"},
    {"name": "Aider",            "dir": "aider",             "cat": "Coding",      "repo": "Aider-AI/aider",                     "lang": "Python"},
    {"name": "Open Interpreter", "dir": "open-interpreter",  "cat": "Coding",      "repo": "OpenInterpreter/open-interpreter",   "lang": "Python"},
    {"name": "LlamaIndex",       "dir": "llama-index",       "cat": "RAG",         "repo": "run-llama/llama_index",              "lang": "Python"},
    {"name": "RAGFlow",          "dir": "ragflow",           "cat": "RAG",         "repo": "infiniflow/ragflow",                 "lang": "Python/TS"},
    {"name": "OpenViking",       "dir": "openviking",        "cat": "Memory",      "repo": "volcengine/OpenViking",              "lang": "Python"},
    {"name": "MiroFish",         "dir": "mirofish",          "cat": "Swarm",       "repo": "666ghj/MiroFish",                    "lang": "Python/Vue"},
    {"name": "OASIS",            "dir": "oasis",             "cat": "Swarm",       "repo": "camel-ai/oasis",                     "lang": "Python"},
    {"name": "Generative Agents","dir": "generative-agents", "cat": "Simulation",  "repo": "joonspk-research/generative_agents",  "lang": "Python"},
    {"name": "AgentVerse",       "dir": "agentverse",        "cat": "Simulation",  "repo": "OpenBMB/AgentVerse",                  "lang": "Python"},
    {"name": "TwinMarket",       "dir": "twinmarket",        "cat": "Simulation",  "repo": "TobyYang7/TwinMarket",                "lang": "Python"},
    {"name": "Swarms",           "dir": "swarms",            "cat": "Swarm",       "repo": "kyegomez/swarms",                     "lang": "Python"},
    {"name": "Ollama",           "dir": "ollama",            "cat": "Local LLM",   "repo": "ollama/ollama",                      "lang": "Go"},
    {"name": "Unsloth",          "dir": "unsloth",           "cat": "Training",    "repo": "unslothai/unsloth",                  "lang": "Python"},
    {"name": "NanoChat",         "dir": "nanochat",          "cat": "Training",    "repo": "karpathy/nanochat",                  "lang": "Python"},
    {"name": "Heretic",          "dir": "heretic",           "cat": "Modding",     "repo": "p-e-w/heretic",                      "lang": "Python"},
    {"name": "ComfyUI",          "dir": "comfyui",           "cat": "Media",       "repo": "comfyanonymous/ComfyUI",             "lang": "Python"},
    {"name": "Kokoro TTS",       "dir": "kokoro-tts",        "cat": "Media",       "repo": "hexgrad/kokoro",                     "lang": "Python"},
    {"name": "AI Engineering Hub","dir": "ai-engineering-hub","cat": "Tutorials",   "repo": "alawalmuazu/ai-engineering-hub",     "lang": "Python"},
    {"name": "LLaMA-Factory",    "dir": "llama-factory",     "cat": "Training",    "repo": "hiyouga/LLaMA-Factory",              "lang": "Python"},
    {"name": "Fabric",           "dir": "fabric",            "cat": "Coding",      "repo": "danielmiessler/fabric",              "lang": "Go"},
    {"name": "Anything-LLM",     "dir": "anything-llm",      "cat": "RAG",         "repo": "Mintplex-Labs/anything-llm",         "lang": "JavaScript"},
    {"name": "Tabby",            "dir": "tabby",             "cat": "Coding",      "repo": "TabbyML/tabby",                      "lang": "Rust"},
    {"name": "Claude Engineer",  "dir": "claude-engineer",   "cat": "Coding",      "repo": "Doriandarko/claude-engineer",        "lang": "Python"},
    {"name": "OpenClaw",         "dir": "openclaw",           "cat": "Automation",  "repo": "openclaw/openclaw",                  "lang": "TypeScript"},
    {"name": "Browser-Use",      "dir": "browser-use",        "cat": "Browser",     "repo": "browser-use/browser-use",            "lang": "Python"},
    {"name": "Langflow",         "dir": "langflow",           "cat": "Agents",      "repo": "langflow-ai/langflow",               "lang": "Python"},
    {"name": "Fish Speech",      "dir": "fish-speech",        "cat": "Media",       "repo": "fishaudio/fish-speech",              "lang": "Python"},
    {"name": "vLLM",             "dir": "vllm",               "cat": "Serving",     "repo": "vllm-project/vllm",                  "lang": "Python"},
    {"name": "Open WebUI",       "dir": "open-webui",          "cat": "Local LLM",   "repo": "open-webui/open-webui",              "lang": "Python/Svelte"},
    {"name": "DeepSeek-V3",      "dir": "deepseek",            "cat": "Local LLM",   "repo": "deepseek-ai/DeepSeek-V3",            "lang": "Python"},
    {"name": "Gemini CLI",       "dir": "gemini-cli",          "cat": "Coding",      "repo": "google-gemini/gemini-cli",           "lang": "TypeScript"},
    {"name": "Claude Code",      "dir": "claude-code",         "cat": "Coding",      "repo": "anthropics/claude-code",             "lang": "TypeScript"},
    {"name": "n8n",              "dir": "n8n",                 "cat": "Automation",  "repo": "n8n-io/n8n",                         "lang": "TypeScript"},
    {"name": "MetaGPT",          "dir": "metagpt",             "cat": "Agents",      "repo": "geekan/MetaGPT",                     "lang": "Python"},
    {"name": "AutoGPT",          "dir": "autogpt",             "cat": "Agents",      "repo": "Significant-Gravitas/AutoGPT",       "lang": "Python"},
    {"name": "LangChain",        "dir": "langchain",           "cat": "Agents",      "repo": "langchain-ai/langchain",             "lang": "Python"},
    {"name": "Cursor Rules",     "dir": "cursor-rules",        "cat": "Coding",      "repo": "PatrickJS/awesome-cursorrules",      "lang": "Markdown"},
    {"name": "Haystack",         "dir": "haystack",            "cat": "RAG",         "repo": "deepset-ai/haystack",                "lang": "Python"},
    {"name": "Chainlit",         "dir": "chainlit",            "cat": "Agents",      "repo": "Chainlit/chainlit",                  "lang": "Python/TS"},
    {"name": "Mem0",             "dir": "mem0",                "cat": "Memory",      "repo": "mem0ai/mem0",                        "lang": "Python"},
    {"name": "Phidata",          "dir": "phidata",             "cat": "Agents",      "repo": "phidatahq/phidata",                  "lang": "Python"},
    {"name": "SWE-Agent",        "dir": "swe-agent",           "cat": "Coding",      "repo": "princeton-nlp/SWE-agent",            "lang": "Python"},
    {"name": "Bolt.new",         "dir": "bolt-new",            "cat": "Coding",      "repo": "stackblitz/bolt.new",                "lang": "TypeScript"},
    {"name": "PandasAI",         "dir": "pandas-ai",           "cat": "Data",        "repo": "Sinaptik-AI/pandas-ai",              "lang": "Python"},
    {"name": "Dataherald",       "dir": "dataherald",           "cat": "Data",        "repo": "Dataherald/dataherald",              "lang": "Python"},
    {"name": "Nuclei",           "dir": "nuclei",               "cat": "Security",    "repo": "projectdiscovery/nuclei",            "lang": "Go"},
    {"name": "Caido",            "dir": "caido",                "cat": "Security",    "repo": "caido/caido",                        "lang": "Rust"},
    {"name": "OpenMAIC",          "dir": "openmaic",             "cat": "Simulation",  "repo": "THU-MAIC/OpenMAIC",                  "lang": "TypeScript"},
    {"name": "NuminaMath",        "dir": "numinamath",           "cat": "Math",        "repo": "project-numina/aimo-progress-prize", "lang": "Python"},
    {"name": "IMO25",             "dir": "imo25",                "cat": "Math",        "repo": "lyang36/IMO25",                      "lang": "Python"},
    {"name": "Math Medalist",     "dir": "agent-math-medalist",  "cat": "Math",        "repo": "MattJBorowski1991/AgentMathOlympiadMedalist", "lang": "Python"},
    {"name": "AI Math Olympiad",  "dir": "ai-math-olympiad",     "cat": "Math",        "repo": "awsaf49/ai-math-olympiad",           "lang": "Python"},
    {"name": "Lean4",             "dir": "lean4",                "cat": "Math",        "repo": "leanprover/lean4",                   "lang": "Lean"},
    {"name": "Mathlib4",          "dir": "mathlib4",             "cat": "Math",        "repo": "leanprover-community/mathlib4",      "lang": "Lean"},
    {"name": "LeRobot",           "dir": "lerobot",              "cat": "Robotics",    "repo": "huggingface/lerobot",                "lang": "Python"},
    {"name": "Isaac Lab",         "dir": "isaac-lab",            "cat": "Robotics",    "repo": "isaac-sim/IsaacLab",                 "lang": "Python"},
    {"name": "OpenVLA",           "dir": "openvla",              "cat": "Robotics",    "repo": "openvla/openvla",                    "lang": "Python"},
    {"name": "Whisper",           "dir": "whisper",              "cat": "Voice",       "repo": "openai/whisper",                     "lang": "Python"},
    {"name": "Bark",              "dir": "bark",                 "cat": "Voice",       "repo": "suno-ai/bark",                       "lang": "Python"},
    {"name": "Piper",             "dir": "piper",                "cat": "Voice",       "repo": "rhasspy/piper",                      "lang": "C++"},
    {"name": "Manim",             "dir": "manim",                "cat": "Media",       "repo": "3b1b/manim",                         "lang": "Python"},
    {"name": "Rive",              "dir": "rive-runtime",         "cat": "Media",       "repo": "rive-app/rive-runtime",              "lang": "C++/JS"},
    {"name": "Gaussian Splatting","dir": "gaussian-splatting",   "cat": "Media",       "repo": "graphdeco-inria/gaussian-splatting", "lang": "Python/CUDA"},
    {"name": "AudioCraft",        "dir": "audiocraft",           "cat": "Media",       "repo": "facebookresearch/audiocraft",        "lang": "Python"},
    {"name": "SAM",               "dir": "segment-anything",     "cat": "Media",       "repo": "facebookresearch/segment-anything",  "lang": "Python"},
    {"name": "Taichi",            "dir": "taichi",               "cat": "Simulation",  "repo": "taichi-dev/taichi",                  "lang": "Python/CUDA"},
    {"name": "AlphaFold",         "dir": "alphafold",            "cat": "Science",     "repo": "google-deepmind/alphafold",          "lang": "Python"},
    {"name": "Qiskit",            "dir": "qiskit",               "cat": "Science",     "repo": "Qiskit/qiskit",                      "lang": "Python"},
]

# ═══ Colors ═══
class C:
    HEADER = '\033[95m'; BLUE = '\033[94m'; CYAN = '\033[96m'; GREEN = '\033[92m'
    YELLOW = '\033[93m'; RED = '\033[91m'; BOLD = '\033[1m'; DIM = '\033[2m'
    END = '\033[0m'

def banner():
    print(f"\n{C.CYAN}{C.BOLD}  ╔═══════════════════════════════════════╗")
    print(f"  ║        SupAgentic CLI v2.0.0          ║")
    print(f"  ╚═══════════════════════════════════════╝{C.END}\n")

def cmd_list(args):
    """List all tools"""
    banner()
    cats = {}
    for t in TOOLS:
        cats.setdefault(t["cat"], []).append(t)

    for cat, tools in cats.items():
        print(f"  {C.BOLD}{C.YELLOW}{cat}{C.END}")
        for t in tools:
            installed = "✅" if (TOOLS_DIR / t["dir"]).exists() else "❌"
            print(f"    {installed} {t['name']:<22} {C.DIM}[{t['lang']}]{C.END}")
        print()

    total_tools = len([t for t in TOOLS if t['cat'] != 'Tutorials'])
    total_tutorials = len([t for t in TOOLS if t['cat'] == 'Tutorials'])
    installed = sum(1 for t in TOOLS if (TOOLS_DIR / t["dir"]).exists() and t['cat'] != 'Tutorials')
    print(f"  {C.CYAN}{installed}/{total_tools} tools installed{C.END} {C.DIM}(+ {total_tutorials} tutorial collections){C.END}\n")

def cmd_search(args):
    """Search tools by name, category or language"""
    if not args:
        print("Usage: supagentic search <query>")
        return

    query = " ".join(args).lower()
    matches = [t for t in TOOLS if query in t["name"].lower() or query in t["cat"].lower() or query in t["lang"].lower() or query in t["dir"].lower()]

    if not matches:
        print(f"  {C.RED}No tools match '{query}'{C.END}")
        return

    print(f"\n  {C.CYAN}{len(matches)} result(s) for '{query}':{C.END}\n")
    for t in matches:
        installed = "✅" if (TOOLS_DIR / t["dir"]).exists() else "❌"
        print(f"  {installed} {C.BOLD}{t['name']}{C.END} — {t['cat']} [{t['lang']}]")
        print(f"     github.com/{t['repo']}")
        print()

def cmd_info(args):
    """Show detailed info about a tool"""
    if not args:
        print("Usage: supagentic info <tool-name>")
        return

    query = " ".join(args).lower()
    tool = next((t for t in TOOLS if query in t["name"].lower() or query == t["dir"]), None)

    if not tool:
        print(f"  {C.RED}Tool '{query}' not found{C.END}")
        return

    path = TOOLS_DIR / tool["dir"]
    installed = path.exists()

    print(f"\n  {C.BOLD}{C.CYAN}{tool['name']}{C.END}")
    print(f"  {'─' * 40}")
    print(f"  Category:  {tool['cat']}")
    print(f"  Language:  {tool['lang']}")
    print(f"  Repo:      github.com/{tool['repo']}")
    print(f"  Local:     {path}")
    print(f"  Installed: {'✅ Yes' if installed else '❌ No'}")

    if installed:
        try:
            log = subprocess.check_output(["git", "-C", str(path), "log", "-1", "--format=%ai | %s"], text=True).strip()
            print(f"  Last commit: {log}")
        except: pass

        readme = path / "README.md"
        if readme.exists():
            lines = readme.read_text(encoding="utf-8", errors="ignore").split("\n")
            desc = next((l.strip("# \n") for l in lines if l.strip() and not l.startswith("#")), "No description")
            print(f"  Description: {desc[:80]}...")
    print()

def cmd_health(args):
    """Check health of all installed tools"""
    banner()
    print(f"  {C.BOLD}Tool Health Report{C.END}\n")

    for t in TOOLS:
        path = TOOLS_DIR / t["dir"]
        if not path.exists():
            print(f"  ❌ {t['name']:<22} — not installed")
            continue

        try:
            date_str = subprocess.check_output(
                ["git", "-C", str(path), "log", "-1", "--format=%ai"], text=True
            ).strip()[:10]
            commit_date = datetime.strptime(date_str, "%Y-%m-%d")
            days_ago = (datetime.now() - commit_date).days

            if days_ago > 180:
                status = f"{C.RED}🔴 Stale ({days_ago}d){C.END}"
            elif days_ago > 90:
                status = f"{C.YELLOW}🟡 Aging ({days_ago}d){C.END}"
            else:
                status = f"{C.GREEN}🟢 Fresh ({days_ago}d){C.END}"

            print(f"  {status:>40}  {t['name']}")
        except:
            print(f"  ⚠️  {t['name']:<22} — git error")

    print()

def cmd_update(args):
    """Git pull one or all tools"""
    tools_to_update = TOOLS
    if args:
        query = " ".join(args).lower()
        tools_to_update = [t for t in TOOLS if query in t["name"].lower() or query == t["dir"]]

    for t in tools_to_update:
        path = TOOLS_DIR / t["dir"]
        if not path.exists():
            continue
        print(f"  📥 Pulling {t['name']}...", end="", flush=True)
        try:
            subprocess.run(["git", "-C", str(path), "pull", "--ff-only"],
                         capture_output=True, timeout=30)
            print(f" {C.GREEN}✅{C.END}")
        except:
            print(f" {C.RED}❌{C.END}")

def cmd_serve(args):
    """Start dashboard HTTP server"""
    port = int(args[0]) if args else 8899
    print(f"  {C.CYAN}Starting dashboard at http://localhost:{port}{C.END}")
    print(f"  Press Ctrl+C to stop\n")
    webbrowser.open(f"http://localhost:{port}")
    os.chdir(str(SCRIPT_DIR))
    subprocess.run([sys.executable, "-m", "http.server", str(port)])

def cmd_open(args):
    """Open tool directory"""
    if not args:
        print("Usage: supagentic open <tool-name>")
        return

    query = " ".join(args).lower()
    tool = next((t for t in TOOLS if query in t["name"].lower() or query == t["dir"]), None)
    if tool:
        path = TOOLS_DIR / tool["dir"]
        if path.exists():
            if sys.platform == "win32":
                os.startfile(str(path))
            else:
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)])
        else:
            print(f"  {C.RED}Tool not installed locally{C.END}")
    else:
        print(f"  {C.RED}Tool '{query}' not found{C.END}")

# ═══ Dependency Map ═══
DEPS = {
    "mirofish":  {"needs": ["oasis"], "ports": "3000/5001", "start": "npm run dev"},
    "oasis":     {"needs": [], "ports": None, "start": "python -m oasis"},
    "langflow":  {"needs": [], "ports": "7860", "start": "python -m langflow run"},
    "openclaw":  {"needs": ["ollama"], "ports": "3000", "start": "npm run dev"},
    "browser-use": {"needs": [], "ports": None, "start": "python -m browser_use"},
    "fish-speech": {"needs": [], "ports": "7862", "start": "python tools/webui/app.py"},
    "vllm":      {"needs": [], "ports": "8000", "start": "python -m vllm.entrypoints.openai.api_server"},
    "ollama":    {"needs": [], "ports": "11434", "start": "ollama serve"},
    "comfyui":   {"needs": [], "ports": "8188", "start": "python main.py"},
    "ragflow":   {"needs": [], "ports": "9380", "start": "docker compose up -d"},
    "dify":      {"needs": [], "ports": "3000", "start": "docker compose up -d"},
    "open-webui": {"needs": ["ollama"], "ports": "3000", "start": "docker compose up -d"},
    "gemini-cli": {"needs": [], "ports": None, "start": "npx @anthropic-ai/claude-code"},
    "claude-code": {"needs": [], "ports": None, "start": "npx @anthropic-ai/claude-code"},
}

# ═══ Orchestration Pipelines ═══
PIPELINES = {
    "scrape-predict-narrate": {
        "desc": "Scrape web → Simulate prediction → Voice narrate the report",
        "steps": [
            {"tool": "browser-use", "action": "Scrape target URL and extract data"},
            {"tool": "mirofish", "action": "Build knowledge graph → Run multi-agent simulation → Generate report"},
            {"tool": "fish-speech", "action": "Convert report to natural speech audio"},
        ]
    },
    "train-serve-deploy": {
        "desc": "Fine-tune model → Serve with vLLM → Connect to agents",
        "steps": [
            {"tool": "unsloth", "action": "Fine-tune base model with LoRA/QLoRA"},
            {"tool": "vllm", "action": "Deploy model with OpenAI-compatible API"},
            {"tool": "langflow", "action": "Build agent workflow using served model"},
        ]
    },
    "research-simulate-report": {
        "desc": "RAG retrieval → Agent simulation → Automated analysis",
        "steps": [
            {"tool": "ragflow", "action": "Ingest documents and build RAG pipeline"},
            {"tool": "agentverse", "action": "Run multi-agent debate/analysis on findings"},
            {"tool": "mirofish", "action": "Generate comprehensive prediction report"},
        ]
    },
}

def cmd_run(args):
    """Start a tool with auto-detected startup method"""
    if not args:
        print(f"  {C.YELLOW}Usage: supagentic run <tool-name>{C.END}")
        print(f"  {C.DIM}Example: supagentic run mirofish{C.END}")
        return

    query = " ".join(args).lower()
    tool = next((t for t in TOOLS if query in t["name"].lower() or query == t["dir"]), None)
    if not tool:
        print(f"  {C.RED}Tool '{query}' not found{C.END}")
        return

    path = TOOLS_DIR / tool["dir"]
    if not path.exists():
        print(f"  {C.RED}Tool not installed. Run: git clone https://github.com/{tool['repo']}.git {path}{C.END}")
        return

    dep_info = DEPS.get(tool["dir"], {})
    ports = dep_info.get("ports", "")
    custom_start = dep_info.get("start", "")

    # Check dependencies
    needs = dep_info.get("needs", [])
    if needs:
        print(f"  {C.YELLOW}⚠ Dependencies: {', '.join(needs)}{C.END}")

    # Auto-detect startup
    if custom_start:
        cmd = custom_start
    elif (path / "package.json").exists():
        cmd = "npm run dev"
    elif (path / "docker-compose.yml").exists() or (path / "docker-compose.yaml").exists():
        cmd = "docker compose up -d"
    elif (path / "main.py").exists():
        cmd = f"{sys.executable} main.py"
    elif (path / "run.py").exists():
        cmd = f"{sys.executable} run.py"
    elif (path / "app.py").exists():
        cmd = f"{sys.executable} app.py"
    else:
        print(f"  {C.YELLOW}No auto-start method detected. Check the tool's README.{C.END}")
        return

    print(f"\n  {C.BOLD}{C.CYAN}🚀 Starting {tool['name']}{C.END}")
    if ports:
        print(f"  {C.DIM}Ports: {ports}{C.END}")
    print(f"  {C.DIM}Command: {cmd}{C.END}")
    print(f"  {C.DIM}Working dir: {path}{C.END}\n")

    try:
        subprocess.run(cmd, shell=True, cwd=str(path))
    except KeyboardInterrupt:
        print(f"\n  {C.YELLOW}Stopped {tool['name']}{C.END}")

def cmd_setup(args):
    """Auto-install dependencies for a tool"""
    if not args:
        print(f"  {C.YELLOW}Usage: supagentic setup <tool-name>{C.END}")
        print(f"  {C.DIM}Detects requirements.txt, package.json, pyproject.toml, etc.{C.END}")
        return

    query = " ".join(args).lower()
    tool = next((t for t in TOOLS if query in t["name"].lower() or query == t["dir"]), None)
    if not tool:
        print(f"  {C.RED}Tool '{query}' not found{C.END}")
        return

    path = TOOLS_DIR / tool["dir"]
    if not path.exists():
        print(f"  {C.RED}Tool not installed locally{C.END}")
        return

    print(f"\n  {C.BOLD}{C.CYAN}📦 Setting up {tool['name']}{C.END}")
    print(f"  {C.DIM}Scanning {path} for dependency files...{C.END}\n")

    found = False

    # Python: pyproject.toml (uv or pip)
    if (path / "pyproject.toml").exists():
        found = True
        print(f"  {C.GREEN}Found pyproject.toml{C.END} — installing with uv...")
        try:
            subprocess.run(["uv", "sync"], cwd=str(path), timeout=120)
        except FileNotFoundError:
            print(f"  {C.YELLOW}uv not found, trying pip...{C.END}")
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=str(path), timeout=120)

    # Python: requirements.txt
    if (path / "requirements.txt").exists():
        found = True
        print(f"  {C.GREEN}Found requirements.txt{C.END} — installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=str(path), timeout=120)

    # Node: package.json
    if (path / "package.json").exists():
        found = True
        print(f"  {C.GREEN}Found package.json{C.END} — installing with npm...")
        subprocess.run(["npm", "install"], cwd=str(path), shell=True, timeout=120)

    # Python: setup.py
    if (path / "setup.py").exists() and not (path / "pyproject.toml").exists():
        found = True
        print(f"  {C.GREEN}Found setup.py{C.END} — installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=str(path), timeout=120)

    # Python: Pipfile
    if (path / "Pipfile").exists():
        found = True
        print(f"  {C.GREEN}Found Pipfile{C.END} — installing with pipenv...")
        try:
            subprocess.run(["pipenv", "install"], cwd=str(path), timeout=120)
        except FileNotFoundError:
            print(f"  {C.YELLOW}pipenv not found. Install with: pip install pipenv{C.END}")

    # Docker
    if (path / "docker-compose.yml").exists() or (path / "docker-compose.yaml").exists() or (path / "compose.yaml").exists():
        found = True
        print(f"  {C.GREEN}Found Docker Compose{C.END} — run: docker compose up -d")

    if not found:
        print(f"  {C.YELLOW}No dependency files detected. Check the tool's README for setup instructions.{C.END}")
    else:
        print(f"\n  {C.GREEN}✅ Setup complete for {tool['name']}{C.END}\n")

def cmd_deps(args):
    """Show dependency tree for a tool"""
    banner()
    if not args:
        print(f"  {C.BOLD}Tool Dependency Map{C.END}\n")
        for name, info in DEPS.items():
            tool = next((t for t in TOOLS if t["dir"] == name), None)
            if not tool:
                continue
            needs = info.get("needs", [])
            ports = info.get("ports", "")
            start = info.get("start", "")
            deps_str = f" → {', '.join(needs)}" if needs else ""
            port_str = f" [:{ports}]" if ports else ""
            print(f"  {C.CYAN}{tool['name']:<20}{C.END}{deps_str}{C.DIM}{port_str}{C.END}")
        print()
        return

    query = " ".join(args).lower()
    tool = next((t for t in TOOLS if query in t["name"].lower() or query == t["dir"]), None)
    if not tool:
        print(f"  {C.RED}Tool '{query}' not found{C.END}")
        return

    info = DEPS.get(tool["dir"], {})
    print(f"  {C.BOLD}{tool['name']}{C.END}")
    print(f"  {C.DIM}Category:{C.END} {tool['cat']}")
    print(f"  {C.DIM}Start:{C.END}    {info.get('start', 'N/A')}")
    print(f"  {C.DIM}Ports:{C.END}    {info.get('ports', 'None')}")
    needs = info.get("needs", [])
    if needs:
        print(f"  {C.DIM}Needs:{C.END}    {', '.join(needs)}")
        for n in needs:
            ni = DEPS.get(n, {})
            print(f"    └─ {n} → {ni.get('start', '?')} [:{ni.get('ports', '?')}]")
    print()

def cmd_pipeline(args):
    """Show or run orchestration pipelines"""
    banner()
    if not args:
        print(f"  {C.BOLD}Orchestration Pipelines{C.END}\n")
        for name, pipe in PIPELINES.items():
            print(f"  {C.CYAN}{name}{C.END}")
            print(f"  {C.DIM}{pipe['desc']}{C.END}")
            for i, step in enumerate(pipe["steps"], 1):
                tool = next((t for t in TOOLS if t["dir"] == step["tool"]), {"name": step["tool"]})
                print(f"    {i}. {C.BOLD}{tool['name']}{C.END} → {step['action']}")
            print()
        print(f"  {C.DIM}Run: supagentic pipeline <name>{C.END}\n")
        return

    name = " ".join(args).lower().replace(" ", "-")
    pipe = PIPELINES.get(name)
    if not pipe:
        print(f"  {C.RED}Pipeline '{name}' not found{C.END}")
        return

    print(f"\n  {C.BOLD}{C.CYAN}▶ Running pipeline: {name}{C.END}")
    print(f"  {C.DIM}{pipe['desc']}{C.END}\n")
    for i, step in enumerate(pipe["steps"], 1):
        tool = next((t for t in TOOLS if t["dir"] == step["tool"]), {"name": step["tool"], "dir": step["tool"]})
        path = TOOLS_DIR / tool["dir"] if isinstance(tool, dict) and "dir" in tool else None
        installed = path and path.exists() if path else False
        status = f"{C.GREEN}✅{C.END}" if installed else f"{C.RED}❌ not installed{C.END}"
        print(f"  Step {i}: {C.BOLD}{tool['name']}{C.END} {status}")
        print(f"  {C.DIM}  → {step['action']}{C.END}\n")

def cmd_mcp(args):
    """Start MCP (Model Context Protocol) server for tool discovery"""
    import json as js

    tools_manifest = []
    for t in TOOLS:
        path = TOOLS_DIR / t["dir"]
        dep_info = DEPS.get(t["dir"], {})
        tools_manifest.append({
            "name": t["name"],
            "directory": t["dir"],
            "category": t["cat"],
            "language": t["lang"],
            "repository": f"https://github.com/{t['repo']}",
            "installed": path.exists(),
            "start_command": dep_info.get("start", None),
            "ports": dep_info.get("ports", None),
            "dependencies": dep_info.get("needs", []),
        })

    manifest = {
        "name": "supagentic",
        "version": "1.0.0",
        "description": "SupAgentic AI Toolkit — 35 tools across 13 categories",
        "tools_count": len(tools_manifest),
        "categories": sorted(set(t["cat"] for t in TOOLS)),
        "tools": tools_manifest,
        "pipelines": {n: {"description": p["desc"], "steps": [s["tool"] for s in p["steps"]]} for n, p in PIPELINES.items()},
    }

    if args and args[0] == "--json":
        print(js.dumps(manifest, indent=2))
    else:
        banner()
        print(f"  {C.BOLD}MCP Server Manifest{C.END}\n")
        print(f"  {C.DIM}Tools:{C.END}      {manifest['tools_count']}")
        print(f"  {C.DIM}Categories:{C.END} {', '.join(manifest['categories'])}")
        print(f"  {C.DIM}Pipelines:{C.END}  {', '.join(manifest['pipelines'].keys())}")
        print(f"\n  {C.CYAN}Export JSON:  python supagentic.py mcp --json{C.END}")
        print(f"  {C.CYAN}Pipe to MCP:  python supagentic.py mcp --json | mcp-server{C.END}")
        print()

def cmd_clone(args):
    """Clone a tool from GitHub on-demand"""
    if not args:
        print(f"  {C.YELLOW}Usage: supagentic clone <tool-name>{C.END}")
        print(f"  {C.DIM}Example: supagentic clone mirofish{C.END}")
        print(f"\n  {C.DIM}Not installed:{C.END}")
        for t in TOOLS:
            if t["cat"] == "Tutorials":
                continue
            path = TOOLS_DIR / t["dir"]
            if not path.exists():
                print(f"    {C.RED}✗{C.END} {t['name']} ({t['cat']})")
        print()
        return

    query = " ".join(args).lower()
    tool = next((t for t in TOOLS if query in t["name"].lower() or query == t["dir"]), None)
    if not tool:
        print(f"  {C.RED}Tool '{query}' not found{C.END}")
        return

    path = TOOLS_DIR / tool["dir"]
    if path.exists():
        print(f"  {C.GREEN}✅ {tool['name']} already installed at {path}{C.END}")
        return

    url = f"https://github.com/{tool['repo']}.git"
    print(f"\n  {C.BOLD}{C.CYAN}📥 Cloning {tool['name']}{C.END}")
    print(f"  {C.DIM}{url} → {path}{C.END}\n")

    try:
        subprocess.run(["git", "clone", "--depth", "1", url, str(path)], timeout=120)
        print(f"\n  {C.GREEN}✅ {tool['name']} installed!{C.END}")
        print(f"  {C.DIM}Run: supagentic setup {tool['dir']}{C.END}")
        print(f"  {C.DIM}     supagentic run {tool['dir']}{C.END}\n")
    except Exception as e:
        print(f"  {C.RED}Clone failed: {e}{C.END}")

def cmd_stats(args):
    """Fetch live GitHub stats for tools"""
    import urllib.request

    banner()
    print(f"  {C.BOLD}GitHub Stats (Live){C.END}\n")

    tools_to_check = TOOLS
    if args:
        query = " ".join(args).lower()
        tools_to_check = [t for t in TOOLS if query in t["name"].lower() or query == t["dir"] or query == t["cat"].lower()]

    for t in tools_to_check:
        if t["cat"] == "Tutorials":
            continue
        try:
            url = f"https://api.github.com/repos/{t['repo']}"
            req = urllib.request.Request(url, headers={"User-Agent": "SupAgentic-CLI/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                stars = data.get("stargazers_count", 0)
                forks = data.get("forks_count", 0)
                issues = data.get("open_issues_count", 0)

                if stars >= 100000:
                    star_str = f"{C.GREEN}{stars//1000}k ⭐{C.END}"
                elif stars >= 10000:
                    star_str = f"{C.CYAN}{stars//1000}k ⭐{C.END}"
                else:
                    star_str = f"{stars//1000}k ⭐"

                print(f"  {t['name']:<22} {star_str:>16}  {forks:>5} forks  {issues:>4} issues")
        except Exception:
            print(f"  {t['name']:<22} {C.DIM}(offline){C.END}")

    print()

def cmd_create(args):
    """Scaffold a new tool entry"""
    if not args:
        print(f"  {C.YELLOW}Usage: supagentic create <name> <github-repo> <category> <language>{C.END}")
        print(f"  {C.DIM}Example: supagentic create MyTool user/repo Agents Python{C.END}")
        return

    if len(args) < 4:
        print(f"  {C.RED}Need 4 args: name, repo, category, language{C.END}")
        return

    name, repo, cat, lang = args[0], args[1], args[2], " ".join(args[3:])
    dir_name = name.lower().replace(" ", "-")

    # Check if already exists
    if any(t["dir"] == dir_name for t in TOOLS):
        print(f"  {C.RED}Tool '{name}' already registered{C.END}")
        return

    # Create directory structure
    path = TOOLS_DIR / dir_name
    path.mkdir(parents=True, exist_ok=True)

    # Create README
    readme = path / "README.md"
    readme.write_text(f"# {name}\n\n> Added via `supagentic create`\n\n"
                      f"- **Category**: {cat}\n- **Language**: {lang}\n"
                      f"- **Repository**: https://github.com/{repo}\n", encoding="utf-8")

    # Show what to add to registry
    entry = f'    {{"name": "{name}", "dir": "{dir_name}", "cat": "{cat}", "repo": "{repo}", "lang": "{lang}"}},'
    print(f"\n  {C.GREEN}✅ Scaffolded {name} at {path}{C.END}")
    print(f"  {C.DIM}Created README.md{C.END}")
    print(f"\n  {C.YELLOW}Add this line to TOOLS in supagentic.py:{C.END}")
    print(f"  {C.CYAN}{entry}{C.END}")

    # Optionally clone
    print(f"\n  {C.DIM}Clone: supagentic clone {dir_name}{C.END}\n")

def cmd_tui(args):
    """Interactive TUI for browsing tools"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.prompt import Prompt
        from rich import box
    except ImportError:
        print(f"  {C.YELLOW}Installing rich...{C.END}")
        subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.prompt import Prompt
        from rich import box

    console = Console()

    while True:
        console.clear()

        # Header
        console.print(Panel.fit(
            "[bold cyan]SupAgentic[/] — [dim]Interactive Tool Browser[/]",
            border_style="cyan", box=box.DOUBLE
        ))

        # Category list
        cats = {}
        for t in TOOLS:
            if t["cat"] == "Tutorials":
                continue
            cats.setdefault(t["cat"], []).append(t)

        cat_names = sorted(cats.keys())
        console.print("\n[bold yellow]Categories:[/]")
        for i, cat in enumerate(cat_names, 1):
            count = len(cats[cat])
            console.print(f"  [cyan]{i:>2}.[/] {cat} [dim]({count} tools)[/]")

        console.print(f"\n[dim]Type a category number, tool name, 'all', or 'q' to quit[/]")
        choice = Prompt.ask("\n[bold]>>", default="all")

        if choice.lower() in ("q", "quit", "exit"):
            break

        # Build tool list based on choice
        if choice == "all":
            show_tools = [t for t in TOOLS if t["cat"] != "Tutorials"]
            title = "All Tools"
        elif choice.isdigit() and 1 <= int(choice) <= len(cat_names):
            cat = cat_names[int(choice) - 1]
            show_tools = cats[cat]
            title = cat
        else:
            show_tools = [t for t in TOOLS if choice.lower() in t["name"].lower() and t["cat"] != "Tutorials"]
            title = f"Search: {choice}"

        if not show_tools:
            console.print(f"[red]No tools found[/]")
            Prompt.ask("[dim]Press Enter to continue[/]")
            continue

        # Display table
        table = Table(title=title, box=box.ROUNDED, border_style="cyan")
        table.add_column("#", style="dim", width=3)
        table.add_column("Tool", style="bold white")
        table.add_column("Category", style="yellow")
        table.add_column("Language", style="cyan")
        table.add_column("Status", justify="center")

        for i, t in enumerate(show_tools, 1):
            installed = (TOOLS_DIR / t["dir"]).exists()
            status = "[green]✅[/]" if installed else "[red]✗[/]"
            table.add_row(str(i), t["name"], t["cat"], t["lang"], status)

        console.print()
        console.print(table)

        # Actions
        console.print(f"\n[dim]Enter tool number for actions, or press Enter to go back[/]")
        pick = Prompt.ask("[bold]>>", default="")

        if pick.isdigit() and 1 <= int(pick) <= len(show_tools):
            t = show_tools[int(pick) - 1]
            console.print(f"\n[bold cyan]{t['name']}[/]")
            console.print(f"  [dim]Category:[/]  {t['cat']}")
            console.print(f"  [dim]Language:[/]  {t['lang']}")
            console.print(f"  [dim]Repo:[/]      https://github.com/{t['repo']}")
            console.print(f"  [dim]Dir:[/]       tools/{t['dir']}/")
            installed = (TOOLS_DIR / t["dir"]).exists()
            console.print(f"  [dim]Status:[/]    {'[green]Installed[/]' if installed else '[red]Not installed[/]'}")

            console.print(f"\n  [cyan]r[/]=run  [cyan]s[/]=setup  [cyan]c[/]=clone  [cyan]o[/]=open  [cyan]Enter[/]=back")
            action = Prompt.ask("[bold]>>", default="")

            if action == "r" and installed:
                cmd_run([t["dir"]])
            elif action == "s" and installed:
                cmd_setup([t["dir"]])
            elif action == "c" and not installed:
                cmd_clone([t["dir"]])
            elif action == "o" and installed:
                cmd_open([t["dir"]])

def cmd_mcp_serve(args):
    """Launch the full MCP server"""
    server_path = SCRIPT_DIR / "mcp_server.py"
    cmd_args = [sys.executable, str(server_path)]
    if "--sse" in args:
        cmd_args.append("--sse")
        for i, a in enumerate(args):
            if a == "--port" and i + 1 < len(args):
                cmd_args.extend(["--port", args[i + 1]])
    try:
        subprocess.run(cmd_args)
    except KeyboardInterrupt:
        print(f"\n  {C.YELLOW}MCP server stopped{C.END}")

def cmd_mcp_register(args):
    """Register MCP server with Claude Desktop / Cursor"""
    server_path = SCRIPT_DIR / "mcp_server.py"
    subprocess.run([sys.executable, str(server_path), "--register"])

# ═══ Command Router ═══
COMMANDS = {
    "list": cmd_list, "ls": cmd_list,
    "search": cmd_search, "find": cmd_search,
    "info": cmd_info,
    "health": cmd_health, "status": cmd_health,
    "update": cmd_update, "pull": cmd_update,
    "serve": cmd_serve, "dashboard": cmd_serve,
    "open": cmd_open,
    "run": cmd_run, "start": cmd_run,
    "setup": cmd_setup, "install": cmd_setup,
    "clone": cmd_clone, "get": cmd_clone,
    "stats": cmd_stats,
    "create": cmd_create, "new": cmd_create,
    "tui": cmd_tui, "browse": cmd_tui,
    "mcp": cmd_mcp,
    "mcp-serve": cmd_mcp_serve,
    "mcp-register": cmd_mcp_register,
    "deps": cmd_deps, "dependencies": cmd_deps,
    "pipeline": cmd_pipeline, "pipe": cmd_pipeline,
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        banner()
        print("  Commands:")
        print(f"    {C.CYAN}list{C.END}              List all tools")
        print(f"    {C.CYAN}search <query>{C.END}    Search tools by name/category/language")
        print(f"    {C.CYAN}info <tool>{C.END}       Show tool details")
        print(f"    {C.CYAN}health{C.END}            Check repo freshness")
        print(f"    {C.CYAN}update [tool]{C.END}     Git pull tool(s)")
        print(f"    {C.CYAN}clone <tool>{C.END}      Install a tool on-demand from GitHub")
        print(f"    {C.CYAN}run <tool>{C.END}        Start a tool (auto-detect startup)")
        print(f"    {C.CYAN}setup <tool>{C.END}      Install dependencies for a tool")
        print(f"    {C.CYAN}stats [query]{C.END}     Live GitHub stars/forks/issues")
        print(f"    {C.CYAN}create <args>{C.END}     Scaffold a new tool entry")
        print(f"    {C.CYAN}deps [tool]{C.END}       Show dependency map")
        print(f"    {C.CYAN}pipeline [name]{C.END}   Show/run orchestration pipelines")
        print(f"    {C.CYAN}tui{C.END}               Interactive tool browser (rich)")
        print(f"    {C.CYAN}mcp [--json]{C.END}      MCP manifest / JSON export")
        print(f"    {C.CYAN}mcp-serve{C.END}         Launch MCP server (stdio or --sse)")
        print(f"    {C.CYAN}mcp-register{C.END}      Register with Claude Desktop / Cursor")
        print(f"    {C.CYAN}serve [port]{C.END}      Start dashboard server")
        print(f"    {C.CYAN}open <tool>{C.END}       Open tool directory")
        print()
        return

    cmd = sys.argv[1].lower()
    handler = COMMANDS.get(cmd)
    if handler:
        handler(sys.argv[2:])
    else:
        print(f"  {C.RED}Unknown command: {cmd}{C.END}")
        print(f"  Run 'python supagentic.py --help' for usage")

if __name__ == "__main__":
    main()
