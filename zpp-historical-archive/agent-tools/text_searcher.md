## Text Searcher

> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: text_searcher
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

```python

#!/usr/bin/env python3
"""
text_searcher.py
ZPP Phase 5 Local Agent Tool - Deep Content Grep Engine (Unique Receipts)
"""

import os
import sys
import json
from datetime import datetime, timezone

def search_vault_text(keyword: str, root_path: str) -> str:
    print(f"📡 Text Search Tool initiated. Scanning for string: '{keyword}'")
    
    if not os.path.exists(root_path):
        return f"Error: Vault path '{root_path}' does not exist."
        
    search_results = {
        "query": keyword,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "total_matches": 0,
        "matches": []
    }
    
    searchable_extensions = {'.txt', '.md', '.json', '.log', '.csv', '.py'}
    
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in {".git", "venv", "__pycache__", "sandbox"} and not d.startswith('.')]
        
        for file in files:
            if os.path.splitext(file)[1].lower() in searchable_extensions:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if keyword.lower() in line.lower():
                                search_results["matches"].append({
                                    "file": file,
                                    "path": relative_path,
                                    "line": line_num,
                                    "content": line.strip()
                                })
                                search_results["total_matches"] += 1
                except:
                    continue

    # Clean the keyword so it's safe to use as a filename (removes spaces/special characters)
    safe_keyword = "".join([c if c.isalnum() else "-" for c in keyword]).strip("-")
    if not safe_keyword:
        safe_keyword = "query"
        
    # Generate a unique filename using the term and current timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    filename = f"text-search-{safe_keyword}-{timestamp}.md"
    report_path = os.path.join("/Users/<LOCAL_USER>/vault/sandbox", filename)
    
    md_content = [
        f"# Local Agent Text Search Query Results",
        f"**Search Target String:** `{keyword}`",
        f"**Executed UTC:** {search_results['timestamp_utc']}",
        f"**Total Document Matches:** {search_results['total_matches']}\n",
        "---",
        "## 🔍 Match Log Summary\n"
    ]
    
    if search_results["total_matches"] == 0:
        md_content.append(f"*No instances of the phrase '{keyword}' were located.*")
    else:
        for item in search_results["matches"]:
            md_content.append(f"### 📄 `{item['path']}` (Line {item['line']})")
            md_content.append(f"> {item['content']}\n")
            
    with open(report_path, "w") as f:
        f.write("\n".join(md_content))
        
    return f"Search complete. Found {search_results['total_matches']} occurrences. Details dumped to sandbox/{filename}"

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Phase 5"
    search_vault_text(query, "/Users/<LOCAL_USER>/vault")

```