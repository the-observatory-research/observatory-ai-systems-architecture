# Open validation program — not executed in this publication package

The archived [Architecture Invariant Audit](architecture_invariant_audit.md), Section 21, defines seven required tests. The original audit remained open. The following is a **faithful navigation summary**, not a claim that these tests were run after the documented snapshot.

| Test | Purpose | Historical pass condition or required work | Package status |
|---|---|---|---|
| A — Source fidelity | Preserve the original source through retrieval and broadcast | Source, retrieved and broadcast hashes match | Not rerun |
| B — Changed-only ingestion | Test seeded NODE_E manifest | Unchanged vault yields no new validations/reasoning; one edited/new file yields one relevant processing path | **Named next test — not rerun** |
| C — Persistence across restart | Full shutdown and restart | Databases, reasoning, manifest and pulses recover without manual reconstruction | Not rerun |
| D — Signed transport tamper test | Verify integrity enforcement | Signed payload accepted; modified signed payload rejected with no state mutation | Not rerun |
| E — Differentiated convergence | Validate measurements without forced node uniformity | Equivalent canonical source yields consistent required measurements across distinct nodes | Not rerun |
| F — Reasoning persistence | Test NODE_F output capture | Each completed reasoning stream is automatically persisted in its database | Not rerun |
| G — Failure isolation | Test partial failures | Define separate pass criteria before disconnecting NODE_B, restarting NODE_E or interrupting NODE_F | Not rerun |

Additional open runtime questions in `multi_agent_runtime_observations.md` concern queue dynamics, fluid-weight stability, state sampling resolution, exactly-once change handling, and potential batching of large source updates.

## Safe next validation boundary

The original audit specifically named **NODE_E changed-only ingestion with a seeded 182-path manifest** as its next checkpoint. Before executing it again, use a deliberately small synthetic vault, new local keys, scratch SQLite stores, and a bounded Ollama workload. Do not expose a private archive, original credentials, private keys, or recovered conversation databases merely to reproduce a historical run.

Results of future tests should be added as newly dated evidence files with commands, environment descriptions, source hashes, observed outputs, and failure classifications. Do **not** modify the original four Markdown records in place to retrofit future findings.
