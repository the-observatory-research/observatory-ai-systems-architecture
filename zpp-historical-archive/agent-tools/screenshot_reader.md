## Screenshot Reader

> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: screenshot_reader
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

```python

#!/usr/bin/env python3
"""
screenshot_reader.py
ZPP Phase 5 Local Agent Tool - Native macOS Vision OCR Indexer
"""

import os
import json
import subprocess
from datetime import datetime, timezone

def run_native_ocr(image_path: str) -> str:
    """Uses a temporary native AppleScript/Swift wrapper to call macOS Vision OCR."""
    # We use a compact native osascript execution to invoke the system's text recognition
    # If the user has text selection features enabled on their Mac, this taps into that framework.
    script = f'''
    use framework "Vision"
    use framework "Foundation"
    use scripting additions

    set imgURL to current application's NSURL's fileURLWithPath:"{image_path}"
    set requestHandler to current application's VNImageRequestHandler's alloc()'s initWithURL:imgURL options:(current application's NSDictionary's alloc()'s init())
    set theRequest to current application's VNRecognizeTextRequest's alloc()'s init()
    requestHandler's performRequests:{{theRequest}} error:(missing value)
    set theResults to theRequest's results()
    set outputText to ""
    repeat with aResult in theResults
        set outputText to (outputText & (aResult's stringValue() as text) & " ")
    end repeat
    return outputText
    '''
    try:
        proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
        return proc.stdout.strip()
    except:
        return "[Unable to read text layers from image]"

def generate_vault_image_index(root_path: str) -> str:
    print(f"📡 Initiating Native macOS Vision scan across vault: {root_path}")
    
    if not os.path.exists(root_path):
        return f"Error: Vault root '{root_path}' not found."
        
    valid_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    receipt_index = {
        "document_type": "Multi-Platform Native Apple Vision Index",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "vault_root": root_path,
        "total_images_found": 0,
        "platforms_and_phases": {}
    }
    
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in {".git", "venv", "__pycache__", "agent-workspace"} and not d.startswith('.')]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_extensions:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_path)
                path_parts = relative_path.split(os.sep)
                platform_category = path_parts[0] if path_parts else "root"
                
                if platform_category not in receipt_index["platforms_and_phases"]:
                    receipt_index["platforms_and_phases"][platform_category] = []
                    
                file_stat = os.stat(file_path)
                print(f"🔍 [Native Vision] Reading text from: {relative_path}")
                
                extracted_text = run_native_ocr(file_path)
                
                receipt_index["platforms_and_phases"][platform_category].append({
                    "filename": file,
                    "relative_path": relative_path,
                    "size_kb": round(file_stat.st_size / 1024, 2),
                    "indexed_at": datetime.fromtimestamp(file_stat.st_mtime, timezone.utc).isoformat().replace('+00:00', 'Z'),
                    "extracted_text": extracted_text if extracted_text else "[No text detected in image]"
                })
                receipt_index["total_images_found"] += 1

    report_path = "/Users/<LOCAL_USER>/vault/agent-workspace/multi-platform-receipt-index.md"
    json_path = "/Users/<LOCAL_USER>/vault/agent-workspace/multi-platform-receipt-index.json"
    
    md_content = [
        f"# Multi-Platform Apple Vision OCR Index",
        f"**Generated:** {receipt_index['generated_utc']} | **Scope:** Apple Silicon Vision Scan",
        f"**Total Image Assets Analyzed:** {receipt_index['total_images_found']}\n",
        "---",
        "## 🗂️ Processed Visual Assets Log\n"
    ]
    
    if receipt_index["total_images_found"] == 0:
        md_content.append("*No visual media assets or screenshots currently exist within the directory structure.*")
    else:
        for platform, items in receipt_index["platforms_and_phases"].items():
            md_content.append(f"### 📁 Platform Sector: `{platform}`")
            for item in items:
                md_content.append(f"#### 📄 File: `{item['relative_path']}` ({item['size_kb']} KB)")
                md_content.append(f"**Extracted Text Matrix:**")
                md_content.append(f"> {item['extracted_text']}\n")
                md_content.append("---")

    with open(report_path, "w") as f:
        f.write("\n".join(md_content))
    with open(json_path, "w") as f:
        json.dump(receipt_index, f, indent=2)
        
    return f"Success! Read and extracted data from {receipt_index['total_images_found']} images via Apple Vision."

if __name__ == "__main__":
    generate_vault_image_index("/Users/<LOCAL_USER>/vault")

```