## Appendix B - Cryptographic Key Specifications

zpp_id: appendix-b-cryptographic-key-specifications
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: ✅ VERIFIED
timestamp: 2026-05

---

### B.1 Algorithm Selection

| Parameter      | Value    |
| -------------- | -------- |
| Algorithm      | Ed25519  |
| Key length     | 256 bits |
| Signature size | 64 bytes |
| Security level | 128 bits |
| Deterministic  | Yes      |

---
### B.2 Canonical JSON Serialization

| Rule           | Specification                             |
| -------------- | ----------------------------------------- |
| Key ordering   | Alphabetical (`sort_keys=True`)           |
| Whitespace     | No extra spaces (`separators=(',', ':')`) |
| Encoding       | UTF-8                                     |
| Numbers        | Integers only (basis points)              |
| Schema version | `"schema_version": "zpp.event.v1"`        |

Floats are converted to basis points (multiply by 10,000) to ensure integer representation.

---
### B.3 Signature Payload Structure

```python
payload = {
    "schema_version": "zpp.event.v1",
    "timestamp_iso": "2026-05-20T12:34:56.789Z",
    "final_score_bp": 6413,
    "alpha_bp": 5350,
    "gamma_bp": 6400,
    "assigned_route": "GAMMA",
    "prompt_hash": hashlib.sha256(prompt_text.encode()).hexdigest(),
    "anchor_id": "threat_vector_1716234567"
}
```

---
### B.4 Verification Requirements

| Requirement              | Enforcement                     |
| ------------------------ | ------------------------------- |
| Signature valid          | `verify_payload()` returns True |
| Timestamp within window  | ±5 minutes (configurable)       |
| Prompt hash matches      | Prevents payload substitution   |
| Peer key in trust circle | Rejected if unknown             |
