#!/usr/bin/env python3
"""
Zero-Point Protocol — Validator Database Deduplicator

Safely removes repeated exact-content records from NODE_A/B/C.

Safety:
- Dry run by default.
- Groups by speaker + SHA-256(content).
- Prefers canonical rows containing memory_layer metadata.
- Creates timestamped backups before any write.
- Writes a JSON deletion manifest.
- Never touches NODE_D, NODE_E, or NODE_F.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


DB_FILES = [
    Path("db_lattice/NODE_A_matrix.db"),
    Path("db_lattice/NODE_B_matrix.db"),
    Path("db_lattice/NODE_C_matrix.db"),
]


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def parse_metadata(raw: str | None) -> dict:
    if not raw:
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def choose_canonical(records: list[dict]) -> dict:
    """
    Prefer a row containing memory_layer metadata.
    If several qualify, keep the earliest ID.
    Otherwise keep the earliest ID overall.
    """

    tagged = [
        record
        for record in records
        if record["metadata"].get("memory_layer")
    ]

    if tagged:
        return min(tagged, key=lambda row: row["id"])

    return min(records, key=lambda row: row["id"])


def analyze_database(db_path: Path) -> dict:
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

    groups = defaultdict(list)

    for row_id, timestamp, speaker, content, metadata_json in rows:
        metadata = parse_metadata(metadata_json)
        digest = content_hash(content)

        key = (
            speaker,
            digest,
        )

        groups[key].append(
            {
                "id": row_id,
                "timestamp": timestamp,
                "speaker": speaker,
                "content_hash": digest,
                "metadata": metadata,
            }
        )

    deletion_ids = []
    manifest_groups = []

    for (speaker, digest), records in groups.items():
        if len(records) <= 1:
            continue

        canonical = choose_canonical(records)

        duplicates = [
            row
            for row in records
            if row["id"] != canonical["id"]
        ]

        deletion_ids.extend(
            row["id"]
            for row in duplicates
        )

        manifest_groups.append(
            {
                "speaker": speaker,
                "content_hash": digest,
                "canonical_row_id": canonical["id"],
                "canonical_timestamp": canonical["timestamp"],
                "canonical_memory_layer": canonical[
                    "metadata"
                ].get("memory_layer"),
                "deleted_row_ids": [
                    row["id"]
                    for row in duplicates
                ],
            }
        )

    return {
        "db_path": db_path,
        "total_rows": len(rows),
        "duplicate_groups": len(manifest_groups),
        "deletion_ids": sorted(deletion_ids),
        "manifest_groups": manifest_groups,
    }


def backup_database(db_path: Path, timestamp: str) -> Path:
    backup_path = db_path.with_name(
        f"{db_path.stem}_pre_dedupe_{timestamp}{db_path.suffix}"
    )

    shutil.copy2(
        db_path,
        backup_path
    )

    return backup_path


def delete_rows(db_path: Path, row_ids: list[int]) -> None:
    if not row_ids:
        return

    with sqlite3.connect(db_path) as conn:
        conn.execute("BEGIN IMMEDIATE")

        try:
            # Chunk to avoid SQLite parameter limits.
            chunk_size = 500

            for start in range(0, len(row_ids), chunk_size):
                chunk = row_ids[start:start + chunk_size]

                placeholders = ",".join(
                    "?"
                    for _ in chunk
                )

                conn.execute(
                    f"""
                    DELETE FROM conversation_history
                    WHERE id IN ({placeholders})
                    """,
                    chunk,
                )

            conn.commit()

        except Exception:
            conn.rollback()
            raise


def verify_database(db_path: Path) -> tuple[int, int]:
    """
    Return:
        remaining row count
        remaining duplicate row count
    """

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT speaker, content
            FROM conversation_history
            """
        ).fetchall()

    seen = set()
    duplicate_rows = 0

    for speaker, content in rows:
        key = (
            speaker,
            content_hash(content),
        )

        if key in seen:
            duplicate_rows += 1
        else:
            seen.add(key)

    return len(rows), duplicate_rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely deduplicate NODE_A/B/C validator databases."
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually remove duplicates. Default is dry run.",
    )

    args = parser.parse_args()

    reports = []

    print()
    print("ZERO-POINT PROTOCOL — VALIDATOR DEDUPLICATION")
    print(
        "MODE:",
        "WRITE" if args.write else "DRY RUN — NO CHANGES"
    )
    print()

    for relative_path in DB_FILES:
        db_path = relative_path.expanduser().resolve()

        if not db_path.exists():
            print(
                f"[Error] Database not found: {db_path}"
            )
            continue

        report = analyze_database(db_path)
        reports.append(report)

        remaining = (
            report["total_rows"]
            - len(report["deletion_ids"])
        )

        print("=" * 72)
        print(f"DATABASE: {db_path.name}")
        print("=" * 72)
        print(
            f"Current rows:          {report['total_rows']}"
        )
        print(
            f"Duplicate groups:      {report['duplicate_groups']}"
        )
        print(
            f"Rows marked duplicate: {len(report['deletion_ids'])}"
        )
        print(
            f"Rows after cleanup:    {remaining}"
        )
        print()

    if not args.write:
        print("DRY RUN ONLY — no databases changed.")
        return 0

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%SZ")

    manifest = {
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "strategy": (
            "speaker + sha256(content); "
            "prefer memory_layer-tagged canonical row"
        ),
        "databases": [],
    }

    for report in reports:
        db_path = report["db_path"]

        backup_path = backup_database(
            db_path,
            timestamp
        )

        delete_rows(
            db_path,
            report["deletion_ids"]
        )

        remaining_rows, remaining_duplicates = (
            verify_database(db_path)
        )

        manifest["databases"].append(
            {
                "database": str(db_path),
                "backup": str(backup_path),
                "deleted_rows": len(
                    report["deletion_ids"]
                ),
                "remaining_rows": remaining_rows,
                "remaining_duplicate_rows": (
                    remaining_duplicates
                ),
                "groups": report[
                    "manifest_groups"
                ],
            }
        )

        print(
            f"[Cleanup] {db_path.name}: "
            f"removed {len(report['deletion_ids'])} rows"
        )

        print(
            f"[Verify] {db_path.name}: "
            f"{remaining_rows} rows remain | "
            f"duplicate rows remaining="
            f"{remaining_duplicates}"
        )

        print(
            f"[Backup] {backup_path.name}"
        )

    manifest_dir = Path("logs")
    manifest_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    manifest_path = manifest_dir / (
        f"validator_dedupe_manifest_{timestamp}.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True
        ),
        encoding="utf-8",
    )

    print()
    print(
        f"[Manifest] {manifest_path.resolve()}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())