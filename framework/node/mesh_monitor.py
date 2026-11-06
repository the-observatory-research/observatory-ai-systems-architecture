#!/usr/bin/env python3
"""
Zero-Point Protocol — Horizon Runtime Monitor

Displays:
- configured mesh nodes and roles
- node process/log activity
- Horizon pipeline ledger status
- recent pipeline verification events

This monitor provides a lightweight runtime view of the
integrated Horizon system. It is intended for diagnostics
until the full dashboard replaces it.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple


NODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = NODE_DIR.parent

CONFIG_PATH = NODE_DIR / "config.json"

LEDGER_PATH = (
    PROJECT_ROOT
    / "ledger"
    / "horizon_pipeline.jsonl"
)

LOGS_DIR = NODE_DIR / "logs"

REFRESH_INTERVAL_SECONDS = 1.5
RECENT_EVENT_LIMIT = 8


def clear_terminal() -> None:
    os.system(
        "cls"
        if os.name == "nt"
        else "clear"
    )


def load_peer_map() -> Dict[str, Dict[str, Any]]:
    with CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as config_file:
        config = json.load(config_file)

    peer_map = config.get("peer_network_map", {})

    if not isinstance(peer_map, dict):
        return {}

    return peer_map

def parse_jsonl(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    if not path.exists() or path.stat().st_size == 0:
        return records

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as ledger_file:
            for line in ledger_file:
                stripped = line.strip()

                if not stripped:
                    continue

                try:
                    record = json.loads(stripped)

                    if isinstance(record, dict):
                        records.append(record)

                except json.JSONDecodeError:
                    continue

    except OSError:
        return []

    return records

def parse_pipeline_ledger() -> Tuple[
    int,
    str,
    List[Dict[str, Any]],
]:
    if (
        not LEDGER_PATH.exists()
        or LEDGER_PATH.stat().st_size == 0
    ):
        return 0, "N/A", []

    records = parse_jsonl(LEDGER_PATH)

    if not records:
        return 0, "N/A", []

    last_record = records[-1]

    last_hash = str(
        last_record.get(
            "payload_hash",
            last_record.get(
                "state_hash",
                last_record.get(
                    "envelope_hash",
                    last_record.get(
                        "anchor_hash",
                        "UNKNOWN",
                    ),
                ),
            ),
        )
    )

    return (
        len(records),
        last_hash,
        records[-RECENT_EVENT_LIMIT:],
    )

def process_status(
    legacy_node_id: str,
) -> str:
    log_path = (
        LOGS_DIR
        / f"{legacy_node_id.lower()}.log"
    )

    if not log_path.exists():
        return "NO LOG"

    age_seconds = time.time() - log_path.stat().st_mtime

    if age_seconds < 15:
        return "ACTIVE"

    return "IDLE"


def format_event(
    record: Dict[str, Any],
) -> str:

    timestamp = record.get(
        "timestamp",
        "?",
    )

    status = record.get(
        "status",
        "UNKNOWN",
    )

    constraint = record.get(
        "constraint",
        "?",
    )

    payload_hash = str(
        record.get(
            "payload_hash",
            "UNKNOWN",
        )
    )

    trace = record.get(
        "trace",
        [],
    )

    if isinstance(trace, list) and trace:
        summary = trace[-1]
    else:
        summary = "No trace"

    summary = str(summary).replace(
        "\n",
        " ",
    )[:70]

    return (
        f"[{timestamp}] "
        f"status={status:<8} "
        f"constraint={constraint:<4} "
        f"hash={payload_hash[:12]} "
        f"{summary}"
    )


def main() -> None:
    peer_map = load_peer_map()

    while True:
        clear_terminal()

        ledger_height, last_hash, recent_events = (
            parse_pipeline_ledger()
        )

        print("=" * 72)
        print(
            "HORIZON — LIVE MESH MONITOR"
        )
        print("=" * 72)
        print(
            f"Network state: ACTIVE"
            f" | Pipeline ledger height: {ledger_height}"
        )

        print(
            f"Latest pipeline hash: {last_hash[:24]}"
        )
        print("-" * 72)
        print("CONFIGURED NODE ACTIVITY")
        print()

        for legacy_node_id, peer_config in peer_map.items():
            stable_id = peer_config.get(
                "stable_id",
                legacy_node_id,
            )
            role = str(
                peer_config.get("role", "unknown")
            ).upper()

            status = process_status(legacy_node_id)

            print(
                f"  {legacy_node_id:<8} "
                f"{stable_id:<18} "
                f"role={role:<10} "
                f"status={status:<7} "
            )

        print("-" * 72)
        print("RECENT HORIZON PIPELINE RECORDS")
        print()

        if not recent_events:
            print("  Waiting for Horizon pipeline records...")
        else:
            for event in reversed(recent_events):
                print(f"  {format_event(event)}")

        print("=" * 72)
        print(
            "Pipeline records and node activity are shown separately."
        )
        print("Press Ctrl+C to close the monitor.")

        time.sleep(REFRESH_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            "\nMonitor closed. Mesh processes remain operational."
        )
