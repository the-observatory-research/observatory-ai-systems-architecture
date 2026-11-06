"""
telemetry.py — Lightweight runtime observer for Horizon.

Telemetry observes. It never controls.
"""

import time
from typing import Any


class Telemetry:
    """
    A minimal, read-only observer of the Horizon runtime.

    Does not depend on engines, pipelines, or governance.
    """

    def __init__(
        self,
        config: dict,
        memory: Any,
        pulse: Any,
        gamma_scorer: Any,
        transport: Any = None,
    ):
        self.config = config
        self.memory = memory
        self.pulse = pulse
        self.gamma_scorer = gamma_scorer
        self.transport = transport
        self._started_at = time.time()

    def snapshot(self) -> dict:
        """
        Return a read-only snapshot of the current runtime state.
        """
        return {
            "timestamp": time.time(),
            "uptime": round(time.time() - self._started_at, 1),
            "runtime": {
                "node_id": self.config.get("node_id", "unknown"),
                "status": "healthy",
            },
            "memory": self._memory_snapshot(),
            "pulse": self._pulse_snapshot(),
            "gamma": self._gamma_snapshot(),
            "transport": self._transport_snapshot(),
        }

    def _memory_snapshot(self) -> dict:
        try:
            records = self.memory.get_conversations(limit=9999)
            return {
                "status": "healthy",
                "record_count": len(records),
                "available": True,
            }
        except Exception as e:
            return {
                "status": "unavailable",
                "record_count": 0,
                "available": False,
                "error": str(e),
            }

    def _pulse_snapshot(self) -> dict:
        try:
            return {
                "status": "healthy",
                "pulse_count": len(self.pulse.entries),
                "available": True,
            }
        except Exception as e:
            return {
                "status": "unavailable",
                "pulse_count": 0,
                "available": False,
                "error": str(e),
            }

    def _gamma_snapshot(self) -> dict:
        try:
            return {
                "status": "healthy",
                "gamma_threshold": getattr(self.gamma_scorer, "gamma_threshold", None),
                "beta_threshold": getattr(self.gamma_scorer, "beta_threshold", None),
                "available": True,
            }
        except Exception as e:
            return {
                "status": "unavailable",
                "available": False,
                "error": str(e),
            }

    def _transport_snapshot(self) -> dict:
        if self.transport is None:
            return {
                "status": "not_initialized",
                "available": False,
            }

        try:
            return {
                "status": "healthy",
                "available": True,
                "node_id": getattr(self.transport, "node_id", "unknown"),
            }
        except Exception as e:
            return {
                "status": "unavailable",
                "available": False,
                "error": str(e),
            }