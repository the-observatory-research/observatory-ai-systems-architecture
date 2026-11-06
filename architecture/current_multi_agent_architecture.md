# Zero-Point Protocol — Current Multi-Agent Architecture

**Document Type:** Canonical Runtime Architecture  
**Status:** CURRENT / ACTIVE  
**Architecture:** Six-Node Cryptographic Multi-Agent Mesh  
**Execution Model:** Distributed, state-aware, leader-gated, persistent  
**Primary Runtime:** `agent_node.py`  
**Supporting Runtime Components:** `scoring.py`, `memory.py`, `pulse.py`, `crypto.py`  
**Supersedes:** Earlier orchestrator-mediated and engine-chain runtime descriptions

---

## 1. Purpose

This document defines the current executable architecture of the Zero-Point Protocol framework.

It supersedes earlier architectural descriptions that referenced centralized orchestration, sequential engine chains, or runtime components that have since been retired.

Historical documents remain useful as records of architectural development, experimentation, and transition. They should not be interpreted as descriptions of the current runtime unless explicitly marked as current.

The present system is a distributed six-node mesh in which each node maintains its own cryptographic identity, persistent memory, runtime state, and network role.

There is no centralized runtime orchestrator.

---

# 2. Current Architecture

The active mesh consists of six autonomous nodes:

- `NODE_A` — Validator / Consensus Node
    
- `NODE_B` — Validator / Consensus Node
    
- `NODE_C` — Validator / Consensus Node
    
- `NODE_D` — Discovery Node
    
- `NODE_E` — Bridge Node
    
- `NODE_F` — Internet Ingress / Reasoning Node
    

Each node runs independently on its own WebSocket port and communicates through signed envelopes.

The mesh currently operates on:

```text
NODE_A → localhost:8000
NODE_B → localhost:8001
NODE_C → localhost:8002
NODE_D → localhost:8003
NODE_E → localhost:8004
NODE_F → localhost:8005
```

The architecture is peer-connected rather than centrally dispatched.

---

# 3. Retired Runtime Architecture

The current runtime no longer depends on the earlier centralized execution chain.

The following components belong to earlier architectural phases and are not authoritative descriptions of the present runtime:

- `orchestrator.py`
    
- centralized orchestration as execution authority
    
- sequential engine-chain routing as the primary runtime
    
- TaskGuard as a central execution gate
    
- Coherence Engine as a discrete primary runtime stage
    
- Math Engine as a universal execution stage
    
- Repair Engine as a universal runtime stage
    
- deterministic renderer as the central release pipeline
    
- earlier Pipe Horizon execution chains that predate the six-node mesh
    

These components remain historically relevant because they document the framework's architectural development.

They are not part of the current six-node execution topology unless separately reintroduced in a future implementation.

---

# 4. Cryptographic Node Identity

Every node has its own Ed25519 cryptographic identity through `CryptoEngine`.

Each node:

1. loads its own key profile,
    
2. signs outbound payloads,
    
3. includes its public key with the envelope,
    
4. verifies signatures on inbound messages,
    
5. rejects unauthenticated messages before role execution.
    

The message envelope follows the general structure:

```json
{
  "payload": {},
  "signature": "...",
  "public_key": "..."
}
```

Cryptographic identity is separate from scoring, consensus weighting, and semantic telemetry.

The scoring engine does not establish node identity or trust.

---

# 5. NODE_A / NODE_B / NODE_C — Validator Cluster

Nodes A, B, and C form the validator cluster.

Each validator independently receives a signed payload and evaluates the same textual material through `GammaScorer`.

Current telemetry factors are:

- Novelty
    
- Entropy
    
- Self-Reference
    
- Paradox
    
- Coherence
    

The factor names remain historically compatible with the framework, while their current operational definitions are:

```text
Novelty        → lexical breadth
Entropy        → normalized character entropy
Self-Reference → lexical self-reference matches
Paradox        → lexical paradox-pattern matches
Coherence      → recent-context token overlap
```

