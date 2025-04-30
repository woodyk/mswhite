import gjson, os
from collections import defaultdict

GRAPH_FILE = "knowledge_graph.json"

def suggest_rules():
    if not os.path.exists(GRAPH_FILE):
        print("[ERR] Missing knowledge_graph.json")
        return

    G = gjson.read(GRAPH_FILE)
    rel_by_subject = defaultdict(lambda: defaultdict(set))

    for u, v, d in G.edges(data=True):
        rel = d.get("label", "related")
        rel_by_subject[u][rel].add(v)

    for subject, rels in rel_by_subject.items():
        for rel, targets in rels.items():
            if len(targets) > 1:
                print(f"→ Candidate Rule: IF ({subject}, {rel}, ?X) AND ({subject}, {rel}, ?Y) THEN (?X, related, ?Y)")

if __name__ == "__main__":
    suggest_rules()
