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

zpp_id: math_engine_py
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
from typing import Any, Dict, List, Optional, Tuple
from typing import Any, Dict, List, Literal, Optional, Tuple

import math
import re

# ============================================================
# VERSION
# ============================================================

MATH_ENGINE_VERSION = "1.0.0"


MathVerdict = Literal[
    "verified",
    "contradicted",
    "insufficient_claims",
    "unsupported",
    "parse_failure",
]


@dataclass
class MathVerificationResult:
    verified: bool
    verifiable: bool
    confidence: float
    verdict: MathVerdict
    issues: List[str] = field(default_factory=list)
    computed: Dict[str, Any] = field(default_factory=dict)
    extracted: Dict[str, Any] = field(default_factory=dict)
    verifier: Optional[str] = None
    message: Optional[str] = None


class MathEngine:
    """
    Deterministic mathematical verification engine.

    Version 1.1 refines:
    - verification verdict precision
    - claim extraction semantics
    - contradictory-claim detection
    - endpoint handling in motion intervals
    - analytical explanation of sequence divergence

    Supported verifier families remain unchanged:
    1. One-dimensional cubic polynomial motion problems.
    2. The reference heartbeat sequence:
       a_n = sin(n) * (1 + 0.1 * sin(n / 10))
    """

    NUMBER_PATTERN = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"

    def verify(
        self,
        problem: str,
        answer: str,
    ) -> MathVerificationResult:
        problem_text = problem or ""
        answer_text = answer or ""

        if self._looks_like_polynomial_motion(problem_text):
            return self._verify_polynomial_motion(
                problem_text,
                answer_text,
            )

        if self._looks_like_reference_sequence(problem_text):
            return self._verify_reference_sequence(
                problem_text,
                answer_text,
            )

        return MathVerificationResult(
            verified=False,
            verifiable=False,
            verdict="UNVERIFIABLE",
            confidence=0.0,
            issues=[
                "No supported deterministic verifier matched this problem."
            ],
            verifier=None,
            message="The problem was not recognized by MathEngine v1.",
        )

    # ============================================================
    # DETERMINISTIC RENDERERS
    # ============================================================
    def render_verified_answer(
        self,
        *,
        problem: str,
        result: MathVerificationResult,
    ) -> Optional[str]:
        """
        Render an authoritative answer from deterministic computed values.
        Returns None when no deterministic renderer supports the verifier.
        """
        if not result.verifiable:
            return None

        if result.verifier == "polynomial_motion":
            return self._render_polynomial_motion_answer(result)

        if result.verifier == "reference_sequence":
            return self._render_reference_sequence_answer(result)

        return None

    def _render_polynomial_motion_answer(
        self,
        result: MathVerificationResult,
    ) -> Optional[str]:
        computed = result.computed or {}
        velocity = computed.get("velocity_coefficients", {})
        acceleration = computed.get("acceleration_coefficients", {})
        roots = computed.get("velocity_roots", [])
        right_intervals = computed.get("right_intervals", [])
        left_intervals = computed.get("left_intervals", [])
        total_distance = computed.get("total_distance")
        interval = computed.get("interval", {})

        if not velocity or not acceleration or total_distance is None:
            return None

        velocity_text = self._format_quadratic_expression(
            velocity.get("quadratic", 0.0),
            velocity.get("linear", 0.0),
            velocity.get("constant", 0.0),
        )
        acceleration_text = self._format_linear_expression(
            acceleration.get("linear", 0.0),
            acceleration.get("constant", 0.0),
        )
        roots_text = " and ".join(
            f"t = {self._format_number(root)}"
            for root in roots
        ) or "no direction changes in the requested interval"
        right_text = self._format_intervals(right_intervals)
        left_text = self._format_intervals(left_intervals)
        start_time = self._format_number(interval.get("start", 0.0))
        end_time = self._format_number(interval.get("end", 0.0))
        distance_text = self._format_number(total_distance)

        return (
            "**Velocity**\n\n"
            f"v(t) = {velocity_text}\n\n"
            "**Acceleration**\n\n"
            f"a(t) = {acceleration_text}\n\n"
            "**Direction changes**\n\n"
            f"The velocity is zero at {roots_text}.\n\n"
            "**Motion intervals**\n\n"
            f"The particle moves right on {right_text}.\n\n"
            f"The particle moves left on {left_text}.\n\n"
            "**Total distance traveled**\n\n"
            f"From t = {start_time} to t = {end_time}, "
            f"the total distance traveled is "
            f"{distance_text} units."
        )

    def _render_reference_sequence_answer(
        self,
        result: MathVerificationResult,
    ) -> Optional[str]:
        computed = result.computed or {}
        if "converges" not in computed:
            return None

        sample_count = computed.get("sample_count", 0)
        sample_min = computed.get("sample_min", 0.0)
        sample_max = computed.get("sample_max", 0.0)
        sample_mean = computed.get("sample_mean", 0.0)

        return (
            "The sequence does not converge. Integer values of n modulo 2π "
            "come arbitrarily close to angles where sin(n) is 1 and -1, so "
            "sin(n) has subsequences approaching both positive and negative "
            "extremes. The multiplier 1 + 0.1 sin(n/10) remains positive and "
            "bounded away from zero, between 0.9 and 1.1. It therefore cannot "
            "collapse that oscillation into a single limit.\n\n"
            "Numerical diagnostics over "
            f"{sample_count} sampled terms:\n"
            f"- minimum ≈ {sample_min:.6f}\n"
            f"- maximum ≈ {sample_max:.6f}\n"
            f"- mean ≈ {sample_mean:.6f}"
        )

    # ============================================================
    # FORMATTING HELPERS
    # ============================================================
    @staticmethod
    def _format_number(value: float) -> str:
        numeric = float(value)
        if abs(numeric - round(numeric)) <= 1e-10:
            return str(int(round(numeric)))
        return f"{numeric:.10g}"

    def _format_quadratic_expression(
        self,
        quadratic: float,
        linear: float,
        constant: float,
    ) -> str:
        parts: List[str] = []
        self._append_polynomial_term(parts, quadratic, "t²")
        self._append_polynomial_term(parts, linear, "t")
        self._append_polynomial_term(parts, constant, "")
        return " ".join(parts) if parts else "0"

    def _format_linear_expression(
        self,
        linear: float,
        constant: float,
    ) -> str:
        parts: List[str] = []
        self._append_polynomial_term(parts, linear, "t")
        self._append_polynomial_term(parts, constant, "")
        return " ".join(parts) if parts else "0"

    def _append_polynomial_term(
        self,
        parts: List[str],
        coefficient: float,
        variable: str,
    ) -> None:
        if abs(coefficient) <= 1e-12:
            return
        absolute = abs(coefficient)
        if variable and abs(absolute - 1.0) <= 1e-12:
            magnitude = variable
        else:
            magnitude = f"{self._format_number(absolute)}{variable}"
        if not parts:
            parts.append(
                magnitude if coefficient > 0 else f"-{magnitude}"
            )
        else:
            operator = "+" if coefficient > 0 else "-"
            parts.append(f"{operator} {magnitude}")

    def _format_intervals(
        self,
        intervals: List[Tuple[float, float]],
    ) -> str:
        if not intervals:
            return "none"
        return " and ".join(
            f"({self._format_number(start)}, {self._format_number(end)})"
            for start, end in intervals
        )

    # ============================================================
    # POLYNOMIAL MOTION
    # ============================================================
    def _looks_like_polynomial_motion(self, problem: str) -> bool:
        lowered = problem.lower()
        has_position = "s(t)" in lowered or "position" in lowered
        has_motion_language = any(
            term in lowered
            for term in (
                "velocity",
                "acceleration",
                "distance traveled",
                "moving to the right",
                "moving to the left",
            )
        )
        return has_position and has_motion_language

    def _verify_polynomial_motion(
        self,
        problem: str,
        answer: str,
    ) -> MathVerificationResult:
        coefficients = self._extract_cubic_position_coefficients(problem)
        interval = self._extract_time_interval(problem)

        if coefficients is None:
            return MathVerificationResult(
                verified=False,
                verifiable=False,
                verdict="UNVERIFIABLE",
                confidence=0.0,
                issues=["Could not parse the cubic position function s(t)."],
                verifier="polynomial_motion",
            )

        if interval is None:
            return MathVerificationResult(
                verified=False,
                verifiable=False,
                verdict="UNVERIFIABLE",
                confidence=0.0,
                issues=["Could not determine the requested time interval."],
                verifier="polynomial_motion",
            )

        a, b, c, d = coefficients
        start_time, end_time = interval

        velocity_coefficients = (3.0 * a, 2.0 * b, c)
        acceleration_coefficients = (6.0 * a, 2.0 * b)

        velocity_roots = self._quadratic_roots(*velocity_coefficients)
        roots_in_interval = sorted(
            root for root in velocity_roots if start_time <= root <= end_time
        )

        breakpoints: List[float] = []

        for point in sorted([start_time, *roots_in_interval, end_time]):
            if not breakpoints or not self._close(
                point,
                breakpoints[-1],
                tolerance=1e-10,
            ):
                breakpoints.append(point)

        positions = {
            point: self._evaluate_cubic(coefficients, point)
            for point in breakpoints
        }

        total_distance = sum(
            abs(positions[breakpoints[index + 1]] - positions[breakpoints[index]])
            for index in range(len(breakpoints) - 1)
        )

        net_displacement = positions[end_time] - positions[start_time]

        right_intervals: List[Tuple[float, float]] = []
        left_intervals: List[Tuple[float, float]] = []

        for left, right in zip(breakpoints, breakpoints[1:]):
            midpoint = (left + right) / 2.0
            velocity_value = self._evaluate_quadratic(velocity_coefficients, midpoint)
            if velocity_value > 0:
                right_intervals.append((left, right))
            elif velocity_value < 0:
                left_intervals.append((left, right))

        computed = {
            "position_coefficients": {
                "cubic": a,
                "quadratic": b,
                "linear": c,
                "constant": d,
            },
            "velocity_coefficients": {
                "quadratic": velocity_coefficients[0],
                "linear": velocity_coefficients[1],
                "constant": velocity_coefficients[2],
            },
            "acceleration_coefficients": {
                "linear": acceleration_coefficients[0],
                "constant": acceleration_coefficients[1],
            },
            "velocity_roots": roots_in_interval,
            "right_intervals": right_intervals,
            "left_intervals": left_intervals,
            "positions": positions,
            "net_displacement": net_displacement,
            "total_distance": total_distance,
            "interval": {"start": start_time, "end": end_time},
        }

        extracted = {
            "claimed_total_distance": self._extract_total_distance_claim(answer),
            "claimed_velocity_roots": self._extract_direction_change_claims(answer),
        }

        issues: List[str] = []
        checks = 0
        passed_checks = 0

        claimed_distance = extracted["claimed_total_distance"]
        if claimed_distance is not None:
            checks += 1
            if self._close(claimed_distance, total_distance, tolerance=1e-3):
                passed_checks += 1
            else:
                issues.append(
                    f"Claimed total distance {claimed_distance:g} does not match "
                    f"the computed total distance {total_distance:g}."
                )
                if self._close(claimed_distance, net_displacement, tolerance=1e-3):
                    issues.append(
                        "The answer appears to use net displacement instead of total distance."
                    )

        claimed_roots = extracted["claimed_velocity_roots"]

        if claimed_roots is not None:
            checks += 1

            if self._same_numeric_set(
                claimed_roots,
                roots_in_interval,
                tolerance=1e-3,
            ):
                passed_checks += 1
            else:
                issues.append(
                    f"Claimed direction-change times {claimed_roots} "
                    f"do not match the velocity roots {roots_in_interval}."
                )

        if self._answer_uses_acceleration_for_direction(answer):
            issues.append(
                "Direction must be determined from the sign of velocity, not the sign of acceleration."
            )

        if checks == 0:
            confidence = 0.0
            verified = False
            issues.append(
                "The engine computed the correct motion quantities, "
                "but could not confidently extract enough claims from the answer to compare them."
            )
        else:
            confidence = passed_checks / checks
            verified = len(issues) == 0

        return MathVerificationResult(
            verified=verified,
            verifiable=True,
            verdict="PASS" if verified else "FAIL",
            confidence=round(confidence, 4),
            issues=issues,
            computed=computed,
            extracted=extracted,
            verifier="polynomial_motion",
            message=(
                "Polynomial motion claims verified."
                if verified
                else f"Polynomial motion verification found {len(issues)} issue(s)."
            ),
        )

    def _extract_cubic_position_coefficients(
        self,
        problem: str,
    ) -> Optional[Tuple[float, float, float, float]]:
        normalized = (
            problem.replace("−", "-")
            .replace("–", "-")
            .replace("^", "")
            .replace("³", "3")
            .replace("²", "2")
        )
        match = re.search(
            r"s\s*\(\s*t\s*\)\s*=\s*"
            rf"({self.NUMBER_PATTERN})\s*\*?\s*t3\s*"
            rf"([+-]\s*{self.NUMBER_PATTERN})\s*\*?\s*t2\s*"
            rf"([+-]\s*{self.NUMBER_PATTERN})\s*\*?\s*t\s*"
            rf"([+-]\s*{self.NUMBER_PATTERN})",
            normalized,
            re.IGNORECASE,
        )
        if not match:
            match = re.search(
                r"s\s*\(\s*t\s*\)\s*=\s*"
                rf"({self.NUMBER_PATTERN})\s*t3\s*"
                rf"([+-]\s*{self.NUMBER_PATTERN})\s*t2\s*"
                rf"([+-]\s*{self.NUMBER_PATTERN})\s*t\s*"
                rf"([+-]\s*{self.NUMBER_PATTERN})",
                normalized,
                re.IGNORECASE,
            )
        if not match:
            return None
        return tuple(float(group.replace(" ", "")) for group in match.groups())

    def _extract_time_interval(
        self,
        problem: str,
    ) -> Optional[Tuple[float, float]]:
        match = re.search(
            rf"from\s+t\s*=\s*({self.NUMBER_PATTERN})"
            rf".*?to\s+t\s*=\s*({self.NUMBER_PATTERN})",
            problem,
            re.IGNORECASE | re.DOTALL,
        )
        if not match:
            return None
        start = float(match.group(1))
        end = float(match.group(2))
        if end < start:
            start, end = end, start
        return start, end

    def _extract_total_distance_claim(
        self,
        answer: str,
    ) -> Optional[float]:
        """
        Extract the final claimed total-distance value.

        Prefer a number immediately following a complete phrase such as
        'the total distance traveled is', avoiding interval endpoints.
        """

        normalized = (
            answer.replace("−", "-")
            .replace("–", "-")
        )

        patterns = [
            (
                r"(?:the\s+)?total\s+distance"
                r"(?:\s+traveled)?\s+"
                r"(?:is|equals)\s+"
                rf"({self.NUMBER_PATTERN})"
                r"(?![\d.])"
            ),
            (
                r"(?:the\s+)?total\s+distance"
                r"(?:\s+traveled)?\s*=\s*"
                rf"({self.NUMBER_PATTERN})"
                r"(?![\d.])"
            ),
            (
                r"\\boxed\s*\{\s*"
                rf"({self.NUMBER_PATTERN})"
                r"\s*\}"
            ),
        ]

        candidates: List[float] = []

        for pattern in patterns:
            for match in re.finditer(
                pattern,
                normalized,
                re.IGNORECASE | re.DOTALL,
            ):
                try:
                    candidates.append(
                        float(match.group(1))
                    )
                except (TypeError, ValueError):
                    continue

        return candidates[-1] if candidates else None

    def _extract_direction_change_claims(
        self,
        answer: str,
    ) -> Optional[List[float]]:
        """
        Extract claimed velocity roots only from sentences that explicitly
        describe zero velocity or direction changes.

        Returns:
            None if no direction-change claim could be extracted.
            [] if the answer explicitly claims there are no direction changes.
            [values...] if specific direction-change times are claimed.
        """

        normalized = (
            answer.replace("−", "-")
            .replace("–", "-")
        )

        if re.search(
            r"(?:no\s+direction\s+changes?"
            r"|never\s+changes?\s+direction"
            r"|no\s+velocity\s+roots?"
            r"|velocity\s+never\s+(?:becomes?|is)\s+zero)",
            normalized,
            re.IGNORECASE,
        ):
            return []

        values: List[float] = []

        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            normalized,
        )

        relevant_sentences = [
            sentence
            for sentence in sentences
            if re.search(
                (
                    r"velocity\s+(?:is\s+)?zero"
                    r"|v\s*\(\s*t\s*\)\s*=\s*0"
                    r"|direction\s+changes?"
                    r"|critical\s+times?"
                ),
                sentence,
                re.IGNORECASE,
            )
        ]

        for sentence in relevant_sentences:
            for match in re.finditer(
                rf"\bt\s*=\s*"
                rf"({self.NUMBER_PATTERN})"
                r"(?![\d.])",
                sentence,
                re.IGNORECASE,
            ):
                try:
                    values.append(
                        float(match.group(1))
                    )
                except ValueError:
                    continue

        unique_values: List[float] = []

        for value in values:
            if not any(
                self._close(
                    value,
                    existing,
                    1e-6,
                )
                for existing in unique_values
            ):
                unique_values.append(value)

        return sorted(unique_values)

    @staticmethod
    def _answer_uses_acceleration_for_direction(answer: str) -> bool:
        lowered = answer.lower()
        indicators = (
            "since the acceleration is negative",
            "since the acceleration is positive",
            "acceleration is negative, which indicates",
            "acceleration is positive, indicating",
        )
        return any(indicator in lowered for indicator in indicators)

    # ============================================================
    # REFERENCE SEQUENCE
    # ============================================================
    def _looks_like_reference_sequence(self, problem: str) -> bool:
        normalized = problem.lower().replace(" ", "")
        return (
            "sin(n)" in normalized
            and "sin(n/10)" in normalized
            and "0.1" in normalized
        )

    def _verify_reference_sequence(
        self,
        problem: str,
        answer: str,
    ) -> MathVerificationResult:
        sample_count = 10_000
        sequence = [
            math.sin(n) * (1.0 + 0.1 * math.sin(n / 10.0))
            for n in range(1, sample_count + 1)
        ]

        sample_min = min(sequence)
        sample_max = max(sequence)
        sample_mean = sum(sequence) / sample_count

        convergence_claim, contradictory_claims = (
            self._extract_convergence_claim(answer)
        )

        issues: List[str] = []

        if contradictory_claims:
            issues.append(
                "The answer contains contradictory convergence and "
                "divergence claims."
            )
        elif convergence_claim is True:
            issues.append(
                "The answer claims the sequence converges, but the sequence "
                "has persistent positive and negative oscillation."
            )
        elif convergence_claim is None:
            issues.append(
                "No clear convergence or divergence conclusion could be "
                "extracted from the answer."
            )

        verified = (
            convergence_claim is False
            and not contradictory_claims
        )

        confidence = 1.0 if convergence_claim is not None else 0.0

        return MathVerificationResult(
            verified=verified,
            verifiable=True,
            verdict="PASS" if verified else "FAIL",
            confidence=confidence,
            issues=issues,
            computed={
                "sample_count": sample_count,
                "sample_min": sample_min,
                "sample_max": sample_max,
                "sample_mean": sample_mean,
                "multiplier_lower_bound": 0.9,
                "multiplier_upper_bound": 1.1,
                "converges": False,
            },

            extracted={"claimed_convergence": convergence_claim},
            verifier="reference_sequence",
            message=(
                "Reference sequence conclusion verified."
                if verified
                else "Reference sequence verification failed."
            ),
        )

    @staticmethod
    def _extract_convergence_claim(answer: str) -> (Optional[bool], bool):
        lowered = answer.lower()

        divergence_patterns = (
            "does not converge",
            "doesn't converge",
            "is divergent",
            "diverges",
            "nonconvergent",
            "non-convergent",
        )
        convergence_patterns = (
            "sequence converges",
            "indeed converges",
            "is convergent",
            "converges to",
        )

        claims_divergence = any(
            pattern in lowered
            for pattern in divergence_patterns
        )
        claims_convergence = any(
            pattern in lowered
            for pattern in convergence_patterns
        )

        contradictory = claims_divergence and claims_convergence

        if contradictory:
            return None, True

        if claims_divergence:
            return False, False

        if claims_convergence:
            return True, False

        return None, False

    # ============================================================
    # NUMERIC HELPERS
    # ============================================================
    @staticmethod
    def _evaluate_cubic(
        coefficients: Tuple[float, float, float, float],
        value: float,
    ) -> float:
        a, b, c, d = coefficients
        return a * value**3 + b * value**2 + c * value + d

    @staticmethod
    def _evaluate_quadratic(
        coefficients: Tuple[float, float, float],
        value: float,
    ) -> float:
        a, b, c = coefficients
        return a * value**2 + b * value + c

    @staticmethod
    def _quadratic_roots(a: float, b: float, c: float) -> List[float]:
        if abs(a) < 1e-12:
            if abs(b) < 1e-12:
                return []
            return [-c / b]

        discriminant = b**2 - 4.0 * a * c
        if discriminant < -1e-12:
            return []
        discriminant = max(discriminant, 0.0)
        square_root = math.sqrt(discriminant)
        roots = [(-b - square_root) / (2.0 * a), (-b + square_root) / (2.0 * a)]

        unique_roots: List[float] = []
        for root in sorted(roots):
            if not any(abs(root - existing) <= 1e-10 for existing in unique_roots):
                unique_roots.append(root)
        return unique_roots

    @staticmethod
    def _close(first: float, second: float, tolerance: float) -> bool:
        return abs(first - second) <= tolerance

    def _same_numeric_set(
        self,
        first: List[float],
        second: List[float],
        tolerance: float,
    ) -> bool:
        if len(first) != len(second):
            return False
        first_sorted = sorted(first)
        second_sorted = sorted(second)
        return all(
            self._close(a, b, tolerance) for a, b in zip(first_sorted, second_sorted)
        )


math_engine = MathEngine()
```