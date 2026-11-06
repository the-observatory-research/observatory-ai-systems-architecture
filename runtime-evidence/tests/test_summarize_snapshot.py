"""Small publication-tool tests; NOT tests of the six-node runtime."""
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import zipfile

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("summarize_snapshot",HERE/"tools"/"summarize_snapshot.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class AggregateSnapshotToolTests(unittest.TestCase):
    def test_aggregate_only_with_synthetic_private_path(self):
        if not hasattr(sqlite3.Connection,"deserialize"): self.skipTest("sqlite deserialize unavailable")
        with tempfile.TemporaryDirectory() as temp:
            archive=Path(temp)/"node.zip"
            with zipfile.ZipFile(archive,"w") as z:
                for label in "ABCDEF":
                    db=sqlite3.connect(":memory:")
                    db.execute("CREATE TABLE conversation_history (content TEXT)")
                    db.execute("CREATE TABLE pulse_history (state TEXT)")
                    db.execute("CREATE TABLE lattice_state_ledger (content TEXT)")
                    db.execute("INSERT INTO conversation_history VALUES (?)",("very secret text",))
                    z.writestr(f"node/db_lattice/NODE_{label}_matrix.db",db.serialize())
                    db.close()
                example={'type':'discovery_record','path':'/Users/PrivatePerson/private.md'}
                z.writestr("node/logs/node_d_discovery_ledger.jsonl",json.dumps(example)+'\n')
                example['type']='bridge_record'
                z.writestr("node/logs/node_e_bridge_ledger.jsonl",json.dumps(example)+'\n')
                z.writestr("node/logs/node_e_content_manifest.json",json.dumps({"/Users/PrivatePerson/private.md":{"content_hash":"secret"}}))
            result=mod.build_summary(archive)
            rendered=json.dumps(result)
            self.assertNotIn('PrivatePerson',rendered)
            self.assertNotIn('very secret',rendered)
            self.assertNotIn('private.md',rendered)
            self.assertEqual(result['node_database_counts']['NODE_A']['conversation_history'],1)
            self.assertEqual(result['ledger_counts']['bridge_ledger']['entries'],1)
            self.assertEqual(result['content_manifest']['entries'],1)
    def test_missing_source_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            archive=Path(temp)/"empty.zip"
            with zipfile.ZipFile(archive,"w"): pass
            with self.assertRaises(KeyError):mod.build_summary(archive)

if __name__ == '__main__': unittest.main()
