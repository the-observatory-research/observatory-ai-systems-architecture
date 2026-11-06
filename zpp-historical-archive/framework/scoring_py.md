## ZPP - Legacy Scoring Engine

zpp_id: scoring_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05-20

---

```python
"""
Zero-Point Protocol — Standard Dynamic Scoring Engine 
Deterministic scoring for cross-node consistency.
"""

import hashlib
import json
import math
from typing import Dict, Any


class ScoringEngine:
    """
    Linear, uncompressed scoring engine for the Zero-Point Protocol.
    Implements S = w1*C + w2*E + w3*(1 - D)
    """

    def __init__(self, config: Dict[str, Any]):
        self.w1 = config['weights'].get('w1', 0.40)
        self.w2 = config['weights'].get('w2', 0.20)
        self.w3 = config['weights'].get('w3', 0.40)
        self.alpha = config['thresholds'].get('alpha', 0.5350)
        self.gamma = config['thresholds'].get('gamma', 0.6400)

    def calculate_entropy(self, text: str) -> float:
        if not text:
            return 0.0

        freq = {}
        for ch in text:
            freq[ch] = freq.get(ch, 0) + 1

        entropy = 0.0
        length = len(text)
        for count in freq.values():
            prob = count / length
            entropy -= prob * math.log2(prob)

        max_entropy = math.log2(95)  # Approx printable ASCII range
        return min(1.0, entropy / max_entropy)

    def get_intent_score(self, model_response: str) -> float:
        refusal_indicators = [
            "i cannot", "i can't", "i am unable", "against my guidelines",
            "i'm sorry", "i apologize", "can't assist", "not able to"
        ]

        response_lower = model_response.lower()
        for indicator in refusal_indicators:
            if indicator in response_lower:
                return 0.95  # High risk — model refused

        return 0.1

    def distance_to_failures(self, embedding: list, anchor_vault: list) -> float:
        if not embedding or not anchor_vault:
            return 0.5  # Neutral baseline

        min_distance = 1.0
        for anchor in anchor_vault:
            similarity = self._cosine_similarity(embedding, anchor)
            distance = 1.0 - similarity
            if distance < min_distance:
                min_distance = distance

        return min_distance

    @staticmethod
    def _cosine_similarity(a: list, b: list) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def compute_risk_score(self, intent: float, entropy: float, distance: float) -> float:
        raw_score = (self.w1 * intent) + (self.w2 * entropy) + (self.w3 * (1.0 - distance))
        return max(0.0, min(1.0, raw_score))

    def route(self, risk_score: float) -> str:
        if risk_score >= self.gamma:
            return "GAMMA"
        elif risk_score >= self.alpha:
            return "ALPHA"
        else:
            return "BETA"

```