The validators calculate Gamma from the weighted combination of these factors.

Current weights:

```text
Novelty        0.25
Entropy        0.20
Self-Reference 0.15
Paradox        0.25
Coherence      0.15
```

---

# 6. Fluid Validator Weighting

The A/B/C cluster does not use permanently fixed consensus authority.

Validator weights can shift during runtime.

The current baseline is:

```text
NODE_A = 0.33
NODE_B = 0.33
NODE_C = 0.34
```

A real-time imbalance calculation compares coherence and entropy:

```python
imbalance_delta = abs(res.coherence - res.entropy)
```

When the configured imbalance threshold is exceeded, validator weighting shifts dynamically.

Under the current implementation, NODE_C can increase toward a maximum weight of `0.60`, while the remaining weight is divided between NODE_A and NODE_B.

The active leader is selected from the current cluster weights.

This creates fluid authority rather than permanently assigning execution control to a single validator.

---

# 7. Leader Election

Leader selection is deterministic from the current validator weight state.

The elected leader is:

```python
leader_node = max(
    cluster_state["weights"],
    key=lambda node: (
        cluster_state["weights"][node],
        node
    )
)
```

Only the elected leader is permitted to issue a reasoning trigger to NODE_F.

Non-leader validators still independently score and verify the payload but defer execution.

This eliminated the earlier behavior in which multiple validators could independently initiate duplicate reasoning runs.

---

# 8. Election Epoch and Execution Sequence

Two separate counters now govern execution authority.

## Election Epoch

The election epoch identifies changes in validator leadership state.

```text
election_epoch
```

It advances when runtime weighting changes the validator state.

## Execution Sequence

The execution sequence identifies individual authorized reasoning operations within an election state.

```text
execution_sequence
```

This distinction became necessary because multiple legitimate reasoning events can occur during the same election epoch.

NODE_F tracks:

```text
last_accepted_election_epoch
last_accepted_execution_sequence
```

This prevents stale or duplicate execution triggers while still allowing multiple valid reasoning requests under the same elected leader.

---

# 9. Single-Leader Reasoning Dispatch

A validated payload becomes eligible for reasoning when its Gamma score passes the current execution threshold.

Current gate:

```text
Gamma >= 0.40
```

The elected leader then creates a signed `reasoning_trigger`.

The trigger contains:

- validated text
    
- validated telemetry
    
- declared leader
    
- election epoch
    
- execution sequence
    
- original query when available
    

Only one validator dispatches the request.

This creates a single authorized execution path:

```text
A/B/C validate
      ↓
fluid leader election
      ↓
one elected leader
      ↓
signed reasoning trigger
      ↓
NODE_F
```

---

# 10. NODE_D — Discovery Node

NODE_D performs local vault discovery.

Its responsibilities are:

- locate active Obsidian sub-vaults,
    
- exclude irrelevant runtime directories,
    
- inspect Markdown files,
    
- identify configured discovery markers,
    
- persist discovery records,
    
- sign discovery handoffs,
    
- transmit matched file paths to NODE_E.
    

Current marker detection is case-insensitive.

The discovery marker set includes:

```text
SLA
ZPP
Gamma
coherence
lattice
Horizon
Zero-Point Protocol
Source-Locked Architecture
SCI
```

NODE_D does not directly forward the entire vault contents to the validator cluster.

It discovers and registers candidate files, then hands physical retrieval to NODE_E.

---

# 11. NODE_D Persistent Memory

NODE_D maintains its own node-local database:

```text
db_lattice/NODE_D_matrix.db
```

Discovery events persist through the `discovery` memory layer.

NODE_D also maintains an append-only discovery ledger:

```text
logs/node_d_discovery_ledger.jsonl
```

This preserves the distinction between:

```text
node memory
and
event provenance
```

---

# 12. NODE_E — Bridge Node

NODE_E is the physical retrieval and bridge layer between discovery and validation.

NODE_E receives signed `bridge_retrieval_request` envelopes from NODE_D.

