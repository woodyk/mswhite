"""
consensus_client.py - Resolve conflicts after federation merges based on policy.
Usage:
  python consensus_client.py
"""

import yaml
import json
import os
from datetime import datetime

CONFIG = "consensus_config.yaml"
MEMORY_FILE = "memory.json"
FEDS_DIR = "federation_incoming"  # directory where peer memories are stored

def load_config():
    return yaml.safe_load(open(CONFIG, 'r'))

def load_memory(path):
    if os.path.exists(path):
        return json.load(open(path, 'r'))
    return {}

def save_memory(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def last_write_wins_merge(local, peers):
    # Each peer dict has 'timestamp' and memory dict
    entries = {}
    # local base entries with timestamp '1970'
    for key, val in local.items():
        entries[key] = {'value': val, 'timestamp': '1970-01-01T00:00:00Z'}
    # apply peer updates
    for peer in peers:
        mem = peer.get('memory', {})
        ts = peer.get('timestamp', '1970-01-01T00:00:00Z')
        for k, v in mem.items():
            # if newer timestamp, replace
            if ts > entries.get(k, {}).get('timestamp', ''):
                entries[k] = {'value': v, 'timestamp': ts}
    return {k: entries[k]['value'] for k in entries}

def host_priority_merge(local, peers, priority_list):
    merged = local.copy()
    for host in priority_list:
        for peer in peers:
            if peer.get('host') == host:
                merged.update(peer.get('memory', {}))
    # then others
    for peer in peers:
        if peer.get('host') not in priority_list:
            merged.update(peer.get('memory', {}))
    return merged

def main():
    cfg = load_config()
    policy = cfg.get('merge_policy')
    local_mem = load_memory(MEMORY_FILE)
    # gather peers' memory snapshots
    peers = []
    if os.path.isdir(FEDS_DIR):
        for fname in os.listdir(FEDS_DIR):
            path = os.path.join(FEDS_DIR, fname)
            try:
                peer_data = json.load(open(path))
                peers.append(peer_data)
            except:
                pass
    # select merge
    if policy == 'last_write_wins':
        merged = last_write_wins_merge(local_mem, peers)
    else:
        merged = host_priority_merge(local_mem, peers, cfg.get('host_priority', []))
    save_memory(MEMORY_FILE, merged)
    print(f"[OK] Consensus merge using policy '{policy}' applied.")

if __name__ == "__main__":
    main()
