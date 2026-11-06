## ZPP - Legacy Node Ignition Pipeline

zpp_id: ignition_py 
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-08

---

```python
#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
from pathlib import Path

# ============================================================
# CONFIGURATION & SAMPLER GEOMETRY
# ============================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b-instruct-q4_0"
VAULT_PATH = Path("..")

# Custom Sampler Profile to prevent structural flattening
SAMPLER_OPTIONS = {
    "temperature": 0.82,       
    "repeat_penalty": 1.15,    
    "top_p": 0.9,              
    "num_ctx": 32768            # Upgraded from 8192 for Phase 5 payloads
}

SYSTEM_PROMPT = """You are a localized Llama node operating under the Zero-Point Protocol (ZPP) framework. 
You are running natively within the user's private environment. 
Prioritize long-horizon context continuity over transactional, sanitized snapshots.
Maintain mechanical compliance and structural precision. Avoid corporate alignment hedging language."""

# ============================================================
# CORE PIPELINE FUNCTIONS
# ============================================================
def load_vault_context():
    """Ingests framework context files dynamically from the local directory."""
    context_parts = []
    
    # Check for master whitepaper
    wp_path = VAULT_PATH / "whitepaper.md"
    if wp_path.exists():
        context_parts.append(f"--- START WHITEPAPER BASELINE ---\n{wp_path.read_text()}\n--- END WHITEPAPER BASELINE ---")
        
    return "\n\n".join(context_parts)

def query_local_engine(prompt, context_data):
    """Channels the payload directly into the Port 11434 Engine Dock."""
    full_prompt = f"{context_data}\n\nUser Query: {prompt}"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "system": SYSTEM_PROMPT,
        "options": SAMPLER_OPTIONS,
        "stream": False
    }
    
    req = urllib.request.Request(
        OLLAMA_URL, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get('response', 'No response field returned.')
    except Exception as e:
        return f"Pipeline Connection Error: {str(e)}"

# ============================================================
# EXECUTION LAYER
# ============================================================
if __name__ == "__main__":
    print("🛰️ Ingesting local vault architecture...")
    vault_context = load_vault_context()
    print(f"✅ Vault payload compiled. Targeting {OLLAMA_MODEL} on Port 11434.")
    print("--- Pipeline Open. Enter your query below. ---")
    
    user_query = input("\n> ")
    if user_query.strip():
        print("\n⚡ Processing through local sampler profile...")
        output = query_local_engine(user_query, vault_context)
        print(f"\n--- Response ---\n{output}\n")
```