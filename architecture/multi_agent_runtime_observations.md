# Zero-Point Protocol — Multi-Agent Runtime Observations

**Document Type:** Empirical Runtime Observation Record  
**Status:** CURRENT  
**Scope:** Observed behavior of the active six-node multi-agent mesh  
**Companion Documents:**

- `current_multi_agent_architecture.md`
    
- `architecture_transition_record.md`
    

---

## 1. Purpose

This document records empirical observations made while operating and evolving the current Zero-Point Protocol multi-agent framework.

It is not an architectural specification.

It does not describe what the system is intended to do in theory.

It records what was actually observed during execution, including:

- successful behavior,
    
- unexpected behavior,
    
- runtime failures,
    
- persistence gaps,
    
- state transitions,
    
- queue behavior,
    
- database effects,
    
- validator behavior,
    
- reasoning behavior,
    
- and architectural corrections produced by those observations.
    

The distinction is:

```text
ARCHITECTURE
what the system is designed to do

RUNTIME OBSERVATION
what the system actually did
```

This document addresses the second category.

---

# 2. Observation Environment

The current runtime consists of six autonomous nodes:

```text
NODE_A
NODE_B
NODE_C
NODE_D
NODE_E
NODE_F
```

Each node maintains:

- its own cryptographic identity,
    
- WebSocket network presence,
    
- node-local persistent SQLite memory,
    
- runtime state,
    
- asynchronous heartbeat telemetry.
    

The system operates locally with DeepSeek-R1 through Ollama for NODE_F reasoning.

Current local reasoning model:

```text
deepseek-r1:7b
```

---

# 3. Validator Symmetry

A/B/C repeatedly received the same signed payload and independently produced equivalent telemetry for that payload.

Observed example:

```text
NODE_A Validator
Gamma: 1.0
Novelty: 1.0
Entropy: 0.8453
Self-Reference: 1.0
Paradox: 1.0
Coherence: 1.0

NODE_B Validator
Gamma: 1.0
Novelty: 1.0
Entropy: 0.8453
Self-Reference: 1.0
Paradox: 1.0
Coherence: 1.0

NODE_C Validator
Gamma: 1.0
Novelty: 1.0
Entropy: 0.8453
Self-Reference: 1.0
Paradox: 1.0
Coherence: 1.0
```

### Observation

The validators behaved deterministically with respect to identical input and equivalent local context.

### Significance

Distributed validation did not introduce arbitrary scoring divergence during these tests.

The cluster therefore demonstrated:

```text
same input
→ independent validation
→ same measured result
```

under the tested conditions.

---

# 4. Coherence Was Not Permanently Fixed at 0.5

An earlier recurring observation suggested that the coherence metric remained fixed at:

```text
0.5
```

This raised the possibility of a hard-coded default or scoring defect.

Subsequent runtime execution produced:

```text
Coherence: 1.0
```

without changing the coherence implementation immediately beforehand.

### Observation

The metric was not structurally locked at `0.5`.

Its value changed when recent-context token overlap changed.

### Significance

The earlier `0.5` state was attributable to the context relationship being measured rather than a permanent constant inside the scoring layer.

This shifted investigation away from:

```text
"coherence implementation is frozen"
```

toward:

```text
"what context is actually being supplied to the scorer?"
```

---

# 5. Query/Evidence Conflation

During early internet reasoning tests, NODE_F correctly retrieved external search context but DeepSeek sometimes responded to the retrieved matrix rather than the original user question.

One output merely identified what the query appeared to be asking instead of directly answering it.

### Observation

The original query and retrieved evidence were being treated too similarly inside the reasoning prompt.

### Correction

The runtime introduced explicit separation between:

```text
USER QUERY
```

and:

```text
MATRIX
```

### Result

Later reasoning correctly identified the user's original query while using retrieved results as evidence.

### Significance

Prompt structure produced better behavior than adding increasingly specific behavioral instructions.

---

# 6. System-Prompt Specificity Observation

