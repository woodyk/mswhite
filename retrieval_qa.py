"""
retrieval_qa.py - Hybrid QA over vector embeddings + graph context.
Usage: python retrieval_qa.py "question text"
"""

import subprocess, json, os, numpy as np, networkx as nx, sys
from numpy.linalg import norm

GRAPH_FILE = "knowledge_graph.json"
EMB_FILE = "embeddings.json"

def embed(text):
    # call host_adapter to get 10-dim vec
    resp = subprocess.check_output(["python","host_adapter.py", f"Generate a 10-dim numeric embedding (comma separated) for: {text}"], text=True)
    return np.array([float(x) for x in resp.strip().split(",")[:10]])

def top_k_nodes(query_vec, k=5):
    if not os.path.exists(EMB_FILE):
        return []
    emb = json.load(open(EMB_FILE))
    sims=[]
    for node, vec in emb.items():
        v=np.array(vec)
        sim=float(np.dot(query_vec,v)/(norm(query_vec)*norm(v)+1e-9))
        sims.append((sim,node))
    sims.sort(reverse=True)
    return [n for _,n in sims[:k]]

def build_context(nodes):
    if not os.path.exists(GRAPH_FILE):
        return ""
    G=nx.read_gjson(GRAPH_FILE)
    ctx=[]
    for n in nodes:
        neigh=list(G.neighbors(n))
        ctx.append(f"{n}: {'; '.join(neigh)}")
    return "\\n".join(ctx)

def main():
    if len(sys.argv)<2:
        print("Provide a question.")
        return
    q=" ".join(sys.argv[1:])
    qvec=embed(q)
    nodes=top_k_nodes(qvec)
    context=build_context(nodes)
    prompt=f"Context:\\n{context}\\nQuestion: {q}"
    answer=subprocess.check_output(["python","host_adapter.py", prompt], text=True)
    print("Answer:",answer.strip())

if __name__=="__main__":
    main()
