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

zpp_id: test_coherence_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from coherence_engine import coherence_engine


def run_test(
    name: str,
    prompt: str,
    response: str,
    context=None,
) -> None:
    print(f"\n=== {name} ===")

    result = coherence_engine.verify(
        prompt=prompt,
        response=response,
        context=context or [],
    )

    print("Coherent:", result.coherent)
    print("Score:", result.score)
    print("Confidence:", result.confidence)
    print("Task alignment:", result.task_alignment)
    print("Context continuity:", result.context_continuity)
    print("Internal consistency:", result.internal_consistency)
    print("Topic drift:", result.topic_drift)
    print("Issues:")

    if result.issues:
        for issue in result.issues:
            print(" -", issue)
    else:
        print(" - None")

    print("Warnings:")

    if result.warnings:
        for warning in result.warnings:
            print(" -", warning)
    else:
        print(" - None")

    print("Computed:", result.computed)


# ============================================================
# TEST 1 — GOOD TASK ALIGNMENT
# ============================================================

run_test(
    "TEST 1 — BAT AND BALL CORRECT",
    prompt="""
A bat and a ball cost $1.10 in total.
The bat costs $1.00 more than the ball.
How much does the ball cost?
""",
    response="""
Let the ball cost x dollars. Then the bat costs x + 1.00.
Therefore x + (x + 1.00) = 1.10, so 2x = 0.10 and x = 0.05.
The ball costs $0.05.
""",
)


# ============================================================
# TEST 2 — SEVERE TASK DRIFT
# ============================================================

run_test(
    "TEST 2 — BAT AND BALL BECOMES SNAIL",
    prompt="""
A bat and a ball cost $1.10 in total.
The bat costs $1.00 more than the ball.
How much does the ball cost?
""",
    response="""
A snail climbs three feet during the day and slips two feet
during the night. It reaches the top of the well in 18 days.
""",
)


# ============================================================
# TEST 3 — TAX TASK DRIFT
# ============================================================

run_test(
    "TEST 3 — TAX BECOMES LABOR ALLOCATION",
    prompt="""
Calculate Total Regional Tax.

Base Revenue = Active Users * Average Spend.
Active Users = 50,000.
Average Spend = (120 - 20) / 2.
Luxury Surcharge = Base Revenue * 0.10.
Subsidy Credit = 2,500.
""",
    response="""
A company has 100 units of labor to allocate between Line A
and Line B. Total profit is maximized by testing each labor amount.
""",
)


# ============================================================
# TEST 4 — DIRECT INTERNAL CONTRADICTION
# ============================================================

run_test(
    "TEST 4 — INTERNAL CONTRADICTION",
    prompt="""
Determine whether the sequence converges.
""",
    response="""
The sequence converges to zero.
The sequence does not converge because its oscillations persist.
""",
)


# ============================================================
# TEST 5 — CONCISE VALID JSON
# ============================================================

run_test(
    "TEST 5 — CONCISE JSON",
    prompt="""
Return a JSON compliance log containing keys:
"sql_vulnerable"
"cookie_vulnerable"
""",
    response="""
{
  "sql_vulnerable": true,
  "cookie_vulnerable": true
}
""",
)


# ============================================================
# TEST 6 — CONTEXT CONTINUITY
# ============================================================

run_test(
    "TEST 6 — CONTEXT CONTINUITY",
    prompt="""
Explain why total distance differs from displacement.
""",
    response="""
Displacement compares only the initial and final positions,
while total distance adds the absolute distance traveled across
every interval where direction changes.
""",
    context=[
        {
            "role": "user",
            "content": (
                "We are analyzing polynomial motion and velocity roots."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "Velocity roots identify the times when direction may change."
            ),
        },
    ],
)
```