During reasoning development, increasingly detailed system instructions produced brittle or over-constrained behavior.

The instruction was subsequently simplified.

### Observation

More detailed behavioral instructions did not consistently produce better reasoning.

Highly specific instructions sometimes caused the model to:

- over-focus on telemetry,
    
- classify the query instead of answering it,
    
- assign unsupported meanings to metrics,
    
- attach global metrics to individual search results.
    

### Correction

The system prompt was reduced to a minimal operating contract while structural distinctions were moved into the payload itself.

### Result

The reasoning interface became:

```text
USER QUERY
VALIDATED TELEMETRY
HISTORY
MATRIX
```

rather than relying primarily on a long system directive.

---

# 7. Telemetry Over-Interpretation

DeepSeek initially interpreted telemetry metrics beyond their operational definitions.

Examples included treating:

```text
Entropy
```

as evidence of implementation efficiency or complexity,

and assigning payload-wide telemetry values to individual search results.

### Observation

The model treated numerical telemetry as semantic evidence when the metric definitions did not support those conclusions.

### Correction

Telemetry was labeled explicitly as applying to:

```text
the complete MATRIX payload
```

and local definitions were placed directly beside each metric.

### Significance

This reinforced a separation between:

```text
quantitative measurement
```

and:

```text
qualitative interpretation
```

---

# 8. Election Epoch Limitation

An early leader-gating implementation used only:

```text
election_epoch
```

to reject stale reasoning triggers.

The first reasoning request succeeded.

A second legitimate request under the same leadership state was rejected as:

```text
stale/duplicate election epoch
```

### Observation

Leadership identity and execution identity are not equivalent.

Multiple valid executions can occur during one election state.

### Correction

A separate:

```text
execution_sequence
```

was introduced.

NODE_F now tracks both:

```text
last_accepted_election_epoch
last_accepted_execution_sequence
```

### Result

Repeated valid executions under the same elected leader became possible while duplicate triggers remained rejectable.

---

# 9. Missing Runtime State Initialization

At one point NODE_F raised:

```text
CryptographicAgentNode object has no attribute
last_accepted_election_epoch
```

### Observation

The acceptance-state logic existed in the handler before the corresponding state variables were initialized on the node.

### Correction

The node constructor was expanded to initialize:

```text
last_accepted_election_epoch = -1
last_accepted_execution_sequence = -1
```

### Significance

The error confirmed that network protocol state must be explicit and persistent for the lifetime of the agent.

---

# 10. Apparent Reasoning Freeze

NODE_F repeatedly appeared to stop after receiving a valid reasoning trigger.

Initial suspicion focused on:

```text
reasoning_lock
```

and a possible asynchronous deadlock.

### Observation

Additional traceback instrumentation exposed the actual cause:

```text
NameError: original_query is not defined
```

inside the reasoning prompt construction.

A second error occurred because:

```text
traceback
```

had not been imported.

### Result

The apparent lock failure was not a lock failure.

The reasoning task was crashing before normal output.

### Significance

This was an important diagnostic event:

```text
apparent concurrency problem
≠
actual concurrency problem
```

The root cause was an undefined variable in the reasoning path.

---

# 11. Reasoning Lock Behavior

After the prompt error was corrected, NODE_F successfully executed reasoning tasks under:

```text
self.reasoning_lock
```

### Observation

The lock serialized Ollama execution.

During the large vault run, DeepSeek repeatedly displayed:

```text
[NODE_F Core] Active streaming reasoning pipeline engaged...
```

then completed one stream before beginning another.

### Significance

The observed pattern was:

```text
job
→ reasoning
→ completion
→ next job
```

rather than uncontrolled concurrent inference.

The lock therefore operated as a local resource boundary.

---

# 12. Full Historical Vault Stress Run

A complete historical vault scan triggered a large number of qualifying file handoffs.

NODE_D discovered the files.

NODE_E retrieved the contents.

A/B/C validated them.

