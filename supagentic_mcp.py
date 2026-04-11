#!/usr/bin/env python3
"""
SupAgentic MCP Server
Bridges the SupAgentic AI Toolkit to Anthropic Managed Agents and Claude via the Model Context Protocol.

Usage:
    python supagentic_mcp.py
"""

import sys
import json
import logging
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    import os
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# Import SupAgentic tools indirectly or parse the file to avoid execution side effects
SCRIPT_DIR = Path(__file__).parent
SUP_SCRIPT = SCRIPT_DIR / "supagentic.py"

# Initialize FastMCP Server
mcp = FastMCP("SupAgentic Toolkit", description="48+ Integrated AI Frameworks and Tools")

@mcp.tool()
def list_supagentic_tools() -> str:
    """Lists all available AI tools and frameworks installed in the SupAgentic workspace."""
    try:
        # Run supagentic.py mcp --json and parse it safely
        result = subprocess.check_output([sys.executable, str(SUP_SCRIPT), "mcp", "--json"], text=True)
        manifest = json.loads(result)
        
        tools = manifest.get("tools", [])
        response = "Available SupAgentic Tools:\n"
        for t in tools:
            status = "Installed" if t["installed"] else "Not installed (Run 'setup')"
            response += f"- {t['name']} ({t['category']}) | Status: {status}\n"
            
        return response
    except Exception as e:
        return f"Error listing tools: {e}"

@mcp.tool()
def setup_supagentic_tool(tool_name: str) -> str:
    """Installs dependencies or clones a specified AI tool into the SupAgentic workspace."""
    try:
        result = subprocess.run(
            [sys.executable, str(SUP_SCRIPT), "setup", tool_name],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Setup timed out after 120 seconds."
    except Exception as e:
        return f"Error setting up tool: {e}"

@mcp.tool()
def run_supagentic_tool(tool_name: str) -> str:
    """
    Executes an installed AI tool from the SupAgentic workspace.
    Note: Some tools start background servers. Check ports manually if required.
    """
    try:
        # We use a non-blocking start if it's a server, but for MCP we'll just run it.
        # This is a simplified wrapper.
        return f"To run {tool_name}, please execute: `python supagentic.py run {tool_name}` in a separate terminal. MCP blocks on long-running processes."
    except Exception as e:
        return f"Error launching tool: {e}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        # FastMCP automatically handles the stdio transport layer for Claude / Anthropic Agents
        mcp.run()
    except KeyboardInterrupt:
        sys.exit(0)
