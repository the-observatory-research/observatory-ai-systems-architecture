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

zpp_id: memory_schema_sql
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS memory_records (
    anchor_id TEXT PRIMARY KEY,
    parent_anchor_id TEXT,
    memory_class TEXT NOT NULL CHECK (
        memory_class IN (
            'trusted_conversation',
            'blocked_response',
            'telemetry',
            'system_event',
            'pulse',
            'external_observation',
            'repair_artifact'
        )
    ),
    trust_role TEXT NOT NULL CHECK (
        trust_role IN (
            'TRUSTED',
            'OPERATIONAL',
            'OBSERVATIONAL',
            'QUARANTINED',
            'ARCHIVED'
        )
    ),
    verification_state TEXT NOT NULL CHECK (
        verification_state IN (
            'UNVERIFIED',
            'VERIFIED',
            'REJECTED',
            'REVIEW_REQUIRED'
        )
    ),
    source TEXT NOT NULL,
    speaker TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    supersedes TEXT,
    superseded_by TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (parent_anchor_id)
        REFERENCES memory_records(anchor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (supersedes)
        REFERENCES memory_records(anchor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (superseded_by)
        REFERENCES memory_records(anchor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS idx_memory_records_created_at
    ON memory_records(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_memory_records_parent
    ON memory_records(parent_anchor_id);

CREATE INDEX IF NOT EXISTS idx_memory_records_trust_role
    ON memory_records(trust_role);

CREATE INDEX IF NOT EXISTS idx_memory_records_class
    ON memory_records(memory_class);

CREATE INDEX IF NOT EXISTS idx_memory_records_verification
    ON memory_records(verification_state);

CREATE INDEX IF NOT EXISTS idx_memory_records_source
    ON memory_records(source);

CREATE TABLE IF NOT EXISTS memory_events (
    event_id TEXT PRIMARY KEY,
    anchor_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (
        event_type IN (
            'CREATED',
            'PROMOTED',
            'QUARANTINED',
            'ARCHIVED',
            'VERIFIED',
            'REJECTED',
            'SUPERSEDED',
            'METADATA_UPDATED'
        )
    ),
    previous_role TEXT,
    new_role TEXT,
    previous_verification_state TEXT,
    new_verification_state TEXT,
    reason TEXT NOT NULL,
    actor TEXT NOT NULL,
    created_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (anchor_id)
        REFERENCES memory_records(anchor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_memory_events_anchor
    ON memory_events(anchor_id, created_at ASC);

CREATE INDEX IF NOT EXISTS idx_memory_events_type
    ON memory_events(event_type);

CREATE TABLE IF NOT EXISTS memory_schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

INSERT OR IGNORE INTO memory_schema_version (
    version,
    applied_at
)
VALUES (
    1,
    strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
);

-- ────────────────────────────────────────────────────────────
-- PULSE RECORDS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pulse_records (
    pulse_id TEXT PRIMARY KEY,

    anchor_id TEXT NOT NULL,

    pulse_type TEXT NOT NULL CHECK (
        pulse_type IN ('reflection', 'continuity', 'diagnostic')
    ),

    pulse_number INTEGER NOT NULL,

    content TEXT NOT NULL,
    prompt TEXT NOT NULL,

    coherence REAL DEFAULT 0.0,
    entropy REAL DEFAULT 0.0,
    novelty REAL DEFAULT 0.0,
    self_reference REAL DEFAULT 0.0,
    paradox REAL DEFAULT 0.0,
    raw_score REAL DEFAULT 0.0,

    trust_role TEXT NOT NULL CHECK (
        trust_role IN (
            'TRUSTED',
            'OPERATIONAL',
            'OBSERVATIONAL',
            'QUARANTINED',
            'ARCHIVED'
        )
    ) DEFAULT 'OBSERVATIONAL',

    verification_state TEXT NOT NULL CHECK (
        verification_state IN (
            'UNVERIFIED',
            'VERIFIED',
            'REJECTED',
            'REVIEW_REQUIRED'
        )
    ) DEFAULT 'UNVERIFIED',

    source TEXT NOT NULL DEFAULT 'PulseFramework',
    speaker TEXT NOT NULL DEFAULT 'Kai',

    created_at TEXT NOT NULL,

    parent_pulse_id TEXT,
    supersedes TEXT,
    superseded_by TEXT,

    metadata_json TEXT NOT NULL DEFAULT '{}',

    FOREIGN KEY (anchor_id)
        REFERENCES memory_records(anchor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (parent_pulse_id)
        REFERENCES pulse_records(pulse_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (supersedes)
        REFERENCES pulse_records(pulse_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (superseded_by)
        REFERENCES pulse_records(pulse_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_pulse_records_pulse_number
    ON pulse_records(pulse_number DESC);

CREATE INDEX IF NOT EXISTS idx_pulse_records_created_at
    ON pulse_records(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_pulse_records_pulse_type
    ON pulse_records(pulse_type);

CREATE INDEX IF NOT EXISTS idx_pulse_records_trust_role
    ON pulse_records(trust_role);

CREATE INDEX IF NOT EXISTS idx_pulse_records_anchor
    ON pulse_records(anchor_id);

CREATE INDEX IF NOT EXISTS idx_pulse_records_parent
    ON pulse_records(parent_pulse_id);
```