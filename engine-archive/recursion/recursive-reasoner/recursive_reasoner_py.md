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

zpp_id: recursive_reasoner_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
import difflib
import re

from dataclasses import dataclass
from typing import Callable, List, Tuple

from cycle_detector import CycleDetector

@dataclass
class ReasoningStep:
    depth: int
    answer: str
    critique: str
    similarity_to_previous: float
    unresolved_issues: List[str]


class RecursiveReasoner:
    def __init__(
        self,
        model_query: Callable[[list], str],
        max_depth: int = 5,
        convergence_threshold: float = 0.985,
    ):
        self.model_query = model_query
        self.max_depth = max_depth
        self.convergence_threshold = convergence_threshold

    @staticmethod
    def _similarity(previous: str, current: str) -> float:
        return difflib.SequenceMatcher(None, previous.strip(), current.strip()).ratio()

    @staticmethod
    def _extract_issues(critique: str) -> List[str]:
        issues = re.findall(r"(?im)^\s*ISSUE:\s*(.+?)\s*$", critique)
        return [issue.strip() for issue in issues]

    def _critique(self, prompt: str, answer: str, depth: int) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an adversarial reasoning auditor. "
                    "Inspect the proposed answer for logical gaps, unsupported "
                    "assumptions, contradictions, missed edge cases, numerical "
                    "errors, and failures to answer the original question. "
                    "Do not rewrite the answer. For every material problem, "
                    "write one line beginning with 'ISSUE:'. "
                    "If there are no material issues, output exactly: NO_ISSUES"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original problem:\n{prompt}\n\n"
                    f"Proposed answer at recursion depth {depth}:\n{answer}"
                ),
            },
        ]
        return self.model_query(messages).strip()

    def _revise(
        self,
        prompt: str,
        previous_answer: str,
        critique: str,
        depth: int,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a rigorous problem solver. Revise the answer using "
                    "the audit. Preserve correct material, repair every valid "
                    "issue, and show necessary derivations. "
                    "Output only the final user-facing answer itself. "
                    "Do not add a heading, preface, label, or introductory sentence. "
                    "Never write phrases such as 'Here is the revised answer', "
                    "'Here is the corrected answer', 'Here is the improved answer', "
                    "or similar wording. "
                    "Do not mention revision, repair, audit, verification, "
                    "internal instructions, or internal processing."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original problem:\n{prompt}\n\n"
                    f"Previous answer:\n{previous_answer}\n\n"
                    f"Audit at recursion depth {depth}:\n{critique}"
                ),
            },
        ]
        revised = self.model_query(messages).strip()

        for prefix in (
            "Here is the revised answer:",
            "Here is the corrected answer:",
            "Here is the improved answer:",
            "Revised answer:",
            "Corrected answer:",
            "Improved answer:",
        ):
            if revised.lower().startswith(prefix.lower()):
                revised = revised[len(prefix):].lstrip()
                break

        return revised

    def reason(
        self,
        prompt: str,
        initial_answer: str,
    ) -> Tuple[str, List[ReasoningStep]]:
        current_answer = initial_answer.strip()
        trace: List[ReasoningStep] = []
        cycle_detector = CycleDetector()
        cycle_detector.observe(current_answer)

        for depth in range(1, self.max_depth + 1):
            critique = self._critique(prompt, current_answer, depth)
            issues = self._extract_issues(critique)
            if critique == "NO_ISSUES" or not issues:
                trace.append(
                    ReasoningStep(
                        depth=depth,
                        answer=current_answer,
                        critique=critique,
                        similarity_to_previous=1.0,
                        unresolved_issues=[],
                    )
                )
                break

            revised_answer = self._revise(
                prompt=prompt,
                previous_answer=current_answer,
                critique=critique,
                depth=depth,
            )
            if not revised_answer or revised_answer.startswith("[CONNECTION_ERROR]"):
                break

            cycle_result = cycle_detector.observe(revised_answer)
            if cycle_result.detected:
                if "critical error: loop detected" in prompt.lower():
                    trace.append(
                        ReasoningStep(
                            depth=depth,
                            answer="CRITICAL ERROR: LOOP DETECTED",
                            critique=(
                                "Deterministic cycle detector found a repeated "
                                f"reasoning state of length {cycle_result.cycle_length}."
                            ),
                            similarity_to_previous=1.0,
                            unresolved_issues=[],
                        )
                    )
                    return "CRITICAL ERROR: LOOP DETECTED", trace
                break

            similarity = self._similarity(current_answer, revised_answer)
            trace.append(
                ReasoningStep(
                    depth=depth,
                    answer=revised_answer,
                    critique=critique,
                    similarity_to_previous=similarity,
                    unresolved_issues=issues,
                )
            )
            current_answer = revised_answer
            if similarity >= self.convergence_threshold:
                break
        return current_answer, trace
```