#!/usr/bin/env python3
"""
Zero-Point Protocol — Cryptographic Identity Engine

Provides:
- persistent Ed25519 node identity
- deterministic canonical JSON serialization
- payload signing and public-key verification
- public-key fingerprinting
- Base64 encoding for JSON transport
- explicit local key rotation

Private keys never leave this engine.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


_SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9_.-]+")


class CryptoEngine:
    """
    Persistent Ed25519 identity belonging to one runtime or mesh node.

    A model identifier such as model:ollama:deepseek-r1-7b should not
    normally own this key. The key belongs to the process/node sending
    the signed protocol event.
    """

    def __init__(
        self,
        node_id: str,
        key_directory: str | Path,
    ):
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("node_id must be a non-empty string")

        self.node_id = node_id.strip()
        self.key_directory = Path(key_directory).expanduser().resolve()
        self.key_directory.mkdir(parents=True, exist_ok=True)

        safe_node_id = _SAFE_FILENAME_PATTERN.sub("_", self.node_id)

        self._private_key_path = (
            self.key_directory / f"{safe_node_id}_private.pem"
        )
        self._public_key_path = (
            self.key_directory / f"{safe_node_id}_public.pem"
        )

        self._private_key = self._load_or_create_private_key()
        self._public_key = self._private_key.public_key()

        self._persist_public_key()

    @staticmethod
    def _to_canonical_json(payload: Mapping[str, Any]) -> str:
        """
        Produce deterministic JSON suitable for signing and hashing.

        NaN and Infinity are rejected because they are not portable
        protocol values.
        """
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")

        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )

    def _load_or_create_private_key(
        self,
    ) -> ed25519.Ed25519PrivateKey:
        if self._private_key_path.exists():
            key = serialization.load_pem_private_key(
                self._private_key_path.read_bytes(),
                password=None,
            )

            if not isinstance(
                key,
                ed25519.Ed25519PrivateKey,
            ):
                raise TypeError(
                    f"Stored key is not Ed25519: "
                    f"{self._private_key_path}"
                )

            return key

        key = ed25519.Ed25519PrivateKey.generate()

        private_bytes = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        self._write_private_key(private_bytes)
        return key

    def _write_private_key(self, private_bytes: bytes) -> None:
        temporary_path = self._private_key_path.with_suffix(".tmp")

        temporary_path.write_bytes(private_bytes)
        os.chmod(temporary_path, 0o600)
        temporary_path.replace(self._private_key_path)
        os.chmod(self._private_key_path, 0o600)

    def _persist_public_key(self) -> None:
        self._public_key_path.write_bytes(
            self.get_public_key_pem()
        )

        try:
            os.chmod(self._public_key_path, 0o644)
        except OSError:
            pass

    def get_public_key_pem(self) -> bytes:
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def get_public_key_text(self) -> str:
        return self.get_public_key_pem().decode("utf-8")

    def get_public_key_fingerprint(self) -> str:
        public_key_der = self._public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        digest = hashlib.sha256(public_key_der).hexdigest()
        return f"sha256:{digest}"

    def identity_document(self) -> Dict[str, str]:
        """
        Public identity information safe to announce over transport.
        """
        return {
            "node_id": self.node_id,
            "key_algorithm": "ed25519",
            "public_key_pem": self.get_public_key_text(),
            "public_key_fingerprint": self.get_public_key_fingerprint(),
        }

    def sign_payload(self, payload: Mapping[str, Any]) -> bytes:
        canonical = self._to_canonical_json(payload)
        return self._private_key.sign(canonical.encode("utf-8"))

    def sign_payload_base64(
        self,
        payload: Mapping[str, Any],
    ) -> str:
        signature = self.sign_payload(payload)

        return base64.b64encode(signature).decode("ascii")

    @classmethod
    def verify_payload(
        cls,
        payload: Mapping[str, Any],
        signature: bytes,
        public_key_pem: bytes,
    ) -> bool:
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem
            )

            if not isinstance(
                public_key,
                ed25519.Ed25519PublicKey,
            ):
                return False

            canonical = cls._to_canonical_json(payload)

            public_key.verify(
                signature,
                canonical.encode("utf-8"),
            )

            return True

        except (
            InvalidSignature,
            ValueError,
            TypeError,
        ):
            return False

    @classmethod
    def verify_payload_base64(
        cls,
        payload: Mapping[str, Any],
        signature_base64: str,
        public_key_pem: str | bytes,
    ) -> bool:
        try:
            signature = base64.b64decode(
                signature_base64,
                validate=True,
            )
        except (ValueError, TypeError):
            return False

        if isinstance(public_key_pem, str):
            public_key_bytes = public_key_pem.encode("utf-8")
        elif isinstance(public_key_pem, bytes):
            public_key_bytes = public_key_pem
        else:
            return False

        return cls.verify_payload(
            payload=payload,
            signature=signature,
            public_key_pem=public_key_bytes,
        )

    def rotate_keypair(self) -> Dict[str, str]:
        """
        Rotate this node's local keypair.

        Returns public rotation evidence only. The new private key
        remains local and is never placed inside a network payload.
        """
        previous_fingerprint = self.get_public_key_fingerprint()

        if self._private_key_path.exists():
            backup_path = self._private_key_path.with_suffix(
                ".previous.pem"
            )

            if backup_path.exists():
                backup_path.unlink()

            self._private_key_path.replace(backup_path)

        self._private_key = ed25519.Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()

        private_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        self._write_private_key(private_bytes)
        self._persist_public_key()

        return {
            "node_id": self.node_id,
            "algorithm": "ed25519",
            "previous_fingerprint": previous_fingerprint,
            "new_fingerprint": self.get_public_key_fingerprint(),
            "new_public_key_pem": self.get_public_key_text(),
            "rotated_at": (
                datetime.now(UTC)
                .isoformat()
                .replace("+00:00", "Z")
            ),
        }

    @staticmethod
    def hash_prompt(prompt_text: str) -> str:
        if not isinstance(prompt_text, str):
            raise TypeError("prompt_text must be a string")

        return hashlib.sha256(
            prompt_text.encode("utf-8")
        ).hexdigest()

    @classmethod
    def hash_payload(
        cls,
        payload: Mapping[str, Any],
    ) -> str:
        canonical = cls._to_canonical_json(payload)

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def create_anchor_payload(
        anchor_id: str,
        prompt_hash: str,
        score: float,
        route: str,
        alpha: float,
        gamma: float,
        chain_id: str,
        entry_id: int,
        prev_hash: str,
        *,
        origin_node_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a standardized signable Horizon event.
        Identity fields are explicit:
        - origin_node_id identifies the signing runtime
        - agent_id identifies Kai
        - model_id identifies the model backend
        """
        payload: Dict[str, Any] = {
            "schema_version": "zpp.event.v1",
            "chain_id": chain_id,
            "entry_id": int(entry_id),
            "prev_hash": prev_hash,
            "anchor_id": anchor_id,
            "prompt_hash": prompt_hash,
            "score_bp": round(float(score) * 10_000),
            "alpha_bp": round(float(alpha) * 10_000),
            "gamma_bp": round(float(gamma) * 10_000),
            "assigned_route": route,
            "timestamp_iso": (
                datetime.now(UTC)
                .isoformat()
                .replace("+00:00", "Z")
            ),
        }
        
        if origin_node_id:
            payload["origin_node_id"] = origin_node_id
        if agent_id:
            payload["agent_id"] = agent_id
        if model_id:
            payload["model_id"] = model_id
            
        if "active_weights" in kwargs:
            payload["fluid_matrix"] = {
                "active_weights": kwargs["active_weights"],
                "variance": kwargs.get("variance", 0.0)
            }
            
        return payload

