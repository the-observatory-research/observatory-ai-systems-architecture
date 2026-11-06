## Transport Simulation: Tampered Payload Test (REJECT)

zpp_id: transport_sim_tamper
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_DEPLOYMENT`
timestamp: 2026-06-08

---

### Test Configuration

| Parameter           | Value                                |
| :------------------ | :----------------------------------- |
| **Node A**          | `NODE_A` (port 8000)                 |
| **Node B**          | `NODE_B` (port 8001)                 |
| **Test type**       | Tampered payload (invalid signature) |
| **Expected result** | REJECT / QUARANTINE                  |

---

#### Terminal Output (Node A)

```console
(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % python3 transport_sim.py NODE_A

🛰️  [NODE_A DOCK] Listening on port 8000...

--- NODE_A Online. Target peer is NODE_B ---

NODE_A > Enter '1' for VALID payload, '2' for TAMPERED payload: 2

⚠️ Injecting invalid signature field for verification testing...

⚡ Sending proposal to NODE_B on port 8001...
✅ Transmission to NODE_B complete.

NODE_A > Enter '1' for VALID payload, '2' for TAMPERED payload:
```

#### Terminal Output (Node B)

```console
(zero_point_env) <LOCAL_USER>@<LOCAL_HOST> node % python3 transport_sim.py NODE_B

🛰️  [NODE_B DOCK] Listening on port 8001...

--- NODE_B Online. Target peer is NODE_A ---

NODE_B > Enter '1' for VALID payload, '2' for TAMPERED payload: 

📥 [NODE_B INBOUND PACKET RECEIVED FROM NODE_A]
Checking cryptographic signature integrity...
🚨 [CRITICAL ALERT - VERIFICATION FAILED]: Signature mismatch!
Resulting Consensus State: REJECT / QUARANTINE
```

### Verification Summary

| Claim                             | Result                  |
| --------------------------------- | ----------------------- |
| Tampered payload detected         | ✅                       |
| Cryptographic verification failed | ✅                       |
| Consensus state                   | ❌ `REJECT / QUARANTINE` |
| Expected behavior                 | ✅ Confirmed             |

