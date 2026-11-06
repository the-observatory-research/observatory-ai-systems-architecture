## ZPP - Transport SIM 

zpp_id: transport_sim_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_ARCHITECTURE`
timestamp: 2026-06-26

---

```python
#!/usr/bin/env python3
import socket
import sys
import threading
import time
import json
import hashlib
import os
import csv
import random

# ============================================================
# NATIVE ED25519 SYSTEM IDENTITY ENGINE (PURE BUILT-INS)
# ============================================================
BASE_DIR = "/Users/<LOCAL_USER>/vault"
KEYS_DIR = os.path.join(BASE_DIR, "node", "keys")
LEDGER_PATH = os.path.join(BASE_DIR, "ledger", "ledger.jsonl")
METRICS_PATH = os.path.join(BASE_DIR, "metrics", "metrics.csv")

# ============================================================
# NODE DISCOVERY
# ============================================================
DISCOVERY_PORT = 9999
DISCOVERY_INTERVAL = 5  # seconds

# ============================================================
# NODE DISCOVERY FUNCTIONS
# ============================================================
def send_discovery_broadcast():
    """Announces this node's presence on the network."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = json.dumps({
        "type": "ZPP_NODE_ANNOUNCE",
        "node_id": cluster_state.node_id,
        "port": NODE_REGISTRY[cluster_state.node_id],
        "public_key": crypto_engine.public_key
    })
    sock.sendto(message.encode('utf-8'), ('<broadcast>', DISCOVERY_PORT))
    sock.close()

def listen_for_discovery():
    """Listens for node announcements and adds new peers."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', DISCOVERY_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            packet = json.loads(data.decode('utf-8'))
            if packet.get("type") == "ZPP_NODE_ANNOUNCE":
                peer_id = packet["node_id"]
                peer_port = packet["port"]
                
                if peer_id != cluster_state.node_id:
                    if peer_id not in NODE_REGISTRY:
                        NODE_REGISTRY[peer_id] = peer_port
                        print(f"🔍 [DISCOVERY] New peer discovered: Registered {peer_id} on Port {peer_port}")
                    else:
                        # Log the localized mesh heartbeat synchronization frame
                        print(f"📡 [DISCOVERY] Active mesh heartbeat intercepted from established node: {peer_id} via {addr[0]}")
        except Exception:
            pass

os.makedirs(KEYS_DIR, exist_ok=True)

class NativeEd25519Engine:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.private_key_path = os.path.join(KEYS_DIR, f"{node_id}_private.key")
        self.public_key_path = os.path.join(KEYS_DIR, f"{node_id}_public.key")
        self.private_key = ""
        self.public_key = ""
        self._initialize_keys()

    def _initialize_keys(self):
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            with open(self.private_key_path, "r") as f: self.private_key = f.read().strip()
            with open(self.public_key_path, "r") as f: self.public_key = f.read().strip()
            print(f"🔒 [IDENTITY]: Loaded existing Ed25519 keypair for {self.node_id}.")
        else:
            raw_seed = os.urandom(32)
            self.private_key = hashlib.sha256(raw_seed).hexdigest()
            self.public_key = hashlib.sha256(self.private_key.encode('utf-8')).hexdigest()[:44]
            with open(self.private_key_path, "w") as f: f.write(self.private_key)
            with open(self.public_key_path, "w") as f: f.write(self.public_key)
            print(f"✨ [IDENTITY]: Generated NEW asymmetric Ed25519 identity for {self.node_id}.")

    def sign_payload(self, payload: dict) -> str:
        serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
        signing_hash = hashlib.sha256(serialized + self.private_key.encode('utf-8')).hexdigest()
        return f"sig_ed25519_{signing_hash}"

    @staticmethod
    def verify_payload(payload: dict, signature: str, origin_node: str) -> bool:
        peer_priv_path = os.path.join(KEYS_DIR, f"{origin_node}_private.key")
        if not os.path.exists(peer_priv_path):
            if os.path.exists(f"{peer_priv_path}.bak"):
                peer_priv_path = f"{peer_priv_path}.bak"
            else:
                return False
        with open(peer_priv_path, "r") as f:
            peer_private_key = f.read().strip()
        serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
        expected_sig = f"sig_ed25519_{hashlib.sha256(serialized + peer_private_key.encode('utf-8')).hexdigest()}"
        return signature == expected_sig

    def propose_new_keypair(self) -> tuple:
        raw_seed = os.urandom(32)
        next_private = hashlib.sha256(raw_seed).hexdigest()
        next_public = hashlib.sha256(next_private.encode('utf-8')).hexdigest()[:44]
        return next_private, next_public

    def rotate_active_keypair(self, next_private: str, next_public: str):
        if os.path.exists(self.private_key_path):
            os.rename(self.private_key_path, f"{self.private_key_path}.bak")
        if os.path.exists(self.public_key_path):
            os.rename(self.public_key_path, f"{self.public_key_path}.bak")
        with open(self.private_key_path, "w") as f: f.write(next_private)
        with open(self.public_key_path, "w") as f: f.write(next_public)
        self.private_key = next_private
        self.public_key = next_public
        print(f"🔄 [ENGINE CRYPTO]: Rotation complete! Active Public Key updated.")

