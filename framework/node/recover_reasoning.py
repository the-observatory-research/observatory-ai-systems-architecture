#!/usr/bin/env python3
"""
Zero-Point Protocol — Node F Reasoning Recovery Importer

Recovers completed DeepSeek-R1 reasoning streams from a saved Node F
terminal transcript and imports them into NODE_F_matrix.db.

Safety behavior:
- Dry-run by default.
- Never modifies A/B/C databases.
- One reasoning stream = one database row.
- SHA-256 deduplication prevents duplicate imports.
- Existing Node F reasoning records are checked before insertion.
- Creates a database backup before an actual write.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any


STREAM_START = "================== DEEPSEEK-R1 RAW COGNITIVE STREAM =================="
STREAM_END = "===================================================================="


def hash_reasoning(content: str) -> str:
    """Return deterministic SHA-256 hash for a reasoning block."""
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def extract_reasoning_blocks(transcript: str) -> List[str]:
    """
    Extract complete DeepSeek reasoning blocks from the transcript.

    Only content between STREAM_START and STREAM_END is recovered.
    Empty blocks are ignored.
    """

    blocks: List[str] = []
    position = 0

    while True:
        start_index = transcript.find(
            STREAM_START,
            position
        )

        if start_index == -1:
            break

        content_start = (
            start_index + len(STREAM_START)
        )

        end_index = transcript.find(
            STREAM_END,
            content_start
        )

        if end_index == -1:
            # Incomplete final stream.
            # Do not import a partial response.
            break

        block = transcript[
            content_start:end_index
        ].strip()

        if block:
            blocks.append(block)

        position = (
            end_index + len(STREAM_END)
        )

    return blocks


def deduplicate_blocks(
    blocks: List[str]
) -> tuple[List[Dict[str, Any]], int]:
    """
    Deduplicate reasoning blocks inside the recovery transcript itself.
    """

    unique_blocks: List[Dict[str, Any]] = []
    seen_hashes = set()
    duplicate_count = 0

    for index, content in enumerate(
        blocks,
        start=1
    ):
        content_hash = hash_reasoning(content)

        if content_hash in seen_hashes:
            duplicate_count += 1
            continue

        seen_hashes.add(content_hash)

        unique_blocks.append(
            {
                "sequence": index,
                "content": content,
                "content_hash": content_hash,
                "character_count": len(content),
            }
        )

    return unique_blocks, duplicate_count


def load_existing_reasoning_hashes(
    db_path: Path
) -> set[str]:
    """
    Calculate hashes for existing Node F reasoning rows.

    This allows recovery to be safely rerun without importing
    the same reasoning response twice.
    """

    if not db_path.exists():
        return set()

    hashes: set[str] = set()

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT content, metadata_json
            FROM conversation_history
            """
        ).fetchall()

    for content, metadata_json in rows:
        metadata = {}

        if metadata_json:
            try:
                metadata = json.loads(
                    metadata_json
                )
            except json.JSONDecodeError:
                metadata = {}

        if metadata.get("memory_layer") != "reasoning":
            continue

        existing_hash = metadata.get(
            "reasoning_hash"
        )

        if existing_hash:
            hashes.add(existing_hash)
        elif content:
            hashes.add(
                hash_reasoning(content)
            )

    return hashes


def build_import_set(
    blocks: List[Dict[str, Any]],
    existing_hashes: set[str]
) -> tuple[List[Dict[str, Any]], int]:
    """
    Remove reasoning blocks already present in NODE_F_matrix.db.
    """

    import_blocks = []
    already_present = 0

    for block in blocks:
        if block["content_hash"] in existing_hashes:
            already_present += 1
            continue

        import_blocks.append(block)

    return import_blocks, already_present


def backup_database(db_path: Path) -> Path:
    """Create timestamped safety backup before modifying Node F DB."""

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%SZ")

    backup_path = db_path.with_name(
        f"{db_path.stem}_pre_reasoning_recovery_"
        f"{timestamp}{db_path.suffix}"
    )

    shutil.copy2(
        db_path,
        backup_path
    )

    return backup_path


