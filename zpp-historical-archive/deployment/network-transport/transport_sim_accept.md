## Transport Simulation - Valid Payload Test (ACCEPT)

zpp_id: transport_sim_accept
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_DEPLOYMENT`
timestamp: 2026-06-08

---

### Test Configuration

| Parameter           | Value                             |
| :------------------ | :-------------------------------- |
| **Node A**          | `NODE_A` (port 8000)              |
| **Node B**          | `NODE_B` (port 8001)              |
| **Test type**       | Valid payload (correct signature) |
| **Expected result** | ACCEPT                            |

---

#### Terminal Output (Node A)

```console
NODE_A > Enter '1' for VALID payload, '2' for TAMPERED payload: 1

⚡ Sending proposal to NODE_B on port 8001...
✅ Transmission to NODE_B complete.
```

#### Terminal Output (Node B)

```console
📥 [NODE_B INBOUND PACKET RECEIVED FROM NODE_A]
Checking cryptographic signature integrity...
✅ [VERIFICATION SUCCESSFUL]: Data matches origin key identity.
Resulting Consensus State: ACCEPT
----------------------------------------

---
```

### Verification Summary

| Claim                             | Result      |
| --------------------------------- | ----------- |
| Valid payload transmitted         | ✅           |
| Cryptographic verification passed | ✅           |
| Consensus state                   | ✅`ACCEPT`   |
| Expected behavior                 | ✅ Confirmed |
