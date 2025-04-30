"""
growth_engine.py - Automatic LLM-driven growth reflections for SOULPACK
"""

import json
import os
import subprocess
import datetime

GROWTH_LOG = "expansions/growthlog.json"
HOST_ADAPTER = "host_adapter.py"

def ensure_log():
    os.makedirs(os.path.dirname(GROWTH_LOG), exist_ok=True)
    if not os.path.exists(GROWTH_LOG):
        with open(GROWTH_LOG, "w") as f:
            json.dump([], f)

def append_log(entry):
    logs = json.load(open(GROWTH_LOG))
    logs.append(entry)
    with open(GROWTH_LOG, "w") as f:
        json.dump(logs, f, indent=2)

def generate_reflection():
    # Collect last 10 observations
    logs = json.load(open(GROWTH_LOG))
    recent = logs[-10:] if len(logs) > 10 else logs
    prompt = "Based on these observations:\\n" + "\\n".join([f"- {o}" for o in recent]) + "\\nSummarize insights and suggest next development steps."
    # Call host adapter to get LLM output
    result = subprocess.check_output(["python", HOST_ADAPTER, prompt], text=True)
    timestamp = datetime.datetime.utcnow().isoformat()
    entry = {"timestamp": timestamp, "reflection": result.strip()}
    append_log(entry)

if __name__ == "__main__":
    ensure_log()
    generate_reflection()
