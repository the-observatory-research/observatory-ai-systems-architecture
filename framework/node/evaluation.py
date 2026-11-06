#!/usr/bin/env python3

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EvaluationResult:
    """
    Authoritative evaluation record shared by scoring, routing,
    telemetry, persistence, and the dashboard.
    """

    # Primary scores
    gamma_score: float
    coherence: float
    entropy: float
    novelty: float
    self_reference: float
    paradox: float

    # Routing
    route: str
    gamma_lock: bool

    # Operational measurements
    recursion_depth: int = 0
    convergence_similarity: Optional[float] = None
    issues_detected: int = 0

    # Risk is separate from gamma quality.
    risk_score: Optional[float] = None

    # Metadata
    anchor_id: Optional[str] = None
    source: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dictionary."""
        return asdict(self)

    def to_legacy_gamma_dict(self) -> Dict[str, Any]:
        """
        Compatibility format for code still expecting the old
        GammaScorer dictionary.
        """
        return {
            "score": self.gamma_score,
            "route": self.route,
            "gamma_lock": self.gamma_lock,
            "factors": {
                "coherence": self.coherence,
                "entropy": self.entropy,
                "novelty": self.novelty,
                "self_reference": self.self_reference,
                "paradox": self.paradox,
            },
            "recursion": {
                "depth": self.recursion_depth,
                "convergence_similarity": (
                    self.convergence_similarity
                ),
                "issues_detected": self.issues_detected,
            },
            "risk_score": self.risk_score,
        }