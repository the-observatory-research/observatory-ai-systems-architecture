#!/usr/bin/env python3
"""
Zero-Point Protocol — Cryptographic Fluid Agent Node
100% Standalone Build. Fully inline internet and Ollama reasoning cores.
"""
import sys
import asyncio
import json
import re
import urllib.parse
import aiohttp
import websockets
import traceback
import os
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "vendor")
)

from ddgs import DDGS

from pulse import AsynchronousPulse

from scoring import GammaScorer
from evaluation import EvaluationResult
from memory import MemoryLattice
from crypto import CryptoEngine
from datetime import datetime, timezone

DISCOVERY_MARKERS = [
    "SLA",
    "ZPP",
    "Gamma",
    "coherence",
    "lattice",
    "Horizon",
    "Zero-Point Protocol",
    "Source-Locked Architecture",
    "SCI",
]

class CryptographicAgentNode:
    def __init__(self, node_id: str, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        self.peers = peers

        # Runtime fluid weight parameters
        self.cluster_weights = {
            "NODE_A": 0.33,
            "NODE_B": 0.33,
            "NODE_C": 0.34
        }

        self.election_epoch = 0
        self.execution_sequence = 0
        self.discovery_sequence = 0
        self.bridge_sequence = 0

        if node_id in ["NODE_A", "NODE_B", "NODE_C"]:
            self.current_state = "VALIDATOR_READY"

        elif node_id in ["NODE_D", "D"]:
            self.current_state = "DISCOVERY_IDLE"

        elif node_id in ["NODE_E", "E"]:
            self.current_state = "BRIDGE_IDLE"

        elif node_id in ["NODE_F", "F"]:
            self.current_state = "INGRESS_READY"

        else:
            self.current_state = "IDLE"

        self.last_accepted_election_epoch = -1
        self.last_accepted_execution_sequence = -1

        self.weights = {
            "novelty": 0.25,
            "entropy": 0.20,
            "self_reference": 0.15,
            "paradox": 0.25,
            "coherence": 0.15,
        }

        # Localized engine modules
        self.scorer = GammaScorer(weights=self.weights)
        self.lattice = MemoryLattice(f"db_lattice/{node_id}_matrix.db", node_id)
        self.pulse = AsynchronousPulse(
            memory_lattice=self.lattice,
            state_getter=lambda: self.current_state
        )

        # Serial processing queue locks for Node F (Protects Ollama from VRAM crashes)
        self.reasoning_lock = asyncio.Lock() if node_id in ["F", "NODE_F"] else None

        # Ed25519 Identity Engine
        self.crypto = CryptoEngine(node_id=node_id, key_directory=Path("./keys"))
        print(f"[{self.node_id}] Cryptographic Identity Locked: {self.crypto.get_public_key_fingerprint()}")

    async def start(self):
        async with websockets.serve(
            self.handle_incoming,
            "localhost",
            self.port
        ):
            print(
                f"[{self.node_id}] "
                f"Mesh socket listening on port {self.port}"
            )

            await self.connect_to_mesh()

            asyncio.create_task(
                self.pulse.start_metronome(
                    interval_seconds=60.0
                )
            )
            await asyncio.Future()

    async def handle_incoming(self, websocket):
        try:
            async for message in websocket:
                envelope = json.loads(message)

                payload = envelope.get("payload", {})
                signature = envelope.get("signature")
                sender_pubkey = envelope.get("public_key")

                if not payload or not signature or not sender_pubkey:
                    continue

                is_authentic = CryptoEngine.verify_payload_base64(
                    payload,
                    signature,
                    sender_pubkey
                )

                if not is_authentic:
                    print(
                        f"[{self.node_id} Security Alert] "
                        f"Signature verification failed."
                    )
                    continue

                msg_type = payload.get("type")
                sender_id = payload.get("origin_node_id")

                if msg_type == "handshake":
                    print(f"[{self.node_id}] Authenticated peer handshake established with {sender_id}")
                elif msg_type == "fluid_weight_shift":
                    await self.adjust_weights(payload.get("trigger_factors"))
                elif msg_type == "internet_query" and self.node_id in ["NODE_F", "F"]:
                    asyncio.create_task(self.run_gateway_pipeline(payload.get("payload")))
                elif msg_type == "vault_scan_trigger" and self.node_id in ["NODE_D", "D"]:
                    vault_path = payload.get("vault_path", "./vault")
                    asyncio.create_task(self.execute_obsidian_discovery(vault_path))
                elif msg_type == "reasoning_trigger" and self.node_id in ["NODE_F", "F"]:
                    try:
                        text_context = payload.get("text_to_analyze", "")
                        telemetry_context = payload.get("validated_telemetry", "")
                        declared_leader = payload.get("leader")
                        election_epoch = payload.get("election_epoch", -1)
                        execution_sequence = payload.get("execution_sequence", -1)

                        if sender_id != declared_leader:
                            continue

                        if election_epoch < self.last_accepted_election_epoch:
                            continue

                        if execution_sequence <= self.last_accepted_execution_sequence:
                            continue

                        self.last_accepted_election_epoch = election_epoch
                        self.last_accepted_execution_sequence = execution_sequence

                        async def locked_reasoning_task(text, telemetry):
                            async with self.reasoning_lock:
                                self.current_state = "REASONING_ACTIVE"

                                try:
                                    await self.execute_core_reasoning_pipeline(
                                        text,
                                        telemetry
                                    )
                                finally:
                                    self.current_state = "INGRESS_READY"

                        task = asyncio.create_task(
                            locked_reasoning_task(
                                text_context,
                                telemetry_context
                            )
                        )

                        def reasoning_task_done(completed_task):
                            try:
                                completed_task.result()
                            except Exception:
                                print(
                                    f"[NODE_F ERROR] Reasoning task crashed:",
                                    file=sys.stderr
                                )
                                traceback.print_exc()

                        task.add_done_callback(reasoning_task_done)

                    except Exception:
                        print(
                            "[NODE_F ERROR] reasoning_trigger handler crashed:",
                            file=sys.stderr
                        )
                        traceback.print_exc()

                elif msg_type == "bridge_retrieval_request" and self.node_id in ["NODE_E", "E"]:
                    asyncio.create_task(
                        self.execute_bridge_retrieval(payload)
                    )

                elif msg_type == "consensus_broadcast":
                    await self.process_validation(
                        payload.get("text"),
                        sender_id,
                        original_query=payload.get("original_query", "")
                    )

        except websockets.exceptions.ConnectionClosed:
            pass

        except Exception as e:
            print(
                f"[{self.node_id} Error] Inbound handler drop: {e}",
                file=sys.stderr
            )

    async def connect_to_mesh(self):
        for peer_id, url in self.peers.items():
            if peer_id != self.node_id:
                asyncio.create_task(self.maintain_connection(peer_id, url))

    async def maintain_connection(self, peer_id, url):
        while True:
            try:
                async with websockets.connect(url) as ws:
                    handshake_doc = self.crypto.create_anchor_payload(
                        anchor_id="handshake_init", prompt_hash="0", score=0, route="INIT",
                        alpha=0, gamma=0, chain_id="zpp_gamma_mainnet", entry_id=0, prev_hash="0",
                        origin_node_id=self.node_id
                    )
                    handshake_doc["type"] = "handshake"

                    envelope = {
                        "payload": handshake_doc,
                        "signature": self.crypto.sign_payload_base64(handshake_doc),
                        "public_key": self.crypto.get_public_key_text()
                    }
                    await ws.send(json.dumps(envelope))
                    while True:
                        await asyncio.sleep(3600)
            except Exception:
                await asyncio.sleep(1.5)

    async def run_gateway_pipeline(self, target_query: str):
        self.current_state = "SEARCH_ACTIVE"

        print(
            f"\n[NODE_F] Triggering unrestricted JSON API gateway fetch for: "
            f"'{target_query}'"
        )
        import urllib.parse
        encoded_query = urllib.parse.quote(target_query)
        
        # ────────────────────────────────────────────────────────
        # PUBLIC JSON API GATEWAY ROUTE
        # Hits the non-interactive text node. Returns pure JSON, bypassing HTML and captchas.
        # ────────────────────────────────────────────────────────
        gateway_url = (
            f"https://api.duckduckgo.com/"
            f"?q={encoded_query}"
            f"&format=json"
            f"&no_html=1"
            f"&skip_disambig=1"
        )
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(gateway_url, headers=headers, timeout=8) as response:
                    if response.status != 200:
                        raise RuntimeError(f"API Gateway returned HTTP {response.status}")
                    
                    # Parse the incoming stream directly as structural JSON data
                    raw_json = await response.json(content_type=None)
                    
                    # Extract the primary encyclopedia Abstract text or related vector topic strings
                    extracted_text = raw_json.get("AbstractText", "")
                    
                    # Fallback path if Abstract text is empty: harvest the first related topic definition string
                    if not extracted_text and raw_json.get("RelatedTopics"):
                        for topic in raw_json["RelatedTopics"]:
                            if "Text" in topic:
                                extracted_text = topic["Text"]
                                break
                                
                    if not extracted_text:
                        extracted_context = await self.run_serp_fallback(
                            target_query
                        )
                        status_msg = "LIVE_SERP_INGRESS_SUCCESS"

                        print(
                            f"[NODE_F] SERP fallback context acquired. "
                            f"Vector bytes read: {len(extracted_context)}"
                        )
                    else:
                        extracted_context = (
                            f"LIVE_API_CONTEXT: {extracted_text[:4000]}"
                        )
                        status_msg = "LIVE_INTERNET_INGRESS_SUCCESS"

                        print(
                            f"[NODE_F] Public JSON Gateway extraction complete. "
                            f"Vector bytes read: {len(extracted_text)}"
                        )
                    
        except Exception as e:
            # Safe local direct-text bypass fallback loop
            print(f"[NODE_F Warning] API Gateway link dropped ({type(e).__name__}: {e}). Routing direct payload...")
            extracted_context = target_query
            status_msg = "INBOUND_DIRECT_OVERRIDE_COMPLETE"

        # Commit the acquired text data cleanly into our Memory Lattice database file
        await self.lattice.commit_to_field(
            layer="internet_ingress", speaker="Node_F_Core", content=extracted_context,
            metadata={"target_query": target_query, "network_status": status_msg}
        )
        
        # Pull latest record out using proper list indexing variables to prevent script crashes
        context_blocks = await self.lattice.get_volatile_context(limit=1)

        if context_blocks and isinstance(context_blocks, list) and len(context_blocks) > 0:
            latest_text = context_blocks[0]["content"]  # ◄── Index 0 extraction securely verified
            
            broadcast_doc = self.crypto.create_anchor_payload(
                anchor_id="consensus_trigger", prompt_hash=CryptoEngine.hash_prompt(latest_text),
                score=0.4948, route="BETA", alpha=0.0, gamma=0.55, chain_id="zpp_gamma_mainnet",
                entry_id=1, prev_hash="0", origin_node_id=self.node_id
            )
            broadcast_doc["type"] = "consensus_broadcast"
            broadcast_doc["text"] = latest_text
            broadcast_doc["original_query"] = target_query

            envelope = {
                "payload": broadcast_doc,
                "signature": self.crypto.sign_payload_base64(broadcast_doc),
                "public_key": self.crypto.get_public_key_text()
            }

            await self.broadcast_to_validators(envelope)

            self.current_state = "INGRESS_READY"

    async def run_serp_fallback(self, target_query: str):
        """
        Secondary live search ingress.
        Retrieves structured web search results through DDGS when the
        Public JSON Gateway returns no Instant Answer context.
        """

        print(
            f"[NODE_F] Instant Answer empty. "
            f"Activating DDGS search fallback for: '{target_query}'"
        )

        search_results = await asyncio.to_thread(
            lambda: DDGS(timeout=8).text(
                target_query,
                region="us-en",
                safesearch="moderate",
                max_results=5,
                backend="auto"
            )
        )

        if not search_results:
            raise ValueError(
                "DDGS search returned no structured search results."
            )

        context_parts = [
            "LIVE_SEARCH_CONTEXT",
            f"QUERY: {target_query}",
            ""
        ]

        for index, result in enumerate(search_results, start=1):
            title = result.get("title", "")
            url = result.get("href", "")
            snippet = result.get("body", "")

            context_parts.extend([
                f"RESULT_{index}",
                f"TITLE: {title}",
                f"URL: {url}",
                f"SNIPPET: {snippet}",
                ""
            ])

        extracted_context = "\n".join(context_parts)

        print(
            f"[NODE_F] DDGS search extraction complete. "
            f"Structured results acquired: {len(search_results)}"
        )

        return extracted_context

    async def execute_obsidian_discovery(self, root_path_str: str):
        self.current_state = "DISCOVERY_ACTIVE"

        print(f"\n[NODE_D] Mapping internal structure of root repository: '{root_path_str}'")

        discovered_count = 0

        root_dir = Path(root_path_str).expanduser().resolve()
        if not root_dir.exists():
            self.current_state = "DISCOVERY_IDLE"
            return

        detected_vault_paths = []
        garbage_filters = { "node_modules", ".git", ".venv", "env", "db_lattice", "keys", "env3.14" }

        for root, dirs, _ in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in garbage_filters]
            if ".obsidian" in dirs:
                current_vault_path = Path(root)
                if current_vault_path.name == "vault":
                    continue
                detected_vault_paths.append(current_vault_path)
                print(f"   ► [Sub-Vault Registered] Active content matrix: {current_vault_path.name}")

        # Step 2: Read markdown strings exclusively out of verified sub-vaults matching your signatures
        for vault_path in detected_vault_paths:
            for root, dirs, files in os.walk(vault_path):
                for file in files:
                    if file.endswith(".md"):
                        file_path = Path(root) / file
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()

                            content_lower = content.lower()

                            matched_markers = [
                                marker
                                for marker in DISCOVERY_MARKERS
                                if marker.lower() in content_lower
                            ]

                            if matched_markers:
                                print(
                                    f"    ↳ [Signature Matched] "
                                    f"Registering critical matrix: "
                                    f"{vault_path.name} -> "
                                    f"{file.replace('.md', '')}"
                                )

                                discovery_record = {
                                    "type": "discovery_record",
                                    "origin_node_id": self.node_id,
                                    "timestamp": datetime.now(
                                        timezone.utc
                                    ).isoformat(),
                                    "vault": vault_path.name,
                                    "path": str(file_path),
                                    "filename": file,
                                    "markers": matched_markers,
                                }

                                await self.write_discovery_ledger(
                                    discovery_record
                                )
                                await self.lattice.commit_to_field(
                                    layer="discovery",
                                    speaker="NODE_D",
                                    content=str(file_path),
                                    metadata={
                                        "vault": vault_path.name,
                                        "filename": file,
                                        "markers": matched_markers,
                                        "timestamp": discovery_record["timestamp"],
                                    }
                                )
                                await self.send_discovery_to_bridge(
                                    file_path=file_path,
                                    vault_name=vault_path.name,
                                    filename=file,
                                    markers=matched_markers
                                )

                                discovered_count += 1

                        except Exception as e:
                            print(
                                f"[NODE_D Error] Discovery processing failed "
                                f"for {file}: {type(e).__name__}: {e}",
                                file=sys.stderr
                            )

        if discovered_count == 0:
            print(
                "[NODE_D Warning] Sweep complete. "
                "No signature-locked files found in active sub-vaults."
            )
            self.current_state = "DISCOVERY_IDLE"
            return

        print(
            f"[NODE_D] Discovery finalized. "
            f"Registered {discovered_count} authoritative files. "
            f"Bridge handoffs complete."
        )

        self.current_state = "DISCOVERY_IDLE"

    async def write_discovery_ledger(self, record: dict):
        """
        Persist Node D discovery events as an append-only JSONL ledger.
        """

        ledger_path = Path(
            "logs/node_d_discovery_ledger.jsonl"
        )

        ledger_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            ledger_path,
            "a",
            encoding="utf-8"
        ) as ledger:
            ledger.write(
                json.dumps(
                    record,
                    sort_keys=True
                ) + "\n"
            )

    async def send_discovery_to_bridge(
        self,
        file_path: Path,
        vault_name: str,
        filename: str,
        markers: list
    ):
        """
        Sign and transmit a Node D discovery record to Node E.
        """

        path_string = str(file_path)

        self.discovery_sequence += 1

        handoff_doc = self.crypto.create_anchor_payload(
            anchor_id="discovery_handoff",
            prompt_hash=CryptoEngine.hash_prompt(
                path_string
            ),
            score=0.0,
            route="BRIDGE",
            alpha=0.0,
            gamma=0.55,
            chain_id="zpp_gamma_mainnet",
            entry_id=self.discovery_sequence,
            prev_hash="0",
            origin_node_id=self.node_id
        )

        handoff_doc["type"] = "bridge_retrieval_request"
        handoff_doc["source_path"] = path_string
        handoff_doc["vault"] = vault_name
        handoff_doc["filename"] = filename
        handoff_doc["markers"] = markers

        envelope = {
            "payload": handoff_doc,
            "signature": self.crypto.sign_payload_base64(
                handoff_doc
            ),
            "public_key": self.crypto.get_public_key_text()
        }

        try:
            async with websockets.connect(
                self.peers["NODE_E"]
            ) as ws:
                await ws.send(
                    json.dumps(envelope)
                )

            print(
                f"[NODE_D] Signed discovery handoff sent "
                f"to NODE_E: {filename}"
            )

        except Exception as e:
            print(
                f"[NODE_D Error] Bridge handoff failed "
                f"for {filename}: {e}"
            )

    def load_content_manifest(self) -> dict:
        """
        Load Node E's persistent content-hash manifest.
        Returns an empty manifest if none exists yet.
        """
        manifest_path = Path(
            "logs/node_e_content_manifest.json"
        )

        if not manifest_path.exists():
            return {}

        try:
            with open(
                manifest_path,
                "r",
                encoding="utf-8"
            ) as manifest_file:
                return json.load(manifest_file)

        except Exception as e:
            print(
                f"[NODE_E Warning] Content manifest load failed: {e}"
            )
            return {}


    def save_content_manifest(self, manifest: dict):
        """
        Persist Node E's content-hash manifest atomically enough
        for normal single-process bridge operation.
        """
        manifest_path = Path(
            "logs/node_e_content_manifest.json"
        )

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


    def classify_content_change(
        self,
        manifest: dict,
        file_path: Path,
        content_hash: str
    ) -> str:
        """
        Return one of:
        NEW
        MODIFIED
        UNCHANGED
        """
        path_key = str(
            file_path.expanduser().resolve()
        )

        previous_record = manifest.get(
            path_key
        )

        if previous_record is None:
            return "NEW"

        previous_hash = previous_record.get(
        "content_hash"
        )

        if previous_hash == content_hash:
            return "UNCHANGED"

        return "MODIFIED"

    async def execute_bridge_retrieval(self, payload: dict):
        self.current_state = "BRIDGE_ACTIVE"

        """
        Node E bridge retrieval pipeline.
        Reads a file discovered by Node D, persists a retrieval ledger,
        and forwards the content to the validator cluster.
        """

        source_path = payload.get("source_path", "")
        vault_name = payload.get("vault", "")
        filename = payload.get("filename", "")
        markers = payload.get("markers", [])

        if not source_path:
            print("[NODE_E Warning] Bridge request missing source_path.")
            self.current_state = "BRIDGE_IDLE"
            return

        file_path = Path(source_path).expanduser().resolve()

        if not file_path.exists() or not file_path.is_file():
            print(
                f"[NODE_E Warning] Bridge source unavailable: {file_path}"
            )
            self.current_state = "BRIDGE_IDLE"
            return

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:
                content = f.read()

        except Exception as e:
            print(
                f"[NODE_E Error] Retrieval failed for "
                f"{filename}: {e}"
            )
            self.current_state = "BRIDGE_IDLE"
            return

        content_hash = CryptoEngine.hash_prompt(content)

        manifest = self.load_content_manifest()

        change_state = self.classify_content_change(
            manifest=manifest,
            file_path=file_path,
            content_hash=content_hash
        )

        if change_state == "UNCHANGED":
            print(
                f"[NODE_E] Unchanged file skipped: "
                f"{filename}"
            )

            self.current_state = "BRIDGE_IDLE"
            return

        print(
            f"[NODE_E] {change_state} file accepted: "
            f"{filename}"
        )

        await self.lattice.commit_to_field(
            layer="bridge_retrieval",
            speaker="NODE_E",
            content=content,
            metadata={
                "source_path": str(file_path),
                "vault": vault_name,
                "filename": filename,
                "markers": markers,
                "content_hash": content_hash,
                "change_state": change_state,
                "discovered_by": payload.get(
                    "origin_node_id",
                    "NODE_D"
                ),
                "retrieved_by": self.node_id,
            }
        )

        bridge_record = {
            "type": "bridge_record",
            "origin_node_id": self.node_id,
            "discovered_by": payload.get(
                "origin_node_id",
                "NODE_D"
            ),
            "retrieved_by": self.node_id,
            "vault": vault_name,
            "path": str(file_path),
            "filename": filename,
            "markers": markers,
            "content_hash": content_hash,
            "content_length": len(content),
            "change_state": change_state,
        }

        await self.write_bridge_ledger(
            bridge_record
        )

        print(
            f"[NODE_E] Bridge retrieval complete: "
            f"{filename} | Bytes={len(content)}"
        )

        self.bridge_sequence += 1

        bridge_doc = self.crypto.create_anchor_payload(
            anchor_id="bridge_payload",
            prompt_hash=content_hash,
            score=0.0,
            route="VALIDATION",
            alpha=0.0,
            gamma=0.55,
            chain_id="zpp_gamma_mainnet",
            entry_id=self.bridge_sequence,
            prev_hash="0",
            origin_node_id=self.node_id
        )

        bridge_doc["type"] = "consensus_broadcast"
        bridge_doc["text"] = content
        bridge_doc["source_path"] = str(file_path)
        bridge_doc["filename"] = filename
        bridge_doc["vault"] = vault_name
        bridge_doc["markers"] = markers
        bridge_doc["content_hash"] = content_hash
        bridge_doc["discovered_by"] = payload.get(
            "origin_node_id",
            "NODE_D"
        )
        bridge_doc["retrieved_by"] = self.node_id

        envelope = {
            "payload": bridge_doc,
            "signature": self.crypto.sign_payload_base64(
                bridge_doc
            ),
            "public_key": self.crypto.get_public_key_text()
        }

        await self.broadcast_to_validators(
            envelope
        )

        path_key = str(
            file_path.expanduser().resolve()
        )

        manifest[path_key] = {
            "content_hash": content_hash,
            "filename": filename,
            "vault": vault_name,
            "markers": markers,
            "last_change_state": change_state,
            "processed_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        self.save_content_manifest(
            manifest
        )

        self.current_state = "BRIDGE_IDLE"

    async def write_bridge_ledger(self, record: dict):
        """
        Persist Node E retrieval events as an append-only JSONL ledger.
        """

        ledger_path = Path(
            "logs/node_e_bridge_ledger.jsonl"
        )

        ledger_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            ledger_path,
            "a",
            encoding="utf-8"
        ) as ledger:
            ledger.write(
                json.dumps(
                    record,
                    sort_keys=True
                ) + "\n"
            )

    async def execute_core_reasoning_pipeline(
        self,
        context_text: str,
        telemetry_context: str
    ):
        """
        Inline Asynchronous Local Ollama DeepSeek-R1 Streaming Pipeline.
        Unrestricted Build: Persona wrappers removed to let raw data emergence surface freely.
        """
        print(f"\n[NODE_F Core] Active streaming reasoning pipeline engaged...")
        lattice_history = await self.lattice.get_volatile_context(limit=5)
        history_summary = ""
        if lattice_history:
            history_summary = "\n".join([f"[{h.get('speaker')}] {h.get('content')}" for h in lattice_history])
        
        # ────────────────────────────────────────────────────────
        # PERSHONA REMOVAL OVERRIDE
        # Completely neutral structural directives focused purely on vector utility
        # ────────────────────────────────────────────────────────
        system_instruction = (
            "Answer the USER QUERY directly using the supplied MATRIX and HISTORY. "
            "Treat VALIDATED TELEMETRY as authoritative quantitative measurements and "
            "interpret each metric only according to its provided definition and scale. "
            "Do not recalculate or invent telemetry values. "
            "Separately observe qualitative structural, semantic, and behavioral patterns "
            "present in the supplied material. Keep qualitative observations distinct from "
            "quantitative measurements."
        )

        user_prompt = (
            f"= USER QUERY =\n"
            f"{context_text}\n"
            f"= VALIDATED TELEMETRY =\n"
            f"{telemetry_context}\n"
            f"= HISTORY =\n"
            f"{history_summary}\n"
            f"= MATRIX =\n"
            f"{context_text}"
        )
        
        endpoint = "http://localhost:11434/api/chat"
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
        payload = {
            "model": "deepseek-r1:7b",
            "messages": messages,
            "stream": True,
            "options": {"temperature": 0.4, "num_ctx": 8192}
        }
        
        try:
            print("\n================== DEEPSEEK-R1 RAW COGNITIVE STREAM ==================")
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint, json=payload) as response:
                    if response.status != 200:
                        raise RuntimeError(f"Ollama returned status {response.status}")
                    
                    async for line in response.content:
                        if line:
                            decoded_line = line.decode('utf-8').strip()
                            if not decoded_line:
                                continue
                            try:
                                chunk_json = json.loads(decoded_line)
                                token = chunk_json.get("message", {}).get("content", "")
                                sys.stdout.write(token)
                                sys.stdout.flush()
                            except Exception:
                                pass
            print("\n====================================================================\n")
        except Exception as e:
            print(f"[NODE_F Core Error] Streaming session dropped: {e}")


    async def broadcast_to_validators(self, envelope: dict):
        for peer_id in ["NODE_A", "NODE_B", "NODE_C"]:
            try:
                async with websockets.connect(
                    self.peers[peer_id]
                ) as ws:
                    await ws.send(
                        json.dumps(envelope)
                    )

            except Exception as e:
                print(
                    f"[{self.node_id} Error] "
                    f"Broadcast failed to {peer_id}: {e}"
                )

    async def process_validation(
        self,
        text: str,
        origin: str,
        original_query: str = ""
    ):
        self.current_state = "VALIDATING"

        context = await self.lattice.get_volatile_context(limit=3)

        res = self.scorer.evaluate(
            text,
            context=context
        )

        telemetry_context = (
            "VALIDATED TELEMETRY — applies to the complete MATRIX payload:\n"
            f"Gamma: {res.gamma_score}\n"
            f"Novelty: {res.novelty} (lexical breadth)\n"
            f"Entropy: {res.entropy} (normalized character entropy)\n"
            f"Self-Reference: {res.self_reference} (lexical self-reference matches)\n"
            f"Paradox: {res.paradox} (lexical paradox-pattern matches)\n"
            f"Coherence: {res.coherence} (recent-context token overlap)\n"
        )

        print(f"[{self.node_id} Validator] Securely verified message from {origin}")
        print(
            f"    ↳ Gamma: {res.gamma_score} | "
            f"Novelty: {res.novelty} | "
            f"Entropy: {res.entropy} | "
            f"Self-Reference: {res.self_reference} | "
            f"Paradox: {res.paradox} | "
            f"Coherence: {res.coherence}"
        )
        
        # Real-time fluid balance shifts to fight semantic drift
        imbalance_delta = abs(res.coherence - res.entropy)
        if imbalance_delta > 0.15:
            self.cluster_weights["NODE_C"] = min(0.60, self.cluster_weights["NODE_C"] + 0.02)
            remaining = 1.0 - self.cluster_weights["NODE_C"]
            self.cluster_weights["NODE_A"] = remaining / 2
            self.cluster_weights["NODE_B"] = remaining / 2

            self.election_epoch += 1

            print(f"[{self.node_id}] Continuous weight tuning executed -> {self.cluster_weights}")

        await self.lattice.commit_to_field(layer="conversation", speaker=origin, content=text)

        # ────────────────────────────────────────────────────────
        # THE SINGLE-LEADER GATING LOGIC
        # ────────────────────────────────────────────────────────
        cluster_state = {
            "epoch": self.election_epoch,
            "weights": self.cluster_weights.copy(),
        }

        leader_node = max(
            cluster_state["weights"],
            key=lambda node: (
                cluster_state["weights"][node],
                node
            )
        )

        print(
            f"[{self.node_id}] Leader={leader_node} | "
            f"Election Epoch={cluster_state['epoch']}"
        )
        
        if res.gamma_score >= 0.40:
            if self.node_id == leader_node:
                self.current_state = "LEADER_ACTIVE"
                self.execution_sequence += 1

                # Only the elected cluster leader is permitted to sign and dispatch the order
                print(
                    f"[{self.node_id}] !CLUSTER LEADER DISPATCH ACTIVE! "
                    f"Sending clean 1x reasoning trigger to Core..."
                )

                execution_doc = self.crypto.create_anchor_payload(
                    anchor_id="reasoning_relay",
                    prompt_hash=CryptoEngine.hash_prompt(text),
                    score=res.gamma_score,
                    route="GAMMA",
                    alpha=0.0,
                    gamma=0.55,
                    chain_id="zpp_gamma_mainnet",
                    entry_id=77,
                    prev_hash="0",
                    origin_node_id=self.node_id
                )

                execution_doc["type"] = "reasoning_trigger"
                execution_doc["text_to_analyze"] = text
                execution_doc["validated_telemetry"] = telemetry_context
                execution_doc["leader"] = leader_node
                execution_doc["election_epoch"] = cluster_state["epoch"]
                execution_doc["execution_sequence"] = self.execution_sequence
                execution_doc["original_query"] = original_query

                envelope = {
                    "payload": execution_doc,
                    "signature": self.crypto.sign_payload_base64(execution_doc),
                    "public_key": self.crypto.get_public_key_text()
                }
                try:
                    async with websockets.connect(self.peers["NODE_F"]) as ws:
                        await ws.send(json.dumps(envelope))
                except Exception:
                    pass

                self.current_state = "VALIDATOR_READY"

            else:
                # Non-leader validators log verification silently to prevent 3x cluttering
                print(f"[{self.node_id}] Consensus verified. Deferring network execution to elected Leader node: {leader_node}")

    async def adjust_weights(self, factors: dict):
        if factors.get("paradox", 0) > 0.6:
            self.weights["paradox"] = min(0.50, self.weights["paradox"] + 0.05)
            self.scorer = GammaScorer(weights=self.weights)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    node_id_arg = sys.argv[1]
    port_arg = int(sys.argv[2])

    peer_config = {
        "NODE_A": "ws://localhost:8000", "NODE_B": "ws://localhost:8001", "NODE_C": "ws://localhost:8002",
        "NODE_D": "ws://localhost:8003", "NODE_E": "ws://localhost:8004", "NODE_F": "ws://localhost:8005",
    }

    node = CryptographicAgentNode(node_id_arg, port_arg, peer_config)
    asyncio.run(node.start())
