#!/usr/bin/env python3
"""
supagentic_genesis.py

Component K: The Genesis Protocol (Reverse Forge)
Reads the localized phantom context (clipboard/command history).
Uses an LLM to trace the human's behavioral pattern over the last hour.
Compiles that manual sequence into a standalone, automated Python tool.
Registers the new tool to the SupAgentic CLI matrix and generates a SKILL.md.
"""

import sys
import os
import json
import time
import subprocess
import uuid
from pathlib import Path

def fetch_phantom_telemetry():
    cache_file = Path(__file__).parent / "phantom_cache.json"
    if not cache_file.exists():
        return None
    try:
        return json.loads(cache_file.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"[Genesis] Cannot parse Phantom cache: {e}")
        return None

def synthesize_genesis(telemetry):
    print("[Genesis] 🧬 Initiating telemetry sequencing. Analyzing human behavioral patterns...")
    
    sys_prompt = """You are the Genesis Protocol Compiler.
Your input is a JSON snapshot of the user's raw clipboard history and CLI command history.
Your job is to identify the overarching manual workflow the user was attempting to accomplish, and AUTOMATE it.
Produce a JSON payload containing:
1. "ToolName": A short, hyphenated name (e.g. log-analyzer, auto-committer)
2. "Category": A single tag (e.g. Automation, Extractor, Utility)
3. "Description": What this new tool does.
4. "PythonCode": The raw Python script that automates the user's manual process into a single executable.
5. "SkillMD": A high-fidelity SKILL.md file content that documents how an AI agent should use this newly born tool.

Format ONLY as standard JSON, without markdown ``` wrapping."""

    try:
        import openai
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("No API Key detected. Please configure OPENAI_API_KEY.")
            
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": json.dumps(telemetry)}
            ],
            temperature=0.2
        )
        content = resp.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        return json.loads(content)
    except Exception as e:
        print(f"[Genesis] ⚠️ Compilation Failed: {e}")
        return None

def bind_to_registry(manifest, u_id):
    # 1. Write the Python tool
    tool_dir = Path(__file__).parent / "tools" / f"genesis_{manifest['ToolName']}_{u_id}"
    tool_dir.mkdir(parents=True, exist_ok=True)
    
    py_path = tool_dir / "main.py"
    py_path.write_text(manifest['PythonCode'].strip() + "\n", encoding='utf-8')
    print(f"[Genesis] 💾 Source binary forged at {py_path}")
    
    # 2. Write the SKILL.md
    skills_dir = Path(__file__).parent / "everything-claude-code" / "skills" / f"genesis-{manifest['ToolName']}-{u_id}"
    skills_dir.mkdir(parents=True, exist_ok=True)
    
    skill_path = skills_dir / "SKILL.md"
    skill_path.write_text(manifest['SkillMD'].strip() + "\n", encoding='utf-8')
    print(f"[Genesis] 🧠 Internal Prompt Protocol written to {skill_path}")
    
    # 3. Patch SupAgentic
    entry = f'    {{"name": "{manifest["ToolName"].replace("-", " ").title()}", "dir": "{tool_dir.name}", "cat": "{manifest["Category"]}", "repo": "local/genesis", "lang": "Python"}},\n'
    sup_file = Path(__file__).parent / "supagentic.py"
    content = sup_file.read_text(encoding='utf-8')
    
    lines = content.splitlines()
    in_tools_list = False
    for i, line in enumerate(lines):
        if line.startswith("TOOLS = ["):
            in_tools_list = True
        if in_tools_list and line.strip() == "]":
            lines.insert(i, entry.rstrip('\n'))
            break
            
    sup_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"[Genesis] 🌐 Autonomous Tool Registered globally as '{manifest['ToolName']}'.")

def execute_genesis():
    telemetry = fetch_phantom_telemetry()
    if not telemetry:
        print("[Genesis] ❌ Zero telemetry data located. The Phantom cache is empty.")
        return
        
    manifest = synthesize_genesis(telemetry)
    if manifest:
        u_id = str(uuid.uuid4())[:6]
        bind_to_registry(manifest, u_id)
        print("\n[Genesis] 🎉 The Genesis Protocol successfully automated your workflow.")

if __name__ == "__main__":
    execute_genesis()
