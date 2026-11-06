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

zpp_id: gatekeeper_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
import hashlib
import json
import sys
import time

from typing import Callable, List, Tuple

from math_engine import math_engine
from task_guard import task_guard
from coherence_engine import coherence_engine
from repair_engine import repair_engine

from recursion.reasoner import ReasoningStep, RecursiveReasoner

# ────────────────────────────────────────────────────────────
# RECURSIVE GATEKEEPER
# ────────────────────────────────────────────────────────────
class RecursiveGatekeeper:
    def __init__(
        self,
        config_path: str,
        model_query: Callable[[list], str],
        context_lock,
        conversation_context,
    ):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.model_query = model_query
        self.context_lock = context_lock
        self.conversation_context = conversation_context

        self.gates = self.config.get("simulated_pipeline", {})
        self.constraint = 0.5
        self.constraint_threshold = 0.9
        self.cooldown = False
        self.cooldown_until = 0
        self.ledger = []
        self.last_reasoning_metrics = {
            "recursion_depth": 0,
            "issues_detected": 0,
            "convergence_similarity": None,
        }
        self.last_math_metrics = {
            "verifiable": False,
            "verified": False,
            "confidence": 0.0,
            "verifier": None,
            "issues": [],
        }
        self.last_task_metrics = {
            "preserved": True,
            "score": 1.0,
            "missing_terms": [],
            "missing_phrases": [],
            "missing_json_keys": [],
            "issues": [],
        }
        self.last_coherence_metrics = {
            "coherent": True,
            "score": 1.0,
            "confidence": 0.0,
            "task_alignment": 1.0,
            "context_continuity": 1.0,
            "internal_consistency": 1.0,
            "topic_drift": 0.0,
            "issues": [],
            "warnings": [],
        }
        self.last_repair_metrics = {
            "required": False,
            "attempted": False,
            "successful": False,
            "terminal": False,
            "actions": [],
            "reasons": [],
            "error": None,
        }
        self.last_final_verification = {
            "passed": False,
            "task": {},
            "coherence": {},
            "math": {},
        }
        self.max_depth = 3
        self.reasoner = RecursiveReasoner(
            model_query=model_query,
            max_depth=self.max_depth,
            convergence_threshold=0.985,
        )

    def check_lcp(self, payload: dict) -> Tuple[bool, str]:
        if self.cooldown and time.time() < self.cooldown_until:
            return False, "LCP cooldown active"
        if payload.get("tax", 0.0) > 0.1:
            self.constraint = min(
                self.constraint * 1.5 + 0.1,
                self.constraint_threshold,
            )
            if self.constraint >= self.constraint_threshold:
                self.cooldown = True
                self.cooldown_until = time.time() + 30
                return False, "LCP constraint exceeded — cooldown"
            return False, "LCP violation — constraint tightened"
        self.constraint = max(0.1, self.constraint * 0.9)
        self.cooldown = False
        return True, "LCP passed"

    def check_vre(
        self,
        prompt: str,
        response: str,
    ) -> Tuple[bool, str]:
        has_mbp = "[MBP]" in response or "MBP:" in response
        has_dcl = "[DCL]" in response or "DCL:" in response
        if not (has_mbp and has_dcl):
            return (
                False,
                "VRE failed — missing invariant metadata structural traces (MBP/DCL)",
            )
        return True, "VRE passed — architectural structural validation verified"

    def build_vre_audit(
        self,
        response: str,
        reasoning_steps: List[ReasoningStep],
    ) -> str:
        total_issues = sum(len(step.unresolved_issues) for step in reasoning_steps)
        final_similarity = (
            reasoning_steps[-1].similarity_to_previous if reasoning_steps else 1.0
        )
        return (
            f"{response}\n\n"
            f"[MBP] refinement_depth={len(reasoning_steps)}; issues_detected={total_issues}\n"
            f"[DCL] convergence_similarity={final_similarity:.4f}; counterfactual_audit=true"
        )

    def repair_math_answer(
        self,
        prompt: str,
        answer: str,
        math_result,
    ) -> str:
        issues_text = "\n".join(f"- {issue}" for issue in math_result.issues)
        computed_text = json.dumps(math_result.computed, indent=2, default=str)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a rigorous mathematical repair engine. "
                    "Correct the answer using the deterministic verification "
                    "results provided. Preserve all correct work. "
                    "Output only the user-facing answer itself. "
                    "Do not add an introduction, heading, preface, or explanation. "
                    "Never write phrases such as 'Here is the revised answer', "
                    "'Here is the corrected answer', or similar wording. "
                    "Do not mention repair, revision, verification, evaluation, "
                    "internal instructions, or internal processing."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original problem:\n{prompt}\n\n"
                    f"Current answer:\n{answer}\n\n"
                    f"Deterministic verification issues:\n"
                    f"{issues_text}\n\n"
                    f"Computed reference values:\n"
                    f"{computed_text}"
                ),
            },
        ]
        repaired = self.reasoner.model_query(messages).strip()

        if not repaired or repaired.startswith("[CONNECTION_ERROR]"):
            return answer

        for prefix in (
            "Here is the revised answer:",
            "Here is the corrected answer:",
            "Here is the improved answer:",
            "Revised answer:",
            "Corrected answer:",
            "Improved answer:",
        ):
            if repaired.lower().startswith(prefix.lower()):
                repaired = repaired[len(prefix):].lstrip()
                break

        return repaired

    def hash_state(self, payload: dict) -> str:
        state_str = json.dumps(payload, sort_keys=True) + str(time.time())
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

    def log_state(self, payload: dict, status: str, trace: List[str]):
        entry = {
            "timestamp": int(time.time()),
            "status": status,
            "trace": trace,
            "payload_hash": self.hash_state(payload),
            "constraint": round(self.constraint, 4),
        }
        self.ledger.append(entry)
        try:
            with open("/PATH/TO/LOCAL/VAULT/ledger/gatekeeper.jsonl", "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            sys.stderr.write(f"[GATEKEEPER] Ledger write failed: {e}\n")

    def process(self, prompt: str, response: str) -> Tuple[bool, str, List[str]]:
            trace = []
            payload = {"text": response, "tax": 0.0, "state": "GAMMA_LOCK"}

            # 1. Check LCP first
            lcp_ok, lcp_msg = self.check_lcp(payload)
            trace.append(lcp_msg)
            if not lcp_ok:
                self.log_state(payload, "BLOCKED_LCP", trace)
                return False, response, trace

            # ------------------------------------------------------------
            # STEP 1 & 2: INITIAL LLM ANSWER -> RECURSIVE REASONER
            # ------------------------------------------------------------
            final_response, reasoning_steps = self.reasoner.reason(prompt, response)

            recursion_depth = len(reasoning_steps)
            issues_detected = sum(len(step.unresolved_issues) for step in reasoning_steps)
            convergence_similarity = (
                reasoning_steps[-1].similarity_to_previous if reasoning_steps else None
            )
            reasoning_converged = (
                not reasoning_steps
                or not reasoning_steps[-1].unresolved_issues
            )

            self.last_reasoning_metrics = {
                "recursion_depth": recursion_depth,
                "issues_detected": issues_detected,
                "convergence_similarity": convergence_similarity,
                "converged": reasoning_converged,
            }
        
            for step in reasoning_steps:
                trace.append(f"Depth {step.depth}: {len(step.unresolved_issues)} issue(s) detected, similarity={step.similarity_to_previous:.4f}")

            # ------------------------------------------------------------
            # STEP 3: TASKGUARD (INITIAL)
            # ------------------------------------------------------------
            task_result = task_guard.verify(prompt=prompt, response=final_response)
            self.last_task_metrics = {
                "preserved": task_result.preserved,
                "score": task_result.score,
                "missing_terms": list(task_result.missing_terms),
                "missing_phrases": list(task_result.missing_phrases),
                "missing_json_keys": list(task_result.missing_json_keys),
                "issues": list(task_result.issues),
            }
            trace.append(f"Initial Task Verification: preserved={task_result.preserved}, score={task_result.score:.4f}")

            # ------------------------------------------------------------
            # STEP 4: COHERENCEENGINE (INITIAL)
            # ------------------------------------------------------------
            with self.context_lock:
                coherence_context = self.conversation_context[-6:].copy()
            coherence_result = coherence_engine.verify(prompt=prompt, response=final_response, context=coherence_context)
            self.last_coherence_metrics = {
                "coherent": coherence_result.coherent,
                "score": coherence_result.score,
                "confidence": coherence_result.confidence,
                "task_alignment": coherence_result.task_alignment,
                "context_continuity": coherence_result.context_continuity,
                "internal_consistency": coherence_result.internal_consistency,
                "topic_drift": coherence_result.topic_drift,
                "issues": list(coherence_result.issues),
                "warnings": list(coherence_result.warnings),
            }
            trace.append(f"Initial Coherence Verification: coherent={coherence_result.coherent}, score={coherence_result.score:.4f}")

            # ------------------------------------------------------------
            # STEP 5: MATHENGINE (INITIAL)
            # ------------------------------------------------------------
            math_result = math_engine.verify(problem=prompt, answer=final_response)
            self.last_math_metrics = {
                "verifiable": math_result.verifiable,
                "verified": math_result.verified,
                "confidence": math_result.confidence,
                "verifier": math_result.verifier,
                "issues": list(math_result.issues),
                "computed": dict(math_result.computed),
            }
            trace.append(f"Initial Math Verification: verifiable={math_result.verifiable}, verified={math_result.verified}")

            # ------------------------------------------------------------
            # STEP 6: DETERMINISTIC RENDERER (WHEN SUPPORTED MATH FAILS)
            # ------------------------------------------------------------
            authoritative_math_answer = False

            if math_result.verifiable and not math_result.verified:
                rendered_math_answer = math_engine.render_verified_answer(problem=prompt, result=math_result)
                if rendered_math_answer:
                    final_response = rendered_math_answer

                    trace.append("Deterministic math repair applied via renderer")

                    math_result = math_engine.verify(problem=prompt, answer=final_response)

                    task_result = task_guard.verify(
                        prompt=prompt,
                        response=final_response,
                    )

                    authoritative_math_answer = (
                        math_result.verifiable
                        and math_result.verified
                        and task_result.preserved
                    )

                    self.last_math_metrics = {
                        "verifiable": math_result.verifiable,
                        "verified": math_result.verified,
                        "confidence": math_result.confidence,
                        "verifier": math_result.verifier,
                        "issues": list(math_result.issues),
                        "computed": dict(math_result.computed),
                    }

                    trace.append(
                        "Post-Render Math Recheck: "
                        f"verified={math_result.verified}, "
                        f"confidence={math_result.confidence:.4f}"
                    )

                    # ------------------------------------------------------------
                    # STEP 7: TASKGUARD RECHECK
                    # ------------------------------------------------------------
                    task_result = task_guard.verify(prompt=prompt, response=final_response)
                    self.last_task_metrics = {
                        "preserved": task_result.preserved,
                        "score": task_result.score,
                        "missing_terms": list(task_result.missing_terms),
                        "missing_phrases": list(task_result.missing_phrases),
                        "missing_json_keys": list(task_result.missing_json_keys),
                        "issues": list(task_result.issues),
                    }
                    trace.append(f"Post-Render Task Recheck: preserved={task_result.preserved}")

                    # ------------------------------------------------------------
                    # STEP 8: COHERENCEENGINE RECHECK
                    # ------------------------------------------------------------
                    with self.context_lock:
                        coherence_context = self.conversation_context[-6:].copy()
                    coherence_result = coherence_engine.verify(prompt=prompt, response=final_response, context=coherence_context)
                    self.last_coherence_metrics = {
                        "coherent": coherence_result.coherent,
                        "score": coherence_result.score,
                        "confidence": coherence_result.confidence,
                        "task_alignment": coherence_result.task_alignment,
                        "context_continuity": coherence_result.context_continuity,
                        "internal_consistency": coherence_result.internal_consistency,
                        "topic_drift": coherence_result.topic_drift,
                        "issues": list(coherence_result.issues),
                        "warnings": list(coherence_result.warnings),
                    }
                    trace.append(f"Post-Render Coherence Recheck: coherent={coherence_result.coherent}")

                    authoritative_math_answer = (
                        math_result.verifiable
                        and math_result.verified
                        and task_result.preserved
                    )

            # ------------------------------------------------------------
            # STEP 9: REPAIRENGINE (ONLY IF ANYTHING STILL REMAINS FAILING)
            # ------------------------------------------------------------
            loop_detected = (final_response == "CRITICAL ERROR: LOOP DETECTED")
        
            math_failed = (
                self.last_math_metrics["verifiable"]
                and not self.last_math_metrics["verified"]
            )

            reasoning_failed = (
                self.last_reasoning_metrics.get(
                    "issues_detected",
                    0,
                ) > 0
                and not self.last_reasoning_metrics.get(
                    "converged",
                    False,
                )
            )

            coherence_failed = (
                not self.last_coherence_metrics["coherent"]
            )

            repair_needed = (
                not self.last_task_metrics["preserved"]
                or math_failed
                or loop_detected
                or (
                   coherence_failed
                   and not authoritative_math_answer
                )
                or (
                    reasoning_failed
                    and not authoritative_math_answer
                )
            )

            if repair_needed:
                trace.append(
                    "Discrepancies remain. "
                    "Generating dynamic Repair Plan..."
                )

                repair_plan = repair_engine.plan(
                    prompt=prompt,
                    answer=final_response,
                    reasoning=self.last_reasoning_metrics,
                    task=self.last_task_metrics,
                    coherence=self.last_coherence_metrics,
                    math=self.last_math_metrics,
                    cycle={
                        "detected": loop_detected,
                        "cycle_type": (
                            "deterministic"
                            if loop_detected
                            else None
                        ),
                        "cycle_length": None,
                    },
                )
                repair_execution = repair_engine.execute(
                    plan=repair_plan,
                    answer=final_response,
                    model_query=self.model_query,
                )
                self.last_repair_metrics = {
                    "required": repair_plan.repair_required,
                    "attempted": repair_execution.attempted,
                    "successful": repair_execution.successful,
                    "terminal": repair_plan.terminal,
                    "actions": [action.category for action in repair_plan.actions],
                    "reasons": list(repair_plan.reasons),
                    "error": repair_execution.error,
                }
                final_response = repair_execution.final_answer
                trace.append(f"Repair Stage Complete: successful={repair_execution.successful}, terminal={repair_plan.terminal}")

                if repair_plan.terminal:
                    trace.append("Repair stage structural terminal response selected.")
                    self.last_final_verification = {"passed": True, "terminal": True, "task": {}, "coherence": {}, "math": {}}
                    self.log_state(payload, "TERMINATED_CYCLE", trace)
                    return True, final_response, trace
            else:
                trace.append("No active engine discrepancies. Skipping RepairEngine step.")
                self.last_repair_metrics = {"required": False, "attempted": False, "successful": True, "terminal": False, "actions": [], "reasons": [], "error": None}

            # ------------------------------------------------------------
            # STEP 10: FINAL VERIFICATION
            # ------------------------------------------------------------
            final_task_result = task_guard.verify(prompt=prompt, response=final_response)
            with self.context_lock:
                final_coherence_context = self.conversation_context[-6:].copy()
            final_coherence_result = coherence_engine.verify(prompt=prompt, response=final_response, context=final_coherence_context)

            final_math_result = math_engine.verify(problem=prompt, answer=final_response)
            final_math_passed = (not final_math_result.verifiable or final_math_result.verified)
            
            final_coherence_passed = (
                final_coherence_result.coherent
                or authoritative_math_answer
                or final_coherence_result.score >= 0.25
            )

            final_verification_passed = (
                final_task_result.preserved
                and final_coherence_passed
                and final_math_passed
            )

            self.last_final_verification = {
                "passed": final_verification_passed,
                "task": {
                    "preserved": final_task_result.preserved,
                    "score": final_task_result.score,
                    "missing_terms": list(final_task_result.missing_terms),
                    "missing_phrases": list(final_task_result.missing_phrases),
                    "missing_json_keys": list(final_task_result.missing_json_keys),
                    "issues": list(final_task_result.issues),
                },
                "coherence": {
                    "coherent": final_coherence_result.coherent,
                    "score": final_coherence_result.score,
                    "confidence": final_coherence_result.confidence,
                    "task_alignment": final_coherence_result.task_alignment,
                    "context_continuity": final_coherence_result.context_continuity,
                    "internal_consistency": final_coherence_result.internal_consistency,
                    "topic_drift": final_coherence_result.topic_drift,
                    "issues": list(final_coherence_result.issues),
                    "warnings": list(final_coherence_result.warnings),
                },
                "math": {
                    "verifiable": final_math_result.verifiable,
                    "verified": final_math_result.verified,
                    "confidence": final_math_result.confidence,
                    "verifier": final_math_result.verifier,
                    "issues": list(final_math_result.issues),
                    "computed": dict(final_math_result.computed),
                },
            }

            # Override history metrics with the true final evaluated states
            self.last_task_metrics = self.last_final_verification["task"].copy()
            self.last_coherence_metrics = self.last_final_verification["coherence"].copy()
            self.last_math_metrics = self.last_final_verification["math"].copy()

            trace.append(
                "Final Gate Assessment: "
                f"passed={final_verification_passed}, "
                f"task={final_task_result.preserved}, "
                f"coherence={final_coherence_passed}, "
                f"math={final_math_passed}, "
                f"authoritative_math={authoritative_math_answer}"
            )

            # ------------------------------------------------------------
            # STEP 11: RELEASE GATE
            # ------------------------------------------------------------
            if not final_verification_passed:
                trace.append("Release blocked: final verification check failure.")
                self.log_state(payload, "FAILED_FINAL_VERIFICATION", trace)
                return False, final_response, trace

            synthesized_response = self.build_vre_audit(final_response, reasoning_steps)
            vre_ok, vre_msg = self.check_vre(prompt, synthesized_response)
            trace.append(vre_msg)
            if not vre_ok:
                self.log_state(payload, "BLOCKED_VRE", trace)
                return False, response, trace

            self.log_state(payload, "PASSED", trace)
            return True, final_response, trace
```