#!/usr/bin/env python3
"""
memory_bus.py

Component C: The Unified Memory Tissue.
A frictionless SQLite backend leveraging FTS5 (Full Text Search) to act as a 
shared dataset/subconscious for the entire SupAgentic AI ecosystem.

Agents can write findings here, and other agents can search memory chronologically 
or via contextual full-text correlation.
"""

import sqlite3
import time
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "supagentic_memory.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Create the virtual table for full-text search
    c.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS memory USING fts5(
            tool_name,
            action_type,
            payload,
            timestamp UNINDEXED
        )
    ''')
    conn.commit()
    conn.close()

def store_memory(tool_name: str, action_type: str, payload_data):
    """
    Commit a new memory to the unified tissue.
    `payload_data` can be a string or a dict (which will be JSON stringified).
    """
    if isinstance(payload_data, dict) or isinstance(payload_data, list):
        payload_data = json.dumps(payload_data, ensure_ascii=False)
        
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (tool_name, action_type, payload, timestamp) VALUES (?, ?, ?, ?)",
        (tool_name, action_type, str(payload_data), int(time.time()))
    )
    conn.commit()
    conn.close()

def search_memory(query: str, limit: int = 5):
    """
    Recall memories matching the full-text search query.
    """
    conn = get_connection()
    c = conn.cursor()
    # FTS5 MATCH query
    sql = '''
        SELECT tool_name, action_type, payload, timestamp, rank 
        FROM memory 
        WHERE memory MATCH ? 
        ORDER BY rank 
        LIMIT ?
    '''
    try:
        # FTS queries treat tokens specially. A simple phrase search is wrapped in quotes.
        safe_query = f'"{query}"'
        c.execute(sql, (safe_query, limit))
        results = [dict(row) for row in c.fetchall()]
        return results
    except Exception as e:
        print(f"[MemoryBus] Warning: FTS query failed: {e}")
        return []
    finally:
        conn.close()
        
def get_recent_memory(limit: int = 10):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT tool_name, action_type, payload, timestamp
        FROM memory 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    return results

if __name__ == "__main__":
    import sys
    init_db()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "search" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            res = search_memory(query)
            print(json.dumps(res, indent=2))
        elif cmd == "recent":
            res = get_recent_memory()
            print(json.dumps(res, indent=2))
        else:
            print("Usage: python memory_bus.py [search <query> | recent]")
    else:
        print("✅ Unified Memory Tissue Initialized (FTS5 SQLite).")
