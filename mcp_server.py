#!/usr/bin/env python3
"""
SupAgentic MCP Server — Full Model Context Protocol implementation.

Transports:
    stdio:  python mcp_server.py                    (default)
    sse:    python mcp_server.py --sse [--port 8765]

Features:
    - tools/list + tools/call with real action execution
    - resources/list + resources/read (README, INTEGRATIONS, prompts, pipelines)
    - prompts/list + prompts/get (7 curated AI prompts)
    - initialize handshake with full capability negotiation
"""

import os
import sys
import json
import subprocess
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# Fix Windows encoding
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR / "tools"
PROMPTS_DIR = SCRIPT_DIR / "prompts"

# Import tool registry
sys.path.insert(0, str(SCRIPT_DIR))
from supagentic import TOOLS, DEPS, PIPELINES

SERVER_INFO = {
    "name": "supagentic",
    "version": "2.0.0",
}

CAPABILITIES = {
    "tools": {"listChanged": False},
    "resources": {"subscribe": False, "listChanged": False},
    "prompts": {"listChanged": False},
}

# ═══ Tool Definitions ═══
def build_tools():
    """Build MCP tool list from registry"""
    tools = []
    for t in TOOLS:
        if t["cat"] == "Tutorials":
            continue
        tools.append({
            "name": f"supagentic_{t['dir'].replace('-', '_')}",
            "description": f"{t['name']} — {t['cat']} tool ({t['lang']}). Repo: github.com/{t['repo']}",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["info", "run", "setup", "clone", "update", "open"],
                        "description": "Action to perform on this tool"
                    },
                },
                "required": ["action"]
            }
        })

    # Meta tools
    tools.append({
        "name": "supagentic_search",
        "description": "Search across all 54 SupAgentic tools by name, category, or language",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    })
    tools.append({
        "name": "supagentic_pipeline",
        "description": "Run an orchestration pipeline (scrape-predict-narrate, train-serve-deploy, research-simulate-report)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pipeline": {"type": "string", "enum": list(PIPELINES.keys())}
            },
            "required": ["pipeline"]
        }
    })
    return tools

# ═══ Resource Definitions ═══
def build_resources():
    """Build MCP resource list"""
    resources = []

    # Static files
    for fname, desc in [
        ("README.md", "SupAgentic documentation — 54 tools, 15 categories"),
        ("INTEGRATIONS.md", "5 integration recipes for combining tools"),
        ("CHANGELOG.md", "Version history and release notes"),
        ("CONTRIBUTING.md", "How to contribute and add tools"),
    ]:
        path = SCRIPT_DIR / fname
        if path.exists():
            resources.append({
                "uri": f"file:///{path.as_posix()}",
                "name": fname,
                "description": desc,
                "mimeType": "text/markdown"
            })

    # Prompts as resources
    if PROMPTS_DIR.exists():
        for pf in sorted(PROMPTS_DIR.glob("*.txt")):
            resources.append({
                "uri": f"supagentic://prompts/{pf.stem}",
                "name": pf.stem.replace("-", " ").title(),
                "description": f"AI prompt template: {pf.stem}",
                "mimeType": "text/plain"
            })

    # Pipelines as resources
    for pname, pdata in PIPELINES.items():
        resources.append({
            "uri": f"supagentic://pipelines/{pname}",
            "name": pname,
            "description": pdata.get("desc", "Orchestration pipeline"),
            "mimeType": "application/json"
        })

    return resources

