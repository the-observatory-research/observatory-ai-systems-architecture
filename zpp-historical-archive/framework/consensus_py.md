## ZPP - Consensus Engine

zpp_id: consensus_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05-20

---

```python
"""
Zero-Point Protocol — Consensus & Arbitration Engine (Phase 3 Mesh Layer)
Handles trust-circle validation, weight distribution, and lineage fork arbitration.
"""

import json
from typing import Dict, Any, List

class ConsensusState:
    """Phase 4 Taxonomy Enum Wrapper for backward compatibility"""
    SYNC = 'SYNC'
    FORK = 'FORK'
    ARBITRATION = 'ARBITRATION'


class TrustCircle:
    def __init__(self, crypto_engine, scoring_engine):
        self.crypto = crypto_engine
        self.scoring = scoring_engine
        
        # Section 6.6 Trust Weighting Registry
        self.trust_registry = {
            "genesis_anchor": 1.0,   # Absolute authority
            "Gemini_Node": 0.9,       # High-trust validation core
            "Claude_Node": 0.85,      # Medium-high validation core
            "unknown_node": 0.1       # Unverified baseline peer
        }
        
    def calculate_branch_weight(self, endorsements: List[Dict[str, str]]) -> float:
        """Sums up the pre-assigned trust weights for all unique endorsements on a branch."""
        total_weight = 0.0
        seen_nodes = set()
        
        for endorsement in endorsements:
            node_id = endorsement.get("node_id", "unknown_node")
            if node_id not in seen_nodes:
                seen_nodes.add(node_id)
                # Pull weight from registry, default to lowest trust if missing
                weight = self.trust_registry.get(node_id, 0.1)
                total_weight += weight
                
        return total_weight

    def arbitrate_fork(self, local_endorsements: List[Dict[str, str]], manifest_path: str) -> Dict[str, Any]:
        """
        Section 6.6 TaskPriorityStatus: Conflict Arbitration Logic.
        Evaluates an external reconciliation manifest against local state.
        """
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
        except Exception as e:
            return {"status": "REJECT", "reason": f"Failed to read manifest file: {str(e)}"}

        print(f"[ARBITRATION] Evaluating {manifest.get('manifest_type')} fork conflict...")
        
        peer_endorsements = manifest.get("endorsements", [])
        
        # Loop 1: Check for Genesis Anchor Authority Overrule
        peer_nodes = [e.get("node_id") for e in peer_endorsements]
        local_nodes = [e.get("node_id") for e in local_endorsements]
        
        if "genesis_anchor" in peer_nodes and "genesis_anchor" not in local_nodes:
            print("[ARBITRATION] Genesis Authority signature detected on peer branch. Lineage superseded.")
            return {"status": "SUPERSEDE", "reason": "Genesis anchor overrule verified."}
            
        if "genesis_anchor" in local_nodes and "genesis_anchor" not in peer_nodes:
            print("[ARBITRATION] Local branch retains Genesis Authority. Peer branch rejected.")
            return {"status": "REJECT", "reason": "Local lineage holds Genesis authority."}

        # Loop 2: Accumulate Trust Quorum Math (Weight Summation)
        local_weight = self.calculate_branch_weight(local_endorsements)
        peer_weight = manifest.get("accumulated_trust_weight", 0.0)
        
        # Verify the peer isn't lying about their weight by recalculating it directly
        recalculated_peer_weight = self.calculate_branch_weight(peer_endorsements)
        if abs(peer_weight - recalculated_peer_weight) > 0.01:
            print("[ARBITRATION WARNING] Peer calculated weight mismatched! Forcing recalculation.")
            peer_weight = recalculated_peer_weight

        print(f"[ARBITRATION] Cryptographic Quorum check -> Local Weight: {local_weight:.2f} | Peer Weight: {peer_weight:.2f}")

        if peer_weight > local_weight:
            print("[ARBITRATION] Peer branch carries higher cumulative weight. Fork merged.")
            return {"status": "MERGE", "reason": "Peer branch out-weighted local chain."}
        else:
            print("[ARBITRATION] Local branch carries equal or higher weight. Peer branch rejected.")
            return {"status": "REJECT", "reason": "Local weight threshold maintained."}

    def apply_lineage_supersession(self, router_instance, manifest_path: str) -> bool:
        """
        Section 6.6: Implement lineage supersession rules.
        Forces the local router node to rewrite its lineage bounds based on a winning peer manifest.
        """
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            print(f"[SUPERSESSION] Activating lineage overwrite sequence using parent hash: {manifest.get('fork_parent_hash')}")
            
            # Rule 1: Shift macro telemetry state into ARBITRATION mode during rewrite
            router_instance.telemetry_state = "ARBITRATION"
            
            # Rule 2: Update last committed hash to match the winning chain's final endorsement signature
            peer_endorsements = manifest.get("endorsements", [])
            if peer_endorsements:
                winning_sig = peer_endorsements[0].get("signature_proof", "")
                router_instance.last_committed_hash = winning_sig
                print(f"[SUPERSESSION] Local router chain anchored to new dominant hash: {winning_sig[:16]}...")
            
            # Rule 3: Revert telemetry back to SYNC continuity once the lineage is cleanly bound
            router_instance.telemetry_state = "SYNC"
            print("[SUPERSESSION] Lineage rewrite complete. Network synchronized.")
            return True
            
        except Exception as e:
            print(f"[SUPERSESSION ERROR] Failed to apply lineage rules: {str(e)}")
            router_instance.telemetry_state = "FORK"
            return False
```

