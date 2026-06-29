#!/usr/bin/env python3
"""
supagentic_ui.py

Component E: Ephemeral Glass UIs
Turns raw terminal stdout (JSON/markdown) into a transient, beautiful, 
glassmorphic browser interface instantly.

Usage:
    python supagentic_ui.py "raw text or json to render"
"""

import sys
import json
import webbrowser
import threading
import http.server
import socketserver
import tempfile
import os
import time
from pathlib import Path

# -- Premium Glassmorphism HTML Template --
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SupAgentic | Ephemeral UI</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&family=Fira+Code&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --primary: #3b82f6;
            --secondary: #8b5cf6;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }

        body {
            margin: 0;
            padding: 3rem;
            min-height: 100vh;
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            display: flex;
            justify-content: center;
        }

        .glass-container {
            width: 100%;
            max-width: 1200px;
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            padding: 3rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--glass-border);
            padding-bottom: 1.5rem;
        }

        .title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .badge {
            background: rgba(59, 130, 246, 0.2);
            color: var(--primary);
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.3s ease, background 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .card-key {
            font-size: 0.85rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .card-value {
            font-size: 1.25rem;
            font-weight: 500;
            word-break: break-word;
        }

        pre {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 1.5rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.95rem;
            overflow-x: auto;
            color: #e2e8f0;
            line-height: 1.5;
        }
    </style>
</head>
<body>

<div class="glass-container">
    <div class="header">
        <h1 class="title">Execution Artifact</h1>
        <div class="badge">Ephemeral Interface</div>
    </div>
    
    <div id="content">
        <!-- INJECT_CONTENT_HERE -->
    </div>
</div>

<script>
    const rawData = `RAW_DATA_INJECTION`;
    const contentDiv = document.getElementById('content');

    try {
        // Try parsing as JSON first
        const json = JSON.parse(rawData);
        
        if (typeof json === 'object' && json !== null) {
            let html = '<div class="cards-grid">';
            for (const [key, value] of Object.entries(json)) {
                let displayValue = value;
                if (typeof value === 'object') {
                    displayValue = `<pre>${JSON.stringify(value, null, 2)}</pre>`;
                }
                html += `
                    <div class="card">
                        <div class="card-key">${key}</div>
                        <div class="card-value">${displayValue}</div>
                    </div>
                `;
            }
            html += '</div>';
            contentDiv.innerHTML = html;
        } else {
            throw new Error("Not an object");
        }
    } catch (e) {
        // Fallback to raw text/markdown
        contentDiv.innerHTML = `<pre>${rawData}</pre>`;
    }
</script>

</body>
</html>
"""

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Shhh

def launch_ephemeral_ui(payload: str):
    print("[Glass UI] 🖥️ Intercepted output. Constructing ephemeral renderer...")
    
    # Escape payload for template injection
    safe_payload = payload.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    rendered_html = HTML_TEMPLATE.replace("RAW_DATA_INJECTION", safe_payload)
    
    # Create temp directory and file
    temp_dir = tempfile.mkdtemp()
    temp_file = Path(temp_dir) / "index.html"
    temp_file.write_text(rendered_html, encoding='utf-8')
    
    # Find active port
    port = 8787
    Handler = QuietHandler
    
    # Serve the file
    os.chdir(temp_dir)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"[Glass UI] ✨ Rendering at http://localhost:{port}")
        webbrowser.open(f"http://localhost:{port}")
        
        # Keep alive for 15 seconds then shutdown automatically (Ephemeral)
        def kill_server():
            time.sleep(15)
            httpd.shutdown()
            print("[Glass UI] 🌌 Interface dissolved.")
            
        threading.Thread(target=kill_server, daemon=True).start()
        httpd.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Load from file if it is an existing file, otherwise treat it as raw text
        target = sys.argv[1]
        try:
            if Path(target).exists():
                payload = Path(target).read_text(encoding='utf-8')
            else:
                payload = target
        except Exception:
            payload = target
            
        launch_ephemeral_ui(payload)
