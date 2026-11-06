## ZPP - Verify Ledger

zpp_id: verify_ledger_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-07-01

---

```python

#!/usr/bin/env python3
"""
verify_ledger.py — ZPP Ledger Integrity Verifier (Supports SINGLE_TX & BATCH_BLOCK)
"""

import json
import os

LEDGER_PATH = "/Users/<LOCAL_USER>/vault/ledger/ledger.jsonl"

def verify_ledger():
    if not os.path.exists(LEDGER_PATH):
        print("❌ Ledger file not found.")
        return False

    with open(LEDGER_PATH, 'r') as f:
        lines = f.readlines()

    if not lines:
        print("⚠️ Ledger is empty.")
        return True

    prev_hash = None

    for idx, line in enumerate(lines, start=1):
        try:
            block = json.loads(line.strip())
        except json.JSONDecodeError:
            print(f"❌ Block {idx}: Invalid JSON")
            return False

        # Check block type
        block_type = block.get("type", "SINGLE_TX")  # Default to SINGLE_TX if not present

        # Required fields based on type
        if block_type == "BATCH_BLOCK":
            required = ["index", "timestamp", "type", "block_size", "transactions", "state_hash"]
        else:
            required = ["index", "timestamp", "origin_node", "payload", "state_hash"]

        for field in required:
            if field not in block:
                print(f"❌ Block {idx}: Missing required field '{field}' (type: {block_type})")
                return False

        if block["index"] != idx:
            print(f"❌ Block {idx}: Index mismatch (expected {idx}, got {block['index']})")
            return False

        # Chain continuity (if prev_hash exists)
        if "prev_hash" in block:
            if block["prev_hash"] != prev_hash:
                print(f"❌ Block {idx}: Prev hash mismatch")
                return False
            print(f"✅ Block {idx}: prev_hash matches")
        elif idx > 1:
            print(f"⚠️ Block {idx}: No prev_hash field — skipping chain check")

        prev_hash = block["state_hash"]

    print(f"✅ Ledger verified. {len(lines)} blocks structurally intact.")
    return True

if __name__ == "__main__":
    verify_ledger()
```

