#!/usr/bin/env python3
"""
Zero-Point Protocol — Asynchronous Heartbeat Matrix
Evolves linear time intervals into non-blocking network metronomes.
"""
import sys
import time
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class AsynchronousPulse:
    def __init__(
        self,
        memory_lattice=None,
        state_getter=None,
        max_entries: int = 100
    ):
        self.entries: List[Dict[str, Any]] = []
        self.max_entries = max_entries
        self.memory = memory_lattice  
        self.state_getter = state_getter
        self._pulse_lock = asyncio.Lock()
        self.is_beating = False

    async def record(self, thought: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Injects a structural heartbeat frame directly into the volatile memory matrix
        without locking execution threads or stalling incoming web socket packages.
        """
        pulse_frame = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "epoch_ticks": time.time(),
            "thought": thought,
            "metadata": metadata or {}
        }

        async with self._pulse_lock:
            self.entries.append(pulse_frame)
            if len(self.entries) > self.max_entries:
                self.entries.pop(0)

        # Non-blocking streaming direct into the active lattice field
        if self.memory:
            # commit_to_field handles the background thread disk persistence automatically
            await self.memory.commit_to_field(
                layer="pulse",
                speaker="Pulse",
                content=thought,
                metadata=pulse_frame["metadata"]
            )

    async def start_metronome(self, interval_seconds: float = 60.0):
        """
        Launches the background metronome loop.
        Records node-local, state-aware heartbeat telemetry at regular intervals.
        """
        if self.is_beating:
            return

        self.is_beating = True

        node_id = (
            self.memory.node_id
            if self.memory
            else "UNKNOWN"
        )

        print(
            f"[Pulse Engine] "
            f"{node_id} asynchronous metronome initialized."
        )

        while self.is_beating:
            try:
                current_state = (
                    self.state_getter()
                    if self.state_getter
                    else "UNKNOWN"
                )

                tick_meta = {
                    "node_id": node_id,
                    "state": current_state,
                    "active_tasks": len(asyncio.all_tasks()),
                    "pulse_signature": (
                        f"{node_id}_tick_{int(time.time())}"
                    )
                }

                await self.record(
                    thought=f"{node_id} heartbeat: {current_state}.",
                    metadata=tick_meta
                )

                await asyncio.sleep(interval_seconds)

            except asyncio.CancelledError:
                self.is_beating = False

                print(
                    f"[Pulse Engine] "
                    f"{node_id} metronome halted gracefully."
                )
                break

            except Exception as e:
                print(
                    f"[Pulse Error] "
                    f"{node_id} metronome drift detected: {e}",
                    file=sys.stderr
                )

                await asyncio.sleep(2)

    def stop_metronome(self):
        self.is_beating = False

    def last(self, n: int = 1) -> List[Dict[str, Any]]:
        return self.entries[-n:] if self.entries else []

    def all(self) -> List[Dict[str, Any]]:
        return self.entries

    def clear(self):
        self.entries = []
