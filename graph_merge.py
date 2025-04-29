"""
graph_merge.py - Merge peer knowledge graphs with semantic union.
"""

import networkx as nx, os, json

GRAPH_FILE = "knowledge_graph.json"
PEER_DIR = "federation_incoming_graphs"

def merge_graphs():
    G = nx.read_gjson(GRAPH_FILE) if os.path.exists(GRAPH_FILE) else nx.Graph()
    if not os.path.isdir(PEER_DIR):
        return
    for fname in os.listdir(PEER_DIR):
        try:
            H = nx.read_gjson(os.path.join(PEER_DIR, fname))
            G = nx.compose(G, H)
        except:
            pass
    nx.write_gjson(G, GRAPH_FILE)
    print("[OK] Graphs merged.")

if __name__ == "__main__":
    merge_graphs()
