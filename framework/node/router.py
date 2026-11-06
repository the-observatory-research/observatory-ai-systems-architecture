#!/usr/bin/env python3
"""
Zero-Point Protocol — Main Router Engine
Orchestrates local runtime ingestion, scoring, and routing.
"""

import json
import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

from scoring import GammaScorer
from crypto import CryptoEngine

# ────────────────────────────────────────────────────────────
# GAMMA SCORER
# ────────────────────────────────────────────────────────────

_gamma_scorer = GammaScorer(gamma_threshold=0.50)

def score_gamma(text: str, context: Optional[list] = None):
    result = _gamma_scorer.score(text, context)
    return result.get("score", 0.0), result.get("route", "UNKNOWN")


# ────────────────────────────────────────────────────────────
# ROUTER
# ────────────────────────────────────────────────────────────

class ZeroPointRouter:
    """
    Routes prompts, tracks state, and manages ingress/egress.
    No gates. No taxes. No simulated geometry.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.node_id = self.config.get("node_id", "unknown_node")
        self.chain_id = self.config.get("chain_id", "zpp_main")

        self.crypto = CryptoEngine(self.node_id)

        self.entry_counter = 0
        self.last_committed_hash = self.config.get("genesis", {}).get("prev_hash", "0" * 64)

        self.ingress_log_directory = os.getenv("ZPP_INGRESS_LOG_DIRECTORY", "./logs/ingress")
        os.makedirs(self.ingress_log_directory, exist_ok=True)

        self.mesh_transport = None

        print(f"[ROUTER] Node '{self.node_id}' ready.")

    @staticmethod
    def _load_config(path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config missing: {path}")
        with open(path, "r") as f:
            return json.load(f)

    def process_ingress_prompt(
        self,
        prompt_text: str,
        anchor_id: str,
        mock_model_response: str = "",
    ) -> Dict[str, Any]:
        """Process an incoming prompt and return a routing receipt."""

        self.entry_counter += 1
        prompt_hash = self.crypto.hash_prompt(prompt_text)

        gamma_score, route = score_gamma(mock_model_response or prompt_text)

        payload = self.crypto.create_anchor_payload(
            anchor_id=anchor_id,
            prompt_hash=prompt_hash,
            score=gamma_score,
            route=route,
            chain_id=self.chain_id,
            entry_id=self.entry_counter,
            prev_hash=self.last_committed_hash,
        )

        local_signature = self.crypto.sign_payload(payload)
        network_signatures = {self.node_id: local_signature.hex()}

        if self.mesh_transport:
            envelope = self.mesh_transport.create_signed_envelope(
                anchor_id=anchor_id,
                payload=payload,
            )
            self.mesh_transport.broadcast(envelope)
            network_signatures[self.node_id] = envelope["signature"]

        # Save ingress log
        log_path = os.path.join(self.ingress_log_directory, f"packet_{anchor_id}.json")
        with open(log_path, "w") as f:
            json.dump({
                "anchor_id": anchor_id,
                "gamma_score": gamma_score,
                "route": route,
                "entry_id": self.entry_counter,
            }, f, indent=4)

        self.last_committed_hash = hashlib.sha256(local_signature).hexdigest()

        return {
            "protocol_version": "zpp.kai.v1",
            "anchor_id": anchor_id,
            "prompt_hash": prompt_hash,
            "metrics": {
                "gamma_score": gamma_score,
                "route": route,
            },
            "route": route,
            "consensus_state": "ACCEPT",
            "payload": payload,
            "signatures": network_signatures,
        }