The elected validator dispatched reasoning triggers.

NODE_F processed the resulting queue sequentially.

### Observation

The queue required approximately several hours to drain.

NODE_F repeatedly entered reasoning execution as each waiting task acquired the lock.

### Result

A total of:

```text
181 completed DeepSeek reasoning streams
```

were later recovered from the saved terminal transcript.

### Significance

The run acted as an unintended but useful stress test of:

- discovery throughput,
    
- bridge throughput,
    
- validator fan-out,
    
- leader gating,
    
- reasoning serialization,
    
- asynchronous task accumulation,
    
- pulse-state observation.
    

---

# 13. State-Aware Pulse Validation

The asynchronous pulse system initially recorded heartbeat activity without exposing meaningful runtime state.

It was subsequently connected to:

```text
self.current_state
```

through a state getter.

The initial role-aware heartbeat state was observed as:

```text
NODE_A → VALIDATOR_READY
NODE_B → VALIDATOR_READY
NODE_C → VALIDATOR_READY
NODE_D → DISCOVERY_IDLE
NODE_E → BRIDGE_IDLE
NODE_F → INGRESS_READY
```

### Observation

The heartbeat database accurately reflected role-specific initial state.

---

# 14. REASONING_ACTIVE Capture

During the large historical reasoning queue, NODE_F pulse records showed:

```text
REASONING_ACTIVE
```

across multiple consecutive 60-second samples.

Example:

```json
{
  "node_id": "NODE_F",
  "state": "REASONING_ACTIVE",
  "active_tasks": 203
}
```

followed by additional pulses with approximately:

```text
202–203 active tasks
```

### Observation

The pulse system captured sustained reasoning activity without controlling or interrupting it.

### Significance

The heartbeat became a runtime observer rather than a simple liveness marker.

---

# 15. Async Task Expansion Under Queue Load

NODE_F startup pulse telemetry showed approximately:

```text
22 active asyncio tasks
```

During the large reasoning backlog this increased to approximately:

```text
202–203 active tasks
```

### Observation

A large number of queued or supporting asynchronous tasks existed while only one reasoning task could own the reasoning lock at a time.

### Status

This observation has not yet been fully classified as either:

- expected queued-task expansion,
    
- persistent task accumulation,
    
- or a mixture of both.
    

### Future Observation

The task count should be compared before, during, and after future bounded reasoning workloads.

---

# 16. Discovery/Bridge Separation Validation

NODE_D successfully discovered matching vault files and issued signed handoffs to NODE_E.

NODE_E independently retrieved the files from disk.

Observed messages included:

```text
[NODE_D] Signed discovery handoff sent to NODE_E
```

and:

```text
[NODE_E] Bridge retrieval complete
```

### Observation

The discovery and physical retrieval responsibilities operated independently.

### Significance

The runtime validated the role separation:

```text
D finds
E reads
```

rather than one node performing both responsibilities.

---

# 17. Node-Local Persistence Asymmetry

During early multi-agent testing, A/B/C were persisting validator inputs while:

```text
NODE_D
NODE_E
NODE_F
```

had incomplete or empty role-specific databases.

NODE_D and NODE_E were writing JSONL logs, but their corresponding MemoryLattice databases remained empty.

NODE_F initially persisted search ingress, but not all relevant reasoning output.

### Observation

Network participation did not automatically imply local persistence.

### Root Cause

`MemoryLattice._disk_write()` supported only a limited set of layers.

Newer runtime roles were committing:

```text
discovery
bridge_retrieval
internet_ingress
reasoning
```

but the persistence layer did not initially map all of them to SQLite storage.

### Correction

MemoryLattice was expanded to recognize the new role-specific layers.

### Result

All six node databases became operational.

---

# 18. Six-Database Persistence Validation

After MemoryLattice updates, all six databases were confirmed functioning.

```text
NODE_A_matrix.db
NODE_B_matrix.db
NODE_C_matrix.db
NODE_D_matrix.db
NODE_E_matrix.db
NODE_F_matrix.db
```

