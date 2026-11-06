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

zpp_id: task_guard
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

Component

TaskGuard

Version

1.0.0

Status

Prototype

Category

Task Preservation

First Released

v1.0.0

---

**Purpose**

TaskGuard determines whether a response preserves the explicit requirements of the original prompt.

Rather than evaluating factual correctness or broad semantic coherence, TaskGuard checks whether required entities, exact phrases, and structured output obligations remain present in the response.

TaskGuard protects the original task from omission, substitution, and incomplete execution before release.

---

**Verification Pipeline**

Prompt

↓

TaskGuard.verify()

↓

Extract Required Terms

↓

Extract Exact Phrases

↓

Extract Required JSON Keys

↓

Compare Against Response

↓

Calculate Preservation Score

↓

Preserved  
or  
Not Preserved

↓

Release Gate

---

**Verification Process**

TaskGuard performs deterministic comparison between the prompt and the response.

The current implementation extracts three classes of requirements:

• required terms

• required exact phrases

• required JSON keys

It then determines which requirements are missing and calculates a preservation score.

Hard requirements and soft requirements are weighted differently.

---

**Requirement Classes**

| Requirement Class | Description                                                                    |
| ----------------- | ------------------------------------------------------------------------------ |
| Required Terms    | Explicit task entities and benchmark-style concepts expected to remain present |
| Exact Phrases     | Phrases the prompt explicitly requires the system to output exactly            |
| JSON Keys         | Structured fields explicitly requested in JSON output                          |

---

**Hard and Soft Checks**

Exact phrases and required JSON keys are treated as hard checks.

Required terms are treated as soft checks.

When hard checks exist:

• hard requirements contribute 80% of the score

• soft requirements contribute 20% of the score

• preservation requires every hard requirement to be present

When only soft checks exist:

• the score is based on preserved required terms

• preservation requires a soft score of at least 0.50

When no explicit requirements are detected:

• the score defaults to 1.0

• the task is considered preserved

---

**Current Scoring**

Hard Score

80%

↓

Soft Score

20%

↓

Task Preservation Score

For prompts without hard checks, the soft score becomes the full preservation score.

---

**Failure Behaviour**

TaskGuard may identify:

• missing task entities

• missing exact phrases

• missing JSON keys

• partial task preservation

• complete hard-requirement failure

A failed TaskGuard result does not rewrite the response.

It reports the missing requirements so the RepairEngine or Release Gate can determine the next action.

---

**Current Implementation**

Public interface:

- `task_guard.verify()`
    
- `TaskGuardResult`
    
- `task_guard`
    

**Result includes:**

- `preserved`
    
- `score`
    
- `required_terms`
    
- `missing_terms`
    
- `required_phrases`
    
- `missing_phrases`
    
- `required_json_keys`
    
- `missing_json_keys`
    
- `issues`
    
- `metadata`
    

**Metadata includes:**

- `hard_checks`
    
- `hard_missing`
    
- `soft_checks`
    
- `soft_missing`
    
- `hard_score`
    
- `soft_score`
    

---

**Current Extraction Scope**

Version 1 recognizes:

• benchmark-style named entities

• selected security terms

• selected financial calculation terms

• explicit exact-output instructions

• explicitly requested JSON keys

The current extractor is intentionally conservative.

It does not treat every quoted string as a required key and does not invent requirements that were not explicitly present in the prompt.

---

**Known Limitations**

TaskGuard does not currently determine whether the response is factually correct.

TaskGuard does not evaluate broad semantic coherence.

TaskGuard does not currently implement a general-purpose topic-substitution detector, despite that behavior being identified as a Version 1 design goal.

TaskGuard recognizes only the requirement patterns currently defined in its deterministic extractors.

Prompts expressed in unsupported forms may receive a perfect preservation score when no explicit requirements are detected.

---

**Future Extensions**

Future extensions may include:

• generalized entity extraction

• explicit topic-substitution detection

• schema validation beyond key presence

• nested JSON structure validation

• ordered-step preservation

• instruction hierarchy tracking

• semantic requirement extraction

• configurable domain registries

• prompt-specific preservation policies

• regression coverage for adversarial task drift

---

**Design Consequences**

|Principle|Primary Implementation|
|---|---|
|Task Preservation|`task_guard.verify()`|
|Exact Output Enforcement|Exact Phrase Extraction|
|Structured Output Preservation|JSON Key Extraction|
|Requirement Weighting|Hard and Soft Scoring|
|Observable Failure|Missing Requirement Reports|
|Trusted Release|Release Gate|

---

**Related Specifications**

• [[design_philosophy|Design Philosophy]]

• [[zero_point_protocol|Zero Point Protocol]]

• [[coherence_engine|CoherenceEngine]]

• [[repair_engine|RepairEngine]]

• [[trust_circle|Trust Circle]]

• [[release_gate|The Release Gate]]

---

**Engine Observation**

Task preservation is not the same as correctness.

A response may preserve every requested entity, phrase, and structured field while still containing incorrect reasoning.

TaskGuard protects the shape of the task so that other engines can evaluate the quality and correctness of the answer without first losing the operator’s original intent.