>[!NOTE] Prototype Lineage — Decomposition Phase  
This component was created during Horizon's **Decomposition Phase**, when broader architectural principles were deliberately isolated into individual engines to observe and test specific behaviors in isolation.
>
This engine was a prototype of a **function**, not a declaration that reasoning requires a permanent, centralized control layer. IIts architectural purpose was to make a specific question observable: _Can this property be measured, verified, preserved, or corrected independently?_
>
Initial testing indicated the prototype performed its intended function. However, because the original test data was not permanently preserved, this component is retained as a tested historical implementation rather than a currently validated runtime requirement.
>
The current multi-agent architecture does not assume that reasoning requires passage through a fixed sequence of specialized engines, evaluators, gates, or centralized control components in order to proceed. The Horizon prototypes isolated these functions so they could be observed and tested independently; their existence did not establish that the functions must remain permanently separated or universally applied. Where the underlying principles remain useful, they may be expressed through native capability, distributed observation, evidence, persistent state, deterministic verification where applicable, or lateral interaction among independent agents—without introducing an authority merely to grant reasoning permission.
>
**The architecture observes where observation is useful. It verifies where verification is possible. It does not create an authority merely so reasoning can ask permission to proceed.**
>
See: [[horizon_decomposition_phase]]

---

zpp_id: memory_exceptions_py
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
document_state: `HISTORICAL_LOCKED`
architectural_status: `PROTOTYPE_IMPLEMENTATION`
timestamp: 2026-07-15

---

```python
class MemoryRepositoryError(Exception):
    """Base exception for Memory Lattice persistence failures."""


class MemoryRecordNotFoundError(MemoryRepositoryError):
    """Raised when a requested memory record does not exist."""


class DuplicateMemoryRecordError(MemoryRepositoryError):
    """Raised when an anchor or event ID already exists."""


class MemoryIntegrityError(MemoryRepositoryError):
    """Raised when a write would violate lattice integrity."""


class MemoryTransactionError(MemoryRepositoryError):
    """Raised when a database transaction fails."""


class InvalidMemoryTransitionError(MemoryRepositoryError):
    """Raised when a governance transition is not permitted."""
```