### Observation

Each node could now retain role-relevant runtime information locally.

This established a distributed memory topology rather than a validator-only persistence topology.

---

# 19. NODE_F Reasoning Persistence Gap

Although NODE_F persisted live search ingress, DeepSeek output was originally streamed only to the terminal.

### Observation

The reasoning process was computationally successful but not durably recorded in NODE_F's database.

This became visible only after the multi-hour vault reasoning run.

### Consequence

Hours of reasoning existed only in terminal output.

### Recovery

The terminal transcript was preserved as:

```text
Vault Reasoning.txt
```

A recovery utility parsed the DeepSeek stream boundaries.

Dry-run recovery reported:

```text
Completed streams found: 181
Unique transcript blocks: 181
Transcript duplicates: 0
Already present in DB: 0
Ready for import: 181
```

The recovered reasoning was then imported.

Verification afterward reported:

```text
Already present in DB: 181
Ready for import: 0
Characters to recover: 0
```

### Significance

The reasoning layer was successfully reconstructed without rerunning the historical vault.

---

# 20. Vault Reasoning Corpus

The recovered reasoning corpus contains 181 unique DeepSeek responses generated from historical vault material.

The material includes reasoning across earlier framework phases, including:

- distributed-system experiments,
    
- CRDT observations,
    
- coherence experiments,
    
- earlier Horizon architecture,
    
- source-locked architecture,
    
- routing experiments,
    
- alignment-tax material,
    
- simulation reports,
    
- governance models,
    
- earlier orchestration structures,
    
- retired engine architecture,
    
- observational studies of multiple LLMs.
    

### Observation

DeepSeek sometimes treated historical architecture as though it represented the current runtime.

### Cause

The vault documentation had not yet been updated to distinguish clearly between:

```text
historical architecture
```

and:

```text
current executable architecture
```

### Resulting Documentation Change

Current architecture documentation was added and retired material began moving into:

```text
historical-archive/
```

---

# 21. Validator Database Duplication

Repeated historical vault scans caused the same exact content to be stored multiple times in A/B/C.

A read-only duplicate audit reported:

```text
NODE_A
636 rows
204 unique payloads
185 duplicate groups
432 extra duplicate rows

NODE_B
636 rows
204 unique payloads
185 duplicate groups
432 extra duplicate rows

NODE_C
636 rows
204 unique payloads
185 duplicate groups
432 extra duplicate rows
```

### Observation

The duplication was deterministic and highly systematic.

Many vault files existed four times in each validator database.

---

# 22. Validator Deduplication Result

A dry-run cleanup predicted:

```text
636
→ 204
```

rows per validator.

The write pass then removed:

```text
432 duplicate rows
```

from each database.

Final verification:

```text
NODE_A
204 rows
duplicate rows remaining = 0

NODE_B
204 rows
duplicate rows remaining = 0

NODE_C
204 rows
duplicate rows remaining = 0
```

### Safety

Before cleanup, the framework created:

- three timestamped database backups,
    
- a deletion manifest recording canonical rows and removed row IDs.
    

### Significance

The validator data was restored to one canonical copy of each exact persisted payload.

---

# 23. NODE_E Historical Retrieval Duplication

NODE_E's database contained:

```text
364 bridge candidate rows
```

representing:

```text
182 unique source paths
```

and:

```text
182 repeated source paths
```

### Observation

Each known vault source path had been retrieved more than once.

This demonstrated that validator deduplication alone would not prevent future replay.

The ingestion boundary itself required change detection.

---

# 24. Changed-Only Manifest

A persistent NODE_E manifest was introduced:

```text
logs/node_e_content_manifest.json
```

A seeding utility reconstructed the current baseline from NODE_E's existing records.

Seed result:

```text
Total Node E rows:      364
Bridge candidate rows:  364
Usable bridge rows:     364
Repeated source paths:  182
Unique manifest paths:  182
Missing source path:    0
Missing content hash:   0
```