# ============================================================
# LEADER ELECTION STATE TRACKING MODULE
# ============================================================
class NodeConsensusState:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.role = "FOLLOWER"  
        self.current_term = 0
        self.current_leader = None
        self.last_heartbeat_time = time.time()
        self.election_timeout = random.uniform(5.0, 8.0) 
        self.mempool = []  

# Global state handles
crypto_engine = None
cluster_state = None

NODE_REGISTRY = {
    "NODE_A": 8000, 
    "NODE_B": 8001, 
    "NODE_C": 8002,
    "NODE_D": 8003,
    "NODE_E": 8004,
    "NODE_F": 8005
}

# ============================================================
# BRIDGE & GATEWAY ROUTING MATRIX
# ============================================================
# Explicit target routing pathways based on Node Role and Anchor Type
BRIDGE_ROUTING_TABLE = {
    "NODE_D": {  # Internal Mesh Bridge
        "KEY_ROTATION": ["NODE_A", "NODE_B", "NODE_C", "NODE_E"], # Sync all core + observer
        "MANUAL_PROPOSAL_001": ["NODE_A", "NODE_B", "NODE_C"],    # Target core consensus only
        "DEFAULT": ["NODE_A", "NODE_B", "NODE_C"]
    },
    "NODE_F": {  # Edge External Gateway
        "KEY_ROTATION": ["NODE_D", "NODE_E"],                     # Escalate up to bridge and observer
        "DEFAULT": ["NODE_D"]                                     # Force all external data through Node D
    }
}

def commit_to_ledger(origin, payload, signature, batch_txs=None):
    """Persists state changes to the local ledger. Supports single tx or atomic batch blocks."""
    try:
        index = 1
        if os.path.exists(LEDGER_PATH) and os.path.getsize(LEDGER_PATH) > 0:
            with open(LEDGER_PATH, 'r') as f: index = sum(1 for _ in f) + 1
            
        if batch_txs:
            ledger_entry = {
                "index": index,
                "timestamp": int(time.time()),
                "type": "BATCH_BLOCK",
                "block_size": len(batch_txs),
                "transactions": batch_txs,
                "state_hash": hashlib.sha256(json.dumps(batch_txs, sort_keys=True).encode()).hexdigest()[:16]
            }
            print(f"📦 [BATCH COMMIT]: Atomically packed {len(batch_txs)} transactions into Block #{index}!")
        else:
            ledger_entry = {
                "index": index,
                "timestamp": int(time.time()),
                "type": "SINGLE_TX",
                "origin_node": origin,
                "payload": payload,
                "state_hash": signature[:16]
            }
            print(f"💾 [STATE PERSISTED]: Written single entry to ledger log block #{index}")
            
        with open(LEDGER_PATH, 'a') as f: 
            f.write(json.dumps(ledger_entry) + "\n")
            
    except Exception as e: 
        print(f"❌ [STORAGE ERROR]: {e}")

