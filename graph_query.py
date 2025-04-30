"""
graph_query.py - Simple CLI to query knowledge_graph.json.
Usage: python graph_query.py "search term"
"""

import sys, json, networkx as nx, os

GRAPH_FILE = "knowledge_graph.json"

def search(term):
    if not os.path.exists(GRAPH_FILE):
        print("No knowledge graph yet. Run knowledge_graph.py first.")
        return
    G = nx.read_gjson(GRAPH_FILE)
    matches = [n for n in G.nodes if term.lower() in n.lower()]
    for m in matches:
        print(f"Node: {m}")
        print("  Connections:", list(G.neighbors(m)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please supply a search term.")
    else:
        search(sys.argv[1])
