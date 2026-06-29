#!/usr/bin/env python3
"""
supagentic_fusion.py

Component G: Genetic Tool Fusion
Unlike 'Compose' which acts as a generic IO pipe, Fusion acts as a Meta-Compiler.
It reads the Abstract Syntax (or core logic structure) of two independent scripts,
injects them into an LLM Compiler, and outputs a permanently fused, hybrid tool script.

Usage: 
    python supagentic_fusion.py <path_to_tool_A> <path_to_tool_B> "hybridized task specification"
"""

import sys
import os
import re
import json
from pathlib import Path
import subprocess

def extract_core_logic(tool_path: Path):
    """Naively extract what looks like the entry script for a tool"""
    content = ""
    # Look for .py, .js, .ts. Prefer main, index, run, app, cli
    targets = ["main.py", "cli.py", "app.py", "index.js", "run.py"]
    if tool_path.is_file():
        return tool_path.read_text(encoding='utf-8')
    
    if tool_path.is_dir():
        for target in targets:
            tp = tool_path / target
            if tp.exists():
                return tp.read_text(encoding='utf-8')
        # fallback to the biggest python file
        py_files = list(tool_path.glob("*.py"))
        if py_files:
            py_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
            return py_files[0].read_text(encoding='utf-8')
            
    return None

def synthesize_hybrid(tool_a_name, source_a, tool_b_name, source_b, goal):
    print(f"[Fusion] 🧬 Initiating genome sequencing for {tool_a_name} & {tool_b_name}...")
    sys_prompt = f"""You are the SupAgentic Fusion Compiler.
Your task is to take the source code of two different tools and COMBINE them into a single standalone Python script that performs the user's hybrid goal.
Do not just pipe data. Extract the actual core functions from both sources and weave their logic together natively if possible, or wrap them tightly using Python subprocess bindings.
Output ONLY the combined, raw Python code. Do not wrap in markdown ```. No explanations."""
    
    user_prompt = f"""
--- TOOL A ({tool_a_name}) ---
{source_a[:3000]}...

--- TOOL B ({tool_b_name}) ---
{source_b[:3000]}...

--- HYBRIDIZATION GOAL ---
{goal}

Generate the final fused script.
"""
    try:
        import openai
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("No API Key")
        
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        content = resp.choices[0].message.content.strip()
        if content.startswith("```python"):
            content = content[9:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return content
    except Exception as e:
        print(f"[Fusion] ⚠️ LLM Compiler Error: {e}")
        return None

def forge_fusion(path_a, path_b, goal):
    pA, pB = Path(path_a), Path(path_b)
    
    source_a = extract_core_logic(pA)
    source_b = extract_core_logic(pB)
    
    if not source_a or not source_b:
        print("[Fusion] ❌ Failed to extract core logic sequences from targets.")
        return
        
    hybrid_code = synthesize_hybrid(pA.name, source_a, pB.name, source_b, goal)
    if not hybrid_code:
        return
        
    hybrid_name = f"{pA.name}_x_{pB.name}_hybrid"
    out_dir = Path.cwd() / "tools" / hybrid_name
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = out_dir / "main.py"
    out_file.write_text(hybrid_code.strip() + "\n", encoding='utf-8')
    
    print(f"[Fusion] 🎉 Synthesis complete! Hybrid binary stored at {out_file}")
    
    # Let's inject it into the SupAgentic Registry automatically just like Forge
    entry = f'    {{"name": "{hybrid_name.replace("_", " ").title()}", "dir": "tools/{hybrid_name}", "cat": "Hybrids", "repo": "local/hybrid", "lang": "Python"}},\n'
    sup_file = Path.cwd() / "supagentic.py"
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
    print(f"[Fusion] ✅ Hybrid registered in master CLI. Run via: python supagentic.py run {hybrid_name}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python supagentic_fusion.py <tool_A_path> <tool_B_path> \"goal\"")
        sys.exit(1)
        
    forge_fusion(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