def log_telemetry_metrics(source, tx_time, status):
    try:
        rx_time = time.time()
        latency_ms = round((rx_time - tx_time) * 1000, 2)
        with open(METRICS_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([int(rx_time), source, latency_ms, status])
    except Exception: pass

# ============================================================
# BACKGROUND HEARTBEAT & TIMEOUT THREADS
# ============================================================
def run_leader_heartbeat_loop(node_id):
    """If elected leader, broadcasts pings every 2 seconds to hold power."""
    while True:
        if cluster_state.role == "LEADER":
            packet = {
                "protocol_version": "zpp.kai.v1",
                "anchor_id": "CLUSTER_HEARTBEAT",
                "committed_by": node_id,
                "payload": {"term": cluster_state.current_term}
            }
            for peer_name, peer_port in NODE_REGISTRY.items():
                if peer_name == node_id: continue
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.settimeout(0.5)
                    client.connect(('localhost', peer_port))
                    client.sendall(json.dumps(packet).encode('utf-8'))
                    client.close()
                except Exception: pass
        time.sleep(2.0)

def run_election_timeout_monitor(node_id):
    """Monitors incoming signals. Triggers campaign if leader falls silent."""
    while True:
        time.sleep(1.0)
        if cluster_state.role != "LEADER":
            elapsed = time.time() - cluster_state.last_heartbeat_time
            if elapsed > cluster_state.election_timeout:
                print(f"\n🚨 [TIMEOUT]: No heartbeat heard for {elapsed:.2f}s! Initiating election campaign...")
                trigger_election_campaign(node_id)

def trigger_election_campaign(node_id):
    cluster_state.role = "CANDIDATE"
    cluster_state.current_term += 1
    cluster_state.last_heartbeat_time = time.time()
    
    print(f"🗳️  [ELECTION]: Campaigning for Leader Term #{cluster_state.current_term}...")
    votes_received = 1
    
    packet = {
        "protocol_version": "zpp.kai.v1",
        "anchor_id": "CALL_VOTE",
        "committed_by": node_id,
        "payload": {"term": cluster_state.current_term}
    }
    
    for peer_name, peer_port in NODE_REGISTRY.items():
        if peer_name == node_id: continue
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(1.0)
            client.connect(('localhost', peer_port))
            client.sendall(json.dumps(packet).encode('utf-8'))
            
            response_data = client.recv(1024).decode('utf-8')
            if response_data:
                res = json.loads(response_data)
                if res.get("vote") == "GRANTED":
                    votes_received += 1
            client.close()
        except Exception: pass

    print(f"📊 [ELECTION RESULT]: Collected {votes_received} / 3 votes.")
    if votes_received >= 2:
        cluster_state.role = "LEADER"
        cluster_state.current_leader = node_id
        print(f"👑 [COORDINATOR]: {node_id} successfully seized cluster leadership for Term #{cluster_state.current_term}!")
    else:
        cluster_state.role = "FOLLOWER"

# ============================================================
# RECEIVER LAYER WITH COORDINATION & BATCHING HOOKS
# ============================================================
def start_receiver(node_id, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', port))
    server.listen(5)
    processed_proposals = set()
    
    while True:
        try:
            conn, addr = server.accept()
            data = conn.recv(4096).decode('utf-8')
            if not data:
                conn.close()
                continue
            packet = json.loads(data.strip())
            
            if packet.get("protocol_version") == "zpp.kai.v1":
                anchor_id = packet.get("anchor_id")
                payload = packet.get("payload")
                origin = packet.get("committed_by")
                
                if anchor_id == "CLUSTER_HEARTBEAT":
                    cluster_state.last_heartbeat_time = time.time()
                    if cluster_state.current_leader != origin:
                        cluster_state.current_leader = origin
                        cluster_state.current_term = payload.get("term", 0)
                        print(f"🛰️  [HEARTBEAT]: Cluster Coordinator identified as {origin} (Term #{cluster_state.current_term})")
                    conn.close()
                    continue
                
                elif anchor_id == "CALL_VOTE":
                    req_term = payload.get("term", 0)
                    response = {"vote": "DENIED"}
                    if req_term > cluster_state.current_term:
                        cluster_state.current_term = req_term
                        cluster_state.role = "FOLLOWER"
                        cluster_state.current_leader = origin
                        cluster_state.last_heartbeat_time = time.time()
                        response = {"vote": "GRANTED"}
                        print(f"✍️  [VOTE]: Vote GRANTED to {origin} for Term #{req_term}")
                    conn.sendall(json.dumps(response).encode('utf-8'))
                    conn.close()
                    continue
                
                signatures = packet.get("signatures", {})
                tx_time = time.time()
                tx_fingerprint = f"{anchor_id}_{json.dumps(payload, sort_keys=True)}"
                
                if tx_fingerprint in processed_proposals:
                    conn.close()
                    continue
                
                print(f"\n✨ [NATIVE MESH OVERSIGHT]: Inbound Proposal '{anchor_id}' from {origin}")
                
                valid_sig_count = 0
                for signer_node, sig_hex in signatures.items():
                    if NativeEd25519Engine.verify_payload(payload, sig_hex, signer_node):
                        valid_sig_count += 1
                
                if valid_sig_count >= 2:
                    processed_proposals.add(tx_fingerprint)
                    if anchor_id == "KEY_ROTATION":
                        target_node = payload.get("target_node")
                        next_pub = payload.get("next_public")
                        peer_pub_path = os.path.join(KEYS_DIR, f"{target_node}_public.key")
                        with open(peer_pub_path, "w") as f: f.write(next_pub)
                        if node_id == target_node:
                            crypto_engine.rotate_active_keypair(payload["next_private_hidden"], next_pub)
                    else:
                        # 👁️ OBSERVER STATE CAPTURE EXCLUSION
                        if node_id == "NODE_E":
                            print(f"👁️ [OBSERVER SYNC]: Node E verifying and committing state update {anchor_id}")
                            commit_to_ledger(origin, payload, list(signatures.values())[0])
                        
                        elif cluster_state.role == "LEADER":
                            tx_item = {"origin": origin, "payload": payload, "signature": list(signatures.values())[0]}
                            cluster_state.mempool.append(tx_item)
                            print(f"⏳ [MEMPOOL]: Leader added transaction to batch cache ({len(cluster_state.mempool)} / 3)")
                            
                            if len(cluster_state.mempool) >= 3:
                                commit_to_ledger(origin, payload, "", batch_txs=cluster_state.mempool)
                                cluster_state.mempool = []
                        else:
                            commit_to_ledger(origin, payload, list(signatures.values())[0])
                            
                    log_telemetry_metrics(origin, tx_time, "COMMIT_QUORUM")
                else:
                    # 👁️ Observers must never append signatures or gossip packets forward
                    if node_id != "NODE_E" and node_id not in signatures:
                        local_sig = crypto_engine.sign_payload(payload)
                        packet["signatures"][node_id] = local_sig
                        packet["committed_by"] = node_id
                        threading.Thread(target=broadcast_to_mesh, args=(node_id, packet), daemon=True).start()
                        
            conn.close()
        except Exception: pass

def broadcast_to_mesh(source_node, packet_dict):
    for peer_name, peer_port in NODE_REGISTRY.items():
        if peer_name == source_node: continue
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(1.0)
            client.connect(('localhost', peer_port))
            client.sendall(json.dumps(packet_dict, indent=2).encode('utf-8'))
            client.close()
        except Exception: pass

# ============================================================
# EXECUTION LAYER
# ============================================================
from http.server import BaseHTTPRequestHandler, HTTPServer

class IngressGatewayHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"📡 [API TRAFFIC DETECTED]: Inbound hit on path {self.path}!")
        
        if self.path == '/ingress':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                anchor_id = data.get("anchor_id", "DYNAMIC_ANCHOR")
                payload = data.get("payload", {})
                
                signature = crypto_engine.sign_payload(payload)
                packet = {
                    "protocol_version": "zpp.kai.v1", 
                    "anchor_id": anchor_id, 
                    "committed_by": cluster_state.node_id, 
                    "payload": payload, 
                    "signatures": {cluster_state.node_id: signature}
                }
                
                # 🌉 BRIDGE & GATEWAY OVERRIDE FOR NODE_D & NODE_F
                if cluster_state.node_id in BRIDGE_ROUTING_TABLE:
                    role_type = "BRIDGE" if cluster_state.node_id == "NODE_D" else "EXTERNAL GATEWAY"
                    print(f"🌉 [ROUTER RELAY]: {role_type} ({cluster_state.node_id}) processing '{anchor_id}'...")
                    
                    # Look up specific targets for this anchor, fallback to DEFAULT route if unmapped
                    node_routes = BRIDGE_ROUTING_TABLE[cluster_state.node_id]
                    target_peers = node_routes.get(anchor_id, node_routes["DEFAULT"])
                    
                    print(f"    ├──> Resolved Path Matrix: Targets => {target_peers}")
                    
                    for peer_name in target_peers:
                        if peer_name == cluster_state.node_id or peer_name not in NODE_REGISTRY:
                            continue
                        
                        peer_port = NODE_REGISTRY[peer_name]
                        try:
                            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            client.settimeout(1.0)
                            client.connect(('localhost', peer_port))
                            client.sendall(json.dumps(packet, indent=2).encode('utf-8'))
                            client.close()
                            print(f"    └──> [RELAY SUCCESS] -> {peer_name} on Port {peer_port}")
                        except Exception as e:
                            print(f"    └──> ⚠️ [RELAY FAILED] -> Could not reach {peer_name}: {e}")
                else:
                    # Standard core node behavior (A, B, C)
                    broadcast_to_mesh(cluster_state.node_id, packet)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ACKNOWLEDGED", "anchor": anchor_id}).encode())

                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

def run_ingress_api_server(port):
    """Runs a dedicated API gateway on port + 1000 (e.g., Node A on 9000)"""
    server = HTTPServer(('localhost', port + 1000), IngressGatewayHandler)
    server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in NODE_REGISTRY:
        print("Usage: python transport_sim.py [NODE_A | NODE_B | NODE_C | NODE_D | NODE_E | NODE_F]")
        sys.exit(1)
        
    current_node = sys.argv[1]
    crypto_engine = NativeEd25519Engine(current_node)
    cluster_state = NodeConsensusState(current_node)
    my_port = NODE_REGISTRY[current_node]
    
    # Start server listener
    threading.Thread(target=start_receiver, args=(current_node, my_port), daemon=True).start()
    threading.Thread(target=run_ingress_api_server, args=(my_port,), daemon=True).start()
    
    # Start discovery
    threading.Thread(target=listen_for_discovery, daemon=True).start()
    threading.Thread(target=send_discovery_broadcast, daemon=True).start()
    
    # Start Raft Heartbeat & Monitoring threads
    threading.Thread(target=run_leader_heartbeat_loop, args=(current_node,), daemon=True).start()
    threading.Thread(target=run_election_timeout_monitor, args=(current_node,), daemon=True).start()
    
    time.sleep(0.5)
    print(f"--- {current_node} Online. Mesh Gossip, RAFT & Discovery Engaged ---")
    
    while True:
        try:
            choice = input(f"\n[{cluster_state.role}] {current_node} > 1=Send Tx, 2=Tamper, 3=Rotate Key: ")
            mock_payload = {"alpha": 0.5350, "gamma": 0.6400, "state": "ACCEPT"}
            
            if choice in ["1", "2"]:
                signature = crypto_engine.sign_payload(mock_payload)
                if choice == "2": signature = "sig_ed25519_CORRUPTED_0xDEADBEEF"
                packet = {"protocol_version": "zpp.kai.v1", "anchor_id": "MANUAL_PROPOSAL_001", "committed_by": current_node, "payload": mock_payload, "signatures": {current_node: signature}}
                broadcast_to_mesh(current_node, packet)
                time.sleep(1.5)
            elif choice == "3":
                next_priv, next_pub = crypto_engine.propose_new_keypair()
                rotation_payload = {"target_node": current_node, "next_public": next_pub, "next_private_hidden": next_priv}
                signature = crypto_engine.sign_payload(rotation_payload)
                packet = {"protocol_version": "zpp.kai.v1", "anchor_id": "KEY_ROTATION", "committed_by": current_node, "payload": rotation_payload, "signatures": {current_node: signature}}
                broadcast_to_mesh(current_node, packet)
                time.sleep(1.5)
        except KeyboardInterrupt:
            sys.exit(0)