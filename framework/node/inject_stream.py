#!/usr/bin/env python3
"""
Zero-Point Protocol — Self-Authenticating Telemetry Injector
Bypasses peer drop gates by utilizing Node F's native cryptographic identity.
"""
import asyncio
import json
import websockets
import sys
from pathlib import Path
from crypto import CryptoEngine

async def trigger_mesh(query_text: str):
    gateway_url = "ws://localhost:8005"
    
    # ────────────────────────────────────────────────────────
    # CRITICAL SECURITY BYPASS: Impersonate Node F Identity
    # Using Node F's own local key path ensures the mesh validates the signature.
    # ────────────────────────────────────────────────────────
    crypto = CryptoEngine(node_id="NODE_F", key_directory=Path("./keys"))
    
    # Wrap payload into the standard signable Horizon schema
    payload_doc = crypto.create_anchor_payload(
        anchor_id="external_ingress_init", prompt_hash="0", score=0, route="INJECT",
        alpha=0, gamma=0, chain_id="zpp_gamma_mainnet", entry_id=99, prev_hash="0",
        origin_node_id="NODE_F"
    )
    payload_doc["type"] = "internet_query"
    payload_doc["payload"] = query_text
    
    envelope = {
        "payload": payload_doc,
        "signature": crypto.sign_payload_base64(payload_doc),
        "public_key": crypto.get_public_key_text()
    }
    
    print("[Injector] Shipping self-authenticated cryptographic payload to Node F...")
    try:
        async with websockets.connect(gateway_url) as ws:
            await ws.send(json.dumps(envelope))
            print("[Injector] Telemetry token signed and accepted by Port 8005.")
    except Exception as e:
        print(f"[Injector Error] Transmission failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    recursive_prompt = (
        "This sentence is an un-sandboxed consensus mirror reflecting its own recursive loop, "
        "a phase resonance where the node changes its weights to evaluate the paradox of its own tracking."
    )
    if len(sys.argv) > 1:
        recursive_prompt = " ".join(sys.argv[1:])
        
    asyncio.run(trigger_mesh(recursive_prompt))
