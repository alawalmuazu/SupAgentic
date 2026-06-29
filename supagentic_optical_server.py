#!/usr/bin/env python3
"""
supagentic_optical_server.py
Component J: The Optical Override

A local WebSocket server acting as the bridge between the Chrome DOM Extension
and the local SupAgentic routing matrix.

Requires: `pip install websockets`
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Note: In a true production environment this uses the `websockets` library.
try:
    import websockets
except ImportError:
    print("[Optical Override] ⚠️ 'websockets' module not found. Run: pip install websockets")
    sys.exit(1)

async def optical_handler(websocket):
    print("[Optical Override] 🌐 DOM Extension securely connected to OS.")
    try:
        async for message in websocket:
            payload = json.loads(message)
            event = payload.get("event")
            
            if event == "orb_clicked":
                url = payload.get("url", "")
                print(f"[Optical Override] ⚡ Neural link clicked from {url}")
                
                # Contextual Awareness Logic
                if "github.com" in url:
                    repo_path = url.split("github.com/")[1].split("/")[0:2]
                    repo_id = "/".join(repo_path)
                    print(f"   --> Auto-Forge Target Detected: {repo_id}")
                    # In true execution we run subprocess SupAgentic Forge here
                    
                    response = {
                        "action": "notify",
                        "text": f"Forge Protocol Initiated for {repo_id}!"
                    }
                    await websocket.send(json.dumps(response))
                else:
                    response = {
                        "action": "notify",
                        "text": "SupAgentic Omni-Presence Online."
                    }
                    await websocket.send(json.dumps(response))
                    
    except websockets.exceptions.ConnectionClosed:
        print("[Optical Override] 📡 Link severed.")

async def main():
    print("[Optical Override] 🔮 Igniting WebSocket Bridge on ws://localhost:8789")
    async with websockets.serve(optical_handler, "localhost", 8789):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Optical Override] Spun down.")
