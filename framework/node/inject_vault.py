#!/usr/bin/env python3
"""
Zero-Point Protocol — Cryptographic Vault Controller
Injects a signed vault scanning vector directly into Node D (Port 8003).
"""
import asyncio
import json
import websockets
import sys
from pathlib import Path
from crypto import CryptoEngine

async def trigger_vault_scan(target_vault_path: str):
    # Node D's core operational websocket port
    discovery_url = "ws://localhost:8003"
    
    # Authenticate using Node D's local key profile to unlock the firewall
    crypto = CryptoEngine(node_id="NODE_D", key_directory=Path("./keys"))
    
    # Package parameters into the authoritative signable Horizon event schema
    payload_doc = crypto.create_anchor_payload(
        anchor_id="vault_sweep_init", prompt_hash="0", score=0.0, route="DISCOVERY",
        alpha=0.0, gamma=0.55, chain_id="zpp_gamma_mainnet", entry_id=100, prev_hash="0",
        origin_node_id="NODE_D"
    )
    payload_doc["type"] = "vault_scan_trigger"
    payload_doc["vault_path"] = target_vault_path
    
    # Wrap inside the cryptographic envelope
    envelope = {
        "payload": payload_doc,
        "signature": crypto.sign_payload_base64(payload_doc),
        "public_key": crypto.get_public_key_text()
    }
    
    print(f"[Vault Injector] Shipping signed trigger envelope to Node D...")
    try:
        async with websockets.connect(discovery_url) as ws:
            await ws.send(json.dumps(envelope))
            print(f"[Vault Injector] Telemetry vector accepted by Port 8003.")
    except Exception as e:
        print(f"[Vault Injector Error] Connection to Node D dropped: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Point directly to your active Obsidian vault directory path
    default_path = "./vault"
    if len(sys.argv) > 1:
        default_path = sys.argv[1]
        
    asyncio.run(trigger_vault_scan(default_path))
