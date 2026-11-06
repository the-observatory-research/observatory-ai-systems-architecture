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

zpp_id: test_cycle_detector_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from cycle_detector import CycleDetector


def run_test(
    name: str,
    states: list[str],
) -> None:
    detector = CycleDetector()

    result = detector.detect_sequence(states)

    print(f"\n=== {name} ===")
    print("Detected:", result.detected)
    print("Cycle type:", result.cycle_type)
    print("First seen index:", result.first_seen_index)
    print("Repeated index:", result.repeated_index)
    print("Cycle length:", result.cycle_length)
    print("Normalized state:", result.normalized_state)
    print("Issues:", result.issues)


run_test(
    "TEST 1 — DIRECT REPEAT",
    [
        "Evaluate Property B",
        "Evaluate Property C",
        "Evaluate Property B",
    ],
)


run_test(
    "TEST 2 — NORMALIZED REPEAT",
    [
        "Step 1: Re-evaluate Property B from the beginning.",
        "Step 2: Evaluate Property C.",
        "Step 3: reevaluate Property B restart.",
    ],
)


run_test(
    "TEST 3 — NO CYCLE",
    [
        "Evaluate Property A",
        "Evaluate Property B",
        "Evaluate Property C",
        "Determine Category Z",
    ],
)


run_test(
    "TEST 4 — LONGER CYCLE",
    [
        "State A",
        "State B",
        "State C",
        "State A",
    ],
)


run_test(
    "TEST 5 — IDENTICAL FINAL OUTPUT",
    [
        "The answer is 42.",
        "The answer is 42.",
    ],
)
```