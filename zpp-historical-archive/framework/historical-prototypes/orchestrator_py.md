
> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: orchestrator_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

```python

#!/usr/bin/env python3
"""
orchestrator.py - File Reader, Search, and Legacy Operations
"""

import json
import subprocess
import os
import glob
import re
from datetime import datetime, timezone

VAULT_ROOT = "/Users/<LOCAL_USER>/vault"
SANDBOX = "/Users/<LOCAL_USER>/vault/sandbox"
LOG_FILE = f"{SANDBOX}/conversation_log.txt"

os.makedirs(SANDBOX, exist_ok=True)


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

def ask_deepseek(prompt, context=""):
    url = "http://localhost:11434/v1/chat/completions"
    
    user_content = f"{context}\n\nUser: {prompt}\nAssistant:" if context else f"User: {prompt}\nAssistant:"
    
    payload = {
        "model": "deepseek-r1:7b",
        "messages": [
            {"role": "user", "content": user_content}
        ],
        "stream": False,
        "temperature": 0.4
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json'}
        )
        response = json.loads(urllib.request.urlopen(req).read())
        return response['choices'][0]['message']['content']
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
# BLOCK HEIGHT & SYSTEM EVENTS
# ────────────────────────────────────────────────────────────

def get_block_height():
    """Returns the current block height from the ledger or a fallback counter."""
    try:
        ledger_path = "/Users/<LOCAL_USER>/vault/ledger/ledger.jsonl"
        if not os.path.exists(ledger_path):
            return 0
        with open(ledger_path, 'r') as f:
            last_line = None
            for line in f:
                if line.strip():
                    last_line = line
            if last_line:
                entry = json.loads(last_line)
                return entry.get('index', 0)
        return 0
    except Exception:
        try:
            counter_file = "/Users/<LOCAL_USER>/vault/node/state/block_counter.txt"
            os.makedirs(os.path.dirname(counter_file), exist_ok=True)
            if os.path.exists(counter_file):
                with open(counter_file, 'r') as f:
                    count = int(f.read().strip())
                count += 1
            else:
                count = 1
            with open(counter_file, 'w') as f:
                f.write(str(count))
            return count
        except Exception:
            return 0

def log_system_event(event: str, details: dict = None):
    """Log a major system event to ledger.jsonl."""
    try:
        import time
        import json
        import os

        ledger_path = "/Users/<LOCAL_USER>/vault/ledger/ledger.jsonl"
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)

        entry = {
            "timestamp": int(time.time()),
            "event": event,
            "type": "SYSTEM_EVENT",
            "details": details or {}
        }

        with open(ledger_path, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"⚠️ [SYSTEM EVENT LOG ERROR]: {e}")


# ────────────────────────────────────────────────────────────
# RUNTIME PROTECTION BOUNDARY
# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🛰️ Orchestrator Standalone CLI Ready")
    print(f"📁 Vault: {VAULT_ROOT}")
    print("💡 Commands: 'read /path/to/file.md' | 'search <keyword>' | just chat")
    print(" Type 'exit' to quit\n")

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
        
        response = ask_deepseek(user, context)
        print(f"\n {response}\n")
        log_conversation(user, response)
```