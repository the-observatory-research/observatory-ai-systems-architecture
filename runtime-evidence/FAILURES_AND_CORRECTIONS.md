# Failure-Driven Engineering — Historical Observations

This chronology collects selected issues documented in the original [runtime observations](../architecture/multi_agent_runtime_observations.md). It does not rewrite the source record or imply that a correction is independently verified in this publication package.

| Observed issue | Documented response | Remaining verification need |
|---|---|---|
| A query was inferred from retrieved evidence rather than handled distinctly | Separate `USER QUERY`, `VALIDATED TELEMETRY`, `HISTORY`, `MATRIX` in the reasoning contract | Repeat a question-answering evaluation across varied retrieved matrices |
| Too-specific instruction text distorted local reasoning | Reduce directive complexity and move definitions into payload structure | Controlled prompt comparisons with frozen inputs |
| Runtime reasoning appeared stalled | Debugging traced a `NameError` and a missing traceback import, not confirmed lock deadlock | Automated exception/recovery test for current code revision |
| Execution authority could not be uniquely specified by election epoch | Add an execution-sequence identifier | Replay/stale trigger and concurrent dispatch tests |
| D/E/F records were not all persisted through node-local memory layer mappings | Extend `MemoryLattice` role-specific storage handling | Restart/replay and complete data-lineage validation |
| Historical reasoning outputs required recovery after a persistence gap | Recover documented outputs and inspect NODE_F memory behavior | New-run persistence test: inference → durable write → process restart → retrieval |
| Validator copies accumulated redundant content | Deduplication audit and corrective handling | Subsequent bounded scan should preserve content integrity without new duplicates |
| Repeated vault scanning triggered duplicate bridge processing | Seed 182-path content-hash manifest; gate `UNCHANGED` | Run the exact outstanding changed-only test: unchanged/new/modified paths |
| Large reasoning queue drove many asynchronous tasks | Serialize Ollama inference with a reasoning lock | Bounded-load tests to distinguish transient backlog from runaway task accumulation |

### No causation without controls

The original documents also note a gap between implemented routing logic and demonstrated behavior. The [architecture invariant audit](../architecture/architecture_invariant_audit.md) remains the authoritative source for which properties are merely implemented, observed, reproduced, or validated.
