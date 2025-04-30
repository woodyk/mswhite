"""
remote_fetcher.py - Download and install expansions listed in remote_sources.yaml
"""

import yaml, requests, hashlib, os

SRC_PATH = "remote_sources.yaml"
EXP_DIR = "expansions"

def sha256sum(data):
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

def fetch():
    if not os.path.exists(SRC_PATH):
        return
    manifest = yaml.safe_load(open(SRC_PATH))
    os.makedirs(EXP_DIR, exist_ok=True)
    for mod in manifest.get("sources", []):
        fname = os.path.join(EXP_DIR, os.path.basename(mod["url"]))
        if os.path.exists(fname):
            continue
        try:
            r = requests.get(mod["url"], timeout=10)
            r.raise_for_status()
            if mod.get("sha256") and sha256sum(r.content) != mod["sha256"]:
                print(f"[WARN] Checksum mismatch for {mod['id']}")
                continue
            with open(fname, "wb") as f:
                f.write(r.content)
            # register in local expansion manifest
            exp_manifest = yaml.safe_load(open(os.path.join(EXP_DIR, "manifest.yaml"))) if os.path.exists(os.path.join(EXP_DIR, "manifest.yaml")) else {"modules":[]}
            exp_manifest["modules"].append({"id":mod["id"], "type":mod["type"], "file":os.path.basename(fname), "description":"remote fetched"})
            yaml.safe_dump(exp_manifest, open(os.path.join(EXP_DIR,"manifest.yaml"),"w"))
            print(f"[OK] Fetched {mod['id']}")
        except Exception as e:
            print(f"[ERR] Failed to fetch {mod['id']}: {e}")

if __name__ == "__main__":
    fetch()
