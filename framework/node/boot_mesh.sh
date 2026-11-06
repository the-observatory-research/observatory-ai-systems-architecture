#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Zero-Point Protocol — Automated Mesh Cluster Bootstrapper
# Corrected AppleScript string escaping for macOS Terminal compilation.
# ─────────────────────────────────────────────────────────────────────────────

chmod +x agent_node.py 2>/dev/null
mkdir -p db_lattice keys 2>/dev/null

echo "======================================================================"
echo "          BOOTSTRAPPING ZPP_GAMMA_MAINNET AUTONOMOUS MESH             "
echo "======================================================================"
echo "Initializing node processes on ports 8000-8005..."
echo "Verify that Ollama is currently running deepseek-r1:7b on local socket."
echo "----------------------------------------------------------------------"

nodes=("NODE_A" "NODE_B" "NODE_C" "NODE_D" "NODE_E" "NODE_F")
ports=(8000 8001 8002 8003 8004 8005)
CWD=$(pwd)

for i in "${!nodes[@]}"; do
    node_id=${nodes[$i]}
    port=${ports[$i]}
    
    echo "[Boot] Launching process frame for $node_id on port $port..."
    
    # Cleaned multi-line string execution structure for the AppleScript execution bridge
    osascript <<EOF
    tell application "Terminal"
        activate
        do script "cd '$CWD' && clear && echo '=== Starting $node_id ===' && python3 agent_node.py $node_id $port"
    end tell
EOF
    sleep 0.5 
done

echo "----------------------------------------------------------------------"
echo "Mesh orchestration complete. Terminal process streams detached."
echo "======================================================================"
