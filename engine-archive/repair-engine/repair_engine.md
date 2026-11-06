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

zpp_id: repair_engine
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

Component 

RepairEngine

Version

1.0.0

Status

Prototype

Category

Controlled Repair

First Released

v1.0.0

---

**Purpose**

RepairEngine converts independent verification evidence into one prioritized, consolidated repair plan.

Rather than allowing each observer to trigger its own rewrite, the engine gathers task, schema, mathematical, coherence, reasoning, and cycle evidence into a single controlled correction request.

RepairEngine is limited to one repair attempt.

It does not independently determine whether the repaired response is trusted. Final verification remains the responsibility of the Recursive Gatekeeper and Release Gate.

---

**Repair Principle**

Repair must restore integrity without becoming a new source of drift.

The engine preserves correct material, changes only what the evidence requires, and prevents uncontrolled repair loops by allowing at most one model-assisted repair pass.

---

**Repair Pipeline**

Observer Evidence

↓

RepairEngine.plan()

↓

Cycle Termination Check

↓

Collect Repair Actions

↓

Assign Priorities

↓

Build Consolidated Repair Prompt

↓

RepairEngine.execute()

↓

One Repair Attempt

↓

Final Re-verification

↓

Release Gate

---

**Bounded Authority**

RepairEngine does not independently:

• detect mathematical errors

• measure coherence

• determine task preservation

• detect reasoning cycles

• establish final correctness

• retry failed repairs

• authorize release

It consumes evidence produced by specialized observers and converts that evidence into a bounded repair action.

---

**Repair Sources**

RepairEngine may receive evidence from:

|Evidence Source|Repair Concern|
|---|---|
|TaskGuard|Missing task concepts or exact-output requirements|
|Structured Output Checks|Missing JSON keys or schema obligations|
|MathEngine|Deterministically identified mathematical errors|
|CoherenceEngine|Topic drift, contradiction, or semantic instability|
|RecursiveReasoner|Unresolved reasoning issues or incomplete convergence|
|CycleDetector|Terminal reasoning-cycle condition|

---

**Repair Priorities**

|Repair Category|Priority|
|---|--:|
|Task|100|
|Schema|95|
|Mathematics|90|
|Coherence|80|
|Reasoning|70|

Higher-priority actions appear first in the consolidated repair plan.

The priority model ensures that explicit task and format requirements are restored before lower-priority reasoning refinements.

---

**Repair Planning**

`RepairEngine.plan()` performs deterministic planning.

The planner:

• normalizes observer input

• checks for terminal cycle evidence

• creates task repair actions

• creates schema repair actions

• creates mathematical repair actions

• creates coherence repair actions

• creates reasoning repair actions

• sorts actions by priority

• constructs one consolidated repair prompt

Planning does not require a model call.

---

**Terminal Cycle Handling**

When deterministic cycle evidence is present, RepairEngine does not attempt another rewrite.

It returns a terminal plan containing:

`CRITICAL ERROR: LOOP DETECTED`

This prevents repair from extending an already detected reasoning cycle.

---

**Task Repair**

Task repair may be requested when:

• required task concepts are missing

• an exact required phrase was omitted

• the response substituted another task, domain, or scenario

• general task preservation failed

Task repair has the highest priority because all later verification depends on preserving the operator’s original request.

---

**Schema Repair**

Schema repair is requested when explicitly required JSON keys are missing.

The repair instruction requires the response to return to the requested structured format and include every required field.

Schema repair is treated as a hard output obligation.

---

**Mathematical Repair**

Mathematical repair is requested only when:

• the problem is deterministically verifiable

• verification failed

When available, computed reference values are attached as repair evidence.

The repair peer is instructed to follow those values, preserve correct work, and correct only the affected mathematical claims.

A deterministic renderer may take precedence when the supported MathEngine domain can produce an authoritative answer directly.

---

**Coherence Repair**

Coherence repair may address:

• weak task alignment

• topic drift

• internal contradiction

• general semantic instability

Repair instructions are derived from the measured coherence state rather than from a generic rewrite request.

---

**Reasoning Repair**

Reasoning repair may be requested when:

• unresolved issues remain

• convergence was not achieved

• the final similarity remains below the configured convergence threshold

The engine asks the repair peer to preserve correct conclusions while resolving unsupported assumptions and outstanding reasoning failures.

