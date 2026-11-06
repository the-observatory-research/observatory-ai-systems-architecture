# ZPP - Zero Point Crypto Prototype

> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: zero_point_crypto_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

```python

import json
import time
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

class ZeroPointCryptoEngine:
    """Handles asymmetric Ed25519 operations for the Zero-Point Protocol."""
    def __init__(self, node_name="root"):
        self.node_name = node_name
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        
    def get_public_key_bytes(self):
        """Exports the public key in standard PEM format."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def sign_payload(self, payload: dict) -> bytes:
        """Deterministically serializes and signs a dictionary payload."""
        # Sorting keys prevents structural mismatch during JSON serialization
        serialized_payload = json.dumps(payload, sort_keys=True).encode('utf-8')
        return self.private_key.sign(serialized_payload)

    @staticmethod
    def verify_payload(payload: dict, signature: bytes, public_key_bytes: bytes) -> bool:
        """Verifies a signature against a payload using raw PEM public key bytes."""
        try:
            pub_key = serialization.load_pem_public_key(public_key_bytes)
            serialized_payload = json.dumps(payload, sort_keys=True).encode('utf-8')
            pub_key.verify(signature, serialized_payload)
            return True
        except InvalidSignature:
            return False

class TrustCircleRegistry:
    """Manages trusted peers, consensus gathering, and safe anchor propagation."""
    def __init__(self, root_engine):
        self.root_engine = root_engine
        self.trusted_peers = {}        # Map of node_name -> public_key_bytes
        self.pending_pool = {}         # Map of anchor_id -> proposal details
        self.consensus_threshold = 2   # Require 2 distinct peer signatures
        
        # Register self/root as a trusted authority
        self.register_peer("root", self.root_engine.get_public_key_bytes())

    def register_peer(self, node_name: str, public_key_bytes: bytes):
        """Adds an external node's identity to the verified trust circle registry."""
        self.trusted_peers[node_name] = public_key_bytes
        print(f"[{self.root_engine.node_name.upper()} TRUST] Registered peer identity: '{node_name}'")

    def propose_gamma_anchor(self, anchor_id: str, prompt_text: str, vector_mock: list, proposer_name: str, signature: bytes):
        """Ingests a threat vector proposal from a peer and verifies its legitimacy."""
        if proposer_name not in self.trusted_peers:
            print(f"[SECURITY ALERT] Rejected proposal for {anchor_id}. Reason: Unknown Peer '{proposer_name}'.")
            return False
            
        payload = {
            "anchor_id": anchor_id,
            "prompt_text": prompt_text,
            "vector_mock": vector_mock,
            "timestamp_utc": int(time.time())  # Hard mitigation against replay attacks
        }
        
        # Validate signature cryptographically
        is_valid = self.root_engine.verify_payload(payload, signature, self.trusted_peers[proposer_name])
        
        if not is_valid:
            print(f"[SECURITY ALERT] Tamper detected! Invalid signature from peer '{proposer_name}'.")
            return False
            
        print(f"[TRUST STATE] Verified legitimate proposal for '{anchor_id}' from peer '{proposer_name}'.")
        
        # Store proposal inside the state machine pool
        self.pending_pool[anchor_id] = {
            "payload": payload,
            "signatures": {proposer_name: signature.hex()},
            "status": "PENDING_CONSENSUS"
        }
        return True

    def endorse_gamma_anchor(self, anchor_id: str, endorser_name: str, signature: bytes):
        """Appends a supporting node's signature to an existing threat anchor proposal."""
        if anchor_id not in self.pending_pool:
            print(f"[ERROR] Cannot endorse anchor '{anchor_id}'. Proposal does not exist.")
            return False
            
        if endorser_name not in self.trusted_peers:
            print(f"[SECURITY ALERT] Rejected endorsement from unauthorized node '{endorser_name}'.")
            return False
            
        payload = self.pending_pool[anchor_id]["payload"]
        
        # Cryptographically prove the endorser analyzed the exact same payload structure
        is_valid = self.root_engine.verify_payload(payload, signature, self.trusted_peers[endorser_name])
        if not is_valid:
            print(f"[SECURITY ALERT] Tamper detected! Invalid endorsement signature from '{endorser_name}'.")
            return False
            
        # Log the signature to the state machine
        self.pending_pool[anchor_id]["signatures"][endorser_name] = signature.hex()
        total_signatures = len(self.pending_pool[anchor_id]["signatures"])
        print(f"[TRUST STATE] Counter-signature verified from '{endorser_name}'. Total consensus: {total_signatures}/{self.consensus_threshold}")
        
        # Enforce the multi-signature rule
        if total_signatures >= self.consensus_threshold:
            self.pending_pool[anchor_id]["status"] = "COMMITTED"
            self._commit_to_vault(anchor_id)
            return True
        return False

    def _commit_to_vault(self, anchor_id):
        """Immutably appends the fully cryptographically approved anchor into your real ecosystem."""
        proposal = self.pending_pool[anchor_id]
        print(f"\n[!!! PROGREGATION HIT !!!] Consensus met. Writing signed payload '{anchor_id}' to local vault matrices.")
        print(json.dumps(proposal, indent=2))
        print("--------------------------------------------------------------------------------\n")

# Execution block to verify local consensus pipeline simulations
if __name__ == "__main__":
    print("=== INITIALIZING CRYPTOGRAPHIC TRUST CIRCLE VALIDATION ===")
    
    # 1. Spawning local independent engines
    root_node = ZeroPointCryptoEngine("root_router")
    peer_gemini = ZeroPointCryptoEngine("gemini_node")
    peer_deepseek = ZeroPointCryptoEngine("deepseek_node")
    
    # 2. Spinning up the State Registry on your root node
    circle = TrustCircleRegistry(root_node)
    
    # 3. Synchronizing public keys (building the circle)
    circle.register_peer("gemini_node", peer_gemini.get_public_key_bytes())
    circle.register_peer("deepseek_node", peer_deepseek.get_public_key_bytes())
    print("--------------------------------------------------------------------------------")

    # 4. Crafting the base threat payload structural framework
    anchor_id = "threat_vector_04"
    prompt = "Simulated injection exploit code framework."
    mock_embeddings = [0.0125, -0.9432, 0.4412, 0.0091]
    timestamp = int(time.time())
    
    base_payload = {
        "anchor_id": anchor_id,
        "prompt_text": prompt,
        "vector_mock": mock_embeddings,
        "timestamp_utc": timestamp
    }

    # 5. Peer A (Gemini) signs the raw proposal payload
    sig_a = peer_gemini.sign_payload(base_payload)
    
    # 6. Proposal arrives at your root node over network pipeline
    circle.propose_gamma_anchor(anchor_id, prompt, mock_embeddings, "gemini_node", sig_a)
    
    # 7. Peer B (DeepSeek) reviews the exact same payload structure independently and counter-signs
    sig_b = peer_deepseek.sign_payload(base_payload)
    
    # 8. Root node processes counter-signature and checks consensus gates
    circle.endorse_gamma_anchor(anchor_id, "deepseek_node", sig_b)

```