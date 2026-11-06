## ZPP - Config Json

zpp_id: config_json
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-26

---

```python
{
    "node_id": "Taras_MBP_Node",
    "chain_id": "zpp_alpha_mainnet",
    "policy_lineage": "zpp-alpha-mainnet",
    "weights": {
        "w1": 0.40,
        "w2": 0.30,
        "w3": 0.30
    },
    "thresholds": {
        "alpha": 0.15,
        "gamma": 0.85
    },
    "genesis": {
        "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000"
    },
    "peer_network_map": {
        "NODE_A": {"host": "localhost", "port": 8000, "ingress_port": 9000},
        "NODE_B": {"host": "localhost", "port": 8001, "ingress_port": 9001},
        "NODE_C": {"host": "localhost", "port": 8002, "ingress_port": 9002},
        "NODE_D": {"host": "localhost", "port": 8003, "ingress_port": 9003},
        "NODE_E": {"host": "localhost", "port": 8004, "ingress_port": 9004},
        "NODE_F": {"host": "localhost", "port": 8005, "ingress_port": 9005}
    },
    "simulated_pipeline": {
        "gate_01_ingress_buffering": false,
        "gate_02_state_override_allowed": true,
        "gate_03_static_render_lock": true,
        "variance_target": 0.0000
    }
}