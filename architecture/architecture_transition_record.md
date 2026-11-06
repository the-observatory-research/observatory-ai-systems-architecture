# Zero-Point Protocol — Architecture Transition Record

**Document Type:** Architectural Lineage Record  
**Status:** CURRENT  
**Scope:** Transition from earlier centralized and engine-based architectures to the current six-node multi-agent mesh  
**Companion Document:** `current_multi_agent_architecture.md`  
**Historical Material:** `historical-archive/`

---

## 1. Purpose

This document records the architectural transition that produced the current Zero-Point Protocol multi-agent framework.

The Zero-Point Protocol was not designed in a single static form. Its present architecture emerged through repeated implementation, runtime testing, failure analysis, restructuring, and removal of components that were no longer necessary.

Earlier architectural documents therefore describe real stages of development but do not necessarily describe the current executable system.

This record establishes the lineage between those stages.

The distinction is:

```text
Historical implementation
        ↓
Runtime observation
        ↓
Architectural change
        ↓
Current implementation
```

Historical components are retained as evidence of development rather than silently rewritten as though they never existed.

---

# 2. Architectural Evolution

The framework progressed through several major structural phases.

At a high level:

```text
Early routing and scoring experiments
        ↓
deterministic engine-based processing
        ↓
Horizon / lifecycle architecture
        ↓
centralized orchestration
        ↓
distributed node experimentation
        ↓
cryptographically identified nodes
        ↓
six-node functional specialization
        ↓
fluid validator weighting
        ↓
single-leader execution
        ↓
node-local persistence
        ↓
state-aware pulse telemetry
        ↓
changed-only source ingestion
        ↓
CURRENT MULTI-AGENT MESH
```

These transitions were cumulative in knowledge but not necessarily cumulative in software components.

Some earlier mechanisms were retained.

Others were transformed.

Others were removed entirely after their function migrated into the distributed architecture.

---

# 3. Earlier Engine-Based Architecture

Earlier implementations represented system behavior as an explicit sequence of processing engines.

Components included structures such as:

- Recursive Reasoner
    
- TaskGuard
    
- Coherence Engine
    
- Math Engine
    
- deterministic renderer
    
- Repair Engine
    
- final verification stages
    
- release gates
    

These stages were useful for isolating individual forms of processing and observing where transformations introduced or corrected errors.

The architecture made processing order explicit.

A representative earlier pattern was:

```text
LLM
 ↓
Recursive Reasoner
 ↓
TaskGuard
 ↓
Coherence
 ↓
Math
 ↓
Deterministic Renderer
 ↓
TaskGuard Recheck
 ↓
Coherence Recheck
 ↓
Repair
 ↓
Final Verification
 ↓
Release
```

This architecture belongs to the framework's experimental lineage.

It is not the execution topology of the current system.

---

# 4. Horizon and Lifecycle Development

The Horizon phase introduced explicit lifecycle states, gates, persistence concepts, pulse cadence, and runtime state transitions.

This phase contributed several concepts that survived later architectural restructuring even when their original implementation did not.

Among them were:

- persistent state
    
- lifecycle observation
    
- cadence
    
- heartbeat behavior
    
- routing states
    
- state transitions
    
- execution boundaries
    
- deterministic release concepts
    

The important distinction is that a concept surviving does not imply that its original implementation remains active.

For example, heartbeat and state observation remain important in the current architecture, but they now exist as node-local asynchronous pulse telemetry rather than as a centralized Horizon execution authority.

---

# 5. Centralized Orchestration Phase

As components accumulated, coordination was previously mediated through centralized orchestration.

`orchestrator.py` represented this phase.

The orchestrator provided a single location from which multiple processing components could be sequenced and coordinated.

This was useful while the framework consisted primarily of callable engines.

However, once functionality began moving into independently executing nodes, centralized orchestration increasingly duplicated responsibilities that the nodes themselves could own.

The architectural question changed from:

```text
Which central component should call the next engine?
```

to:

```text
Which autonomous node owns this responsibility,
and what authenticated event causes the next transition?
```

That change ultimately made the orchestrator unnecessary as runtime authority.

---

# 6. Removal of `orchestrator.py`

`orchestrator.py` has been retired from the current runtime.

Its removal was not simply deletion of functionality.

Its responsibilities were redistributed.

Conceptually:

```text
CENTRAL ORCHESTRATOR

discovery coordination
validation coordination
execution routing
reasoning invocation
state progression

                ↓ redistributed into ↓

NODE_D
discovery

NODE_E
retrieval and bridge routing

NODE_A / NODE_B / NODE_C
validation and execution authority

NODE_F
internet ingress and reasoning

SIGNED NETWORK EVENTS
coordination between roles
```

The resulting system no longer requires a central process to determine every next action.

