# Architecture-to-implementation crosswalk

This table is a navigation aid for the **supplied September 2026 snapshots**. File presence is not evidence that a feature was successfully revalidated in a new environment.

| Architecture responsibility | Source record | Source code location (sibling `framework/`) | Evidence or open issue |
|---|---|---|---|
| Six-node execution and event handling | `current_multi_agent_architecture.md` | `../framework/node/agent_node.py` | Historical runtime observations; new integration run not performed |
| Signed transport / Ed25519 identity | `current_multi_agent_architecture.md` | `../framework/node/crypto.py`, `agent_node.py` | Verify trust-key binding and message rejection without state mutation; beyond signature cryptography alone |
| Validator scoring and fluid leader selection | `current_multi_agent_architecture.md` | `../framework/node/scoring.py`, `agent_node.py` | Independent validator scoring and singular dispatch documented; check convergence and leadership changes |
| Node-local persistence | `multi_agent_runtime_observations.md` | `../framework/node/memory.py` | Previously incomplete roles corrected; cold restart persistence remains a dedicated audit test |
| State-aware heartbeat | `current_multi_agent_architecture.md` | `../framework/node/pulse.py` | Role-specific pulse states historically observed; verify sampling during brief transitions |
| Vault discovery, bridge and changed-only ingestion | `architecture_invariant_audit.md` | `../framework/node/agent_node.py`, `seed_node_e_manifest.py` | **Next named validation:** NODE_E changed-only check against seeded 182-path manifest |
| Serialized local reasoning | `multi_agent_runtime_observations.md` | `../framework/node/agent_node.py` | Historical Ollama lock operation observed; reasoning persistence requires follow-up |
| Startup | `current_multi_agent_architecture.md` | **`../framework/node/boot_mesh.sh`** | Active launcher in the supplied implementation; retired `start_mesh.py` should not be used |

**Documented observations (not rerun for this package):** six SQLite node stores, independent validator results, leader-gated dispatch, 181 recovered reasoning streams, and the 182-path content-manifest seed are recorded in `multi_agent_runtime_observations.md`. Their inclusion here preserves the claim's original source; it is not a fresh performance benchmark.

**Architectural staging:** `engine-archive/` is not a runtime dependency of the six-node mesh. Earlier `orchestrator.py`, Pipe Horizon, and engine chains are part of development history, not an active execution sequence.

**Audit interpretation:** The invariant audit records provisional classifications. A provisionally *strengthened*, *preserved*, or *evolved* invariant is not necessarily *validated*.
