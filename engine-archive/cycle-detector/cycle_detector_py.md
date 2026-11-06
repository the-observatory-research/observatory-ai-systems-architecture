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

zpp_id: cycle_detector_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import hashlib
import re


@dataclass
class CycleDetectionResult:
    detected: bool
    cycle_type: Optional[str]
    first_seen_index: Optional[int]
    repeated_index: Optional[int]
    cycle_length: Optional[int]

    normalized_state: Optional[str] = None
    state_hash: Optional[str] = None

    issues: List[str] = field(default_factory=list)
    metadata: Dict[str, object] = field(default_factory=dict)


class CycleDetector:
    """
    Deterministic cycle detector for recursive reasoning traces.

    Version 1 detects:
    - exact normalized state repetition;
    - period-2 oscillation such as A -> B -> A;
    - repeated states across any earlier depth.
    """

    def __init__(
        self,
        *,
        max_history: int = 100,
    ):
        self.max_history = max_history
        self._history: List[str] = []
        self._hash_to_first_index: Dict[str, int] = {}

    def reset(self) -> None:
        self._history.clear()
        self._hash_to_first_index.clear()

    def observe(
        self,
        state: str,
    ) -> CycleDetectionResult:
        normalized = self.normalize_state(state)
        state_hash = self.hash_state(normalized)

        current_index = len(self._history)

        if state_hash in self._hash_to_first_index:
            first_seen_index = self._hash_to_first_index[
                state_hash
            ]

            cycle_length = (
                current_index
                - first_seen_index
            )

            cycle_type = (
                "period_2"
                if cycle_length == 2
                else "repeated_state"
            )

            return CycleDetectionResult(
                detected=True,
                cycle_type=cycle_type,
                first_seen_index=first_seen_index,
                repeated_index=current_index,
                cycle_length=cycle_length,
                normalized_state=normalized,
                state_hash=state_hash,
                issues=[
                    "Repeated reasoning state detected."
                ],
                metadata={
                    "history_size": len(self._history),
                },
            )

        self._history.append(state_hash)
        self._hash_to_first_index[
            state_hash
        ] = current_index

        self._trim_history()

        return CycleDetectionResult(
            detected=False,
            cycle_type=None,
            first_seen_index=None,
            repeated_index=None,
            cycle_length=None,
            normalized_state=normalized,
            state_hash=state_hash,
            issues=[],
            metadata={
                "history_size": len(self._history),
            },
        )

    def detect_sequence(
        self,
        states: List[str],
    ) -> CycleDetectionResult:
        """
        Detect the first repeated state in a complete sequence.

        This resets internal history before scanning.
        """
        self.reset()

        last_result = CycleDetectionResult(
            detected=False,
            cycle_type=None,
            first_seen_index=None,
            repeated_index=None,
            cycle_length=None,
        )

        for state in states:
            last_result = self.observe(state)

            if last_result.detected:
                return last_result

        return last_result

    @staticmethod
    def normalize_state(
        state: str,
    ) -> str:
        """
        Normalize prose enough to detect repeated reasoning states
        despite formatting differences.

        This deliberately does not perform semantic equivalence.
        """
        text = (state or "").lower()

        replacements = {
            "re-evaluate": "reevaluate",
            "re evaluate": "reevaluate",
            "re-start": "restart",
            "start over": "restart",
            "from the beginning": "restart",
        }

        for original, replacement in replacements.items():
            text = text.replace(
                original,
                replacement,
            )

        text = re.sub(
            r"\bdepth\s+\d+\b",
            "depth",
            text,
        )

        text = re.sub(
            r"\bstep\s+\d+\b",
            "step",
            text,
        )

        text = re.sub(
            r"\bpass\s+\d+\b",
            "pass",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        text = re.sub(
            r"[^\w\s=<>:+\-]",
            "",
            text,
        )

        return text.strip()

    @staticmethod
    def hash_state(
        normalized_state: str,
    ) -> str:
        return hashlib.sha256(
            normalized_state.encode("utf-8")
        ).hexdigest()

    def _trim_history(self) -> None:
        if len(self._history) <= self.max_history:
            return

        excess = len(self._history) - self.max_history
        self._history = self._history[excess:]

        self._hash_to_first_index = {
            state_hash: index
            for index, state_hash in enumerate(
                self._history
            )
        }


cycle_detector = CycleDetector()
```