def import_reasoning_blocks(
    db_path: Path,
    blocks: List[Dict[str, Any]],
    source_file: Path
) -> int:
    """
    Persist recovered reasoning into Node F's conversation_history.

    Records are marked with memory_layer='reasoning' so they are
    compatible with the evolved MemoryLattice persistence schema.
    """

    imported = 0

    with sqlite3.connect(db_path) as conn:
        for block in blocks:
            timestamp = datetime.now(
                timezone.utc
            ).isoformat()

            metadata = {
                "memory_layer": "reasoning",
                "model": "deepseek-r1:7b",
                "source": "vault_reasoning_recovery",
                "recovered_from": source_file.name,
                "original_stream_sequence": block[
                    "sequence"
                ],
                "reasoning_hash": block[
                    "content_hash"
                ],
                "character_count": block[
                    "character_count"
                ],
                "recovered_at": timestamp,
            }

            conn.execute(
                """
                INSERT INTO conversation_history
                (
                    timestamp,
                    speaker,
                    content,
                    metadata_json
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    timestamp,
                    "NODE_F_CORE",
                    block["content"],
                    json.dumps(
                        metadata,
                        sort_keys=True
                    ),
                ),
            )

            imported += 1

        conn.commit()

    return imported


def print_report(
    transcript_path: Path,
    db_path: Path,
    total_blocks: int,
    unique_blocks: int,
    transcript_duplicates: int,
    existing_duplicates: int,
    import_blocks: List[Dict[str, Any]],
    dry_run: bool
) -> None:
    """Print recovery summary."""

    recovered_characters = sum(
        block["character_count"]
        for block in import_blocks
    )

    print()
    print(
        "========== NODE F REASONING "
        "RECOVERY REPORT =========="
    )
    print(
        f"Transcript:              "
        f"{transcript_path}"
    )
    print(
        f"Target DB:               "
        f"{db_path}"
    )
    print(
        f"Completed streams found: {total_blocks}"
    )
    print(
        f"Unique transcript blocks:{unique_blocks:>5}"
    )
    print(
        f"Transcript duplicates:   "
        f"{transcript_duplicates}"
    )
    print(
        f"Already present in DB:   "
        f"{existing_duplicates}"
    )
    print(
        f"Ready for import:        "
        f"{len(import_blocks)}"
    )
    print(
        f"Characters to recover:  "
        f"{recovered_characters}"
    )

    if dry_run:
        print()
        print(
            "DRY RUN ONLY — database unchanged."
        )

    print(
        "==========================================="
    )
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Recover DeepSeek reasoning streams "
            "into NODE_F_matrix.db."
        )
    )

    parser.add_argument(
        "transcript",
        type=Path,
        help="Clean Node F transcript TXT file."
    )

    parser.add_argument(
        "--db",
        type=Path,
        default=Path(
            "db_lattice/NODE_F_matrix.db"
        ),
        help=(
            "Node F SQLite database path. "
            "Default: db_lattice/NODE_F_matrix.db"
        )
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Actually import recovered reasoning. "
            "Without this flag the script performs "
            "a dry run only."
        )
    )

    args = parser.parse_args()

    transcript_path = (
        args.transcript.expanduser().resolve()
    )

    db_path = (
        args.db.expanduser().resolve()
    )

    if not transcript_path.exists():
        print(
            f"[Recovery Error] Transcript not found: "
            f"{transcript_path}",
            file=sys.stderr
        )
        return 1

    if not db_path.exists():
        print(
            f"[Recovery Error] Node F database "
            f"not found: {db_path}",
            file=sys.stderr
        )
        return 1

    transcript = transcript_path.read_text(
        encoding="utf-8"
    )

    raw_blocks = extract_reasoning_blocks(
        transcript
    )

    unique_blocks, transcript_duplicates = (
        deduplicate_blocks(raw_blocks)
    )

    existing_hashes = (
        load_existing_reasoning_hashes(
            db_path
        )
    )

    import_blocks, existing_duplicates = (
        build_import_set(
            unique_blocks,
            existing_hashes
        )
    )

    print_report(
        transcript_path=transcript_path,
        db_path=db_path,
        total_blocks=len(raw_blocks),
        unique_blocks=len(unique_blocks),
        transcript_duplicates=(
            transcript_duplicates
        ),
        existing_duplicates=(
            existing_duplicates
        ),
        import_blocks=import_blocks,
        dry_run=not args.write,
    )

    if not args.write:
        return 0

    if not import_blocks:
        print(
            "[Recovery] Nothing new to import."
        )
        return 0

    backup_path = backup_database(
        db_path
    )

    print(
        f"[Recovery] Safety backup created: "
        f"{backup_path}"
    )

    imported = import_reasoning_blocks(
        db_path=db_path,
        blocks=import_blocks,
        source_file=transcript_path,
    )

    print(
        f"[Recovery] Successfully imported "
        f"{imported} reasoning records "
        f"into NODE_F_matrix.db."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())