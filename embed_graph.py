import networkx as nx, subprocess, json, os
import gjson

GRAPH_FILE = "knowledge_graph.json"
EMB_FILE = "embeddings.json"

def embed(text):
    prompt = f"Give only 10 comma-separated floats for this embedding: {text}"
    out = subprocess.check_output(["python", "host_adapter.py", prompt], text=True)
    import re
    vals = [float(x) for x in re.findall(r"-?\d+\.\d+", out)[:10]]
    return vals

def main():
    if not os.path.exists(GRAPH_FILE):
        print("[ERR] No graph file.")
        return
    G = gjson.read(GRAPH_FILE)
    emb = {}
    for node in G.nodes():
        emb[node] = embed(node)
    with open(EMB_FILE, "w") as f:
        json.dump(emb, f, indent=2)
    print(f"[OK] Saved embeddings for {len(emb)} nodes.")

if __name__ == "__main__":
    main()
