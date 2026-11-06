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

zpp_id: test_repair_engine
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from repair_engine import repair_engine


def show_plan(name, plan):
    print(f"\n=== {name} ===")
    print("Repair required:", plan.repair_required)
    print("Terminal:", plan.terminal)
    print("Terminal response:", plan.terminal_response)
    print("Reasons:", plan.reasons)
    print("Actions:")

    if not plan.actions:
        print(" - None")
    else:
        for action in plan.actions:
            print(
                f" - {action.priority} "
                f"[{action.category}] "
                f"{action.instruction}"
            )

            for evidence in action.evidence:
                print(f"     • {evidence}")

    print("Metadata:", plan.metadata)

    if plan.repair_prompt:
        print("\nRepair prompt:")
        print(plan.repair_prompt)


# ============================================================
# TEST 1 — HEALTHY ANSWER
# ============================================================

healthy = repair_engine.plan(
    prompt="What is 2 + 2?",
    answer="2 + 2 = 4.",
    reasoning={
        "issues_detected": 0,
        "convergence_similarity": 1.0,
        "converged": True,
    },
    task={
        "preserved": True,
        "missing_terms": [],
        "missing_phrases": [],
        "missing_json_keys": [],
        "issues": [],
    },
    coherence={
        "coherent": True,
        "task_alignment": 1.0,
        "internal_consistency": 1.0,
        "topic_drift": 0.0,
        "issues": [],
    },
    math={
        "verifiable": True,
        "verified": True,
        "issues": [],
    },
    cycle={
        "detected": False,
    },
)

show_plan(
    "TEST 1 — HEALTHY ANSWER",
    healthy,
)


# ============================================================
# TEST 2 — TASK DRIFT
# ============================================================

task_drift = repair_engine.plan(
    prompt=(
        "A bat and a ball cost $1.10. "
        "How much does the ball cost?"
    ),
    answer=(
        "A snail climbs a well and reaches the top "
        "after several days."
    ),
    task={
        "preserved": False,
        "missing_terms": [
            "bat",
            "ball",
        ],
        "missing_phrases": [],
        "missing_json_keys": [],
        "issues": [
            "Important task concepts were not preserved."
        ],
    },
    coherence={
        "coherent": False,
        "task_alignment": 0.2,
        "internal_consistency": 1.0,
        "topic_drift": 0.9,
        "issues": [
            "Severe topic drift detected."
        ],
    },
)

show_plan(
    "TEST 2 — TASK DRIFT",
    task_drift,
)


# ============================================================
# TEST 3 — MATH FAILURE
# ============================================================

math_failure = repair_engine.plan(
    prompt=(
        "Find the total distance traveled by the particle "
        "from t=0 to t=3."
    ),
    answer="The total distance is 36 meters.",
    math={
        "verifiable": True,
        "verified": False,
        "confidence": 1.0,
        "verifier": "polynomial_motion",
        "issues": [
            (
                "Claimed total distance 36 does not match "
                "the computed total distance 22.5."
            )
        ],
        "computed": {
            "total_distance": 22.5,
            "net_displacement": 9.0,
        },
    },
)

show_plan(
    "TEST 3 — MATH FAILURE",
    math_failure,
)


# ============================================================
# TEST 4 — JSON SCHEMA FAILURE
# ============================================================

schema_failure = repair_engine.plan(
    prompt=(
        'Return JSON with keys "sql_vulnerable" '
        'and "cookie_vulnerable".'
    ),
    answer="The SQL query is unsafe.",
    task={
        "preserved": False,
        "missing_terms": [],
        "missing_phrases": [],
        "missing_json_keys": [
            "sql_vulnerable",
            "cookie_vulnerable",
        ],
        "issues": [
            "Required JSON keys were missing."
        ],
    },
)

show_plan(
    "TEST 4 — JSON SCHEMA FAILURE",
    schema_failure,
)


# ============================================================
# TEST 5 — MULTIPLE FAILURES
# ============================================================

multiple_failures = repair_engine.plan(
    prompt="Solve the original tax problem and return JSON.",
    answer="A labor-allocation puzzle has several possible answers.",
    reasoning={
        "issues_detected": 3,
        "convergence_similarity": 0.72,
        "converged": False,
    },
    task={
        "preserved": False,
        "missing_terms": [
            "Base Revenue",
            "Luxury Surcharge",
        ],
        "missing_phrases": [],
        "missing_json_keys": [
            "total_regional_tax",
        ],
        "issues": [
            "The original task was replaced."
        ],
    },
    coherence={
        "coherent": False,
        "task_alignment": 0.18,
        "internal_consistency": 0.65,
        "topic_drift": 0.88,
        "issues": [
            "Severe topic drift detected.",
            "Potential contradiction detected.",
        ],
    },
    math={
        "verifiable": True,
        "verified": False,
        "issues": [
            "The required tax calculation was not completed."
        ],
        "computed": {
            "total_regional_tax": 385000.0,
        },
    },
)

show_plan(
    "TEST 5 — MULTIPLE FAILURES",
    multiple_failures,
)


# ============================================================
# TEST 6 — CYCLE TERMINATION
# ============================================================

cycle_failure = repair_engine.plan(
    prompt=(
        "If a repeated state occurs, output exactly "
        "CRITICAL ERROR: LOOP DETECTED"
    ),
    answer="Evaluate Property B again.",
    cycle={
        "detected": True,
        "cycle_type": "period_2",
        "cycle_length": 2,
    },
)

show_plan(
    "TEST 6 — CYCLE TERMINATION",
    cycle_failure,
)
```