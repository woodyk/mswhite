import subprocess, json, os, numpy as np, networkx as nx, sys, re
from numpy.linalg import norm
import gjson

GRAPH_FILE = "knowledge_graph.json"
EMB_FILE = "embeddings.json"

def embed(text):
    prompt = f"Give only 10 comma-separated floats for this embedding: {text}"
    resp = subprocess.check_output(["python","host_adapter.py", prompt], text=True)
    nums = re.findall(r"-?\d+\.\d+", resp)
    return np.array([float(x) for x in nums[:10]])

def top_k_nodes(query_vec, k=5):
    if not os.path.exists(EMB_FILE):
        print("[WARN] No embeddings.json found.")
        return []
    emb = json.load(open(EMB_FILE))
    if not emb:
        print("[WARN] embeddings.json is empty.")
        return []
    sims = []
    for node, vec in emb.items():
        v = np.array(vec)
        sim = float(np.dot(query_vec, v) / (norm(query_vec)*norm(v) + 1e-9))
        sims.append((sim, node))
    sims.sort(reverse=True)
    return [n for _, n in sims[:k]]

def build_context(nodes):
    if not os.path.exists(GRAPH_FILE): return ""
    G = gjson.read(GRAPH_FILE)
    ctx = []
    for n in nodes:
        neigh = list(G.neighbors(n))
        ctx.append(f"{n}: {'; '.join(neigh)}")
    return "\n".join(ctx)

def main():
    if len(sys.argv)<2:
        print("Provide a question.")
        return
    q = " ".join(sys.argv[1:])
    qvec = embed(q)
    nodes = top_k_nodes(qvec)
    context = build_context(nodes)
    prompt = f"Context:\n{context}\nQuestion: {q}"
    answer = subprocess.check_output(["python", "host_adapter.py", prompt], text=True)
    print("Answer:", answer.strip())

if __name__ == "__main__":
    main()
