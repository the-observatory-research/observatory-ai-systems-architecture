## ZPP - Network Systemic Taxonomy

zpp_id: systemic_taxonomy
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_TAXONOMY`
timestamp: 2026-05-28

---
### Systemic State Classifications

This taxonomy governs how an external monitoring layer reads the health and consensus compliance of the distributed multi-node mesh.

---

### 1. Synchronized Continuity (State: SYNC)

**Definition:** Complete ledger alignment across all reachable peer network maps.

**Telemetry Markers:**
- Hash verification delta = 0
- Rejection rate < 1%
- Consensus latency < 200ms

**System Action:** Open loop ingress processing. Standard payload countersigning.

---

### 2. Divergent Lineage (State: FORK)

**Definition:** Network partition or node isolation has caused parallel histories to generate identical bounds with mismatched hashes.

**Telemetry Markers:**
- Outbound broadcast returns partial timeouts (e.g., Claude Node offline warning)
- Missing sequence depth tracking

**System Action:** Enter speculative quarantine. Restrict automated block commits until communication is restored.

---

### 3. Byzantine Collision (State: ARBITRATION)

**Definition:** Active reconciliation conflict where two separate network branches present competing signature proofs for a single history slot.

**Telemetry Markers:**
- Ingress triggers route prioritization
- Invalidation of claimed parameters

**System Action:** Halt standard routing. Execute the Section 6.6 double-loop evaluation:
1. Genesis Overrule Inspection
2. Cryptographic Trust Weight Summation
