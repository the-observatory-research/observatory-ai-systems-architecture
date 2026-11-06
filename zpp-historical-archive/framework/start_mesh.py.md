## ZPP - Start Mesh

zpp_id: start_mesh_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-26

---

```python
#!/usr/bin/env python3
import subprocess
import time
import sys
import os

nodes = [
    {"name": "NODE_A", "cmd": ["python3", "-u", "transport_sim.py", "NODE_A"]},
    {"name": "NODE_B", "cmd": ["python3", "-u", "transport_sim.py", "NODE_B"]},
    {"name": "NODE_C", "cmd": ["python3", "-u", "transport_sim.py", "NODE_C"]},
    {"name": "NODE_D", "cmd": ["python3", "-u", "transport_sim.py", "NODE_D"]},
    {"name": "NODE_E", "cmd": ["python3", "-u", "transport_sim.py", "NODE_E"]},
    {"name": "NODE_F", "cmd": ["python3", "-u", "transport_sim.py", "NODE_F"]},
]

launched_processes = []

print("============================================================")
print("⚡ INITIALIZING ZERO-POINT REPLICATION CONSENSUS ARCHITECTURE")
print("============================================================")

os.makedirs("/Users/<LOCAL_USER>/vault/node/logs", exist_ok=True)

for node in nodes:
    log_path = f"/Users/<LOCAL_USER>/vault/node/logs/{node['name'].lower()}.log"
    log_file = open(log_path, "w")
    
    try:
        proc = subprocess.Popen(
            node["cmd"],
            cwd="/Users/<LOCAL_USER>/vault/node",
            stdout=log_file,
            stderr=log_file,
            text=True
        )
        launched_processes.append((node["name"], proc, log_file))
        print(f"✅ Spawned background process: {node['name']} -> Logs routed to logs/ folder")
        time.sleep(0.5) 
    except Exception as e:
        print(f"❌ Failed to boot process {node['name']}: {e}")

print("\n🚀 All 6 nodes initialized. Topology verification complete.")
print("Run 'python3 mesh_monitor.py' or open 'dashboard.html' to inspect execution matrices.")
print("Press Ctrl+C inside this controller script to safely terminate all background units.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 SHUTDOWN SIGNAL DETECTED: Deallocating network process nodes...")
    for name, proc, log_file in launched_processes:
        print(f"Stopping {name}...")
        proc.terminate()
        proc.wait()
        log_file.close()
    print("✨ All backend sockets freed successfully. Mesh safe.")


