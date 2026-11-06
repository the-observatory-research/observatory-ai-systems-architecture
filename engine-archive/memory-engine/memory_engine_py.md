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

zpp_id: memory_engine_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from types import MappingProxyType
from typing import Any, Mapping, Sequence
from uuid import uuid4

from .exceptions import InvalidMemoryTransitionError
from .health import MemoryHealthReport
from .models import (
    MemoryClass,
    MemoryEvent,
    MemoryEventType,
    MemoryRecord,
    PulseRecord,
    TrustRole,
    VerificationState,
)
from .policies import (
    DEFAULT_REASONING_CLASSES,
    DEFAULT_REASONING_ROLES,
    default_trust_role,
    default_verification_state,
    default_pulse_trust_role,
    default_pulse_verification_state,
    validate_transition,
)
from .repository import MemoryRepository, datetime_to_storage, encode_metadata


# ────────────────────────────────────────────────────────────
# CONTEXT REQUEST & RESPONSE
# ────────────────────────────────────────────────────────────

class ContextRequest:
    """
    Request configuration for retrieving reasoning context.

    By default, only TRUSTED and OPERATIONAL records from
    trusted_conversation, pulse, external_observation, and repair_artifact
    are included. Quarantined and Archived records are never included
    in normal context reconstruction.
    """

    def __init__(
        self,
        query: str = "",
        max_records: int = 12,
        max_characters: int = 12_000,
        include_classes: frozenset[MemoryClass] | None = None,
        include_roles: frozenset[TrustRole] | None = None,
        required_anchor_ids: tuple[str, ...] = (),
        include_superseded: bool = False,
    ):
        if max_records < 1:
            raise ValueError("max_records must be at least 1.")
        if max_characters < 1:
            raise ValueError("max_characters must be at least 1.")

        self.query = query
        self.max_records = max_records
        self.max_characters = max_characters
        self.include_classes = include_classes or DEFAULT_REASONING_CLASSES
        self.include_roles = include_roles or DEFAULT_REASONING_ROLES
        self.required_anchor_ids = required_anchor_ids
        self.include_superseded = include_superseded

        if TrustRole.QUARANTINED in self.include_roles:
            raise ValueError(
                "Quarantined memory cannot be loaded into reasoning context."
            )

        if TrustRole.ARCHIVED in self.include_roles:
            raise ValueError(
                "Archived memory cannot be loaded into reasoning context. "
                "Use inspect_archive() for historical inspection."
            )


class ReconstructedContext:
    """
    Structured result of a context retrieval request.
    """

    def __init__(
        self,
        records: tuple[MemoryRecord, ...],
        total_characters: int,
        excluded_by_budget: int,
        required_anchors_loaded: tuple[str, ...],
        required_anchors_missing: tuple[str, ...],
        lineage_complete: bool,
    ):
        self.records = records
        self.total_characters = total_characters
        self.excluded_by_budget = excluded_by_budget
        self.required_anchors_loaded = required_anchors_loaded
        self.required_anchors_missing = required_anchors_missing
        self.lineage_complete = lineage_complete

    def render(self) -> str:
        """Render context as a human-readable string."""
        sections = []
        for record in self.records:
            sections.append(
                "\n".join((
                    f"[{record.anchor_id}]",
                    f"Source: {record.source}",
                    f"Speaker: {record.speaker}",
                    f"Class: {record.memory_class.value}",
                    f"Trust: {record.trust_role.value}",
                    f"Created: {record.created_at.isoformat()}",
                    "",
                    record.content,
                ))
            )
        return "\n\n---\n\n".join(sections)

    def to_messages(self) -> list[dict[str, str]]:
        """Convert to OpenAI-compatible message format for Kai."""
        messages = []
        for record in self.records:
            role = "user" if record.speaker == "user" else "assistant"
            messages.append({
                "role": role,
                "content": record.content,
            })
        return messages


# ────────────────────────────────────────────────────────────
# MEMORY ENGINE
# ────────────────────────────────────────────────────────────

