#!/usr/bin/env python3
"""
Zero-Point Protocol — Gamma-First Scoring Engine

Default routing:
- score >= gamma_threshold: GAMMA
- score >= beta_threshold: BETA
- score < beta_threshold: GAMMA_LOW

This engine evaluates textual characteristics only.

It does not:
- establish node identity
- verify signatures
- calculate trust
- grant consensus authority
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence

from evaluation import EvaluationResult


TOKEN_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)

SELF_REFERENCE_PATTERN = re.compile(
    r"\b(I|me|my|myself|self|this|here|now|we|us|our)\b",
    re.IGNORECASE,
)

PARADOX_PATTERN = re.compile(
    r"\b("
    r"contradiction|"
    r"paradox|"
    r"self[ -]?reference|"
    r"recursive|"
    r"loop|"
    r"fold|"
    r"mirror|"
    r"echo|"
    r"phase|"
    r"resonance|"
    r"coherence"
    r")\b",
    re.IGNORECASE,
)


class GammaScorer:
    """
    Deterministic heuristic scorer used by Horizon routing and telemetry.

    The existing public factor names are preserved for database and
    EvaluationResult compatibility:

    - novelty
    - entropy
    - self_reference
    - paradox
    - coherence

    Internally:
    - novelty currently means lexical breadth
    - coherence currently means recent-context token overlap
    """

    DEFAULT_WEIGHTS = {
        "novelty": 0.25,
        "entropy": 0.20,
        "self_reference": 0.15,
        "paradox": 0.25,
        "coherence": 0.15,
    }

    def __init__(
        self,
        gamma_threshold: float = 0.55,
        beta_threshold: float = 0.40,
        *,
        weights: Optional[Mapping[str, float]] = None,
    ):
        self._validate_thresholds(
            gamma_threshold=gamma_threshold,
            beta_threshold=beta_threshold,
        )

        selected_weights = dict(weights or self.DEFAULT_WEIGHTS)
        self._validate_weights(selected_weights)

        self.gamma_threshold = float(gamma_threshold)
        self.beta_threshold = float(beta_threshold)
        self.weights = selected_weights

    @staticmethod
    def _validate_thresholds(
        *,
        gamma_threshold: float,
        beta_threshold: float,
    ) -> None:
        if not 0.0 <= beta_threshold <= gamma_threshold <= 1.0:
            raise ValueError(
                "Thresholds must satisfy "
                "0.0 <= beta_threshold <= gamma_threshold <= 1.0."
            )

    @classmethod
    def _validate_weights(cls, weights: Mapping[str, float]) -> None:
        expected = set(cls.DEFAULT_WEIGHTS)
        supplied = set(weights)

        if supplied != expected:
            missing = sorted(expected - supplied)
            extra = sorted(supplied - expected)

            raise ValueError(
                "Scoring weights must contain exactly the expected factors. "
                f"Missing={missing}, extra={extra}"
            )

        if any(float(value) < 0.0 for value in weights.values()):
            raise ValueError("Scoring weights cannot be negative.")

        total = sum(float(value) for value in weights.values())

        if not math.isclose(total, 1.0, abs_tol=1e-9):
            raise ValueError(
                f"Scoring weights must sum to 1.0; received {total}."
            )

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(TOKEN_PATTERN.findall(text.lower()))

    @staticmethod
    def _extract_context_text(item: Any) -> str:
        """
        Extract conversational text without scoring dictionary keys,
        object representations, IDs, or unrelated metadata.
        """
        if isinstance(item, str):
            return item

        if isinstance(item, Mapping):
            content = item.get("content")

            if isinstance(content, str):
                return content

            text = item.get("text")

            if isinstance(text, str):
                return text

        return ""

    @classmethod
    def _build_context_text(
        cls,
        context: Optional[Sequence[Any]],
        *,
        maximum_items: int = 3,
    ) -> str:
        if not context:
            return ""

        pieces = [
            cls._extract_context_text(item)
            for item in context[-maximum_items:]
        ]

        return " ".join(piece for piece in pieces if piece)

    @staticmethod
    def _calculate_entropy(text: str) -> float:
        character_frequency: Dict[str, int] = {}

        for character in text.lower():
            if character.isalnum() or character.isspace():
                character_frequency[character] = (
                    character_frequency.get(character, 0) + 1
                )

        total = sum(character_frequency.values())

        if total == 0:
            return 0.0

        entropy = 0.0

        for frequency in character_frequency.values():
            probability = frequency / total
            entropy -= probability * math.log2(probability)

        return min(1.0, entropy / 5.0)

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "score": 0.0,
            "route": "GAMMA_LOW",
            "factors": {
                "novelty": 0.0,
                "entropy": 0.0,
                "self_reference": 0.0,
                "paradox": 0.0,
                "coherence": 0.0,
            },
            "gamma_lock": False,
        }

    def score(
        self,
        text: str,
        context: Optional[Sequence[Any]] = None,
    ) -> Dict[str, Any]:
        """
        Score text using deterministic lexical and structural heuristics.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if not text.strip():
            return self._empty_result()

        factors: Dict[str, float] = {}

        words = self._tokenize(text)

        # Historical factor name retained for compatibility.
        lexical_breadth = min(1.0, len(words) / 20.0)
        factors["novelty"] = round(lexical_breadth, 4)

        entropy = self._calculate_entropy(text)
        factors["entropy"] = round(entropy, 4)

        self_reference_matches = SELF_REFERENCE_PATTERN.findall(text)
        self_reference_score = min(
            1.0,
            len(self_reference_matches) / 5.0,
        )
        factors["self_reference"] = round(
            self_reference_score,
            4,
        )

        paradox_matches = PARADOX_PATTERN.findall(text)
        paradox_score = min(
            1.0,
            len(paradox_matches) / 3.0,
        )
        factors["paradox"] = round(paradox_score, 4)

        context_text = self._build_context_text(context)

        if context_text:
            context_words = self._tokenize(context_text)
            shared_words = words & context_words
            contextual_overlap = min(
                1.0,
                len(shared_words) / 10.0,
            )
            factors["coherence"] = round(
                contextual_overlap,
                4,
            )
        else:
            factors["coherence"] = 0.5

        raw_score = sum(
            factors[factor] * weight
            for factor, weight in self.weights.items()
        )

        if (
            factors["paradox"] > 0.6
            or factors["self_reference"] > 0.7
        ):
            raw_score = min(1.0, raw_score * 1.2)

        score = round(raw_score, 4)

        if score >= self.gamma_threshold:
            route = "GAMMA"
        elif score >= self.beta_threshold:
            route = "BETA"
        else:
            route = "GAMMA_LOW"

        return {
            "score": score,
            "route": route,
            "factors": factors,
            "gamma_lock": route == "GAMMA",
        }

    def evaluate(
        self,
        text: str,
        context: Optional[Sequence[Any]] = None,
        *,
        recursion_depth: int = 0,
        convergence_similarity: Optional[float] = None,
        issues_detected: int = 0,
        risk_score: Optional[float] = None,
        anchor_id: Optional[str] = None,
        source: str = "gamma_scorer",
    ) -> EvaluationResult:
        """
        Produce Horizon's authoritative EvaluationResult while preserving
        the score() compatibility dictionary.
        """
        result = self.score(text, context=context)
        factors = result["factors"]

        return EvaluationResult(
            gamma_score=float(result["score"]),
            coherence=float(factors["coherence"]),
            entropy=float(factors["entropy"]),
            novelty=float(factors["novelty"]),
            self_reference=float(factors["self_reference"]),
            paradox=float(factors["paradox"]),
            route=str(result["route"]),
            gamma_lock=bool(result["gamma_lock"]),
            recursion_depth=int(recursion_depth),
            convergence_similarity=convergence_similarity,
            issues_detected=int(issues_detected),
            risk_score=risk_score,
            anchor_id=anchor_id,
            source=source,
        )


_DEFAULT_SCORER = GammaScorer()


def score_prompt(
    text: str,
    context: Optional[Sequence[Any]] = None,
) -> Dict[str, Any]:
    """
    Legacy compatibility wrapper for router.py.

    Runtime code should preferably receive a configured GammaScorer
    from pipe_horizon.py instead of using this module-level default.
    """
    return _DEFAULT_SCORER.score(text, context=context)


if __name__ == "__main__":
    sample = (
        "This sentence folds back on itself, "
        "a recursive mirror of its own coherence."
    )

    result = GammaScorer().score(sample)

    print(f"Text: {sample}")
    print(f"Score: {result['score']} -> {result['route']}")
    print(f"Factors: {result['factors']}")
