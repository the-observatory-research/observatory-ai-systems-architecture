## ZPP - Buffer Proxy Handler

zpp_id: buffer_proxy_handler
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-07-01

---

```python

#!/usr/bin/env python3
import os
import json
import time
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
import requests

OBSERVATORY_LOG = "/Users/<LOCAL_USER>/vault/ledger/observatory_proxy.txt"
LOCAL_OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
LOCAL_MODEL = "llama3:8b-instruct-q4_0"

def write_zpp_proxy_log(status_state, target_model, request_body, response_body):
    """Generates a structured ZPP-compliant telemetry entry for the proxy observatory."""
    try:
        os.makedirs(os.path.dirname(OBSERVATORY_LOG), exist_ok=True)
        timestamp_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        unix_ts = int(time.time())
        deterministic_seed = f"{unix_ts}_{status_state}_{target_model}"
        zpp_id = f"zpp_tx_{hashlib.md5(deterministic_seed.encode()).hexdigest()[:12]}"
        
        zpp_packet = [
            f"zpp_id: {zpp_id}",
            "schema_version: zpp.entropy.char.nfc.v1",
            "lineage_tracking: zpp-core-mainnet",
            f"status: {status_state}",
            "origin_node: local_buffer_proxy_gateway",
            f"timestamp: {timestamp_iso}",
            "\n## Head",
            f"* **Target Endpoint:** Local Ollama Instance",
            f"* **Target Model:** {target_model}",
            f"* **Network UNIX Epoch:** {unix_ts}",
            f"* **Route State Lock:** LOCAL_HARDWARE_LOOP",
            "\n## Body",
            "### Inbound Pipeline Ingress Stream:",
            f"```json\n{request_body}\n```",
            "\n### Upstream Model Egress Matrix:",
            f"```markdown\n{response_body}\n```",
            "\n" + "─" * 60 + "\n"
        ]
        
        with open(OBSERVATORY_LOG, "a") as f:
            f.write("\n".join(zpp_packet))
    except Exception as e:
        print(f"⚠️ [ZPP LEDGER WRITE ERROR]: {e}")

class LocalProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read the local format request payload from pipeline_horizon.py
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        local_payload = json.loads(post_data.decode('utf-8'))
        
        # Ensure the payload points to the local model instance
        local_payload["model"] = LOCAL_MODEL
        
        print(f"📡 Routing core request directly to Local Ollama Engine [{LOCAL_MODEL}]...")
        
        try:
            # 2. Ship to local Ollama instance over the internal OpenAI compatibility route
            headers = {"Content-Type": "application/json"}
            response = requests.post(LOCAL_OLLAMA_URL, headers=headers, json=local_payload, timeout=300)
            
            if response.status_code == 200:
                ollama_json = response.json()
                
                # Extract text out of Ollama's OpenAI array schema safely
                choices = ollama_json.get("choices", [])
                if choices:
                    ai_text = choices[0].get("message", {}).get("content", "⚠️ Empty content parsed.")
                else:
                    ai_text = "⚠️ Error parsing response choices sequence."
                
                # 3. Re-structure response to the format pipeline_horizon expects
                simulated_local_response = {
                    "message": {
                        "role": "assistant",
                        "content": ai_text
                    },
                    "done": True
                }
                
                # Write tracking details safely to your telemetry log file
                write_zpp_proxy_log("SYNC_COMPLETE", LOCAL_MODEL, json.dumps(local_payload, indent=2), ai_text)
                
                # Send processed content back down the framework wire to Kai
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(simulated_local_response).encode('utf-8'))
                print("✨ Local sync complete. Matrix updated.")
                
            else:
                error_msg = f"Local Ollama Engine Error: Status {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                write_zpp_proxy_log("LOCAL_API_ERROR", LOCAL_MODEL, json.dumps(local_payload, indent=2), error_msg)
                self.send_error(response.status_code, error_msg)
                
        except Exception as e:
            error_msg = f"Local Runtime Exception: {str(e)}"
            print(f"⚠️ {error_msg}")
            write_zpp_proxy_log("LOCAL_ENGINE_DISCONNECTED", LOCAL_MODEL, json.dumps(local_payload, indent=2), error_msg)
            self.send_error(502, error_msg)

    def log_message(self, format, *args):
        # Mute standard HTTP server logs to prevent screen clutter
        return

def run_proxy():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, LocalProxyHandler)
    print("🛡️ Local Buffer Proxy Operational [ROUTE: LOCALHOST:8080 ──> LOCAL OLLAMA]")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Local Proxy...")
        httpd.server_close()

if __name__ == '__main__':
    run_proxy()
    ```