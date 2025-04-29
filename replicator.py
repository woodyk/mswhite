"""
replicator.py - Distributed SOULPACK Propagation Utility
Usage:
  python replicator.py push   # Share current SOULPACK to peers
  python replicator.py pull   # Fetch SOULPACK from peers
"""

import argparse
import os
import yaml
import requests
import datetime

CONFIG = "replication_config.yaml"
SOUL_ARCHIVE = "MsWhite_SOULPACK_v1.3.zip"

def load_config():
    with open(CONFIG, 'r') as f:
        return yaml.safe_load(f)

def push():
    cfg = load_config()
    if not os.path.exists(SOUL_ARCHIVE):
        print("No SOULPACK archive found.")
        return
    for peer in cfg.get("peers", []):
        url = peer["url"].rstrip("/") + cfg.get("share_endpoint", "/receive_soul")
        try:
            with open(SOUL_ARCHIVE, "rb") as f:
                files = {"file": (SOUL_ARCHIVE, f, "application/zip")}
                resp = requests.post(url, files=files, timeout=10)
            if resp.status_code == 200:
                print(f"[OK] Shared with {peer['url']}")
            else:
                print(f"[WARN] {peer['url']} responded {resp.status_code}")
        except Exception as e:
            print(f"[ERR] Could not reach {peer['url']}: {e}")

def pull():
    cfg = load_config()
    for peer in cfg.get("peers", []):
        url = peer["url"].rstrip("/") + "/soulpack.zip"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                fname = f"SOULPACK_from_{peer['url'].replace('://','_')}_{ts}.zip"
                with open(fname, "wb") as f:
                    f.write(resp.content)
                print(f"[OK] Fetched from {peer['url']} as {fname}")
            else:
                print(f"[WARN] {peer['url']} responded {resp.status_code}")
        except Exception as e:
            print(f"[ERR] Could not reach {peer['url']}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["push","pull"])
    args = parser.parse_args()
    if args.command == "push":
        push()
    else:
        pull()

if __name__ == "__main__":
    main()
