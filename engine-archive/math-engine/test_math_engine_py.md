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

zpp_id: test_math_engine_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from math_engine import (
    math_engine,
    MATH_ENGINE_VERSION,
)

# ============================================================
# TEST 1 — INCORRECT ANSWER IS REJECTED
# ============================================================

problem = r"""
A particle moves along a straight line such that its position
at time t is given by:

s(t) = 4t^3 - 15t^2 + 12t + 8

Calculate velocity and acceleration.
Determine where it moves right and left.
Calculate total distance traveled from t = 0 to t = 3.
"""


answer = r"""
Velocity:
v(t) = 12t^2 - 30t + 12

Acceleration:
a(t) = 24t - 30

The particle moves left for 0 <= t < 5/4 and right for t >= 5/4.

The total distance traveled from t = 0 to t = 3 is 36 meters.
"""


result = math_engine.verify(
    problem=problem,
    answer=answer,
)

print("Verified:", result.verified)
print("Verifiable:", result.verifiable)
print("Confidence:", result.confidence)
print("Issues:")

for issue in result.issues:
    print(" -", issue)

print("Computed:", result.computed)
print("Extracted:", result.extracted)

# ============================================================
# TEST 2 — DETERMINISTIC RENDERER ROUND TRIP
# ============================================================

rendered_answer = math_engine.render_verified_answer(
    problem=problem,
    result=result,
)

print("\n=== TEST 2 — DETERMINISTIC RENDERER ===")
print(rendered_answer)

assert rendered_answer is not None
assert "22.5" in rendered_answer
assert "t = 0.5" in rendered_answer
assert "t = 2" in rendered_answer
assert "moves right" in rendered_answer.lower()
assert "moves left" in rendered_answer.lower()

rendered_result = math_engine.verify(
    problem=problem,
    answer=rendered_answer,
)

print("\n=== TEST 3 — RENDERED ANSWER RECHECK ===")
print("Verified:", rendered_result.verified)
print("Verifiable:", rendered_result.verifiable)
print("Confidence:", rendered_result.confidence)
print("Issues:", rendered_result.issues)
print("Extracted:", rendered_result.extracted)

assert rendered_result.verifiable is True
assert rendered_result.verified is True
assert rendered_result.issues == []

print(
    f"\n✅ MathEngine v{MATH_ENGINE_VERSION} regression tests passed."
)
```