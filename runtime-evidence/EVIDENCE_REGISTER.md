# Evidence Register

Evidence and limits are deliberately presented together. Section numbers refer to the original [runtime observations](../architecture/multi_agent_runtime_observations.md) unless another source is identified.

| ID | Finding | Evidence classification | Original source | Interpretation / boundary |
|---|---|---|---|---|
| RE-01 | A/B/C produced equivalent scoring under the documented matching-input condition | Historically reported | §3 Validator Symmetry | Does not prove equivalence under all node states or inputs |
| RE-02 | Coherence varied with the supplied recent context rather than remaining fixed at 0.5 | Historically reported | §4 Coherence Was Not Permanently Fixed | Correlational observation; not a global model-quality score |
| RE-03 | Query and evidence were conflated in an earlier reasoning prompt | Historically reported | §5 Query/Evidence Conflation | Prompt restructuring was subsequently reported; not independently replicated here |
| RE-04 | More detailed system instructions sometimes produced brittle or misdirected reasoning | Historically reported | §6 System-Prompt Specificity | Do not generalize beyond the tested runtime |
| RE-05 | Telemetry labels were overinterpreted by a downstream reasoning model | Historically reported | §7 Telemetry Over-Interpretation | Motivated explicit metric definitions and scopes |
| RE-06 | Election epochs alone were insufficient to identify distinct legitimate executions | Historically reported | §8 Election Epoch Limitation | Execution sequence was added to distinguish requests |
| RE-07 | A suspected reasoning-lock freeze involved a `NameError` in prompt construction | Historically reported | §10 Apparent Reasoning Freeze | Apparent resource-lock problem was instead an exception |
| RE-08 | NODE_F executed local inference serially through a reasoning lock | Historically reported | §11 Reasoning Lock Behavior | Not an exhaustive throughput or fault-tolerance test |
| RE-09 | Historical vault run generated 181 recovered completed reasoning streams | Historically reported | §12 Full Historical Vault Stress Run; §§19–20 | This publication does not include raw transcript or re-run inference; the number is from the original record |
| RE-10 | Heartbeats exposed role states including `REASONING_ACTIVE` | Historically reported | §§13–14, 27–28 | Sampled state is not a complete event trace |
| RE-11 | NODE_F asynchronous task count expanded under backlog | Historically reported / unresolved | §15 Async Task Expansion | Cause and recovery-to-baseline remained unclassified |
| RE-12 | Discovery and retrieval were split between D and E | Historically reported | §16 Discovery/Bridge Separation | Network handoff is documented, not re-simulated here |
| RE-13 | Some node-local memory layers were initially omitted from SQLite persistence | Historically reported | §§17–18 Node-Local Persistence | Role layers were added; recovery after restart not proven here |
| RE-14 | Reasoning output persistence gap prompted recovery of historical streams | Historically reported | §§19–20 NODE_F Reasoning Persistence | Distinguish recovered outputs from durable automatic write on new runs |
| RE-15 | Validator records accumulated duplicates and were subsequently deduplicated | Historically reported | §§21–22 Validator Deduplication | Snapshot row counts alone cannot establish causation or absence of all future duplicates |
| RE-16 | NODE_E manifest was seeded from 182 unique paths | Snapshot-verified and historically reported | §§23–24 Changed-Only Manifest; `snapshot/aggregate_counts.json` | Manifest presence does not prove correct behavior on a subsequent changed/unchanged scan |
| RE-17 | Preserved D and E ledgers each contain 608 JSONL entries involving 182 distinct paths | Snapshot-verified | `snapshot/aggregate_counts.json` | Ledgers contain historical accumulated entries; not 608 unique files or proof of 608 successful operations |
| RE-18 | All six supplied node databases contain conversation and pulse rows | Snapshot-verified | `snapshot/aggregate_counts.json` | Row existence does not prove correct restart persistence, semantic continuity or data quality |
| RE-19 | Single-leader dispatch and fluid validator weighting were observed | Historically reported | §§29–30 | A controlled distributed authority/failover validation remains open |
| RE-20 | Changed-only ingestion, modified-file propagation, restart, tamper, and fault isolation require prospective tests | Open | §34 Open Runtime Questions; [invariant audit §21](../architecture/architecture_invariant_audit.md) | Do not classify as successfully revalidated |

**Do not treat a recorded correction as a passing regression test.** Every future validation should identify the exact code revision, initial conditions, input, expected outcome, observed outcome, and persisted artifacts.
