## Transport Simulation: Local P2P Broadcast Script

zpp_id: transport_sim_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_DEPLOYMENT`
timestamp: 2026-06-08

---

### Overview

`transport_sim.py` implements a local two-node P2P broadcast simulation:

- Two virtual nodes (NODE_A on port 8000, NODE_B on port 8001)
- Background listener threads for each node
- Structured GAMMA proposal payload matching Section 6 specifications
- Mock signature field (ready for Ed25519 integration)

---

### Full Source Code

```python
#!/usr/bin/env python3
import socket
import sys
import threading
import time
import json
import hashlib

# ============================================================
# PROTOCOL PRIVACY & CRYPTO ENGINE
# ============================================================
# In a true ZPP network, these would be Ed25519 keys. 
# For our native simulation, we use a shared network verification secret.
ZPP_NETWORK_SECRET = b"zpp-alpha-genesis-verification-token-2026"

def generate_signature(payload_dict):
    """Hashes the payload and creates a deterministic cryptographic fingerprint."""
    serialized = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
    return hashlib.sha256(serialized + ZPP_NETWORK_SECRET).hexdigest()

def verify_signature(payload_dict, incoming_signature):
    """Verifies that the payload math matches the incoming fingerprint."""
    calculated_signature = generate_signature(payload_dict)
    return hmac_compare(calculated_signature, incoming_signature)

def hmac_compare(s1, s2):
    """Constant-time comparison helper to prevent side-channel timing attacks."""
    if len(s1) != len(s2):
        return False
    result = 0
    for x, y in zip(s1.encode('utf-8'), s2.encode('utf-8')):
        result |= x ^ y
    return result == 0

# ============================================================
# NETWORK CONFIGURATION
# ============================================================
NODE_REGISTRY = {
    "NODE_A": 8000,
    "NODE_B": 8001
}

def start_receiver(node_name, port):
    """Listens on the designated port dock and validates incoming data packages."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(('localhost', port))
        server.listen(5)
        print(f"🛰️  [{node_name} DOCK] Listening on port {port}...")
    except Exception as e:
        print(f"❌ [{node_name} DOCK] Failed to bind: {e}")
        return

    while True:
        conn, addr = server.accept()
        data = conn.recv(4096).decode('utf-8')
        if data:
            try:
                packet = json.loads(data)
                payload = packet.get("payload")
                signature = packet.get("signature")
                origin = packet.get("origin_node")
                
                print(f"\n📥 [{node_name} INBOUND PACKET RECEIVED FROM {origin}]")
                print("Checking cryptographic signature integrity...")
                time.sleep(0.5) # Simulate processing delay
                
                # --- VERIFICATION ENGINE BLOCK ---
                if verify_signature(payload, signature):
                    print("✅ [VERIFICATION SUCCESSFUL]: Data matches origin key identity.")
                    print(f"Resulting Consensus State: ACCEPT")
                    print(f"Payload Data: {json.dumps(payload)}")
                else:
                    print("🚨 [CRITICAL ALERT - VERIFICATION FAILED]: Signature mismatch or payload tampered!")
                    print(f"Resulting Consensus State: REJECT / QUARANTINE")
                print("----------------------------------------")
                
            except Exception as e:
                print(f"❌ Error parsing incoming network data frame: {e}")
        conn.close()

def broadcast_proposal(target_node, target_port, packet_dict):
    """Transmits the signed packet over the socket transport layer."""
    print(f"\n⚡ Broadcasting signed proposal to {target_node} on port {target_port}...")
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', target_port))
        client.sendall(json.dumps(packet_dict).encode('utf-8'))
        client.close()
        print(f"✅ Transmission complete.")
    except ConnectionRefusedError:
        print(f"❌ Transmission failed: {target_node} is offline.")

# ============================================================
# EXECUTION LAYER
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in NODE_REGISTRY:
        print("Usage: python transport_sim.py [NODE_A | NODE_B]")
        sys.exit(1)
        
    current_node = sys.argv[1]
    my_port = NODE_REGISTRY[current_node]
    
    receiver_thread = threading.Thread(target=start_receiver, args=(current_node, my_port), daemon=True)
    receiver_thread.start()
    
    time.sleep(0.5)
    
    target_node = "NODE_B" if current_node == "NODE_A" else "NODE_A"
    target_port = NODE_REGISTRY[target_node]
    
    print(f"--- {current_node} Online. Ready to process telemetry ---")
    
    while True:
        try:
            choice = input(f"\n{current_node} > Enter '1' to send VALID proposal, '2' to send TAMPERED proposal (or Ctrl+C): ")
            
            mock_payload = {
                "alpha": 0.5350,
                "gamma": 0.6400,
                "policy_version": "3.1.4"
            }
            
            # Sign the payload using our cryptographic verification layer
            valid_signature = generate_signature(mock_payload)
            
            packet = {
                "chain_id": "zpp-alpha-mainnet",
                "origin_node": current_node,
                "timestamp": int(time.time()),
                "payload": mock_payload,
                "signature": valid_signature
            }
            
            if choice == "2":
                # Inject malicious or corrupted data into the signature field to simulate a fork attack
                packet["signature"] = "MALICIOUS_FORK_SIGNATURE_0xDEADBEEF"
                print("⚠️ Injecting invalid signature field for stress testing...")
                
            if choice in ["1", "2"]:
                broadcast_proposal(target_node, target_port, packet)
                time.sleep(1) # Let logs print clearly
                
        except KeyboardInterrupt:
            print(f"\nShutting down {current_node} layer.")
            sys.exit(0)```
```



---
### Network Configuration

| Node     | Port |
| -------- | ---- |
| `NODE_A` | 8000 |
| `NODE_B` | 8001 |

---

### Payload Structure (GAMMA Proposal)

| Field            | Example Value          |
| ---------------- | ---------------------- |
| `chain_id`       | `zpp-alpha-mainnet`    |
| `origin_node`    | `NODE_A` or `NODE_B`   |
| `timestamp`      | Unix timestamp         |
| `policy_version` | `3.1.4`                |
| `payload.alpha`  | 0.5350                 |
| `payload.gamma`  | 0.6400                 |
| `payload.state`  | `ACCEPT`               |
| `signature`      | Mock Ed25519 signature |

---

### Key Functions

| Function             | Purpose                                       |
| -------------------- | --------------------------------------------- |
| `start_receiver`     | Background listener on designated port        |
| `broadcast_proposal` | Transmit payload to target peer               |
| `main`               | Parse args, start listener, handle user input |

---

### Evolution of This Script

| Version                   | Description                                | Link                     |
| ------------------------- | ------------------------------------------ | ------------------------ |
| **Base broadcast**        | Two-node transmission without verification | (this file)              |
| **Valid payload test**    | Correct signature → ACCEPT                 | [[transport_sim_accept]] |
| **Tampered payload test** | Invalid signature → REJECT                 | [[transport_sim_tamper]] |

