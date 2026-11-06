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

zpp_id: repair_engine_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RepairAction:
    """
    One requested correction in a consolidated repair plan.
    """

    category: str
    priority: int
    instruction: str
    evidence: List[str] = field(default_factory=list)


@dataclass
class RepairPlan:
    """
    Deterministic plan describing whether and how an answer should
    receive one controlled repair pass.
    """

    repair_required: bool
    terminal: bool
    terminal_response: Optional[str]

    actions: List[RepairAction] = field(default_factory=list)
    repair_prompt: str = ""

    reasons: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RepairExecutionResult:
    """
    Result of executing one repair plan.

    Execution is limited to at most one model call.
    """

    attempted: bool
    successful: bool

    original_answer: str
    final_answer: str

    plan: RepairPlan

    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attempted": self.attempted,
            "successful": self.successful,
            "original_answer": self.original_answer,
            "final_answer": self.final_answer,
            "plan": self.plan.to_dict(),
            "error": self.error,
        }


class RepairEngine:
    """
    Consolidate observer evidence into one controlled repair plan.

    This engine does not independently:
    - detect mathematical errors;
    - measure coherence;
    - determine task preservation;
    - detect reasoning cycles;
    - retry repairs.

    It only decides whether to:
    1. terminate;
    2. continue unchanged;
    3. request one consolidated repair.
    """

    PRIORITY_TASK = 100
    PRIORITY_SCHEMA = 95
    PRIORITY_MATH = 90
    PRIORITY_COHERENCE = 80
    PRIORITY_REASONING = 70

    LOOP_RESPONSE = "CRITICAL ERROR: LOOP DETECTED"

    # ============================================================
    # PUBLIC API — PLAN
    # ============================================================

    def plan(
        self,
        *,
        prompt: str,
        answer: str,
        reasoning: Optional[Dict[str, Any]] = None,
        task: Optional[Dict[str, Any]] = None,
        coherence: Optional[Dict[str, Any]] = None,
        math: Optional[Dict[str, Any]] = None,
        cycle: Optional[Dict[str, Any]] = None,
    ) -> RepairPlan:
        """
        Build one deterministic repair plan from observer evidence.
        """

        reasoning_data = reasoning or {}
        task_data = task or {}
        coherence_data = coherence or {}
        math_data = math or {}
        cycle_data = cycle or {}

        if cycle_data.get("detected", False):
            return RepairPlan(
                repair_required=False,
                terminal=True,
                terminal_response=self.LOOP_RESPONSE,
                actions=[],
                repair_prompt="",
                reasons=[
                    "Deterministic cycle detection requested termination."
                ],
                metadata={
                    "cycle_type": cycle_data.get("cycle_type"),
                    "cycle_length": cycle_data.get("cycle_length"),
                },
            )

        actions: List[RepairAction] = []
        reasons: List[str] = []

        self._add_task_actions(
            actions=actions,
            reasons=reasons,
            task=task_data,
        )

        self._add_math_actions(
            actions=actions,
            reasons=reasons,
            math=math_data,
        )

        self._add_coherence_actions(
            actions=actions,
            reasons=reasons,
            coherence=coherence_data,
        )

        self._add_reasoning_actions(
            actions=actions,
            reasons=reasons,
            reasoning=reasoning_data,
        )

        actions.sort(
            key=lambda action: action.priority,
            reverse=True,
        )

        repair_required = bool(actions)

        repair_prompt = ""

        if repair_required:
            repair_prompt = self._build_repair_prompt(
                prompt=prompt,
                answer=answer,
                actions=actions,
            )

        return RepairPlan(
            repair_required=repair_required,
            terminal=False,
            terminal_response=None,
            actions=actions,
            repair_prompt=repair_prompt,
            reasons=reasons,
            metadata={
                "action_count": len(actions),
                "highest_priority": (
                    actions[0].priority
                    if actions
                    else None
                ),
                "categories": [
                    action.category
                    for action in actions
                ],
            },
        )

    # ============================================================
    # PUBLIC API — EXECUTE
    # ============================================================

    def execute(
        self,
        *,
        plan: RepairPlan,
        answer: str,
        model_query: Callable[[list], str],
    ) -> RepairExecutionResult:
        """
        Execute at most one repair call.

        This method never retries and never creates a repair loop.
        """

        if plan.terminal:
            return RepairExecutionResult(
                attempted=False,
                successful=True,
                original_answer=answer,
                final_answer=(
                    plan.terminal_response
                    or answer
                ),
                plan=plan,
                error=None,
            )

        if not plan.repair_required:
            return RepairExecutionResult(
                attempted=False,
                successful=True,
                original_answer=answer,
                final_answer=answer,
                plan=plan,
                error=None,
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a precise repair peer. "
                    "Follow the repair plan exactly. "
                    "Do not discuss the repair process. "
                    "Return only the corrected final answer."
                ),
            },
            {
                "role": "user",
                "content": plan.repair_prompt,
            },
        ]

        try:
            repaired_answer = model_query(
                messages
            ).strip()

            if (
                not repaired_answer
                or repaired_answer.startswith(
                    "[CONNECTION_ERROR]"
                )
            ):
                return RepairExecutionResult(
                    attempted=True,
                    successful=False,
                    original_answer=answer,
                    final_answer=answer,
                    plan=plan,
                    error=(
                        repaired_answer
                        or "Repair peer returned an empty response."
                    ),
                )

            return RepairExecutionResult(
                attempted=True,
                successful=True,
                original_answer=answer,
                final_answer=repaired_answer,
                plan=plan,
                error=None,
            )

        except Exception as exc:
            return RepairExecutionResult(
                attempted=True,
                successful=False,
                original_answer=answer,
                final_answer=answer,
                plan=plan,
                error=repr(exc),
            )

    # ============================================================
    # TASK PRESERVATION
    # ============================================================

    def _add_task_actions(
        self,
        *,
        actions: List[RepairAction],
        reasons: List[str],
        task: Dict[str, Any],
    ) -> None:
        if not task:
            return

        preserved = bool(
            task.get(
                "preserved",
                True,
            )
        )

        missing_terms = self._string_list(
            task.get("missing_terms")
        )

        missing_phrases = self._string_list(
            task.get("missing_phrases")
        )

        missing_json_keys = self._string_list(
            task.get("missing_json_keys")
        )

        issues = self._string_list(
            task.get("issues")
        )

        if missing_json_keys:
            actions.append(
                RepairAction(
                    category="schema",
                    priority=self.PRIORITY_SCHEMA,
                    instruction=(
                        "Return the answer in the required structured "
                        "format and include every required JSON key."
                    ),
                    evidence=[
                        f"Missing JSON key: {key}"
                        for key in missing_json_keys
                    ],
                )
            )

            reasons.append(
                "Required output schema was not preserved."
            )

        if missing_phrases:
            actions.append(
                RepairAction(
                    category="task",
                    priority=self.PRIORITY_TASK,
                    instruction=(
                        "Honor every exact-output instruction from the "
                        "original task. When an exact phrase is required, "
                        "return that phrase exactly."
                    ),
                    evidence=[
                        f"Missing required phrase: {phrase}"
                        for phrase in missing_phrases
                    ],
                )
            )

            reasons.append(
                "An exact required phrase was missing."
            )

        if not preserved and missing_terms:
            actions.append(
                RepairAction(
                    category="task",
                    priority=self.PRIORITY_TASK,
                    instruction=(
                        "Return to the original task. Do not substitute "
                        "a different scenario, puzzle, domain, or set of "
                        "entities. Restore the missing task concepts."
                    ),
                    evidence=[
                        f"Missing task concept: {term}"
                        for term in missing_terms
                    ],
                )
            )

            reasons.append(
                "The response drifted away from the original task."
            )

        elif (
            not preserved
            and issues
            and not missing_json_keys
            and not missing_phrases
        ):
            actions.append(
                RepairAction(
                    category="task",
                    priority=self.PRIORITY_TASK,
                    instruction=(
                        "Restore fidelity to the original task and satisfy "
                        "its explicit requirements."
                    ),
                    evidence=issues,
                )
            )

            reasons.append(
                "Task preservation failed."
            )

    # ============================================================
    # MATHEMATICS
    # ============================================================

    def _add_math_actions(
        self,
        *,
        actions: List[RepairAction],
        reasons: List[str],
        math: Dict[str, Any],
    ) -> None:
        if not math:
            return

        verifiable = bool(
            math.get(
                "verifiable",
                False,
            )
        )

        verified = bool(
            math.get(
                "verified",
                False,
            )
        )

        issues = self._string_list(
            math.get("issues")
        )

        if not verifiable or verified:
            return

        evidence = list(issues)

        computed = math.get("computed")

        if computed:
            evidence.append(
                "Deterministic reference values are available "
                "and must be followed."
            )

            evidence.append(
                f"Reference values: {computed}"
            )

        actions.append(
            RepairAction(
                category="math",
                priority=self.PRIORITY_MATH,
                instruction=(
                    "Correct all deterministically identified mathematical "
                    "errors. Recompute the affected steps, preserve correct "
                    "work, distinguish total distance from displacement "
                    "when relevant, and use the supplied reference values."
                ),
                evidence=evidence,
            )
        )

        reasons.append(
            "Deterministic mathematical verification failed."
        )

    # ============================================================
    # COHERENCE
    # ============================================================

    def _add_coherence_actions(
        self,
        *,
        actions: List[RepairAction],
        reasons: List[str],
        coherence: Dict[str, Any],
    ) -> None:
        if not coherence:
            return

        coherent = bool(
            coherence.get(
                "coherent",
                True,
            )
        )

        issues = self._string_list(
            coherence.get("issues")
        )

        task_alignment = self._safe_float(
            coherence.get("task_alignment"),
            default=1.0,
        )

        internal_consistency = self._safe_float(
            coherence.get("internal_consistency"),
            default=1.0,
        )

        topic_drift = self._safe_float(
            coherence.get("topic_drift"),
            default=0.0,
        )

        if coherent:
            return

        instruction_parts: List[str] = []

        if (
            task_alignment < 0.50
            or topic_drift >= 0.50
        ):
            instruction_parts.append(
                "Remove unrelated material and restore direct alignment "
                "with the original task."
            )

        if internal_consistency < 1.0:
            instruction_parts.append(
                "Resolve all internal contradictions so mutually "
                "incompatible claims do not remain."
            )

        if not instruction_parts:
            instruction_parts.append(
                "Improve semantic coherence while preserving all correct "
                "and relevant content."
            )

        actions.append(
            RepairAction(
                category="coherence",
                priority=self.PRIORITY_COHERENCE,
                instruction=" ".join(
                    instruction_parts
                ),
                evidence=issues,
            )
        )

        reasons.append(
            "The coherence observer found semantic or logical instability."
        )

    # ============================================================
    # REASONING
    # ============================================================

    def _add_reasoning_actions(
        self,
        *,
        actions: List[RepairAction],
        reasons: List[str],
        reasoning: Dict[str, Any],
    ) -> None:
        if not reasoning:
            return

        issues_detected = self._safe_int(
            reasoning.get("issues_detected"),
            default=0,
        )

        converged = reasoning.get(
            "converged"
        )

        convergence_similarity = reasoning.get(
            "convergence_similarity"
        )

        unresolved = (
            converged is False
            or (
                issues_detected > 0
                and convergence_similarity is not None
                and self._safe_float(
                    convergence_similarity,
                    default=1.0,
                ) < 0.985
            )
        )

        if not unresolved:
            return

        evidence = [
            f"Outstanding issues detected: {issues_detected}",
        ]

        if convergence_similarity is not None:
            evidence.append(
                "Convergence similarity: "
                f"{convergence_similarity}"
            )

        actions.append(
            RepairAction(
                category="reasoning",
                priority=self.PRIORITY_REASONING,
                instruction=(
                    "Resolve the remaining reasoning issues. Preserve "
                    "correct conclusions, repair unsupported assumptions, "
                    "and answer the original question directly."
                ),
                evidence=evidence,
            )
        )

        reasons.append(
            "Recursive reasoning did not fully converge."
        )

    # ============================================================
    # PROMPT CONSTRUCTION
    # ============================================================

    def _build_repair_prompt(
        self,
        *,
        prompt: str,
        answer: str,
        actions: List[RepairAction],
    ) -> str:
        sections: List[str] = [
            (
                "Revise the current answer using the independent "
                "verification evidence below."
            ),
            (
                "Preserve every correct part of the answer. Make only "
                "the changes required to satisfy the evidence."
            ),
            (
                "Do not mention the repair process, observers, audits, "
                "or internal framework."
            ),
            (
                "Return only the corrected final answer in the format "
                "required by the original task."
            ),
            "",
            "ORIGINAL TASK:",
            prompt.strip(),
            "",
            "CURRENT ANSWER:",
            answer.strip(),
            "",
            "REQUIRED REPAIRS:",
        ]

        for index, action in enumerate(
            actions,
            start=1,
        ):
            sections.append(
                f"{index}. [{action.category.upper()}] "
                f"{action.instruction}"
            )

            for evidence_item in action.evidence:
                sections.append(
                    f"   - {evidence_item}"
                )

        return "\n".join(
            sections
        ).strip()

    # ============================================================
    # HELPERS
    # ============================================================

    @staticmethod
    def _string_list(
        value: Any,
    ) -> List[str]:
        if value is None:
            return []

        if isinstance(value, str):
            return [
                value
            ] if value.strip() else []

        if isinstance(
            value,
            (list, tuple, set),
        ):
            return [
                str(item)
                for item in value
                if str(item).strip()
            ]

        return [str(value)]

    @staticmethod
    def _safe_float(
        value: Any,
        *,
        default: float,
    ) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_int(
        value: Any,
        *,
        default: int,
    ) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default


repair_engine = RepairEngine()
```