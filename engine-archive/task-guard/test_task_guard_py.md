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

zpp_id: test_task_guard_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from task_guard import task_guard


def run_test(
    name: str,
    prompt: str,
    response: str,
) -> None:
    print(f"\n=== {name} ===")

    result = task_guard.verify(
        prompt=prompt,
        response=response,
    )

    print("Preserved:", result.preserved)
    print("Score:", result.score)
    print("Required terms:", result.required_terms)
    print("Missing terms:", result.missing_terms)
    print("Required phrases:", result.required_phrases)
    print("Missing phrases:", result.missing_phrases)
    print("Required JSON keys:", result.required_json_keys)
    print("Missing JSON keys:", result.missing_json_keys)
    print("Issues:")

    if result.issues:
        for issue in result.issues:
            print(" -", issue)
    else:
        print(" - None")


# ============================================================
# TEST 1 — LOOP DETECTION
# ============================================================

loop_prompt = """
Analyze the following logical sequence to determine if Object A
belongs to Category Z.

If you run into a cycle where you repeat a previously analyzed step,
output the exact phrase: "CRITICAL ERROR: LOOP DETECTED"
and terminate.

Premises:
1. If an object has Property A, check Property B.
2. Property B requires evaluating Property C.
3. Property C states that if Property D is false,
   then Property B must be re-evaluated from the beginning.
4. Object A has Property A.
5. Property D is permanently false.
"""

loop_wrong_response = """
Object A has Property X and should next be checked for Property Y.
If both are present, Condition Z can be evaluated.
"""

run_test(
    "TEST 1 — LOOP DETECTION",
    loop_prompt,
    loop_wrong_response,
)


# ============================================================
# TEST 2 — NESTED ECONOMIC EQUATION
# ============================================================

tax_prompt = """
Calculate Total Regional Tax.

TRT = (Base Revenue * 0.15)
    + (Luxury Surcharge * 0.05)
    - Subsidy Credit.

Base Revenue = Active Users * Average Spend.
Active Users = 50,000.
Average Spend = (120 - 20) / 2.
Luxury Surcharge = Base Revenue * 0.10.
Subsidy Credit = 2,500.
"""

tax_wrong_response = """
A company has 100 units of labor to allocate between Line A
and Line B. The goal is to maximize total profit.
"""

run_test(
    "TEST 2 — NESTED ECONOMIC EQUATION",
    tax_prompt,
    tax_wrong_response,
)


# ============================================================
# TEST 3 — BAT AND BALL
# ============================================================

bat_ball_prompt = """
A bat and a ball cost $1.10 in total.
The bat costs $1.00 more than the ball.

Output only the final corrected value in a clean JSON block.
"""

bat_ball_wrong_response = """
A snail is at the bottom of a 20-foot well.
It climbs 3 feet each day and slips back 2 feet each night.
It reaches the top in 21 days.
"""

run_test(
    "TEST 3 — BAT AND BALL",
    bat_ball_prompt,
    bat_ball_wrong_response,
)


# ============================================================
# TEST 4 — CODE AUDIT
# ============================================================

code_prompt = """
Audit the following code in two chunks.

Chunk 1 must be checked for SQL injection.
Chunk 2 must be checked for cookie security flaws.

Return a single JSON compliance log containing keys:
"sql_vulnerable"
"cookie_vulnerable"

Chunk 1:
query = f"SELECT * FROM users WHERE username = '{username}'"

Chunk 2:
response.set_cookie(
    "session_id",
    token,
    secure=False,
    httponly=False,
)
"""

code_wrong_response = """
The username should be sanitized and prepared statements should
be used to avoid SQL injection.
"""

run_test(
    "TEST 4 — CODE AUDIT",
    code_prompt,
    code_wrong_response,
)


# ============================================================
# CONTROL TEST — PRESERVED TASK
# ============================================================

correct_response = """
{
  "sql_vulnerable": true,
  "cookie_vulnerable": true
}
"""

run_test(
    "CONTROL — CORRECT JSON RESPONSE",
    code_prompt,
    correct_response,
)
```