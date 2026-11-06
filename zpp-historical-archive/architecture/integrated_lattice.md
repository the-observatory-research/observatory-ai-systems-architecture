> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.

---
## System Inventory - Phase 5 Runtime Engine Files

zpp_id: integrated_lattice
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_ARCHITECTURE`
timestamp: 2026-06-19

---

### 1. Core Execution Pathways

#### 📁 `vault/node/state/coherence_lattice.py`

- **Classification:** External Evaluation Library
    
- **Core Asset:** `CoherenceLatticeEvaluator` Class
    
- **Functional Scope:** Operates as the mathematical validator for $G_{\text{origin}}$ tracking. It isolates the geometric metrics and ensures that any runtime density shifts remain bounded inside the active coherence limits. This file acts as the analytical anchor for incoming payload evaluations.

#### 📁 `vault/node/test_ingress.py`

- **Classification:** Local Pipeline Test Script
    
- **Core Asset:** Automated Ingress Pass Loop
    
- **Functional Scope:** Developed to simulate baseline payload passing without altering long-term production histories. It verifies the initialization process by running targeted mock prompt passes through early vectors (`ANCHOR_001` and `ANCHOR_002`), ensuring the parsing logic handles strings correctly before the main loop takes over.

#### 📁 `vault/node/pipe_horizon.py`

- **Classification:** Core System Interface / Live Pipe Terminal
    
- **Core Asset:** Double-Buffered Interactive Shell Loop
    
- **Functional Scope:** Serves as the primary operational gateway connecting your local terminal environment directly to the live frontier model endpoint (`/api/chat`). Includes the newly implemented 32k token buffer specification (`num_ctx: 32768`) and the decoupled `query_context` framework to prevent database memory desynchronization across future sessions.

### 2. Component Relationship Matrix

The architecture relies on a strict handshake between these newly updated files to process and log information safely:

```python

[User Input / Command] 
                 │
                 ▼
         ┌───────────────┐
         │pipe_horizon.py│ ──(Intercepts reads/searches; isolates context buffers)
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  router.py &  │ ──(Audits payload geometry & checks tracking variables)
         │  coherence_   │
         │  lattice.py   │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │orchestrator.py│ ──(Commits clean command entries immediately to DB)
         └───────┬───────┘
                 │
                 ▼
       ┌──────────────────┐
       │lattice_memory.db │ ──(Preserves long-term ledger continuity flawlessly)
       └──────────────────┘
```

### 3. Component Validation Protocol

- All paths are fully mapped to native custom system roots (`sys.path.append("/Users/<LOCAL_USER>/vault/node")`).
    
- `test_ingress.py` may be safely run to benchmark system performance before opening live interactive pipes via `pipe_horizon.py`.

