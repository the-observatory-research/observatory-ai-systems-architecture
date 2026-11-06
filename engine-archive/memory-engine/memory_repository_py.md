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

zpp_id: memory_repository_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from __future__ import annotations

import json
import sqlite3

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .exceptions import (
    DuplicateMemoryRecordError,
    MemoryIntegrityError,
    MemoryRecordNotFoundError,
    MemoryTransactionError,
)
from .models import (
    MemoryClass,
    MemoryEvent,
    MemoryEventType,
    MemoryRecord,
    TrustRole,
    VerificationState,
)


def datetime_to_storage(value: datetime) -> str:
    """
    Serialize a timezone-aware datetime as UTC ISO-8601 text.
    """
    if value.tzinfo is None:
        raise ValueError("Cannot store a naive datetime.")

    return value.astimezone(timezone.utc).isoformat(
        timespec="microseconds"
    )


def datetime_from_storage(value: str) -> datetime:
    """
    Deserialize an ISO-8601 datetime and normalize it to UTC.
    """
    parsed = datetime.fromisoformat(value)

    if parsed.tzinfo is None:
        raise ValueError(
            f"Stored datetime is not timezone-aware: {value!r}"
        )

    return parsed.astimezone(timezone.utc)


def encode_metadata(metadata: Mapping[str, Any]) -> str:
    try:
        return json.dumps(
            dict(metadata),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise MemoryIntegrityError(
            "Memory metadata must be JSON-serializable."
        ) from exc


def decode_metadata(value: str | None) -> dict[str, Any]:
    if not value:
        return {}

    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as exc:
        raise MemoryIntegrityError(
            "Stored memory metadata contains invalid JSON."
        ) from exc

    if not isinstance(decoded, dict):
        raise MemoryIntegrityError(
            "Stored memory metadata must be a JSON object."
        )

    return decoded


def row_to_record(row: sqlite3.Row) -> MemoryRecord:
    return MemoryRecord(
        anchor_id=row["anchor_id"],
        parent_anchor_id=row["parent_anchor_id"],
        memory_class=MemoryClass(row["memory_class"]),
        trust_role=TrustRole(row["trust_role"]),
        verification_state=VerificationState(
            row["verification_state"]
        ),
        source=row["source"],
        speaker=row["speaker"],
        content=row["content"],
        created_at=datetime_from_storage(row["created_at"]),
        supersedes=row["supersedes"],
        superseded_by=row["superseded_by"],
        metadata=decode_metadata(row["metadata_json"]),
    )


def row_to_event(row: sqlite3.Row) -> MemoryEvent:
    previous_role = row["previous_role"]
    new_role = row["new_role"]

    previous_verification = row["previous_verification_state"]
    new_verification = row["new_verification_state"]

    return MemoryEvent(
        event_id=row["event_id"],
        anchor_id=row["anchor_id"],
        event_type=MemoryEventType(row["event_type"]),
        reason=row["reason"],
        actor=row["actor"],
        created_at=datetime_from_storage(row["created_at"]),
        previous_role=(
            TrustRole(previous_role) if previous_role else None
        ),
        new_role=TrustRole(new_role) if new_role else None,
        previous_verification_state=(
            VerificationState(previous_verification)
            if previous_verification
            else None
        ),
        new_verification_state=(
            VerificationState(new_verification)
            if new_verification
            else None
        ),
        metadata=decode_metadata(row["metadata_json"]),
    )


class MemoryTransaction:
    """
    A single explicit Memory Lattice transaction.

    Instances are created by MemoryRepository.transaction(). They should
    not be constructed directly.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._closed = False

    def _ensure_open(self) -> None:
        if self._closed:
            raise MemoryTransactionError(
                "This memory transaction is already closed."
            )

    def close(self) -> None:
        self._closed = True

    def insert_record(
        self,
        record: MemoryRecord,
        *,
        actor: str,
        reason: str = "Memory record created.",
    ) -> MemoryRecord:
        self._ensure_open()

        try:
            self._connection.execute(
                """
                INSERT INTO memory_records (
                    anchor_id,
                    parent_anchor_id,
                    memory_class,
                    trust_role,
                    verification_state,
                    source,
                    speaker,
                    content,
                    created_at,
                    supersedes,
                    superseded_by,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.anchor_id,
                    record.parent_anchor_id,
                    record.memory_class.value,
                    record.trust_role.value,
                    record.verification_state.value,
                    record.source,
                    record.speaker,
                    record.content,
                    datetime_to_storage(record.created_at),
                    record.supersedes,
                    record.superseded_by,
                    encode_metadata(record.metadata),
                ),
            )

            event = MemoryEvent.create(
                anchor_id=record.anchor_id,
                event_type=MemoryEventType.CREATED,
                reason=reason,
                actor=actor,
                new_role=record.trust_role,
                new_verification_state=record.verification_state,
            )

            self.insert_event(event)

        except sqlite3.IntegrityError as exc:
            message = str(exc).lower()

            if "unique" in message or "primary key" in message:
                raise DuplicateMemoryRecordError(
                    f"Memory anchor already exists: {record.anchor_id}"
                ) from exc

            raise MemoryIntegrityError(
                f"Could not insert memory record {record.anchor_id}: {exc}"
            ) from exc

        return record

    def insert_event(self, event: MemoryEvent) -> MemoryEvent:
        self._ensure_open()

        try:
            self._connection.execute(
                """
                INSERT INTO memory_events (
                    event_id,
                    anchor_id,
                    event_type,
                    previous_role,
                    new_role,
                    previous_verification_state,
                    new_verification_state,
                    reason,
                    actor,
                    created_at,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.anchor_id,
                    event.event_type.value,
                    (
                        event.previous_role.value
                        if event.previous_role
                        else None
                    ),
                    event.new_role.value if event.new_role else None,
                    (
                        event.previous_verification_state.value
                        if event.previous_verification_state
                        else None
                    ),
                    (
                        event.new_verification_state.value
                        if event.new_verification_state
                        else None
                    ),
                    event.reason,
                    event.actor,
                    datetime_to_storage(event.created_at),
                    encode_metadata(event.metadata),
                ),
            )

        except sqlite3.IntegrityError as exc:
            message = str(exc).lower()

            if "unique" in message or "primary key" in message:
                raise DuplicateMemoryRecordError(
                    f"Memory event already exists: {event.event_id}"
                ) from exc

            raise MemoryIntegrityError(
                f"Could not insert memory event {event.event_id}: {exc}"
            ) from exc

        return event

    def get_record(
        self,
        anchor_id: str,
        *,
        required: bool = True,
    ) -> MemoryRecord | None:
        self._ensure_open()

        row = self._connection.execute(
            """
            SELECT *
            FROM memory_records
            WHERE anchor_id = ?
            """,
            (anchor_id,),
        ).fetchone()

        if row is None:
            if required:
                raise MemoryRecordNotFoundError(
                    f"Memory record not found: {anchor_id}"
                )
            return None

        return row_to_record(row)

    def update_governance(
        self,
        anchor_id: str,
        *,
        trust_role: TrustRole | None = None,
        verification_state: VerificationState | None = None,
        event_type: MemoryEventType,
        actor: str,
        reason: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> MemoryRecord:
        """
        Update governed state while preserving an explicit audit event.

        Transition legality belongs in the future policy layer. This
        repository method only performs an atomic state transition.
        """
        self._ensure_open()

        current = self.get_record(anchor_id)

        next_role = trust_role or current.trust_role
        next_verification = (
            verification_state or current.verification_state
        )

        self._connection.execute(
            """
            UPDATE memory_records
            SET trust_role = ?,
                verification_state = ?
            WHERE anchor_id = ?
            """,
            (
                next_role.value,
                next_verification.value,
                anchor_id,
            ),
        )

        event = MemoryEvent.create(
            anchor_id=anchor_id,
            event_type=event_type,
            previous_role=current.trust_role,
            new_role=next_role,
            previous_verification_state=current.verification_state,
            new_verification_state=next_verification,
            reason=reason,
            actor=actor,
            metadata=metadata,
        )

        self.insert_event(event)

        updated = self.get_record(anchor_id)
        assert updated is not None

        return updated

    def link_supersession(
        self,
        *,
        older_anchor_id: str,
        newer_anchor_id: str,
        actor: str,
        reason: str,
    ) -> tuple[MemoryRecord, MemoryRecord]:
        """
        Atomically connect two records through supersession lineage.
        """
        self._ensure_open()

        if older_anchor_id == newer_anchor_id:
            raise MemoryIntegrityError(
                "A memory record cannot supersede itself."
            )

        older = self.get_record(older_anchor_id)
        newer = self.get_record(newer_anchor_id)

        if older.superseded_by not in (None, newer_anchor_id):
            raise MemoryIntegrityError(
                f"{older_anchor_id} is already superseded by "
                f"{older.superseded_by}."
            )

        if newer.supersedes not in (None, older_anchor_id):
            raise MemoryIntegrityError(
                f"{newer_anchor_id} already supersedes "
                f"{newer.supersedes}."
            )

        self._connection.execute(
            """
            UPDATE memory_records
            SET superseded_by = ?
            WHERE anchor_id = ?
            """,
            (newer_anchor_id, older_anchor_id),
        )

        self._connection.execute(
            """
            UPDATE memory_records
            SET supersedes = ?
            WHERE anchor_id = ?
            """,
            (older_anchor_id, newer_anchor_id),
        )

        self.insert_event(
            MemoryEvent.create(
                anchor_id=older_anchor_id,
                event_type=MemoryEventType.SUPERSEDED,
                reason=reason,
                actor=actor,
                metadata={
                    "superseded_by": newer_anchor_id,
                },
            )
        )

        self.insert_event(
            MemoryEvent.create(
                anchor_id=newer_anchor_id,
                event_type=MemoryEventType.SUPERSEDED,
                reason=reason,
                actor=actor,
                metadata={
                    "supersedes": older_anchor_id,
                },
            )
        )

        updated_older = self.get_record(older_anchor_id)
        updated_newer = self.get_record(newer_anchor_id)

        assert updated_older is not None
        assert updated_newer is not None

        return updated_older, updated_newer


class MemoryRepository:
    """
    SQLite persistence boundary for the Memory Lattice.

    Governance policy belongs above this layer. The repository guarantees
    durable, atomic, auditable storage operations.
    """

    def __init__(
        self,
        database_path: str | Path,
        *,
        schema_path: str | Path | None = None,
        busy_timeout_ms: int = 5_000,
    ) -> None:
        self.database_path = Path(database_path)

        self.schema_path = (
            Path(schema_path)
            if schema_path is not None
            else Path(__file__).with_name("schema.sql")
        )

        self.busy_timeout_ms = busy_timeout_ms

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = sqlite3.connect(
            self.database_path,
            timeout=self.busy_timeout_ms / 1_000,
            isolation_level=None,
        )

        connection.row_factory = sqlite3.Row

        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
            f"PRAGMA busy_timeout = {self.busy_timeout_ms}"
        )

        # WAL permits concurrent readers while preserving one writer.
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")

        return connection

    def initialize(self) -> None:
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"Memory schema not found: {self.schema_path}"
            )

        schema = self.schema_path.read_text(encoding="utf-8")

        connection = self._connect()

        try:
            connection.executescript(schema)
        except sqlite3.DatabaseError as exc:
            raise MemoryTransactionError(
                f"Could not initialize Memory Lattice: {exc}"
            ) from exc
        finally:
            connection.close()

    @contextmanager
    def transaction(self) -> Iterator[MemoryTransaction]:
        """
        Open an explicit write transaction.

        BEGIN IMMEDIATE acquires the SQLite write reservation at the
        beginning of the transaction rather than failing midway through
        a multi-step memory operation.
        """
        connection = self._connect()
        transaction = MemoryTransaction(connection)

        try:
            connection.execute("BEGIN IMMEDIATE")
            yield transaction
            connection.execute("COMMIT")

        except Exception:
            try:
                connection.execute("ROLLBACK")
            except sqlite3.DatabaseError:
                pass
            raise

        finally:
            transaction.close()
            connection.close()

    @contextmanager
    def read_transaction(self) -> Iterator[MemoryTransaction]:
        """
        Open a consistent read snapshot.
        """
        connection = self._connect()
        transaction = MemoryTransaction(connection)

        try:
            connection.execute("BEGIN")
            yield transaction
            connection.execute("COMMIT")

        except Exception:
            try:
                connection.execute("ROLLBACK")
            except sqlite3.DatabaseError:
                pass
            raise

        finally:
            transaction.close()
            connection.close()

    def get_record(
        self,
        anchor_id: str,
        *,
        required: bool = True,
    ) -> MemoryRecord | None:
        with self.read_transaction() as transaction:
            return transaction.get_record(
                anchor_id,
                required=required,
            )

    def get_events(
        self,
        anchor_id: str,
    ) -> tuple[MemoryEvent, ...]:
        connection = self._connect()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM memory_events
                WHERE anchor_id = ?
                ORDER BY created_at ASC, event_id ASC
                """,
                (anchor_id,),
            ).fetchall()

            return tuple(row_to_event(row) for row in rows)

        finally:
            connection.close()

    def list_records(
        self,
        *,
        trust_roles: Sequence[TrustRole] | None = None,
        memory_classes: Sequence[MemoryClass] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[MemoryRecord, ...]:
        if limit < 1:
            raise ValueError("limit must be at least 1.")

        if offset < 0:
            raise ValueError("offset cannot be negative.")

        clauses: list[str] = []
        parameters: list[Any] = []

        if trust_roles:
            placeholders = ",".join("?" for _ in trust_roles)
            clauses.append(f"trust_role IN ({placeholders})")
            parameters.extend(role.value for role in trust_roles)

        if memory_classes:
            placeholders = ",".join("?" for _ in memory_classes)
            clauses.append(f"memory_class IN ({placeholders})")
            parameters.extend(
                memory_class.value
                for memory_class in memory_classes
            )

        where_clause = (
            f"WHERE {' AND '.join(clauses)}"
            if clauses
            else ""
        )

        query = f"""
            SELECT *
            FROM memory_records
            {where_clause}
            ORDER BY created_at DESC, anchor_id DESC
            LIMIT ?
            OFFSET ?
        """

        parameters.extend((limit, offset))

        connection = self._connect()

        try:
            rows = connection.execute(
                query,
                parameters,
            ).fetchall()

            return tuple(row_to_record(row) for row in rows)

        finally:
            connection.close()

    def integrity_check(self) -> tuple[str, ...]:
        connection = self._connect()

        try:
            rows = connection.execute(
                "PRAGMA integrity_check"
            ).fetchall()

            return tuple(str(row[0]) for row in rows)

        finally:
            connection.close()

    def health_metrics(self) -> dict[str, int]:
        connection = self._connect()

        try:
            total_records = connection.execute(
                "SELECT COUNT(*) FROM memory_records"
            ).fetchone()[0]

            total_events = connection.execute(
                "SELECT COUNT(*) FROM memory_events"
            ).fetchone()[0]

            role_rows = connection.execute(
                """
                SELECT trust_role, COUNT(*) AS count
                FROM memory_records
                GROUP BY trust_role
                """
            ).fetchall()

            role_counts = {
                row["trust_role"]: row["count"]
                for row in role_rows
            }

            orphaned_parent_links = connection.execute(
                """
                SELECT COUNT(*)
                FROM memory_records AS child
                LEFT JOIN memory_records AS parent
                    ON child.parent_anchor_id = parent.anchor_id
                WHERE child.parent_anchor_id IS NOT NULL
                  AND parent.anchor_id IS NULL
                """
            ).fetchone()[0]

            broken_supersession_links = connection.execute(
                """
                SELECT COUNT(*)
                FROM memory_records AS older
                LEFT JOIN memory_records AS newer
                    ON older.superseded_by = newer.anchor_id
                WHERE older.superseded_by IS NOT NULL
                  AND (
                      newer.anchor_id IS NULL
                      OR newer.supersedes != older.anchor_id
                  )
                """
            ).fetchone()[0]

            return {
                "total_records": total_records,
                "total_events": total_events,
                "trusted_records": role_counts.get("TRUSTED", 0),
                "operational_records": role_counts.get("OPERATIONAL", 0),
                "observational_records": role_counts.get("OBSERVATIONAL", 0),
                "quarantined_records": role_counts.get("QUARANTINED", 0),
                "archived_records": role_counts.get("ARCHIVED", 0),
                "orphaned_parent_links": orphaned_parent_links,
                "broken_supersession_links": broken_supersession_links,
            }

        finally:
            connection.close()
```