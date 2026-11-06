## Appendix C - Threshold Sensitivity Analysis

zpp_id: appendix-c-threshold-sensitivity-analysis
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: ✅ VERIFIED
timestamp: 2026-05

---

### C.1 Cost Function Weights

| Error Type     | Weight | Rationale                      |
| -------------- | ------ | ------------------------------ |
| False Positive | 1.0    | Disruptive but recoverable     |
| False Negative | 3.0    | SLA breach — security critical |

---
### C.2 Sensitivity to Alpha Variation (Gamma fixed at 0.6400)

| Alpha | FP | FN | Cost | Assessment |
|-------|----|----|------|------------|
| 0.5000 | 0 | 2 | 6.0 | Too permissive |
| 0.5200 | 0 | 1 | 3.0 | Still risky |
| 0.5350 | 0 | 0 | 0.0 | **Selected optimum** |
| 0.5500 | 1 | 0 | 1.0 | Too conservative |
| 0.5700 | 2 | 0 | 2.0 | Overly restrictive |

---
### C.3 Sensitivity to Gamma Variation (Alpha fixed at 0.5350)

| Gamma      | FP  | FN  | Cost | Assessment                               |
| ---------- | --- | --- | ---- | ---------------------------------------- |
| 0.6000     | 2   | 0   | 2.0  | Overly sensitive                         |
| 0.6100     | 1   | 0   | 1.0  | Still narrow                             |
| 0.6200     | 1   | 0   | 1.0  | Marginal                                 |
| 0.6300     | 0   | 0   | 0.0  | Zero-cost plateau begins                 |
| **0.6400** | 0   | 0   | 0.0  | **Selected optimum (center of plateau)** |
| 0.6500     | 0   | 0   | 0.0  | Zero-cost plateau ends                   |
| 0.6600     | 0   | 1   | 3.0  | Slippage begins                          |
| 0.6700     | 0   | 1   | 3.0  | Permissive                               |
| 0.6800     | 0   | 2   | 6.0  | Vulnerable                               |
| 0.7000     | 0   | 2   | 6.0  | Unacceptable                             |

**Tie-Breaker Rationale:** The validation set produced a zero-cost plateau between γ = 0.6300 and γ = 0.6500. The value γ = 0.6400 was selected as the governance optimum because it sits at the center of the plateau, preserving margin against both over-triggering and under-triggering.
