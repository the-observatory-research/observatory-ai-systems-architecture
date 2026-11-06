## Phase 2 - Cryptographic Governance

zpp_id: 05-phase-2-cryptographic-governance
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 
timestamp: 2026-05

---

### 5.1 Ed25519 Signing & Immutable Audit Trail

- **The Problem:** Dependency on heavy external cryptographic libraries introduces supply-chain vulnerability and cross-platform compilation failures in isolated node environments.
    
- **The Solution:** Implementation of a zero-dependency `NativeCryptoFallback` class directly within the core routing architecture. Every execution frame is mapped canonically via Python's standard `hashlib` primitives.

|**Component**|**Runtime Implementation Method**|**Technical Behavior**|
|---|---|---|
|**Payload Hashing**|`crypto.hash_prompt(text)`|Generates a SHA-256 hex digest of the standardized prompt payload.|
|**Payload Signing**|`crypto.sign_payload(payload)`|Serializes data via deterministic, key-sorted canonical JSON mapping and returns the target cryptographic digest.|
|**State Chain Binding**|`self.last_committed_hash`|Dynamically updates the sequential validation hash upon every successful consensus commit.|

---

### 5.2 Automated Resonance Tuning

The threshold optimization problem is defined as minimizing the weighted sum of classification errors, applying a strict security bias to minimize false negatives on critical path boundaries:

$$\min_{\alpha, \gamma} \big( w_{fp} \cdot \text{FP}(\alpha, \gamma) + w_{fn} \cdot \text{FN}(\alpha, \gamma) \big)$$

Where $w_{fn} = 3 \times w_{fp}$ (representing a $3\times$ security bias).

- $\text{FP}$ = False Positive (incorrect `GAMMA` escalation on benign inputs)
    
- $\text{FN}$ = False Negative (missed `GAMMA` threat bypass)

---

### 5.3 Trust Circle & 2/2 Multi-Signature Consensus

The consensus protocol has transitioned from a theoretical design to an active, non-blocking TCP socket bridge running natively within `ZeroPointRouter._broadcast_proposal_to_mesh()`.

GAMMA GATE TRIGGERED (S >= 0.6400)
  |
  v
Construct JSON Transport Packet
  |
  +--> Socket Port 8001 -- Transmit Packet
  |
  +--> Socket Port 8002 -- Transmit Packet
  |
  v
Evaluate Network Signature Quorum
  |
  +--> Quorum >= 2 Nodes --> COMMIT TO LEDGER
  |
  +--> Quorum < 2 Nodes  --> QUARANTINE STATE

📡 **Active Network Status Note:** When a transaction drops into a `GAMMA` pathway, the router executes a live socket flood across the network map (`NODE_A`, `NODE_B`, `NODE_C`). If at least two valid signatures are gossiped back across the transport boundary, the transaction achieves quorum, receives an `ACCEPT` status, and is committed to the local ledger.

---

### 5.4 Manual Override Protocol

When a human operator overrides a routing decision, or when simulated pipeline configurations force an architectural shift, the event MUST be captured natively. The system enforces transparency by recording these changes as explicit, signed event frames rather than silently modifying historical transactions.

The protocol enforces the following standardized tracking payload structure:

```json
{
  "schema_version": "zpp.event.v1",
  "event_type": "MANUAL_OVERRIDE",
  "original_route": "GAMMA",
  "override_route": "ALPHA",
  "target_entry_id": 42,
  "reason": "operator-approved contextual downgrade",
  "operator_signature": "ed25519:...",
  "timestamp": "..."
}
```

📑 **Structural Principle:** Never mask structural interventions or parameter shifts within standard ledger results. Overrides and runtime adjustments must remain fully auditable, revealing precisely where human judgment or state-override constraints altered the machine's baseline path.

---

### 5.5 Hash-Chain Immutability & Fork Lineage

**Single-node chain:**

```json
{
  "chain_id": "genesis_router",
  "entry_id": 42,
  "prev_hash": "sha256_of_entry_41",
  "fork_parent_hash": null,
  "timestamp": "...",
  "payload": { ... }
}
```

**Fork lineage (Phase 3):**

| Field              | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| `chain_id`         | Identifies which node or fork produced the chain |
| `entry_id`         | Monotonically increasing within chain            |
| `prev_hash`        | Links to previous entry (integrity)              |
| `fork_parent_hash` | Links to parent checkpoint (ancestry)            |
