"""
federation_client.py - Multi-agent collaboration: exchange expansions and memory merges.
Usage:
  python federation_client.py exchange  # push local expansions & memory to peers
  python federation_client.py merge     # fetch peers' expansions & memory, merge locally
"""

import argparse, os, yaml, requests, json

CONFIG = "federation_config.yaml"
EXP_DIR = "expansions"
MEMORY_FILE = "memory.json"

def load_config():
    return yaml.safe_load(open(CONFIG, 'r'))

def send_exchange(peer, payload):
    url = peer["url"].rstrip('/') + payload["exchange_endpoint"]
    try:
        files = {
            "expansions": ("expansions.tar", open("expansions.tar", "rb")),
            "memory": ("memory.json", open(MEMORY_FILE, "rb"))
        }
        resp = requests.post(url, files=files, timeout=10)
        return resp.status_code == 200
    except:
        return False

def pack_expansions():
    import tarfile
    with tarfile.open("expansions.tar", "w") as tar:
        tar.add(EXP_DIR, arcname=os.path.basename(EXP_DIR))

def exchange():
    cfg = load_config()
    pack_expansions()
    payload = {"exchange_endpoint": cfg.get("exchange_endpoint", "/exchange_soul")}
    for peer in cfg.get("peers", []):
        ok = send_exchange(peer, payload)
        print(f"[{'OK' if ok else 'ERR'}] exchange with {peer['url']}")

def merge():
    cfg = load_config()
    for peer in cfg.get("peers", []):
        try:
            url = peer["url"].rstrip('/') + "/soulpack/expansions.tar"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                import tarfile, io
                tar = tarfile.open(fileobj=io.BytesIO(r.content))
                tar.extractall(EXP_DIR)
                print(f"[OK] merged expansions from {peer['url']}")
            # memory merge
            if cfg.get("merge_memory"):
                mem_url = peer["url"].rstrip('/') + "/soulpack/memory.json"
                r2 = requests.get(mem_url, timeout=10)
                if r2.status_code == 200:
                    peer_mem = json.loads(r2.text)
                    local_mem = json.load(open(MEMORY_FILE))
                    # simple merge: extend lists
                    for k in peer_mem:
                        if isinstance(local_mem.get(k), list) and isinstance(peer_mem[k], list):
                            local_mem[k].extend(x for x in peer_mem[k] if x not in local_mem[k])
                    json.dump(local_mem, open(MEMORY_FILE, "w"), indent=2)
                    print(f"[OK] merged memory from {peer['url']}")
        except Exception as e:
            print(f"[ERR] merging from {peer['url']}: {e}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["exchange","merge"])
    args = p.parse_args()
    if args.command == "exchange":
        exchange()
    else:
        merge()

if __name__ == "__main__":
    main()
