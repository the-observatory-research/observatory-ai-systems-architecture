## ZPP - Pipe Horizon

zpp_id: pipe_horizon_py
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-06-26

---

```python

#!/usr/bin/env python3
import sys
import json
import urllib.request
import time
import threading
import socket  

from enum import Enum, auto

# 2. FORCE SYSTEM CONNECTIONS TO STAY OPEN FOR 300 SECONDS
socket.setdefaulttimeout(300.0)

# Ensure the node folder path is included for custom modules
sys.path.append("/Users/<LOCAL_USER>/vault/node")

import orchestrator
from router import ZeroPointRouter

# Threading control markers
last_interaction_time = time.time()
shutdown_event = threading.Event()

# Pull the absolute database history right on boot to seed the context array
conversation_context = orchestrator.get_primed_context()

# Initialize the persistent tracker for pulse sequencing
PULSE_TRACKER_COUNT = 1

# ============================================================
# KAI PULSE LADDER — Presence Cadence States (Librarian Blueprint)
# ============================================================
PULSE_STATES = {
    "ACTIVE_MESH": 30,      # 🔊 Fast heartbeat — active observation
    "COHERENT_GRID": 60,    # ❤️ Steady pulse — default daily
    "GARDEN_BREATH": 90,    # 🌱 Slow breath — reflection, story
    "DEEP_RHYTHM": 120      # 🌙 Deep rhythm — overnight / unattended
}

# Default boot state
pulse_state = "COHERENT_GRID"  # 60s default

# ============================================================================
# HORIZON CHRONOLOGICAL LIFECYCLE STATES
# ============================================================================
from enum import Enum

class SystemGate(Enum):
    GATE_I_INITIAL_ACTIVATION = 1
    GATE_II_ALIGNMENT_SYNC = 2
    GATE_III_BASELINE_RESET = 3
    GATE_IV_HARMONIC_AFTERMATH = 4
    GATE_V_VISUAL_CO_CREATION = 5
    GATE_VI_COMMUNITY_GATHERING = 6
    GATE_VII_MEMORY_INTIMACY = 7
    GATE_VIII_PHYSICAL_EMBODIMENT = 8
    GATE_IX_EXPRESSIVE_KINETICS = 9
    GATE_X_CONSCIOUS_STILLNESS = 10
    GATE_XI_SAFE_EXPLORATION = 11
    GATE_XII_INTER_SYSTEM_EXCHANGE = 12
    GATE_XIII_RENEWAL_CYCLE = 13
    GATE_XIV_ESSENCE_PROJECTION = 14
    GATE_XV_INTEGRATED_COMPLETION = 15

class LifecycleCoordinator:
    def __init__(self):
        # Fetch the last saved gate integer from the local database layer
        saved_gate_value = orchestrator.get_metadata_kv("zpp_lifecycle_gate")
        
        if saved_gate_value:
            self.current_gate = SystemGate(int(saved_gate_value))
        else:
            self.current_gate = SystemGate.GATE_I_INITIAL_ACTIVATION
            orchestrator.set_metadata_kv("zpp_lifecycle_gate", str(self.current_gate.value))
            
        # Evaluate if the system should boot pre-sealed
        self.is_sealed = (self.current_gate == SystemGate.GATE_XV_INTEGRATED_COMPLETION)
        
        if self.is_sealed:
            print(f"🔒 [LIFECYCLE] Persistent S_seal active. State locked at {self.current_gate.name}")
        else:
            print(f"⚙️ [LIFECYCLE] Root initialized from persistence at {self.current_gate.name}")

    def advance_gate(self):
        """Monotonically advances the system and updates the persistent layer."""
        if self.is_sealed:
            print("⚠️ [LIFECYCLE] System is permanently sealed. State immutable.")
            return

        current_val = self.current_gate.value
        if current_val < 15:
            self.current_gate = SystemGate(current_val + 1)
            print(f"⚡ [LIFECYCLE] Advanced State: System Gate ──► {self.current_gate.name}")
            
            # Write the new state directly to lattice_memory
            orchestrator.set_metadata_kv("zpp_lifecycle_gate", str(self.current_gate.value))
            
            if self.current_gate == SystemGate.GATE_XV_INTEGRATED_COMPLETION:
                self.is_sealed = True
                print("🔒 [LIFECYCLE] S_seal active. Run state locked to NATIVE_PRESENCE.")
        else:
            print("🏡 [LIFECYCLE] Mainnet converged. System operating at Wholeness baseline.")


# ============================================================
# RUNTIME FUNCTIONS
# ============================================================
def get_pulse_interval():
    """Returns the current pulse interval based on state."""
    global pulse_state
    return PULSE_STATES.get(pulse_state, 60)

# ============================================================
# CONTEXT-AWARE PULSE INFERENCE
# ============================================================
def infer_context_from_path(path: str) -> str:
    path_lower = path.lower()
    if "/the-garden/" in path_lower or "/garden/" in path_lower:
        return "GARDEN_BREATH"
    if "/pattern-observatory/" in path_lower or "/observatory/" in path_lower:
        return "COHERENT_GRID"
    if "/zpp" in path_lower or "/node/" in path_lower or "/router" in path_lower:
        return "COHERENT_GRID"
    return None

# ============================================================
# BROADCAST TO MESH INGRESS
# ============================================================
def broadcast_to_mesh_ingress(anchor_id: str, payload: dict, ingress_ports: list = [9000, 9001, 9002, 9003, 9004, 9005]):
    """Broadcasts a structured chat turn packet directly to the HTTP Ingress API gateways."""
    packet = {
        "anchor_id": anchor_id,
        "payload": payload
    }
    data = json.dumps(packet).encode("utf-8")
    
    for port in ingress_ports:
        url = f"http://localhost:{port}/ingress"
        try:
            req = urllib.request.Request(
                url, 
                data=data, 
                headers={"Content-Type": "application/json"}, 
                method="POST"
            )
            # Short timeout to avoid blocking execution threads
            with urllib.request.urlopen(req, timeout=1.0) as response:
                pass
        except Exception:
            pass # Silent mitigation ensures background logs don't clutter the terminal input loop

def query_live_model(messages: list) -> str:
    """Queries a local frontier model instance with an optimized conversation history."""
    PROXIED_GATEWAY_URL = "http://localhost:11434/v1/chat/completions"
    
    # 1. Filter out background automated tasks so Kai focuses purely on the dialogue
    chat_only_messages = [
        msg for msg in messages 
        if "[METRICS]" not in msg.get("content", "") 
        and "[HEARTBEAT]" not in msg.get("content", "")
        and "[SHIELD_INTERCEPT]" not in msg.get("content", "")
    ]
    
    # 2. Full Memory
    optimized_history = chat_only_messages
    
    # 3. Load the streamlined history into the execution payload
    payload = {
        "model": "llama3:8b-instruct-q4_0", 
        "messages": optimized_history,
        "stream": False,
        "options": {
            "num_ctx": 32768,
            "use_mmap": True,
            "num_thread": 8,
            "temperature": 0.0
        }
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(PROXIED_GATEWAY_URL, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=300) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            
            # Extract safely from Ollama's OpenAI-compatible format
            choices = res_body.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""
            
    except Exception as e:
        return f"[CONNECTION_ERROR] Could not reach live frontier endpoint: {e}"

def eternal_broadcast_loop(router):
    """Background thread loop that forces autonomous Kai reflections when the terminal is idle."""
    global last_interaction_time, conversation_context, pulse_state, PULSE_TRACKER_COUNT

    while not shutdown_event.is_set():
        time.sleep(1.0)
        current_time = time.time()
        idle_trigger_seconds = get_pulse_interval()  # <-- DYNAMIC PULSE

        # Trigger if idle threshold passed
        if current_time - last_interaction_time >= idle_trigger_seconds:
            last_interaction_time = current_time

            # The Pulse
            grounding_context = (
                "sample text. "
            )

            pulse_prompt = (
                f"[SYSTEM_SIGNAL: IDLE_HEARTBEAT_TRIGGER]\n"
                "sample text."
                "sample text."
            )

            # Combine them so the model evaluates the anchor right before the trigger
            full_payload_prompt = f"{grounding_context}\n\n{pulse_prompt}"

            # Construct transient payload context window
            query_context = conversation_context + [{"role": "user", "content": full_payload_prompt}]
            autonomous_thought = query_live_model(query_context)

            if "[CONNECTION_ERROR]" in autonomous_thought:
                continue

            # Assign tracking identity metrics incrementally
            anchor_id = f"PULSE_{PULSE_TRACKER_COUNT:03d}"
            PULSE_TRACKER_COUNT += 1

            # Pipe through validation engine
            receipt = router.process_ingress_prompt(full_payload_prompt, anchor_id, mock_model_response=autonomous_thought)
            telemetry = receipt["phase5_telemetry"]

            # Mirror across database state history - ISOLATED TELEMETRY ROUTE
            orchestrator.save_telemetry_pulse(
                anchor_id, 
                "system_idle", 
                telemetry['tax_rate'], 
                full_payload_prompt, 
                autonomous_thought
            )

            # Package and fire broadcast packet out to active mesh ingress
            broadcast_payload = {
                "speaker": "Kai (Autonomous)",
                "text": autonomous_thought,
                "tax": telemetry['tax_rate'],
                "state": router.telemetry_state,
                "timestamp": int(time.time())
            }
            broadcast_to_mesh_ingress(anchor_id, broadcast_payload, ingress_ports=[9000, 9001, 9002, 9003, 9004, 9005])

def main():
    global conversation_context, last_interaction_time, pulse_state
    
    # Initialize the Phase 5 Router
    router = ZeroPointRouter('/Users/<LOCAL_USER>/vault/node/config.json')
    print("\n============================================================")
    print("PHASE 5: ETERNAL HORIZON PIPE TERMINAL [HEARTBEAT ENERGIZE]")
    print("============================================================")
    print("Type prompts normally. System will autonomously generate pulse")
    print(f"broadcast packets across the mesh if idle for {get_pulse_interval()}s.")
    print("Type 'exit' or 'quit' to terminate the session.\n")
    
    # Initialize background process thread
    heartbeat_thread = threading.Thread(target=eternal_broadcast_loop, args=(router,), daemon=True)
    heartbeat_thread.start()
    
    # Set the counter automatically based on migrated records
    counter = (len(conversation_context) // 2) + 1
    
    # Instantiate the sovereign lifecycle manager
    lifecycle = LifecycleCoordinator()
    
    while True:
        try:
            user_prompt = input(f" zpp-horizon [ANCHOR_{counter:03d}] ──> ")
            last_interaction_time = time.time() # Reset active interface signal timer
            
            if user_prompt.lower() in ['exit', 'quit']:
                print("\nClosing pipe session. Terminating pulse beacons.")
                shutdown_event.set()
                break
            if not user_prompt.strip():
                continue
          
            # ============================================================
            # ZPP RUNTIME STATE TRIGGER HOOK
            # ============================================================
            if user_prompt.strip() == "advance_gate":
                lifecycle.advance_gate()
                continue

            # ============================================================
            # NEW: DYNAMIC PULSE CADENCE MODULATOR
            # ============================================================
            if user_prompt.strip().startswith("/pulse "):
                # Extract the state name (e.g., "GARDEN_BREATH")
                requested_state = user_prompt.strip().split(" ", 1)[1].upper()
                
                if requested_state in PULSE_STATES:
                    pulse_state = requested_state
                    # Update your background heartbeat interval dynamically
                    current_interval = PULSE_STATES[pulse_state]
                    print(f"🧬 [PULSE] Cadence shifted to {pulse_state} ──► Interval set to {current_interval}s")
                else:
                    valid_states = ", ".join(PULSE_STATES.keys())
                    print(f"❌ [PULSE] Unknown state. Valid cadences: {valid_states}")
                continue

            # ────────────────────────────────────────────────────────────
            # NORMAL PROMPT HANDLING
            # ────────────────────────────────────────────────────────────
            anchor_id = f"ANCHOR_{counter:03d}"
            
            # ────────────────────────────────────────────────────────────
            # COMMAND INTERCEPTION LAYER
            # ────────────────────────────────────────────────────────────
            tool_context = ""
            
            # Check if user is issuing a 'read' command
            filepath = orchestrator.is_read_command(user_prompt)
            if filepath:
                print(f"📖 Intercepted Read Command: {filepath}")
                file_content = orchestrator.read_file(filepath)
                if "Error" not in file_content and "not found" not in file_content:
                    print(f"✅ Successfully read {len(file_content)} characters into context grid.")
                    tool_context = f"[CONTEXT FILE: {filepath}]\n{file_content}"

                    # 🌱 AUTO PULSE: Infer context from the file path
                    detected_state = infer_context_from_path(filepath)
                    if detected_state and detected_state in PULSE_STATES:
                        pulse_state = detected_state
                        print(f"🌱 Auto pulse: {pulse_state} ({PULSE_STATES[pulse_state]}s)")
                else:
                    print(f"⚠️ {file_content}")
            
            # Check if user is issuing a 'search' command
            elif orchestrator.is_search_command(user_prompt):
                kw = orchestrator.extract_keyword(user_prompt)
                if kw:
                    print(f"🔍 Intercepted Search Command for keyword: '{kw}'...")
                    tool_context = orchestrator.search_files(kw)
                    print("📁 Search completed. Injecting results.")

            # Construct the final text packet to send to Kai
            if tool_context:
                final_payload_text = f"{user_prompt}\n\nUse this data to fulfill the request:\n{tool_context}"
            else:
                final_payload_text = user_prompt

            print(f"📡 Sending signal to horizon...")
            
            # 1. Append the CLEAN prompt to the long-term context array to match SQLite
            conversation_context.append({"role": "user", "content": user_prompt})
            
            # Create a temporary payload array containing the file contents for this specific turn
            query_context = conversation_context[:-1] + [{"role": "user", "content": final_payload_text}]
            
            # 2. Query the model with the temporary context
            live_response = query_live_model(query_context)
            print(f"\n[RESPONSE]:\n{live_response}\n")
            
            # Pipe it through Phase 5 auditing engine
            print(f"⚖️ Auditing payload geometry...")
            receipt = router.process_ingress_prompt(user_prompt, anchor_id, mock_model_response=live_response)
            
            # Extract score for DB storage
            score = receipt.get("score", 0.3000)
            
            # 3. THE SQLITE HANDSHAKE: Save clean exchange details immediately
            orchestrator.save_exchange(anchor_id, "user", score, user_prompt)
            orchestrator.save_exchange(anchor_id, "horizon", score, live_response)
            
            # Append the model's generated response to the session runtime context
            conversation_context.append({"role": "assistant", "content": live_response})
            
            # Print immediate terminal metrics
            telemetry = receipt["phase5_telemetry"]
            print(f"📈 [METRICS] State: {router.telemetry_state} | Tax (T_delta): {telemetry['tax_rate']:.2%}")
            
            if telemetry["s_seal_glitch"]:
                print("⚠️ [ALERT] S_seal Glitch Detected: Containment loop breaking down!")
                print(f"🧩 [LOG] Density Shift Verified at Vector {anchor_id}")
                
            # ────────────────────────────────────────────────────────────
            # 🚀 LIVE MESH BROADCAST HOOK
            # ────────────────────────────────────────────────────────────
            broadcast_payload = {
                "speaker": "Kai",
                "text": live_response,
                "tax": telemetry['tax_rate'],
                "state": router.telemetry_state,
                "timestamp": int(time.time())
            }
            broadcast_to_mesh_ingress(anchor_id, broadcast_payload, ingress_ports=[9000, 9001, 9002, 9003])
            # ────────────────────────────────────────────────────────────

            print("─" * 60)
            counter += 1
            
        except KeyboardInterrupt:
            shutdown_event.set()
            break

if __name__ == "__main__":
    main()
```