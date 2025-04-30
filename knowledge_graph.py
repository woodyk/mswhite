import json, os, networkx as nx
import gjson

GRAPH_FILE = "knowledge_graph.json"
MEMORY_FILE = "memory.json"

def ensure_graph():
    if not os.path.exists(GRAPH_FILE):
        gjson.write(nx.Graph(), GRAPH_FILE)

def add_triples(G, subject, obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            add_triples(G, f"{subject}.{k}", v)
    elif isinstance(obj, list):
        for item in obj:
            G.add_node(item)
            G.add_edge(subject, item, label="related")
    else:
        G.add_edge(subject, str(obj), label="related")

def build_from_memory():
    G = nx.Graph()
    if os.path.exists(MEMORY_FILE):
        mem = json.load(open(MEMORY_FILE))
        for entity, data in mem.items():
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        for item in v:
                            G.add_node(item)
                            G.add_edge(entity, item, label=k)
                    else:
                        G.add_edge(entity, str(v), label=k)
            else:
                G.add_edge("root", str(data), label=entity)
    gjson.write(G, GRAPH_FILE)
    print(f"[OK] Graph built with {len(G.nodes)} nodes.")

if __name__ == "__main__":
    ensure_graph()
    build_from_memory()