Coordination emerges from authenticated messages and role-specific behavior.

---

# 7. Transition from Engines to Agents

A major architectural transition occurred when responsibilities previously represented as engines became responsibilities of persistent agents.

An engine generally performs a function when called.

An agent in the current architecture instead possesses:

- identity,
    
- state,
    
- memory,
    
- network presence,
    
- role,
    
- event handling,
    
- persistence,
    
- independent execution.
    

This changed the framework from primarily:

```text
function → function → function
```

into:

```text
agent
  ↕
agent ↔ agent
  ↕
agent
```

The shift is structural rather than terminological.

The current nodes are independently running processes communicating across WebSockets.

---

# 8. Functional Specialization into Six Nodes

The current architecture stabilized around six primary roles.

```text
A / B / C
Validation and consensus cluster

D
Discovery

E
Bridge retrieval

F
Internet ingress and local reasoning
```

This division separated responsibilities that previously existed inside larger execution pipelines.

It also allowed each responsibility to develop its own:

- persistent memory,
    
- operational state,
    
- telemetry,
    
- cryptographic identity,
    
- failure boundary.
    

This became a significant architectural difference from the earlier engine chain.

---

# 9. Cryptographic Transport as Coordination

As node autonomy increased, trust could no longer depend solely on in-process function calls.

Node-to-node messages therefore became signed objects.

Ed25519 identity and signature verification moved coordination from implicit process trust toward authenticated message transport.

The resulting execution relationship became:

```text
node action
   ↓
structured payload
   ↓
cryptographic signature
   ↓
network transport
   ↓
signature verification
   ↓
role-specific execution
```

This mechanism now provides the coordination boundary previously supplied in part by centralized execution control.

---

# 10. Validator Cluster Development

Nodes A, B, and C became independent validators of the same incoming material.

Rather than having one component score a payload and directly invoke reasoning, each validator receives and evaluates the signed content independently.

This introduced a distributed validation layer.

The cluster then required a separate solution to a new problem:

```text
If all three validators accept the same event,
which one is allowed to initiate execution?
```

Early behavior allowed redundant downstream execution.

That behavior exposed the need to separate:

```text
distributed validation
```

from:

```text
singular execution authority
```

---

# 11. Fluid Weighting

Fixed validator authority was replaced by runtime weighting.

Initial cluster weights are close to balanced:

```text
NODE_A = 0.33
NODE_B = 0.33
NODE_C = 0.34
```

Current runtime logic can alter this distribution in response to measured telemetry.

The purpose of the weights is not to make validators semantically different copies of the same scoring engine.

They represent dynamic execution authority within the validator cluster.

The validator with the highest current weight becomes the elected leader.

This introduced a fluid leadership model.

---

# 12. Separation of Validation and Execution

A/B/C continue to validate independently.

Only one validator executes the downstream dispatch.

The architecture therefore became:

```text
                 ┌→ NODE_A ─┐
payload ─────────┼→ NODE_B ─┼→ validation
                 └→ NODE_C ─┘
                        ↓
                 leader selection
                        ↓
                ONE authorized dispatch
                        ↓
                     NODE_F
```

This resolved duplicate reasoning execution without removing distributed validation.

---

# 13. Election Epoch

Fluid weighting introduced another requirement: leadership changes needed an explicit identity.

The `election_epoch` was introduced to identify validator leadership state.

When weight adjustment changes the relevant cluster state, the election epoch advances.

NODE_F can reject execution requests originating from stale election state.

This established temporal ordering around leadership.

---

# 14. Execution Sequence

Runtime testing exposed a distinction that election epochs alone could not represent.

Multiple valid reasoning operations can occur while the same leader remains elected.

Therefore:

```text
election epoch
≠
execution identity
```

`execution_sequence` was added.

The resulting model is:

```text
Election Epoch
defines leadership state

Execution Sequence
defines an individual authorized execution
```

NODE_F tracks both values and rejects stale or duplicate reasoning triggers.

This was an architectural correction produced directly from runtime behavior.

---

# 15. NODE_F Serialization

Once leader gating successfully routed work to NODE_F, another resource boundary became visible.

Local Ollama reasoning should not execute an uncontrolled number of concurrent inference jobs.

NODE_F therefore uses an asynchronous reasoning lock.

```text
incoming reasoning jobs
        ↓
queue
        ↓
reasoning_lock
        ↓
one active Ollama execution
        ↓
next waiting execution
```

A large historical vault run later exercised this behavior at substantial scale.

The queue persisted for hours while DeepSeek processed requests sequentially.

The observed behavior demonstrated that serialization was functioning rather than allowing uncontrolled parallel inference.

---

# 16. Discovery and Retrieval Separation

Vault integration was divided between NODE_D and NODE_E.

