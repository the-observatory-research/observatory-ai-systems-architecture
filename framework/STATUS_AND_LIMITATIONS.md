# Framework implementation status and open questions

**Classification:** historical implementation snapshot of a partially completed framework transition. **Validation status:** static syntax and publication-package checks only (for this GitHub export). Historical empirical observations are recorded in the separately supplied `active.zip` documentation.

## Present in the source snapshot

- Six-node `agent_node.py` roles, signed WebSocket envelope processing and Ed25519 identity infrastructure.
- Validator Gamma scoring, changeable cluster weights and elected execution triggering.
- Node-local SQLite memory and state-aware asynchronous pulse functionality.
- NODE_D discovery, NODE_E retrieval/change tracking, NODE_F external ingress and local Ollama reasoning.
- Mac-specific `boot_mesh.sh` that starts the six nodes through Terminal; it supersedes `start_mesh.py`.
- Maintenance and reporting utilities whose compatibility has not been independently checked.

The existence of code is **not** evidence that every mechanism was independently verified in this version.

## Open engineering and security checks

1. Complete the original invariant audit, including changed-only ingestion verification against the seeded source manifest. The original data manifest was intentionally excluded to avoid publishing private source paths.
2. Confirm that each `origin_node_id` is authenticated against a trusted, pinned public-key registry. A valid signature against a public key **supplied by the sender** alone does not prove authorized node identity.
3. Test duplicate/stale execution trigger handling, epoch and sequence behavior, and cross-node restart/replay safety.
4. Revalidate source-path containment: discovery, retrieval and vault scanning read local files; restrict to explicit test directories before use.
5. Revalidate local persistence, queue draining, shutdown and recovery on clean test databases.
6. Confirm dependency versions, macOS/Python compatibility, setup steps, local model availability and full six-node startup.
7. Review the historical `config.json` role labels/settings for consistency with current code. Do not assume the file is an authoritative configuration for all modules.
8. Classify ancillary scripts such as `router.py` and `rest_api.py` before treating them as supported entry points.

## What was excluded

Raw state databases, logs, reasoning transcripts, deduplication manifests, stored source paths, `.env` files, private and public key files, embedded virtual environments, pre-installed vendor packages, compiled bytecode, and macOS metadata are **not** in the upload package.

Do not commit test secrets, local API tokens, real vault content, generated keypairs or runtime files. Because the source ZIP includes an `.env` with cloud-provider credential fields, check the token's current validity and rotate it if there is any concern it was disclosed elsewhere; it is **not** present in this export.

## Source-integrity disclaimer

Only three hard-coded personal paths in Python files were modified for publication. All other included source files are copied verbatim. The published copies are original research code except for those documented redactions; no production-hardening fixes have been silently applied.
