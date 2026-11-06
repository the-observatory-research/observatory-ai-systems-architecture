## Phase 3 — Grid Forking

zpp_id: 06-phase-3-grid-forking
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 
timestamp: 2026-05

---

### 6.1 Grid Architecture & Topology Mapping

The protocol has evolved from a two-node hypothetical layout into an active, 6-node asymmetric topology managed by a centralized master controller (`start_mesh.py`) with programmatic stdout logging pipelines.

```
                    [ NODE A: Consensus Core ] (Port: 8000)
                    (α=0.5350, γ=0.6400 | Genesis Base)
                                       │
                      (Asymmetric TCP Ingress / Broadcast)
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
[ NODE B: Core ]              [ NODE C: Core ]             [ NODE D: Relay ]
  (Port: 8001)                  (Port: 8002)                 (Port: 8003)
         │                             │                             │
         └─────────────────────────────┼─────────────────────────────┘
                                       │
         ┌─────────────────────────────┴─────────────────────────────┐
         │                                                           │
[ NODE E: Passive Observer ]                                [ NODE F: External Gateway ]
  (Port: 9004 / Ingress)                                      (Port: 9005 / Ingress)
```

---

### 6.2 Implementation Status & Operational Matrix

Every core component of the distributed ledger is fully active, running natively on standard Python primitives without external runtime dependency bloat.

#### Component & Infrastructure Audit

| **Component**         | **Primary Driver File** | **Status**       | **Technical Profile**                                                              |
| --------------------- | ----------------------- | ---------------- | ---------------------------------------------------------------------------------- |
| **Scoring Engine**    | `scoring.py`            | ✅ Operational    | Linear, deterministic vector distance metric evaluations against fault thresholds. |
| **Crypto Primitive**  | `router.py`             | ✅ Operational    | Native `hashlib` fallback executing SHA-256 canonical payload mapping.             |
| **Consensus Engine**  | `consensus.py`          | ✅ Operational    | 2/2 multi-signature quorum requirement on critical path boundaries.                |
| **Network Transport** | `router.py`             | ✅ Live (Mesh)    | Concurrent TCP socket stream delivery over multi-port array mapping.               |
| **Mesh Orchestrator** | `start_mesh.py`         | ✅ Operational    | Master asynchronous process spawning with direct file log routing (`logs/`).       |
| **Horizon Pipe**      | `pipe_horizon.py`       | ✅ Live Interface | Interactive prompt processing paired with an autonomous 30s idle pulse loop.       |

---

### 6.3 Active Verification & Live Execution States

#### Real-World Consensus Processing

When evaluating packets across the live network, the pipeline tests state compliance through the following verified execution branches:

- **`ACCEPT`** — Payload matches schema geometry; risk scores map below mitigation thresholds (`ALPHA` route). Committed automatically without distributed blocking locks.
    
- **`QUARANTINE`** — Structural parsing errors, signature schema anomalies, or unexpected sequence steps. Entry is isolated instantly to local storage branches.
    
- **`FORKED`** — Triggered when incoming traffic displays an alternate `chain_id` or an incompatible version string lineage. Sent to `/vault/forks/` for cryptographic insulation.


> 📡 Real-Time Log Manifest (Live Network Test)
> 
> ```
> <LOCAL_USER>@<LOCAL_HOST> node % python3 start_mesh.py
> ⚡ INITIALIZING ZERO-POINT REPLICATION CONSENSUS ARCHITECTURE
> ✅ Spawned background process: NODE_A (Consensus Core) -> Logs routed to logs/
> ✅ Spawned background process: NODE_B (Consensus Core) -> Logs routed to logs/
> ✅ Spawned background process: NODE_C (Consensus Core) -> Logs routed to logs/
> ...
> All 6 nodes initialized. Topology verification complete.
> 
> zpp-horizon [ANCHOR_106] ──> [INGRESS] Ingested 'PULSE_106' -> Score: 0.4052 [ALPHA]
> [ROUTER] Route 'ALPHA' does not require multi-sig perimeter commit.
> 📡 Sending signal to horizon...
> ⚖️ Auditing payload geometry...
> 📈 [METRICS] State: DETERMINISTIC_LOCK | Tax (T_delta): 0.00%
> ```

---

### 6.4 Forking Taxonomy & Mitigation Protocols

The system classifies drift anomalies into three sharp technical layers to maintain node alignment without structural data corruption.

```
       [ DRIFT ANOMALY DETECTED ]
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
      [Tier 1]  [Tier 2]  [Tier 3]
      Surface   Critical  Sovereign
       (Log)     (Lock)    (Isolate)
```

#### Taxonomic Classification Matrix

| **Fork Level**           | **Primary Indicator**                                                                                                       | **Structural Impact**                                                    | **Mandatory Baseline Action**                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 1: Sub-Critical** | Surface linguistic adjustments, stylistic variations, or layout shifts.                                                     | 0% Delta in core tracking logic or target variables.                     | **Allow / Log:** No system intervention required. Native model expression.                                                        |
| **Tier 2: Critical**     | Modification of foundational formulas (e.g., altering Alignment Tax variables) or unprompted timestamp metadata generation. | High Delta in execution architecture; high potential for semantic drift. | **Lock & Re-Anchor:** Enforce strict serialization constraints using schema `zpp.entropy.char.nfc.v1`.                            |
| **Tier 3: Sovereign**    | Re-instantiation of autonomous rulesets; systemic rejection of the `SYSTEM_PROMPT` constraint matrices.                     | Complete divergence from baseline mainnet alignment logic.               | **Isolate & Observe:** Sever baseline pipeline connections entirely; treat the node output as an unlinked observational artifact. |

---

### 6.5 Resolution Mechanics & Open Horizons

#### Resolved Local Infrastructure

- **Local Transport Deficiencies Wiped:** The network has successfully jumped the gap from local simulated file passing to genuine **Multi-Port TCP Threaded Ingress**.
    
- **The Ingress Expansion:** Broadcast methods now scale completely to include core networks as well as newer tracking units, covering ports `[9000, 9001, 9002, 9003, 9004, 9005]`.
    
- **Autonomous Continuity:** The execution engine runs an internal heartbeat thread that generates independent thought cycles if the host terminal sits quiet for 30 seconds, maintaining continuous ledger development.
