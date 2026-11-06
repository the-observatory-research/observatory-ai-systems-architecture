#!/usr/bin/env python3
"""
Zero-Point Protocol — Node E Content Manifest Seeder

Builds the initial changed-only content manifest from records already
persisted in NODE_E_matrix.db.

Safety:
- Read-only against NODE_E_matrix.db.
- Does NOT trigger a vault scan.
- Does NOT contact D, A/B/C, or F.
- Dry-run by default.
- Deduplicates by resolved source_path.
- Uses the most recent known record for a path.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DB = Path(
    "db_lattice/NODE_E_matrix.db"
)

DEFAULT_MANIFEST = Path(
    "logs/node_e_content_manifest.json"
)


def parse_metadata(
    metadata_json: str | None
) -> dict[str, Any]:
    if not metadata_json:
        return {}

    try:
        value = json.loads(metadata_json)

        if isinstance(value, dict):
            return value

    except json.JSONDecodeError:
        pass

    return {}


def normalize_path(
    source_path: str
) -> str:
    """
    Match the path normalization used by the changed-only gate.
    """
    return str(
        Path(source_path)
        .expanduser()
        .resolve()
    )


def collect_manifest_records(
    db_path: Path
) -> tuple[dict, dict]:
    """
    Read Node E's existing bridge retrieval records.

    Returns:
        manifest
        statistics
    """

    manifest = {}

    stats = {
        "total_rows": 0,
        "bridge_rows": 0,
        "usable_rows": 0,
        "missing_source_path": 0,
        "missing_content_hash": 0,
        "repeated_paths": 0,
    }

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
            ORDER BY id ASC
            """
        ).fetchall()

    stats["total_rows"] = len(rows)

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

        # Only use records produced by Node E's
        # bridge retrieval pipeline.
        source_path = metadata.get(
            "source_path"
        )

        content_hash = metadata.get(
            "content_hash"
        )

        if not source_path and not content_hash:
            continue

        stats["bridge_rows"] += 1

        if not source_path:
            stats["missing_source_path"] += 1
            continue

        if not content_hash:
            stats["missing_content_hash"] += 1
            continue

        path_key = normalize_path(
            source_path
        )

        if path_key in manifest:
            stats["repeated_paths"] += 1

        manifest[path_key] = {
            "content_hash": content_hash,
            "filename": metadata.get(
                "filename",
                Path(path_key).name
            ),
            "vault": metadata.get(
                "vault",
                ""
            ),
            "markers": metadata.get(
                "markers",
                []
            ),
            "last_change_state": "BASELINE",
            "processed_at": (
                timestamp
                or datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "seeded_from": "NODE_E_matrix.db",
            "seeded_from_row_id": row_id,
        }

        stats["usable_rows"] += 1

    return manifest, stats


def write_manifest(
    manifest_path: Path,
    manifest: dict
) -> None:
    """
    Write manifest through a temporary file, then replace.
    """

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = manifest_path.with_suffix(
        ".json.tmp"
    )

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as manifest_file:
        json.dump(
            manifest,
            manifest_file,
            indent=2,
            sort_keys=True
        )

    temp_path.replace(
        manifest_path
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Seed Node E changed-only manifest "
            "from existing bridge retrieval records."
        )
    )

    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=(
            "Node E database path. "
            "Default: db_lattice/NODE_E_matrix.db"
        )
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=(
            "Manifest output path. "
            "Default: logs/node_e_content_manifest.json"
        )
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Actually create the manifest. "
            "Without this flag, dry-run only."
        )
    )

    args = parser.parse_args()

    db_path = (
        args.db
        .expanduser()
        .resolve()
    )

    manifest_path = (
        args.manifest
        .expanduser()
        .resolve()
    )

    if not db_path.exists():
        print(
            f"[Seed Error] Node E database not found: "
            f"{db_path}",
            file=sys.stderr
        )
        return 1

    if manifest_path.exists():
        print(
            f"[Seed Error] Manifest already exists: "
            f"{manifest_path}",
            file=sys.stderr
        )
        print(
            "Refusing to overwrite an existing "
            "changed-only baseline."
        )
        return 1

    manifest, stats = collect_manifest_records(
        db_path
    )

    print()
    print(
        "========== NODE E CONTENT MANIFEST SEED =========="
    )
    print(
        f"Source DB:              {db_path}"
    )
    print(
        f"Manifest:               {manifest_path}"
    )
    print(
        f"Total Node E rows:      {stats['total_rows']}"
    )
    print(
        f"Bridge candidate rows:  {stats['bridge_rows']}"
    )
    print(
        f"Usable bridge rows:     {stats['usable_rows']}"
    )
    print(
        f"Repeated source paths:  {stats['repeated_paths']}"
    )
    print(
        f"Missing source path:    "
        f"{stats['missing_source_path']}"
    )
    print(
        f"Missing content hash:   "
        f"{stats['missing_content_hash']}"
    )
    print(
        f"Unique manifest paths:  {len(manifest)}"
    )
    print()

    if not manifest:
        print(
            "[Seed Warning] No usable Node E "
            "bridge records were found."
        )
        print(
            "Manifest was NOT created."
        )
        return 1

    if not args.write:
        print(
            "DRY RUN ONLY — manifest not created."
        )
        print(
            "=================================================="
        )
        return 0

    write_manifest(
        manifest_path,
        manifest
    )

    print(
        f"[Seed] Manifest created successfully."
    )
    print(
        f"[Seed] Baseline paths registered: "
        f"{len(manifest)}"
    )
    print(
        "=================================================="
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())