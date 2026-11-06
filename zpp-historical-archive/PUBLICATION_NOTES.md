# Publication notes — Early Zero-Point Protocol

## Scope

Source upload: `earlier-zpp.zip`  
Source archive SHA-256: `8c6271677a842c0fd42c21837fb69e43c06f95532bb171f5eb39fb76acbf18ab`  
Original source files: 201 (85 Markdown, 116 images), excluding directory and macOS resource-fork metadata entries.  
GitHub-ready release: **85 Markdown files**, plus the curated index, source manifest, media inventory, and integrity checks.

The original ZIP has not been modified. The publication package is a separate derivative and should **not** be mistaken for a bit-identical complete copy of the uploaded archive.

## Publication-only redactions

The Markdown documents were inspected for common high-risk credential patterns, email addresses, absolute local paths and machine identifiers. The source did not contain obvious embedded PEM private keys, GitHub tokens, AWS keys, or standard API credential tokens according to the automated patterns checked. This is **not a guarantee** of exhaustive secret detection.

- The original absolute local home directory prefix was replaced with `/Users/<LOCAL_USER>` in historical code listings and logs.
- Local shell username/hostname pairs were replaced with `<LOCAL_USER>@<LOCAL_HOST>` in terminal transcript fragments.
- The local LAN and gateway addresses were replaced with `<LOCAL_LAN_IP>` and `<LOCAL_GATEWAY>`.

These replacements are intended only to avoid exposing private machine details. They are deliberately **not** a claim that the historical listings are immediately executable on a new computer. Original and published SHA-256 digests and affected filenames are recorded in `SOURCE_MANIFEST.json`.

Redactions across this collection: {"local_account_path": 34, "local_gateway_address": 1, "local_lan_address": 6, "local_shell_prompt": 9}.

## Screenshot/image evidence

The source ZIP contains 116 `.png`/`.jpg` files, including model-conversation screenshots and terminal captures. Some may contain account avatars, browser details, conversation text, local device paths or other information requiring an explicit visual privacy and reuse review. These are **not included** in the public GitHub upload. They remain available in the unchanged source ZIP and are listed, by original relative path and checksum, in `MEDIA_INVENTORY.csv`.

No image contents have been independently verified as safe for unrestricted public distribution. Publish later only after manual review and any necessary redaction, with a corresponding evidence-source and edits record.

## Chronology and current-status boundary

The historical records are mostly dated May–July 2026. They include several stages of routing, transport, consensus, cryptographic simulation, state tracking, and early experimental interpretation. Do not interpret early `CURRENT`, `LOCKED`, `LIVE`, or `VERIFIED` labels as the status of the later distributed architecture. The historical launcher `start_mesh.py` was retired; the later framework snapshot uses `boot_mesh.sh`.

The first-year longitudinal-study documents are historical precursors and **do not reopen or replace** the completed five-part, 33-chapter *What Remains* study.

## Nature of the code

Files such as `framework/pipe_horizon_py.md`, `framework/transport_sim_py.md`, and `framework/historical-prototypes/*.md` are historical Markdown descriptions containing source listings. They are archived as documentation, not deployed or automatically executed. No runtime tests have been claimed for this publication package.

## Licensing

No new license is assigned to the archived source, model transcripts, or screenshots in this packaging step. Confirm rights and redistribution terms before choosing licenses for mixed research records and third-party outputs.
