"""
embed_graph.py - Generate vector embeddings for graph nodes using host_adapter.
Stores embeddings in embeddings.json {node: [vector]}.
"""

import json, networkx as nx, subprocess, os, numpy as np

GRAPH_FILE = "knowledge_graph.json"
EMB_FILE = "embeddings.json"

def embed_text(text: str):
    # Use host_adapter to get embedding-like representation (simple: use LLM to output 10 floats)
    prompt = f"Generate a 10-dim numeric embedding (comma separated) for: {text}"
    response = subprocess.check_output(["python", "host_adapter.py", prompt], text=True)
    try:
        vec = [float(x) for x in response.strip().split(",")[:10]]
    except:
        vec = [0.0]*10
    return vec

def main():
    if not os.path.exists(GRAPH_FILE):
        print("Graph missing. Run knowledge_graph.py first.")
        return
    G = nx.read_gjson(GRAPH_FILE)
    embeddings = {}
    for node in G.nodes:
        embeddings[node] = embed_text(node)
    json.dump(embeddings, open(EMB_FILE,"w"), indent=2)
    print(f"[OK] {len(embeddings)} embeddings stored.")

if __name__ == "__main__":
    main()