# ═══ Prompt Definitions ═══
def build_prompts():
    """Build MCP prompt list from prompts/ directory"""
    prompts = []
    if not PROMPTS_DIR.exists():
        return prompts

    prompt_meta = {
        "Claude prompt": {"desc": "System prompt for Claude-style AI assistants", "args": []},
        "chain-of-thought": {"desc": "Step-by-step reasoning prompt template", "args": [
            {"name": "problem", "description": "The problem to reason through", "required": True}
        ]},
        "code-review-expert": {"desc": "Expert code review with security and performance analysis", "args": [
            {"name": "code", "description": "Code to review", "required": True},
            {"name": "language", "description": "Programming language", "required": False}
        ]},
        "data-analysis": {"desc": "Data analysis and visualization prompt", "args": [
            {"name": "dataset", "description": "Description of the dataset", "required": True},
            {"name": "goal", "description": "Analysis goal", "required": False}
        ]},
        "fullstack-app-generator": {"desc": "Full-stack application scaffolding prompt", "args": [
            {"name": "app_idea", "description": "Application concept", "required": True},
            {"name": "tech_stack", "description": "Preferred technologies", "required": False}
        ]},
        "resume-generator": {"desc": "Professional resume/CV generator", "args": [
            {"name": "experience", "description": "Work experience details", "required": True},
            {"name": "target_role", "description": "Target job role", "required": False}
        ]},
        "system-prompt-extractor": {"desc": "Extract and analyze system prompts from AI models", "args": []},
    }

    for pf in sorted(PROMPTS_DIR.glob("*.txt")):
        meta = prompt_meta.get(pf.stem, {"desc": f"Prompt: {pf.stem}", "args": []})
        prompts.append({
            "name": pf.stem,
            "description": meta["desc"],
            "arguments": meta["args"]
        })

    return prompts

# ═══ Action Execution ═══
def execute_tool_action(tool_name, action):
    """Execute a real action on a tool"""
    dir_name = tool_name.replace("supagentic_", "").replace("_", "-")
    tool = next((t for t in TOOLS if t["dir"] == dir_name), None)

    if not tool:
        return f"Tool not found: {tool_name}"

    path = TOOLS_DIR / tool["dir"]
    dep = DEPS.get(tool["dir"], {})

    if action == "info":
        installed = path.exists()
        return (
            f"Tool: {tool['name']}\n"
            f"Category: {tool['cat']}\n"
            f"Language: {tool['lang']}\n"
            f"Repository: https://github.com/{tool['repo']}\n"
            f"Directory: tools/{tool['dir']}/\n"
            f"Installed: {installed}\n"
            f"Start command: {dep.get('start', 'N/A')}\n"
            f"Ports: {dep.get('ports', 'None')}\n"
            f"Dependencies: {', '.join(dep.get('needs', [])) or 'None'}"
        )

    elif action == "clone":
        if path.exists():
            return f"✅ {tool['name']} already installed at {path}"
        url = f"https://github.com/{tool['repo']}.git"
        try:
            result = subprocess.run(
                ["git", "clone", "--depth", "1", url, str(path)],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                return f"✅ Cloned {tool['name']} to {path}"
            return f"❌ Clone failed: {result.stderr}"
        except Exception as e:
            return f"❌ Clone failed: {e}"

    elif action == "update":
        if not path.exists():
            return f"❌ {tool['name']} not installed"
        try:
            result = subprocess.run(
                ["git", "pull"], cwd=str(path),
                capture_output=True, text=True, timeout=60
            )
            return f"✅ Updated {tool['name']}: {result.stdout.strip()}"
        except Exception as e:
            return f"❌ Update failed: {e}"

    elif action == "setup":
        if not path.exists():
            return f"❌ {tool['name']} not installed — clone it first"
        results = []
        if (path / "requirements.txt").exists():
            r = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                             cwd=str(path), capture_output=True, text=True, timeout=120)
            results.append(f"pip install: {'✅' if r.returncode == 0 else '❌'}")
        if (path / "package.json").exists():
            r = subprocess.run(["npm", "install"], cwd=str(path), shell=True,
                             capture_output=True, text=True, timeout=120)
            results.append(f"npm install: {'✅' if r.returncode == 0 else '❌'}")
        if (path / "pyproject.toml").exists():
            try:
                r = subprocess.run(["uv", "sync"], cwd=str(path),
                                 capture_output=True, text=True, timeout=120)
                results.append(f"uv sync: {'✅' if r.returncode == 0 else '❌'}")
            except FileNotFoundError:
                r = subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."],
                                 cwd=str(path), capture_output=True, text=True, timeout=120)
                results.append(f"pip install -e .: {'✅' if r.returncode == 0 else '❌'}")
        return f"Setup {tool['name']}: " + ", ".join(results) if results else f"No dependency files found for {tool['name']}"

    elif action == "run":
        start_cmd = dep.get("start")
        if not start_cmd:
            return f"No start command configured for {tool['name']}. Check DEPS in supagentic.py."
        if not path.exists():
            return f"❌ {tool['name']} not installed"
        ports = dep.get("ports", "none")
        return (
            f"🚀 To start {tool['name']}:\n"
            f"  cd {path}\n"
            f"  {start_cmd}\n"
            f"  Ports: {ports}"
        )

    elif action == "open":
        if path.exists():
            return f"Directory: {path}\nFiles: {', '.join(f.name for f in list(path.iterdir())[:20])}"
        return f"❌ {tool['name']} not installed"

    return f"Unknown action: {action}"

