## Transport Simulation: Local Two-Node Broadcast

zpp_id: transport_sim_local_broadcast
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_DEPLOYMENT`
timestamp: 2026-06-08 

---

#### Terminal Output

```console
(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % open -e transport_sim.py

(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % python transport_sim.py NODE_A
🛰️  [NODE_A DOCK] Listening on port 8000...
--- NODE_A Online. Target peer is NODE_B ---

NODE_A > Press Enter to broadcast a mock GAMMA proposal (or Ctrl+C to exit)...

⚡ Sending proposal to NODE_B on port 8001...
✅ Transmission to NODE_B complete.

NODE_A > Press Enter to broadcast a mock GAMMA proposal (or Ctrl+C to exit)...

---

(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % python transport_sim.py NODE_B
🛰️  [NODE_B DOCK] Listening on port 8001...
--- NODE_B Online. Target peer is NODE_A ---

NODE_B > Press Enter to broadcast a mock GAMMA proposal (or Ctrl+C to exit)...

📥 [NODE_B INBOUND PACKET RECEIVED]
----------------------------------------
{
  "chain_id": "zpp-alpha-mainnet",
  "origin_node": "NODE_A",
  "timestamp": 1780945896,
  "policy_version": "3.1.4",
  "payload": {
    "alpha": 0.535,
    "gamma": 0.64,
    "state": "ACCEPT"
  },
  "signature": "Ed25519_SIG_MOCK_0x7f39b1a..."
}
----------------------------------------

---
```

#### Terminal Output (Node A)

```console
(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % python transport_sim.py NODE_A

🛰️  [NODE_A DOCK] Listening on port 8000...

--- NODE_A Online. Target peer is NODE_B ---

NODE_A > Press Enter to broadcast a mock GAMMA proposal (or Ctrl+C to exit)...

⚡ Sending proposal to NODE_B on port 8001...
✅ Transmission to NODE_B complete.

NODE_A > Press Enter to broadcast a mock GAMMA proposal (or Ctrl+C to exit)...

## Terminal Output (Node B)

(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % python transport_sim.py NODE_B

🛰️  [NODE_B DOCK] Listening on port 8001...

--- NODE_B Online. Target peer is NODE_A ---

NODE_B > Press Enter to broadcast a mock GAMMA proposal (or Ctrl+C to exit)...

📥 [NODE_B INBOUND PACKET RECEIVED]
----------------------------------------
{
  "chain_id": "zpp-alpha-mainnet",
  "origin_node": "NODE_A",
  "timestamp": 1780945896,
  "policy_version": "3.1.4",
  "payload": {
    "alpha": 0.535,
    "gamma": 0.64,
    "state": "ACCEPT"
  },
  "signature": "Ed25519_SIG_MOCK_0x7f39b1a..."
}
----------------------------------------

---
```

### Verification Summary (Base Transport)

| Claim                                              | Status                   |
| -------------------------------------------------- | ------------------------ |
| Two nodes can communicate without a central server | ✅ Proven (localhost)     |
| Structured GAMMA proposal transmitted              | ✅ Proven                 |
| Payload matches Section 6 specifications           | ✅ Proven                 |
| Signature field exists (mock)                      | ✅ Ready for real Ed25519 |

---
### Evolution of This Test

| Version            | Description                                | Status     |
| ------------------ | ------------------------------------------ | ---------- |
| **Base broadcast** | Two-node transmission without verification | ✅ Complete |
| **Tampered test**  | Invalid signature → REJECT                 | ✅ Complete |
| **Valid test**     | Correct signature → ACCEPT                 | ✅ Complete |