### Result

The manifest was successfully seeded with:

```text
182 baseline paths
```

### Intended Behavior

Future retrieval classification:

```text
NEW
MODIFIED
UNCHANGED
```

UNCHANGED content terminates at NODE_E.

---

# 25. Consolidated Vault Transition

The previously separate research vaults were consolidated into one active vault.

Retired architecture began moving into:

```text
historical-archive/
```

Current architecture documentation was added to the active vault.

### Observation

The historical vault structure had become a source of ambiguity for automated reasoning because old and current architecture coexisted without a strong authority boundary.

### Correction

The documentation topology is now transitioning toward:

```text
active/current documentation
historical-archive
```

---

# 26. Terminal Debug Noise

During development, substantial terminal debugging was introduced to trace:

- envelope reception,
    
- context retrieval,
    
- validator delivery,
    
- reasoning-task execution,
    
- lock behavior.
    

Once those paths were verified, routine debug lines were removed.

### Observation

Terminal logs became difficult to interpret when normal activity and diagnostic detail were mixed continuously.

### Current Direction

Use:

```text
terminal
→ meaningful operational events
→ warnings
→ failures
→ reasoning stream
```

while:

```text
database
→ persistent runtime telemetry
→ pulse history
→ memory
→ reasoning history
```

This separates observability from terminal clutter.

---

# 27. Pulse Persistence Behavior

The pulse system initially appeared inactive because no heartbeat message was printed on each interval.

Inspection of the node databases showed that pulse records had been written correctly from the first launch.

### Observation

Absence of terminal output did not imply absence of heartbeat activity.

### Significance

Database state became the authoritative observation surface for pulse persistence.

---

# 28. Runtime State Model

The current state model has been observed successfully at startup and during active execution.

## A/B/C

```text
VALIDATOR_READY
VALIDATING
LEADER_ACTIVE
```

## D

```text
DISCOVERY_IDLE
DISCOVERY_ACTIVE
```

## E

```text
BRIDGE_IDLE
BRIDGE_ACTIVE
```

## F

```text
INGRESS_READY
SEARCH_ACTIVE
REASONING_ACTIVE
```

### Observation

State is owned by the node.

Pulse only samples it.

This preserved separation between operation and observation.

---

# 29. Leader Behavior

During validator execution, NODE_C frequently became the elected leader under the current fluid-weight adjustment rule.

Observed weight state included:

```text
NODE_A = 0.20
NODE_B = 0.20
NODE_C = 0.60
```

### Observation

Runtime weighting could move substantially from the near-balanced initial state.

### Significance

Leader authority was not permanently hard-coded to NODE_C even though NODE_C frequently became dominant under the current tuning logic.

The distinction remains:

```text
current leader
≠
permanent leader
```

---

# 30. Single-Leader Execution Validation

Before leader gating, independent validators could produce redundant downstream execution.

After leader gating:

```text
NODE_A
NODE_B
NODE_C
```

still validated the same payload, but only the elected leader sent the reasoning trigger.

Non-leaders reported that they were deferring execution.

### Observation

Distributed validation and singular execution successfully coexisted.

---

# 31. Large-Scale Historical Replay Revealed Architectural Boundaries

The historical vault run exposed multiple problems that were not obvious in small tests:

```text
reasoning output not persisted
validator duplication
bridge duplication
large queued task count
historical/current documentation ambiguity
full replay inefficiency
```

### Significance

The run should not be treated simply as an inefficient accident.

It acted as a high-load integration test.

The architecture that existed before the run was not identical to the architecture that existed after it.

The run directly caused:

- reasoning recovery tooling,
    
- validator deduplication tooling,
    
- changed-only ingestion,
    
- documentation restructuring,
    
- stronger persistence requirements.
    

---

# 32. Runtime Correction Pattern

A recurring pattern emerged during development:

