#!/usr/bin/env python3
"""Produce aggregate-only evidence for the historical six-node ZPP snapshot.

Reads fixed, known files from node.zip. Never prints paths, content, SQL rows,
keys, source texts, or node message bodies. This does not run any AI component.
Requires Python 3.11+ with sqlite3.Connection.deserialize support.
"""
import argparse
from collections import Counter
import io
import json
from pathlib import Path
import sqlite3
import sys
import zipfile

LOGS = (
    ("discovery_ledger", "node/logs/node_d_discovery_ledger.jsonl", "discovery_record"),
    ("bridge_ledger", "node/logs/node_e_bridge_ledger.jsonl", "bridge_record"),
)
TABLE_NAMES = ("conversation_history", "pulse_history", "lattice_state_ledger")
NODES = "ABCDEF"
MAX_BYTES = 30_000_000


def build_summary(path: Path) -> dict:
    summary = {
        "record_type": "aggregate_snapshot_inspection",
        "scope": "preserved_local_snapshot; not a live runtime test",
        "method": "read-only local inspection of fixed archive members",
        "node_database_counts": {},
        "ledger_counts": {},
        "content_manifest": {},
        "interpretive_limits": [
            "SQL table row counts are not independent reasoning-stream counts.",
            "Historical document claims are not validated by these aggregates alone.",
            "Log entry counts do not establish successful processing or causal behavior.",
            "No restart, multi-node execution, cryptographic trust, or live changed-only ingestion test was performed.",
        ],
    }
    with zipfile.ZipFile(path) as archive:
        for node in NODES:
            name = f"node/db_lattice/NODE_{node}_matrix.db"
            info = archive.getinfo(name)
            if info.file_size > MAX_BYTES:
                raise ValueError("Database exceeds allowed size")
            db_bytes = archive.read(name)
            db = sqlite3.connect(":memory:")
            try:
                db.deserialize(db_bytes)
                db.execute("PRAGMA query_only=ON")
                counts = {}
                present = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                for table in TABLE_NAMES:
                    if table in present:
                        counts[table] = int(db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0])
                summary["node_database_counts"]["NODE_"+node] = counts
            finally:
                db.close()

        for title, name, expected_type in LOGS:
            info=archive.getinfo(name)
            if info.file_size > MAX_BYTES:
                raise ValueError("Log exceeds allowed size")
            records = [json.loads(line) for line in archive.read(name).decode('utf-8').splitlines() if line.strip()]
            if not all(isinstance(r, dict) for r in records):
                raise ValueError("Unexpected log schema")
            summary["ledger_counts"][title] = {
                "entries": len(records),
                "unique_source_paths": len({r.get('path') for r in records if isinstance(r.get('path'),str)}),
                "expected_type_entries": sum(r.get('type') == expected_type for r in records),
            }

        name='node/logs/node_e_content_manifest.json'
        info=archive.getinfo(name)
        if info.file_size > MAX_BYTES:
            raise ValueError("Manifest exceeds allowed size")
        manifest=json.loads(archive.read(name))
        if not isinstance(manifest,dict): raise ValueError("Unexpected manifest schema")
        summary["content_manifest"] = {
            "entries": len(manifest),
            "value_type_counts": dict(sorted(Counter(type(v).__name__ for v in manifest.values()).items())),
        }
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('node_zip',type=Path,help='Local original node.zip (NOT for publication)')
    p.add_argument('--output',type=Path,help='Path to write aggregate-only JSON. Defaults to stdout.')
    a=p.parse_args()
    summary=build_summary(a.node_zip)
    result=json.dumps(summary,sort_keys=True,indent=2)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result,encoding='utf-8')
        print(f'Wrote aggregate-only summary ({len(result.encode("utf-8"))} bytes).')
    else:
        print(result,end='')

if __name__ == '__main__':main()
