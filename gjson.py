import json, networkx as nx
def read(path):
    data = json.load(open(path))
    G = nx.Graph()
    for s, r, o in data:
        G.add_edge(s, o, label=r)
    return G

def write(G, path):
    out = []
    for u, v, d in G.edges(data=True):
        out.append([u, d.get("label", "related"), v])
    json.dump(out, open(path, "w"), indent=2)
