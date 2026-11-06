> [!warning]
> The core concepts in this document remain relevant, but the runtime
> architecture has evolved into the six-node multi-agent mesh.
> D/F roles and routing matrix have changed substantially.
> For current topology and execution behavior, see:
> `current_multi_agent_architecture.md`.

---
## Context-Aware Edge Bridge & Routing Matrix Integration

zpp_id: edge_bridge_routing_matrix_integration
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
status: 🗄️ `ROLE MAP RETIRED`
origin_node: cluster_core
timestamp: 2026-06-30

---

### 1. Architectural Routing Specification

The perimeter transport topology of the Zero-Point Protocol has been systematically hardened through the implementation of an explicit, multi-tenant decoupling matrix. Rather than relying on hardcoded network boundary checks, `NODE_D` (Internal Mesh Bridge) and `NODE_F` (Edge External Gateway) now dynamically look up target destinations using a data-driven configuration map. This architecture enforces strict network isolation: external payloads are strictly funneled through designated security choke-points, ensuring the core consensus layer (`NODE_A`, `NODE_B`, `NODE_C`) remains isolated from unauthenticated edge traffic.

### 2. Context-Aware Routing Table Map

The global configuration framework has been updated with explicit path matrices defined by node identity and transaction intention (`anchor_id`):

|**Node ID**|**Identity Role**|**Transaction Context (anchor_id)**|**Target Routing Path Matrix**|
|---|---|---|---|
|**`NODE_D`**|Internal Mesh Bridge|`KEY_ROTATION`|`["NODE_A", "NODE_B", "NODE_C", "NODE_E"]`|
|**`NODE_D`**|Internal Mesh Bridge|`MANUAL_PROPOSAL_001`|`["NODE_A", "NODE_B", "NODE_C"]`|
|**`NODE_D`**|Internal Mesh Bridge|`DEFAULT`|`["NODE_A", "NODE_B", "NODE_C"]`|
|**`NODE_F`**|Edge External Gateway|`KEY_ROTATION`|`["NODE_D", "NODE_E"]`|
|**`NODE_F`**|Edge External Gateway|`DEFAULT`|`["NODE_D"]`|

### 3. Core Architectural Adjustments

The `IngressGatewayHandler` object has been overhauled to eliminate standard loopback broadcast leaks:

- **Decoupled Lookups:** The engine extracts the incoming `anchor_id` and queries the localized `BRIDGE_ROUTING_TABLE` map dynamically.
    
- **Fallback Mechanisms:** If an undocumented or arbitrary `anchor_id` hits the gateway, the router gracefully defaults to its secure path configuration (`"DEFAULT"`), preventing traffic drops.
    
- **Self-Filtering Logic:** Broadcasters automatically filter out their own identities from the target peer list during serialization, preventing local descriptor loops.