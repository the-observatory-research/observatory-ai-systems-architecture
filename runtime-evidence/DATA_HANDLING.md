# Publication Safety and Data Handling

The original `node.zip` is **not publication-safe**. Its contents include private Ed25519 keys, a `.env` file, node-local SQLite databases, raw operational JSONL ledgers, an absolute-path content manifest, a virtual environment, and cached/runtime artifacts.

This release intentionally excludes:

- private or public key material and credentials;
- original database files and any copied/exported rows;
- raw vault paths, usernames, filenames, source text, and prompt/response content;
- original operational ledgers and full content-hash manifest;
- terminal transcripts, raw model output and potentially private conversational data;
- virtual environments, caches and local-specific configuration.

The provided `snapshot/aggregate_counts.json` contains only node identifiers, fixed table names, totals, and explanatory limitations. Path strings are **never** serialized by the inspection script. Source archive SHA-256 fingerprints are included in [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md) to support local verification without redistributing those archives.

**Operational security:** If the private keys in the original package have been used on any reachable network or distributed to others, treat them as exposed and rotate them before any further active deployment. If a GitHub repository ever received raw secrets in an earlier commit, removing them in a later commit does not remove them from Git history.
