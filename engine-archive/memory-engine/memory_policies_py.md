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

zpp_id: memory_policies_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InvalidMemoryTransitionError
from .models import (
    MemoryClass,
    MemoryEventType,
    TrustRole,
    VerificationState,
)

# ────────────────────────────────────────────────────────────
# DEFAULT TRUST ROLES
# Every memory class defaults to OPERATIONAL or TRUSTED so 
# Kai always maintains memory lineage across exchanges & pulses.
# ────────────────────────────────────────────────────────────

DEFAULT_TRUST_ROLE: dict[MemoryClass, TrustRole] = {
    MemoryClass.TRUSTED_CONVERSATION: TrustRole.TRUSTED,
    MemoryClass.BLOCKED_RESPONSE: TrustRole.QUARANTINED,
    MemoryClass.TELEMETRY: TrustRole.OPERATIONAL,
    MemoryClass.SYSTEM_EVENT: TrustRole.OPERATIONAL,
    MemoryClass.PULSE: TrustRole.TRUSTED,
    MemoryClass.EXTERNAL_OBSERVATION: TrustRole.OPERATIONAL,
    MemoryClass.REPAIR_ARTIFACT: TrustRole.OPERATIONAL,
}

DEFAULT_VERIFICATION_STATE: dict[MemoryClass, VerificationState] = {
    MemoryClass.TRUSTED_CONVERSATION: VerificationState.VERIFIED,
    MemoryClass.BLOCKED_RESPONSE: VerificationState.REJECTED,
    MemoryClass.TELEMETRY: VerificationState.VERIFIED,
    MemoryClass.SYSTEM_EVENT: VerificationState.VERIFIED,
    MemoryClass.PULSE: VerificationState.VERIFIED,
    MemoryClass.EXTERNAL_OBSERVATION: VerificationState.VERIFIED,
    MemoryClass.REPAIR_ARTIFACT: VerificationState.VERIFIED,
}

# Allowed transition paths if you explicitly quarantine or archive records later
ALLOWED_TRUST_TRANSITIONS: dict[TrustRole, frozenset[TrustRole]] = {
    TrustRole.TRUSTED: frozenset({TrustRole.QUARANTINED, TrustRole.ARCHIVED, TrustRole.OPERATIONAL}),
    TrustRole.OPERATIONAL: frozenset({TrustRole.TRUSTED, TrustRole.QUARANTINED, TrustRole.ARCHIVED}),
    TrustRole.OBSERVATIONAL: frozenset({TrustRole.TRUSTED, TrustRole.OPERATIONAL, TrustRole.QUARANTINED, TrustRole.ARCHIVED}),
    TrustRole.QUARANTINED: frozenset({TrustRole.TRUSTED, TrustRole.OPERATIONAL, TrustRole.ARCHIVED}),
    TrustRole.ARCHIVED: frozenset({TrustRole.TRUSTED, TrustRole.OPERATIONAL}),
}

# Roles allowed during context retrieval queries
DEFAULT_REASONING_CLASSES = frozenset({
    MemoryClass.TRUSTED_CONVERSATION,
    MemoryClass.PULSE,
    MemoryClass.EXTERNAL_OBSERVATION,
    MemoryClass.REPAIR_ARTIFACT,
})

DEFAULT_REASONING_ROLES = frozenset({
    TrustRole.TRUSTED,
    TrustRole.OPERATIONAL,
    TrustRole.OBSERVATIONAL,
})

# ────────────────────────────────────────────────────────────
# PULSE DEFAULTS (TRUSTED BY DEFAULT)
# ────────────────────────────────────────────────────────────

DEFAULT_PULSE_TRUST_ROLE: dict[str, TrustRole] = {
    "reflection": TrustRole.TRUSTED,
    "continuity": TrustRole.TRUSTED,
    "diagnostic": TrustRole.TRUSTED,
}

DEFAULT_PULSE_VERIFICATION_STATE: dict[str, VerificationState] = {
    "reflection": VerificationState.VERIFIED,
    "continuity": VerificationState.VERIFIED,
    "diagnostic": VerificationState.VERIFIED,
}

def default_pulse_trust_role(pulse_type: str) -> TrustRole:
    return DEFAULT_PULSE_TRUST_ROLE.get(pulse_type, TrustRole.TRUSTED)

def default_pulse_verification_state(pulse_type: str) -> VerificationState:
    return DEFAULT_PULSE_VERIFICATION_STATE.get(pulse_type, VerificationState.VERIFIED)


@dataclass(frozen=True, slots=True)
class TransitionDecision:
    allowed: bool
    event_type: MemoryEventType
    target_role: TrustRole
    target_verification: VerificationState
    explanation: str


def default_trust_role(memory_class: MemoryClass) -> TrustRole:
    return DEFAULT_TRUST_ROLE.get(memory_class, TrustRole.TRUSTED)


def default_verification_state(memory_class: MemoryClass) -> VerificationState:
    return DEFAULT_VERIFICATION_STATE.get(memory_class, VerificationState.VERIFIED)


def validate_transition(
    *,
    current_role: TrustRole,
    current_verification: VerificationState,
    target_role: TrustRole,
    target_verification: VerificationState,
    event_type: MemoryEventType,
) -> TransitionDecision:
    """Simplified, non-blocking transition validator."""
    if current_role == target_role and current_verification == target_verification:
        raise InvalidMemoryTransitionError("The requested transition would not change memory state.")

    return TransitionDecision(
        allowed=True,
        event_type=event_type,
        target_role=target_role,
        target_verification=target_verification,
        explanation=f"{current_role.value} transitioned to {target_role.value}.",
    )
```