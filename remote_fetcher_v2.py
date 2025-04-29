"""
remote_fetcher_v2.py - Secure download & signature verify for SOULPACK expansions.
Requires: cryptography
"""

import yaml, requests, os, hashlib, base64, sys
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

PUBKEY_PATH = "pubkey.pem"
SRC_PATH = "remote_sources.yaml"
EXP_DIR = "expansions"

def load_pubkey():
    with open(PUBKEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def sha256sum(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

def fetch():
    if not os.path.exists(SRC_PATH):
        print("[INFO] no remote_sources.yaml")
        return
    pb = load_pubkey()
    manifest = yaml.safe_load(open(SRC_PATH))
    os.makedirs(EXP_DIR, exist_ok=True)
    for mod in manifest.get("sources", []):
        dest = os.path.join(EXP_DIR, os.path.basename(mod["url"]))
        if os.path.exists(dest):
            continue
        try:
            data = requests.get(mod["url"], timeout=10).content
            sig  = requests.get(mod["sig"], timeout=10).content
            # verify ed25519 signature
            pb.verify(sig, data)
            with open(dest, "wb") as f:
                f.write(data)
            exp_manifest_path = os.path.join(EXP_DIR, "manifest.yaml")
            exp_mani = yaml.safe_load(open(exp_manifest_path)) if os.path.exists(exp_manifest_path) else {"modules":[]}
            exp_mani["modules"].append({"id": mod["id"], "type": mod["type"], "file": os.path.basename(dest), "description": "remote signed"})
            yaml.safe_dump(exp_mani, open(exp_manifest_path,"w"))
            print(f"[OK] fetched & verified {mod['id']}")
        except Exception as e:
            print(f"[ERR] failed {mod['id']}: {e}")

if __name__ == "__main__":
    fetch()