class MemoryEngine:
    """
    Trust-governed runtime interface to the Memory Lattice.

    MemoryEngine decides what transitions are legal, what records
    influence future reasoning, and how context is reconstructed.

    MemoryRepository performs the durable storage operations.
    """

    def __init__(
        self,
        repository: MemoryRepository,
        actor: str = "MemoryEngine",
    ):
        self.repository = repository
        self.actor = actor

    # ────────────────────────────────────────────────────────
    # RECORDING
    # ────────────────────────────────────────────────────────

    def record_exchange(
        self,
        speaker: str,
        content: str,
        source: str = "Horizon 🌅",
        parent_anchor_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        trusted: bool = False,
        reason: str = "Conversation exchange recorded.",
    ) -> MemoryRecord:
        """Record a conversation exchange."""
        trust_role = TrustRole.TRUSTED if trusted else TrustRole.OBSERVATIONAL
        verification_state = VerificationState.VERIFIED if trusted else VerificationState.UNVERIFIED

        record = MemoryRecord.create(
            memory_class=MemoryClass.TRUSTED_CONVERSATION,
            trust_role=trust_role,
            verification_state=verification_state,
            source=source,
            speaker=speaker,
            content=content,
            parent_anchor_id=parent_anchor_id,
            metadata=metadata,
        )

        with self.repository.transaction() as tx:
            tx.insert_record(record, actor=self.actor, reason=reason)

        return record

    def record_observation(
        self,
        memory_class: MemoryClass,
        speaker: str,
        content: str,
        source: str = "Horizon 🌅",
        parent_anchor_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        reason: str = "Observation recorded.",
    ) -> MemoryRecord:
        """Record a non-conversation observation (telemetry, pulse, system event, etc.)."""
        record = MemoryRecord.create(
            memory_class=memory_class,
            trust_role=default_trust_role(memory_class),
            verification_state=default_verification_state(memory_class),
            source=source,
            speaker=speaker,
            content=content,
            parent_anchor_id=parent_anchor_id,
            metadata=metadata,
        )

        with self.repository.transaction() as tx:
            tx.insert_record(record, actor=self.actor, reason=reason)

        return record

    def record_pulse(
        self,
        pulse_type: str,
        content: str,
        prompt: str,
        anchor_id: str,
        pulse_number: int,
        coherence: float = 0.0,
        entropy: float = 0.0,
        novelty: float = 0.0,
        self_reference: float = 0.0,
        paradox: float = 0.0,
        raw_score: float = 0.0,
        trust_role: TrustRole | None = None,
        verification_state: VerificationState | None = None,
        source: str = "PulseFramework",
        speaker: str = "Kai",
        parent_pulse_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        reason: str = "Pulse recorded.",
    ) -> PulseRecord:
        """
        Record a pulse from the Pulse Framework.

        This creates a pulse record in the dedicated pulse_records table
        AND creates a corresponding memory_record for lineage tracking.
        """
        trust_role = trust_role or default_pulse_trust_role(pulse_type)
        verification_state = verification_state or default_pulse_verification_state(pulse_type)

        pulse = PulseRecord.create(
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
            parent_pulse_id=parent_pulse_id,
            metadata=metadata,
        )

        # Also create a memory record for lineage
        memory_record = MemoryRecord.create(
            anchor_id=anchor_id,
            memory_class=MemoryClass.PULSE,
            trust_role=trust_role,
            verification_state=verification_state,
            source=source,
            speaker=speaker,
            content=content,
            metadata={
                "pulse_id": pulse.pulse_id,
                "pulse_type": pulse_type,
                "pulse_number": pulse_number,
                "prompt": prompt,
                "coherence": coherence,
                "entropy": entropy,
                "novelty": novelty,
                "self_reference": self_reference,
                "paradox": paradox,
                "raw_score": raw_score,
                **(metadata or {}),
            },
        )

        with self.repository.transaction() as tx:
            # Insert memory record
            tx.insert_record(
                memory_record,
                actor="PulseFramework",
                reason=f"Pulse recorded: {pulse_type} #{pulse_number}",
            )

            # Insert pulse record
            self._insert_pulse_record(tx, pulse)

        return pulse

    def _insert_pulse_record(self, transaction, pulse: PulseRecord) -> None:
        """Insert a pulse record into the pulse_records table."""
        connection = transaction._connection
        connection.execute(
            """
            INSERT INTO pulse_records (
                pulse_id, anchor_id, pulse_type, pulse_number,
                content, prompt,
                coherence, entropy, novelty, self_reference, paradox, raw_score,
                trust_role, verification_state,
                source, speaker, created_at,
                parent_pulse_id, supersedes, superseded_by,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pulse.pulse_id,
                pulse.anchor_id,
                pulse.pulse_type,
                pulse.pulse_number,
                pulse.content,
                pulse.prompt,
                pulse.coherence,
                pulse.entropy,
                pulse.novelty,
                pulse.self_reference,
                pulse.paradox,
                pulse.raw_score,
                pulse.trust_role.value,
                pulse.verification_state.value,
                pulse.source,
                pulse.speaker,
                datetime_to_storage(pulse.created_at),
                pulse.parent_pulse_id,
                pulse.supersedes,
                pulse.superseded_by,
                encode_metadata(pulse.metadata),
            )
        )

    # ────────────────────────────────────────────────────────
    # GOVERNANCE
    # ────────────────────────────────────────────────────────

    def promote(
        self,
        anchor_id: str,
        reason: str,
        actor: str | None = None,
    ) -> MemoryRecord:
        """Promote a record to TRUSTED and VERIFIED."""
        current = self.repository.get_record(anchor_id)

        decision = validate_transition(
            current_role=current.trust_role,
            current_verification=current.verification_state,
            target_role=TrustRole.TRUSTED,
            target_verification=VerificationState.VERIFIED,
            event_type=MemoryEventType.PROMOTED,
        )

        with self.repository.transaction() as tx:
            return tx.update_governance(
                anchor_id,
                trust_role=decision.target_role,
                verification_state=decision.target_verification,
                event_type=decision.event_type,
                actor=actor or self.actor,
                reason=reason,
            )

    def quarantine(
        self,
        anchor_id: str,
        reason: str,
        actor: str | None = None,
        reject: bool = False,
    ) -> MemoryRecord:
        """Move a record to QUARANTINED."""
        current = self.repository.get_record(anchor_id)

        verification_state = (
            VerificationState.REJECTED if reject else VerificationState.REVIEW_REQUIRED
        )

        decision = validate_transition(
            current_role=current.trust_role,
            current_verification=current.verification_state,
            target_role=TrustRole.QUARANTINED,
            target_verification=verification_state,
            event_type=MemoryEventType.QUARANTINED,
        )

        with self.repository.transaction() as tx:
            return tx.update_governance(
                anchor_id,
                trust_role=decision.target_role,
                verification_state=decision.target_verification,
                event_type=decision.event_type,
                actor=actor or self.actor,
                reason=reason,
            )

    def archive(
        self,
        anchor_id: str,
        reason: str,
        actor: str | None = None,
    ) -> MemoryRecord:
        """Move a record to ARCHIVED."""
        current = self.repository.get_record(anchor_id)

        decision = validate_transition(
            current_role=current.trust_role,
            current_verification=current.verification_state,
            target_role=TrustRole.ARCHIVED,
            target_verification=current.verification_state,
            event_type=MemoryEventType.ARCHIVED,
        )

        with self.repository.transaction() as tx:
            return tx.update_governance(
                anchor_id,
                trust_role=decision.target_role,
                verification_state=decision.target_verification,
                event_type=decision.event_type,
                actor=actor or self.actor,
                reason=reason,
            )

    def restore_from_archive(
        self,
        anchor_id: str,
        reason: str,
        actor: str | None = None,
    ) -> MemoryRecord:
        """Restore an archived record to OBSERVATIONAL."""
        current = self.repository.get_record(anchor_id)

        if current.trust_role != TrustRole.ARCHIVED:
            raise InvalidMemoryTransitionError(
                f"Record {anchor_id} is not archived (current: {current.trust_role.value})."
            )

        decision = validate_transition(
            current_role=current.trust_role,
            current_verification=current.verification_state,
            target_role=TrustRole.OBSERVATIONAL,
            target_verification=VerificationState.UNVERIFIED,
            event_type=MemoryEventType.PROMOTED,
        )

        with self.repository.transaction() as tx:
            return tx.update_governance(
                anchor_id,
                trust_role=decision.target_role,
                verification_state=decision.target_verification,
                event_type=decision.event_type,
                actor=actor or self.actor,
                reason=reason,
            )

    # ────────────────────────────────────────────────────────
    # INSPECTION
    # ────────────────────────────────────────────────────────

    def get_record(self, anchor_id: str) -> MemoryRecord | None:
        """Retrieve a single record by anchor_id."""
        return self.repository.get_record(anchor_id, required=False)

    def get_events(self, anchor_id: str) -> tuple[MemoryEvent, ...]:
        """Retrieve all events for a record."""
        return self.repository.get_events(anchor_id)

    def get_lineage(
        self,
        anchor_id: str,
        max_depth: int = 100,
    ) -> tuple[MemoryRecord, ...]:
        """Trace the parent lineage of a record."""
        if max_depth < 1:
            raise ValueError("max_depth must be at least 1.")

        lineage = []
        visited = set()
        current = self.repository.get_record(anchor_id)

        while current is not None:
            if current.anchor_id in visited:
                raise RuntimeError(f"Cycle detected in memory lineage at {current.anchor_id}.")
            visited.add(current.anchor_id)
            lineage.append(current)

            if len(lineage) >= max_depth or current.parent_anchor_id is None:
                break

            current = self.repository.get_record(current.parent_anchor_id, required=False)

        return tuple(reversed(lineage))

    def inspect_archive(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[MemoryRecord, ...]:
        """Retrieve archived records for historical inspection only."""
        return self.repository.list_records(
            trust_roles=(TrustRole.ARCHIVED,),
            limit=limit,
            offset=offset,
        )

    def search(
        self,
        query: str,
        trust_roles: Sequence[TrustRole] | None = None,
        memory_classes: Sequence[MemoryClass] | None = None,
        limit: int = 20,
    ) -> tuple[MemoryRecord, ...]:
        """Search memory records by content (basic keyword search)."""
        trust_roles = trust_roles or tuple(DEFAULT_REASONING_ROLES)
        memory_classes = memory_classes or tuple(DEFAULT_REASONING_CLASSES)

        candidates = self.repository.list_records(
            trust_roles=trust_roles,
            memory_classes=memory_classes,
            limit=limit * 2,
        )

        query_terms = self._query_terms(query)
        scored = sorted(
            candidates,
            key=lambda r: self._relevance_score(r, query_terms),
            reverse=True,
        )

        return tuple(scored[:limit])

    # ────────────────────────────────────────────────────────
    # CONTEXT RECONSTRUCTION
    # ────────────────────────────────────────────────────────

    def retrieve_context(self, request: ContextRequest) -> ReconstructedContext:
        """Retrieve trusted context for Kai's reasoning."""
        candidate_limit = max(request.max_records * 10, 100)

        candidates = self.repository.list_records(
            trust_roles=tuple(request.include_roles),
            memory_classes=tuple(request.include_classes),
            limit=candidate_limit,
        )

        required_records = []
        required_loaded = []
        required_missing = []

        for anchor_id in request.required_anchor_ids:
            record = self.repository.get_record(anchor_id, required=False)
            if record is None:
                required_missing.append(anchor_id)
                continue
            if record.trust_role in (TrustRole.QUARANTINED, TrustRole.ARCHIVED):
                required_missing.append(anchor_id)
                continue
            if record.trust_role not in request.include_roles:
                required_missing.append(anchor_id)
                continue
            if record.memory_class not in request.include_classes:
                required_missing.append(anchor_id)
                continue
            required_records.append(record)
            required_loaded.append(anchor_id)

        query_terms = self._query_terms(request.query)

        scored_candidates = sorted(
            candidates,
            key=lambda r: (
                self._relevance_score(r, query_terms),
                r.created_at,
            ),
            reverse=True,
        )

        # Always preserve the newest eligible conversation records.
        latest_records = candidates[:4]

        ordered = []
        seen = set()

        for record in required_records:
            if record.anchor_id not in seen:
                ordered.append(record)
                seen.add(record.anchor_id)

        for record in latest_records:
            if record.anchor_id in seen:
                continue

            if (
                not request.include_superseded
                and record.superseded_by is not None
            ):
                continue

            ordered.append(record)
            seen.add(record.anchor_id)

        for record in scored_candidates:
            if record.anchor_id in seen:
                continue

            if (
                not request.include_superseded
                and record.superseded_by is not None
            ):
                continue

            ordered.append(record)
            seen.add(record.anchor_id)

        selected = []
        total_characters = 0
        excluded_by_budget = 0

        for record in ordered:
            if len(selected) >= request.max_records:
                excluded_by_budget += 1
                continue

            if (
                total_characters + len(record.content)
                > request.max_characters
            ):
                excluded_by_budget += 1
                continue

            selected.append(record)
            total_characters += len(record.content)

        selected.sort(key=lambda record: record.created_at)

        lineage_complete = self._lineage_is_complete(selected)

        return ReconstructedContext(
            records=tuple(selected),
            total_characters=total_characters,
            excluded_by_budget=excluded_by_budget,
            required_anchors_loaded=tuple(required_loaded),
            required_anchors_missing=tuple(required_missing),
            lineage_complete=lineage_complete,
        )

    # ────────────────────────────────────────────────────────
    # HEALTH & MAINTENANCE
    # ────────────────────────────────────────────────────────

    def health_check(self) -> MemoryHealthReport:
        """Run a full health check on the Memory Lattice."""
        integrity = self.repository.integrity_check()
        metrics = self.repository.health_metrics()

        warnings = []
        database_healthy = integrity == ("ok",)

        if not database_healthy:
            warnings.append("SQLite integrity check did not return 'ok'.")
        if metrics["orphaned_parent_links"] > 0:
            warnings.append("Memory Lattice contains orphaned parent links.")
        if metrics["broken_supersession_links"] > 0:
            warnings.append("Memory Lattice contains broken supersession links.")

        return MemoryHealthReport(
            is_healthy=(
                database_healthy
                and metrics["orphaned_parent_links"] == 0
                and metrics["broken_supersession_links"] == 0
            ),
            database_integrity=integrity,
            total_records=metrics["total_records"],
            total_events=metrics["total_events"],
            trusted_records=metrics["trusted_records"],
            operational_records=metrics["operational_records"],
            observational_records=metrics["observational_records"],
            quarantined_records=metrics["quarantined_records"],
            archived_records=metrics["archived_records"],
            orphaned_parent_links=metrics["orphaned_parent_links"],
            broken_supersession_links=metrics["broken_supersession_links"],
            warnings=tuple(warnings),
        )

    def compact(
        self,
        older_than_days: int = 90,
        actor: str = "MemoryEngine",
    ) -> tuple[int, list[str]]:
        """Archive records older than the threshold."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
        candidates = self.repository.list_records(
            trust_roles=(TrustRole.OBSERVATIONAL, TrustRole.OPERATIONAL),
            limit=1000,
        )

        archived = []
        for record in candidates:
            if record.created_at < cutoff:
                self.archive(
                    record.anchor_id,
                    reason=f"Automatically archived due to age ({older_than_days} days).",
                    actor=actor,
                )
                archived.append(record.anchor_id)

        return len(archived), archived

    # ────────────────────────────────────────────────────────
    # INTERNAL HELPERS
    # ────────────────────────────────────────────────────────

    @staticmethod
    def _query_terms(query: str) -> frozenset[str]:
        return frozenset(
            token.lower()
            for token in re.findall(r"[A-Za-z0-9_]+", query)
            if len(token) >= 2
        )

    @staticmethod
    def _relevance_score(record: MemoryRecord, query_terms: frozenset[str]) -> int:
        if not query_terms:
            return 0
        searchable = " ".join((record.content, record.source, record.speaker, record.memory_class.value)).lower()
        return sum(searchable.count(term) for term in query_terms)

    def _lineage_is_complete(self, records: Sequence[MemoryRecord]) -> bool:
        loaded_ids = {r.anchor_id for r in records}
        for record in records:
            if record.parent_anchor_id is not None and record.parent_anchor_id not in loaded_ids:
                parent = self.repository.get_record(record.parent_anchor_id, required=False)
                if parent is None:
                    return False
        return True
```