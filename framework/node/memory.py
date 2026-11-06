#!/usr/bin/env python3
"""
Zero-Point Protocol — Evolved Multi-Agent Memory Lattice
Replaces standard SQLite blockages with asynchronous concurrent relays.
"""
import sys
import json
import sqlite3
import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

class MemoryLattice:
    def __init__(self, db_path: str, node_id: str):
        self.db_path = db_path
        self.node_id = node_id
        
        # The Living Field: High-speed volatile memory matrix for real-time agent handoffs
        self._volatile_matrix: Dict[str, List[Dict[str, Any]]] = {
            "conversation": [],
            "pulse": [],
            "anchor": [],
            "internet_ingress": [],
            "discovery": [],
            "bridge_retrieval": [],
            "reasoning": [],
        }
        self._matrix_lock = asyncio.Lock()
        self._init_db()

    def _init_db(self):
        """Maintains structural backward compatibility for system persistence."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    speaker TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata_json TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pulse_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata_json TEXT
                )
            """)
            # Unified State Hash Registry for cross-node tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lattice_state_ledger (
                    state_hash TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    origin_node TEXT NOT NULL,
                    zpp_baseline REAL NOT NULL
                )
            """)

    async def commit_to_field(self, layer: str, speaker: str, content: str, metadata: Optional[dict] = None):
        """
        Non-blocking atomic injection. Streams token patterns directly into the active
        volatile matrix so other nodes can access it instantly over web sockets.
        """
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "speaker": speaker,
            "content": content,
            "origin_node": self.node_id,
            "metadata": metadata or {}
        }
        
        async with self._matrix_lock:
            self._volatile_matrix[layer].append(payload)
            # Prevent volatile matrix bloat: compress past 100 deep-context records
            if len(self._volatile_matrix[layer]) > 100:
                self._volatile_matrix[layer].pop(0)

        # Offload persistent disk writing to a background task so it doesn't block web socket loops
        asyncio.create_task(self._persist_layer(layer, payload))

    async def _persist_layer(self, layer: str, payload: dict):
        """Asynchronous background file writer handling physical disk storage."""
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._disk_write, layer, payload)
        except Exception as e:
            print(f"[Lattice Error] Background persistence failed on Node {self.node_id}: {e}", file=sys.stderr)

    def _disk_write(self, layer: str, payload: dict):
        """Isolated sync thread executor for SQLite persistence."""
        with sqlite3.connect(self.db_path) as conn:
            if layer in [
                "conversation",
                "anchor",
                "internet_ingress",
                "discovery",
                "bridge_retrieval",
                "reasoning",
            ]:
                metadata = dict(payload["metadata"])
                metadata["memory_layer"] = layer

                conn.execute(
                    "INSERT INTO conversation_history (timestamp, speaker, content, metadata_json) VALUES (?, ?, ?, ?)",
                    (
                        payload["timestamp"],
                        payload["speaker"],
                        payload["content"],
                        json.dumps(metadata)
                    )
                )

            elif layer == "pulse":
                conn.execute(
                    "INSERT INTO pulse_history (timestamp, content, metadata_json) VALUES (?, ?, ?)",
                    (
                        payload["timestamp"],
                        payload["content"],
                        json.dumps(payload["metadata"])
                    )
                )

    async def register_state_hash(self, consensus_text: str, zpp_val: float) -> str:
        """
        Generates a cryptographic signature of the current consensus vector.
        Allows nodes to verify state parity without exchanging full transaction histories.
        """
        state_string = f"{consensus_text}_{zpp_val}_{datetime.now(timezone.utc).date()}"
        state_hash = hashlib.sha256(state_string.encode('utf-8')).hexdigest()
        
        def _write_ledger():
            with sqlite3.connect(self.db_path) as conn:
                try:
                    conn.execute(
                        "INSERT INTO lattice_state_ledger (state_hash, timestamp, origin_node, zpp_baseline) VALUES (?, ?, ?, ?)",
                        (state_hash, datetime.now(timezone.utc).isoformat(), self.node_id, zpp_val)
                    )
                except sqlite3.IntegrityError:
                    pass # State signature already synchronized across the network

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _write_ledger)
        return state_hash

    async def get_volatile_context(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Reads instantly from volatile memory space, skipping slow database lookups completely."""
        async with self._matrix_lock:
            combined = []
            for item in self._volatile_matrix["conversation"]:
                combined.append({"timestamp": item["timestamp"], "speaker": item["speaker"], "content": item["content"], "type": "conversation"})
            for item in self._volatile_matrix["pulse"]:
                combined.append({"timestamp": item["timestamp"], "speaker": "Pulse", "content": f"[Pulse] {item['content']}", "type": "pulse"})
            for item in self._volatile_matrix["internet_ingress"]:
                combined.append({"timestamp": item["timestamp"], "speaker": "Ingress", "content": f"[Internet] {item['content']}", "type": "ingress"})
            
            combined.sort(key=lambda x: x["timestamp"])
            return combined[-limit:]