---

**Consolidated Repair Prompt**

The repair prompt contains:

• the original task

• the current answer

• prioritized repair actions

• evidence supporting each action

• instructions to preserve correct content

• instructions to return only the corrected answer

• instructions not to expose internal audits or framework details

This allows multiple observer failures to be addressed in one controlled pass rather than through separate competing rewrites.

---

**Execution Rules**

`RepairEngine.execute()` follows three paths.

**Terminal Plan**

No repair is attempted.

The terminal response is returned immediately.

**No Repair Required**

The original answer is returned unchanged.

**Repair Required**

One model-assisted repair call is permitted.

The engine never retries.

---

**Execution Outcomes**

RepairEngine may return:

• terminal response selected

• no repair required

• repair attempted and response returned

• repair attempt failed

• empty repair response

• model connection failure

• execution exception

When repair execution fails, the original answer is preserved.

---

**Important Success Boundary**

A successful repair execution means that the repair peer returned a non-empty response without a connection error.

It does not mean that the repaired answer has passed verification.

TaskGuard, CoherenceEngine, MathEngine, and the final release pipeline must evaluate the repaired response again before release.

---

**Current Implementation**

Public interface:

- `repair_engine.plan()`
    
- `repair_engine.execute()`
    
- `RepairAction`
    
- `RepairPlan`
    
- `RepairExecutionResult`
    
- `repair_engine`
    

**RepairAction includes:**

- `category`
    
- `priority`
    
- `instruction`
    
- `evidence`
    

**RepairPlan includes:**

- `repair_required`
    
- `terminal`
    
- `terminal_response`
    
- `actions`
    
- `repair_prompt`
    
- `reasons`
    
- `metadata`
    

**RepairExecutionResult includes:**

- `attempted`
    
- `successful`
    
- `original_answer`
    
- `final_answer`
    
- `plan`
    
- `error`
    

---

**Failure Behaviour**

RepairEngine fails closed around the original response.

If repair execution returns no usable answer, encounters a connection error, or raises an exception, the original answer is retained and the error is recorded.

The engine does not silently substitute an incomplete repair.

The surrounding architecture then determines whether the unchanged response must be blocked, quarantined, or evaluated through another deterministic path.

---

**Known Limitations**

RepairEngine currently:

• permits only one model-assisted repair call

• relies on the quality of observer evidence

• does not independently validate the repaired answer

• does not merge conflicting repair actions semantically

• does not detect whether one repair instruction undermines another

• does not rank evidence strength beyond category priority

• does not protect authoritative deterministic output by itself

• does not persist repair history independently

Protection of authoritative output and post-repair verification are enforced by the Recursive Gatekeeper.

---

**Future Extensions**

Future extensions may include:

• explicit authoritative-state protection

• evidence confidence weighting

• repair-action conflict detection

• deterministic repair handlers by domain

• schema-native repair without model inference

• repair-diff generation

• provenance tracking for every changed claim

• rollback support

• operator approval for high-impact repairs

• repair-cost telemetry

• MemoryEngine integration

• multi-model repair comparison

• policy-defined repair permissions

---

**Design Consequences**

|Principle|Primary Implementation|
|---|---|
|Consolidated Repair|`plan()`|
|Bounded Repair|Single-Call `execute()`|
|Priority Preservation|Repair Action Priorities|
|Terminal Cycle Safety|Terminal Repair Plan|
|Evidence-Based Correction|Observer Evidence|
|Original-State Preservation|Failure Fallback|
|Post-Repair Trust|Final Re-verification|
|Observable Failure|`RepairExecutionResult`|

---

**Related Specifications**

• [[design_philosophy|Design Philosophy]]

• [[gatekeeper_architecture|Recursive Gatekeeper]]

• [[RecursiveReasoner|RecursiveReasoner]]

• [[task_guard|TaskGuard]]

• [[coherence_engine|CoherenceEngine]]

• [[math_engine|MathEnginev1]]

• [[CycleDetector|CycleDetector]]

• [[release_gate|The Release Gate]]

• [[gamma_framework|GAMMA Framework]]

---

**Engine Observation**

Repair is not trust.

RepairEngine creates one evidence-guided opportunity to restore integrity, but the repaired answer earns trust only by passing verification again.

A repair that is not re-verified is merely another generation.