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

zpp_id: recursive_reasoner
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

Component

RecursiveReasoner

Version

1.0.0

Status

Prototype

Category

Iterative Reasoning

First Released

v1.0.0

---

**Purpose**

RecursiveReasoner improves an initial response through structured self-critique before HorizonPipeline continues with the remaining reasoning stages.

Rather than accepting the first generated answer, the engine performs bounded recursive refinement by identifying unresolved issues, revising the response, measuring convergence, and terminating when further refinement is no longer justified.

The objective is not endless reasoning.

The objective is bounded improvement before the verification pipeline begins.

---

**Verification Pipeline**

Prompt
↓
Kai Produces Candidate Response
↓
RecursiveReasoner.reason()
↓
Adversarial Critique
↓
Issue Extraction
↓
Revision
↓
Convergence Check
↓
Verification Evidence Returned to HorizonPipeline
↓
Kai Continues the Verification Pipeline

---

**Reasoning Process**

Each reasoning cycle consists of four stages:

• Critique

• Issue Extraction

• Revision

• Convergence Measurement

The critique stage searches for logical gaps, unsupported assumptions, contradictions, numerical errors, missed edge cases, and failures to answer the original task.

Only identified issues are revised.

Correct reasoning is intentionally preserved rather than regenerated.

---

**Convergence**

Reasoning continues until one of the following conditions is met:

• No material issues remain

• Convergence threshold reached

• Maximum recursion depth reached

• Cycle detected

• Revision failure

The engine measures textual similarity between successive reasoning states to estimate convergence while independently tracking unresolved issues.

---

**Cycle Detection**

Recursive reasoning must remain bounded.

Each revised response is monitored by the CycleDetector to identify repeated reasoning states.

When deterministic cycles are detected, recursion terminates rather than consuming additional computation.

---

**Current Implementation**

Current public interface:

- `reason()`
- `_critique()`
- `_revise()`
- `_extract_issues()`
- `_similarity()`

**Result includes:**

- final_answer
- reasoning_trace
- recursion_depth
- unresolved_issues
- convergence_similarity

---

**Failure Behaviour**

RecursiveReasoner may terminate because of:

• Maximum recursion depth reached

• No material issues detected

• Convergence achieved

• Deterministic reasoning cycle detected

• Revision failure

• Model communication failure

Failure does not automatically terminate reasoning.

Subsequent HorizonPipeline stages determine whether additional repair or verification is appropriate.

---

**Future Extensions**

Planned extensions include:

• Branch exploration

• Parallel reasoning paths

• Evidence-weighted critique

• Domain-specific reasoning strategies

• Cross-model recursive critique

• Memory-aware recursive refinement

• Adaptive recursion depth

---

**Design Consequences**

| Principle                | Primary Implementation |
| ------------------------ | ---------------------- |
| Iterative Improvement    | `reason()`             |
| Structured Self-Critique | `_critique()`          |
| Bounded Recursion        | `max_depth`            |
| Convergence Detection    | `_similarity()`        |
| Cycle Prevention         | `CycleDetector`        |
| Verification Integration | HorizonPipeline        |

---

**Related Specifications**

• [[design_philosophy|Design Philosophy]]

• [[task_guard|TaskGuard]]

• [[coherence_engine|CoherenceEngine]]

• [[math_engine|MathEnginev1]]

• [[repair_engine|RepairEngine]]

• [[historical-archive/generations/horizon/architecture/horizon_pipeline|HorizonPipeline]]

---

**Engine Observation**

Recursive reasoning does not seek a perfect answer.

It seeks to improve Kai's candidate response through bounded refinement before subsequent reasoning stages.

Improvement is measured by the reduction of unresolved issues rather than the number of reasoning cycles.