#!/usr/bin/env python3
"""
supagentic_phantom_daemon.py

The Phantom Context Engine for SupAgentic.
Runs as a background daemon monitoring:
1. Windows Clipboard (Text)
2. Windows PowerShell History

Maintains a rolling JSON cache so when you run `supagentic run <tool>`,
the tool implicitly knows exactly what you were just doing/looking at.

Usage:
    python supagentic_phantom_daemon.py
"""

import time
import json
import os
import sys
import subprocess
from pathlib import Path

try:
    from harness import ContextManager, PermissionGate, SubagentOrchestrator
except ImportError:
    pass # Will be fully integrated in the upcoming refactor phase

# Try to import pyperclip, install if missing
try:
    import pyperclip
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "-q"])
    import pyperclip

# Configuration
SCRIPT_DIR = Path(__file__).parent
PHANTOM_CACHE = SCRIPT_DIR / "phantom_cache.json"

# Resolve PowerShell History File
PS_HISTORY = Path(os.environ.get('APPDATA', '')) / "Microsoft" / "Windows" / "PowerShell" / "PSReadLine" / "ConsoleHost_history.txt"

MAX_CONTEXT_ITEMS = 50

def load_cache():
    if PHANTOM_CACHE.exists():
        try:
            with open(PHANTOM_CACHE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"clipboard": [], "history": []}
    return {"clipboard": [], "history": []}

def save_cache(cache):
    with open(PHANTOM_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)

def add_to_buffer(buffer_list, item):
    if not buffer_list or buffer_list[-1]['content'] != item:
        buffer_list.append({
            "timestamp": time.time(),
            "content": item
        })
        if len(buffer_list) > MAX_CONTEXT_ITEMS:
            buffer_list.pop(0)
        return True
    return False

def tail_file(filepath, lines=10):
    """Returns the last N non-empty lines of a file securely."""
    if not filepath.exists():
        return []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().splitlines()
            return [line for line in content if line.strip()][-lines:]
    except Exception:
        return []

def run_daemon():
    print("👻 Phantom Context Engine matching...")
    print(f"Monitoring PS History: {PS_HISTORY.exists()}")
    cache = load_cache()
    last_clipboard = pyperclip.paste()
    
    # Pre-pad the clipboard cache to prevent duplicate startup writes
    add_to_buffer(cache['clipboard'], last_clipboard)
    
    last_history_state = tail_file(PS_HISTORY)
    if last_history_state:
        add_to_buffer(cache['history'], last_history_state[-1])
        
    save_cache(cache)

    try:
        while True:
            updated = False
            
            # Check Clipboard
            current_clipboard = pyperclip.paste()
            if current_clipboard != last_clipboard and current_clipboard.strip():
                # Avoid saving massive base64 images or gigabyte strings
                if len(current_clipboard) < 10000:
                    add_to_buffer(cache['clipboard'], current_clipboard)
                    last_clipboard = current_clipboard
                    updated = True
            
            # Check PS History
            current_history_state = tail_file(PS_HISTORY, 1)
            if current_history_state and current_history_state != last_history_state:
                cmd = current_history_state[0]
                # Ignore supagentic commands to prevent recursive feedback loops
                if not cmd.startswith("supagentic") and not cmd.startswith("python supagentic"):
                    add_to_buffer(cache['history'], cmd)
                    last_history_state = current_history_state
                    updated = True
                    
            if updated:
                save_cache(cache)
                
            time.sleep(1.5)
            
    except KeyboardInterrupt:
        print("\n👻 Phantom Context Engine powering down.")

if __name__ == "__main__":
    run_daemon()
