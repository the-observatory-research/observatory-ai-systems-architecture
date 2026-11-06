# Source and publication record

- **Source supplied by research author:** `node.zip` (uploaded framework snapshot).
- **Original ZIP SHA-256:** `5e191a9f4e1da14c8f2b51afb1e9cefefdab002619ee5f119cbbd61511722d1e`
- **Companion descriptive records:** `active.zip` (not included here; may be published later in `architecture/` and/or `runtime-evidence/`).
- **Companion ZIP SHA-256:** `08019239112326ec8c637e2a8708cbbe597e6f3d1f401805a90749e6f0745c7e`
- **Publication preparation:** 2026-11-06.

## Verbatim files and modifications

All included source files from `node.zip` are copied byte-for-byte **except** the following three privacy/portability edits:

1. `node/agent_node.py`: removed a hard-coded `/Users/...` default vault path and replaced it with `./vault`.
2. `node/inject_vault.py`: removed a hard-coded `/Users/...` default vault path and replaced it with `./vault`.
3. `node/router.py`: removed a hard-coded `/Users/...` ingress-log path and replaced it with `os.getenv("ZPP_INGRESS_LOG_DIRECTORY", "./logs/ingress")`.

Original SHA-256 and published SHA-256 digests for all source files appear in `SOURCE_MANIFEST.json`. Source originals are intentionally **not duplicated** in this public export because they contain personal filesystem paths; the researcher should retain the original input ZIP privately.

## Not included in this folder

- `start_mesh.py` (retired launch path; it requires an absent `transport_sim.py`).
- The complete `node/.env`, all `node/keys/` files, databases, original vault reasoning text, logs, state, generated manifests, vendor packages, virtual environments and macOS resource forks.

The original supplied ZIP has not been edited or overwritten.

## Important provenance distinction

The `active.zip` documents were written during development, and not every line is necessarily synchronized with the specific `node.zip` code revision. This package does not claim those documents were generated from these exact source-file hashes.
