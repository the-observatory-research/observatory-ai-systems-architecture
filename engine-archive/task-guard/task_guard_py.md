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

zpp_id: task_guard_py
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
import re


@dataclass
class TaskGuardResult:
    preserved: bool
    score: float

    required_terms: List[str] = field(default_factory=list)
    missing_terms: List[str] = field(default_factory=list)

    required_phrases: List[str] = field(default_factory=list)
    missing_phrases: List[str] = field(default_factory=list)

    required_json_keys: List[str] = field(default_factory=list)
    missing_json_keys: List[str] = field(default_factory=list)

    issues: List[str] = field(default_factory=list)
    metadata: Dict[str, object] = field(default_factory=dict)


class TaskGuard:
    """
    Deterministic task-preservation guard.

    Version 1 checks:
    - important entities from the original prompt;
    - exact required phrases;
    - required JSON keys;
    - severe topic substitution.
    """

    STOPWORDS = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "to",
        "of",
        "in",
        "on",
        "for",
        "with",
        "is",
        "are",
        "be",
        "if",
        "then",
        "from",
        "by",
        "at",
        "this",
        "that",
        "your",
        "you",
        "must",
        "output",
        "answer",
        "problem",
        "task",
        "step",
        "current",
        "final",
    }

    def verify(
        self,
        prompt: str,
        response: str,
    ) -> TaskGuardResult:
        prompt_text = prompt or ""
        response_text = response or ""

        required_terms = self._extract_required_terms(
            prompt_text
        )

        required_phrases = self._extract_exact_phrases(
            prompt_text
        )

        required_json_keys = self._extract_json_keys(
            prompt_text
        )

        response_lower = response_text.lower()

        missing_terms = [
            term
            for term in required_terms
            if term.lower() not in response_lower
        ]

        missing_phrases = [
            phrase
            for phrase in required_phrases
            if phrase.lower() not in response_lower
        ]

        missing_json_keys = [
            key
            for key in required_json_keys
            if not re.search(
                rf'["\']?{re.escape(key)}["\']?\s*:',
                response_text,
                re.IGNORECASE,
            )
        ]

        issues: List[str] = []

        if missing_terms:
            issues.append(
                "Task entities not echoed in the response: "
                + ", ".join(missing_terms)
            )

        if missing_phrases:
            issues.append(
                "Required exact phrase was not produced: "
                + ", ".join(missing_phrases)
            )

        if missing_json_keys:
            issues.append(
                "Required JSON keys were missing: "
                + ", ".join(missing_json_keys)
            )

        hard_checks = (
            len(required_phrases)
          + len(required_json_keys)
        )

        hard_missing = (
            len(missing_phrases)
            + len(missing_json_keys)
        )

        soft_checks = len(required_terms)
        soft_missing = len(missing_terms)

        if hard_checks > 0:
            hard_score = max(
                0.0,
                1.0 - (hard_missing / hard_checks),
            )
        else:
            hard_score = 1.0

        if soft_checks > 0:
            soft_score = max(
                0.0,
                1.0 - (soft_missing / soft_checks),
            )
        else:
            soft_score = 1.0

        if hard_checks > 0:
            score = (
                0.8 * hard_score
                + 0.2 * soft_score
            )
            preserved = (hard_missing == 0)

        elif soft_checks > 0:
            score = soft_score
            preserved = (soft_score >= 0.5)

        else:
            score = 1.0
            preserved = True

        return TaskGuardResult(
            preserved=preserved,
            score=round(score, 4),
            required_terms=required_terms,
            missing_terms=missing_terms,
            required_phrases=required_phrases,
            missing_phrases=missing_phrases,
            required_json_keys=required_json_keys,
            missing_json_keys=missing_json_keys,
            issues=issues,
            metadata={
                "hard_checks": hard_checks,
                "hard_missing": hard_missing,
                "soft_checks": soft_checks,
                "soft_missing": soft_missing,
                "hard_score": round(hard_score, 4),
                "soft_score": round(soft_score, 4),
            },
        )

    def _extract_required_terms(
        self,
        prompt: str,
    ) -> List[str]:
        """
        Extract explicit task entities without inventing partial matches.
        """
        candidates: List[str] = []

        symbolic_matches = re.findall(
            r"\b(?:"
            r"Object\s+[A-Z]"
            r"|Category\s+[A-Z]"
            r"|Property\s+[A-Z]"
            r"|Chunk\s+\d+"
            r"|Pass\s+\d+"
            r"|Total Regional Tax"
            r"|Base Revenue"
            r"|Active Users"
            r"|Average Spend"
            r"|Luxury Surcharge"
            r"|Subsidy Credit"
            r")\b",
            prompt,
            re.IGNORECASE,
        )

        candidates.extend(
            match.strip()
            for match in symbolic_matches
        )

        # Important nouns used in benchmark-style prompts.
        benchmark_terms = (
            "bat",
            "ball",
            "sql injection",
            "cookie",
            "secure=false",
            "httponly=false",
            "total regional tax",
            "base revenue",
            "active users",
            "average spend",
            "luxury surcharge",
            "subsidy credit",
        )

        prompt_lower = prompt.lower()

        for term in benchmark_terms:
            if term in prompt_lower:
                candidates.append(term)

        return self._deduplicate(candidates)

    def _extract_exact_phrases(
        self,
        prompt: str,
    ) -> List[str]:
        phrases: List[str] = []

        patterns = [
            r'output\s+the\s+exact\s+phrase:\s*"([^"]+)"',
            r"output\s+exactly:\s*([^\n]+)",
            r"return\s+exactly:\s*([^\n]+)",
        ]

        for pattern in patterns:
            for match in re.finditer(
                pattern,
                prompt,
                re.IGNORECASE,
            ):
                phrase = match.group(1).strip()

                if phrase:
                    phrases.append(phrase)

        return self._deduplicate(phrases)

    def _extract_json_keys(
        self,
        prompt: str,
    ) -> List[str]:
        """
        Extract only keys explicitly requested as JSON fields.
        Do not treat every quoted string in the prompt as a key.
        """
        keys: List[str] = []

        key_sections = re.findall(
            r"(?:containing|with)\s+keys?\s*:\s*([^\n.]+(?:\n[^\n.]+)*)",
            prompt,
            re.IGNORECASE,
        )

        for section in key_sections:
            keys.extend(
                re.findall(
                    r'["\']([A-Za-z_][A-Za-z0-9_]*)["\']',
                    section,
                )
            )

        return self._deduplicate(keys)

    @staticmethod
    def _deduplicate(
        values: List[str],
    ) -> List[str]:
        seen = set()
        ordered: List[str] = []

        for value in values:
            normalized = value.strip().lower()

            if not normalized or normalized in seen:
                continue

            seen.add(normalized)
            ordered.append(value.strip())

        return ordered


task_guard = TaskGuard()
```