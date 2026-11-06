# Engine Archive — The Observatory

**Historical prototype-engine implementation records | Proposed engine study not yet executed**

This folder preserves the *Decomposition Phase* engine prototypes developed in the earlier Horizon / Pipe Horizon architecture. The original records were stored as Markdown, often with embedded Python source and test code. They are preserved here as **historical research artifacts**, not presented as currently active modules in the later six-node ZPP mesh.

## Index

| Engine / component | Archive folder | Preserved contents |
|---|---|---|
| Repair Engine | [`repair-engine/`](repair-engine/) | Implementation, technical notes, test source |
| Recursive Reasoner | [`recursion/recursive-reasoner/`](recursion/recursive-reasoner/) | Implementation and notes |
| Recursive Gatekeeper | [`recursion/recursive-gatekeeper/`](recursion/recursive-gatekeeper/) | Implementation and architecture notes; this earlier gatekeeper was not the persistent later runtime authority |
| TaskGuard | [`task-guard/`](task-guard/) | Implementation, notes, tests |
| Cycle Detector | [`cycle-detector/`](cycle-detector/) | Implementation, notes, tests |
| Coherence Engine | [`coherence-engine/`](coherence-engine/) | Implementation, notes, tests |
| Math Engine | [`math-engine/`](math-engine/) | Implementation, notes, tests |
| Memory Engine | [`memory-engine/`](memory-engine/) | Implementation, data model, policies, repository, schema, health, exceptions, tests |

## Architectural boundaries

- **Historical engines:** The engines were developed and tested as separable components during an earlier architectural phase. Their presence in this archive **does not mean** they all operated together simultaneously or are currently used in the six-node mesh.
- **Later multi-agent runtime:** The later mesh uses `agent_node.py` and its supporting node modules. Per the project owner, the active launcher is **`boot_mesh.sh`**; `start_mesh.py` is retired. Runtime code and this archive should remain distinct.
- **Engine study:** A systematic comparative engine study was planned but **was not completed**. See [`ENGINE_STUDY_NOT_STARTED.md`](ENGINE_STUDY_NOT_STARTED.md). Historical `test_*` documents are test *source*, not evidence that the proposed comparative study was carried out.

## Source treatment

- All source records are included as `.md` files in their original relative layout; they have not been converted to executable `.py` modules.
- macOS packaging artifacts (`__MACOSX`, `.DS_Store`, `._*`) were excluded.
- **One publication-only redaction** removes a user-specific absolute file path from `recursion/recursive-gatekeeper/gatekeeper_py.md`; this path will need configuration before code is executable. Other source `.md` contents are byte-for-byte preserved.
- See [`SOURCE_NOTES.md`](SOURCE_NOTES.md) for SHA-256 provenance; no model inference or runtime validation was performed as part of this packaging.

## Intended publication

This is a source archive for inspectability and later study. It is **not** a ready-to-run engine distribution or an assurance of runtime safety, compatibility, or security. Dependencies, fixtures, credentials, local filesystem paths and behavior must be audited before running or republishing executable versions.

No project-wide open-source license has been applied in this package; release licensing should be considered separately by the author.