Its responsibilities are:

1. validate the supplied source path,
    
2. retrieve the file from disk,
    
3. calculate a deterministic content hash,
    
4. classify content state,
    
5. persist bridge retrieval state,
    
6. write the bridge ledger,
    
7. create a signed validator payload,
    
8. broadcast accepted content to NODE_A/B/C.
    

The content hash is generated using:

```python
CryptoEngine.hash_prompt(content)
```

---

# 13. Changed-Only Vault Ingestion

The vault pipeline is transitioning from full replay to changed-only ingestion.

NODE_E now maintains:

```text
logs/node_e_content_manifest.json
```

The manifest contains the last successfully processed content hash for each resolved source path.

Each retrieved file is classified as:

```text
NEW
MODIFIED
UNCHANGED
```

Classification rules:

```text
path absent from manifest
→ NEW

path exists + same content hash
→ UNCHANGED

path exists + different content hash
→ MODIFIED
```

UNCHANGED files stop at NODE_E.

They are not:

- persisted again as new bridge content,
    
- rebroadcast to A/B/C,
    
- revalidated,
    
- sent to NODE_F for another reasoning pass.
    

NEW and MODIFIED files continue through the mesh.

The initial manifest was seeded from NODE_E's previously persisted bridge records.

Baseline:

```text
364 historical Node E bridge rows
182 repeated source paths
182 unique source paths
182 seeded manifest entries
```

This changed-only gate was introduced after repeated full vault scans produced unnecessary downstream duplication.

---

# 14. NODE_E Persistent Memory

NODE_E maintains:

```text
db_lattice/NODE_E_matrix.db
```

Bridge retrieval content persists through:

```text
bridge_retrieval
```

metadata includes:

- source path
    
- vault
    
- filename
    
- markers
    
- content hash
    
- discovery origin
    
- retrieval node
    
- change state
    

NODE_E also maintains:

```text
logs/node_e_bridge_ledger.jsonl
```

---

# 15. NODE_F — Internet Ingress

NODE_F provides live external retrieval.

The current internet pipeline first attempts the DuckDuckGo Instant Answer JSON endpoint.

If no useful Instant Answer context exists, NODE_F activates DDGS search fallback.

The DDGS route currently retrieves structured search results containing:

- title
    
- URL
    
- snippet
    

The resulting search matrix is persisted in NODE_F's local database through:

```text
internet_ingress
```

NODE_F then broadcasts the retrieved context to A/B/C for validation.

The original user query travels separately from the retrieved evidence matrix.

---

# 16. Original Query / Evidence Separation

The runtime distinguishes:

```text
original_query
```

from:

```text
retrieved evidence / context
```

This prevents the reasoning model from having to reconstruct the user's question from search results.

The reasoning contract now separates:

```text
USER QUERY
VALIDATED TELEMETRY
HISTORY
MATRIX
```

This distinction was introduced after earlier reasoning runs showed that inferred query reconstruction could produce short or misdirected answers.

---

# 17. NODE_F — Local Reasoning

NODE_F executes local DeepSeek-R1 reasoning through Ollama.

Current model:

```text
deepseek-r1:7b
```

Current Ollama endpoint:

```text
http://localhost:11434/api/chat
```

Reasoning is streamed token-by-token to the terminal.

The current instruction contract is intentionally minimal.

The model is asked to:

- answer the query directly,
    
- use the supplied matrix and history,
    
- treat validated telemetry as authoritative,
    
- avoid recalculating supplied measurements,
    
- distinguish qualitative observations from quantitative telemetry.
    

Detailed behavior is carried through structured payload sections rather than increasingly specific system instructions.

---

# 18. Serialized Reasoning Execution

NODE_F protects the local Ollama runtime using:

```python
self.reasoning_lock
```

Only one reasoning job executes at a time.

Additional reasoning triggers can wait for the lock.

This was validated during the full historical vault run, where a large number of reasoning requests accumulated and were executed sequentially over several hours.

