#!/usr/bin/env python3
"""
Creates GitHub Issues for newly discovered AI tools.
Reads candidates from /tmp/new_tools.json (produced by discover-tools.py)
"""

import json
import os
import subprocess


def create_issue(tool: dict, token: str):
    """Create a GitHub issue suggesting a new tool."""
    title = f"🆕 New Tool Suggestion: {tool['name']} ({tool['stars']:,}⭐)"
    
    body = f"""## New AI Tool Discovered

| Property | Value |
|----------|-------|
| **Name** | [{tool['name']}]({tool['url']}) |
| **Stars** | {tool['stars']:,} ⭐ |
| **Language** | {tool['language']} |
| **Category** | {tool['category']} |
| **Topics** | {', '.join(tool.get('topics', [])[:8])} |
| **Last Push** | {tool.get('last_push', 'N/A')[:10]} |

### Description
{tool['description']}

### To Add
```bash
# Clone into tools/
git clone --depth 1 {tool['url']}.git tools/{tool['name'].lower()}

# Then update index.html and README.md with the new tool card
```

---
*Auto-discovered by SupAgentic Tool Scanner*
"""
    
    labels = ["enhancement", "new-tool", tool["category"]]
    
    # Use gh CLI to create issue
    cmd = [
        "gh", "issue", "create",
        "--repo", "alawalmuazu/SupAgentic",
        "--title", title,
        "--body", body,
        "--label", ",".join(labels),
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✅ Created issue: {tool['name']}")
            print(f"     {result.stdout.strip()}")
        else:
            # Labels might not exist, retry without labels
            cmd_no_labels = cmd[:-2]
            result2 = subprocess.run(cmd_no_labels, capture_output=True, text=True, timeout=30)
            if result2.returncode == 0:
                print(f"  ✅ Created issue (no labels): {tool['name']}")
            else:
                print(f"  ❌ Failed: {tool['name']} — {result2.stderr[:100]}")
    except Exception as e:
        print(f"  ❌ Error: {tool['name']} — {e}")


def main():
    token = os.environ.get("GH_TOKEN", "")
    
    try:
        with open("/tmp/new_tools.json", "r") as f:
            tools = json.load(f)
    except FileNotFoundError:
        print("No new tools file found. Run discover-tools.py first.")
        return
    
    print(f"📋 Creating issues for {len(tools)} new tool suggestions...\n")
    
    for tool in tools:
        create_issue(tool, token)
    
    print(f"\n✅ Done! Check https://github.com/alawalmuazu/SupAgentic/issues")


if __name__ == "__main__":
    main()
