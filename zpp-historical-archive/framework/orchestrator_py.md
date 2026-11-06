## ZPP - Orchestrator 

zpp_id: orchestrator_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-26

---

```python
#!/usr/bin/env python3
"""
orchestrator.py - Memory, Search, and Direct File Reader
Reads entire files - no truncation | Fully Integrated with SQLite Coherence Lattice
"""

import json
import subprocess
import urllib.request
import os
import glob
import re
import sqlite3
from datetime import datetime, timezone

VAULT_ROOT = "/Users/<LOCAL_USER>/vault"
SANDBOX = "/Users/<LOCAL_USER>/vault/sandbox"
LOG_FILE = f"{SANDBOX}/conversation_log.txt"
DB_PATH = "/Users/<LOCAL_USER>/vault/node/lattice_memory.db"

os.makedirs(SANDBOX, exist_ok=True)

# ────────────────────────────────────────────────────────────
# COHERENT LATTICE: SQLITE INTEGRATION
# ────────────────────────────────────────────────────────────

def init_db():
    """Initializes the SQLite database and creates the schema if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Core Chat Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                anchor_id TEXT NOT NULL,
                speaker TEXT NOT NULL,
                payload_score REAL,
                message_text TEXT NOT NULL
            )
        """)
        # NEW: Telemetry Pulse Table (Keeps background noise isolated)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_pulses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                anchor_id TEXT NOT NULL,
                pulse_type TEXT NOT NULL,
                payload_score REAL,
                prompt_text TEXT NOT NULL,
                thought_text TEXT NOT NULL
            )
        """)
        # NEW: Key-Value Store for Persistent System Metadata Flags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()

# ---> KV HELPER FUNCTIONS <---

def set_metadata_kv(key: str, value: str):
    """Saves or updates a persistent configuration flag in the database."""
    init_db()  # Run safety check
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO system_metadata (key, value)
            VALUES (?, ?)
        """, (key, value))
        conn.commit()

def get_metadata_kv(key: str) -> str:
    """Retrieves a persistent configuration flag from the database."""
    init_db()  # Run safety check
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT value FROM system_metadata WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None
        except sqlite3.OperationalError:
            return None

def save_telemetry_pulse(anchor_id, pulse_type, payload_score, prompt_text, thought_text):
    """Saves background pulses to an isolated table away from core chat history."""
    init_db()  # Quick safety check
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO telemetry_pulses (timestamp, anchor_id, pulse_type, payload_score, prompt_text, thought_text)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now(timezone.utc).isoformat(), anchor_id, pulse_type, payload_score, prompt_text, thought_text))
        conn.commit()

def save_exchange(anchor_id, speaker, payload_score, message_text):
    """Appends a single turn of the conversation into the permanent lattice database
    AND writes a summarized entry to the ledger for telemetry.
    """
    # 1. Write to SQLite (memory/continuity)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversation_history (timestamp, anchor_id, speaker, payload_score, message_text)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now(timezone.utc).isoformat(), anchor_id, speaker, payload_score, message_text))
        conn.commit()

    # 2. Write to ledger.jsonl (telemetry/dashboard)
    try:
        import hashlib
        import time
        
        ledger_path = "/Users/<LOCAL_USER>/vault/ledger/ledger.jsonl"
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        
        # Determine next index
        index = 1
        if os.path.exists(ledger_path) and os.path.getsize(ledger_path) > 0:
            with open(ledger_path, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            if entry.get('index', 0) >= index:
                                index = entry['index'] + 1
                        except:
                            pass
        
        # Truncate long messages for the ledger
        text_preview = message_text[:200] + "..." if len(message_text) > 200 else message_text
        
        ledger_entry = {
            "index": index,
            "timestamp": int(time.time()),
            "type": "SINGLE_TX",
            "origin_node": speaker,
            "payload": {
                "speaker": speaker,
                "text": text_preview,
                "tax": payload_score if isinstance(payload_score, (int, float)) else 0.0,
                "state": "DETERMINISTIC_LOCK",
                "timestamp": int(time.time())
            },
            "state_hash": f"sig_ed25519_{hashlib.md5(str(anchor_id).encode()).hexdigest()[:4]}"
        }
        
        with open(ledger_path, 'a') as f:
            f.write(json.dumps(ledger_entry) + "\n")
    except Exception as e:
        print(f"⚠️ [LEDGER WRITE ERROR]: {e}")

def fetch_full_history():
    """Retrieves all past exchanges in chronological order to seed the pipeline's memory."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT anchor_id, speaker, message_text FROM conversation_history 
            ORDER BY id ASC
        """)
        return cursor.fetchall()

def get_primed_context():
    """Compiles the absolute history into a structural system context for pipe_horizon.py."""
    init_db()  # Self-heal check to ensure table exists
    raw_history = fetch_full_history()
    
    if not raw_history:
        return []
        
    formatted_messages = []
    for anchor_id, speaker, text in raw_history:
        role = "user" if speaker == "user" else "assistant"
        formatted_messages.append({"role": role, "content": text})
        
    return formatted_messages

# ────────────────────────────────────────────────────────────
# LEGACY FLAT-FILE MEMORY & SEARCH OPERATIONS
# ────────────────────────────────────────────────────────────

def log_conversation(user_input, response):
    with open(LOG_FILE, "a") as f:
        ts = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        f.write(f"\n[{ts}] USER: {user_input}\n")
        f.write(f"[{ts}] ASSISTANT: {response}\n")

def get_memory(query):
    if not os.path.exists(LOG_FILE):
        return ""
    with open(LOG_FILE, "r") as f:
        content = f.read()
    keywords = query.lower().split()
    lines = []
    for line in content.split("\n"):
        if any(k in line.lower() for k in keywords):
            lines.append(line)
    return "\n".join(lines[-10:])[:2000]

def read_file(filepath):
    """Read entire file - no character limit"""
    try:
        if not os.path.exists(filepath):
            return f"File not found: {filepath}"
        with open(filepath, 'r') as f:
            content = f.read()
            if not content:
                return "File is empty"
            return content
    except Exception as e:
        return f"Error reading file: {e}"

def search_files(keyword):
    try:
        subprocess.run(["python3", "/Users/<LOCAL_USER>/vault/node/text_searcher.py", keyword], 
                       capture_output=True, text=True)
        files = glob.glob(f"{SANDBOX}/text-search-*.md")
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            with open(files[0], 'r') as f:
                return f.read()[:3000]
    except:
        pass
    return ""

def ask_llama(prompt, context=""):
    url = "http://localhost:11434/api/generate"
    full = f"{context}\n\nUser: {prompt}\nAssistant:" if context else f"User: {prompt}\nAssistant:"
    payload = {"model": "llama3:8b-instruct-q4_0", "prompt": full, "stream": False}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        return json.loads(urllib.request.urlopen(req).read())['response']
    except Exception as e:
        return f"Error: {e}"

def is_read_command(user_input):
    """Only treat as read command if it looks like a file path, allowing spaces"""
    patterns = [
        r'read\s+([\/\w\.\-\s]+\.md)',
        r'read\s+([\/\w\.\-\s]+\.txt)',
        r'read\s+([\/\w\.\-\s]+\.json)',
        r'read\s+(\/[\w\/\.\-\s]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def is_search_command(user_input):
    return re.search(r'(search|find|look for|query)', user_input.lower()) is not None

def extract_keyword(user_input):
    words = user_input.lower().split()
    for i, w in enumerate(words):
        if w in ['search', 'find', 'look', 'query'] and i+1 < len(words):
            return words[i+1].strip('"\'?!.,')
    return None

# ────────────────────────────────────────────────────────────
# RUNTIME PROTECTION BOUNDARY
# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🛰️ Orchestrator Standalone CLI Ready")
    print(f"📁 Vault: {VAULT_ROOT}")
    print("💡 Commands: 'read /path/to/file.md' | 'search <keyword>' | just chat")
    print("🦙 Type 'exit' to quit\n")

    init_db()

    while True:
        user = input("👤 You: ").strip()
        if user.lower() in ['exit', 'quit']:
            break
        if not user:
            continue
        
        context = ""
        
        filepath = is_read_command(user)
        if filepath:
            print(f"📖 Reading: {filepath}")
            content = read_file(filepath)
            if "Error" not in content and "not found" not in content:
                print(f"✅ Read {len(content)} chars")
                context = content
            else:
                print(f"⚠️ {content}")
        
        elif is_search_command(user):
            kw = extract_keyword(user)
            if kw:
                print(f"🔍 Searching for '{kw}'...")
                context = search_files(kw)
                print("📁 Done")
        
        memory = get_memory(user)
        if memory:
            context = f"{context}\n\nPAST:\n{memory}" if context else f"PAST:\n{memory}"
        
        response = ask_llama(user, context)
        print(f"\n🦙 {response}\n")
        log_conversation(user, response)