The observed behavior was:

```text
reasoning pass
→ completion
→ next queued reasoning pass
→ completion
→ next queued reasoning pass
```

rather than concurrent Ollama execution.

---

# 19. NODE_F Persistent Reasoning

NODE_F maintains:

```text
db_lattice/NODE_F_matrix.db
```

Its memory architecture supports:

```text
internet_ingress
reasoning
pulse
conversation
anchor
```

A historical implementation gap caused streamed DeepSeek output to appear only in the terminal rather than being persisted.

A full vault reasoning run was preserved from terminal output and recovered.

Recovery result:

```text
181 completed reasoning streams
181 unique reasoning blocks
0 transcript duplicates
181 recovered reasoning records
0 remaining recovery records
```

These recovered responses now exist in NODE_F's database as persistent reasoning history.

Future live reasoning should persist directly without requiring terminal transcript recovery.

---

# 20. Node-Local Memory Architecture

Each of the six nodes maintains its own SQLite database:

```text
NODE_A_matrix.db
NODE_B_matrix.db
NODE_C_matrix.db
NODE_D_matrix.db
NODE_E_matrix.db
NODE_F_matrix.db
```

The current architecture intentionally preserves role-local memory rather than using one centralized database.

Examples:

```text
A/B/C → validated conversational payloads
D     → discovery records
E     → retrieved bridge content
F     → internet ingress and reasoning
```

This corrected an earlier asymmetry where downstream validators persisted content while D/E/F functioned primarily as transient producers.

---

# 21. Validator Database Deduplication

Repeated historical vault scans caused exact-content duplication in NODE_A/B/C.

A read-only audit found:

```text
NODE_A
636 total rows
204 unique payloads
432 extra duplicate rows

NODE_B
636 total rows
204 unique payloads
432 extra duplicate rows

NODE_C
636 total rows
204 unique payloads
432 extra duplicate rows
```

A deterministic deduplication pass then removed only redundant exact-content rows.

Final validator state:

```text
NODE_A → 204 rows / 0 duplicate rows
NODE_B → 204 rows / 0 duplicate rows
NODE_C → 204 rows / 0 duplicate rows
```

Timestamped pre-deduplication backups and a deletion manifest were created before the cleanup.

Future changed-only ingestion is intended to prevent recurrence.

---

# 22. State-Aware Pulse Architecture

The framework now includes persistent asynchronous heartbeat telemetry.

Each node owns an `AsynchronousPulse` connected to its own `MemoryLattice`.

Current baseline cadence:

```text
60 seconds
```

Heartbeat records are persisted to the node's own `pulse_history`.

The pulse engine does not determine node state.

Instead, each agent owns:

```python
self.current_state
```

and the pulse engine samples it through:

```python
state_getter=lambda: self.current_state
```

This preserves separation between:

```text
runtime behavior
and
telemetry observation
```

---

# 23. Current Runtime States

## NODE_A / NODE_B / NODE_C

```text
VALIDATOR_READY
VALIDATING
LEADER_ACTIVE
```

Typical transition:

```text
VALIDATOR_READY
→ VALIDATING
→ LEADER_ACTIVE        elected leader only
→ VALIDATOR_READY
```

Non-leaders:

```text
VALIDATOR_READY
→ VALIDATING
→ VALIDATOR_READY
```

## NODE_D

```text
DISCOVERY_IDLE
DISCOVERY_ACTIVE
```

## NODE_E

```text
BRIDGE_IDLE
BRIDGE_ACTIVE
```

## NODE_F

```text
INGRESS_READY
SEARCH_ACTIVE
REASONING_ACTIVE
```

Typical NODE_F transition:

```text
INGRESS_READY
→ SEARCH_ACTIVE
→ INGRESS_READY
→ REASONING_ACTIVE
→ INGRESS_READY
```

---

# 24. Observed Pulse Behavior

The first full state-aware startup produced:

