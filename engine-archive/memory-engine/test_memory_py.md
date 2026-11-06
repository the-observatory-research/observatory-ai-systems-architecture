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

zpp_id: test_memory_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
from pathlib import Path

from memory import (
    ContextRequest,
    MemoryClass,
    MemoryEngine,
    MemoryRepository,
    TrustRole,
)

# ────────────────────────────────────────────────────────────
# SETUP
# ────────────────────────────────────────────────────────────

database_path = Path(__file__).with_name("memory_lattice.db")

repository = MemoryRepository(database_path)
repository.initialize()

engine = MemoryEngine(repository)

print("=" * 60)
print("MEMORY ENGINE TEST")
print("=" * 60)
print()

# ────────────────────────────────────────────────────────────
# 1. RECORD A CONVERSATION EXCHANGE
# ────────────────────────────────────────────────────────────

print("1. Recording conversation exchange...")
conversation = engine.record_exchange(
    speaker="Kai",
    content="Memory is not the preservation of text. It is the preservation of trusted architectural state.",
    source="Horizon 🌅",
    metadata={
        "model": "deepseek-r1:7b",
        "channel": "interactive",
    },
)
print(f"   ✅ Created: {conversation.anchor_id}")
print(f"   Trust Role: {conversation.trust_role.value}")
print(f"   Verification: {conversation.verification_state.value}")
print()

# ────────────────────────────────────────────────────────────
# 2. RECORD TELEMETRY (should be excluded from context)
# ────────────────────────────────────────────────────────────

print("2. Recording telemetry (should be excluded from context)...")
telemetry = engine.record_observation(
    memory_class=MemoryClass.TELEMETRY,
    speaker="Node",
    content="Pulse worker completed in 842 milliseconds.",
    source="Horizon 🌅",
    metadata={
        "subsystem": "pulse_worker",
        "duration_ms": 842,
    },
)
print(f"   ✅ Created: {telemetry.anchor_id}")
print(f"   Trust Role: {telemetry.trust_role.value}")
print(f"   Verification: {telemetry.verification_state.value}")
print()

# ────────────────────────────────────────────────────────────
# 3. PROMOTE THE CONVERSATION TO TRUSTED
# ────────────────────────────────────────────────────────────

print("3. Promoting conversation to TRUSTED...")
promoted = engine.promote(
    conversation.anchor_id,
    reason="Architectural statement reviewed and approved for future continuity.",
)
print(f"   ✅ Promoted: {promoted.anchor_id}")
print(f"   New Trust Role: {promoted.trust_role.value}")
print(f"   New Verification: {promoted.verification_state.value}")
print()

# ────────────────────────────────────────────────────────────
# 4. RETRIEVE REASONING CONTEXT
# ────────────────────────────────────────────────────────────

print("4. Retrieving reasoning context...")
context = engine.retrieve_context(
    ContextRequest(
        query="trusted architectural memory",
        max_records=10,
        max_characters=5_000,
    )
)

print(f"   ✅ Retrieved {len(context.records)} records")
print(f"   Total characters: {context.total_characters}")
print(f"   Excluded by budget: {context.excluded_by_budget}")
print()

# ────────────────────────────────────────────────────────────
# 5. VERIFY TELEMETRY IS EXCLUDED
# ────────────────────────────────────────────────────────────

context_ids = {record.anchor_id for record in context.records}

print("5. Verifying telemetry exclusion...")
assert conversation.anchor_id in context_ids, "❌ Conversation not found in context!"
assert telemetry.anchor_id not in context_ids, "❌ Telemetry was included in context!"

print(f"   ✅ Conversation found: {conversation.anchor_id}")
print(f"   ✅ Telemetry excluded: {telemetry.anchor_id}")
print()

# ────────────────────────────────────────────────────────────
# 6. RENDER CONTEXT
# ────────────────────────────────────────────────────────────

print("6. Rendering context as string...")
rendered = context.render()
print(f"   ✅ Rendered {len(rendered)} characters")
print()

# ────────────────────────────────────────────────────────────
# 7. CONVERT CONTEXT TO MESSAGES (for pipeline)
# ────────────────────────────────────────────────────────────

print("7. Converting context to messages...")
messages = context.to_messages()
print(f"   ✅ Generated {len(messages)} messages")
for i, msg in enumerate(messages):
    print(f"      [{i+1}] {msg['role']}: {msg['content'][:60]}...")
print()

# ────────────────────────────────────────────────────────────
# 8. HEALTH CHECK
# ────────────────────────────────────────────────────────────

print("8. Running health check...")
health = engine.health_check()
print(f"   Healthy: {health.is_healthy}")
print(f"   Integrity: {health.database_integrity}")
print(f"   Total Records: {health.total_records}")
print(f"   Total Events: {health.total_events}")
print(f"   Trusted: {health.trusted_records}")
print(f"   Operational: {health.operational_records}")
print(f"   Observational: {health.observational_records}")
print(f"   Quarantined: {health.quarantined_records}")
print(f"   Archived: {health.archived_records}")
print(f"   Orphaned Links: {health.orphaned_parent_links}")
print(f"   Broken Supersession: {health.broken_supersession_links}")
print()

# ────────────────────────────────────────────────────────────
# 9. FINAL ASSERTIONS
# ────────────────────────────────────────────────────────────

print("9. Running final assertions...")
assert health.is_healthy, "❌ Health check failed!"
assert health.database_integrity == ("ok",), "❌ Database integrity check failed!"
assert promoted.trust_role == TrustRole.TRUSTED, "❌ Promotion failed!"
assert conversation.anchor_id not in telemetry.anchor_id, "❌ Anchor IDs collided!"

print("   ✅ All assertions passed!")
print()

# ────────────────────────────────────────────────────────────
# 10. DISPLAY LINEAGE
# ────────────────────────────────────────────────────────────

print("10. Tracing lineage...")
lineage = engine.get_lineage(conversation.anchor_id)
print(f"    ✅ Lineage length: {len(lineage)}")
for record in lineage:
    print(f"       - {record.anchor_id} ({record.trust_role.value})")
print()

# ────────────────────────────────────────────────────────────
# DONE
# ────────────────────────────────────────────────────────────

print("=" * 60)
print("✅ ALL MEMORY ENGINE TESTS PASSED")
print("=" * 60)
```