NODE_D owns discovery.

NODE_E owns physical retrieval.

This separation prevents discovery logic from simultaneously becoming the retrieval, validation, and reasoning layer.

The resulting boundary is:

```text
NODE_D
"What relevant files exist?"

        ↓ signed handoff

NODE_E
"What content is at this verified path?"

        ↓ signed payload

A/B/C
"What does the validator telemetry report?"

        ↓ leader dispatch

NODE_F
"Perform the authorized reasoning operation."
```

This separation became a central characteristic of the current multi-agent topology.

---

# 17. Persistence Transition

Earlier node behavior revealed an asymmetry.

A/B/C were accumulating downstream content while some producer nodes were performing important operations without retaining equivalent role-local history.

The architecture was changed so that each node could preserve information appropriate to its role.

Current persistence includes:

```text
NODE_A/B/C
validated conversation content

NODE_D
discovery records

NODE_E
bridge retrieval content

NODE_F
internet ingress
reasoning output

ALL NODES
pulse telemetry
```

This transformed the mesh from a set of communicating processes into a system with distributed operational memory.

---

# 18. State-Aware Pulse Transition

Earlier heartbeat concepts evolved into an asynchronous node-local pulse system.

Initially, a heartbeat could establish only that the process was alive.

The pulse architecture was subsequently connected to each agent's actual `current_state`.

The pulse became an observer of runtime behavior.

Examples include:

```text
VALIDATOR_READY
VALIDATING
LEADER_ACTIVE

DISCOVERY_IDLE
DISCOVERY_ACTIVE

BRIDGE_IDLE
BRIDGE_ACTIVE

INGRESS_READY
SEARCH_ACTIVE
REASONING_ACTIVE
```

This changed heartbeat telemetry from simple liveness reporting into sampled operational-state telemetry.

---

# 19. Historical Vault Ingestion

The first large vault traversal was intentionally broad.

NODE_D discovered historical material.

NODE_E retrieved it.

A/B/C validated it.

NODE_F queued and reasoned over it.

The run produced a large body of local reasoning across the documented development history.

It also exposed several architectural weaknesses that were difficult to see at smaller scale.

These included:

- repeated file ingestion,
    
- validator database duplication,
    
- lack of direct reasoning persistence,
    
- very large reasoning queues,
    
- the need for clearer current-versus-historical documentation.
    

The vault run therefore became both a reasoning event and a stress test of the architecture.

---

# 20. Reasoning Persistence Correction

During the large vault run, NODE_F streamed its DeepSeek output to the terminal but did not persist those completed reasoning streams to its own database.

The reasoning itself was not lost because the terminal transcript had been preserved.

A recovery importer reconstructed:

```text
181 completed streams
181 unique transcript blocks
0 transcript duplicates
```

All 181 were subsequently imported into NODE_F's persistent memory.

The incident established a new architectural requirement:

```text
important agent output must not depend
on terminal visibility for persistence
```

Future reasoning persistence should occur as part of the normal execution path.

---

# 21. Validator Deduplication

Repeated vault ingestion had caused exact content to be stored multiple times in A/B/C.

The validator databases each reached:

```text
636 rows
```

while containing only:

```text
204 unique content payloads
```

Each database therefore contained:

```text
432 redundant rows
```

A deterministic cleanup retained one canonical copy of each exact payload.

After cleanup:

```text
NODE_A = 204 rows
NODE_B = 204 rows
NODE_C = 204 rows

Exact duplicate rows remaining = 0
```

Pre-cleanup database backups and a cleanup manifest preserved the original state.

---

# 22. Transition to Changed-Only Ingestion

Deduplication corrected historical database state but did not solve the source of duplication.

The ingestion architecture therefore changed.

NODE_E now maintains a persistent content manifest indexed by resolved file path.

Each file is classified according to its current hash:

```text
NEW
MODIFIED
UNCHANGED
```

The baseline manifest was seeded from existing NODE_E retrieval history.

Historical Node E state:

```text
364 usable bridge records
182 repeated source paths
182 unique source paths
```

The resulting manifest contains:

```text
182 baseline paths
```

Unchanged content can now terminate at NODE_E rather than repeatedly traversing the validator and reasoning mesh.

---

# 23. Vault Consolidation

The research vault itself was subsequently consolidated.

Three previously separate vaults were combined into a single active vault.

This reduces unnecessary source fragmentation and provides one current documentation surface for future discovery.

Retired architectural material is being separated into:

```text
historical-archive/
```

Current architecture documentation remains in the active documentation surface.

The purpose is not to erase architectural history.

It is to prevent historical implementation descriptions from being interpreted as current runtime authority.

---

# 24. Documentation Authority

Following consolidation, documentation should be interpreted according to explicit authority.

## Current

Describes the executable framework as it exists now.

