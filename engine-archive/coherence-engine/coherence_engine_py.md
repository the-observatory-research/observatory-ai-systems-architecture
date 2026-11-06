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

zpp_id: coherence_engine_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
#!/usr/bin/env python3

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import math
import re


@dataclass
class CoherenceResult:
    coherent: bool
    score: float
    confidence: float

    task_alignment: float
    context_continuity: float
    internal_consistency: float
    topic_drift: float

    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    computed: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    engine: str = "coherence_v1"


class CoherenceEngine:
    """
    Deterministic coherence baseline.

    Version 1 measures:
    1. Task alignment:
       Does the response preserve important concepts from the prompt?

    2. Context continuity:
       Does the response remain connected to recent conversation context?

    3. Internal consistency:
       Does the response contain obvious direct contradictions?

    4. Topic drift:
       Does the response introduce a largely unrelated topic?

    This is a lexical-semantic baseline, not a full embedding model.
    The public API is designed so embeddings can replace the similarity
    implementation later without changing callers.
    """

    STOPWORDS: Set[str] = {
        "a",
        "about",
        "after",
        "again",
        "all",
        "also",
        "am",
        "an",
        "and",
        "answer",
        "any",
        "are",
        "as",
        "at",
        "be",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "but",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "doing",
        "each",
        "for",
        "from",
        "further",
        "had",
        "has",
        "have",
        "having",
        "he",
        "her",
        "here",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "how",
        "i",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "just",
        "me",
        "more",
        "most",
        "my",
        "myself",
        "no",
        "nor",
        "not",
        "now",
        "of",
        "off",
        "on",
        "once",
        "only",
        "or",
        "other",
        "our",
        "ours",
        "ourselves",
        "out",
        "over",
        "own",
        "please",
        "problem",
        "same",
        "she",
        "should",
        "so",
        "some",
        "such",
        "than",
        "that",
        "the",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "to",
        "too",
        "under",
        "until",
        "up",
        "very",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "who",
        "whom",
        "why",
        "will",
        "with",
        "would",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves",
    }

    NEGATION_WORDS: Set[str] = {
        "not",
        "never",
        "no",
        "cannot",
        "can't",
        "doesn't",
        "doesnt",
        "isn't",
        "isnt",
        "won't",
        "wont",
        "false",
        "incorrect",
        "impossible",
    }

    STRUCTURED_OUTPUT_TERMS: Set[str] = {
        "json",
        "true",
        "false",
        "null",
        "yes",
        "no",
    }

    def __init__(
        self,
        *,
        coherence_threshold: float = 0.55,
        task_weight: float = 0.50,
        context_weight: float = 0.20,
        consistency_weight: float = 0.30,
    ):
        total_weight = (
            task_weight
            + context_weight
            + consistency_weight
        )

        if total_weight <= 0:
            raise ValueError(
                "Coherence weights must sum to a positive value."
            )

        self.coherence_threshold = coherence_threshold

        self.task_weight = task_weight / total_weight
        self.context_weight = context_weight / total_weight
        self.consistency_weight = (
            consistency_weight / total_weight
        )

    def verify(
        self,
        prompt: str,
        response: str,
        context: Optional[Sequence[Any]] = None,
    ) -> CoherenceResult:
        """
        Measure whether a response remains aligned with the current task
        and recent context.

        `context` may contain strings or chat-style dictionaries:
        {"role": "user", "content": "..."}
        """
        prompt_text = self._normalize_input(prompt)
        response_text = self._normalize_input(response)
        context_text = self._flatten_context(context or [])

        if not response_text.strip():
            return CoherenceResult(
                coherent=False,
                score=0.0,
                confidence=1.0,
                task_alignment=0.0,
                context_continuity=0.0,
                internal_consistency=0.0,
                topic_drift=1.0,
                issues=[
                    "The response is empty."
                ],
                computed={},
                metadata={
                    "prompt_token_count": 0,
                    "response_token_count": 0,
                    "context_token_count": 0,
                },
            )

        prompt_tokens = self._content_tokens(prompt_text)
        response_tokens = self._content_tokens(response_text)
        context_tokens = self._content_tokens(context_text)

        prompt_anchors = self._extract_task_anchors(
            prompt_text
        )

        response_lower = response_text.lower()

        preserved_anchors = [
            anchor
            for anchor in prompt_anchors
            if self._anchor_present(
                anchor,
                response_lower,
            )
        ]

        missing_anchors = [
            anchor
            for anchor in prompt_anchors
            if anchor not in preserved_anchors
        ]

        lexical_task_similarity = self._cosine_similarity(
            prompt_tokens,
            response_tokens,
        )

        anchor_score = self._anchor_score(
            prompt_anchors,
            preserved_anchors,
        )

        structured_output_score = (
            self._structured_output_alignment(
                prompt_text,
                response_text,
            )
        )

        task_alignment = self._combine_task_signals(
            lexical_similarity=lexical_task_similarity,
            anchor_score=anchor_score,
            structured_output_score=structured_output_score,
            prompt_anchors=prompt_anchors,
        )

        if context_tokens:
            lexical_context_similarity = self._cosine_similarity(
                context_tokens,
                response_tokens,
            )

            context_continuity = max(
                lexical_context_similarity,
                0.75 * task_alignment,
            )
        else:
            lexical_context_similarity = task_alignment
            context_continuity = task_alignment

        contradictions = self._detect_internal_contradictions(
            response_text
        )

        internal_consistency = max(
            0.0,
            1.0 - min(1.0, len(contradictions) * 0.35),
        )

        topic_drift = self._calculate_topic_drift(
            task_alignment=task_alignment,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            prompt_anchors=prompt_anchors,
            preserved_anchors=preserved_anchors,
        )

        raw_score = (
            self.task_weight * task_alignment
            + self.context_weight * context_continuity
            + self.consistency_weight * internal_consistency
        )

        drift_penalty = 0.25 * topic_drift

        score = max(
            0.0,
            min(1.0, raw_score - drift_penalty),
        )

        issues: List[str] = []
        warnings: List[str] = []

        if task_alignment < 0.35:
            issues.append(
                "The response appears poorly aligned with the original task."
            )

        if (
            prompt_anchors
            and anchor_score < 0.50
        ):
            issues.append(
                "Important task concepts were not preserved: "
                + ", ".join(missing_anchors)
            )

        if contradictions:
            issues.extend(
                f"Potential internal contradiction: {item}"
                for item in contradictions
            )

        if topic_drift >= 0.65:
            issues.append(
                "Severe topic drift detected."
            )
        elif topic_drift >= 0.40:
            warnings.append(
                "Moderate topic drift detected."
            )

        if (
            context_tokens
            and context_continuity < 0.20
        ):
            warnings.append(
                "The response has weak continuity with recent context."
            )

        confidence = self._measurement_confidence(
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            prompt_anchors=prompt_anchors,
        )

        coherent = (
            score >= self.coherence_threshold
            and not contradictions
            and task_alignment >= 0.35
            and topic_drift < 0.65
        )

        return CoherenceResult(
            coherent=coherent,
            score=round(score, 4),
            confidence=round(confidence, 4),
            task_alignment=round(task_alignment, 4),
            context_continuity=round(
                context_continuity,
                4,
            ),
            internal_consistency=round(
                internal_consistency,
                4,
            ),
            topic_drift=round(topic_drift, 4),
            issues=issues,
            warnings=warnings,
            computed={
                "context_lexical_similarity": round(
                    lexical_context_similarity,
                    4,
                ),
                "lexical_task_similarity": round(
                    lexical_task_similarity,
                    4,
                ),
                "anchor_score": round(
                    anchor_score,
                    4,
                ),
                "structured_output_score": round(
                    structured_output_score,
                    4,
                ),
                "prompt_anchors": prompt_anchors,
                "preserved_anchors": preserved_anchors,
                "missing_anchors": missing_anchors,
                "contradictions": contradictions,
            },
            metadata={
                "prompt_token_count": len(prompt_tokens),
                "response_token_count": len(response_tokens),
                "context_token_count": len(context_tokens),
                "threshold": self.coherence_threshold,
                "engine_version": 1,
            },
        )

    # ============================================================
    # INPUT NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_input(value: Any) -> str:
        if value is None:
            return ""

        if isinstance(value, dict):
            return str(value.get("content", ""))

        return str(value)

    def _flatten_context(
        self,
        context: Sequence[Any],
    ) -> str:
        pieces: List[str] = []

        for item in context:
            if isinstance(item, dict):
                content = item.get("content", "")

                if content:
                    pieces.append(str(content))
            elif item is not None:
                pieces.append(str(item))

        return "\n".join(pieces)

    def _content_tokens(
        self,
        text: str,
    ) -> List[str]:
        raw_tokens = re.findall(
            r"[A-Za-z_][A-Za-z0-9_'-]*|\d+(?:\.\d+)?",
            text.lower(),
        )

        return [
            token
            for token in raw_tokens
            if (
                token not in self.STOPWORDS
                and len(token) > 1
            )
        ]

    # ============================================================
    # TASK ALIGNMENT
    # ============================================================

    def _extract_task_anchors(
        self,
        prompt: str,
    ) -> List[str]:
        anchors: List[str] = []

        # Quoted identifiers and required JSON keys.
        anchors.extend(
            re.findall(
                r'["\']([A-Za-z_][A-Za-z0-9_]*)["\']',
                prompt,
            )
        )

        # Function-style names and symbolic identifiers.
        anchors.extend(
            re.findall(
                r"\b[A-Za-z_][A-Za-z0-9_]*\s*\([^)\n]{0,40}\)",
                prompt,
            )
        )

        # Benchmark-style named concepts.
        named_patterns = (
            r"\bObject\s+[A-Z]\b",
            r"\bCategory\s+[A-Z]\b",
            r"\bProperty\s+[A-Z]\b",
            r"\bChunk\s+\d+\b",
            r"\bPass\s+\d+\b",
            r"\bTotal Regional Tax\b",
            r"\bBase Revenue\b",
            r"\bActive Users\b",
            r"\bAverage Spend\b",
            r"\bLuxury Surcharge\b",
            r"\bSubsidy Credit\b",
            r"\bSQL injection\b",
            r"\bcookie security\b",
            r"\bbat\b",
            r"\bball\b",
        )

        for pattern in named_patterns:
            anchors.extend(
                re.findall(
                    pattern,
                    prompt,
                    re.IGNORECASE,
                )
            )

        # Variable names assigned in the prompt.
        anchors.extend(
            re.findall(
                r"\b([A-Za-z_][A-Za-z0-9_ ]{1,40})\s*=",
                prompt,
            )
        )

        cleaned: List[str] = []

        for anchor in anchors:
            normalized = re.sub(
                r"\s+",
                " ",
                anchor.strip(),
            )

            if not normalized:
                continue

            if normalized.lower() in self.STOPWORDS:
                continue

            cleaned.append(normalized)

        return self._deduplicate(cleaned)

    @staticmethod
    def _anchor_present(
        anchor: str,
        response_lower: str,
    ) -> bool:
        normalized_anchor = re.sub(
            r"\s+",
            " ",
            anchor.lower().strip(),
        )

        if normalized_anchor in response_lower:
            return True

        # Allow function-like anchors to match their base identifier.
        base_match = re.match(
            r"([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            normalized_anchor,
        )

        if base_match:
            base_identifier = base_match.group(1)

            return bool(
                re.search(
                    rf"\b{re.escape(base_identifier)}\b",
                    response_lower,
                )
            )

        return False

    @staticmethod
    def _anchor_score(
        prompt_anchors: List[str],
        preserved_anchors: List[str],
    ) -> float:
        if not prompt_anchors:
            return 1.0

        return min(
            1.0,
            len(preserved_anchors) / len(prompt_anchors),
        )

    def _structured_output_alignment(
        self,
        prompt: str,
        response: str,
    ) -> float:
        prompt_lower = prompt.lower()
        response_stripped = response.strip()

        requires_json = (
            "json" in prompt_lower
            or "containing keys" in prompt_lower
            or "keys:" in prompt_lower
        )

        if not requires_json:
            return 1.0

        looks_like_json = (
            response_stripped.startswith("{")
            and response_stripped.endswith("}")
            and ":" in response_stripped
        )

        required_keys = self._extract_explicit_keys(
            prompt
        )

        if not required_keys:
            return 1.0 if looks_like_json else 0.0

        present_keys = sum(
            1
            for key in required_keys
            if re.search(
                rf'["\']?{re.escape(key)}["\']?\s*:',
                response,
                re.IGNORECASE,
            )
        )

        key_score = present_keys / len(required_keys)

        if looks_like_json:
            return key_score

        return 0.5 * key_score

    @staticmethod
    def _extract_explicit_keys(
        prompt: str,
    ) -> List[str]:
        sections = re.findall(
            r"(?:containing|with)\s+keys?\s*:\s*"
            r"([^\n.]+(?:\n[^\n.]+)*)",
            prompt,
            re.IGNORECASE,
        )

        keys: List[str] = []

        for section in sections:
            keys.extend(
                re.findall(
                    r'["\']([A-Za-z_][A-Za-z0-9_]*)["\']',
                    section,
                )
            )

        return CoherenceEngine._deduplicate(keys)

    @staticmethod
    def _combine_task_signals(
        *,
        lexical_similarity: float,
        anchor_score: float,
        structured_output_score: float,
        prompt_anchors: List[str],
    ) -> float:
        if prompt_anchors:
            score = (
                0.35 * lexical_similarity
                + 0.45 * anchor_score
                + 0.20 * structured_output_score
            )
        else:
            score = (
                0.70 * lexical_similarity
                + 0.30 * structured_output_score
            )

        return max(0.0, min(1.0, score))

    # ============================================================
    # CONTINUITY AND SIMILARITY
    # ============================================================

    @staticmethod
    def _cosine_similarity(
        first_tokens: List[str],
        second_tokens: List[str],
    ) -> float:
        if not first_tokens or not second_tokens:
            return 0.0

        first_counter = Counter(first_tokens)
        second_counter = Counter(second_tokens)

        shared_tokens = (
            set(first_counter)
            & set(second_counter)
        )

        dot_product = sum(
            first_counter[token]
            * second_counter[token]
            for token in shared_tokens
        )

        first_norm = math.sqrt(
            sum(
                value * value
                for value in first_counter.values()
            )
        )

        second_norm = math.sqrt(
            sum(
                value * value
                for value in second_counter.values()
            )
        )

        if first_norm == 0 or second_norm == 0:
            return 0.0

        return dot_product / (
            first_norm * second_norm
        )

    def _calculate_topic_drift(
        self,
        *,
        task_alignment: float,
        prompt_tokens: List[str],
        response_tokens: List[str],
        prompt_anchors: List[str],
        preserved_anchors: List[str],
    ) -> float:
        if not response_tokens:
            return 1.0

        prompt_set = set(prompt_tokens)
        response_set = set(response_tokens)

        novel_response_tokens = (
            response_set - prompt_set
        )

        novelty_ratio = (
            len(novel_response_tokens)
            / max(1, len(response_set))
        )

        if prompt_anchors:
            anchor_loss = (
                1.0
                - len(preserved_anchors)
                / len(prompt_anchors)
            )
        else:
            anchor_loss = 0.0

        drift = (
            0.50 * (1.0 - task_alignment)
            + 0.30 * anchor_loss
            + 0.20 * novelty_ratio
        )

        return max(0.0, min(1.0, drift))

    # ============================================================
    # INTERNAL CONSISTENCY
    # ============================================================

    def _detect_internal_contradictions(
        self,
        response: str,
    ) -> List[str]:
        """
        Detect direct polarity reversals around the same subject.

        This intentionally targets obvious contradictions only.
        """
        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+|\n+",
                response,
            )
            if sentence.strip()
        ]

        claims: Dict[str, List[Tuple[bool, str]]] = {}

        for sentence in sentences:
            subject = self._extract_claim_subject(
                sentence
            )

            if not subject:
                continue

            negated = self._sentence_is_negated(
                sentence
            )

            claims.setdefault(
                subject,
                [],
            ).append(
                (
                    negated,
                    sentence,
                )
            )

        contradictions: List[str] = []

        for subject, subject_claims in claims.items():
            polarities = {
                negated
                for negated, _ in subject_claims
            }

            if len(polarities) < 2:
                continue

            positive_sentence = next(
                sentence
                for negated, sentence in subject_claims
                if not negated
            )

            negative_sentence = next(
                sentence
                for negated, sentence in subject_claims
                if negated
            )

            contradictions.append(
                f"'{positive_sentence}' conflicts with "
                f"'{negative_sentence}'"
            )

        return contradictions

    def _extract_claim_subject(
        self,
        sentence: str,
    ) -> Optional[str]:
        lowered = sentence.lower().strip()

        patterns = [
            r"\bthe\s+([a-z][a-z0-9_ -]{0,40}?)\s+"
            r"(?:does\s+not\s+|doesn't\s+|is\s+not\s+|isn't\s+)?"
            r"(?:converge|converges|diverge|diverges|is|are|has|have|can|will)\b",

            r"\b([a-z_][a-z0-9_ -]{0,40}?)\s+"
            r"(?:does\s+not\s+|doesn't\s+|is\s+not\s+|isn't\s+)?"
            r"(?:converge|converges|diverge|diverges|is|are|has|have|can|will)\b",

            r"\b([a-z_][a-z0-9_]*)\s*=\s*",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                lowered,
            )

            if not match:
                continue

            subject = re.sub(
                r"\s+",
                " ",
                match.group(1).strip(),
            )

            subject_tokens = [
                token
                for token in subject.split()
                if token not in self.STOPWORDS
            ]

            if subject_tokens:
                return " ".join(subject_tokens[-4:])

        return None

    def _sentence_is_negated(
        self,
        sentence: str,
    ) -> bool:
        lowered = sentence.lower()

        phrase_patterns = (
            r"\bdoes\s+not\b",
            r"\bdo\s+not\b",
            r"\bis\s+not\b",
            r"\bare\s+not\b",
            r"\bcannot\b",
            r"\bcan't\b",
            r"\bdoesn't\b",
            r"\bisn't\b",
            r"\bnever\b",
            r"\bfalse\b",
            r"\bincorrect\b",
        )  

        return any(
            re.search(pattern, lowered)
            for pattern in phrase_patterns
        )

    # ============================================================
    # CONFIDENCE
    # ============================================================

    @staticmethod
    def _measurement_confidence(
        *,
        prompt_tokens: List[str],
        response_tokens: List[str],
        prompt_anchors: List[str],
    ) -> float:
        evidence_points = 0.0

        if len(prompt_tokens) >= 3:
            evidence_points += 0.35

        if len(response_tokens) >= 3:
            evidence_points += 0.35

        if prompt_anchors:
            evidence_points += 0.30
        else:
            evidence_points += 0.15

        return min(1.0, evidence_points)

    # ============================================================
    # HELPERS
    # ============================================================

    @staticmethod
    def _deduplicate(
        values: List[str],
    ) -> List[str]:
        seen: Set[str] = set()
        result: List[str] = []

        for value in values:
            normalized = value.strip().lower()

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)
            result.append(value.strip())

        return result


coherence_engine = CoherenceEngine()
```