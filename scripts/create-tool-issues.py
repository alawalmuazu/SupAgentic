#!/usr/bin/env python3
"""
Auto-generate GitHub Issues for each tool in the SupAgentic registry.

Usage:
    python scripts/create-tool-issues.py [--dry-run]

Requires:
    pip install PyGithub
    GITHUB_TOKEN environment variable
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from supagentic import TOOLS

def main():
    dry_run = "--dry-run" in sys.argv

    if not dry_run:
        try:
            from github import Github
        except ImportError:
            print("Install PyGithub: pip install PyGithub")
            sys.exit(1)

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("Set GITHUB_TOKEN environment variable")
            sys.exit(1)

        g = Github(token)
        repo = g.get_repo("alawalmuazu/SupAgentic")

    labels = {
        "Agents": "agent",
        "Security": "security",
        "Coding": "coding",
        "RAG": "rag",
        "Memory": "memory",
        "Swarm": "swarm",
        "Simulation": "simulation",
        "Local LLM": "local-llm",
        "Training": "training",
        "Media": "media",
        "Automation": "automation",
        "Browser": "browser",
        "Serving": "serving",
        "Data": "data",
        "Modding": "modding",
    }

    for t in TOOLS:
        if t["cat"] == "Tutorials":
            continue

        title = f"[Tool] {t['name']} — Setup & Integration Guide"
        body = f"""## {t['name']}

**Category**: {t['cat']}
**Language**: {t['lang']}
**Repository**: https://github.com/{t['repo']}
**Directory**: `tools/{t['dir']}/`

### Tasks
- [ ] Verify installation & local setup
- [ ] Document startup command in DEPS map
- [ ] Test with `supagentic run {t['dir']}`
- [ ] Add integration example to INTEGRATIONS.md
- [ ] Write quick-start snippet for README

### Labels
`tool`, `{labels.get(t['cat'], 'other')}`, `documentation`
"""

        if dry_run:
            print(f"[DRY RUN] Would create: {title}")
        else:
            try:
                issue = repo.create_issue(
                    title=title,
                    body=body,
                    labels=["tool", labels.get(t["cat"], "other"), "documentation"]
                )
                print(f"✅ Created #{issue.number}: {title}")
            except Exception as e:
                print(f"❌ Failed: {title} — {e}")

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Done! {len([t for t in TOOLS if t['cat'] != 'Tutorials'])} issues.")

if __name__ == "__main__":
    main()
