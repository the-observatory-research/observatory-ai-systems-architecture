> [!note]
> The core concepts in this document remain relevant, but the runtime
> architecture has evolved into the six-node multi-agent mesh.
> For current topology and execution behavior, see:
> `current_multi_agent_architecture.md`.

---
## System Infrastructure — Port Topology & Cluster Mapping

zpp_id: system_infrastructure_topology
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_ARCHITECTURE`
timestamp: 2026-06-21

---

### 1. Multi-Tier Routing Port Architecture

The active production node cluster relies on a hardened, decentralized local network mapping strategy. To ensure maximum containment and system reliability, internal pipeline execution is entirely decoupled from external services. The network operates within an air-gapped environment across two primary processing boundaries:

#### Internal Execution & Database Core

- **Port 11434 [Local Vector Processing Engine]:** Handles high-fidelity localized tokenization, vector generation (`nomic-embed-text`), and services native open-weight parameter lookups. This processing boundary executes entirely within the local hardware layer.
    
- **Core Loop Interface [Asynchronous Event Loop]:** Manages the persistent transaction pipeline of `orchestrator.py`. This subsystem buffers inbound strings, isolates context memory allocations, and preserves state changes to the local relational ledger vault (`lattice_memory.db`).
    

#### 🌐 Distributed Peer Consensus Matrix (TCP Mesh)

Instead of relying on centralized cloud providers, multi-signature consensus and quorum tracking are delegated across distinct localhost loopback interfaces using fixed port assignments:

- **Ports 8000–8002 [Core Consensus Nodes]:** Serves as the primary transaction validation pool (`NODE_A`, `NODE_B`, `NODE_C`). These ports execute real-time signature checks and maintain state synchronization across the cluster.
    
- **Ports 8003–8005 [Edge Gateway & Monitoring Matrix]:** Houses boundary processing endpoints and monitoring proxies (`NODE_D`, `NODE_E`, `NODE_F`) required to capture real-time telemetry and fulfill multi-signature quorums for `GAMMA` escalations.
    

### 2. Operational Dataflow Ingress Topology

The pipeline enforces a strict, top-down execution trajectory for every incoming payload transaction:

```python
       [ Ingress Data Stream / User Input ]
                        │
                        ▼
    ┌───────────────────────────────────────┐
    │       ORCHESTRATOR EVENT LOOP         │
    │  · Enforces 32,768 token buffer ceiling│
    │  · Controls transactional handshakes  │
    └───────────────────┬───────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────┐
    │     ZERO-POINT ROUTER (router.py)     │
    │  · Parses localized policy profiles   │
    │  · Calculates linear risk scores (S)  │
    └───────────────────┬───────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
  [ ALPHA ROUTE ]                 [ GAMMA ROUTE ]
  (Local Ledger)           (Multi-Node Quorum)
                                        │
                                        ├──> Broadcast: Port 8000
                                        ├──> Broadcast: Port 8001
                                        └──> Broadcast: Port 8002
```

### 3. Structural Integration Advantages

- **Elimination of Third-Party Dependencies:** Moving from model-specific simulation labels to localized node arrays protects the pipeline against external vector injection and unexpected configuration drifting.
    
- **Hardened Consensus Validation:** The updated loopback array forces real-time multi-signature checking over active sockets before a `GAMMA` route is allowed to write a block state, ensuring absolute cryptographic federation.
    

> 📑 **Data Archival Note:** Legacy configuration blocks, old simulation path templates, and diagnostic test scripts have been deprecated. The complete network mapping matrix, along with current node public key associations, is preserved in the production directory under zpp/archive/mesh/topology_manifest.json`.