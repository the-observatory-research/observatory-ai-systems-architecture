## ZPP - Cryptographic Engine

zpp_id: crypto_py 
schema_version: zpp.entropy.char.nfc.v1 
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05-20

---

```python
"""
Zero-Point Protocol — Cryptographic Engine 
Ed25519 signing, verification, and canonical JSON serialization.
"""

import hashlib
import json
from datetime import datetime, UTC
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature


class CryptoEngine:
    """
    Handles Ed25519 cryptographic signatures and canonical JSON serialization.
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self._private_key = ed25519.Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()

    def get_public_key_bytes(self) -> bytes:
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def sign_payload(self, payload: Dict[str, Any]) -> bytes:
        canonical = self._to_canonical_json(payload)
        return self._private_key.sign(canonical.encode('utf-8'))

    @staticmethod
    def verify_payload(payload: Dict[str, Any], signature: bytes, public_key_bytes: bytes) -> bool:
        try:
            pub_key = serialization.load_pem_public_key(public_key_bytes)
            canonical = CryptoEngine._to_canonical_json(payload)
            pub_key.verify(signature, canonical.encode('utf-8'))
            return True
        except (InvalidSignature, ValueError, TypeError):
            return False

    @staticmethod
    def _to_canonical_json(payload: Dict[str, Any]) -> str:
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=False
        )

    @staticmethod
    def hash_prompt(prompt_text: str) -> str:
        return hashlib.sha256(prompt_text.encode('utf-8')).hexdigest()

    @staticmethod
    def create_anchor_payload(
        anchor_id: str, prompt_hash: str, score: float, route: str,
        alpha: float, gamma: float, chain_id: str, entry_id: int, prev_hash: str
    ) -> Dict[str, Any]:
        return {
            "schema_version": "zpp.event.v1",
            "chain_id": chain_id,
            "entry_id": entry_id,
            "prev_hash": prev_hash,
            "anchor_id": anchor_id,
            "prompt_hash": prompt_hash,
            "score_bp": int(score * 10000),
            "alpha_bp": int(alpha * 10000),
            "gamma_bp": int(gamma * 10000),
            "assigned_route": route,
            "timestamp_iso": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        }
```