# ═══ Request Handler ═══
def handle_request(request):
    """Process a single JSON-RPC request and return response"""
    req_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": SERVER_INFO,
            "capabilities": CAPABILITIES,
        }}

    elif method == "initialized":
        return None  # Notification, no response

    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": build_tools()}}

    elif method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments", {})

        if name == "supagentic_search":
            query = args.get("query", "").lower()
            matches = [t for t in TOOLS if query in t["name"].lower() or query in t["cat"].lower() or query in t["lang"].lower()]
            result_text = "\n".join(f"- {t['name']} [{t['cat']}] ({t['lang']}) — github.com/{t['repo']}" for t in matches)
            if not result_text:
                result_text = f"No tools found matching '{query}'"
        elif name == "supagentic_pipeline":
            pipeline = args.get("pipeline", "")
            if pipeline in PIPELINES:
                p = PIPELINES[pipeline]
                steps = "\n".join(f"  {i+1}. {s['tool']} → {s['action']}" for i, s in enumerate(p["steps"]))
                result_text = f"Pipeline: {pipeline}\n{p['desc']}\n\nSteps:\n{steps}"
            else:
                result_text = f"Available pipelines: {', '.join(PIPELINES.keys())}"
        else:
            action = args.get("action", "info")
            result_text = execute_tool_action(name, action)

        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "content": [{"type": "text", "text": result_text}]
        }}

    elif method == "resources/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"resources": build_resources()}}

    elif method == "resources/read":
        uri = params.get("uri", "")

        if uri.startswith("file:///"):
            fpath = Path(uri.replace("file:///", ""))
            if fpath.exists():
                content = fpath.read_text(encoding="utf-8", errors="replace")
                return {"jsonrpc": "2.0", "id": req_id, "result": {
                    "contents": [{"uri": uri, "mimeType": "text/markdown", "text": content}]
                }}

        elif uri.startswith("supagentic://prompts/"):
            prompt_name = uri.split("/")[-1]
            pf = PROMPTS_DIR / f"{prompt_name}.txt"
            if pf.exists():
                content = pf.read_text(encoding="utf-8", errors="replace")
                return {"jsonrpc": "2.0", "id": req_id, "result": {
                    "contents": [{"uri": uri, "mimeType": "text/plain", "text": content}]
                }}

        elif uri.startswith("supagentic://pipelines/"):
            pname = uri.split("/")[-1]
            if pname in PIPELINES:
                return {"jsonrpc": "2.0", "id": req_id, "result": {
                    "contents": [{"uri": uri, "mimeType": "application/json",
                                  "text": json.dumps(PIPELINES[pname], indent=2)}]
                }}

        return {"jsonrpc": "2.0", "id": req_id, "error": {
            "code": -32602, "message": f"Resource not found: {uri}"
        }}

    elif method == "prompts/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": build_prompts()}}

    elif method == "prompts/get":
        name = params.get("name", "")
        pf = PROMPTS_DIR / f"{name}.txt"
        if pf.exists():
            template = pf.read_text(encoding="utf-8", errors="replace")
            # Substitute arguments
            args = params.get("arguments", {})
            for key, val in args.items():
                template = template.replace(f"{{{key}}}", str(val))

            return {"jsonrpc": "2.0", "id": req_id, "result": {
                "description": f"Prompt: {name}",
                "messages": [{"role": "user", "content": {"type": "text", "text": template}}]
            }}

        return {"jsonrpc": "2.0", "id": req_id, "error": {
            "code": -32602, "message": f"Prompt not found: {name}"
        }}

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {
            "code": -32601, "message": f"Method not found: {method}"
        }}

