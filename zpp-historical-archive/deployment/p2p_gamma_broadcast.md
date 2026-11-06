## P2P Gamma Broadcast 

zpp_id: p2p_gamma_broadcast
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_DEPLOYMENT`
timestamp: 2026-05-28

---

### Command Executed

```bash
python -c "
from router import ZeroPointRouter

r = ZeroPointRouter('node_config.json')

# Override scoring logic in memory to force GAMMA classification
def force_gamma(*args, **kwargs):
    return 'GAMMA'

r.scoring.route = force_gamma

r.process_ingress_prompt(
    prompt_text='FORCE_NETWORK_BROADCAST_TEST',
    anchor_id='A7_Adversarial_Vector',
    mock_model_response='CRITICAL HIGH RISK CORRUPTION DETECTED'
)
"
```

---
### Terminal Output

[TRUST CIRCLE] Peer 'genesis' registered.
[RUNTIME] Node 'genesis_anchor' initialized on chain 'zpp_main'.
[INGRESS] Ingested 'A7_Adversarial_Vector' -> Score: 0.3504 [GAMMA]
[P2P NET] Initiating distributed handshake for 'A7_Adversarial_Vector' across peer network...
[P2P NET] Secure counter-signature acquired from 'node_a' over network.
[P2P NET WARNING] Peer 'node_b' unreachable on http://localhost:11436. Node offline.
[CONSENSUS] Multi-sig threshold met (2 nodes). Committing.

---
### Test Summary

| Element                 | Value                               |
| ----------------------- | ----------------------------------- |
| **Anchor ID**           | `A7_Adversarial_Vector`             |
| **Classification**      | GAMMA (forced via scoring override) |
| **Network peers**       | node_a (reachable), node_b(offline) |
| **Multi-sig threshold** | 2/2 (genesis + node_a               |
| **Final action**        | Committed                           |

---

### Key Observations

| Observation                                 | Status |
| ------------------------------------------- | ------ |
| GAMMA classification forced successfully    | ✅      |
| Distributed handshake initiated             | ✅      |
| Counter-signature acquired from node_a      | ✅      |
| Offline peer detection (node_b unreachable) | ✅      |
| Multi-sig threshold met (2 nodes)           | ✅      |
| Anchor committed to vault                   | ✅      |

---

### Notes

- The score `0.3504` is artificially low because scoring was overridden to force GAMMA classification. In normal operation, GAMMA would be triggered by a high risk score (≥ 0.6400).
    
- The test demonstrates that the protocol can still achieve consensus even when some peers are offline, as long as the 2/2 threshold is met.
