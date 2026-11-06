# Framework — ZPP Six-Node Mesh (Development Snapshot)

This folder contains a **publication-reviewed source snapshot** of the six-node Zero-Point Protocol (ZPP) experimental framework from the uploaded `node.zip`. It is an implementation archive **under validation**, not a claim of production readiness, a complete reproducible distribution, or a current live deployment.

**The active mesh launcher in the supplied source snapshot is `node/boot_mesh.sh`.** The retired `start_mesh.py` (an older transport simulator that referred to a missing `transport_sim.py`) is intentionally not published as the current launcher.

The sibling repository folder `engine-archive/` preserves earlier standalone engine work; those historical engines should **not** be interpreted as current mesh dependencies.

## Implementation map

| Node(s) | Role documented in this snapshot |
|---|---|
| NODE_A, NODE_B, NODE_C | Independent validation / Gamma scoring; fluid weighting and elected dispatch |
| NODE_D | Local vault discovery and signed source handoff |
| NODE_E | Physical source retrieval, hashing, change classification, and validator bridge |
| NODE_F | Internet ingress and local reasoning via Ollama / DeepSeek-R1 |

The modules `node/agent_node.py`, `node/crypto.py`, `node/memory.py`, `node/scoring.py` and `node/pulse.py` implement key mesh functionality. The source also includes monitoring, injection, recovery, migration, and exploratory scripts. Those ancillary files are included for provenance; their compatibility with this exact runtime revision has **not** been demonstrated.

### Source layout

- [`node/`](node/) — retained source-file layout, including the Bash launcher and `config.json` snapshot.
- [`STATUS_AND_LIMITATIONS.md`](STATUS_AND_LIMITATIONS.md) — documented evidence, open checks and security qualifications.
- [`SOURCE_AND_REDACTIONS.md`](SOURCE_AND_REDACTIONS.md) — input snapshot and three explicit privacy edits.
- [`requirements.txt`](requirements.txt) — *inferred* third-party imports (not a frozen lockfile).
- [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json) and [`SHA256SUMS.txt`](SHA256SUMS.txt) — per-file source and published-copy hashes.

## Local review and execution (not an end-to-end-tested recipe)

The framework was developed for macOS with the Terminal GUI, Python and local Ollama. `boot_mesh.sh` uses AppleScript to open six Terminal processes on ports **8000–8005**. Do not run it on an untrusted network or against a private vault before reviewing the code and operational boundaries.

```bash
cd framework/node
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r ../requirements.txt
# Review settings, prepare a safe local test environment and run Ollama first.
bash boot_mesh.sh
```

This is the intended historical launch sequence, **not** a promise that the preserved revision will boot unmodified on another computer. The original environment included user-local state, keys, and platform-specific dependencies that are intentionally absent here. Private Ed25519 keys should be generated *locally*, never committed.

The original `config.json` has been retained as an **unaltered historical configuration snapshot**; its role labels and other settings are not guaranteed to agree with the later executable node roles. Check configuration before using it.

## Research status

The original architecture documentation describes prior runtime observations (e.g., local reasoning serialization and multi-node persistence), while the subsequent invariant audit remains open. Newly publishing these Python files does **not** constitute a new multi-node run or a completed invariant audit. See `STATUS_AND_LIMITATIONS.md`.

This folder intentionally does not include an open-source license. Publication rights and third-party dependencies should be reviewed before assigning one.
