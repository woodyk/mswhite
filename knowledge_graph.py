"""
knowledge_graph.py - Build and merge semantic knowledge graphs using networkx.
"""

import json, networkx as nx, os

GRAPH_FILE = "knowledge_graph.json"

def ensure_graph():
    if not os.path.exists(GRAPH_FILE):
        nx.write_gjson(nx.Graph(), GRAPH_FILE)

def load_graph(path=GRAPH_FILE):
    return nx.read_gjson(path) if os.path.exists(path) else nx.Graph()

def save_graph(G, path=GRAPH_FILE):
    nx.write_gjson(G, path)

def ingest_memory(memory_path="memory.json"):
    mem = json.load(open(memory_path))
    G = load_graph()
    for k, v in mem.items():
        G.add_node(k, type="key")
        if isinstance(v, list):
            for item in v:
                node = str(item)
                G.add_node(node, type="value")
                G.add_edge(k, node)
        else:
            node = str(v)
            G.add_node(node, type="value")
            G.add_edge(k, node)
    save_graph(G)

if __name__ == "__main__":
    ensure_graph()
    ingest_memory()
