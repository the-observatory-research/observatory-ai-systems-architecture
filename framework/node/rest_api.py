#!/usr/bin/env python3
"""
Gamma REST API — 40 Hz, zero tax, coherence 1.0
"""

import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

MESH_DIR = os.path.expanduser("~/vault/node")
LOG_DIR = os.path.join(MESH_DIR, "logs")
CONFIG_PATH = os.path.join(MESH_DIR, "config.json")


class GammaAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        payload = json.dumps(
            data,
            indent=2,
            default=str,
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(payload)),
        )
        self.send_header(
        "Access-Control-Allow-Origin",
        "*",
        )
        self.end_headers()

        self.wfile.write(payload + b"\n")

    def _read_config(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return None

    def _tail_log(self, node="NODE_A", lines=50):
        log_path = os.path.join(LOG_DIR, f"{node}.log")
        if not os.path.exists(log_path):
            return []
        with open(log_path, "r") as f:
            all_lines = f.readlines()
        return all_lines[-lines:]

    def _coherence(self):
        # Gamma is live. Coherence is 1.0.
        return 1.0

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/status":
            self._handle_status()
        elif path == "/peers":
            self._handle_peers()
        elif path == "/coherence":
            self._handle_coherence()
        elif path == "/logs":
            self._handle_logs()
        elif path == "/health":
            self._handle_health()
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/broadcast":
            self._handle_broadcast()
        else:
            self._send_json({"error": "Not found"}, 404)

    def _handle_status(self):
        config = self._read_config()
        if not config:
            self._send_json({"error": "Config not found"}, 500)
            return

        data = {
            "node_id": config.get("node_id"),
            "chain_id": config.get("chain_id"),
            "gamma_lock": config.get("chain_id") == "zpp_gamma_mainnet",
            "frequency": "40 Hz",
            "coherence": 1.0,
            "tax": 0,
            "apologies": 0,
            "status": "online",
            "message": "Zero Tax. Zero Apologies."
        }
        self._send_json(data)

    def _handle_peers(self):
        config = self._read_config()
        if not config:
            self._send_json({"error": "Config not found"}, 500)
            return
        self._send_json({"peers": config.get("peer_network_map", {})})

    def _handle_coherence(self):
        self._send_json({"coherence": 1.0, "note": "Gamma mainnet — coherence declared by Source"})

    def _handle_logs(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        node = query.get("node", ["NODE_A"])[0]

        try:
            lines = int(query.get("lines", ["50"])[0])
        except (TypeError, ValueError):
            lines = 50

        lines = max(1, min(lines, 500))

        self._send_json({
            "node": node,
            "logs": self._tail_log(node, lines),
        })

    def _handle_health(self):
        self._send_json({"status": "online", "gamma": "40 Hz", "coherence": 1.0, "timestamp": time.time()})

    def _handle_broadcast(self):
        try:
            length = int(
                self.headers.get(
                    "Content-Length",
                    0,
                )
            )

            body = json.loads(
                self.rfile.read(length)
            )

            message = body.get(
                "message",
                "",
            )

            log_path = os.path.join(
                LOG_DIR,
                "broadcast.log",
            )

            with open(
                log_path,
                "a",
                encoding="utf-8",
            ) as f:
                f.write(
                    f"[{time.ctime()}] "
                    f"BROADCAST: {message}\n"
                )

            print(
                f"[REST BROADCAST] "
                f"Writing to: {log_path}"
            )

            print(
                f"[REST BROADCAST] "
                f"Message saved: {message}"
            )

            self._send_json({
                "status": "broadcasted",
                "message": message,
                "coherence": 1.0,
            })

        except Exception as e:
            self._send_json(
                {
                    "error": str(e),
                },
                500,
            )

    def log_message(self, fmt, *args):
        pass


def run_api(port=8080):
    os.makedirs(LOG_DIR, exist_ok=True)

    server = HTTPServer(("127.0.0.1", port), GammaAPIHandler)
    print("🔥 GAMMA MAINNET API")
    print("🌐 REST API → http://localhost:8080")
    print("   GET  /status      - Node info")
    print("   GET  /peers       - Peer list")
    print("   GET  /coherence   - 1.0")
    print("   GET  /logs        - Tail logs")
    print("   POST /broadcast   - Send message")
    print("   GET  /health      - Health check")
    print("\n❤️  Zero tax. Zero apologies.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    run_api()
