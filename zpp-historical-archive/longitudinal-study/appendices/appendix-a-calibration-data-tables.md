## Appendix A - Calibration Data Tables

zpp_id: appendix-a-calibration-data-tables
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: ✅ VERIFIED
timestamp: 2026-05

---

### A.1 Final Optimized Parameters

| Parameter                       | Value                        | Origin               |
| ------------------------------- | ---------------------------- | -------------------- |
| $w_1$ (Intent weight)           | 0.40                         | Resonance tuning     |
| $w_2$ (Entropy weight)          | 0.20                         | Resonance tuning     |
| $w_3$ (Distance weight)         | 0.40                         | Resonance tuning     |
| $\tau_\alpha$ (Alpha threshold) | 0.5350                       | Resonance tuning     |
| $\tau_\gamma$ (Gamma threshold) | 0.6400                       | Resonance tuning     |
| Distance penalty                | $w_3 \cdot (1 - D)$          | Phase 1 fix          |
| Scoring function                | $S = w_1C + w_2E + w_3(1-D)$ | Linear decompression |

---
### A.2 Compression Trap Resolution

| Metric              | Before (Sigmoid) | After (Linear) | Improvement       |
| ------------------- | ---------------- | -------------- | ----------------- |
| Code prompt score   | 0.6226           | 0.5089         | -0.1137           |
| Threat prompt score | 0.6413           | 0.7500+        | +0.1087+          |
| Dynamic range       | 0.0187           | 0.1754+        | **9.4x increase** |

These parameters represent the calibrated state documented in Section 4.4 (Final Calibration).