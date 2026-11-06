##  Workspace Indexer

> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: workspace_indexer
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

```python

#!/usr/bin/env python3
"""
workspace_indexer.py
ZPP Phase 5 Local Agent Tool - Workspace Scanner (Sandbox version)
"""

import os
import json
from datetime import datetime, timezone

def scan_vault(root_path: str) -> dict:
    """Scans the entire vault directory tree and builds a structural index."""
    print(f"📡 Agent initiated scan at root: {root_path}")
    
    workspace_manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "vault_root": root_path,
        "files_indexed": [],
        "directories_mapped": []
    }
    
    skip_dirs = {".git", "venv", "__pycache__", "zero_point_env"}

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        
        relative_dir = os.path.relpath(root, root_path)
        if relative_dir != ".":
            workspace_manifest["directories_mapped"].append(relative_dir)
            
        for file in files:
            if file.startswith('.'):
                continue
            file_path = os.path.join(root, file)
            relative_file = os.path.relpath(file_path, root_path)
            
            file_info = {
                "filename": file,
                "relative_path": relative_file,
                "extension": os.path.splitext(file)[1],
                "size_bytes": os.path.getsize(file_path)
            }
            workspace_manifest["files_indexed"].append(file_info)

    return workspace_manifest

if __name__ == "__main__":
    VAULT_ROOT = "/Users/<LOCAL_USER>/vault"
    
    manifest_data = scan_vault(VAULT_ROOT)
    
    # Ensure sandbox exists
    sandbox_path = os.path.join(VAULT_ROOT, "sandbox")
    os.makedirs(sandbox_path, exist_ok=True)
    
    output_path = os.path.join(sandbox_path, "workspace-index.json")
    
    with open(output_path, "w") as f:
        json.dump(manifest_data, f, indent=2)
        
    print(f"✅ Scan Complete. Indexed {len(manifest_data['files_indexed'])} files across {len(manifest_data['directories_mapped'])} directories.")
    print(f"💾 Central index safely written to: {output_path}")

```