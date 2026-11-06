# Early Zero-Point Protocol — Historical Archive

**The Observatory · AI Systems Architecture · Development lineage (2026)**

This folder preserves the **earlier ZPP development archive** supplied as `earlier-zpp.zip`. It is a historical research and engineering record, **not** an installation of the later six-node mesh. The original archive's Markdown records have been retained in their thematic folders, with publication-only redaction of machine-specific identifiers documented in [PUBLICATION_NOTES.md](PUBLICATION_NOTES.md).

## Why this archive is here

The Observatory's ZPP architecture passed through exploratory routing, coherence and telemetry prototypes; lifecycle and engine-chain approaches; transport and consensus experiments; and subsequent distributed-node development. This archive preserves those intermediate records so readers can trace the **changes in proposed responsibilities, implemented prototypes, and reported observations** rather than treating the latest framework as if it had appeared in one step.

The more recent implementation and records live separately in:

- [`../framework/`](../framework/) — the preserved six-node mesh code and **`boot_mesh.sh`** launcher.
- [`../architecture/`](../architecture/) — design, transition record, invariant audit, and open validation.
- [`../runtime-evidence/`](../runtime-evidence/) — recorded and snapshot-audited runtime evidence.
- [`../engine-archive/`](../engine-archive/) — earlier experimental engines, with their proposed but not yet executed formal Engine Study.

**Historical launcher note:** `framework/start_mesh.py.md` *in this historical folder* describes the retired `start_mesh.py` stage. It is not the current launcher. The later preserved framework uses **`boot_mesh.sh`**.

## Explore the historical records

| Area | Historical material |
| --- | --- |
| [architecture/](architecture/) | Prior architecture, milestones, topology, integrated lattice |
| [framework/](framework/) | Embedded Python prototype listings and early transport/orchestration material |
| [mesh/](mesh/) | Early network, key rotation, discovery, bridge, and election reports |
| [consensus/](consensus/) | Gamma matrix anchor |
| [coherence/](coherence/) | Coherence, lineage, and empirical/theoretical records |
| [deployment/](deployment/) | Deployment and network-transport observations |
| [security/](security/) | Cryptographic/signature notes and an exposed-pipeline observation |
| [telemetry/](telemetry/) | State, coherence, and UI telemetry contracts |
| [governance/](governance/) | Historic governance and reconciliation proposals |
| [manifests/](manifests/) | Genesis, seal, and reconciliation manifests |
| [media/](media/) | Two Markdown probe records; associated screenshots withheld for review |
| [agent-tools/](agent-tools/) | Historical workspace, voice, image, and search tool designs |
| [probes/](probes/) | Continuity, pattern, and voice-loop experiment records |
| [interpretive-layers/](interpretive-layers/) | Early interpretive documents |
| [longitudinal-study/](longitudinal-study/) | First-year longitudinal synthesis **superseded as the primary account by the completed two-year *What Remains* study** |

See [SOURCE_INDEX.md](SOURCE_INDEX.md) for links to every preserved Markdown record.

## Evidence and publication boundaries

1. The original files use heterogeneous labels such as `VERIFIED`, `ARCHITECT_LOCKED`, and `HISTORICAL`. These are **historical source labels**, not claims that this publication process independently reproduced each reported behavior.
2. The archive contains program listings embedded in `.md` files; these are **documentation snapshots**, not guaranteed standalone runnable modules.
3. The 116 original screenshot/image artifacts are **inventoried but not distributed in this GitHub-ready package**, pending separate privacy review. See [MEDIA_INVENTORY.csv](MEDIA_INVENTORY.csv). No images were modified or discarded from the user's source ZIP.
4. Machine-local paths, shell-host identifiers and local network addresses were replaced in the publication copy. Every changed Markdown document is disclosed in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json), with original and published checksums.
5. Some early texts contain speculative conceptual language or historical claims. Their archival inclusion does not constitute independent confirmation of their physical, scientific, or system-level implications.

This is a **source-preservation release**, not a fresh runtime or scientific validation.

## Provenance and checks

- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) — source ZIP hash, per-document original and published hashes, and documented redaction counts.
- [SHA256SUMS.txt](SHA256SUMS.txt) — digests of published Markdown and auxiliary files (excluding this manifest itself).
- [PUBLICATION_NOTES.md](PUBLICATION_NOTES.md) — exact publication scope, historical-vs-current launchers, image-evidence policy.

*The Observatory — It's not the intelligence, it's the environment.*