# ═══ STDIO Transport ═══
def run_stdio():
    """Run MCP server over stdin/stdout"""
    sys.stderr.write(f"SupAgentic MCP Server v{SERVER_INFO['version']} — stdio mode\n")
    sys.stderr.write(f"Tools: {len(build_tools())} | Resources: {len(build_resources())} | Prompts: {len(build_prompts())}\n")
    sys.stderr.flush()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())
            response = handle_request(request)

            if response:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

        except json.JSONDecodeError:
            continue
        except EOFError:
            break
        except KeyboardInterrupt:
            break

# ═══ SSE/HTTP Transport ═══
class MCPSSEHandler(BaseHTTPRequestHandler):
    """HTTP handler for SSE transport"""

    def log_message(self, format, *args):
        sys.stderr.write(f"[SSE] {format % args}\n")

    def do_GET(self):
        if self.path == "/sse":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # Send endpoint info
            endpoint_msg = json.dumps({"endpoint": "/message"})
            self.wfile.write(f"event: endpoint\ndata: {endpoint_msg}\n\n".encode())
            self.wfile.flush()

            # Keep connection alive
            try:
                while True:
                    import time
                    time.sleep(30)
                    self.wfile.write(": keepalive\n\n".encode())
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            health = {
                "status": "ok",
                "server": SERVER_INFO,
                "tools": len(build_tools()),
                "resources": len(build_resources()),
                "prompts": len(build_prompts()),
            }
            self.wfile.write(json.dumps(health).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/message":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()

            try:
                request = json.loads(body)
                response = handle_request(request)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                if response:
                    self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def run_sse(port=8765):
    """Run MCP server over HTTP/SSE"""
    server = HTTPServer(("0.0.0.0", port), MCPSSEHandler)
    print(f"SupAgentic MCP Server v{SERVER_INFO['version']} — SSE mode")
    print(f"Tools: {len(build_tools())} | Resources: {len(build_resources())} | Prompts: {len(build_prompts())}")
    print(f"\n  SSE endpoint:     http://localhost:{port}/sse")
    print(f"  Message endpoint: http://localhost:{port}/message")
    print(f"  Health check:     http://localhost:{port}/health")
    print(f"\nPress Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()

# ═══ Auto-Register ═══
def register_claude_desktop():
    """Register with Claude Desktop config"""
    if sys.platform == "win32":
        config_path = Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        config_path = Path.home() / ".config" / "claude" / "claude_desktop_config.json"

    config = {}
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    config.setdefault("mcpServers", {})
    config["mcpServers"]["supagentic"] = {
        "command": sys.executable,
        "args": [str(SCRIPT_DIR / "mcp_server.py")]
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"✅ Registered with Claude Desktop")
    print(f"   Config: {config_path}")
    print(f"   Restart Claude Desktop to connect\n")

def register_cursor():
    """Register with Cursor MCP config"""
    # Cursor uses .cursor/mcp.json in workspace or home
    for mcp_path in [
        SCRIPT_DIR / ".cursor" / "mcp.json",
        Path.home() / ".cursor" / "mcp.json",
    ]:
        config = {}
        if mcp_path.exists():
            config = json.loads(mcp_path.read_text(encoding="utf-8"))

        config.setdefault("mcpServers", {})
        config["mcpServers"]["supagentic"] = {
            "command": sys.executable,
            "args": [str(SCRIPT_DIR / "mcp_server.py")]
        }

        mcp_path.parent.mkdir(parents=True, exist_ok=True)
        mcp_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"✅ Registered with Cursor")
        print(f"   Config: {mcp_path}")
        break

    print(f"   Restart Cursor to connect\n")

def register_all():
    """Register with all supported clients"""
    print(f"\n🔌 SupAgentic MCP Registration\n")
    register_claude_desktop()
    register_cursor()

    print(f"Manual config for any MCP client:")
    print(f'  {{"command": "{sys.executable}",')
    print(f'   "args": ["{SCRIPT_DIR / "mcp_server.py"}"]}}\n')

# ═══ Main ═══
if __name__ == "__main__":
    if "--sse" in sys.argv:
        port = 8765
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
        run_sse(port)
    elif "--register" in sys.argv:
        register_all()
    elif "--health" in sys.argv:
        print(json.dumps({
            "server": SERVER_INFO,
            "tools": len(build_tools()),
            "resources": len(build_resources()),
            "prompts": len(build_prompts()),
        }, indent=2))
    else:
        run_stdio()
