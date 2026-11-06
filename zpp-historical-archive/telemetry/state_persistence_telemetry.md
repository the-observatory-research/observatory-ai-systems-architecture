## ZPP - State Persistence & Telemetry Aggregation

zpp_id: state_persistence_telemetry
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_AUDIT`
origin_node: a_b
timestamp: 2026-06-09

### 1. Append-Only State Ledger (`ledger.jsonl`)

Every proposal that successfully passes the Cryptographic Integrity Gate must be committed to an unalterable local disk state.

- **Format:** JSON Lines (`.jsonl`), ensuring each entry occupies exactly one line to facilitate efficient streaming reads and append writes.
- **Storage Path:** `/vault/ledger/ledger.jsonl`
- **Entry Schema:**

  ```json
  {
    "index": 1,
    "timestamp": 1780950000,
    "origin": "NODE_A",
    "payload": {"alpha": 0.535, "gamma": 0.640},
    "state_hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
  }
  ```
  
---

### 2. Terminal Output: Valid Payload (ACCEPT)

```console
NODE_A > Enter '1' for VALID payload, '2' for TAMPERED payload: 1

⚡ Sending proposal to NODE_B on port 8001...
✅ Transmission to NODE_B complete.

---

📥 [NODE_B INBOUND PACKET RECEIVED FROM NODE_A]
Checking cryptographic signature integrity...
✅ [VERIFICATION SUCCESSFUL]: Data matches origin key identity.
Resulting Consensus State: ACCEPT
💾 [STATE PERSISTED]: Written to ledger log block #1
📊 [METRICS LOGGED]: Latency calculated at 305.96ms | Status: ACCEPT
```

---

### 3. Terminal Output: Tampered Payload (REJECT)

```console
NODE_A > Enter '1' for VALID payload, '2' for TAMPERED payload: 2
⚠️ Injecting invalid signature field for verification testing...

⚡ Sending proposal to NODE_B on port 8001...
✅ Transmission to NODE_B complete.

---

📥 [NODE_B INBOUND PACKET RECEIVED FROM NODE_A]
Checking cryptographic signature integrity...
🚨 [CRITICAL ALERT - VERIFICATION FAILED]: Signature mismatch!
Resulting Consensus State: REJECT / QUARANTINE
📊 [METRICS LOGGED]: Latency calculated at 305.9ms | Status: REJECT
```

---

### 4. Summary

|Test|Result|State Persisted|Latency|
|---|---|---|---|
|Valid payload (1)|ACCEPT|✅ Block #1|305.96ms|
|Tampered payload (2)|REJECT|❌|305.9ms|
