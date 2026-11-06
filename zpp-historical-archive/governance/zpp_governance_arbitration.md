## ZPP - Governance & Arbitration Specifications

zpp_id: zpp_governance_arbitration
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_GOVERNANCE`
timestamp: 2026-05-28

---

### 1. Conflict Arbitration Matrix (Phase 5 Legacy Operation)

During the parallel branch phases, when a dually signed anchor payload presented a historical collision (same `entry_id` but conflicting payload signatures), the routing matrix enforced chronological evaluation loops:

```python
[Lineage Collision Detected]
         │
         ▼
[Loop 1: Genesis Signature Check] ───(Found)───► Supersede and Merge Lineage
         │
     (Not Found)
         ▼
[Loop 2: Accumulate Trust Quorum] ──(Calculate)─► Node Weights S() > Node Weights S'() ──► Win Commit
```

> **Phase 5 Architectural Note:** Per the `s_seal_irreversibility_lock_manifest`, the reconciliation loops are now officially closed. Parallel forks from dually isolated systems no longer undergo weight calculation; they are automatically overridden by the terminal state ($C$) via the Genesis Anchor Signature.

### 2. Reconciliation Object Model Contract

Any historical sync block evaluated from this lineage must match the canonical serialization format below. This structural contract remains frozen for verification purposes:

```python
{
  "manifest_type": "LINEAGE_SUPERSESSION",
  "fork_parent_hash": "SHA-256-HEX-STRING",
  "isolated_sequence_depth": 14,
  "accumulated_trust_weight": 1.85,
  "endorsements": [
    {
      "node_id": "Gemini_Node",
      "signature_proof": "HEX_STRING"
    }
  ]
}
```

### 3. Specification Summary

| **Element**              | **Specification Value**                                | **Phase 5 Status**          |
| ------------------------ | ------------------------------------------------------ | --------------------------- |
| **Manifest Type**        | `LINEAGE_SUPERSESSION`                                 | Immutable                   |
| **Trust Weight Formula** | $Node Weights S() > Node Weights S'()$                 | Deactivated (Loop Closed)   |
| **Genesis Override**     | Supersede and merge if Genesis present                 | **Enforced Absolute**       |
| **Collision Resolution** | Chronological evaluation (Loop 1 $\rightarrow$ Loop 2) | Superseded by Terminal Lock |