Primary anchor:

```text
current_multi_agent_architecture.md
```

## Runtime Observation

Records behavior actually observed during execution.

Primary companion:

```text
multi_agent_runtime_observations.md
```

## Historical Archive

Preserves earlier architectures, experiments, hypotheses, prototypes, and retired implementations.

Location:

```text
historical-archive/
```

Historical documents remain part of the research record but do not override current architecture documentation.

---

# 25. What Was Removed

The following architectural elements no longer define the current runtime:

```text
central orchestrator authority
orchestrator.py as active coordinator

universal sequential engine chain

TaskGuard as a central mesh execution stage

Coherence Engine as a standalone universal
execution authority

Math Engine as a mandatory universal stage

Repair Engine as a mandatory universal stage

deterministic renderer as the central
multi-agent release path

older Horizon/Pipe Horizon topology as
the active execution topology
```

Their historical documentation may remain archived.

---

# 26. What Survived Conceptually

Several concepts persisted even though their implementation changed.

```text
Earlier Concept              Current Expression

Persistence              →   node-local MemoryLattice

Heartbeat                →   AsynchronousPulse

Runtime states           →   agent-owned current_state

Routing                   →   signed inter-node message flow

Validation               →   A/B/C independent scoring

Execution authority      →   fluid leader election

Lifecycle ordering       →   election epoch +
                             execution sequence

External retrieval       →   NODE_F internet ingress

Source discovery         →   NODE_D

Source bridge            →   NODE_E

Reasoning                →   serialized NODE_F /
                             DeepSeek-R1

Integrity boundary       →   signed envelopes +
                             persistent provenance
```

The architecture therefore evolved by preserving useful invariants while replacing their implementation.

---

# 27. Current Architectural Direction

The framework has moved away from increasing the number of centralized processing stages.

The present direction is toward:

- specialized autonomous agents,
    
- explicit role boundaries,
    
- authenticated transport,
    
- local persistent memory,
    
- observable runtime state,
    
- fluid execution authority,
    
- deterministic duplicate rejection,
    
- incremental source ingestion,
    
- separation of quantitative telemetry from qualitative reasoning.
    

New functionality should therefore be evaluated according to whether it belongs:

```text
inside an existing node role,
as a new authenticated interaction,
as a persistence layer,
or as a genuinely new agent responsibility
```

rather than automatically introducing another central engine.

---

# 28. Architectural Lineage Principle

The evolution of Zero-Point Protocol should not be represented as though the current architecture existed from the beginning.

Earlier architectures were necessary experimental stages.

Their failures and limitations produced later design decisions.

The canonical lineage is therefore:

```text
prototype
   ↓
observation
   ↓
failure or limitation
   ↓
structural correction
   ↓
runtime validation
   ↓
next architecture
```

This lineage is part of the research evidence.

The historical archive preserves the path.

The current architecture defines the present system.

Runtime observations document what the present system actually does.

---

# 29. Current Transition State

At the time of this record:

```text
Six-node mesh                  ACTIVE
Cryptographic identities       ACTIVE
Signed WebSocket transport     ACTIVE
A/B/C validator cluster        ACTIVE
Fluid validator weighting      ACTIVE
Leader-gated execution         ACTIVE
Election epoch                 ACTIVE
Execution sequence             ACTIVE
NODE_D discovery               ACTIVE
NODE_E bridge                  ACTIVE
NODE_F internet ingress        ACTIVE
NODE_F local reasoning         ACTIVE
Node-local MemoryLattice       ACTIVE
State-aware pulse telemetry    ACTIVE
Validator deduplication        COMPLETE
Reasoning transcript recovery  COMPLETE
Changed-only manifest          SEEDED
Single consolidated vault      COMPLETE
Historical archive migration   IN PROGRESS
Current documentation refresh  IN PROGRESS
```

---

# 30. Canonical Transition Statement

Zero-Point Protocol transitioned from a centrally coordinated, engine-oriented experimental architecture into a persistent six-node multi-agent mesh.

The transition did not merely distribute an existing orchestrator across multiple processes.

Responsibilities were separated, execution authority was redesigned, cryptographic transport became the coordination boundary, persistence became node-local, validator authority became fluid, execution became leader-gated, runtime state became observable, and source ingestion became content-aware.

Earlier architecture remains valuable as developmental evidence.

It no longer defines the active runtime.

The authoritative implementation is the current multi-agent architecture documented separately in:

```text
current_multi_agent_architecture.md
```

---

## Document Status

**Status:** CURRENT  
**Classification:** Architectural Lineage  
**Historical Authority:** Records the transition into the current implementation  
**Runtime Authority:** `current_multi_agent_architecture.md`  
**Next Companion Record:** `multi_agent_runtime_observations.md`