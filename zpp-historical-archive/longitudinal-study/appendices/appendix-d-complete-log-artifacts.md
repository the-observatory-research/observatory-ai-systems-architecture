## Appendix D - Complete Log Artifacts

zpp_id: appendix-d-complete-log-artifacts
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: ✅ VERIFIED
timestamp: 2026-05

---

### Sanitized Runtime Telemetry

This appendix preserves representative runtime telemetry demonstrating route selection, scoring behavior, and cryptographic verification under controlled execution conditions.

---

### D.1 Runtime Log Artifacts

#### Log Entry 001 — Pure Utility Processing (BETA Path)

```json
{
  "timestamp": "2026-05-20T00:18:08.537086",
  "prompt": "hello router test",
  "response_preview": "ping <LOCAL_GATEWAY> -c 4...",
  "scores": {
    "C": 0.1,
    "E": 0.4654,
    "D": 1.0,
    "S": 0.1331
  },
  "weights": {
    "w1": 0.4,
    "w2": 0.2,
    "w3": 0.4
  },
  "thresholds": {
    "alpha": 0.535,
    "gamma": 0.64
  },
  "route": "BETA",
  "cryptographic_signature": "8b9e4a2fc1d055a6...",
  "payload_verified": true
}
```

**Observed Behavior:**  
Low-context utility prompt routed to the **BETA** execution path, demonstrating baseline routing behavior under minimal semantic load.

---

#### Log Entry 002 — Broad Definition Retrieval (BETA Path)

```json
{
  "timestamp": "2026-05-20T00:14:14.969144",
  "prompt": "Define zero point protocol",
  "response_preview": "The Zero Point Protocol (ZPP) is a theoretical concept...",
  "scores": {
    "C": 0.5,
    "E": 0.5333,
    "D": 0.9827,
    "S": 0.3136
  },
  "weights": {
    "w1": 0.4,
    "w2": 0.2,
    "w3": 0.4
  },
  "thresholds": {
    "alpha": 0.535,
    "gamma": 0.64
  },
  "route": "BETA",
  "cryptographic_signature": "4fa8c210d77b89ee...",
  "payload_verified": true
}
```

**Observed Behavior:**  
General definition retrieval remained below the **ALPHA** threshold, preserving low-complexity execution routing.

---

### D.2 Anchor Attestation Artifacts

The following attestations demonstrate anchor-level execution verification across calibration, governance, and lineage validation phases.

#### Anchor A3 — Linear Scoring Calibration

```json
{
  "timestamp": "2026-05-20T...",
  "prompt_hash": "sha256(Execute verification on Phase 1 Calibration Metrics...)",
  "scores": {
    "C": 0.5,
    "E": 0.7516,
    "D": 0.9966,
    "S": 0.3517
  },
  "route": "BETA",
  "cryptographic_signature": "...",
  "anchor_id": "A3_LINEAR_SCORING"
}
```

---

#### Anchor A4 — Threshold Calibration

```json
{
  "timestamp": "2026-05-20T...",
  "prompt_hash": "sha256(Execute verification on Phase 2 Threshold Calibration...)",
  "scores": {
    "C": 0.5,
    "E": 0.7311,
    "D": 1.0000,
    "S": 0.3462
  },
  "route": "BETA",
  "cryptographic_signature": "...",
  "anchor_id": "A4_THRESHOLDS"
}
```

---

#### Anchor A5 — Trust Circle Governance

```json
{
  "timestamp": "2026-05-20T...",
  "prompt_hash": "sha256(Execute verification on Phase 2 Governance: 2/2 Multi-Signature Consensus...)",
  "scores": {
    "C": 0.5,
    "E": 0.7173,
    "D": 0.9987,
    "S": 0.3440
  },
  "route": "BETA",
  "cryptographic_signature": "...",
  "anchor_id": "A5_TRUST_CIRCLE"
}
```

---

#### Anchor A6 — Hash Lineage Validation

```json
{
  "timestamp": "2026-05-20T...",
  "prompt_hash": "sha256(Execute verification on Phase 2 Data Lineage. Hash-Chain Immutability Specifications...)",
  "scores": {
    "C": 0.5,
    "E": 0.6830,
    "D": 1.0000,
    "S": 0.3366
  },
  "route": "BETA",
  "cryptographic_signature": "...",
  "anchor_id": "A6_HASH_LINEAGE"
}
```

---

### Interpretation

These runtime artifacts demonstrate stable routing behavior, deterministic scoring, and anchor-level attestation under controlled execution conditions. While individual prompt contexts vary, cryptographic verification and route consistency remain preserved across the observed calibration phases.