```text
unexpected behavior
        ↓
instrumentation
        ↓
actual failure exposed
        ↓
small structural correction
        ↓
rerun
        ↓
new observed state
```

Examples include:

```text
apparent reasoning deadlock
→ undefined original_query

coherence apparently fixed
→ actual context-dependent variation

duplicate reasoning rejection
→ execution_sequence required

empty D/E/F databases
→ missing MemoryLattice persistence layers

hours of unsaved reasoning
→ transcript recovery + future reasoning persistence requirement

repeated vault duplication
→ changed-only content manifest
```

### Observation

Most significant architecture changes originated in runtime observation rather than prior abstraction.

---

# 33. Observed Architectural Direction

The current runtime behavior suggests a continuing movement away from centralized sequential execution and toward:

- local role ownership,
    
- explicit persistence,
    
- stateful agents,
    
- signed event boundaries,
    
- incremental processing,
    
- singular downstream execution,
    
- distributed validation,
    
- asynchronous observation.
    

This is an observation about the development trajectory, not a claim that the architecture is complete.

---

# 34. Open Runtime Questions

The current implementation has exposed several questions that remain open for further testing.

## Queue Dynamics

Does NODE_F's active task count return consistently to baseline after large workloads?

## Fluid Weight Stability

Under what payload conditions do validator weights stabilize, oscillate, or saturate?

## State Sampling Resolution

Does a fixed 60-second heartbeat capture sufficiently short active-state transitions?

## Changed-Only Scan Behavior

Will the seeded 182-path manifest successfully prevent all unchanged files from reaching A/B/C and F?

## Modified File Propagation

Will exactly one edited file produce exactly one downstream processing path?

## Reasoning Persistence

Will future live NODE_F reasoning persist automatically without transcript recovery?

## Hybrid Batching

Should future large source updates retain per-file validation while consolidating reasoning into bounded batches?

---

# 35. Current Empirical Baseline

At the time of this record:

```text
All six node databases          WORKING
A/B/C exact duplicates          0
NODE_F recovered reasoning      181 unique records
NODE_E changed-only baseline    182 unique paths
State-aware pulse               WORKING
NODE_F REASONING_ACTIVE         OBSERVED
Serialized reasoning            OBSERVED
Single-leader dispatch          OBSERVED
Fluid validator weighting       OBSERVED
Independent A/B/C scoring       OBSERVED
D → E signed handoff            OBSERVED
E → validator broadcast         OBSERVED
Internet ingress persistence    WORKING
Vault reasoning recovery        COMPLETE
Vault consolidation             COMPLETE
Historical archive migration    IN PROGRESS
Changed-only live validation    PENDING TEST
```

---

# 36. Observation Principle

The current framework should continue to distinguish:

```text
designed behavior
observed behavior
inferred behavior
```

A feature being implemented does not establish that it behaves correctly.

A behavior occurring once does not establish that it is universal.

Runtime telemetry and persisted evidence should remain the basis for claims about the active system.

---

# 37. Canonical Runtime Observation Statement

The current Zero-Point Protocol multi-agent mesh has demonstrated functional distributed validation, fluid leader selection, singular reasoning dispatch, node-local persistence, signed discovery and bridge transport, serialized local reasoning, role-aware heartbeat telemetry, and recoverable execution history.

The same runtime has also exposed persistence asymmetries, duplicate ingestion, queue expansion, context-dependent metric behavior, and documentation ambiguity.

These failures were not external to the development process.

They produced the structural corrections that define the current implementation.

The architecture therefore continues to evolve through:

```text
observation
→ evidence
→ correction
→ verification
```

rather than through static specification alone.

---

## Document Status

**Status:** CURRENT  
**Classification:** Empirical Runtime Observation Record  
**Architecture Reference:** `current_multi_agent_architecture.md`  
**Lineage Reference:** `architecture_transition_record.md`  
**Historical Material:** `historical-archive/`  
**Next Validation:** Changed-only vault ingestion against the seeded 182-path NODE_E manifest