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
]

# ═══ Colors ═══
class C:
    HEADER = '\033[95m'; BLUE = '\033[94m'; CYAN = '\033[96m'; GREEN = '\033[92m'
    YELLOW = '\033[93m'; RED = '\033[91m'; BOLD = '\033[1m'; DIM = '\033[2m'
    END = '\033[0m'

def banner():
    print(f"\n{C.CYAN}{C.BOLD}  ╔═══════════════════════════════════════╗")
    print(f"  ║        SupAgentic CLI v1.0.0          ║")
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

    total = len(TOOLS)
    installed = sum(1 for t in TOOLS if (TOOLS_DIR / t["dir"]).exists())
    print(f"  {C.CYAN}{installed}/{total} tools installed{C.END}\n")

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

# ═══ Command Router ═══
COMMANDS = {
    "list": cmd_list, "ls": cmd_list,
    "search": cmd_search, "find": cmd_search,
    "info": cmd_info,
    "health": cmd_health, "status": cmd_health,
    "update": cmd_update, "pull": cmd_update,
    "serve": cmd_serve, "dashboard": cmd_serve,
    "open": cmd_open,
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
