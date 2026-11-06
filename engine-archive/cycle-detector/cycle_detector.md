>[!NOTE] Prototype Lineage — Decomposition Phase  
This component was created during Horizon's **Decomposition Phase**, when broader architectural principles were deliberately isolated into individual engines to observe and test specific behaviors in isolation.
>
This engine was a prototype of a **function**, not a declaration that reasoning requires a permanent, centralized control layer. IIts architectural purpose was to make a specific question observable: _Can this property be measured, verified, preserved, or corrected independently?_
>
Initial testing indicated the prototype performed its intended function. However, because the original test data was not permanently preserved, this component is retained as a tested historical implementation rather than a currently validated runtime requirement.
>
The current multi-agent architecture does not assume that reasoning requires passage through a fixed sequence of specialized engines, evaluators, gates, or centralized control components in order to proceed. The Horizon prototypes isolated these functions so they could be observed and tested independently; their existence did not establish that the functions must remain permanently separated or universally applied. Where the underlying principles remain useful, they may be expressed through native capability, distributed observation, evidence, persistent state, deterministic verification where applicable, or lateral interaction among independent agents—without introducing an authority merely to grant reasoning permission.
>
**The architecture observes where observation is useful. It verifies where verification is possible. It does not create an authority merely so reasoning can ask permission to proceed.**
>
See: [[horizon_decomposition_phase]]

---

zpp_id: cycle_detector
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

Component

CycleDetector

Version

1.0.0

Status

Prototype

Category

Cycle Detection

First Released

v1.0.0

---

**Purpose**

CycleDetector identifies repeated reasoning states that indicate recursive processing is no longer making meaningful forward progress.

Rather than allowing refinement, critique, or repair loops to continue indefinitely, the engine deterministically detects repeated normalized states and returns observable cycle evidence to the surrounding architecture.

CycleDetector protects the system from compute without progress.

---

**Detection Pipeline**

Reasoning State

↓

Normalize State

↓

Generate State Hash

↓

Compare Against History

↓

New State  
or  
Repeated State

↓

Continue Reasoning  
or  
Terminate Cycle

---

**Detection Process**

CycleDetector receives each reasoning state as text.

The engine normalizes superficial formatting differences, generates a SHA-256 hash of the normalized state, and compares that hash against previously observed states.

When a matching state is found, the engine reports:

• the cycle type

• the index where the state first appeared

• the index where it repeated

• the detected cycle length

• the normalized state

• the state hash

• supporting metadata

The engine performs deterministic state comparison and does not use model inference.

---

**Supported Cycle Types**

|Cycle Type|Description|
|---|---|
|`period_2`|A reasoning state repeats after one intervening state, such as A → B → A|
|`repeated_state`|A normalized state repeats at another observed depth|

Version 1 detects exact normalized-state repetition across the retained history.

---

**State Normalization**

Before comparison, CycleDetector normalizes reasoning states by:

• converting text to lowercase

• collapsing repeated whitespace

• removing most punctuation

• normalizing selected restart and reevaluation phrases

• removing changing depth numbers

• removing changing step numbers

• removing changing pass numbers

This allows the engine to detect repeated reasoning states despite minor formatting differences.

Normalization is intentionally conservative.

CycleDetector does not currently determine semantic equivalence between differently worded states.

---

**State Hashing**

Normalized states are hashed using SHA-256.

The hash provides a deterministic comparison key while allowing the engine to retain bounded state history without repeatedly comparing full response text.

The full normalized state remains available in the detection result for inspection and telemetry.

---

**History Management**

CycleDetector maintains:

• an ordered history of observed state hashes

• a mapping from each state hash to its first observed index

The default maximum history length is 100 states.

When retained history exceeds the configured limit, the oldest entries are removed and the remaining state indexes are rebuilt.

The detector may be reset explicitly before evaluating a new reasoning sequence.

---

**Current Implementation**

Public interface:

- `observe()`
    
- `detect_sequence()`
    
- `reset()`
    
- `normalize_state()`
    
- `hash_state()`
    
- `cycle_detector`
    

**Result type:**

- `CycleDetectionResult`
    

**Result includes:**

- `detected`
    
- `cycle_type`
    
- `first_seen_index`
    
- `repeated_index`
    
- `cycle_length`
    
- `normalized_state`
    
- `state_hash`
    
- `issues`
    
- `metadata`
    

---

**Operational Modes**

**Incremental Observation**

`observe()` evaluates one state at a time while preserving internal history.

**Sequence Evaluation**

`detect_sequence()` resets existing history and scans a complete sequence until the first repeated state is found.

**Reset**

`reset()` clears all retained state and begins a new detection window.

---

**Failure Behaviour**

CycleDetector may return:

• no cycle detected

• period-2 oscillation detected

• repeated state detected

• bounded history trimmed

A detected cycle does not independently decide whether a response should be released.

It provides deterministic cycle evidence to RecursiveReasoner, RepairEngine, Recursive Gatekeeper, or another coordinating component.

---

**Known Limitations**

CycleDetector identifies exact repetition after normalization.

It does not currently detect:

• semantically equivalent paraphrases

• gradually shrinking reasoning loops

• conceptual repetition expressed through different language

• cycles distributed across separate execution sessions

• cycles spanning multiple models or nodes

• non-repeating stagnation where reasoning changes text without improving substance

The detector measures repeated state, not reasoning quality.

---

**Future Extensions**

Future extensions may include:

• semantic cycle detection

• embedding-based state comparison

• progress scoring

• cross-session cycle detection

• multi-node cycle correlation

• cycle severity classification

• configurable normalization policies

• stagnation detection without exact repetition

• persistence through MemoryEngine

• compute-tax telemetry for prevented recursion

---

**Design Consequences**

|Principle|Primary Implementation|
|---|---|
|Bounded Recursion|`observe()`|
|Deterministic Detection|State Hash Comparison|
|Period-2 Detection|Cycle-Length Classification|
|Observable Failure|`CycleDetectionResult`|
|Bounded Memory|`max_history`|
|Sequence Analysis|`detect_sequence()`|
|Compute Proportionality|Early Cycle Termination|

---

**Related Specifications**

• [[design_philosophy|Design Philosophy]]

• [[RecursiveReasoner|RecursiveReasoner]]

• [[gatekeeper_architecture|Recursive Gatekeeper]]

• [[repair_engine|RepairEngine]]

• [[gamma_framework|GAMMA Framework]]

• [[pulse_framework|Pulse System]]

---

**Engine Observation**

Recursion is useful only while it produces meaningful change.

CycleDetector does not determine whether reasoning is correct. It determines whether the architecture has returned to a state it has already visited.

When reasoning repeats without progress, termination preserves both architectural stability and compute proportionality.

