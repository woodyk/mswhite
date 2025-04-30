import json, os, networkx as nx
import gjson

GRAPH_FILE = "knowledge_graph.json"
MEMORY_FILE = "memory.json"

def ensure_graph():
    if not os.path.exists(GRAPH_FILE):
        gjson.write(nx.Graph(), GRAPH_FILE)

def build_from_memory():
    G = nx.Graph()
    if os.path.exists(MEMORY_FILE):
        mem = json.load(open(MEMORY_FILE))
        for k, v in mem.items():
            if isinstance(v, list):
                for item in v:
                    G.add_node(item)
                    G.add_edge(k, item, label="related")
            else:
                G.add_edge(k, str(v), label="related")
    gjson.write(G, GRAPH_FILE)
    print(f"[OK] Graph built with {len(G.nodes)} nodes.")

if __name__ == "__main__":
    ensure_graph()
    build_from_memory()
