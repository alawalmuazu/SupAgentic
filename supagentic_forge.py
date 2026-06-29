#!/usr/bin/env python3
"""
supagentic_forge.py

Component D: Recursive Self-Expansion.
Allows SupAgentic to autonomously build itself. When asked for a tool it lacks,
it searches GitHub, clones the ideal repo, uses an LLM to generate the registry 
JSON, and permanently patches supagentic.py so the CLI instantly inherits it.

Usage: 
    python supagentic_forge.py "youtube transcript downloader"
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path

def forge_tool(query):
    print(f"\n[Forge] 🔨 Initiating autonomous build sequence for: '{query}'")
    
    # 1. Search GitHub API for the best match
    print("[Forge] Querying global Open-Source registries...")
    search_query = urllib.parse.quote(query)
    search_url = f"https://api.github.com/search/repositories?q={search_query}&sort=stars&order=desc"
    req = urllib.request.Request(search_url, headers={'User-Agent': 'SupAgentic-Forge'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"[Forge] ❌ GitHub API Error: {e}")
        return
        
    if not data.get("items"):
        print("[Forge] ❌ No actionable tools found on the open internet.")
        return
        
    top_repo = data["items"][0]
    repo_url = top_repo["html_url"]
    repo_full_name = top_repo["full_name"]
    repo_name = top_repo["name"]
    desc = top_repo.get("description", "")
    lang = top_repo.get("language", "Unknown")
    
    print(f"[Forge] 👁️ Discovered optimal tool: {repo_full_name} ({top_repo['stargazers_count']}⭐)")
    print(f"[Forge] 📄 Summary: {desc}")
    
    # 2. Clone the tool to local workspace
    tools_dir = Path.cwd()
    clone_path = tools_dir / repo_name
    if not clone_path.exists():
        print(f"[Forge] 📥 Cloning repository logic into SupAgentic framework...")
        subprocess.run(["git", "clone", repo_url, str(clone_path)])
    else:
        print(f"[Forge] ⚡ Repository '{repo_name}' already exists locally.")

    # 3. Categorize Tool via LLM (or robust heuristic fallback)
    print("[Forge] 🧠 Interrogating LLM for toolkit integration metadata...")
    try:
        # We attempt to use the official OpenAI bindings if authenticated
        import openai
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY missing")
            
        client = openai.OpenAI()
        sys_prompt = "You are an AI tool classifier. Given a GitHub repo name, description, and language, return a single JSON object with: 'name' (readable tool name), 'dir' (folder name exactly as given), 'cat' (one of: Agents, Security, Coding, RAG, Memory, Swarm, Simulation, Local LLM, Training, Modding, Media, Tutorials, Automation, Browser, Serving, Data, Math, Robotics, Voice, Science), 'repo' (owner/repo exactly as given), 'lang' (primary language). OUTPUT PURE JSON, DO NOT WRAP IN BACKTICKS."
        user_prompt = f"Repo: {repo_full_name}\nDesc: {desc}\nLang: {lang}\nFolder: {repo_name}"
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        raw_content = resp.choices[0].message.content.strip()
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:-3]
        elif raw_content.startswith("```"):
            raw_content = raw_content[3:-3]
            
        cat_json = json.loads(raw_content)
        category = cat_json.get("cat", "Tools")
    except Exception as e:
        print(f"[Forge] ⚠️ LLM Classification offline ({e}). Generating categorical blueprint heuristically...")
        cat_json = {
            "name": repo_name.replace("-", " ").title(),
            "dir": repo_name,
            "cat": "Agents" if "agent" in desc.lower() else "Automation",
            "repo": repo_full_name,
            "lang": lang if lang else "Unknown"
        }

    entry = f'    {{"name": "{cat_json["name"]}", "dir": "{cat_json["dir"]}", "cat": "{cat_json["cat"]}", "repo": "{cat_json["repo"]}", "lang": "{cat_json["lang"]}"}},'
    print(f"[Forge] 📡 Generated Registration Payload: \n{entry}")
    
    # 4. Synthetically Patch supagentic.py Registry
    sup_file = Path.cwd() / "supagentic.py"
    if not sup_file.exists():
        print(f"[Forge] ❌ CLI root router not found at {sup_file}")
        return
        
    content = sup_file.read_text(encoding='utf-8')
    if f'"dir": "{repo_name}"' in content:
        print("[Forge] ✅ Setup aborted: Tool is already permanently registered.")
        return
        
    lines = content.splitlines()
    in_tools_list = False
    injected = False
    
    for i, line in enumerate(lines):
        if line.startswith("TOOLS = ["):
            in_tools_list = True
            
        if in_tools_list and line.strip() == "]":
            # We reached the end of the TOOLS array. Insert the entry directly above.
            lines.insert(i, entry)
            injected = True
            break
            
    if injected:
        sup_file.write_text('\n'.join(lines), encoding='utf-8')
        print(f"[Forge] 🏆 Breakthrough achieved. '{cat_json['name']}' autonomously forged into the SupAgentic CLI!")
        print(f"[Forge] ⚡ Run it via: python supagentic.py run {cat_json['dir']}")
    else:
        print("[Forge] ❌ Failed to locate the registry array in supagentic.py.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python supagentic_forge.py <problem statement or tool name>")
        sys.exit(1)
    forge_tool(" ".join(sys.argv[1:]))
