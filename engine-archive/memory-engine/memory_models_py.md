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

zpp_id: memory_models_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4


# ────────────────────────────────────────────────────────────
# ENUMS
# ────────────────────────────────────────────────────────────

class MemoryClass(StrEnum):
    TRUSTED_CONVERSATION = "trusted_conversation"
    BLOCKED_RESPONSE = "blocked_response"
    TELEMETRY = "telemetry"
    SYSTEM_EVENT = "system_event"
    PULSE = "pulse"
    EXTERNAL_OBSERVATION = "external_observation"
    REPAIR_ARTIFACT = "repair_artifact"


class TrustRole(StrEnum):
    TRUSTED = "TRUSTED"
    OPERATIONAL = "OPERATIONAL"
    OBSERVATIONAL = "OBSERVATIONAL"
    QUARANTINED = "QUARANTINED"
    ARCHIVED = "ARCHIVED"


class VerificationState(StrEnum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class MemoryEventType(StrEnum):
    CREATED = "CREATED"
    PROMOTED = "PROMOTED"
    QUARANTINED = "QUARANTINED"
    ARCHIVED = "ARCHIVED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"
    METADATA_UPDATED = "METADATA_UPDATED"


# ────────────────────────────────────────────────────────────
# HELPERS (MUST BE DEFINED BEFORE DATACLASSES THAT USE THEM)
# ────────────────────────────────────────────────────────────

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def create_anchor_id() -> str:
    return f"mem_{uuid4().hex}"


def create_event_id() -> str:
    return f"evt_{uuid4().hex}"


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("Datetime values must be timezone-aware.")
    return value.astimezone(timezone.utc)


def freeze_metadata(
    metadata: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


# ────────────────────────────────────────────────────────────
# PULSE RECORD
# ────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class PulseRecord:
    pulse_id: str
    anchor_id: str
    pulse_type: str
    pulse_number: int
    content: str
    prompt: str

    coherence: float = 0.0
    entropy: float = 0.0
    novelty: float = 0.0
    self_reference: float = 0.0
    paradox: float = 0.0
    raw_score: float = 0.0

    trust_role: TrustRole = TrustRole.OBSERVATIONAL
    verification_state: VerificationState = VerificationState.UNVERIFIED

    source: str = "PulseFramework"
    speaker: str = "Kai"

    created_at: datetime = field(default_factory=utc_now)

    parent_pulse_id: str | None = None
    supersedes: str | None = None
    superseded_by: str | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.pulse_id.strip():
            raise ValueError("pulse_id cannot be empty.")
        if not self.anchor_id.strip():
            raise ValueError("anchor_id cannot be empty.")
        if self.pulse_type not in ("reflection", "continuity", "diagnostic"):
            raise ValueError(f"Invalid pulse_type: {self.pulse_type}")
        if self.pulse_number < 1:
            raise ValueError("pulse_number must be >= 1")
        if not self.content.strip():
            raise ValueError("content cannot be empty.")
        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty.")

        object.__setattr__(self, "created_at", ensure_utc(self.created_at))
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    @classmethod
    def create(
        cls,
        *,
        anchor_id: str,
        pulse_type: str,
        pulse_number: int,
        content: str,
        prompt: str,
        coherence: float = 0.0,
        entropy: float = 0.0,
        novelty: float = 0.0,
        self_reference: float = 0.0,
        paradox: float = 0.0,
        raw_score: float = 0.0,
        trust_role: TrustRole = TrustRole.OBSERVATIONAL,
        verification_state: VerificationState = VerificationState.UNVERIFIED,
        source: str = "PulseFramework",
        speaker: str = "Kai",
        parent_pulse_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        pulse_id: str | None = None,
        created_at: datetime | None = None,
    ) -> PulseRecord:
        return cls(
            pulse_id=pulse_id or f"pulse_{uuid4().hex}",
            anchor_id=anchor_id,
            pulse_type=pulse_type,
            pulse_number=pulse_number,
            content=content,
            prompt=prompt,
            coherence=coherence,
            entropy=entropy,
            novelty=novelty,
            self_reference=self_reference,
            paradox=paradox,
            raw_score=raw_score,
            trust_role=trust_role,
            verification_state=verification_state,
            source=source,
            speaker=speaker,
            created_at=created_at or utc_now(),
            parent_pulse_id=parent_pulse_id,
            metadata=metadata,
        )

# ────────────────────────────────────────────────────────────
# MEMORY RECORD
# ────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class MemoryRecord:
    anchor_id: str
    memory_class: MemoryClass
    trust_role: TrustRole
    verification_state: VerificationState

    source: str
    speaker: str
    content: str
    created_at: datetime

    parent_anchor_id: str | None = None
    supersedes: str | None = None
    superseded_by: str | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.anchor_id.strip():
            raise ValueError("anchor_id cannot be empty.")

        if not self.source.strip():
            raise ValueError("source cannot be empty.")

        if not self.speaker.strip():
            raise ValueError("speaker cannot be empty.")

        if not self.content.strip():
            raise ValueError("content cannot be empty.")

        object.__setattr__(self, "created_at", ensure_utc(self.created_at))
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

        if self.parent_anchor_id == self.anchor_id:
            raise ValueError("A record cannot be its own parent.")

        if self.supersedes == self.anchor_id:
            raise ValueError("A record cannot supersede itself.")

        if self.superseded_by == self.anchor_id:
            raise ValueError("A record cannot be superseded by itself.")

    @classmethod
    def create(
        cls,
        *,
        memory_class: MemoryClass,
        trust_role: TrustRole,
        verification_state: VerificationState,
        source: str,
        speaker: str,
        content: str,
        parent_anchor_id: str | None = None,
        supersedes: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        anchor_id: str | None = None,
        created_at: datetime | None = None,
    ) -> MemoryRecord:
        return cls(
            anchor_id=anchor_id or create_anchor_id(),
            parent_anchor_id=parent_anchor_id,
            memory_class=memory_class,
            trust_role=trust_role,
            verification_state=verification_state,
            source=source,
            speaker=speaker,
            content=content,
            created_at=created_at or utc_now(),
            supersedes=supersedes,
            metadata=freeze_metadata(metadata),
        )


@dataclass(frozen=True, slots=True)
class MemoryEvent:
    event_id: str
    anchor_id: str
    event_type: MemoryEventType

    reason: str
    actor: str
    created_at: datetime

    previous_role: TrustRole | None = None
    new_role: TrustRole | None = None

    previous_verification_state: VerificationState | None = None
    new_verification_state: VerificationState | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id cannot be empty.")

        if not self.anchor_id.strip():
            raise ValueError("anchor_id cannot be empty.")

        if not self.reason.strip():
            raise ValueError("Memory events require a reason.")

        if not self.actor.strip():
            raise ValueError("Memory events require an actor.")

        object.__setattr__(self, "created_at", ensure_utc(self.created_at))
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    @classmethod
    def create(
        cls,
        *,
        anchor_id: str,
        event_type: MemoryEventType,
        reason: str,
        actor: str,
        previous_role: TrustRole | None = None,
        new_role: TrustRole | None = None,
        previous_verification_state: VerificationState | None = None,
        new_verification_state: VerificationState | None = None,
        metadata: Mapping[str, Any] | None = None,
        event_id: str | None = None,
        created_at: datetime | None = None,
    ) -> MemoryEvent:
        return cls(
            event_id=event_id or create_event_id(),
            anchor_id=anchor_id,
            event_type=event_type,
            reason=reason,
            actor=actor,
            created_at=created_at or utc_now(),
            previous_role=previous_role,
            new_role=new_role,
            previous_verification_state=previous_verification_state,
            new_verification_state=new_verification_state,
            metadata=freeze_metadata(metadata),
        )
```