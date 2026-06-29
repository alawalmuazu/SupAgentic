#!/usr/bin/env python3
"""
supagentic_matrix.py

Component H: 3D Swarm Matrix
Spawns the local web server to serve the God-Mode Swarm Matrix UI.

Usage: 
    python supagentic_matrix.py
"""

import sys
import os
import webbrowser
import http.server
import socketserver
from pathlib import Path

class MatrixHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Always serve the matrix file if path is /
        if self.path == '/':
            self.path = '/supagentic_matrix.html'
        return super().do_GET()

def launch_matrix():
    print("[Swarm Matrix] 🌌 Initializing 3D God-Mode Holodeck...")
    
    port = 8788
    # Ensure we serve from the dir containing the html
    os.chdir(Path(__file__).parent)
    
    try:
        with socketserver.TCPServer(("", port), MatrixHandler) as httpd:
            print(f"[Swarm Matrix] ✨ Matrix online at http://localhost:{port}")
            webbrowser.open(f"http://localhost:{port}")
            httpd.serve_forever()
    except OSError as e:
        print(f"[Swarm Matrix] ❌ Port {port} in use, or cannot bind: {e}")

if __name__ == "__main__":
    launch_matrix()
