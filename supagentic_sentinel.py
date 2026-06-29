#!/usr/bin/env python3
"""
supagentic_sentinel.py

Component F: The Pre-Cognitive Sentinel.
An autonomous background daemon that watches the Phantom Context memory bus.
If it detects friction (e.g., a stack trace in the clipboard), it intercepts it,
queries an LLM for a solution, and immediately spawns an Ephemeral Glass UI
sliding in the answer before the user even asks.
"""

import sys
import os
import time
import json
import subprocess
from pathlib import Path

# Tracks what has already been solved to prevent infinite loops
PROCESSED_SIGNATURES = set()

def tail_phantom_cache():
    cache_file = Path(__file__).parent / "phantom_cache.json"
    if not cache_file.exists():
        return None
        
    try:
        data = json.loads(cache_file.read_text(encoding='utf-8'))
        return data.get("clipboard_current", "")
    except Exception:
        return None

def is_friction_point(text):
    if not text:
        return False
    # Simple rule engine: look for stack traces
    triggers = ["Traceback (most recent call last):", "panic:", "Uncaught TypeError", "Exception:"]
    for t in triggers:
        if t in text:
            return True
    return False

def proactive_solve(stack_trace):
    print("[Sentinel] 👁️ Friction Point detected! Proactively diagnosing...")
    # Attempt to use OpenAI to solve it
    sys_prompt = "You are the SupAgentic Sentinel. The user just encountered this error. Provide a concise, highly accurate reason for the crash and the exact code snippet to fix it. Format as JSON with 'Error', 'Reason', and 'Fix'."
    try:
        import openai
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("No API Key")
        
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": stack_trace[-2000:]} # last 2k chars
            ],
            temperature=0
        )
        content = resp.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        solution_payload = json.loads(content)
    except Exception as e:
        solution_payload = {
            "Error": "LLM Offline or Key Missing",
            "Reason": str(e),
            "Fix": "Please configure OPENAI_API_KEY environment variable to enable Sentinel AI diagnostics."
        }
    
    # Send directly to the Glass UI Engine
    print("[Sentinel] 🔮 Pushing Ephemeral UI to user's optical array...")
    ui_script = Path(__file__).parent / "supagentic_ui.py"
    
    import tempfile
    fd, tmp_path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(json.dumps(solution_payload, indent=2))
        
    subprocess.Popen([sys.executable, str(ui_script), tmp_path])

def run_sentinel():
    print("⬡ Sentinel Initialized. Passively observing Phantom telemetry...")
    
    while True:
        clip_text = tail_phantom_cache()
        if clip_text and clip_text not in PROCESSED_SIGNATURES:
            if is_friction_point(clip_text):
                proactive_solve(clip_text)
                PROCESSED_SIGNATURES.add(clip_text)
        
        time.sleep(3) # Polling interval

if __name__ == "__main__":
    try:
        run_sentinel()
    except KeyboardInterrupt:
        print("\n[Sentinel] Going to sleep.")
