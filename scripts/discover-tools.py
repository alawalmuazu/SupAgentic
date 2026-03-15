#!/usr/bin/env python3
"""
SupAgentic Tool Discovery Script
Scans GitHub for trending AI/ML repos that aren't already in SupAgentic.
Outputs new tool candidates to /tmp/new_tools.json
"""

import json
import os
import subprocess
import requests
from datetime import datetime, timedelta

# --- Config ---
SEARCH_QUERIES = [
    "topic:llm topic:agents stars:>1000 pushed:>{since}",
    "topic:rag topic:ai stars:>500 pushed:>{since}",
    "topic:fine-tuning topic:llm stars:>1000 pushed:>{since}",
    "topic:ai-coding-assistant stars:>500 pushed:>{since}",
    "topic:text-to-speech topic:ai stars:>500 pushed:>{since}",
    "topic:generative-ai stars:>2000 pushed:>{since}",
    "topic:machine-learning topic:deep-learning stars:>5000 pushed:>{since}",
    "topic:langchain stars:>1000 pushed:>{since}",
    "topic:autonomous-agents stars:>500 pushed:>{since}",
    "topic:ai-tools stars:>1000 pushed:>{since}",
    "topic:computer-vision topic:ai stars:>2000 pushed:>{since}",
    "topic:nlp topic:transformers stars:>2000 pushed:>{since}",
]

# Tools already in SupAgentic (by repo owner/name patterns)
EXISTING_TOOLS = [
    "agency-agents", "crewai", "autogen", "langgraph", "dify",
    "promptfoo", "impeccable", "aider", "open-interpreter",
    "fabric", "tabby", "claude-engineer", "llama-index", "ragflow",
    "anything-llm", "openviking", "mirofish", "ollama", "unsloth",
    "nanochat", "llama-factory", "heretic", "comfyui", "kokoro",
    "ai-engineering-hub", "ai-project-gallery", "500-ai",
    "end-to-end-generative", "genai-projects", "100-ai",
    "awesome-deep-learning", "awesome-machine-learning",
    "awesome-project-ideas", "awesome-generative-ai",
]

CATEGORIES = {
    "agents": ["agent", "multi-agent", "autonomous", "crew", "swarm"],
    "rag": ["rag", "retrieval", "vector", "embedding", "knowledge"],
    "coding": ["code", "copilot", "coding", "ide", "developer"],
    "training": ["fine-tune", "training", "lora", "qlora", "rlhf"],
    "local-llm": ["ollama", "llama", "local", "inference", "gguf"],
    "media": ["image", "video", "audio", "tts", "diffusion", "comfy"],
    "security": ["security", "red-team", "prompt-injection", "eval"],
    "tutorials": ["tutorial", "awesome", "learn", "course", "project"],
}


def is_already_tracked(repo_name: str) -> bool:
    """Check if a repo is already in SupAgentic."""
    name_lower = repo_name.lower()
    return any(existing in name_lower for existing in EXISTING_TOOLS)


def detect_category(repo: dict) -> str:
    """Auto-detect category from repo topics and description."""
    text = f"{repo.get('description', '')} {' '.join(repo.get('topics', []))}".lower()
    scores = {}
    for cat, keywords in CATEGORIES.items():
        scores[cat] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "tutorials"


def search_github(query: str, token: str) -> list:
    """Search GitHub API for repos matching query."""
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("items", [])
    except Exception as e:
        print(f"  Error: {e}")
        return []


def main():
    token = os.environ.get("GH_TOKEN", "")
    since = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    print(f"🔍 SupAgentic Tool Discovery — scanning since {since}")
    print(f"   Existing tools: {len(EXISTING_TOOLS)}")
    print()

    candidates = {}
    
    for query_template in SEARCH_QUERIES:
        query = query_template.format(since=since)
        print(f"  Searching: {query[:60]}...")
        results = search_github(query, token)
        
        for repo in results:
            full_name = repo["full_name"]
            name = repo["name"]
            
            if is_already_tracked(name):
                continue
            if full_name in candidates:
                continue
            if repo["archived"] or repo["fork"]:
                continue
                
            category = detect_category(repo)
            candidates[full_name] = {
                "name": name,
                "full_name": full_name,
                "url": repo["html_url"],
                "description": repo.get("description", "No description"),
                "stars": repo["stargazers_count"],
                "language": repo.get("language", "Unknown"),
                "topics": repo.get("topics", []),
                "category": category,
                "last_push": repo.get("pushed_at", ""),
                "created": repo.get("created_at", ""),
            }

    # Sort by stars
    sorted_candidates = sorted(candidates.values(), key=lambda x: x["stars"], reverse=True)
    
    # Take top 10
    top = sorted_candidates[:10]
    
    print(f"\n{'='*60}")
    print(f"🎯 Found {len(sorted_candidates)} new candidates, top {len(top)}:")
    print(f"{'='*60}\n")
    
    for i, tool in enumerate(top, 1):
        print(f"  {i}. {tool['name']} ({tool['stars']:,}⭐) — {tool['category']}")
        print(f"     {tool['url']}")
        print(f"     {tool['description'][:80]}")
        print()

    if top:
        with open("/tmp/new_tools.json", "w") as f:
            json.dump(top, f, indent=2)
        print(f"💾 Saved {len(top)} candidates to /tmp/new_tools.json")
    else:
        print("No new tools found this week.")


if __name__ == "__main__":
    main()
