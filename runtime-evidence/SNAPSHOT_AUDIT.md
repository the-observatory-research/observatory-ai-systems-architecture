# Snapshot-Level Aggregate Inspection

The package was built from the *original user-supplied* `node.zip` and `active.zip`, not from synthetic log content. The original runtime databases and logs were inspected locally **without including their raw contents in GitHub**.

## Measurable snapshot results

| Measurement | Result |
|---|---:|
| Six per-node SQLite databases | 6 present; all readable |
| NODE_A/B/C conversation_history | 204 rows each |
| NODE_D/E conversation_history | 364 rows each |
| NODE_F conversation_history | 192 rows |
| NODE_A pulse_history | 12,029 rows |
| NODE_B–F pulse_history | 12,030 rows each |
| `lattice_state_ledger` in each database | 0 rows each |
| NODE_D discovery ledger | 608 JSONL entries; 182 distinct source paths |
| NODE_E bridge ledger | 608 JSONL entries; 182 distinct source paths |
| NODE_E content manifest | 182 entries |

The exact aggregate result is [machine-readable JSON](snapshot/aggregate_counts.json). The included [inspection script](tools/summarize_snapshot.py) can reproduce these aggregate counts from a locally supplied original archive. It does not need network access or a running mesh.

## Interpretive cautions

1. Historical logs and SQLite databases reflect *different record types and processing stages*. The 608 ledger entries, 364 NODE_E conversation rows, 182 distinct source paths and 181 historically reported reasoning streams **must not be equated**. Counts are not independent measures of completed inference.
2. The original runtime-observation report describes 181 recovered reasoning streams; this audit did **not** count or verify those original response transcripts. NODE_F's 192 `conversation_history` rows are not asserted to be 192 distinct reasoning streams.
3. The six `lattice_state_ledger` tables are empty in this snapshot. Other storage layers contain rows; this finding must not be flattened into either "all state lost" or "all state was preserved".
4. A populated content manifest is evidence of a seeded baseline, **not** a successful post-seeding changed-only validation. The source audit explicitly left that test open.
5. A read-only examination of an archive is not an executable end-to-end runtime test; no new validation of cryptographic trust, queue dynamics, replay protection, or fault isolation occurred.

## Reproduce safely

From the repository root, with the original **private** `node.zip` on your local computer:

```bash
python3 runtime-evidence/tools/summarize_snapshot.py /private/path/to/node.zip
```

The script prints counts only. Do **not** commit `node.zip`, the underlying databases, key files, raw logs, or its personal filesystem paths. If your Python version lacks SQLite `Connection.deserialize`, run Python 3.11+.
