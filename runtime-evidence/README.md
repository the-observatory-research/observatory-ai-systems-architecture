# Runtime Evidence — Six-Node ZPP Mesh

**The Observatory — AI Systems Architecture**  
**Record type:** Historical runtime-observation index plus independently inspected snapshot aggregates  
**Status:** Historical development snapshot; active validation program remains open

This folder connects the preserved architecture documents to observable behavior without treating planned features as demonstrated capabilities. It supplements—not replaces—the original [runtime observation record](../architecture/multi_agent_runtime_observations.md) and [architecture invariant audit](../architecture/architecture_invariant_audit.md).

## Start here

- [Evidence register](EVIDENCE_REGISTER.md) — major findings with evidence class and source location.
- [Snapshot audit](SNAPSHOT_AUDIT.md) — read-only aggregate review of the supplied `node.zip` snapshot.
- [Failures and corrections](FAILURES_AND_CORRECTIONS.md) — documented engineering corrections, without claims of causal certainty beyond the record.
- [Open replication plan](OPEN_REPLICATION_PLAN.md) — what a future reproducible runtime evaluation must still demonstrate.
- [Aggregate JSON](snapshot/aggregate_counts.json) — counts only; no original payloads, paths, databases or transcripts.
- [Data handling](DATA_HANDLING.md) — materials deliberately excluded from public release.
- [Provenance](SOURCE_PROVENANCE.md) — hashes and dates of source archives, limitations of snapshot-level verification.

## Evidence terminology

| Term | Meaning here |
|---|---|
| **Snapshot-verified** | Independently calculated from the supplied file snapshot during preparation; not proof of live behavior. |
| **Historically reported** | Described in the original runtime-observation record; not re-executed for this release. |
| **Implemented / static** | Present in the code or documentation; no new runtime pass claimed. |
| **Open** | Requires explicit future testing; not a validated claim. |

The [15-invariant audit](../architecture/architecture_invariant_audit.md) explicitly distinguishes *implemented*, *observed*, *reproduced*, and *validated*. Those original statuses are **not upgraded** by inclusion in this repository.

## Operational context

The historical six-node configuration uses independent A/B/C validators, D discovery, E bridge retrieval, and F internet ingress/local reasoning. The documented active launcher for the supplied framework is [`framework/node/boot_mesh.sh`](../framework/node/boot_mesh.sh); `start_mesh.py` is **retired**. The engine chain in `engine-archive/` belongs to an earlier stage and is not assumed to run within this mesh.

**This folder does not establish production readiness, secure node authentication, complete state persistence, or live changed-only ingestion correctness.** No public copy of the original runtime log files or databases is included; they contain source paths, operational records and possibly sensitive content.
