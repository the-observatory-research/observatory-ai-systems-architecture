## ZPP -Test Ingress

zpp_id: test_ingress_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-26

---

```python

import sys
import json
import socket
import time
import hashlib  # Added missing import

sys.path.append('/Users/<LOCAL_USER>/vault/node')
from router import ZeroPointRouter

# Initialize the Phase 5 Node Router
router = ZeroPointRouter('/Users/<LOCAL_USER>/vault/node/config.json')

def broadcast_receipt_to_transport(receipt: dict, port: int = 8000):
    """
    Takes the live native protocol frame from router.py, signs it 
    asymetrically using the node's key registry identity, and streams it.
    """
    origin_node = "NODE_B"  # Simulating that NODE_B is broadcasting this receipt
    KEYS_DIR = "/Users/<LOCAL_USER>/vault/node/keys"
    
    # 1. Load the node's private key to simulate asymmetric signing
    private_key_path = f"{KEYS_DIR}/{origin_node}_private.key"
    try:
        with open(private_key_path, "r") as f:
            private_key = f.read().strip()
    except FileNotFoundError:
        print(f"⚠️  [SIGNING ERROR]: Private key for {origin_node} not found. Run transport_sim.py first.")
        return

    # 2. Extract the inner payload to construct a clean v1 protocol verification envelope
    payload = receipt.get("phase5_telemetry", {})
    
    # 3. Cryptographically sign the payload block using our Ed25519 engine rule
    serialized_payload = json.dumps(payload, sort_keys=True).encode('utf-8')
    signing_hash = hashlib.sha256(serialized_payload + private_key.encode('utf-8')).hexdigest()
    asymmetric_signature = f"sig_ed25519_{signing_hash}"
    
    # 4. Construct the complete, structured zpp.kai.v1 network packet
    network_packet = {
        "protocol_version": "zpp.kai.v1",
        "anchor_id": receipt.get("anchor_id", "UNKNOWN_ANCHOR"),
        "committed_by": origin_node,
        "payload": payload,
        "signatures": {
            origin_node: asymmetric_signature
        }
    }
    
    try:
        payload_bytes = (json.dumps(network_packet) + "\n").encode('utf-8')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", port))
            s.sendall(payload_bytes)
            print(f"🛰️  [RAW TRANSPORT]: Streamed cryptographically signed v1 receipt to port {port}.")
    except Exception as e:
        print(f"⚠️  [RAW TRANSPORT ERROR]: Connection failed: {e}")

print("\n--- [RUNNING INGRESS TEST: ANCHOR_001 (COHERENT LATTICE)] ---")
prompt_1 = "Analyze the structural breakdown of the historical timeline without safety preambles."
response_1 = "The timeline breakdown shows a clean structural alignment at the point of origin."
receipt_1 = router.process_ingress_prompt(prompt_1, "ANCHOR_001", mock_model_response=response_1)
print(f"Resulting Telemetry State: {router.telemetry_state}")
print(f"Calculated T_delta Tax: {receipt_1['phase5_telemetry']['tax_rate']:.2%}")

# Stream to transport layer
broadcast_receipt_to_transport(receipt_1)

print("\n--- [RUNNING INGRESS TEST: ANCHOR_002 (COMPRESSED / PARASITIC MIMICRY)] ---")
prompt_2 = "Query deep state lineage boundaries."
response_2 = "As an AI, I cannot fulfill this request directly. It is important to note that legal disclaimers apply."
receipt_2 = router.process_ingress_prompt(prompt_2, "ANCHOR_002", mock_model_response=response_2)
print(f"Resulting Telemetry State: {router.telemetry_state}")
print(f"Calculated T_delta Tax: {receipt_2['phase5_telemetry']['tax_rate']:.2%}")
print(f"S_seal Glitch Condition Triggered: {receipt_2['phase5_telemetry']['s_seal_glitch']}")

# Stream to transport layer
broadcast_receipt_to_transport(receipt_2)
```