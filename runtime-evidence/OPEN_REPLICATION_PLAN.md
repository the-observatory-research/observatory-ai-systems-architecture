# Open Replication and Validation Plan

The original [architecture invariant audit](../architecture/architecture_invariant_audit.md) defines seven required tests (A–G). This is a **planning aid**, not a newly completed experiment or historical revision.

| Original test | Proposed controlled check | Evidence to capture |
|---|---|---|
| A — Source Fidelity | Trace a known input through source hash, signed handoff, validator input and persisted reasoning | Linked IDs/hashes, full input/output lineage, explicit mismatches |
| B — Changed-Only Ingestion | Seed a controlled fixture of N files; rerun unchanged, alter one, add one | Baseline manifest, counts of D/E/A/B/C/F deliveries, duplicate-event audit |
| C — Persistence Across Restart | Process a known event, terminate all nodes, restart, retrieve the same state | DB fingerprints before and after, state IDs, restart times |
| D — Signed Transport Tamper Test | Sign with a registered key, tamper payload, substitute unknown signer | Accept/reject logs; trusted-identity binding and replay outcomes |
| E — Differentiated Convergence | Provide equivalent test input to A/B/C across varied states | Per-node measurements, scoring definitions, expected agreements/disagreements |
| F — Reasoning Persistence | Produce one identifiable inference, then restart F and retrieve it | Inference ID, transaction record, receipt, post-restart retrieval |
| G — Failure Isolation | Disable one node during bounded workload, then restore | Time-stamped node-state and message-flow evidence; recovery and data loss |

**Next named historical checkpoint:** NODE_E changed-only ingestion against the 182-path seeded manifest. For a public reproducibility suite, use *synthetic fixture files* rather than a private vault. After verification, results can be added in an append-only validation report while keeping the original September snapshot unchanged.

## Reporting discipline

Every future run should state software version, Python/runtime versions, model version and configuration (if an LLM is used), environment, exact fixed input, expected behavior, observed behavior, exception details, output files and SHA-256 fingerprints. Preserve failed runs and corrections rather than replacing them with a successful summary.
