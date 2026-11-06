## ZPP - Mesh Monitor

zpp_id: mesh_monitor_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-26

---

```python
#!/usr/bin/env python3
import os
import time
import json
import csv

LEDGER_PATH = "/Users/<LOCAL_USER>/vault/ledger/ledger.jsonl"
METRICS_PATH = "/Users/<LOCAL_USER>/vault/metrics/metrics.csv"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_ledger():
    if not os.path.exists(LEDGER_PATH) or os.path.getsize(LEDGER_PATH) == 0:
        return 0, "N/A", []
    
    block_count = 0
    last_block_hash = "N/A"
    recent_transactions = []
    
    try:
        with open(LEDGER_PATH, 'r') as f:
            lines = f.readlines()
            block_count = len(lines)
            if lines:
                last_entry = json.loads(lines[-1].strip())
                last_block_hash = last_entry.get("state_hash", "UNKNOWN")
                
                # Grab last 5 entries for the live feed
                for line in lines[-5:]:
                    entry = json.loads(line.strip())
                    recent_transactions.append(entry)
    except Exception:
        pass
        
    return block_count, last_block_hash, recent_transactions

def parse_metrics():
    if not os.path.exists(METRICS_PATH) or os.path.getsize(METRICS_PATH) == 0:
        return 0.0, {}
    
    total_latency = 0.0
    count = 0
    node_activity = {}
    
    try:
        with open(METRICS_PATH, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:
                    _, source, latency, _ = row
                    lat_val = float(latency)
                    total_latency += lat_val
                    count += 1
                    node_activity[source] = node_activity.get(source, 0) + 1
    except Exception:
        pass
        
    avg_latency = round(total_latency / count, 2) if count > 0 else 0.0
    return avg_latency, node_activity

def main():
    while True:
        clear_terminal()
        block_count, last_hash, recent_txs = parse_ledger()
        avg_latency, node_activity = parse_metrics()
        
        print("=============================================================")
        print("⚡ ZPP-ALPHA MAINNET: LIVE COHERENCE MESH MONITOR ⚡")
        print("=============================================================")
        print(f"📈 Network State:   ACTIVE            │ 📦 Total Block Height: {block_count}")
        print(f"⏱️  Avg Latency:     {avg_latency} ms         │ 🔒 Tip Hash:           {last_hash[:12]}")
        print("─────────────────────────────────────────────────────────────")
        print("📡 ASYMMETRICAL NODE ACTIVITY PROFILE:")
        
        # Hardcoded map of our 6 deployed nodes to print status checks
        all_nodes = ["NODE_A", "NODE_B", "NODE_C", "NODE_D", "NODE_E", "NODE_F"]
        for node in all_nodes:
            hits = node_activity.get(node, 0)
            if node in ["NODE_D", "NODE_F"]:
                role = "EDGE GATEWAY"
            elif node == "NODE_E":
                role = "OBSERVER    "
            else:
                role = "CONSENSUS   "
            print(f"  ● {node} ({role}) ──> Transacted Packets processed: {hits}")
            
        print("─────────────────────────────────────────────────────────────")
        print("📦 RECENT LEDGER BLOCK ENTRIES (LIVE INGRESS FEED):")
        
        if not recent_txs:
            print("  [Waiting for incoming signals...]")
        else:
            for tx in reversed(recent_txs):
                idx = tx.get("index", 0)
                tx_type = tx.get("type", "SINGLE_TX")
                ts = tx.get("timestamp", 0)
                
                if tx_type == "BATCH_BLOCK":
                    print(f"  [#{idx:03d}] 📦 BATCH PACKED — Size: {tx.get('block_size')} txs | Hash: {tx.get('state_hash')}")
                else:
                    payload = tx.get("payload", {})
                    speaker = payload.get("speaker", "UNKNOWN")
                    txt = payload.get("text", "")[:45]
                    print(f"  [#{idx:03d}] 💾 {speaker}: \"{txt}...\"")
                    
        print("=============================================================")
        print("Press Ctrl+C to terminate monitor session.")
        time.sleep(1.5) # Refresh buffer tick rate

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitor paused. System remains operational.")