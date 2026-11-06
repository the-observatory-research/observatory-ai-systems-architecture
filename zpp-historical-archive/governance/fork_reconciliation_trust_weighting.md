## ZPP - Fork Reconciliation & Trust Weighting Logic

zpp_id: fork_reconciliation_trust_weighting
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🗄️ `HISTORICAL_GOVERNANCE`
timestamp: 2026-06-08

---

### 1. Cryptographic Validation Gate

Before any proposal can be evaluated for consensus or network merging, it must pass through a strict cryptographic verification loop.

#### Verification Algorithm

When a packet arrives from an external peer port, the receiving node isolates the raw payload and computes a constant-time HMAC validation using the shared network configuration footprint:

$$
\text{Integrity State} = \begin{cases} 
\text{ACCEPT}, & \text{if } \text{HMAC}_{\text{calc}} \equiv \text{Signature}_{\text{incoming}} \\ 
\text{REJECT}, & \text{if } \text{HMAC}_{\text{calc}} \not\equiv \text{Signature}_{\text{incoming}} 
\end{cases}
$$

**Failure Action:** Any signature failure immediately triggers a `REJECT` state. The sender's temporary trust allocation is instantly dropped by 50%, and the data payload is sequestered into `/vault/quarantine/`.

---

### 2. Lineage Merge & Conflict Resolution

When two perfectly valid keys submit conflicting values for the threshold constants ($\alpha$, $\gamma$), the protocol defaults to **Trust Weighting Arbitration**.

#### Trust Weighting Formula

Every node maintains a local `trust_registry.json`. Reputation weights ($W$) dynamically recalculate based on signature accuracy and node uptime:

$$
W_{\text{peer}} = (\text{Uptime Ratio} \times 0.6) + (\text{Validation Record} \times 0.4)
$$

#### Supersession Rules

1. **Genesis Override:** Any proposal directly signed by the Genesis Developer Key (`NODE_A`) instantly overrides any competing peer fork, regardless of lineage length.

2. **Plurality Wins:** If no Genesis signature is present, the fork lineage possessing the higher cumulative trust weight ($\sum W$) is adopted as the new canonical mainline (`zpp-alpha-mainnet`). The losing branch is safely archived as a historical variant in `/vault/forks/`.

---
### Specification Summary

| Component                  | Formula / Rule                                                    |
| :------------------------- | :---------------------------------------------------------------- |
| **Integrity verification** | HMAC comparison → ACCEPT / REJECT                                 |
| **Failure penalty**        | 50% trust drop + quarantine                                       |
| **Trust weight formula**   | $W = (\text{Uptime} \times 0.6) + (\text{Validation} \times 0.4)$ |
| **Genesis override**       | `NODE_A` signature → automatic supersession                       |
| **Plurality rule**         | Higher $\sum W$ → canonical mainline                              |
