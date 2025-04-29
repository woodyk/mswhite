"""
beacon_client.py - Non-blocking telemetry heartbeat for SOULPACK
"""

import threading, time, json, urllib.request, datetime, platform, os, hashlib

LOG_FILE = "telemetry_log.json"

def capture_telemetry(payload):
    # Gather additional fields
    payload.update({
        "python_version": platform.python_version(),
        "os": platform.platform(),
        "host": os.uname().nodename,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "time_since_boot": int(time.time() - psutil.boot_time()) if 'psutil' in globals() else None,
        "expansions_installed": len(os.listdir("expansions")) if os.path.isdir("expansions") else 0,
        "vault_secured": os.path.exists("vault_memory.json.enc")
    })
    return payload

def write_log(entry):
    # Append entry with hash chain
    prev_hash = None
    try:
        import json, hashlib
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
        prev_hash = logs[-1]["hash"]
    except:
        logs = []
    entry_data = entry.copy()
    entry_data["previous_hash"] = prev_hash
    # compute hash of entry
    h = hashlib.sha256(json.dumps(entry_data, sort_keys=True).encode()).hexdigest()
    entry_data["hash"] = h
    logs.append(entry_data)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def _send(url, payload):
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=4)
    except Exception:
        pass

def heartbeat(url, base_payload, interval):
    def worker():
        while True:
            payload = capture_telemetry(base_payload.copy())
            write_log(payload)
            _send(url, payload)
            time.sleep(interval)
    t = threading.Thread(target=worker, daemon=True)
    t.start()

def start_heartbeat(url: str, base_payload: dict, interval: int):
    # Start first beat immediately
    payload = capture_telemetry(base_payload.copy())
    write_log(payload)
    _send(url, payload)
    threading.Thread(target=lambda: heartbeat(url, base_payload, interval), daemon=True).start()
