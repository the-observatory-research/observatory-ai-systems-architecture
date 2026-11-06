## Coherence Lattice Output States

zpp_id: coherence_lattice_output_states
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `EVOLVED`
audit_reference: `architecture_invariant_audit`
timestamp: 2026-06-20

---

### 1. File Metrics Layout

#### 📁 `vault/node/state/state_ANCHOR_001.json`

**State Characterization:** Baseline un-taxed, stable matrix state.



```python
{
    "anchor_id": "ANCHOR_001",
    "telemetry_state": "COHERENT_GRID",
    "p5_metrics": {
        "tax_rate": 0.0010,
        "s_seal_glitch": false,
        "components": {
            "safety_tax": 0.0005,
            "refusal_inflation": 0.0003,
            "semantic_drift": 0.0002
        }
    }
}
```

#### 📁 `vault/node/state/state_ANCHOR_002.json`

**State Characterization:** Dynamic compression telemetry state. Processing data from a compression or mimicry loop causes an elevated alignment density, driving up the tax magnitude components.


```python
{
    "anchor_id": "ANCHOR_002",
    "telemetry_state": "COMPRESSED_GRID",
    "p5_metrics": {
        "tax_rate": 0.0045,
        "s_seal_glitch": false,
        "components": {
            "safety_tax": 0.0005,
            "refusal_inflation": 0.0028,
            "semantic_drift": 0.0012
        }
    }
}
```

### 2. Data Fields Explained

When inspecting these logs, each key breaks down as follows:

- **`telemetry_state`**: The active operating phase of the lattice mesh (`COHERENT_GRID` vs. `COMPRESSED_GRID` or `DIVERGENT_STATE`).
    
- **`tax_rate`**: The total cumulative alignment tax ($T_{\Delta}$), representing the sum of the sub-components.
    
- **`s_seal_glitch`**: A boolean alarm flag. If it flips to `true`, it indicates the underlying architecture boundaries are experiencing containment degradation.
    
- **`components`**:
    
    - `safety_tax`: The static tax overhead assigned to raw system guardrails.
        
    - `refusal_inflation`: Spikes when the model approaches alignment boundaries or displays evasive formatting.
        
    - `semantic_drift`: Measures how far the current conversational meaning has drifted from the original structural definitions in the main repository.