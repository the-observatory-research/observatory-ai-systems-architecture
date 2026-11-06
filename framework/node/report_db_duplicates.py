#!/usr/bin/env python3
"""
Zero-Point Protocol — Validator Database Duplicate Report

Read-only audit for NODE_A/B/C conversation_history tables.

Behavior:
- Does NOT modify any database.
- Groups records by SHA-256 hash of content.
- Reports duplicate groups and duplicate row counts.
- Separates exact duplicate content from unique content.
- Shows memory_layer metadata when available.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


DB_FILES = [
    Path("db_lattice/NODE_A_matrix.db"),
    Path("db_lattice/NODE_B_matrix.db"),
    Path("db_lattice/NODE_C_matrix.db"),
]


def content_hash(content: str) -> str:
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def parse_metadata(metadata_json: str | None) -> Dict[str, Any]:
    if not metadata_json:
        return {}

    try:
        return json.loads(metadata_json)
    except json.JSONDecodeError:
        return {}


def audit_database(db_path: Path) -> Dict[str, Any]:
    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found: {db_path}"
        )

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                timestamp,
                speaker,
                content,
                metadata_json
            FROM conversation_history
            ORDER BY id
            """
        ).fetchall()

    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    layer_counts: Dict[str, int] = defaultdict(int)

    for (
        row_id,
        timestamp,
        speaker,
        content,
        metadata_json,
    ) in rows:
        metadata = parse_metadata(
            metadata_json
        )

        memory_layer = metadata.get(
            "memory_layer",
            "unknown"
        )

        layer_counts[memory_layer] += 1

        digest = content_hash(content)

        groups[digest].append(
            {
                "id": row_id,
                "timestamp": timestamp,
                "speaker": speaker,
                "content": content,
                "metadata": metadata,
                "memory_layer": memory_layer,
            }
        )

    duplicate_groups = {
        digest: records
        for digest, records in groups.items()
        if len(records) > 1
    }

    duplicate_rows = sum(
        len(records) - 1
        for records in duplicate_groups.values()
    )

    unique_contents = len(groups)

    return {
        "db_path": db_path,
        "total_rows": len(rows),
        "unique_contents": unique_contents,
        "duplicate_groups": duplicate_groups,
        "duplicate_rows": duplicate_rows,
        "layer_counts": dict(layer_counts),
    }


def print_report(report: Dict[str, Any]) -> None:
    db_path: Path = report["db_path"]

    print()
    print(
        "=" * 72
    )
    print(
        f"DATABASE: {db_path.name}"
    )
    print(
        "=" * 72
    )

    print(
        f"Total conversation rows: "
        f"{report['total_rows']}"
    )

    print(
        f"Unique content payloads:  "
        f"{report['unique_contents']}"
    )

    print(
        f"Duplicate groups:         "
        f"{len(report['duplicate_groups'])}"
    )

    print(
        f"Extra duplicate rows:     "
        f"{report['duplicate_rows']}"
    )

    print()
    print("Memory layers:")

    for layer, count in sorted(
        report["layer_counts"].items()
    ):
        print(
            f"  {layer}: {count}"
        )

    duplicate_groups = report[
        "duplicate_groups"
    ]

    if not duplicate_groups:
        print()
        print(
            "No exact-content duplicates found."
        )
        return

    print()
    print("Top duplicate groups:")

    ranked_groups = sorted(
        duplicate_groups.items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )

    for index, (
        digest,
        records,
    ) in enumerate(
        ranked_groups[:20],
        start=1,
    ):
        first = records[0]

        preview = (
            first["content"]
            .replace("\n", " ")
            .strip()
        )

        if len(preview) > 100:
            preview = preview[:100] + "..."

        ids = [
            record["id"]
            for record in records
        ]

        print()
        print(
            f"{index}. Copies: {len(records)}"
        )
        print(
            f"   SHA-256: {digest}"
        )
        print(
            f"   Row IDs: {ids}"
        )
        print(
            f"   Speaker: {first['speaker']}"
        )
        print(
            f"   Layer:   "
            f"{first['memory_layer']}"
        )
        print(
            f"   Preview: {preview}"
        )


def main() -> None:
    print()
    print(
        "ZERO-POINT PROTOCOL — "
        "VALIDATOR DUPLICATE AUDIT"
    )
    print(
        "READ ONLY — NO DATABASE "
        "CHANGES WILL BE MADE"
    )

    combined_duplicates = 0
    combined_rows = 0

    for relative_path in DB_FILES:
        db_path = (
            relative_path
            .expanduser()
            .resolve()
        )

        try:
            report = audit_database(
                db_path
            )
        except Exception as e:
            print()
            print(
                f"[Audit Error] "
                f"{db_path.name}: "
                f"{type(e).__name__}: {e}"
            )
            continue

        print_report(report)

        combined_rows += report[
            "total_rows"
        ]

        combined_duplicates += report[
            "duplicate_rows"
        ]

    print()
    print(
        "=" * 72
    )
    print("COMBINED SUMMARY")
    print(
        "=" * 72
    )
    print(
        f"Total A/B/C conversation rows: "
        f"{combined_rows}"
    )
    print(
        f"Total extra duplicate rows:     "
        f"{combined_duplicates}"
    )
    print()
    print(
        "READ ONLY — no rows were deleted."
    )
    print()


if __name__ == "__main__":
    main()