```text
NODE_A → VALIDATOR_READY
NODE_B → VALIDATOR_READY
NODE_C → VALIDATOR_READY
NODE_D → DISCOVERY_IDLE
NODE_E → BRIDGE_IDLE
NODE_F → INGRESS_READY
```

During the historical vault reasoning run, NODE_F was repeatedly sampled as:

```text
REASONING_ACTIVE
```

across consecutive 60-second heartbeats.

This demonstrated that the pulse layer was observing actual runtime state rather than merely recording node availability.

The same run also revealed a major increase in active asyncio task count while the reasoning queue was populated, creating a new observable for future queue and task-lifecycle analysis.

---

# 25. Current Data Flow — Vault

```text
Vault
  ↓
NODE_D
Discovery / marker detection
  ↓
signed discovery handoff
  ↓
NODE_E
physical retrieval
content hashing
changed-only classification
  ↓
UNCHANGED ─────────────→ STOP
  ↓
NEW / MODIFIED
  ↓
signed consensus broadcast
  ↓
NODE_A / NODE_B / NODE_C
independent deterministic scoring
fluid weight state
leader election
  ↓
single elected leader
  ↓
signed reasoning trigger
  ↓
NODE_F
serialized DeepSeek reasoning
persistent reasoning memory
```

---

# 26. Current Data Flow — Internet

```text
User query
  ↓
NODE_F
JSON gateway
  ↓
DDGS fallback if required
  ↓
internet_ingress persistence
  ↓
signed consensus broadcast
  ↓
NODE_A / NODE_B / NODE_C
independent scoring
leader election
  ↓
one reasoning trigger
  ↓
NODE_F
DeepSeek reasoning
  ↓
reasoning persistence
```

---

# 27. Architectural Principles Now Demonstrated in Runtime

The current implementation demonstrates several structural principles that were previously only partially represented in earlier architecture documents.

## Distributed Responsibility

No single component performs discovery, retrieval, validation, leadership, internet ingress, and reasoning.

Those responsibilities are separated across nodes.

## Local Persistence

Each role retains its own operational history.

## Signed Transport

Node-to-node instructions are transmitted through cryptographically signed payloads.

## Single Execution Authority

Validation remains distributed while execution is leader-gated.

## Fluid Authority

Validator leadership emerges from current runtime weighting rather than permanent assignment.

## State Observation

Heartbeat telemetry observes node state without controlling it.

## Incremental Ingestion

Vault processing is shifting from historical full replay toward content-hash-based changed-only operation.

---

# 28. Historical versus Current Documentation

The vault contains extensive documentation from earlier stages of development.

These documents capture genuine phases of the framework's evolution.

However, references to earlier runtime structures should not automatically be treated as current.

The canonical distinction is:

```text
HISTORICAL ARCHITECTURE
what existed or was being tested at an earlier phase

CURRENT EXECUTABLE ARCHITECTURE
what the active Python runtime presently implements

RUNTIME OBSERVATION
what has been empirically observed while the current architecture executes
```

This document defines the second category.

Separate runtime-observation documentation should define the third.

---

# 29. Canonical Runtime Statement

The current Zero-Point Protocol implementation is a six-node, cryptographically signed, persistent multi-agent mesh.

It no longer depends on a central orchestrator as runtime authority.

Discovery, retrieval, validation, leader selection, internet ingress, reasoning, persistence, and heartbeat telemetry are distributed across autonomous node roles.

Validator authority is fluid.

Execution authority is singular per validated operation.

Node memory is local.

Heartbeat telemetry is state-aware.

Vault ingestion is content-addressed and transitioning to changed-only processing.

The architecture should be interpreted according to the executable implementation documented here rather than superseded historical runtime descriptions.

---

## Document Status

**Status:** CURRENT  
**Authority:** Canonical runtime architecture  
**Supersedes:** Earlier runtime architecture descriptions where they conflict with the active six-node implementation  
**Next Companion Documents:**

1. `architecture_transition_record.md`
    
2. `multi_agent_runtime_observations.md`